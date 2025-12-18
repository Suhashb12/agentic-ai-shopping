from flask import Flask, request, jsonify, render_template, session, redirect
import sqlite3

from llm.intent_classifier import classify_intent
from agents.shopping_agent import existing_ai_pipeline
from agents.order_tracking_agent import track_order
from agents.complaint_agent import handle_complaint, complete_refund

DB_PATH = "shopping.db"
app = Flask(__name__)
app.secret_key = "dev-secret-key"

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message", "").strip()
    intent_data = classify_intent(msg)
    intent = intent_data.get("intent")

    if intent == "track_order":
        return jsonify({"reply": track_order(intent_data["order_id"])})

    if intent in ["raise_complaint", "return_order", "replace_order"]:
        return jsonify({"reply": handle_complaint(intent_data)})

    return jsonify({"reply": existing_ai_pipeline(msg, session.get("user_id"))})

@app.route("/pay/<order_id>")
def pay(order_id):
    return render_template("payment.html", order_id=order_id)

@app.route("/payment-success/<order_id>")
def payment_success(order_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE orders SET payment_status='PAID' WHERE order_id=?", (order_id,))
    conn.commit()
    conn.close()
    return render_template("payment_success.html", order_id=order_id)

@app.route("/api/order/<order_id>")
def api_order(order_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT product_name, price, payment_method, order_status
        FROM orders WHERE order_id=?
    """, (order_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Order not found"}), 404

    return jsonify({
        "order_id": order_id,
        "product": row[0],
        "price": row[1],
        "payment": row[2],
        "status": row[3]
    })

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin@4sy6":
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
    cur.execute("SELECT order_id, product_name FROM orders WHERE order_status='RETURN_REQUESTED'")
    orders = cur.fetchall()
    conn.close()
    return render_template("admin_dashboard.html", orders=orders)

@app.route("/admin/refund/<order_id>", methods=["POST"])
def approve_refund(order_id):
    complete_refund(order_id)
    return redirect("/admin/dashboard")

@app.route("/login", methods=["GET"])
def user_login_page():
    return "User login not implemented yet. Please continue as guest."

@app.route("/signup", methods=["GET"])
def user_signup_page():
    return "User signup not implemented yet. Please continue as guest."


if __name__ == "__main__":
    app.run(debug=True)
