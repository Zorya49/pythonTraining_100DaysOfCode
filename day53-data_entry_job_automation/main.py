import os

from bs4 import BeautifulSoup
import requests
import re
from FormFiller import FormFiller

PAGE_TO_SCRAPE = 'https://appbrewery.github.io/Zillow-Clone/'
FORM_URL = os.getenv('MY_FORM')


def extract_price(price_str):
    match = re.search(r'\$(\d{1,3}(?:,\d{3})*)(?:\+)?', price_str)
    if match:
        price_formatted = match.group(1)
        return f"${price_formatted}"
    else:
        return price_str


def format_address(address_str):
    return address_str.strip().replace(" |", ",")


def get_offers(url_to_scrape):
    offers_webpage = requests.get(url_to_scrape)
    bs = BeautifulSoup(offers_webpage.text, "html.parser")
    offer_cards = bs.find_all(name="div", class_="StyledPropertyCardDataWrapper")

    offers_list = []
    for offer_card in offer_cards:
        address = format_address(offer_card.find(name="address").text)
        price = extract_price(offer_card.find(name="span", class_="PropertyCardWrapper__StyledPriceLine").text)
        link = offer_card.find(name="a")['href']
        offers_list.append({"address": address,
                            "price": price,
                            "link": link})
    return offers_list


offers = get_offers(PAGE_TO_SCRAPE)
print(offers)

bot = FormFiller()
bot.upload_offers(FORM_URL, offers)
