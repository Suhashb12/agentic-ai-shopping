import duckdb
import random

con = duckdb.connect("shop.db")

# Create table
con.execute(open("db/schema.sql").read())

companies = ["Samsung", "Redmi", "Realme", "OnePlus", "Vivo", "Oppo", "Apple", "Motorola"]
designs = ["Plastic", "Metal", "Glass", "Aluminium Alloy"]
display_types = ["Flat", "Curved"]
battery_backup = ["Average", "Good", "Excellent"]

mobiles = []
id_counter = 1

for company in companies:
    for model_num in range(1, 41):  # 8 companies × 40 models = 320 phones

        os = "iOS" if company == "Apple" else "Android"

        actual_price = random.randint(12000, 90000)
        offer_price = actual_price - random.randint(1000, 8000)

        mobiles.append((
            id_counter,  # 1
            f"{company} Model {model_num}",  # 2
            company,  # 3

            random.choice([48, 50, 64, 108]),  # 4 rear_camera_mp
            random.choice([12, 16, 32]),  # 5 front_camera_mp

            random.choice([64, 128, 256]),  # 6 storage_gb
            random.choice([4, 6, 8, 12]),  # 7 ram_gb

            random.choice([4500, 5000, 6000]),  # 8 battery_mah
            random.choice([18, 33, 67]),  # 9 charging_watt
            "USB-C" if company != "Apple" else "Lightning",  # 10 charging_type

            actual_price,  # 11
            offer_price,  # 12

            os,  # 13
            "iOS 17" if company == "Apple" else "Android 14",  # 14

            "Bluetooth 5.3",  # 15
            "Wi-Fi 6",  # 16
            random.choice([True, False]),  # 17 nfc

            round(random.uniform(6.1, 6.9), 1),  # 18 display_size
            random.randint(800, 2000),  # 19 display_nits
            random.choice(display_types),  # 20 display_type
            random.choice([60, 90, 120]),  # 21 refresh_rate

            random.choice([True, False]),  # 22 reverse_charging
            random.choice([True, False]),  # 23 water_resistant

            random.choice(battery_backup),  # 24
            random.choice(designs),  # 25

            random.randint(0, 18)  # 26 stock
        ))

        id_counter += 1

con.executemany("""
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
""", mobiles)


con.close()

print(f"Inserted {len(mobiles)} mobile records")
