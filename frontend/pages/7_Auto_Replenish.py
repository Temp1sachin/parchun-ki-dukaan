# frontend/pages/5_Auto_Replenish.py
import streamlit as st
import pandas as pd
import requests

st.title("📦 Auto Replenish Planner")
st.markdown("Upload current inventory to get smart restocking suggestions.")

# Inputs
import pandas as pd

dist_df = pd.read_csv("../data/districts.csv")
districts = sorted(dist_df["district"].dropna().unique())
district = st.selectbox("📍 Select District", districts)
month = st.selectbox("Month", ["January","February","March","April","May","June","July","August","September","October", "November", "December"])
festival_flag = st.radio("Festival Season?", ["Yes", "No"]) == "Yes"
income_level = st.selectbox("Income Level", ["Low", "Medium", "High"])
kirana_density = st.selectbox("Kirana Density", ["Low", "Medium", "High"])
file = st.file_uploader("Upload Inventory CSV", type=["csv"])

if st.button("📈 Generate Replenishment Plan"):
    if file is None:
        st.warning("Please upload a CSV file.")
    else:
        with st.spinner("Computing..."):
            res = requests.post(
                "http://localhost:8000/replenish",
                data={
                    "district": district,
                    "month": month,
                    "festival_flag": int(festival_flag),
                    "income_level": income_level,
                    "kirana_density": kirana_density
                },
                files={"file": file}
            )
            data = res.json()
            if "replenishment_plan" in data:
                df = pd.DataFrame(data["replenishment_plan"])
                st.markdown("### 📦 Suggested Replenishment")
                st.dataframe(df)
            else:
                st.error("Something went wrong.")
