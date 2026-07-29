from autogluon.tabular import TabularPredictor
import pandas as pd
import os

print(os.getcwd())

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

dataset_path = os.path.join(
    BASE_DIR,
    "features",
    "combined_url_dataset.csv"
)

print(dataset_path)

print(
    os.path.exists(
        dataset_path
    )
)

df = pd.read_csv(
    dataset_path
)

print("\n===== DATASET INFO =====")
print(df.shape)

print("\n===== LABEL COUNTS =====")
print(
    df["label"].value_counts()
)

predictor = TabularPredictor(
    label="label",
    path="../models/url_model"
)

predictor.fit(
    df,

    hyperparameters={
        "RF": {},
        "XT": {},
        "GBM": {},
        "XGB": {},

        "NN_TORCH": {
            "num_epochs": 80,
            "hidden_size": 79,
            "num_layers": 2,
            "learning_rate": 0.005,
            "max_batch_size": 1024
        },

        "CAT": {
            "depth": 4,
            "iterations": 44
        }
    },

    presets="best_v150",
    num_bag_folds= 5
)

print(
    predictor.leaderboard(
        df
    )
)