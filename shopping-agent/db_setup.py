import duckdb
import os

DB_DIR = "db"
DB_PATH = os.path.join(DB_DIR, "shop.db")

os.makedirs(DB_DIR, exist_ok=True)

# Explicitly create a NEW database
con = duckdb.connect(DB_PATH, read_only=False)

con.execute("""
CREATE TABLE products (
    id INTEGER,
    name TEXT,
    category TEXT,
    brand TEXT,
    price INTEGER,
    stock INTEGER
)
""")

products = [
    (1, "Samsung Galaxy A14", "phone", "Samsung", 14000, 10),
    (2, "Redmi Note 12", "phone", "Redmi", 16000, 15),
    (3, "iPhone 13", "phone", "Apple", 52000, 5),
    (4, "Realme Narzo 60", "phone", "Realme", 18000, 8),
    (5, "Dell Inspiron 15", "laptop", "Dell", 48000, 6),
    (6, "HP Pavilion", "laptop", "HP", 55000, 4),
]

con.executemany(
    "INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)",
    products
)

con.close()
print("✅ Fresh DuckDB database created successfully")
