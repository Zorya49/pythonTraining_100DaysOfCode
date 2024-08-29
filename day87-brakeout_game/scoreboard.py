from turtle import Turtle

ALIGNMENT = "left"
FONT = ("Courier", 24, "normal")
SCORE_FILE = "high_score.txt"

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.high_score = self.load_high_score()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(-580, 360)
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(f"Score: {self.score} High Score: {self.high_score}", align=ALIGNMENT, font=FONT)

    def increase_score(self):
        self.score += 1
        self.update_scoreboard()

    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        self.score = 0
        self.update_scoreboard()

    def load_high_score(self):
        try:
            with open(SCORE_FILE, mode="r") as file:
                return int(file.read())
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(self):
        with open(SCORE_FILE, mode="w") as file:
            file.write(str(self.high_score))