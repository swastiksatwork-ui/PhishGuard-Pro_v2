from autogluon.tabular import TabularPredictor

predictor = TabularPredictor.load(
    "ml/models/feature_model"
)

print(
    predictor.feature_metadata_in.get_features()
)