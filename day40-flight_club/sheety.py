import os
import requests
SHEETY_ENDPOINT_USERS = os.environ["SHEETY_ENDPOINT_PRICES"]
SHEETY_TOKEN = os.environ["SHEETY_TOKEN"]
headers_sheety = {
    "Authorization": SHEETY_TOKEN,
    "Content-Type": "application/json"
}


def post_new_user(first_name, last_name, email):
    body = {
        "user": {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
        }
    }

    response = requests.post(url=SHEETY_ENDPOINT_USERS, headers=headers_sheety, json=body)
    response.raise_for_status()
    print(response.text)
