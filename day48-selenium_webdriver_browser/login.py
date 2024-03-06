from selenium import webdriver
from selenium.webdriver.common.by import By

url = "http://secure-retreat-92358.herokuapp.com/"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get(url)

# Input phrase to searchbar and click on button
first_name = driver.find_element(By.NAME, "fName")
last_name = driver.find_element(By.NAME, "lName")
email = driver.find_element(By.NAME, "email")

first_name.send_keys("Jack")
last_name.send_keys("Python")
email.send_keys("Jack.Python@python.org")

signup_button = driver.find_element(By.CLASS_NAME, "btn-block")
signup_button.click()


# driver.quit()
