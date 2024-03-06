import time
from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard

screen = Screen()
screen.setup(800, 600)
screen.bgcolor("black")
screen.title("Pong Game")
screen.tracer(0)

is_game_running = True

r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350, 0))
ball = Ball()
scoreboard = Scoreboard()

screen.listen()
screen.onkeypress(r_paddle.up, "Up")
screen.onkeypress(r_paddle.down, "Down")
screen.onkeypress(l_paddle.up, "w")
screen.onkeypress(l_paddle.down, "s")

while is_game_running:
    screen.update()
    ball.move()
    time.sleep(0.1)

    # Detect wall bounce
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    # Detect paddle bounce
    if ball.xcor() > 320 and ball.distance(r_paddle) < 50 or ball.xcor() < -320 and ball.distance(l_paddle) < 50:
        ball.bounce_x()

    # Detect R paddle miss
    if ball.xcor() > 380 and ball.distance(r_paddle) > 50:
        scoreboard.incr_l_score()
        ball.reset()

    # Detect L paddle miss:
    if ball.xcor() < -380 and ball.distance(l_paddle) > 50:
        scoreboard.incr_r_score()
        ball.reset()

screen.exitonclick()
