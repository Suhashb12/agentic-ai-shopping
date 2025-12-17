import re

def classify_intent(text: str):
    raw_text = text.strip()
    text = raw_text.lower()

    # -------------------------
    # EXTRACT ORDER ID (GLOBAL)
    # -------------------------
    order_match = re.search(r"(ord-[a-z0-9]+)", text)
    order_id = order_match.group(1).upper() if order_match else None

    # -------------------------
    # ORDER TRACKING
    # -------------------------
    if "track" in text and order_id:
        return {
            "intent": "track_order",
            "order_id": order_id
        }

    # -------------------------
    # COMPLAINT / RETURN / REPLACE
    # -------------------------
    match = re.search(r"(ord-[a-z0-9]+)", text)

    if match:
        order_id = match.group(1).upper()

        if text.startswith("raise complaint"):
            return {
                "intent": "raise_complaint",
                "order_id": order_id
            }

        if text.startswith("return order"):
            return {
                "intent": "return_order",
                "order_id": order_id
            }

        if text.startswith("replace order"):
            return {
                "intent": "replace_order",
                "order_id": order_id
            }

    # -------------------------
    # PLACE ORDER
    # -------------------------
    if text.startswith("buy this"):
        product = raw_text[8:].strip()  # removes "buy this"
        return {
            "intent": "place_order",
            "product": product
        }

    # -------------------------
    # FASHION SEARCH
    # -------------------------
    if any(word in text for word in ["cloth", "shirt", "jacket", "jeans", "fashion"]):
        gender = None
        if "women" in text:
            gender = "women"
        elif "men" in text:
            gender = "men"

        filters = {}
        if gender:
            filters["gender"] = gender

        return {
            "intent": "search",
            "category": "fashion",
            "filters": filters
        }

    # -------------------------
    # MOBILE SEARCH
    # -------------------------
    if "phone" in text or "mobile" in text:
        budget_match = re.search(r"under (\d+)", text)
        filters = {}
        if budget_match:
            filters["budget"] = int(budget_match.group(1))

        return {
            "intent": "search",
            "category": "mobiles",
            "filters": filters
        }

    # -------------------------
    # FALLBACK
    # -------------------------
    return {
        "intent": "unknown"
    }
