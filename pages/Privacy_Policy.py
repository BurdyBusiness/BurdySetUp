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
    page_title="Burdy · Privacy Policy",
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

/* ── Privacy Policy content — constrained to a comfortable reading
      width within the page, same way About Us's own text blocks stay
      narrower than the full wide layout ── */
.tc-wrap {
    max-width: 820px;
    margin: 0 auto;
}
.tc-section-title {
    font-family: 'DM Sans', sans-serif;
    font-weight: 700;
    font-size: 18px;
    letter-spacing: -.01em;
    color: var(--orange);
    margin-top: 34px;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
}
.tc-body, .tc-body li {
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
    line-height: 1.75;
    color: var(--text-dim);
}
.tc-body p { margin-bottom: 12px; }
.tc-body ul { margin-top: 4px; margin-bottom: 12px; padding-left: 22px; }
.tc-body strong { color: var(--text); font-weight: 700; }
.tc-contact-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    margin-top: 10px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,.05);
}
.tc-contact-box::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, var(--orange), var(--green), transparent);
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
    .tc-section-title { font-size: 16px !important; }
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
# HERO — page intro (wording preserved from original page)
# =====================================================

st.markdown("""
<div class="about-hero">
  <div class="about-pill">◆ &nbsp;Legal</div>
  <div class="about-headline">Privacy Policy</div>
  <div class="about-body">Burdy Ltd</div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# PRIVACY POLICY CONTENT (wording preserved from original page)
# =====================================================

SECTIONS = [
    ("Introduction", """
<p>The purpose of this privacy policy is to outline how Burdy collects and stores user
data.</p>
"""),
    ("Data Collection", """
<p>Names, email addresses and postcodes are the forms of identifiable information stored by
Burdy. This data is collected in order to manage individual accounts and maintain contact with
users.</p>
"""),
    ("Data Sharing", """
<p>User data is stored on an external database, however will not be shared with third
parties.</p>
"""),
    ("User Rights", """
<p>Users have the right to request all the data held by Burdy, via the above contact details,
along with requesting the correction or deletion of said data.</p>
"""),
    ("Data Security", """
<p>All personal user data is kept on a protected, log in only database, Supabase. This ensures
no unauthorised access will be granted.</p>
"""),
    ("Changes to the Privacy Policy", """
<p>Any changes to the Privacy Policy will be published within the terms and conditions and
separately on the Burdy website, therefore should be reviewed periodically.</p>
"""),
]

st.markdown('<div class="tc-wrap">', unsafe_allow_html=True)

for title, body in SECTIONS:
    st.markdown(f'<div class="tc-section-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="tc-body">{body}</div>', unsafe_allow_html=True)

# ── Contact Details ──
st.markdown('<div class="tc-section-title">Contact Details</div>', unsafe_allow_html=True)
st.markdown("""
<div class="tc-contact-box tc-body">
<ul>
<li><strong>Company name</strong> — Burdy Ltd</li>
<li><strong>Contact email</strong> — burdybusiness@outlook.com</li>
<li><strong>Contact telephone number</strong> — 07348 657 940</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close .tc-wrap

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
