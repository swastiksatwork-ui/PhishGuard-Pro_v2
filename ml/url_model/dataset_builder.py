import os
import pandas as pd

from builders.alexa_builder import build_alexa
from builders.majestic_builder import build_majestic
from builders.phishtank_builder import build_phishtank
from builders.malicious_builder import build_malicious


print("Building Alexa...")
alexa_df = build_alexa()

print("Building Majestic...")
majestic_df = build_majestic()

print("Building PhishTank...")
phishtank_df = build_phishtank()

print("Building Malicious...")
malicious_df = build_malicious()

print("\nMerging datasets...")

combined_df = pd.concat(
    [
        alexa_df,
        majestic_df,
        phishtank_df,
        malicious_df
    ],
    ignore_index=True
)

print("\n===== COMBINED DATASET =====")
print(combined_df.head())
print(combined_df.shape)

print(alexa_df.shape)

print(majestic_df.shape)

print(phishtank_df.shape)

print("\n===== LABEL COUNTS =====")
print(
    combined_df["label"].value_counts()
)

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

save_path = os.path.join(
    BASE_DIR,
    "features",
    "combined_url_dataset.csv"
)

combined_df.to_csv(
    save_path,
    index=False
)

print(
    f"\nSaved: {save_path}"
)