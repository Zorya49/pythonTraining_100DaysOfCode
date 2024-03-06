from selenium import webdriver
from selenium.webdriver.common.by import By

url = ("https://www.amazon.pl/Apple-AirPods-3-generacji-laduj%C4%85cym-MagSafe/dp/B09JQQDLXF/ref=sr_1_2?crid"
       "=FR85GMUQRJNO&dib=eyJ2IjoiMSJ9.G2d_enfW69p5zdQ_srBmS8G1941pcrrg0beKJVZpS_6cN1ErMuHO8H3yeO06bbVpZ_oSg0pdAZsYoP"
       "-gzHBvJlJrzY7-eW7Tv0PEaSL5nAufV5Qj4AfmZZLrKQ"
       "-nK6RMLPr_2u2zRUlWLszNgtgz04y_hSwrae4uoHMMexDjWBd_ilE15iqe6yXdbJObJ44v6gPLfyRwMGF-OJYcXDHHlGL2PHlkkPtNcHP"
       "-qOMOPGY41RZrXOAc2LDvbHrsEfk1O2nJUx7Gg0CaXwr9s7TW2Lr1nCypKkrST1CCMkwmTKI"
       ".0rAhDuf_n9hZqiJwxjU7Y7OWldSiVhecZdeLBR-Q9rE&dib_tag=se&keywords=airpods+magsafe&qid=1708550008&sprefix"
       "=airpods+magsa%2Caps%2C111&sr=8-2")
url2 = "https://www.python.org/"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

# Scraping Amazon item price #
# driver.get(url)
# price_whole = driver.find_element(By.CLASS_NAME, value="a-price-whole")
# price_fraction= driver.find_element(By.CLASS_NAME, value="a-price-fraction")
# print(f"The price is {price_whole.text},{price_fraction.text}")

# Scraping Python.org #
# driver.get(url2)

# search_bar = driver.find_element(By.NAME, value="q")
# button = driver.find_element(By.ID, value="submit")
# print(f"The placeholder for Search Bar is '{search_bar.get_attribute("placeholder")}'.")
# print(f"The size of Submit button is {button.size}.")

# documentation_link = driver.find_element(By.CSS_SELECTOR, value=".documentation-widget a")
# print(documentation_link.text)

# wiki_link = driver.find_element(By.XPATH, value='//*[@id="container"]/li[4]/ul/li[9]/a')
# print(wiki_link.text)

# Get list of events from Python.org #
events_dates = driver.find_elements(By.XPATH, value='/html/body/div/div[3]/div/section/div[2]/div[2]/div/ul/li/time')
events_names = driver.find_elements(By.XPATH, value='/html/body/div/div[3]/div/section/div[2]/div[2]/div/ul/li/a')
print(events_dates[4].text)
print(events_names[2].text)

events_dictionary = {}
for event_id in range(len(events_dates)):
    events_dictionary[event_id] = {
       "date": events_dates[event_id].text,
       "name": events_names[event_id].text
    }
print(events_dictionary)

driver.quit()
