import sqlite3

DB_NAME = "users.db"

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

# ---------------- USERS TABLE ----------------
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    mobile TEXT,
    password_hash TEXT,
    is_verified INTEGER DEFAULT 0,
    verify_token TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# ---------------- CHAT HISTORY ----------------
cur.execute("""
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    role TEXT CHECK(role IN ('user', 'assistant')),
    message TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

# ---------------- PASSWORD RESET OTP ----------------
cur.execute("""
CREATE TABLE IF NOT EXISTS password_otps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    otp TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# ---------------- USER PREFERENCES ----------------
cur.execute("""
CREATE TABLE IF NOT EXISTS user_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    pref_key TEXT NOT NULL,
    pref_value TEXT NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

conn.commit()
conn.close()

print("✅ Auth + Chat + OTP + Preferences DB initialized successfully")
