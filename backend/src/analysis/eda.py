import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def dataset_summary(df: pd.DataFrame) -> None:
    """
    Displays:
    - Shape
    - Columns
    - Missing Values
    - Data Types
    """
    print("=" * 50)
    print("DATASET SUMMARY")
    print("=" * 50)

    print(f"\nShape: {df.shape}")

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nData Types:")
    print(df.dtypes)


def missing_value_report(df: pd.DataFrame) -> pd.Series:
    """
    Returns missing value count for each column.
    """

    return df.isnull().sum()


def numerical_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns descriptive statistics for numerical columns.

    Includes:
    - count
    - mean
    - std
    - min
    - 25%
    - 50%
    - 75%
    - max
    """

    return df.describe()


def categorical_summary(df: pd.DataFrame) -> None:
    """
    Displays frequency counts for categorical columns.
    """

    categorical_cols = df.select_dtypes(
        include=["object", "category"]
    ).columns

    print("=" * 50)
    print("CATEGORICAL SUMMARY")
    print("=" * 50)

    if len(categorical_cols) == 0:
        print("No categorical columns found.")
        return

    for col in categorical_cols:
        print(f"\n{col}")
        print("-" * 30)
        print(df[col].value_counts(dropna=False))


def target_analysis(
    df: pd.DataFrame,
    target_column: str = "productivity_score"
) -> None:
    """
    Displays statistics of the target variable.
    """

    if target_column not in df.columns:
        print(f"{target_column} not found.")
        return

    target = df[target_column]

    print("=" * 50)
    print("TARGET ANALYSIS")

    print(f"Mean   : {target.mean():.2f}")
    print(f"Median : {target.median():.2f}")
    print(f"Min    : {target.min():.2f}")
    print(f"Max    : {target.max():.2f}")
    print(f"Std    : {target.std():.2f}")


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns correlation matrix for numerical columns.
    """

    numeric_df = df.select_dtypes(include=np.number)

    return numeric_df.corr()


def plot_correlation_matrix(df: pd.DataFrame) -> None:
    """
    Displays correlation heatmap.
    """

    corr_matrix = correlation_matrix(df)

    plt.figure(figsize=(10, 8))

    plt.imshow(
        corr_matrix,
        cmap="coolwarm",
        vmin=-1,
        vmax=1
    )

    plt.colorbar()

    plt.xticks(
        range(len(corr_matrix.columns)),
        corr_matrix.columns,
        rotation=90
    )

    plt.yticks(
        range(len(corr_matrix.columns)),
        corr_matrix.columns
    )

    plt.title("Correlation Matrix")
    plt.tight_layout()
    plt.show()


def plot_productivity_distribution(
    df: pd.DataFrame,
    target_column: str = "productivity_score"
) -> None:
    """
    Plots histogram of productivity scores.
    """

    if target_column not in df.columns:
        print(f"{target_column} not found.")
        return

    plt.figure(figsize=(8, 5))

    plt.hist(
        df[target_column],
        bins=20
    )

    plt.title("Productivity Score Distribution")
    plt.xlabel("Productivity Score")
    plt.ylabel("Frequency")

    plt.tight_layout()
    plt.show()


def feature_relationships(
    df: pd.DataFrame,
    target_column: str = "productivity_score"
) -> None:
    """
    Creates scatter plots of important features
    against productivity score.
    """

    features = [
        "sleep_hours",
        "study_hours",
        "screen_time",
        "exercise_minutes",
        "mood_score",
        "energy_level"
    ]

    for feature in features:

        if feature not in df.columns:
            continue

        plt.figure(figsize=(6, 4))

        plt.scatter(
            df[feature],
            df[target_column]
        )

        plt.xlabel(feature)
        plt.ylabel(target_column)

        plt.title(
            f"{feature} vs {target_column}"
        )

        plt.tight_layout()
        plt.show()