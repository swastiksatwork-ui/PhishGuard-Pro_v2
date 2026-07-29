import os
import pandas as pd

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

dataset_path = os.path.join(
    BASE_DIR,
    "..",
    "datasets",
    "raw",
    "threat",
    "urlhaus-04-Nov-2024-alpaca-dataset.json"
)

df = pd.read_json(
    dataset_path
)

print(
    f"Loaded {len(df)} URLHaus records"
)


def search_ioc(search_text):

    search_text = str(
        search_text
    ).lower()

    matches = []

    for _, row in df.iterrows():

        input_text = str(
            row["input"]
        ).lower()

        if search_text in input_text:

            matches.append({
                "type": "ioc_match",
                "confidence": "high",
                "instruction": row["instruction"],
                "input": row["input"]
            })

    return matches[:20]


if __name__ == "__main__":

    results = search_ioc(
        "Mozi"
    )

    print(
        f"Matches: {len(results)}"
    )

    print(
        results[:3]
    )