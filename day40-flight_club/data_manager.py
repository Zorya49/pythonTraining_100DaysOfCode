import os
import requests
SHEETY_ENDPOINT_PRICES = os.environ["SHEETY_ENDPOINT_PRICES"]
SHEETY_ENDPOINT_USERS = os.environ["SHEETY_ENDPOINT_USERS"]
SHEETY_TOKEN = os.environ["SHEETY_TOKEN"]
headers_sheety = {
    "Authorization": SHEETY_TOKEN
}


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.dest_data = {}
        self.customer_data = {}

    def get_prices_data(self):
        response = requests.get(url=SHEETY_ENDPOINT_PRICES, headers=headers_sheety)
        data = response.json()
        self.dest_data = data["prices"]
        return self.dest_data

    def set_iata_codes(self):
        for city in self.dest_data:
            query = {
                    "price": {
                        "iataCode": city["iataCode"]
                    }
                }
            response = requests.put(url=f"{SHEETY_ENDPOINT_PRICES}/{city['id']}", json=query, headers=headers_sheety)

    def get_customer_emails(self):
        response = requests.get(url=SHEETY_ENDPOINT_USERS, headers=headers_sheety)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data
