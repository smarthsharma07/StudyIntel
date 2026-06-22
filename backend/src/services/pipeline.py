"""
services/pipeline.py
====================
Production backend pipeline for StudyIntel.

Flow
----
User Input
  → Validation
  → Save to SQLite  (user-scoped)
  → Fetch User History  (user-scoped)
  → Analytics
  → Feature Engineering
  → Preprocessing  (no LabelEncoder – CatBoost-safe)
  → Select model features / drop target + date  (T2: leakage fix)
  → Prediction
  → SHAP Explanation  (same df as prediction)
  → Return Results
"""

from typing import Dict, Any

import pandas as pd

# DATA
from src.data.study_log import StudyLog
from src.data.validator import validate_study_log

# DATABASE
from database.crud import (
    insert_study_log,
    get_logs_dataframe,
)

# ANALYTICS
from src.analytics.daily import get_daily_summary
from src.analytics.weekly import get_weekly_summary
from src.analytics.monthly import get_monthly_summary
from src.analytics.streaks import get_streak_summary

# FEATURES
from src.features.feature_engineering import engineer_features

# PREPROCESSING
from src.preprocessing.preprocessing import preprocess_data

# MODEL  (model object is loaded once at module-import time in predict.py)
from src.models.predict import predict_productivity, model

# SHAP
from src.explainability.explain import explain_prediction


# Columns that must NEVER be fed to the model.
# 'date'               – temporal identifier, not a feature.
# 'productivity_rating'– this IS the target (T2: data leakage prevention).
# 'id', 'username'     – database artefacts.
_COLUMNS_TO_DROP = {"date", "productivity_rating", "id", "username"}


def process_study_log(
    username: str,
    study_log_dict: Dict[str, Any],
) -> Dict[str, Any]:
    """
    End-to-end pipeline for a single study log submission.

    Parameters
    ----------
    username : str
        The authenticated user submitting the log.
        Used to scope all database reads/writes.
    study_log_dict : dict
        Raw user input matching the StudyLog schema.
        Must NOT include 'username' – that is injected here.

    Returns
    -------
    dict with keys:
        'prediction'  – float [0, 10]
        'analytics'   – dict (daily / weekly / monthly / streaks)
        'shap'        – dict from explain_prediction()
    """

    # ------------------------------------------------------------------
    # 1. VALIDATION
    # ------------------------------------------------------------------
    # Build the dataclass so validate_study_log has the right type.
    log_obj = StudyLog(username=username, **study_log_dict)

    is_valid = validate_study_log(log_obj)
    if not is_valid:
        raise ValueError(
            f"StudyLog validation failed for user='{username}'. "
            f"Check field ranges in validation_rules.py."
        )

    # ------------------------------------------------------------------
    # 2. SAVE TO DATABASE  (T1: username stored with every row)
    # ------------------------------------------------------------------
    insert_study_log(
        username=username,
        date=log_obj.date,
        sleep_hours=log_obj.sleep_hours,
        study_hours=log_obj.study_hours,
        screen_time=log_obj.screen_time,
        exercise_minutes=log_obj.exercise_minutes,
        mood_score=log_obj.mood_score,
        energy_level=log_obj.energy_level,
        task_difficulty=log_obj.task_difficulty,
        study_sessions=log_obj.study_sessions,
        distractions=log_obj.distractions,
        goal_completion=log_obj.goal_completion,
        subject=log_obj.subject,
        productivity_rating=log_obj.productivity_rating,
    )

    # ------------------------------------------------------------------
    # 3. FETCH USER HISTORY  (T1: user-scoped query)
    # ------------------------------------------------------------------
    user_history_df = get_logs_dataframe(username)

    # ------------------------------------------------------------------
    # 4. ANALYTICS  (T1: operate on a single user's history)
    # ------------------------------------------------------------------
    analytics = {
        "daily":   get_daily_summary(user_history_df, log_obj.date),
        "weekly":  get_weekly_summary(user_history_df),
        "monthly": get_monthly_summary(user_history_df),
        "streaks": get_streak_summary(user_history_df),
    }

    # ------------------------------------------------------------------
    # 5. FEATURE ENGINEERING
    # Input: raw log dict as a single-row DataFrame.
    # Note: productivity_rating is kept here because engineer_features
    # is a pure transform that does not use the target column.
    # ------------------------------------------------------------------
    raw_df = pd.DataFrame([study_log_dict])
    engineered_df = engineer_features(raw_df)

    # ------------------------------------------------------------------
    # 6. PREPROCESSING  (T3: no LabelEncoder – CatBoost-safe strings)
    # ------------------------------------------------------------------
    processed_df = preprocess_data(engineered_df)

    # ------------------------------------------------------------------
    # 7. SELECT EXACT MODEL FEATURES  (T2: drop target + date)
    # ------------------------------------------------------------------
    # model.feature_names_ is the ground truth of what the model expects.
    # This also guarantees feature ORDER is identical to training (T5).
    predict_df = processed_df[model.feature_names_].copy()

    # Extra safety: assert none of the leaked columns slipped through.
    leaked = _COLUMNS_TO_DROP & set(predict_df.columns)
    if leaked:
        raise RuntimeError(
            f"Data leakage detected: columns {leaked} present in "
            f"predict_df. This must never happen."
        )

    # Ensure subject (and any other object column) is str, not NaN.
    for col in predict_df.select_dtypes(include=["object"]).columns:
        predict_df[col] = predict_df[col].astype(str)

    # ------------------------------------------------------------------
    # 8. PREDICTION
    # ------------------------------------------------------------------
    prediction = predict_productivity(predict_df)

    # ------------------------------------------------------------------
    # 9. SHAP EXPLANATION  (T5: same predict_df used for prediction)
    # ------------------------------------------------------------------
    shap_results = explain_prediction(
        model=model,
        prediction_df=predict_df,
        top_n=5,
    )

    # ------------------------------------------------------------------
    # RETURN
    # ------------------------------------------------------------------
    return {
        "prediction": prediction,
        "analytics":  analytics,
        "shap":       shap_results,
    }