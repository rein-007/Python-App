import numpy as np
import pandas as pd

def compute_safety_stock(daily_demands: pd.Series, lead_time_days: int = 7, z: float = 1.65) -> float:
    sd = daily_demands.std(ddof=0)
    return float(np.ceil(sd * z * np.sqrt(max(1, lead_time_days))))

def compute_reorder_point(avg_daily_demand: float, lead_time_days: int, safety_stock: float) -> float:
    return float(np.ceil(avg_daily_demand * lead_time_days + safety_stock))