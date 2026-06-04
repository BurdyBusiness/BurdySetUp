import streamlit as st
import requests
import time
import pandas as pd
import hashlib
from PIL import Image
from io import BytesIO
from datetime import datetime, timedelta, timezone
from supabase import create_client
import streamlit.components.v1 as components

# =====================================================
# PAGE CONFIG
# =====================================================

ICON_URL = "https://ujrublkoqtpijwijklvq.supabase.co/storage/v1/object/sign/Brand%20Logo/Bird%20Logo%20Left.png?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV9jYTQwZTg5ZS00MTVkLTQ0NjEtYTZjZi00OTI2MDIwYmYyZTkiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJCcmFuZCBMb2dvL0JpcmQgTG9nbyBMZWZ0LnBuZyIsImlhdCI6MTc4MDU5ODM2NSwiZXhwIjoxODEyMTM0MzY1fQ.OMa5cbOtPSUZR4JTjlT3Mm1XBZlgi2rugZOQx7SLCX0"

response = requests.get(ICON_URL)
icon = Image.open(BytesIO(response.content))

st.set_page_config(
    page_title="Burdy · Event Intelligence",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="auto",
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --orange:      #E8520A;
    --orange-dim:  #c94308;
    --orange-glow: rgba(232,82,10,.12);
    --green:       #179948;
    --green-dim:   #0f7035;
    --green-glow:  rgba(23,153,72,.12);
    --bg:          #F4F5F7;
    --surface:     #FFFFFF;
    --surface2:    #F0F1F4;
    --border:      rgba(0,0,0,.09);
    --text:        #141518;
    --text-dim:    #6B7280;
    --text-muted:  #A0A7B4;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}
.stApp { background: var(--bg) !important; }
#MainMenu, footer, header { visibility: hidden !important; }

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--text-muted); border-radius: 3px; }

.block-container {
    padding: 2rem 3rem 4rem !important;
    max-width: 1400px !important;
}

.burdy-logo {
    display: flex; align-items: center; gap: 12px;
    font-family: 'Syne', sans-serif;
    font-weight: 800; font-size: 24px;
    letter-spacing: -.03em; color: var(--text);
}
.live-badge {
    display: flex; align-items: center; gap: 8px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 999px; padding: 7px 16px;
    font-family: 'DM Mono', monospace;
    font-size: 11px; color: var(--text-dim);
    box-shadow: 0 1px 4px rgba(0,0,0,.06);
}
.live-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 6px var(--green);
    display: inline-block;
}
.control-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0,0,0,.06);
}
.control-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, var(--orange), var(--green), transparent);
}
div[data-testid="stTextInput"] input,
div[data-baseweb="select"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: var(--orange) !important;
    box-shadow: 0 0 0 3px var(--orange-glow) !important;
}
div[data-testid="stTextInput"] label,
.stSlider label {
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    color: var(--text-dim) !important;
    letter-spacing: .08em !important;
    text-transform: uppercase !important;
}
div[data-testid="stSlider"] > div > div > div { background: transparent !important; }
div[data-testid="stSlider"] > div > div > div > div {
    background: var(--orange) !important;
    box-shadow: 0 0 8px var(--orange-glow) !important;
}
.stButton > button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 12px !important;
    letter-spacing: .06em !important;
    text-transform: uppercase !important;
    border-radius: 8px !important;
    padding: 10px 22px !important;
    transition: all .2s !important;
    width: 100% !important;
    background: var(--orange) !important;
    color: #fff !important;
    border: none !important;
    box-shadow: 0 3px 14px var(--orange-glow) !important;
}
.stButton > button:hover {
    background: var(--orange-dim) !important;
    box-shadow: 0 5px 20px rgba(232,82,10,.3) !important;
    transform: translateY(-1px) !important;
}
div[data-testid="metric-container"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 20px 24px !important;
    position: relative !important;
    overflow: hidden !important;
    box-shadow: 0 2px 8px rgba(0,0,0,.05) !important;
}
div[data-testid="metric-container"]::after {
    content: '';
    position: absolute; bottom: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--orange), transparent);
}
div[data-testid="metric-container"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    color: var(--text-dim) !important;
    letter-spacing: .1em !important;
    text-transform: uppercase !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 32px !important;
    color: var(--orange) !important;
    letter-spacing: -.03em !important;
}
div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, var(--orange), var(--green)) !important;
    border-radius: 999px !important;
}
div[data-testid="stProgressBar"] > div {
    background: var(--surface2) !important;
    border-radius: 999px !important;
    height: 4px !important;
}
div[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
}
div[data-testid="stAlert"][kind="success"] {
    background: rgba(23,153,72,.08) !important;
    border: 1px solid rgba(23,153,72,.28) !important;
    color: #0f7035 !important;
}
div[data-testid="stAlert"][kind="error"] {
    background: rgba(232,82,10,.07) !important;
    border: 1px solid rgba(232,82,10,.28) !important;
    color: #c94308 !important;
}
div[data-testid="stAlert"][kind="info"] {
    background: rgba(0,0,0,.03) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-dim) !important;
}
div[data-testid="stAlert"][kind="warning"] {
    background: rgba(232,82,10,.06) !important;
    border: 1px solid rgba(232,82,10,.2) !important;
    color: #a03a06 !important;
}
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 28px 0 !important;
}
h3 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 18px !important;
    letter-spacing: -.02em !important;
    color: var(--text) !important;
}
.burdy-footer {
    margin-top: 60px;
    padding-top: 24px;
    border-top: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
}
.footer-copy {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: var(--text-muted);
}
.footer-badges { display: flex; gap: 8px; flex-wrap: wrap; }
.footer-badge {
    font-family: 'DM Mono', monospace;
    font-size: 10px; letter-spacing: .08em; text-transform: uppercase;
    padding: 4px 10px;
    border: 1px solid var(--border);
    border-radius: 4px;
    color: var(--text-muted);
    background: var(--surface);
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# CONFIG
# =====================================================

TICKETMASTER_API_KEY = st.secrets["TICKETMASTER_API_KEY"]
SUPABASE_URL         = st.secrets["SUPABASE_URL"]
SUPABASE_KEY         = st.secrets["SUPABASE_SERVICE_ROLE_KEY"]
BIRD_LOGO_URL        = "https://ujrublkoqtpijwijklvq.supabase.co/storage/v1/object/sign/Brand%20Logo/Bird%20Logo%20Left.png?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV9jYTQwZTg5ZS00MTVkLTQ0NjEtYTZjZi00OTI2MDIwYmYyZTkiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJCcmFuZCBMb2dvL0JpcmQgTG9nbyBMZWZ0LnBuZyIsImlhdCI6MTc4MDU5ODM2NSwiZXhwIjoxODEyMTM0MzY1fQ.OMa5cbOtPSUZR4JTjlT3Mm1XBZlgi2rugZOQx7SLCX0"
WORD_LOGO_URL        = "https://ujrublkoqtpijwijklvq.supabase.co/storage/v1/object/sign/Brand%20Logo/Font%20logo.png?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV9jYTQwZTg5ZS00MTVkLTQ0NjEtYTZjZi00OTI2MDIwYmYyZTkiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJCcmFuZCBMb2dvL0ZvbnQgbG9nby5wbmciLCJpYXQiOjE3ODA1OTg0MTEsImV4cCI6MTgxMjEzNDQxMX0.pt-zS-TT80l_mp-_jGklDgtx8K2wc0uafgW36VDklbo"

TM_BASE_URL  = "https://app.ticketmaster.com/discovery/v2/events.json"
POSTCODE_API = "https://api.postcodes.io/postcodes/{}"

WINDOW_DAYS  = 30
MONTHS_AHEAD = 24
MAX_PAGES    = 5
PAGE_SIZE    = 200

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# =====================================================
# HEADER
# =====================================================

st.markdown(f"""
<style>
.burdy-header {{
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 999;
    background: rgba(244,245,247,0.92);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    padding: 0 3rem;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}}
.burdy-header::after {{
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--orange), var(--green), transparent);
}}
.block-container {{ padding-top: 100px !important; }}
.ticker-wrap {{ overflow: hidden; flex: 1; margin: 0 40px; }}
.ticker-track {{
    display: flex;
    white-space: nowrap;
    animation: ticker 18s linear infinite;
}}
.ticker-track:hover {{ animation-play-state: paused; }}
.ticker-item {{
    font-family: 'DM Mono', monospace;
    font-size: 11px; color: var(--text-dim);
    letter-spacing: .08em; text-transform: uppercase;
    padding-right: 48px;
}}
.ticker-sep {{ color: var(--orange); padding-right: 48px; font-size: 11px; font-family: 'DM Mono', monospace; }}
@keyframes ticker {{
    0%   {{ transform: translateX(0); }}
    100% {{ transform: translateX(-50%); }}
}}
</style>

<div class="burdy-header">
  <div class="burdy-logo">
    <img src="{BIRD_LOGO_URL}" height="80" style="display:block;" />
    <img src="{WORD_LOGO_URL}" height="150" style="display:block;" />
  </div>
  <div class="ticker-wrap">
    <div class="ticker-track">
      <span class="ticker-item">Ticketmaster Discovery v2</span><span class="ticker-sep">◆</span>
      <span class="ticker-item">Supabase Live Sync</span><span class="ticker-sep">◆</span>
      <span class="ticker-item">PostCodes.io Geolocation</span><span class="ticker-sep">◆</span>
      <span class="ticker-item">24 Months Event Coverage</span><span class="ticker-sep">◆</span>
      <span class="ticker-item">UK Events Only</span><span class="ticker-sep">◆</span>
      <span class="ticker-item">Ticketmaster Discovery v2</span><span class="ticker-sep">◆</span>
      <span class="ticker-item">Supabase Live Sync</span><span class="ticker-sep">◆</span>
      <span class="ticker-item">PostCodes.io Geolocation</span><span class="ticker-sep">◆</span>
      <span class="ticker-item">24 Months Event Coverage</span><span class="ticker-sep">◆</span>
      <span class="ticker-item">UK Events Only</span><span class="ticker-sep">◆</span>
    </div>
  </div>
  <div class="live-badge">
    <span class="live-dot"></span>
    Live
  </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# CONTROL CARD
# =====================================================

st.markdown("""
  <div style="
    font-family: 'DM Sans', sans-serif;
    font-weight: 700;
    font-size: 28px;
    letter-spacing: -.02em;
    color: var(--text);
    margin-bottom: 20px;
    text-align: center;
  ">Burdy Business Event Finder</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    postcode = st.text_input("Enter postcode")

with col2:
    radius = st.slider("Search radius (miles)", 1, 100, 10)

with col3:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    find_events = st.button("Find new events", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# HELPERS
# =====================================================

def get_location(postcode_input):
    geo = requests.get(
        POSTCODE_API.format(postcode_input.replace(" ", "").upper())
    ).json()
    if not geo.get("result"):
        return None, None
    return geo["result"]["latitude"], geo["result"]["longitude"]


def render_rows(data_df):
    headers = "".join(
        f"<th style='padding:10px 14px;text-align:left;font-family:DM Mono,monospace;"
        f"font-size:11px;color:#6B7280;letter-spacing:.08em;text-transform:uppercase;"
        f"border-bottom:1px solid rgba(0,0,0,.09);background:#fff;white-space:nowrap;'>{col}</th>"
        for col in data_df.columns
    )
    rows = "".join(
        "<tr>" + "".join(
            f"<td style='padding:10px 14px;border-bottom:1px solid rgba(0,0,0,.06);"
            f"font-size:13px;font-family:DM Sans,sans-serif;color:#141518;"
            f"background:#fff;white-space:nowrap;'>{val}</td>"
            for val in row
        ) + "</tr>"
        for row in data_df.itertuples(index=False)
    )
    return f"<thead><tr>{headers}</tr></thead><tbody>{rows}</tbody>"


def render_table(df):
    """Render the 3-visible + blurred overlay table via components.html."""
    visible_df = df.head(3)
    blurred_df = df.iloc[3:13]

    visible_html = render_rows(visible_df)
    blurred_html = render_rows(blurred_df) if len(df) > 3 else ""

    visible_height = 44 + (len(visible_df) * 44)
    blurred_height = 44 + (len(blurred_df) * 44) if len(df) > 3 else 0
    total_height   = visible_height + min(blurred_height, 320) + 100

    blur_block = f"""
  <div class="blur-section">
    <div class="blur-inner">
      <table>{blurred_html}</table>
    </div>
    <div class="overlay">
      <div class="card">
        <div class="card-top"></div>
        <div class="lock">🔒</div>
        <div class="title">Unlock Full Results</div>
        <div class="body">
          You're viewing a preview of 3 results.<br>
          Contact Burdy Business to activate your subscription
          and unlock all events in your area.
        </div>
        <a class="btn" href="mailto:hello@burdy.com">Get in Touch</a>
      </div>
    </div>
  </div>
""" if len(df) > 3 else ""

    html = f"""<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: #F4F5F7; font-family: 'DM Sans', sans-serif; }}
  table {{ width: 100%; border-collapse: collapse; background: #fff; }}
  .visible-wrap {{
    border-radius: {('14px 14px 0 0' if len(df) > 3 else '14px')};
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,.05);
  }}
  .blur-section {{
    position: relative;
    border-radius: 0 0 14px 14px;
    overflow: hidden;
  }}
  .blur-inner {{
    filter: blur(5px);
    pointer-events: none;
    user-select: none;
    opacity: 0.6;
  }}
  .overlay {{
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(to bottom,
      rgba(244,245,247,0) 0%,
      rgba(244,245,247,0.85) 30%,
      rgba(244,245,247,0.85) 100%);
    z-index: 10;
  }}
  .card {{
    background: #fff;
    border: 1px solid rgba(0,0,0,.09);
    border-radius: 16px;
    padding: 28px 32px;
    max-width: 400px;
    width: 90%;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,.1);
    position: relative;
    overflow: hidden;
  }}
  .card-top {{
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #E8520A, #179948, transparent);
  }}
  .lock  {{ font-size: 32px; margin-bottom: 12px; }}
  .title {{
    font-family: 'Syne', sans-serif;
    font-weight: 800; font-size: 20px;
    letter-spacing: -.02em; color: #141518;
    margin-bottom: 10px;
  }}
  .body  {{ font-size: 13px; color: #6B7280; line-height: 1.6; margin-bottom: 20px; }}
  .btn {{
    display: inline-block; background: #E8520A; color: #fff;
    font-family: 'Syne', sans-serif; font-weight: 700; font-size: 11px;
    letter-spacing: .06em; text-transform: uppercase;
    padding: 10px 24px; border-radius: 8px; text-decoration: none;
    box-shadow: 0 3px 14px rgba(232,82,10,.25);
  }}
</style>
</head>
<body>
  <div class="visible-wrap">
    <table>{visible_html}</table>
  </div>
  {blur_block}
</body>
</html>"""

    components.html(html, height=total_height, scrolling=False)

# =====================================================
# FIND NEW EVENTS
# =====================================================

if find_events:
    if not postcode:
        st.warning("Enter a postcode")
        st.stop()

    lat, lon = get_location(postcode)
    if lat is None:
        st.error("Invalid postcode")
        st.stop()

    start_date    = datetime.now(timezone.utc)
    end_limit     = start_date + timedelta(days=30 * MONTHS_AHEAD)
    events        = {}
    progress      = st.progress(0)
    status        = st.empty()
    window        = 0
    total_windows = max(1, (end_limit - start_date).days // WINDOW_DAYS)

    while start_date < end_limit:
        end_date = start_date + timedelta(days=WINDOW_DAYS)
        window  += 1
        status.text(f"Scanning window {window}/{total_windows}")

        page        = 0
        total_pages = 1

        while page < total_pages and page < MAX_PAGES:
            params = {
                "apikey":        TICKETMASTER_API_KEY,
                "latlong":       f"{lat},{lon}",
                "radius":        radius,
                "unit":          "miles",
                "countryCode":   "GB",
                "size":          PAGE_SIZE,
                "page":          page,
                "startDateTime": start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "endDateTime":   end_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            }

            res = requests.get(TM_BASE_URL, params=params, timeout=15)

            if res.status_code == 429:
                time.sleep(2)
                continue
            if res.status_code != 200:
                st.error(f"API error {res.status_code}")
                st.stop()

            data = res.json()
            total_pages = min(data.get("page", {}).get("totalPages", 1), MAX_PAGES)

            for e in data.get("_embedded", {}).get("events", []):
                venues = e.get("_embedded", {}).get("venues", [])
                if not venues:
                    continue
                v        = venues[0]
                event_id = str(e.get("id")).strip()
                raw      = (
                    str(e.get("name")) +
                    str(e.get("dates", {}).get("start", {}).get("localDate")) +
                    str(v.get("name")) +
                    str(v.get("city", {}).get("name"))
                )
                events[event_id] = {
                    "ID":           event_id,
                    "Name":         e.get("name"),
                    "Date":         e.get("dates", {}).get("start", {}).get("localDate"),
                    "Time":         e.get("dates", {}).get("start", {}).get("localTime"),
                    "Venue Name":   v.get("name"),
                    "City":         v.get("city", {}).get("name"),
                    "PostalCode":   v.get("postalCode"),
                    "Latitude":     v.get("location", {}).get("latitude"),
                    "Longitude":    v.get("location", {}).get("longitude"),
                    "url":          e.get("url"),
                    "event_hash":   hashlib.md5(raw.encode()).hexdigest(),
                    "last_seen_at": datetime.now(timezone.utc).isoformat(),
                }

            page += 1
            time.sleep(0.2)

        progress.progress(min(window / total_windows, 1.0))
        start_date = end_date

    # Before counts
    before_total = supabase.table("BurdySteupTest").select("ID", count="exact").execute().count
    before_radius_count = len(
        supabase.rpc("search_within_radius",
            {"lat": lat, "lng": lon, "radius_meters": radius * 1609.34}
        ).execute().data or []
    )

    # Upsert
    batch = list(events.values())
    if batch:
        supabase.table("BurdySteupTest").upsert(batch, on_conflict="ID").execute()

    # After counts
    after_total = supabase.table("BurdySteupTest").select("ID", count="exact").execute().count
    after_radius_resp = supabase.rpc(
        "search_within_radius",
        {"lat": lat, "lng": lon, "radius_meters": radius * 1609.34}
    ).execute()
    after_radius_count = len(after_radius_resp.data or [])

    # ── SAVE TO SESSION STATE ──
    st.session_state["search_df"]    = pd.DataFrame(after_radius_resp.data or [])
    st.session_state["search_label"] = f"{after_radius_count} events within {radius} miles of {postcode.upper()}"

    status.empty()
    status.empty()
    progress.empty()

    st.markdown(f"""
    <style>
    .stat-row {{
        display: flex;
        gap: 12px;
        margin-bottom: 8px;
    }}
    .stat-box {{
        flex: 1;
        background: transparent;
        border: 1px solid rgba(0,0,0,.09);
        border-radius: 10px;
        padding: 16px 20px;
        text-align: center;
        font-family: 'DM Sans', sans-serif;
    }}
    .stat-num {{
        font-size: 28px;
        font-weight: 700;
        color: #141518;
        margin-bottom: 4px;
    }}
    .stat-label {{
        font-size: 12px;
        color: #6B7280;
        font-weight: 400;
    }}
    </style>
    <div class="stat-row">
      <div class="stat-box">
        <div class="stat-num">{after_total - before_total}</div>
        <div class="stat-label">New Events Added</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">{after_radius_count}</div>
        <div class="stat-label">Nearby Events within {radius} miles</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">{after_total}</div>
        <div class="stat-label">Total Events in Database</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
# =====================================================
# SEARCH VIEW
# =====================================================

if postcode and not find_events:
    lat, lon = get_location(postcode)
    if lat is not None:
        resp = supabase.rpc(
            "search_within_radius",
            {"lat": lat, "lng": lon, "radius_meters": radius * 1609.34}
        ).execute()
        st.session_state["search_df"]    = pd.DataFrame(resp.data or [])
        st.session_state["search_label"] = f"{len(st.session_state['search_df'])} events within {radius} miles of {postcode.upper()}"

df    = st.session_state.get("search_df", pd.DataFrame())
label = st.session_state.get("search_label", "")

if not df.empty:
    st.divider()
    st.subheader(label)
    st.caption(f"{len(df)} events found — showing preview")
    render_table(df)

# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div class="burdy-footer">
  <div class="footer-copy">© 2026 Burdy Business · Powered by Ticketmaster Discovery API</div>
  <div class="footer-badges">
    <span class="footer-badge">TM Discovery v2</span>
    <span class="footer-badge">Supabase</span>
    <span class="footer-badge">PostCodes.io</span>
    <span class="footer-badge">Streamlit</span>
  </div>
</div>
""", unsafe_allow_html=True)
