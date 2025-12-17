import sqlite3
import json
from llm.groq_client import get_llm


DB_PATH = "products.db"


def handle_shopping(user_input: str, intent: dict) -> str:
    """
    Main shopping agent:
    - Grounds response in SQLite products
    - Uses LLM only for reasoning & explanation
    """

    category = intent.get("category", "other")
    budget = intent.get("budget")

    # If category not supported
    if category not in ["mobile", "cosmetics", "fashion"]:
        return "I can help with mobiles, cosmetics, and fashion products. Please specify one."

    # ---------------- FETCH PRODUCTS ----------------
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    query = "SELECT name, brand, price, offer_price, attributes FROM products WHERE category=?"
    params = [category]

    if budget:
        query += " AND offer_price <= ?"
        params.append(budget)

    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return f"Sorry, I couldn't find any {category} products within your budget."

    # Prepare product summary for LLM
    products = []
    for name, brand, price, offer_price, attrs in rows[:5]:
        products.append({
            "name": name,
            "brand": brand,
            "price": price,
            "offer_price": offer_price,
            "attributes": json.loads(attrs)
        })

    # ---------------- LLM RESPONSE ----------------
    llm = get_llm()

    prompt = f"""
You are a professional shopping assistant.

User request:
"{user_input}"

Available products (JSON):
{json.dumps(products, indent=2)}

Instructions:
- Recommend the best 2–3 products
- Explain briefly why they match the user's request
- Be polite, calm, and professional
- Do NOT mention databases or SQL
"""

    try:
        response = llm.invoke(prompt)
        return response.content.strip()

    except Exception as e:
        print("❌ Shopping agent error:", e)
        return "I found some products but had trouble explaining them. Please try again."
