from bs4 import BeautifulSoup
import requests


def search_jobs(main_link: str, search_link: str) -> list:
    webpage = requests.get(main_link+search_link)
    soup = BeautifulSoup(webpage.text, "html.parser")
    jobs = soup.find_all(name="span", class_="jobTitle hidden-phone")
    jobs_list = []

    for job_tag in jobs:
        title = job_tag.find("a").getText()
        rel_link = job_tag.find("a").get("href")
        jobs_list.append({"title": title, "link": main_link+rel_link})

    return jobs_list
