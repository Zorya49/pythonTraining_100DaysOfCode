import os
from twilio.rest import Client
import smtplib

TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
TWILIO_FROM_NO = os.getenv('TWILIO_PHONE')
TWILIO_TO_NO = os.getenv('MY_PHONE')
EMAIL = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')


class NotificationManager:
    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_TOKEN)

    def send_alert(self, alert):
        message = self.client.messages.create(
                body=alert,
                from_=TWILIO_FROM_NO,
                to=TWILIO_TO_NO
            )
        print(message.status)

    def send_emails(self, emails, message):
        with smtplib.SMTP("smtp-mail.outlook.com", port=587) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            for email in emails:
                connection.sendmail(
                    from_addr=EMAIL,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}".encode('utf-8')
                )
