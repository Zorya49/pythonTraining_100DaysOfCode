import time

import requests
from datetime import datetime
import time

LOCATION_PARAMS = {
    "lat": -41.199633,  # 50.064651,
    "lng": 146.357117,  # 19.944981,
    "formatted": 0
}


def get_iss_position():
    response_iss_pos = requests.get(url="http://api.open-notify.org/iss-now.json")
    response_iss_pos.raise_for_status()

    data_iss_pos = response_iss_pos.json()
    print(data_iss_pos)

    longitude = float(data_iss_pos["iss_position"]["longitude"])
    latitude = float(data_iss_pos["iss_position"]["latitude"])
    iss_position = (longitude, latitude)
    return iss_position


def is_iss_overhead():
    iss_position = get_iss_position()
    if (LOCATION_PARAMS["lng"] - 5 < iss_position[0] < LOCATION_PARAMS["lng"] + 5
            and LOCATION_PARAMS["lat"] - 5 < iss_position[1] < LOCATION_PARAMS["lat"] + 5):
        return True
    else:
        return False


def is_nighttime():
    time_now = datetime.now()

    response_day_params = requests.get(url="https://api.sunrise-sunset.org/json", params=LOCATION_PARAMS)
    response_day_params.raise_for_status()
    data_day_params = response_day_params.json()

    sunrise_hh = int(data_day_params["results"]["sunrise"].split("T")[1].split(":")[0])
    sunrise_mm = int(data_day_params["results"]["sunrise"].split("T")[1].split(":")[1])
    sunset_hh = int(data_day_params["results"]["sunset"].split("T")[1].split(":")[0])
    sunset_mm = int(data_day_params["results"]["sunset"].split("T")[1].split(":")[1])

    if ((time_now.hour >= sunset_hh and time_now.minute >= sunset_mm)
            or (time_now.hour <= sunrise_hh and time_now.minute <= sunrise_mm)):
        return True
    else:
        return False


def look_up_for_iss():
    if is_iss_overhead() and is_nighttime():
        print("Look up for the ISS")
    else:
        pass


while True:
    look_up_for_iss()
    time.sleep(60)


