def send_verification_email(email, token):
    # Hackathon-safe (prints link)
    print(f"[EMAIL VERIFY] http://localhost:5000/verify?token={token}")
