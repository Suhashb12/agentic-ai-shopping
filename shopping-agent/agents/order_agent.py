import duckdb
import uuid

DB_PATH = "db/shop.db"

class OrderAgent:
    def handle(self, product_name: str):
        con = duckdb.connect(DB_PATH)

        product = con.execute("""
            SELECT id, price, stock FROM products
            WHERE LOWER(name) LIKE ?
        """, [f"%{product_name.lower()}%"]).fetchone()

        if not product:
            return "Product not found"

        if product[2] <= 0:
            return "Out of stock"

        order_id = str(uuid.uuid4())[:8]

        con.execute("""
            UPDATE products SET stock = stock - 1
            WHERE id = ?
        """, [product[0]])

        con.close()
        return f"Order placed successfully. Order ID: {order_id}"
