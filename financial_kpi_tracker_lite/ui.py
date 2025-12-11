import streamlit as st
import pandas as pd
import yfinance as yf
import pycountry
from config import KPI_LABELS
from data_fetcher import load_financial_data
from analytics import compute_kpis
from charts import revenue_expenses_chart, cashflow_chart
from reporting import build_pptx, save_pptx
from io import BytesIO

# Common currency symbols (fallback to code if not found)
currency_symbols = {
    "PHP": "₱", "USD": "$", "EUR": "€", "JPY": "¥", "AUD": "A$",
    "GBP": "£", "CNY": "¥", "INR": "₹", "CAD": "C$", "CHF": "CHF"
}

def get_rate(base="PHP", target="USD"):
    """Fetch latest exchange rate using Yahoo Finance."""
    if base == target:
        return 1.0
    ticker = f"{base}{target}=X"
    data = yf.Ticker(ticker).history(period="1d")
    return data["Close"].iloc[-1]

def run_dashboard():
    st.set_page_config(page_title="Financial KPI Tracker - Lite", layout="wide")
    st.title("📊 Financial KPI Tracker - Lite")

    # --- Download Blank Template ---
    st.subheader("Download Blank Template")
    template_df = pd.DataFrame(columns=["Date","Revenue","Expenses","CashFlow"])
    buffer = BytesIO()
    template_df.to_csv(buffer, index=False)
    st.download_button(
        label="⬇️ Download Blank CSV Template",
        data=buffer.getvalue(),
        file_name="financial_kpi_template.csv",
        mime="text/csv"
    )

    # Dynamically get all ISO currency codes
    currencies = [c.alpha_3 for c in pycountry.currencies]
    selected_currency = st.selectbox(
        "Display Currency:",
        currencies,
        index=currencies.index("PHP") if "PHP" in currencies else 0
    )
    symbol = currency_symbols.get(selected_currency, selected_currency)

    # Upload data
    uploaded_file = st.file_uploader("Upload financial data (CSV/Excel)", type=["csv","xlsx"])
    if uploaded_file:
        df = load_financial_data(uploaded_file)
        kpis = compute_kpis(df)

        # Convert KPIs if needed
        rate = get_rate("PHP", selected_currency)
        for key in kpis:
            if kpis[key] is not None:
                kpis[key] *= rate

        # KPI cards with commas + currency
        st.subheader("Overview KPIs")
        cols = st.columns(len(KPI_LABELS))
        for i, (key,label) in enumerate(KPI_LABELS.items()):
            val = kpis.get(key)
            if val is not None:
                cols[i].metric(label, f"{symbol}{val:,.2f}")
            else:
                cols[i].metric(label, "--")

        # Charts
        st.subheader("Trends")
        st.pyplot(revenue_expenses_chart(df))
        st.pyplot(cashflow_chart(df))

        # Export
        st.subheader("Export Report")
        if st.button("Generate PPTX"):
            prs = build_pptx(kpis, revenue_expenses_chart(df), cashflow_chart(df))
            path = save_pptx(prs)
            st.success(f"Report saved: {path}")