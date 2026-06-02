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
#-------PAGE-----

st.title("Careers")
st.write("You want to work for us? Good luck!")

import streamlit as st

# --- Page configuration ---
st.set_page_config(
    page_title="Careers - Burdy Business",
    layout="wide",
    page_icon="💼"
)

# --- Inject custom CSS for styling ---
st.markdown("""
<style>
/* Headers */
h1, h2 {
    color: #007bff;
}

/* Job container */
.job-box {
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

/* Apply button styling */
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
st.title("💼 Careers at Burdy Business")
st.markdown("Join our team! We're looking for talented individuals to help us collect and analyze data for the local events and hospitality industry.")

# --- Job Vacancy ---
with st.container():
    st.markdown("## Current Vacancy: Data Architect / Engineer")
    st.markdown('<div class="job-box">', unsafe_allow_html=True)
    
    st.markdown("""
**Location:** Remote / Flexible  
**Job Type:** Full-time  

**Role Overview:**  
We are seeking an experienced **Data Architect / Engineer** to design and maintain robust data systems that support our analytics platform. You will work closely with the analytics and product teams to ensure high-quality data pipelines for local events and hospitality data.  

**Key Responsibilities:**  
- Design, implement, and maintain scalable data pipelines and architectures  
- Optimize data storage, retrieval, and ETL processes  
- Collaborate with analytics and product teams to meet data needs  
- Ensure data quality, integrity, and security  

**Required Skills & Qualifications:**  
- Strong experience in SQL, Python, and data modeling  
- Familiarity with cloud data platforms (AWS, Azure, or GCP)  
- Experience with ETL tools and pipelines  
- Knowledge of data warehousing concepts  
- Strong problem-solving and communication skills  

**Nice-to-Have:**  
- Experience in real-time event data processing  
- Knowledge of the hospitality or local events industry  
""")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Application Form ---
st.markdown("## Apply for this role")
with st.form("application_form"):
    applicant_name = st.text_input("Full Name")
    applicant_email = st.text_input("Email Address")
    applicant_linkedin = st.text_input("LinkedIn Profile URL (optional)")
    applicant_resume = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
    applicant_message = st.text_area("Cover Letter / Message", height=150)
    submitted = st.form_submit_button("Submit Application")

if submitted:
    if not applicant_name or not applicant_email or not applicant_resume:
        st.error("⚠️ Please provide your name, email, and upload your resume.")
    else:
        # For demonstration, we'll just display a success message.
        # In production, you could send this info via email or store in a database.
        st.success(f"✅ Thank you {applicant_name}! Your application has been submitted. Our recruitment team will contact you shortly.")



