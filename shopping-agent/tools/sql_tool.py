import duckdb

DB_PATH = "db/shop.db"

def search_products(query: str):
    con = duckdb.connect(DB_PATH)
    like = f"%{query.lower()}%"
    result = con.execute("""
        SELECT name, brand, price, stock
        FROM products
        WHERE LOWER(name) LIKE ?
           OR LOWER(brand) LIKE ?
           OR LOWER(category) LIKE ?
    """, [like, like, like]).fetchall()
    con.close()
    return result


def products_under_price(max_price: int):
    con = duckdb.connect(DB_PATH)
    result = con.execute("""
        SELECT name, brand, price, stock
        FROM products
        WHERE price <= ?
        ORDER BY price ASC
    """, [max_price]).fetchall()
    con.close()
    return result
