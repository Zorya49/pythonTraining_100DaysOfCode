from tkinter import *
from tkinter import messagebox
from random import choice, shuffle, randint
import pandas
BACKGROUND_COLOR = "#B1DDC6"
LANG_FONT = ("Arial", 40, "italic")
WORD_FONT = ("Arial", 60, "bold")

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
finally:
    dictionary_fr_en = data.to_dict(orient="records")

print(dictionary_fr_en)
print(type(dictionary_fr_en))
current_card = {}
was_flipped = True


# ### Flipping Cards ###
def flip_card():
    global current_card, was_flipped
    was_flipped = True
    canvas.itemconfig(card_image, image=img_card_back)
    canvas.itemconfig(card_lang, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")

# ### Changing Cards ###
def pick_card():
    global current_card, flip_timer, was_flipped
    if was_flipped == False:
        dictionary_fr_en.remove(current_card)
    was_flipped = False
    window.after_cancel(flip_timer)
    current_card = choice(dictionary_fr_en)
    canvas.itemconfig(card_image, image=img_card_front)
    canvas.itemconfig(card_lang, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    flip_timer = window.after(3000, flip_card)

# ### UI ###
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526)
img_card_back = PhotoImage(file="images/card_back.png")
img_card_front = PhotoImage(file="images/card_front.png")
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_image = canvas.create_image(400, 263, image=img_card_front)
card_lang = canvas.create_text(400, 150, text="", font=LANG_FONT)
card_word = canvas.create_text(400, 263, text="", font=WORD_FONT)
canvas.grid(row=0, column=0, columnspan=2)

img_wrong = PhotoImage(file="images/wrong.png")
btn_wrong = Button(image=img_wrong, command=flip_card, highlightthickness=0)
btn_wrong.grid(row=1, column=0)

img_right = PhotoImage(file="images/right.png")
btn_right = Button(image=img_right, command=pick_card, highlightthickness=0)
btn_right.grid(row=1, column=1)


flip_timer = window.after(3000, flip_card)
pick_card()


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        data_to_save = pandas.DataFrame(dictionary_fr_en)
        data_to_save.to_csv("data/words_to_learn.csv", index=False)

        window.destroy()


window.protocol("WM_DELETE_WINDOW", on_closing)
window.bind('<Escape>', lambda e: on_closing)
window.mainloop()
