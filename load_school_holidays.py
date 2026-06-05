"""
school_holidays_full_rebuild.py
═══════════════════════════════════════════════════════════════════════════════
Single script. Run this on your LOCAL machine.

  1. Wipes school_holidays table in Supabase
  2. For every council, tries three sources in order:
       a) GOV.UK page  (gov.uk/school-term-holiday-dates/{slug}) — consistent
          format, covers all 361 councils
       b) Raw text already in the spreadsheet (instant, no fetch needed)
       c) Council's own URL as a final fallback
  3. Deduplicates everything before inserting — can never create duplicates
  4. Prints a clear summary of what succeeded and what still needs attention

Run once. Safe to re-run — always wipes first.

Usage:
    pip install pandas openpyxl requests beautifulsoup4 python-dateutil supabase
    python school_holidays_full_rebuild.py
"""

import os, sys, re, time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from dateutil import parser as dparse
from datetime import timedelta
from collections import defaultdict
from supabase import create_client

# ── Config ─────────────────────────────────────────────────────────────────────

XLSX_PATH = r"C:\Users\user\OneDrive\Documents\Business\BurdySetUp\UK_Councils_Term_Dates_Final_URLs.xlsx"

try:
    import streamlit as st
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_SERVICE_ROLE_KEY"]
except Exception:
    SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
    SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")

if not SUPABASE_URL or not SUPABASE_KEY:
    sys.exit("ERROR: Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-GB,en;q=0.9",
}

DELAY   = 1.0   # seconds between requests — be polite to servers
TIMEOUT = 15

# ── Parser ─────────────────────────────────────────────────────────────────────

DATE_PAT = (
    r"(\d{1,2}(?:st|nd|rd|th)?\s+"
    r"(?:January|February|March|April|May|June|July|"
    r"August|September|October|November|December),?\s*\d{0,4})"
)

HOLIDAY_LABELS = [
    ("Christmas",          r"christmas"),
    ("Easter",             r"easter"),
    ("Summer",             r"summer\s+holida"),
    ("October Half Term",  r"(?:october|autumn)\s+half.term"),
    ("February Half Term", r"(?:february|spring)\s+half.term"),
    ("May Half Term",      r"(?:may|summer)\s+half.term|spring\s+bank"),
    ("Half Term",          r"half.term|half term break|mid.term"),
    ("Term Holiday",       r"term\s+holiday\s+\d"),
]

# (month_start, month_end, min_days, max_days, name)
# Summer restricted to Jul/Aug start to avoid false positives
HOLIDAY_WINDOWS = [
    (10, 10,  5, 14, "October Half Term"),
    (12,  1,  9, 21, "Christmas"),
    ( 2,  2,  5, 14, "February Half Term"),
    ( 3,  4,  9, 21, "Easter"),
    ( 5,  5,  5, 14, "May Half Term"),
    ( 7,  8, 35, 49, "Summer"),
]


def region_for(ons):
    if str(ons).startswith("S"): return "Scotland"
    if str(ons).startswith("W"): return "Wales"
    if str(ons).startswith("N"): return "Northern Ireland"
    return "England"


def classify_gap(gap_start, gap_end):
    span = (gap_end - gap_start).days + 1
    m = gap_start.month
    for mo_s, mo_e, mn, mx, name in HOLIDAY_WINDOWS:
        in_month = (mo_s <= m <= mo_e) if mo_s <= mo_e else (m >= mo_s or m <= mo_e)
        if in_month and mn <= span <= mx:
            return name
    return None


def try_parse(d_str, fallback_years=None):
    try:
        if not re.search(r"\d{4}", d_str) and fallback_years:
            for yr in fallback_years:
                try:
                    return dparse.parse(d_str.strip() + " " + yr, dayfirst=True).date()
                except Exception:
                    pass
        return dparse.parse(d_str.strip(), dayfirst=True).date()
    except Exception:
        return None


def extract(council_name, ons_code, raw_text):
    """
    Extract holiday rows from text.
    Strategy 1: find explicit holiday labels with date ranges.
    Strategy 2: infer holidays from gaps between consecutive term dates.
    """
    region = region_for(ons_code)
    rows = []
    seen = set()

    def add(name, start, end):
        if not start or not end:
            return
        if start > end:
            start, end = end, start
        if start.year < 2025 or start.year > 2028:
            return
        key = (ons_code, start.isoformat())
        if key in seen:
            return
        seen.add(key)
        rows.append({
            "council_name": council_name,
            "council_code": ons_code,
            "holiday_name": name,
            "start_date":   start.isoformat(),
            "end_date":     end.isoformat(),
            "year":         start.year,
            "region":       region,
        })

    text = re.sub(r"\|", "\n", str(raw_text))
    text = re.sub(r"\t",  " ", text)
    fallback_years = re.findall(r"\b(202[5-9])\b", text)
    segments = [s.strip() for s in re.split(r"\n+", text) if s.strip()]

    # Strategy 1 — explicit holiday labels
    for i, seg in enumerate(segments):
        holiday_name = None
        for name, pattern in HOLIDAY_LABELS:
            if re.search(pattern, seg, re.IGNORECASE):
                holiday_name = name
                break
        if not holiday_name:
            continue
        search_text = " ".join(segments[i:min(i + 4, len(segments))])
        to_m   = re.search(DATE_PAT + r"\s+to\s+"   + DATE_PAT, search_text, re.IGNORECASE)
        dash_m = re.search(DATE_PAT + r"\s*[-–]\s*" + DATE_PAT, search_text, re.IGNORECASE)
        date_pair = None
        if to_m:
            date_pair = (to_m.group(1), to_m.group(2))
        elif dash_m:
            date_pair = (dash_m.group(1), dash_m.group(2))
        else:
            all_d = re.findall(DATE_PAT, search_text, re.IGNORECASE)
            if len(all_d) >= 2:
                date_pair = (all_d[0], all_d[1])
        if date_pair:
            s = try_parse(date_pair[0], fallback_years)
            e = try_parse(date_pair[1], fallback_years)
            if s and e and 2 <= abs((e - s).days) <= 49:
                add(holiday_name, s, e)

    # Strategy 2 — gap inference fallback (only when < 3 explicit rows found)
    if len(rows) < 3:
        all_d_raw = re.findall(DATE_PAT, text, re.IGNORECASE)
        parsed_dates = sorted(set(
            d for d_str in all_d_raw
            for d in [try_parse(d_str, fallback_years)]
            if d and 2025 <= d.year <= 2028
        ))
        candidates = []
        for j in range(len(parsed_dates) - 1):
            gap_s = parsed_dates[j] + timedelta(days=1)
            gap_e = parsed_dates[j + 1] - timedelta(days=1)
            if gap_e < gap_s:
                continue
            name = classify_gap(gap_s, gap_e)
            if not name:
                continue
            span = (gap_e - gap_s).days + 1
            acad_year = gap_s.year if gap_s.month >= 9 else gap_s.year - 1
            candidates.append((name, acad_year, span, gap_s, gap_e))
        # Keep only the longest gap per holiday type per academic year
        best = {}
        for name, acad_year, span, gap_s, gap_e in candidates:
            key = (name, acad_year)
            if key not in best or span > best[key][0]:
                best[key] = (span, gap_s, gap_e)
        for (name, _), (_, gap_s, gap_e) in best.items():
            add(name, gap_s, gap_e)

    return rows


def fetch(url):
    """Fetch a URL and return (plain_text, error_string)."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        if r.status_code != 200:
            return None, f"HTTP {r.status_code}"
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script", "style", "nav", "header", "footer"]):
            tag.decompose()
        text = soup.get_text(separator="\n")
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip(), None
    except Exception as e:
        return None, str(e)


# ── Main ────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 65)
    print("SCHOOL HOLIDAYS FULL REBUILD")
    print("=" * 65)

    print(f"\nReading {XLSX_PATH} ...")
    df = pd.read_excel(XLSX_PATH)
    total = len(df)
    print(f"  {total} councils to process\n")

    all_rows = []
    results  = {}  # ons_code -> {"rows": n, "source": str, "error": str|None}

    # Track which council URLs have already been fetched to avoid re-fetching
    # when multiple councils share the same URL (e.g. all 12 Essex districts)
    url_cache = {}

    for idx, row in df.iterrows():
        council     = row["Council_Name"]
        ons         = row["ONS_Council_Code"]
        govuk_url   = str(row["GOVUK_Term_Dates_URL"]).strip()
        council_url = str(row["Council_Term_Dates_URL"]).strip()
        raw_text    = row["Term_Dates_Raw_Text"]

        print(f"[{idx+1:3}/{total}] {council}", end=" ... ", flush=True)

        holidays = []

        # ── Source 1: GOV.UK page ──────────────────────────────────────────
        if not holidays and govuk_url.startswith("http"):
            if govuk_url not in url_cache:
                url_cache[govuk_url], _ = fetch(govuk_url)
                time.sleep(DELAY)
            text = url_cache[govuk_url]
            if text:
                holidays = extract(council, ons, text)
                if holidays:
                    results[ons] = {"rows": len(holidays), "source": "GOV.UK", "error": None}
                    print(f"{len(holidays)} rows  [GOV.UK]")

        # ── Source 2: raw text from spreadsheet ───────────────────────────
        if not holidays:
            has_text = (pd.notna(raw_text)
                        and len(str(raw_text).strip()) > 20
                        and not str(raw_text).strip().startswith("http"))
            if has_text:
                holidays = extract(council, ons, str(raw_text))
                if holidays:
                    results[ons] = {"rows": len(holidays), "source": "spreadsheet", "error": None}
                    print(f"{len(holidays)} rows  [spreadsheet]")

        # ── Source 3: council's own URL ────────────────────────────────────
        if not holidays and council_url.startswith("http") and council_url != govuk_url:
            if council_url not in url_cache:
                url_cache[council_url], err = fetch(council_url)
                time.sleep(DELAY)
            text = url_cache.get(council_url)
            if text:
                holidays = extract(council, ons, text)
                if holidays:
                    results[ons] = {"rows": len(holidays), "source": "council URL", "error": None}
                    print(f"{len(holidays)} rows  [council URL]")
                else:
                    results[ons] = {"rows": 0, "source": "council URL", "error": "parsed 0 rows"}
                    print("0 rows parsed")
            else:
                results[ons] = {"rows": 0, "source": "council URL", "error": "fetch failed"}
                print("fetch failed")

        if not holidays and ons not in results:
            results[ons] = {"rows": 0, "source": "—", "error": "no data found"}
            print("no data")

        all_rows.extend(holidays)

    # ── Global deduplication ───────────────────────────────────────────────
    print("\nDeduplicating ...")
    seen_keys = set()
    deduped = []
    for r in all_rows:
        key = (r["council_code"], r["holiday_name"], r["start_date"])
        if key not in seen_keys:
            seen_keys.add(key)
            deduped.append(r)

    councils_with_data = len(set(r["council_code"] for r in deduped))
    print(f"  {len(deduped)} unique rows across {councils_with_data} councils")

    # ── Wipe Supabase ──────────────────────────────────────────────────────
    print("\nClearing school_holidays table ...")
    supabase.table("school_holidays").delete().neq("id", 0).execute()
    print("  Cleared.")

    # ── Insert ─────────────────────────────────────────────────────────────
    print("Inserting ...")
    BATCH = 500
    inserted = 0
    for i in range(0, len(deduped), BATCH):
        supabase.table("school_holidays").insert(deduped[i:i + BATCH]).execute()
        inserted += len(deduped[i:i + BATCH])
        print(f"  {inserted}/{len(deduped)} rows ...")

    # ── Summary ────────────────────────────────────────────────────────────
    final = supabase.table("school_holidays").select("id", count="exact").execute()

    by_source = defaultdict(int)
    for v in results.values():
        if v["rows"] > 0:
            by_source[v["source"]] += 1

    failed = {ons: v for ons, v in results.items() if v["rows"] == 0}
    name_lookup = {row["ONS_Council_Code"]: row["Council_Name"] for _, row in df.iterrows()}

    print(f"\n{'='*65}")
    print("SUMMARY")
    print(f"  Rows in Supabase:        {final.count}")
    print(f"  Councils with data:      {councils_with_data} / {total}")
    print(f"  Source breakdown:")
    for source, count in sorted(by_source.items(), key=lambda x: -x[1]):
        print(f"    {source:20} {count} councils")
    print(f"  No data:                 {len(failed)} councils")
    if failed:
        print(f"\n  Councils still missing:")
        for ons, v in list(failed.items())[:30]:
            print(f"    {name_lookup.get(ons, ons):40} ({v['error']})")
        if len(failed) > 30:
            print(f"    ... and {len(failed)-30} more")
    print("=" * 65)


if __name__ == "__main__":
    main()
