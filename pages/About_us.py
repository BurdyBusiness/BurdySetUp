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
# ---------------- ABOUT US TITLE ----------------
st.markdown(
    "<h1 style='text-align:center;font-size:50px;color:black;'>About us</h1>",
    unsafe_allow_html=True
)

st.markdown(
"<h1 style='text-align:center;font-size:18px;font-weight:normal'>Burdy Business is a Birmingham based Corporate Planning tool, providing innovative local events data to strategic, future-minded companies.</h1>",
unsafe_allow_html=True
)



st.write(
"With over 25 years experience in all areas of the hospitality industry, our founders bring full-spectrum, comprehensive insight into the impacts of events on a dynamic hotel industry, a fast paced leisure sector and fundamental background distribution and logistics." 
)

st.markdown(
"<hr style='border: 1px solid green;'>",
unsafe_allow_html=True
)


# ---------------- MISSION STATEMENT ----------------
st.markdown(
    """
    <h2 style='text-align:center; font-size:32px; color:#4A7B1F; max-width:900px; margin:auto;'>
        "Our mission is to empower businesses with a comprehensive view of their area,
        enabling smarter decisions, effective stock and staff planning and improved
        operational performance."
    </h2>
    """,
    unsafe_allow_html=True
)

st.write("")
st.write("")

#---------------------Values---------------

st.markdown(
    "<h1 style='text-align:center;font-size:50px;color:black;'>Our Values</h1>",
    unsafe_allow_html=True
)

st.markdown("""
<div style='text-align:center; font-size:18px; font-weight:normal; color:#333; max-width:800px; margin:auto;'>
<ul style='list-style-type: disc; text-align:left; display:inline-block; padding-left:20px;'>
    <li><strong>Innovation</strong> – We embrace creativity and continuously improve our tools and services.</li>
    <li><strong>Customer-Centricity</strong> – Our solutions are designed to empower businesses and meet their needs, increasing profitability and productivity.</li>
    <li><strong>Collaboration</strong> – We value teamwork and partnerships to achieve shared success.</li>
    <li><strong>Community Engagement</strong> – We support and connect local businesses and events.</li>
    <li><strong>Agility</strong> – We adapt quickly to changing markets and client needs.</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

#----------------------Company History-------------




#---------------------Meet the team---------------


#----------------------Vision Statement------------

st.markdown(
    """
    <h2 style='text-align:center; font-size:32px; color:#EB973D; max-width:900px; margin:auto;'>
        "Our vision is to be the trusted, go-to platform for local event intelligence, transforming how businesses plan, engage, and grow within their communities."
    </h2>
    """,
    unsafe_allow_html=True
)





#------------------Achievements/Reviews-------------------

