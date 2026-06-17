import pandas as pd
from sklearn.preprocessing import LabelEncoder


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing values.

    Numerical columns -> median
    Categorical columns -> mode
    """

    df = df.copy()

    numerical_cols = df.select_dtypes(include=["number"]).columns

    categorical_cols = df.select_dtypes(
        include=["object", "category"]
    ).columns

    for col in numerical_cols:
        df[col] = df[col].fillna(df[col].median())

    for col in categorical_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    return df


def encode_categorical_features(
    df: pd.DataFrame
) -> tuple[pd.DataFrame, dict]:
    """
    Label encodes categorical features.

    Returns:
    --------
    encoded dataframe
    encoders dictionary
    """

    df = df.copy()

    encoders = {}

    categorical_cols = df.select_dtypes(
        include=["object", "category"]
    ).columns

    for col in categorical_cols:

        encoder = LabelEncoder()

        df[col] = encoder.fit_transform(
            df[col].astype(str)
        )

        encoders[col] = encoder

    return df, encoders


def preprocess_data(
    df: pd.DataFrame
) -> tuple[pd.DataFrame, dict]:
    """
    Complete preprocessing pipeline.

    Steps:
    -------
    1. Missing Value Handling
    2. Categorical Encoding

    Returns:
    --------
    processed dataframe
    encoders
    """

    df = handle_missing_values(df)

    df, encoders = encode_categorical_features(df)

    return df, encoders