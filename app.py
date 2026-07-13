import streamlit as st
import pandas as pd
from datetime import datetime

# Custom Theme Styling (Dark, Gold, Cyan)
st.markdown("""
    <style>
    .stApp { background-color: #020308; color: #ffffff; }
    h1, h2, h3 { color: #f2bf26 !important; }
    .stButton>button { 
        background-color: #00ccd5 !important; color: #020308 !important; 
        font-weight: bold !important; border-radius: 8px !important; width: 100%;
    }
    div[data-baseweb="select"] { background-color: #05080f !important; }
    div[data-baseweb="input"] { background-color: #05080f !important; }
    .css-1r6slb0 { background-color: #03050a !important; border: 1px solid #f2bf26; }
    </style>
""", unsafe_allow_html=True)

st.title("Performance Management System")

# Navigation using tabs for Mobile
tab1, tab2, tab3 = st.tabs(["Main Page", "Consumer Page", "AI Optimizer"])

if "database" not in st.session_state:
    st.session_state.database = pd.DataFrame()

with tab1:
    st.subheader("Data Entry")
    employee = st.selectbox("Employee Name:", ["Employee 1", "Employee 2", "Employee 3"])
    product = st.selectbox("Product:", ["Finora / Zarnova", "Simazer Endowed Life", "Omid Endowed Life", "Omid Retirement"])
    
    st.write("---")
    st.subheader("Registered Data Log")
    if not st.session_state.database.empty:
        st.dataframe(st.session_state.database)
    else:
        st.info("No data recorded yet.")

with tab2:
    st.subheader("Consumer Profile")
    with st.container():
        c_name = st.text_input("Consumer Name:")
        birth_year = st.number_input("Birth Year (Solar):", value=1370, step=1)
        gender = st.selectbox("Gender:", ["Male", "Female", "Prefer not to say"])
        marital = st.selectbox("Marital Status:", ["Single", "Married", "Divorced", "Widowed"])
        children = st.number_input("Children Count:", value=0, step=1)
        job_status = st.selectbox("Employment:", ["Employed", "Unemployed", "Student", "Retired"])
        job_title = st.text_input("Exact Job Title:")
        notes = st.text_area("Notes:")
        
        purchased = st.checkbox("Successful Presentation (Registered Document)")
        investment = st.number_input("Investment Amount:", value=0.0)
        
        # Portfolio calculation logic
        portfolio = investment * 0.40 if product == "Finora / Zarnova" else investment
        st.markdown(f"*Premium (Portfolio): <span style='color:#f2bf26'>{portfolio:,.0f} Tomans</span>*", unsafe_allow_html=True)
        
        if st.button("Save Presentation Details"):
            new_row = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Employee": employee, "Product": product, "ConsumerName": c_name,
                "BirthYear": birth_year, "Gender": gender, "Marital": marital,
                "Children": children, "JobStatus": job_status, "JobTitle": job_title,
                "Notes": notes, "Purchased": purchased, "Investment": investment
            }
            st.session_state.database = pd.concat([st.session_state.database, pd.DataFrame([new_row])], ignore_index=True)
            st.success("Presentation data successfully saved!")

with tab3:
    st.subheader("Deep Learning Optimizer")
    opt_emp = st.selectbox("Select Employee for Diagnostics:", ["Employee 1", "Employee 2", "Employee 3"])
    if st.button("Run AI Sales Optimization Engine"):
        st.markdown("### <span style='color:#f2bf26'>--- AI Performance Optimization Report ---</span>", unsafe_allow_html=True)
        st.info("AI-Prescribed Action Plan for Sales Improvement will appear here based on database analysis.")