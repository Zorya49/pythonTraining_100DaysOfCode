from turtle import Turtle
MOVE_DISTANCE = 20
SCREEN_HEIGHT = 1000


class Bullet(Turtle):
    def __init__(self, position):
        super().__init__()
        self.speed(0)
        self.shape("arrow")
        self.color("silver")
        self.penup()
        self.setheading(90)
        self.shapesize(0.3, 1)
        self.goto(position)
        self.dy = MOVE_DISTANCE
        self.state = "ready"  # Bullet is ready to be fired

    def move(self):
        self.sety(self.ycor() + self.dy)
        if self.ycor() > SCREEN_HEIGHT//2:
            self.ht()

    def remove_from_screen(self):
        self.ht()
        self.goto(1000, 1000)
