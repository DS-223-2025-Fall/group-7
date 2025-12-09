import streamlit as st
import requests
import os

API_BASE = os.getenv("BACKEND_URL", "http://backend:8000")

# Hide sidebar
st.markdown("""
<style>
[data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Special Offer", layout="centered")


# --------------------------
#  LOGIC (UNCHANGED)
# --------------------------

def get_default_project():
    r = requests.get(f"{API_BASE}/projects")
    if r.status_code != 200 or len(r.json()) == 0:
        return None
    return r.json()[0]["project_id"]

PROJECT_ID = get_default_project()

if PROJECT_ID is None:
    st.error("No projects found. Ask admin to create one.")
    st.stop()

# Load price once
if "offer" not in st.session_state:
    r = requests.post(f"{API_BASE}/projects/{PROJECT_ID}/thompson/select")
    if r.status_code == 200:
        st.session_state.offer = r.json()
    else:
        st.error("Backend returned no price.")
        st.stop()

offer = st.session_state.offer
bandit_id = offer["bandit_id"]
price = float(offer["price"])


# --------------------------
#  FETCH PROJECT TO SHOW IMAGE
# --------------------------

def make_public_image_url(path: str | None):
    if not path:
        return None
    return f"http://localhost:8000{path}"

def fetch_project(pid):
    r = requests.get(f"{API_BASE}/projects/{pid}")
    if r.status_code != 200:
        return None
    return r.json()

project_data = fetch_project(PROJECT_ID)
product_image = make_public_image_url(project_data.get("image_path")) if project_data else None


# --------------------------
#  HEADER + QUESTION
# --------------------------
st.markdown(
    """
    <div style='text-align:center; margin-top:1rem;'>
        <h1 style='color:var(--text-main); margin-bottom:0.4rem;'>Special Offer</h1>
        <p style='color:var(--text-soft); font-size:1rem;'>Do you want to buy this product?</p>
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------
#  IMAGE (CENTERED PROPERLY)
# --------------------------
if product_image:
    st.markdown(
        f"""
        <div style="
            display:flex;
            justify-content:center;
            width:100%;
            margin-top:0.5rem;
            margin-bottom:1rem;
        ">
            <img src="{product_image}" style="width:200px; border-radius:10px;">
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------
#  PRICE DISPLAY (CENTERED)
# --------------------------
st.markdown(
    f"""
    <div style='text-align:center; margin-top:0.5rem; margin-bottom:0.8rem;'>
        <span style='color:var(--accent-strong); font-size:2rem; font-weight:700;'>
            ${price:.2f}
        </span>
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------
#  REWARD HANDLER (UNCHANGED)
# --------------------------

def send_reward(value):
    requests.post(
        f"{API_BASE}/bandits/{bandit_id}/thompson/reward",
        json={"reward": value, "decision": "customer_click"}
    )
    st.info("Response saved. Refresh the page for a new price.")


# --------------------------
#  BUTTONS (CENTERED + THEMED)
# --------------------------

st.markdown(
    """
    <style>
    .btn-row button {
        padding: 0.6rem 1.3rem !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
    }

    .btn-buy button {
        background: var(--accent-strong) !important;
        color: green !important;
        border: none !important;
    }

    .btn-skip button {
        background: rgba(148,163,184,0.25) !important;
        color: var(--text-main) !important;
        border: 1px solid rgba(148,163,184,0.35) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

center = st.container()
with center:
    a, b, c = st.columns([1,2,1])  # Center column is wider
    with b:
        col1, col2 = st.columns([1,1])

        with col1:
            st.markdown("<div class='btn-row btn-buy'>", unsafe_allow_html=True)
            if st.button("Buy Now"):
                send_reward(price)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='btn-row btn-skip'>", unsafe_allow_html=True)
            if st.button("Not Interested"):
                send_reward(0.0)
            st.markdown("</div>", unsafe_allow_html=True)


# --------------------------
#  FOOTER NOTE
# --------------------------
st.markdown(
    "<p style='text-align:center; margin-top:1rem; color:var(--text-mute);'>"
    "Price updates only when the page is refreshed."
    "</p>",
    unsafe_allow_html=True
)
