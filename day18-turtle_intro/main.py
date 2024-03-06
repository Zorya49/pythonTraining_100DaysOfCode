import random
from turtle import Turtle, Screen
import random as r

marian = Turtle()

marian.shape("triangle")


marian.pendown()

# Square
# for _ in range(4):
#     marian.forward(100)
#     marian.rt(270)

#Dotted line
# for _ in range(20):
#     marian.pendown()
#     marian.forward(10)
#     marian.penup()
#     marian.forward(10)

# Dotted square
# for _ in range(4):
#     for _ in range(20):
#         marian.pendown()
#         marian.forward(10)
#         marian.penup()
#         marian.forward(10)
#     marian.rt(270)

def change_color():
    R = random.random()
    B = random.random()
    G = random.random()

    marian.color(R, G, B)

# Figures
# for n_gon in range(3,11):
#     change_color()
#     for _ in range(n_gon):
#         marian.forward(100)
#         marian.rt(360/n_gon)

# # Random walk
# marian.pensize(20)
# marian.speed(10)
# for _ in range(1000):
#     change_color()
#     marian.rt(r.randint(0, 3) * 90)
#     marian.forward(40)

# Spirograph
marian.speed(1000)
steps = 50
for _ in range(steps):
    change_color()
    marian.circle(100)
    marian.rt(360 / steps)












screen = Screen()
screen.exitonclick()
