# db/init_db.py

import sqlite3

DB_PATH = "shopping.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# -------------------------------------------------
# MOBILES TABLE
# -------------------------------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS mobiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    brand TEXT,
    rear_camera INTEGER,
    front_camera INTEGER,
    ram INTEGER,
    storage INTEGER,
    battery INTEGER,
    price INTEGER,
    stock INTEGER
)
""")

# -------------------------------------------------
# FASHION TABLE
# -------------------------------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS fashion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    gender TEXT,
    season TEXT,
    material TEXT,
    waterproof INTEGER,
    price INTEGER,
    stock INTEGER
)
""")

# -------------------------------------------------
# COSMETICS TABLE
# -------------------------------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS cosmetics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    brand TEXT,
    type TEXT,
    skin_type TEXT,
    gender TEXT,
    price INTEGER,
    stock INTEGER
)
""")

# -------------------------------------------------
# ORDERS TABLE
# -------------------------------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT,
    user_id TEXT,
    product_name TEXT,
    category TEXT,
    price INTEGER,
    name TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    payment_method TEXT,
    payment_status TEXT,
    order_status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# -------------------------------------------------
# COMPLAINTS / RETURNS TABLE
# -------------------------------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT,
    complaint_type TEXT,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    full_name TEXT,
    password_hash TEXT,
    is_verified INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    token TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS email_tokens (
    email TEXT,
    token TEXT,
    expires_at TIMESTAMP
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS password_otps (
    email TEXT,
    otp TEXT,
    expires_at TIMESTAMP
)
""")

conn.commit()
conn.close()

print("✅ Database initialized successfully with all required tables")
