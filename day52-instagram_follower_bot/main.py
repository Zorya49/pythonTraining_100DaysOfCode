import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

INSTA_LOGIN = os.getenv('INSTA_LOGIN')
INSTA_PASSWORD = os.getenv('INSTA_PASSWORD')
INSTA_URL = "https://www.instagram.com/"
profile_w_followers_url = "https://www.instagram.com/wkdzik/"


class InstagramFollowerBot:
    def __init__(self):
        self.driver = webdriver.Firefox()

    def load_page(self, url_to_load):
        self.driver.get(url_to_load)
        sleep(3)
        try:
            btn_defer_cookies = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[1]/div/div['
                                                                   '2]/div/div/div/div/div[2]/div/button[2]')
            btn_defer_cookies.click()
            sleep(3)
        except NoSuchElementException:
            pass

    def login(self):
        input_login = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div['
                                                         '1]/section/main/article/div[2]/div[1]/div[2]/form/div/div['
                                                         '1]/div/label/input')
        input_login.send_keys(INSTA_LOGIN)
        input_password = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div['
                                                            '1]/section/main/article/div[2]/div[1]/div['
                                                            '2]/form/div/div[2]/div/label/input')
        input_password.send_keys(INSTA_PASSWORD)
        input_password.send_keys(Keys.ENTER)
        sleep(3)

    def find_followers(self):
        a_followers = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div['
                                                         '2]/div[2]/section/main/div/header/section/ul/li[2]/a')
        a_followers.click()
        sleep(3)
        followers = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div['
                                                       '2]/div/div/div[3]')
        for i in range(100):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers)
            sleep(2)

    def follow_all(self):
        followers_list = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div['
                                                            '2]/div/div/div[3]/div[1]/div')
        follow_buttons = followers_list.find_elements(By.TAG_NAME, 'button')
        for button in follow_buttons:
            try:
                button.click()
                sleep(1)
            except ElementClickInterceptedException:
                cancel_button = self.driver.find_element(by=By.XPATH, value="//button[contains(text(), 'Anuluj')]")
                cancel_button.click()


bot = InstagramFollowerBot()

bot.load_page(url_to_load=INSTA_URL)
bot.login()
bot.load_page(url_to_load=profile_w_followers_url)
bot.find_followers()
bot.follow_all()
