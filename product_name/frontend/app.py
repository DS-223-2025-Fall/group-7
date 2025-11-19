import streamlit as st

# -----------------------------
# GLOBAL PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Adaptive Pricing System",
    layout="wide"
)

# -----------------------------
# NAVIGATION
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

def go_to(page_name):
    st.session_state.page = page_name

# -----------------------------
# LOGIN PAGE
# -----------------------------
def login_page():
    st.markdown("<h1 style='text-align:center; color:#333;'>Login Page</h1>", unsafe_allow_html=True)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        go_to("dashboard")

# -----------------------------
# DASHBOARD PAGE
# -----------------------------
def dashboard_page():
    st.markdown("<h1>Dashboard</h1>", unsafe_allow_html=True)
    st.write("Welcome to the dashboard!")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Revenue", "$77,777")
    with col2:
        st.metric("Average Conversion", "22%")
    with col3:
        st.metric("Regret Minimization", "5%")

# -----------------------------
# PAGE ROUTING
# -----------------------------
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "dashboard":
    dashboard_page()
