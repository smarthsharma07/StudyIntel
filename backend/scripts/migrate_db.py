"""
scripts/migrate_db.py
=====================
One-time migration script to add the 'username' column to an existing
study_logs.db that was created before multi-user support was added.

Run from the backend/ directory:
    python scripts/migrate_db.py

Safe to run multiple times – it checks for the column before adding it.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "study_logs.db"


def migrate():
    print(f"Opening database: {DB_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # Check whether 'username' column already exists
    cursor.execute("PRAGMA table_info(study_logs)")
    columns = [row[1] for row in cursor.fetchall()]

    if "username" in columns:
        print("'username' column already exists – nothing to do.")
        conn.close()
        return

    print("Adding 'username' column to study_logs table ...")
    cursor.execute(
        "ALTER TABLE study_logs ADD COLUMN username TEXT NOT NULL DEFAULT 'legacy_user'"
    )

    conn.commit()
    conn.close()
    print("Migration complete.")
    print(
        "NOTE: existing rows have been assigned username='legacy_user'.\n"
        "      Update them manually if you know their real usernames."
    )


if __name__ == "__main__":
    migrate()
