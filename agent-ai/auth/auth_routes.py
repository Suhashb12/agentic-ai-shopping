from flask import Blueprint, request, render_template, redirect, url_for
import sqlite3
import uuid

auth = Blueprint("auth", __name__)

DB_PATH = "shopping.db"


# -----------------------------
# SIGNUP (GET + POST)
# -----------------------------
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    email = request.form["email"]
    password = request.form["password"]

    token = str(uuid.uuid4())

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users (email, password, verified, token)
        VALUES (?, ?, 0, ?)
    """, (email, password, token))

    conn.commit()
    conn.close()

    # Simulate email verification link
    print(f"VERIFY EMAIL LINK → http://127.0.0.1:5000/verify-email/{token}")

    return "Signup successful. Check console for verification link."


# -----------------------------
# EMAIL VERIFICATION
# -----------------------------
@auth.route("/verify-email/<token>")
def verify_email(token):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET verified = 1
        WHERE token = ?
    """, (token,))

    conn.commit()
    conn.close()

    return render_template("verify_email.html")


# -----------------------------
# LOGIN (GET + POST)
# -----------------------------
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form["email"]
    password = request.form["password"]

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT id FROM users
        WHERE email = ? AND password = ? AND verified = 1
    """, (email, password))

    user = cur.fetchone()
    conn.close()

    if not user:
        return "Invalid login or email not verified", 401

    return "Login successful"
