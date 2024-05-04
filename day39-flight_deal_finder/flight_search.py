import os
import requests
from datetime import datetime, timedelta
from flight_data import FlightData
TEQUILA_ENDPOINT = os.environ["TEQUILA_ENDPOINT"]
TEQUILA_APIKEY = os.environ["TEQUILA_APIKEY"]
tequila_header = {
    "apikey": TEQUILA_APIKEY
}


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        pass

    def get_iata_code(self, city_name):
        query = {
            "term": city_name,
            "location_types": "city"
        }
        data = requests.get(url=f"{TEQUILA_ENDPOINT}/locations/query", params=query, headers=tequila_header)
        airport_data = data.json()
        iata_code = airport_data["locations"][0]["code"]
        return iata_code

    def search_flights(self, dest_city_iata):
        date_from = datetime.now() + timedelta(days=1)
        date_to = datetime.now() + timedelta(days=180)

        query = {
            "fly_from": "KRK",
            "fly_to": dest_city_iata,
            "date_from": f"{date_from.strftime("%d/%m/%Y")}",
            "date_to": f"{date_to.strftime("%d/%m/%Y")}",
            "nights_in_dst_from": 2,
            "nights_in_dst_to": 7,
            "adults": 1,
            "curr": "EUR",
            "price_to": 100,
            "limit": 20
        }
        response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", params=query, headers=tequila_header)
        try:
            f_data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {dest_city_iata}.")
            return None

        flight_data = FlightData(
            price=f_data["price"],
            origin_city=f_data["route"][0]["cityFrom"],
            origin_airport=f_data["route"][0]["flyFrom"],
            destination_city=f_data["route"][0]["cityTo"],
            destination_airport=f_data["route"][0]["flyTo"],
            flight_date=f_data["route"][0]["local_departure"].split("T")[0],
            return_date=f_data["route"][1]["local_departure"].split("T")[0]
        )
        print(f"{flight_data.destination_city}: £{flight_data.price}")
        return flight_data
