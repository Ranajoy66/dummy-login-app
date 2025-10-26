# create_db.py
import sqlite3
import os

DB_PATH = os.path.join("data", "users.db")

os.makedirs("data", exist_ok=True)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
)
''')

# Insert sample users
c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("admin", "admin123"))
c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("test", "test123"))

conn.commit()
conn.close()

print("✅ Database created successfully at:", DB_PATH)
