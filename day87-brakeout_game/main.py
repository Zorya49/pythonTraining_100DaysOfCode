import turtle
from paddle import Paddle
from ball import Ball
from bricks import Wall
from scoreboard import Scoreboard
import time

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800


def setup_screen():
    win = turtle.Screen()
    win.title("Breakout Game")
    win.bgcolor("black")
    win.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    win.tracer(0)
    return win


def check_wall_collision(ball, scoreboard):
    if abs(ball.xcor()) > (SCREEN_WIDTH // 2 - 10):
        ball.bounce_x()

    if ball.ycor() > (SCREEN_HEIGHT // 2 - 10):
        ball.bounce_y()

    if ball.ycor() < -(SCREEN_HEIGHT // 2 - 10):
        ball.reset_position()
        scoreboard.reset()
        return True
    return False


def check_paddle_collision(ball, paddle):
    if ball.distance(paddle) < 110 and ball.ycor() == -330:
        ball.bounce_y()


def check_brick_collision(ball, wall, scoreboard):
    for brick in wall.bricks:
        if ball.distance(brick) < 35:
            wall.remove_brick(brick)
            scoreboard.increase_score()
            if ball.xcor() < brick.left or ball.xcor() > brick.right:
                ball.bounce_x()
            elif ball.ycor() > brick.top or ball.ycor() < brick.bottom:
                ball.bounce_y()
            break


def main():
    win = setup_screen()
    paddle = Paddle()
    ball = Ball()
    wall = Wall()
    scoreboard = Scoreboard()

    win.listen()
    win.onkeypress(paddle.move_right, "Right")
    win.onkeypress(paddle.move_left, "Left")

    while True:
        win.update()
        time.sleep(0.01)

        ball.move()
        if check_wall_collision(ball, scoreboard):
            print("You lost!")
            break

        check_paddle_collision(ball, paddle)
        check_brick_collision(ball, wall, scoreboard)

        if len(wall.bricks) == 0:
            print("You won!")
            break

    win.mainloop()

    win.mainloop()


if __name__ == "__main__":
    main()
