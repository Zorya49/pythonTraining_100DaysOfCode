from selenium import webdriver
from selenium.webdriver.common.by import By

url = "https://orteil.dashnet.org/experiments/cookie/"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get(url)
cookie = driver.find_element(By.ID, "cookie")
buy_list = []
buy_cursor = driver.find_element(By.ID, "buyCursor")
buy_grandma = driver.find_element(By.ID, "buyGrandma")
buy_factory = driver.find_element(By.ID, "buyFactory")
buy_mine = driver.find_element(By.ID, "buyMine")
buy_shipment = driver.find_element(By.ID, "buyShipment")
buy_alab = driver.find_element(By.ID, "buyAlchemy lab")

print()
upgrades_params = {
    "cursor": {
        "price": 15,
        "cps": 0.2,
        "profitability": 0.013
    },
    "grandma": {
        "price": 100,
        "cps": 1,
        "profitability": 0.010
    },
    "factory": {
        "price": 500,
        "cps": 4,
        "profitability": 0.008
    },
    "mine": {
        "price": 2000,
        "cps": 10,
        "profitability": 0.005
    },
    "shipment": {
        "price": 7000,
        "cps": 20,
        "profitability": 0.00286
    },
    "alab": {
        "price": 2000,
        "cps": 10,
        "profitability": 0.002
    }
}


def clicker():
    for _ in range(50):
        cookie.click()


def calculate_profitability(cps, current_price) -> float:
    return cps / current_price


def update_upgrades():
    upgrades_params["cursor"]["price"] = int(
        driver.find_element(By.XPATH, "/html/body/div[3]/div[5]/div/div[1]/b").text.split(" ")[2].replace(",", ""))
    upgrades_params["grandma"]["price"] = int(
        driver.find_element(By.XPATH, "/html/body/div[3]/div[5]/div/div[2]/b").text.split(" ")[2].replace(",", ""))
    upgrades_params["factory"]["price"] = int(
        driver.find_element(By.XPATH, "/html/body/div[3]/div[5]/div/div[3]/b").text.split(" ")[2].replace(",", ""))
    upgrades_params["mine"]["price"] = int(
        driver.find_element(By.XPATH, "/html/body/div[3]/div[5]/div/div[4]/b").text.split(" ")[2].replace(",", ""))
    upgrades_params["shipment"]["price"] = int(
        driver.find_element(By.XPATH, "/html/body/div[3]/div[5]/div/div[5]/b").text.split(" ")[2].replace(",", ""))
    upgrades_params["alab"]["price"] = int(
        driver.find_element(By.XPATH, "/html/body/div[3]/div[5]/div/div[6]/b").text.split(" ")[3].replace(",", ""))

    for upgrade in upgrades_params:
        upgrades_params[upgrade]['profitability'] = calculate_profitability(upgrades_params[upgrade]['cps'], upgrades_params[upgrade]['price'])
    print(upgrades_params)


def buy_best_upgrade():
    # Create a dictionary to map item names to their corresponding elements
    item_elements = {
        "cursor": driver.find_element(By.ID, "buyCursor"),
        "grandma": driver.find_element(By.ID, "buyGrandma"),
        "factory": driver.find_element(By.ID, "buyFactory"),
        "mine": driver.find_element(By.ID, "buyMine"),
        "shipment": driver.find_element(By.ID, "buyShipment"),
        "alab": driver.find_element(By.ID, "buyAlchemy lab")
    }

    best_item = max(upgrades_params, key=lambda item: upgrades_params[item]["profitability"])

    try:
        # Click the element corresponding to the best item
        item_elements[best_item].click()
    except:
        pass  # Handle the case where the best item is available to buy or not in the dictionary


while True:
    clicker()
    update_upgrades()
    buy_best_upgrade()

# CpS to beat: 105.6
#
# V1: CpS: 69.6 after 5min
# Algo: click 100 times + check and buy 1 available upgrade from the top
# V2: CpS: 166.4 after 5min
# Algo: click 100 times + buy 1 out of 4 upgrades based on profitability
# V3: CpS: 169.2 after 5min
# Algo: click 100 times + buy 1 out of 6 upgrades based on profitability
