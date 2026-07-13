import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Patients Display", layout="wide")

# 2. Styling (Dark & Gold Theme)
st.markdown("""
    <style>
    .stApp { background-color: #020308; color: #ffffff; }
    h1, h2, h3, label { color: #f2bf26 !important; font-weight: bold; }
    .stButton>button { 
        background-color: #00ccd5 !important; color: #020308 !important; 
        font-weight: bold !important; border-radius: 8px !important; width: 100%;
        border: none !important; padding: 0.6rem !important;
    }
    div[data-baseweb="select"], div[data-baseweb="input"], textarea { 
        background-color: #05080f !important; border: 1px solid #f2bf26 !important; color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Patients Display System")

# 3. Initialize Database
if "database" not in st.session_state:
    st.session_state.database = pd.DataFrame(columns=[
        "Timestamp", "Employee", "JoinDate", "Product", 
        "Investment", "Gender", "MaritalStatus", "Children", "Education", "Smoker"
    ])

# 4. Layout Columns
left_panel, right_panel = st.columns([1, 1.5])

# --- LEFT PANEL ---
with left_panel:
    st.markdown("### 🛠️ Controls & Registration")
    main_group = st.tabs(["Main", "Consumer"])
    
    with main_group[0]:
        employee_name = st.text_input("Employee Name", value="")
        join_us_date = st.number_input("Join Us Date (Year)", value=1400, step=1)
        submit_button = st.button("Submit Profile Log")
        
    with main_group[1]:
        product = st.selectbox("Product", ['Finora/ Zarnova', 'Simazer', 'Andokhte dar', 'Omid Bazneshastegi'])
        investment = st.number_input("Investment Amount", value=0, step=1000)
    
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("*Gender*")
        male = st.checkbox("Male", value=True)
        female = st.checkbox("Female", value=False)
        
        st.markdown("*Marital Status*")
        single = st.checkbox("Single", value=True)
        married = st.checkbox("Married", value=False)
        
    with col2:
        st.markdown("*Smoker*")
        smoker_yes = st.checkbox("Yes", value=True)
        smoker_no = st.checkbox("No", value=True)
        
        num_of_children = st.number_input("Num of children", min_value=0, max_value=10, value=0, step=1)
    
    education = st.radio("Education Level", ['Diploma', "Bachelor's degree", "Master's degree"], index=0)

# --- RIGHT PANEL ---
with right_panel:
    st.markdown("### 📊 Display Panel")
    right_tabs = st.tabs(["Data Log Table", "Text Diagnostics"])
    
    with right_tabs[0]:
        st.subheader("Registered Patients / Consumers Data")
        if not st.session_state.database.empty:
            df = st.session_state.database.copy()
            if not male: df = df[df["Gender"] != "Male"]
            if not female: df = df[df["Gender"] != "Female"]
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No data recorded in the system yet.")
            
    with right_tabs[1]:
        st.text_area("Text Area Diagnostics Log", value="System initialized successfully...\nReady for operation.", height=300)

# 5. Save Data Logic
if submit_button and employee_name:
    gender_str = "Male" if male else "Female"
    marital_str = "Single" if single else "Married"
    smoker_str = "Yes" if smoker_yes else "No"
    
    new_row = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Employee": employee_name, "JoinDate": join_us_date, "Product": product,
        "Investment": investment, "Gender": gender_str, "MaritalStatus": marital_str,
        "Children": num_of_children, "Education": education, "Smoker": smoker_str
    }
    st.session_state.database = pd.concat([st.session_state.database, pd.DataFrame([new_row])], ignore_index=True)
    st.success(f"Log for {employee_name} saved successfully!")
    st.rerun()
