import streamlit as st
import pandas as pd
from datetime import datetime, date
from streamlit_autorefresh import st_autorefresh
import pydeck as pdk
import os

# CARA ADDED 05/02/2026 --------------- SIDEBAR STYLING ----------------
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

#----PAGE#----
st.markdown(
    "<h1 style='text-align:center;font-size:50px;color:black;'>Accessibility Statement</h1>",
    unsafe_allow_html=True
)

import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Accessibility Statement - Burdy Business",
    layout="wide",
    page_icon="♿"
)

# --- Inject CSS for styling ---
st.markdown("""
<style>
/* Headers */
h1, h2, h3 {
    color: #007bff;
}

/* Section container */
.section-box {
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

/* Links */
a {
    color: #007bff;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}

/* Lists */
ul {
    margin-left: 20px;
}

/* Buttons */
div.stButton > button {
    background-color: #007bff;
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 16px;
}
div.stButton > button:hover {
    background-color: #0056b3;
}
</style>
""", unsafe_allow_html=True)

# --- Page Title ---
st.markdown("Burdy Business is committed to ensuring digital accessibility for all users, including people with disabilities.")

# --- Statement Sections ---
with st.container():
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown("""
### Our Commitment
We strive to make our website and digital services accessible to everyone, regardless of ability or technology used. We follow best practices and aim to meet the accessibility standards outlined in the **Web Content Accessibility Guidelines (WCAG) 2.1 Level AA**.

### Accessibility Features
Our website includes:
- Keyboard navigation support for all interactive elements
- Clear, readable fonts with sufficient contrast
- Alt text for all images and icons
- Semantic headings and structure for screen readers
- Forms with descriptive labels and error handling
- Responsive design for mobile and tablet users

### Ongoing Efforts
We continually evaluate and improve our website to meet accessibility standards. We perform regular audits, usability testing, and updates to ensure content is perceivable, operable, understandable, and robust for all users.

### Known Limitations
While we strive for full accessibility, some third-party content or embedded services may not fully comply with WCAG 2.1 standards. We are actively working to minimize these limitations.

### Feedback
We welcome feedback on accessibility issues. If you encounter any barriers or have suggestions, please contact us:

- Email: [burdybusiness@outlook.com](mailto:accessibility@burdybusiness.com)  
- Phone: +44 (555) 123-4567

We aim to respond to all inquiries within **2 business days**.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Accessibility Feedback Form ---
st.markdown("### Submit Accessibility Feedback")
with st.form("accessibility_form"):
    name = st.text_input("Your Name (optional)")
    email = st.text_input("Your Email (optional)")
    message = st.text_area("Message / Feedback", height=150)
    submitted = st.form_submit_button("Send Feedback")

if submitted:
    if not message:
        st.error("⚠️ Please enter your feedback before submitting.")
    else:
        # In production, this can send to an email or database
        st.success("✅ Thank you for your feedback! We will review it promptly.")


