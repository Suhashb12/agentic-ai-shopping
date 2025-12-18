import hashlib
import secrets
import random
import time

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

def generate_token():
    return secrets.token_urlsafe(32)

def generate_otp():
    return str(random.randint(100000, 999999))

def expiry(minutes=10):
    return int(time.time()) + (minutes * 60)
