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

balanced_path = os.path.join(
    BASE_DIR,
    "..",
    "..",
    "datasets",
    "raw",
    "url",
    "data_bal_phistank_i2pLocation - 20000.xlsx"
)

imbalanced_path = os.path.join(
    BASE_DIR,
    "..",
    "..",
    "datasets",
    "raw",
    "url",
    "data_imbal_phistank_i2pLocation  - 55000.xlsx"
)

print(balanced_path)
print(os.path.exists(balanced_path))

print(imbalanced_path)
print(os.path.exists(imbalanced_path))

balanced_df = pd.read_excel(
    balanced_path
)

imbalanced_df = pd.read_excel(
    imbalanced_path
)

df = pd.concat(
    [
        balanced_df,
        imbalanced_df
    ],
    ignore_index=True
)

print("\n===== HEAD =====")
print(df.head())

print("\n===== COLUMNS =====")
print(df.columns)

print("\n===== SHAPE =====")
print(df.shape)


def build_phishtank():

    rows = []

    for _, row in df.iterrows():

        features = extract_features(
            str(row["URLs"])
        )

        features["label"] = int(
            row["Labels"]
        )

        rows.append(features)

    dataset = pd.DataFrame(rows)

    print("\n===== PHISHTANK DATASET =====")
    print(dataset.head())

    print(
        dataset["label"].value_counts()
    )

    return dataset


if __name__ == "__main__":

    dataset = build_phishtank()

    print(dataset.shape)