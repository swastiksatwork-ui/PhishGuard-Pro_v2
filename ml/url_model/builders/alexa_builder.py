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
    "Alexa_top-1m.csv"
)

print(dataset_path)
print(os.path.exists(dataset_path))

df = pd.read_csv(
    dataset_path,
    header=None
)

print("\n===== HEAD =====")
print(df.head())

print("\n===== COLUMNS =====")
print(df.columns)

print("\n===== SHAPE =====")
print(df.shape)


def build_alexa():

    rows = []

    for _, row in df.iterrows():

        features = extract_features(
            str(row[1])
        )

        features["label"] = 0

        rows.append(features)

    dataset = pd.DataFrame(rows)

    print("\n===== ALEXA DATASET =====")
    print(dataset.head())

    print(
        dataset["label"].value_counts()
    )

    return dataset


if __name__ == "__main__":

    dataset = build_alexa()

    print(dataset.shape)