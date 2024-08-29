import turtle

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 1000

def setup_screen():
    window = turtle.Screen()
    window.bgcolor("black")
    window.title("Space Invaders")
    window.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    window.tracer(0)
    draw_border()
    return window


def draw_border():
    border = turtle.Turtle()
    border.speed(0)
    border.color("white")
    border.penup()
    border.setposition(((-SCREEN_WIDTH)//2), ((-SCREEN_HEIGHT)//2))
    border.pendown()
    border.pensize(3)
    for side in range(2):
        border.fd(SCREEN_WIDTH)
        border.lt(90)
        border.fd(SCREEN_HEIGHT)
        border.lt(90)
    border.hideturtle()