# create_db.py
import sqlite3
import os

DB_PATH = os.path.join("data", "users.db")

os.makedirs("data", exist_ok=True)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Drop the old table
# c.execute("DROP TABLE IF EXISTS users")

c.execute('''
CREATE TABLE IF NOT EXISTS users (
    fullname TEXT NOT NULL,
    email TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    cpass TEXT NOT NULL
)
''')

# c.execute("DELETE FROM users WHERE fullname = ?", ("Pradip Gosh",))

# Insert sample users
c.execute("INSERT OR IGNORE INTO users (fullname, email, password, cpass) VALUES (?, ?, ?, ?)", ("admin", "admin@yahoo.com", "9999", "9999"))

conn.commit()
conn.close()

print("✅ Database created successfully at:", DB_PATH)
