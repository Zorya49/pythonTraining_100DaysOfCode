from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class FormFiller:
    def __init__(self):
        self.driver = webdriver.Firefox()

    def load_page(self, form_url):
        self.driver.get(form_url)
        sleep(3)

    def fill_and_send(self, offer):
        try:
            input_address = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            input_price = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            input_link = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            input_address.send_keys(offer["address"])
            input_price.send_keys(offer["price"])
            input_link.send_keys(offer["link"])
            btn_send = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div')
            btn_send.click()
        except NoSuchElementException:
            print(f"Error during filling the form: 'NoSuchElementException'")

    def upload_offers(self, form_url, offers_list):
        for offer in offers_list:
            self.load_page(form_url)
            sleep(1)
            self.fill_and_send(offer)
            sleep(1)

    def __del__(self):
        self.driver.quit()