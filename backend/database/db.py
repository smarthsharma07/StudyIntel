import sqlite3
from pathlib import Path

def get_connection():
    db_path = Path(__file__).resolve().parent.parent / "study_logs.db"
    conn = sqlite3.connect(str(db_path))
    return conn