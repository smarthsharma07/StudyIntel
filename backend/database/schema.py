from database.db import get_connection


def create_study_logs_table():
    """
    Create the study_logs table with username support.
    Run this once to initialise a fresh database.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_logs (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        username            TEXT    NOT NULL,
        date                TEXT    NOT NULL,
        sleep_hours         REAL,
        study_hours         REAL,
        screen_time         REAL,
        exercise_minutes    INTEGER,
        mood_score          INTEGER,
        energy_level        INTEGER,
        task_difficulty     INTEGER,
        study_sessions      INTEGER,
        distractions        INTEGER,
        goal_completion     REAL,
        subject             TEXT,
        productivity_rating REAL
    )
    """)

    conn.commit()
    conn.close()