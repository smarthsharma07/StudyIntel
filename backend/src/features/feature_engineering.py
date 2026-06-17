import pandas as pd
import numpy as np


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates engineered features for StudyIntel.

    Engineered Features:
    --------------------
    study_efficiency
    distraction_rate
    screen_study_ratio
    wellness_score
    goal_efficiency
    optimal_sleep
    day_of_week
    month
    is_weekend
    is_exam_season
    """

    df = df.copy()
    # =====================================================
    # DATE FEATURES
    # =====================================================

    df["date"] = pd.to_datetime(df["date"])

    df["day_of_week"] = df["date"].dt.dayofweek

    df["month"] = df["date"].dt.month

    df["is_weekend"] = (
        df["day_of_week"]
        .isin([5, 6])
        .astype(int)
    )

    df["is_exam_season"] = (
        df["month"]
        .isin([3, 4, 5, 10, 11, 12])
        .astype(int)
    )
    # =====================================================
    # STUDY FEATURES
    # =====================================================

    df["study_efficiency"] = (
        df["study_hours"]
        / df["study_sessions"]
    )

    df["distraction_rate"] = (
        df["distractions"]
        / df["study_sessions"]
    )

    df["screen_study_ratio"] = (
        df["screen_time"]
        / df["study_hours"]
    )
    # =====================================================
    # WELLNESS FEATURES
    # =====================================================

    df["wellness_score"] = (
        (
            df["sleep_hours"]
            + df["mood_score"]
            + df["energy_level"]
            + (df["exercise_minutes"] / 30)
        )
        / 4
    )

    df["optimal_sleep"] = (
        (
            (df["sleep_hours"] >= 7)
            & (df["sleep_hours"] <= 9)
        )
        .astype(int)
    )
    # =====================================================
    # PERFORMANCE FEATURES
    # =====================================================
    df["goal_efficiency"] = (
        df["goal_completion"]
        / df["study_hours"]
    )
    # =====================================================
    # HANDLE INF VALUES
    # =====================================================

    df.replace(
        [np.inf, -np.inf],
        np.nan,
        inplace=True
    )

    return df