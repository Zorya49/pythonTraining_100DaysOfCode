from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
import sheety
from inputimeout import inputimeout, TimeoutOccurred

datamanager = DataManager()
flightsearch = FlightSearch()
notificationmanager = NotificationManager()


print("Welcome to Flight Club.\n"
      "We find the best flight deals and email them to you.")

# Give 30 seconds to decide to add new user and proceed with adding or proceed to refreshing flight deals data
# (in case that we want to run program automatically through some service like PythonAnywhere)
try:
    choice = inputimeout(prompt="Type 'add' to register a new user or press enter to refresh deals.\n", timeout=5)

    if choice.lower() == "add":
        first_name = input("What is your first name?").title()
        last_name = input("What is your last name?").title()

        email1 = "email1"
        email2 = "email2"
        while email1 != email2:
            email1 = input("What is your email? ")
            if email1.lower() == "quit" or email1.lower() == "exit":
                exit()
            email2 = input("Please type your email again to confirm: ")
            if email2.lower() == "quit" or email2.lower() == "exit":
                exit()

        sheety.post_new_user(first_name, last_name, email1)
        print("You are now in the club!")
        exit()  # Exit program when purpose of running was adding new user
except TimeoutOccurred:
    pass


sheet_data = datamanager.get_prices_data()

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flightsearch.get_iata_code(row["city"])
    datamanager.destination_data = sheet_data
    datamanager.set_iata_codes()

for destination in sheet_data:
    flight = flightsearch.search_flights(destination["iataCode"])

    if flight.price < destination["lowestPrice"]:
        customers = datamanager.get_customer_emails()
        emails = [customer["email"] for customer in customers]

        message = (f"Low price on desired destination! {flight.price}EUR for flight from "
                   f"{flight.origin_city}-{flight.origin_airport} to "
                   f"{flight.destination_city}-{flight.destination_airport}, "
                   f"from {flight.flight_date} to {flight.return_date}.")

        if flight.stop_overs > 0:
            message += (f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city} (out) "
                        f"and {flight.via_city_return} (return).")

        notificationmanager.send_emails(emails, message)
