import sqlite3
import json
import random

conn = sqlite3.connect("products.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  category TEXT,
  name TEXT,
  brand TEXT,
  price INTEGER,
  offer_price INTEGER,
  attributes TEXT,
  stock INTEGER
)
""")

# ---------------- COSMETICS ----------------
cosmetics = [
    ("cosmetics", "Vitamin C Face Serum", "Minimalist", 799, 599,
     json.dumps({"skin_type": "all", "volume_ml": 30}), random.randint(1, 20)),

    ("cosmetics", "Matte Lipstick", "Maybelline", 599, 449,
     json.dumps({"shade": "Red", "finish": "Matte"}), random.randint(1, 20)),

    ("cosmetics", "Sunscreen SPF 50", "Neutrogena", 699, 549,
     json.dumps({"spf": 50, "water_resistant": True}), random.randint(1, 20)),
]

# ---------------- FASHION ----------------
fashion = [
    ("fashion", "Men Cotton T-Shirt", "H&M", 999, 699,
     json.dumps({"size": "M", "color": "Black", "material": "Cotton"}), random.randint(1, 20)),

    ("fashion", "Women Kurti", "Biba", 1999, 1499,
     json.dumps({"size": "L", "fabric": "Rayon"}), random.randint(1, 20)),

    ("fashion", "Denim Jeans", "Levi's", 2999, 2299,
     json.dumps({"fit": "Slim", "color": "Blue"}), random.randint(1, 20)),
]

cur.executemany("""
INSERT INTO products
(category, name, brand, price, offer_price, attributes, stock)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", cosmetics + fashion)

conn.commit()
conn.close()

print("✅ Cosmetics & Fashion dummy data inserted")
