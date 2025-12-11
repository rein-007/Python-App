import streamlit as st
from data_utils import get_blank_template_csv

def sidebar_inputs():
    st.header("Inputs")
    st.download_button(
        label="Download Blank CSV Template",
        data=get_blank_template_csv(),
        file_name="demand_template.csv",
        mime="text/csv"
    )

    uploaded_file = st.file_uploader("Upload demand history (CSV)", type=["csv"])
    date_col = st.text_input("Date column", value="date")
    sku_col = st.text_input("SKU column", value="sku")
    qty_col = st.text_input("Quantity column", value="qty")
    forecast_horizon = st.number_input("Forecast horizon (days)", min_value=1, max_value=90, value=30)
    lead_time = st.number_input("Lead time (days)", min_value=1, value=7)
    run_button = st.button("Run Planner")

    return uploaded_file, date_col, sku_col, qty_col, forecast_horizon, lead_time, run_button