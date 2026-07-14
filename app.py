import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Convert Gregorian date to Shamsi (Simplified Persian Calendar converter for default selection)
def get_current_shamsi():
    today = datetime.now()
    gy = today.year
    gm = today.month
    gd = today.day

    g_days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if (gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0):
        g_days_in_month[1] = 29

    g_day_no = sum(g_days_in_month[:gm - 1]) + gd

    if g_day_no > 79:
        sh_day_no = g_day_no - 79
        sh_year = gy - 621
        if sh_day_no <= 186:
            sh_month = (sh_day_no - 1) // 31 + 1
            sh_day = (sh_day_no - 1) % 31 + 1
        else:
            sh_day_no_2 = sh_day_no - 186
            sh_month = (sh_day_no_2 - 1) // 30 + 7
            sh_day = (sh_day_no_2 - 1) % 30 + 1
    else:
        sh_year = gy - 622
        is_prev_sh_leap = ((sh_year % 33) in [1, 5, 9, 13, 17, 22, 26, 30])
        prev_year_days = 366 if is_prev_sh_leap else 365
        sh_day_no = prev_year_days - (79 - g_day_no)
        if sh_day_no <= 186:
            sh_month = (sh_day_no - 1) // 31 + 1
            sh_day = (sh_day_no - 1) % 31 + 1
        else:
            sh_day_no_2 = sh_day_no - 186
            sh_month = (sh_day_no_2 - 1) // 30 + 7
            sh_day = (sh_day_no_2 - 1) % 30 + 1

    return str(sh_year), str(sh_month), str(sh_day)

sh_y_now, sh_m_now, sh_d_now = get_current_shamsi()

st.set_page_config(page_title="Enterprise Manager & Employee Portal", layout="centered")

# --- Elegant, Dark Blue Gold/Neon Gradient Theme with Fixed Input Colors ---
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(180deg, #070b12 0%, #101726 100%);
            color: #e2e8f0;
        }
        
        h1, h2, h3, h4, h5, h6, label, p {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        h1, h2, h3, h4, h5, h6, label {
            color: #f1c40f !important;
            text-shadow: 0 0 12px rgba(241, 196, 15, 0.25);
            font-weight: 600 !important;
        }
        
        div[data-baseweb="input"] {
            background-color: #0c1220 !important;
            border: 1px solid rgba(241, 196, 15, 0.4) !important;
            border-radius: 8px !important;
            transition: all 0.3s ease-in-out !important;
        }
        
        div[data-baseweb="input"]:focus-within {
            border-color: #00e5ff !important;
            box-shadow: 0 0 10px rgba(0, 229, 255, 0.35) !important;
        }
        
        input {
            background-color: #0c1220 !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }

        input:-webkit-autofill,
        input:-webkit-autofill:hover, 
        input:-webkit-autofill:focus, 
        input:-webkit-autofill:active {
            -webkit-box-shadow: 0 0 0 30px #0c1220 inset !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        
        div[data-baseweb="select"] {
            background-color: #0c1220 !important;
        }
        
        div[data-baseweb="select"] * {
            color: #ffffff !important;
        }
        
        .stButton>button {
            background: linear-gradient(135deg, #e6b800 0%, #c19600 100%) !important;
            color: #070b12 !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 12px rgba(193, 150, 0, 0.2) !important;
            transition: all 0.4s ease !important;
        }
        
        .stButton>button:hover {
            background: linear-gradient(135deg, #00d9f5 0%, #0077b3 100%) !important;
            color: #ffffff !important;
            box-shadow: 0 6px 18px rgba(0, 217, 245, 0.4) !important;
            transform: translateY(-1px);
        }
        
        hr {
            border-color: rgba(241, 196, 15, 0.15) !important;
        }
        
        .signup-text {
            color: rgba(241, 196, 15, 0.8);
            font-size: 1.1rem;
            margin-top: 8px;
        }
    </style>
""", unsafe_allow_html=True)

USERS_FILE = "users_db.json"
SALES_FILE = "sales_data.json"

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {
        "admin": ["admin", "Manager"],
        "RaminaChehrehsaz": ["123456", "Manager"]
    }

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def load_sales():
    if os.path.exists(SALES_FILE):
        try:
            with open(SALES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return []

def save_sales(sales):
    with open(SALES_FILE, "w", encoding="utf-8") as f:
        json.dump(sales, f, ensure_ascii=False, indent=4)

if "users_db" not in st.session_state:
    st.session_state.users_db = load_users()
if "sales_data" not in st.session_state:
    st.session_state.sales_data = load_sales()
if "current_page" not in st.session_state:
    st.session_state.current_page = "LandingPage"
if "current_employee" not in st.session_state:
    st.session_state.current_employee = ""
if "temp_data" not in st.session_state:
    st.session_state.temp_data = {}

def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

# ----------------- Landing Page -----------------
if st.session_state.current_page == "LandingPage":
    st.title("Enterprise Portal")
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Manager Login", use_container_width=True):
            navigate_to("ManagerLoginPanel")
    with col2:
        if st.button("Employee Login", use_container_width=True):
            navigate_to("EmployeeLoginPanel")
            
    st.write("---")
    
    col_text, col_btn = st.columns([1, 3])
    with col_text:
        st.markdown("<p class='signup-text'>New employee?</p>", unsafe_allow_html=True)
    with col_btn:
        if st.button("Sign up", use_container_width=False):
            navigate_to("SignupPanel")

# ----------------- Manager Login Panel -----------------
elif st.session_state.current_page == "ManagerLoginPanel":
    st.title("Manager Authentication")
    
    user = st.text_input("Username")
    passw = st.text_input("Password", type="password")
    
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back", use_container_width=True):
            navigate_to("LandingPage")
    with col2:
        if st.button("Login", use_container_width=True):
            if not user or not passw:
                st.error("Please enter both Username and Password.")
            else:
                user_data = st.session_state.users_db.get(user)
                if user_data and tuple(user_data[:2]) == (passw, "Manager"):
                    st.success("Login Successful!")
                    navigate_to("ManagerDashboard")
                else:
                    st.error("Invalid Manager credentials.")

# ----------------- Employee Login Panel -----------------
elif st.session_state.current_page == "EmployeeLoginPanel":
    st.title("Employee Authentication")
    
    user = st.text_input("Username")
    passw = st.text_input("Password", type="password")
    
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back", use_container_width=True):
            navigate_to("LandingPage")
    with col2:
        if st.button("Login", use_container_width=True):
            if not user or not passw:
                st.error("Please enter both Username and Password.")
            elif user in st.session_state.users_db:
                user_info = st.session_state.users_db[user]
                saved_p = user_info[0]
                role = user_info[1]
                if saved_p == passw and role == "Employee":
                    st.session_state.current_employee = user
                    st.success("Login Successful!")
                    navigate_to("EmployeeDashboard")
                else:
                    st.error("Wrong password or invalid account type.")
            else:
                st.error("Username does not exist. Please sign up first.")

# ----------------- Signup Panel -----------------
elif st.session_state.current_page == "SignupPanel":
    st.title("New Employee Registration")
    
    user = st.text_input("Choose Username")
    passw = st.text_input("Choose Password", type="password")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    
    team_options = [
        "انجمن نخبگان ایده پرداز",
        "کانون توسعه سرمایه",
        "کافه موفقیت",
        "ایده پردازان نوین",
        "فارمارک",
        "مستقل IT",
        "نسل آینده ساز گیشا"
    ]
    team_name = st.selectbox("Select Team", options=team_options)
    
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back", use_container_width=True):
            navigate_to("LandingPage")
    with col2:
        if st.button("Create Account", use_container_width=True):
            if not user or not passw or not first_name or not last_name or not email or not phone:
                st.error("Please fill out all fields.")
            elif user in st.session_state.users_db:
                st.error("Username is already taken.")
            else:
                st.session_state.users_db[user] = [
                    passw, 
                    "Employee", 
                    {"first_name": first_name, "last_name": last_name, "email": email, "phone": phone, "team": team_name}
                ]
                save_users(st.session_state.users_db)
                st.session_state.current_employee = user
                st.success("Account created successfully!")
                navigate_to("EmployeeDashboard")

# ----------------- Manager Dashboard -----------------
elif st.session_state.current_page == "ManagerDashboard":
    st.title("Manager Dashboard")
    
    col_header, col_logout = st.columns([3, 1])
    with col_logout:
        if st.button("Logout", use_container_width=True):
            navigate_to("LandingPage")
            
    employees = [u for u, data in st.session_state.users_db.items() if data[1] == "Employee"]
    
    if not employees:
        st.info("No employees registered yet.")
    else:
        with col_header:
            selected_emp = st.selectbox("Select Employee", options=["All Employees"] + employees)
            
        if selected_emp == "All Employees":
            emp_records = st.session_state.sales_data
        else:
            emp_records = [r for r in st.session_state.sales_data if r["Employee"] == selected_emp]
        
        st.subheader("Daily Performance Summary")
        if emp_records:
            df_all = pd.DataFrame(emp_records)
            summary_data = []
            for date_val, group in df_all.groupby("ShamsiDate"):
                total_presented = len(group)
                total_sold = len(group[group["Status"] == "Sold"])
                summary_data.append({
                    "Date": date_val,
                    "Total Presented": total_presented,
                    "Total Sold": total_sold
                })
            summary_df = pd.DataFrame(summary_data)
            st.dataframe(summary_df, use_container_width=True, hide_index=True)
        else:
            st.info("No data available for daily summary.")
            
        st.write("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Detailed Sales List")
            if emp_records:
                df_details = pd.DataFrame(emp_records)
                cols_to_show = ["ShamsiDate", "Employee", "Product", "PR", "Status", "Age", "Gender", "MaritalStatus", "Occupation"]
                existing_cols = [c for c in cols_to_show if c in df_details.columns]
                st.dataframe(df_details[existing_cols], use_container_width=True, hide_index=True)
            else:
                st.write("No sales records found.")
                
        with col2:
            st.subheader("Conversion Rate (CR) Trend")
            if emp_records:
                days_data = {}
                for r in emp_records:
                    try:
                        day = int(r["ShamsiDate"].split("/")[2])
                        if day not in days_data:
                            days_data[day] = []
                        days_data[day].append(r["Status"])
                    except:
                        continue
                        
                sorted_days = sorted(days_data.keys())
                cr_values = []
                
                for d in sorted_days:
                    cumulative_statuses = []
                    for cd in sorted_days:
                        if cd <= d:
                            cumulative_statuses.extend(days_data[cd])
                    sold_count = cumulative_statuses.count("Sold")
                    lead_count = cumulative_statuses.count("Lead")
                    total = sold_count + lead_count
                    cr_values.append((sold_count / total * 100) if total > 0 else 0.0)
                
                if sorted_days:
                    chart_df = pd.DataFrame({
                        "Day": [str(d) for d in sorted_days],
                        "CR %": cr_values
                    }).set_index("Day")
                    st.line_chart(chart_df)
            else:
                st.write("No trend data available.")

# ----------------- Employee Dashboard -----------------
elif st.session_state.current_page == "EmployeeDashboard":
    # Removed the decorative stars from the header
    st.markdown(f"<h1>Welcome, Dear <i>{st.session_state.current_employee}</i>!</h1>", unsafe_allow_html=True)
    
    col_logout = st.columns([3, 1])[1]
    if col_logout.button("Logout", use_container_width=True):
        st.session_state.current_employee = ""
        navigate_to("LandingPage")
        
    st.subheader("Submit Sale/Lead Details")
    
    col_y, col_m, col_d = st.columns(3)
    
    # Year Options Setup
    year_options = ["1405", "1406", "1407", "1408"]
    default_year_idx = year_options.index(sh_y_now) if sh_y_now in year_options else 0
    year = col_y.selectbox("Year", year_options, index=default_year_idx)
    
    # Month Options Setup
    month_options = [str(i) for i in range(1, 13)]
    default_month_idx = month_options.index(sh_m_now) if sh_m_now in month_options else 0
    month = col_m.selectbox("Month", month_options, index=default_month_idx)
    
    # Day Options Setup
    day_options = [str(i) for i in range(1, 32)]
    default_day_idx = day_options.index(sh_d_now) if sh_d_now in day_options else 0
    day = col_d.selectbox("Day", day_options, index=default_day_idx)
    
    product = st.selectbox("Product", ["Simazar", "Andokhte dar", "Omid", "Finora/ Zarnova"])
    is_sale_successful = st.toggle("Submit Successful Sale", value=False)
    
    invest_val = 0.0
    if is_sale_successful:
        col_inv, col_unit = st.columns([5, 1])
        invest_val = col_inv.number_input("Investment Amount", min_value=0.0, step=1000.0, format="%.2f")
        col_unit.markdown("<h4 style='margin-top: 28px;'>Rial</h4>", unsafe_allow_html=True)
        
    if st.button("Consumer Data", type="primary", use_container_width=True):
        status = "Sold" if is_sale_successful else "Lead"
        if is_sale_successful and invest_val <= 0:
            st.error("Please enter a valid investment amount.")
        else:
            shamsi_date = f"{year}/{int(month):02d}/{int(day):02d}"
            st.session_state.temp_data = {
                "ShamsiDate": shamsi_date,
                "Employee": st.session_state.current_employee,
                "Product": product,
                "Investment": invest_val,
                "Status": status
            }
            navigate_to("ConsumerData")

# ----------------- Consumer Data -----------------
elif st.session_state.current_page == "ConsumerData":
    st.title("Enter Customer Specifications")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=0, max_value=120, value=0, step=1)
        gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
        marital_status = st.radio("Marital Status", ["Single", "Married"], horizontal=True)
        
    with col2:
        num_children = st.number_input("Num of children", min_value=0, max_value=20, value=0, step=1)
        smoker = st.radio("Smoker", ["Yes", "No"], horizontal=True)
        education = st.selectbox("Education", ["Diploma", "Bachelor's degree", "Master's degree", "PhD"])
        
    occupation = st.text_input("Occupation")
    cust_notes = st.text_area("Notes")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Submit", use_container_width=True):
            temp = st.session_state.temp_data
            invest = temp["Investment"]
            prod = temp["Product"]
            
            if prod in ["Simazar", "Andokhte dar", "Omid"]:
                pr = invest
            elif prod in ["Finora/ Zarnova", "Finora", "Zarnova"]:
                pr = 0.40 * invest
            else:
                pr = 0
            
            new_row = {
                "ShamsiDate": temp["ShamsiDate"],
                "Employee": temp["Employee"],
                "Product": prod,
                "Investment": invest,
                "PR": pr,
                "Status": temp["Status"],
                "Age": age,
                "Gender": gender,
                "MaritalStatus": marital_status,
                "NumChildren": num_children,
                "Smoker": smoker,
                "Education": education,
                "Occupation": occupation,
                "CustomerNotes": cust_notes
            }
            
            st.session_state.sales_data.append(new_row)
            save_sales(st.session_state.sales_data)
            
            st.toast("Data registered successfully!")
            st.session_state.temp_data = {}
            navigate_to("EmployeeDashboard")
                
    with col_btn2:
        if st.button("Cancel", use_container_width=True):
            st.session_state.temp_data = {}
            navigate_to("EmployeeDashboard")
