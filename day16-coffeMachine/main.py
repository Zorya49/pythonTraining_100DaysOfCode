import time

MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
    "money": 0
}


def show_resources():
    print(f"Water: {resources["water"]}")
    print(f"Milk: {resources["milk"]}")
    print(f"Coffee: {resources["coffee"]}")
    print(f"Money: ${resources["money"]}")


def is_resources_available(drink_type, current_resources):
    global MENU
    if MENU[drink_type]["ingredients"]["water"] > current_resources["water"]:
        print("Sorry there is not enough water.")
        return False
    if "milk" in MENU[drink_type]["ingredients"]:
        if MENU[drink_type]["ingredients"]["milk"] > current_resources["milk"]:
            print("Sorry there is not enough water.")
            return False
    if MENU[drink_type]["ingredients"]["coffee"] > current_resources["coffee"]:
        print("Sorry there is not enough coffee beans.")
        return False
    return True


def collect_payment():
    print("Please insert coins.")
    quarters = int(input("How many quarters?: "))
    dimes = int(input("How many dimes?: "))
    nickles = int(input("How many nickles?: "))
    pennies = int(input("How many pennies?: "))

    return quarters * 0.25 + dimes * 0.1 + nickles * 0.05 + pennies * 0.01


def update_resources(drink_type, current_resources):
    global MENU
    current_resources["water"] -= MENU[drink_type]["ingredients"]["water"]
    if "milk" in MENU[drink_type]["ingredients"]:
        current_resources["milk"] -= MENU[drink_type]["ingredients"]["milk"]
    current_resources["coffee"] -= MENU[drink_type]["ingredients"]["coffee"]
    current_resources["money"] += MENU[drink_type]["cost"]


while True:
    order = input("What would you like? (espresso/latte/cappuccino): ").lower()

    if order == "report":
        show_resources()
        continue

    if order == "off":
        print("Turning off the machine...")
        time.sleep(1)
        exit(0)

    if order not in MENU:
        continue

    if not is_resources_available(order, resources):
        continue

    payment = collect_payment()
    if payment >= MENU[order]["cost"]:
        change = round(payment - MENU[order]["cost"], 2)
        update_resources(order, resources)
        print(f"Here is ${change} in change.")
        print(f"Here is your {order} ☕ Enjoy!")
    else:
        print("Sorry that's not enough money. Money refunded.")



