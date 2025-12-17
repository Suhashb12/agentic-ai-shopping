import sqlite3
import random

conn = sqlite3.connect("shopping.db")
cur = conn.cursor()

brands = ["Samsung", "Redmi", "Realme", "Motorola", "OnePlus", "Vivo", "Oppo"]
models = ["A", "Note", "Pro", "Plus", "Ultra"]

for i in range(300):
    brand = random.choice(brands)
    model = f"{random.choice(models)} {random.randint(1, 50)}"
    name = f"{brand} {model}"

    rear_camera = random.choice([48, 50, 64, 108])
    front_camera = random.choice([8, 13, 16, 32])
    ram = random.choice([4, 6, 8, 12])
    storage = random.choice([64, 128, 256])
    battery = random.choice([4500, 5000, 6000])
    price = random.randint(7000, 35000)
    stock = random.randint(0, 20)

    cur.execute("""
        INSERT INTO mobiles
        (name, brand, rear_camera, front_camera, ram, storage, battery, price, stock)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name, brand, rear_camera, front_camera,
        ram, storage, battery, price, stock
    ))

conn.commit()
conn.close()
print("✅ 300 mobile products inserted")
