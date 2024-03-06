import os
import requests
import datetime
TEQUILA_ENDPOINT = os.environ["TEQUILA_ENDPOINT"]
TEQUILA_APIKEY = os.environ["TEQUILA_APIKEY"]
tequila_header = {
    "apikey": TEQUILA_APIKEY
}

class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self):
        pass

    def search_flights(self, city_iata):
        date_from = datetime.datetime.now() + datetime.timedelta(days=1)
        date_to = datetime.datetime.now() + datetime.timedelta(days=180)

        query = {
            "fly_from": "KRK",
            "fly_to": city_iata,
            "date_from": f"{date_from.strftime("%d/%m/%Y")}",
            "date_to": f"{date_to.strftime("%d/%m/%Y")}",
            "nights_in_dst_from": 2,
            "nights_in_dst_to": 7,
            "adults": 1,
            "curr": "EUR",
            "price_to": 100,
            "limit": 20
        }
        print(query)
        response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", params=query, headers=tequila_header)
        airport_data = response.json()

        print(airport_data)
        return airport_data
