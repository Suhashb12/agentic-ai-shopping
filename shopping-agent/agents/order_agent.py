import duckdb
import uuid

DB_PATH = "db/shop.db"

class OrderAgent:
    def handle(self, user_input: str):
        con = duckdb.connect(DB_PATH)

        # --- clean user input ---
        text = user_input.lower()
        for word in ["buy", "order", "purchase"]:
            text = text.replace(word, "")

        product_query = text.strip()

        product = con.execute("""
            SELECT id, name, price, stock
            FROM products
            WHERE LOWER(name) LIKE ?
        """, [f"%{product_query}%"]).fetchone()

        if not product:
            con.close()
            return "Product not found."

        if product[3] <= 0:
            con.close()
            return "Sorry, product is out of stock."

        order_id = str(uuid.uuid4())[:8]

        con.execute("""
            UPDATE products
            SET stock = stock - 1
            WHERE id = ?
        """, [product[0]])

        con.close()
        return f"✅ Order placed for {product[1]} (₹{product[2]}). Order ID: {order_id}"
