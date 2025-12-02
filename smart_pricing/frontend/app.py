import streamlit as st
import requests
from decimal import Decimal
import pandas as pd
import numpy as np

API_BASE_URL = "http://backend:8000"  # docker-compose backend name


# ----------------------- STREAMLIT CONFIG --------------------------
st.set_page_config(page_title="Smart Pricing System", layout="wide")

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] { background-color: #6f7ec9; }
    [data-testid="stSidebar"] { background-color: #111827; }
    #MainMenu, header, footer { visibility: hidden; }
    .title-text { text-align: center; color: #fff; font-size: 36px; 
                  font-weight: 700; letter-spacing: 2px; margin-top: 40px;}
    .card { background-color: rgba(255,255,255,0.05); padding: 32px; border-radius: 4px;
            border: 1px solid rgba(255,255,255,0.4); box-shadow: 0 4px 8px rgba(0,0,0,0.25);}
    .nav-title { color: #fff; font-size: 22px; font-weight: 700;}
    .metric-card { background-color: #3866a6; padding: 18px; border-radius: 4px; 
                   color: #fff; text-align: center;}
    .metric-label { font-size: 13px; text-transform: uppercase; }
    .metric-value { font-size: 22px; font-weight: 700; margin-top: 8px; }
    .section-title { color: #fff; font-size: 24px; font-weight: 700; margin-bottom: 16px;}
    .subheading { color: #cdd4ff; font-size: 14px; margin-bottom: 8px;}
    .right-button { display: flex; justify-content: flex-end; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------- SESSION STATE ----------------------------
if "page" not in st.session_state:
    st.session_state.page = "auth"
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "show_register" not in st.session_state:
    st.session_state.show_register = False


def go_to(page_name):
    st.session_state.page = page_name


def to_float(v):
    try:
        return float(v)
    except:
        return v


# Force auth if not logged in
if not st.session_state.is_authenticated and st.session_state.page != "auth":
    st.session_state.page = "auth"


# ------------------------- API HELPERS -----------------------------
def fetch_projects():
    try:
        r = requests.get(f"{API_BASE_URL}/projects")
        return r.json() if r.status_code == 200 else []
    except:
        return []


def fetch_bandits_for_project(project_id: int):
    try:
        r = requests.get(f"{API_BASE_URL}/projects/{project_id}/bandits")
        return r.json() if r.status_code == 200 else []
    except:
        return []


def run_algorithm_for_project(project_id: int):
    try:
        r = requests.post(f"{API_BASE_URL}/projects/{project_id}/thompson/select")
        return r.json() if r.status_code == 200 else None
    except:
        return None


def submit_reward(bandit_id: int, reward: float, decision=None):
    payload = {"reward": reward, "decision": decision}
    try:
        r = requests.post(f"{API_BASE_URL}/bandits/{bandit_id}/thompson/reward", json=payload)
        return r.json() if r.status_code == 200 else None
    except:
        return None


# -------------------------- HEADER NAV -----------------------------
def render_header():
    if not st.session_state.is_authenticated:
        return

    cols = st.columns([3, 1.2, 1.2, 1.3, 1])
    with cols[0]:
        st.markdown("<div class='nav-title'>DASHBOARD</div>", unsafe_allow_html=True)
        st.markdown(
            f"<span style='font-size:12px;color:#e5e7ff;'>Signed in as {st.session_state.user_email}</span>",
            unsafe_allow_html=True,
        )
    with cols[1]:
        if st.button("Overview", use_container_width=True):
            go_to("dashboard")
    with cols[2]:
        if st.button("Product Status", use_container_width=True):
            go_to("product_details")
    with cols[3]:
        if st.button("Add New Product", use_container_width=True):
            go_to("add_product")
    with cols[4]:
        if st.button("Logout", use_container_width=True):
            st.session_state.is_authenticated = False
            st.session_state.user_email = ""
            go_to("auth")

    st.markdown("<hr style='border-color: rgba(255,255,255,0.3);'/>", unsafe_allow_html=True)


# -------------------------- AUTH PAGE ------------------------------
def auth_page():
    st.markdown("<div class='title-text'>ADAPTIVE PRICING SYSTEM</div>", unsafe_allow_html=True)
    left, center, right = st.columns([1, 1, 1])

    with center:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;color:#fff;font-size:20px;'>Dashboard Login</div>", unsafe_allow_html=True)

        email = st.text_input("", placeholder="EMAIL", label_visibility="collapsed", key="login_email")
        password = st.text_input("", placeholder="PASSWORD", type="password", label_visibility="collapsed", key="login_password")
        login_clicked = st.button("LOGIN", use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

        if login_clicked:
            if email and password:
                try:
                    r = requests.post(f"{API_BASE_URL}/auth/login", json={"email": email, "password": password})
                    if r.status_code == 200:
                        data = r.json()
                        st.session_state.is_authenticated = True
                        st.session_state.user_email = data.get("email", email)
                        go_to("dashboard")
                        st.rerun()
                    else:
                        st.error("Login failed.")
                except Exception as e:
                    st.error(f"Error: {e}")

        if st.button("Create Account", use_container_width=True):
            st.session_state.show_register = True

    # ------- Registration --------
    if st.session_state.show_register:
        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
        _, mid, _ = st.columns([1, 1, 1])
        with mid:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div style='text-align:center;color:#fff;'>Create Account</div>", unsafe_allow_html=True)

            reg_email = st.text_input("", placeholder="EMAIL", label_visibility="collapsed", key="reg_email")
            reg_password = st.text_input("", placeholder="PASSWORD", type="password", label_visibility="collapsed", key="reg_password")
            reg_confirm = st.text_input("", placeholder="CONFIRM PASSWORD", type="password", label_visibility="collapsed", key="reg_confirm")
            reg_submit = st.button("REGISTER", use_container_width=True)

            if reg_submit:
                if not reg_email or reg_password != reg_confirm:
                    st.error("Invalid data.")
                else:
                    try:
                        r = requests.post(f"{API_BASE_URL}/auth/register", json={"email": reg_email, "password": reg_password})
                        if r.status_code in (200, 201):
                            st.success("Account created. You can login now.")
                            st.session_state.show_register = False
                        else:
                            st.error("Register failed.")
                    except:
                        st.error("Backend error.")


# -------------------------- DASHBOARD ------------------------------
def dashboard_page():
    projects = fetch_projects()
    st.markdown("<div class='section-title'>DASHBOARD / OVERVIEW</div>", unsafe_allow_html=True)

    st.metric("Total Projects", len(projects))
    dates = pd.date_range("2024-08-01", periods=10, freq="7D")
    line_one = np.linspace(0.8, 2.0, len(dates)) + np.random.uniform(-0.2, 0.2, len(dates))
    df_chart = pd.DataFrame({"date": dates, "Revenue": line_one}).set_index("date")
    st.line_chart(df_chart, height=260)


# --------------------- PRODUCT DETAILS PAGE ------------------------
def product_details_page():
    projects = fetch_projects()
    if not projects:
        st.info("No products yet.")
        return

    # Project selection
    project_map = {p["project_id"]: p for p in projects}
    selected_id = st.selectbox(
        "Select Product",
        list(project_map.keys()),
        format_func=lambda pid: project_map[pid]["description"]
    )

    # Fetch bandits for this project
    bandits = fetch_bandits_for_project(selected_id)
    if not bandits:
        st.warning("No bandits created yet for this product.")
        return

    # Best price so far
    best = max(bandits, key=lambda b: float(b["mean"]))
    best_price = to_float(best["price"])
    st.markdown(
        f"<div class='section-title'>Optimal Price: ${best_price:.2f}</div>",
        unsafe_allow_html=True
    )

    # Bandits Table
    rows = [{
        "Price": to_float(b["price"]),
        "Trials": b["trial"],
        "Reward Sum": to_float(b["reward"]),
        "Mean": to_float(b["mean"]),
    } for b in bandits]
    st.dataframe(rows, use_container_width=True)

    # Buttons (Run Algorithm + Plot + Simulation)
    col1, col2 = st.columns(2)

    # ----- Run Thompson Sampling -----
    with col1:
        if st.button("Run Algorithm", use_container_width=True):
            res = run_algorithm_for_project(selected_id)
            if res:
                price_val = float(res.get("price", 0))
                st.success(f"New price selected: ${price_val:.2f}")
            else:
                st.error("Failed to run algorithm.")

    # ----- Plot & Simulation in SAME BLOCK -----
    with col2:
        if st.button("Show Posterior Plot", use_container_width=True):
            plot_url = f"{API_BASE_URL}/projects/{selected_id}/thompson/plot"

            try:
                plot_response = requests.get(plot_url)

                if plot_response.status_code == 200:
                    st.image(plot_response.content, caption="Posterior Distributions of Bandits")
                else:
                    st.error(f"Error fetching plot: {plot_response.text}")

            except Exception as e:
                st.error(f"Could not load plot: {e}")

        if st.button("Run Full Simulation (Updates Model)", use_container_width=True):
            sim_res = requests.post(
                f"{API_BASE_URL}/projects/{selected_id}/thompson/run",
                json={"n_trials": 50}  # Try changing this later
            )
            if sim_res.status_code == 200:
                st.success("Simulation finished! Try the plot again.")
                st.rerun()  # Refresh UI after DB update
            else:
                st.error(f"Error running simulation: {sim_res.text}")



# ------------------------- ADD PRODUCT -----------------------------
def add_product_page():
    st.write("DEBUG: using latest version")

    st.markdown("<div class='section-title'>ADD NEW PRODUCT</div>", unsafe_allow_html=True)

    top_cols = st.columns([3, 1])
    with top_cols[1]:
        if st.button("BACK TO DASHBOARD", use_container_width=True):
            go_to("dashboard")
            st.rerun()

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    with st.form("add_product_form"):
        product_name = st.text_input("", placeholder="PRODUCT NAME", label_visibility="collapsed")
        price_variants_str = st.text_input("", placeholder="ENTER PRICE VARIANTS TO TEST (e.g. 10, 15, 20)",
                                           label_visibility="collapsed")
        start_clicked = st.form_submit_button("START EXPERIMENT")

    if start_clicked:
        if not product_name:
            st.error("Product name is required.")
            return

        # Parse prices
        try:
            prices = [float(p.strip()) for p in price_variants_str.split(",") if p.strip()]
        except:
            st.error("Invalid price format.")
            return

        number_bandits = len(prices) if prices else 1

        # --------------------------
        # 1) CREATE PROJECT
        # --------------------------
        payload = {"description": product_name, "number_bandits": number_bandits}
        r = requests.post(f"{API_BASE_URL}/projects", json=payload)

        try:
            project = r.json()
            project_id = project.get("project_id")
            st.success(f"Project created successfully! Project ID = {project_id}")
        except Exception:
            st.error(f"Failed to create product: {r.text}")
            return


        project = r.json()
        project_id = project.get("project_id")
        st.success(f"Project created successfully! ID = {project_id}")

        # --------------------------
        # 2) CREATE BANDITS
        # --------------------------
        if not prices:
            prices = [0.0]

        created_bandits = 0
        for price in prices:
            rb = requests.post(f"{API_BASE_URL}/projects/{project_id}/bandits", json={"price": price})
            if rb.status_code in (200, 201):
                created_bandits += 1

        st.success(f"Created {created_bandits} bandits successfully.")

        # --------------------------
        # 3) RUN ALGORITHM ONCE
        # --------------------------
        res = run_algorithm_for_project(project_id)
        if res and "price" in res:
            st.success(f"Thompson Sampling suggested starting price: ${float(res['price']):.2f}")
        else:
            st.info("Project created. Waiting for data...")


# ----------------------------- ROUTER -------------------------------
if st.session_state.page == "auth":
    auth_page()
else:
    render_header()
    if st.session_state.page == "dashboard":
        dashboard_page()
    elif st.session_state.page == "product_details":
        product_details_page()
    elif st.session_state.page == "add_product":
        add_product_page()
