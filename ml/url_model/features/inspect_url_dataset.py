import os
import pandas as pd

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

dataset_path = os.path.join(
    BASE_DIR,
    "features",
    "combined_url_dataset.csv"
)

print(dataset_path)
print(os.path.exists(dataset_path))

df = pd.read_csv(
    dataset_path
)

print(df.shape)
print(df.columns)
print(df["label"].value_counts())