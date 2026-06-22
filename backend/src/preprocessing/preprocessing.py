import pandas as pd
from sklearn.preprocessing import LabelEncoder


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing values.

    Numerical columns  -> median
    Categorical (str)  -> 'Unknown'
    """
    df = df.copy()

    numerical_cols = df.select_dtypes(include=["number"]).columns

    # T3: Do NOT use LabelEncoder on categorical cols.
    # CatBoost handles string categoricals natively and is robust
    # to unseen category values (e.g. new subjects the model has
    # never seen during training).  We only fill NaN with 'Unknown'
    # so CatBoost receives a valid string rather than NaN.
    categorical_cols = df.select_dtypes(
        include=["object", "category"]
    ).columns

    for col in numerical_cols:
        df[col] = df[col].fillna(df[col].median())

    for col in categorical_cols:
        df[col] = df[col].fillna("Unknown").astype(str)

    return df


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Complete preprocessing pipeline for CatBoost inference.

    Steps
    -----
    1. Fill missing values (numerics → median, categoricals → 'Unknown').

    IMPORTANT: No LabelEncoder / OrdinalEncoder / OneHotEncoder is applied
    here.  CatBoost was trained with raw string categoricals (cat_features
    parameter) and must receive the same format at inference time.
    Encoding categoricals at inference breaks on any subject that was unseen
    during training (LabelEncoder raises ValueError for unknown labels).

    Returns
    -------
    pd.DataFrame
        Preprocessed dataframe ready for feature-column selection and
        model.predict().
    """
    df = handle_missing_values(df)
    return df