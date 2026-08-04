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
    page_title="Burdy · FAQ",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="auto",
)

# =====================================================
# CUSTOM CSS — identical to the rest of the Burdy site
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
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 20px 0 !important;
}

/* ── FAQ accordion items ── */
.faq-item {
    padding: 4px 0;
}
.faq-item summary {
    list-style: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 15px;
    letter-spacing: -.01em;
    color: var(--text);
    padding: 14px 4px;
    transition: color .15s;
}
.faq-item summary::-webkit-details-marker { display: none; }
.faq-item summary::after {
    content: '+';
    flex-shrink: 0;
    font-family: 'DM Mono', monospace;
    font-size: 18px;
    font-weight: 400;
    color: var(--orange);
    transition: transform .2s;
}
.faq-item[open] summary::after { transform: rotate(45deg); }
.faq-item summary:hover { color: var(--orange); }
.faq-item p {
    font-family: 'DM Sans', sans-serif;
    font-size: 13.5px;
    line-height: 1.7;
    color: var(--text-dim);
    margin: 0 0 14px;
    padding: 0 4px;
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
# PAGE HEADING
# =====================================================

st.markdown("""
<div style="font-family:'Syne',sans-serif;font-weight:700;font-size:20px;
  letter-spacing:-.02em;color:#141518;margin:20px 0 8px;text-align:center;">
  Frequently Asked Questions
</div>
<div style="font-family:'DM Sans',sans-serif;font-size:13px;color:#6B7280;
  text-align:center;margin-bottom:24px;">
  Find answers to common questions about our data services for local events and the hospitality industry.
</div>
""", unsafe_allow_html=True)

# =====================================================
# FAQ DATA
# =====================================================

faqs = [
    {
        "question": "What type of data do you collect?",
        "answer": "We collect data on local events, venues, attendance, customer preferences, and trends in the hospitality sector."
    },
    {
        "question": "How often is your data updated?",
        "answer": "Our data is updated in real-time for most events and venues. We also perform weekly quality checks to ensure accuracy."
    },
    {
        "question": "Can I access historical event data?",
        "answer": "Yes! We provide historical datasets for analysis and reporting, covering several years depending on the region and venue."
    },
    {
        "question": "How do you ensure the accuracy of your data?",
        "answer": "We use a combination of direct event sources, venue reports, social media monitoring, and automated verification tools to ensure data reliability."
    },
    {
        "question": "What industries can benefit from your data?",
        "answer": "Our data is useful for hospitality businesses, event organizers, marketing agencies, city planners, and tourism boards."
    },
    {
        "question": "Is your data compliant with privacy laws?",
        "answer": "Absolutely. All data collection is GDPR and CCPA compliant, with anonymized customer information where applicable."
    },
    {
        "question": "How can I subscribe to your data services?",
        "answer": "You can subscribe via our website by contacting our sales team or signing up for one of our subscription plans tailored to your needs."
    },
    {
        "question": "Do you offer custom reports or analytics?",
        "answer": "Yes, we provide custom reports and analytics services to help businesses make data-driven decisions about events and hospitality operations."
    },
    {
        "question": "How exactly is the data delivered — a file, a dashboard, or something else?",
        "answer": "Data syncs directly into your own Supabase database in real time, the moment you run a search or a Fetch & Sync — there's no manual export step and no static file to keep re-downloading. Once it's synced, it's yours to query, filter, or plug into your own tools. You also get a built-in dashboard with calendar, list, and map views, plus a simple rating/impact score for each event, so your team can start exploring straight away without writing a single query."
    },
    {
        "question": "Which event sources make up your data, and are there any gaps we should know about?",
        "answer": "We aggregate live data from two major UK ticketing platforms, Ticketmaster and Skiddle. One current limitation: ticket price isn't included in either feed directly, so where pricing context matters we estimate a rough tier using the event's minimum age restriction as a proxy, rather than pulling an exact price from source."
    },
    {
        "question": "Is your coverage limited to the UK, or can we search other countries?",
        "answer": "Right now Burdy is UK-only. Search is postcode-precise — you enter a UK postcode and a radius from 1 to 100 miles, and we return every matching event we hold for that area."
    },
    {
        "question": "How far ahead does your event data go?",
        "answer": "Each sync looks 24 months forward from today, so you're always working with a rolling two-year window of upcoming events across the UK."
    },
    {
        "question": "What event categories does Burdy track?",
        "answer": "Festival, Live Music, Clubbing, Dating, Theatre, Comedy, Exhibition, Kids / Family, Bar / Pub, Gay / Lesbian, Sport, and Arts events."
    },
    {
        "question": "Can we see a history of what's been searched, or is it a black box?",
        "answer": "Every search and Fetch & Sync run is logged with the postcode, radius, and result counts, giving you a transparent audit trail of what's been queried and when — nothing happens silently in the background."
    },
]

# =====================================================
# FAQ LIST
# =====================================================

_left, _center, _right = st.columns([1, 2.4, 1])

with _center:
    faq_html = '<div class="control-card">'
    for i, faq in enumerate(faqs):
        faq_html += (
            f'<details class="faq-item">'
            f'<summary>{faq["question"]}</summary>'
            f'<p>{faq["answer"]}</p>'
            f'</details>'
        )
        if i < len(faqs) - 1:
            faq_html += '<hr>'
    faq_html += '</div>'
    st.markdown(faq_html, unsafe_allow_html=True)

    st.markdown("""
    <div class="control-card" style="text-align:center;">
      <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:15px;
        color:#141518;margin-bottom:6px;">
        Still have questions?
      </div>
      <div style="font-family:'DM Sans',sans-serif;font-size:13px;color:#6B7280;">
        Contact our support team at
        <a href="mailto:support@yourcompany.com" style="color:var(--orange);text-decoration:none;">support@yourcompany.com</a>
        or use our Contact Us page.
      </div>
    </div>
    """, unsafe_allow_html=True)

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
