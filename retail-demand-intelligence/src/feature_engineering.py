import pandas as pd


def load_processed_data():

    df = pd.read_parquet("data/processed/sales_dataset.parquet")

    return df


def create_time_features(df):

    df["date"] = pd.to_datetime(df["date"])

    df["day_of_week"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month
    df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)

    return df


def create_lag_features(df):

    df = df.sort_values(["store_id", "item_id", "date"])

    df["lag_7"] = df.groupby(["store_id", "item_id"])["sales"].shift(7)
    df["lag_14"] = df.groupby(["store_id", "item_id"])["sales"].shift(14)
    df["lag_28"] = df.groupby(["store_id", "item_id"])["sales"].shift(28)

    return df


def create_rolling_features(df):

    df["rolling_mean_7"] = (
        df.groupby(["store_id", "item_id"])["sales"]
        .transform(lambda x: x.shift(7).rolling(7).mean())
    )

    df["rolling_std_14"] = (
        df.groupby(["store_id", "item_id"])["sales"]
        .transform(lambda x: x.shift(7).rolling(14).std())
    )

    return df


def create_price_features(df):

    df["price_change"] = (
        df.groupby(["store_id","item_id"])["sell_price"]
        .pct_change(fill_method=None)
    )

    df["price_change"] = df["price_change"].fillna(0)

    return df

def build_features():

    df = load_processed_data()

    df = create_time_features(df)
    df = create_lag_features(df)
    df = create_rolling_features(df)
    df = create_price_features(df)

    df = df.dropna(subset=["lag_7","lag_14","lag_28"])

    df.to_parquet("data/processed/features_dataset.parquet")

    print("Feature engineering completed")
    print(df.shape)


if __name__ == "__main__":
    build_features()