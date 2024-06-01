import tkinter as tk
import random
import time
from tkinter import messagebox
from words import common_words


class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("600x400")
        self.words = common_words
        self.selected_words = random.sample(self.words, 50)
        self.start_time = None
        self.end_time = None
        self.typed_words = []
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Type the following words:", font=("Arial", 14))
        self.label.pack(pady=10)

        self.text_display = tk.Text(self.root, height=10, width=50, wrap="word", font=("Arial", 12))
        self.text_display.insert(tk.END, " ".join(self.selected_words))
        self.text_display.config(state=tk.DISABLED)
        self.text_display.pack(pady=10)

        self.entry = tk.Entry(self.root, font=("Arial", 14))
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.check_typing)

        self.start_button = tk.Button(self.root, text="Start", command=self.start_test, font=("Arial", 14))
        self.start_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

    def start_test(self):
        self.start_time = time.time()
        self.entry.focus()
        self.root.after(30000, self.end_test)  # 30 seconds timer

    def check_typing(self, event):
        typed_word = self.entry.get().strip()
        self.typed_words.append(typed_word)
        self.entry.delete(0, tk.END)

    def end_test(self):
        self.end_time = time.time()
        elapsed_time = self.end_time - self.start_time
        wpm = len(self.typed_words) / (elapsed_time / 60)
        self.result_label.config(text=f"Words per minute: {wpm:.2f}")
        messagebox.showinfo("Test Complete", f"Your typing speed is {wpm:.2f} words per minute.")
        self.entry.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()
