import streamlit as st
import requests
import time
import pandas as pd
import hashlib
import calendar
import json
import math
import re
import urllib.parse
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
div[data-testid="stSlider"] div[class*="thumbValue"] { color: var(--text) !important; }
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
    white-space: nowrap !important;
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
    opacity: 0;
    pointer-events: none;
    transition: left .2s ease, opacity .2s ease;
}
.burdy-footer.visible {
    opacity: 1;
    pointer-events: auto;
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

/* ── When the sidebar is open, the footer has less horizontal room —
      shrink everything so the badges stay on one row instead of wrapping
      onto a second line and growing the footer's height. Toggled via JS
      (the same script that repositions the header/footer) rather than a
      media query, since this depends on sidebar state, not viewport size. ── */
.burdy-footer.sidebar-open {
    padding-left: 1.25rem !important;
    padding-right: 1.25rem !important;
    gap: 8px !important;
}
.burdy-footer.sidebar-open .footer-copy {
    font-size: 9.5px !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    flex-shrink: 1 !important;
    min-width: 0 !important;
}
.burdy-footer.sidebar-open .footer-badges {
    gap: 4px !important;
    flex-wrap: nowrap !important;
    flex-shrink: 0 !important;
}
.burdy-footer.sidebar-open .footer-badge {
    padding: 3px 6px !important;
    font-size: 8px !important;
    letter-spacing: .04em !important;
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
            toggleSidebar();
        };

        p.body.appendChild(toggle);
        return toggle;
    }

    function toggleSidebar() {
        var stBtn = p.querySelector('[data-testid="stSidebarCollapseButton"] button')
                 || p.querySelector('[data-testid="stSidebarCollapsedControl"] button')
                 || p.querySelector('[data-testid="stSidebarCollapseButton"]')
                 || p.querySelector('[data-testid="stSidebarCollapsedControl"]');
        if (stBtn) stBtn.click();
    }

    function positionToggle() {
        var toggle = ensureToggle();
        var sidebar = p.querySelector('[data-testid="stSidebar"]');
        var sidebarRight = sidebar ? sidebar.getBoundingClientRect().right : 0;
        var isCollapsed = sidebarRight < 10;
        toggle.style.left = (isCollapsed ? 0 : sidebarRight) + 'px';
        toggle.innerHTML  = isCollapsed ? '&#10095;' : '&#10094;';

        // The header is position:fixed spanning the full viewport, but the
        // sidebar sits above it (higher z-index) — without this it just
        // gets covered on the left whenever the sidebar is open. Shifting
        // left to match the sidebar's actual right edge, with the CSS
        // `right: 0` left untouched, lets the header's own width recalculate
        // to fill exactly the remaining space rather than being hidden.
        var header = p.querySelector('.burdy-header');
        if (header) header.style.left = (isCollapsed ? 0 : sidebarRight) + 'px';

        // Same mechanism for the footer.
        var footer = p.querySelector('.burdy-footer');
        if (footer) {
            footer.style.left = (isCollapsed ? 0 : sidebarRight) + 'px';
            footer.classList.toggle('sidebar-open', !isCollapsed);
        }
    }

    function bindLogoClick() {
        // st.markdown-rendered HTML strips inline onclick handlers even with
        // unsafe_allow_html=True — only components.html (this script) runs
        // unsanitized JS, so the click listener has to be attached from here
        // rather than as an onclick attribute in the header markup. The
        // logo element gets re-created on every Streamlit rerun, so this
        // runs on the same polling loop as positionToggle and uses a data
        // attribute to avoid stacking duplicate listeners on the same node.
        var logo = p.querySelector('.burdy-logo');
        if (logo && !logo.dataset.clickBound) {
            logo.style.cursor = 'pointer';
            logo.addEventListener('click', toggleSidebar);
            logo.dataset.clickBound = '1';
        }
    }

    function checkFooterVisibility() {
        var footer = p.querySelector('.burdy-footer');
        if (!footer) return;
        var win = p.defaultView || window.parent;
        var scrollY    = win.scrollY || p.documentElement.scrollTop || 0;
        var winHeight  = win.innerHeight || p.documentElement.clientHeight || 0;
        var docHeight  = p.documentElement.scrollHeight || 0;
        var nearBottom = (docHeight - scrollY - winHeight) < 120;
        footer.classList.toggle('visible', nearBottom);
    }

    positionToggle();
    bindLogoClick();
    checkFooterVisibility();
    setInterval(function() { positionToggle(); bindLogoClick(); checkFooterVisibility(); }, 100);
    try {
        new MutationObserver(function() { positionToggle(); bindLogoClick(); }).observe(p.body, {
            attributes: true, subtree: true,
            attributeFilter: ['style', 'class']
        });
    } catch(e) {}
    try {
        var scrollWin = p.defaultView || window.parent;
        scrollWin.addEventListener('scroll', checkFooterVisibility, { passive: true });
    } catch(e) {}
})();
</script>
""", height=1)


# =====================================================
# CONFIG
# =====================================================

TICKETMASTER_API_KEY = st.secrets["TICKETMASTER_API_KEY"]
SKIDDLE_API_KEY      = st.secrets["SKIDDLE_API_KEY"]
NH_API_KEY           = st.secrets.get("NH_API_KEY", "")
SUPABASE_URL         = st.secrets["SUPABASE_URL"]
SUPABASE_KEY         = st.secrets["SUPABASE_SERVICE_ROLE_KEY"]
BIRD_LOGO_URL        = "https://ujrublkoqtpijwijklvq.supabase.co/storage/v1/object/sign/Brand%20Logo/Bird%20Logo%20Left.png?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV9jYTQwZTg5ZS00MTVkLTQ0NjEtYTZjZi00OTI2MDIwYmYyZTkiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJCcmFuZCBMb2dvL0JpcmQgTG9nbyBMZWZ0LnBuZyIsImlhdCI6MTc4MDU5ODM2NSwiZXhwIjoxODEyMTM0MzY1fQ.OMa5cbOtPSUZR4JTjlT3Mm1XBZlgi2rugZOQx7SLCX0"
WORD_LOGO_URL        = "https://ujrublkoqtpijwijklvq.supabase.co/storage/v1/object/sign/Brand%20Logo/Font%20logo.png?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV9jYTQwZTg5ZS00MTVkLTQ0NjEtYTZjZi00OTI2MDIwYmYyZTkiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJCcmFuZCBMb2dvL0ZvbnQgbG9nby5wbmciLCJpYXQiOjE3ODA1OTg0MTEsImV4cCI6MTgxMjEzNDQxMX0.pt-zS-TT80l_mp-_jGklDgtx8K2wc0uafgW36VDklbo"

TM_BASE_URL      = "https://app.ticketmaster.com/discovery/v2/events.json"
SKIDDLE_URL      = "https://www.skiddle.com/api/v1/events/search/"
POSTCODE_API     = "https://api.postcodes.io/postcodes/{}"
NH_BASE_URL      = "https://api.data.nationalhighways.co.uk/roads/v2.0/closures"

WINDOW_DAYS      = 30
MONTHS_AHEAD     = 24
TM_MAX_PAGES     = 5
TM_PAGE_SIZE     = 200
SK_MAX_PAGES     = 10
SK_PAGE_SIZE     = 100

ROADWORKS_TABLE       = "road_closures"
ROADWORKS_DAYS_AHEAD  = 30   # planned closures: how far ahead to query
ROADWORKS_HOURS_BACK  = 6    # unplanned closures: how far back to query

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

def log_search_event(action, postcode=None, radius=None, lat=None, lon=None,
                      results_count=None, new_events_count=None):
    """Write one row to the Burdy Search Log table for every Search / Fetch & Sync run."""
    try:
        supabase.table("Burdy Search Log").insert({
            "action":            action,
            "postcode":          postcode.upper() if postcode else None,
            "radius_miles":      radius,
            "latitude":          lat,
            "longitude":         lon,
            "results_count":     results_count,
            "new_events_count":  new_events_count,
            "searched_at":       datetime.now(timezone.utc).isoformat(),
        }).execute()
    except Exception as e:
        st.warning(f"Couldn't write to Burdy Search Log: {e}")

def get_search_log_count():
    """Total number of searches (Search + Fetch & Sync runs) stored in Burdy Search Log."""
    try:
        return supabase.table("Burdy Search Log").select("id", count="exact").execute().count or 0
    except Exception:
        return 0

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
    transition: left .2s ease;
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
  <div class="burdy-logo" style="cursor:pointer;">
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

_hero_html = """
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
        <div class="stat-val">__SEARCH_COUNT__</div>
        <div class="stat-lbl">Searches Completed</div>
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
"""

_hero_html = _hero_html.replace("__SEARCH_COUNT__", str(get_search_log_count()))
components.html(_hero_html, height=520, scrolling=False)

col1, col2, col3, col4 = st.columns([2, 3, 1, 1.5])

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

def _stat_row_initial(total, today, this_week):
    return f"""
<div class="stat-row">
  <div class="stat-box" style="flex:1;">
    <div class="stat-num">{total}</div>
    <div class="stat-label">Total in Database</div>
  </div>
  <div class="stat-box" style="flex:1;">
    <div class="stat-num">{today}</div>
    <div class="stat-label">Events Today</div>
  </div>
  <div class="stat-box" style="flex:1;">
    <div class="stat-num">{this_week}</div>
    <div class="stat-label">Events This Week</div>
  </div>
</div>"""

def get_events_today_count():
    try:
        _today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        return supabase.table("BurdySteupTest").select("ID", count="exact") \
            .eq("Date", _today).execute().count or 0
    except Exception:
        return "—"

def get_events_this_week_count():
    try:
        _today     = datetime.now(timezone.utc).date()
        _week_end  = _today + timedelta(days=6)
        return supabase.table("BurdySteupTest").select("ID", count="exact") \
            .gte("Date", _today.strftime("%Y-%m-%d")) \
            .lte("Date", _week_end.strftime("%Y-%m-%d")) \
            .execute().count or 0
    except Exception:
        return "—"

def _stat_row_search(today_count, week_count, nearby_count, total_db, radius_label):
    return f"""
<div class="stat-row">
  <div class="stat-box" style="flex:1;">
    <div class="stat-num">{today_count}</div>
    <div class="stat-label">Events Today within {radius_label} miles</div>
  </div>
  <div class="stat-box" style="flex:1;">
    <div class="stat-num">{week_count}</div>
    <div class="stat-label">Events This Week within {radius_label} miles</div>
  </div>
  <div class="stat-box" style="flex:1;">
    <div class="stat-num">{nearby_count}</div>
    <div class="stat-label">Events within {radius_label} miles</div>
  </div>
  <div class="stat-box" style="flex:1;">
    <div class="stat-num">{total_db}</div>
    <div class="stat-label">Events in Database</div>
  </div>
</div>"""

def _parse_date_safe(val):
    """Parse a single date value, trying a fast ISO path then falling back to
    a lenient parse (handles DD/MM/YYYY, timestamps, etc)."""
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return None
    s = str(val).strip()
    if not s or s.lower() == "none":
        return None
    if len(s) >= 10 and s[4] == "-" and s[7] == "-":
        try:
            return datetime.strptime(s[:10], "%Y-%m-%d").date()
        except ValueError:
            pass
    try:
        from dateutil import parser as _date_parser
        return _date_parser.parse(s, dayfirst=True).date()
    except Exception:
        return None

def _count_in_date_range(df, start_date, end_date):
    """Count rows in a search-result DataFrame whose event_date falls within [start_date, end_date]."""
    if df is None or df.empty:
        return 0
    col_lower = {c.lower(): c for c in df.columns}
    date_col = (
        col_lower.get("event_date")
        or col_lower.get("date")
        or col_lower.get("eventdate")
    )
    if not date_col:
        st.warning(
            "Couldn't find a date column in the search results, so the "
            "'Events Today / This Week within X miles' cards can't be computed. "
            f"Columns actually returned by search_within_radius: {list(df.columns)}"
        )
        return "—"

    parsed  = df[date_col].apply(_parse_date_safe)
    matches = parsed.apply(lambda d: d is not None and start_date <= d <= end_date)
    return int(matches.sum())

stats_slot = st.empty()
try:
    _initial_total = supabase.table("BurdySteupTest").select("ID", count="exact").execute().count or 0
except Exception:
    _initial_total = "—"
_initial_today     = get_events_today_count()
_initial_this_week = get_events_this_week_count()
stats_slot.markdown(
    _stat_row_initial(_initial_total, _initial_today, _initial_this_week),
    unsafe_allow_html=True
)

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


# WMO weather codes (used by Open-Meteo) collapsed down to a small icon set —
# see https://open-meteo.com/en/docs for the full code table.
_WEATHER_ICONS = {
    0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️",
    45: "🌫️", 48: "🌫️",
    51: "🌦️", 53: "🌦️", 55: "🌦️",
    56: "🌧️", 57: "🌧️",
    61: "🌧️", 63: "🌧️", 65: "🌧️",
    66: "🌧️", 67: "🌧️",
    71: "🌨️", 73: "🌨️", 75: "🌨️", 77: "🌨️",
    80: "🌦️", 81: "🌧️", 82: "⛈️",
    85: "🌨️", 86: "🌨️",
    95: "⛈️", 96: "⛈️", 99: "⛈️",
}


@st.cache_data(ttl=1800, show_spinner=False)
def _fetch_weather_forecast_cached(lat, lon):
    """Does the actual Open-Meteo call. Raises on failure rather than
    swallowing the error, so a transient failure never gets cached as
    "no weather" for the full TTL — st.cache_data only stores a value that
    was successfully returned, not one that was raised."""
    resp = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude":  round(lat, 2),
            "longitude": round(lon, 2),
            "daily":     "weathercode,temperature_2m_max,temperature_2m_min",
            "hourly":    "temperature_2m,weathercode",
            "timezone":  "auto",
            "forecast_days": 16,
        },
        timeout=10,
    )
    resp.raise_for_status()
    payload = resp.json()

    daily  = payload.get("daily", {})
    dates  = daily.get("time", [])
    codes  = daily.get("weathercode", [])
    tmaxes = daily.get("temperature_2m_max", [])
    tmins  = daily.get("temperature_2m_min", [])

    # A handful of evenly-spaced points through the day, rather than all 24
    # hours — enough to show a shape (morning/midday/evening/overnight)
    # without cluttering a small modal.
    TARGET_HOURS = {"00", "06", "12", "18"}
    hourly = payload.get("hourly", {})
    hourly_by_date = {}
    for t, code, temp in zip(hourly.get("time", []), hourly.get("weathercode", []), hourly.get("temperature_2m", [])):
        date_part, _, time_part = t.partition("T")
        hh = time_part[:2]
        if hh not in TARGET_HOURS:
            continue
        hourly_by_date.setdefault(date_part, []).append({
            "time": f"{hh}:00",
            "icon": _WEATHER_ICONS.get(code, "🌡️"),
            "temp": round(temp) if temp is not None else None,
        })

    return {
        date: {
            "icon":   _WEATHER_ICONS.get(code, "🌡️"),
            "tmax":   round(tmax) if tmax is not None else None,
            "tmin":   round(tmin) if tmin is not None else None,
            "hourly": hourly_by_date.get(date, []),
        }
        for date, code, tmax, tmin in zip(dates, codes, tmaxes, tmins)
    }


def fetch_weather_forecast(lat, lon):
    """Open-Meteo daily forecast (free, no API key) — returns a dict keyed by
    'YYYY-MM-DD' with icon/tmax/tmin, for whatever days the API covers
    (typically today + the next ~15 days). The underlying call is cached for
    30 min per lat/lon; failures are handled here, outside the cache, so a
    one-off failure doesn't get "stuck" for the whole TTL."""
    try:
        return _fetch_weather_forecast_cached(lat, lon)
    except Exception as e:
        st.caption(f"⚠ Weather forecast unavailable right now ({e})")
        return {}


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


# =====================================================
# IMPACT SCORE ENGINE
# =====================================================
# Calculates a 0-100 impact score from fields already
# available in the event data returned by Ticketmaster
# and Skiddle. Fields not available (Spotify, social)
# default to 0 — they can be enriched later.

from datetime import date as _date

# Map event type strings to internal category
_TYPE_MAP = {
    "festival":    4,
    "live music":  1,
    "concert":     1,
    "comedy":      2,
    "sport":       3,
    "clubbing":    1,
    "theatre":     2,
    "exhibition":  5,
    "conference":  5,
    "arts":        2,
    "kids":        2,
    "family":      2,
}

# Approximate UK city populations for venue-city fit
_CITY_POP = {
    "london":       9_000_000,
    "birmingham":   1_100_000,
    "manchester":   550_000,
    "glasgow":      630_000,
    "leeds":        800_000,
    "liverpool":    500_000,
    "sheffield":    580_000,
    "bristol":      470_000,
    "edinburgh":    520_000,
    "cardiff":      360_000,
    "belfast":      340_000,
    "nottingham":   330_000,
    "leicester":    360_000,
    "coventry":     370_000,
    "newcastle":    300_000,
}

# Approximate venue capacities by name keyword
_VENUE_CAPS = {
    "stadium":        40_000,
    "arena":          15_000,
    "nec":            12_000,
    "hippodrome":      1_800,
    "symphony hall":   2_300,
    "town hall":       1_500,
    "academy":         2_000,
    "o2 academy":      2_000,
    "institute":       1_500,
    "civic hall":      1_600,
    "barclaycard":    15_000,
    "utilita":        15_000,
    "genting":         1_600,
    "mill":              500,
    "hall":            2_500,
    "theatre":         1_200,
    "amphitheatre":    5_000,
    "forum":           2_500,
    "pavilion":        1_000,
    "o2":              2_000,
    "jam house":         400,
    "hare and hounds":   300,
    "castle":            400,
    "warehouse":         800,
    "factory":           600,
    "arts centre":     1_000,
    "arts club":         500,
    "plaza":             800,
    "ballroom":        1_200,
    "venue":           1_000,
    "club":              600,
    "bar":               300,
    "pub":               200,
    "restaurant":        150,
    "cafe":              100,
}


def _guess_capacity(venue_name):
    """Estimate venue capacity from venue name keywords."""
    if not venue_name:
        return 1_000
    vl = str(venue_name).lower()
    for kw, cap in _VENUE_CAPS.items():
        if kw in vl:
            return cap
    return 1_000


def _guess_city_pop(city):
    """Look up approximate city population."""
    if not city:
        return 500_000
    return _CITY_POP.get(str(city).lower(), 500_000)


def _guess_event_type(type_str, name_str):
    """Map type/name string to internal 1-5 category."""
    combined = f"{type_str or ''} {name_str or ''}".lower()
    for kw, cat in _TYPE_MAP.items():
        if kw in combined:
            return cat
    return 1  # default: concert


def _day_score(date_str):
    """Score 4-8 based on day of week (Sat=8)."""
    try:
        d = _date.fromisoformat(str(date_str)[:10])
        return [4, 4, 5, 6, 7, 8, 7][d.weekday()]
    except Exception:
        return 6


def _months_until(date_str):
    """Months between today and event date."""
    try:
        ev = _date.fromisoformat(str(date_str)[:10])
        delta = (ev - _date.today()).days / 30
        return max(0, delta)
    except Exception:
        return 3.0


def _price_score(min_age):
    """
    We don't have ticket price in the feed, so we use min_age as a proxy:
    18+ events tend to be priced mid-range; all-ages often cheaper;
    no age restriction → assume mid (score 6).
    """
    try:
        age = int(float(str(min_age)))
        if age == 0:
            return 8   # all-ages / free-ish
        if age < 18:
            return 7
        return 6       # 18+ mainstream
    except Exception:
        return 6


def _type_modifier(event_type_int):
    return {1: 0, 2: 0, 3: 1, 4: 2, 5: -2}.get(event_type_int, 0)


def _get(row, *keys):
    """Case-insensitive field lookup — handles any column naming convention."""
    # Build normalised lookup once: lowercase + spaces-to-underscores
    index = list(row.index) if hasattr(row, "index") else list(row.keys())
    norm  = {str(k).lower().replace(" ", "_"): k for k in index}
    for key in keys:
        # 1. exact match
        if key in index:
            v = row[key]
            if v is not None and str(v) not in ("", "nan", "None", "NaN"):
                return v
        # 2. normalised match
        nk = str(key).lower().replace(" ", "_")
        if nk in norm:
            v = row[norm[nk]]
            if v is not None and str(v) not in ("", "nan", "None", "NaN"):
                return v
    return ""


def calculate_impact_score(row):
    """
    Given a pandas Series (one event row), return an integer impact score 0-100.

    Uses case-insensitive field lookup (_get) so it works regardless of whether
    Supabase / the search RPC returns 'Venue Name', 'venue_name', 'venuename', etc.

    Dimensions and max points:
      Venue scale          0-25   (capacity inferred from venue name)
      Event type           0-20   (festival > concert > comedy > conference)
      Artist signal        0-15   (named artists, headliner keywords)
      Date timing          0-15   (proximity + day of week)
      City market size     0-10   (major city = larger potential audience)
      Name/brand signal    0-10   (keywords: tour, headline, sold out, etc.)
      Distance             0-5    (closer to search postcode = more relevant)
    Total                  0-100
    """
    name       = str(_get(row, "name",       "Name",       "event_name",  "eventname")).strip()
    date_str   = str(_get(row, "event_date", "Date",       "date",        "start_date"))
    type_str   = str(_get(row, "type",       "Type",       "event_type",  "category"))
    venue_name = str(_get(row, "venue_name", "Venue Name", "venue",       "venuename"))
    city       = str(_get(row, "city",       "City",       "town",        "location"))
    artists    = str(_get(row, "artists",    "Artists",    "artist",      "performers"))
    genres     = str(_get(row, "genres",     "Genres",     "genre"))
    distance   = _get(row, "distance", "Distance", "dist") or 0

    name_lower  = name.lower()
    venue_lower = venue_name.lower()
    type_lower  = type_str.lower()

    # ── 1. VENUE SCALE  (0-25) ──────────────────────────────
    # Larger venues = higher potential impact
    capacity = _guess_capacity(venue_name)
    if capacity >= 20_000:   venue_pts = 25
    elif capacity >= 10_000: venue_pts = 22
    elif capacity >= 5_000:  venue_pts = 18
    elif capacity >= 2_000:  venue_pts = 14
    elif capacity >= 1_000:  venue_pts = 10
    elif capacity >= 500:    venue_pts = 6
    else:                    venue_pts = 3

    # ── 2. EVENT TYPE  (0-20) ───────────────────────────────
    # Festivals and arena-scale events naturally draw more
    event_type_int = _guess_event_type(type_str, name)
    type_pts = {
        4: 20,   # Festival
        1: 14,   # Concert / Live Music / Clubbing
        3: 16,   # Sport
        2: 12,   # Comedy / Theatre / Arts
        5: 6,    # Conference / Exhibition
    }.get(event_type_int, 10)

    # ── 3. ARTIST SIGNAL  (0-15) ────────────────────────────
    # Named headliners, multiple artists, or recognised genre keywords
    artist_pts = 0
    if artists and len(artists.strip()) > 2:
        n_artists = len([a for a in artists.split(",") if a.strip()])
        if n_artists >= 5:   artist_pts = 15   # multi-act lineup
        elif n_artists >= 3: artist_pts = 12
        elif n_artists >= 1: artist_pts = 9
    else:
        # No named artists in feed — use name/genre keywords as signal
        high_signal = ["tour", "headline", "live", "festival", "presents", "vs ", " ft "]
        if any(kw in name_lower for kw in high_signal):
            artist_pts = 7
        elif genres and len(genres.strip()) > 2:
            artist_pts = 5
        else:
            artist_pts = 3

    # ── 4. DATE TIMING  (0-15) ──────────────────────────────
    # Combination of: how soon (sweet spot 2-8 weeks), day of week
    months_adv = _months_until(date_str)
    day_pts    = _day_score(date_str)  # 4-8

    # Proximity score: events 0.5-2 months away score highest
    if months_adv < 0:
        prox_pts = 0   # past
    elif months_adv <= 0.05:
        prox_pts = 7   # today / tomorrow — happening now
    elif months_adv <= 0.5:
        prox_pts = 7   # this week / next few weeks
    elif months_adv <= 2:
        prox_pts = 6   # prime booking window
    elif months_adv <= 6:
        prox_pts = 4
    elif months_adv <= 12:
        prox_pts = 2
    else:
        prox_pts = 1   # far out

    # Day of week normalised to 0-8, combined with proximity
    date_pts = min(15, prox_pts + (day_pts - 4))   # day_pts 4-8 → adds 0-4

    # ── 5. CITY MARKET SIZE  (0-10) ─────────────────────────
    city_pop = _guess_city_pop(city)
    if city_pop >= 5_000_000:   city_pts = 10
    elif city_pop >= 1_000_000: city_pts = 8
    elif city_pop >= 500_000:   city_pts = 6
    elif city_pop >= 250_000:   city_pts = 4
    else:                       city_pts = 2

    # ── 6. NAME / BRAND SIGNAL  (0-10) ──────────────────────
    # Keywords in event name that suggest scale or demand
    name_pts = 0
    boost_words = {
        "sold out": 10, "arena": 9, "stadium": 9, "tour": 7,
        "headline": 7,  "world": 6,  "uk":  5,   "live": 4,
        "official": 4,  "presents": 3,
    }
    for word, pts in boost_words.items():
        if word in name_lower:
            name_pts = max(name_pts, pts)   # take highest match

    # ── 7. DISTANCE  (0-5) ──────────────────────────────────
    # Closer events are more relevant to the searcher
    try:
        dist = float(distance)
        if dist <= 1:    dist_pts = 5
        elif dist <= 5:  dist_pts = 4
        elif dist <= 10: dist_pts = 3
        elif dist <= 20: dist_pts = 2
        else:            dist_pts = 1
    except (TypeError, ValueError):
        dist_pts = 3   # unknown distance → neutral

    total = int(max(0, min(100,
        venue_pts + type_pts + artist_pts + date_pts + city_pts + name_pts + dist_pts
    )))
    return total


def score_label(score):
    """Return (label, hex_colour) for a given score."""
    if score >= 85:
        return "Blockbuster", "#179948"
    if score >= 65:
        return "Strong",      "#E8520A"
    if score >= 45:
        return "Moderate",    "#d97706"
    return "Low",             "#dc2626"


def add_impact_scores(df):
    """Add Impact Score and Rating columns to a dataframe of events."""
    if df.empty:
        return df
    df = df.copy()

    df["Impact Score"] = df.apply(calculate_impact_score, axis=1)
    df["Rating"]        = df["Impact Score"].apply(lambda s: score_label(s)[0])
    return df


def build_roadworks_list_rows(roadworks_df):
    """Map road_closures rows onto the same display columns used for events
    (Name / Venue Name / Date / Type / City / Impact Score / Rating), so
    roadworks entries can be merged straight into the events List-view table."""
    if roadworks_df is None or roadworks_df.empty:
        return pd.DataFrame()

    def _row(r):
        start_date = str(r.get("start_time") or "")[:10]
        ctype      = r.get("closure_type") or "planned"
        return {
            "Name":         r.get("road") or "Unknown road",
            "Venue Name":   r.get("location") or "—",
            "Date":         start_date,
            "Type":         f"Roadworks ({ctype})",
            "City":         "",
            "Impact Score": "",
            "Rating":       "Roadworks",
        }

    return pd.DataFrame([_row(r) for _, r in roadworks_df.iterrows()])


def render_rows(data_df):
    # Add impact scores before rendering — but only if they aren't already present,
    # so rows that already carry a fixed value (e.g. roadworks rows merged into the
    # list, tagged "Roadworks" rather than scored) don't get overwritten.
    if "Impact Score" not in data_df.columns or "Rating" not in data_df.columns:
        data_df = add_impact_scores(data_df)

    cols = list(data_df.columns)

    # Find the actual column names regardless of casing
    col_lower  = {c.lower(): c for c in cols}
    name_col   = col_lower.get("name")
    url_col    = col_lower.get("url")
    score_col  = "Impact Score"
    rating_col = "Rating"

    # Display all columns except the url column; put Impact Score + Rating first
    priority = [score_col, rating_col]
    display_cols = (
        [c for c in priority if c in cols] +
        [c for c in cols if c not in priority and c != url_col]
    )

    # Badge colours
    _BADGE = {
        "Blockbuster": ("rgba(23,153,72,.12)",  "#0f7035"),
        "Strong":      ("rgba(232,82,10,.12)",  "#c94308"),
        "Moderate":    ("rgba(217,119,6,.12)",  "#92400e"),
        "Low":         ("rgba(220,38,38,.10)",  "#991b1b"),
        "Roadworks":   ("rgba(0,69,124,.10)",   "#00457c"),
    }

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

            if col == score_col:
                if val == "":
                    # No Impact Score applies (e.g. roadworks rows) — plain dash, no bar
                    cell = (
                        f"<td style='padding:8px 14px;border-bottom:1px solid rgba(0,0,0,.06);"
                        f"background:#fff;white-space:nowrap;min-width:90px;'>"
                        f"<div style='font-family:DM Mono,monospace;font-size:13px;"
                        f"color:#A0A7B4;'>—</div></td>"
                    )
                else:
                    # Render as a number with mini progress bar
                    score_int = int(val)
                    bar_color = score_label(score_int)[1]
                    cell = (
                        f"<td style='padding:8px 14px;border-bottom:1px solid rgba(0,0,0,.06);"
                        f"background:#fff;white-space:nowrap;min-width:90px;'>"
                        f"<div style='font-family:DM Mono,monospace;font-size:13px;font-weight:600;"
                        f"color:{bar_color};margin-bottom:4px;'>{score_int}<span style='font-size:10px;"
                        f"color:#A0A7B4;font-weight:400;'>/100</span></div>"
                        f"<div style='height:3px;background:#F0F1F4;border-radius:2px;'>"
                        f"<div style='width:{score_int}%;height:3px;background:{bar_color};"
                        f"border-radius:2px;'></div></div></td>"
                    )

            elif col == rating_col:
                # Render as a pill badge
                bg, fg = _BADGE.get(str(val), ("rgba(0,0,0,.06)", "#6B7280"))
                cell = (
                    f"<td style='padding:10px 14px;border-bottom:1px solid rgba(0,0,0,.06);"
                    f"background:#fff;white-space:nowrap;'>"
                    f"<span style='display:inline-block;padding:3px 10px;border-radius:999px;"
                    f"font-family:DM Mono,monospace;font-size:10px;font-weight:600;"
                    f"letter-spacing:.06em;text-transform:uppercase;"
                    f"background:{bg};color:{fg};'>{val}</span></td>"
                )

            elif col == name_col and url_col:
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
table {{ width:100%; min-width:640px; border-collapse:collapse; background:#fff; }}
.table-wrap {{ border-radius:14px; overflow-x:auto; overflow-y:hidden;
               -webkit-overflow-scrolling:touch; box-shadow:0 2px 10px rgba(0,0,0,.05); }}
</style></head><body>
  <div class="table-wrap"><table>{page_html}</table></div>
</body></html>"""

    components.html(html, height=total_height, scrolling=False)
    return total_pages, page


def render_calendar(df, year, month, roadworks_df=None, lat=None, lon=None, all_events_df=None):
    """Render a month-grid calendar view of events, grouped by their event_date.
    Days are clickable to show the full list of events; each event is clickable
    for more detail (venue, type, city, time, Impact Score/Rating, and a link if available).
    roadworks_df (optional) is bucketed by day the same way and linked to the
    "Roadworks" stat box in each day cell. lat/lon (optional) enable the
    "Weather" stat box via Open-Meteo — days outside the forecast's ~16-day
    window (past days, or far-future months) just show no data, same as the
    Holidays/Other placeholders. all_events_df (optional) is a separate,
    all-time (incl. historical) fetch used ONLY to get accurate Events counts
    for days that have already passed — df itself only ever contains
    current/future events (search_within_radius filters out anything before
    "now" server-side), so past days would otherwise always show 0."""
    df = add_impact_scores(df)

    col_lower  = {c.lower(): c for c in df.columns}
    date_col   = col_lower.get("event_date") or col_lower.get("date") or col_lower.get("eventdate")
    name_col   = col_lower.get("name")
    venue_col  = col_lower.get("venue_name")
    type_col   = col_lower.get("type")
    city_col   = col_lower.get("city")
    time_col   = col_lower.get("event_time") or col_lower.get("time")
    url_col    = col_lower.get("url")
    score_col  = "Impact Score" if "Impact Score" in df.columns else None
    rating_col = "Rating" if "Rating" in df.columns else None

    def _cell(row, col):
        return str(row[col]) if col and pd.notna(row.get(col, None)) else ""

    events_by_day = {}
    if date_col:
        for _, row in df.iterrows():
            d = _parse_date_safe(row[date_col])
            if d is None or d.year != year or d.month != month:
                continue
            score = int(row[score_col]) if score_col and pd.notna(row.get(score_col, None)) else None
            events_by_day.setdefault(d.day, []).append({
                "name":   _cell(row, name_col)  or "Event",
                "venue":  _cell(row, venue_col),
                "type":   _cell(row, type_col),
                "city":   _cell(row, city_col),
                "time":   _cell(row, time_col),
                "url":    _cell(row, url_col),
                "score":  score,
                "rating": _cell(row, rating_col) if rating_col else "",
            })

    # Highest Impact Score first within each day (instead of start time / insertion order)
    for _events in events_by_day.values():
        _events.sort(key=lambda e: e["score"] if e["score"] is not None else -1, reverse=True)

    # Past-day Events counts: df above only ever contains current/future
    # events, so we use the separate all-time fetch here just for a count —
    # past days aren't clickable, so there's no need to build full entries.
    past_events_count_by_day = {}
    if all_events_df is not None and not all_events_df.empty:
        _ae_col_lower = {c.lower(): c for c in all_events_df.columns}
        _ae_date_col  = _ae_col_lower.get("event_date") or _ae_col_lower.get("date") or _ae_col_lower.get("eventdate")
        if _ae_date_col:
            for _, _row in all_events_df.iterrows():
                _d = _parse_date_safe(_row[_ae_date_col])
                if _d is None or _d.year != year or _d.month != month:
                    continue
                past_events_count_by_day[_d.day] = past_events_count_by_day.get(_d.day, 0) + 1

    # ── Roadworks, bucketed by day the same way events are ──
    # Linked only to their start_time day (not spanned across every day through
    # end_time) — spanning caused the same closure to appear to "duplicate"
    # across adjacent days whenever a re-published record's start_time shifted
    # slightly, since each version would separately span into the other's day.
    month_first = datetime(year, month, 1).date()
    month_last  = month_first.replace(day=calendar.monthrange(year, month)[1])

    roadworks_by_day = {}
    if roadworks_df is not None and not roadworks_df.empty:
        for _, rw in roadworks_df.iterrows():
            start_d = _parse_date_safe(rw.get("start_time"))
            if start_d is None or start_d < month_first or start_d > month_last:
                continue
            entry = {
                "road":         rw.get("road") or "Unknown road",
                "location":     rw.get("location") or "",
                "status":       rw.get("status") or "",
                "closure_type": rw.get("closure_type") or "planned",
                "cause":        rw.get("cause") or "",
                "comment":      rw.get("comment") or "",
                "start_time":   rw.get("start_time") or "",
                "end_time":     rw.get("end_time") or "",
            }
            roadworks_by_day.setdefault(start_d.day, []).append(entry)

    weather_by_day = {}
    if lat is not None and lon is not None:
        forecast = fetch_weather_forecast(lat, lon)
        for date_str, info in forecast.items():
            d = _parse_date_safe(date_str)
            if d is not None and d.year == year and d.month == month:
                weather_by_day[d.day] = info

    # Only present for days Open-Meteo actually returned data for (its
    # forecast window, typically today + ~15 days) — days outside that
    # range simply won't have a key here, which the modal uses to decide
    # whether to show the interval strip at all.
    weather_hourly_by_day = {
        day: info.get("hourly", [])
        for day, info in weather_by_day.items()
        if info.get("hourly")
    }

    cal_obj = calendar.Calendar(firstweekday=0)  # Monday start
    weeks   = cal_obj.monthdayscalendar(year, month)
    today   = datetime.now(timezone.utc).date()

    # Rating → colour, matching the List view's badge palette
    _RATING_COLORS = {
        "Blockbuster": "#179948",
        "Strong":      "#E8520A",
        "Moderate":    "#d97706",
        "Low":         "#dc2626",
    }

    day_headers = "".join(
        f"<div class='cal-head'>{d}</div>" for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    )

    cells_html = ""
    events_count_by_day = {}
    is_past_by_day = {}
    for week in weeks:
        for day in week:
            if day == 0:
                cells_html += "<div class='cal-cell cal-empty'></div>"
                continue
            day_events = events_by_day.get(day, [])
            day_rw     = roadworks_by_day.get(day, [])
            is_today   = (day == today.day and month == today.month and year == today.year)
            is_past    = datetime(year, month, day).date() < today

            n_events   = past_events_count_by_day.get(day, 0) if is_past else len(day_events)
            events_count_by_day[day] = n_events
            is_past_by_day[day] = is_past
            events_num_class = "cal-stat-num" if n_events else "cal-stat-num cal-stat-empty"
            events_val = str(n_events) if n_events else "0"
            # Counts still reflect what's in Supabase regardless of date — only
            # the click affordance is gated off for days that have already passed.
            events_onclick = f' onclick="event.stopPropagation(); openDay({day})"' if day_events and not is_past else ""
            events_style   = ' style="cursor:pointer;"' if day_events and not is_past else ""

            n_rw = len(day_rw)
            rw_num_class = "cal-stat-num" if n_rw else "cal-stat-num cal-stat-empty"
            rw_val       = str(n_rw) if n_rw else "–"
            rw_onclick   = f' onclick="event.stopPropagation(); openDayRoadworks({day})"' if n_rw and not is_past else ""
            rw_style     = ' style="cursor:pointer;"' if n_rw and not is_past else ""

            wx = weather_by_day.get(day)
            wx_html = ""
            if wx and wx.get("tmax") is not None:
                wx_html = f'<span class="cal-daynum-wx">{wx["icon"]} {wx["tmax"]}°</span>'

            stats_html = f"""<div class="cal-stat-grid">
                <div class="cal-stat-box cal-stat-events"{events_onclick}{events_style}>
                    <div class="{events_num_class}">{events_val}</div>
                    <div class="cal-stat-label">Events</div>
                </div>
                <div class="cal-stat-box cal-stat-holidays">
                    <div class="cal-stat-num cal-stat-empty">–</div>
                    <div class="cal-stat-label">Holidays</div>
                </div>
                <div class="cal-stat-box cal-stat-roadworks"{rw_onclick}{rw_style}>
                    <div class="{rw_num_class}">{rw_val}</div>
                    <div class="cal-stat-label">Travel</div>
                </div>
                <div class="cal-stat-box cal-stat-other">
                    <div class="cal-stat-num cal-stat-empty">–</div>
                    <div class="cal-stat-label">Other</div>
                </div>
            </div>"""

            # Clicking the day cell itself (anywhere other than the Events or
            # Travel boxes, which stop their own click from bubbling up here)
            # opens a lightweight day-summary placeholder — not the full
            # events list, which is reserved for clicking the Events box
            # specifically.
            cell_class = "cal-cell" + (" cal-today" if is_today else "") + " cal-clickable"
            cells_html += f"""<div class="{cell_class}" onclick="openDaySummary({day})" style="cursor:pointer;">
                <div class="cal-daynum">{day}{wx_html}</div>
                <div class="cal-events">{stats_html}</div>
            </div>"""

    n_weeks      = len(weeks)
    grid_height  = 46 + (n_weeks * 116) + 20

    events_json       = json.dumps(events_by_day).replace("</", "<\\/")
    roadworks_json    = json.dumps(roadworks_by_day).replace("</", "<\\/")
    events_count_json = json.dumps(events_count_by_day).replace("</", "<\\/")
    is_past_json      = json.dumps(is_past_by_day).replace("</", "<\\/")
    weather_hourly_json = json.dumps(weather_hourly_by_day).replace("</", "<\\/")
    month_label       = f"{calendar.month_name[month]} {year}"

    html = f"""<!DOCTYPE html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
<style>
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ background:#F4F5F7; font-family:'DM Sans',sans-serif; }}
.cal-wrap {{ background:#fff; border-radius:14px; overflow:hidden; box-shadow:0 2px 10px rgba(0,0,0,.05); border:1px solid rgba(0,0,0,.09); position:relative; }}
.cal-scroll {{ overflow-x:auto; -webkit-overflow-scrolling:touch; }}
.cal-grid {{ display:grid; grid-template-columns:repeat(7,1fr); min-width:630px; }}
.cal-head {{ padding:10px 8px; font-family:'DM Mono',monospace; font-size:11px; color:#6B7280;
             text-transform:uppercase; letter-spacing:.08em; text-align:center;
             background:#F4F5F7; border-bottom:1px solid rgba(0,0,0,.09); }}
.cal-cell {{ min-height:108px; border-right:1px solid rgba(0,0,0,.06); border-bottom:1px solid rgba(0,0,0,.06);
             padding:6px; position:relative; }}
.cal-empty {{ background:#FAFAFB; }}
.cal-today {{ background:rgba(232,82,10,.05); }}
.cal-clickable {{ cursor:pointer; transition:background .15s; }}
.cal-clickable:hover {{ background:rgba(232,82,10,.06); }}
.cal-daynum {{ font-family:'Syne',sans-serif; font-weight:700; font-size:13px; color:#141518;
               display:flex; align-items:center; gap:6px; margin-bottom:5px; }}
.cal-count {{ background:#E8520A; color:#fff; font-family:'DM Mono',monospace; font-size:9px;
              padding:1px 6px; border-radius:999px; }}
.cal-event {{ font-size:10px; color:#141518; background:#F4F5F7; border-radius:4px;
              padding:2px 5px; margin-bottom:3px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
              display:flex; align-items:center; gap:4px; }}
.cal-event-dot {{ width:6px; height:6px; border-radius:50%; flex-shrink:0; }}
.cal-more {{ font-size:9px; color:#A0A7B4; font-family:'DM Mono',monospace; }}

.cal-stat-grid {{ display:grid; grid-template-columns:1fr 1fr; grid-template-rows:1fr 1fr;
                   gap:3px; height:70px; }}
.cal-stat-box {{ background:#F4F5F7; border-radius:5px; display:flex; flex-direction:column;
                  align-items:center; justify-content:center; padding:2px; text-align:center;
                  overflow:hidden; }}
.cal-stat-num {{ font-family:'Syne',sans-serif; font-weight:800; font-size:13px; color:#141518;
                  line-height:1.1; }}
.cal-stat-num.cal-stat-empty {{ color:#C7CBD3; font-weight:600; }}
.cal-stat-label {{ font-family:'DM Mono',monospace; font-size:7px; color:#6B7280;
                    text-transform:uppercase; letter-spacing:.02em; margin-top:1px; white-space:nowrap; }}
.cal-stat-events {{ background:var(--orange-glow, rgba(232,82,10,.1)); }}
.cal-stat-events .cal-stat-num:not(.cal-stat-empty) {{ color:#E8520A; }}
.cal-stat-holidays .cal-stat-num:not(.cal-stat-empty) {{ color:#179948; }}
.cal-stat-roadworks .cal-stat-num:not(.cal-stat-empty) {{ color:#00457c; }}
.cal-daynum-wx {{ font-family:'DM Mono',monospace; font-weight:500; font-size:10px; color:#0284c7;
                   margin-left:auto; white-space:nowrap; }}
.cal-stat-roadworks[style*="cursor:pointer"] {{ background:rgba(0,69,124,.10); transition:background .15s; }}
.cal-stat-roadworks[style*="cursor:pointer"]:hover {{ background:rgba(0,69,124,.18); }}
.cal-stat-events[style*="cursor:pointer"] {{ transition:background .15s; }}
.cal-stat-events[style*="cursor:pointer"]:hover {{ background:rgba(232,82,10,.22); }}

/* ── Modal ── */
.modal-overlay {{ display:none; position:absolute; inset:0; background:rgba(20,21,24,.55);
                   z-index:1000; align-items:center; justify-content:center; padding:20px; }}
.modal-overlay.open {{ display:flex; }}
.modal-box {{ background:#fff; border-radius:14px; width:100%; max-width:420px; max-height:100%;
              display:flex; flex-direction:column; overflow:hidden;
              box-shadow:0 12px 40px rgba(0,0,0,.25); position:relative; }}
.modal-box::before {{ content:''; position:absolute; top:0; left:0; right:0; height:3px;
                       background:linear-gradient(90deg,#E8520A,#179948,transparent); z-index:1; }}
.modal-header {{ display:flex; align-items:center; justify-content:space-between;
                  padding:18px 20px 12px; border-bottom:1px solid rgba(0,0,0,.08);
                  flex-shrink:0; background:#fff; position:relative; z-index:1; }}
.modal-title {{ font-family:'Syne',sans-serif; font-weight:800; font-size:15px; color:#141518; }}
.modal-close {{ cursor:pointer; font-size:18px; color:#A0A7B4; line-height:1; padding:2px 6px;
                border-radius:6px; }}
.modal-close:hover {{ background:#F0F1F4; color:#141518; }}
.modal-body {{ padding:14px 20px 20px; overflow-y:auto; flex:1; }}
.day-event-row {{ padding:12px 14px; border:1px solid rgba(0,0,0,.08); border-radius:10px;
                   margin-bottom:10px; cursor:pointer; transition:border-color .15s, background .15s; }}
.day-event-row:hover {{ border-color:#E8520A; background:rgba(232,82,10,.04); }}
.day-event-top {{ display:flex; align-items:center; justify-content:space-between; gap:8px;
                   margin-bottom:3px; }}
.day-event-name {{ font-family:'DM Sans',sans-serif; font-weight:700; font-size:13px; color:#141518; }}
.day-event-window {{ font-family:'DM Mono',monospace; font-weight:500; font-size:10px; color:#6B7280;
                      margin-left:7px; white-space:nowrap; }}
.day-event-sub {{ font-family:'DM Mono',monospace; font-size:10px; color:#6B7280;
                   letter-spacing:.02em; }}
.rating-badge {{ display:inline-block; padding:2px 9px; border-radius:999px; flex-shrink:0;
                  font-family:'DM Mono',monospace; font-size:9px; font-weight:600;
                  letter-spacing:.06em; text-transform:uppercase; white-space:nowrap; }}
.back-link {{ font-family:'DM Mono',monospace; font-size:11px; color:#E8520A; cursor:pointer;
              margin-bottom:14px; display:inline-block; text-transform:uppercase; letter-spacing:.06em; }}
.detail-name {{ font-family:'Syne',sans-serif; font-weight:800; font-size:17px; color:#141518;
                margin-bottom:10px; line-height:1.3; }}
.score-row {{ display:flex; align-items:center; gap:10px; margin-bottom:16px; }}
.score-num {{ font-family:'DM Mono',monospace; font-size:15px; font-weight:600; }}
.score-num small {{ font-size:10px; color:#A0A7B4; font-weight:400; }}
.score-bar-track {{ flex:1; height:4px; background:#F0F1F4; border-radius:2px; overflow:hidden; }}
.score-bar-fill {{ height:4px; border-radius:2px; }}
.detail-field {{ margin-bottom:12px; }}
.detail-label {{ font-family:'DM Mono',monospace; font-size:9px; color:#A0A7B4; text-transform:uppercase;
                  letter-spacing:.1em; margin-bottom:2px; }}
.detail-value {{ font-family:'DM Sans',sans-serif; font-size:13px; color:#141518; font-weight:500; }}
.detail-link {{ display:inline-block; margin-top:6px; background:#E8520A; color:#fff !important;
                 font-family:'Syne',sans-serif; font-weight:700; font-size:11px; letter-spacing:.05em;
                 text-transform:uppercase; text-decoration:none; padding:10px 18px; border-radius:8px; }}
.detail-link:hover {{ background:#c94308; }}
</style></head><body>
  <div class="cal-wrap">
    <div class="cal-scroll">
      <div class="cal-grid">{day_headers}{cells_html}</div>
    </div>

    <div class="modal-overlay" id="modal-overlay" onclick="if(event.target===this) closeModal()">
      <div class="modal-box">
        <div class="modal-header">
          <div class="modal-title" id="modal-title">Events</div>
          <div class="modal-close" onclick="closeModal()">&times;</div>
        </div>
        <div class="modal-body" id="modal-body"></div>
      </div>
    </div>
  </div>

<script>
const EVENTS_BY_DAY       = {events_json};
const ROADWORKS_BY_DAY    = {roadworks_json};
const EVENTS_COUNT_BY_DAY = {events_count_json};
const IS_PAST_BY_DAY      = {is_past_json};
const WEATHER_HOURLY_BY_DAY = {weather_hourly_json};
const MONTH_LABEL      = {json.dumps(month_label)};
const RATING_COLORS = {{
  "Blockbuster": {{ bg: "rgba(23,153,72,.12)",  fg: "#0f7035" }},
  "Strong":      {{ bg: "rgba(232,82,10,.12)",  fg: "#c94308" }},
  "Moderate":    {{ bg: "rgba(217,119,6,.12)",  fg: "#92400e" }},
  "Low":         {{ bg: "rgba(220,38,38,.10)",  fg: "#991b1b" }}
}};
const CLOSURE_COLORS = {{
  "planned":   {{ bg: "rgba(217,119,6,.12)", fg: "#92400e" }},
  "unplanned": {{ bg: "rgba(220,38,38,.10)", fg: "#991b1b" }}
}};
let currentDay  = null;
let currentMode = 'events';   // 'events' | 'roadworks'

function esc(s) {{
  const d = document.createElement('div');
  d.innerText = (s || '');
  return d.innerHTML;
}}

function ratingBadge(rating) {{
  if (!rating) return '';
  const c = RATING_COLORS[rating] || {{ bg: "rgba(0,0,0,.06)", fg: "#6B7280" }};
  return '<span class="rating-badge" style="background:' + c.bg + ';color:' + c.fg + ';">' + esc(rating) + '</span>';
}}

function closureBadge(ctype) {{
  const c = CLOSURE_COLORS[ctype] || {{ bg: "rgba(0,0,0,.06)", fg: "#6B7280" }};
  return '<span class="rating-badge" style="background:' + c.bg + ';color:' + c.fg + ';">' + esc(ctype) + '</span>';
}}

function openDay(day) {{
  currentMode = 'events';
  currentDay  = day;
  document.getElementById('modal-title').innerText = 'Events — ' + day + ' ' + MONTH_LABEL;
  renderDayList(day);
  document.getElementById('modal-overlay').classList.add('open');
}}

function openDayRoadworks(day) {{
  currentMode = 'roadworks';
  currentDay  = day;
  document.getElementById('modal-title').innerText = 'Travel — ' + day + ' ' + MONTH_LABEL;
  renderRoadworksList(day);
  document.getElementById('modal-overlay').classList.add('open');
}}

function openDaySummary(day) {{
  // Lightweight placeholder overview for clicking the day cell itself —
  // distinct from openDay/openDayRoadworks, which show the full lists and
  // are only reachable by clicking the Events or Travel boxes specifically.
  currentMode = 'summary';
  currentDay  = day;
  const nEvents = EVENTS_COUNT_BY_DAY[day] || 0;
  const nTravel = (ROADWORKS_BY_DAY[day] || []).length;
  const isPast  = !!IS_PAST_BY_DAY[day];
  const hourly  = WEATHER_HOURLY_BY_DAY[day] || [];
  document.getElementById('modal-title').innerText = day + ' ' + MONTH_LABEL;
  let hint;
  if (nEvents === 0) {{
    hint = 'Nothing on the books for this day yet.';
  }} else if (isPast) {{
    hint = 'This day has passed — the full list is no longer available to open.';
  }} else {{
    hint = 'Click Events above for the full list.';
  }}
  let weatherHtml = '';
  if (hourly.length) {{
    weatherHtml =
      '<div style="font-family:\\'DM Mono\\',monospace; font-size:9px; color:#A0A7B4; text-transform:uppercase; letter-spacing:.05em; margin:12px 0 6px;">Through the day</div>' +
      '<div style="display:flex; gap:6px;">' +
        hourly.map(function(h) {{
          return '<div style="flex:1; background:#F4F5F7; border-radius:8px; padding:8px 4px; text-align:center;">' +
            '<div style="font-family:\\'DM Mono\\',monospace; font-size:8px; color:#A0A7B4;">' + esc(h.time) + '</div>' +
            '<div style="font-size:15px; margin:3px 0;">' + h.icon + '</div>' +
            '<div style="font-family:\\'DM Sans\\',sans-serif; font-weight:700; font-size:11px; color:#141518;">' + h.temp + '°</div>' +
          '</div>';
        }}).join('') +
      '</div>';
  }}
  document.getElementById('modal-body').innerHTML =
    '<div style="padding:8px 2px;">' +
      '<div style="display:flex; gap:10px; margin-bottom:4px;">' +
        '<div style="flex:1; background:#F4F5F7; border-radius:10px; padding:14px; text-align:center;">' +
          '<div style="font-family:\\'Syne\\',sans-serif; font-weight:800; font-size:20px; color:#E8520A;">' + nEvents + '</div>' +
          '<div style="font-family:\\'DM Mono\\',monospace; font-size:9px; color:#6B7280; text-transform:uppercase; letter-spacing:.05em; margin-top:2px;">Events</div>' +
        '</div>' +
        '<div style="flex:1; background:#F4F5F7; border-radius:10px; padding:14px; text-align:center;">' +
          '<div style="font-family:\\'Syne\\',sans-serif; font-weight:800; font-size:20px; color:#00457c;">' + nTravel + '</div>' +
          '<div style="font-family:\\'DM Mono\\',monospace; font-size:9px; color:#6B7280; text-transform:uppercase; letter-spacing:.05em; margin-top:2px;">Travel</div>' +
        '</div>' +
      '</div>' +
      weatherHtml +
      '<div style="font-family:\\'DM Sans\\',sans-serif; font-size:11px; color:#A0A7B4; text-align:center; margin-top:10px;">' +
        hint +
      '</div>' +
    '</div>';
  document.getElementById('modal-overlay').classList.add('open');
}}

function closeModal() {{
  document.getElementById('modal-overlay').classList.remove('open');
}}

function renderDayList(day) {{
  const events = EVENTS_BY_DAY[day] || [];
  let html = '';
  events.forEach(function(e, idx) {{
    const sub = [e.time, e.venue, e.city].filter(Boolean).join(' · ');
    html += '<div class="day-event-row" onclick="showDetail(' + day + ',' + idx + ')">' +
              '<div class="day-event-top">' +
                '<div class="day-event-name">' + esc(e.name) + '</div>' +
                ratingBadge(e.rating) +
              '</div>' +
              (sub ? '<div class="day-event-sub">' + esc(sub) + '</div>' : '') +
            '</div>';
  }});
  document.getElementById('modal-body').innerHTML = html;
}}

function renderRoadworksList(day) {{
  const items = ROADWORKS_BY_DAY[day] || [];
  let html = '';
  items.forEach(function(r, idx) {{
    const sub = [r.status, (r.comment || r.location)].filter(Boolean).join(' · ');
    const windowHtml = (r.start_time || r.end_time)
      ? '<span class="day-event-window">' + esc(formatWindow(r.start_time, r.end_time)) + '</span>'
      : '';
    html += '<div class="day-event-row" onclick="showRoadworksDetail(' + day + ',' + idx + ')">' +
              '<div class="day-event-top">' +
                '<div class="day-event-name">' + esc(r.road) + windowHtml + '</div>' +
                closureBadge(r.closure_type) +
              '</div>' +
              (sub ? '<div class="day-event-sub">' + esc(sub) + '</div>' : '') +
            '</div>';
  }});
  document.getElementById('modal-body').innerHTML = html || '<div class="day-event-sub">No travel linked to this day.</div>';
}}

function showDetail(day, idx) {{
  const e = (EVENTS_BY_DAY[day] || [])[idx];
  if (!e) return;
  document.getElementById('modal-title').innerText = 'Event Details';
  let html = '<div class="back-link" onclick="backToDay()">‹ Back to ' + day + ' ' + MONTH_LABEL + '</div>';
  html += '<div class="detail-name">' + esc(e.name) + '</div>';
  if (e.score !== null && e.score !== undefined) {{
    const c = RATING_COLORS[e.rating] || {{ bg: "rgba(0,0,0,.06)", fg: "#6B7280" }};
    html += '<div class="score-row">' +
              '<div class="score-num" style="color:' + c.fg + ';">' + e.score + '<small>/100</small></div>' +
              '<div class="score-bar-track"><div class="score-bar-fill" style="width:' + e.score + '%;background:' + c.fg + ';"></div></div>' +
              ratingBadge(e.rating) +
            '</div>';
  }}
  if (e.venue) html += '<div class="detail-field"><div class="detail-label">Venue</div><div class="detail-value">' + esc(e.venue) + '</div></div>';
  if (e.city)  html += '<div class="detail-field"><div class="detail-label">City</div><div class="detail-value">' + esc(e.city) + '</div></div>';
  if (e.type)  html += '<div class="detail-field"><div class="detail-label">Type</div><div class="detail-value">' + esc(e.type) + '</div></div>';
  if (e.time)  html += '<div class="detail-field"><div class="detail-label">Time</div><div class="detail-value">' + esc(e.time) + '</div></div>';
  html += '<div class="detail-field"><div class="detail-label">Date</div><div class="detail-value">' + day + ' ' + MONTH_LABEL + '</div></div>';
  if (e.url) html += '<a class="detail-link" href="' + e.url + '" target="_blank" rel="noopener noreferrer">View Event ↗</a>';
  document.getElementById('modal-body').innerHTML = html;
}}

function isoTimePart(iso) {{
  const m = String(iso || '').match(/T(\\d{{2}}:\\d{{2}})/);
  return m ? m[1] : null;
}}

function isoDatePart(iso) {{
  const m = String(iso || '').match(/^(\\d{{4}}-\\d{{2}}-\\d{{2}})/);
  return m ? m[1] : null;
}}

function formatWindow(startIso, endIso) {{
  const sTime = isoTimePart(startIso);
  const eTime = isoTimePart(endIso);
  const sDate = isoDatePart(startIso);
  const eDate = isoDatePart(endIso);

  const startLabel = sTime || (startIso ? String(startIso) : '?');
  let endLabel = 'ongoing';
  if (eTime) {{
    endLabel = eTime;
    // Overnight/multi-day closures: flag the end time with a short date so
    // "20:00 → 05:00" doesn't read as if it ends the same evening it started.
    if (sDate && eDate && sDate !== eDate) {{
      const d = new Date(eDate + 'T00:00:00Z');
      const dayNum = d.getUTCDate();
      const mon = d.toLocaleString('en-GB', {{ month: 'short', timeZone: 'UTC' }});
      endLabel = eTime + ' (' + dayNum + ' ' + mon + ')';
    }}
  }}
  return startLabel + ' → ' + endLabel;
}}

function showRoadworksDetail(day, idx) {{
  const r = (ROADWORKS_BY_DAY[day] || [])[idx];
  if (!r) return;
  document.getElementById('modal-title').innerText = 'Travel Detail';
  let html = '<div class="back-link" onclick="backToDay()">‹ Back to ' + day + ' ' + MONTH_LABEL + '</div>';
  html += '<div class="detail-name">' + esc(r.road) + '</div>';
  html += '<div class="score-row">' + closureBadge(r.closure_type) + '</div>';
  if (r.location) html += '<div class="detail-field"><div class="detail-label">Location</div><div class="detail-value">' + esc(r.location) + '</div></div>';
  if (r.status)   html += '<div class="detail-field"><div class="detail-label">Status</div><div class="detail-value">' + esc(r.status) + '</div></div>';
  if (r.cause)    html += '<div class="detail-field"><div class="detail-label">Cause</div><div class="detail-value">' + esc(r.cause) + '</div></div>';
  if (r.start_time || r.end_time) {{
    html += '<div class="detail-field"><div class="detail-label">Window</div><div class="detail-value">' +
            esc(formatWindow(r.start_time, r.end_time)) + '</div></div>';
  }}
  if (r.comment) html += '<div class="detail-field"><div class="detail-label">Comment</div><div class="detail-value">' + esc(r.comment) + '</div></div>';
  document.getElementById('modal-body').innerHTML = html;
}}

function backToDay() {{
  if (currentMode === 'roadworks') {{
    document.getElementById('modal-title').innerText = 'Travel — ' + currentDay + ' ' + MONTH_LABEL;
    renderRoadworksList(currentDay);
  }} else {{
    document.getElementById('modal-title').innerText = 'Events — ' + currentDay + ' ' + MONTH_LABEL;
    renderDayList(currentDay);
  }}
}}
</script>
</body></html>"""

    components.html(html, height=grid_height, scrolling=False)



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
# ROADWORKS (National Highways Road & Lane Closures)
# =====================================================
# Adapted from roadworks_near_postcode.py: same DATEX II parsing / distance
# logic, but wired into this app's existing `supabase` client and postcode
# geocoding instead of running as its own standalone script.

def haversine_miles(lat1, lon1, lat2, lon2):
    r = 3958.8  # earth radius, miles
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def _parse_pos_list(pos_list_str):
    """posList is a space-separated list of 'lat lon lat lon ...' (WGS84)."""
    nums = [float(n) for n in pos_list_str.split()]
    return list(zip(nums[0::2], nums[1::2]))


def _points_from_loc(loc):
    pts = []
    linear = loc.get("locLinearLocation")
    if linear:
        gml = linear.get("gmlLineString", {}).get("locGmlLineString", {})
        pos_list = gml.get("posList")
        if pos_list:
            pts.extend(_parse_pos_list(pos_list))
    return pts


def _locs_from_reference(location_reference):
    if not location_reference:
        return []
    grouped = location_reference.get("locLocationGroupByList")
    if grouped:
        return grouped.get("locationContainedInGroup", [])
    return [location_reference]


def _extract_points(location_reference):
    """Return list of (lat, lon) points, handling both the single-location
    and multi-location (grouped) schema variants documented for this API."""
    points = []
    for loc in _locs_from_reference(location_reference):
        points.extend(_points_from_loc(loc))
    return points


def _extract_road_and_description(location_reference):
    roads = set()
    descs = []
    for loc in _locs_from_reference(location_reference):
        linear = loc.get("locLinearLocation", {})
        supp = linear.get("supplementaryPositionalDescription", {})
        desc = supp.get("locationDescription")
        if desc:
            descs.append(desc)
        single = loc.get("locSingleRoadLinearLocation", {})
        for lw in single.get("linearWithinLinearElement", []):
            code = lw.get("linearElement", {}).get("locLinearElementByCode", {})
            rn = code.get("roadName")
            if rn:
                roads.add(rn)
    road = ", ".join(sorted(roads)) if roads else "Unknown road"
    desc = "; ".join(dict.fromkeys(descs))
    return road, desc


def _nearest_point(lat, lon, points):
    """Return (point, distance_miles) for the closest point, or (None, None)."""
    if not points:
        return None, None
    best = min(points, key=lambda p: haversine_miles(lat, lon, p[0], p[1]))
    return best, haversine_miles(lat, lon, best[0], best[1])


def _stable_record_id(node, location_ref):
    """Prefer the DATEX II idG (stable across repeated calls). Fall back to a
    deterministic hash of key fields if idG is ever missing."""
    idg = node.get("idG")
    if idg:
        return idg
    basis = json.dumps({
        "loc": location_ref,
        "comment": node.get("generalPublicComment"),
        "validity": node.get("validity"),
    }, sort_keys=True)
    return "hash-" + hashlib.sha256(basis.encode("utf-8")).hexdigest()[:32]


def _nh_seconds_to_wait(resp, default=5):
    """Pull a wait time out of a 429 response: prefer the Retry-After header,
    fall back to parsing '...Try again in N seconds' from the JSON body."""
    retry_after = resp.headers.get("Retry-After")
    if retry_after:
        try:
            return float(retry_after) + 0.5
        except ValueError:
            pass
    match = re.search(r"(\d+(?:\.\d+)?)\s*seconds?", resp.text or "")
    if match:
        return float(match.group(1)) + 0.5
    return default


def fetch_nh_closures(subscription_key, closure_type=None, start=None, end=None):
    """Yields situationRecord dicts from the National Highways closures API,
    following pagination via the x-next header."""
    params = {}
    if closure_type:
        params["closureType"] = closure_type
    if start:
        params["startDateTime"] = start
    if end:
        params["endDateTime"] = end

    url = NH_BASE_URL + ("?" + urllib.parse.urlencode(params) if params else "")
    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "X-Response-MediaType": "application/json",
        "X-Data-Format": "DATEXII",
        "Accept": "application/json",
    }

    seen_urls = set()
    while url and url not in seen_urls:
        seen_urls.add(url)
        max_retries = 3
        resp = None
        for attempt in range(max_retries + 1):
            resp = requests.get(url, headers=headers, timeout=30)
            if resp.status_code == 429 and attempt < max_retries:
                time.sleep(_nh_seconds_to_wait(resp))
                continue
            if not resp.ok:
                raise RuntimeError(f"HTTP {resp.status_code} calling National Highways API: {resp.text[:300]}")
            break

        body = resp.json()
        next_url = resp.headers.get("x-next")
        payload = body.get("D2Payload", body)
        for situation in payload.get("situation", []):
            for record in situation.get("situationRecord", []):
                yield record

        url = next_url
        if url:
            time.sleep(0.5)  # courtesy pause between pages


def summarize_roadworks_record(record, ref_lat, ref_lon, radius_miles, closure_type):
    node = record.get("sitRoadOrCarriagewayOrLaneManagement", record)
    location_ref = node.get("locationReference", {})
    points = _extract_points(location_ref)
    best_point, distance = _nearest_point(ref_lat, ref_lon, points)
    if distance is None or distance > radius_miles:
        return None

    validity = node.get("validity", {})
    time_spec = validity.get("validityTimeSpecification", {})
    cause = node.get("cause", {})
    comments = node.get("generalPublicComment", [])
    comment_text = "; ".join(c.get("comment", "") for c in comments if c.get("comment"))
    road, desc = _extract_road_and_description(location_ref)

    return {
        "record_id":     _stable_record_id(node, location_ref),
        "closure_type":  closure_type,
        "distance_miles": round(distance, 2),
        "road":          road,
        "location":      desc,
        "status":        validity.get("validityStatus"),
        "start_time":    time_spec.get("overallStartTime"),
        "end_time":      time_spec.get("overallEndTime"),
        "cause":         cause.get("causeType"),
        "comment":       comment_text,
        "latitude":      best_point[0] if best_point else None,
        "longitude":     best_point[1] if best_point else None,
    }


def to_roadworks_db_row(summary):
    """Drop fields that are relative to a specific search (not a fixed
    attribute of the closure itself) before writing to Supabase."""
    row = dict(summary)
    row.pop("distance_miles", None)
    # Explicit rather than relying on the column's DB-side default, so this
    # keeps working correctly even if the default ever changes or the table
    # gets recreated. The Street Manager receiver stamps its own rows with
    # source="street_manager" the same way.
    row["source"] = "national_highways"
    return row


def fetch_roadworks(lat, lon, radius, status, progress):
    """Fetch National Highways closures (planned + unplanned) near lat/lon
    within `radius` miles. Mirrors the fetch_ticketmaster / fetch_skiddle
    pattern: returns a list of summary dicts ready for storage."""
    if not NH_API_KEY:
        status.text("⚠ Roadworks skipped — add NH_API_KEY to secrets")
        return []

    now = datetime.now(timezone.utc)
    windows = [
        ("unplanned", now - timedelta(hours=ROADWORKS_HOURS_BACK), now),
        ("planned",   now, now + timedelta(days=ROADWORKS_DAYS_AHEAD)),
    ]

    results   = []
    seen_ids  = set()
    for i, (ctype, start_dt, end_dt) in enumerate(windows):
        status.text(f"Querying {ctype} roadworks...")
        start = start_dt.strftime("%Y-%m-%dT%H:%M:%S")
        end   = end_dt.strftime("%Y-%m-%dT%H:%M:%S")
        try:
            for record in fetch_nh_closures(NH_API_KEY, closure_type=ctype, start=start, end=end):
                summary = summarize_roadworks_record(record, lat, lon, radius, ctype)
                # The unplanned/planned windows can both match an ongoing closure
                # (or the API's own paging can resurface a record) — keep only the
                # first sighting of a given record_id so we never send duplicate
                # rows into the same upsert batch.
                if summary and summary["record_id"] not in seen_ids:
                    seen_ids.add(summary["record_id"])
                    results.append(summary)
        except RuntimeError as e:
            st.warning(f"National Highways API ({ctype}): {e}")
        progress.progress(min(1.0, 0.5 + (i + 1) * 0.25))

    return results


def table_fetch_all(table_name: str, select: str = "*", page_size: int = 1000) -> list:
    """Read a Supabase table with .range() paging until all rows are returned,
    bypassing the default 1 000-row cap. Same approach as rpc_fetch_all, but
    for a plain table select instead of an RPC call."""
    all_rows = []
    offset = 0
    while True:
        resp = (
            supabase.table(table_name)
            .select(select)
            .range(offset, offset + page_size - 1)
            .execute()
        )
        batch = resp.data or []
        all_rows.extend(batch)
        if len(batch) < page_size:
            break          # last (or only) page
        offset += page_size
    return all_rows


def get_roadworks_within_radius(lat, lon, radius):
    """Read every stored closure from Supabase and filter to those within
    `radius` miles of (lat, lon), computing distance client-side (this table
    has no PostGIS radius RPC like BurdySteupTest does)."""
    try:
        rows = table_fetch_all(ROADWORKS_TABLE, "*")
    except Exception as e:
        st.warning(f"Couldn't read {ROADWORKS_TABLE} from Supabase: {e}")
        return pd.DataFrame()

    nearby = []
    for r in rows:
        rlat, rlon = r.get("latitude"), r.get("longitude")
        if rlat is None or rlon is None:
            continue
        dist = haversine_miles(lat, lon, rlat, rlon)
        if dist <= radius:
            r = dict(r)
            r["distance_miles"] = round(dist, 2)
            nearby.append(r)

    nearby.sort(key=lambda r: r["distance_miles"])
    df = pd.DataFrame(nearby)

    # Both dedup steps below only affect what's *displayed* — every row stays
    # in Supabase untouched, each still keyed by its own unique record_id.
    # When duplicates are found, keep the newest one: "id" is the table's
    # auto-increment primary key, so the highest id is the most recently
    # inserted row.
    if not df.empty and "id" in df.columns:
        df = df.sort_values("id", ascending=False)

    # Defensive: if the table ever ends up with duplicate record_ids (e.g. the
    # upsert's on_conflict target isn't backed by a real unique constraint in
    # Postgres), don't let that surface as duplicate rows in the UI.
    if not df.empty and "record_id" in df.columns:
        df = df.drop_duplicates(subset="record_id", keep="first")
    # National Highways can re-publish the same real-world closure under a
    # brand-new record_id (e.g. a revised/re-versioned situation record), which
    # the record_id-based dedup above can't catch. If two rows describe the
    # same location, comment, and time window, treat them as one closure and
    # keep the newest.
    dedup_cols = ["location", "comment", "start_time", "end_time"]
    if not df.empty and all(c in df.columns for c in dedup_cols):
        df = df.drop_duplicates(subset=dedup_cols, keep="first")

    df = df.sort_values("distance_miles")
    return df


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


def get_all_time_events_within_radius(lat, lon, radius, type_filters=None, venue_filters=None):
    """search_within_radius filters out anything before "now" server-side
    (see its WHERE clause), so the live search's filtered_df never contains
    historical events — that's why past calendar days always showed 0. This
    calls the exact same RPC, same radius/type/venue filters, but with a
    deliberately ancient now_utc so its date comparison never excludes a row.
    Used only to get accurate historical counts for past days in the
    calendar; the live search itself is untouched."""
    params = {
        "lat": lat, "lng": lon, "radius_meters": radius * 1609.34,
        "now_utc": "1900-01-01T00:00:00+00:00",
        "type_filters": type_filters or [], "venue_filters": venue_filters or [],
    }
    rows = rpc_fetch_all("search_within_radius", params)
    return pd.DataFrame(rows)

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

        # ── ROADWORKS (National Highways) ──
        rw_count = 0
        try:
            rw_events = fetch_roadworks(lat, lon, radius, status, progress)
        except RuntimeError as e:
            st.error(str(e))
            rw_events = []
        if rw_events:
            rw_rows = [to_roadworks_db_row(r) for r in rw_events]
            try:
                supabase.table(ROADWORKS_TABLE).upsert(rw_rows, on_conflict="record_id").execute()
            except Exception as e:
                st.warning(f"Couldn't save roadworks to Supabase: {e}")
            rw_count = len(rw_rows)
        status.text(f"✓ Roadworks: {rw_count} closures processed")

        # Read back everything within radius (fresh inserts + anything already stored)
        st.session_state["roadworks_df"] = get_roadworks_within_radius(lat, lon, radius)

        # All-time (incl. historical) events within radius, for accurate
        # past-day counts in the calendar — the live search below only
        # returns current/future events by design.
        st.session_state["all_events_df"] = get_all_time_events_within_radius(lat, lon, radius)

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
        st.session_state["_last_search_key"]  = f"{postcode}|{radius}"
        st.session_state["_last_filter_key"] = "|"
        st.session_state.pop("calendar_year", None)
        st.session_state.pop("calendar_month", None)

        new_events_count = after_total - before_total
        st.session_state["new_events_count"] = new_events_count

        log_search_event(
            action="fetch_sync",
            postcode=postcode,
            radius=radius,
            lat=lat,
            lon=lon,
            results_count=after_radius_count,
            new_events_count=new_events_count,
        )

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
            st.session_state.pop("calendar_year", None)
            st.session_state.pop("calendar_month", None)

            # Just re-read whatever roadworks are already stored within radius —
            # Search doesn't hit the National Highways API (that only happens on Fetch & Sync)
            st.session_state["roadworks_df"] = get_roadworks_within_radius(lat, lon, radius)

            # All-time (incl. historical) events within radius, for accurate
            # past-day counts in the calendar — the live search above only
            # returns current/future events by design.
            st.session_state["all_events_df"] = get_all_time_events_within_radius(lat, lon, radius)

            log_search_event(
                action="search",
                postcode=postcode,
                radius=radius,
                lat=lat,
                lon=lon,
                results_count=len(rows),
            )

            try:
                _search_total = supabase.table("BurdySteupTest").select("ID", count="exact").execute().count or 0
            except Exception:
                _search_total = "—"

            _today_date = datetime.now(timezone.utc).date()
            _week_end   = _today_date + timedelta(days=6)
            _events_today_radius = _count_in_date_range(st.session_state["search_df"], _today_date, _today_date)
            _events_week_radius  = _count_in_date_range(st.session_state["search_df"], _today_date, _week_end)

            stats_slot.markdown(
                _stat_row_search(_events_today_radius, _events_week_radius, len(rows), _search_total, radius),
                unsafe_allow_html=True
            )

df    = st.session_state.get("search_df", pd.DataFrame())
label = st.session_state.get("search_label", "")

# Only show results if Search or Fetch & Sync has actually been pressed for
# the postcode/radius currently in the inputs — dragging the radius slider
# or editing the postcode afterward hides the stale results until re-run.
_results_committed = st.session_state.get("_last_search_key") == f"{postcode}|{radius}"
if not _results_committed:
    df = pd.DataFrame()
    st.session_state["search_df"]     = pd.DataFrame()
    st.session_state["filtered_df"]   = pd.DataFrame()
    st.session_state["search_label"]  = ""
    st.session_state["roadworks_df"]  = pd.DataFrame()
    stats_slot.markdown(
        _stat_row_initial(_initial_total, _initial_today, _initial_this_week),
        unsafe_allow_html=True
    )

# ── Postcode info panel ──
_pci = st.session_state.get("postcode_info") if _results_committed else None
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

    filter_l, filter_m, filter_r = st.columns(3)

    with filter_l:
        if type_col:
            type_options   = sorted(df[type_col].dropna().unique().tolist())
            selected_types = st.multiselect("Filter by Event Type", options=type_options,
                                            placeholder="All types")
        else:
            selected_types = []

    with filter_m:
        if venue_col:
            venue_options   = sorted(df[venue_col].dropna().unique().tolist())
            selected_venues = st.multiselect("Filter by Venue", options=venue_options,
                                             placeholder="All venues")
        else:
            selected_venues = []

    with filter_r:
        _rating_options  = ["Blockbuster", "Strong", "Moderate", "Low"]
        selected_ratings = st.multiselect("Filter by Rating", options=_rating_options,
                                          placeholder="All ratings")

    # Re-query Supabase when Type/Venue filters change
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
            st.session_state["all_events_df"] = get_all_time_events_within_radius(
                _lat, _lon, _rad,
                selected_types or [],
                selected_venues or [],
            )

    filtered_df = st.session_state.get("filtered_df", df)

    # Rating is computed client-side (not in Supabase), so filter it locally
    filtered_df = add_impact_scores(filtered_df)
    if selected_ratings:
        filtered_df = filtered_df[filtered_df["Rating"].isin(selected_ratings)]

    # Reset pagination whenever any filter (incl. Rating) changes
    _local_filter_key = f"{_filter_key}|{','.join(sorted(selected_ratings))}"
    if _local_filter_key != st.session_state.get("_last_local_filter_key"):
        st.session_state["_last_local_filter_key"] = _local_filter_key
        st.session_state["page_num"] = 1

    # ── View toggle: subtle pill-style buttons, right-aligned, Calendar shown by default ──
    if "view_mode" not in st.session_state:
        st.session_state["view_mode"] = "Calendar"

    def _toggle_pill_css(key, active):
        if active:
            return f"""<style>
.st-key-{key} .stButton > button {{
    background: var(--orange-glow) !important;
    color: var(--orange) !important;
    border: 1px solid rgba(232,82,10,.32) !important;
    box-shadow: none !important;
    border-radius: 999px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    font-weight: 600 !important;
    letter-spacing: .07em !important;
    text-transform: uppercase !important;
    padding: 7px 16px !important;
}}
.st-key-{key} .stButton > button:hover {{
    background: var(--orange-glow) !important;
    transform: none !important;
    box-shadow: none !important;
}}
</style>"""
        return f"""<style>
.st-key-{key} .stButton > button {{
    background: transparent !important;
    color: var(--text-dim) !important;
    border: 1px solid var(--border) !important;
    box-shadow: none !important;
    border-radius: 999px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    font-weight: 500 !important;
    letter-spacing: .07em !important;
    text-transform: uppercase !important;
    padding: 7px 16px !important;
}}
.st-key-{key} .stButton > button:hover {{
    background: var(--surface2) !important;
    color: var(--text) !important;
    transform: none !important;
    box-shadow: none !important;
}}
</style>"""

    _cal_active  = st.session_state["view_mode"] == "Calendar"
    _list_active = st.session_state["view_mode"] == "List"
    _map_active  = st.session_state["view_mode"] == "Map"

    _spacer, _btn_cal, _btn_list, _btn_map = st.columns([5, 1.3, 1.3, 1.3])
    with _btn_cal:
        with st.container(key="btn_view_calendar_wrap"):
            st.markdown(_toggle_pill_css("btn_view_calendar_wrap", _cal_active), unsafe_allow_html=True)
            if st.button("Calendar", use_container_width=True, key="btn_view_calendar"):
                st.session_state["view_mode"] = "Calendar"
                st.rerun()
    with _btn_list:
        with st.container(key="btn_view_list_wrap"):
            st.markdown(_toggle_pill_css("btn_view_list_wrap", _list_active), unsafe_allow_html=True)
            if st.button("List", use_container_width=True, key="btn_view_list"):
                st.session_state["view_mode"] = "List"
                st.rerun()
    with _btn_map:
        with st.container(key="btn_view_map_wrap"):
            st.markdown(_toggle_pill_css("btn_view_map_wrap", _map_active), unsafe_allow_html=True)
            if st.button("Map", use_container_width=True, key="btn_view_map"):
                st.session_state["view_mode"] = "Map"
                st.rerun()

    view_mode = st.session_state["view_mode"]

    if view_mode == "Map":
        st.markdown(f"""
        <div style="background:var(--surface);border:1px solid var(--border);border-radius:16px;
                     padding:60px 32px;text-align:center;box-shadow:0 2px 12px rgba(0,0,0,.06);">
          <div style="font-size:32px;margin-bottom:12px;">🗺️</div>
          <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:18px;
                       color:var(--text);margin-bottom:6px;">Map view coming soon</div>
          <div style="font-family:'DM Mono',monospace;font-size:12px;color:var(--text-dim);">
            Events will be plotted geographically here in a future update.
          </div>
        </div>
        """, unsafe_allow_html=True)

    elif view_mode == "List":
        # ── Pagination controls ──
        if "page_num" not in st.session_state:
            st.session_state["page_num"] = 1
        if "rows_per_page" not in st.session_state:
            st.session_state["rows_per_page"] = 25

        # Roadworks are merged into the same list, mapped onto the events' display
        # columns (Name / Venue Name / Date / Type / City / Impact Score / Rating).
        roadworks_df   = st.session_state.get("roadworks_df", pd.DataFrame())
        roadworks_rows = build_roadworks_list_rows(roadworks_df)
        combined_df = (
            pd.concat([filtered_df, roadworks_rows], ignore_index=True, sort=False)
            if not roadworks_rows.empty else filtered_df
        )

        per_page    = st.session_state["rows_per_page"]
        total_pages = max(1, -(-len(combined_df) // per_page))
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
            n_rw = len(roadworks_rows)
            if n_rw:
                total_label = f"{len(filtered_df)} events · {n_rw} roadworks"
            elif len(filtered_df) == len(df):
                total_label = f"{len(filtered_df)} events"
            else:
                total_label = f"{len(filtered_df)} filtered results"
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

        render_table(combined_df, page=st.session_state["page_num"], per_page=per_page)

    else:
        # ── Calendar view ──
        col_lower = {c.lower(): c for c in filtered_df.columns}
        date_col  = col_lower.get("event_date") or col_lower.get("date") or col_lower.get("eventdate")

        valid_dates = []
        if date_col:
            valid_dates = [d for d in filtered_df[date_col].apply(_parse_date_safe) if d is not None]

        if "calendar_year" not in st.session_state or "calendar_month" not in st.session_state:
            if valid_dates:
                _min_date = min(valid_dates)
                st.session_state["calendar_year"]  = _min_date.year
                st.session_state["calendar_month"] = _min_date.month
            else:
                _today = datetime.now(timezone.utc).date()
                st.session_state["calendar_year"]  = _today.year
                st.session_state["calendar_month"] = _today.month

        cal_year  = st.session_state["calendar_year"]
        cal_month = st.session_state["calendar_month"]

        nav_l, nav_mid, nav_r = st.columns([1, 4, 1])
        with nav_l:
            if st.button("‹ Prev month", use_container_width=True):
                new_month, new_year = cal_month - 1, cal_year
                if new_month < 1:
                    new_month, new_year = 12, new_year - 1
                st.session_state["calendar_year"]  = new_year
                st.session_state["calendar_month"] = new_month
                st.rerun()
        with nav_mid:
            st.markdown(
                f"<div style='text-align:center;font-family:Syne,sans-serif;font-weight:800;"
                f"font-size:18px;padding-top:6px;color:#141518;'>"
                f"{calendar.month_name[cal_month]} {cal_year}</div>",
                unsafe_allow_html=True,
            )
        with nav_r:
            if st.button("Next month ›", use_container_width=True):
                new_month, new_year = cal_month + 1, cal_year
                if new_month > 12:
                    new_month, new_year = 1, new_year + 1
                st.session_state["calendar_year"]  = new_year
                st.session_state["calendar_month"] = new_month
                st.rerun()

        render_calendar(
            filtered_df, cal_year, cal_month,
            st.session_state.get("roadworks_df", pd.DataFrame()),
            lat=st.session_state.get("_search_lat"),
            lon=st.session_state.get("_search_lon"),
            all_events_df=st.session_state.get("all_events_df", pd.DataFrame()),
        )
