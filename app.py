import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# --- FUNCTIONS & HELPERS ---
def get_current_shamsi():
    today = datetime.now()
    gy, gm, gd = today.year, today.month, today.day
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
        sh_day_no = (366 if is_prev_sh_leap else 365) - (79 - g_day_no)
        if sh_day_no <= 186:
            sh_month = (sh_day_no - 1) // 31 + 1
            sh_day = (sh_day_no - 1) % 31 + 1
        else:
            sh_day_no_2 = sh_day_no - 186
            sh_month = (sh_day_no_2 - 1) // 30 + 7
            sh_day = (sh_day_no_2 - 1) % 30 + 1
    return str(sh_year), f"{sh_month:02d}", f"{sh_day:02d}"

sh_y_now, sh_m_now, sh_d_now = get_current_shamsi()

st.set_page_config(page_title="Enterprise Portal", layout="wide")

# --- CUSTOM CSS FOR THEME, ALIGNMENT & MENU ---
st.markdown("""
    <style>
        .stApp { background: linear-gradient(180deg, #070b12 0%, #101726 100%); color: #e2e8f0; }
        h1, h2, h3, h4, h5, h6, label, p { font-family: 'Segoe UI', Tahoma, sans-serif; }
        h1, h2, h3, h4, h5, h6, label { color: #f1c40f !important; font-weight: 600 !important; }
        div[data-baseweb="input"], div[data-baseweb="select"] { background-color: #0c1220 !important; border: 1px solid rgba(241, 196, 15, 0.4) !important; border-radius: 8px !important; }
        input { background-color: #0c1220 !important; color: #ffffff !important; }
        .stButton>button { background: linear-gradient(135deg, #e6b800 0%, #c19600 100%) !important; color: #070b12 !important; font-weight: 600 !important; border-radius: 8px !important; }
        .stButton>button:hover { background: linear-gradient(135deg, #00d9f5 0%, #0077b3 100%) !important; color: #ffffff !important; }
        [data-testid="stSidebar"] { background-color: #090e18 !important; border-left: 1px solid rgba(241, 196, 15, 0.2); }
        .followup-box { background-color: #1a2436; border-left: 3px solid #f1c40f; padding: 6px 12px; margin: 4px 0; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

USERS_FILE = "users_db.json"
SALES_FILE = "sales_data.json"
TEAMS_LIST = ["انجمن نخبگان ایده پرداز", "کانون توسعه سرمایه", "کافه موفقیت", "ایده پردازان نوین", "فارمارک", "مستقل IT", "نسل آینده ساز گیشا"]

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return {"admin": ["admin", "Manager", {"team": "Global"}], "RaminaChehrehsaz": ["123456", "Manager", {"team": "Global"}]}

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f: json.dump(users, f, ensure_ascii=False, indent=4)

def load_sales():
    if os.path.exists(SALES_FILE):
        with open(SALES_FILE, "r", encoding="utf-8") as f: 
            data = json.load(f)
            for item in data:
                if "follow_ups" not in item:
                    item["follow_ups"] = []
            return data
    return []

def save_sales(sales):
    with open(SALES_FILE, "w", encoding="utf-8") as f: json.dump(sales, f, ensure_ascii=False, indent=4)

if "users_db" not in st.session_state: st.session_state.users_db = load_users()
if "sales_data" not in st.session_state: st.session_state.sales_data = load_sales()
if "current_page" not in st.session_state: st.session_state.current_page = "LandingPage"
if "current_user" not in st.session_state: st.session_state.current_user = ""
if "temp_data" not in st.session_state: st.session_state.temp_data = {}

if "manager_step" not in st.session_state: st.session_state.manager_step = "SelectTeam"
if "selected_team" not in st.session_state: st.session_state.selected_team = ""
if "selected_member" not in st.session_state: st.session_state.selected_member = ""

def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

def calculate_cr(sold, total):
    return f"{(sold / total * 100):.1f}%" if total > 0 else "0.0%"

# --- LANDING PAGE ---
if st.session_state.current_page == "LandingPage":
    st.title("Enterprise Portal")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Manager Login", use_container_width=True): navigate_to("ManagerLoginPanel")
    with col2:
        if st.button("Employee Login", use_container_width=True): navigate_to("EmployeeLoginPanel")
    if st.button("Sign up as Employee", use_container_width=True): navigate_to("SignupPanel")

# --- SIGNUP PANEL ---
elif st.session_state.current_page == "SignupPanel":
    st.title("New Employee Registration")
    u = st.text_input("Choose Username")
    p = st.text_input("Choose Password", type="password")
    fn = st.text_input("First Name")
    ln = st.text_input("Last Name")
    em = st.text_input("Email Address")
    ph = st.text_input("Phone Number")
    team = st.selectbox("Select Team", TEAMS_LIST)
    if st.button("Register"):
        if u and p and fn and ln:
            st.session_state.users_db[u] = [p, "Employee", {"first_name": fn, "last_name": ln, "email": em, "phone": ph, "team": team}]
            save_users(st.session_state.users_db)
            st.success("Registered successfully!")
            navigate_to("LandingPage")
        else:
            st.error("Please fill all required fields.")

# --- LOGIN PANELS ---
elif st.session_state.current_page in ["ManagerLoginPanel", "EmployeeLoginPanel"]:
    role_target = "Manager" if st.session_state.current_page == "ManagerLoginPanel" else "Employee"
    st.title(f"{role_target} Authentication")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        user_data = st.session_state.users_db.get(u)
        if user_data and user_data[0] == p and user_data[1] == role_target:
            st.session_state.current_user = u
            if role_target == "Manager":
                st.session_state.manager_step = "SelectTeam"
                navigate_to("ManagerDashboard")
            else:
                navigate_to("EmployeeDashboard")
        else:
            st.error("Invalid Credentials.")
    if st.button("Back"): navigate_to("LandingPage")

# --- MANAGER DASHBOARD & NAVIGATION ---
elif st.session_state.current_page in ["ManagerDashboard", "ManagerLiveReport", "ManagerLedger", "ManagerArchive", "ManagerTrend", "ManagerSettings"]:
    
    # --- MANAGER SIDEBAR MENU ---
    with st.sidebar:
        st.markdown(f"### ⚙️ منوی مدیریت")
        st.markdown(f"**کاربر:** `{st.session_state.current_user}`")
        if st.session_state.selected_team:
            st.markdown(f"**تیم منتخب:** `{st.session_state.selected_team}`")
            st.markdown(f"**عضو منتخب:** `{st.session_state.selected_member}`")
        st.write("---")
        
        if st.button("👥 انتخاب تیم و عضو", use_container_width=True): navigate_to("ManagerDashboard")
        if st.button("📊 نرخ تبدیل محصولات و کلی", use_container_width=True): navigate_to("ManagerLiveReport")
        if st.button("📋 جدول ارائه‌ها و فروش", use_container_width=True): navigate_to("ManagerLedger")
        if st.button("📅 آرشیو عملکرد ماه‌های قبل", use_container_width=True): navigate_to("ManagerArchive")
        if st.button("📈 نمودار روند تبدیل (CR)", use_container_width=True): navigate_to("ManagerTrend")
        if st.button("🛡️ تنظیمات امنیتی حساب", use_container_width=True): navigate_to("ManagerSettings")
        st.write("---")
        if st.button("🚪 خروج از حساب", use_container_width=True): 
            st.session_state.selected_team = ""
            st.session_state.selected_member = ""
            navigate_to("LandingPage")

    # Shared Filtered Data Logic for Manager
    df_all = pd.DataFrame(st.session_state.sales_data) if st.session_state.sales_data else pd.DataFrame()
    team = st.session_state.selected_team
    member = st.session_state.selected_member
    
    team_members_list = []
    for u, d in st.session_state.users_db.items():
        if len(d) > 2 and isinstance(d[2], dict) and d[2].get("team") == team and d[1] == "Employee":
            team_members_list.append(u)

    if not df_all.empty and team:
        if member == "All Team (کل تیم)":
            filtered_df = df_all[df_all['Employee'].isin(team_members_list)].copy()
        else:
            filtered_df = df_all[df_all['Employee'] == member].copy()
    else:
        filtered_df = pd.DataFrame()

    # --- 1) MANAGER DASHBOARD: SELECT TEAM & MEMBER ---
    if st.session_state.current_page == "ManagerDashboard":
        st.title("👥 انتخاب تیم و عضو جهت بررسی")
        
        if st.session_state.manager_step == "SelectTeam":
            st.subheader("مرحله اول: انتخاب تیم")
            selected_team = st.selectbox("تیم مورد نظر را انتخاب کنید:", TEAMS_LIST)
            if st.button("بعدی ➔ انتخاب عضو", type="primary"):
                st.session_state.selected_team = selected_team
                st.session_state.manager_step = "SelectMember"
                st.rerun()

        elif st.session_state.manager_step == "SelectMember":
            st.subheader(f"مرحله دوم: انتخاب عضو از تیم: {st.session_state.selected_team}")
            
            team_members = []
            for username, data in st.session_state.users_db.items():
                if len(data) > 2 and isinstance(data[2], dict):
                    if data[2].get("team") == st.session_state.selected_team and data[1] == "Employee":
                        team_members.append(username)
                        
            member_options = ["All Team (کل تیم)"] + team_members
            selected_member = st.selectbox("عضو مورد نظر را انتخاب کنید:", member_options)
            
            col_back, col_next = st.columns(2)
            with col_back:
                if st.button("⬅ بازگشت به انتخاب تیم", use_container_width=True):
                    st.session_state.manager_step = "SelectTeam"
                    st.rerun()
            with col_next:
                if st.button("تایید و بارگذاری اطلاعات ➔", type="primary", use_container_width=True):
                    st.session_state.selected_member = selected_member
                    st.success(f"اطلاعات تیم {st.session_state.selected_team} با موفقیت بارگذاری شد. از منوی کناری بخش دلخواه خود را بررسی کنید.")
                    navigate_to("ManagerLiveReport")

    # --- 2) MANAGER LIVE REPORT (CR & METRICS) ---
    elif st.session_state.current_page == "ManagerLiveReport":
        st.title("📊 گزارش نرخ‌های تبدیل")
        if not team:
            st.warning("⚠️ لطفاً ابتدا از منوی کناری بخش 'انتخاب تیم و عضو' تیم خود را انتخاب کنید.")
        elif filtered_df.empty:
            st.info("داده‌ای برای تیم یا عضو انتخاب شده یافت نشد.")
        else:
            # 1) CR per Product
            st.markdown("### 1) CR per Product Type (نرخ تبدیل به تفکیک هر محصول)")
            products = ["Simazar", "Andokhte dar", "Omid", "Finora/ Zarnova"]
            cols_cr = st.columns(4)
            for idx, prod in enumerate(products):
                prod_df = filtered_df[filtered_df['Product'] == prod]
                p_total = len(prod_df)
                p_sold = (prod_df['Status'] == 'Sold').sum()
                cols_cr[idx].metric(f"{prod} CR", calculate_cr(p_sold, p_total), f"Sold: {p_sold} / Total: {p_total}")

            st.write("---")
            # 2) CR کلی
            st.markdown("### 2) Global Conversion Rate (نرخ تبدیل کلی)")
            total_presents = len(filtered_df)
            total_solds = (filtered_df['Status'] == 'Sold').sum()
            st.metric(label="Overall CR (کل ارائه‌ها)", value=calculate_cr(total_solds, total_presents))

    # --- 3) MANAGER PRESENTATION LEDGER ---
    elif st.session_state.current_page == "ManagerLedger":
        st.title("📋 جدول ارائه‌ها و فروش")
        if not team:
            st.warning("⚠️ لطفاً ابتدا از منوی کناری بخش 'انتخاب تیم و عضو' تیم خود را انتخاب کنید.")
        elif filtered_df.empty:
            st.info("داده‌ای برای تیم یا عضو انتخاب شده یافت نشد.")
        else:
            display_df = filtered_df.copy()
            display_df['Investment'] = display_df['Investment'].apply(lambda x: f"{int(x):,} Rial" if pd.notnull(x) else "0")
            display_df['PR'] = display_df['PR'].apply(lambda x: f"{int(x):,} Rial" if pd.notnull(x) else "0")
            
            display_df = display_df.rename(columns={
                "ShamsiDate": "تاریخ شمسی",
                "Product": "نوع محصول",
                "Investment": "مبلغ سرمایه‌گذاری",
                "PR": "پورتفوی (PR)",
                "Status": "وضعیت"
            })
            
            existing_cols = ["تاریخ شمسی", "نوع محصول", "مبلغ سرمایه‌گذاری", "پورتفوی (PR)", "وضعیت", "Employee"]
            valid_cols = [c for c in existing_cols if c in display_df.columns]
            st.dataframe(display_df[valid_cols], use_container_width=True, hide_index=True)

    # --- 4) MANAGER ARCHIVE (MONTHLY ACCUMULATIVE) ---
    elif st.session_state.current_page == "ManagerArchive":
        st.title("📅 آرشیو عملکرد و پورتفوی ماه‌های قبل")
        if not team:
            st.warning("⚠️ لطفاً ابتدا از منوی کناری بخش 'انتخاب تیم و عضو' تیم خود را انتخاب کنید.")
        elif filtered_df.empty:
            st.info("داده‌ای برای تیم یا عضو انتخاب شده یافت نشد.")
        else:
            filtered_df['Month'] = filtered_df['ShamsiDate'].apply(lambda x: x.split('/')[1] if len(x.split('/')) > 1 else '00')
            filtered_df['Year'] = filtered_df['ShamsiDate'].apply(lambda x: x.split('/')[0] if len(x.split('/')) > 1 else '00')
            
            unique_months = filtered_df.groupby(['Year', 'Month']).size().reset_index()[['Year', 'Month']]
            products = ["Simazar", "Andokhte dar", "Omid", "Finora/ Zarnova"]
            monthly_records = []
            
            for _, row in unique_months.iterrows():
                y, m = row['Year'], row['Month']
                m_df = filtered_df[(filtered_df['Year'] == y) & (filtered_df['Month'] == m)]
                
                m_total_presents = len(m_df)
                m_total_solds = (m_df['Status'] == 'Sold').sum()
                m_cr = calculate_cr(m_total_solds, m_total_presents)
                m_pr = m_df['PR'].sum()
                
                prod_cr_details = []
                for prod in products:
                    prod_m_df = m_df[m_df['Product'] == prod]
                    p_total = len(prod_m_df)
                    p_sold = (prod_m_df['Status'] == 'Sold').sum()
                    if p_total > 0:
                        prod_cr_details.append(f"{prod}: {calculate_cr(p_sold, p_total)}")
                    else:
                        prod_cr_details.append(f"{prod}: N/A")
                
                monthly_records.append({
                    "سال": y,
                    "ماه": m,
                    "کل پرزنت‌ها": m_total_presents,
                    "فروش موفق": m_total_solds,
                    "نرخ تبدیل ماهانه (CR)": m_cr,
                    "مجموع پورتفوی (PR)": f"{int(m_pr):,} Rial",
                    "جزئیات محصولات": " | ".join(prod_cr_details)
                })
            
            st.dataframe(pd.DataFrame(monthly_records), use_container_width=True, hide_index=True)

    # --- 5) MANAGER TREND CHART ---
    elif st.session_state.current_page == "ManagerTrend":
        st.title("📈 روند تغییرات نرخ تبدیل (CR)")
        if not team:
            st.warning("⚠️ لطفاً ابتدا از منوی کناری بخش 'انتخاب تیم و عضو' تیم خود را انتخاب کنید.")
        elif filtered_df.empty:
            st.info("داده‌ای جهت رسم نمودار یافت نشد.")
        else:
            filtered_df['Month'] = filtered_df['ShamsiDate'].apply(lambda x: x.split('/')[1] if len(x.split('/')) > 1 else '00')
            filtered_df['Year'] = filtered_df['ShamsiDate'].apply(lambda x: x.split('/')[0] if len(x.split('/')) > 1 else '00')
            filtered_df['YearMonth'] = filtered_df['Year'] + "/" + filtered_df['Month']
            
            products_options = ["All (کل محصولات)", "Simazar", "Andokhte dar", "Omid", "Finora/ Zarnova"]
            selected_prod_trend = st.selectbox("فیلتر محصول جهت بررسی روند نمودار:", products_options)
            
            if selected_prod_trend != "All (کل محصولات)":
                trend_df = filtered_df[filtered_df['Product'] == selected_prod_trend].copy()
            else:
                trend_df = filtered_df.copy()
                
            if trend_df.empty:
                st.info(f"داده‌ای برای محصول {selected_prod_trend} یافت نشد.")
            else:
                grouped = trend_df.groupby('YearMonth')
                trend_records = []
                
                for ym, group in grouped:
                    total_presents = len(group)
                    total_solds = (group['Status'] == 'Sold').sum()
                    cr_percentage = (total_solds / total_presents * 100) if total_presents > 0 else 0.0
                    
                    trend_records.append({
                        "تاریخ (سال/ماه)": ym,
                        "کل پرزنت‌ها": total_presents,
                        "فروش موفق": total_solds,
                        "نرخ تبدیل (CR %)": round(cr_percentage, 1)
                    })
                
                chart_data = pd.DataFrame(trend_records).sort_values(by="تاریخ (سال/ماه)")
                
                col_metric1, col_metric2 = st.columns(2)
                total_p_trend = chart_data["کل پرزنت‌ها"].sum()
                total_s_trend = chart_data["فروش موفق"].sum()
                global_cr_trend = (total_s_trend / total_p_trend * 100) if total_p_trend > 0 else 0
                
                with col_metric1:
                    st.metric(f"Total Presentations ({selected_prod_trend})", f"{total_p_trend} Presents")
                with col_metric2:
                    st.metric(f"Overall CR ({selected_prod_trend})", f"{global_cr_trend:.1f}%")
                
                st.line_chart(
                    chart_data.set_index("تاریخ (سال/ماه)")["نرخ تبدیل (CR %)"], 
                    use_container_width=True,
                    color="#f1c40f"
                )

    # --- 6) MANAGER SECURITY SETTINGS ---
    elif st.session_state.current_page == "ManagerSettings":
        st.title("🛡️ تنظیمات امنیتی حساب کاربری مدیر")
        new_u = st.text_input("تغییر نام کاربری مدیریت", value=st.session_state.current_user)
        new_p = st.text_input("رمز عبور جدید مدیریت", type="password")
        if st.button("بروزرسانی حساب کاربری"):
            if new_u and new_p:
                old_data = st.session_state.users_db.pop(st.session_state.current_user)
                st.session_state.users_db[new_u] = [new_p, "Manager", old_data[2]]
                save_users(st.session_state.users_db)
                st.session_state.current_user = new_u
                st.success("حساب کاربری مدیریت با موفقیت بروزرسانی شد!")
            else:
                st.error("لطفاً همه فیلدها را پر کنید.")

# --- EMPLOYEE DASHBOARD & NAVIGATED VIEWS ---
elif st.session_state.current_page in ["EmployeeDashboard", "MyPresentList", "CustomersSold", "VisitorsLeads", "MyPortfolio", "ProfileSettings"]:
    with st.sidebar:
        st.markdown(f"### Menu Navigation")
        if st.button("📋 Submit New Presentation", use_container_width=True): navigate_to("EmployeeDashboard")
        if st.button("👥 My Present List", use_container_width=True): navigate_to("MyPresentList")
        if st.button("💰 Customers (Sold)", use_container_width=True): navigate_to("CustomersSold")
        if st.button("🚶 Visitors (Leads)", use_container_width=True): navigate_to("VisitorsLeads")
        if st.button("📊 My Portfolio & CR", use_container_width=True): navigate_to("MyPortfolio")
        if st.button("⚙️ Profile Settings", use_container_width=True): navigate_to("ProfileSettings")
        st.write("---")
        if st.button("🚪 Logout", use_container_width=True): navigate_to("LandingPage")

    df_all = pd.DataFrame(st.session_state.sales_data) if st.session_state.sales_data else pd.DataFrame()
    df_user = df_all[df_all['Employee'] == st.session_state.current_user] if not df_all.empty else pd.DataFrame()

    if st.session_state.current_page == "EmployeeDashboard":
        st.markdown(f"<h1>Welcome, Dear <i>{st.session_state.current_user}</i>!</h1>", unsafe_allow_html=True)
        st.subheader("Submit Presentation/Lead Details")
        
        col_y, col_m, col_d = st.columns(3)
        year = col_y.selectbox("Year", ["1405", "1406", "1407", "1408"], index=0)
        month = col_m.selectbox("Month", [f"{i:02d}" for i in range(1, 13)], index=int(sh_m_now)-1)
        day = col_d.selectbox("Day", [f"{i:02d}" for i in range(1, 32)], index=int(sh_d_now)-1)
        
        product = st.selectbox("Product", ["Simazar", "Andokhte dar", "Omid", "Finora/ Zarnova"])
        is_sale_successful = st.toggle("Submit Successful Sale", value=False)
        
        invest_val = 0
        if is_sale_successful:
            invest_str = st.text_input("Investment Amount (Rial)", value="0")
            cleaned_invest = invest_str.replace(",", "")
            if cleaned_invest.isdigit():
                invest_val = int(cleaned_invest)
                st.caption(f"Formatted Value: {invest_val:,} Rial")
            else:
                st.error("Please enter numbers only.")

        if st.button("Proceed to Consumer Data", type="primary", use_container_width=True):
            shamsi_date = f"{year}/{month}/{day}"
            st.session_state.temp_data = {
                "ShamsiDate": shamsi_date,
                "Employee": st.session_state.current_user,
                "Product": product,
                "Investment": invest_val,
                "Status": "Sold" if is_sale_successful else "Lead",
                "follow_ups": []
            }
            navigate_to("ConsumerData")

    elif st.session_state.current_page == "MyPresentList":
        st.title("My Present List (All Presented Persons)")
        st.dataframe(df_user, use_container_width=True)

    elif st.session_state.current_page == "CustomersSold":
        st.title("My Customers (Successful Transactions)")
        st.dataframe(df_user[df_user['Status'] == 'Sold'] if not df_user.empty else pd.DataFrame(), use_container_width=True)

    elif st.session_state.current_page == "VisitorsLeads":
        st.title("Visitors (Presented but Not Purchased)")
        
        leads_exist = False
        for idx, record in enumerate(st.session_state.sales_data):
            if record['Employee'] == st.session_state.current_user and record['Status'] == 'Lead':
                leads_exist = True
                st.markdown(f"### 📍 Present: {record['Product']} ({record['ShamsiDate']})")
                
                if "follow_ups" not in record:
                    record["follow_ups"] = []
                
                if record["follow_ups"]:
                    st.markdown("**ثبت شده:**")
                    for f_idx, note in enumerate(record["follow_ups"]):
                        st.markdown(f"<div class='followup-box'>{f_idx+1}) {note}</div>", unsafe_allow_html=True)
                
                current_count = len(record["follow_ups"])
                if current_count < 3:
                    col_input, col_add = st.columns([5, 1])
                    with col_input:
                        new_note = st.text_input(f"توضیحات کوتاه علت عدم خرید ({current_count}/3):", key=f"note_in_{idx}")
                    with col_add:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("➕ ثبت", key=f"add_btn_{idx}"):
                            if new_note.strip():
                                record["follow_ups"].append(new_note.strip())
                                save_sales(st.session_state.sales_data)
                                st.success("توضیحات با موفقیت ثبت شد!")
                                st.rerun()
                            else:
                                st.error("متن را وارد کنید.")
                else:
                    st.info("حداکثر ۳ مورد توضیح برای این پرزنت ثبت شده است.")
                st.write("---")
                
        if not leads_exist:
            st.info("No leads available.")

    elif st.session_state.current_page == "MyPortfolio":
        st.title("My Financial Portfolio & Conversion Rates")
        if not df_user.empty:
            total_p = len(df_user)
            total_s = (df_user['Status'] == 'Sold').sum()
            st.metric("My Total Conversion Rate (CR)", calculate_cr(total_s, total_p))
            
            st.markdown("#### CR Breakdown By Product Type")
            for prod in ["Simazar", "Andokhte dar", "Omid", "Finora/ Zarnova"]:
                df_p = df_user[df_user['Product'] == prod]
                p_total = len(df_p)
                p_sold = (df_p['Status'] == 'Sold').sum()
                st.write(f"**{prod}**: {calculate_cr(p_sold, p_total)} (Presents: {p_total})")
        else:
            st.info("No data tracking profile metrics yet.")

    elif st.session_state.current_page == "ProfileSettings":
        st.title("Account Profile Settings")
        
        current_profile_data = st.session_state.users_db[st.session_state.current_user]
        current_pwd = current_profile_data[0]
        meta = current_profile_data[2] if len(current_profile_data) > 2 and isinstance(current_profile_data[2], dict) else {}
        
        old_fn = meta.get("first_name", "")
        old_ln = meta.get("last_name", "")
        old_em = meta.get("email", "")
        old_ph = meta.get("phone", "")
        old_team = meta.get("team", TEAMS_LIST[0])

        new_username = st.text_input("Modify Username", value=st.session_state.current_user)
        new_password = st.text_input("Modify Password", type="password", value=current_pwd)
        
        st.write("---")
        st.markdown("#### Personal & Team Details")
        new_fn = st.text_input("First Name", value=old_fn)
        new_ln = st.text_input("Last Name", value=old_ln)
        new_em = st.text_input("Email Address", value=old_em)
        new_ph = st.text_input("Phone Number", value=old_ph)
        
        default_team_idx = TEAMS_LIST.index(old_team) if old_team in TEAMS_LIST else 0
        new_team = st.selectbox("Team Selection", TEAMS_LIST, index=default_team_idx)

        if st.button("Save Profile Adjustments", type="primary"):
            if new_username and new_password and new_fn and new_ln:
                if new_username != st.session_state.current_user:
                    st.session_state.users_db.pop(st.session_state.current_user)
                
                st.session_state.users_db[new_username] = [
                    new_password, 
                    "Employee", 
                    {
                        "first_name": new_fn, 
                        "last_name": new_ln, 
                        "email": new_em, 
                        "phone": new_ph, 
                        "team": new_team
                    }
                ]
                save_users(st.session_state.users_db)
                st.session_state.current_user = new_username
                st.success("All credentials and profile information altered successfully!")
                st.rerun()
            else:
                st.error("Username, Password, First Name, and Last Name are required.")

# --- CONSUMER DATA SPECIFICATION FORM ---
elif st.session_state.current_page == "ConsumerData":
    st.title("Enter Consumer Specifications")
    st.info("Please fill out all the mandatory fields below to complete submission.")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=1, max_value=100, step=1, value=25)
        gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
        marital_status = st.radio("Marital Status", ["Single", "Married"], horizontal=True)
    with col2:
        num_children = st.number_input("Number of Children (Optional)", min_value=0, max_value=15, value=0, step=1)
        smoker = st.radio("Smoker", ["Yes", "No"], horizontal=True)
        education = st.selectbox("Education", ["Under Diploma", "Diploma", "Bachelor's degree", "Master's degree", "PhD"])

    occupations_list = [
        "پزشک و کادر درمانی بالا رتبه", "کارمند اداری/شرکتی", "مهندس/مشاور فنی", 
        "فرهنگی/استاد دانشگاه/معلم", "بازنشسته کشوری یا لشگری", "خانه دار", 
        "شغل آزاد/اصناف مستقل", "کارگر صنعتی/امور فنی دستمزد", "دانشجو/دانش آموز", "سایر"
    ]
    occupation = st.selectbox("Occupation (شغل)", occupations_list)
    
    custom_occupation = ""
    if occupation == "سایر":
        custom_occupation = st.text_input("لطفاً شغل دقیق را بنویسید:")

    cust_notes = st.text_area("Notes / Client Feedback")

    if st.button("Complete Entry & Save", type="primary"):
        final_occupation = custom_occupation if occupation == "سایر" else occupation
        
        if occupation == "سایر" and not custom_occupation:
            st.error("لطفا فیلد سایر شغل را پر کنید.")
        else:
            temp = st.session_state.temp_data
            invest = temp["Investment"]
            prod = temp["Product"]
            
            pr = invest if prod in ["Simazar", "Andokhte dar", "Omid"] else (0.40 * invest)
            
            new_record = {
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
                "Occupation": final_occupation,
                "Notes": cust_notes,
                "follow_ups": []
            }
            
            st.session_state.sales_data.append(new_record)
            save_sales(st.session_state.sales_data)
            st.success("Successfully logged consumer transaction details!")
            st.session_state.temp_data = {}
            navigate_to("EmployeeDashboard")

    if st.button("Discard Presentation Log"):
        st.session_state.temp_data = {}
        navigate_to("EmployeeDashboard")
