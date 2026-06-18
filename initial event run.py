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
div[data-testid="stTextInput"] small,
div[data-testid="stTextInput"] [data-testid="InputInstructions"] {
    display: none !important;
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

import streamlit as st
import streamlit.components.v1 as components

# =====================================================
# SIDEBAR — paste this entire block into any associated
# page, directly after st.set_page_config()
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

/* ── Sidebar panel ── */
[data-testid="stSidebar"] {
    background: var(--bg) !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: 2px 0 16px rgba(0,0,0,.06) !important;
}
[data-testid="stSidebar"] > div:first-child {
    background: var(--bg) !important;
    padding-top: 1rem !important;
}

/* Orange → green accent bar along right edge */
[data-testid="stSidebar"]::after {
    content: '';
    position: absolute;
    top: 0; right: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, var(--orange), var(--green), transparent);
    z-index: 10;
}

/* ── Nav links ── */
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
[data-testid="stSidebarNavLink"] svg { color: inherit !important; }

/* ── Headings ── */
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

/* ── Body text & labels ── */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    color: var(--text-dim) !important;
}

/* ── Inputs & selects ── */
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

/* ── Hide stButtons inside sidebar ── */
[data-testid="stSidebar"] .stButton,
[data-testid="stSidebar"] .stButton > button {
    display: none !important;
}

/* ── Dividers ── */
[data-testid="stSidebar"] hr {
    border-top: 1px solid var(--border) !important;
    margin: 16px 0 !important;
}

/* ── Scrollbar ── */
[data-testid="stSidebar"] ::-webkit-scrollbar { width: 4px; }
[data-testid="stSidebar"] ::-webkit-scrollbar-track { background: var(--bg); }
[data-testid="stSidebar"] ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

/* ── Native collapse button: hidden visually but NOT display:none
      so it stays in the DOM and JS can click it ── */
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"] {
    position: fixed !important;
    width: 1px !important;
    height: 1px !important;
    opacity: 0 !important;
    overflow: hidden !important;
    z-index: -1 !important;
}
</style>
""", unsafe_allow_html=True)


# ── Custom ‹ / › toggle ────────────────────────────────────────────────────
# Injects a slim tab that floats at the sidebar edge and clicks Streamlit's
# native (but visually hidden) collapse button.
# NOTE: the native button must NOT be display:none — see CSS above.
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

        toggle.style.position       = 'fixed';
        toggle.style.top            = '50%';
        toggle.style.transform      = 'translateY(-50%)';
        toggle.style.zIndex         = '99999';
        toggle.style.width          = '20px';
        toggle.style.height         = '56px';
        toggle.style.background     = '#FFFFFF';
        toggle.style.border         = '1px solid rgba(0,0,0,0.12)';
        toggle.style.borderLeft     = '0';
        toggle.style.borderRadius   = '0 6px 6px 0';
        toggle.style.cursor         = 'pointer';
        toggle.style.boxShadow      = '2px 0 8px rgba(0,0,0,0.10)';
        toggle.style.display        = 'flex';
        toggle.style.alignItems     = 'center';
        toggle.style.justifyContent = 'center';
        toggle.style.padding        = '0';
        toggle.style.fontSize       = '12px';
        toggle.style.color          = '#6B7280';
        toggle.style.lineHeight     = '1';

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
                     || p.querySelector('[data-testid="stSidebarCollapsedControl"] button')
                     || p.querySelector('[data-testid="stSidebarCollapseButton"]')
                     || p.querySelector('[data-testid="stSidebarCollapsedControl"]');
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
        toggle.style.left = (isCollapsed ? 0 : sidebarRight) + 'px';
        toggle.innerHTML  = isCollapsed ? '&#10095;' : '&#10094;';
    }

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
# CONFIG
# =====================================================

TICKETMASTER_API_KEY = st.secrets["TICKETMASTER_API_KEY"]
SKIDDLE_API_KEY      = st.secrets["SKIDDLE_API_KEY"]
SUPABASE_URL         = st.secrets["SUPABASE_URL"]
SUPABASE_KEY         = st.secrets["SUPABASE_SERVICE_ROLE_KEY"]
BIRD_LOGO_URL        = "https://ujrublkoqtpijwijklvq.supabase.co/storage/v1/object/sign/Brand%20Logo/Bird%20Logo%20Left.png?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV9jYTQwZTg5ZS00MTVkLTQ0NjEtYTZjZi00OTI2MDIwYmYyZTkiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJCcmFuZCBMb2dvL0JpcmQgTG9nbyBMZWZ0LnBuZyIsImlhdCI6MTc4MDU5ODM2NSwiZXhwIjoxODEyMTM0MzY1fQ.OMa5cbOtPSUZR4JTjlT3Mm1XBZlgi2rugZOQx7SLCX0"
WORD_LOGO_URL        = "https://ujrublkoqtpijwijklvq.supabase.co/storage/v1/object/sign/Brand%20Logo/Font%20logo.png?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV9jYTQwZTg5ZS00MTVkLTQ0NjEtYTZjZi00OTI2MDIwYmYyZTkiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJCcmFuZCBMb2dvL0ZvbnQgbG9nby5wbmciLCJpYXQiOjE3ODA1OTg0MTEsImV4cCI6MTgxMjEzNDQxMX0.pt-zS-TT80l_mp-_jGklDgtx8K2wc0uafgW36VDklbo"

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

col1, col2, col3, col4 = st.columns([2, 4, 1, 1])

with col1:
    postcode = st.text_input("Enter postcode", placeholder="e.g. B2 5RE")
with col2:
    radius = st.slider("Search radius (miles)", 1, 100, 10)
with col3:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    search_db = st.button("Search", use_container_width=True)
with col4:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    find_events = st.button("Fetch & Sync", use_container_width=True)

# ── Inject location button into the postcode text input via parent DOM ──
components.html("""
<script>
(function() {
  function inject() {
    var doc = window.parent.document;

    // Already injected — skip
    if (doc.getElementById('locate-btn')) return;

    // Find the first text input inside a stTextInput container
    var wrapper = doc.querySelector('[data-testid="stTextInput"]');
    if (!wrapper) { setTimeout(inject, 100); return; }

    var inputEl = wrapper.querySelector('input[type="text"]');
    if (!inputEl) { setTimeout(inject, 100); return; }

    // Style the input container as relative so we can absolutely position the button
    var inputContainer = inputEl.parentElement;
    inputContainer.style.position = 'relative';

    // Add right padding to the input so text doesn't go under the button
    inputEl.style.paddingRight = '130px';

    // Create the button
    var btn = doc.createElement('button');
    btn.id = 'locate-btn';
    btn.type = 'button';
    btn.innerHTML = '&#128205; Use my location';
    btn.style.cssText = [
      'position:absolute',
      'right:8px',
      'top:50%',
      'transform:translateY(-50%)',
      'font-family:DM Mono,monospace',
      'font-size:10px',
      'letter-spacing:.05em',
      'text-transform:uppercase',
      'background:transparent',
      'color:#E8520A',
      'border:1px solid rgba(232,82,10,.4)',
      'border-radius:5px',
      'padding:4px 10px',
      'cursor:pointer',
      'white-space:nowrap',
      'transition:background .2s,border-color .2s',
      'z-index:10',
      'line-height:1.4'
    ].join(';');

    btn.addEventListener('mouseenter', function() {
      btn.style.background = 'rgba(232,82,10,.08)';
      btn.style.borderColor = '#E8520A';
    });
    btn.addEventListener('mouseleave', function() {
      btn.style.background = 'transparent';
      btn.style.borderColor = 'rgba(232,82,10,.4)';
    });

    btn.addEventListener('click', function() {
      btn.disabled = true;
      btn.innerHTML = '&#9203; Locating&hellip;';

      if (!navigator.geolocation) {
        btn.innerHTML = '&#128205; Use my location';
        btn.disabled = false;
        alert('Geolocation is not supported by your browser.');
        return;
      }

      navigator.geolocation.getCurrentPosition(
        function(pos) {
          fetch('https://api.postcodes.io/postcodes?lon=' + pos.coords.longitude + '&lat=' + pos.coords.latitude)
            .then(function(r) { return r.json(); })
            .then(function(data) {
              var pc = data && data.result && data.result[0] && data.result[0].postcode;
              if (!pc) throw new Error('No postcode found');

              var setter = Object.getOwnPropertyDescriptor(window.parent.HTMLInputElement.prototype, 'value').set;
              setter.call(inputEl, pc);
              inputEl.dispatchEvent(new Event('input', { bubbles: true }));
              inputEl.dispatchEvent(new Event('change', { bubbles: true }));
              inputEl.focus();
              inputEl.dispatchEvent(new Event('blur', { bubbles: true }));

              btn.innerHTML = '&#10003; ' + pc;
              btn.disabled = false;
            })
            .catch(function() {
              btn.innerHTML = '&#128205; Use my location';
              btn.disabled = false;
              alert('Could not find a postcode for your location.');
            });
        },
        function() {
          btn.innerHTML = '&#128205; Use my location';
          btn.disabled = false;
          alert('Location access denied or unavailable.');
        },
        { timeout: 10000 }
      );
    });

    inputContainer.appendChild(btn);
  }

  // Wait for DOM to be ready
  if (window.parent.document.readyState === 'complete') {
    inject();
  } else {
    window.parent.document.addEventListener('DOMContentLoaded', inject);
    setTimeout(inject, 300);
  }
})();
</script>
""", height=1, scrolling=False)

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
    <div class="stat-num" id="new-events-num">{new_events}</div>
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

# Reserve the footer slot immediately so it is always in the DOM,
# even while the fetch progress bar is updating.
_footer_html = """
<div class="burdy-footer">
  <div class="footer-copy">© 2026 Burdy Business · Powered by blood, sweat and tears from Trish Burley and Cara Moody</div>
  <div class="footer-badges">
    <a class="footer-badge" href="https://ticketmaster.co.uk" target="_blank" rel="noopener noreferrer" style="text-decoration:none;">Ticketmaster.co.uk</a>
    <a class="footer-badge" href="https://www.skiddle.com" target="_blank" rel="noopener noreferrer" style="text-decoration:none;">Skiddle.com</a>
    <a class="footer-badge" href="https://github.com" target="_blank" rel="noopener noreferrer" style="text-decoration:none;">Github.com</a>
    <a class="footer-badge" href="https://supabase.com" target="_blank" rel="noopener noreferrer" style="text-decoration:none;">Supabase.com</a>
    <a class="footer-badge" href="https://postcodes.io" target="_blank" rel="noopener noreferrer" style="text-decoration:none;">PostCodes.io</a>
    <a class="footer-badge" href="https://streamlit.io" target="_blank" rel="noopener noreferrer" style="text-decoration:none;">Streamlit.io</a>
    <a class="footer-badge" href="https://mapbox.com" target="_blank" rel="noopener noreferrer" style="text-decoration:none;">Mapbox.com</a>
  </div>
</div>
"""
footer_slot = st.empty()
footer_slot.markdown(_footer_html, unsafe_allow_html=True)


# =====================================================
# HELPERS
# =====================================================

def burdy_new_events_modal(events):
    """Inject a new events modal into the parent DOM, shown when the stat number is clicked."""
    import json as _json
    unique = int(time.time() * 1000)

    safe_events = []
    for e in events:
        safe_events.append({
            "name":  e.get("Name") or "Unknown Event",
            "date":  (e.get("Date") or "")[:10],
            "venue": e.get("Venue Name") or "—",
            "type":  e.get("Type") or "—",
            "url":   e.get("url") or "",
        })
    events_json = _json.dumps(safe_events)

    components.html(f"""
<script>
(function() {{
  var _ts = {unique};
  var doc = window.parent.document;
  var events = {events_json};

  // Remove any previously injected modal
  var old = doc.getElementById('burdy-nem');
  if (old) old.remove();
  var oldS = doc.getElementById('burdy-nem-style');
  if (oldS) oldS.remove();

  if (!doc.getElementById('burdy-fonts')) {{
    var lnk = doc.createElement('link');
    lnk.id = 'burdy-fonts'; lnk.rel = 'stylesheet';
    lnk.href = 'https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400;500&display=swap';
    doc.head.appendChild(lnk);
  }}

  var style = doc.createElement('style');
  style.id = 'burdy-nem-style';
  style.textContent = `
    #burdy-nem {{
      display:none;position:fixed;inset:0;
      background:rgba(20,21,24,0.5);
      backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);
      align-items:center;justify-content:center;
      z-index:999999;
    }}
    #burdy-nem.show {{ display:flex;animation:bNemFade .18s ease; }}
    @keyframes bNemFade {{ from{{opacity:0}} to{{opacity:1}} }}
    #burdy-nem .box {{
      background:#fff;border-radius:16px;padding:28px 32px 24px;
      width:min(720px,92vw);max-height:80vh;
      position:relative;overflow:hidden;display:flex;flex-direction:column;
      box-shadow:0 24px 60px rgba(0,0,0,.2),0 4px 16px rgba(0,0,0,.10);
      animation:bNemUp .2s ease;
    }}
    @keyframes bNemUp {{ from{{transform:translateY(16px);opacity:0}} to{{transform:translateY(0);opacity:1}} }}
    #burdy-nem .box::before {{
      content:'';position:absolute;top:0;left:0;right:0;height:3px;
      background:linear-gradient(90deg,#E8520A,#179948,transparent);
    }}
    #burdy-nem .hd {{
      display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;
    }}
    #burdy-nem .ttl {{
      font-family:'Syne',sans-serif;font-weight:800;font-size:16px;
      letter-spacing:-.02em;color:#141518;
    }}
    #burdy-nem .xcl {{
      background:none;border:none;cursor:pointer;font-size:18px;
      color:#A0A7B4;padding:4px;transition:color .15s;line-height:1;
    }}
    #burdy-nem .xcl:hover {{ color:#141518; }}
    #burdy-nem .scr {{
      overflow-y:auto;flex:1;border-radius:8px;
      border:1px solid rgba(0,0,0,.08);
    }}
    #burdy-nem table {{ width:100%;border-collapse:collapse;background:#fff; }}
    #burdy-nem thead th {{
      padding:10px 12px;text-align:left;
      font-family:'DM Mono',monospace;font-size:9px;
      letter-spacing:.1em;text-transform:uppercase;color:#A0A7B4;
      background:#F4F5F7;border-bottom:1px solid rgba(0,0,0,.08);
      position:sticky;top:0;
    }}
    #burdy-nem td {{
      padding:10px 12px;border-bottom:1px solid rgba(0,0,0,.06);
      font-size:12px;font-family:'DM Sans',sans-serif;color:#141518;
    }}
    #burdy-nem td.dc,#burdy-nem td.vc,#burdy-nem td.tc {{ color:#6B7280; }}
    #burdy-nem td.dc {{ white-space:nowrap; }}
    #burdy-nem .ft {{ margin-top:16px;text-align:center; }}
    #burdy-nem .btn {{
      font-family:'Syne',sans-serif;font-weight:700;font-size:11px;
      letter-spacing:.08em;text-transform:uppercase;
      background:#E8520A;color:#fff;border:none;border-radius:8px;
      padding:10px 28px;cursor:pointer;
      box-shadow:0 3px 14px rgba(232,82,10,.3);
      transition:background .2s,transform .15s,box-shadow .2s;
    }}
    #burdy-nem .btn:hover {{
      background:#c94308;transform:translateY(-1px);
      box-shadow:0 5px 20px rgba(232,82,10,.4);
    }}
  `;
  doc.head.appendChild(style);

  var modal = doc.createElement('div');
  modal.id = 'burdy-nem';
  modal.innerHTML =
    '<div class="box">'
    + '<div class="hd"><div class="ttl">&#127381; Newest Events Added</div>'
    + '<button class="xcl" id="burdy-nem-x">&#10005;</button></div>'
    + '<div class="scr"><table>'
    + '<thead><tr><th>Event</th><th>Date</th><th>Venue</th><th>Type</th></tr></thead>'
    + '<tbody id="burdy-nem-tbody"></tbody>'
    + '</table></div>'
    + '<div class="ft"><button class="btn" id="burdy-nem-close">Close</button></div>'
    + '</div>';
  doc.body.appendChild(modal);

  // Build rows via DOM so special characters can never break the JS
  var tbody = doc.getElementById('burdy-nem-tbody');
  events.forEach(function(e) {{
    var tr = doc.createElement('tr');
    var tdName = doc.createElement('td');
    if (e.url) {{
      var a = doc.createElement('a');
      a.href = e.url; a.target = '_blank'; a.rel = 'noopener noreferrer';
      a.style.cssText = 'color:#E8520A;text-decoration:none;font-weight:500;';
      a.textContent = e.name;
      tdName.appendChild(a);
    }} else {{
      tdName.textContent = e.name;
    }}
    var tdDate  = doc.createElement('td'); tdDate.className  = 'dc'; tdDate.textContent  = e.date  || '—';
    var tdVenue = doc.createElement('td'); tdVenue.className = 'vc'; tdVenue.textContent = e.venue || '—';
    var tdType  = doc.createElement('td'); tdType.className  = 'tc'; tdType.textContent  = e.type  || '—';
    tr.appendChild(tdName); tr.appendChild(tdDate); tr.appendChild(tdVenue); tr.appendChild(tdType);
    tbody.appendChild(tr);
  }});

  function show() {{ modal.classList.add('show'); }}
  function dismiss() {{
    modal.style.opacity = '0';
    modal.style.transition = 'opacity .15s ease';
    setTimeout(function() {{ modal.style.opacity=''; modal.style.transition=''; modal.classList.remove('show'); }}, 150);
  }}

  doc.getElementById('burdy-nem-close').addEventListener('click', dismiss);
  doc.getElementById('burdy-nem-x').addEventListener('click', dismiss);
  modal.addEventListener('click', function(e) {{ if (e.target === modal) dismiss(); }});
  doc.addEventListener('keydown', function handler(e) {{
    if (e.key === 'Escape') {{ dismiss(); doc.removeEventListener('keydown', handler); }}
  }});

  // Attach click to the stat number — retry until it appears in the DOM
  function attachClick() {{
    var el = doc.getElementById('new-events-num');
    if (el) {{
      el.style.cursor = 'pointer';
      el.onclick = show;
    }} else {{
      setTimeout(attachClick, 200);
    }}
  }}
  attachClick();
}})();
</script>
""", height=1, scrolling=False)


def burdy_error(message):
    """Inject a Burdy-styled modal directly into the parent page DOM so it overlays everything."""
    safe = message.replace("'", "\\'").replace("\n", " ")
    unique = int(time.time() * 1000)
    components.html(f"""
<script>
(function() {{
  var _ts = {unique}; // forces Streamlit to treat this as a new component each call
  // Remove any existing modal
  var old = window.parent.document.getElementById('burdy-error-modal');
  if (old) old.remove();

  // Inject Google Fonts into parent if not already there
  if (!window.parent.document.getElementById('burdy-fonts')) {{
    var link = window.parent.document.createElement('link');
    link.id = 'burdy-fonts';
    link.rel = 'stylesheet';
    link.href = 'https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap';
    window.parent.document.head.appendChild(link);
  }}

  var css = `
    #burdy-error-modal {{
      position: fixed;
      inset: 0;
      background: rgba(20,21,24,0.5);
      backdrop-filter: blur(4px);
      -webkit-backdrop-filter: blur(4px);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 999999;
      animation: burdyFadeIn .18s ease;
    }}
    @keyframes burdyFadeIn {{ from {{ opacity:0 }} to {{ opacity:1 }} }}
    #burdy-error-modal .bm {{
      background: #fff;
      border-radius: 16px;
      padding: 32px 36px 28px;
      max-width: 460px;
      width: 90%;
      position: relative;
      overflow: hidden;
      box-shadow: 0 24px 60px rgba(0,0,0,.2), 0 4px 16px rgba(0,0,0,.10);
      animation: burdySlideUp .2s ease;
    }}
    @keyframes burdySlideUp {{ from {{ transform:translateY(16px);opacity:0 }} to {{ transform:translateY(0);opacity:1 }} }}
    #burdy-error-modal .bm::before {{
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0; height: 3px;
      background: linear-gradient(90deg, #E8520A, #c94308, transparent);
    }}
    #burdy-error-modal .bm-title {{
      font-family: 'Syne', sans-serif;
      font-weight: 800;
      font-size: 16px;
      letter-spacing: -.02em;
      color: #141518;
      margin-bottom: 8px;
    }}
    #burdy-error-modal .bm-msg {{
      font-family: 'DM Sans', sans-serif;
      font-size: 13px;
      color: #6B7280;
      line-height: 1.65;
      margin-bottom: 24px;
    }}
    #burdy-error-modal .bm-btn {{
      font-family: 'Syne', sans-serif;
      font-weight: 700;
      font-size: 11px;
      letter-spacing: .08em;
      text-transform: uppercase;
      background: #E8520A;
      color: #fff;
      border: none;
      border-radius: 8px;
      padding: 10px 24px;
      cursor: pointer;
      transition: background .2s, transform .15s, box-shadow .2s;
      box-shadow: 0 3px 14px rgba(232,82,10,.3);
    }}
    #burdy-error-modal .bm-btn:hover {{
      background: #c94308;
      transform: translateY(-1px);
      box-shadow: 0 5px 20px rgba(232,82,10,.4);
    }}
  `;

  var style = window.parent.document.createElement('style');
  style.id = 'burdy-error-style';
  var oldStyle = window.parent.document.getElementById('burdy-error-style');
  if (oldStyle) oldStyle.remove();
  style.textContent = css;
  window.parent.document.head.appendChild(style);

  var modal = window.parent.document.createElement('div');
  modal.id = 'burdy-error-modal';
  modal.innerHTML = `
    <div class="bm">
      <div class="bm-title">Invalid Postcode</div>
      <div class="bm-msg">{safe}</div>
      <div style="text-align:center;"><button class="bm-btn" id="burdy-dismiss">Dismiss</button></div>
    </div>
  `;
  window.parent.document.body.appendChild(modal);

  function dismiss() {{
    var m = window.parent.document.getElementById('burdy-error-modal');
    if (m) {{
      m.style.opacity = '0';
      m.style.transition = 'opacity .15s ease';
      setTimeout(function() {{ m.remove(); }}, 150);
    }}
  }}

  window.parent.document.getElementById('burdy-dismiss').addEventListener('click', dismiss);
  modal.addEventListener('click', function(e) {{ if (e.target === modal) dismiss(); }});
  window.parent.document.addEventListener('keydown', function handler(e) {{
    if (e.key === 'Escape') {{ dismiss(); window.parent.document.removeEventListener('keydown', handler); }}
  }});
}})();
</script>
""", height=1, scrolling=False)


def classify_postcode(raw):
    """Return 'uk' if the format matches a UK postcode, else 'non_uk'."""
    import re
    pc = raw.strip().upper().replace(" ", "")
    if re.fullmatch(r"[A-Z]{1,2}[0-9][0-9A-Z]?[0-9][A-Z]{2}", pc):
        return "uk"
    return "non_uk"


def get_location(postcode_input):
    geo = requests.get(
        POSTCODE_API.format(postcode_input.replace(" ", "").upper())
    ).json()
    if not geo.get("result"):
        return None, None, None
    r = geo["result"]
    info = {
        "postcode":          r.get("postcode"),
        "admin_district":    r.get("admin_district"),
        "admin_district_code": r.get("codes", {}).get("admin_district"),
        "admin_county":      r.get("admin_county"),
        "admin_ward":        r.get("admin_ward"),
        "parish":            r.get("parish"),
        "region":            r.get("region"),
        "country":           r.get("country"),
        "parliamentary_constituency": r.get("parliamentary_constituency"),
        "nhs_ha":            r.get("nhs_ha"),
    }
    return r["latitude"], r["longitude"], info


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
    cols = list(data_df.columns)

    # Find the actual column names regardless of casing
    col_lower = {c.lower(): c for c in cols}
    name_col  = col_lower.get("name")
    url_col   = col_lower.get("url")

    # Display all columns except the url column
    display_cols = [c for c in cols if c != url_col]

    headers = "".join(
        f"<th style='padding:10px 14px;text-align:left;font-family:DM Mono,monospace;"
        f"font-size:11px;color:#6B7280;letter-spacing:.08em;text-transform:uppercase;"
        f"border-bottom:1px solid rgba(0,0,0,.09);background:#fff;white-space:nowrap;'>{col}</th>"
        for col in display_cols
    )
    rows_html = []
    for _, row in data_df.iterrows():
        cells = []
        for col in display_cols:
            val = row[col] if pd.notna(row[col]) else ""
            if col == name_col and url_col:
                url_val = row.get(url_col, "")
                if pd.notna(url_val) and str(url_val).startswith("http"):
                    cell = (
                        f"<td style='padding:10px 14px;border-bottom:1px solid rgba(0,0,0,.06);"
                        f"font-size:13px;font-family:DM Sans,sans-serif;background:#fff;white-space:nowrap;'>"
                        f"<a href='{url_val}' target='_blank' rel='noopener noreferrer' "
                        f"style='color:#E8520A;text-decoration:none;font-weight:500;'>{val}</a></td>"
                    )
                else:
                    cell = (
                        f"<td style='padding:10px 14px;border-bottom:1px solid rgba(0,0,0,.06);"
                        f"font-size:13px;font-family:DM Sans,sans-serif;color:#141518;"
                        f"background:#fff;white-space:nowrap;'>{val}</td>"
                    )
            else:
                cell = (
                    f"<td style='padding:10px 14px;border-bottom:1px solid rgba(0,0,0,.06);"
                    f"font-size:13px;font-family:DM Sans,sans-serif;color:#141518;"
                    f"background:#fff;white-space:nowrap;'>{val}</td>"
                )
            cells.append(cell)
        rows_html.append("<tr>" + "".join(cells) + "</tr>")
    rows = "".join(rows_html)
    return f"<thead><tr>{headers}</tr></thead><tbody>{rows}</tbody>"


def render_table(df, page=1, per_page=25):
    total        = len(df)
    total_pages  = max(1, -(-total // per_page))
    page         = max(1, min(page, total_pages))
    start        = (page - 1) * per_page
    page_df      = df.iloc[start : start + per_page]

    page_html    = render_rows(page_df)
    row_height   = 44
    total_height = 44 + (len(page_df) * row_height) + 40

    html = f"""<!DOCTYPE html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
<style>
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ background:#F4F5F7; font-family:'DM Sans',sans-serif; }}
table {{ width:100%; border-collapse:collapse; background:#fff; }}
.table-wrap {{ border-radius:14px; overflow:hidden; box-shadow:0 2px 10px rgba(0,0,0,.05); }}
</style></head><body>
  <div class="table-wrap"><table>{page_html}</table></div>
</body></html>"""

    components.html(html, height=total_height, scrolling=False)
    return total_pages, page


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


# ── Helper: paginate an RPC call that returns rows ──
def rpc_fetch_all(fn_name: str, params: dict, page_size: int = 1000) -> list:
    """Call a Supabase RPC function repeatedly with .range() until all rows are
    returned, bypassing the default 1 000-row cap."""
    all_rows = []
    offset = 0
    while True:
        resp = (
            supabase.rpc(fn_name, params)
            .range(offset, offset + page_size - 1)
            .execute()
        )
        batch = resp.data or []
        all_rows.extend(batch)
        if len(batch) < page_size:
            break          # last (or only) page
        offset += page_size
    return all_rows

# =====================================================
# FIND & SYNC ALL EVENTS
# =====================================================

if find_events:
    _abort = False

    if not postcode:
        st.warning("Enter a postcode")
        _abort = True

    if not _abort:
        lat, lon, postcode_info = get_location(postcode)
        if lat is None:
            if classify_postcode(postcode) != "uk":
                burdy_error("This looks like a non UK postcode. Please enter a valid UK postcode (e.g. B2 5RE, SW1A 1AA).")
            else:
                burdy_error("Postcode not found. Please check the postcode and try again.")
            _abort = True
        else:
            st.session_state["postcode_info"] = postcode_info

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
            {"lat": lat, "lng": lon, "radius_meters": radius * 1609.34,
             "now_utc": datetime.now(timezone.utc).isoformat()}
        ).execute().data
        after_radius_rows = rpc_fetch_all(
            "search_within_radius",
            {"lat": lat, "lng": lon, "radius_meters": radius * 1609.34,
             "now_utc": datetime.now(timezone.utc).isoformat(),
             "type_filters": [], "venue_filters": []}
        )

        st.session_state["search_df"]    = pd.DataFrame(after_radius_rows)
        st.session_state["filtered_df"]  = st.session_state["search_df"]
        st.session_state["search_label"] = (
            f"{after_radius_count} events within {radius} miles of {postcode.upper()}"
        )
        st.session_state["page_num"]       = 1
        st.session_state["_search_lat"]    = lat
        st.session_state["_search_lon"]    = lon
        st.session_state["_search_radius"] = radius
        st.session_state["_last_filter_key"] = "|"

        new_events_count = after_total - before_total
        st.session_state["new_events_count"] = new_events_count

        # Fetch the newest events by Created At for the popup
        if new_events_count > 0:
            try:
                newest_rows = supabase.table("BurdySteupTest")\
                    .select("Name, \"Venue Name\", Date, Type, url, \"Created At\"")\
                    .order("Created At", desc=True)\
                    .limit(new_events_count)\
                    .execute().data
                st.session_state["newest_events"] = newest_rows
            except Exception as ex:
                st.session_state["newest_events"] = []
        else:
            st.session_state["newest_events"] = []

        status.empty()
        progress.empty()

        # Final update with all real values
        stats_slot.markdown(
            _stat_row(tm_count, sk_count, new_events_count, after_radius_count, after_total, radius),
            unsafe_allow_html=True
        )

        # Register the new events modal listener if there are new events
        if new_events_count > 0:
            burdy_new_events_modal(st.session_state["newest_events"])

# =====================================================
# SEARCH VIEW
# =====================================================

if search_db:
    if not postcode:
        st.warning("Enter a postcode first")
    else:
        lat, lon, postcode_info = get_location(postcode)
        if lat is None:
            if classify_postcode(postcode) != "uk":
                burdy_error("This looks like a non UK postcode. Please enter a valid UK postcode (e.g. B2 5RE, SW1A 1AA).")
            else:
                burdy_error("Postcode not found. Please check the postcode and try again.")
        else:
            st.session_state["postcode_info"] = postcode_info
            rows = rpc_fetch_all(
                "search_within_radius",
                {"lat": lat, "lng": lon, "radius_meters": radius * 1609.34,
                 "now_utc": datetime.now(timezone.utc).isoformat(),
                 "type_filters": [], "venue_filters": []}
            )
            st.session_state["search_df"]        = pd.DataFrame(rows)
            st.session_state["filtered_df"]       = st.session_state["search_df"]
            st.session_state["search_label"]      = (
                f"{len(st.session_state['search_df'])} events within "
                f"{radius} miles of {postcode.upper()}"
            )
            st.session_state["page_num"]          = 1
            st.session_state["_search_lat"]       = lat
            st.session_state["_search_lon"]       = lon
            st.session_state["_search_radius"]    = radius
            st.session_state["_last_search_key"]  = f"{postcode}|{radius}"
            st.session_state["_last_filter_key"]  = "|"

df    = st.session_state.get("search_df", pd.DataFrame())
label = st.session_state.get("search_label", "")

# ── Postcode info panel ──
_pci = st.session_state.get("postcode_info")
if _pci:
    def _pci_field(label, value):
        if not value or value == "—":
            return ""
        return f"""<div><div class="field-label">{label}</div><div class="field-value">{value}</div></div>"""

    council_name = _pci.get("admin_district") or "—"
    council_code = _pci.get("admin_district_code") or "—"
    county       = _pci.get("admin_county") or "—"
    ward         = _pci.get("admin_ward") or "—"
    parish       = _pci.get("parish") or "—"
    region       = _pci.get("region") or "—"
    country      = _pci.get("country") or "—"
    constituency = _pci.get("parliamentary_constituency") or "—"
    nhs_ha       = _pci.get("nhs_ha") or "—"
    postcode_fmt = _pci.get("postcode") or "—"

    fields_html = "".join(filter(None, [
        _pci_field("Postcode",            postcode_fmt),
        _pci_field("Council",             council_name),
        _pci_field("Council Code",        council_code),
        _pci_field("County",              county),
        _pci_field("Ward",                ward),
        _pci_field("Parish",              parish),
        _pci_field("Region",              region),
        _pci_field("Country",             country),
        _pci_field("Constituency",        constituency),
        _pci_field("NHS Health Authority", nhs_ha),
    ]))

    _card_html = f"""<!DOCTYPE html><html><head>
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
<style>
* {{ box-sizing:border-box; margin:0; padding:0; }}
html, body {{ background:transparent; overflow:hidden; }}
.card {{
    background:#fff;
    border:1px solid rgba(0,0,0,.09);
    border-radius:14px;
    padding:20px 24px;
    position:relative;
    overflow:hidden;
    box-shadow:0 2px 10px rgba(0,0,0,.05);
}}
.card::before {{
    content:'';
    position:absolute;
    top:0;left:0;right:0;height:3px;
    background:linear-gradient(90deg,#E8520A,#179948,transparent);
}}
.heading {{
    font-family:'DM Mono',monospace;
    font-size:10px;
    letter-spacing:.1em;
    text-transform:uppercase;
    color:#A0A7B4;
    margin-bottom:14px;
}}
.fields {{
    display:flex;
    flex-wrap:wrap;
    gap:20px 32px;
}}
.field-label {{
    font-family:'DM Mono',monospace;
    font-size:9px;
    letter-spacing:.1em;
    text-transform:uppercase;
    color:#A0A7B4;
    margin-bottom:2px;
}}
.field-value {{
    font-family:'DM Sans',sans-serif;
    font-size:13px;
    font-weight:500;
    color:#141518;
}}
</style>
</head><body>
<div class="card">
  <div class="heading">&#9670; &nbsp;Postcode Intelligence</div>
  <div class="fields">{fields_html}</div>
</div>
</body></html>"""

    components.html(_card_html, height=110, scrolling=False)
# ── Helper: run a filtered Supabase query ──
def run_filtered_query(lat, lon, radius, type_filters=None, venue_filters=None):
    params = {
        "lat":           lat,
        "lng":           lon,
        "radius_meters": radius * 1609.34,
        "now_utc":       datetime.now(timezone.utc).isoformat(),
        "type_filters":  type_filters or [],
        "venue_filters": venue_filters or [],
    }
    rows = rpc_fetch_all("search_within_radius", params)
    return pd.DataFrame(rows)

if not df.empty:
    st.divider()
    st.subheader(label)

    # ── Filters ──
    col_lower = {c.lower(): c for c in df.columns}
    type_col  = col_lower.get("type")
    venue_col = col_lower.get("venue_name")

    filter_l, filter_r = st.columns(2)

    with filter_l:
        if type_col:
            type_options   = sorted(df[type_col].dropna().unique().tolist())
            selected_types = st.multiselect("Filter by Event Type", options=type_options,
                                            placeholder="All types")
        else:
            selected_types = []

    with filter_r:
        if venue_col:
            venue_options   = sorted(df[venue_col].dropna().unique().tolist())
            selected_venues = st.multiselect("Filter by Venue", options=venue_options,
                                             placeholder="All venues")
        else:
            selected_venues = []

    # Re-query Supabase when filters change
    _filter_key = f"{','.join(sorted(selected_types))}|{','.join(sorted(selected_venues))}"
    if _filter_key != st.session_state.get("_last_filter_key"):
        st.session_state["_last_filter_key"] = _filter_key
        st.session_state["page_num"] = 1
        _lat = st.session_state.get("_search_lat")
        _lon = st.session_state.get("_search_lon")
        _rad = st.session_state.get("_search_radius")
        if _lat and _lon and _rad:
            st.session_state["filtered_df"] = run_filtered_query(
                _lat, _lon, _rad,
                selected_types or [],
                selected_venues or [],
            )

    filtered_df = st.session_state.get("filtered_df", df)

    # ── Pagination controls ──
    if "page_num" not in st.session_state:
        st.session_state["page_num"] = 1
    if "rows_per_page" not in st.session_state:
        st.session_state["rows_per_page"] = 25

    per_page    = st.session_state["rows_per_page"]
    total_pages = max(1, -(-len(filtered_df) // per_page))
    page_num    = max(1, min(st.session_state["page_num"], total_pages))

    ctrl_left, ctrl_mid, ctrl_right = st.columns([2, 6, 2])

    with ctrl_left:
        options = [10, 25, 50, 100]
        new_per = st.selectbox("Rows per page", options=options,
                               index=options.index(per_page))
        if new_per != per_page:
            st.session_state["rows_per_page"] = new_per
            st.session_state["page_num"]      = 1
            st.rerun()

    with ctrl_mid:
        total_label = f"{len(filtered_df)} events" if len(filtered_df) == len(df) else f"{len(filtered_df)} filtered results"
        st.markdown(
            f"<div style='text-align:center;font-family:DM Mono,monospace;font-size:12px;"
            f"color:#6B7280;padding-top:28px;'>"
            f"Page {page_num} of {total_pages} &nbsp;·&nbsp; {total_label}"
            f"</div>",
            unsafe_allow_html=True,
        )

    with ctrl_right:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        nav_l, nav_r = st.columns(2)
        with nav_l:
            if st.button("‹ Prev", disabled=(page_num <= 1), use_container_width=True):
                st.session_state["page_num"] = page_num - 1
                st.rerun()
        with nav_r:
            if st.button("Next ›", disabled=(page_num >= total_pages), use_container_width=True):
                st.session_state["page_num"] = page_num + 1
                st.rerun()

    render_table(filtered_df, page=st.session_state["page_num"], per_page=per_page)
