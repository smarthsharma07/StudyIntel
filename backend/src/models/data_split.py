import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def prepare_train_test_data(
    df: pd.DataFrame,
    target_column: str = "productivity_rating",
    test_size: float = 0.2,
    random_state: int = 42
):
    """
    Splits dataframe into train and test sets.

    Returns:
    --------
    X_train
    X_test
    y_train
    y_test
    """

    X = df.drop(
        columns=[
            target_column,
            "date"
        ]
    )

    y = df[target_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state
    )

    return (
        X_train,
        X_test,
        y_train,
        y_test
    )