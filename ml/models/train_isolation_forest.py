from sklearn.ensemble import IsolationForest
import pandas as pd
import joblib

from sklearn.ensemble import IsolationForest

dataset_path = (
    "ml/datasets/raw/isolation_forest/"
    "isolation_dataset.csv"
)

df = pd.read_csv(
    dataset_path
)

print(
    "\nRows:",
    len(df)
)

print(
    "Columns:",
    len(df.columns)
)

model = IsolationForest(

    n_estimators=200,

    contamination=0.1,

    random_state=42

)

model.fit(
    df
)

joblib.dump(

    model,

    "ml/models/isolation_forest/"
    "isolation_forest.pkl"

)

print(
    "\nIsolation Forest trained!"
)

print(
    "Saved:",
    "ml/models/isolation_forest/"
    "isolation_forest.pkl"
)