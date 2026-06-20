import pandas as pd


def fill_missing_dates(df):
    df = df.copy()

    df["date"] = pd.to_datetime(df["date"])

    all_dates = pd.date_range(
        start=df["date"].min(),
        end=df["date"].max(),
        freq="D"
    )

    full_df = pd.DataFrame({
        "date": all_dates
    })

    full_df = full_df.merge(
        df,
        on="date",
        how="left"
    )

    zero_fill_columns = [
        "study_hours",
        "exercise_minutes",
        "study_sessions",
        "distractions"
    ]

    for col in zero_fill_columns:
        if col in full_df.columns:
            full_df[col] = full_df[col].fillna(0)

    return full_df