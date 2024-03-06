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
        self.data = {}

    def get_prices_data(self):
        response = requests.get(url=SHEETY_ENDPOINT, headers=headers_sheety)
        self.data = response.json()
        return self.data["prices"]

    def set_iata_code(self, row_id, iata_code):
        query = {
                "price": {
                    "iataCode": iata_code
                }
            }
        response = requests.put(url=f"{SHEETY_ENDPOINT}/{row_id}", json=query, headers=headers_sheety)
        print(response.text)

