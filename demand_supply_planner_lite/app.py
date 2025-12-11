import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from data_utils import parse_uploaded_csv, ensure_date_column
from forecasting import forecast_exponential_smoothing
from inventory import compute_safety_stock, compute_reorder_point
from ui_components import sidebar_inputs

# ----------------------
# Streamlit setup
# ----------------------
st.set_page_config(page_title="Demand & Supply Planner - Lite", layout="wide")
st.title("📦 Demand & Supply Planner - Lite")

# Sidebar inputs
uploaded_file, date_col, sku_col, qty_col, forecast_horizon, lead_time, run_button = sidebar_inputs()

# Main logic
if run_button and uploaded_file is not None:
    df = parse_uploaded_csv(uploaded_file)
    df = ensure_date_column(df, date_col)

    st.success(f"Loaded {len(df)} rows, {df[sku_col].nunique()} SKUs")

    results = []
    for sku in df[sku_col].unique():
        ts = df[df[sku_col] == sku].set_index(date_col)[qty_col].resample("D").sum().fillna(0)

        pred = forecast_exponential_smoothing(ts, forecast_horizon)
        avg_daily = ts.tail(90).mean() if len(ts) >= 30 else ts.mean()
        safety = compute_safety_stock(ts, lead_time, z=1.65)
        reorder = compute_reorder_point(avg_daily, lead_time, safety)

        results.append({
            "sku": sku,
            "forecast_total": int(np.ceil(pred.sum())),
            "safety_stock": safety,
            "reorder_point": reorder
        })

        # Chart
        future_index = pd.date_range(start=ts.index.max() + pd.Timedelta(days=1), periods=forecast_horizon, freq="D")
        chart_df = pd.DataFrame({"historical": ts, "forecast": pred}, index=future_index.union(ts.index))
        chart_df = chart_df.reset_index().melt(id_vars="index", value_vars=["historical", "forecast"], var_name="series", value_name="qty")
        fig = px.line(chart_df, x="index", y="qty", color="series", title=f"{sku} demand + forecast")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Summary")
    st.dataframe(pd.DataFrame(results))