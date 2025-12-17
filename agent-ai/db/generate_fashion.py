# db/generate_fashion.py
import sqlite3
import random

DB_PATH = "shopping.db"
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

men_items = [
    "White Cotton T-Shirt", "Blue Denim Shirt", "Black Hoodie",
    "Rainproof Jacket", "Casual Polo T-Shirt", "Slim Fit Jeans"
]

women_items = [
    "Pink Gown", "Floral Kurti", "Rainy Season Shrug",
    "Long Skirt", "Cotton Saree", "Casual Top"
]

unisex_items = [
    "Waterproof Jacket", "Hooded Raincoat",
    "Quick Dry Trousers", "Windcheater"
]

def insert_items(items, gender, count):
    for i in range(count):
        name = random.choice(items)
        season = random.choice(["rainy", "summer", "winter"])
        material = random.choice(["cotton", "polyester", "nylon"])
        waterproof = 1 if "Rain" in name or "Waterproof" in name else 0
        price = random.randint(800, 5000)
        stock = random.randint(1, 20)

        cur.execute("""
            INSERT INTO fashion
            (name, category, gender, season, material, waterproof, price, stock)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f"{name} - {gender}",
            "clothing",
            gender,
            season,
            material,
            waterproof,
            price,
            stock
        ))

insert_items(men_items, "men", 300)
insert_items(women_items, "women", 300)
insert_items(unisex_items, "unisex", 150)

conn.commit()
conn.close()
print("✅ Fashion data generated successfully")
