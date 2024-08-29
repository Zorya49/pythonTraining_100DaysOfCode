from turtle import Turtle
MOVE_DISTANCE = 5
START_POS = (0, -200)
SCREEN_HEIGHT = 800


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.speed(40)
        self.shape("circle")
        self.color("white")
        self.penup()
        self.goto(START_POS)
        self.dx = MOVE_DISTANCE
        self.dy = MOVE_DISTANCE

    def move(self):
        self.goto(self.xcor() + self.dx, self.ycor() + self.dy)

    def bounce_x(self):
        self.dx *= -1

    def bounce_y(self):
        self.dy *= -1

    def reset_position(self):
        self.goto(START_POS)
        self.dy = MOVE_DISTANCE
