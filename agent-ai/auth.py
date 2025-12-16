import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from email_utils import send_verification_email


DB = "users.db"

def create_user(full_name, email, mobile, password):
    try:
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (full_name, email, mobile, password_hash) VALUES (?, ?, ?, ?)",
            (full_name, email, mobile, generate_password_hash(password))
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def authenticate_user(email, password):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, password_hash FROM users WHERE email=?",
        (email,)
    )
    row = cur.fetchone()
    conn.close()

    if row and check_password_hash(row[1], password):
        return row[0]
    return None

def create_user(full_name, email, mobile, password):
    token = str(uuid.uuid4())
    try:
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO users 
               (full_name, email, mobile, password_hash, verify_token, is_verified)
               VALUES (?, ?, ?, ?, ?, 0)""",
            (full_name, email, mobile, generate_password_hash(password), token)
        )
        conn.commit()
        send_verification_email(email, token)
        return True
    except:
        return False
    finally:
        conn.close()
