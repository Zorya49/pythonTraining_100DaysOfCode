import os
import smtplib
from bs4 import BeautifulSoup
import requests

my_email = os.getenv('EMAIL_ADDRESS')
password = os.getenv('EMAIL_PASSWORD')
connection = smtplib.SMTP("smtp-mail.outlook.com", port=587)

url = "https://www.amazon.pl/Apple-AirPods-3-generacji-laduj%C4%85cym-MagSafe/dp/B09JQQDLXF/ref=sr_1_2?crid=FR85GMUQRJNO&dib=eyJ2IjoiMSJ9.G2d_enfW69p5zdQ_srBmS8G1941pcrrg0beKJVZpS_6cN1ErMuHO8H3yeO06bbVpZ_oSg0pdAZsYoP-gzHBvJlJrzY7-eW7Tv0PEaSL5nAufV5Qj4AfmZZLrKQ-nK6RMLPr_2u2zRUlWLszNgtgz04y_hSwrae4uoHMMexDjWBd_ilE15iqe6yXdbJObJ44v6gPLfyRwMGF-OJYcXDHHlGL2PHlkkPtNcHP-qOMOPGY41RZrXOAc2LDvbHrsEfk1O2nJUx7Gg0CaXwr9s7TW2Lr1nCypKkrST1CCMkwmTKI.0rAhDuf_n9hZqiJwxjU7Y7OWldSiVhecZdeLBR-Q9rE&dib_tag=se&keywords=airpods+magsafe&qid=1708550008&sprefix=airpods+magsa%2Caps%2C111&sr=8-2"
header = {
        "Accept-Language":"pl,en-US;q=0.7,en;q=0.3",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
}

target_price = 800


def send_notification(current_price):
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(from_addr=my_email,
                        to_addrs=my_email,
                        msg=f"Subject:Price Tracker: price of tracked item just dropped below expected level!\n\n"
                            f"Price of tracked item just dropped below expected level!\n"
                            f"Price: {current_price}zl\n"
                            f"Get it now: {url}"
                        )
    connection.close()


product_webpage = requests.get(url, headers=header)

soup = BeautifulSoup(product_webpage.content, "html.parser")

price_tag = soup.find(name="span", class_="a-offscreen").getText()
price = float(price_tag.split("zł")[0].replace(",", "."))


if price<target_price:
    send_notification(price)
