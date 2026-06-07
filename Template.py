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
    initial_sidebar_state="collapsed",
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

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
    padding: 0 3rem 80px !important;
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
/* Orange buttons — main content only, never in sidebar */
.main .stButton > button,
section.main .stButton > button,
[data-testid="stMainBlockContainer"] .stButton > button {
    font-family: 'DM Sans', sans-serif !important;
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
.main .stButton > button:hover,
section.main .stButton > button:hover,
[data-testid="stMainBlockContainer"] .stButton > button:hover {
    background: var(--orange-dim) !important;
    box-shadow: 0 5px 20px rgba(232,82,10,.3) !important;
    transform: translateY(-1px) !important;
}

/* Sidebar — hide nav buttons but restore collapse/expand toggle */
[data-testid="stSidebar"] .stButton,
[data-testid="stSidebar"] .stButton > button {
    display: none !important;
}

/* Native collapse button — visually hidden but in DOM so JS can click it */
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"] {
    position: fixed !important;
    width: 1px !important;
    height: 1px !important;
    opacity: 0 !important;
    overflow: hidden !important;
    z-index: -1 !important;
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
    font-family: 'DM Sans', sans-serif !important;
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
    font-family: 'DM Sans', sans-serif !important;
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
    margin-left: calc(-50vw + 50%);
    width: 100vw;
    margin-bottom: -80px;
    background: rgba(244,245,247,0.92);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    overflow: hidden;
    box-sizing: border-box;
    transition: margin-left 0.3s ease, width 0.3s ease;
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

/* =====================================================
   SIDEBAR
   ===================================================== */

/* Sidebar panel background & border */
[data-testid="stSidebar"] {
    background: var(--bg) !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: 2px 0 16px rgba(0,0,0,.06) !important;
}
[data-testid="stSidebar"] > div:first-child {
    background: var(--bg) !important;
    padding-top: 1rem !important;
}

/* Orange/green accent bar along the top of the sidebar */
[data-testid="stSidebar"]::after {
    content: '';
    position: absolute;
    top: 0; right: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, var(--orange), var(--green), transparent);
    z-index: 10;
}

/* Page nav links (stSidebarNavLink) */
[data-testid="stSidebarNavLink"] {
    border-radius: 8px !important;
    margin: 0 6px !important;
    padding: 0 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: -.01em !important;
    color: var(--text-dim) !important;
    transition: background .15s, color .15s !important;
    border: 1px solid transparent !important;
}
[data-testid="stSidebarNavLink"]:hover {
    background: var(--orange-glow) !important;
    color: var(--orange) !important;
    border-color: rgba(232,82,10,.2) !important;
}
[data-testid="stSidebarNavLink"][aria-current="page"],
[data-testid="stSidebarNavLink"].active {
    background: var(--orange-glow) !important;
    color: var(--orange) !important;
    border-color: rgba(232,82,10,.25) !important;
    font-weight: 600 !important;
}

/* Nav icons */
[data-testid="stSidebarNavLink"] svg {
    color: inherit !important;
}

/* Section headers / any markdown headings inside sidebar */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    letter-spacing: .08em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
    margin: 20px 0 8px !important;
}

/* Body text / captions in sidebar */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    color: var(--text-dim) !important;
}

/* Inputs inside sidebar */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] [data-baseweb="select"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
    color: var(--text) !important;
}
[data-testid="stSidebar"] input:focus {
    border-color: var(--orange) !important;
    box-shadow: 0 0 0 3px var(--orange-glow) !important;
}

/* Buttons inside sidebar */
/* Dividers inside sidebar */
[data-testid="stSidebar"] hr {
    border-top: 1px solid var(--border) !important;
    margin: 16px 0 !important;
}

/* Scrollbar inside sidebar */
[data-testid="stSidebar"] ::-webkit-scrollbar { width: 4px; }
[data-testid="stSidebar"] ::-webkit-scrollbar-track { background: var(--bg); }
[data-testid="stSidebar"] ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }


@media (max-width: 768px) {
    .block-container {
        padding: 0 1rem 60px !important;
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

    # Inject header directly into parent page DOM via components.html.
    # st.markdown runs inside an iframe so its JS cannot reliably access
    # window.parent.  components.html also runs in an iframe but its script
    # can reach window.parent (same origin), letting us inject the header
    # element and CSS straight into the real page and measure the sidebar.
    components.html(f"""
    <script>
    (function() {{
        var p = window.parent.document;

        // ── Inject CSS into parent <head> once ──────────────────────────────
        if (!p.getElementById('burdy-header-style')) {{
            var style = p.createElement('style');
            style.id = 'burdy-header-style';
            style.textContent = `
                @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');
                #burdy-header {{
                    position: fixed;
                    top: 0;
                    right: 0;
                    left: 0;
                    z-index: 1000;
                    background: rgba(244,245,247,0.92);
                    backdrop-filter: blur(8px);
                    -webkit-backdrop-filter: blur(8px);
                    padding: 0 3rem;
                    height: 80px;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    transition: left 0.3s ease;
                    box-sizing: border-box;
                }}
                #burdy-header::after {{
                    content: '';
                    position: absolute;
                    bottom: 0; left: 0; right: 0;
                    height: 3px;
                    background: linear-gradient(90deg, #E8520A, #179948, transparent);
                }}
                #burdy-header .burdy-logo {{ display: flex; align-items: center; gap: 12px; }}
                #burdy-header .live-badge {{
                    display: flex; align-items: center; gap: 8px;
                    background: #FFFFFF;
                    border: 1px solid rgba(0,0,0,.09);
                    border-radius: 999px; padding: 7px 16px;
                    font-family: 'DM Mono', monospace;
                    font-size: 11px; color: #6B7280;
                    box-shadow: 0 1px 4px rgba(0,0,0,.06);
                    flex-shrink: 0;
                }}
                #burdy-header .live-dot {{
                    width: 7px; height: 7px; border-radius: 50%;
                    background: #179948;
                    box-shadow: 0 0 6px #179948;
                    display: inline-block;
                }}
                #burdy-header .burdy-ticker-wrap {{ overflow: hidden; flex: 1; margin: 0 40px; }}
                #burdy-header .burdy-ticker-track {{
                    display: flex;
                    white-space: nowrap;
                    animation: burdy-ticker 18s linear infinite;
                }}
                #burdy-header .burdy-ticker-track:hover {{ animation-play-state: paused; }}
                #burdy-header .burdy-ticker-item {{
                    font-family: 'DM Mono', monospace;
                    font-size: 11px; color: #6B7280;
                    letter-spacing: .08em; text-transform: uppercase;
                    padding-right: 48px;
                }}
                #burdy-header .burdy-ticker-sep {{
                    color: #E8520A; padding-right: 48px;
                    font-size: 11px; font-family: 'DM Mono', monospace;
                }}
                @keyframes burdy-ticker {{
                    0%   {{ transform: translateX(0); }}
                    100% {{ transform: translateX(-50%); }}
                }}
                @media (max-width: 768px) {{
                    #burdy-header {{
                        padding: 0 1rem !important;
                        height: 56px !important;
                    }}
                    #burdy-header .burdy-ticker-wrap {{ display: none !important; }}
                    #burdy-header .live-badge {{ padding: 5px 10px !important; font-size: 10px !important; }}
                }}
            `;
            p.head.appendChild(style);
        }}

        // ── Inject header HTML into parent <body> once ──────────────────────
        if (!p.getElementById('burdy-header')) {{
            var header = p.createElement('div');
            header.id = 'burdy-header';
            header.innerHTML = `
                <div class="burdy-logo">
                    <img src="{BIRD_LOGO_URL}" style="display:block;height:clamp(40px,8vw,80px);" />
                    <img src="{WORD_LOGO_URL}" style="display:block;height:clamp(60px,12vw,150px);" />
                </div>
                <div class="burdy-ticker-wrap">
                    <div class="burdy-ticker-track">
                        <span class="burdy-ticker-item">Most searched event</span><span class="burdy-ticker-sep">&#9670;</span>
                        <span class="burdy-ticker-item">Biggest hotel demand</span><span class="burdy-ticker-sep">&#9670;</span>
                        <span class="burdy-ticker-item">Biggest 24 hour growth</span><span class="burdy-ticker-sep">&#9670;</span>
                        <span class="burdy-ticker-item">Newest event announced</span><span class="burdy-ticker-sep">&#9670;</span>
                        <span class="burdy-ticker-item">Biggest travel disruption</span><span class="burdy-ticker-sep">&#9670;</span>
                        <span class="burdy-ticker-item">Hospitality news</span><span class="burdy-ticker-sep">&#9670;</span>
                        <span class="burdy-ticker-item">Highest revenue event</span><span class="burdy-ticker-sep">&#9670;</span>
                        <span class="burdy-ticker-item">Newest venue announcement</span><span class="burdy-ticker-sep">&#9670;</span>
                        <span class="burdy-ticker-item">Most viewed event</span><span class="burdy-ticker-sep">&#9670;</span>
                        <span class="burdy-ticker-item">Weather impacts expected</span><span class="burdy-ticker-sep">&#9670;</span>
                    </div>
                </div>
                <div class="live-badge">
                    <span class="live-dot"></span>
                    Live
                </div>
            `;
            p.body.prepend(header);
        }}

        // ── Sidebar-aware left positioning ───────────────────────────────────
        function updateHeaderLeft() {{
            var header = p.getElementById('burdy-header');
            if (!header) return;

            var sidebar = p.querySelector('[data-testid="stSidebar"]');
            var sidebarW = sidebar ? sidebar.getBoundingClientRect().width : 0;

            // When collapsed, the sidebar shrinks but the toggle button floats
            // separately. Find its right edge so we never cover it.
            var toggleBtn = p.querySelector('[data-testid="stSidebarCollapsedControl"]')
                         || p.querySelector('[data-testid="stSidebarCollapseButton"]');
            var toggleRight = toggleBtn ? toggleBtn.getBoundingClientRect().right : 0;

            header.style.left = Math.max(sidebarW, toggleRight) + 'px';
        }}

        updateHeaderLeft();

        // Poll to track the sidebar CSS transition (opens/closes over ~300 ms)
        setInterval(updateHeaderLeft, 150);

        // MutationObserver as fast-path for instant response
        try {{
            new MutationObserver(updateHeaderLeft).observe(p.body, {{
                attributes: true, subtree: true,
                attributeFilter: ['style', 'class']
            }});
        }} catch(e) {{}}
    }})();
    </script>
    """, height=0)

    # ── Custom sidebar toggle injected into parent DOM ──────────────────────
    components.html("""
    <script>
    (function() {
        var p = window.parent.document;

        function ensureToggle() {
            var existing = p.getElementById('burdy-sidebar-toggle');
            if (existing) return existing;

            var toggle = p.createElement('button');
            toggle.id = 'burdy-sidebar-toggle';
            toggle.setAttribute('aria-label', 'Toggle sidebar');

            toggle.style.position        = 'fixed';
            toggle.style.top             = '50%';
            toggle.style.transform       = 'translateY(-50%)';
            toggle.style.zIndex          = '99999';
            toggle.style.width           = '20px';
            toggle.style.height          = '56px';
            toggle.style.background      = '#FFFFFF';
            toggle.style.border          = '1px solid rgba(0,0,0,0.12)';
            toggle.style.cursor          = 'pointer';
            toggle.style.boxShadow       = '2px 0 8px rgba(0,0,0,0.10)';
            toggle.style.display         = 'flex';
            toggle.style.alignItems      = 'center';
            toggle.style.justifyContent  = 'center';
            toggle.style.padding         = '0';
            toggle.style.fontSize        = '12px';
            toggle.style.color           = '#6B7280';
            toggle.style.lineHeight      = '1';
            toggle.style.left            = '200px';

            toggle.onmouseenter = function() {
                this.style.color       = '#E8520A';
                this.style.borderColor = 'rgba(232,82,10,0.4)';
            };
            toggle.onmouseleave = function() {
                this.style.color       = '#6B7280';
                this.style.borderColor = 'rgba(0,0,0,0.12)';
            };

            toggle.onclick = function() {
                var stBtn = p.querySelector('[data-testid="stSidebarCollapseButton"] button')
                         || p.querySelector('[data-testid="stSidebarCollapsedControl"] button');
                if (stBtn) stBtn.click();
            };

            p.body.appendChild(toggle);
            return toggle;
        }

        function positionToggle() {
            var toggle = ensureToggle();
            var sidebar = p.querySelector('[data-testid="stSidebar"]');
            var sidebarRight = sidebar ? sidebar.getBoundingClientRect().right : 0;
            var isCollapsed = sidebarRight < 10;

            if (isCollapsed) {
                toggle.style.left         = '0px';
                toggle.style.borderRadius = '0 6px 6px 0';
                toggle.style.borderLeft   = '0';
                toggle.innerHTML          = '&#10095;'; // ›
            } else {
                toggle.style.left         = sidebarRight + 'px';
                toggle.style.borderRadius = '0 6px 6px 0';
                toggle.style.borderLeft   = '0';
                toggle.innerHTML          = '&#10094;'; // ‹
            }
        }

        // Run immediately, then keep synced
        positionToggle();
        setInterval(positionToggle, 100);
        try {
            new MutationObserver(positionToggle).observe(p.body, {
                attributes: true, subtree: true,
                attributeFilter: ['style', 'class']
            });
        } catch(e) {}
    })();
    </script>
    """, height=1)



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
      window.addEventListener('resize', function() {
        var h = document.body.scrollHeight;
        if (window.frameElement) window.frameElement.style.height = h + 'px';
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
      @media (max-width: 600px) {
        .hero { flex-direction: column; min-height: unset; }
        .img-panel { display: none !important; }
        .centre { padding: 32px 20px 28px; }
        .headline { font-size: 20px; }
        .body-text { font-size: 13px; margin-bottom: 20px; }
        .stats { gap: 12px; }
        .stat-val { font-size: 16px; }
        .divider { display: none; }
      }
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
    <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
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
    .how-inner { display: flex; gap: 48px; align-items: stretch; }
    .how-left { flex: 1; min-width: 0; display: flex; flex-direction: column; }
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
    .how-steps { display: flex; flex-direction: column; gap: 4px; flex: 1; justify-content: space-between; }
    .how-step {
        display: flex; gap: 16px; padding: 16px 18px;
        border-radius: 12px; border: 1px solid transparent;
        cursor: pointer; transition: all .18s; background: transparent; position: relative;
        flex: 1; align-items: center;
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
        font-family: 'DM Sans', sans-serif; font-weight: 700;
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
    .pipe-node-title { font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 13px; color: var(--text); margin-bottom: 3px; }
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
          <h2 class="how-title">From raw events to <em>confident action</em></h2>
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
                <div class="step-desc">Burdy learns from your actuals. Feed back revenue, footfall, or staffing data and watch forecast accuracy improve every cycle.</div>
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
    window.addEventListener('resize', function() {
      var h = document.body.scrollHeight;
      if (window.frameElement) window.frameElement.style.height = h + 'px';
    });
    </script>
    """, height=520, scrolling=False)


    # =====================================================
    # MID-PAGE HERO
    # =====================================================

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
          var rect = wrapper.getBoundingClientRect();
          var offsetLeft  = rect.left;
          var offsetRight = window.parent.innerWidth - rect.right;
          wrapper.style.marginLeft  = '-' + offsetLeft  + 'px';
          wrapper.style.marginRight = '-' + offsetRight + 'px';
          wrapper.style.width       = window.parent.innerWidth + 'px';
          wrapper.style.maxWidth    = 'none';
          el.style.width            = '100%';
          el.style.maxWidth         = 'none';
          el.style.display          = 'block';
        } catch(e) {}
      });
    </script>
    <style>
      .hero2 {
        overflow: hidden;
        font-family: 'DM Sans', sans-serif;
        display: flex;
        align-items: stretch;
        min-height: 340px;
        width: 100%;
        position: relative;
        background: #F4F5F7;
      }
      /* Left and right plain background panels with text */
      .side2 {
        flex: 0 0 30%;
        background: #F4F5F7;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 40px 32px;
        text-align: center;
        position: relative;
        z-index: 2;
      }
      /* Centre image panel */
      .img-centre2 {
        flex: 0 0 40%;
        position: relative;
        overflow: hidden;
      }
      .img-centre2 img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center;
        display: block;
        animation: kenburns2 14s ease-in-out infinite alternate;
        transform-origin: center center;
      }
      @keyframes kenburns2 {
        0%   { transform: scale(1) translateX(0) translateY(0); }
        100% { transform: scale(1.08) translateX(-1%) translateY(-1%); }
      }
      /* Fade image edges into background */
      .img-centre2::before {
        content: '';
        position: absolute;
        inset: 0;
        z-index: 1;
        background: linear-gradient(to right,
          #F4F5F7 0%,
          transparent 18%,
          transparent 82%,
          #F4F5F7 100%);
      }
      .headline2 {
        font-weight: 800;
        font-size: 26px;
        letter-spacing: -.03em;
        color: #141518;
        margin-bottom: 12px;
        line-height: 1.2;
      }
      .body-text2 {
        font-size: 13px;
        color: #6B7280;
        line-height: 1.7;
        margin-bottom: 24px;
      }
      .stats2 {
        display: flex;
        flex-direction: column;
        gap: 16px;
        width: 100%;
      }
      .stat-row2 {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
      }
      .stat-val2 {
        font-weight: 800;
        font-size: 18px;
        color: #179948;
        letter-spacing: -.02em;
        white-space: nowrap;
      }
      .stat-lbl2 {
        font-family: 'DM Mono', monospace;
        font-size: 9px;
        color: #A0A7B4;
        letter-spacing: .06em;
        text-transform: uppercase;
        text-align: right;
        line-height: 1.4;
      }
      .stat-divider2 {
        height: 1px;
        background: rgba(0,0,0,.07);
        width: 100%;
      }
      @media (max-width: 600px) {
        .hero2 { flex-direction: column; min-height: unset; }
        .img-centre2 { display: none !important; }
        .side2 { flex: unset; width: 100%; padding: 28px 20px; }
        .headline2 { font-size: 20px; }
        .body-text2 { font-size: 13px; }
        .stat-val2 { font-size: 15px; }
      }
    </style>

    <div class="hero2">

      <!-- Left side: headline + description -->
      <div class="side2">
        <div class="headline2">What events do<br>for <span style="font-style:italic;color:#179948;">your business</span></div>
        <div class="body-text2">Every event creates a ripple of demand that reaches far beyond the venue gates. Hotels fill up, delivery orders spike, footfall shifts, and consumer spending concentrates in ways that are entirely predictable — if you have the right intelligence. From a major sporting fixture to a local food festival, Burdy connects your business to the events shaping your area, giving you the foresight to act before demand arrives.</div>
      </div>

      <!-- Centre: image only -->
      <div class="img-centre2">
        <img src="https://images.unsplash.com/photo-1531152369337-1d0b0b9ef20d?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" alt="City street crowd" />
      </div>

      <!-- Right side: stats -->
      <div class="side2">
        <div class="stats2">
          <div class="stat-row2">
            <div class="stat-val2">20,000+</div>
            <div class="stat-lbl2">Events tracked</div>
          </div>
          <div class="stat-divider2"></div>
          <div class="stat-row2">
            <div class="stat-val2">5</div>
            <div class="stat-lbl2">Industries served</div>
          </div>
          <div class="stat-divider2"></div>
          <div class="stat-row2">
            <div class="stat-val2">15 min</div>
            <div class="stat-lbl2">Update frequency</div>
          </div>
          <div class="stat-divider2"></div>
          <div class="stat-row2">
            <div class="stat-val2">90 days</div>
            <div class="stat-lbl2">Advance visibility</div>
          </div>
        </div>
      </div>

    </div>
    """, height=370, scrolling=False)

    st.markdown("<style>iframe[title='streamlit_components.v1.html'] { margin-bottom: -2rem !important; display: block; } .element-container:has(iframe) { margin-bottom: 0 !important; padding-bottom: 0 !important; } </style>", unsafe_allow_html=True)

    # =====================================================
    # WHO IS IT FOR
    # =====================================================

    components.html("""
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
:root {
    --orange:#E8520A; --orange-dim:#c94308; --orange-glow:rgba(232,82,10,.12);
    --green:#179948; --green-glow:rgba(23,153,72,.12);
    --bg:#F4F5F7; --surface:#FFFFFF; --surface2:#F0F1F4;
    --border:rgba(0,0,0,.09); --text:#141518; --text-dim:#6B7280; --text-muted:#A0A7B4;
}
*{box-sizing:border-box;margin:0;padding:0;}
html,body{background:var(--bg);font-family:'DM Sans',sans-serif;color:var(--text);overflow:hidden;}

.section{padding:40px 0 0;}
.section-label{font-family:'DM Mono',monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--text-muted);margin-bottom:10px;}
.section-title{font-family:'DM Sans',sans-serif;font-weight:800;font-size:26px;letter-spacing:-.03em;color:var(--text);line-height:1.2;margin-bottom:28px;}
.section-title em{font-style:italic;color:var(--orange);}

.panels-wrap{display:flex;gap:48px;align-items:stretch;}
.tabs-col{width:200px;flex-shrink:0;display:flex;flex-direction:column;gap:4px;justify-content:space-between;}
.tab{display:flex;align-items:center;gap:10px;padding:12px 14px;border-radius:10px;border:1px solid transparent;cursor:pointer;transition:all .18s;background:transparent;position:relative;flex:1;}
.tab.active{background:var(--surface);border-color:var(--border);box-shadow:0 2px 10px rgba(0,0,0,.06);}
.tab.active::before{content:'';position:absolute;left:0;top:10px;bottom:10px;width:3px;border-radius:0 2px 2px 0;background:linear-gradient(180deg,var(--orange),var(--green));}
.tab:hover:not(.active){background:var(--surface2);}
.tab-icon{font-size:16px;width:20px;text-align:center;}
.tab-label{font-family:'DM Sans',sans-serif;font-weight:500;font-size:13px;color:var(--text-dim);}
.tab.active .tab-label{color:var(--orange);font-weight:600;}

.panel-col{flex:1;min-width:0;}
.panel{display:none;}
.panel.active{display:flex;gap:32px;align-items:stretch;}

.panel-content{flex:1;min-width:0;}
.panel-tag{display:inline-block;background:var(--orange-glow);border:1px solid rgba(232,82,10,.2);border-radius:999px;padding:4px 12px;font-family:'DM Mono',monospace;font-size:10px;color:var(--orange);letter-spacing:.08em;text-transform:uppercase;margin-bottom:14px;}
.panel-title{font-family:'DM Sans',sans-serif;font-weight:800;font-size:18px;letter-spacing:-.02em;color:var(--text);line-height:1.3;margin-bottom:10px;}
.panel-desc{font-size:13px;line-height:1.6;color:var(--text-dim);margin-bottom:20px;}
.metrics{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
.metric{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:12px 14px;position:relative;overflow:hidden;}
.metric::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--orange),transparent);}
.metric-num{font-family:'DM Sans',sans-serif;font-size:22px;font-weight:800;color:var(--orange);letter-spacing:-.02em;margin-bottom:3px;}
.metric-label{font-family:'DM Mono',monospace;font-size:10px;color:var(--text-muted);letter-spacing:.04em;line-height:1.4;}

.panel-visual{width:280px;flex-shrink:0;background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:18px;position:relative;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.05);display:flex;flex-direction:column;}
.panel-visual::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,var(--orange),var(--green),transparent);}
.vis-label{font-family:'DM Mono',monospace;font-size:10px;color:var(--text-muted);letter-spacing:.06em;text-transform:uppercase;margin-bottom:14px;}

.bar-row{display:flex;align-items:center;gap:8px;margin-bottom:8px;}
.bar-name{font-family:'DM Mono',monospace;font-size:10px;color:var(--text-dim);width:110px;flex-shrink:0;}
.bar-track{flex:1;height:8px;background:var(--surface2);border-radius:4px;overflow:hidden;}
.bar-fill{height:100%;border-radius:4px;transition:width .6s ease;}
.bar-val{font-family:'DM Mono',monospace;font-size:10px;color:var(--orange);width:36px;text-align:right;flex-shrink:0;}

.sched-row{display:flex;align-items:center;gap:8px;margin-bottom:7px;}
.sched-day{font-family:'DM Mono',monospace;font-size:10px;width:44px;flex-shrink:0;}
.sched-bar{flex:1;height:10px;border-radius:4px;}
.sched-val{font-family:'DM Mono',monospace;font-size:10px;width:52px;text-align:right;flex-shrink:0;}

.venue-badges{display:flex;flex-direction:column;gap:8px;margin-top:12px;}
.venue-badge{display:flex;align-items:center;justify-content:space-between;padding:8px 12px;border-radius:8px;background:var(--surface2);border:1px solid var(--border);}
.venue-name{font-family:'DM Sans',sans-serif;font-size:12px;font-weight:500;color:var(--text);}
.venue-pct{font-family:'DM Mono',monospace;font-size:12px;font-weight:700;color:var(--orange);}

@media(max-width:640px){.panels-wrap{flex-direction:column;}.tabs-col{width:100%;flex-direction:row;flex-wrap:wrap;}.panel.active{flex-direction:column;}.panel-visual{width:100%;}}
</style>

<div class="section">
  <p class="section-label">Who is it for</p>
  <h2 class="section-title">Built for every team that <em>runs on demand</em></h2>

  <div class="panels-wrap">
    <div class="tabs-col" id="tabs">
      <div class="tab active" onclick="showPanel(0)"><span class="tab-icon">🏨</span><span class="tab-label">Hospitality</span></div>
      <div class="tab" onclick="showPanel(1)"><span class="tab-icon">🍔</span><span class="tab-label">Food & Delivery</span></div>
      <div class="tab" onclick="showPanel(2)"><span class="tab-icon">🛍</span><span class="tab-label">Retail</span></div>
      <div class="tab" onclick="showPanel(3)"><span class="tab-icon">🚕</span><span class="tab-label">Transport</span></div>
      <div class="tab" onclick="showPanel(4)"><span class="tab-icon">👥</span><span class="tab-label">Staffing</span></div>
    </div>

    <div class="panel-col" id="panels">

      <!-- Hospitality -->
      <div class="panel active">
        <div class="panel-content">
          <span class="panel-tag">🏨 Hospitality</span>
          <h3 class="panel-title">Stop leaving rooms empty when the city's full</h3>
          <p class="panel-desc">When 80,000 fans arrive for a stadium concert, your hotel should already know. Burdy gives revenue managers event context 90 days ahead — so every night is priced perfectly.</p>
          <div class="metrics">
            <div class="metric"><div class="metric-num">+31%</div><div class="metric-label">Average RevPAR uplift in event-adjacent periods</div></div>
            <div class="metric"><div class="metric-num">90</div><div class="metric-label">Days of advance visibility on high-demand nights</div></div>
            <div class="metric"><div class="metric-num">3.4×</div><div class="metric-label">Return on investment across hotel customers</div></div>
            <div class="metric"><div class="metric-num">94%</div><div class="metric-label">Forecast accuracy on 7-day occupancy spikes</div></div>
          </div>
        </div>
        <div class="panel-visual">
          <div class="vis-label">Demand score by event type</div>
          <div class="bar-row"><span class="bar-name">Stadium concerts</span><div class="bar-track"><div class="bar-fill" style="width:92%;background:linear-gradient(90deg,#E8520A,#179948);"></div></div><span class="bar-val">+92%</span></div>
          <div class="bar-row"><span class="bar-name">Major sports</span><div class="bar-track"><div class="bar-fill" style="width:78%;background:linear-gradient(90deg,#E8520A,#179948);"></div></div><span class="bar-val">+78%</span></div>
          <div class="bar-row"><span class="bar-name">Conferences</span><div class="bar-track"><div class="bar-fill" style="width:64%;background:linear-gradient(90deg,#E8520A,#179948);"></div></div><span class="bar-val">+64%</span></div>
          <div class="bar-row"><span class="bar-name">Public holidays</span><div class="bar-track"><div class="bar-fill" style="width:55%;background:linear-gradient(90deg,#179948,#E8520A);"></div></div><span class="bar-val">+55%</span></div>
          <div class="bar-row"><span class="bar-name">Exhibitions</span><div class="bar-track"><div class="bar-fill" style="width:41%;background:linear-gradient(90deg,#179948,#E8520A);"></div></div><span class="bar-val">+41%</span></div>
          <div style="margin-top:12px;font-family:'DM Mono',monospace;font-size:10px;color:var(--text-muted);">Avg. across 400+ properties · Last 12 months</div>
        </div>
      </div>

      <!-- Food & Delivery -->
      <div class="panel">
        <div class="panel-content">
          <span class="panel-tag">🍔 Food & Delivery</span>
          <h3 class="panel-title">Right riders, right zones — before demand peaks</h3>
          <p class="panel-desc">Match courier supply to demand before the surge hits. Burdy's 15-minute event updates let ops teams pre-position drivers and kitchens with up to 4-hour lead times.</p>
          <div class="metrics">
            <div class="metric"><div class="metric-num">–22%</div><div class="metric-label">Reduction in unfulfilled orders on event nights</div></div>
            <div class="metric"><div class="metric-num">4hrs</div><div class="metric-label">Average lead time for demand signal delivery</div></div>
            <div class="metric"><div class="metric-num">+18%</div><div class="metric-label">Gross order value on pre-positioned event days</div></div>
            <div class="metric"><div class="metric-num">60+</div><div class="metric-label">Cities with hyperlocal 500m-radius coverage</div></div>
          </div>
        </div>
        <div class="panel-visual">
          <div class="vis-label">Rider demand — Manchester centre</div>
          <div style="height:160px;position:relative;">
            <svg viewBox="0 0 240 140" width="100%" height="140" style="display:block;">
              <line x1="0" y1="70" x2="240" y2="70" stroke="rgba(0,0,0,.06)" stroke-width="1"/>
              <line x1="0" y1="35" x2="240" y2="35" stroke="rgba(0,0,0,.06)" stroke-width="1"/>
              <line x1="0" y1="105" x2="240" y2="105" stroke="rgba(0,0,0,.06)" stroke-width="1"/>
              <path d="M0 90 L40 88 L80 85 L120 80 L160 78 L200 76 L240 74" fill="none" stroke="rgba(0,0,0,.15)" stroke-width="1.5" stroke-dasharray="4 3"/>
              <path d="M0 90 L40 88 L80 82 L100 62 L120 38 L140 24 L160 32 L180 52 L200 72 L240 82" fill="none" stroke="#E8520A" stroke-width="2" stroke-linecap="round"/>
              <path d="M0 90 L40 88 L80 82 L100 62 L120 38 L140 24 L160 32 L180 52 L200 72 L240 82 L240 140 L0 140Z" fill="rgba(232,82,10,.07)"/>
              <line x1="140" y1="4" x2="140" y2="140" stroke="rgba(232,82,10,.3)" stroke-width="1" stroke-dasharray="3 3"/>
              <rect x="116" y="2" width="48" height="16" rx="3" fill="rgba(232,82,10,.12)"/>
              <text x="140" y="14" text-anchor="middle" font-family="DM Mono,sans-serif" font-size="8" fill="#E8520A">EVENT 20:00</text>
              <text x="4" y="136" font-family="DM Mono,sans-serif" font-size="8" fill="#A0A7B4">12:00</text>
              <text x="124" y="136" font-family="DM Mono,sans-serif" font-size="8" fill="#A0A7B4">20:00</text>
              <text x="210" y="136" font-family="DM Mono,sans-serif" font-size="8" fill="#A0A7B4">00:00</text>
            </svg>
          </div>
          <div style="display:flex;gap:16px;margin-top:8px;">
            <span style="display:flex;align-items:center;gap:5px;font-family:'DM Mono',monospace;font-size:10px;color:var(--text-muted);"><span style="display:inline-block;width:14px;height:2px;border-top:2px dashed rgba(0,0,0,.2);"></span>Baseline</span>
            <span style="display:flex;align-items:center;gap:5px;font-family:'DM Mono',monospace;font-size:10px;color:var(--text-muted);"><span style="display:inline-block;width:14px;height:2px;background:#E8520A;border-radius:1px;"></span>Event demand</span>
          </div>
        </div>
      </div>

      <!-- Retail -->
      <div class="panel">
        <div class="panel-content">
          <span class="panel-tag">🛍 Retail</span>
          <h3 class="panel-title">Stock the right items before the crowds arrive</h3>
          <p class="panel-desc">From football strips to festival gear, Burdy predicts product-level demand shifts based on nearby events — letting buyers and replenishment teams act weeks in advance.</p>
          <div class="metrics">
            <div class="metric"><div class="metric-num">–19%</div><div class="metric-label">Reduction in stockouts on high-demand event weekends</div></div>
            <div class="metric"><div class="metric-num">+27%</div><div class="metric-label">Increase in event-related category sell-through</div></div>
            <div class="metric"><div class="metric-num">21</div><div class="metric-label">Days average advance notice for replenishment</div></div>
            <div class="metric"><div class="metric-num">8,400+</div><div class="metric-label">Retail locations using Burdy globally</div></div>
          </div>
        </div>
        <div class="panel-visual">
          <div class="vis-label">Weekly footfall index — city centre</div>
          <div style="display:flex;align-items:flex-end;gap:6px;height:140px;padding-top:20px;">
            <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;"><div style="width:100%;background:rgba(232,82,10,.25);border-radius:4px 4px 0 0;height:30px;"></div><span style="font-family:'DM Mono',monospace;font-size:9px;color:var(--text-muted);">Mon</span></div>
            <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;"><div style="width:100%;background:rgba(232,82,10,.3);border-radius:4px 4px 0 0;height:40px;"></div><span style="font-family:'DM Mono',monospace;font-size:9px;color:var(--text-muted);">Tue</span></div>
            <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;"><div style="width:100%;background:rgba(232,82,10,.3);border-radius:4px 4px 0 0;height:35px;"></div><span style="font-family:'DM Mono',monospace;font-size:9px;color:var(--text-muted);">Wed</span></div>
            <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;"><div style="width:100%;background:rgba(232,82,10,.35);border-radius:4px 4px 0 0;height:45px;"></div><span style="font-family:'DM Mono',monospace;font-size:9px;color:var(--text-muted);">Thu</span></div>
            <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;position:relative;"><div style="position:absolute;top:-22px;left:50%;transform:translateX(-50%);background:rgba(232,82,10,.12);color:#E8520A;font-size:8px;padding:2px 6px;border-radius:4px;white-space:nowrap;font-family:'DM Mono',monospace;">Festival</div><div style="width:100%;background:#E8520A;border-radius:4px 4px 0 0;height:96px;"></div><span style="font-family:'DM Mono',monospace;font-size:9px;color:var(--orange);">Fri</span></div>
            <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;"><div style="width:100%;background:#179948;border-radius:4px 4px 0 0;height:118px;"></div><span style="font-family:'DM Mono',monospace;font-size:9px;color:var(--green);">Sat</span></div>
            <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;"><div style="width:100%;background:rgba(23,153,72,.5);border-radius:4px 4px 0 0;height:80px;"></div><span style="font-family:'DM Mono',monospace;font-size:9px;color:var(--text-muted);">Sun</span></div>
          </div>
        </div>
      </div>

      <!-- Transport -->
      <div class="panel">
        <div class="panel-content">
          <span class="panel-tag">🚕 Transport</span>
          <h3 class="panel-title">Get drivers where they need to be — before passengers ask</h3>
          <p class="panel-desc">Event-aware dispatch gives rideshare and taxi fleets a strategic advantage. Know when 20,000 people will be exiting a venue 6 hours before it happens.</p>
          <div class="metrics">
            <div class="metric"><div class="metric-num">–14%</div><div class="metric-label">Driver wait time during post-event surge periods</div></div>
            <div class="metric"><div class="metric-num">+35%</div><div class="metric-label">Trips completed per driver on event evenings</div></div>
            <div class="metric"><div class="metric-num">6hrs</div><div class="metric-label">Lead time for surge-zone pre-positioning alerts</div></div>
            <div class="metric"><div class="metric-num">98%</div><div class="metric-label">Event start-time accuracy within 15 minutes</div></div>
          </div>
        </div>
        <div class="panel-visual">
          <div class="vis-label">Surge zone pre-positioning</div>
          <div class="venue-badges">
            <div class="venue-badge"><span class="venue-name">Wembley Stadium</span><span class="venue-pct">+220%</span></div>
            <div class="venue-badge"><span class="venue-name">O2 Arena</span><span class="venue-pct">+180%</span></div>
            <div class="venue-badge"><span class="venue-name">Twickenham</span><span class="venue-pct">+95%</span></div>
            <div class="venue-badge"><span class="venue-name">AO Arena MCR</span><span class="venue-pct">+140%</span></div>
            <div class="venue-badge"><span class="venue-name">Tottenham Hotspur</span><span class="venue-pct">+160%</span></div>
          </div>
        </div>
      </div>

      <!-- Staffing -->
      <div class="panel">
        <div class="panel-content">
          <span class="panel-tag">👥 Staffing</span>
          <h3 class="panel-title">Schedule the right people — not just enough of them</h3>
          <p class="panel-desc">Workforce platforms can finally build rosters that reflect demand reality. Burdy's event feed flags demand spikes automatically with 2-week advance notice.</p>
          <div class="metrics">
            <div class="metric"><div class="metric-num">–28%</div><div class="metric-label">Reduction in last-minute shift scrambles</div></div>
            <div class="metric"><div class="metric-num">+16%</div><div class="metric-label">Employee satisfaction on event-week schedules</div></div>
            <div class="metric"><div class="metric-num">2 wks</div><div class="metric-label">Advance schedule building window enabled</div></div>
            <div class="metric"><div class="metric-num">40+</div><div class="metric-label">WFM platform integrations including Skedulo</div></div>
          </div>
        </div>
        <div class="panel-visual">
          <div class="vis-label">Roster demand signal — next 14 days</div>
          <div class="sched-row"><span class="sched-day" style="color:var(--text-muted);">Mon 2</span><div class="sched-bar" style="background:rgba(232,82,10,.18);"></div><span class="sched-val" style="color:var(--text-muted);">Normal</span></div>
          <div class="sched-row"><span class="sched-day" style="color:var(--text-muted);">Tue 3</span><div class="sched-bar" style="background:rgba(232,82,10,.2);"></div><span class="sched-val" style="color:var(--text-muted);">Normal</span></div>
          <div class="sched-row"><span class="sched-day" style="color:var(--text-muted);">Wed 4</span><div class="sched-bar" style="background:rgba(232,82,10,.2);"></div><span class="sched-val" style="color:var(--text-muted);">Normal</span></div>
          <div class="sched-row"><span class="sched-day" style="color:#c94308;">Thu 5</span><div class="sched-bar" style="background:rgba(232,82,10,.5);"></div><span class="sched-val" style="color:#c94308;">+45% ⚑</span></div>
          <div class="sched-row"><span class="sched-day" style="color:#E8520A;">Fri 6</span><div class="sched-bar" style="background:#E8520A;"></div><span class="sched-val" style="color:#E8520A;">+130% ⚑⚑</span></div>
          <div class="sched-row"><span class="sched-day" style="color:#E8520A;">Sat 7</span><div class="sched-bar" style="background:#179948;"></div><span class="sched-val" style="color:#179948;">+185% ⚑⚑</span></div>
          <div class="sched-row"><span class="sched-day" style="color:var(--text-muted);">Sun 8</span><div class="sched-bar" style="background:rgba(232,82,10,.25);"></div><span class="sched-val" style="color:var(--text-muted);">+30%</span></div>
          <p style="font-family:'DM Mono',monospace;font-size:10px;color:var(--text-muted);margin-top:12px;">⚑ Burdy-detected event driving demand spike</p>
        </div>
      </div>

    </div>
  </div>
</div>

<script>
function showPanel(i) {
  document.querySelectorAll('.tab').forEach((t,j) => t.classList.toggle('active', j===i));
  document.querySelectorAll('.panel').forEach((p,j) => p.classList.toggle('active', j===i));
  var h = document.body.scrollHeight;
  if (window.frameElement) window.frameElement.style.height = h + 'px';
}
window.addEventListener('load', function() {
  var h = document.body.scrollHeight;
  if (window.frameElement) window.frameElement.style.height = h + 'px';
});
</script>
""", height=440, scrolling=False)

    st.markdown("<style>iframe[title='streamlit_components.v1.html'] { margin-bottom: -2rem !important; display: block; } .element-container:has(iframe) { margin-bottom: 0 !important; padding-bottom: 0 !important; } </style>", unsafe_allow_html=True)

    # =====================================================
    # TRANSIENT TRADE HERO
    # =====================================================

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
          var rect = wrapper.getBoundingClientRect();
          var offsetLeft  = rect.left;
          var offsetRight = window.parent.innerWidth - rect.right;
          wrapper.style.marginLeft  = '-' + offsetLeft  + 'px';
          wrapper.style.marginRight = '-' + offsetRight + 'px';
          wrapper.style.width       = window.parent.innerWidth + 'px';
          wrapper.style.maxWidth    = 'none';
          el.style.width            = '100%';
          el.style.maxWidth         = 'none';
          el.style.display          = 'block';
        } catch(e) {}
      });
    </script>
    <style>
      .hero3 {
        overflow: hidden;
        font-family: 'DM Sans', sans-serif;
        display: flex;
        align-items: stretch;
        min-height: 340px;
        width: 100%;
        position: relative;
        background: #F4F5F7;
      }
      .img-left3 {
        flex: 0 0 45%;
        position: relative;
        overflow: hidden;
      }
      .img-left3 img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center 30%;
        display: block;
        animation: kenburns3 16s ease-in-out infinite alternate;
        transform-origin: center center;
      }
      @keyframes kenburns3 {
        0%   { transform: scale(1) translateX(0) translateY(0); }
        100% { transform: scale(1.07) translateX(1%) translateY(-1%); }
      }
      .img-left3::after {
        content: '';
        position: absolute;
        inset: 0;
        z-index: 1;
        background: linear-gradient(to right,
          transparent 70%,
          #F4F5F7 100%);
      }
      .text-right3 {
        flex: 1;
        background: #F4F5F7;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 52px 56px 52px 48px;
        position: relative;
        z-index: 2;
      }
      .pill3 {
        display: none;
      }
      .headline3 {
        font-weight: 800;
        font-size: 28px;
        letter-spacing: -.03em;
        color: #141518;
        line-height: 1.2;
        margin-bottom: 16px;
      }
      .headline3 em { font-style: italic; color: #179948; }
      .body3 {
        font-size: 14px;
        color: #6B7280;
        line-height: 1.8;
        margin-bottom: 28px;
        max-width: 480px;
      }
      .bullets3 {
        display: flex;
        flex-direction: column;
        gap: 10px;
      }
      .bullet3 {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        font-size: 13px;
        color: #6B7280;
        line-height: 1.5;
      }
      .bullet3-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #179948;
        flex-shrink: 0;
        margin-top: 6px;
      }
      @media (max-width: 600px) {
        .hero3 { flex-direction: column; min-height: unset; }
        .img-left3 { display: none !important; }
        .text-right3 { padding: 32px 20px; }
        .headline3 { font-size: 20px; }
        .body3 { font-size: 13px; margin-bottom: 20px; }
      }
    </style>

    <div class="hero3">

      <div class="img-left3">
        <img src="https://images.unsplash.com/photo-1653407980547-31786734695b?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" alt="Busy train station terminal" />
      </div>

      <div class="text-right3">
        <span class="pill3">Transient Trade</span>
        <div class="headline3">The crowd doesn't just go<br>to the event — they pass<br><em>right by your door</em></div>
        <p class="body3">When a stadium sells out or a festival floods the city, thousands of people spill into surrounding streets with time to spend and nowhere specific to be. That unplanned footfall is some of the highest-converting trade a local business will ever see — if they're ready for it.</p>
        <div class="bullets3">
          <div class="bullet3"><div class="bullet3-dot"></div><span><strong style="color:#141518;">Cafés &amp; restaurants</strong> near venues see walk-in covers spike up to 3× on event evenings — with no marketing spend.</span></div>
          <div class="bullet3"><div class="bullet3-dot"></div><span><strong style="color:#141518;">Convenience &amp; off-licence</strong> stores report basket sizes 40% higher when a major event is within 800m.</span></div>
          <div class="bullet3"><div class="bullet3-dot"></div><span><strong style="color:#141518;">Hotels on transit routes</strong> fill last-minute rooms at premium rates as attendees miss the last train home.</span></div>
        </div>
      </div>

    </div>
    """, height=480, scrolling=False)


    # =====================================================
    # COMPARISON
    # =====================================================

    components.html("""
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
:root {
    --orange:#E8520A; --orange-dim:#c94308; --orange-glow:rgba(232,82,10,.12);
    --green:#179948; --green-glow:rgba(23,153,72,.12);
    --bg:#F4F5F7; --surface:#FFFFFF; --surface2:#F0F1F4;
    --border:rgba(0,0,0,.09); --text:#141518; --text-dim:#6B7280; --text-muted:#A0A7B4;
}
*{box-sizing:border-box;margin:0;padding:0;}
html,body{background:var(--bg);font-family:'DM Sans',sans-serif;color:var(--text);overflow:hidden;}

.compare-section{padding:0 0 32px;}
.section-label{font-family:'DM Mono',monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--text-muted);margin-bottom:10px;text-align:left;}
.section-title{font-family:'DM Sans',sans-serif;font-weight:800;font-size:26px;letter-spacing:-.03em;color:var(--text);line-height:1.2;margin-bottom:0;text-align:left;}
.section-sub{font-size:14px;color:var(--text-dim);line-height:1.7;margin:16px 0 0;text-align:left;max-width:600px;}

.compare-table-wrap{margin-top:32px;overflow-x:auto;-webkit-overflow-scrolling:touch;border-radius:16px;box-shadow:0 2px 16px rgba(0,0,0,.07);}
.compare-table{min-width:560px;}
.compare-table{width:100%;border-collapse:collapse;background:var(--surface);font-family:'DM Sans',sans-serif;font-size:13px;}
.compare-table thead tr{background:var(--surface2);}
.compare-table th{padding:16px 20px;font-family:'DM Mono',monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--text-muted);font-weight:500;text-align:left;border-bottom:1px solid var(--border);}
.th-prism{color:var(--orange) !important;position:relative;}
.th-prism::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--orange),var(--green));}
.prism-badge{display:inline-block;background:var(--orange-glow);border:1px solid rgba(232,82,10,.3);border-radius:999px;padding:2px 8px;font-size:9px;color:var(--orange);letter-spacing:.1em;margin-left:6px;vertical-align:middle;}

.compare-table tbody tr{border-bottom:1px solid var(--border);transition:background .15s;}
.compare-table tbody tr:last-child{border-bottom:none;}
.compare-table tbody tr:hover{background:rgba(232,82,10,.03);}
.compare-table td{padding:14px 20px;color:var(--text-dim);vertical-align:middle;}
.compare-table td:first-child{font-weight:500;color:var(--text);font-size:13px;}
.td-prism{color:var(--text) !important;font-weight:500;background:rgba(232,82,10,.03);}

.check{color:var(--green);font-weight:700;margin-right:4px;}
.cross{color:#D1433A;font-weight:700;margin-right:4px;}
.partial{color:#c99a06;}
</style>

<div class="compare-section">
  <div>
    <p class="section-label">Why Burdy</p>
    <h2 class="section-title">How we compare</h2>
    <p class="section-sub">Not all event intelligence is equal. Here's how Burdy stacks up against the alternatives.</p>
  </div>
  <div class="compare-table-wrap">
    <table class="compare-table">
      <thead>
        <tr>
          <th style="width:32%;">Feature</th>
          <th class="th-prism">Burdy <span class="prism-badge">US</span></th>
          <th style="color:var(--text-muted);">PredictHQ</th>
          <th style="color:var(--text-muted);">Manual Research</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Global event coverage</td>
          <td class="td-prism">19M+ events, 180 countries</td>
          <td>500K+ events</td>
          <td><span class="cross">✕</span> Not scalable</td>
        </tr>
        <tr>
          <td>Refresh rate</td>
          <td class="td-prism"><span class="check">✓</span> Every 15 minutes</td>
          <td><span class="partial">~ Daily</span></td>
          <td><span class="cross">✕</span> Weekly at best</td>
        </tr>
        <tr>
          <td>AI demand scoring</td>
          <td class="td-prism"><span class="check">✓</span> 0–100 with confidence band</td>
          <td><span class="partial">~ Basic ranking</span></td>
          <td><span class="cross">✕</span> None</td>
        </tr>
        <tr>
          <td>Hyperlocal radius (500m)</td>
          <td class="td-prism"><span class="check">✓</span> 60+ cities</td>
          <td><span class="partial">~ City-level only</span></td>
          <td><span class="cross">✕</span></td>
        </tr>
        <tr>
          <td>Revenue attribution</td>
          <td class="td-prism"><span class="check">✓</span> Automated, per-event</td>
          <td><span class="cross">✕</span> Not available</td>
          <td><span class="cross">✕</span></td>
        </tr>
        <tr>
          <td>Native WFM / RMS connectors</td>
          <td class="td-prism"><span class="check">✓</span> 150+ integrations</td>
          <td><span class="partial">~ API only</span></td>
          <td><span class="cross">✕</span></td>
        </tr>
        <tr>
          <td>Setup time</td>
          <td class="td-prism">Under 1 afternoon</td>
          <td>2–4 weeks</td>
          <td>Ongoing manual effort</td>
        </tr>
        <tr>
          <td>Free trial</td>
          <td class="td-prism"><span class="check">✓</span> 14 days, no card</td>
          <td><span class="partial">~ Demo only</span></td>
          <td>N/A</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<script>
window.addEventListener('load', function() {
  var h = document.body.scrollHeight;
  if (window.frameElement) window.frameElement.style.height = h + 'px';
});
</script>
""", height=560, scrolling=False)

    st.markdown("<style>iframe[title='streamlit_components.v1.html'] { margin-bottom: -2rem !important; display: block; } .element-container:has(iframe) { margin-bottom: 0 !important; padding-bottom: 0 !important; } </style>", unsafe_allow_html=True)

    # =====================================================
    # WEATHER HERO
    # =====================================================

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
          var rect = wrapper.getBoundingClientRect();
          var offsetLeft  = rect.left;
          var offsetRight = window.parent.innerWidth - rect.right;
          wrapper.style.marginLeft  = '-' + offsetLeft  + 'px';
          wrapper.style.marginRight = '-' + offsetRight + 'px';
          wrapper.style.width       = window.parent.innerWidth + 'px';
          wrapper.style.maxWidth    = 'none';
          el.style.width            = '100%';
          el.style.maxWidth         = 'none';
          el.style.display          = 'block';
        } catch(e) {}
      });
    </script>
    <style>
      .hero4 {
        overflow: hidden;
        font-family: 'DM Sans', sans-serif;
        display: flex;
        align-items: stretch;
        min-height: 340px;
        width: 100%;
        position: relative;
        background: #F4F5F7;
      }
      .text-left4 {
        flex: 1;
        background: #F4F5F7;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 52px 48px 52px 56px;
        position: relative;
        z-index: 2;
      }
      .img-right4 {
        flex: 0 0 45%;
        position: relative;
        overflow: hidden;
      }
      .img-right4 img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center 60%;
        display: block;
        animation: kenburns4 16s ease-in-out infinite alternate;
        transform-origin: center center;
      }
      @keyframes kenburns4 {
        0%   { transform: scale(1) translateX(0) translateY(0); }
        100% { transform: scale(1.07) translateX(-1%) translateY(1%); }
      }
      .img-right4::before {
        content: '';
        position: absolute;
        inset: 0;
        z-index: 1;
        background: linear-gradient(to left,
          transparent 70%,
          #F4F5F7 100%);
      }
      .headline4 {
        font-weight: 800;
        font-size: 28px;
        letter-spacing: -.03em;
        color: #141518;
        line-height: 1.2;
        margin-bottom: 16px;
      }
      .headline4 em { font-style: italic; color: #179948; }
      .body4 {
        font-size: 14px;
        color: #6B7280;
        line-height: 1.8;
        margin-bottom: 28px;
        max-width: 480px;
      }
      .bullets4 {
        display: flex;
        flex-direction: column;
        gap: 10px;
      }
      .bullet4 {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        font-size: 13px;
        color: #6B7280;
        line-height: 1.5;
      }
      .bullet4-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #179948;
        flex-shrink: 0;
        margin-top: 6px;
      }
      @media (max-width: 600px) {
        .hero4 { flex-direction: column; min-height: unset; }
        .img-right4 { display: none !important; }
        .text-left4 { padding: 32px 20px; }
        .headline4 { font-size: 20px; }
        .body4 { font-size: 13px; margin-bottom: 20px; }
      }
    </style>

    <div class="hero4">

      <div class="text-left4">
        <div class="headline4">Weather changes plans.<br>Is your hospitality<br><em>ready for the shift?</em></div>
        <p class="body4">A sudden heatwave fills every beer garden and coastal hotel in hours. An unexpected cold snap empties restaurant terraces overnight. Weather doesn't just affect footfall — it reshapes it entirely, and businesses that don't see it coming are left scrambling with the wrong stock, wrong staff, and wrong pricing.</p>
        <div class="bullets4">
          <div class="bullet4"><div class="bullet4-dot"></div><span><strong style="color:#141518;">Hotels &amp; holiday lets</strong> see last-minute booking surges of up to 4× when a sunny weekend is forecast — leaving unprepared properties fully booked but underpriced.</span></div>
          <div class="bullet4"><div class="bullet4-dot"></div><span><strong style="color:#141518;">Pubs &amp; restaurants</strong> with outdoor space report up to 60% higher covers on warm evenings, with no time to call in extra staff.</span></div>
          <div class="bullet4"><div class="bullet4-dot"></div><span><strong style="color:#141518;">Coastal &amp; leisure venues</strong> face their busiest days with standard rotas — Burdy's weather signals give you 5-day advance notice to plan ahead.</span></div>
        </div>
      </div>

      <div class="img-right4">
        <img src="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0" alt="Busy sunny beach" />
      </div>

    </div>
    """, height=480, scrolling=False)

    st.markdown("<style>iframe[title='streamlit_components.v1.html'] { margin-bottom: -2rem !important; display: block; } .element-container:has(iframe) { margin-bottom: 0 !important; padding-bottom: 0 !important; } </style>", unsafe_allow_html=True)

    # =====================================================
    # PRICING
    # =====================================================

    components.html("""
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;700;800&display=swap" rel="stylesheet">
<style>
:root {
    --orange:#E8520A; --orange-dim:#c94308; --orange-glow:rgba(232,82,10,.12);
    --green:#179948; --green-glow:rgba(23,153,72,.12);
    --bg:#F4F5F7; --surface:#FFFFFF; --surface2:#F0F1F4;
    --border:rgba(0,0,0,.09); --text:#141518; --text-dim:#6B7280; --text-muted:#A0A7B4;
}
*{box-sizing:border-box;margin:0;padding:0;}
html,body{background:var(--bg);font-family:'DM Sans',sans-serif;color:var(--text);overflow:hidden;}

.pricing-section{padding:48px 0 40px;}
.pricing-inner{max-width:1100px;margin:0 auto;}
.section-label{font-family:'DM Mono',monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--text-muted);margin-bottom:10px;text-align:center;}
.section-title{font-family:'DM Sans',sans-serif;font-weight:800;font-size:26px;letter-spacing:-.03em;color:var(--text);line-height:1.2;text-align:center;}
.section-sub{font-size:14px;color:var(--text-dim);line-height:1.7;margin:16px auto 0;text-align:center;max-width:480px;}

.pricing-toggle{display:flex;align-items:center;justify-content:center;gap:10px;margin:28px 0;font-family:'DM Mono',monospace;font-size:12px;color:var(--text-dim);}
.toggle-pill{width:44px;height:24px;background:var(--orange);border-radius:999px;position:relative;cursor:pointer;transition:background .2s;}
.toggle-pill::after{content:'';position:absolute;top:3px;left:3px;width:18px;height:18px;background:#fff;border-radius:50%;transition:transform .2s;}
.toggle-pill.annual::after{transform:translateX(20px);}
.savings-tag{background:var(--green-glow);border:1px solid rgba(23,153,72,.25);border-radius:999px;padding:3px 10px;font-family:'DM Mono',monospace;font-size:10px;color:var(--green);letter-spacing:.06em;}

.pricing-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:8px;}
.price-card{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:28px 24px;position:relative;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,.06);display:flex;flex-direction:column;}
.price-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,var(--orange),var(--green),transparent);}
.price-card.featured{background:var(--surface);border-color:rgba(232,82,10,.35);box-shadow:0 4px 28px rgba(232,82,10,.15);}
.price-card.featured::before{background:linear-gradient(90deg,var(--orange),var(--green),transparent);}
.price-popular{display:inline-block;background:var(--orange-glow);border:1px solid rgba(232,82,10,.4);border-radius:999px;padding:3px 12px;font-family:'DM Mono',monospace;font-size:10px;color:var(--orange);letter-spacing:.08em;text-transform:uppercase;margin-bottom:14px;}
.price-tier{font-family:'DM Sans',sans-serif;font-weight:700;font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:var(--text-dim);margin-bottom:12px;}
.price-value{font-family:'DM Sans',sans-serif;font-weight:800;font-size:44px;letter-spacing:-.04em;color:var(--orange);line-height:1;margin-bottom:6px;}
.price-value sup{font-size:22px;vertical-align:super;line-height:0;}
.price-per{font-family:'DM Mono',monospace;font-size:11px;color:var(--text-muted);margin-bottom:16px;}
.price-desc{font-size:13px;color:var(--text-dim);line-height:1.6;margin-bottom:20px;}
.price-card.featured .price-desc{color:var(--text-dim);}
.price-divider{height:1px;background:var(--border);margin-bottom:20px;}
.price-features{list-style:none;display:flex;flex-direction:column;gap:9px;flex:1;margin-bottom:24px;}
.price-features li{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--text-dim);}
.price-card.featured .price-features li{color:var(--text);}
.pf-check{display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:4px;background:var(--green-glow);color:var(--green);font-size:10px;flex-shrink:0;}
.btn-plan{display:block;text-align:center;padding:12px;border-radius:8px;font-family:'DM Mono',monospace;font-size:11px;font-weight:500;letter-spacing:.06em;text-transform:uppercase;text-decoration:none;background:var(--surface2);border:1px solid var(--border);color:var(--text);transition:all .18s;margin-top:auto;}
.btn-plan:hover{background:var(--orange-glow);border-color:rgba(232,82,10,.3);color:var(--orange);}
.featured-btn{background:var(--orange);border:none;color:#fff;}
.featured-btn:hover{background:var(--orange-dim);opacity:1;color:#fff;box-shadow:0 5px 20px rgba(232,82,10,.3);}

@media(max-width:700px){
  .pricing-grid{grid-template-columns:1fr;}
  .pricing-section{padding:32px 0 24px;}
  .section-title{font-size:20px;}
  .price-value{font-size:34px;}
  .pricing-toggle{margin:20px 0;}
}
@media(max-width:480px){
  .pricing-inner{padding:0 4px;}
  .price-card{padding:20px 16px;}
}
</style>

<div class="pricing-section">
  <div class="pricing-inner">
    <div style="text-align:center;max-width:560px;margin:0 auto;">
      <p class="section-label">Pricing</p>
      <h2 class="section-title">Simple, transparent<br>pricing</h2>
      <p class="section-sub">Scale from one location to thousands. Cancel anytime.</p>
    </div>
    <div class="pricing-toggle">
      <span>Monthly</span>
      <div class="toggle-pill" id="billingToggle" onclick="toggleBilling()" title="Toggle billing period"></div>
      <span>Annual</span>
      <span class="savings-tag">Save 20%</span>
    </div>
    <div class="pricing-grid">

      <!-- Starter -->
      <div class="price-card">
        <div class="price-tier">Starter</div>
        <div class="price-value" id="p0"><sup>£</sup>149</div>
        <div class="price-per" id="pp0">per month · 1 location</div>
        <p class="price-desc">Perfect for independent hotels, restaurants, or single-site retailers getting started with event intelligence.</p>
        <div class="price-divider"></div>
        <ul class="price-features">
          <li><span class="pf-check">✓</span> Up to 1 location</li>
          <li><span class="pf-check">✓</span> 50,000 events / month</li>
          <li><span class="pf-check">✓</span> 7-day demand forecasts</li>
          <li><span class="pf-check">✓</span> REST API access</li>
          <li><span class="pf-check">✓</span> Email alerts</li>
          <li><span class="pf-check">✓</span> Community support</li>
        </ul>
        <a href="#" class="btn-plan">Start free trial</a>
      </div>

      <!-- Growth -->
      <div class="price-card featured">
        <div class="price-popular">Most popular</div>
        <div class="price-tier" style="color:#E8520A;">Growth</div>
        <div class="price-value" id="p1" style="background:linear-gradient(135deg,#E8520A,#179948);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;"><sup style="-webkit-text-fill-color:#E8520A;">£</sup>499</div>
        <div class="price-per" id="pp1">per month · up to 10 locations</div>
        <p class="price-desc">For multi-site operators, regional chains, and growing platforms that need depth and scale.</p>
        <div class="price-divider" style="background:rgba(232,82,10,0.3);"></div>
        <ul class="price-features">
          <li><span class="pf-check" style="background:var(--orange-glow);color:#E8520A;">✓</span> Up to 10 locations</li>
          <li><span class="pf-check" style="background:var(--orange-glow);color:#E8520A;">✓</span> Unlimited events</li>
          <li><span class="pf-check" style="background:var(--orange-glow);color:#E8520A;">✓</span> 90-day demand forecasts</li>
          <li><span class="pf-check" style="background:var(--orange-glow);color:#E8520A;">✓</span> Hyperlocal 500m radius</li>
          <li><span class="pf-check" style="background:var(--orange-glow);color:#E8520A;">✓</span> Webhook & Slack alerts</li>
          <li><span class="pf-check" style="background:var(--orange-glow);color:#E8520A;">✓</span> Revenue attribution</li>
          <li><span class="pf-check" style="background:var(--orange-glow);color:#E8520A;">✓</span> Priority support</li>
        </ul>
        <a href="#" class="btn-plan featured-btn">Start free trial</a>
      </div>

      <!-- Enterprise -->
      <div class="price-card">
        <div class="price-tier">Enterprise</div>
        <div class="price-value">Custom</div>
        <div class="price-per">tailored to your portfolio</div>
        <p class="price-desc">For enterprise groups, platforms with API resale, or organisations needing SLAs and custom data pipelines.</p>
        <div class="price-divider"></div>
        <ul class="price-features">
          <li><span class="pf-check">✓</span> Unlimited locations</li>
          <li><span class="pf-check">✓</span> Dedicated data pipeline</li>
          <li><span class="pf-check">✓</span> Custom ML models</li>
          <li><span class="pf-check">✓</span> White-label API option</li>
          <li><span class="pf-check">✓</span> SSO & SAML</li>
          <li><span class="pf-check">✓</span> 99.99% SLA</li>
          <li><span class="pf-check">✓</span> Dedicated CSM</li>
        </ul>
        <a href="#" class="btn-plan">Talk to sales</a>
      </div>

    </div>
  </div>
</div>

<script>
var annual = false;
var prices = [{m:149,a:119},{m:499,a:399}];
var pers = ['per month · 1 location','per month · up to 10 locations'];
var persA = ['per month · billed annually','per month · billed annually'];
function toggleBilling() {
  annual = !annual;
  document.getElementById('billingToggle').classList.toggle('annual', annual);
  [0,1].forEach(function(i) {
    document.getElementById('p'+i).childNodes[document.getElementById('p'+i).childNodes.length-1].nodeValue = (annual ? prices[i].a : prices[i].m);
    document.getElementById('pp'+i).textContent = annual ? persA[i] : pers[i];
  });
}
window.addEventListener('load', function() {
  var h = document.body.scrollHeight;
  if (window.frameElement) window.frameElement.style.height = h + 'px';
});
</script>
""", height=820, scrolling=False)


    # ── Footer: injected into parent DOM like the header ──────────────────
    components.html("""
    <script>
    (function() {
        var p = window.parent.document;

        if (!p.getElementById('burdy-footer-style')) {
            var style = p.createElement('style');
            style.id = 'burdy-footer-style';
            style.textContent = `
                @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');
                #burdy-footer {
                    position: fixed;
                    bottom: 0;
                    left: 0;
                    right: 0;
                    z-index: 1000;
                    background: rgba(244,245,247,0.92);
                    backdrop-filter: blur(8px);
                    -webkit-backdrop-filter: blur(8px);
                    padding: 14px 3rem;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    gap: 12px;
                    box-sizing: border-box;
                    transition: left 0.3s ease;
                }
                #burdy-footer::before {
                    content: '';
                    position: absolute;
                    top: 0; left: 0; right: 0;
                    height: 3px;
                    background: linear-gradient(90deg, #E8520A, #179948, transparent);
                }
                #burdy-footer .footer-copy {
                    font-family: 'DM Mono', monospace;
                    font-size: 11px;
                    color: #A0A7B4;
                    white-space: nowrap;
                }
                #burdy-footer .footer-badges { display: flex; gap: 8px; flex-wrap: nowrap; }
                #burdy-footer .footer-badge {
                    font-family: 'DM Mono', monospace;
                    font-size: 10px; letter-spacing: .08em; text-transform: uppercase;
                    padding: 4px 10px;
                    border: 1px solid rgba(0,0,0,.09);
                    border-radius: 4px;
                    color: #A0A7B4;
                    background: #FFFFFF;
                    text-decoration: none;
                    transition: border-color .15s, background .15s;
                }
                #burdy-footer .footer-badge:hover {
                    border-color: #E8520A;
                    background: rgba(232,82,10,.08);
                    color: #E8520A;
                }
            `;
            p.head.appendChild(style);
        }

        if (!p.getElementById('burdy-footer')) {
            var footer = p.createElement('div');
            footer.id = 'burdy-footer';
            footer.innerHTML = `
                <span class="footer-copy">© 2026 Burdy Business · Powered by blood, sweat and tears from Trish Burley and Cara Moody</span>
                <div class="footer-badges">
                    <a href="https://ticketmaster.co.uk" target="_blank" rel="noopener noreferrer" class="footer-badge">Ticketmaster.co.uk</a>
                    <a href="https://www.skiddle.com" target="_blank" rel="noopener noreferrer" class="footer-badge">Skiddle.com</a>
                    <a href="https://github.com" target="_blank" rel="noopener noreferrer" class="footer-badge">Github.com</a>
                    <a href="https://supabase.com" target="_blank" rel="noopener noreferrer" class="footer-badge">Supabase.com</a>
                    <a href="https://postcodes.io" target="_blank" rel="noopener noreferrer" class="footer-badge">PostCodes.io</a>
                    <a href="https://streamlit.io" target="_blank" rel="noopener noreferrer" class="footer-badge">Streamlit.io</a>
                    <a href="https://mapbox.com" target="_blank" rel="noopener noreferrer" class="footer-badge">Mapbox.com</a>
                </div>
            `;
            p.body.appendChild(footer);
        }

        function updateFooterLeft() {
            var footer = p.getElementById('burdy-footer');
            if (!footer) return;
            var sidebar = p.querySelector('[data-testid="stSidebar"]');
            var sidebarW = sidebar ? sidebar.getBoundingClientRect().width : 0;
            var toggleBtn = p.querySelector('[data-testid="stSidebarCollapsedControl"]')
                         || p.querySelector('[data-testid="stSidebarCollapseButton"]');
            var toggleRight = toggleBtn ? toggleBtn.getBoundingClientRect().right : 0;
            footer.style.left = Math.max(sidebarW, toggleRight) + 'px';
        }

        function updateFooterLeft() {
            var footer = p.getElementById('burdy-footer');
            if (!footer) return;
            var sidebar = p.querySelector('[data-testid="stSidebar"]');
            var sidebarW = sidebar ? sidebar.getBoundingClientRect().width : 0;
            var toggleBtn = p.querySelector('[data-testid="stSidebarCollapsedControl"]')
                         || p.querySelector('[data-testid="stSidebarCollapseButton"]');
            var toggleRight = toggleBtn ? toggleBtn.getBoundingClientRect().right : 0;
            footer.style.left = Math.max(sidebarW, toggleRight) + 'px';
        }

        updateFooterLeft();
        setInterval(updateFooterLeft, 150);
        try {
            new MutationObserver(updateFooterLeft).observe(p.body, {
                attributes: true, subtree: true,
                attributeFilter: ['style', 'class']
            });
        } catch(e) {}
    })();
    </script>
    """, height=0)
