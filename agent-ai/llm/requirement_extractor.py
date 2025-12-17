import re

def extract_requirements(user_input: str):
    text = user_input.lower()

    requirements = {
        "category": None,
        "gender": None,
        "keywords": []
    }

    # Category inference
    if any(k in text for k in ["shirt", "pant", "cloth", "wear", "fashion", "rain", "jacket"]):
        requirements["category"] = "fashion"

    elif any(k in text for k in ["phone", "mobile", "camera", "battery"]):
        requirements["category"] = "mobile"

    elif any(k in text for k in ["cream", "lipstick", "makeup", "cosmetic"]):
        requirements["category"] = "cosmetics"

    # Gender
    if "men" in text or "male" in text:
        requirements["gender"] = "men"
    elif "women" in text or "female" in text:
        requirements["gender"] = "women"

    # Context keywords
    for word in ["rainy", "waterproof", "winter", "summer", "formal", "casual"]:
        if word in text:
            requirements["keywords"].append(word)

    return requirements
