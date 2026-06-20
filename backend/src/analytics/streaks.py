from src.utils.aggregation import get_daily_aggregated
from src.utils.date_utils import fill_missing_dates

def get_current_streak(df):
    df = get_daily_aggregated(df)
    df = fill_missing_dates(df)

    df = df.sort_values("date")

    current_streak = 0

    for study_hours in reversed(df["study_hours"].tolist()):
        if study_hours > 0:
            current_streak += 1
        else:
            break

    return current_streak

def get_longest_streak(df):
    df = get_daily_aggregated(df)
    df = fill_missing_dates(df)

    df = df.sort_values("date")

    longest = 0
    current = 0

    for study_hours in df["study_hours"]:
        if study_hours > 0:
            current += 1
            longest = max(longest, current)
        else:
            current = 0

    return longest

def get_streak_summary(df):
    current_streak = get_current_streak(df)
    longest_streak = get_longest_streak(df)
    consistency_score = (
        (df["study_hours"] > 0).sum()
        / len(df)
    ) * 100
    summary = {
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "consistency_score": round(consistency_score, 2)
    }

    return summary