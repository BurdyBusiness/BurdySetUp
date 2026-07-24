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
    page_title="Burdy · Contact Us",
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
div[data-testid="stTextArea"] textarea,
div[data-baseweb="select"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: var(--orange) !important;
    box-shadow: 0 0 0 3px var(--orange-glow) !important;
}
div[data-testid="stTextInput"] small,
div[data-testid="stTextInput"] [data-testid="InputInstructions"],
div[data-testid="stTextArea"] small,
div[data-testid="stTextArea"] [data-testid="InputInstructions"] {
    display: none !important;
}
div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stSelectbox"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    color: var(--text-dim) !important;
    letter-spacing: .08em !important;
    text-transform: uppercase !important;
}
.stButton > button {
    font-family: 'DM Sans', sans-serif !important;
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
div[data-testid="stDialog"] {
    background: rgba(20,21,24,0.35) !important;
    backdrop-filter: blur(6px) !important;
    -webkit-backdrop-filter: blur(6px) !important;
    z-index: 500 !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
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
    margin: 0 !important;
    top: auto !important;
    left: auto !important;
    transform: none !important;
}
div[data-testid="stDialog"] [role="dialog"]::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, var(--orange), var(--green), transparent);
    z-index: 1;
}
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 28px 0 !important;
}
/* ── Section heading — identical to About Us ── */
.section-heading {
    font-family: 'DM Sans', sans-serif;
    font-weight: 700;
    font-size: 20px;
    letter-spacing: -.02em;
    color: var(--text);
    text-align: center;
    margin: 8px 0 24px;
}
h3 {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 18px !important;
    letter-spacing: -.02em !important;
    color: var(--text) !important;
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
# SIDEBAR — identical block used across the whole site
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

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
# PAGE HEADING
# =====================================================

st.markdown("""
<div class="section-heading">
  Contact Us
</div>
""", unsafe_allow_html=True)

# =====================================================
# CONTACT FORM
# =====================================================

# Clear form fields on the run after a successful submission (must happen
# before the widgets below are instantiated with these keys)
if st.session_state.get("clear_form"):
    st.session_state.contact_name = ""
    st.session_state.contact_email = ""
    st.session_state.contact_subject = "-- Select a reason --"
    st.session_state.contact_message = ""
    st.session_state.clear_form = False

_left, _center, _right = st.columns([1, 1.3, 1])

with _center:
    with st.form("contact_form"):
        st.markdown("""
        <div style="font-family:'DM Sans',sans-serif;font-size:13px;color:#6B7280;
          text-align:center;margin-bottom:20px;">
          We'd love to hear from you! Fill out the form below and we'll get back to you as soon as possible.
        </div>
        """, unsafe_allow_html=True)

        name = st.text_input("Full Name", max_chars=100, key="contact_name")
        email = st.text_input("Email Address *", key="contact_email")

        subject_options = [
            "Product Inquiry",
            "Order Issue",
            "Billing Question",
            "Technical Support",
            "Feedback / Suggestion",
            "Partnership / Collaboration",
            "Other",
        ]
        subject = st.selectbox(
            "Subject", ["-- Select a reason --"] + subject_options, key="contact_subject"
        )

        message = st.text_area("Message", height=150, key="contact_message")

        submitted = st.form_submit_button("Send Message")

# =====================================================
# SUCCESS POPUP
# =====================================================

@st.dialog(" ")
def _success_dialog():
    st.markdown("""
    <div style="text-align:center; padding: 8px 4px 4px;">
      <div style="font-size:36px; margin-bottom:10px;">✅</div>
      <div style="font-family:'DM Sans',sans-serif; font-weight:700; font-size:18px;
        color:#141518; margin-bottom:8px;">
        Message sent!
      </div>
      <div style="font-family:'DM Sans',sans-serif; font-size:13px; color:#6B7280;">
        Thanks for reaching out — we'll get back to you as soon as possible.
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Close", use_container_width=True, key="success_dialog_close"):
        st.session_state.show_success_dialog = False
        st.rerun()

if st.session_state.get("show_success_dialog"):
    _success_dialog()

# =====================================================
# VALIDATION WARNING POPUP
# =====================================================

@st.dialog(" ")
def _warning_dialog(message):
    st.markdown(f"""
    <div style="text-align:center; padding: 8px 4px 4px;">
      <div style="font-size:36px; margin-bottom:10px;">⚠️</div>
      <div style="font-family:'DM Sans',sans-serif; font-weight:700; font-size:18px;
        color:#141518; margin-bottom:8px;">
        Please check the form
      </div>
      <div style="font-family:'DM Sans',sans-serif; font-size:13px; color:#6B7280;">
        {message}
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Close", use_container_width=True, key="warning_dialog_close"):
        st.rerun()

if submitted:
    if not name or not email or subject == "-- Select a reason --" or not message:
        _warning_dialog("Please fill in all fields and select a subject.")
    elif "@" not in email:
        _warning_dialog("Please enter a valid email address.")
    else:
        try:
            # API key comes from Streamlit secrets — never hard-code credentials
            # in source code. Add this to secrets.toml:
            #   RESEND_API_KEY = "re_xxxxxxxxxxxxxxxxxxxxxxxx"
            resend_api_key = st.secrets["RESEND_API_KEY"]
            receiver_email = "burdybusiness@outlook.com"

            body_text = f"""
Name: {name}
Email: {email}
Subject: {subject}

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
                    "from": "Burdy Business Contact Form <onboarding@resend.dev>",
                    "to": [receiver_email],
                    "reply_to": email,
                    "subject": f"[Contact Form] {subject}",
                    "text": body_text,
                },
                timeout=15,
            )

            if response.status_code in (200, 201):
                # Defer clearing to the top of the next run (can't mutate
                # widget state after the widgets have already been created
                # in this run)
                st.session_state.clear_form = True
                st.session_state.show_success_dialog = True
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
