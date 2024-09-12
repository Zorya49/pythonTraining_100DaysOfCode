import os
from twilio.rest import Client

TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
TWILIO_FROM_NO = os.getenv('TWILIO_PHONE')
TWILIO_TO_NO = os.getenv('MY_PHONE')


class NotificationManager:
    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_TOKEN)

    def send_alert(self, alert):
        message = self.client.messages.create(
                body=alert,
                from_=TWILIO_FROM_NO,
                to=TWILIO_TO_NO
            )
