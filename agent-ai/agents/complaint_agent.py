import sqlite3
import time

DB_PATH = "shopping.db"

def handle_complaint(intent_data):
    intent = intent_data["intent"]
    order_id = intent_data["order_id"]

    if intent == "raise_complaint":
        return (
            f"What would you like to do with Order {order_id}?\n"
            f"Type **return order {order_id}** or **replace order {order_id}**"
        )

    if intent == "return_order":
        _update(order_id, "RETURN_REQUESTED")
        return f"🔁 Return initiated for Order {order_id}."

    if intent == "replace_order":
        _update(order_id, "REPLACEMENT_REQUESTED")
        return f"🔄 Replacement initiated for Order {order_id}."

    return "Invalid request."


def _update(order_id, status):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("UPDATE orders SET order_status=? WHERE order_id=?", (status, order_id))
    cur.execute(
        "INSERT INTO complaints (order_id, complaint_type, status) VALUES (?, ?, ?)",
        (order_id, status, status)
    )

    conn.commit()
    conn.close()


def complete_refund(order_id):
    time.sleep(5)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("UPDATE orders SET order_status='REFUNDED' WHERE order_id=?", (order_id,))
    cur.execute("UPDATE complaints SET status='REFUNDED' WHERE order_id=?", (order_id,))
    conn.commit()
    conn.close()
