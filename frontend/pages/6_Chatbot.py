import streamlit as st
import requests

st.set_page_config(page_title="Kirana Chatbot", layout="centered")
st.title("🧠 Kirana + Walmart Assistant")

st.markdown("Ask me anything about stocking strategy, festivals, Walmart partnership, etc.")

query = st.text_input("💬 Your Question")

if query:
    with st.spinner("Thinking..."):
        res = requests.get("http://localhost:8000/chat", params={"q": query})
        st.success(res.json()["response"])
