import tkinter as tk
from tkinter import colorchooser, messagebox

class PixelGridApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pixel Grid with Input")
        self.geometry("400x150")

        self.grid_frame = None
        self.pixels = {}
        self.pixel_size = 25

        # Input UI
        self.label = tk.Label(self, text="Enter your steak:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self, justify="center")
        self.entry.pack()

        self.button = tk.Button(self, text="Create Grid", command=self.create_grid_from_input)
        self.button.pack(pady=10)

    def create_grid_from_input(self):
        value = self.entry.get().strip()
        if not value.isdigit():
            messagebox.showerror("Invalid input", "Please enter a valid positive integer.")
            return

        n = int(value)
        if n < 1 or n > 50:
            messagebox.showwarning("Out of range", "Please enter a number between 1 and 50.")
            return

        # Clear previous UI
        self.label.pack_forget()
        self.entry.pack_forget()
        self.button.pack_forget()

        # Resize window dynamically based on grid
        self.geometry(f"{n * self.pixel_size + 50}x{n * self.pixel_size + 50}")

        self.create_grid(n, n)

    def create_grid(self, rows, cols):
        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack(padx=10, pady=10)
        for r in range(rows):
            for c in range(cols):
                frame = tk.Frame(
                    self.grid_frame,
                    width=self.pixel_size,
                    height=self.pixel_size,
                    bg="white",
                    highlightbackground="gray",
                    highlightthickness=1
                )
                frame.grid(row=r, column=c)
                frame.bind("<Button-1>", lambda e, row=r, col=c: self.pick_color(row, col))
                self.pixels[(r, c)] = frame

    def pick_color(self, row, col):
        color = colorchooser.askcolor(title="Choose color")[1]
        if color:
            self.pixels[(row, col)].configure(bg=color)

if __name__ == "__main__":
    app = PixelGridApp()
    app.mainloop()
