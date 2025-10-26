# utils.py
import hashlib
import sqlite3
import base64
import requests
import os
import json
import pandas as pd
from datetime import datetime

# ===== Basic Settings =====
DB_PATH = os.path.join("data", "users.db")
GITHUB_REPO = "Ranajoy66/dummy-login-app"   # 🔹 Change this to your repo name
DB_FILE_PATH = "data/users.db"
PUBLIC_CSV_PATH = "data/users_public.csv"
BRANCH = "main"

# ===== Password Hashing =====
def make_hashes(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

# ===== Database Export =====
def export_public_csv():
    """Export usernames and plain-text passwords for public view (demo purpose)."""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query("SELECT username, password FROM users", conn)
    finally:
        conn.close()

    # Save to CSV with clear table structure
    df.to_csv(PUBLIC_CSV_PATH, index=False)
    print("✅ Exported users_public.csv with usernames and passwords")


# ===== GitHub Sync =====
def _commit_file_to_github(file_path, github_path, token, commit_message):
    """Commit a file to GitHub repo."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{github_path}"
    headers = {"Authorization": f"token {token}"}

    with open(file_path, "rb") as f:
        content = base64.b64encode(f.read()).decode()

    # Check if file already exists (to get SHA)
    response = requests.get(url, headers=headers)
    sha = response.json().get("sha") if response.status_code == 200 else None

    data = {
        "message": commit_message,
        "content": content,
        "branch": BRANCH,
    }
    if sha:
        data["sha"] = sha

    r = requests.put(url, headers=headers, data=json.dumps(data))
    if r.status_code in [200, 201]:
        print(f"✅ {os.path.basename(file_path)} updated on GitHub.")
    else:
        print(f"⚠️ Failed to update {os.path.basename(file_path)}:", r.json())

def update_github_db_and_csv(token):
    """Push both users.db and users_public.csv to GitHub."""
    export_public_csv()
    commit_message = f"Update users.db and users_public.csv ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"
    _commit_file_to_github(DB_PATH, DB_FILE_PATH, token, commit_message)
    _commit_file_to_github(PUBLIC_CSV_PATH, PUBLIC_CSV_PATH, token, commit_message)
