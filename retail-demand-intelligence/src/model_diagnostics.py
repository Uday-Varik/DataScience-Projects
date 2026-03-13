import pandas as pd
import numpy as np


def add_forecast_intervals(df):

    df["error"] = df["sales"] - df["predicted_demand"]

    error_std = df["error"].std()

    df["upper_ci"] = df["predicted_demand"] + 1.96 * error_std
    df["lower_ci"] = df["predicted_demand"] - 1.96 * error_std

    return df

## Automated Demand Anomaly Detection
def detect_demand_anomalies(df):

    mean = df["sales"].mean()
    std = df["sales"].std()

    threshold = mean + 3 * std

    df["anomaly"] = df["sales"] > threshold

    return df


## Model Monitoring Metrics

def compute_model_metrics(df):

    mae = np.mean(np.abs(df["sales"] - df["predicted_demand"]))

    mape = np.mean(
        np.abs((df["sales"] - df["predicted_demand"]) / (df["sales"] + 1e-5))
    ) * 100

    rmse = np.sqrt(
        np.mean((df["sales"] - df["predicted_demand"]) ** 2)
    )

    return {
        "MAE": round(mae,2),
        "MAPE": round(mape,2),
        "RMSE": round(rmse,2)
    }