from groq import Groq
from tools.sql_tool import search_products, products_under_price
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are an intelligent shopping assistant.
You decide which tool to use based on the user query.

Rules:
- If user asks about price limit → use products_under_price
- If user asks about brand/category → use search_products
- Never make up prices
- Use tools, then explain results clearly
"""

def run_agent(user_input: str):
    # Simple routing (agentic decision)
    if "under" in user_input.lower():
        price = int("".join(filter(str.isdigit, user_input)))
        data = products_under_price(price)
        return format_response(data)

    data = search_products(user_input)
    return format_response(data)


def format_response(rows):
    if not rows:
        return "No products found."

    response = "Here are some matching products:\n"
    for name, brand, price, stock in rows:
        response += f"- {name} ({brand}) – ₹{price}, Stock: {stock}\n"
    return response
