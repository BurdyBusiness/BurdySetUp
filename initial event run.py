import streamlit as st
import requests
import csv
import io
import time
from datetime import datetime, timedelta, timezone

# -----------------------------
# CONFIG
# -----------------------------
TICKETMASTER_API_KEY = st.secrets["TICKETMASTER_API_KEY"]
TM_BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"
POSTCODE_API = "https://api.postcodes.io/postcodes/{}"

MAX_PAGES = 5          # Ticketmaster hard limit
PAGE_SIZE = 200
WINDOW_DAYS = 30       # date window size
MONTHS_AHEAD = 24      # how far into future to search

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="Ticketmaster Event Finder", layout="centered")
st.title("Burdy Business Event Finder")
st.write("Find all local events in your area")

postcode = st.text_input("Enter postcode")
radius = st.slider("Search radius (miles)", min_value=1, max_value=100, value=10)

if st.button("Search Events"):
    if not postcode:
        st.warning("Please enter a postcode.")
        st.stop()

    clean_postcode = postcode.replace(" ", "").upper()

    # -----------------------------
    # POSTCODE → LAT/LONG
    # -----------------------------
    geo = requests.get(POSTCODE_API.format(clean_postcode)).json()
    if not geo.get("result"):
        st.error("Invalid postcode.")
        st.stop()

    lat = geo["result"]["latitude"]
    lon = geo["result"]["longitude"]

    # -----------------------------
    # DATE WINDOWS
    # -----------------------------
    start_date = datetime.now(timezone.utc)
    end_date = start_date + timedelta(days=WINDOW_DAYS)
    final_date = start_date + timedelta(days=30 * MONTHS_AHEAD)

    events = {}
    progress = st.progress(0)
    status = st.empty()

    total_windows = max(1, (final_date - start_date).days // WINDOW_DAYS)
    window_count = 0

    while start_date < final_date:
        window_count += 1
        status.text(
            f"Date window {window_count}/{total_windows} "
            f"({start_date.date()} → {end_date.date()})"
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

            try:
                response = requests.get(TM_BASE_URL, params=params, timeout=10)
            except requests.RequestException as e:
                st.error(f"Request error: {e}")
                st.stop()

            if response.status_code == 429:
                # Rate limit hit, wait and retry
                time.sleep(2)
                continue

            if response.status_code != 200:
                st.error(f"Ticketmaster error {response.status_code}")
                st.code(response.text)
                st.stop()

            data = response.json()
            total_pages = min(data.get("page", {}).get("totalPages", 1), MAX_PAGES)

for event in data.get("_embedded", {}).get("events", []):
    venues = event.get("_embedded", {}).get("venues", [])
    if not venues:
        continue
    venue = venues[0]

    event_id = event.get("id")
    events[event_id] = {
        "name": event.get("name"),
        "date": event.get("dates", {}).get("start", {}).get("localDate"),
        "time": event.get("dates", {}).get("start", {}).get("localTime"),
        "venue": venue.get("name"),
        "city": venue.get("city", {}).get("name"),
        "url": event.get("url"),
    }

            page += 1
            time.sleep(0.2)

        # advance to next window
        start_date = end_date
        end_date = start_date + timedelta(days=WINDOW_DAYS)
        progress.progress(min(window_count / total_windows, 1.0))

    status.text("Done!")

    if not events:
        st.info("No events found.")
        st.stop()

    # -----------------------------
    # CSV OUTPUT
    # -----------------------------
    rows = list(events.values())
    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

    filename = f"{clean_postcode}.csv"

    st.success(f"Found {len(rows)} unique events")
    st.dataframe(rows)

    st.download_button(
        "⬇️ Download CSV",
        csv_buffer.getvalue(),
        file_name=filename,
        mime="text/csv"
    )
