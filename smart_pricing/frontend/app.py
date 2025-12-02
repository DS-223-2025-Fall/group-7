import streamlit as st
import requests
from decimal import Decimal
import pandas as pd
import numpy as np

API_BASE_URL = "http://backend:8000"  # docker-compose backend name

# ----------------------- STREAMLIT CONFIG --------------------------
st.set_page_config(
    page_title="Smart Pricing System",
    layout="wide",
    page_icon="💸",
)

st.markdown(
    """
    <style>
    /* ---------- GLOBAL LAYOUT ---------- */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top, #4f46e5 0, #111827 55%, #020617 100%);
        color: #e5e7eb;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #020617, #020617);
        border-right: 1px solid rgba(148, 163, 184, 0.2);
    }
    #MainMenu, header, footer { visibility: hidden; }

    /* ---------- TYPOGRAPHY ---------- */
    .title-text {
        text-align: center;
        color: #f9fafb;
        font-size: 38px;
        font-weight: 800;
        letter-spacing: 0.14em;
        margin-top: 30px;
        text-transform: uppercase;
    }
    .subtitle-text {
        text-align: center;
        color: #c7d2fe;
        font-size: 14px;
        margin-top: 6px;
        margin-bottom: 24px;
    }
    .section-title {
        color: #f9fafb;
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 4px;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    .section-subtitle {
        color: #9ca3af;
        font-size: 13px;
        margin-bottom: 16px;
    }

    /* ---------- CARDS ---------- */
    .card {
        background: linear-gradient(
            135deg,
            rgba(15, 23, 42, 0.95),
            rgba(30, 64, 175, 0.90)
        );
        border-radius: 18px;
        padding: 26px 24px;
        border: 1px solid rgba(148, 163, 184, 0.45);
        box-shadow:
            0 22px 45px rgba(15, 23, 42, 0.7),
            0 0 0 1px rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(16px);
    }
    .card-plain {
        background: rgba(15, 23, 42, 0.85);
        border-radius: 16px;
        padding: 22px 20px;
        border: 1px solid rgba(55, 65, 81, 0.9);
        box-shadow:
            0 14px 30px rgba(0, 0, 0, 0.55),
            0 0 0 1px rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(16px);
    }

    /* ---------- NAV BAR ---------- */
    .nav-title {
        color: #f9fafb;
        font-size: 22px;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }
    .nav-sub {
        color: #9ca3af;
        font-size: 12px;
        margin-top: 6px;
    }
    .nav-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 3px 9px;
        border-radius: 999px;
        background: rgba(55, 65, 81, 0.85);
        color: #e5e7eb;
        font-size: 11px;
        margin-left: 8px;
    }

    /* make the nav buttons look like pills */
    .stButton > button {
        border-radius: 999px !important;
        border: 1px solid rgba(148, 163, 184, 0.5);
        background: linear-gradient(135deg, #1d4ed8, #3b82f6);
        color: #f9fafb;
        font-weight: 600;
        font-size: 13px;
        padding: 0.4rem 0.8rem;
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.55);
        transition: all 0.18s ease-out;
    }
    .stButton > button:hover {
        box-shadow: 0 14px 30px rgba(15, 23, 42, 0.8);
        transform: translateY(-1px);
        border-color: rgba(191, 219, 254, 0.8);
    }

    /* ---------- AUTH CARDS ---------- */
    .auth-card {
        max-width: 420px;
        margin: 0 auto;
    }
    .auth-title {
        text-align: center;
        color: #f9fafb;
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 18px;
    }

    /* ---------- INPUTS ---------- */
    .stTextInput > div > div > input {
        background: rgba(15, 23, 42, 0.75);
        color: #e5e7eb;
        border-radius: 999px;
        border: 1px solid rgba(148, 163, 184, 0.5);
        padding-left: 16px;
        padding-right: 16px;
        height: 40px;
        font-size: 13px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 1px rgba(59, 130, 246, 0.6);
    }

    /* ---------- METRICS ---------- */
    .metric-card {
        background: linear-gradient(135deg, #1d4ed8, #2563eb);
        padding: 14px 16px;
        border-radius: 14px;
        color: #f9fafb;
        text-align: left;
        border: 1px solid rgba(191, 219, 254, 0.7);
        box-shadow:
            0 14px 30px rgba(15, 23, 42, 0.7),
            0 0 0 1px rgba(30, 64, 175, 0.7);
    }
    .metric-label {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #e0f2fe;
    }
    .metric-value {
        font-size: 22px;
        font-weight: 700;
        margin-top: 4px;
    }
    .metric-sub {
        font-size: 11px;
        color: #bfdbfe;
        margin-top: 4px;
    }

    /* ---------- SMALL UTILITIES ---------- */
    .right-button {
        display: flex;
        justify-content: flex-end;
    }
    .chip {
        display: inline-flex;
        padding: 4px 10px;
        border-radius: 999px;
        border: 1px solid rgba(148, 163, 184, 0.6);
        font-size: 11px;
        color: #e5e7eb;
        gap: 6px;
        align-items: center;
    }
    .chip-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #22c55e;
        box-shadow: 0 0 8px rgba(34, 197, 94, 0.6);
    }
    .divider-soft {
        border: none;
        border-top: 1px solid rgba(148, 163, 184, 0.35);
        margin: 10px 0 16px 0;
    }
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
    except Exception:
        return v


# Force auth if not logged in
if not st.session_state.is_authenticated and st.session_state.page != "auth":
    st.session_state.page = "auth"


# ------------------------- API HELPERS -----------------------------
def fetch_projects():
    try:
        r = requests.get(f"{API_BASE_URL}/projects")
        return r.json() if r.status_code == 200 else []
    except Exception:
        return []


def fetch_bandits_for_project(project_id: int):
    try:
        r = requests.get(f"{API_BASE_URL}/projects/{project_id}/bandits")
        return r.json() if r.status_code == 200 else []
    except Exception:
        return []


def run_algorithm_for_project(project_id: int):
    try:
        r = requests.post(f"{API_BASE_URL}/projects/{project_id}/thompson/select")
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


def submit_reward(bandit_id: int, reward: float, decision=None):
    payload = {"reward": reward, "decision": decision}
    try:
        r = requests.post(
            f"{API_BASE_URL}/bandits/{bandit_id}/thompson/reward", json=payload
        )
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


# -------------------------- HEADER NAV -----------------------------
def render_header():
    if not st.session_state.is_authenticated:
        return

    cols = st.columns([3, 1.1, 1.2, 1.6, 1])
    with cols[0]:
        st.markdown(
            """
            <div class="nav-title">
                SMART PRICING
                <span class="nav-badge">
                    <span class="chip-dot"></span>
                    Live Dashboard
                </span>
            </div>
            <div class="nav-sub">
                Signed in as <strong>{email}</strong>
            </div>
            """.format(email=st.session_state.user_email),
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

    st.markdown("<hr class='divider-soft'/>", unsafe_allow_html=True)


# -------------------------- AUTH PAGE ------------------------------
def auth_page():
    st.markdown(
        "<div class='title-text'>ADAPTIVE PRICING SYSTEM</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='subtitle-text'>Experiment with prices, learn from demand, and converge to optimal pricing in real-time.</div>",
        unsafe_allow_html=True,
    )

    # Center card
    _, center, _ = st.columns([1, 1, 1])
    with center:
        st.markdown("<div class='card auth-card'>", unsafe_allow_html=True)
        st.markdown(
            "<div class='auth-title'>Dashboard Login</div>",
            unsafe_allow_html=True,
        )

        email = st.text_input(
            "",
            placeholder="EMAIL",
            label_visibility="collapsed",
            key="login_email",
        )
        password = st.text_input(
            "",
            placeholder="PASSWORD",
            type="password",
            label_visibility="collapsed",
            key="login_password",
        )
        login_clicked = st.button("LOGIN", use_container_width=True)

        if login_clicked:
            if email and password:
                try:
                    r = requests.post(
                        f"{API_BASE_URL}/auth/login",
                        json={"email": email, "password": password},
                    )
                    if r.status_code == 200:
                        data = r.json()
                        st.session_state.is_authenticated = True
                        st.session_state.user_email = data.get("email", email)
                        go_to("dashboard")
                        st.rerun()
                    else:
                        st.error("Login failed. Please check your credentials.")
                except Exception as e:
                    st.error(f"Error connecting to backend: {e}")
            else:
                st.error("Please enter both email and password.")

        st.markdown(
            "<div style='margin-top:10px;font-size:12px;text-align:center;color:#e5e7eb;'>Need an account?</div>",
            unsafe_allow_html=True,
        )
        if st.button("Create Account", use_container_width=True):
            st.session_state.show_register = True

        st.markdown("</div>", unsafe_allow_html=True)

    # ------- Registration --------
    if st.session_state.show_register:
        st.markdown("<div style='height:26px;'></div>", unsafe_allow_html=True)
        _, mid, _ = st.columns([1, 1, 1])
        with mid:
            st.markdown("<div class='card auth-card'>", unsafe_allow_html=True)
            st.markdown(
                "<div class='auth-title'>Create Account</div>",
                unsafe_allow_html=True,
            )

            reg_email = st.text_input(
                "",
                placeholder="EMAIL",
                label_visibility="collapsed",
                key="reg_email",
            )
            reg_password = st.text_input(
                "",
                placeholder="PASSWORD",
                type="password",
                label_visibility="collapsed",
                key="reg_password",
            )
            reg_confirm = st.text_input(
                "",
                placeholder="CONFIRM PASSWORD",
                type="password",
                label_visibility="collapsed",
                key="reg_confirm",
            )
            reg_submit = st.button("REGISTER", use_container_width=True)

            if reg_submit:
                if not reg_email or not reg_password:
                    st.error("Email and password are required.")
                elif reg_password != reg_confirm:
                    st.error("Passwords do not match.")
                else:
                    try:
                        r = requests.post(
                            f"{API_BASE_URL}/auth/register",
                            json={"email": reg_email, "password": reg_password},
                        )
                        if r.status_code in (200, 201):
                            st.success(
                                "Account created successfully. You can login now."
                            )
                            st.session_state.show_register = False
                        else:
                            st.error("Register failed. Please try again.")
                    except Exception:
                        st.error("Backend error. Please check your server.")

            st.markdown("</div>", unsafe_allow_html=True)


# -------------------------- DASHBOARD ------------------------------
def dashboard_page():
    projects = fetch_projects()

    st.markdown(
        "<div class='section-title'>Dashboard / Overview</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='section-subtitle'>High-level view of your ongoing pricing experiments and performance trends.</div>",
        unsafe_allow_html=True,
    )

    top = st.columns([1.1, 2])
    with top[0]:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown(
            "<div class='metric-label'>Total Projects</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='metric-value'>{len(projects)}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='metric-sub'>Projects currently tracked in your adaptive pricing engine.</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Simple synthetic chart (as in your original)
    with top[1]:
        dates = pd.date_range("2024-08-01", periods=10, freq="7D")
        line_one = (
            np.linspace(0.8, 2.0, len(dates))
            + np.random.uniform(-0.2, 0.2, len(dates))
        )
        df_chart = pd.DataFrame({"date": dates, "Revenue Index": line_one}).set_index(
            "date"
        )
        st.markdown(
            "<div style='font-size:13px;color:#e5e7eb;margin-bottom:4px;'>Revenue Trend (Synthetic)</div>",
            unsafe_allow_html=True,
        )
        st.line_chart(df_chart, height=260)


# --------------------- PRODUCT DETAILS PAGE ------------------------
def product_details_page():
    projects = fetch_projects()
    st.markdown(
        "<div class='section-title'>Products / Status</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='section-subtitle'>Inspect each experiment, current bandits, and the best-performing prices so far.</div>",
        unsafe_allow_html=True,
    )

    if not projects:
        st.info("No products yet. Add a product to start an experiment.")
        return

    container = st.container()
    with container:
        project_map = {p["project_id"]: p for p in projects}
        selected_id = st.selectbox(
            "Select Product",
            list(project_map.keys()),
            format_func=lambda pid: project_map[pid]["description"],
        )

        bandits = fetch_bandits_for_project(selected_id)
        if not bandits:
            st.warning("No bandits created yet for this product.")
            return

        best = max(bandits, key=lambda b: float(b["mean"]))
        best_price = to_float(best["price"])

        st.markdown(
            f"""
            <div class="card-plain" style="margin-top:10px;margin-bottom:18px;">
                <div style="display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap;">
                    <div>
                        <div style="font-size:12px;text-transform:uppercase;letter-spacing:0.12em;color:#9ca3af;">Optimal Price (Current Estimate)</div>
                        <div style="font-size:26px;font-weight:700;color:#f9fafb;margin-top:4px;">${best_price:.2f}</div>
                        <div style="font-size:12px;color:#9ca3af;margin-top:4px;">Based on Thompson Sampling posterior mean reward.</div>
                    </div>
                    <div class="chip">
                        <div class="chip-dot"></div>
                        <span>Active Bandits: {len(bandits)}</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        rows = [
            {
                "Price": to_float(b["price"]),
                "Trials": b["trial"],
                "Reward Sum": to_float(b["reward"]),
                "Mean Reward": to_float(b["mean"]),
            }
            for b in bandits
        ]
        st.markdown(
            "<div style='font-size:13px;color:#e5e7eb;margin-bottom:4px;'>Bandit Statistics</div>",
            unsafe_allow_html=True,
        )
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
                    st.error("Failed to run algorithm. Please check backend logs.")

        # ----- Plot & Simulation in SAME BLOCK -----
        with col2:
            if st.button("Show Posterior Plot", use_container_width=True):
                plot_url = f"{API_BASE_URL}/projects/{selected_id}/thompson/plot"

                try:
                    plot_response = requests.get(plot_url)

                    if plot_response.status_code == 200:
                        st.image(
                            plot_response.content,
                            caption="Posterior Distributions of Bandits",
                        )
                    else:
                        st.error(
                            f"Error fetching plot: {plot_response.text}"
                        )

                except Exception as e:
                    st.error(f"Could not load plot: {e}")

            if st.button(
                "Run Full Simulation (Updates Model)", use_container_width=True
            ):
                sim_res = requests.post(
                    f"{API_BASE_URL}/projects/{selected_id}/thompson/run",
                    json={"n_trials": 50},
                )
                if sim_res.status_code == 200:
                    st.success("Simulation finished! Try the plot again.")
                    st.rerun()
                else:
                    st.error(f"Error running simulation: {sim_res.text}")


# ------------------------- ADD PRODUCT -----------------------------
def add_product_page():
    st.markdown(
        "<div class='section-title'>Add New Product</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='section-subtitle'>Define a new pricing experiment by specifying a product and the candidate prices to test.</div>",
        unsafe_allow_html=True,
    )

    top_cols = st.columns([3, 1])
    with top_cols[1]:
        st.markdown("<div class='right-button'>", unsafe_allow_html=True)
        if st.button("Back to Dashboard", use_container_width=True):
            go_to("dashboard")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    with st.form("add_product_form"):
        st.markdown("<div class='card-plain'>", unsafe_allow_html=True)

        product_name = st.text_input(
            "",
            placeholder="PRODUCT NAME",
            label_visibility="collapsed",
        )
        price_variants_str = st.text_input(
            "",
            placeholder="ENTER PRICE VARIANTS TO TEST (e.g. 10, 15, 20)",
            label_visibility="collapsed",
        )

        st.markdown(
            "<div style='font-size:11px;color:#9ca3af;margin-top:8px;'>Provide at least one price. The system will create one bandit per price and initialize Thompson Sampling.</div>",
            unsafe_allow_html=True,
        )

        start_clicked = st.form_submit_button("START EXPERIMENT")

        st.markdown("</div>", unsafe_allow_html=True)

    if start_clicked:
        if not product_name:
            st.error("Product name is required.")
            return

        # Parse prices
        try:
            prices = [
                float(p.strip())
                for p in price_variants_str.split(",")
                if p.strip()
            ]
        except Exception:
            st.error("Invalid price format. Use comma-separated numeric values.")
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
        except Exception:
            st.error(f"Failed to create product: {r.text}")
            return

        st.success(f"Project created successfully! Project ID = {project_id}")

        # --------------------------
        # 2) CREATE BANDITS
        # --------------------------
        if not prices:
            prices = [0.0]

        created_bandits = 0
        for price in prices:
            rb = requests.post(
                f"{API_BASE_URL}/projects/{project_id}/bandits",
                json={"price": price},
            )
            if rb.status_code in (200, 201):
                created_bandits += 1

        st.success(f"Created {created_bandits} bandits successfully.")

        # --------------------------
        # 3) RUN ALGORITHM ONCE
        # --------------------------
        res = run_algorithm_for_project(project_id)
        if res and "price" in res:
            st.success(
                f"Thompson Sampling suggested starting price: ${float(res['price']):.2f}"
            )
        else:
            st.info("Project created. Waiting for reward data before convergence.")


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
