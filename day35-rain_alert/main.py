import requests
import os
from twilio.rest import Client

OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
FORECAST_PARAMS = {
    "lat": 50.07,
    "lon": 20.00,
    "appid": os.getenv('APP_ID'),
    "cnt": 4
}
account_sid = os.getenv('ACC_SID')
auth_token = os.getenv('AUTH_TOKEN')


def get_forecast():
    response = requests.get(url=OWM_ENDPOINT, params=FORECAST_PARAMS)
    response.raise_for_status()
    return response.json()


def is_umbrella_needed(daytime_forecast):
    for _ in daytime_forecast["list"]:
        if int(_["weather"][0]["id"]) < 700:
            return True


def get_conditions(daytime_forecast):
    conditions = ""
    for _ in daytime_forecast["list"]:
        time = _["dt_txt"].split()[1]
        desc = _["weather"][0]["description"]
        conditions += f"{time}: {desc}\n"
    return conditions


forecast = get_forecast()
conditions = get_conditions(forecast)

if is_umbrella_needed(forecast):
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
                body="\nIt's going to rain today! Conditions:\n"+conditions,
                from_='+13159152760',
                to=os.getenv('MY_PHONE')
                )
    print(message.status)
else:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
                body="\nNo rain today! Conditions:\n"+conditions,
                from_='+13159152760',
                to=os.getenv('MY_PHONE')
                )
    print(message.status)
