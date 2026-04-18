import sqlite3
import os

DB_PATH = "data/patients.db"

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    heart_rate INTEGER,
    oxygen INTEGER,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Insert demo data
sample_data = [
    ("Rahul Das", 45, 130, 88, "High Risk"),
    ("Ananya Roy", 30, 85, 97, "Low Risk"),
    ("Suman Ghosh", 60, 105, 93, "Medium Risk"),
    ("Priya Sen", 50, 120, 89, "High Risk"),
    ("Arjun Paul", 25, 78, 99, "Low Risk")
]

cursor.executemany("""
INSERT INTO patients (name, age, heart_rate, oxygen, status)
VALUES (?, ?, ?, ?, ?)
""", sample_data)

conn.commit()
conn.close()

print("✅ patients.db created with demo data!")
