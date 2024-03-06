##################### Extra Hard Starting Project ######################
# 1. Update the birthdays.csv
# 2. Check if today matches a birthday in the birthdays.csv
# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv
# 4. Send the letter generated in step 3 to that person's email address.

import pandas as pd
import smtplib
import datetime as dt
import random
import os

my_email = os.getenv('LOGIN')
password = os.getenv('PASSWORD')
connection = smtplib.SMTP("smtp-mail.outlook.com", port=587)
letters_list = os.listdir("letter_templates")


def prepare_wishes(recipient_name):
    letter = random.choice(letters_list)
    with open(f"letter_templates/{letter}") as lt:
        message_text = lt.read()
    return message_text.replace("[NAME]", recipient_name)


def send_wishes(recipient_name, recipients_email):
    message = prepare_wishes(recipient_name)
    connection.sendmail(from_addr=my_email,
                        to_addrs=recipients_email,
                        msg=f"Subject:Happy B-day!\n\n"
                        f"{message}")


connection.starttls()
connection.login(user=my_email, password=password)

birthday_db = pd.read_csv("birthdays.csv")
birthday_db_dict = birthday_db.to_dict(orient="records")

current_month = dt.datetime.now().month
current_day = dt.datetime.now().day

for record in birthday_db_dict:
    if record["month"] == current_month and record["day"] == current_day:
        send_wishes(record["name"], record["email"])

connection.close()








