import os
import sys
import pandas as pd

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

sys.path.append(
    os.path.join(
        BASE_DIR,
        ".."
    )
)

from feature_extractor import extract_features

dataset_path = os.path.join(
    BASE_DIR,
    "..",
    "..",
    "datasets",
    "raw",
    "url",
    "majestic_million.csv"
)

print(dataset_path)
print(os.path.exists(dataset_path))

df = pd.read_csv(
    dataset_path
)

print("\n===== HEAD =====")
print(df.head())

print("\n===== COLUMNS =====")
print(df.columns)

print("\n===== SHAPE =====")
print(df.shape)


def build_majestic():

    rows = []

    for _, row in df.iterrows():

        features = extract_features(
            str(row["Domain"])
        )

        features["label"] = 0

        rows.append(features)

    dataset = pd.DataFrame(rows)

    print("\n===== MAJESTIC DATASET =====")
    print(dataset.head())

    print(
        dataset["label"].value_counts()
    )

    return dataset


if __name__ == "__main__":

    dataset = build_majestic()

    print(dataset.shape)