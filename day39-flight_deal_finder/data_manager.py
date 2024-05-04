import os
import requests
SHEETY_ENDPOINT = os.environ["SHEETY_ENDPOINT"]
SHEETY_TOKEN = os.environ["SHEETY_TOKEN"]
headers_sheety = {
    "Authorization": SHEETY_TOKEN
}


class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.dest_data = {}

    def get_prices_data(self):
        response = requests.get(url=SHEETY_ENDPOINT, headers=headers_sheety)
        data = response.json()
        self.dest_data = data["prices"]
        return self.dest_data

    def set_iata_codes(self):
        for city in self.dest_data:
            query = {
                    "price": {
                        "iataCode": city["iata_code"]
                    }
                }
            response = requests.put(url=f"{SHEETY_ENDPOINT}/{city['id']}", json=query, headers=headers_sheety)
            print(response.text)

