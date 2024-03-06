#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from flight_data import FlightData

datamanager = DataManager()
flightsearch = FlightSearch()
flightdata = FlightData()
notificationmanager = NotificationManager()


# sheet_data = datamanager.get_prices_data()
#
# for destination in sheet_data:
#     if destination["iataCode"] == "":
#         iata_code = flightsearch.get_iata_code(destination["city"])
#         datamanager.set_iata_code(destination["id"], iata_code)

iata_code = flightsearch.get_iata_code("London")
print(iata_code)

flightdata.search_flights("LON")
