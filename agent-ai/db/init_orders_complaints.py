import sqlite3

conn = sqlite3.connect("users.db")
cur = conn.cursor()

# Orders table
cur.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT UNIQUE,
    user_id INTEGER,
    full_name TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    alt_phone TEXT,
    payment_method TEXT,
    status TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Complaints table
cur.execute("""
CREATE TABLE IF NOT EXISTS complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT,
    user_id INTEGER,
    type TEXT,
    status TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("✅ Orders & Complaints tables initialized")
