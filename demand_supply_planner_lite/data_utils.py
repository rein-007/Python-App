import pandas as pd

def parse_uploaded_csv(uploaded):
    return pd.read_csv(uploaded)

def ensure_date_column(df, date_col="date"):
    df[date_col] = pd.to_datetime(df[date_col])
    return df.sort_values(date_col)

def get_blank_template_csv():
    template_df = pd.DataFrame(columns=["date", "sku", "qty"])
    return template_df.to_csv(index=False).encode("utf-8")