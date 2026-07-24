import streamlit as st
import requests
import re
from PIL import Image
from io import BytesIO
import streamlit.components.v1 as components

# =====================================================
# PAGE CONFIG
# =====================================================

ICON_URL = "https://ujrublkoqtpijwijklvq.supabase.co/storage/v1/object/sign/Brand%20Logo/Bird%20Logo%20Left.png?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV9jYTQwZTg5ZS00MTVkLTQ0NjEtYTZjZi00OTI2MDIwYmYyZTkiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJCcmFuZCBMb2dvL0JpcmQgTG9nbyBMZWZ0LnBuZyIsImlhdCI6MTc4MDU5ODM2NSwiZXhwIjoxODEyMTM0MzY1fQ.OMa5cbOtPSUZR4JTjlT3Mm1XBZlgi2rugZOQx7SLCX0"

response = requests.get(ICON_URL)
icon = Image.open(BytesIO(response.content))

st.set_page_config(
    page_title="Burdy · Site Map",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="auto",
)

# =====================================================
# CUSTOM CSS — identical to the rest of the Burdy site
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

/* Streamlit applies a filter/transform to the main content wrapper while a
   st.dialog is open, which changes the containing block for any
   position:fixed descendant (our site header) and breaks its pinning.
   Force these back off so the header always stays viewport-fixed. */
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stBottomBlockContainer"],
.main {
    filter: none !important;
    -webkit-filter: none !important;
    transform: none !important;
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--text-muted); border-radius: 3px; }

.block-container {
    padding: 2rem 3rem 80px !important;
    max-width: 1400px !important;
}

.burdy-logo {
    display: flex; align-items: center; gap: 12px;
    font-family: 'DM Sans', sans-serif;
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
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 28px 0 !important;
}

/* ── Hero-style intro (pill + headline + body-text), same pattern as
      About Us's intro block, contained within the page width ── */
.about-hero {
    text-align: center;
    padding: 8px 20px 4px;
    margin-bottom: 8px;
}
.about-pill {
    display: inline-block;
    background: var(--orange-glow);
    border: 1px solid rgba(232,82,10,.22);
    border-radius: 999px;
    padding: 5px 16px;
    margin-bottom: 18px;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: var(--orange);
    letter-spacing: .12em;
    text-transform: uppercase;
    font-weight: 500;
}
.about-headline {
    font-family: 'DM Sans', sans-serif;
    font-weight: 800;
    font-size: 28px;
    letter-spacing: -.03em;
    color: var(--text);
    max-width: 780px;
    margin: 0 auto 16px;
    line-height: 1.2;
}
.about-body {
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
    color: var(--text-dim);
    max-width: 640px;
    margin: 0 auto;
    line-height: 1.75;
}

/* ── Section heading (matches About Us's "Our Values" heading) ── */
.section-heading {
    font-family: 'DM Sans', sans-serif;
    font-weight: 700;
    font-size: 20px;
    letter-spacing: -.02em;
    color: var(--text);
    text-align: center;
    margin: 8px 0 24px;
}

/* ── Sitemap link cards — same visual style as the "stat-box" cards used
      throughout initial_event_run.py (white surface, 12px radius, gradient
      bar across the bottom, centered content) — no live figures here, just
      matching the look. Scoped via Streamlit's documented st.container(key=...)
      class convention (.st-key-<key>) rather than internal data-testid
      attributes — those are implementation details that can shift between
      Streamlit versions, which is why earlier attempts rendered
      inconsistently. Every sitemap-card-* container gets this styling. ── */
div[class*="st-key-sitemap-card-"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 4px 4px 16px !important;
    position: relative !important;
    overflow: hidden !important;
    box-shadow: 0 2px 8px rgba(0,0,0,.05) !important;
    transition: box-shadow .15s, border-color .15s !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    text-align: center !important;
    height: 100% !important;
    min-height: 148px !important;
    box-sizing: border-box !important;
}
div[class*="st-key-sitemap-card-"]::after {
    content: '' !important;
    position: absolute !important;
    bottom: 0 !important; left: 0 !important; right: 0 !important; height: 3px !important;
    background: linear-gradient(90deg, var(--orange), var(--green), transparent) !important;
    z-index: 5 !important;
}
div[class*="st-key-sitemap-card-"]:hover {
    border-color: rgba(232,82,10,.3) !important;
    box-shadow: 0 4px 14px rgba(0,0,0,.08) !important;
}
[data-testid="stPageLink"] {
    padding: 14px 16px 2px !important;
    width: 100% !important;
    justify-content: center !important;
}
[data-testid="stPageLink"] p {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    letter-spacing: -.01em !important;
    color: var(--text) !important;
    text-align: center !important;
}
[data-testid="stPageLink"]:hover p {
    color: var(--orange) !important;
}
.sitemap-desc {
    font-family: 'DM Sans', sans-serif;
    font-size: 12.5px;
    line-height: 1.6;
    color: var(--text-dim);
    padding: 0 16px;
    text-align: center;
}
.sitemap-path {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: var(--text-muted);
    padding: 8px 16px 0;
    letter-spacing: .02em;
    text-align: center;
    margin-top: auto; /* pins the path to the card's bottom regardless of description length, so every card's footer lines up */
}

/* ── Sitemap card grid: fixed-width columns (not stretched to fill),
      centered as a row, and stretched to equal height within each row —
      this is what makes rows with fewer than 3 cards (Main, Support,
      Subscribers, This Page) sit centered instead of left-packed with
      empty space on the right, and every card in a row match height even
      if one description wraps to an extra line. Also key-scoped, this time
      to the row wrapper, so it can't affect columns anywhere else. ── */
div[class*="st-key-sitemap-row-"] div[data-testid="stHorizontalBlock"] {
    justify-content: center !important;
    align-items: stretch !important;
    gap: 20px !important;
}
div[class*="st-key-sitemap-row-"] div[data-testid="stColumn"] {
    flex: 0 0 340px !important;
    width: 340px !important;
    max-width: 340px !important;
    min-width: 340px !important;
    display: flex !important;
}
div[class*="st-key-sitemap-row-"] div[data-testid="stColumn"] > div {
    width: 100% !important;
    display: flex !important;
    flex-direction: column !important;
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
    .about-headline { font-size: 20px !important; }
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

# ── Custom ‹ / › toggle ────────────────────────────────────────────────────
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
# HEADER — identical block used across the whole site
# =====================================================

BIRD_LOGO_URL = "https://ujrublkoqtpijwijklvq.supabase.co/storage/v1/object/sign/Brand%20Logo/Bird%20Logo%20Left.png?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV9jYTQwZTg5ZS00MTVkLTQ0NjEtYTZjZi00OTI2MDIwYmYyZTkiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJCcmFuZCBMb2dvL0JpcmQgTG9nbyBMZWZ0LnBuZyIsImlhdCI6MTc4MDU5ODM2NSwiZXhwIjoxODEyMTM0MzY1fQ.OMa5cbOtPSUZR4JTjlT3Mm1XBZlgi2rugZOQx7SLCX0"
WORD_LOGO_URL = "https://ujrublkoqtpijwijklvq.supabase.co/storage/v1/object/sign/Brand%20Logo/Font%20logo.png?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV9jYTQwZTg5ZS00MTVkLTQ0NjEtYTZjZi00OTI2MDIwYmYyZTkiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJCcmFuZCBMb2dvL0ZvbnQgbG9nby5wbmciLCJpYXQiOjE3ODA1OTg0MTEsImV4cCI6MTgxMjEzNDQxMX0.pt-zS-TT80l_mp-_jGklDgtx8K2wc0uafgW36VDklbo"

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
# HERO — page intro
# =====================================================

st.markdown("""
<div class="about-hero">
  <div class="about-pill">◆ &nbsp;Navigate</div>
  <div class="about-headline">Site Map</div>
  <div class="about-body">Every page on Burdy, in one place.</div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# SITE PAGES
# =====================================================
# NOTE: st.page_link resolves paths relative to whichever script Streamlit
# was actually launched with (the entrypoint) — not relative to this file.
# Since there's no fixed entrypoint yet, HOME_ENTRYPOINT below is the one
# line to change once that's settled. Everything else on this page is
# layout/styling only. The rest of PAGES assumes About Us, Contact Us,
# Terms & Conditions, Privacy Policy, and this Site Map all live together
# in a `pages/` folder next to the entrypoint, per Streamlit's standard
# multipage convention — adjust those paths too if that's not accurate.

HOME_ENTRYPOINT = "initial event run.py"

CATEGORIES = [
    {
        "title": "Main",
        "pages": [
            {
                "path": HOME_ENTRYPOINT,
                "label": "Home — Event & Roadworks Search",
                "desc": "Search live events and roadworks within a radius of any UK postcode.",
            },
            {
                "path": "pages/Demo_Page.py",
                "label": "Demo Page",
                "desc": "A guided walkthrough of what Burdy can do.",
            },
        ],
    },
    {
        "title": "Company",
        "pages": [
            {
                "path": "pages/About_us.py",
                "label": "About Us",
                "desc": "Who we are, our mission and vision, and what we value.",
            },
            {
                "path": "pages/Careers.py",
                "label": "Careers",
                "desc": "Open roles and what it's like to work at Burdy.",
            },
            {
                "path": "pages/Investors.py",
                "label": "Investors",
                "desc": "Company updates, financial highlights, and investor relations.",
            },
        ],
    },
    {
        "title": "Support",
        "pages": [
            {
                "path": "pages/Contact_Us.py",
                "label": "Contact Us",
                "desc": "Send us a message and we'll get back to you.",
            },
            {
                "path": "pages/FAQ's.py",
                "label": "FAQ's",
                "desc": "Answers to common questions about Burdy.",
            },
        ],
    },
    {
        "title": "Subscribers",
        "pages": [
            {
                "path": "pages/Subscribers_Page.py",
                "label": "Subscribers Page",
                "desc": "Manage your subscription and account details.",
            },
            {
                "path": "pages/Subscribers_Calendar.py",
                "label": "Subscribers Calendar",
                "desc": "Your personalised calendar of monitored events.",
            },
        ],
    },
    {
        "title": "Legal",
        "pages": [
            {
                "path": "pages/Terms and Conditions.py",
                "label": "Terms & Conditions",
                "desc": "The terms that govern use of Burdy's services.",
            },
            {
                "path": "pages/Privacy_Policy.py",
                "label": "Privacy Policy",
                "desc": "How we collect, store and protect your data.",
            },
            {
                "path": "pages/Accessibility_Statement.py",
                "label": "Accessibility Statement",
                "desc": "Our commitment to an accessible experience for all users.",
            },
        ],
    },
    {
        "title": "This Page",
        "pages": [
            {
                "path": "pages/Site_Map.py",
                "label": "Site Map",
                "desc": "You're here — every page on Burdy, in one place.",
            },
        ],
    },
]


def _slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _render_page_card(page, key):
    with st.container(border=True, key=key):
        try:
            st.page_link(page["path"], label=page["label"])
        except Exception:
            # Streamlit resolves st.page_link paths relative to whatever
            # script it was actually launched with — if that's not a
            # fixed, known entrypoint yet, this call can fail depending
            # on how the app happens to be run. Fall back to a plain,
            # non-clickable label rather than crashing the whole page.
            st.markdown(
                f'<div style="font-family:\'DM Sans\',sans-serif;font-weight:700;'
                f'font-size:15px;color:var(--text-muted);padding:14px 16px 2px;">'
                f'⚠ {page["label"]}</div>',
                unsafe_allow_html=True,
            )
        st.markdown(f'<div class="sitemap-desc">{page["desc"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sitemap-path">{page["path"]}</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)


_row_counter = 0
for category in CATEGORIES:
    st.markdown(f'<div class="section-heading">{category["title"]}</div>', unsafe_allow_html=True)
    pages = category["pages"]
    cat_slug = _slugify(category["title"])
    # Row wraps to a new st.columns() call every 3 cards, so categories with
    # more than 3 pages still lay out correctly, while a category with 1–2
    # pages only ever creates that many columns — no empty invisible column
    # left over to throw off the centering. Each row is wrapped in its own
    # keyed container so the CSS above can reliably find and center it.
    for row_start in range(0, len(pages), 3):
        row_pages = pages[row_start:row_start + 3]
        _row_counter += 1
        with st.container(key=f"sitemap-row-{_row_counter}"):
            cols = st.columns(len(row_pages))
            for col, page in zip(cols, row_pages):
                with col:
                    card_key = f"sitemap-card-{cat_slug}-{_slugify(page['label'])}"
                    _render_page_card(page, card_key)

# =====================================================
# FOOTER — identical block used across the whole site
# =====================================================

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
