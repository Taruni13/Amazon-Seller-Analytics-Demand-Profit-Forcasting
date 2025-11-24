"""Streamlit app entry (landing page). Run with: `streamlit run app.py`"""
import streamlit as st

st.set_page_config(page_title="Amazon Seller Analytics", layout="wide")

st.title("Amazon Seller Analytics — Dashboard")

st.markdown(
    """
    This Streamlit app provides EDA, modeling, forecasting and business insights
    using the cleaned datasets in `data_process/`.

    Use the pages in the left sidebar (or the `pages/` navigation) to move between:
    - EDA
    - Modeling
    - Forecast
    - Insights
    """
)

st.write("Select a page from the sidebar to begin.")
