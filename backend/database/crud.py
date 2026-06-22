from database.db import get_connection
import pandas as pd


def insert_study_log(
    username: str,
    date: str,
    sleep_hours: float,
    study_hours: float,
    screen_time: float,
    exercise_minutes: int,
    mood_score: int,
    energy_level: int,
    task_difficulty: int,
    study_sessions: int,
    distractions: int,
    goal_completion: float,
    subject: str,
    productivity_rating: float
) -> None:
    """
    Insert a single study log row for a specific user.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO study_logs (
            username,
            date,
            sleep_hours,
            study_hours,
            screen_time,
            exercise_minutes,
            mood_score,
            energy_level,
            task_difficulty,
            study_sessions,
            distractions,
            goal_completion,
            subject,
            productivity_rating
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        username,
        date,
        sleep_hours,
        study_hours,
        screen_time,
        exercise_minutes,
        mood_score,
        energy_level,
        task_difficulty,
        study_sessions,
        distractions,
        goal_completion,
        subject,
        productivity_rating
    ))

    conn.commit()
    conn.close()


def get_all_logs() -> list:
    """
    Return all rows from study_logs (all users).
    Primarily useful for admin / retraining purposes.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM study_logs")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_logs_dataframe(username: str) -> pd.DataFrame:
    """
    Return all logs for a specific user as a DataFrame.

    Parameters
    ----------
    username : str
        The user whose logs to fetch.

    Returns
    -------
    pd.DataFrame
        Logs filtered to the given username.
    """
    conn = get_connection()
    query = "SELECT * FROM study_logs WHERE username = ?"
    df = pd.read_sql_query(query, conn, params=(username,))
    conn.close()
    return df


def get_all_logs_dataframe() -> pd.DataFrame:
    """
    Return every row across all users as a DataFrame.
    Use only for model retraining, not for user-facing analytics.
    """
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM study_logs", conn)
    conn.close()
    return df