import pandas as pd
import joblib
import numpy as np


MODEL_PATH = "models/demand_forecast_model.pkl"
FEATURE_DATA_PATH = "data/processed/features_dataset.parquet"


def load_data():

    df = pd.read_parquet(FEATURE_DATA_PATH)
    model = joblib.load(MODEL_PATH)

    return df, model


def prepare_features(df):

    features = [
        "sell_price",
        "lag_7",
        "lag_14",
        "lag_28",
        "rolling_mean_7",
        "rolling_std_14",
        "price_change",
        "day_of_week",
        "month",
        "week_of_year"
    ]

    return df[features]


def generate_forecast(df, model):

    X = prepare_features(df)

    df["predicted_demand"] = model.predict(X)

    return df


def calculate_safety_stock(df):

    SERVICE_LEVEL_Z = 1.28  # ~90% service level
    LEAD_TIME_DAYS = 7

    df["demand_std"] = df.groupby(
        ["store_id", "item_id"]
    )["sales"].transform("std")

    safety = SERVICE_LEVEL_Z * df["demand_std"] * np.sqrt(LEAD_TIME_DAYS)
    df["safety_stock"] = safety.clip(upper=df["predicted_demand"] * 0.5)

    return df


def calculate_inventory_recommendation(df):

    df["recommended_stock"] = (
                            df["predicted_demand"] + df["safety_stock"]
                            ).round()

    df["recommended_stock"] = df["recommended_stock"].clip(lower=0)

    return df


def save_results(df):

    output_cols = [
        "store_id",
        "item_id",
        "date",
        "sales",
        "predicted_demand",
        "safety_stock",
        "recommended_stock"
    ]

    result = df[output_cols]

    result.to_csv("reports/inventory_recommendations.csv", index=False)

    print("Inventory recommendations saved.")


def run_inventory_optimizer():

    df, model = load_data()

    df = generate_forecast(df, model)

    df = calculate_safety_stock(df)

    df = calculate_inventory_recommendation(df)

    save_results(df)


if __name__ == "__main__":

    run_inventory_optimizer()