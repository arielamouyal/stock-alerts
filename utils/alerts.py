import os
from twilio.rest import Client

def send_sms(message):
    sid = os.getenv("TWILIO_SID")
    token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(sid, token)
    twilio_phone = os.getenv("TWILIO_PHONE")
    alert_phone = os.getenv("ALERT_PHONE")
    try:
        client.messages.create(body=message, from_=twilio_phone, to=alert_phone)
    except Exception as e:
        print("SMS failed:", e)
