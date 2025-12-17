import sqlite3
import threading
import time

DB_PATH = "shopping.db"


def handle_complaint(intent_data):
    intent = intent_data["intent"]
    order_id = intent_data["order_id"]

    # -------------------------
    # START COMPLAINT
    # -------------------------
    if intent == "raise_complaint":
        return (
            f"What would you like to do with Order {order_id}?\n"
            f"→ Type **return order {order_id}**\n"
            f"→ Type **replace order {order_id}**"
        )

    # -------------------------
    # RETURN
    # -------------------------
    if intent == "return_order":
        _update_complaint(order_id, "RETURN")
        return (
            f"🔁 Return initiated for Order {order_id}.\n"
            f"Once pickup is completed, your amount will be refunded to the original payment method."
        )

    # -------------------------
    # REPLACEMENT
    # -------------------------
    if intent == "replace_order":
        _update_complaint(order_id, "REPLACEMENT")
        return (
            f"🔄 Replacement initiated for Order {order_id}.\n"
            f"A new item will be shipped soon."
        )

    return "Invalid complaint action."


# -------------------------------------------------
# INTERNAL: CREATE COMPLAINT + UPDATE ORDER STATUS
# -------------------------------------------------
def _update_complaint(order_id, complaint_type):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Insert complaint
    cur.execute("""
        INSERT INTO complaints (order_id, complaint_type, status)
        VALUES (?, ?, ?)
    """, (
        order_id,
        complaint_type,
        "INITIATED"
    ))

    # Update order status
    if complaint_type == "RETURN":
        order_status = "REFUND_INITIATED"
    else:
        order_status = "REPLACEMENT_REQUESTED"

    cur.execute("""
        UPDATE orders
        SET order_status = ?
        WHERE order_id = ?
    """, (
        order_status,
        order_id
    ))

    conn.commit()
    conn.close()

    # 🔁 Simulate async refund completion (RETURN only)
    if complaint_type == "RETURN":
        threading.Thread(
            target=_complete_refund_after_delay,
            args=(order_id,),
            daemon=True
        ).start()


# -------------------------------------------------
# INTERNAL: COMPLETE REFUND (SIMULATED)
# -------------------------------------------------
def _complete_refund_after_delay(order_id):
    time.sleep(5)  # simulate bank delay

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        UPDATE orders
        SET order_status = 'REFUNDED'
        WHERE order_id = ?
    """, (order_id,))

    cur.execute("""
        UPDATE complaints
        SET status = 'REFUNDED'
        WHERE order_id = ?
    """, (order_id,))

    conn.commit()
    conn.close()
