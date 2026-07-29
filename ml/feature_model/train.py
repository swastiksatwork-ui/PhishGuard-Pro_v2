from autogluon.tabular import TabularPredictor
import pandas as pd
import os

from arff_loader import load_arff

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

dataset1_path = os.path.join(
    BASE_DIR,
    "..",
    "datasets",
    "raw",
    "feature",
    "UCI_old.arff"
)

dataset2_path = os.path.join(
    BASE_DIR,
    "..",
    "datasets",
    "raw",
    "feature",
    "UCI_Training Dataset.arff"
)

df1 = load_arff(
    dataset1_path
)

df2 = load_arff(
    dataset2_path
)

print(
    "Old Dataset:",
    df1.shape
)

print(
    "UCI Dataset:",
    df2.shape
)

# Merge both datasets
df = pd.concat(
    [df1, df2],
    ignore_index=True
)

# Remove duplicates if present
df = df.drop_duplicates()

print(
    "Combined Dataset:",
    df.shape
)

predictor = TabularPredictor(
    label="Result",
    path="../models/feature_model_combined"
)

predictor.fit(

    df,

    hyperparameters={

        "RF": {},
        "XT": {},
        "GBM": {},
        "XGB": {},

        "NN_TORCH": {
            "num_epochs": 15,
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

    num_bag_folds=0

)

print(
    predictor.leaderboard(
        df
    )
)