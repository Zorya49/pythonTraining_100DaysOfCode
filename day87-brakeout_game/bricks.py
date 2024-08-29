from turtle import Turtle
import random

COLORS = ['light blue', 'light steel blue', 'light sky blue', 'blue', 'steel blue', 'light cyan']
WALL_BOTTOM_POS = 0
WALL_TOP_POS = 250
WALL_Y_DIST = 30
WALL_X_DIST = 80
SCREEN_WIDTH = 1200


class Brick(Turtle):
    def __init__(self, xpos, ypos):
        super().__init__()
        self.speed(0)
        self.shape("square")
        self.color(random.choice(COLORS))
        self.shapesize(stretch_wid=1, stretch_len=3)
        self.penup()
        self.goto(xpos, ypos)
        self.calculate_boundaries()

    def calculate_boundaries(self):
        self.top = self.ycor() + 10
        self.bottom = self.ycor() - 10
        self.left = self.xcor() - 30
        self.right = self.xcor() + 30


class Wall:
    def __init__(self):
        self.bricks = []
        self.create_wall()

    def create_wall(self):
        delta = -20
        for y in range(WALL_BOTTOM_POS, WALL_TOP_POS, WALL_Y_DIST):
            delta = (delta + 20) % 60
            for x in range(-SCREEN_WIDTH // 2 + 50, SCREEN_WIDTH // 2 - 50, WALL_X_DIST):
                brick = Brick(x + delta, y)
                self.bricks.append(brick)

    def remove_brick(self, brick):
        brick.goto(1000, 1000)
        self.bricks.remove(brick)
