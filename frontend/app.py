import streamlit as st
import requests
import plotly.express as px

# --------------------------
# CONFIG
# --------------------------
API_URL = "http://localhost:8000/recommend"

# --------------------------
# Streamlit UI
# --------------------------
st.set_page_config(page_title="Walmart Kirana Digital Twin", layout="centered")

st.title("📦 Digital Twin: Rural Kirana + Walmart")
st.subheader("Simulate stocking strategy based on district data")

# Select district
district = st.selectbox("📍 Select District", [
    "Dhanbad", "Mysuru", "Varanasi", "Pune", "Raipur", "Bikaner", "Coimbatore"
])

# Mode toggle
mode = st.radio("🛒 Mode", ["Walmart-only", "Walmart + Kirana Co-op"])
mode_param = "walmart_only" if mode == "Walmart-only" else "coop"

# Fetch data from backend
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
        # Show District Context Info
        # --------------------------
        st.markdown("### 🧾 District Profile")
        col1, col2, col3 = st.columns(3)
        col1.metric("Population", f"{data['population']:,}")
        col2.metric("Income Level", data["income_level"])
        col3.metric("Kirana Density", data["kirana_density"])

        # --------------------------
        # Show Festivals
        # --------------------------
        st.markdown("### 🎉 Upcoming Festivals")
        if data["festivals"]:
            st.write(", ".join(data["festivals"]))
        else:
            st.write("No major festivals found.")

        # --------------------------
        # Recommended SKUs
        # --------------------------
        st.markdown("### 🛍️ Recommended SKUs")

        if data["recommended_skus"]:
            sku_df = {"SKU": data["recommended_skus"]}
            fig = px.bar(sku_df, x="SKU", y=[1]*len(sku_df["SKU"]),
                         labels={"y": "Recommendation Score"},
                         title="SKU Recommendation Chart")
            st.plotly_chart(fig)
        else:
            st.warning("No recommended SKUs found for this scenario.")
