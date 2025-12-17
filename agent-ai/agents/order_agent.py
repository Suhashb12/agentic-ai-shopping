# agents/order_agent.py

import uuid
import sqlite3
from agents.order_state import order_sessions

DB_PATH = "shopping.db"

ORDER_FIELDS = ["name", "email", "phone", "address", "payment_method"]

QUESTIONS = {
    "name": "Please share your full name.",
    "email": "Please provide your email address.",
    "phone": "Please provide your phone number.",
    "address": "Please provide your delivery address.",
    "payment_method": "How would you like to pay? (COD / link)"
}


def start_order(session_id: str, product: dict) -> str:
    order_sessions[session_id] = {
        "step": 0,
        "data": {},
        "product": product
    }
    return QUESTIONS["name"]


def continue_order(session_id: str, user_input: str) -> str:
    session = order_sessions.get(session_id)
    step = session["step"]

    field = ORDER_FIELDS[step]
    session["data"][field] = user_input
    session["step"] += 1

    if session["step"] < len(ORDER_FIELDS):
        next_field = ORDER_FIELDS[session["step"]]
        return QUESTIONS[next_field]

    return finalize_order(session_id)


def finalize_order(session_id: str) -> str:
    session = order_sessions.pop(session_id)
    data = session["data"]
    product = session["product"]

    order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    payment_method = data["payment_method"].lower()
    payment_status = "pending" if payment_method == "link" else "paid"

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO orders (
            order_id, user_id, product_name, category, price,
            name, email, phone, address,
            payment_method, payment_status, order_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        order_id,
        "guest",
        product["name"],
        product["category"],
        product["price"],
        data["name"],
        data["email"],
        data["phone"],
        data["address"],
        data["payment_method"],
        payment_status,
        "placed"
    ))

    conn.commit()
    conn.close()

    if payment_method == "link":
        print(f"💳 Payment link: http://localhost:5000/pay/{order_id}")
        return f"Please complete payment using the link. Order ID: {order_id}"

    return f"✅ Order placed successfully! Your Order ID is {order_id}"
