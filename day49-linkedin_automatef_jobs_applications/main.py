import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

APPLY_FOR_OFFERS = 1
SAVE_OFFERS = 2
ACCOUNT_USERNAME = os.getenv('ACCOUNT_USERNAME')
ACCOUNT_PASSWORD = os.getenv('ACCOUNT_PASSWORD')
PHONE = os.getenv('PHONE')

url = ("https://www.linkedin.com/jobs/search/?currentJobId=3825113949&f_LF=f_AL&geoId=90009830&keywords=python"
       "%20tester&location=Krak%C3%B3w%20i%20okolice&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true")


def apply():
    try:
        btn_apply = driver.find_element(by=By.CSS_SELECTOR, value=".jobs-s-apply button")
        btn_apply.click()

        time.sleep(1)
        input_phone = driver.find_element(by=By.CSS_SELECTOR, value="input[id*=phoneNumber]")
        input_phone.send_keys(PHONE)

        btn_submit = driver.find_element(by=By.CSS_SELECTOR, value="footer button")
        if btn_submit.get_attribute("aria-label") == "Przejdź do następnego kroku":
            abort_application()
            # Complex application - skip
            return
        else:
            btn_submit.click()

        time.sleep(1)
        btn_close = driver.find_element(by=By.CLASS_NAME, value="artdeco-modal__dismiss")
        btn_close.click()

    except NoSuchElementException:
        abort_application()
        # No application button - skip
        return


def abort_application():
    # Click Close Button
    btn_close = driver.find_element(by=By.CLASS_NAME, value="artdeco-modal__dismiss")
    btn_close.click()

    time.sleep(2)
    # Click Discard Button
    btn_confirm = driver.find_elements(by=By.CLASS_NAME, value="artdeco-modal__confirm-dialog-btn")[1]
    btn_confirm.click()


def save_offer():
    btn_save_offer = driver.find_element(By.XPATH, "//*[@id='main']/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div["
                                                   "1]/div/div[1]/div[1]/div[4]/div/button/span[1]")
    btn_save_offer.click()

mode = 0
while mode != APPLY_FOR_OFFERS and mode != SAVE_OFFERS:
    mode = int(input(f"What would you like; apply for offers (type '1') or just save them (type '2')? "))

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get(url)

time.sleep(1)
btn_signin = driver.find_element(By.XPATH, '/html/body/div[3]/header/nav/div/a[2]')
btn_signin.click()

time.sleep(1)
input_username = driver.find_element(By.ID, "username")
input_password = driver.find_element(By.ID, "password")
btn_signin2 = driver.find_element(By.XPATH, "//*[@id='organic-div']/form/div[3]/button")

input_username.send_keys(ACCOUNT_USERNAME)
input_password.send_keys(ACCOUNT_PASSWORD)
btn_signin2.click()

time.sleep(15)

all_results = driver.find_elements(By.CLASS_NAME, "job-card-container--clickable")

for result in all_results:
    result.click()
    time.sleep(1)

    if mode == SAVE_OFFERS:
        save_offer()
    elif mode == APPLY_FOR_OFFERS:
        apply()

if mode == SAVE_OFFERS:
    print(f"Saved {len(all_results)} offers!")
elif mode == APPLY_FOR_OFFERS:
    print(f"Applied for {len(all_results)} offers!")

time.sleep(5)
driver.quit()
