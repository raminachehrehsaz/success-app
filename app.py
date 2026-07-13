import streamlit as st
import pandas as pd

st.set_page_config(page_title="Enterprise Manager & Employee Portal", layout="centered")

if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "admin": ("admin", "Manager"),
        "RaminaChehrehsaz": ("123456", "Manager")
    }
if "sales_data" not in st.session_state:
    st.session_state.sales_data = []
if "current_page" not in st.session_state:
    st.session_state.current_page = "RoleSelection"
if "current_employee" not in st.session_state:
    st.session_state.current_employee = ""
if "temp_data" not in st.session_state:
    st.session_state.temp_data = {}

def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

# ----------------- Role Selection -----------------
if st.session_state.current_page == "RoleSelection":
    st.title("Choose your role:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Manager Login", use_container_width=True):
            navigate_to("ManagerLogin")
    with col2:
        if st.button("Employee Login", use_container_width=True):
            navigate_to("EmployeeLogin")

# ----------------- Manager Login -----------------
elif st.session_state.current_page == "ManagerLogin":
    st.title("Manager Login")
    user = st.text_input("Username")
    passw = st.text_input("Password", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Return", use_container_width=True):
            navigate_to("RoleSelection")
    with col2:
        if st.button("Enter", use_container_width=True):
            if user in st.session_state.users_db and st.session_state.users_db[user] == (passw, "Manager"):
                st.success("Login Successful!")
                navigate_to("ManagerDashboard")
            else:
                st.error("Invalid Manager credentials.")

# ----------------- Employee Login -----------------
elif st.session_state.current_page == "EmployeeLogin":
    st.title("Employee Login / Signup")
    user = st.text_input("Username")
    passw = st.text_input("Password", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Return", use_container_width=True):
            navigate_to("RoleSelection")
    with col2:
        if st.button("Enter", use_container_width=True):
            if not user or not passw:
                st.error("Username and Password cannot be empty.")
            elif user in st.session_state.users_db:
                saved_p, role = st.session_state.users_db[user]
                if saved_p == passw and role == "Employee":
                    st.session_state.current_employee = user
                    st.success("Login Successful!")
                    navigate_to("EmployeeDashboard")
                else:
                    st.error("Wrong password or invalid account.")
            else:
                st.session_state.users_db[user] = (passw, "Employee")
                st.session_state.current_employee = user
                st.success("Account created and registered successfully!")
                navigate_to("EmployeeDashboard")

# ----------------- Manager Dashboard -----------------
elif st.session_state.current_page == "ManagerDashboard":
    st.title("Manager Dashboard")
    
    col_header, col_logout = st.columns([3, 1])
    with col_logout:
        if st.button("Logout", use_container_width=True):
            navigate_to("RoleSelection")
            
    employees = [u for u, (p, r) in st.session_state.users_db.items() if r == "Employee"]
    
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
                    "Total Presented (پرزنت شده)": total_presented,
                    "Total Sold (خریده شده)": total_sold
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
                        "Day": sorted_days,
                        "CR %": cr_values
                    }).set_index("Day")
                    st.line_chart(chart_df)
            else:
                st.write("No trend data available.")

# ----------------- Employee Dashboard -----------------
elif st.session_state.current_page == "EmployeeDashboard":
    st.title(f"Welcome, {st.session_state.current_employee}")
    
    col_logout = st.columns([3, 1])[1]
    if col_logout.button("Logout", use_container_width=True):
        st.session_state.current_employee = ""
        navigate_to("RoleSelection")
        
    st.subheader("Submit Sale/Lead Details")
    
    st.write("Date (Shamsi)")
    col_y, col_m, col_d = st.columns(3)
    year = col_y.selectbox("Year", ["1405", "1406", "1407", "1408"], index=0)
    month = col_m.selectbox("Month", [str(i) for i in range(1, 13)], index=0)
    day = col_d.selectbox("Day", [str(i) for i in range(1, 32)], index=0)
    
    product = st.selectbox("Product", ["Simazar", "Andokhte dar", "Omid", "Finora/ Zarnova"])
    is_sale_successful = st.toggle("Submit Successful Sale", value=False)
    
    invest_val = 0.0
    if is_sale_successful:
        col_inv, col_unit = st.columns([5, 1])
        invest_val = col_inv.number_input("Investment Amount", min_value=0.0, step=1000.0, format="%.2f")
        col_unit.markdown("<h4 style='margin-top: 28px;'>ریال</h4>", unsafe_allow_html=True)
        
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
            st.toast("Data registered successfully!")
            st.session_state.temp_data = {}
            navigate_to("EmployeeDashboard")
                
    with col_btn2:
        if st.button("Cancel", use_container_width=True):
            st.session_state.temp_data = {}
            navigate_to("EmployeeDashboard")
