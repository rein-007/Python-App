import pandas as pd

def compute_kpis(df: pd.DataFrame) -> dict:
    revenue = df["Revenue"].sum()
    expenses = df["Expenses"].sum()
    profit_margin = (revenue - expenses) / revenue if revenue else None
    cash_flow = df["CashFlow"].sum()

    # Growth rate: compare last vs first revenue
    first_rev = df["Revenue"].iloc[0]
    last_rev = df["Revenue"].iloc[-1]
    growth_rate = ((last_rev - first_rev) / first_rev) * 100 if first_rev else None

    return {
        "revenue": revenue,
        "expenses": expenses,
        "profit_margin": profit_margin,
        "cash_flow": cash_flow,
        "growth_rate": growth_rate
    }