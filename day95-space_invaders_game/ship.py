from turtle import Turtle

MOVE_DISTANCE = 15
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 1000


class Ship(Turtle):
    def __init__(self):
        super().__init__()
        self.speed(0)
        self.shape("triangle")
        self.color("blue")
        self.setheading(90)
        self.penup()
        self.goto(0, -(SCREEN_HEIGHT//2)+50)

    def move_right(self):
        x = self.xcor() + MOVE_DISTANCE
        if self.xcor() > SCREEN_WIDTH//2-20:
            x = SCREEN_WIDTH//2-20
        self.setx(min(x, SCREEN_WIDTH//2 - 50))

    def move_left(self):
        x = self.xcor() - MOVE_DISTANCE
        if self.xcor() < -SCREEN_WIDTH//2+20:
            x = -SCREEN_WIDTH//2+20
        self.setx(max(x, -(SCREEN_WIDTH//2) + 50))

    def get_position(self):
        x = self.xcor()
        y = self.ycor()
        return x, y

    def remove_from_screen(self):
        self.ht()
        self.goto(1000, 1000)
