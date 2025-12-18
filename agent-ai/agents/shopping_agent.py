import sqlite3
import uuid
from llm.intent_classifier import classify_intent

DB_PATH = "shopping.db"
ORDER_SESSIONS = {}

def generate_order_id():
    return "ORD-" + uuid.uuid4().hex[:8].upper()


def existing_ai_pipeline(user_input: str, user_id: str = None):
    user_key = user_id or "guest"

    # Continue order flow
    if user_key in ORDER_SESSIONS:
        return continue_order_flow(user_key, user_input)

    intent_data = classify_intent(user_input)
    intent = intent_data.get("intent")

    # Start order
    if intent == "place_order":
        product_name = intent_data.get("product")
        if not product_name:
            return "Please specify which product you want to buy."

        clean = product_name.lower().replace("- men", "").replace("- women", "").strip()

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        for table in ["mobiles", "fashion", "cosmetics"]:
            cur.execute(
                f"SELECT name, price FROM {table} WHERE LOWER(name) LIKE ?",
                (f"%{clean}%",)
            )
            row = cur.fetchone()
            if row:
                product, price = row
                category = table
                break
        else:
            conn.close()
            return f"Sorry, I couldn't find **{product_name}** in our inventory."

        conn.close()

        ORDER_SESSIONS[user_key] = {
            "step": "name",
            "product": product,
            "price": price,
            "category": category
        }
        return "Please share your full name."

    return handle_shopping(intent_data)


def handle_shopping(intent_data):
    category = intent_data.get("category")
    filters = intent_data.get("filters", {})

    if category not in ["fashion", "mobiles", "cosmetics"]:
        return "I can help you with mobiles, fashion, and cosmetics."

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    query = f"SELECT name, price, gender FROM {category}"
    conditions, params = [], []

    if filters.get("budget"):
        conditions.append("price <= ?")
        params.append(filters["budget"])

    if category == "fashion" and filters.get("gender"):
        conditions.append("gender = ?")
        params.append(filters["gender"])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " LIMIT 5"
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return "Sorry, no products match your request."

    reply = "Here are some options:\n"
    for name, price, gender in rows:
        reply += f"- {name} - {gender} – ₹{price}\n"

    reply += "Say **buy this <product name>** to place an order."
    return reply


def continue_order_flow(user_key, user_input):
    s = ORDER_SESSIONS[user_key]

    if s["step"] == "name":
        s["name"] = user_input
        s["step"] = "phone"
        return "Please share your mobile number."

    if s["step"] == "phone":
        s["phone"] = user_input
        s["step"] = "address"
        return "Please share your delivery address."

    if s["step"] == "address":
        s["address"] = user_input
        s["step"] = "payment"
        return "Choose payment method: COD or ONLINE."

    if s["step"] == "payment":
        payment = user_input.lower()
        order_id = generate_order_id()

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO orders (
                order_id, user_id, product_name, category, price,
                name, phone, address, payment_method,
                payment_status, order_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            order_id, user_key, s["product"], s["category"], s["price"],
            s["name"], s["phone"], s["address"],
            payment.upper(),
            "PAID" if payment == "online" else "PENDING",
            "CONFIRMED"
        ))

        conn.commit()
        conn.close()
        del ORDER_SESSIONS[user_key]

        if payment == "cod":
            return (
                f"✅ Order placed successfully!\n"
                f"Order ID: {order_id}\n"
                f"Product: {s['product']}\n"
                f"Price: ₹{s['price']}\n"
                f"Payment: COD\n"
                f"Status: CONFIRMED"
            )

        return (
            f"💳 Complete payment here: "
            f"<a href='http://localhost:5000/pay/{order_id}' "
            f"class='payment-link' target='_blank'>"
            f"Click to Pay for Order {order_id}</a>"
        )
