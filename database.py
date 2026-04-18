import sqlite3
import os

DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "patients.db")

def connect_db():
    # Ensure directory exists (VERY IMPORTANT for Streamlit Cloud)
    os.makedirs(DB_DIR, exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        heart_rate INTEGER,
        oxygen INTEGER,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
