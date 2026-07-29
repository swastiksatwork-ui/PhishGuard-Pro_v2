from autogluon.tabular import TabularPredictor
import os

model_path = r"ml\models\url_model"

print(os.path.exists(model_path))

predictor = TabularPredictor.load(
    model_path
)

print(
    predictor.model_names()
)

print("MODEL LOADED SUCCESSFULLY")

print(
    predictor.leaderboard(
        silent=True
    )
)