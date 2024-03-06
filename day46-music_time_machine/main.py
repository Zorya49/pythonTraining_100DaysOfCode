import os
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "playlist-modify-private"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        show_dialog=True,
        cache_path="token.txt"
    )
)

status_code = 0
while status_code != 200:
    picked_date = input("Which day do you want to travel to? Type date in format YYYY-MM-DD: ")
    b100_webpage = requests.get(f"https://www.billboard.com/charts/hot-100/{picked_date}/")
    status_code = b100_webpage.status_code
    if status_code != 200:
        print("Wrong date, try again!")

soup = BeautifulSoup(b100_webpage.text, "html.parser")
songs = soup.find_all(name="div", class_="o-chart-results-list-row-container")

songs_titles = []
for song in songs:
    title = song.find(name="h3", id="title-of-a-story")
    songs_titles.append(title.getText().strip())

song_uris = []
year = picked_date.split("-")[0]
year_earlier = str(int(year)-1)
for song in songs_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        # Check also for case when track was released year earlier
        result = sp.search(q=f"track:{song} year:{year_earlier}", type="track")
        try:
            uri = result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
        except IndexError:
            print(f"{song} doesn't exist in Spotify. Skipped.")

user_id = sp.current_user()["id"]
playlist = sp.user_playlist_create(user=user_id, name=f"{picked_date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
