from tkinter import *

window = Tk()
window.title("mile2km Converter")
window.minsize(500, 400)
window.config(padx=20, pady=20)

# Label1
label1 = Label(text="miles", justify="left", font=("Comic Sans MS", 15))
label1.grid(row=0, column=2)

# Label2
label2 = Label(text="km", justify="left", font=("Comic Sans MS", 15))
label2.grid(row=1, column=2)

# Label3
label3 = Label(text="is equal to", justify="right", font=("Comic Sans MS", 15))
label3.grid(row=1, column=0)

# Entry
entry = Entry(width=10)
entry.grid(row=0, column=1)

# Text
text = Text(width=15, height=1)
text.grid(row=1, column=1)

# Button
def button_clicked():
    # my_label.config(text="Button clicked!")
    kilometers = str(round(float(entry.get()) * 1.609344, 2))
    text.delete('1.0', END)
    text.insert(END, kilometers)

button = Button(text="Calculate", command=button_clicked)
button.grid(row=2, column=1)



window.mainloop()

