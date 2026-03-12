import pandas as pd
import numpy as np


DATA_PATH = "reports/inventory_recommendations.csv"


def load_data():

    df = pd.read_csv(DATA_PATH)

    return df


def baseline_strategy(df):

    df["baseline_stock"] = (
        df.groupby(["store_id", "item_id"])["sales"]
        .transform(lambda x: x.rolling(28).mean())
    )

    return df


def ml_strategy(df):

    df["ml_stock"] = df["recommended_stock"]

    return df


def calculate_metrics(df):

    HOLDING_COST = 2
    STOCKOUT_COST = 12

    # Baseline metrics
    df["baseline_stockout"] = np.maximum(df["sales"] - df["baseline_stock"], 0)
    df["baseline_overstock"] = np.maximum(df["baseline_stock"] - df["sales"], 0)

    # ML metrics
    df["ml_stockout"] = np.maximum(df["sales"] - df["ml_stock"], 0)
    df["ml_overstock"] = np.maximum(df["ml_stock"] - df["sales"], 0)

    baseline_cost = (
        df["baseline_overstock"].sum() * HOLDING_COST +
        df["baseline_stockout"].sum() * STOCKOUT_COST
    )

    ml_cost = (
        df["ml_overstock"].sum() * HOLDING_COST +
        df["ml_stockout"].sum() * STOCKOUT_COST
    )

    results = pd.DataFrame({
        "strategy": ["baseline", "ml_system"],
        "total_cost": [baseline_cost, ml_cost],
        "stockouts": [df["baseline_stockout"].sum(), df["ml_stockout"].sum()],
        "overstock": [df["baseline_overstock"].sum(), df["ml_overstock"].sum()]
    })

    return results


def save_results(results):

    results.to_csv("reports/business_impact_analysis.csv", index=False)

    print(results)
    print("\nBusiness impact analysis saved.")


def run_simulation():

    df = load_data()

    df = baseline_strategy(df)

    df = ml_strategy(df)

    results = calculate_metrics(df)

    save_results(results)


if __name__ == "__main__":

    run_simulation()