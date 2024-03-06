from tkinter import *
from tkinter import messagebox
from random import choice, shuffle, randint
import pyperclip
import json
FONT_NAME = "Courier New"
DEFAULT_USERNAME = "mail@domena.pl"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
#from Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = randint(8, 10)
    nr_symbols = randint(3, 4)
    nr_numbers = randint(3, 4)

    password_letters = [choice(letters) for _ in range(nr_letters)]
    password_symbols = [choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    new_password = "".join(password_list)

    entry_password.delete(0, END)
    entry_password.insert(0, new_password)
    pyperclip.copy(new_password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_pw_to_db():
    if entry_website.get() == "" or entry_username.get() == "" or entry_password.get() == "":
        messagebox.showinfo(title="Saving error",
                             message="Some ofthe fields are missing.\nPlease insert all data.")
        return

    is_ok = messagebox.askokcancel(title=entry_website.get(),
                           message=f"These are the details entered: \n"
                                   f"Username: {entry_username.get()}\n"
                                   f"Password: {entry_password.get()}\n"
                                   f"Is it ok to save?")
    if not is_ok:
        return

    entry_to_save = {
        entry_website.get(): {
            "username": entry_username.get(),
            "password": entry_password.get()
        }
    }

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        with open("data.json", "w") as data_file:
            json.dump(entry_to_save, data_file, indent=4)
    else:
        data.update(entry_to_save)
        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)
    finally:
        entry_website.delete(0, END)
        entry_username.delete(0, END)
        entry_password.delete(0, END)
        entry_username.insert(0, DEFAULT_USERNAME)
        entry_website.focus()

# SEARCH AND SHOW PASSWORD
def find_password():
    website = entry_website.get()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="No data file",
                             message="No data file found.")
        return
    #Option1: using if/else
    # else:
    #     if website in data:
    #         saved_username = data[website]["username"]
    #         saved_password = data[website]["password"]
    #         messagebox.showinfo(title=website,
    #                             message=f"Email: {saved_username}\n"
    #                                     f"Password: {saved_password}")
    #     else:
    #         messagebox.showerror(title="No website exist",
    #                              message=f"Website {website} not found in data file.")

    #Option2: using try/except
    try:
        saved_username = data[website]["username"]
        saved_password = data[website]["password"]
        messagebox.showinfo(title=website,
                            message=f"Email: {saved_username}\n"
                                    f"Password: {saved_password}")
    except KeyError:
        messagebox.showerror(title="No website exist",
                             message=f"Website {website} not found in data file.")
        return

    entry_website.delete(0, END)
    entry_website.focus()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)



canvas = Canvas(width=200, height=220)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# labels
lbl_website = Label()
lbl_website.config(text="Website:", font=(FONT_NAME, 12))
lbl_website.grid(row=1, column=0)

lbl_username = Label()
lbl_username.config(text="Email/Username:", font=(FONT_NAME, 12))
lbl_username.grid(row=2, column=0)

lbl_password = Label()
lbl_password.config(text="Password:", font=(FONT_NAME, 12))
lbl_password.grid(row=3, column=0)

# entries
entry_website = Entry()
entry_website.config(width=33)
entry_website.grid(row=1, column=1)
entry_website.focus()

entry_username = Entry()
entry_username.config(width=52)
entry_username.grid(row=2, column=1, columnspan=2)
entry_username.insert(0, DEFAULT_USERNAME)

entry_password = Entry()
entry_password.config(width=33)
entry_password.grid(row=3, column=1)

# buttons
btn_search = Button(text="Search", command=find_password, width=15)
btn_search.grid(row=1, column=2)

btn_gen_pw = Button(text="Generate password", command=generate_password, width=15)
btn_gen_pw.grid(row=3, column=2)

btn_add_to_db = Button(text="Add to password database",
                       command=add_pw_to_db, width=44)
btn_add_to_db.grid(row=4, column=1, columnspan=2)

window.mainloop()
