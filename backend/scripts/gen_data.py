import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================

np.random.seed(42)

N_ROWS = 18000

OUTPUT_PATH = Path(r"C:\Users\Smarth Sharma\Desktop\StudyIntel-1\backend\data\raw\study_logs.csv")

# ============================================================
# SUBJECTS
# ============================================================

subjects = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "English",
    "History",
    "Geography",
    "Economics",
    "Political Science",
    "Accountancy",
    "Business Studies",
    "Computer Science",
    "Programming",
    "Data Structures",
    "Machine Learning",
    "Database Systems",
    "Operating Systems",
    "Computer Networks",
    "Electronics",
    "Engineering Mathematics",
    "Reasoning",
    "Quantitative Aptitude",
    "Current Affairs",
    "Research",
    "Project Work",
    "Exam Revision"
]

difficulty_ranges = {
    "Mathematics": (6, 10),
    "Physics": (6, 10),
    "Chemistry": (5, 9),
    "Biology": (4, 8),
    "English": (2, 6),
    "History": (3, 7),
    "Geography": (3, 7),
    "Economics": (4, 8),
    "Political Science": (3, 7),
    "Accountancy": (5, 9),
    "Business Studies": (3, 7),
    "Computer Science": (5, 9),
    "Programming": (5, 10),
    "Data Structures": (6, 10),
    "Machine Learning": (7, 10),
    "Database Systems": (5, 9),
    "Operating Systems": (6, 10),
    "Computer Networks": (6, 10),
    "Electronics": (6, 10),
    "Engineering Mathematics": (6, 10),
    "Reasoning": (4, 8),
    "Quantitative Aptitude": (5, 9),
    "Current Affairs": (2, 6),
    "Research": (6, 10),
    "Project Work": (4, 8),
    "Exam Revision": (3, 8)
}

# ============================================================
# STUDENT TYPES
# ============================================================

student_types = [
    "Topper",
    "Average",
    "Crammer",
    "Distracted",
    "Burnout",
    "Active"
]

student_probs = [0.15, 0.40, 0.15, 0.15, 0.10, 0.05]

# ============================================================
# DATES
# ============================================================

start_date = pd.Timestamp("2020-01-01")
end_date = pd.Timestamp("2025-12-31")

total_days = (end_date - start_date).days

# ============================================================
# GENERATION
# ============================================================

rows = []

for _ in range(N_ROWS):

    random_day = np.random.randint(0, total_days)

    date = start_date + pd.Timedelta(days=random_day)

    month = date.month
    weekday = date.weekday()

    student_type = np.random.choice(
        student_types,
        p=student_probs
    )

    # --------------------------------------------------------
    # Student Profiles
    # --------------------------------------------------------

    if student_type == "Topper":
        sleep = np.random.normal(7.8, 0.8)
        study = np.random.normal(7.0, 1.2)
        screen = np.random.normal(2.5, 1)
        exercise = np.random.normal(40, 15)
        distractions = np.random.randint(0, 4)

    elif student_type == "Average":
        sleep = np.random.normal(7.0, 1)
        study = np.random.normal(5.0, 1.5)
        screen = np.random.normal(4.5, 1.5)
        exercise = np.random.normal(30, 15)
        distractions = np.random.randint(1, 6)

    elif student_type == "Crammer":
        sleep = np.random.normal(5.8, 1)
        study = np.random.normal(8.0, 2)
        screen = np.random.normal(4, 1)
        exercise = np.random.normal(15, 10)
        distractions = np.random.randint(2, 6)

    elif student_type == "Distracted":
        sleep = np.random.normal(6.5, 1)
        study = np.random.normal(2.5, 1)
        screen = np.random.normal(8.0, 2)
        exercise = np.random.normal(20, 10)
        distractions = np.random.randint(5, 11)

    elif student_type == "Burnout":
        sleep = np.random.normal(5.0, 1)
        study = np.random.normal(6.0, 2)
        screen = np.random.normal(5.5, 1.5)
        exercise = np.random.normal(10, 10)
        distractions = np.random.randint(3, 8)

    else:  # Active
        sleep = np.random.normal(7.5, 1)
        study = np.random.normal(5.5, 1.5)
        screen = np.random.normal(3.5, 1)
        exercise = np.random.normal(60, 20)
        distractions = np.random.randint(1, 5)

    # --------------------------------------------------------
    # Weekend Effect
    # --------------------------------------------------------

    if weekday >= 5:
        study *= 0.85
        screen *= 1.2
        exercise *= 1.15

    # --------------------------------------------------------
    # Exam Season Effect
    # --------------------------------------------------------

    if month in [3, 4, 5, 10, 11, 12]:
        study *= 1.2

    # --------------------------------------------------------
    # Subject
    # --------------------------------------------------------

    subject = np.random.choice(subjects)

    low, high = difficulty_ranges[subject]

    task_difficulty = np.random.randint(low, high + 1)

    # --------------------------------------------------------
    # Clip Values
    # --------------------------------------------------------

    sleep = round(np.clip(sleep, 2, 10), 1)
    study = round(np.clip(study, 0.5, 12), 1)
    screen = round(np.clip(screen, 0.5, 14), 1)

    exercise = int(np.clip(exercise, 0, 120))

    study_sessions = np.random.randint(1, 8)

    mood = np.clip(
        5
        + 0.30 * sleep
        + 0.015 * exercise
        - 0.15 * distractions
        + np.random.normal(0, 1),
        1,
        10
    )

    energy = np.clip(
        4
        + 0.45 * sleep
        + 0.01 * exercise
        - 0.10 * screen
        + np.random.normal(0, 1),
        1,
        10
    )

    goal_completion = np.clip(
        25
        + study * 8
        + mood * 2
        - distractions * 2
        + np.random.normal(0, 8),
        0,
        100
    )

    productivity_score = (
        0.25 * sleep
        + 0.70 * study
        + 0.40 * mood
        + 0.50 * energy
        + 0.03 * goal_completion
        + 0.01 * exercise
        - 0.30 * distractions
        - 0.15 * screen
        - 0.10 * task_difficulty
        + np.random.normal(0, 1)
    )

    productivity_rating = int(
        np.clip(
            round(productivity_score),
            1,
            10
        )
    )

    rows.append([
        date.strftime("%Y-%m-%d"),
        sleep,
        study,
        screen,
        exercise,
        round(mood, 1),
        round(energy, 1),
        task_difficulty,
        study_sessions,
        distractions,
        round(goal_completion, 0),
        subject,
        productivity_rating
    ])

# ============================================================
# DATAFRAME
# ============================================================

columns = [
    "date",
    "sleep_hours",
    "study_hours",
    "screen_time",
    "exercise_minutes",
    "mood_score",
    "energy_level",
    "task_difficulty",
    "study_sessions",
    "distractions",
    "goal_completion",
    "subject",
    "productivity_rating"
]

df = pd.DataFrame(rows, columns=columns)

# ============================================================
# MISSING VALUES (3%)
# ============================================================

for col in [
    "sleep_hours",
    "exercise_minutes",
    "mood_score",
    "energy_level"
]:
    mask = np.random.rand(len(df)) < 0.03
    df.loc[mask, col] = np.nan

# ============================================================
# OUTLIERS (1%)
# ============================================================

outlier_rows = np.random.choice(
    df.index,
    size=int(len(df) * 0.01),
    replace=False
)

df.loc[outlier_rows, "screen_time"] = np.random.uniform(
    12,
    16,
    len(outlier_rows)
)

# ============================================================
# SAVE
# ============================================================

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("=" * 50)
print("Dataset Generated Successfully")
print("=" * 50)
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Saved to: {OUTPUT_PATH}")
print()
print(df.head())