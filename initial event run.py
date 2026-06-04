import streamlit as st
import requests
import csv
import io
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
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

TM_BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"
POSTCODE_API = "https://api.postcodes.io/postcodes/{}"

MAX_PAGES = 5
PAGE_SIZE = 200
WINDOW_DAYS = 30
MONTHS_AHEAD = 24

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# =====================================================
# UI
# =====================================================

st.title("Burdy Business Event Finder")
st.write("Find local events using Ticketmaster")

postcode = st.text_input("Enter postcode")
radius = st.slider(
    "Search radius (miles)",
    min_value=1,
    max_value=100,
    value=10
)

# =====================================================
# SEARCH
# =====================================================

if st.button("Search Events"):

    if not postcode:
        st.warning("Please enter a postcode.")
        st.stop()

    clean_postcode = postcode.replace(" ", "").upper()

    # -------------------------------------------------
    # Convert postcode to latitude/longitude
    # -------------------------------------------------

    try:
        geo_response = requests.get(
            POSTCODE_API.format(clean_postcode),
            timeout=10
        )

        geo = geo_response.json()

    except Exception as e:
        st.error(f"Postcode lookup failed: {e}")
        st.stop()

    if not geo.get("result"):
        st.error("Invalid postcode.")
        st.stop()

    lat = geo["result"]["latitude"]
    lon = geo["result"]["longitude"]

    # -------------------------------------------------
    # Search Ticketmaster
    # -------------------------------------------------

    start_date = datetime.now(timezone.utc)
    final_date = start_date + timedelta(days=30 * MONTHS_AHEAD)

    events = {}

    progress = st.progress(0)
    status = st.empty()

    total_windows = max(
        1,
        (final_date - start_date).days // WINDOW_DAYS
    )

    window_count = 0

    while start_date < final_date:

        end_date = start_date + timedelta(days=WINDOW_DAYS)

        window_count += 1

        status.text(
            f"Searching window {window_count}/{total_windows} "
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

                response = requests.get(
                    TM_BASE_URL,
                    params=params,
                    timeout=15
                )

            except requests.RequestException as e:

                st.error(f"Ticketmaster request failed: {e}")
                st.stop()

            if response.status_code == 429:
                time.sleep(2)
                continue

            if response.status_code != 200:

                st.error(
                    f"Ticketmaster error {response.status_code}"
                )

                st.code(response.text)

                st.stop()

            data = response.json()

            total_pages = min(
                data.get("page", {}).get("totalPages", 1),
                MAX_PAGES
            )

            for event in data.get("_embedded", {}).get("events", []):

                venues = (
                    event.get("_embedded", {})
                    .get("venues", [])
                )

                if not venues:
                    continue

                venue = venues[0]

                event_id = event.get("id")

                classifications = event.get(
                    "classifications",
                    []
                )

                event_type = "Unknown"

                if classifications:
                    event_type = (
                        classifications[0]
                        .get("segment", {})
                        .get("name", "Unknown")
                    )

                events[event_id] = {

                    "ID": event_id,

                    "Date":
                        event.get("dates", {})
                        .get("start", {})
                        .get("localDate"),

                    "Time":
                        event.get("dates", {})
                        .get("start", {})
                        .get("localTime"),

                    "Name":
                        event.get("name"),

                    "Venue Name":
                        venue.get("name"),

                    "Type":
                        event_type,

                    "City":
                        venue.get("city", {})
                        .get("name"),

                    "PostalCode":
                        venue.get("postalCode"),

                    "Latitude":
                        venue.get("location", {})
                        .get("latitude"),

                    "Longitude":
                        venue.get("location", {})
                        .get("longitude"),

                    "url":
                        event.get("url"),

                    "Created At":
                        datetime.utcnow().isoformat()
                }

            page += 1
            time.sleep(0.2)

        progress.progress(
            min(window_count / total_windows, 1.0)
        )

        start_date = end_date

    status.success("Search complete")

    # =================================================
    # NO EVENTS FOUND
    # =================================================

    if not events:

        st.info("No events found.")
        st.stop()

    rows = list(events.values())

    st.success(
        f"Found {len(rows):,} unique events"
    )

    # =================================================
    # SUPABASE UPLOAD
    # =================================================

    upload_status = st.empty()

    upload_status.info(
        f"Uploading {len(rows):,} events..."
    )

    batch_size = 500
    uploaded = 0

    try:

        for i in range(0, len(rows), batch_size):

            batch = rows[i:i + batch_size]

            (
                supabase
                .table("BurdySteupTest")
                .upsert(
                    batch,
                    on_conflict="ID"
                )
                .execute()
            )

            uploaded += len(batch)

        upload_status.success(
            f"Uploaded {uploaded:,} events"
        )

    except Exception as e:

        st.error(
            f"Supabase upload failed:\n\n{e}"
        )

        st.stop()

    # =================================================
    # DATABASE COUNT
    # =================================================

    try:

        count_result = (
            supabase
            .table("BurdySteupTest")
            .select(
                "ID",
                count="exact"
            )
            .execute()
        )

        st.info(
            f"Database contains "
            f"{count_result.count:,} events"
        )

    except Exception:
        pass

    # =================================================
    # DISPLAY RESULTS
    # =================================================

    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        use_container_width=True
    )

    # =================================================
    # CSV DOWNLOAD
    # =================================================

    csv_buffer = io.StringIO()

    writer = csv.DictWriter(
        csv_buffer,
        fieldnames=df.columns
    )

    writer.writeheader()
    writer.writerows(rows)

    st.download_button(
        label="⬇ Download CSV",
        data=csv_buffer.getvalue(),
        file_name=f"{clean_postcode}.csv",
        mime="text/csv"
    )
