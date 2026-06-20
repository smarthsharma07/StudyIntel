import pandas as pd


def get_subject_analytics(df):

    subject_summary = (
        df.groupby("subject")
        .agg(
            total_study_hours=("study_hours", "sum"),
            average_productivity_rating=("productivity_rating", "mean"),
            average_task_difficulty=("task_difficulty", "mean"),
            total_study_sessions=("study_sessions", "sum")
        )
        .reset_index()
    )

    subject_summary["study_percentage"] = (
        subject_summary["total_study_hours"]
        /
        subject_summary["total_study_hours"].sum()
    ) * 100

    most_studied_subject = subject_summary.loc[
        subject_summary["total_study_hours"].idxmax(),
        "subject"
    ]

    least_studied_subject = subject_summary.loc[
        subject_summary["total_study_hours"].idxmin(),
        "subject"
    ]

    summary = {
        "subject_breakdown": subject_summary.to_dict("records"),
        "most_studied_subject": most_studied_subject,
        "least_studied_subject": least_studied_subject
    }

    return summary