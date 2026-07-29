import os
import sys
import pandas as pd

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

# Allows import from url_model/
sys.path.append(
    os.path.join(
        BASE_DIR,
        ".."
    )
)

from feature_extractor import extract_features


def build_malicious():

    dataset_path = os.path.join(
        BASE_DIR,
        "..",
        "..",
        "datasets",
        "raw",
        "url",
        "malicious_phish.csv"
    )

    print(dataset_path)
    print(os.path.exists(dataset_path))

    df = pd.read_csv(
        dataset_path
    )

    rows = []

    for _, row in df.iterrows():

        features = extract_features(
            str(row["url"])
        )

        label = row["type"]

        if label == "benign":
            label = 0
        else:
            label = 1

        features["label"] = label

        rows.append(features)

    dataset = pd.DataFrame(
        rows
    )

    print(
        "\n===== MALICIOUS DATASET ====="
    )

    print(
        dataset.head()
    )

    print(
        dataset["label"].value_counts()
    )

    return dataset


if __name__ == "__main__":

    dataset = build_malicious()

    print(
        dataset.shape
    )