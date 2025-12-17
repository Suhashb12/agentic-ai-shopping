import sqlite3

def get_db():
    return sqlite3.connect("db/app.db", check_same_thread=False)

def save_chat(user_id, role, message):
    if not user_id:
        return
    db = get_db()
    db.execute(
        "INSERT INTO chats (user_id, role, message) VALUES (?, ?, ?)",
        (user_id, role, message)
    )
    db.commit()
