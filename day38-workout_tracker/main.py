import requests
from datetime import datetime as dt
import json
import os

APP_ID = os.environ["APP_ID"]
APP_KEY = os.environ["APP_KEY"]

NUTRITIONIX_ENDPOINT = os.environ["NUTRITIONIX_ENDPOINT"]
headers_nutritionix = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY
}

SHEETY_ENDPOINT = os.environ["SHEETY_ENDPOINT"]
SHEETY_TOKEN = os.environ["SHEETY_TOKEN"]
headers_sheety = {
    "Authorization": SHEETY_TOKEN
}

user_query = input("Tell me which exercises you did: ")

query_params = {
    "query":  user_query,
    "weight_kg": 80,
    "height_cm": 180,
    "age": 25
}

response = requests.post(url=NUTRITIONIX_ENDPOINT, json=query_params, headers=headers_nutritionix)
exercises = json.loads(response.text)

today = dt.now()

for exercise in exercises["exercises"]:
    sheety_query = {
        "workout": {
            "date": today.strftime("%d/%m/%Y"),
            "time": today.strftime("%X"),
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    sheety_response = requests.post(url=SHEETY_ENDPOINT, json=sheety_query, headers=headers_sheety)

