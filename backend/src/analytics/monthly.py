import pandas as pd

from src.utils.aggregation import get_daily_aggregated
from src.utils.date_utils import fill_missing_dates


def get_monthly_summary(df):
    df = get_daily_aggregated(df)
    df = fill_missing_dates(df)

    latest_date = df["date"].max()

    month_start = latest_date.replace(day=1)

    monthly_df = df[
        (df["date"] >= month_start)
        &
        (df["date"] <= latest_date)
    ]

    if monthly_df.empty:
        return None

    days_in_period = len(monthly_df)

    consistency_score = (
        (monthly_df["study_hours"] > 0).sum()
        / days_in_period
    ) * 100

    if monthly_df["productivity_rating"].notna().any():
        most_productive_day = str(
            monthly_df.loc[
                monthly_df["productivity_rating"].idxmax(),
                "date"
            ].date()
        )
    else:
        most_productive_day = None

    summary = {
        "month_start": str(month_start.date()),
        "month_end": str(latest_date.date()),

        "total_study_hours": float(
            monthly_df["study_hours"].sum()
        ),

        "average_daily_study_hours": float(
            monthly_df["study_hours"].mean()
        ),

        "average_sleep_hours": float(
            monthly_df["sleep_hours"].mean()
        ),

        "average_screen_time": float(
            monthly_df["screen_time"].mean()
        ),

        "average_mood_score": float(
            monthly_df["mood_score"].mean()
        ),

        "average_energy_level": float(
            monthly_df["energy_level"].mean()
        ),

        "average_task_difficulty": float(
            monthly_df["task_difficulty"].mean()
        ),

        "average_goal_completion": float(
            monthly_df["goal_completion"].mean()
        ),

        "average_productivity_rating": float(
            monthly_df["productivity_rating"].mean()
        ),

        "total_study_sessions": int(
            monthly_df["study_sessions"].sum()
        ),

        "total_exercise_minutes": int(
            monthly_df["exercise_minutes"].sum()
        ),

        "total_distractions": int(
            monthly_df["distractions"].sum()
        ),

        "consistency_score": float(
            round(consistency_score, 2)
        ),

        "most_productive_day": most_productive_day
    }

    return summary