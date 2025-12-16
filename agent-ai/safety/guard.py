import re

SENSITIVE_PATTERNS = [
    r"\b\d{6}\b",        # OTP
    r"password",
    r"cvv",
    r"upi\s*pin",
    r"card\s*number"
]

def check_sensitive_input(text: str) -> bool:
    for p in SENSITIVE_PATTERNS:
        if re.search(p, text, re.IGNORECASE):
            return True
    return False

def safe_refusal():
    return (
        "For your safety, I can’t help with passwords, OTPs, or payment details. "
        "I can guide you through the process securely instead."
    )
