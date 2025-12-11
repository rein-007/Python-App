import yfinance as yf

def fetch_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo")
    info = stock.info
    price = info.get("currentPrice", None)
    prev_close = info.get("previousClose", None)
    pct_change = None
    if price and prev_close:
        pct_change = ((price - prev_close) / prev_close) * 100
    return hist, price, pct_change