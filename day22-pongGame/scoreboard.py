from turtle import Turtle
ALIGN = "center"
FONT = ('Comic Sans MS', 60, 'normal')


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.l_score = 0
        self.r_score = 0
        self.color("white")
        self.penup()
        self.ht()
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.goto(-100, 200)
        self.write(self.l_score, align=ALIGN, font=FONT)
        self.goto(100, 200)
        self.write(self.r_score, align=ALIGN, font=FONT)

    def gameover(self):
        self.goto(0, 0)
        self.write("GAME OVER", align=ALIGN, font=FONT)

    def incr_l_score(self):
        self.l_score += 1
        self.update_scoreboard()

    def incr_r_score(self):
        self.r_score += 1
        self.update_scoreboard()


