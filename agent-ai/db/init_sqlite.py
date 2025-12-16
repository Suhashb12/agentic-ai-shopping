import sqlite3
import random

conn = sqlite3.connect("mobiles.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS mobiles (
    id INTEGER PRIMARY KEY,
    name TEXT,
    company TEXT,

    rear_camera_mp INTEGER,
    front_camera_mp INTEGER,

    storage_gb INTEGER,
    ram_gb INTEGER,

    battery_mah INTEGER,
    charging_watt INTEGER,
    charging_type TEXT,

    actual_price INTEGER,
    offer_price INTEGER,

    os TEXT,
    os_version TEXT,

    bluetooth_version TEXT,
    wifi_version TEXT,
    nfc INTEGER,

    display_size REAL,
    display_nits INTEGER,
    display_type TEXT,
    refresh_rate INTEGER,

    reverse_charging INTEGER,
    water_resistant INTEGER,

    battery_backup TEXT,
    design_type TEXT,

    stock INTEGER
)
""")

# Clear existing data
cur.execute("DELETE FROM mobiles")

companies = ["Samsung", "Redmi", "Realme", "OnePlus", "Vivo", "Oppo", "Apple", "Motorola"]
designs = ["Plastic", "Metal", "Glass", "Aluminium Alloy"]
display_types = ["Flat", "Curved"]
battery_backup = ["Average", "Good", "Excellent"]

id_counter = 1

for company in companies:
    for model in range(1, 41):

        os = "iOS" if company == "Apple" else "Android"
        actual_price = random.randint(12000, 90000)
        offer_price = actual_price - random.randint(1000, 8000)

        cur.execute("""
        INSERT INTO mobiles (
            id,
            name,
            company,
            rear_camera_mp,
            front_camera_mp,
            storage_gb,
            ram_gb,
            battery_mah,
            charging_watt,
            charging_type,
            actual_price,
            offer_price,
            os,
            os_version,
            bluetooth_version,
            wifi_version,
            nfc,
            display_size,
            display_nits,
            display_type,
            refresh_rate,
            reverse_charging,
            water_resistant,
            battery_backup,
            design_type,
            stock
        ) VALUES (
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?
        )
        """, (
            id_counter,                          # 1
            f"{company} Model {model}",          # 2
            company,                             # 3

            random.choice([48, 50, 64, 108]),    # 4
            random.choice([12, 16, 32]),         # 5

            random.choice([64, 128, 256]),       # 6
            random.choice([4, 6, 8, 12]),        # 7

            random.choice([4500, 5000, 6000]),   # 8
            random.choice([18, 33, 67]),         # 9
            "USB-C" if company != "Apple" else "Lightning",  # 10

            actual_price,                        # 11
            offer_price,                         # 12

            os,                                  # 13
            "iOS 17" if company == "Apple" else "Android 14",  # 14

            "Bluetooth 5.3",                     # 15
            "Wi-Fi 6",                           # 16
            random.choice([0, 1]),               # 17

            round(random.uniform(6.1, 6.9), 1),  # 18
            random.randint(800, 2000),           # 19
            random.choice(display_types),        # 20
            random.choice([60, 90, 120]),        # 21

            random.choice([0, 1]),               # 22
            random.choice([0, 1]),               # 23

            random.choice(battery_backup),       # 24
            random.choice(designs),              # 25

            random.randint(0, 18)                # 26
        ))

        id_counter += 1

conn.commit()
conn.close()

print("✅ SQLite DB created with mobile data")
