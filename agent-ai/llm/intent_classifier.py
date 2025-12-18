import re

def classify_intent(text: str):
    raw = text.strip()
    text = raw.lower()

    # Extract order id globally
    match = re.search(r"(ord-[a-z0-9]+)", text)
    order_id = match.group(1).upper() if match else None

    # -------------------------
    # TRACK ORDER
    # -------------------------
    if "track" in text and order_id:
        return {
            "intent": "track_order",
            "order_id": order_id
        }

    # -------------------------
    # COMPLAINT / RETURN / REPLACE
    # -------------------------
    if order_id:
        if text.startswith("raise complaint"):
            return {"intent": "raise_complaint", "order_id": order_id}

        if text.startswith("return order"):
            return {"intent": "return_order", "order_id": order_id}

        if text.startswith("replace order"):
            return {"intent": "replace_order", "order_id": order_id}

    # -------------------------
    # PLACE ORDER
    # -------------------------
    if text.startswith("buy this"):
        product = raw[8:].strip()
        return {
            "intent": "place_order",
            "product": product
        }

    # -------------------------
    # FASHION SEARCH
    # -------------------------
    if any(k in text for k in ["shirt", "jacket", "jeans", "cloth", "fashion"]):
        filters = {}
        if "men" in text:
            filters["gender"] = "men"
        elif "women" in text:
            filters["gender"] = "women"

        return {
            "intent": "search",
            "category": "fashion",
            "filters": filters
        }

    # -------------------------
    # MOBILE SEARCH
    # -------------------------
    if "mobile" in text or "phone" in text:
        budget = re.search(r"under (\d+)", text)
        return {
            "intent": "search",
            "category": "mobiles",
            "filters": {
                "budget": int(budget.group(1)) if budget else None
            }
        }

    return {"intent": "unknown"}
