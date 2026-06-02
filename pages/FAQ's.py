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
    "<h1 style='text-align:center;font-size:50px;color:black;'>Frequently Asked Questions</h1>",
    unsafe_allow_html=True
)

import streamlit as st

# --- Page configuration ---
st.set_page_config(
    page_title="FAQ - Local Events & Hospitality Data",
    layout="wide",
    page_icon="❓"
)

# --- Inject CSS for styling ---
st.markdown("""
<style>
/* Headers */
h1, h2 {
    color: #007bff;
}

/* FAQ container */
.faq-box {
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

/* Expandable questions */
details summary {
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    margin-bottom: 8px;
}

/* Question hover */
details summary:hover {
    color: #0056b3;
}

/* Answer */
details p {
    font-size: 16px;
    margin-left: 15px;
    margin-top: 5px;
}
</style>
""", unsafe_allow_html=True)

# --- Page Title ---
st.markdown("Find answers to common questions about our data services for local events and the hospitality industry.")

# --- FAQ Data ---
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
]

# --- Display FAQs ---
for faq in faqs:
    st.markdown(f'<div class="faq-box"><details><summary>{faq["question"]}</summary><p>{faq["answer"]}</p></details></div>', unsafe_allow_html=True)

# --- Contact prompt ---
st.markdown("""
---
💡 **Still have questions?**  
Contact our support team at [support@yourcompany.com](mailto:support@yourcompany.com) or use our [Contact Us](#) page.
""")


