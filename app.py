import streamlit as st
import pandas as pd
import time
from database import create_table, insert_patient, get_all_patients
from ai_model import predict_risk
from utils import style_risk, speak_alert

st.set_page_config(page_title="Smart Hospital Dashboard", layout="wide")

# Load CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🏥 Smart Hospital Dashboard")

create_table()

menu = ["📊 Dashboard", "➕ Add Patient", "📋 Records"]
choice = st.sidebar.radio("Navigation", menu)

# ---------------- DASHBOARD ----------------
if choice == "📊 Dashboard":
    st.subheader("Real-Time Patient Monitoring")

    placeholder = st.empty()

    while True:
        data = get_all_patients()
        df = pd.DataFrame(data, columns=["ID","Name","Age","Heart Rate","Oxygen","Status"])

        with placeholder.container():
            if not df.empty:
                st.dataframe(df, use_container_width=True)

                col1, col2, col3 = st.columns(3)

                high = df[df["Status"] == "High Risk"].shape[0]
                medium = df[df["Status"] == "Medium Risk"].shape[0]
                low = df[df["Status"] == "Low Risk"].shape[0]

                col1.metric("🚨 High Risk", high)
                col2.metric("⚠ Medium Risk", medium)
                col3.metric("✅ Stable", low)

                # Alerts
                if high > 0:
                    st.error("🚨 High Risk Patient Detected!")
                    speak_alert("High risk patient detected")

                # Charts
                st.line_chart(df[["Heart Rate", "Oxygen"]])

            else:
                st.warning("No patient data available")

        time.sleep(5)
        st.experimental_rerun()

# ---------------- ADD PATIENT ----------------
elif choice == "➕ Add Patient":
    st.subheader("Add New Patient")

    with st.form("patient_form"):
        name = st.text_input("Patient Name")
        age = st.number_input("Age", 1, 120)
        hr = st.slider("Heart Rate", 40, 180, 80)
        oxygen = st.slider("Oxygen Level", 70, 100, 98)

        submitted = st.form_submit_button("Save")

        if submitted:
            status = predict_risk(hr, oxygen)
            insert_patient(name, age, hr, oxygen, status)
            st.success(f"Patient Added → {status}")

# ---------------- RECORDS ----------------
elif choice == "📋 Records":
    st.subheader("Patient Records")

    data = get_all_patients()
    df = pd.DataFrame(data, columns=["ID","Name","Age","Heart Rate","Oxygen","Status"])

    if not df.empty:
        df["Status"] = df["Status"].apply(style_risk)
        st.dataframe(df, use_container_width=True, unsafe_allow_html=True)
    else:
        st.info("No records found")
