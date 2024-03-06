from tkinter import *

window = Tk()
window.title("First GUI Program")
window.minsize(500,400)
window.config(padx=50, pady=50)

# Label
my_label = Label(text="I am a label.", font=("Comic Sans MS", 20))
# my_label.pack()
my_label.grid(row=0, column=0)

my_label["text"] = "New Text"
my_label.config(text="New Text 2")

# Button
def button_clicked():
    # my_label.config(text="Button clicked!")
    in_text = entry.get()
    my_label.config(text=in_text)


button = Button(text="click here!", command=button_clicked)
# button.pack()
button.grid(row=1, column=1)

# Entry
entry = Entry(width=10)
# entry.pack()
entry.grid(row=2, column=3)

# Button2
button2 = Button(text="sad useless button")
# button.pack()
button2.grid(row=0, column=2)

window.mainloop()
