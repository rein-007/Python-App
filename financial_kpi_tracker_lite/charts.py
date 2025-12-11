import matplotlib.pyplot as plt
from config import ACCENT_COLOR, FONT_NAME

def revenue_expenses_chart(df):
    fig, ax = plt.subplots(figsize=(8,4))
    df.plot(x="Date", y="Revenue", ax=ax, label="Revenue", color=ACCENT_COLOR)
    df.plot(x="Date", y="Expenses", ax=ax, label="Expenses", color="red")
    ax.set_title("Revenue vs Expenses", fontname=FONT_NAME)
    ax.set_ylabel("Amount")
    ax.grid(True, alpha=0.3)
    ax.legend()
    return fig

def cashflow_chart(df):
    fig, ax = plt.subplots(figsize=(8,4))
    df.plot(x="Date", y="CashFlow", ax=ax, label="Cash Flow", color="green")
    ax.set_title("Cash Flow Over Time", fontname=FONT_NAME)
    ax.set_ylabel("Amount")
    ax.grid(True, alpha=0.3)
    return fig