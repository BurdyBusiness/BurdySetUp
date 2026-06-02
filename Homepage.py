import streamlit as st
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Burdy Business", layout="wide")

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "HomePage"

# ---------------- CSS: Lucida font + sticky header ----------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Lucida Sans", "Lucida Grande", "Lucida Sans Unicode", sans-serif;
}
.sticky-header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    background-color: orange;
    padding: 10px 30px;
    border-bottom: 1px solid #eee;
}
.main > div:first-child {
    margin-top: 80px;
}
.sticky-header h1 {
    margin: 0;
    padding-top: 10px;
    font-size: 1.8em;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="sticky-header">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 8, 2])
with col1:
    st.image(r"C:\Users\user\OneDrive\Documents\Business\Colour Logo.png", width=100)
with col2:
    st.markdown("<h1>Burdy Business</h1>", unsafe_allow_html=True)
with col3:
    clock_placeholder = st.empty()
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

# Sidebar logo (replacing "Dashboard" title)
st.sidebar.image(
    r"C:\Users\user\OneDrive\Documents\Business\Colour Logo.png",
    width=120
)
# ---------------- CENTERED SIDEBAR TITLE ----------------
st.sidebar.markdown(
    """
    <h2 style='text-align: center; color: #333333; margin-bottom: 0px;'>
        Burdy Business
    </h2>
    """,
    unsafe_allow_html=True)
# Optional spacing after logo
st.sidebar.markdown("<br>", unsafe_allow_html=True)


# ---------------- SIDEBAR STYLING ----------------
st.markdown(
    """
    <style>
    /* Sidebar background color with colored edge */
    [data-testid="stSidebar"] {
        background-color: #f7f0e6;   /* sidebar background */
        border-right: 5px solid #ff7f50; /* colored edge / border */
        padding-top: 0px;  /* optional spacing at top */
    }

    /* Full-width buttons with custom style */
    div[data-testid="stSidebar"] button[kind="primary"] {
        width: 100%;
        padding: 10px 0;
        margin-bottom: 5px;
        text-align: left;
        background-color: #f0f2f6;  /* button background */
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 16px;
        cursor: pointer;
    }

    div[data-testid="stSidebar"] button[kind="primary"]:hover {
        background-color: #e0e3ea;  /* hover effect */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- LIVE CLOCK ----------------
current_time = datetime.now().strftime("%I:%M %p")
current_date = datetime.now().strftime("%d %b %Y")
with clock_placeholder:
    st.markdown(f"""
    <div style="text-align: right;">
        <strong style="font-size: 1.2em;">{current_time}</strong><br>
        <span style="font-size: 0.9em;">{current_date}</span>
    </div>
    """, unsafe_allow_html=True)
    
#---------FOOTER---------------
st.markdown(
    "<hr style='border: 1px solid green;'>",
    unsafe_allow_html=True
)
footer_links = {
    "Terms & Conditions": "https://example.com/terms",
    "About Us": "https://example.com/about",
    "Contact Us": "burdybusiness@outlook.com",
    "Sitemap": "https://example.com/sitemap",
    "Careers": "https://example.com/sitemap",
    "FAQ's": "https://example.com/sitemap",
    "Privacy Policy": "https://example.com/sitemap",
    "Terms of Use": "https://example.com/sitemap",
    "Copyright Notice": "https://example.com/sitemap",
    "Investors": "https://example.com/sitemap",
    "Accessibility Statement": "https://example.com/sitemap",
    "Cookies": "https://example.com/cookies"
}

# Define 3 rows of keys
row_1 = ["Terms & Conditions", "About Us", "Contact Us", "Sitemap"]
row_2 = ["Careers", "FAQ's", "Privacy Policy", "Terms of Use"]
row_3 = ["Copyright Notice", "Investors", "Accessibility Statement", "Cookies"]

# Function to build a clickable row
def build_row(keys):
    return " | ".join(
        f'<a href="{footer_links[k]}" target="_blank">{k}</a>'
        for k in keys
    )

# Combine rows with <br> for 3 lines
footer_html = (
    build_row(row_1) + "<br>" +
    build_row(row_2) + "<br>" +
    build_row(row_3)
)

# Display in Streamlit
st.markdown(
    f"<div style='text-align:center; font-size:0.85em; color:gray;'>{footer_html}</div>",
    unsafe_allow_html=True
)

