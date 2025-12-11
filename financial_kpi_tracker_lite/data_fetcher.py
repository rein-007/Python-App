import pandas as pd

def load_financial_data(file) -> pd.DataFrame:
    """
    Load financial data from CSV or Excel.
    Expected columns: Date, Revenue, Expenses, CashFlow
    """
    if hasattr(file, "name"):  # Streamlit UploadedFile
        if file.name.endswith(".csv"):
            df = pd.read_csv(file, parse_dates=["Date"])
        else:
            df = pd.read_excel(file, parse_dates=["Date"])
    else:  # Local string path
        if str(file).endswith(".csv"):
            df = pd.read_csv(file, parse_dates=["Date"])
        else:
            df = pd.read_excel(file, parse_dates=["Date"])
    df = df.sort_values("Date")
    return df