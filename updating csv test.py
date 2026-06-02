import streamlit as st
import requests
import csv
import time
import os
from datetime import datetime, timedelta
import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
TICKETMASTER_API_KEY = st.secrets["TICKETMASTER_API_KEY"]
TM_BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"
POSTCODE_API = "https://api.postcodes.io/postcodes/{}"

MAX_PAGES = 5
PAGE_SIZE = 200
WINDOW_DAYS = 30
MONTHS_AHEAD = 24

SNAPSHOT_PATH = r"C:\Users\user\Downloads\B25RE.csv"

FIELDNAMES = [
    "Date",
    "Name",
    "Time",
    "Venue Name",
    "Type",
    "City",
    "ID",
    "url",
    "PostalCode",
    "Latitude",
    "Longitude",
    "Created At",
]

# -----------------------------
# HELPERS
# -----------------------------
def trim_trailing_blank_rows(path):
    """Remove trailing empty rows from CSV (rows with blank 'ID')"""
    if not os.path.exists(path):
        return
    with open(path, newline="", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    # Keep rows with non-empty ID
    non_blank_rows = [row for row in reader if row.get("ID", "").strip()]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(non_blank_rows)


def load_existing_ids(path):
    """Load existing CSV snapshot and return set of IDs"""
    if not os.path.exists(path):
        return set()
    existing_ids = set()
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            event_id = row.get("ID", "").strip()
            if event_id:
                existing_ids.add(event_id)
    return existing_ids


def append_new_events(path, new_rows):
    """Append new rows to CSV"""
    file_exists = os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerows(new_rows)


def build_event_row(event):
    """Build a single event dict in the requested format"""
    venue = event["_embedded"]["venues"][0]
    event_type = (
        event.get("classifications", [{}])[0].get("segment", {}).get("name", "")
    )
    event_id = event.get("id")
    return {
        "Date": event.get("dates", {}).get("start", {}).get("localDate", ""),
        "Name": event.get("name", ""),
        "Time": event.get("dates", {}).get("start", {}).get("localTime", ""),
        "Venue Name": venue.get("name", ""),
        "Type": event_type,
        "City": venue.get("city", {}).get("name", ""),
        "ID": event_id,
        "url": event.get("url", ""),
        "PostalCode": venue.get("postalCode", ""),
        "Latitude": venue.get("location", {}).get("latitude", ""),
        "Longitude": venue.get("location", {}).get("longitude", ""),
        "Created At": pd.Timestamp.now(),
    }


# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="Ticketmaster Event Finder", layout="centered")
st.title("🎟️ Ticketmaster Event Finder")
st.write(
    "Fetch new events and append them directly below the last line of your CSV snapshot (deduplicated by ID)."
)

postcode = st.text_input("Enter postcode")
radius = st.slider("Search radius (miles)", 1, 100, 25)

if st.button("Search Events"):
    if not postcode:
        st.warning("Please enter a postcode.")
        st.stop()

    clean_postcode = postcode.replace(" ", "").upper()

    # -----------------------------
    # TRIM EMPTY ROWS FIRST
    # -----------------------------
    trim_trailing_blank_rows(SNAPSHOT_PATH)

    # -----------------------------
    # LOAD EXISTING SNAPSHOT (by ID)
    # -----------------------------
    existing_ids = load_existing_ids(SNAPSHOT_PATH)
    st.info(f"Loaded {len(existing_ids)} existing events from snapshot")

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
    # DATE WINDOWS (full range)
    # -----------------------------
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=WINDOW_DAYS)
    final_date = start_date + timedelta(days=30 * MONTHS_AHEAD)

    new_events = []  # preserve order returned by API
    progress = st.progress(0)
    status = st.empty()

    window_count = 0
    total_windows = max((final_date - start_date).days // WINDOW_DAYS, 1)

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

            response = requests.get(TM_BASE_URL, params=params)

            if response.status_code == 429:
                time.sleep(1.5)
                continue

            if response.status_code != 200:
                st.error(f"Ticketmaster error {response.status_code}")
                st.code(response.text)
                st.stop()

            data = response.json()
            total_pages = min(data.get("page", {}).get("totalPages", 1), MAX_PAGES)

            for event in data.get("_embedded", {}).get("events", []):
                row = build_event_row(event)
                event_id = row["ID"]
                if event_id and event_id not in existing_ids:
                    new_events.append(row)
                    existing_ids.add(event_id)  # prevent duplicates in same run

            page += 1
            time.sleep(0.2)

        start_date = end_date
        end_date += timedelta(days=WINDOW_DAYS)
        progress.progress(min(window_count / total_windows, 1.0))

    status.text("Done!")

    # -----------------------------
    # APPEND NEW EVENTS DIRECTLY TO CSV
    # -----------------------------
    if not new_events:
        st.info("No new events found.")
        st.stop()

    append_new_events(SNAPSHOT_PATH, new_events)

    st.success(f"Added {len(new_events)} new events to snapshot")
    st.subheader("🆕 Newly Added Events")
    st.dataframe(new_events)
