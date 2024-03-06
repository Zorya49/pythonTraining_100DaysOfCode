from turtle import Turtle, Screen

pawel = Turtle()
screen = Screen()


def move_forward():
    pawel.forward(10)


def move_backward():
    pawel.backward(10)


def turn_right():
    pawel.rt(10)


def turn_left():
    pawel.lt(10)


def clear_sketch():
    screen.resetscreen()


screen.listen()
screen.onkey(move_forward, "Up")
screen.onkey(move_backward, "Down")
screen.onkey(turn_left, "Left")
screen.onkey(turn_right, "Right")
screen.onkey(clear_sketch, "C")

screen.exitonclick()




