import sqlite3
def get_connection():
    conn = sqlite3.connect('study_logs.db')
    return conn