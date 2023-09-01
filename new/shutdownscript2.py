import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess

class CountdownTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shutdown Timer")
        self.root.geometry("400x300")  # Adjust the window size as needed

        # Load the background image
        self.background_image = tk.PhotoImage(file="background2.png")  # Replace "background.png" with your image file
        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        self.title_label = ttk.Label(root, text="Select shutdown time:")
        self.title_label.pack(pady=10)

        self.create_button("30 Minutes", 100, self.start_shutdown_timer, 30 * 60)
        self.create_button("1 Hour", 150, self.start_shutdown_timer, 60 * 60)
        self.create_button("2 Hours", 200, self.start_shutdown_timer, 2 * 60 * 60)
        self.create_button("Cancel", 250, self.cancel_shutdown_timer)
        self.timer_id = None

        self.disable_cancel_button()

    def create_button(self, text, y, command, seconds=None):
        button = ttk.Button(self.root, text=text, command=lambda: command(seconds) if seconds else command())
        button.place(x=75, y=y)

    def start_shutdown_timer(self, seconds):
        self.title_label.config(text="Shutting down in:")
        self.disable_buttons()
        self.enable_cancel_button()
        self.cancel_timer()

        self.remaining_seconds = seconds
        self.update_clock()
        self.timer_id = self.root.after(1000, self.update_timer)

    def cancel_shutdown_timer(self):
        self.title_label.config(text="Select shutdown time:")
        self.enable_buttons()
        self.disable_cancel_button()
        self.cancel_timer()

    def update_clock(self):
        minutes, seconds = divmod(self.remaining_seconds, 60)
        self.title_label.config(text=f"Shutting down in: {minutes:02}:{seconds:02}")

    def update_timer(self):
        if self.remaining_seconds <= 0:
            self.shutdown_computer()
        else:
            self.remaining_seconds -= 1
            self.update_clock()
            self.timer_id = self.root.after(1000, self.update_timer)

    def cancel_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def disable_buttons(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Button) and widget["text"] != "Cancel":
                widget.state(['disabled'])

    def enable_buttons(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Button) and widget["text"] != "Cancel":
                widget.state(['!disabled'])

    def disable_cancel_button(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Button) and widget["text"] == "Cancel":
                widget.state(['disabled'])

    def enable_cancel_button(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Button) and widget["text"] == "Cancel":
                widget.state(['!disabled'])

    def shutdown_computer(self):
        try:
            subprocess.run(["shutdown", "/s", "/t", "0"], check=True)
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Failed to initiate shutdown")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownTimerApp(root)
    root.mainloop()
