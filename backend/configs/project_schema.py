# | Column             | Type     | Range               |
# | ------------------ | -------- | ------------------- |
# | date               | Date     | YYYY-MM-DD          |
# | sleep_hours        | Float    | 0–12                |
# | study_hours        | Float    | 0–16                |
# | screen_time        | Float    | 0–24                |
# | exercise_minutes   | Integer  | 0–180               |
# | mood_score         | Integer  | 1–10                |
# | energy_level       | Integer  | 1–10                |
# | task_difficulty    | Integer  | 1–5                 |
# | study_sessions     | Integer  | 1–20                |
# | distractions       | Integer  | 0+                  |
# | goal_completion    | Float    | 0–100               |
# | subject            | Category | DSA, ML, Math, etc. |
# | productivity_rating | Integer  | 1–10                |
#Target column - productivity_rating


DAILY_LOG_COLUMNS = [
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

