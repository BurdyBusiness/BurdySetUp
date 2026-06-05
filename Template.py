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
.element-container:has(iframe) {
    margin-bottom: -1.5rem !important;
    line-height: 0 !important;
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

.burdy-footer-wrap {
    position: relative;
    margin-top: 48px;
    margin-left: -3rem;
    margin-right: -3rem;
    margin-bottom: -80px;
    background: rgba(244,245,247,0.92);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    overflow: hidden;
}
.burdy-footer-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--orange), var(--green), transparent);
}
.burdy-footer {
    padding: 14px 3rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: nowrap;
    gap: 12px;
}
.footer-copy {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: var(--text-muted);
    white-space: nowrap;
}
.footer-badges { display: flex; gap: 8px; flex-wrap: nowrap; }
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
    .burdy-footer-wrap { margin-left: -1rem; margin-right: -1rem; }
    .burdy-footer { padding: 10px 1rem; }
    .footer-badges { display: none; }
    .footer-copy { font-size: 10px; overflow: hidden; text-overflow: ellipsis; }
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


</style>
""", unsafe_allow_html=True)

# =====================================================
# CONFIG
# =====================================================

TICKETMASTER_API_KEY = st.secrets["TICKETMASTER_API_KEY"]
SKIDDLE_API_KEY      = st.secrets["SKIDDLE_API_KEY"]
SUPABASE_URL         = st.secrets["SUPABASE_URL"]
SUPABASE_KEY         = st.secrets["SUPABASE_SERVICE_ROLE_KEY"]

BIRD_LOGO_URL        = "https://ujrublkoqtpijwijklvq.supabase.co/storage/v1/object/sign/Brand%20Logo/Bird%20Logo%20Left.png?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV9jYTQwZTg5ZS00MTVkLTQ0NjEtYTZjZi00OTI2MDIwYmYyZTkiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJCcmFuZCBMb2dvL0JpcmQgTG9nbyBMZWZ0LnBuZyIsImlhdCI6MTc4MDU5ODM2NSwiZXhwIjoxODEyMTM0MzY1fQ.OMa5cbOtPSUZR4JTjlT3Mm1XBZlgi2rugZOQx7SLCX0"
WORD_LOGO_URL        = "https://ujrublkoqtpijwijklvq.supabase.co/storage/v1/object/sign/Brand%20Logo/Font%20logo.png?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV9jYTQwZTg5ZS00MTVkLTQ0NjEtYTZjZi00OTI2MDIwYmYyZTkiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJCcmFuZCBMb2dvL0ZvbnQgbG9nby5wbmciLCJpYXQiOjE3ODA2ODA3OTYsImV4cCI6MjA5NjA0MDc5Nn0.yI5FtOyAlXnLpf1Nbu4SFFUmVt9i4eSKQ17UTwRjHdE"

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

# Only render page content when this is the active page (not a subpage)
import pathlib
if pathlib.Path(__file__).stem == pathlib.Path(st.context.pages[st.context.active_page_id]["page_script_hash"] if hasattr(st.context, "pages") else __file__).stem:
    pass  # always true on main page — guard below uses simpler check

# Streamlit runs Template.py as base for all pages; guard content to home page only
_current_script = pathlib.Path(__file__).resolve()
_running_script = pathlib.Path(st.runtime.get_instance()._main_script_path).resolve() if hasattr(st, 'runtime') else _current_script

if _current_script == _running_script:
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
    .burdy-logo {{ display: flex; align-items: center; gap: 12px; }}
    .live-badge {{
        display: flex; align-items: center; gap: 8px;
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 999px; padding: 7px 16px;
        font-family: 'DM Mono', monospace;
        font-size: 11px; color: var(--text-dim);
        box-shadow: 0 1px 4px rgba(0,0,0,.06);
        flex-shrink: 0;
    }}
    .live-dot {{
        width: 7px; height: 7px; border-radius: 50%;
        background: var(--green);
        box-shadow: 0 0 6px var(--green);
        display: inline-block;
    }}
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
        <img src="{BIRD_LOGO_URL}" style="display:block;height:clamp(40px,8vw,80px);" />
        <img src="{WORD_LOGO_URL}" style="display:block;height:clamp(60px,12vw,150px);" />
      </div>
      <div class="ticker-wrap">
        <div class="ticker-track">
          <span class="ticker-item">Most searched event</span><span class="ticker-sep">◆</span>
          <span class="ticker-item">Biggest hotel demand</span><span class="ticker-sep">◆</span>
          <span class="ticker-item">Biggest 24 hour growth</span><span class="ticker-sep">◆</span>
          <span class="ticker-item">Newest event announced</span><span class="ticker-sep">◆</span>
          <span class="ticker-item">Biggest travel disruption</span><span class="ticker-sep">◆</span>
          <span class="ticker-item">Hospitality news</span><span class="ticker-sep">◆</span>
          <span class="ticker-item">Highest revenue event</span><span class="ticker-sep">◆</span>
          <span class="ticker-item">Newest venue announcement</span><span class="ticker-sep">◆</span>
          <span class="ticker-item">Most viewed event</span><span class="ticker-sep">◆</span>
          <span class="ticker-item">Weather impacts expected</span><span class="ticker-sep">◆</span>
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
        background: transparent;
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
        <img src="https://images.unsplash.com/photo-1506157786151-b8491531f063?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" alt="Festival crowd" />
      </div>

      <div class="centre">
        <div class="headline">Multiple Business Intelligence Models.<br>On one platform.</div>
        <div class="body-text">
          Burdy transforms real-world events into demand signals — so your pricing, staffing, and operations are always ahead of the curve. Every signal on one platform. From concerts to school holidays, we connect your business to over 20,000 events in real time.
        </div>
        <div class="stats">
          <div style="text-align:center;">
            <div class="stat-val">Multi-source</div>
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
            <div class="stat-lbl">Database sync</div>
          </div>
          <div class="divider"></div>
          <div style="text-align:center;">
            <div class="stat-val">UK-wide</div>
            <div class="stat-lbl">Postcode precision</div>
          </div>
        </div>
        <div style="display:flex;justify-content:center;gap:12px;margin:28px 0 0;flex-wrap:wrap;">
          <button onclick="window.open('https://www.youtube.com', '_blank')" style="
            display:inline-flex;align-items:center;gap:8px;
            font-family:'DM Mono',monospace;font-size:11px;font-weight:500;
            letter-spacing:.06em;text-transform:uppercase;text-decoration:none;
            padding:11px 22px;border-radius:8px;
            background:#ffffff;color:#E8520A;
            border:1px solid rgba(232,82,10,.35);
            box-shadow:0 2px 8px rgba(232,82,10,.1);
            transition:all .2s;cursor:pointer;"
            onmouseover="this.style.background='rgba(232,82,10,.06)';this.style.borderColor='#E8520A'"
            onmouseout="this.style.background='#ffffff';this.style.borderColor='rgba(232,82,10,.35)'">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none" style="flex-shrink:0">
              <circle cx="7" cy="7" r="6.5" stroke="#E8520A" stroke-width="1"/>
              <polygon points="5.5,4.5 10,7 5.5,9.5" fill="#E8520A"/>
            </svg>
            Watch 3 min demo
          </button>
          <button onclick="window.open('https://burdysetup-initial.streamlit.app', '_blank')" style="
            display:inline-flex;align-items:center;gap:8px;
            font-family:'DM Mono',monospace;font-size:11px;font-weight:500;
            letter-spacing:.06em;text-transform:uppercase;text-decoration:none;
            padding:11px 22px;border-radius:8px;
            background:#E8520A;color:#ffffff;
            border:1px solid #E8520A;
            box-shadow:0 3px 14px rgba(232,82,10,.25);
            transition:all .2s;"
            onmouseover="this.style.background='#c94308';this.style.boxShadow='0 5px 20px rgba(232,82,10,.35)'"
            onmouseout="this.style.background='#E8520A';this.style.boxShadow='0 3px 14px rgba(232,82,10,.25)'">
            Try for free
            <svg width="12" height="12" viewBox="0 0 12 12" fill="none" style="flex-shrink:0">
              <path d="M2 6h8M7 3l3 3-3 3" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </a>
        </div>
      </div>

      <div class="img-panel right">
        <img src="https://images.unsplash.com/photo-1556816214-fda351e4a7fb?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" />
      </div>

    </div>
    """, height=370, scrolling=False)

    # Remove gap between hero iframe and How it works section
    st.markdown("<style>iframe[title='streamlit_components.v1.html'] { margin-bottom: -2rem !important; display: block; } .element-container:has(iframe) { margin-bottom: 0 !important; padding-bottom: 0 !important; } </style>", unsafe_allow_html=True)


    # =====================================================
    # HOW IT WORKS
    # =====================================================

    components.html("""
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
    :root {
        --orange:      #E8520A;
        --orange-dim:  #c94308;
        --orange-glow: rgba(232,82,10,.12);
        --green:       #179948;
        --green-glow:  rgba(23,153,72,.12);
        --bg:          #F4F5F7;
        --surface:     #FFFFFF;
        --surface2:    #F0F1F4;
        --border:      rgba(0,0,0,.09);
        --text:        #141518;
        --text-dim:    #6B7280;
        --text-muted:  #A0A7B4;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body { background: var(--bg); font-family: 'DM Sans', sans-serif; color: var(--text); overflow: hidden; }

    .how-section { padding: 40px 0 32px; }
    .how-inner { display: flex; gap: 48px; align-items: flex-start; }
    .how-left { flex: 1; min-width: 0; }
    .how-right { width: 340px; flex-shrink: 0; }

    .how-label {
        font-family: 'DM Mono', monospace;
        font-size: 11px; letter-spacing: .1em; text-transform: uppercase;
        color: var(--text-muted); margin-bottom: 10px;
    }
    .how-title {
        font-family: 'DM Sans', sans-serif;
        font-weight: 800; font-size: 26px; letter-spacing: -.03em;
        color: var(--text); line-height: 1.2; margin-bottom: 28px;
    }
    .how-title em { font-style: italic; color: var(--orange); }
    .how-steps { display: flex; flex-direction: column; gap: 4px; }
    .how-step {
        display: flex; gap: 16px; padding: 16px 18px;
        border-radius: 12px; border: 1px solid transparent;
        cursor: pointer; transition: all .18s; background: transparent; position: relative;
    }
    .how-step.active {
        background: var(--surface); border-color: var(--border);
        box-shadow: 0 2px 10px rgba(0,0,0,.06);
    }
    .how-step.active::before {
        content: ''; position: absolute;
        left: 0; top: 12px; bottom: 12px; width: 3px;
        border-radius: 0 2px 2px 0;
        background: linear-gradient(180deg, var(--orange), var(--green));
    }
    .how-step:hover:not(.active) { background: var(--surface2); }
    .step-num {
        font-family: 'DM Mono', monospace; font-size: 12px; font-weight: 500;
        color: var(--text-muted); min-width: 24px; padding-top: 2px;
    }
    .how-step.active .step-num { color: var(--orange); }
    .step-title {
        font-family: 'Syne', sans-serif; font-weight: 700;
        font-size: 14px; letter-spacing: -.01em; color: var(--text); margin-bottom: 4px;
    }
    .step-desc { font-size: 13px; line-height: 1.55; color: var(--text-dim); display: none; }
    .how-step.active .step-desc { display: block; }

    .pipe-nodes { display: flex; flex-direction: column; }
    .pipe-node {
        background: var(--surface); border: 1px solid var(--border);
        border-radius: 12px; padding: 16px 18px;
        position: relative; overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,.05);
        transition: box-shadow .2s, border-color .2s;
    }
    .pipe-node.pipe-active {
        border-color: rgba(232,82,10,.35);
        box-shadow: 0 4px 16px var(--orange-glow);
    }
    .pipe-node::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; }
    .pipe-node-0::before { background: linear-gradient(90deg, var(--orange), var(--green), transparent); }
    .pipe-node-1::before { background: linear-gradient(90deg, var(--green), var(--orange), transparent); }
    .pipe-node-2::before { background: linear-gradient(90deg, var(--orange), transparent); }
    .pipe-node-3::before { background: linear-gradient(90deg, var(--green), transparent); }
    .pipe-node-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 13px; color: var(--text); margin-bottom: 3px; }
    .pipe-node-sub { font-family: 'DM Mono', monospace; font-size: 10px; color: var(--text-muted); letter-spacing: .04em; }
    .pipe-connector { display: flex; flex-direction: column; align-items: center; padding: 2px 0; }
    .pipe-line { width: 2px; height: 20px; background: linear-gradient(180deg, var(--orange), var(--green)); opacity: .4; }
    .pipe-arrow { width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent; border-top: 7px solid var(--green); opacity: .5; }
    .pipe-dots { display: flex; gap: 5px; margin-top: 6px; }
    .pipe-dot { width: 7px; height: 7px; border-radius: 50%; }
    .pipe-bars { display: flex; align-items: flex-end; gap: 3px; height: 20px; margin-top: 6px; }
    .pipe-bars span { width: 5px; border-radius: 2px 2px 0 0; background: var(--green); }
    .pipe-pulse { display: flex; gap: 6px; margin-top: 6px; }
    .pipe-pulse-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--orange); animation: ppulse 1.5s infinite; }
    .pipe-pulse-dot:nth-child(2) { animation-delay: .3s; }
    .pipe-pulse-dot:nth-child(3) { animation-delay: .6s; }
    @keyframes ppulse { 0%,100%{opacity:.7;transform:scale(1);}50%{opacity:.25;transform:scale(1.4);} }
    .pipe-loop { font-family: 'DM Mono', monospace; font-size: 10px; color: var(--orange); letter-spacing: .04em; margin-top: 6px; }

    @media (max-width: 640px) {
        .how-inner { flex-direction: column; }
        .how-right { width: 100%; }
        .how-title { font-size: 20px; }
    }
    </style>

    <div class="how-section">
      <div class="how-inner">
        <div class="how-left">
          <p class="how-label">How it works</p>
          <h2 class="how-title">From raw events to<br><em>confident action</em></h2>
          <div class="how-steps">
            <div class="how-step active" onclick="activate(0)">
              <span class="step-num">01</span>
              <div>
                <div class="step-title">Ingest — we collect everything</div>
                <div class="step-desc">Our crawlers monitor 3,000+ sources: ticketing platforms, government calendars, sports leagues, social signals, and live RSS feeds. Updated every 15 minutes.</div>
              </div>
            </div>
            <div class="how-step" onclick="activate(1)">
              <span class="step-num">02</span>
              <div>
                <div class="step-title">Enrich — we add business context</div>
                <div class="step-desc">Each event is scored for predicted attendance, local impact radius, category, and correlation to demand spikes in your vertical — built on 10 years of training data.</div>
              </div>
            </div>
            <div class="how-step" onclick="activate(2)">
              <span class="step-num">03</span>
              <div>
                <div class="step-title">Deliver — to wherever you work</div>
                <div class="step-desc">Push signals via API, webhook, or our native connectors. Your teams get event-aware dashboards, automated alerts, and ML-ready datasets.</div>
              </div>
            </div>
            <div class="how-step" onclick="activate(3)">
              <span class="step-num">04</span>
              <div>
                <div class="step-title">Optimise — and get smarter over time</div>
                <div class="step-desc">Prism learns from your actuals. Feed back revenue, footfall, or staffing data and watch forecast accuracy improve every cycle.</div>
              </div>
            </div>
          </div>
        </div>

        <div class="how-right">
          <div class="pipe-nodes">
            <div class="pipe-node pipe-node-0 pipe-active" id="pnode-0">
              <div class="pipe-node-title">Data Ingestion Layer</div>
              <div class="pipe-node-sub">3,000+ sources · 19M events</div>
              <div class="pipe-dots">
                <div class="pipe-dot" style="background:#E8520A"></div>
                <div class="pipe-dot" style="background:#179948"></div>
                <div class="pipe-dot" style="background:#c94308"></div>
                <div class="pipe-dot" style="background:#A0A7B4"></div>
              </div>
            </div>
            <div class="pipe-connector"><div class="pipe-line"></div><div class="pipe-arrow"></div></div>
            <div class="pipe-node pipe-node-1" id="pnode-1">
              <div class="pipe-node-title">AI Enrichment Engine</div>
              <div class="pipe-node-sub">Scoring · Impact radius · Demand curves</div>
              <div class="pipe-bars">
                <span style="height:10px;opacity:.6"></span>
                <span style="height:14px;opacity:.8"></span>
                <span style="height:8px;opacity:.5"></span>
                <span style="height:18px;opacity:.9"></span>
                <span style="height:12px;opacity:.7"></span>
              </div>
            </div>
            <div class="pipe-connector"><div class="pipe-line"></div><div class="pipe-arrow"></div></div>
            <div class="pipe-node pipe-node-2" id="pnode-2">
              <div class="pipe-node-title">Delivery & Integration</div>
              <div class="pipe-node-sub">API · Webhooks · Native connectors</div>
              <div class="pipe-pulse">
                <div class="pipe-pulse-dot"></div>
                <div class="pipe-pulse-dot"></div>
                <div class="pipe-pulse-dot"></div>
              </div>
            </div>
            <div class="pipe-connector"><div class="pipe-line"></div><div class="pipe-arrow"></div></div>
            <div class="pipe-node pipe-node-3" id="pnode-3">
              <div class="pipe-node-title">Continuous Learning</div>
              <div class="pipe-node-sub">Actuals feedback loop</div>
              <div class="pipe-loop">↺ improving every cycle</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <script>
    function activate(i) {
      document.querySelectorAll('.how-step').forEach((s,j) => s.classList.toggle('active', j===i));
      document.querySelectorAll('.pipe-node').forEach((n,j) => n.classList.toggle('pipe-active', j===i));
      // Resize iframe to fit content
      var h = document.body.scrollHeight;
      if (window.frameElement) window.frameElement.style.height = h + 'px';
    }
    // Set initial iframe height
    window.addEventListener('load', function() {
      var h = document.body.scrollHeight;
      if (window.frameElement) window.frameElement.style.height = h + 'px';
    });
    </script>
    """, height=520, scrolling=False)


    # ── Footer slot: rendered early so it's always in the DOM ──
    _badge_style = (
        "font-family:'DM Mono',monospace;font-size:10px;letter-spacing:.08em;"
        "text-transform:uppercase;padding:4px 10px;"
        "border:1px solid rgba(0,0,0,.09);border-radius:4px;"
        "color:#A0A7B4;background:#FFFFFF;text-decoration:none;"
        "display:inline-block;"
    )
    _footer_html = f"""
    <div style="
        position:relative;
        background:rgba(244,245,247,0.92);
        width:100vw;
        margin-left:calc(-50vw + 50%);
        margin-top:48px;
        backdrop-filter:blur(8px);
        -webkit-backdrop-filter:blur(8px);
        overflow:hidden;
    ">
      <div style="
          position:absolute;top:0;left:0;right:0;height:3px;
          background:linear-gradient(90deg,#E8520A,#179948,transparent);
      "></div>
      <div style="
          padding:14px 3rem;
          display:flex;
          align-items:center;
          justify-content:space-between;
          flex-wrap:nowrap;
          gap:12px;
      ">
        <div style="font-family:'DM Mono',monospace;font-size:11px;color:#A0A7B4;white-space:nowrap;">
          © 2026 Burdy Business · Powered by blood, sweat and tears from Trish Burley and Cara Moody
        </div>
        <div style="display:flex;gap:8px;flex-wrap:nowrap;">
          <a href="https://ticketmaster.co.uk" target="_blank" rel="noopener noreferrer" style="{_badge_style}">Ticketmaster.co.uk</a>
          <a href="https://www.skiddle.com" target="_blank" rel="noopener noreferrer" style="{_badge_style}">Skiddle.com</a>
          <a href="https://github.com" target="_blank" rel="noopener noreferrer" style="{_badge_style}">Github.com</a>
          <a href="https://supabase.com" target="_blank" rel="noopener noreferrer" style="{_badge_style}">Supabase.com</a>
          <a href="https://postcodes.io" target="_blank" rel="noopener noreferrer" style="{_badge_style}">PostCodes.io</a>
          <a href="https://streamlit.io" target="_blank" rel="noopener noreferrer" style="{_badge_style}">Streamlit.io</a>
          <a href="https://mapbox.com" target="_blank" rel="noopener noreferrer" style="{_badge_style}">Mapbox.com</a>
        </div>
      </div>
    </div>
    """
    footer_slot = st.empty()
    footer_slot.markdown(_footer_html, unsafe_allow_html=True)
