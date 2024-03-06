# import colorgram
import turtle
from turtle import Turtle, Screen
import random as r

# image_colors_tuple = []
# image_colors = colorgram.extract('image2.jpg', 16)
# for color in image_colors:
#     image_colors_tuple.append((color.rgb.r, color.rgb.g, color.rgb.b))

final_colors_list = [(54, 108, 149), (225, 201, 108), (134, 85, 58),(224, 141, 62), (197, 144, 171), (143, 180, 206), (137, 82, 106), (210, 90, 68), (232, 226, 194), (188, 78, 122), (69, 101, 86), (132, 183, 132), (65, 156, 86), (137, 132, 74)]

screen = Screen()
tom = Turtle()

screen.colormode(255)

tom.penup()
tom.hideturtle()
tom.speed(100)
tom.teleport(-225, -225)

for row in range(10):
    for _ in range(10):
        tom.dot(20, r.choice(final_colors_list))
        tom.forward(50)
    tom.teleport(-225, -225 + (row + 1) * 50)



screen.exitonclick()