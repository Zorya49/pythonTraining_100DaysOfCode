from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine
import time

current_menu = Menu()
coffee_machine = CoffeeMaker()
money_machine = MoneyMachine()

while True:
    request = input(f"What would you like? ({current_menu.get_items()}): ").lower()

    if request == "report":
        coffee_machine.report()
        money_machine.report()
        continue

    if request == "off":
        print("Turning off the machine...")
        time.sleep(1)
        exit(0)

    ordered_drink = current_menu.find_drink(request)
    if ordered_drink is None:
        continue

    if coffee_machine.is_resource_sufficient(ordered_drink) and money_machine.make_payment(ordered_drink.cost):
        coffee_machine.make_coffee(ordered_drink)