import os
import smtplib
from email.mime.text import MIMEText

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

"""Send grid"""
def send_reset_email(to_email: str, reset_token: str):
    reset_link = f"http://127.0.0.1/reset-password?token={reset_token}"
    subject = "Password Reset Request"
    body = f"Click the link to reset your password: {reset_link}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "yourapp@yourdomain.com"
    msg["To"] = to_email

    with smtplib.SMTP("smtp.sendgrid.net", 587) as server:
        server.starttls()
        server.login("apikey", SENDGRID_API_KEY)
        server.sendmail("yourapp@yourdomain.com", to_email, msg.as_string())

    print("Email sent successfully")


#