import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import streamlit as st
import requests
from decimal import Decimal
import pandas as pd
import numpy as np
import threading
import time

from db.database_init import init_db
from backend.endpoints import app as flask_app

API_BASE_URL = "http://localhost:5000"

st.set_page_config(page_title="Smart Pricing System", layout="wide")

if "backend_started" not in st.session_state:
    init_db()
    def _run_backend():
        flask_app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
    t = threading.Thread(target=_run_backend, daemon=True)
    t.start()
    time.sleep(1)
    st.session_state.backend_started = True

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #6f7ec9;
    }
    [data-testid="stSidebar"] {
        background-color: #111827;
    }
    #MainMenu, header, footer {
        visibility: hidden;
    }
    .title-text {
        text-align: center;
        color: #ffffff;
        font-size: 36px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-top: 40px;
        margin-bottom: 40px;
    }
    .card {
        background-color: rgba(255,255,255,0.05);
        padding: 32px;
        border-radius: 4px;
        border: 1px solid rgba(255,255,255,0.4);
        box-shadow: 0 4px 8px rgba(0,0,0,0.25);
    }
    .nav-title {
        color: #ffffff;
        font-size: 22px;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .metric-card {
        background-color: #3866a6;
        padding: 18px;
        border-radius: 4px;
        color: #ffffff;
        text-align: center;
    }
    .metric-label {
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-value {
        font-size: 22px;
        font-weight: 700;
        margin-top: 8px;
    }
    .section-title {
        color: #ffffff;
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 16px;
    }
    .subheading {
        color: #cdd4ff;
        font-size: 14px;
        margin-bottom: 8px;
    }
    .right-button {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        margin-top: 12px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "page" not in st.session_state:
    st.session_state.page = "auth"
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "show_register" not in st.session_state:
    st.session_state.show_register = False

def to_float(v):
    if isinstance(v, Decimal):
        return float(v)
    try:
        return float(v)
    except Exception:
        return v

def go_to(page_name):
    st.session_state.page = page_name

if not st.session_state.is_authenticated and st.session_state.page != "auth":
    st.session_state.page = "auth"

def render_header():
    if not st.session_state.is_authenticated:
        return
    with st.container():
        cols = st.columns([3, 1.2, 1.2, 1.3, 1])
        with cols[0]:
            st.markdown("<div class='nav-title'>DASHBOARD</div>", unsafe_allow_html=True)
            if st.session_state.user_email:
                st.markdown(f"<span style='font-size:12px;color:#e5e7ff;'>Signed in as {st.session_state.user_email}</span>", unsafe_allow_html=True)
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

def auth_page():
    st.markdown("<div class='title-text'>ADAPTIVE PRICING SYSTEM</div>", unsafe_allow_html=True)
    left, center, right = st.columns([1, 1, 1])
    with center:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;color:#ffffff;font-size:20px;font-weight:600;margin-bottom:20px;'>Dashboard Login</div>", unsafe_allow_html=True)
        email = st.text_input("", placeholder="EMAIL", label_visibility="collapsed", key="login_email")
        password = st.text_input("", placeholder="PASSWORD", type="password", label_visibility="collapsed", key="login_password")
        login_clicked = st.button("LOGIN", key="login_btn", use_container_width=True)
        st.markdown("<div style='text-align:center;margin-top:10px;'><span style='color:#e5e7ff;font-size:13px;'>Forgot password?</span></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;margin-top:16px;'><span style='color:#e5e7ff;font-size:13px;'>Don't have an account?</span></div>", unsafe_allow_html=True)
        register_clicked = st.button("Create Account", key="open_register", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        if login_clicked:
            if not email or not password:
                st.error("Please enter email and password.")
            else:
                try:
                    r = requests.post(f"{API_BASE_URL}/auth/login", json={"email": email, "password": password})
                    if r.status_code == 200:
                        data = r.json()
                        st.session_state.is_authenticated = True
                        st.session_state.user_email = data.get("email", email)
                        go_to("dashboard")
                        st.rerun()
                    else:
                        try:
                            msg = r.json().get("message") or r.text
                        except Exception:
                            msg = r.text
                        st.error(f"Login failed: {msg}")
                except Exception as e:
                    st.error(f"Login error: {e}")
        if register_clicked:
            st.session_state.show_register = True
    if st.session_state.show_register:
        st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
        r_left, r_center, r_right = st.columns([1, 1, 1])
        with r_center:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div style='text-align:center;color:#ffffff;font-size:18px;font-weight:600;margin-bottom:18px;'>Create Account</div>", unsafe_allow_html=True)
            reg_email = st.text_input("", placeholder="EMAIL", label_visibility="collapsed", key="reg_email")
            reg_password = st.text_input("", placeholder="PASSWORD", type="password", label_visibility="collapsed", key="reg_password")
            reg_confirm = st.text_input("", placeholder="CONFIRM PASSWORD", type="password", label_visibility="collapsed", key="reg_confirm")
            reg_submit = st.button("REGISTER", key="register_btn", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            if reg_submit:
                if not reg_email or not reg_password or reg_password != reg_confirm:
                    st.error("Please provide a valid email and matching passwords.")
                else:
                    try:
                        r = requests.post(f"{API_BASE_URL}/auth/register", json={"email": reg_email, "password": reg_password})
                        if r.status_code == 201:
                            st.success("Registration successful. You can now log in.")
                            st.session_state.show_register = False
                        else:
                            try:
                                msg = r.json().get("message") or r.text
                            except Exception:
                                msg = r.text
                            st.error(f"Registration failed: {msg}")
                    except Exception as e:
                        st.error(f"Registration error: {e}")

def fetch_projects():
    try:
        r = requests.get(f"{API_BASE_URL}/projects")
        if r.status_code == 200:
            return r.json()
    except Exception:
        return []
    return []

def fetch_bandits():
    try:
        r = requests.get(f"{API_BASE_URL}/bandits")
        if r.status_code == 200:
            return r.json()
    except Exception:
        return []
    return []

def fetch_experiments():
    try:
        r = requests.get(f"{API_BASE_URL}/experiments")
        if r.status_code == 200:
            return r.json()
    except Exception:
        return []
    return []

def run_algorithm_for_project(project_id, strategy="bernoulli", create_experiment=True):
    try:
        r = requests.post(
            f"{API_BASE_URL}/algorithm/run/{project_id}",
            json={"strategy": strategy, "create_experiment": create_experiment},
        )
        if r.status_code in (200, 201):
            return r.json()
        return None
    except Exception:
        return None

def fetch_optimal_info(project_id):
    try:
        r = requests.get(f"{API_BASE_URL}/algorithm/optimal_price/{project_id}")
        if r.status_code == 200:
            return r.json()
    except Exception:
        return None
    return None

def dashboard_page():
    projects = fetch_projects()
    bandits = fetch_bandits()
    experiments = fetch_experiments()
    total_projects = len(projects)
    total_bandits = len(bandits)
    total_experiments = len(experiments)
    total_reward = 0.0
    for e in experiments:
        if "reward" in e and e["reward"] is not None:
            total_reward += to_float(e["reward"])
    st.markdown("<div class='section-title'>DASHBOARD / OVERVIEW</div>", unsafe_allow_html=True)
    top_cols = st.columns([1, 1, 1, 1])
    with top_cols[0]:
        st.markdown("<div class='metric-card'><div class='metric-label'>Total Revenue</div><div class='metric-value'>$ {:,.2f}</div></div>".format(total_reward), unsafe_allow_html=True)
    with top_cols[1]:
        avg_conv = "22%"
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Average Conversion</div><div class='metric-value'>{avg_conv}</div></div>", unsafe_allow_html=True)
    with top_cols[2]:
        regret = "5%"
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Regret Minimization</div><div class='metric-value'>{regret}</div></div>", unsafe_allow_html=True)
    with top_cols[3]:
        st.markdown("<div class='right-button'>", unsafe_allow_html=True)
        if st.button("CREATE NEW EXPERIMENT", key="create_experiment_btn"):
            go_to("add_product")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='subheading'>Active Experiments Table</div>", unsafe_allow_html=True)
    if experiments:
        rows = []
        bandit_by_id = {b["bandit_id"]: b for b in bandits}
        project_by_id = {p["project_id"]: p for p in projects}
        for e in experiments:
            b = bandit_by_id.get(e["bandit_id"], {})
            p = project_by_id.get(e["project_id"], {})
            rows.append(
                {
                    "Product Name": p.get("description", ""),
                    "Current Best Price": to_float(b.get("price")),
                    "Conversion Rate": "22%",
                    "Revenue": to_float(e.get("reward")),
                    "Status": "Active",
                }
            )
        st.dataframe(rows, use_container_width=True, height=220)
    else:
        st.info("No active experiments yet.")
    st.markdown("<div class='subheading' style='margin-top:20px;'>Revenue And Trend Over Time</div>", unsafe_allow_html=True)
    dates = pd.date_range("2024-08-01", periods=10, freq="7D")
    line_one = np.linspace(0.8, 2.0, len(dates)) + np.random.uniform(-0.2, 0.2, len(dates))
    line_two = np.linspace(0.6, 1.8, len(dates)) + np.random.uniform(-0.2, 0.2, len(dates))
    df_chart = pd.DataFrame({"date": dates, "Line One": line_one, "Line Two": line_two}).set_index("date")
    st.line_chart(df_chart, height=260)

def product_details_page():
    projects = fetch_projects()
    bandits = fetch_bandits()
    experiments = fetch_experiments()
    if not projects:
        st.info("No products available yet.")
        return
    project_map = {p["project_id"]: p for p in projects}
    bandits_by_project = {}
    for b in bandits:
        pid = b.get("project_id")
        bandits_by_project.setdefault(pid, []).append(b)
    st.markdown("<div class='section-title'>PRODUCT NAME / STATUS</div>", unsafe_allow_html=True)
    project_ids = [p["project_id"] for p in projects]
    selected_id = st.selectbox("Select Product", project_ids, index=0, format_func=lambda pid: project_map[pid]["description"])
    selected_project = project_map[selected_id]
    opt_info = fetch_optimal_info(selected_id)
    optimal_price = None
    if opt_info and opt_info.get("optimal_price") is not None:
        optimal_price = opt_info.get("optimal_price")
    else:
        selected_bandits = bandits_by_project.get(selected_id, [])
        if selected_bandits:
            best = max(selected_bandits, key=lambda b: float(b.get("mean") or 0.0))
            optimal_price = to_float(best.get("price"))
    col_left, col_right = st.columns([2, 1])
    with col_left:
        if optimal_price is not None:
            st.markdown(
                f"<div class='metric-card' style='margin-top:8px;max-width:260px;text-align:center;'>"
                f"<div class='metric-label'>Optimal Price (So Far)</div>"
                f"<div class='metric-value' style='margin-top:6px;'>${float(optimal_price):.2f}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
        else:
            st.info("No pricing data yet for this product.")
    with col_right:
        if st.button("BACK TO DASHBOARD", use_container_width=True):
            go_to("dashboard")
            st.rerun()
        if st.button("Run Algorithm", use_container_width=True):
            res = run_algorithm_for_project(selected_id, strategy="bernoulli", create_experiment=True)
            if res:
                st.success(f"Thompson Sampling selected price ${float(res['optimal_price']):.2f} for project {selected_id}.")
                st.rerun()
            else:
                st.error("Failed to run algorithm.")
        if st.button("Pause Test", use_container_width=True):
            st.warning("Test paused (placeholder).")
    st.markdown("<div class='subheading' style='margin-top:20px;'>Active Experiments Table</div>", unsafe_allow_html=True)
    selected_bandits = bandits_by_project.get(selected_id, [])
    if selected_bandits:
        total_trials = sum(b.get("trial", 0) for b in selected_bandits) or 1
        rows = []
        for b in selected_bandits:
            impressions = b.get("trial", 0)
            reward = to_float(b.get("reward"))
            conv_rate = 0.0
            if impressions > 0:
                conv_rate = min(1.0, reward / impressions)
            allocated = impressions / total_trials * 100.0
            rows.append(
                {
                    "Price Variant": to_float(b.get("price")),
                    "Impressions": impressions,
                    "Conversion Rate": f"{conv_rate*100:.1f}%",
                    "Revenue": reward,
                    "Allocated Traffic": f"{allocated:.1f}%",
                }
            )
        st.dataframe(rows, use_container_width=True, height=260)
    else:
        st.info("No bandits configured for this product.")
    st.markdown(
        """
        <div style="color:#e5e7ff;font-size:12px;margin-top:18px;">
        <div>Last updated: 2 minutes ago</div>
        <div>Algorithm: Thompson Sampling (Bernoulli)</div>
        <div>Next update scheduled: In 10 minutes</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div style="color:#e5e7ff;font-size:12px;margin-top:10px;">
        <div><strong>Algorithm Insights:</strong></div>
        <ul>
        <li>Thompson Sampling currently favors the price with highest sampled reward.</li>
        <li>Estimated regret reduced compared to static A/B testing.</li>
        <li>Model confidence increases as more data accumulates.</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

def add_product_page():
    st.markdown("<div class='section-title'>ADD NEW PRODUCT</div>", unsafe_allow_html=True)
    top_cols = st.columns([3, 1])
    with top_cols[1]:
        if st.button("BACK TO DASHBOARD", use_container_width=True, key="back_dashboard_btn"):
            go_to("dashboard")
            st.rerun()
    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    with st.form("add_product_form"):
        product_name = st.text_input("", placeholder="PRODUCT NAME", label_visibility="collapsed")
        product_category = st.text_input("", placeholder="PRODUCT CATEGORY", label_visibility="collapsed")
        product_description = st.text_area("", placeholder="PRODUCT DESCRIPTION", label_visibility="collapsed", height=100)
        price_variants_str = st.text_input("", placeholder="ENTER PRICE VARIANTS TO TEST (e.g. 10, 15, 20)", label_visibility="collapsed")
        duration = st.selectbox("EXPERIMENT DURATION", ["7 DAYS", "14 DAYS", "30 DAYS"], index=0)
        traffic_split = st.selectbox("TRAFFIC SPLIT", ["Automatic (Thompson Sampling)", "Even Split", "Custom"], index=0)
        metric = st.selectbox("CONVERSION METRIC", ["Purchase", "Click"], index=0)
        start_col, cancel_col = st.columns([1, 1])
        with start_col:
            start_clicked = st.form_submit_button("START EXPERIMENT")
        with cancel_col:
            cancel_clicked = st.form_submit_button("CANCEL")
    if cancel_clicked:
        go_to("dashboard")
        st.rerun()
    if start_clicked:
        if not product_name:
            st.error("Product name is required.")
            return
        prices = []
        if price_variants_str:
            for token in price_variants_str.replace(";", ",").split(","):
                token = token.strip()
                if not token:
                    continue
                try:
                    prices.append(float(token))
                except ValueError:
                    st.error(f"Invalid price value: {token}")
                    return
        number_bandits = max(1, len(prices)) if prices else 1
        try:
            payload = {"description": product_name, "number_bandits": number_bandits}
            r = requests.post(f"{API_BASE_URL}/projects", json=payload)
            if r.status_code != 201:
                st.error(f"Failed to create product: {r.text}")
                return
            project = r.json()
            project_id = project.get("project_id")
            created_bandits = 0
            if not prices:
                prices = [0.0]
            for price in prices:
                b_payload = {
                    "project_id": project_id,
                    "price": price,
                    "mean": 0.0,
                    "variance": 1.0,
                    "reward": 0.0,
                    "trial": 0,
                    "number_explored": 0,
                }
                rb = requests.post(f"{API_BASE_URL}/bandits", json=b_payload)
                if rb.status_code == 201:
                    created_bandits += 1
            res = run_algorithm_for_project(project_id, strategy="bernoulli", create_experiment=True)
            if res:
                st.success(
                    f"Experiment created for '{product_name}' with {created_bandits} price variants. "
                    f"Initial optimal price from Thompson Sampling: ${float(res['optimal_price']):.2f}."
                )
            else:
                st.success(f"Experiment created for '{product_name}' with {created_bandits} price variants.")
        except Exception as e:
            st.error(f"Error creating experiment: {e}")

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
