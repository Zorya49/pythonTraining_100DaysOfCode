import os

from twilio.rest import Client
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')


class NotificationManager:
    def send_alert(self, alert):
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        message = client.messages \
            .create(
                body=alert,
                from_='+13159152760',
                to=os.getenv('MY_PHONE')
            )
        print(message.status)
