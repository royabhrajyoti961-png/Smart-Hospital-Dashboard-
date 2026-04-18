import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
from database import create_table, insert_patient, get_all_patients
from ai_model import predict_risk

st.set_page_config(page_title="Smart Hospital", layout="wide")

# 🍎 Apple UI Styling
st.markdown("""
<style>

/* Apple Font Stack */
html, body, [class*="css"], [class*="st-"] {
    font-family: -apple-system, BlinkMacSystemFont,
                 "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    background-color: #f5f5f7;
}

/* Header */
h1 {
    font-weight: 600;
    letter-spacing: -0.5px;
}

/* Sidebar Blur */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(20px);
}

/* Cards */
.card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
}

/* Buttons */
button {
    border-radius: 12px !important;
    background: black !important;
    color: white !important;
    border: none !important;
}

/* Inputs */
input, textarea {
    border-radius: 10px !important;
}

/* Table */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* Metrics */
.stMetric {
    background: white;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

st.title("🏥 Smart Hospital Dashboard")

create_table()

# Auto demo data
if len(get_all_patients()) == 0:
    insert_patient("Demo Patient", 40, 110, 92, "Medium Risk")

menu = ["Dashboard", "Add Patient", "Records"]
choice = st.sidebar.radio("Menu", menu)

# ---------------- DASHBOARD ----------------
if choice == "Dashboard":
    st.subheader("Overview")

    data = get_all_patients()
    df = pd.DataFrame(data, columns=["ID","Name","Age","Heart Rate","Oxygen","Status","Time"])

    if not df.empty:
        col1, col2, col3 = st.columns(3)

        high = df[df["Status"]=="High Risk"].shape[0]
        medium = df[df["Status"]=="Medium Risk"].shape[0]
        low = df[df["Status"]=="Low Risk"].shape[0]

        col1.metric("🚨 High Risk", high)
        col2.metric("⚠ Medium", medium)
        col3.metric("✅ Stable", low)

        st.markdown("### Patient Data")
        st.dataframe(df, use_container_width=True)

        st.markdown("### Trends")
        st.line_chart(df[["Heart Rate","Oxygen"]])

    else:
        st.warning("No data available")

# ---------------- ADD PATIENT ----------------
elif choice == "Add Patient":
    st.subheader("Add Patient")

    with st.form("form"):
        name = st.text_input("Name")
        age = st.number_input("Age", 1, 120)
        hr = st.slider("Heart Rate", 40, 180)
        oxygen = st.slider("Oxygen", 70, 100)

        submit = st.form_submit_button("Save")

        if submit:
            status = predict_risk(hr, oxygen)
            insert_patient(name, age, hr, oxygen, status)
            st.success(f"Saved ({status})")

# ---------------- RECORDS ----------------
elif choice == "Records":
    st.subheader("All Records")

    data = get_all_patients()
    df = pd.DataFrame(data, columns=["ID","Name","Age","Heart Rate","Oxygen","Status","Time"])

    st.dataframe(df, use_container_width=True)
