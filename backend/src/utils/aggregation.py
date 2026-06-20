import pandas as pd

def get_daily_aggregated(df):
    df = df.copy()

    df["date"] = pd.to_datetime(df["date"])

    daily_aggregated_df = (
        df.groupby("date")
        .agg({
            "study_hours": "sum",
            "sleep_hours": "mean",
            "screen_time": "mean",
            "exercise_minutes": "sum",
            "mood_score": "mean",
            "energy_level": "mean",
            "task_difficulty": "mean",
            "study_sessions": "sum",
            "distractions": "sum",
            "goal_completion": "mean",
            "productivity_rating": "mean",
            "subject": lambda x: list(x.unique())
        })
        .reset_index()
    )

    return daily_aggregated_df