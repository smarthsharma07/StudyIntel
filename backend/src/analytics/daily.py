import pandas as pd

def get_daily_summary(df, date):
    daily_df = df[df["date"] == date]

    if daily_df.empty:
        return None

    summary = {
    "date": date,
    "total_study_hours": float(daily_df["study_hours"].sum()),
    "average_sleep_hours": float(daily_df["sleep_hours"].mean()),
    "average_screen_time": float(daily_df["screen_time"].mean()),
    "total_exercise_minutes": int(daily_df["exercise_minutes"].sum()),
    "average_mood_score": float(daily_df["mood_score"].mean()),
    "average_energy_level": float(daily_df["energy_level"].mean()),
    "average_task_difficulty": float(daily_df["task_difficulty"].mean()),
    "total_study_sessions": int(daily_df["study_sessions"].sum()),
    "total_distractions": int(daily_df["distractions"].sum()),
    "average_goal_completion": float(daily_df["goal_completion"].mean()),
    "average_productivity_rating": float(daily_df["productivity_rating"].mean()),
    "subjects_studied": daily_df["subject"].unique().tolist(),
    "number_of_subjects": int(daily_df["subject"].nunique())
}

    return summary