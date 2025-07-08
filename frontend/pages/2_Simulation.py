import streamlit as st
import requests
import plotly.express as px
import pandas as pd

# --------------------------
# CONFIG
# --------------------------
API_URL = "http://localhost:8000/recommend"

st.set_page_config(page_title="Walmart Kirana Digital Twin", layout="centered")

# --------------------------
# PAGE TITLE
# --------------------------
st.title("📦 Digital Twin: Rural Kirana + Walmart")
st.subheader("Simulate stocking strategy based on district data")

# --------------------------
# USER INPUT
# --------------------------
# Fetch full list of districts from backend
import pandas as pd

dist_df = pd.read_csv("../data/districts.csv")
districts = sorted(dist_df["district"].dropna().unique())
district = st.selectbox("📍 Select District", districts)


mode = st.radio("🛒 Mode", ["Walmart-only", "Walmart + Kirana Co-op"])
mode_param = "walmart_only" if mode == "Walmart-only" else "coop"

# --------------------------
# API CALL
# --------------------------
if st.button("🔍 Run Simulation"):
    with st.spinner("Analyzing district..."):
        try:
            res = requests.get(API_URL, params={"district": district, "mode": mode_param})
            data = res.json()
        except Exception as e:
            st.error("API Error: Could not connect to backend.")
            st.stop()

        if "error" in data:
            st.error(data["error"])
            st.stop()

        # --------------------------
        # DISTRICT PROFILE
        # --------------------------
        st.markdown("### 🧾 District Profile")
        col1, col2, col3 = st.columns(3)
        col1.metric("Population", f"{data['population']:,}")
        col2.metric("Income Level", data["income_level"])
        col3.metric("Kirana Density", data["kirana_density"])

        # --------------------------
        # UPCOMING FESTIVALS
        # --------------------------
        st.markdown("### 🎉 Upcoming Festivals")
        if data["festivals"]:
            st.success(", ".join(data["festivals"]))
        else:
            st.info("No major festivals found.")

        # --------------------------
        # SKU RECOMMENDATIONS
        # --------------------------
        st.markdown("### 🛍️ Recommended SKUs")

        if data["recommended_skus"]:
            sku_names = [sku["name"] for sku in data["recommended_skus"]]
            sku_scores = [sku["score"] for sku in data["recommended_skus"]]

            fig = px.bar(
                x=sku_names,
                y=sku_scores,
                labels={"x": "SKU", "y": "Demand Score"},
                title="📊 SKU Demand Prediction Scores",
                text=sku_scores
            )
            fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig.update_layout(yaxis_range=[0, 1], height=400)
            st.plotly_chart(fig, use_container_width=True)

            df = pd.DataFrame({
                "SKU": sku_names,
                "Score": [round(score, 2) for score in sku_scores]
            })
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No recommended SKUs found for this scenario.")

        # --------------------------
        # MODEL PERFORMANCE METRICS
        # --------------------------
        st.markdown("### 📈 Model Confidence Metrics")
        if "metrics" in data:
            rmse = round(data["metrics"]["rmse"], 2)
            mae = round(data["metrics"]["mae"], 2)
            acc = round(data["metrics"]["accuracy"] * 100, 2)

            col1, col2, col3 = st.columns(3)
            col1.metric("RMSE", f"{rmse}")
            col2.metric("MAE", f"{mae}")
            col3.metric("Accuracy", f"{acc}%")
        else:
            st.info("No model metrics available for this district.")

        # --------------------------
        # OPTIONAL: STRATEGY COMPARISON (if backend supports)
        # --------------------------
        if "coop_comparison" in data:
            st.markdown("### ⚖️ Walmart vs Co-op Strategy Comparison")
            comp_df = pd.DataFrame(data["coop_comparison"])
            fig2 = px.bar(
                comp_df,
                x="SKU",
                y=["Walmart-only", "Walmart + Co-op"],
                barmode="group",
                title="SKU Demand: Walmart vs Co-op Strategy"
            )
            st.plotly_chart(fig2, use_container_width=True)
