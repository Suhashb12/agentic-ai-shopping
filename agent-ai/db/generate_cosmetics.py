# db/generate_cosmetics.py
import sqlite3
import random

DB_PATH = "shopping.db"
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

products = [
    ("Face Wash", "oily"),
    ("Moisturizer", "dry"),
    ("Sunscreen", "all"),
    ("Lip Balm", "dry"),
    ("Hair Serum", "all"),
    ("Body Lotion", "dry")
]

brands = ["Nivea", "Lakme", "Mamaearth", "Plum", "Minimalist"]
genders = ["men", "women", "unisex"]

for _ in range(300):
    product, skin = random.choice(products)
    brand = random.choice(brands)
    gender = random.choice(genders)
    price = random.randint(150, 1500)
    stock = random.randint(1, 25)

    cur.execute("""
        INSERT INTO cosmetics
        (name, brand, type, skin_type, gender, price, stock)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        f"{brand} {product} - {gender}",
        brand,
        product,
        skin,
        gender,
        price,
        stock
    ))

conn.commit()
conn.close()
print("✅ Cosmetics data generated successfully")
