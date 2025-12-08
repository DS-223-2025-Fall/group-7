# frontend/app.py
import streamlit as st
import requests
import pandas as pd
import numpy as np
from typing import Optional
import os
import altair as alt
from scipy.stats import norm



# ==== CONFIG ====
API_BASE_URL = os.getenv("BACKEND_URL", "http://backend:8000")

# Convert backend static path → public URL
def make_public_image_url(path: str | None):
    if not path:
        return None
    # Streamlit UI loads from browser → needs localhost, not backend
    return f"http://localhost:8000{path}"

# ==== PAGE CONFIG ====
st.set_page_config(
    page_title="Smart Pricing System",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==== STYLES ====
st.markdown(
    """
    <style>
    :root {
        --bg-main: #020617;
        --bg-elevated: #020617;
        --bg-card: rgba(15,23,42,0.9);
        --bg-soft: rgba(15,23,42,0.6);
        --border-subtle: rgba(148,163,184,0.25);
        --border-strong: rgba(148,163,184,0.4);
        --accent: #4f46e5;
        --accent-soft: rgba(79,70,229,0.12);
        --accent-strong: #6366f1;
        --accent-muted: #818cf8;
        --success: #22c55e;
        --danger: #ef4444;
        --text-main: #e5e7eb;
        --text-soft: #9ca3af;
        --text-mute: #6b7280;
        --radius-lg: 18px;
        --radius-md: 12px;
        --radius-pill: 999px;
        --shadow-soft: 0 18px 45px rgba(15,23,42,0.75);
        --shadow-subtle: 0 10px 30px rgba(15,23,42,0.6);
        --shadow-pill: 0 12px 25px rgba(37,99,235,0.45);
    }

    /* App background */
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at top, rgba(79,70,229,0.35) 0, transparent 50%),
            radial-gradient(circle at bottom left, rgba(59,130,246,0.18) 0, transparent 45%),
            var(--bg-main);
        color: var(--text-main);
    }

    /* Main container */
    .main .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1180px;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020617, #020617);
        border-right: 1px solid rgba(15,23,42,0.9);
        box-shadow: 18px 0 45px rgba(15,23,42,0.85);
    }

    [data-testid="stSidebar"] > div {
        padding-top: 1rem;
    }

    .sidebar-header {
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--text-soft);
        margin-bottom: 0.2rem;
    }

    .sidebar-brand {
        font-size: 1.55rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--text-main);
        margin-bottom: 0.1rem;
    }

    .sidebar-sub {
        font-size: 0.78rem;
        color: var(--text-mute);
        margin-bottom: 1.3rem;
    }

    .sidebar-section-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        color: var(--text-mute);
        margin: 0.6rem 0 0.2rem 0.1rem;
    }

    /* Global buttons */
    .stButton > button {
        width: 100%;
        border-radius: var(--radius-pill);
        border: 1px solid rgba(148,163,184,0.2);
        padding: 0.55rem 0.9rem;
        font-size: 0.84rem;
        font-weight: 500;
        letter-spacing: 0.02em;
        background: linear-gradient(135deg, rgba(15,23,42,0.95), rgba(15,23,42,0.98));
        color: var(--text-main);
        transition: all 160ms ease-out;
        box-shadow: 0 0 0 rgba(37,99,235,0);
    }

    .stButton > button:hover {
        border-color: var(--accent-muted);
        background: radial-gradient(circle at top left, rgba(79,70,229,0.16), rgba(15,23,42,0.98));
        box-shadow: 0 10px 27px rgba(15,23,42,0.9);
        transform: translateY(-1px);
    }

    .stButton > button:focus {
        outline: none;
        box-shadow: 0 0 0 1px var(--accent-muted);
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--accent), var(--accent-strong));
        border-color: transparent;
        color: #f9fafb;
        box-shadow: var(--shadow-pill);
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, var(--accent-strong), #7c3aed);
        box-shadow: 0 12px 30px rgba(79,70,229,0.55);
    }

    /* Inputs */
    .stTextInput > div > div > input,
    .stNumberInput input {
        background-color: rgba(15,23,42,0.9);
        border-radius: 10px;
        border: 1px solid rgba(148,163,184,0.35);
        color: var(--text-main);
        font-size: 0.88rem;
    }

    .stTextInput > label,
    .stNumberInput > label,
    .stFileUploader > label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: var(--text-soft);
    }

    .stFileUploader > div {
        background-color: rgba(15,23,42,0.9);
        border-radius: 12px;
        border: 1px dashed rgba(148,163,184,0.45);
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border-radius: var(--radius-lg);
        overflow: hidden;
        box-shadow: var(--shadow-subtle);
    }

    /* Headings */
    .page-header {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        margin-bottom: 1.2rem;
        gap: 1.1rem;
    }

    .page-title {
        font-size: 1.75rem;
        font-weight: 650;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        margin-bottom: 0.2rem;
    }

    .page-subtitle {
        font-size: 0.9rem;
        color: var(--text-soft);
    }

    .page-pill {
        font-size: 0.72rem;
        border-radius: 999px;
        padding: 0.2rem 0.7rem;
        background: rgba(15,23,42,0.8);
        border: 1px solid rgba(148,163,184,0.28);
        color: var(--text-soft);
        text-transform: uppercase;
        letter-spacing: 0.18em;
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
    }

    .page-pill-dot {
        width: 8px;
        height: 8px;
        border-radius: 999px;
        background: var(--accent-muted);
        box-shadow: 0 0 0 3px rgba(129,140,248,0.28);
    }

    .section-title {
        margin-top: 0.2rem;
        margin-bottom: 0.6rem;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        color: var(--text-mute);
    }

    /* Cards */
    .surface-card {
        background: linear-gradient(145deg, rgba(15,23,42,0.96), rgba(15,23,42,0.9));
        border-radius: var(--radius-lg);
        border: 1px solid var(--border-subtle);
        box-shadow: var(--shadow-soft);
        padding: 1.1rem 1.15rem;
        position: relative;
        overflow: hidden;
    }

    .surface-card::before {
        content: "";
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at top right, rgba(79,70,229,0.18), transparent 60%);
        opacity: 0.9;
        pointer-events: none;
    }

    .surface-card-inner {
        position: relative;
        z-index: 1;
    }

    .surface-soft {
        background: rgba(15,23,42,0.8);
        border-radius: var(--radius-md);
        border: 1px solid rgba(148,163,184,0.28);
        padding: 0.9rem 1rem;
    }

    /* Metric chips */
    .metric-card {
        background: linear-gradient(135deg, rgba(37,99,235,0.95), rgba(79,70,229,1));
        padding: 10px 12px;
        border-radius: 14px;
        color: #f9fafb;
        box-shadow: 0 14px 32px rgba(37,99,235,0.52);
        border: 1px solid rgba(191,219,254,0.35);
    }
    .metric-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        color: #e0f2fe;
        letter-spacing: 0.16em;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 1.1rem;
        font-weight: 650;
    }

    .metric-tag {
        font-size: 0.7rem;
        padding: 0.15rem 0.55rem;
        border-radius: var(--radius-pill);
        background: rgba(15,23,42,0.8);
        border: 1px solid rgba(148,163,184,0.28);
        color: var(--text-soft);
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        margin-top: 0.35rem;
    }

    .metric-tag-dot {
        width: 7px;
        height: 7px;
        border-radius: 999px;
        background: rgba(34,197,94,0.9);
    }

    /* Product card */
    .product-card {
        background: rgba(15,23,42,0.95);
        border-radius: 16px;
        border: 1px solid rgba(148,163,184,0.27);
        padding: 0.9rem 1rem;
        margin-bottom: 0.85rem;
        box-shadow: 0 14px 32px rgba(15,23,42,0.85);
        position: relative;
        overflow: hidden;
    }

    .product-card::before {
        content: "";
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at top left, rgba(79,70,229,0.25), transparent 60%);
        opacity: 0.85;
        pointer-events: none;
    }

    .product-card-inner {
        position: relative;
        z-index: 1;
    }

    .product-title {
        font-size: 1.05rem;
        font-weight: 600;
        margin-bottom: 0.15rem;
    }

    .product-sub {
        font-size: 0.8rem;
        color: var(--text-soft);
    }

    .product-image-placeholder {
        width: 150px;
        height: 150px;
        border-radius: 16px;
        border: 1px dashed rgba(148,163,184,0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.78rem;
        color: var(--text-soft);
        background: rgba(15,23,42,0.8);
    }

    .product-meta-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        color: var(--text-mute);
        margin-bottom: 0.1rem;
    }

    .product-meta-value {
        font-size: 0.84rem;
        color: var(--text-soft);
    }

    /* Divider */
    .divider-soft {
        border-top: 1px solid rgba(148,163,184,0.2);
        margin: 0.8rem 0 1.2rem 0;
    }

    /* Alert tweaks */
    .stAlert {
        border-radius: 12px;
        background: rgba(15,23,42,0.9);
        border: 1px solid rgba(148,163,184,0.4);
    }

    /* Code in sidebar */
    .sidebar-api {
        font-size: 0.72rem !important;
        border-radius: 10px !important;
        background: rgba(15,23,42,0.95) !important;
        border: 1px solid rgba(148,163,184,0.35) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==== SESSION STATE ====
if "page" not in st.session_state:
    st.session_state.page = "customer"

if "current_project_id" not in st.session_state:
    st.session_state.current_project_id = None

if "current_bandit_id" not in st.session_state:
    st.session_state.current_bandit_id = None

if "last_price" not in st.session_state:
    st.session_state.last_price = None

if "customer_offers" not in st.session_state:
    st.session_state.customer_offers = {}

if "customer_refresh" not in st.session_state:
    st.session_state.customer_refresh = True


# ==== API SAFE REQUEST WRAPPER ====
def _safe_request(method: str, url: str, **kwargs) -> Optional[requests.Response]:
    try:
        return requests.request(method, url, timeout=5, **kwargs)
    except requests.RequestException as e:
        st.error(f"Network error calling {url}: {e}")
        return None


# ==== API HELPERS ====
def fetch_projects():
    r = _safe_request("GET", f"{API_BASE_URL}/projects")
    return r.json() if r and r.status_code == 200 else []


def create_project(description: str, number_bandits: int, price: float):
    payload = {"description": description, "number_bandits": number_bandits, "price": price}
    r = _safe_request("POST", f"{API_BASE_URL}/projects", json=payload)
    return r.json() if r and r.status_code in (200, 201) else None


def create_bandit(project_id: int, price: float):
    r = _safe_request("POST", f"{API_BASE_URL}/projects/{project_id}/bandits", json={"price": price})
    return r.json() if r and r.status_code in (200, 201) else None


def fetch_bandits(project_id: int):
    r = _safe_request("GET", f"{API_BASE_URL}/projects/{project_id}/bandits")
    return r.json() if r and r.status_code == 200 else []


def thompson_select(project_id: int):
    r = _safe_request("POST", f"{API_BASE_URL}/projects/{project_id}/thompson/select")
    return r.json() if r and r.status_code == 200 else None


def submit_reward(bandit_id: int, reward: float, decision: str):
    r = _safe_request(
        "POST",
        f"{API_BASE_URL}/bandits/{bandit_id}/thompson/reward",
        json={"reward": float(reward), "decision": decision},
    )
    if not r:
        st.error("Reward request failed (network).")
        return None
    if r.status_code != 200:
        st.error(f"Reward request failed: {r.status_code} {r.text}")
        return None
    res = r.json()
    st.write("Debug reward response:", res)  # TEMP: to see it in the UI
    return res


def fetch_posterior_plot(project_id: int):
    r = _safe_request("GET", f"{API_BASE_URL}/projects/{project_id}/thompson/plot")
    return r.content if r and r.status_code == 200 else None


# ==== SIDEBAR NAVIGATION ====
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">Smart Pricing</div>
        <div class="sidebar-sub">Adaptive experiments for retail pricing.</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-section-label">Workspace</div>', unsafe_allow_html=True)
    if st.button("Customer View"):
        st.session_state.page = "customer"

    if st.button("New Product (Admin)"):
        st.session_state.page = "add"

    if st.button("Experiment (Admin)"):
        st.session_state.page = "experiment"

    st.markdown("---")

    st.markdown('<div class="sidebar-section-label">Backend URL</div>', unsafe_allow_html=True)
    st.sidebar.code(API_BASE_URL, line_numbers=False)
    st.markdown(
        '<p style="font-size:0.7rem;color:#6b7280;margin-top:0.35rem;">All requests are sent directly from this UI to the configured backend.</p>',
        unsafe_allow_html=True,
    )


# ======================================================
#                ADD PRODUCT PAGE
# ======================================================
def add_product_page():
    st.markdown(
        """
        <div class="page-header">
            <div>
                <div class="page-title">New Product</div>
                <div class="page-subtitle">
                    Define a product, upload an image, and configure price variants to start a new experiment.
                </div>
            </div>
            <div class="page-pill">
                <span class="page-pill-dot"></span>
                <span>Admin • Setup</span>
            </div>
        </div>
        <div class="divider-soft"></div>
        """,
        unsafe_allow_html=True,
    )

    col_main, col_side = st.columns([2.1, 1])

    with col_main:
        st.markdown('<div class="section-title">Product configuration</div>', unsafe_allow_html=True)
        st.markdown('<div class="surface-card"><div class="surface-card-inner">', unsafe_allow_html=True)

        with st.form("create_product"):
            description = st.text_input("Product name")
            prices_str = st.text_input("Price variants (comma separated)")
            initial_price = st.number_input("Initial price", min_value=0.0, value=10.0)
            uploaded_image = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])
            st.markdown(
                """
                <div style="font-size:0.76rem;color:#9ca3af;margin-top:0.45rem;">
                    Use <strong>comma separated values</strong> for price variants. Each value will become a bandit arm.
                </div>
                """,
                unsafe_allow_html=True,
            )
            submitted = st.form_submit_button("Create product and bandits")

        st.markdown("</div></div>", unsafe_allow_html=True)

    with col_side:
        st.markdown('<div class="section-title">How it works</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="surface-soft" style="font-size:0.8rem;color:#9ca3af;">
                <ol style="padding-left:1.1rem;margin:0;">
                    <li style="margin-bottom:0.4rem;">
                        Provide a <strong>name</strong> for your product.
                    </li>
                    <li style="margin-bottom:0.4rem;">
                        Add one or more <strong>price variants</strong>. Each price defines a separate policy.
                    </li>
                    <li style="margin-bottom:0.4rem;">
                        Optionally <strong>upload an image</strong> to improve the customer view.
                    </li>
                    <li>
                        The system automatically creates a project and bandits for Thompson sampling.
                    </li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if not submitted:
        return

    if not description:
        st.error("Product name is required.")
        return

    # Parse prices
    if prices_str:
        try:
            prices = [float(x.strip()) for x in prices_str.split(",") if x.strip()]
        except Exception:
            st.error("Invalid price list.")
            return
    else:
        prices = [float(initial_price)]

    proj = create_project(description, len(prices), prices[0])
    if not proj or "project_id" not in proj:
        st.error("Could not create project.")
        return

    pid = proj["project_id"]

    # Upload image
    if uploaded_image:
        files = {"file": (uploaded_image.name, uploaded_image, uploaded_image.type)}
        _safe_request("POST", f"{API_BASE_URL}/projects/{pid}/upload-image", files=files)

    # Create bandits
    for p in prices:
        create_bandit(pid, p)

    st.session_state.current_project_id = pid
    st.session_state.page = "experiment"
    st.rerun()


# ======================================================
#                EXPERIMENT PAGE
# ======================================================
def experiment_page():
    st.markdown(
        """
        <div class="page-header">
            <div>
                <div class="page-title">Experiment Console</div>
                <div class="page-subtitle">
                    Monitor bandit performance and manually trigger Thompson sampling decisions.
                </div>
            </div>
            <div class="page-pill">
                <span class="page-pill-dot"></span>
                <span>Admin • Live experiment</span>
            </div>
        </div>
        <div class="divider-soft"></div>
        """,
        unsafe_allow_html=True,
    )

    pid = st.session_state.current_project_id
    if not pid:
        projs = fetch_projects()
        if not projs:
            st.info("No projects found.")
            return

        st.markdown('<div class="section-title">Project selection</div>', unsafe_allow_html=True)
        with st.container():
            col_left, col_right = st.columns([2, 1])
            with col_left:
                pid = st.selectbox("Choose a project", [p["project_id"] for p in projs])
            with col_right:
                st.markdown("<div style='height:1.6rem;'></div>", unsafe_allow_html=True)
                if st.button("Load selected project", type="primary"):
                    st.session_state.current_project_id = pid
                    st.rerun()
        return

    bandits = fetch_bandits(pid)

    if bandits:
        df = pd.DataFrame(
            [
                {
                    "bandit_id": b["bandit_id"],
                    "price": float(b["price"]),
                    "mean": float(b["mean"]),
                    "variance": float(b["variance"]),
                    "reward_sum": float(b["reward"]),
                    "trials": int(b["trial"]),
                }
                for b in bandits
            ]
        )

        # Bandit table
        st.markdown('<div class="section-title">Bandit state</div>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
            

        # ===== SUMMARY KPIs =====
        total_trials = int(df["trials"].sum())
        total_reward = float(df["reward_sum"].sum())
        conversion_rate = total_reward / total_trials if total_trials > 0 else 0

        best_idx = df["mean"].idxmax()
        best_price = df.loc[best_idx, "price"]
        best_mean = df.loc[best_idx, "mean"]

        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

        with kpi_col1:
            st.metric("Total Trials", total_trials)

        with kpi_col2:
            st.metric("Total Reward", f"{total_reward:.0f}")

        with kpi_col3:
            st.metric("Conversion Rate", f"{conversion_rate:.2%}")

        with kpi_col4:
            st.metric("Best Price (by expected reward)", f"${best_price:.2f}", f"{best_mean:.3f}")

        # ===== BANDIT COMPARISON CHART =====
        st.subheader("Bandit Performance Comparison")

        comparison_df = df[["price", "mean", "trials"]]
        st.bar_chart(
            comparison_df.set_index("price")[["mean"]],
            use_container_width=True,
        )

        # ===== TIME-SERIES PERFORMANCE CHART =====
        st.subheader("Performance Over Time (Cumulative Trials)")

        # Create a simple timeline (index = trial number)
        if total_trials > 0:
            timeline_df = pd.DataFrame(
                {
                    "trial": np.arange(1, total_trials + 1),
                    "conversion": [1] * int(total_reward) + [0] * (total_trials - int(total_reward)),
                }
            )
            # Rolling conversion rate for smoothness
            timeline_df["rolling_rate"] = timeline_df["conversion"].rolling(20, min_periods=1).mean()

            st.line_chart(
                timeline_df.set_index("trial")[["rolling_rate"]],
                use_container_width=True,
            )
    else:
        st.info("No bandits found for this project.")
    # ==== POSTERIOR DISTRIBUTIONS (NATIVE STREAMLIT PLOT) ====
    st.subheader("Posterior Distributions (Thompson Sampling)")

    if not df.empty:
        bandit_curves = []

        # Build Gaussian posterior curves for each bandit
        for _, row in df.iterrows():
            mean = float(row["mean"])
            var = float(row["variance"])
            std = max(var, 1e-6) ** 0.5
            price = float(row["price"])
            bandit_id = int(row["bandit_id"])

            xs = np.linspace(mean - 4 * std, mean + 4 * std, 200)

            for x in xs:
                bandit_curves.append({
                    "x": x,
                    "density": norm.pdf(x, mean, std),
                    "bandit": f"Bandit {bandit_id} | price={price}"
                })

        chart_df = pd.DataFrame(bandit_curves)

        posterior_chart = (
            alt.Chart(chart_df)
            .mark_line()
            .encode(
                x=alt.X("x:Q", title="Expected Reward"),
                y=alt.Y("density:Q", title="Density"),
                color=alt.Color("bandit:N", title="Bandit"),
                tooltip=["bandit", "x", "density"]
            )
            .properties(
                height=350,
                width="container"
            )
            .interactive()
        )

        st.altair_chart(posterior_chart, use_container_width=True)

    else:
        st.info("No bandits available for posterior plot.")



    # ===== CONTROL SECTION =====
    st.markdown('<div class="section-title">Control</div>', unsafe_allow_html=True)
    control_col_left, control_col_right = st.columns([1.5, 1])

    with control_col_left:
        st.markdown('<div class="surface-soft">', unsafe_allow_html=True)
        st.markdown(
            """
            <div style="font-size:0.78rem;color:#9ca3af;margin-bottom:0.35rem;">
                Trigger a Thompson sampling step. The selected price will also be reflected in the customer-facing shop.
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Sample price using Thompson", type="primary"):
            r = thompson_select(pid)
            if r:
                st.success(f"Selected price ${float(r['price']):.2f}")
                st.session_state.current_bandit_id = r["bandit_id"]
                st.session_state.last_price = float(r["price"])
                st.session_state.customer_refresh = True
        st.markdown("</div>", unsafe_allow_html=True)


    # ===== MANUAL OUTCOMES =====
    st.markdown('<div class="section-title">Manual outcomes</div>', unsafe_allow_html=True)
    colA, colB = st.columns(2)

    with colA:
        st.markdown('<div class="surface-soft">', unsafe_allow_html=True)
        st.markdown(
            "<div style='font-size:0.8rem;color:#9ca3af;margin-bottom:0.35rem;'>Record a successful purchase for the currently selected bandit.</div>",
            unsafe_allow_html=True,
        )
        if st.button("Record buy (admin)", type="primary"):
            submit_reward(pid, 1.0, "buy_admin")
            st.session_state.customer_refresh = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with colB:
        st.markdown('<div class="surface-soft">', unsafe_allow_html=True)
        st.markdown(
            "<div style='font-size:0.8rem;color:#9ca3af;margin-bottom:0.35rem;'>Record a non-purchase for the currently selected bandit.</div>",
            unsafe_allow_html=True,
        )
        if st.button("Record no-buy (admin)"):
            submit_reward(pid, 0.0, "no_buy_admin")
            st.session_state.customer_refresh = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ===== EXPLANATORY TEXT =====
    st.markdown(
        """
        ### How to Interpret These Analytics

        **Summary KPIs** give a quick overview of experiment health:
        - *Total Trials* shows sample size.
        - *Conversion Rate* helps measure customer interest.
        - *Best Price* reflects the bandit with the highest expected reward.

        **Bandit Performance Comparison** visualizes which price performs best at the moment.

        **Performance Over Time** shows whether learning is stabilizing or drifting.

        Together, these analytics support clearer and faster decisions about pricing experiments.
        """
    )


# ======================================================
#                CUSTOMER PAGE
# ======================================================
def customer_page():
    st.markdown(
        """
        <div class="page-header">
            <div>
                <div class="page-title">Shop</div>
                <div class="page-subtitle">
                    Explore the catalog. Each price you see is generated by a live pricing experiment.
                </div>
            </div>
            <div class="page-pill">
                <span class="page-pill-dot"></span>
                <span>Customer • Live pricing</span>
            </div>
        </div>
        <div class="divider-soft"></div>
        """,
        unsafe_allow_html=True,
    )

    projects = fetch_projects()
    if not projects:
        st.info("No products available.")
        return

    top_bar_left, top_bar_right = st.columns([1.5, 2])
    with top_bar_left:
        if st.button("Refresh prices", type="primary"):
            st.session_state.customer_refresh = True

    with top_bar_right:
        st.markdown(
            """
            <div style="font-size:0.78rem;color:#9ca3af;margin-top:0.35rem;">
                Prices are personalized per refresh using Thompson sampling over observed purchase behavior.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Refresh Thompson samples
    if st.session_state.customer_refresh:
        offers = {}
        for p in projects:
            pid = p["project_id"]
            r = thompson_select(pid)
            if r:
                offers[pid] = {
                    "bandit_id": r["bandit_id"],
                    "price": float(r["price"]),
                }
        st.session_state.customer_offers = offers
        st.session_state.customer_refresh = False

    offers = st.session_state.customer_offers

    st.markdown('<div class="section-title">Products</div>', unsafe_allow_html=True)

    # --- DISPLAY PRODUCTS ---
    for p in projects:
        pid = p["project_id"]
        pname = p["description"]

        img_url = make_public_image_url(p.get("image_path"))

        offer = offers.get(pid)
        if not offer:
            continue

        price = offer["price"]
        bid = offer["bandit_id"]

        st.markdown('<div class="product-card"><div class="product-card-inner">', unsafe_allow_html=True)

        cols = st.columns([1.4, 2.4, 1.2, 1.2])

        # IMAGE
        with cols[0]:
            if img_url:
                st.image(img_url, width=150)
            else:
                st.markdown(
                    "<div class='product-image-placeholder'>No image available</div>",
                    unsafe_allow_html=True,
                )

        # NAME + CONTEXT
        with cols[1]:
            st.markdown(f"<div class='product-title'>{pname}</div>", unsafe_allow_html=True)
            st.markdown(
                "<div class='product-sub'>This product is currently part of a live pricing experiment.</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                """
                <div style="margin-top:0.6rem;">
                    <div class="product-meta-label">Experiment note</div>
                    <div class="product-meta-value">
                        The price you see is sampled from a probabilistic model that learns from aggregated customer decisions.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # PRICE CARD
        with cols[2]:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Current price</div>
                    <div class="metric-value">${price:.2f}</div>
                    <div class="metric-tag">
                        <span class="metric-tag-dot"></span>
                        <span>Adaptive offer</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # ACTIONS
        with cols[3]:
            st.markdown(
                "<div style='display:flex;flex-direction:column;gap:0.4rem;margin-top:0.2rem;'>",
                unsafe_allow_html=True,
            )
            if st.button("Buy now", key=f"buy_{pid}", type="primary"):
                submit_reward(bid, 1.0, "buy_customer")
                st.session_state.customer_refresh = True
                st.rerun()

            if st.button("Not now", key=f"nobuy_{pid}"):
                submit_reward(bid, 0.0, "no_buy_customer")
                st.session_state.customer_refresh = True
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)


# ==== MAIN ROUTER ====
st.markdown("<div class='divider-soft'></div>", unsafe_allow_html=True)

if st.session_state.page == "add":
    add_product_page()
elif st.session_state.page == "experiment":
    experiment_page()
else:
    customer_page()
