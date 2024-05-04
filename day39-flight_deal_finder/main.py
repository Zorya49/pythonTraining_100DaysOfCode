#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

datamanager = DataManager()
flightsearch = FlightSearch()
notificationmanager = NotificationManager()


sheet_data = datamanager.get_prices_data()

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flightsearch.get_iata_code( row["city"] )
    datamanager.destination_data = sheet_data
    datamanager.set_iata_codes()


for destination in sheet_data:
    flight = flightsearch.search_flights( destination["iataCode"] )
    if flight.price < destination["lowestPrice"]:
        notificationmanager.send_alert(
            alert=f"Low price on desired destination! {flight.price}EUR for flight from "
                  f"{flight.origin_city}-{flight.origin_airport} to "
                  f"{flight.destination_city}-{flight.destination_airport}, "
                  f"from {flight.out_date} to {flight.return_date}.")
