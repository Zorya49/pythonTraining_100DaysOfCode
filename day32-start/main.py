import smtplib
import datetime as dt
import random

my_email = os.getenv('LOGIN')
password = os.getenv('PASSWORD')

connection = smtplib.SMTP("smtp-mail.outlook.com", port=587)
connection.starttls()
connection.login(user=my_email, password=password)

now = dt.datetime.now()
if now.weekday() == 4:
    with open("quotes.txt") as file:
        data = file.readlines()
        chosen_quote = random.choice(data)
        connection.sendmail(from_addr=my_email,
                            to_addrs="xxx@gmail.com",
                            msg=f"Subject:Quote of the day\n\n"
                                f"{chosen_quote}")

connection.close()
