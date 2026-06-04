import streamlit as st
import requests
import time
import pandas as pd

from datetime import datetime, timedelta, timezone
from supabase import create_client

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Ticketmaster Event Finder",
    layout="centered"
)

TICKETMASTER_API_KEY = st.secrets["TICKETMASTER_API_KEY"]
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_SERVICE_ROLE_KEY"]

TM_BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"
POSTCODE_API = "https://api.postcodes.io/postcodes/{}"

MAX_PAGES = 5
PAGE_SIZE = 200
WINDOW_DAYS = 30
MONTHS_AHEAD = 24

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# =====================================================
# UI
# =====================================================

st.title("Burdy Business Event Finder")
st.write("Ticketmaster → Supabase Event Pipeline")

postcode = st.text_input("Enter postcode")
radius = st.slider("Search radius (miles)", 1, 100, 10)

# =====================================================
# LOAD FULL DATABASE (FIXED PAGINATION)
# =====================================================

def load_database():
    all_rows = []
    limit = 1000
    offset = 0

    while True:
        response = (
            supabase
            .table("BurdySteupTest")
            .select("*")
            .range(offset, offset + limit - 1)
            .execute()
        )

        data = response.data or []

        if not data:
            break

        all_rows.extend(data)

        if len(data) < limit:
            break

        offset += limit

    return all_rows

# =====================================================
# SYNC BUTTON
# =====================================================

if st.button("Sync Events from Ticketmaster"):

    if not postcode:
        st.warning("Please enter a postcode.")
        st.stop()

    clean_postcode = postcode.replace(" ", "").upper()

    # -----------------------------
    # GEO LOOKUP
    # -----------------------------
    geo = requests.get(POSTCODE_API.format(clean_postcode)).json()

    if not geo.get("result"):
        st.error("Invalid postcode.")
        st.stop()

    lat = geo["result"]["latitude"]
    lon = geo["result"]["longitude"]

    # -----------------------------
    # GET EXISTING IDS (FOR NEW DETECTION)
    # -----------------------------
    existing_ids_response = (
        supabase
        .table("BurdySteupTest")
        .select("ID")
        .execute()
    )

    existing_ids = set(
        item["ID"] for item in (existing_ids_response.data or [])
    )

    # -----------------------------
    # SEARCH SETUP
    # -----------------------------
    start_date = datetime.now(timezone.utc)
    final_date = start_date + timedelta(days=30 * MONTHS_AHEAD)

    events = {}

    progress = st.progress(0)
    status = st.empty()

    total_windows = max(1, (final_date - start_date).days // WINDOW_DAYS)
    window_count = 0

    # -----------------------------
    # TICKETMASTER LOOP
    # -----------------------------
    while start_date < final_date:

        end_date = start_date + timedelta(days=WINDOW_DAYS)
        window_count += 1

        status.text(
            f"Scanning window {window_count}/{total_windows}"
        )

        page = 0
        total_pages = 1

        while page < total_pages and page < MAX_PAGES:

            params = {
                "apikey": TICKETMASTER_API_KEY,
                "latlong": f"{lat},{lon}",
                "radius": radius,
                "unit": "miles",
                "countryCode": "GB",
                "size": PAGE_SIZE,
                "page": page,
                "startDateTime": start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "endDateTime": end_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            }

            response = requests.get(TM_BASE_URL, params=params, timeout=15)

            if response.status_code == 429:
                time.sleep(2)
                continue

            if response.status_code != 200:
                st.error(f"Ticketmaster error {response.status_code}")
                st.stop()

            data = response.json()

            total_pages = min(
                data.get("page", {}).get("totalPages", 1),
                MAX_PAGES
            )

            for event in data.get("_embedded", {}).get("events", []):

                venues = event.get("_embedded", {}).get("venues", [])
                if not venues:
                    continue

                venue = venues[0]
                event_id = event.get("id")

                classifications = event.get("classifications", [])
                event_type = (
                    classifications[0]
                    .get("segment", {})
                    .get("name", "Unknown")
                    if classifications else "Unknown"
                )

                is_new = event_id not in existing_ids

                events[event_id] = {
                    "ID": event_id,
                    "Date": event.get("dates", {}).get("start", {}).get("localDate"),
                    "Time": event.get("dates", {}).get("start", {}).get("localTime"),
                    "Name": event.get("name"),
                    "Venue Name": venue.get("name"),
                    "Type": event_type,
                    "City": venue.get("city", {}).get("name"),
                    "PostalCode": venue.get("postalCode"),
                    "Latitude": venue.get("location", {}).get("latitude"),
                    "Longitude": venue.get("location", {}).get("longitude"),
                    "url": event.get("url"),
                    "Is New": is_new,
                    "Created At": datetime.now(timezone.utc).isoformat()
                }

            page += 1
            time.sleep(0.2)

        progress.progress(min(window_count / total_windows, 1.0))
        start_date = end_date

    status.success("Sync complete")

    # -----------------------------
    # UPLOAD TO SUPABASE
    # -----------------------------
    rows = list(events.values())

    new_rows = [r for r in rows if r["Is New"]]

    st.info(f"Found {len(rows)} events")
    st.success(f"New events to insert: {len(new_rows)}")

    if new_rows:

        batch_size = 500
        uploaded = 0

        try:
            for i in range(0, len(new_rows), batch_size):

                batch = new_rows[i:i + batch_size]

                supabase.table("BurdySteupTest").upsert(
                    batch,
                    on_conflict="ID"
                ).execute()

                uploaded += len(batch)

            st.success(f"Uploaded {uploaded} new events")

        except Exception as e:
            st.error(f"Supabase upload failed:\n{e}")
            st.stop()

# =====================================================
# ALWAYS DISPLAY FULL DATABASE
# =====================================================

db_rows = load_database()

if not db_rows:
    st.info("No events in database yet.")
    st.stop()

df = pd.DataFrame(db_rows)

st.subheader("All Events in Supabase Database")
st.dataframe(df, use_container_width=True)
