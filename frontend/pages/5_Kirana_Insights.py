import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Kirana Inventory Analyzer", layout="centered")
st.title("📋 Kirana Inventory Analyzer")
st.markdown("Upload your kirana store’s inventory and compare it with ML-predicted demand to find stock gaps and suggestions.")

# ------------------------- Input Section -------------------------
st.subheader("📥 Upload + Context Info")

import pandas as pd

dist_df = pd.read_csv("../data/districts.csv")
districts = sorted(dist_df["district"].dropna().unique())
district = st.selectbox("📍 Select District", districts)
month = st.selectbox("Month", ["January","February","March","April","May","June","July","August","September","October", "November", "December"])
festival_flag = st.radio("🎉 Is it a festival season?", ["Yes", "No"]) == "Yes"
income_level = st.selectbox("💰 Income Level", ["Low", "Medium", "High"])
kirana_density = st.selectbox("🏪 Kirana Density", ["Low", "Medium", "High"])
file = st.file_uploader("📁 Upload Inventory CSV", type=["csv"], help="CSV must have columns: `sku`, `stock`")

# ------------------------- Submit & Response -------------------------
if st.button("🔍 Analyze Inventory"):
    if file is None:
        st.warning("⚠️ Please upload a CSV file before submitting.")
    else:
        with st.spinner("🔄 Analyzing your inventory..."):
            try:
                response = requests.post(
                    "http://localhost:8000/analyze_inventory",
                    data={
                        "district": district,
                        "month": month,
                        "festival_flag": int(festival_flag),
                        "income_level": income_level,
                        "kirana_density": kirana_density
                    },
                    files={"file": file}
                )
                data = response.json()
            except Exception as e:
                st.error(f"❌ API Error: {e}")
                st.stop()

            if "analysis" in data:
                df = pd.DataFrame(data["analysis"])
                df.columns = [col.lower().strip() for col in df.columns]

                st.success("✅ Inventory analyzed successfully!")
                st.markdown("### 📊 Inventory Health Overview")

                # Color-coded status
                def highlight_status(val):
                    color = "green" if "OK" in val else "orange" if "Low" in val else "red"
                    return f"background-color: {color}; color: white"

                if "status" in df.columns:
                    styled_df = df.style.applymap(highlight_status, subset=["status"])
                    st.dataframe(styled_df, use_container_width=True)
                else:
                
                    st.dataframe(df)

                # Bar chart
                st.markdown("### 📦 Demand vs Stock")
                st.bar_chart(df.set_index("sku")[["stock", "predicted_demand"]])

                # Download
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("📥 Download Report as CSV", csv, "inventory_report.csv", "text/csv")
            else:
                st.error("❌ Inventory analysis failed.")
