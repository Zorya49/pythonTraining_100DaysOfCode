import time
from turtle import Screen
import random
from player import Player, FINISH_LINE_Y
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.title("Turtle Crossing")
screen.tracer(0)

scoreboard = Scoreboard()
turtle = Player()
car_manager = CarManager()
level = 1

screen.listen()
screen.onkeypress(turtle.move_forward, "Up")

game_is_on = True

while game_is_on:
    screen.update()
    time.sleep(0.1)
    car_manager.move(level)

    if random.randint(1, 7) == 1:
        car_manager.create_car()

    for car in car_manager.all_cars:
        if turtle.distance(car) < 20:
            scoreboard.game_over()
            game_is_on = False

    if turtle.ycor() > FINISH_LINE_Y:
        scoreboard.increase_level()
        turtle.go_to_start_position()
        level += 1

screen.exitonclick()
