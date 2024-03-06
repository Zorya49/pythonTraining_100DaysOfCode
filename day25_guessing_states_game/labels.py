from turtle import Turtle
ALIGN = "center"
FONT = ('Comic Sans MS', 8, 'normal')


class Labels:
    def create_label(self, label, position):
        new_label = Turtle()
        new_label.color("black")
        new_label.penup()
        new_label.ht()
        new_label.goto(position)
        new_label.write(label, align=ALIGN, font=FONT)

