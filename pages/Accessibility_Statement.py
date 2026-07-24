import streamlit as st
import requests
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
    page_title="Burdy · Accessibility Statement",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="auto",
)

# =====================================================
# CUSTOM CSS — identical to the rest of the Burdy site
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;700;800&display=swap');

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
    margin-bottom: 24px;
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
    margin: 20px 0 !important;
}

/* ── Hero-style intro block (pill + headline), contained within the
      page width to match the rest of the site's simpler pages ── */
.page-hero {
    text-align: center;
    padding: 8px 20px 4px;
    margin-bottom: 8px;
}
.page-pill {
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
.page-headline {
    font-family: 'DM Sans', sans-serif;
    font-weight: 800;
    font-size: 26px;
    letter-spacing: -.03em;
    color: var(--text);
    max-width: 720px;
    margin: 0 auto 16px;
    line-height: 1.3;
}

/* ── Split image+text hero blocks — same pattern as the Mission/Vision
      sections on About Us (image + text, alternating sides, Ken Burns
      zoom, gradient fade) ── */
.mv-hero {
    display: flex;
    align-items: stretch;
    min-height: 280px;
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 24px;
    border: 1px solid var(--border);
    box-shadow: 0 2px 12px rgba(0,0,0,.06);
    background: var(--surface);
}
.mv-hero.reverse { flex-direction: row-reverse; }
.mv-img {
    flex: 0 0 40%;
    position: relative;
    overflow: hidden;
}
.mv-img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    animation: mvKenburns 16s ease-in-out infinite alternate;
    transform-origin: center center;
}
@keyframes mvKenburns {
    0%   { transform: scale(1)    translateX(0)  translateY(0); }
    100% { transform: scale(1.08) translateX(1%) translateY(-1%); }
}
.mv-img.fade-right::after {
    content: '';
    position: absolute; inset: 0;
    background: linear-gradient(to right, transparent 65%, var(--surface) 100%);
}
.mv-img.fade-left::after {
    content: '';
    position: absolute; inset: 0;
    background: linear-gradient(to left, transparent 65%, var(--surface) 100%);
}
.mv-text {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 36px 44px;
}
.mv-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: .14em;
    text-transform: uppercase;
    margin-bottom: 12px;
    font-weight: 500;
}
.mv-hero.commitment .mv-eyebrow { color: var(--green); }
.mv-hero.efforts .mv-eyebrow    { color: var(--orange); }
.mv-body {
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
    line-height: 1.75;
    color: var(--text-dim);
    max-width: 460px;
}
.mv-body b, .mv-body strong { color: var(--text); font-weight: 700; }

/* ── Content sections ── */
.section-title {
    font-family: 'DM Sans', sans-serif;
    font-weight: 700;
    font-size: 15px;
    letter-spacing: -.01em;
    color: var(--text);
    margin: 0 0 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-title::before {
    content: '';
    width: 3px; height: 14px;
    background: linear-gradient(180deg, var(--orange), var(--green));
    border-radius: 2px;
    display: inline-block;
}
.section-body {
    font-family: 'DM Sans', sans-serif;
    font-size: 13.5px;
    line-height: 1.75;
    color: var(--text-dim);
}
.section-body b, .section-body strong { color: var(--text); font-weight: 700; }
.content-list {
    list-style: none;
    margin: 4px 0 0;
    padding: 0;
}
.content-list li {
    font-family: 'DM Sans', sans-serif;
    font-size: 13.5px;
    line-height: 1.7;
    color: var(--text-dim);
    padding: 3px 0 3px 20px;
    position: relative;
}
.content-list li::before {
    content: '';
    position: absolute; left: 0; top: 11px;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--orange);
}
.contact-line {
    font-family: 'DM Mono', monospace;
    font-size: 12.5px;
    color: var(--text-dim);
    margin: 4px 0;
}
.contact-line a { color: var(--orange); text-decoration: none; }
.contact-line a:hover { text-decoration: underline; }
.inline-link {
    color: var(--orange);
    font-weight: 700;
    text-decoration: none;
}
.inline-link:hover { text-decoration: underline; }
.two-col-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 24px;
    align-items: stretch;
}
.two-col-grid .control-card {
    margin-bottom: 0;
    height: 100%;
}

/* ── Popup dialog (success / warning) ── */
div[data-testid="stDialog"] {
    background: rgba(20,21,24,0.35) !important;
    backdrop-filter: blur(6px) !important;
    -webkit-backdrop-filter: blur(6px) !important;
    z-index: 500 !important;
    position: fixed !important;
    top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important;
    width: 100vw !important; height: 100vh !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
div[data-testid="stDialog"] [role="dialog"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    position: relative !important;
    overflow: hidden !important;
    box-shadow: 0 8px 32px rgba(0,0,0,.25) !important;
    margin: 0 !important; top: auto !important; left: auto !important; transform: none !important;
}
div[data-testid="stDialog"] [role="dialog"]::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, var(--orange), var(--green), transparent);
    z-index: 1;
}

/* ── Form styling (matches Contact Us) ── */
div[data-testid="stForm"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 28px 32px !important;
    position: relative !important;
    overflow: hidden !important;
    box-shadow: 0 2px 12px rgba(0,0,0,.06) !important;
}
div[data-testid="stForm"]::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, var(--orange), var(--green), transparent);
}
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    color: var(--text) !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: var(--orange) !important;
    box-shadow: 0 0 0 3px var(--orange-glow) !important;
}
div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: .06em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}
.stButton > button, button[kind="formSubmit"] {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 12px !important;
    letter-spacing: .06em !important;
    text-transform: uppercase !important;
    border-radius: 8px !important;
    padding: 10px 22px !important;
    transition: all .2s !important;
    background: var(--orange) !important;
    color: #fff !important;
    border: none !important;
    box-shadow: 0 3px 14px var(--orange-glow) !important;
}
.stButton > button:hover, button[kind="formSubmit"]:hover {
    background: var(--orange-dim) !important;
    box-shadow: 0 5px 20px rgba(232,82,10,.3) !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    background: rgba(0,0,0,.03) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-dim) !important;
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
[data-testid="stSidebar"]::after {
    content: '';
    position: absolute;
    top: 0; right: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, var(--orange), var(--green), transparent);
    z-index: 10;
}
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
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    color: var(--text-dim) !important;
}
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
[data-testid="stSidebar"] .stButton,
[data-testid="stSidebar"] .stButton > button {
    display: none !important;
}
[data-testid="stSidebar"] hr {
    border-top: 1px solid var(--border) !important;
    margin: 16px 0 !important;
}
[data-testid="stSidebar"] ::-webkit-scrollbar { width: 4px; }
[data-testid="stSidebar"] ::-webkit-scrollbar-track { background: var(--bg); }
[data-testid="stSidebar"] ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
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
    .block-container { padding: 2rem 1rem 60px !important; }
    .page-headline { font-size: 20px !important; }
    .two-col-grid {
        grid-template-columns: 1fr !important;
    }
    .mv-hero, .mv-hero.reverse {
        flex-direction: column !important;
    }
    .mv-img { flex: 0 0 180px !important; }
    .mv-img.fade-right::after,
    .mv-img.fade-left::after {
        background: linear-gradient(to bottom, transparent 60%, var(--surface) 100%) !important;
    }
    .mv-text { padding: 24px 20px !important; }
    .burdy-footer {
        padding: 10px 1rem !important;
        height: 44px !important;
        overflow: hidden !important;
        flex-wrap: nowrap !important;
    }
    .footer-badges { display: none !important; }
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
# HERO — page intro (wording preserved from original page)
# =====================================================

st.markdown("""
<div class="page-hero">
  <div class="page-pill">♿ &nbsp;Accessibility Statement</div>
  <div class="page-headline">
    Burdy Business is committed to ensuring digital accessibility for all users,
    including people with disabilities.
  </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# OUR COMMITMENT — split hero (image left, text right),
# same treatment as the Mission section on About Us
# =====================================================

st.markdown("""
<div class="mv-hero commitment">
  <div class="mv-img fade-right">
    <img src="https://images.unsplash.com/photo-1531152369337-1d0b0b9ef20d?w=1200&q=95" alt="Diverse crowd of people" />
  </div>
  <div class="mv-text">
    <div class="mv-eyebrow">Our Commitment</div>
    <div class="mv-body">
      We strive to make our website and digital services accessible to everyone,
      regardless of ability or technology used. We follow best practices and aim to
      meet the accessibility standards outlined in the
      <a href="https://www.w3.org/TR/WCAG21/" target="_blank" rel="noopener noreferrer"
        class="inline-link">Web Content Accessibility Guidelines (WCAG) 2.1 Level AA</a>.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# ONGOING EFFORTS — split hero (text left, image right),
# same treatment as the Vision section on About Us
# =====================================================

st.markdown("""
<div class="mv-hero efforts reverse">
  <div class="mv-img fade-left">
    <img src="https://images.unsplash.com/photo-1653407980547-31786734695b?w=1200&q=95" alt="People moving through a busy public space" />
  </div>
  <div class="mv-text">
    <div class="mv-eyebrow">Ongoing Efforts</div>
    <div class="mv-body">
      We continually evaluate and improve our website to meet accessibility standards.
      We perform regular audits, usability testing, and updates to ensure content is
      perceivable, operable, understandable, and robust for all users.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# SUPPORTING SECTIONS
# =====================================================

st.markdown("""
<div class="two-col-grid">
  <div class="control-card">
    <div class="section-title">Accessibility Features</div>
    <div class="section-body" style="margin-bottom:6px;">Our website includes:</div>
    <ul class="content-list">
      <li>Keyboard navigation support for all interactive elements</li>
      <li>Clear, readable fonts with sufficient contrast</li>
      <li>Alt text for all images and icons</li>
      <li>Semantic headings and structure for screen readers</li>
      <li>Forms with descriptive labels and error handling</li>
      <li>Responsive design for mobile and tablet users</li>
    </ul>
  </div>

  <div class="control-card">
    <div class="section-title">Known Limitations</div>
    <div class="section-body">
      While we strive for full accessibility, some third-party content or embedded
      services may not fully comply with WCAG 2.1 standards. We are actively working
      to minimize these limitations.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

_left, _center, _right = st.columns([1, 2.4, 1])

with _center:
    st.markdown("""
    <div class="control-card">
      <div class="section-title">Feedback</div>
      <div class="section-body" style="margin-bottom:10px;">
        We welcome feedback on accessibility issues. If you encounter any barriers or
        have suggestions, please contact us:
      </div>
      <div class="contact-line">✉ &nbsp;<a href="mailto:burdybusiness@outlook.com">burdybusiness@outlook.com</a></div>
      <div class="contact-line">☎ &nbsp;+44 (7348) 657940</div>
      <div class="section-body" style="margin-top:10px;">
        We aim to respond to all inquiries within <b>2 business days</b>.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # ACCESSIBILITY FEEDBACK FORM
    # =====================================================

    # Clear form fields on the run after a successful submission (must
    # happen before the widgets below are instantiated with these keys)
    if st.session_state.get("a11y_clear_form"):
        st.session_state.a11y_name = ""
        st.session_state.a11y_email = ""
        st.session_state.a11y_message = ""
        st.session_state.a11y_clear_form = False

    with st.form("accessibility_form"):
        st.markdown("""
        <div style="font-family:'DM Sans',sans-serif;font-weight:700;font-size:15px;
          color:#141518;margin-bottom:16px;">
          Submit Accessibility Feedback
        </div>
        """, unsafe_allow_html=True)
        name = st.text_input("Your Name (optional)", key="a11y_name")
        email = st.text_input("Your Email (optional)", key="a11y_email")
        message = st.text_area("Message / Feedback", height=150, key="a11y_message")
        submitted = st.form_submit_button("Send Feedback")

    # =====================================================
    # SUCCESS / WARNING POPUPS
    # =====================================================

    @st.dialog(" ")
    def _success_dialog():
        st.markdown("""
        <div style="text-align:center; padding: 8px 4px 4px;">
          <div style="font-size:36px; margin-bottom:10px;">✅</div>
          <div style="font-family:'DM Sans',sans-serif; font-weight:700; font-size:18px;
            color:#141518; margin-bottom:8px;">
            Feedback received!
          </div>
          <div style="font-family:'DM Sans',sans-serif; font-size:13px; color:#6B7280;">
            Thank you — we'll review it promptly.
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("Close", use_container_width=True, key="a11y_success_close"):
            st.session_state.a11y_show_success = False
            st.rerun()

    if st.session_state.get("a11y_show_success"):
        _success_dialog()

    @st.dialog(" ")
    def _warning_dialog(message_text):
        st.markdown(f"""
        <div style="text-align:center; padding: 8px 4px 4px;">
          <div style="font-size:36px; margin-bottom:10px;">⚠️</div>
          <div style="font-family:'DM Sans',sans-serif; font-weight:700; font-size:18px;
            color:#141518; margin-bottom:8px;">
            Please check the form
          </div>
          <div style="font-family:'DM Sans',sans-serif; font-size:13px; color:#6B7280;">
            {message_text}
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("Close", use_container_width=True, key="a11y_warning_close"):
            st.rerun()

    if submitted:
        if not message:
            _warning_dialog("Please enter your feedback before submitting.")
        else:
            try:
                # API key comes from Streamlit secrets — never hard-code credentials
                # in source code. Add this to secrets.toml:
                #   RESEND_API_KEY = "re_xxxxxxxxxxxxxxxxxxxxxxxx"
                resend_api_key = st.secrets["RESEND_API_KEY"]
                receiver_email = "burdybusiness@outlook.com"

                body_text = f"""
Name: {name or '(not provided)'}
Email: {email or '(not provided)'}

Message:
{message}
"""
                response = requests.post(
                    "https://api.resend.com/emails",
                    headers={
                        "Authorization": f"Bearer {resend_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "from": "Burdy Business Accessibility Feedback <onboarding@resend.dev>",
                        "to": [receiver_email],
                        "reply_to": email if email else receiver_email,
                        "subject": "[Accessibility Feedback] New submission",
                        "text": body_text,
                    },
                    timeout=15,
                )

                if response.status_code in (200, 201):
                    st.session_state.a11y_clear_form = True
                    st.session_state.a11y_show_success = True
                    st.rerun()
                else:
                    st.error(f"❌ Error sending email: {response.status_code} — {response.text}")

            except KeyError:
                st.error(
                    "❌ Email isn't configured yet. Add RESEND_API_KEY to this app's secrets."
                )
            except Exception as e:
                st.error(f"❌ Error sending email: {e}")

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
