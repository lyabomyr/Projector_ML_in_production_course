from sklearn.ensemble import RandomForestRegressor
from datetime import datetime
import pandas as pd
import typer
from sklearn.ensemble import RandomForestRegressor
from joblib import dump
from feast import FeatureStore


def get_df(repo_path: str):
    entity_df = pd.DataFrame.from_dict(
        {
            "driver_id": [1001, 1002, 1003],
            "event_timestamp": [
                datetime(2021, 4, 12, 10, 59, 42),
                datetime(2021, 4, 12, 8, 12, 10),
                datetime(2021, 4, 12, 16, 40, 26),
            ],
            "label_driver_reported_satisfaction": [1, 5, 3],
            "val_to_add": [1, 2, 3],
            "val_to_add_2": [10, 20, 30],
        }
    )

    fs = FeatureStore(repo_path=repo_path)

    training_df = fs.get_historical_features(
        entity_df=entity_df,
        features=[
            "driver_hourly_stats:conv_rate",
            "driver_hourly_stats:acc_rate",
            "driver_hourly_stats:avg_daily_trips",
            "transformed_conv_rate:conv_rate_plus_val1",
            "transformed_conv_rate:conv_rate_plus_val2",
        ],
    ).to_df()

    print("----- Feature schema -----\n")
    print(training_df.info())

    print()
    print("----- Example features -----\n")
    print(training_df.head())
    return training_df


def train(df: pd.DataFrame, model_path: str):
    target = "label_driver_reported_satisfaction"
    print("label_driver_reported_satisfaction")
    print(df.head())

    X = df[df.columns.drop(target).drop("event_timestamp")]
    y = df[[target]].to_numpy().ravel()
    print(X.head())
    print("y", y)

    reg = RandomForestRegressor()
    reg.fit(X, y)
    dump(reg, model_path)

def main(repo_path: str = "", model_path: str = "model.bin"):
    train_df = get_df(repo_path)
    train(train_df, model_path)
    

if __name__ == "__main__":
    typer.run(main)
