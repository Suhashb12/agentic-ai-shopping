from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import sqlite3

# ---- Core AI logic ----

from agents.complaint_agent import handle_complaint
from llm.intent_classifier import classify_intent
from agents.shopping_agent import existing_ai_pipeline
from agents.order_tracking_agent import track_order

DB_PATH = "shopping.db"

app = Flask(__name__)
app.secret_key = "dev-secret-key"


# -------------------------------------------------
# 🏠 Home
# -------------------------------------------------
@app.route("/")
def index():
    return render_template("chat.html")


# -------------------------------------------------
# 💬 Chat Router (MAIN ENTRY)
# -------------------------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return jsonify({"reply": "Please enter a message."})

    user_id = session.get("user_id")  # None if guest

    try:
        intent_data = classify_intent(user_input)
        intent = intent_data.get("intent")  # ✅ FIX

        # -------------------------
        # ORDER TRACKING
        # -------------------------
        if intent == "track_order":
            order_id = intent_data.get("order_id")
            reply = track_order(order_id)
            return jsonify({"reply": reply})

        # -------------------------
        # COMPLAINT / RETURN
        # -------------------------
        if intent in ["raise_complaint", "return_order", "replace_order"]:
            reply = handle_complaint(intent_data)
            return jsonify({"reply": reply})

        # -------------------------
        # SHOPPING / ORDER FLOW
        # -------------------------
        reply = existing_ai_pipeline(user_input, user_id)
        return jsonify({"reply": reply})

    except Exception as e:
        print("CHAT ERROR:", e)
        return jsonify({"reply": "Something went wrong. Please try again."})


# -------------------------------------------------
# 💳 Payment Page
# -------------------------------------------------
@app.route("/pay/<order_id>")
def pay(order_id):
    return render_template("payment.html", order_id=order_id)


# -------------------------------------------------
# ✅ Payment Success
# -------------------------------------------------
@app.route("/payment-success/<order_id>")
def payment_success(order_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        UPDATE orders
        SET payment_status = 'PAID',
            order_status = 'CONFIRMED'
        WHERE order_id = ?
    """, (order_id,))
    conn.commit()

    cur.execute("""
        SELECT product_name, price, payment_method
        FROM orders
        WHERE order_id = ?
    """, (order_id,))
    row = cur.fetchone()
    conn.close()

    product, price, payment = row if row else ("Unknown", 0, "ONLINE")

    return render_template(
        "payment_success.html",
        order_id=order_id,
        product=product,
        price=price,
        payment=payment
    )


# -------------------------------------------------
# 🔐 Minimal Auth (Optional)
# -------------------------------------------------
@app.route("/login", methods=["POST"])
def login():
    session["user_id"] = request.json.get("user_id")
    return jsonify({"status": "logged_in"})


@app.route("/logout")
def logout():
    session.clear()
    return jsonify({"status": "logged_out"})

# ------------------------------------
# ORDER DETAILS API (USED BY CHAT.JS)
# ------------------------------------
@app.route("/api/order/<order_id>", methods=["GET"])
def get_order(order_id):
    import sqlite3

    conn = sqlite3.connect("shopping.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT product_name, price, payment_method, order_status
        FROM orders
        WHERE order_id = ?
    """, (order_id,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Order not found"}), 404

    product, price, payment, status = row

    return jsonify({
        "order_id": order_id,
        "product": product,
        "price": price,
        "payment": payment,
        "status": status
    })

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "admin@4sy6":
            session["admin"] = True
            return redirect("/admin/dashboard")

        return "Invalid credentials", 401

    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect("/admin/login")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT o.order_id, o.product_name, o.order_status
        FROM orders o
        WHERE o.order_status = 'REFUND_INITIATED'
    """)

    orders = cur.fetchall()
    conn.close()

    return render_template("admin_dashboard.html", orders=orders)

@app.route("/admin/refund/<order_id>", methods=["POST"])
def approve_refund(order_id):
    if not session.get("admin"):
        return "Unauthorized", 403

    complete_refund(order_id)
    return redirect("/admin/dashboard")

# -------------------------------------------------
# 🚀 Run
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
