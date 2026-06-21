import pandas as pd
import shap


def explain_prediction(
    model,
    prediction_df: pd.DataFrame,
    top_n: int = 5
) -> dict:
    """
    Generate SHAP explanations for a prediction.

    Parameters
    ----------
    model : trained CatBoost model

    prediction_df : pd.DataFrame
        Single-row dataframe used for prediction.

    top_n : int
        Number of positive/negative factors to return.

    Returns
    -------
    dict
    """

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(
        prediction_df
    )

    prediction = model.predict(
        prediction_df
    )[0]

    base_value = float(
        explainer.expected_value
    )

    explanation_df = pd.DataFrame({
        "feature": prediction_df.columns,
        "value": prediction_df.iloc[0].values,
        "shap_value": shap_values[0]
    })

    positive_factors = (
        explanation_df[
            explanation_df["shap_value"] > 0
        ]
        .sort_values(
            "shap_value",
            ascending=False
        )
        .head(top_n)
    )

    negative_factors = (
        explanation_df[
            explanation_df["shap_value"] < 0
        ]
        .sort_values(
            "shap_value"
        )
        .head(top_n)
    )

    return {
        "prediction": prediction,
        "base_value": base_value,
        "positive_factors": positive_factors,
        "negative_factors": negative_factors,
        "shap_dataframe": explanation_df
    }