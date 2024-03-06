import turtle
import pandas
import labels


screen = turtle.Screen()
screen.title("US State Guessing Game")
screen.setup(740, 500)
screen.addshape("blank_states_img.gif")
turtle.shape("blank_states_img.gif")

label = labels.Labels()
guessed = 0
is_game_ongoing = True

states_data = pandas.read_csv("50_states.csv")
states_to_learn = states_data

while is_game_ongoing:
    answer_state = screen.textinput(title=f"{guessed}/50: Guess the State", prompt="What's the next state's name?").title()

    if answer_state == "Exit":
        states_to_learn = states_to_learn.drop(columns=['x', 'y'])
        states_to_learn.to_csv("states_to_learn.csv")
        break

    if answer_state in states_data["state"].values:
        pos_x = int(states_data[states_data.state == answer_state].x)
        pos_y = int(states_data[states_data.state == answer_state].y)
        pos_tuple = (pos_x, pos_y)
        label.create_label(answer_state, pos_tuple)
        guessed += 1

        states_to_learn = states_to_learn.drop(states_to_learn[states_to_learn["state"] == answer_state].index)
