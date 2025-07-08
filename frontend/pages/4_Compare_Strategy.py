import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Strategy Comparator", layout="wide")
st.title("🧮 Strategy Comparator")
st.markdown("Compare stocking recommendations between **Walmart-only** vs **Walmart + Kirana Co-op** modes.")

# Fetch full list of districts from backend
import pandas as pd

dist_df = pd.read_csv("../data/districts.csv")
districts = sorted(dist_df["district"].dropna().unique())
district = st.selectbox("📍 Select District", districts)


if st.button("📊 Compare Strategies"):
    with st.spinner("Fetching recommendations..."):
        try:
            res1 = requests.get("http://localhost:8000/recommend", params={"district": district, "mode": "walmart_only"})
            res2 = requests.get("http://localhost:8000/recommend", params={"district": district, "mode": "coop"})
            data_walmart = res1.json()
            data_coop = res2.json()
        except Exception as e:
            st.error(f"❌ API Error: {e}")
            st.stop()

        if "error" in data_walmart or "error" in data_coop:
            st.error("❌ Invalid district or API failure.")
            st.stop()

        # ---------------------------------------
        # Normalize SKU lists (dicts or strings)
        # ---------------------------------------
        def extract_skus(data):
            raw = data["recommended_skus"]
            if isinstance(raw[0], dict):
                return {sku["name"]: sku.get("score", 1.0) for sku in raw}
            else:
                return {sku: 1.0 for sku in raw}

        sku_walmart = extract_skus(data_walmart)
        sku_coop = extract_skus(data_coop)

        set_walmart = set(sku_walmart.keys())
        set_coop = set(sku_coop.keys())

        # ---------------------------------------
        # Side-by-side Tables
        # ---------------------------------------
        st.subheader("🆚 SKU Recommendations")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Walmart-only")
            df1 = pd.DataFrame(list(sku_walmart.items()), columns=["SKU", "Score"])
            st.dataframe(df1.sort_values("Score", ascending=False))

        with col2:
            st.markdown("#### Walmart + Kirana Co-op")
            df2 = pd.DataFrame(list(sku_coop.items()), columns=["SKU", "Score"])
            st.dataframe(df2.sort_values("Score", ascending=False))

        # ---------------------------------------
        # Breakdown Analysis
        # ---------------------------------------
        both = set_walmart & set_coop
        only_walmart = set_walmart - set_coop
        only_coop = set_coop - set_walmart

        st.markdown("### 🔍 Breakdown")
        colA, colB, colC = st.columns(3)
        colA.metric("✅ Common SKUs", len(both))
        colB.metric("🧊 Only in Walmart", len(only_walmart))
        colC.metric("🤝 Only in Co-op", len(only_coop))

        # Overlap %
        total_union = len(set_walmart | set_coop)
        overlap_percent = (len(both) / total_union) * 100 if total_union else 0
        st.write(f"📊 **Overlap**: `{overlap_percent:.1f}%` of SKUs are common between both strategies.")

        # ---------------------------------------
        # Venn-like Bar Chart
        # ---------------------------------------
        fig = go.Figure(data=[
            go.Bar(name='Walmart-only', x=['SKUs'], y=[len(set_walmart)], marker_color='blue'),
            go.Bar(name='Co-op', x=['SKUs'], y=[len(set_coop)], marker_color='green'),
            go.Bar(name='Overlap', x=['SKUs'], y=[len(both)], marker_color='gray')
        ])
        fig.update_layout(title="SKU Set Comparison", barmode='group')
        st.plotly_chart(fig, use_container_width=True)

        # ---------------------------------------
        # Show Top Differing SKUs
        # ---------------------------------------
        st.markdown("### 📌 Notable Differences")

        diff_data = []
        for sku in only_walmart:
            diff_data.append({"SKU": sku, "Strategy": "Walmart-only", "Score": sku_walmart[sku]})
        for sku in only_coop:
            diff_data.append({"SKU": sku, "Strategy": "Co-op", "Score": sku_coop[sku]})
        df_diff = pd.DataFrame(diff_data)

        if not df_diff.empty:
            fig2 = px.bar(df_diff, x="SKU", y="Score", color="Strategy", barmode="group", title="Unique SKU Demand Scores")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("✅ All SKUs are shared between both strategies.")

        # ---------------------------------------
        # Download Options
        # ---------------------------------------
        csv1 = df1.to_csv(index=False).encode("utf-8")
        csv2 = df2.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Walmart-only SKUs", csv1, "walmart_only_skus.csv", "text/csv")
        st.download_button("⬇️ Download Co-op SKUs", csv2, "coop_skus.csv", "text/csv")
