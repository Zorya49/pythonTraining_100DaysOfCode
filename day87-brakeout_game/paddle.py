from turtle import Turtle

MOVE_DISTANCE = 50
SCREEN_WIDTH = 1200


class Paddle(Turtle):
    def __init__(self):
        super().__init__()
        self.speed(0)
        self.shape("square")
        self.color("blue")
        self.shapesize(stretch_wid=1, stretch_len=10)
        self.penup()
        self.goto(0, -350)

    def move_right(self):
        x = self.xcor() + MOVE_DISTANCE
        self.setx(min(x, (SCREEN_WIDTH // 2) - 50))

    def move_left(self):
        x = self.xcor() - MOVE_DISTANCE
        self.setx(max(x, -(SCREEN_WIDTH // 2) + 50))
