from src.models.load_model import load_model

path= r"C:\Users\Smarth Sharma\Desktop\StudyIntel-1\backend\artifacts\trained models\catboost_v1.pkl"

model = load_model(path)

def predict_productivity(input_df):
    """
    Predict productivity using the loaded model.

    Args:
        input_df (pd.DataFrame): Input data for prediction.

    Returns:
        float: Predicted productivity value.
    """
    prediction= model.predict(input_df)
    prediction = max(0,min(10,prediction[0]))
    return float(prediction)