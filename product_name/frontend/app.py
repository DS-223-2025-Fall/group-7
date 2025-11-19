import streamlit as st
import pandas as pd

# --------- GLOBAL STYLE ---------
st.set_page_config(layout="wide", page_title="Adaptive Pricing System")

st.markdown(
    """
    <style>
        /* Page background */
        body {
            background-color: #7986CB;
        }
        .main {
            background-color: #7986CB;
            min-height: 100vh;
            overflow-y: auto;
            padding-top: 20px;
            padding-bottom: 50px;
        }

        /* Title */
        .title-text {
            font-size: 42px;
            font-weight: bold;
            text-align: center;
            color: white;
            margin-top: 40px;
        }

        /* Login box */
        .login-box {
            background-color: rgba(255,255,255,0.15);
            padding: 40px;
            border-radius: 10px;
            width: 380px;
            margin: auto;
            margin-top: 40px;
        }
        label, input {
            color: white !important;
        }

        /* Dashboard title */
        .dashboard-title {
            font-size: 38px;
            font-weight: bold;
            color: white;
            margin-bottom: 20px;
        }

        /* Card styling */
        .card {
            background-color: rgba(0,0,0,0.15);
            padding: 25px;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 20px;
        }
        .card h3 {
            margin: 0;
            padding: 0;
            font-size: 20px;
        }
        .card p {
            font-size: 26px;
            font-weight: bold;
        }

        /* Section titles */
        .section-title {
            color: white;
            font-size: 22px;
            margin-top: 20px;
            margin-bottom: 10px;
        }

        /* Table styling override */
        .stDataFrame table {
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- PAGE SELECTOR ----------------
page = st.sidebar.selectbox("Navigate", ["Login", "Dashboard", "Product Status"])

# ---------------- LOGIN PAGE ----------------
if page == "Login":
    st.markdown('<div class="title-text">ADAPTIVE PRICING SYSTEM</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("LOGIN", use_container_width=True)
    st.write("<div style='text-align:center;color:white;margin-top:10px;'>Forgot password?</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- DASHBOARD PAGE ----------------
elif page == "Dashboard":
    st.markdown('<div class="dashboard-title">DASHBOARD / OVERVIEW</div>', unsafe_allow_html=True)

    c1, c2, c3, _ = st.columns([1,1,1,0.3])
    with c1:
        st.markdown('<div class="card"><h3>TOTAL REVENUE</h3><p>$ 77,777</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><h3>AVERAGE CONVERSION</h3><p>22%</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="card"><h3>REGRET MINIMIZATION</h3><p>5%</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Active Experiments Table</div>', unsafe_allow_html=True)
    df_active = pd.DataFrame({
        "Product Name": [],
        "Current Best Price": [],
        "Conversion Rate": [],
        "Revenue": [],
        "Status": []
    })
    st.dataframe(df_active, height=300)

    st.markdown('<div class="section-title">Revenue And Trend Over Time</div>', unsafe_allow_html=True)
    st.line_chart({"Line One":[1,2,1.5,2.2,1.8],"Line Two":[0.8,1.4,1.2,1.3,0.6]})

# ---------------- PRODUCT STATUS PAGE ----------------
elif page == "Product Status":
    st.markdown('<div class="dashboard-title">PRODUCT NAME / STATUS</div>', unsafe_allow_html=True)
    st.markdown('<div class="card" style="width:300px;">OPTIMAL PRICE (SO FAR)<br><p>$25</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Active Experiments Table</div>', unsafe_allow_html=True)
    df_product = pd.DataFrame({
        "Price Variant": [],
        "Impressions": [],
        "Conversion Rate": [],
        "Revenue": [],
        "Allocated Traffic": []
    })
    st.dataframe(df_product, height=300)

    colA, colB = st.columns([1,1])
    with colA:
        st.write("Last updated: 2 minutes ago")
        st.write("Algorithm: Thompson Sampling (Bernoulli)")
        st.write("Next update scheduled: In 10 minutes")
    with colB:
        st.write("Algorithm Insights:")
        st.write("• Thompson Sampling currently favors Price $12 with 45% traffic.")
        st.write("• Estimated regret reduced by 18% compared to static A/B testing.")
        st.write("• Model confidence: 87%.")

    st.button("Run Algorithm")
    st.button("Pause Test")
