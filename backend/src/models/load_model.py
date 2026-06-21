import joblib

def load_model(model_path):
    """
    Load a machine learning model from a file.

    Args:
        model_path (str): The path to the model file.
    """
    return joblib.load(model_path)