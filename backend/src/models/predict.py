from pathlib import Path
from src.models.load_model import load_model

# T4: model loads exactly ONCE at module import time.
# predict_productivity() is called N times without reloading the model.
_MODEL_PATH = Path(__file__).resolve().parent.parent.parent / \
    "artifacts" / "trained models" / "catboost_v1.pkl"

model = load_model(str(_MODEL_PATH))


def predict_productivity(input_df):
    """
    Predict productivity using the pre-loaded CatBoost model.

    Parameters
    ----------
    input_df : pd.DataFrame
        Single-row dataframe containing ONLY the features the model was
        trained on (model.feature_names_).
        Must NOT include 'productivity_rating' or 'date'
        (those are dropped upstream in the pipeline).

    Returns
    -------
    float
        Predicted productivity score clipped to [0, 10].
    """
    prediction = model.predict(input_df)
    prediction = max(0, min(10, prediction[0]))
    return float(prediction)