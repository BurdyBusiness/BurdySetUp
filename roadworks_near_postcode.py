#!/usr/bin/env python3
"""
roadworks_app.py

A single-file Streamlit app: find National Highways road/lane closures
within X miles of a UK postcode, store new results in Supabase, and browse
everything you've collected.

Data source: National Highways "Road and Lane Closures" API v2.0 (DATEX II)
  https://developer.data.nationalhighways.co.uk/api-details#api=road-and-lane-closures-v2

You need a free subscription key from that developer portal, plus a
Supabase project (URL + API key). Provide these in the sidebar, or via
.streamlit/secrets.toml / environment variables:
    NH_API_KEY, SUPABASE_URL, SUPABASE_KEY

Run with:
    streamlit run roadworks_app.py

No secrets are hardcoded here. This file is safe to make public (GitHub,
Streamlit Community Cloud, etc.) -- all credentials come from the sidebar,
secrets.toml, or environment variables.
"""
import hashlib
import json
import math
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

import requests
import streamlit as st

POSTCODES_IO = "https://api.postcodes.io/postcodes/"
NH_BASE = "https://api.data.nationalhighways.co.uk/roads/v2.0/closures"


def get_secret(name):
    """Look up a credential from (in order): the OS environment, or --
    if running inside Streamlit -- st.secrets (populated from secrets.toml).
    """
    val = os.environ.get(name)
    if val:
        return val
    try:
        return st.secrets.get(name)
    except Exception:
        return None


def secrets_diagnostics():
    """Report exactly what get_secret() can see, so a missing/misplaced
    secrets.toml is obvious instead of silently falling through to None."""
    report = {"error": None, "secrets_file_loaded": False, "keys_in_secrets": [], "found": {}}
    try:
        keys = list(st.secrets.keys())
        report["secrets_file_loaded"] = True
        report["keys_in_secrets"] = keys
    except Exception as e:
        report["error"] = f"{type(e).__name__}: {e}"
    for name in ("NH_API_KEY", "SUPABASE_URL", "SUPABASE_KEY"):
        report["found"][name] = bool(get_secret(name))
    return report


# --------------------------------------------------------------------------
# Postcode -> lat/lon
# --------------------------------------------------------------------------
def geocode_postcode(postcode):
    url = POSTCODES_IO + urllib.parse.quote(postcode.strip())
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        raise ValueError(f"Could not geocode postcode '{postcode}': HTTP {e.code}") from e
    if data.get("status") != 200:
        raise ValueError(f"Could not geocode postcode '{postcode}': {data.get('error')}")
    result = data["result"]
    return result["latitude"], result["longitude"]


# --------------------------------------------------------------------------
# Geometry helpers
# --------------------------------------------------------------------------
def haversine_miles(lat1, lon1, lat2, lon2):
    r = 3958.8  # earth radius, miles
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def parse_pos_list(pos_list_str):
    """posList is a space-separated list of 'lat lon lat lon ...' (WGS84)."""
    nums = [float(n) for n in pos_list_str.split()]
    return list(zip(nums[0::2], nums[1::2]))


def _points_from_loc(loc):
    pts = []
    linear = loc.get("locLinearLocation")
    if linear:
        gml = linear.get("gmlLineString", {}).get("locGmlLineString", {})
        pos_list = gml.get("posList")
        if pos_list:
            pts.extend(parse_pos_list(pos_list))
    return pts


def _locs_from_reference(location_reference):
    if not location_reference:
        return []
    grouped = location_reference.get("locLocationGroupByList")
    if grouped:
        return grouped.get("locationContainedInGroup", [])
    return [location_reference]


def extract_points(location_reference):
    """Return list of (lat, lon) points, handling both the single-location
    and multi-location (grouped) schema variants documented for this API."""
    points = []
    for loc in _locs_from_reference(location_reference):
        points.extend(_points_from_loc(loc))
    return points


def extract_road_and_description(location_reference):
    roads = set()
    descs = []
    for loc in _locs_from_reference(location_reference):
        linear = loc.get("locLinearLocation", {})
        supp = linear.get("supplementaryPositionalDescription", {})
        desc = supp.get("locationDescription")
        if desc:
            descs.append(desc)
        single = loc.get("locSingleRoadLinearLocation", {})
        for lw in single.get("linearWithinLinearElement", []):
            code = lw.get("linearElement", {}).get("locLinearElementByCode", {})
            rn = code.get("roadName")
            if rn:
                roads.add(rn)
    road = ", ".join(sorted(roads)) if roads else "Unknown road"
    desc = "; ".join(dict.fromkeys(descs))
    return road, desc


def nearest_point(lat, lon, points):
    """Return (point, distance_miles) for the closest point, or (None, None)."""
    if not points:
        return None, None
    best = min(points, key=lambda p: haversine_miles(lat, lon, p[0], p[1]))
    return best, haversine_miles(lat, lon, best[0], best[1])


def stable_record_id(node, location_ref):
    """Prefer the DATEX II idG (stable across repeated calls). Fall back to a
    deterministic hash of key fields if idG is ever missing."""
    idg = node.get("idG")
    if idg:
        return idg
    basis = json.dumps({
        "loc": location_ref,
        "comment": node.get("generalPublicComment"),
        "validity": node.get("validity"),
    }, sort_keys=True)
    return "hash-" + hashlib.sha256(basis.encode("utf-8")).hexdigest()[:32]


# --------------------------------------------------------------------------
# National Highways API
# --------------------------------------------------------------------------
def fetch_closures(subscription_key, closure_type=None, start=None, end=None,
                    modified_since=None):
    """Yields situationRecord dicts, following pagination via the x-next header."""
    params = {}
    if closure_type:
        params["closureType"] = closure_type
    if start:
        params["startDateTime"] = start
    if end:
        params["endDateTime"] = end
    if modified_since:
        params["modifiedSinceDateTime"] = modified_since

    url = NH_BASE + ("?" + urllib.parse.urlencode(params) if params else "")
    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "X-Response-MediaType": "application/json",
        "X-Data-Format": "DATEXII",
        "Accept": "application/json",
    }

    seen_urls = set()
    while url and url not in seen_urls:
        seen_urls.add(url)
        req = urllib.request.Request(url, headers=headers)

        max_retries = 3
        for attempt in range(max_retries + 1):
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    body = json.load(resp)
                    next_url = resp.headers.get("x-next")
                break
            except urllib.error.HTTPError as e:
                raw = e.read().decode(errors="replace")
                if e.code == 429 and attempt < max_retries:
                    wait = _seconds_to_wait(e, raw)
                    time.sleep(wait)
                    continue
                raise RuntimeError(f"HTTP {e.code} calling National Highways API: {raw}") from e

        payload = body.get("D2Payload", body)
        for situation in payload.get("situation", []):
            for record in situation.get("situationRecord", []):
                yield record

        url = next_url
        if url:
            # Small courtesy pause between pages to avoid re-tripping the limit.
            time.sleep(0.5)


def _seconds_to_wait(http_error, raw_body, default=5):
    """Pull a wait time out of a 429 response: prefer the Retry-After header,
    fall back to parsing '...Try again in N seconds' from the JSON body."""
    retry_after = http_error.headers.get("Retry-After") if http_error.headers else None
    if retry_after:
        try:
            return float(retry_after) + 0.5
        except ValueError:
            pass
    match = re.search(r"(\d+(?:\.\d+)?)\s*seconds?", raw_body)
    if match:
        return float(match.group(1)) + 0.5
    return default


def summarize_record(record, ref_lat, ref_lon, radius_miles, closure_type):
    node = record.get("sitRoadOrCarriagewayOrLaneManagement", record)
    location_ref = node.get("locationReference", {})
    points = extract_points(location_ref)
    best_point, distance = nearest_point(ref_lat, ref_lon, points)
    if distance is None or distance > radius_miles:
        return None

    validity = node.get("validity", {})
    time_spec = validity.get("validityTimeSpecification", {})
    cause = node.get("cause", {})
    comments = node.get("generalPublicComment", [])
    comment_text = "; ".join(c.get("comment", "") for c in comments if c.get("comment"))
    road, desc = extract_road_and_description(location_ref)

    return {
        "record_id": stable_record_id(node, location_ref),
        "closure_type": closure_type,
        "distance_miles": round(distance, 2),
        "road": road,
        "location": desc,
        "status": validity.get("validityStatus"),
        "start_time": time_spec.get("overallStartTime"),
        "end_time": time_spec.get("overallEndTime"),
        "cause": cause.get("causeType"),
        "comment": comment_text,
        "latitude": best_point[0] if best_point else None,
        "longitude": best_point[1] if best_point else None,
    }


# --------------------------------------------------------------------------
# Supabase storage
# --------------------------------------------------------------------------
def to_db_row(summary):
    """Drop fields that are relative to a specific search (not a fixed
    attribute of the closure itself) before writing to Supabase."""
    row = dict(summary)
    row.pop("distance_miles", None)
    return row


def insert_into_supabase(rows, supabase_url, supabase_key, table="road_closures",
                          on_conflict="record_id"):
    """Upsert rows into a Supabase table via PostgREST, relying on a unique
    constraint on `on_conflict` to silently skip rows that already exist.
    Returns (inserted_rows, skipped_count)."""
    if not rows:
        return [], 0

    endpoint = f"{supabase_url.rstrip('/')}/rest/v1/{table}?on_conflict={on_conflict}"
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json",
        # ignore-duplicates -> INSERT ... ON CONFLICT DO NOTHING
        # return=representation -> response body contains only the rows actually inserted
        "Prefer": "resolution=ignore-duplicates,return=representation",
    }
    resp = requests.post(endpoint, headers=headers, json=rows, timeout=30)
    if not resp.ok:
        raise RuntimeError(f"HTTP {resp.status_code} writing to Supabase: {resp.text[:300]}")
    inserted = resp.json()
    skipped = len(rows) - len(inserted)
    return inserted, skipped


def fetch_all_from_supabase(supabase_url, supabase_key, table="road_closures"):
    """Read every row ever stored (the search flow above only inserts)."""
    endpoint = f"{supabase_url.rstrip('/')}/rest/v1/{table}?select=*&order=start_time.desc.nullslast"
    headers = {"apikey": supabase_key, "Authorization": f"Bearer {supabase_key}"}
    resp = requests.get(endpoint, headers=headers, timeout=30)
    if not resp.ok:
        raise RuntimeError(f"HTTP {resp.status_code} reading from Supabase: {resp.text[:300]}")
    return resp.json()


# ==========================================================================
# Streamlit UI
# ==========================================================================
st.set_page_config(page_title="Roadworks Near You", page_icon="🚧", layout="centered")

# Light theming to nod at UK highway signage: motorway blue + hazard amber
st.markdown(
    """
    <style>
        .stApp { background-color: #14171a; }
        .gantry-banner {
            background:#00457c; border-bottom:5px solid #ffb81c;
            padding:18px 22px; border-radius:8px; margin-bottom:18px;
        }
        .gantry-banner h1 { color:#fff; margin:0; font-size:28px; }
        .gantry-banner p { color:#cfe0f0; margin:4px 0 0; font-size:14px; }
        .badge {
            display:inline-block; font-size:11px; font-weight:600; text-transform:uppercase;
            letter-spacing:.4px; padding:3px 8px; border-radius:4px; margin-right:6px;
        }
        .badge-planned { background:#3a2c0d; color:#ffb81c; }
        .badge-unplanned { background:#3d0f14; color:#ff8a94; }
        .badge-distance { background:#00457c; color:#fff; }
        .rw-card {
            border:1px solid #333a42; border-left:5px solid #ffb81c;
            border-radius:8px; padding:12px 16px; margin-bottom:10px; background:#1d2126;
        }
        .rw-card.unplanned { border-left-color:#d0021b; }
        .rw-road { font-size:17px; font-weight:700; color:#eceef0; }
        .rw-meta { font-size:13px; color:#8a93a0; margin-top:4px; line-height:1.5; }
        .rw-comment { font-size:13px; color:#eceef0; margin-top:6px; border-left:2px solid #333a42; padding-left:8px; }
    </style>
    <div class="gantry-banner">
        <h1>🚧 Roadworks Near You</h1>
        <p>National Highways closures, filtered to your postcode and stored in Supabase</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar: connections
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Connections")
    nh_key = st.text_input(
        "National Highways subscription key",
        value=get_secret("NH_API_KEY") or "",
        type="password",
    )
    supabase_url = st.text_input("Supabase URL", value=get_secret("SUPABASE_URL") or "")
    supabase_key = st.text_input(
        "Supabase API key", value=get_secret("SUPABASE_KEY") or "", type="password"
    )
    supabase_table = st.text_input("Supabase table", value="road_closures")
    st.caption(
        "Values here override secrets.toml / environment variables, for this "
        "session only."
    )

    with st.expander("🔧 Secrets diagnostics"):
        diag = secrets_diagnostics()
        if diag["error"]:
            st.error(f"st.secrets could not be read: {diag['error']}")
            st.caption(
                "This usually means Streamlit found no secrets.toml at all. "
                "It looks for `.streamlit/secrets.toml` in the same folder as "
                "this script (and in your current working directory), or "
                "`~/.streamlit/secrets.toml` globally."
            )
        elif not diag["secrets_file_loaded"] or not diag["keys_in_secrets"]:
            st.warning("secrets.toml was found but contains no keys.")
        else:
            st.caption(f"Keys visible in st.secrets: {', '.join(diag['keys_in_secrets'])}")
        for name, ok in diag["found"].items():
            st.write(("✅ " if ok else "❌ ") + name)
        st.caption(
            "If a key shows ❌ here even though it's in your secrets.toml: "
            "double-check the file path, that Streamlit was restarted after "
            "editing it, and that there are no typos in the key names."
        )

# ---------------------------------------------------------------------------
# Search form
# ---------------------------------------------------------------------------
col1, col2 = st.columns([2, 1])
with col1:
    postcode = st.text_input("Postcode", placeholder="e.g. SW1A 1AA")
with col2:
    radius = st.number_input("Radius (miles)", min_value=0.5, value=10.0, step=0.5)

closure_type = st.radio("Closure type", ["both", "planned", "unplanned"], horizontal=True)

with st.expander("Advanced"):
    days_ahead = st.number_input("Days ahead (planned closures)", min_value=1, value=14)
    hours_back = st.number_input("Hours back (unplanned closures)", min_value=1, value=6)

search_col, reload_col = st.columns(2)
search_clicked = search_col.button("🔍 Search", use_container_width=True, type="primary")
reload_clicked = reload_col.button("↻ Reload stored results", use_container_width=True)

if "results" not in st.session_state:
    st.session_state.results = []
if "results_title" not in st.session_state:
    st.session_state.results_title = "Stored results"
if "last_ref" not in st.session_state:
    st.session_state.last_ref = None  # (lat, lon, postcode)

# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------
@st.cache_data(ttl=300, show_spinner=False)
def _cached_fetch_records(nh_key, closure_type, start, end):
    """Materialize fetch_closures() and cache the result for 5 minutes.
    Repeated searches with the same key/type/window (e.g. re-clicking Search
    while testing) reuse this instead of re-hitting the rate-limited API.
    Exceptions are never cached, so a failed call is retried next time."""
    return list(fetch_closures(nh_key, closure_type=closure_type, start=start, end=end))


def _bucketed_now(minutes=5):
    """Round 'now' down to the nearest N-minute mark so that start/end times
    built from it are identical across repeated searches in quick succession,
    which is what makes the cache above actually hit."""
    now = datetime.now(timezone.utc)
    discard = timedelta(minutes=now.minute % minutes, seconds=now.second, microseconds=now.microsecond)
    return now - discard


if search_clicked:
    if not postcode or not radius:
        st.error("Enter both a postcode and a radius.")
    elif not nh_key:
        st.error("Add your National Highways subscription key in the sidebar.")
    else:
        try:
            with st.spinner(f"Looking up {postcode}..."):
                lat, lon = geocode_postcode(postcode)
            st.session_state.last_ref = (lat, lon, postcode)

            types_to_query = ["planned", "unplanned"] if closure_type == "both" else [closure_type]
            now = _bucketed_now()
            results = []

            for i, ctype in enumerate(types_to_query):
                if i > 0:
                    time.sleep(1)  # courtesy pause between closure-type queries

                if ctype == "unplanned":
                    start = (now - timedelta(hours=hours_back)).strftime("%Y-%m-%dT%H:%M:%S")
                    end = now.strftime("%Y-%m-%dT%H:%M:%S")
                else:
                    start = now.strftime("%Y-%m-%dT%H:%M:%S")
                    end = (now + timedelta(days=days_ahead)).strftime("%Y-%m-%dT%H:%M:%S")

                with st.spinner(f"Querying {ctype} closures..."):
                    for record in _cached_fetch_records(nh_key, ctype, start, end):
                        summary = summarize_record(record, lat, lon, radius, ctype)
                        if summary:
                            results.append(summary)

            results.sort(key=lambda r: r["distance_miles"])
            st.session_state.results = results
            st.session_state.results_title = f"Within {radius} mi of {postcode.upper()}"

            if not results:
                st.info(f"No closures found within {radius} miles of {postcode}.")
            else:
                st.success(f"Found {len(results)} closure(s) within {radius} miles.")

        except ValueError as e:
            st.error(str(e))
        except RuntimeError as e:
            st.error(f"National Highways API error: {e}")
            if "HTTP 429" in str(e):
                st.caption(
                    "The app already retries automatically a few times with a "
                    "short wait, but the limit is still being hit. Try again "
                    "in about a minute, or narrow your search (e.g. one "
                    "closure type instead of Both)."
                )
        else:
            # Only attempt to store if the search above succeeded.
            if supabase_url and supabase_key:
                try:
                    with st.spinner("Saving new results to Supabase..."):
                        db_rows = [to_db_row(r) for r in results]
                        inserted, skipped = insert_into_supabase(
                            db_rows, supabase_url, supabase_key, table=supabase_table
                        )
                    st.info(f"Supabase: {len(inserted)} new entries added, {skipped} already stored.")
                except RuntimeError as e:
                    st.error(f"Supabase error: {e}")
                    if "42501" in str(e) or "row-level security" in str(e).lower():
                        st.caption(
                            "Row Level Security is blocking the insert. Either use "
                            "your Supabase **service_role** key (bypasses RLS — keep "
                            "it private), or add an RLS policy on this table allowing "
                            "your key's role to insert, e.g. for the anon role:\n\n"
                            "```sql\n"
                            "create policy \"Allow insert\" on road_closures\n"
                            "  for insert to anon with check (true);\n"
                            "create policy \"Allow select\" on road_closures\n"
                            "  for select to anon using (true);\n"
                            "```"
                        )
            else:
                st.warning("Add Supabase details in the sidebar to save these results.")

# ---------------------------------------------------------------------------
# Reload everything stored in Supabase
# ---------------------------------------------------------------------------
if reload_clicked:
    if not (supabase_url and supabase_key):
        st.error("Add Supabase details in the sidebar first.")
    else:
        try:
            with st.spinner("Loading stored results from Supabase..."):
                rows = fetch_all_from_supabase(supabase_url, supabase_key, supabase_table)

            if st.session_state.last_ref:
                lat, lon, pc = st.session_state.last_ref
                for r in rows:
                    if r.get("latitude") is not None and r.get("longitude") is not None:
                        r["distance_miles"] = round(
                            haversine_miles(lat, lon, r["latitude"], r["longitude"]), 2
                        )
                st.session_state.results_title = f"All stored · distance from {pc.upper()}"
            else:
                st.session_state.results_title = "All stored results"

            st.session_state.results = rows
            st.success(f"Loaded {len(rows)} record(s) from Supabase.")
        except RuntimeError as e:
            st.error(str(e))

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
st.subheader(st.session_state.results_title)

results = st.session_state.results
if not results:
    st.caption("No closures to show yet. Run a search above.")
else:
    m1, m2, m3 = st.columns(3)
    m1.metric("Total", len(results))
    m2.metric("Planned", sum(1 for r in results if r.get("closure_type") == "planned"))
    m3.metric("Unplanned", sum(1 for r in results if r.get("closure_type") == "unplanned"))

    sorted_results = sorted(
        results,
        key=lambda r: r.get("distance_miles") if r.get("distance_miles") is not None else float("inf"),
    )

    for r in sorted_results:
        ctype = r.get("closure_type") or "planned"
        badge_class = "badge-planned" if ctype == "planned" else "badge-unplanned"
        distance_badge = (
            f'<span class="badge badge-distance">{r["distance_miles"]} mi</span>'
            if r.get("distance_miles") is not None
            else ""
        )
        meta_bits = []
        if r.get("status"):
            meta_bits.append(f'<strong>{r["status"]}</strong>')
        if r.get("location"):
            meta_bits.append(r["location"])
        meta_line = " · ".join(meta_bits)
        time_line = ""
        if r.get("start_time") or r.get("end_time"):
            time_line = f'<br>{r.get("start_time") or "?"} → {r.get("end_time") or "ongoing"}'
        cause_line = f'<br>Cause: {r["cause"]}' if r.get("cause") else ""
        comment_html = f'<div class="rw-comment">{r["comment"]}</div>' if r.get("comment") else ""

        st.markdown(
            f"""
            <div class="rw-card {'unplanned' if ctype == 'unplanned' else ''}">
                <div class="rw-road">{r.get('road', 'Unknown road')}</div>
                <div>
                    <span class="badge {badge_class}">{ctype}</span>
                    {distance_badge}
                </div>
                <div class="rw-meta">{meta_line}{time_line}{cause_line}</div>
                {comment_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

st.caption("Data: National Highways Road & Lane Closures API · Geocoding: postcodes.io")
