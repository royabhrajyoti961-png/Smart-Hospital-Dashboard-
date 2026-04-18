import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
from database import create_table, insert_patient, get_all_patients
from ai_model import predict_risk

st.set_page_config(page_title="Smart Hospital Dashboard", layout="wide")

st.title("🏥 Smart Hospital Dashboard")

# Ensure DB exists
create_table()

# Auto demo data (only once)
if len(get_all_patients()) == 0:
    insert_patient("Demo Patient", 40, 110, 92, "Medium Risk")

menu = ["Dashboard", "Add Patient", "Records"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Dashboard":
    data = get_all_patients()
    df = pd.DataFrame(data, columns=["ID","Name","Age","Heart Rate","Oxygen","Status","Created"])

    st.subheader("Live Dashboard")

    if not df.empty:
        st.dataframe(df)

        st.metric("High Risk", df[df["Status"]=="High Risk"].shape[0])
        st.line_chart(df[["Heart Rate","Oxygen"]])
    else:
        st.warning("No data")

elif choice == "Add Patient":
    name = st.text_input("Name")
    age = st.number_input("Age", 1, 120)
    hr = st.slider("Heart Rate", 40, 180)
    oxygen = st.slider("Oxygen", 70, 100)

    if st.button("Save"):
        status = predict_risk(hr, oxygen)
        insert_patient(name, age, hr, oxygen, status)
        st.success("Saved")

elif choice == "Records":
    data = get_all_patients()
    df = pd.DataFrame(data, columns=["ID","Name","Age","Heart Rate","Oxygen","Status","Created"])
    st.dataframe(df)
