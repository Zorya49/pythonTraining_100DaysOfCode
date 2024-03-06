from turtle import Turtle, Screen
import random

screen = Screen()

screen.setup(width=500, height=400)
user_bet = screen.textinput(title="Make your bet!", prompt="Which turtle will win the race?\n(red, orange, yellow, green, blue, indigo, purple)")

positions = [(-240, -150), (-240, -100), (-240, -50), (-240, 0), (-240, 50), (-240, 100), (-240, 150)]
colors = ["red", "orange", "yellow", "green", "blue", "indigo", "purple"]
is_race_on = False

turtles = []

for turtle_idx in range(7):
    turtles.append(Turtle(shape="turtle"))
    turtles[turtle_idx].penup()
    turtles[turtle_idx].color(colors[turtle_idx])
    turtles[turtle_idx].goto(positions[turtle_idx])


if user_bet:
    is_race_on = True

while is_race_on:
    for turtle in turtles:
        random_distance = random.randint(1,10)
        turtle.forward(random_distance)

        if turtle.xcor() > 220:
            is_race_on = False
            winner = turtle.pencolor()


if winner == user_bet.lower():
    print(f"You won! The {winner} turtle is the winner.")
else:
    print(f"You lost! The {winner} turtle is the winner.")

screen.exitonclick()

