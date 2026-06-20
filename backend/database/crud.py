from database.db import get_connection
import pandas as pd

def insert_study_log(
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
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO study_logs (
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
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
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


def get_all_logs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM study_logs")

    rows = cursor.fetchall()

    conn.close()

    return rows

def get_logs_dataframe():
    conn = get_connection()
    query = "SELECT * FROM study_logs"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df