from bs4 import BeautifulSoup
import requests

yc_webpage = requests.get("https://news.ycombinator.com/news")
soup = BeautifulSoup(yc_webpage.text, "html.parser")

articles = soup.find_all(name="span", class_="titleline")
score_tags = soup.find_all(name="span", class_="score")
article_texts = []
article_links = []
article_upvotes = []

for article_tag in articles:
    article_texts.append(article_tag.find("a").getText())
    article_links.append(article_tag.find("a").get("href"))
for score_tag in score_tags:
    score = int(score_tag.getText().split()[0])
    article_upvotes.append(score)
