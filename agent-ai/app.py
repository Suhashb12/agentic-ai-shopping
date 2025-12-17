from flask import Flask, render_template, request, jsonify, redirect, session
from flask_session import Session

# ---------------- EXISTING AI IMPORTS (DO NOT CHANGE) ----------------
from llm.intent_classifier import classify_intent
from agents.shopping_agent import handle_shopping

# ---------------- AUTH + CHAT STORAGE ----------------
from auth import create_user, authenticate_user
from chat_store import save_chat, load_chats

import sqlite3

# -------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = "super-secret-key-change-this"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# ---------------- HOME ----------------
@app.route("/")
def index():
    chat_history = []
    if "user_id" in session:
        chat_history = load_chats(session["user_id"])
    return render_template("chat.html", chat_history=chat_history)


# ---------------- CHAT API ----------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"reply": "Please enter a message."})

    # ================= SAFETY WRAP (RECOMMENDED) =================
    try:
        # 🔹 EXISTING AI PIPELINE (UNCHANGED)
        intent = classify_intent(user_input)
        reply = handle_shopping(user_input, intent)

    except Exception as e:
        # Never crash UI
        print("❌ AI ERROR:", e)
        reply = "Sorry, something went wrong while processing your request. Please try again."

    # ================= CHAT PERSISTENCE =================
    if "user_id" in session:
        save_chat(session["user_id"], "user", user_input)
        save_chat(session["user_id"], "assistant", reply)

    return jsonify({"reply": reply})


# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        success = create_user(
            request.form["full_name"],
            request.form["email"],
            request.form["mobile"],
            request.form["password"]
        )
        if success:
            return redirect("/login")
        return "User already exists"

    return render_template("signup.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = authenticate_user(
            request.form["email"],
            request.form["password"]
        )
        if user_id:
            session["user_id"] = user_id
            return redirect("/")
        return "Invalid credentials"

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- EMAIL VERIFY ----------------
@app.route("/verify")
def verify():
    token = request.args.get("token")
    if not token:
        return "Invalid verification link"

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET is_verified=1 WHERE verify_token=?",
        (token,)
    )
    conn.commit()
    conn.close()

    return "Email verified successfully. You can now log in."


# ---------------- FORGOT PASSWORD ----------------
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]

        import random
        otp = str(random.randint(100000, 999999))

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO password_otps (email, otp) VALUES (?, ?)",
            (email, otp)
        )
        conn.commit()
        conn.close()

        print(f"[OTP DEBUG] {email} -> {otp}")
        return redirect("/reset-password")

    return render_template("forgot_password.html")


# ---------------- RESET PASSWORD ----------------
@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        email = request.form["email"]
        otp = request.form["otp"]
        new_password = request.form["password"]

        from werkzeug.security import generate_password_hash

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT 1 FROM password_otps WHERE email=? AND otp=?",
            (email, otp)
        )
        valid = cur.fetchone()

        if not valid:
            conn.close()
            return "Invalid OTP"

        cur.execute(
            "UPDATE users SET password_hash=? WHERE email=?",
            (generate_password_hash(new_password), email)
        )
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("reset_password.html")


# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(debug=True)
