import sqlite3

DB = "users.db"

def save_chat(user_id, role, message):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chats (user_id, role, message) VALUES (?, ?, ?)",
        (user_id, role, message)
    )
    conn.commit()
    conn.close()

def load_chats(user_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        "SELECT role, message FROM chats WHERE user_id=? ORDER BY id",
        (user_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows
