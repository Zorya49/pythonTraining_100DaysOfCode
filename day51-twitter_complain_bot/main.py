import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

PROMISED_DOWN = 500
PROMISED_UP = 30
X_LOGIN = os.getenv('X_LOGIN')
X_PASSWORD = os.getenv('X_PASSWORD')
X_USERNAME = os.getenv('X_USERNAME')
X_URL = "https://twitter.com/i/flow/login"
ST_URL = "https://www.speedtest.net/"


class InternetSpeedTwitterBot:
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.down_speed = 0
        self.up_speed = 0

    def get_internet_speeds(self):
        self.driver.get(ST_URL)
        sleep(2)

        btn_reject_cookies = self.driver.find_element(By.ID, "onetrust-reject-all-handler")
        btn_reject_cookies.click()

        btn_start_test = self.driver.find_element(By.CLASS_NAME, "js-start-test")
        btn_start_test.click()
        sleep(60)

        self.down_speed = float(self.driver.find_element(By.CLASS_NAME, "download-speed").text)
        self.up_speed = float(self.driver.find_element(By.CLASS_NAME, "upload-speed").text)
        print(f"Measured download speed: {self.down_speed} Mbps")
        print(f"Measured upload speed: {self.up_speed} Mbps")

        return self.down_speed, self.up_speed

    def login_on_x(self):
        input_username = self.driver.find_element(By.XPATH, '/html/body/div/div/div/div['
                                                            '1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div['
                                                            '2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
        input_username.send_keys(X_LOGIN)
        input_username.send_keys(Keys.ENTER)
        sleep(3)
        try:
            input_password = self.driver.find_element(By.XPATH, '/html/body/div/div/div/div['
                                                                '1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div['
                                                                '2]/div[2]/div[1]/div/div/div[3]/div/label/div/div['
                                                                '2]/div[1]/input')
            input_password.send_keys(X_PASSWORD)
            input_password.send_keys(Keys.ENTER)

        except NoSuchElementException:
            username = self.driver.find_element(By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div["
                                                          "2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div["
                                                          "2]/div/input")
            username.send_keys(X_USERNAME)
            username.send_keys(Keys.ENTER)
            sleep(3)
            input_password = self.driver.find_element(By.XPATH, '/html/body/div/div/div/div['
                                                                '1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div['
                                                                '2]/div[2]/div[1]/div/div/div[3]/div/label/div/div['
                                                                '2]/div[1]/input')
            input_password.send_keys(X_PASSWORD)
            input_password.send_keys(Keys.ENTER)

        sleep(3)

    def post_tweet(self, tweet_text):
        input_tweet = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div['
                                                         '2]/main/div/div/div/div/div/div[3]/div/div[2]/div['
                                                         '1]/div/div/div/div[2]/div['
                                                         '1]/div/div/div/div/div/div/div/div/div/div/label/div['
                                                         '1]/div/div/div/div/div/div[2]/div/div/div/div')
        input_tweet.send_keys(tweet_text)

        btn_post = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div['
                                                      '2]/main/div/div/div/div/div/div[3]/div/div[2]/div['
                                                      '1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div')
        btn_post.click()

    def make_a_complaint_on_x(self):
        self.driver.get(X_URL)
        sleep(3)

        self.login_on_x()
        complaint_text = (f"Hey ISP, my download speed is {self.down_speed} and upload speed is {self.up_speed}."
                          f"This is below promised {PROMISED_DOWN}/{PROMISED_UP} Mbps speeds. Check that!")
        self.post_tweet(tweet_text=complaint_text)


bot = InternetSpeedTwitterBot()

measured_speeds = bot.get_internet_speeds()

if measured_speeds[0] < PROMISED_DOWN or measured_speeds[1] < PROMISED_UP:
    bot.make_a_complaint_on_x()
