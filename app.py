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

def login_user(email, password):
    import sqlite3
    conn = sqlite3.connect('data/users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    data = c.fetchone()
    conn.close()
    return data


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if choice == "Login":
    st.subheader("Login Section")
    email = st.text_input("Username",key="login_email")
    password = st.text_input("Password", type='password',key="login_password")
    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.success(f"Welcome {email}!")
            st.session_state.logged_in = True
            st.session_state.email = email
        else:
            st.error("Invalid username or password.")

elif choice == "Sign Up":
    st.subheader("Create New Account")
    fullname=st.text_input("Full Name")
    email=st.text_input("Email")
    password = st.text_input("Password", type='password')
    cpass = st.text_input("Confirm Password", type='password')
    token = st.secrets["GITHUB_TOKEN"]

    if st.button("Sign Up"):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        try:
            c.execute(
                'INSERT INTO users (fullname, email, password, cpass) VALUES (?, ?, ?, ?)',
                (fullname, email, password, cpass)
            )

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
        for key in ["logged_in", "user", "login_email", "login_password"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
