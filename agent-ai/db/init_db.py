import duckdb

con = duckdb.connect("shop.db")

con.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER,
    name TEXT,
    category TEXT,
    price INTEGER,
    camera_mp INTEGER
)
""")

con.execute("DELETE FROM products")

products = [
    (1, "Redmi Note 13", "phone", 18000, 50),
    (2, "Samsung Galaxy A15", "phone", 17000, 50),
    (3, "Realme Narzo 60", "phone", 19000, 50),
    (4, "iPhone 12", "phone", 45000, 12),
    (5, "Dell Inspiron", "laptop", 55000, None),
]

con.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?)", products)
con.close()

print("DuckDB initialized")
