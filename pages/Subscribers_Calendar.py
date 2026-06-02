import streamlit as st
import pandas as pd
from datetime import date
import calendar

# ---------------- SIDEBAR STYLING ----------------
st.markdown("""
<style>
[data-testid="stSidebar"] {background-color: #f7f0e6; border-right: 5px solid #ff7f50; padding-top: 0px;}
div[data-testid="stSidebar"] button[kind="primary"] {width:100%; padding:10px 0; margin-bottom:5px; text-align:left; background-color:#f0f2f6; border:1px solid #ddd; border-radius:4px; font-size:16px; cursor:pointer;}
div[data-testid="stSidebar"] button[kind="primary"]:hover {background-color:#e0e3ea;}
</style>
""", unsafe_allow_html=True)

# ---------------- CONFIG ----------------
EXCEL_PATH = rf"C:\Users\user\OneDrive\Documents\Business\BurdySetUp\{st.session_state.user_postcode}.xlsx"
DATE_COL = "Date"
TITLE_COL = "Name"
TYPE_COL = "Type"
VENUE_COL = "Venue Name"
CITY_COL = "City"
DESC_COL = "Description"
MONITOR_COL = "Monitor"  # Only show monitored events

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data(path):
    df = pd.read_excel(path)
    df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")
    df = df.dropna(subset=[DATE_COL])
    df[TYPE_COL] = df[TYPE_COL].astype(str)
    if MONITOR_COL not in df.columns:
        df[MONITOR_COL] = False
    df[MONITOR_COL] = df[MONITOR_COL].astype(bool)
    return df

df = load_data(EXCEL_PATH)

# ---------------- FILTER MONITORED ----------------
df = df[df[MONITOR_COL]]

# ---------------- MONTH NAVIGATION ----------------
today = date.today()
if "calendar_month" not in st.session_state:
    st.session_state.calendar_month = today.month
if "calendar_year" not in st.session_state:
    st.session_state.calendar_year = today.year

col1, col2, col3 = st.columns([1,2,1])
with col1:
    if st.button("◀ Previous Month"):
        if st.session_state.calendar_month == 1:
            st.session_state.calendar_month = 12
            st.session_state.calendar_year -= 1
        else:
            st.session_state.calendar_month -= 1
with col2:
    month = st.session_state.calendar_month
    year = st.session_state.calendar_year
    st.markdown(f"## 📅 {calendar.month_name[month]} {year}", unsafe_allow_html=True)
with col3:
    if st.button("Next Month ▶"):
        if st.session_state.calendar_month == 12:
            st.session_state.calendar_month = 1
            st.session_state.calendar_year += 1
        else:
            st.session_state.calendar_month += 1

# ---------------- CALENDAR GRID ----------------
cal = calendar.Calendar(firstweekday=0)
month_days = cal.monthdatescalendar(year, month)

# ---------------- TYPE COLORS ----------------
event_types = sorted(df[TYPE_COL].unique())
TYPE_COLORS = {}
palette = ["#FFB347", "#87CEFA", "#90EE90", "#FF6961", "#C0C0C0"]
for i, t in enumerate(event_types):
    TYPE_COLORS[t] = palette[i % len(palette)]

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.day-box {
    padding: 10px;
    height: 120px;
    min-height: 120px;
    border-radius: 4px;
    margin-bottom: 5px;
    overflow-y: auto;
    font-size: 12px;
}
.day-number {
    font-weight: bold;
    font-size: 16px;
    margin-bottom: 5px;
}
.event-color-box {
    display:inline-block;
    width:12px;
    height:12px;
    margin-right:4px;
    vertical-align:middle;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DAY-OF-WEEK HEADER ----------------
days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
header_cols = st.columns(7)
for d, col in zip(days_of_week, header_cols):
    col.markdown(f"**{d}**", unsafe_allow_html=True)

# ---------------- BUILD CALENDAR ----------------
for week in month_days:
    cols = st.columns(7)
    for day, col in zip(week, cols):
        # Skip days not in the current month
        if day.month != month:
            continue

        with col:
            day_events = df[df[DATE_COL].dt.date == day]

            # Determine background
            if day.weekday() in [4,5]:  # Friday/Saturday
                box_bg = "#d9d9d9"  # darker gray
            else:
                box_bg = "#f7f7f7"  # normal weekday

            day_box = f"<div class='day-box' style='background-color:{box_bg}'>"

            # Highlight today
            if day == today:
                day_box += f"<div class='day-number' style='color:red'>{day.day}</div>"
            else:
                day_box += f"<div class='day-number'>{day.day}</div>"

            # Events
            for _, event in day_events.iterrows():
                color = TYPE_COLORS.get(event[TYPE_COL], "#CCCCCC")
                day_box += f"<details><summary>{event[TITLE_COL]} ({event[TYPE_COL]})</summary>"
                day_box += f"- **Venue:** {event.get(VENUE_COL,'N/A')}<br>"
                day_box += f"- **City:** {event.get(CITY_COL,'N/A')}<br>"
                day_box += f"- **Description:** {event.get(DESC_COL,'No description')}<br>"
                day_box += f"<span class='event-color-box' style='background-color:{color}'></span>Event Type Color"
                day_box += "</details>"

            day_box += "</div>"
            col.markdown(day_box, unsafe_allow_html=True)
