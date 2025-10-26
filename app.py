# app.py
import streamlit as st
import sqlite3
from utils import make_hashes, check_hashes, update_github_db_and_csv, DB_PATH

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:   # use 'user' instead of 'username' for logic
    st.session_state.user = ""

st.set_page_config(page_title="Login System", page_icon="🔐", layout="centered")

st.title("🔐 Global Login App (with GitHub Synced DB)")

menu = ["Login", "Sign Up"]
choice = st.sidebar.selectbox("Menu", menu)

def login_user(username, password):
    import sqlite3
    conn = sqlite3.connect('data/users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    data = c.fetchone()
    conn.close()
    return data


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if choice == "Login":
    st.subheader("Login Section")
    username = st.text_input("Username",key="login_username")
    password = st.text_input("Password", type='password',key="login_password")
    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.success(f"Welcome {username}!")
            st.session_state.logged_in = True
            st.session_state.username = username
        else:
            st.error("Invalid username or password.")

elif choice == "Sign Up":
    st.subheader("Create New Account")
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type='password')
    token = st.secrets["GITHUB_TOKEN"]

    if st.button("Sign Up"):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                      (new_user, new_pass))
            conn.commit()
            st.success("🎉 Account created successfully!")
            st.info("You can now log in.")
            if token:
                update_github_db_and_csv(token)
        except sqlite3.IntegrityError:
            st.error("Username already exists.")
        conn.close()

if st.session_state.logged_in:
    st.success(f"✅ You are logged in as {st.session_state.username}")
    if st.button("Logout"):
        for key in ["logged_in", "user", "login_username", "login_password"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
