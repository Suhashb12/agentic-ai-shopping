# db/db_health.py

import sqlite3
import os

DB_PATH = "shopping.db"

REQUIRED_TABLES = {
    "mobiles",
    "fashion",
    "cosmetics",
    "orders",
    "complaints",
}


def check_db_health():
    # 1️⃣ DB file exists
    if not os.path.exists(DB_PATH):
        raise RuntimeError(
            f"❌ Database file '{DB_PATH}' not found. "
            f"Run: python db/init_db.py"
        )

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 2️⃣ Fetch existing tables
    cur.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table';
    """)
    existing_tables = {row[0] for row in cur.fetchall()}
    conn.close()

    # 3️⃣ Compare
    missing = REQUIRED_TABLES - existing_tables
    if missing:
        raise RuntimeError(
            f"❌ Database missing tables: {missing}. "
            f"Re-run: python db/init_db.py"
        )

    print("✅ DB health check passed — all required tables present")
