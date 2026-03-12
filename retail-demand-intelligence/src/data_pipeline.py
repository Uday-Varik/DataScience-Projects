import pandas as pd

def load_data():

    sales = pd.read_csv(
        "data/raw/sales_train_validation.csv",
        dtype={
            "item_id": "category",
            "dept_id": "category",
            "cat_id": "category",
            "store_id": "category",
            "state_id": "category"
        }
    )

    calendar = pd.read_csv("data/raw/calendar.csv")
    prices = pd.read_csv("data/raw/sell_prices.csv")

    return sales, calendar, prices


def preprocess_data():

    sales, calendar, prices = load_data()

    # Development subset
    sales = sales.sample(2000, random_state=42)

    # Select limited days
    day_cols = [col for col in sales.columns if col.startswith("d_")][:200]

    sales_long = sales.melt(
        id_vars=["id","item_id","dept_id","cat_id","store_id","state_id"],
        value_vars=day_cols,
        var_name="d",
        value_name="sales"
    )

    sales_long["sales"] = sales_long["sales"].astype("int16")

    df = sales_long.merge(calendar, on="d", how="left")

    df = df.merge(
        prices,
        on=["store_id","item_id","wm_yr_wk"],
        how="left"
    )

    return df


if __name__ == "__main__":

    df = preprocess_data()

    df.to_parquet("data/processed/sales_dataset.parquet")

    print("Pipeline completed.")
    print(df.shape)