from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

url = "https://en.wikipedia.org/wiki/Main_Page"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get(url)

# Get, print and click articles number #
# article_count = driver.find_element(By.XPATH, '//*[@id="articlecount"]/a[1]')
# print(article_count.text)
# article_count.click()

# Get, print and click articles number #
# all_portals = driver.find_element(By.LINK_TEXT, "Content portals")
# all_portals.click()

# Input phrase to searchbar and click on button
search_bar = driver.find_element(By.NAME, "search")
search_bar.send_keys("Python")
# search_bar.send_keys("Python", Keys.ENTER)
search_button = driver.find_element(By.CLASS_NAME, "cdx-search-input__end-button")
search_button.click()

# driver.quit()
