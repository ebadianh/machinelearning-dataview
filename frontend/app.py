"""Streamlit-frontend för Dataview.

Frontend pratar bara med backend via HTTP – ingen ML-kod och ingen
databasåtkomst här. Kör med:

    streamlit run frontend/app.py
"""

import os

import requests
import streamlit as st

API_URL = os.getenv("DATAVIEW_API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Dataview", page_icon="📊")
st.title("📊 Dataview")
st.caption("Ladda upp en CSV, välj target och jämför tre modeller.")

st.subheader("Backend-status")
st.write(f"API: `{API_URL}`")

if st.button("Kontrollera igen"):
    st.rerun()

try:
    response = requests.get(f"{API_URL}/health", timeout=5)
    response.raise_for_status()
    data = response.json()
    st.success(f"Backend svarar: {data.get('status')} (version {data.get('version')})")
except requests.exceptions.RequestException as exc:
    st.error(f"Får inte kontakt med backend: {exc}")
    st.info("Starta backend i ett annat terminalfönster:\n\n`uvicorn backend.main:app --reload`")
