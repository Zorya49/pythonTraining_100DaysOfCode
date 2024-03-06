import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Write your code below this line 👇
empire_webpage = requests.get(URL)
soup = BeautifulSoup(empire_webpage.text, "html.parser")

title_tags = soup.find_all("h3", class_="title")

movie_list = []

for tag in title_tags[::-1]:
    movie_list.append(tag.getText())

with open("movies.txt", "w", encoding="utf-8") as file:
    for item in movie_list:
        file.write(f"{item} \n")

file.close()


