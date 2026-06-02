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
    "<h1 style='text-align:center;font-size:50px;color:black;'>Investor Page</h1>",
    unsafe_allow_html=True
)

import streamlit as st

# --- Page configuration ---
st.set_page_config(
    page_title="Investors - Burdy Business",
    layout="wide",
)

# --- Inject custom CSS for styling ---
st.markdown("""
<style>
/* Headers */
h1, h2, h3 {
    color: #007bff;
}

/* Section containers */
.section {
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 12px;
    margin-bottom: 20px;
}

/* Highlight boxes */
.highlight-box {
    background-color: #ffffff;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    margin-bottom: 10px;
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

# --- Header ---
st.markdown("Welcome to the Burdy Business Investors Portal. Here you'll find company updates, financial highlights, and key information for our investors.")

# --- Company Overview ---
with st.container():
    st.markdown("## Company Overview")
    st.markdown("""
    Burdy Business is a rapidly growing company in [your industry].  
    Our mission is to deliver innovative solutions while creating value for our investors.  
    We are committed to transparency, sustainability, and long-term growth.
    """)

# --- Financial Highlights ---
with st.container():
    st.markdown("## Financial Highlights")
    st.markdown("""
    <div class="highlight-box">
        <strong>Revenue Growth:</strong> +25% YoY
    </div>
    <div class="highlight-box">
        <strong>Net Profit Margin:</strong> 18%
    </div>
    <div class="highlight-box">
        <strong>Cash Reserves:</strong> $12M
    </div>
    <div class="highlight-box">
        <strong>Active Markets:</strong> 5 Countries
    </div>
    """, unsafe_allow_html=True)

# --- Latest News / Announcements ---
with st.container():
    st.markdown("## Latest News")
    st.markdown("""
    <div class="highlight-box">
        <strong>Jan 2026:</strong> Launched our new AI-powered platform for small businesses.
    </div>
    <div class="highlight-box">
        <strong>Dec 2025:</strong> Secured $5M Series A funding from strategic partners.
    </div>
    <div class="highlight-box">
        <strong>Nov 2025:</strong> Expanded operations to Germany and France.
    </div>
    """, unsafe_allow_html=True)

# --- Investor Contact Form ---
with st.container():
    st.markdown("## Contact Investor Relations")
    st.markdown("If you are an investor or potential investor and would like to reach out, please fill out the form below.")
    
    with st.form("investor_form"):
        investor_name = st.text_input("Full Name")
        investor_email = st.text_input("Email Address")
        inquiry_type = st.selectbox(
            "Inquiry Type",
            ["-- Select --", "Investment Opportunity", "Financial Reports", "Partnership", "Other"]
        )
        inquiry_message = st.text_area("Message", height=150)
        submitted = st.form_submit_button("Submit Inquiry")
    
    if submitted:
        if not investor_name or not investor_email or inquiry_type == "-- Select --" or not inquiry_message:
            st.error("⚠️ Please fill all fields before submitting.")
        else:
            st.success("✅ Thank you! Your inquiry has been submitted. Our Investor Relations team will contact you shortly.")
