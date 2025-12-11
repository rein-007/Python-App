import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def forecast_exponential_smoothing(series: pd.Series, horizon: int = 30):
    model = ExponentialSmoothing(series, initialization_method="estimated")
    fit = model.fit(optimized=True)
    return fit.forecast(horizon)