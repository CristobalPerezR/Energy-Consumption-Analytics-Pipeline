import pandas as pd
import numpy as np
import os

FEATURES = [
    "global_active_power",
    "is_weekend",
    "hour_sin",
    "hour_cos",
    "day_of_week_sin",
    "day_of_week_cos",
    "global_active_power_ma_5m",
    "global_active_power_ma_15m",
    "global_active_power_ma_30m",
]

def create_dataset(path_csv:str) -> str:
    mlr_dir = os.path.join("data", "ml")
    os.makedirs(mlr_dir, exist_ok=True)
    path_ml_ready = os.path.join(mlr_dir, "ml_ready.csv")

    try:
        df = pd.read_csv(path_csv, sep=";")
        print("create_dataset: data loaded")
    except Exception as e:
        raise FileNotFoundError(f"Processed dataset not found. Run ETL first. Error: {e}")
    
    df = df.sort_values("datetime").reset_index(drop=True)

    df["global_active_power"] = df["global_active_power"].interpolate(limit=2)
    df = df.dropna(subset=["global_active_power"])

    df["global_active_power_ma_5m"] = (df["global_active_power"].rolling(window=5, min_periods=1).mean())
    df["global_active_power_ma_15m"] = (df["global_active_power"].rolling(window=15, min_periods=1).mean())
    df["global_active_power_ma_30m"] = (df["global_active_power"].rolling(window=30, min_periods=1).mean())

    df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
    df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)

    df["day_of_week_sin"] = np.sin(2 * np.pi * df["day_of_week"] / 7)
    df["day_of_week_cos"] = np.cos(2 * np.pi * df["day_of_week"] / 7)
    print("create_dataset: features created")

    df = df[FEATURES]

    df.to_csv(path_ml_ready, sep=";", index=False)
    print(f"create_features: dataset created and saved at {path_ml_ready}")
    
    return path_ml_ready