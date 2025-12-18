import smtplib
from email.mime.text import MIMEText

SMTP_EMAIL = "suhas@saturam.com"
SMTP_PASS = "mkts mqbr zrgu xhkv"

def send_email(to, subject, body):
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = SMTP_EMAIL
    msg["To"] = to

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SMTP_EMAIL, SMTP_PASS)
        server.send_message(msg)
