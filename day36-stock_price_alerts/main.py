import os
import requests
from datetime import datetime, timedelta
from twilio.rest import Client

STOCK = "AAPL"
COMPANY_NAME = "Apple"

ALPHAVANTAGE_ENDPOINT = "https://www.alphavantage.co/query"
ALPHAVANTAGE_API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')
STOCK_PARAMS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHAVANTAGE_API_KEY,
    "outputsize": "compact"
}

yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')
NEWS_PARAMS = {
    "q": COMPANY_NAME,
    "from": yesterday,
    "sortBy": "popularity",
    "apiKey": NEWS_API_KEY
}

account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')


def get_prices():
    response = requests.get(url=ALPHAVANTAGE_ENDPOINT, params=STOCK_PARAMS)
    response.raise_for_status()
    prices_data = response.json()
    yesterday_closing = list(prices_data["Time Series (Daily)"].values())[0]["4. close"]
    dayb4_yesterday_closing = list(prices_data["Time Series (Daily)"].values())[1]["4. close"]
    return [float(yesterday_closing), float(dayb4_yesterday_closing)]


def get_news():
    news_text = ""
    response = requests.get(url=NEWS_ENDPOINT, params=NEWS_PARAMS)
    response.raise_for_status()
    news_data = response.json()
    for news_counter in range(3):
        news_text += f"Source: {news_data["articles"][news_counter]["source"]["name"]} \n"
        news_text += f"Headline: {news_data["articles"][news_counter]["title"]} \n"
        news_text += f"URL: {news_data["articles"][news_counter]["url"]} \n"
    return news_text


def send_alert(alert):
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
                body=alert,
                from_='+13159152760',
                to=os.getenv('MY_PHONE')
                )
    print(message.status)


prices = get_prices()
percentage_change = round((prices[0]-prices[1])/prices[1]*100, 2)

if percentage_change > 2:
    alert_msg = f"\n↗️ Rise of {percentage_change}%\n{get_news()}"
    send_alert(alert_msg)
elif percentage_change < 2:
    alert_msg = f"\n↘️ Drop of {percentage_change}%\n{get_news()}"
    send_alert(alert_msg)
else:
    pass
