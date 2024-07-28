import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException

# 1. Preparation + functions
URL = "https://games-stats.com/steam/"
df = pd.DataFrame(columns=['Name', 'Release Date', 'Price', 'Categories', 'Followers', 'Reviews', 'Rating'])
data = []


def convert_to_int(value):
    try:
        return int(value.replace(',', ''))
    except ValueError:
        return np.nan


def get_games_info():
    rows = driver.find_elements(By.CSS_SELECTOR, "tr")

    for row in rows:
        try:
            game_name_element = row.find_element(By.XPATH, ".//td/a[not(@target)]")
            game_name = game_name_element.text

            release_date_element = row.find_element(By.CSS_SELECTOR, "td span[title]")
            release_date = release_date_element.get_attribute("title")

            try:
                discounted_price_element = row.find_element(By.CSS_SELECTOR, "span.mr-1[style*='color: red']")
                current_price = discounted_price_element.text
            except NoSuchElementException:
                try:
                    regular_price_element = row.find_element(By.XPATH, "td[4]")
                    current_price = regular_price_element.text
                except NoSuchElementException:
                    current_price = None

            category_elements = row.find_elements(By.CSS_SELECTOR, "span.badge-pill")
            categories = [category.text for category in category_elements if category.text != '']

            followers_element = row.find_element(By.XPATH, "td[6]")
            followers = convert_to_int(followers_element.text)

            reviews_element = row.find_element(By.XPATH, "td[7]")
            reviews = convert_to_int(reviews_element.text)

            rating_element = row.find_element(By.XPATH, "td[8]")
            rating = rating_element.text

            data.append(
                {'Name': game_name, 'Release Date': release_date, 'Price': current_price,
                 'Categories': categories, 'Followers': followers, 'Reviews': reviews, 'Rating': rating}
            )

        except Exception as e2:
            print(f"Error: {e2}")
            continue


# 2. Web Scraping
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get(URL)

wait = WebDriverWait(driver, 10)
wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "table")))  # Wait for the table to load

btn_consent = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/div[2]/div[2]/button[1]')
btn_consent.click()

get_games_info()

for n in range(5):
    try:
        pagination_links = driver.find_elements(By.CSS_SELECTOR, "li.page-item a.page-link")
        if pagination_links:
            last_page_link = pagination_links[-1]
            last_page_link.get_attribute("href")
            driver.get(last_page_link.get_attribute("href"))
            wait = WebDriverWait(driver, 10)
            wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "table")))  # Wait for the table to load
            get_games_info()
        else:
            print("No pagination links found.")
            break
    except Exception as e:
        print(f"Error: {e}")
        break

driver.close()

# 3. Put all data into Pandas' DataFrame and save
df = pd.DataFrame(data)
df['Release Date'] = pd.to_datetime(df['Release Date'], format='%b %d, %Y')
df.to_csv("games_data.csv")
