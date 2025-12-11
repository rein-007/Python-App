import streamlit as st
import matplotlib.pyplot as plt
from config import DEFAULT_TICKERS, ACCENT_COLOR, FONT_NAME
from data_fetcher import fetch_data
from reporting import export_to_pptx

def run_dashboard():
    st.set_page_config(page_title="Stock Dashboard - Lite", layout="centered")
    st.title("📊 Stock Dashboard - Lite")

    ticker = st.selectbox(
        "Select Company:",
        options=list(DEFAULT_TICKERS.keys()),
        format_func=lambda x: DEFAULT_TICKERS[x]
    )

    if st.button("Load Data"):
        hist, price, pct_change = fetch_data(ticker)

        st.metric(label=f"{ticker} Price", value=f"{price:.2f} USD", delta=f"{pct_change:.2f}%")

        fig, ax = plt.subplots(figsize=(7,4))
        hist['Close'].plot(ax=ax, color=ACCENT_COLOR)
        ax.set_title(f"{ticker} Closing Prices (Last 30 Days)", fontname=FONT_NAME)
        ax.set_ylabel("Price (USD)")
        ax.grid(True)
        st.pyplot(fig)

        if st.button("Export Report"):
            folder = "."  # default current folder
            output_file = export_to_pptx(ticker, hist, price, pct_change, folder=folder)

            st.success(f"Report saved as {output_file}")
