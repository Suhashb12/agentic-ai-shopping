import sqlite3

DB_PATH = "shopping.db"

def track_order(order_id, user_id=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT product_name, price, payment_method, order_status
        FROM orders
        WHERE order_id = ?
    """, (order_id,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return f"❌ No order found with Order ID **{order_id}**."

    product, price, payment, status = row

    return (
        f"📦 **Order Status**\n\n"
        f"🧾 Order ID: {order_id}\n"
        f"🛍 Product: {product}\n"
        f"💰 Price: ₹{price}\n"
        f"💳 Payment: {payment}\n"
        f"📍 Status: {status}"
    )
