import tkinter as tk
from tkinter import ttk
import time


class WritingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timed Writing App")
        self.root.geometry("500x400")

        # Variables
        self.inactivity_time = tk.IntVar(value=5)
        self.expected_time = tk.IntVar(value=1)
        self.typing_started = False
        self.inactivity_timer_running = False
        self.last_key_press_time = time.time()
        self.expected_writing_duration = 0

        self.main_view()

    def main_view(self):
        self.clear_view()

        ttk.Label(self.root, text="Select Inactivity Timer:").pack(pady=5)
        ttk.Radiobutton(self.root, text="5 seconds", variable=self.inactivity_time, value=5).pack(pady=2)
        ttk.Radiobutton(self.root, text="10 seconds", variable=self.inactivity_time, value=10).pack(pady=2)

        ttk.Label(self.root, text="Select Expected Writing Time:").pack(pady=5)
        ttk.Radiobutton(self.root, text="1 minute", variable=self.expected_time, value=1).pack(pady=2)
        ttk.Radiobutton(self.root, text="3 minutes", variable=self.expected_time, value=3).pack(pady=2)
        ttk.Radiobutton(self.root, text="5 minutes", variable=self.expected_time, value=5).pack(pady=2)
        ttk.Radiobutton(self.root, text="10 minutes", variable=self.expected_time, value=10).pack(pady=2)

        ttk.Button(self.root, text="Start Typing", command=self.typing_view).pack(pady=20)

    def typing_view(self):
        self.clear_view()

        self.typing_box = tk.Text(self.root, width=50, height=20)
        self.typing_box.pack(pady=10)
        self.typing_box.bind("<KeyPress>", self.on_key_press)

        self.message_label = ttk.Label(self.root, text="", foreground="green")
        self.message_label.pack(pady=5)

        self.typing_started = True
        self.last_key_press_time = time.time()
        self.expected_writing_duration = time.time() + (self.expected_time.get() * 60)
        self.inactivity_timer_running = True

        self.root.after(1000, self.check_inactivity_timer)

    def inactivity_ended_view(self):
        self.clear_view()

        ttk.Label(self.root, text="Inactivity Timer Ended!").pack(pady=20)
        ttk.Button(self.root, text="Restart Game", command=self.main_view).pack(pady=20)

    def clear_view(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def on_key_press(self, event):
        self.last_key_press_time = time.time()

    def check_inactivity_timer(self):
        if not self.typing_started:
            return

        current_time = time.time()
        if current_time >= self.expected_writing_duration:
            self.message_label.config(text="Well done. You've reached expected typing time!")
            self.inactivity_timer_running = False
            return

        if self.inactivity_timer_running and (current_time - self.last_key_press_time) >= self.inactivity_time.get():
            self.typing_box.delete(1.0, tk.END)
            self.inactivity_timer_running = False
            self.typing_started = False
            self.inactivity_ended_view()
        else:
            self.root.after(1000, self.check_inactivity_timer)

if __name__ == "__main__":
    root = tk.Tk()
    app = WritingApp(root)
    root.mainloop()
