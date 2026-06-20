from database.crud import get_logs_dataframe

from src.analytics.daily import get_daily_summary
from src.analytics.weekly import get_weekly_summary
from src.analytics.monthly import get_monthly_summary
from src.analytics.streaks import get_streak_summary
from src.analytics.subject import get_subject_analytics


def run_analytics_tests():
    print("=" * 50)
    print("LOADING DATA")
    print("=" * 50)

    df = get_logs_dataframe()

    print(df.head())
    print(f"\nTotal Rows: {len(df)}")

    print("\n" + "=" * 50)
    print("DAILY ANALYTICS")
    print("=" * 50)

    latest_date = df["date"].max()

    daily_summary = get_daily_summary(df, latest_date)

    print(daily_summary)

    print("\n" + "=" * 50)
    print("WEEKLY ANALYTICS")
    print("=" * 50)

    weekly_summary = get_weekly_summary(df)

    print(weekly_summary)

    print("\n" + "=" * 50)
    print("MONTHLY ANALYTICS")
    print("=" * 50)

    monthly_summary = get_monthly_summary(df)

    print(monthly_summary)

    print("\n" + "=" * 50)
    print("STREAK ANALYTICS")
    print("=" * 50)

    streak_summary = get_streak_summary(df)

    print(streak_summary)

    print("\n" + "=" * 50)
    print("SUBJECT ANALYTICS")
    print("=" * 50)

    subject_summary = get_subject_analytics(df)

    print(subject_summary)

    print("\n" + "=" * 50)
    print("ALL ANALYTICS TESTS PASSED")
    print("=" * 50)


if __name__ == "__main__":
    run_analytics_tests()