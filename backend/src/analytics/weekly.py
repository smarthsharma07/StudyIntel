import pandas as pd
from src.utils.aggregation import get_daily_aggregated
from src.utils.date_utils import fill_missing_dates

def get_weekly_summary(df):
    df=get_daily_aggregated(df)
    df=fill_missing_dates(df)
    df["date"] = pd.to_datetime(df["date"])

    latest_date = df["date"].max()

    week_start = latest_date - pd.Timedelta(days=6)

    weekly_df = df[
        (df["date"] >= week_start)
        &
        (df["date"] <= latest_date)
    ]

    if weekly_df.empty:
        return None
    consistency_score = (
        (weekly_df["study_hours"] > 0).sum()
        / 7
    ) * 100
    if weekly_df["productivity_rating"].notna().any():
        most_productive_day = str(
            weekly_df.loc[
                weekly_df["productivity_rating"].idxmax(),
                "date"
            ].date()
        )
    else:
        most_productive_day = None

    summary = {
        "week_start": str(week_start.date()),
        "week_end": str(latest_date.date()),
        "total_study_hours": float(
            weekly_df["study_hours"].sum()
        ),
        "average_daily_study_hours": float(
            weekly_df["study_hours"].sum() / 7
        ),
        "average_sleep_hours": float(
            weekly_df["sleep_hours"].mean()
        ),
        "average_mood_score": float(
            weekly_df["mood_score"].mean()
        ),
        "average_energy_level": float(
            weekly_df["energy_level"].mean()
        ),
        "average_productivity_rating": float(
            weekly_df["productivity_rating"].mean()
        ),
        "total_study_sessions": int(
            weekly_df["study_sessions"].sum()
        ),
        "consistency_score": float(
            round(consistency_score, 2)
        ),

        "most_productive_day": 
            most_productive_day
        
    }

    return summary