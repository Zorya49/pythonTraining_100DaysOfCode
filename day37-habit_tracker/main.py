import os

import requests
from datetime import datetime

# https://pixe.la/v1/users/plaything1004/graphs/graph1.html
PIXELA_ENDPOINT = "https://pixe.la/v1/users"
TOKEN = os.getenv('PIXELA_TOKEN')
USERNAME = os.getenv('PIXELA_USERNAME')
USER_PARAMS = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes"
}

# response = requests.post(url=PIXELA_ENDPOINT, json=USER_PARAMS)
# print(response.text)

GRAPH_ENDPOINT = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs"
GRAPH_ID = "graph1"
GRAPH_CONFIG = {
    "id": GRAPH_ID,
    "name": "Learning Graph",
    "unit": "minutes",
    "type": "int",
    "color": "ichou"
}

HEADER = {
    "X-USER-TOKEN": TOKEN
}

# graph_response = requests.post(url=GRAPH_ENDPOINT, json=GRAPH_CONFIG, headers=HEADER)
# print(graph_response.text)

date_to_fill = datetime(year=2024, month=2, day=5)
PIXEL_ENDPOINT = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{GRAPH_ID}"
pixel_config = {
    "date": date_to_fill.strftime("%Y%m%d"),
    "quantity": "50"
}

graph_response = requests.post(url=PIXEL_ENDPOINT, json=pixel_config, headers=HEADER)
print(graph_response.text)

date_to_change = datetime(year=2024, month=2, day=5)
CHANGE_ENDPOINT = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{GRAPH_ID}/{date_to_change.strftime('%Y%m%d')}"
change_config = {
    "quantity": "80"
}

# update_response = requests.put(url=CHANGE_ENDPOINT, json=change_config, headers=HEADER)
# print(update_response.text)

date_to_delete = datetime(year=2024, month=2, day=5)
DELETE_ENDPOINT = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{GRAPH_ID}/{date_to_delete.strftime('%Y%m%d')}"

# update_response = requests.delete(url=DELETE_ENDPOINT, headers=HEADER)
# print(update_response.text)


