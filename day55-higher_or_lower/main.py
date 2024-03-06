import random

from flask import Flask
app = Flask(__name__)
number = 0


def correct():
    return ('<h1 style="color: green">You found me!</h1>'
            '<img src="https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif"/>')


def too_low():
    return ('<h1 style="color: red">Too low, try again!</h1>'
            '<img src="https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif"/>')


def too_high():
    return ('<h1 style="color: purple">Too high, try again!</h1>'
            '<img src="https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif"/>')


@app.route('/')
def guess_number():
    return ('<h1>Guess a number between 0 and 9</h1>'
            '<img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif">')


@app.route('/<guessed_number>')
def check_number(guessed_number):
    try:
        guess = int(guessed_number)
    except ValueError or TypeError:
        return "Please input a valid integer!"

    if not 0 <= guess <= 9:
        return "Please input an integer between 0 and 9!"

    if guess < number:
        return too_low()
    elif guess > number:
        return too_high()
    else:
        return correct()


if __name__ == "__main__":
    number = random.randint(0, 9)
    app.run(debug=True)
