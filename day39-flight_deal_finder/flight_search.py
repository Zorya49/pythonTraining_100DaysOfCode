import os
import requests
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
