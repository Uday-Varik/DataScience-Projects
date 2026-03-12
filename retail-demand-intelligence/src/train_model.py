import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import lightgbm as lgb
import joblib


def load_features():

    df = pd.read_parquet("data/processed/features_dataset.parquet")

    return df


def prepare_data(df):

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

    X = df[features]
    y = df["sales"]

    return X, y


def train_model(X, y):

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    model = lgb.LGBMRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=8,
        num_leaves=50
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    print("Model MAE:", mae)

    return model


def save_model(model):

    joblib.dump(model, "models/demand_forecast_model.pkl")

    print("Model saved.")


if __name__ == "__main__":

    df = load_features()

    X, y = prepare_data(df)

    model = train_model(X, y)

    save_model(model)