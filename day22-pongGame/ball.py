from turtle import Turtle




class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.goto(0, 0)
        self.ball_heading = 30
        self.move_distance = 10

    def move(self):
        self.setheading(self.ball_heading)
        self.forward(self.move_distance)

    def bounce_y(self):
        self.ball_heading *= -1

    def bounce_x(self):
        self.ball_heading = 180 - self.ball_heading
        self.move_distance += 3

    def reset(self):
        self.goto(0, 0)
        self.move_distance = 10
        self.bounce_x()