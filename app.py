import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
from database import create_table, insert_patient, get_all_patients
from ai_model import predict_risk

st.set_page_config(page_title="Smart Hospital Dashboard", layout="wide")

# Load Google Font (Poppins)
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Load CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🏥 Smart Hospital Dashboard")

# Ensure DB exists
create_table()

# Add demo data if empty
if len(get_all_patients()) == 0:
    insert_patient("Demo Patient", 40, 110, 92, "Medium Risk")

# Sidebar Menu
menu = ["Dashboard", "Add Patient", "Records"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- DASHBOARD ----------------
if choice == "Dashboard":
    st.subheader("Patient Overview")

    data = get_all_patients()
    df = pd.DataFrame(data, columns=["ID","Name","Age","Heart Rate","Oxygen","Status","Time"])

    if not df.empty:
        col1, col2, col3 = st.columns(3)

        col1.metric("High Risk", df[df["Status"]=="High Risk"].shape[0])
        col2.metric("Medium Risk", df[df["Status"]=="Medium Risk"].shape[0])
        col3.metric("Low Risk", df[df["Status"]=="Low Risk"].shape[0])

        st.dataframe(df, use_container_width=True)
        st.line_chart(df[["Heart Rate","Oxygen"]])

    else:
        st.warning("No data available")

# ---------------- ADD PATIENT ----------------
elif choice == "Add Patient":
    st.subheader("Add Patient")

    name = st.text_input("Name")
    age = st.number_input("Age", 1, 120)
    hr = st.slider("Heart Rate", 40, 180)
    oxygen = st.slider("Oxygen Level", 70, 100)

    if st.button("Save"):
        status = predict_risk(hr, oxygen)
        insert_patient(name, age, hr, oxygen, status)
        st.success(f"Saved ({status})")

# ---------------- RECORDS ----------------
elif choice == "Records":
    st.subheader("All Records")

    data = get_all_patients()
    df = pd.DataFrame(data, columns=["ID","Name","Age","Heart Rate","Oxygen","Status","Time"])

    st.dataframe(df, use_container_width=True)
