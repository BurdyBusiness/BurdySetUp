import streamlit as st
import pandas as pd
import requests
import os
import time
import csv
import pydeck as pdk
from datetime import datetime, date, timedelta
from io import BytesIO
import re
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- FUNCTIONS ----------------
def set_date_range(start, end, date_key):
    st.session_state[date_key] = (start, end)

def strip_html(text):
    if not isinstance(text, str):
        return text
    return re.sub(r'<[^>]+>', '', text)

# ---------------- CONSTANTS ----------------
DATE_COLUMN = "Date"
VENUE_COLUMN = "Venue Name"
TYPE_COLUMN = "Type"
HIDDEN_COLUMNS = ["Latitude", "Longitude", "ID", "PostalCode"]
os.environ["MAPBOX_API_KEY"] = st.secrets["MAPBOX_API_KEY"]

# ---------------- SIDEBAR STYLING ----------------
st.markdown("""
<style>
[data-testid="stSidebar"] {background-color: #f7f0e6; border-right: 5px solid #ff7f50; padding-top: 0px;}
div[data-testid="stSidebar"] button[kind="primary"] {width:100%; padding:10px 0; margin-bottom:5px; text-align:left; background-color:#f0f2f6; border:1px solid #ddd; border-radius:4px; font-size:16px; cursor:pointer;}
div[data-testid="stSidebar"] button[kind="primary"]:hover {background-color:#e0e3ea;}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD USERS ----------------
USERS_PATH = r"C:\Users\user\OneDrive\Documents\Business\BurdySetUp\Users.xlsx"

@st.cache_data
def load_users(path):
    df = pd.read_excel(path)
    df["Username"] = df["Username"].astype(str).str.strip().str.lower()
    df["Password"] = df["Password"].astype(str).str.strip()
    df["Postcode"] = df["Postcode"].astype(str).str.strip()
    return df

users_df = load_users(USERS_PATH)

# ---------------- SESSION STATE ----------------
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("username", "")
st.session_state.setdefault("user_postcode", "")

# ---------------- LOGIN ----------------
if not st.session_state.logged_in:
    st.subheader("🔐 Login")
    with st.form("login_form"):
        username_input = st.text_input("Username").strip().lower()
        password_input = st.text_input("Password", type="password").strip()
        submitted = st.form_submit_button("Login")

        if submitted:
            user_match = users_df[
                (users_df["Username"] == username_input) &
                (users_df["Password"] == password_input)
            ]
            if not user_match.empty:
                st.session_state.logged_in = True
                st.session_state.username = username_input
                st.session_state.user_postcode = user_match.iloc[0]["Postcode"]
                st.success(f"Welcome, {username_input}!")
                st.rerun()
            else:
                st.error("Invalid username or password.")
    st.stop()

# ---------------- AFTER LOGIN ----------------
st.sidebar.write(f"✅ Logged in as: {st.session_state.username}")
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.user_postcode = ""
    st.rerun()

# ---------------- EXCEL PATH ----------------
EXCEL_PATH = rf"C:\Users\user\OneDrive\Documents\Business\BurdySetUp\{st.session_state.user_postcode}.xlsx"

@st.cache_data
def load_sheet(path):
    return pd.read_excel(path)

try:
    df_excel = load_sheet(EXCEL_PATH)
except FileNotFoundError:
    st.error("Your subscription is not working")
    st.stop()

# ---------------- TICKETMASTER REFRESH FUNCTION ----------------
def refresh_ticketmaster_events(excel_path, postcode, radius=25, api_key=st.secrets["TICKETMASTER_API_KEY"]):
    TM_BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"
    MAX_PAGES = 5
    PAGE_SIZE = 200
    WINDOW_DAYS = 30
    MONTHS_AHEAD = 24

    FIELDNAMES = [
        "Date", "Name", "Time", "Venue Name", "Type", "City",
        "ID", "url", "PostalCode", "Latitude", "Longitude", "Created At"
    ]

    # Trim trailing blank rows
    if os.path.exists(excel_path):
        df_existing = pd.read_excel(excel_path)
        df_existing = df_existing[df_existing["ID"].notna()]
    else:
        df_existing = pd.DataFrame(columns=FIELDNAMES)

    existing_ids = set(df_existing["ID"].astype(str).str.strip())

    # Get lat/lon from postcode
    POSTCODE_API = "https://api.postcodes.io/postcodes/{}"
    geo = requests.get(POSTCODE_API.format(postcode.replace(" ", "").upper())).json()
    if not geo.get("result"):
        st.error("Invalid postcode for Ticketmaster refresh.")
        return df_existing
    lat = geo["result"]["latitude"]
    lon = geo["result"]["longitude"]

    # Date windows
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=WINDOW_DAYS)
    final_date = start_date + timedelta(days=30 * MONTHS_AHEAD)

    new_events = []
    while start_date < final_date:
        page = 0
        total_pages = 1

        while page < total_pages and page < MAX_PAGES:
            params = {
                "apikey": api_key,
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
                return df_existing

            data = response.json()
            total_pages = min(data.get("page", {}).get("totalPages", 1), MAX_PAGES)

            for event in data.get("_embedded", {}).get("events", []):
                venue = event["_embedded"]["venues"][0]
                event_type = event.get("classifications", [{}])[0].get("segment", {}).get("name", "")
                event_id = event.get("id")
                if event_id and event_id not in existing_ids:
                    row = {
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
                    new_events.append(row)
                    existing_ids.add(event_id)
            page += 1
            time.sleep(0.1)

        start_date = end_date
        end_date += timedelta(days=WINDOW_DAYS)

    # Append to Excel
    if new_events:
        df_new = pd.DataFrame(new_events)
        df_updated = pd.concat([df_existing, df_new], ignore_index=True)
        df_updated.to_excel(excel_path, index=False)
        st.success(f"✅ Added {len(new_events)} new events")
        return df_updated
    else:
        st.info("No new events found")
        return df_existing

# ---------------- PAGE HEADER ----------------
st.markdown(
    f"<h1 style='text-align:center;font-size:50px;color:black;'>Event Planning for {st.session_state.user_postcode}</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<h1 style='text-align:center;font-size:18px;font-weight:normal'>Burdy Business is a Birmingham based Corporate Planning tool, providing innovative local events data to strategic, future-minded companies.</h1>",
    unsafe_allow_html=True
)
# ---------------- REFRESH BUTTON ----------------
st.markdown("<hr style='border: 1px solid green;'>", unsafe_allow_html=True)
st.subheader("Find New Events")
if st.button("Search for new events"):
    # Refresh Ticketmaster events
    df_excel = refresh_ticketmaster_events(EXCEL_PATH, st.session_state.user_postcode)
    
    # Clear cached load_sheet
    load_sheet.clear()
    
    # Reload updated Excel
    df_excel = load_sheet(EXCEL_PATH)
    
    # ----------------- Recompute selected_columns -----------------
    visible_columns = [c for c in df_excel.columns if c not in HIDDEN_COLUMNS]
    selected_columns = [c for c in visible_columns if st.session_state.get(f"show_{c}", True)]
    
    # ----------------- Rebuild editable_table_df -----------------
    display_df = df_excel[selected_columns].copy()

    # Add "New" column based on Created At today
    display_df["New"] = df_excel.get("Created At", pd.Series([pd.NaT]*len(df_excel))).apply(
        lambda x: "New!" if pd.notna(x) and pd.to_datetime(x).date() == date.today() else ""
    )

    # Ensure Monitor column exists
    if "Monitor" not in display_df.columns:
        display_df["Monitor"] = False
    else:
        display_df["Monitor"] = display_df["Monitor"].astype(bool)

    # Clean URL column
    if "url" in display_df.columns:
        display_df["url"] = display_df["url"].apply(lambda x: x if pd.notna(x) else "")

    # Update session state table
    st.session_state.editable_table_df = display_df.copy()
    
    # No st.stop() here — let the script continue to display tables


#-----

table_placeholder = st.empty()


# ---------------- REST OF YOUR EXISTING CODE ----------------
# Add your event addition form, filters, table, map, and download buttons below.
# Replace any references to df_excel with the refreshed dataframe from the button.
# Everything else (filters, table, map, downloads) remains the same.


# ------ EVENT ADDITION ------
st.markdown("<hr style='border: 1px solid green;'>", unsafe_allow_html=True)
st.subheader("➕ Add a new event")

with st.form("add_event_form", clear_on_submit=True):
    col1, col2, col3, col4 = st.columns([3, 2, 2, 3])

    with col1:
        event_name = st.text_input("Event name")
    with col2:
        event_date = st.date_input("Date")
    with col3:
        event_time = st.text_input("Time (e.g. 19:30)")
    with col4:
        venue_name = st.text_input("Venue name")

    event_url = st.text_input("Event URL (optional)")
    submitted = st.form_submit_button("💾 Add event")

if submitted:
    if not event_name or not venue_name:
        st.error("Event name and venue are required.")
    else:
        try:
            # Load existing Excel
            df_existing = pd.read_excel(EXCEL_PATH)

            # Prepare new row with full datetime format
            new_row = {
                "Name": event_name,
                "Date": pd.Timestamp(event_date),  # <- change here
                "Time": event_time,
                "Venue Name": venue_name,
                "url": event_url,
                "Created At": pd.Timestamp.now(),          # <- new column for when entered
            }

            # Fill missing columns
            for col in df_existing.columns:
                if col not in new_row:
                    new_row[col] = ""

            # Append new row
            df_updated = pd.concat([df_existing, pd.DataFrame([new_row])], ignore_index=True)

            # Save to Excel
            df_updated.to_excel(EXCEL_PATH, index=False)

            # 🔥 Clear cache
            load_sheet.clear()

            # 🔥 Reload the Excel into main df_excel variable
            df_excel = load_sheet(EXCEL_PATH)

            st.success("✅ Event added successfully")

        except Exception as e:
            st.error(f"Failed to add event: {e}")


# ---------------- COLUMN SELECTION ----------------
st.markdown("<hr style='border: 1px solid green;'>", unsafe_allow_html=True)
st.subheader("Select your event data")

with st.expander("📌 Select columns to display", expanded=True):
    selected_columns = []
    visible_columns = [c for c in df_excel.columns if c not in HIDDEN_COLUMNS]
    cols_ui = st.columns(min(4, len(visible_columns)))
    for i, col in enumerate(visible_columns):
        with cols_ui[i % len(cols_ui)]:
            if st.checkbox(col, value=True, key=f"show_{col}"):
                selected_columns.append(col)
    if not selected_columns:
        st.warning("Please select at least one column.")
        st.stop()

df_visible = df_excel[selected_columns + HIDDEN_COLUMNS].copy()

# ---------------- FILTERS ----------------
st.markdown("<hr style='border: 1px solid green;'>", unsafe_allow_html=True)
st.subheader("Filter your events")

with st.expander("🔍 Filters", expanded=True):
    filters = {}
    filterable_columns = [c for c in df_visible.columns if c not in HIDDEN_COLUMNS]
    existing_dates = pd.to_datetime(df_excel[DATE_COLUMN], errors="coerce").dropna()
    min_date = existing_dates.min().date() if not existing_dates.empty else date.today()
    max_date = existing_dates.max().date() if not existing_dates.empty else date.today()
    today_date = date.today()
    display_columns = [c for c in filterable_columns if c != "url"]
    num_cols_per_row = 6
    cols = st.columns(num_cols_per_row)
    for i, col in enumerate(display_columns):
        key = f"filter_{col}"
        col_ui = cols[i % num_cols_per_row]
        with col_ui:
            if col == VENUE_COLUMN:
                options = sorted(df_excel[VENUE_COLUMN].dropna().astype(str).unique())
                default = [v for v in st.session_state.get(key, []) if v in options]
                filters[col] = st.multiselect(f"Select {col}", options=options, default=default, key=key)
            elif col == TYPE_COLUMN:
                options = sorted(df_excel[TYPE_COLUMN].dropna().astype(str).unique())
                default = [v for v in st.session_state.get(key, []) if v in options]
                filters[col] = st.multiselect(f"Select {col}", options=options, default=default, key=key)
            elif col == DATE_COLUMN:
                if key not in st.session_state:
                    st.session_state[key] = (today_date, max_date)
                filters[col] = st.date_input(f"Select {DATE_COLUMN} range", value=st.session_state[key], min_value=min_date, max_value=max_date, key=key)
            else:
                filters[col] = st.text_input(f"Search {col}", value=st.session_state.get(key, ""), key=key)

    # DATE SHORTCUTS + RESET
    sc1, sc2, sc3, sc4, sc5, sc6 = st.columns([1,1,1,1,1,1])
    with sc1: st.markdown("📅 Date Shortcuts")
    with sc2:
        st.button("Today", key="shortcut_today", on_click=set_date_range, args=(today_date, today_date, f"filter_{DATE_COLUMN}"), use_container_width=True)
    with sc3:
        st.button("Tomorrow", key="shortcut_tomorrow", on_click=set_date_range, args=(today_date + timedelta(days=1), today_date + timedelta(days=1), f"filter_{DATE_COLUMN}"), use_container_width=True)
    with sc4:
        start_week = today_date
        end_week = today_date + timedelta(days=6 - today_date.weekday())
        st.button("This Week", key="shortcut_week", on_click=set_date_range, args=(start_week, end_week, f"filter_{DATE_COLUMN}"), use_container_width=True)
    with sc5:
        start_month = today_date
        end_month = today_date + timedelta(days=30 - today_date.weekday())
        st.button("This Month", key="shortcut_month", on_click=set_date_range, args=(start_month, end_month, f"filter_{DATE_COLUMN}"), use_container_width=True)
    with sc6:
        if st.button("🔄 Reset Filters", key="reset_filters", use_container_width=True):
            for col in filterable_columns:
                k = f"filter_{col}"
                if k in st.session_state:
                    del st.session_state[k]
            st.session_state[f"filter_{DATE_COLUMN}"] = (today_date, max_date)
            st.session_state["__reset_trigger__"] = not st.session_state.get("__reset_trigger__", False)

# ---------------- APPLY FILTERS ----------------
filtered_df = df_excel.copy()
for col in filterable_columns:
    value = st.session_state.get(f"filter_{col}", None)
    if col in [VENUE_COLUMN, TYPE_COLUMN] and value:
        filtered_df = filtered_df[filtered_df[col].isin(value)]
    elif col == DATE_COLUMN and value:
        if isinstance(value, tuple) and len(value) == 2:
            start_date, end_date = value
            filtered_df["_sort_date"] = pd.to_datetime(filtered_df[DATE_COLUMN], errors="coerce")
            filtered_df = filtered_df[(filtered_df["_sort_date"].dt.date >= start_date) & (filtered_df["_sort_date"].dt.date <= end_date)]
            filtered_df.drop(columns="_sort_date", inplace=True)
    elif value and isinstance(value, str):
        filtered_df = filtered_df[filtered_df[col].astype(str).str.contains(value, case=False, na=False)]

# ---------------- SORT BY DATE ----------------
if DATE_COLUMN in filtered_df.columns:
    filtered_df["_sort_date"] = pd.to_datetime(filtered_df[DATE_COLUMN], errors="coerce")
    filtered_df = filtered_df.sort_values("_sort_date", ascending=True)
    filtered_df[DATE_COLUMN] = filtered_df["_sort_date"].dt.strftime("%d/%m/%Y")
    filtered_df.drop(columns="_sort_date", inplace=True)

# ---------------- DISPLAY TABLE ----------------
import streamlit as st
import pandas as pd
from datetime import date

# ---------------- INITIALIZE / UPDATE EDITABLE TABLE ----------------
if "editable_table_df" not in st.session_state:
    # Start with filtered dataframe
    df = filtered_df[selected_columns].copy()

    # Add "New" column based on Created At
    df["New"] = df.get("Created At", pd.Series([pd.NaT]*len(df))).apply(
        lambda x: "New!" if pd.notna(x) and pd.to_datetime(x).date() == date.today() else ""
    )

    # Ensure Monitor column exists
    if "Monitor" not in df.columns:
        df["Monitor"] = False
    else:
        df["Monitor"] = df["Monitor"].astype(bool)

    # Clean URL column
    if "url" in df.columns:
        df["url"] = df["url"].apply(lambda x: x if pd.notna(x) else "")

    st.session_state.editable_table_df = df.copy()
else:
    # Update "New" column for existing table in session_state
    df = st.session_state.editable_table_df.copy()
    if "Created At" in df.columns:
        df["New"] = df["Created At"].apply(
            lambda x: "New!" if pd.notna(x) and pd.to_datetime(x).date() == date.today() else ""
        )
    st.session_state.editable_table_df = df.copy()

# ---------------- REORDER "NEW" COLUMN FIRST ----------------
df = st.session_state.editable_table_df.copy()
if "New" in df.columns:
    cols = df.columns.tolist()
    cols.remove("New")
    cols = ["New"] + cols
    df = df[cols]
    st.session_state.editable_table_df = df.copy()

display_df = df.copy()  # this will be used for display

# ---------------- TOP "NEW!" EVENTS TABLE ----------------
with table_placeholder.container():
    # Always show all "New!" events, ignore filters
    new_df = st.session_state.editable_table_df[
        st.session_state.editable_table_df["New"] == "New!"
    ].copy()

    if not new_df.empty:
        # Reorder "New" column first
        cols = new_df.columns.tolist()
        if "New" in cols:
            cols.remove("New")
            cols = ["New"] + cols
            new_df = new_df[cols]

        edited_new_df = st.data_editor(
            new_df,
            column_config={
                "Monitor": st.column_config.CheckboxColumn(
                    "Monitor", help="Tick to monitor this new event"
                )
            },
            key="new_events_table",
            hide_index=True,
            use_container_width=True,
        )

        # Sync Monitor column back to session_state for main table
        for idx, event_id in enumerate(
            edited_new_df.get("ID", pd.Series([None] * len(edited_new_df)))
        ):
            if event_id in st.session_state.editable_table_df.get(
                "ID", pd.Series([])
            ).values:
                st.session_state.editable_table_df.loc[
                    st.session_state.editable_table_df["ID"] == event_id,
                    "Monitor",
                ] = edited_new_df.loc[idx, "Monitor"]
# ---------------- MAIN INTERACTIVE TABLE ----------------
st.subheader("All Events")

# Start from filtered dataframe (filters only apply here)
main_table_df = filtered_df.copy()

# Add "New" and "Monitor" from session state
for col in ["New", "Monitor"]:
    if col in st.session_state.editable_table_df.columns:
        main_table_df[col] = st.session_state.editable_table_df[col]

# ---------------- HIDE TECHNICAL COLUMNS ----------------
HIDE_MAIN_TABLE_COLS = [
    "PostalCode",
    "Latitude",
    "Longitude",
    "Created At"
]

main_table_df = main_table_df.drop(
    columns=[c for c in HIDE_MAIN_TABLE_COLS if c in main_table_df.columns],
    errors="ignore"
)

# ---------------- REORDER "NEW" COLUMN FIRST ----------------
if "New" in main_table_df.columns:
    cols = main_table_df.columns.tolist()
    cols.remove("New")
    cols = ["New"] + cols
    main_table_df = main_table_df[cols]

# ---------------- EDITABLE TABLE ----------------
edited_df = st.data_editor(
    main_table_df,
    column_config={
        "Monitor": st.column_config.CheckboxColumn(
            "Monitor", help="Tick to monitor this event"
        )
    },
    key="editable_table",
    hide_index=True,
    use_container_width=True,
)
# ---------------- SAVE BUTTON ----------------
if st.button("💾 Save changes to source file"):
    full_df = pd.read_excel(EXCEL_PATH)

    # Merge Monitor column
    if "Monitor" in full_df.columns:
        full_df.drop(columns=["Monitor"], inplace=True)

    if "ID" in full_df.columns and "ID" in edited_df.columns:
        full_df = full_df.merge(
            edited_df[["ID", "Monitor"]],
            on="ID",
            how="left"
        )
    else:
        full_df["Monitor"] = edited_df["Monitor"]

    full_df.to_excel(EXCEL_PATH, index=False)
    st.success("✅ Changes saved!")

    # Update session state after saving
    st.session_state.editable_table_df = edited_df.copy()



# ---------------- MAP & DOWNLOAD BUTTONS ----------------
# The rest of your code (map, PDF/CSV/XLSX downloads) remains unchanged.
# Use `filtered_df` and `display_df` wherever needed to reflect new data.


# ---------------- MAP HEADER ----------------
st.markdown(
"<hr style='border: 1px solid green;'>",
unsafe_allow_html=True
)
st.header("Map")
# ---------------- PYDECK MAP ----------------

# Required columns for map
required_map_cols = [VENUE_COLUMN, "Latitude", "Longitude"]

# Check if required columns exist
if not all(col in filtered_df.columns for col in required_map_cols):
    st.info(f"Map requires '{VENUE_COLUMN}', 'Latitude', and 'Longitude' columns in your data.")
else:
    # Prepare map data
    map_df = filtered_df.dropna(subset=["Latitude", "Longitude"]).copy()
    map_df["Latitude"] = pd.to_numeric(map_df["Latitude"], errors="coerce")
    map_df["Longitude"] = pd.to_numeric(map_df["Longitude"], errors="coerce")
    map_df = map_df.dropna(subset=["Latitude", "Longitude"])

    # Check if map data is empty
    if map_df.empty:
        st.error("⚠️ No events available for the selected filters. Adjust your filters to see events on the map.")
    else:
        # ---------------- Convert columns for tooltip ----------------
        for col in map_df.columns:
            if pd.api.types.is_datetime64_any_dtype(map_df[col]):
                map_df[col] = map_df[col].dt.strftime("%d/%m/%Y")
            elif pd.api.types.is_numeric_dtype(map_df[col]):
                map_df[col] = map_df[col].astype(float)
            else:
                map_df[col] = map_df[col].astype(str)

        # ---------------- Compute next event per venue ----------------
        df_excel["_event_date"] = pd.to_datetime(df_excel[DATE_COLUMN], errors="coerce")
        df_excel["_upcoming_date"] = df_excel["_event_date"].apply(
            lambda x: x if pd.notna(x) and x.date() >= date.today() else pd.NaT
        )

        event_name_col = "Name"  # replace with your actual event name column
        df_next = df_excel[[VENUE_COLUMN, "_upcoming_date", event_name_col]].dropna(subset=["_upcoming_date"])
        df_next = df_next.sort_values([VENUE_COLUMN, "_upcoming_date"])
        next_event_df = df_next.groupby(VENUE_COLUMN).first().reset_index()
        next_event_df.rename(columns={
            "_upcoming_date": "Next Event Date",
            event_name_col: "Next Event Name"
        }, inplace=True)

        map_df = map_df.merge(next_event_df, on=VENUE_COLUMN, how="left")
        map_df["Next Event Date"] = map_df["Next Event Date"].dt.strftime("%d/%m/%Y")
        map_df["Next Event Date"] = map_df["Next Event Date"].fillna("")
        map_df["Next Event Name"] = map_df["Next Event Name"].fillna("")

        # ---------------- Color coding ----------------
        def get_color(row):
            try:
                dt = pd.to_datetime(row.get(DATE_COLUMN), errors="coerce")
                if pd.notna(dt) and dt.date() >= date.today():
                    return [0, 200, 0]  # upcoming events: green
                return [255, 165, 0]    # past events: orange
            except:
                return [255, 165, 0]

        map_df["color"] = map_df.apply(get_color, axis=1)

        # ---------------- Map view ----------------
        avg_lat = map_df["Latitude"].mean()
        avg_lon = map_df["Longitude"].mean()

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position='[Longitude, Latitude]',
            get_color="color",
            get_radius=200,
            pickable=True
        )

        tooltip_html = f"<b>{{{VENUE_COLUMN}}}</b><br>Next event: {{Next Event Name}}<br>Date: {{Next Event Date}}"

        r = pdk.Deck(
            map_style="mapbox://styles/mapbox/streets-v11",
            initial_view_state=pdk.ViewState(
                latitude=avg_lat,
                longitude=avg_lon,
                zoom=12,
                pitch=0
            ),
            layers=[layer],
            tooltip={
                "html": tooltip_html,
                "style": {
                    "backgroundColor": "white",
                    "color": "black",
                    "padding": "10px",
                    "borderRadius": "5px",
                    "boxShadow": "0px 0px 5px rgba(0,0,0,0.3)"
                }
            }
        )

        st.pydeck_chart(r)

# ---------------- DOWNLOAD BUTTONS ----------------
st.markdown("""
<div style="border-top: 2px solid green; margin-bottom: 4px;"></div>
<h3 style="margin-top:0; margin-bottom:0;">Download your results</h3>
""", unsafe_allow_html=True)

# ---------- CREATE COLUMNS ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.download_button(
        label="⬇️ Download as CSV",
        data=display_df.to_csv(index=False),
        file_name="birmingham_events_custom_view.csv",
        mime="text/csv"
)

with col2:
    import re
    from io import BytesIO

    # ---------- Strip HTML tags from URL column ----------
    def strip_html(text):
        if not isinstance(text, str):
            return text
        return re.sub(r'<[^>]+>', '', text)  # remove all HTML tags

    if "url" in display_df.columns:
        display_df["url"] = display_df["url"].apply(strip_html)

    # ---------- Write to XLSX ----------
    xlsx_buffer = BytesIO()
    display_df.to_excel(xlsx_buffer, index=False, engine="openpyxl")
    xlsx_buffer.seek(0)

    # ---------- Streamlit download button ----------
    st.download_button(
        label="⬇️ Download as XLSX",
        data=xlsx_buffer,
        file_name="birmingham_events_custom_view.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

with col3:
    
    from io import BytesIO
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet

    pdf_buffer = BytesIO()

    # ---------- CONFIG ----------
    FONT_SIZE = 8
    LEFT_MARGIN = RIGHT_MARGIN = 18
    TOP_MARGIN = BOTTOM_MARGIN = 18
    NAME_COL_RATIO = 0.4  # portion of remaining width for Name column
    DATE_FIXED_CHARS = 10  # '22/22/2222'
    DATE_PADDING = 8  # extra padding in points

    styles = getSampleStyleSheet()
    cell_style = styles["Normal"]
    cell_style.fontSize = FONT_SIZE
    cell_style.leading = FONT_SIZE + 2

    # ---------- PREP DATA ----------
    # Exclude 'New', 'Monitor', 'Created At' columns
    pdf_df = main_table_df.drop(
    columns=["New", "Monitor", "Created At", "url", "City"],
    errors="ignore"
).copy()


    # ---------- PAGE SETUP ----------
    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN
    )

    page_width, _ = A4
    usable_width = page_width - LEFT_MARGIN - RIGHT_MARGIN

    # ---------- COLUMN WIDTHS ----------
    date_col_width = FONT_SIZE * 0.55 * DATE_FIXED_CHARS + DATE_PADDING
    remaining_width = usable_width - date_col_width
    other_cols = len(pdf_df.columns) - 2  # Name + Date

    col_widths = []
    for col in pdf_df.columns:
        col_lower = col.lower()
        if col_lower == "name":
            col_widths.append(remaining_width * NAME_COL_RATIO)
        elif col_lower == "date":
            col_widths.append(date_col_width)
        elif col_lower == "time":
            col_widths.append(date_col_width)
        else:
            col_widths.append(remaining_width * (1 - NAME_COL_RATIO) / other_cols)

    # ---------- BUILD TABLE DATA ----------
    table_data = []

    # Header row
    table_data.append([Paragraph(col, cell_style) for col in pdf_df.columns])

    # Data rows
    for _, row in pdf_df.iterrows():
        row_cells = []
        for col in pdf_df.columns:
            row_cells.append(Paragraph(str(row[col]), cell_style))
        table_data.append(row_cells)

    # ---------- CREATE TABLE ----------
    table = Table(table_data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), FONT_SIZE),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))

    # ---------- ADD LOGO + TITLE ----------
    logo_path = r"C:\Users\user\OneDrive\Documents\Business\Colour Logo.png"
    logo = Image(logo_path)
    logo.drawHeight = 50
    logo.drawWidth = 50

    title_style = styles["Heading1"]
    title_style.fontSize = 16
    title_style.leading = 18
    title_style.alignment = 0  # left-align
    title_paragraph = Paragraph("Birmingham Events", title_style)

    header_table = Table(
        [[logo, title_paragraph]],
        colWidths=[logo.drawWidth + 4, usable_width - logo.drawWidth - 4]
    )
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 12),
        ("GRID", (0,0), (-1,-1), 0, colors.white)
    ]))

    # ---------- BUILD PDF ----------
    story = [header_table, Spacer(1, 12), table]
    doc.build(story)
    pdf_buffer.seek(0)

    # ---------- STREAMLIT DOWNLOAD ----------
    st.download_button(
        label="⬇️ Download as PDF",
        data=pdf_buffer,
        file_name="birmingham_events_custom_view.pdf",
        mime="application/pdf"
    )



st.markdown(
"<hr style='border: 1px solid green;'>",
unsafe_allow_html=True
)


