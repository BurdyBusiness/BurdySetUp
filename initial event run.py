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
    padding: 2rem 3rem 80px !important;
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
    background: var(--surface) !important;
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
div[data-testid="stSlider"] label,
.stSlider label {
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    color: var(--text-dim) !important;
    letter-spacing: .08em !important;
    text-transform: uppercase !important;
}
div[data-testid="stSlider"] > div > div > div { background: transparent !important; }
div[data-testid="stSlider"] > div > div > div > div {
    background: var(--green) !important;
    box-shadow: 0 0 8px var(--green-glow) !important;
}
div[data-testid="stSlider"] [role="slider"] {
    background: var(--green) !important;
    border-color: var(--green) !important;
    box-shadow: 0 0 0 4px var(--green-glow) !important;
}
div[data-testid="stSlider"] [data-testid="stThumbValue"],
div[data-testid="stSlider"] [data-testid="stTickBarMin"],
div[data-testid="stSlider"] [data-testid="stTickBarMax"],
div[data-testid="stSlider"] div[class*="StyledThumbValue"],
div[data-testid="stSlider"] div[class*="thumbValue"] { color: var(--green) !important; }
div[data-testid="stSlider"] label,
div[data-testid="stSlider"] label p,
div[data-testid="stSlider"] label span { color: var(--text-dim) !important; }
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
.stat-row {
    display: flex;
    gap: 12px;
    margin-bottom: 24px;
}
.stat-box {
    flex: 1;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 16px;
    text-align: center;
    font-family: 'DM Sans', sans-serif;
    box-shadow: 0 2px 8px rgba(0,0,0,.05);
    position: relative;
    overflow: hidden;
}
.stat-box::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--orange), var(--green), transparent);
}
.stat-num {
    font-family: 'DM Sans', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: var(--orange);
    letter-spacing: -.03em;
    margin-bottom: 4px;
}
.stat-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: var(--text-dim);
    letter-spacing: .08em;
    text-transform: uppercase;
}

.burdy-footer {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    z-index: 998;
    background: #F4F5F7;
    padding: 14px 3rem;
    border-top: 1px solid rgba(0,0,0,.07);
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
    overflow: hidden;
}
.burdy-footer::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--orange), var(--green), transparent);
}
.footer-copy {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: var(--text-muted);
}
.footer-badges { display: flex; gap: 8px; flex-wrap: wrap; }
.footer-badge,
a.footer-badge,
a.footer-badge:link,
a.footer-badge:visited {
    font-family: 'DM Mono', monospace;
    font-size: 10px; letter-spacing: .08em; text-transform: uppercase;
    padding: 4px 10px;
    border: 1px solid var(--border);
    border-radius: 4px;
    color: var(--text-muted) !important;
    background: var(--surface);
    text-decoration: none !important;
    transition: border-color .15s, background .15s;
}
a.footer-badge:hover {
    border-color: var(--orange);
    background: var(--orange-glow);
    color: var(--orange) !important;
}

@media (max-width: 768px) {
    .block-container {
        padding: 2rem 1rem 60px !important;
    }

    /* Hero — hide images, centre text full width */
    .img-panel {
        display: none !important;
    }
    .centre {
        padding: 32px 20px !important;
    }
    .headline {
        font-size: 22px !important;
    }
    .body-text {
        font-size: 13px !important;
    }
    .stats {
        gap: 16px !important;
    }
    .stat-val {
        font-size: 16px !important;
    }

    /* Stat boxes — wrap to 2 columns */
    .stat-row {
        flex-wrap: wrap !important;
        gap: 8px !important;
    }
    .stat-box {
        flex: 1 1 calc(50% - 8px) !important;
        min-width: 0 !important;
        padding: 14px 10px !important;
    }
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 22px !important;
    }

    /* Control card — stack inputs */
    div[data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
    }

    /* Footer — fixed height, hide badges, show copyright only */
    .burdy-footer {
        padding: 10px 1rem !important;
        height: 44px !important;
        overflow: hidden !important;
        flex-wrap: nowrap !important;
    }
    .footer-badges {
        display: none !important;
    }
    .footer-copy {
        font-size: 10px !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# CONFIG
# =====================================================

TICKETMASTER_API_KEY = st.secrets["TICKETMASTER_API_KEY"]
SKIDDLE_API_KEY      = st.secrets["SKIDDLE_API_KEY"]
SUPABASE_URL         = st.secrets["SUPABASE_URL"]
SUPABASE_KEY         = st.secrets["SUPABASE_SERVICE_ROLE_KEY"]

TM_BASE_URL      = "https://app.ticketmaster.com/discovery/v2/events.json"
SKIDDLE_URL      = "https://www.skiddle.com/api/v1/events/search/"
POSTCODE_API     = "https://api.postcodes.io/postcodes/{}"

WINDOW_DAYS      = 30
MONTHS_AHEAD     = 24
TM_MAX_PAGES     = 5
TM_PAGE_SIZE     = 200
SK_MAX_PAGES     = 10
SK_PAGE_SIZE     = 100

SKIDDLE_ONLY     = {"Genres", "Artists", "Distance", "Min Age", "Tickets URL", "source"}

EVENTCODE_MAP = {
    "FEST":    "Festival",
    "LIVE":    "Live Music",
    "CLUB":    "Clubbing",
    "DATE":    "Dating",
    "THEATRE": "Theatre",
    "COMEDY":  "Comedy",
    "EXHIB":   "Exhibition",
    "KIDS":    "Kids / Family",
    "BARPUB":  "Bar / Pub",
    "LGB":     "Gay / Lesbian",
    "SPORT":   "Sport",
    "ARTS":    "Arts",
}

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)




# =====================================================
# CONTROL CARD
# =====================================================

st.markdown("""
<style>
  /* Full-bleed hero — targets the component wrapper injected by components.html */
  [data-testid="stCustomComponentV1"]:first-of-type {
    margin-left: -3rem !important;
    margin-right: -3rem !important;
    width: calc(100% + 6rem) !important;
    max-width: none !important;
    display: block !important;
  }
  [data-testid="stCustomComponentV1"]:first-of-type iframe {
    width: 100% !important;
    max-width: none !important;
    display: block !important;
  }
</style>
""", unsafe_allow_html=True)

components.html("""
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { background: transparent; width: 100%; overflow: hidden; }
</style>
<script>
  window.addEventListener('load', function() {
    try {
      var el = window.frameElement;
      if (!el) return;
      var wrapper = el.closest('[data-testid="stCustomComponentV1"]') || el.parentElement;
      if (!wrapper) return;

      // Measure how far the wrapper's left edge is from the viewport left edge
      var rect = wrapper.getBoundingClientRect();
      var offsetLeft  = rect.left;
      var offsetRight = window.parent.innerWidth - rect.right;

      var headerHeight = 80;
      var offsetTop   = rect.top - headerHeight;
      wrapper.style.marginLeft  = '-' + offsetLeft  + 'px';
      wrapper.style.marginRight = '-' + offsetRight + 'px';
      wrapper.style.marginTop   = '-' + offsetTop   + 'px';
      wrapper.style.width       = window.parent.innerWidth + 'px';
      wrapper.style.maxWidth    = 'none';
      el.style.width            = '100%';
      el.style.maxWidth         = 'none';
      el.style.display          = 'block';
    } catch(e) {}
  });
</script>
<style>
  .hero {
    background: #F4F5F7;
    overflow: hidden;
    font-family: 'DM Sans', sans-serif;
    display: flex;
    align-items: stretch;
    min-height: 340px;
    width: 100%;
    position: relative;
  }



  /* Image panels */
  .img-panel {
    flex: 0 0 20%;
    position: relative;
    overflow: hidden;
  }
  .img-panel img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    animation: kenburns 14s ease-in-out infinite alternate;
    transform-origin: center center;
  }
  .img-panel.right img {
    animation: kenburns-r 14s ease-in-out infinite alternate;
  }
  @keyframes kenburns {
    0%   { transform: scale(1)    translateX(0)   translateY(0); }
    100% { transform: scale(1.1) translateX(-2%) translateY(-2%); }
  }
  @keyframes kenburns-r {
    0%   { transform: scale(1)    translateX(0)  translateY(0); }
    100% { transform: scale(1.1) translateX(2%) translateY(-2%); }
  }
  .img-panel.left::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(to right,
      rgba(0,0,0,.18) 0%,
      rgba(0,0,0,.05) 30%,
      rgba(244,245,247,0) 45%,
      rgba(244,245,247,.5) 65%,
      rgba(244,245,247,.85) 80%,
      #F4F5F7 100%);
  }
  .img-panel.right::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(to left,
      rgba(0,0,0,.18) 0%,
      rgba(0,0,0,.05) 30%,
      rgba(244,245,247,0) 45%,
      rgba(244,245,247,.5) 65%,
      rgba(244,245,247,.85) 80%,
      #F4F5F7 100%);
  }

  /* Centre content */
  .centre {
    flex: 1;
    padding: 48px 40px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    z-index: 2;
    background: #F4F5F7;
  }
  .pill {
    display: inline-block;
    background: rgba(232,82,10,.10);
    border: 1px solid rgba(232,82,10,.22);
    border-radius: 999px;
    padding: 5px 16px;
    margin-bottom: 18px;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #E8520A;
    letter-spacing: .12em;
    text-transform: uppercase;
    font-weight: 500;
  }
  .headline {
    font-weight: 800;
    font-size: 30px;
    letter-spacing: -.03em;
    color: #141518;
    margin-bottom: 14px;
    line-height: 1.15;
  }
  .body-text {
    font-size: 14px;
    color: #6B7280;
    max-width: 520px;
    margin: 0 auto 28px;
    line-height: 1.75;
  }
  .stats {
    display: flex;
    justify-content: center;
    gap: 28px;
    flex-wrap: wrap;
    align-items: center;
  }
  .stat-val {
    font-weight: 800;
    font-size: 20px;
    color: #E8520A;
    letter-spacing: -.02em;
  }
  .stat-lbl {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    color: #A0A7B4;
    letter-spacing: .08em;
    text-transform: uppercase;
    margin-top: 2px;
  }
  .divider { width: 1px; height: 32px; background: rgba(0,0,0,.09); }
</style>

<div class="hero">

  <div class="img-panel left">
    <img src="https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=800&q=95" alt="Festival crowd" />
  </div>

  <div class="centre">
    <div class="pill">&#9670; &nbsp;Event Intelligence Platform</div>
    <div class="headline">Discover Every Event.<br>Anywhere in the UK.</div>
    <div class="body-text">
      Burdy Event Intelligence aggregates live data from <strong>Ticketmaster</strong> and
      <strong>Skiddle</strong> — two of the UK's largest ticketing platforms — and syncs it
      directly into your Supabase database in real time. Search by postcode, define your radius,
      and surface every upcoming event within your target area across the next 24 months.
      No manual exports. No stale data. Just clean, structured event intelligence at your fingertips.
    </div>
    <div class="stats">
      <div style="text-align:center;">
        <div class="stat-val">2 Sources</div>
        <div class="stat-lbl">Live API feeds</div>
      </div>
      <div class="divider"></div>
      <div style="text-align:center;">
        <div class="stat-val">24 Months</div>
        <div class="stat-lbl">Forward coverage</div>
      </div>
      <div class="divider"></div>
      <div style="text-align:center;">
        <div class="stat-val">Real-time</div>
        <div class="stat-lbl">Supabase sync</div>
      </div>
      <div class="divider"></div>
      <div style="text-align:center;">
        <div class="stat-val">UK-wide</div>
        <div class="stat-lbl">Postcode precision</div>
      </div>
    </div>
  </div>

  <div class="img-panel right">
    <img src="https://images.unsplash.com/photo-1524368535928-5b5e00ddc76b?w=800&q=95" alt="Concert crowd" />
  </div>

</div>

<div style="font-family:'DM Sans',sans-serif;font-weight:700;font-size:20px;
  letter-spacing:-.02em;color:#141518;margin:20px 0 8px;text-align:center;">
  Run a Search
</div>
""", height=520, scrolling=False)

col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    postcode = st.text_input("Enter postcode")
with col2:
    radius = st.slider("Search radius (miles)", 1, 100, 10)
with col3:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    find_events = st.button("Find events", use_container_width=True)

# ── Stat boxes: always visible, updated progressively during fetch ──
def _stat_row(tm, sk, new_events, nearby, total, radius_label):
    return f"""
<div class="stat-row">
  <div class="stat-box">
    <div class="stat-num">{tm}</div>
    <div class="stat-label">Ticketmaster Events</div>
  </div>
  <div class="stat-box">
    <div class="stat-num">{sk}</div>
    <div class="stat-label">Skiddle Events</div>
  </div>
  <div class="stat-box">
    <div class="stat-num">{new_events}</div>
    <div class="stat-label">New Events Added</div>
  </div>
  <div class="stat-box">
    <div class="stat-num">{nearby}</div>
    <div class="stat-label">Nearby within {radius_label} miles</div>
  </div>
  <div class="stat-box">
    <div class="stat-num">{total}</div>
    <div class="stat-label">Total in Database</div>
  </div>
</div>"""

stats_slot = st.empty()
try:
    _initial_total = supabase.table("BurdySteupTest").select("ID", count="exact").execute().count or 0
except Exception:
    _initial_total = "—"
stats_slot.markdown(_stat_row("—", "—", "—", "—", _initial_total, radius), unsafe_allow_html=True)




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


def upsert_batch(events_dict, strip_keys=None):
    """Upsert a dict of events, preserving first_seen_at / Created At on existing rows."""
    strip_keys = strip_keys or set()
    now        = datetime.now(timezone.utc).isoformat()
    batch = [
        {**{k: v for k, v in e.items() if k not in strip_keys},
         "first_seen_at": now,
         "Created At":    now}
        for e in events_dict.values()
    ]
    if not batch:
        return 0

    # Chunk ID lookup to avoid URL length limits
    all_ids      = [r["ID"] for r in batch]
    existing_ids = set()
    for i in range(0, len(all_ids), 100):
        chunk = all_ids[i:i + 100]
        rows  = (
            supabase.table("BurdySteupTest")
            .select("ID")
            .in_("ID", chunk)
            .execute()
            .data or []
        )
        existing_ids.update(row["ID"] for row in rows)

    new_rows    = [r for r in batch if r["ID"] not in existing_ids]
    update_rows = [
        # Only send fields that are non-null so we never overwrite existing data with NULL
        {k: v for k, v in r.items()
         if k not in {"first_seen_at", "Created At"} and v is not None}
        for r in batch if r["ID"] in existing_ids
    ]

    if new_rows:
        supabase.table("BurdySteupTest").insert(new_rows).execute()
    if update_rows:
        supabase.table("BurdySteupTest").upsert(update_rows, on_conflict="ID").execute()

    return len(batch)


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
    visible_df    = df.head(3)
    blurred_df    = df.iloc[3:13]
    visible_html  = render_rows(visible_df)
    blurred_html  = render_rows(blurred_df) if len(df) > 3 else ""
    visible_height = 44 + (len(visible_df) * 44)
    blurred_height = 44 + (len(blurred_df) * 44) if len(df) > 3 else 0
    total_height   = visible_height + min(blurred_height, 320) + 100

    blur_block = f"""
  <div class="blur-section">
    <div class="blur-inner"><table>{blurred_html}</table></div>
    <div class="overlay">
      <div class="card">
        <div class="card-top"></div>
        <div class="lock">🔒</div>
        <div class="title">Unlock Full Results</div>
        <div class="body">You're viewing a preview of 3 results.<br>
          Log in or contact Burdy Business to unlock all events in your area.</div>
        <div style="display:flex;gap:10px;justify-content:center;margin-top:4px;">
          <a class="btn-primary" href="/login">Log In</a>
          <a class="btn-secondary" href="mailto:hello@burdy.com">Contact Us</a>
        </div>
      </div>
    </div>
  </div>""" if len(df) > 3 else ""

    html = f"""<!DOCTYPE html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
<style>
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ background:#F4F5F7; font-family:'DM Sans',sans-serif; }}
table {{ width:100%; border-collapse:collapse; background:#fff; }}
.visible-wrap {{ border-radius:{'14px 14px 0 0' if len(df) > 3 else '14px'}; overflow:hidden; box-shadow:0 2px 10px rgba(0,0,0,.05); }}
.blur-section {{ position:relative; border-radius:0 0 14px 14px; overflow:hidden; }}
.blur-inner {{ filter:blur(5px); pointer-events:none; user-select:none; opacity:0.6; }}
.overlay {{ position:absolute; top:0; left:0; right:0; bottom:0; display:flex; align-items:center; justify-content:center;
  background:linear-gradient(to bottom,rgba(244,245,247,0) 0%,rgba(244,245,247,0.85) 30%,rgba(244,245,247,0.85) 100%); z-index:10; }}
.card {{ background:#fff; border:1px solid rgba(0,0,0,.09); border-radius:16px; padding:28px 32px; max-width:400px; width:90%; text-align:center; box-shadow:0 8px 32px rgba(0,0,0,.1); position:relative; overflow:hidden; }}
.card-top {{ position:absolute; top:0; left:0; right:0; height:3px; background:linear-gradient(90deg,#E8520A,#179948,transparent); }}
.lock {{ font-size:32px; margin-bottom:12px; }}
.title {{ font-family:'Syne',sans-serif; font-weight:800; font-size:20px; letter-spacing:-.02em; color:#141518; margin-bottom:10px; }}
.body {{ font-size:13px; color:#6B7280; line-height:1.6; margin-bottom:20px; }}
.btn-primary {{ display:inline-block; background:#E8520A; color:#fff; font-family:'DM Sans',sans-serif; font-weight:600; font-size:12px; padding:10px 24px; border-radius:8px; text-decoration:none; box-shadow:0 3px 14px rgba(232,82,10,.25); }}
.btn-secondary {{ display:inline-block; background:transparent; color:#E8520A; font-family:'DM Sans',sans-serif; font-weight:600; font-size:12px; padding:10px 24px; border-radius:8px; text-decoration:none; border:1px solid #E8520A; }}
</style></head><body>
  <div class="visible-wrap"><table>{visible_html}</table></div>
  {blur_block}
</body></html>"""

    components.html(html, height=total_height, scrolling=False)


# =====================================================
# FETCH FUNCTIONS
# =====================================================

def fetch_ticketmaster(lat, lon, radius, status, progress):
    """Fetch all TM events for lat/lon/radius and return event dict."""
    start_dt      = datetime.now(timezone.utc)
    end_limit     = start_dt + timedelta(days=30 * MONTHS_AHEAD)
    events        = {}
    window        = 0
    total_windows = max(1, (end_limit - start_dt).days // WINDOW_DAYS)

    while start_dt < end_limit:
        end_dt  = start_dt + timedelta(days=WINDOW_DAYS)
        window += 1
        status.text(f"Searching Ticketmaster "
                    f"({start_dt.strftime('%b %Y')})")

        page        = 0
        total_pages = 1

        while page < total_pages and page < TM_MAX_PAGES:
            params = {
                "apikey":        TICKETMASTER_API_KEY,
                "latlong":       f"{lat},{lon}",
                "radius":        radius,
                "unit":          "miles",
                "countryCode":   "GB",
                "size":          TM_PAGE_SIZE,
                "page":          page,
                "startDateTime": start_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "endDateTime":   end_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            }
            res = requests.get(TM_BASE_URL, params=params, timeout=15)
            if res.status_code == 429:
                time.sleep(2)
                continue
            if res.status_code != 200:
                raise RuntimeError(f"Ticketmaster API error {res.status_code}")

            data        = res.json()
            total_pages = min(data.get("page", {}).get("totalPages", 1), TM_MAX_PAGES)

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

        progress.progress(min(window / (total_windows * 2), 0.5))
        start_dt = end_dt

    return events


def fetch_skiddle(lat, lon, radius, status, progress):
    """Fetch all Skiddle events for lat/lon/radius and return event dict."""
    start_dt      = datetime.now(timezone.utc)
    end_limit     = start_dt + timedelta(days=30 * MONTHS_AHEAD)
    events        = {}
    window        = 0
    total_windows = max(1, (end_limit - start_dt).days // WINDOW_DAYS)

    while start_dt < end_limit:
        end_dt  = start_dt + timedelta(days=WINDOW_DAYS)
        window += 1
        status.text(f"Searching Skiddle "
                    f"({start_dt.strftime('%b %Y')})")
        offset = 0

        for _ in range(SK_MAX_PAGES):
            params = {
                "api_key":     SKIDDLE_API_KEY,
                "latitude":    lat,
                "longitude":   lon,
                "radius":      radius,
                "minDate":     start_dt.strftime("%Y-%m-%d"),
                "maxDate":     end_dt.strftime("%Y-%m-%d"),
                "limit":       SK_PAGE_SIZE,
                "offset":      offset,
                "description": 1,
                "getdistance": 1,
                "order":       "date",
            }
            res = requests.get(SKIDDLE_URL, params=params, timeout=15)
            if res.status_code == 429:
                time.sleep(2)
                continue
            if res.status_code != 200:
                raise RuntimeError(f"Skiddle API error {res.status_code}: {res.text}")

            data    = res.json()
            results = data.get("results", [])

            for e in results:
                venue       = e.get("venue") or {}
                event_id    = str(e.get("id", "")).strip()
                artists     = e.get("artists") or []
                artist_names = ", ".join(
                    a.get("artistname", "") for a in artists if a.get("artistname")
                )
                raw = (
                    str(e.get("eventname")) +
                    str(e.get("date")) +
                    str(venue.get("name")) +
                    str(venue.get("town"))
                )
                events[event_id] = {
                    "ID":          event_id,
                    "Name":        e.get("eventname"),
                    "Date":        e.get("date"),
                    "Time":        e.get("openingtimes", {}).get("doorsopen"),
                    "Venue Name":  venue.get("name"),
                    "Type":        EVENTCODE_MAP.get(e.get("EventCode"), e.get("EventCode")),
                    "City":        venue.get("town"),
                    "PostalCode":  venue.get("postcode"),
                    "Latitude":    venue.get("latitude"),
                    "Longitude":   venue.get("longitude"),
                    "url":         e.get("link"),
                    "Genres":      ", ".join(g.get("name", "") for g in e.get("genres") or [] if g.get("name")) or None,
                    "Artists":     artist_names or None,
                    "Distance":    e.get("distance"),
                    "Min Age":     e.get("minage"),
                    "Tickets URL": e.get("tickets") or e.get("link"),
                    "source":      "skiddle",
                    "event_hash":  hashlib.md5(raw.encode()).hexdigest(),
                    "last_seen_at": datetime.now(timezone.utc).isoformat(),
                }

            if len(results) < SK_PAGE_SIZE:
                break
            offset += SK_PAGE_SIZE
            time.sleep(0.2)

        progress.progress(0.5 + min(window / (total_windows * 2), 0.5))
        start_dt = end_dt

    return events


# =====================================================
# FIND & SYNC ALL EVENTS
# =====================================================

if find_events:
    _abort = False

    if not postcode:
        st.warning("Enter a postcode")
        _abort = True

    if not _abort:
        lat, lon = get_location(postcode)
        if lat is None:
            st.error("Invalid postcode")
            _abort = True

    if not _abort:
        progress = st.progress(0)
        status   = st.empty()

        before_total = supabase.table("BurdySteupTest").select("ID", count="exact").execute().count

        # ── TICKETMASTER ──
        try:
            tm_events = fetch_ticketmaster(lat, lon, radius, status, progress)
            tm_count  = upsert_batch(tm_events)
            status.text(f"✓ Ticketmaster: {tm_count} events processed")
        except RuntimeError as e:
            st.error(str(e))
            tm_count = 0

        # Update stat boxes with Ticketmaster count as soon as it's known
        stats_slot.markdown(_stat_row(tm_count, "—", "—", "—", "—", radius), unsafe_allow_html=True)

        # ── SKIDDLE ──
        try:
            sk_events = fetch_skiddle(lat, lon, radius, status, progress)
            sk_count  = upsert_batch(sk_events, strip_keys=SKIDDLE_ONLY)
            status.text(f"✓ Skiddle: {sk_count} events processed")
        except RuntimeError as e:
            st.error(str(e))
            sk_count = 0

        progress.progress(1.0)

        # ── AFTER COUNTS ──
        after_total = supabase.table("BurdySteupTest").select("ID", count="exact").execute().count
        after_radius_count = supabase.rpc(
            "count_within_radius",
            {"lat": lat, "lng": lon, "radius_meters": radius * 1609.34}
        ).execute().data
        after_radius_resp = supabase.rpc(
            "search_within_radius",
            {"lat": lat, "lng": lon, "radius_meters": radius * 1609.34}
        ).execute()

        st.session_state["search_df"]    = pd.DataFrame(after_radius_resp.data or [])
        st.session_state["search_label"] = (
            f"{after_radius_count} events within {radius} miles of {postcode.upper()}"
        )

        status.empty()
        progress.empty()

        # Final update with all real values
        stats_slot.markdown(
            _stat_row(tm_count, sk_count, after_total - before_total, after_radius_count, after_total, radius),
            unsafe_allow_html=True
        )


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
        st.session_state["search_label"] = (
            f"{len(st.session_state['search_df'])} events within "
            f"{radius} miles of {postcode.upper()}"
        )

df    = st.session_state.get("search_df", pd.DataFrame())
label = st.session_state.get("search_label", "")

if not df.empty:
    st.divider()
    st.subheader(label)
    st.caption(f"{len(df)} events found — showing preview")
    render_table(df)
