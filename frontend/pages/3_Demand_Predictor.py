import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="Demand Predictor", layout="centered")
st.title("📈 Demand Predictor (ML-Backed)")
st.caption("Forecast SKU demand based on district, month, festival and kirana profile")

# --------------------------
# User Inputs
# --------------------------
import pandas as pd

dist_df = pd.read_csv("../data/districts.csv")
districts = sorted(dist_df["district"].dropna().unique())
district = st.selectbox("📍 Select District", districts)
month = st.selectbox("🗓️ Select Month", [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
])
festival_flag = st.checkbox("🎉 Is there a major festival?")
income_level = st.selectbox("💰 Income Level", ["Low", "Medium", "High"])
kirana_density = st.selectbox("🏪 Kirana Density", ["Low", "Medium", "High"])

# --------------------------
# Prediction Request
# --------------------------
if st.button("📊 Predict Demand"):
    with st.spinner("Running prediction model..."):
        try:
            res = requests.post("http://localhost:8000/predict_demand", json={
                "district": district,
                "month": month,
                "festival_flag": int(festival_flag),
                "income_level": income_level,
                "kirana_density": kirana_density
            })
            data = res.json()
        except:
            st.error("❌ Backend not responding. Ensure FastAPI is running.")
            st.stop()

        # --------------------------
        # Demand Prediction Table
        # --------------------------
        st.subheader("🔮 Predicted SKU Demand (Units)")
        df = pd.DataFrame(data["predictions"])  # expects list of {sku, predicted_demand}
        df["predicted_demand"] = df["predicted_demand"].round().astype(int)

        fig = px.bar(
            df,
            x="sku",
            y="predicted_demand",
            title="📊 SKU Demand Forecast",
            labels={"sku": "SKU", "predicted_demand": "Units"}
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df, use_container_width=True)

        # --------------------------
        # Model Performance Metrics
        # --------------------------
        if "metrics" in data:
            st.markdown("### 📈 Model Performance")
            col1, col2, col3 = st.columns(3)
            col1.metric("RMSE", round(data["metrics"]["rmse"], 2))
            col2.metric("MAE", round(data["metrics"]["mae"], 2))
            col3.metric("Accuracy", f"{round(data['metrics']['accuracy'] * 100, 2)}%")

        # --------------------------
        # Feature Importance (Optional)
        # --------------------------
        if "feature_importance" in data:
            st.markdown("### 🧠 Feature Importance")
            fi_df = pd.DataFrame(data["feature_importance"])
            fi_fig = px.bar(
                fi_df,
                x="feature",
                y="importance",
                title="🔍 Features Driving Prediction",
                labels={"feature": "Feature", "importance": "Importance"}
            )
            st.plotly_chart(fi_fig, use_container_width=True)
