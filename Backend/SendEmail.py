import os 

import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SENDER = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")
def send_booking_email(to_email, name, room_name, date, time_slot, players, booking_id):
    msg = EmailMessage()
    msg["Subject"] = f"Room Zero - Booking #{booking_id} confirmed"
    msg["From"] = SENDER
    msg["To"] = to_email
    msg.set_content(
        f"Hi {name},\n\n"
        f"Your booking is confirmed.\n\n"
        f"Booking ID: {booking_id}\n"
        f"Room: {room_name}\n"
        f"Date: {date}\n"
        f"Time: {time_slot}\n"
        f"Players: {players}\n\n"
        f"Your escape begins at zero.\n"
        f"Room Zero"
    )
    with smtplib.SMTP(SMTP_HOST , SMTP_PORT , timeout= 10 ) as server:
        server.starttls()
        server.login(SENDER  , PASSWORD )
        server.send_message(msg)
        

