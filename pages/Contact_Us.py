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

import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- Page configuration ---
st.set_page_config(page_title="Contact Us - Burdy Business", layout="wide")
st.title("Contact Us")
st.write("We'd love to hear from you! Fill out the form below and we'll get back to you as soon as possible.")

# --- Form fields ---
with st.form("contact_form"):
    name = st.text_input("Full Name", max_chars=100)
    email = st.text_input("Email Address")
    
    subject_options = [
        "Product Inquiry",
        "Order Issue",
        "Billing Question",
        "Technical Support",
        "Feedback / Suggestion",
        "Partnership / Collaboration",
        "Other"
    ]
    subject = st.selectbox("Subject", ["-- Select a reason --"] + subject_options)
    
    message = st.text_area("Message", height=150)
    
    submitted = st.form_submit_button("Send Message")

# --- Email sending ---
if submitted:
    if not name or not email or subject == "-- Select a reason --" or not message:
        st.error("Please fill in all fields and select a subject.")
    else:
        try:
            # --- Email settings for Outlook ---
            sender_email = "burdybusiness@outlook.com"   # <-- Replace with your Outlook email
            sender_password = "#TowanBlystra37!"         # <-- Replace with your Outlook password or app password
            receiver_email = "burdybusiness@outlook.com"
            
            # --- Compose the email ---
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = f"[Contact Form] {subject}"
            
            body = f"""
Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
"""
            msg.attach(MIMEText(body, 'plain'))
            
            # --- Send email via Outlook SMTP ---
            with smtplib.SMTP("smtp.office365.com", 587) as server:
                server.starttls()  # Secure the connection
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
            
            st.success("✅ Your message has been sent successfully!")
            
            # --- Reset form fields ---
            st.experimental_rerun()
        
        except Exception as e:
            st.error(f"❌ Error sending email: {e}")


