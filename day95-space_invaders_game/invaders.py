from turtle import Turtle
import random

COLORS = ['green', 'dark green', 'olive drab', 'dark sea green', 'forest green']
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 1000
WALL_BOTTOM_POS = SCREEN_HEIGHT//2 - 200
WALL_TOP_POS = SCREEN_HEIGHT//2 - 50
WALL_LEFT_POS = -SCREEN_WIDTH // 2 + 50
WALL_RIGHT_POS = SCREEN_WIDTH // 2 - 200
WALL_Y_DIST = 25
WALL_X_DIST = 35

wall_movement = 5


class Invader(Turtle):
    def __init__(self, xpos, ypos):
        super().__init__()
        self.speed(0)
        self.shape("square")
        self.color(random.choice(COLORS))
        self.penup()
        self.goto(xpos, ypos)

    def remove_from_screen(self):
        self.ht()
        self.goto(1000, 1000)


class InvadersWall:
    def __init__(self):
        self.invaders = []
        self.create_invaders()

    def create_invaders(self):
        delta = 0
        for y in range(WALL_BOTTOM_POS, WALL_TOP_POS, WALL_Y_DIST):
            delta = (delta + 20) % 60
            for x in range(WALL_LEFT_POS, WALL_RIGHT_POS, WALL_X_DIST):
                brick = Invader(x + delta, y)
                self.invaders.append(brick)

    def check_wall_collision(self):
        collision = False
        for invader in self.invaders:
            if invader.xcor() > (SCREEN_WIDTH // 2 - 20) or invader.xcor() < (-SCREEN_WIDTH // 2 + 20):
                collision = True
        return collision

    def move_invaders(self):
        global wall_movement

        for invader in self.invaders:
            x = invader.xcor()
            x += wall_movement
            invader.setx(x)

        if self.check_wall_collision():
            wall_movement *= -1
            for invader in self.invaders:
                y = invader.ycor()
                y -= 10
                invader.sety(y)

    def remove_invader(self, invader):
        invader.remove_from_screen()
        self.invaders.remove(invader)
