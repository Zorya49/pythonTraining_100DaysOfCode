from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10


class CarManager:
    def __init__(self):
        self.all_cars = []

    def create_car(self):
        new_car = Turtle("square")
        new_car.color(random.choice(COLORS))
        new_car.shapesize(1, 2)
        new_car.penup()
        new_car.goto(300, random.randint(-250, 250))
        new_car.setheading(180)
        self.all_cars.append(new_car)

    def move(self, level):
        for car in self.all_cars:
            car.forward(STARTING_MOVE_DISTANCE + (level - 1) * MOVE_INCREMENT)
