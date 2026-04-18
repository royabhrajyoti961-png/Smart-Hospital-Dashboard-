import sqlite3
import os

DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "patients.db")

def connect_db():
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

def insert_patient(name, age, hr, oxygen, status):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO patients (name, age, heart_rate, oxygen, status)
    VALUES (?, ?, ?, ?, ?)
    """, (name, age, hr, oxygen, status))

    conn.commit()
    conn.close()

def get_all_patients():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients ORDER BY created_at DESC")
    data = cursor.fetchall()

    conn.close()
    return data
