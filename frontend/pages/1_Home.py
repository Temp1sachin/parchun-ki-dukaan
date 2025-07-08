import streamlit as st

st.set_page_config(page_title="Walmart Kirana Digital Twin", page_icon="📦", layout="wide")

# Dark mode-safe card style (no fixed light bg)
card_style = """
    background-color: rgba(255, 255, 255, 0.05);
    padding: 1.2rem 1rem; 
    margin: 0.5rem 0.5rem;
    border-radius: 1rem;
    border: 1px solid rgba(255,255,255,0.1);
"""

button_style = lambda color: f"""
    width: 100%;
    padding: 0.6rem 0;
    border: none;
    background: {color};
    color: white;
    border-radius: 0.5rem;
    font-size: 1rem;
"""

# Title
st.markdown("<h1 style='color:#facc15;'>📦 Walmart Kirana Digital Twin</h1>", unsafe_allow_html=True)

# Welcome
st.markdown(
    """
    <div style='font-size:1.1rem; color:inherit;'>
        Welcome to the <b>Walmart + Kirana Micro-Franchise Simulator</b>.<br>
        Use the sidebar to explore our tools.
    </div>
    """, unsafe_allow_html=True
)

st.markdown("<hr>", unsafe_allow_html=True)

# Top Row
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
        <div style="{card_style}">
            <h3>🔍 Simulation</h3>
            <p>Generate SKU strategies by district.</p>
            <a href="Simulation" target="_self">
                <button style="{button_style('#3b82f6')}">Go to Simulation</button>
            </a>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div style="{card_style}">
            <h3>📈Demand Predictor</h3>
            <p>Forecast SKU demand using ML.</p>
            <a href="Demand_Predictor" target="_self">
                <button style="{button_style('#10b981')}">Go to Predictor</button>
            </a>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div style="{card_style}">
            <h3>🆚Compare Strategy</h3>
            <p>Walmart-only vs Co-op models.</p>
            <a href="Compare_Strategy" target="_self">
                <button style="{button_style('#f59e0b')}">Go to Compare</button>
            </a>
        </div>
    """, unsafe_allow_html=True)

# Bottom Row
col4, col5, col6 = st.columns(3)
with col4:
    st.markdown(f"""
        <div style="{card_style}">
            <h3>🧠 Kirana Insights</h3>
            <p>Upload inventory and check stock health.</p>
            <a href="Kirana_Insights" target="_self">
                <button style="{button_style('#8b5cf6')}">Go to Insights</button>
            </a>
        </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
        <div style="{card_style}">
            <h3>🤖 Chatbot</h3>
            <p>Ask questions about Walmart policies.</p>
            <a href="Chatbot" target="_self">
                <button style="{button_style('#ef4444')}">Go to Chatbot</button>
            </a>
        </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown(f"""
        <div style="{card_style}">
            <h3>🔄 Auto Replenish</h3>
            <p>Suggest restock quantities automatically.</p>
            <a href="Auto_Replenish" target="_self">
                <button style="{button_style('#0ea5e9')}">Go to Replenish</button>
            </a>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; color:gray;'>Demo for Walmart hackathon<3</div>", unsafe_allow_html=True)
