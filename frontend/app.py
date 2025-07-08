
import streamlit as st

# Redirect to Home page (1_Home.py) on app load
try:
    st.switch_page("pages/1_Home.py")
except Exception:
    # Fallback: show a clickable link if switch_page is not available
    st.title("Redirecting to Home page...")
    st.markdown("[Go to Home](/Home)")
