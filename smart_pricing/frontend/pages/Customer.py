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

# Choose project automatically (first project)
def get_default_project():
    r = requests.get(f"{API_BASE}/projects")
    if r.status_code != 200 or len(r.json()) == 0:
        return None
    return r.json()[0]["project_id"]

PROJECT_ID = get_default_project()

if PROJECT_ID is None:
    st.error("No projects found. Ask admin to create one.")
    st.stop()

# Price loaded only once
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

st.title("Special Offer")
st.subheader(f"Today's Price: **${price:.2f}**")

# --- reward handler ---
def send_reward(value):
    requests.post(
        f"{API_BASE}/bandits/{bandit_id}/thompson/reward",
        json={"reward": value, "decision": "customer_click"}
    )
    st.info("Response saved. Refresh the page for a new price.")

col1, col2 = st.columns(2)

with col1:
    if st.button("Buy Now"):
        send_reward(1.0)

with col2:
    if st.button("Not Interested"):
        send_reward(0.0)

st.caption("Price updates only when the page is refreshed.")
