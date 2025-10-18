import tkinter as tk
from tkinter import colorchooser

class PixelGrid(tk.Tk):
    def __init__(self, rows=16, cols=16, pixel_size=25):
        super().__init__()
        self.title("Pixel Selection & Coloring")
        self.rows = rows
        self.cols = cols
        self.pixel_size = pixel_size

        # State
        self.selection_enabled = False
        self.color_enabled = False
        self.selected_pixels = set()  # set of (row, col) tuples

        self.pixels = {}  # {(row,col): frame}

        self.create_ui()
        self.create_grid()

    def create_ui(self):
        # Top button to participate
        self.participate_button = tk.Button(self, text="I want to participate", command=self.enable_selection)
        self.participate_button.pack(pady=10)

        # Frame for grid
        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack()

        # Bottom frame for selection info and confirm
        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.pack(pady=10)
        self.selection_label = tk.Label(self.bottom_frame, text="")
        self.selection_label.pack(side=tk.LEFT)
        self.confirm_button = tk.Button(self.bottom_frame, text="Confirm selection", command=self.confirm_selection)
        self.confirm_button.pack(side=tk.LEFT, padx=10)
        self.confirm_button.config(state="disabled")

    def create_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                frame = tk.Frame(
                    self.grid_frame,
                    width=self.pixel_size,
                    height=self.pixel_size,
                    bg="white",
                    highlightbackground="gray",
                    highlightthickness=1
                )
                frame.grid(row=r, column=c)
                frame.bind("<Button-1>", lambda e, row=r, col=c: self.on_pixel_click(row, col))
                self.pixels[(r, c)] = frame

    def enable_selection(self):
        self.selection_enabled = True
        self.participate_button.config(state="disabled")
        self.selection_label.config(text="Select pixels you want")
        self.confirm_button.config(state="normal")

    def on_pixel_click(self, row, col):
        if self.selection_enabled and not self.color_enabled:
            # selection mode
            if (row, col) not in self.selected_pixels:
                self.selected_pixels.add((row, col))
                self.pixels[(row, col)].config(bg="lightblue")
            else:
                self.selected_pixels.remove((row, col))
                self.pixels[(row, col)].config(bg="white")
            self.selection_label.config(text=f"Selected pixels: {len(self.selected_pixels)}")

        elif self.color_enabled:
            # coloring mode
            if (row, col) in self.selected_pixels:
                color = colorchooser.askcolor(title="Choose color")[1]
                if color:
                    self.pixels[(row, col)].config(bg=color)

    def confirm_selection(self):
        if len(self.selected_pixels) == 0:
            self.selection_label.config(text="Select at least one pixel before confirming.")
            return
        self.selection_enabled = False
        self.color_enabled = True
        self.confirm_button.config(state="disabled")
        self.selection_label.config(text=f"{len(self.selected_pixels)} pixels confirmed. Now color only these.")

if __name__ == "__main__":
    app = PixelGrid(rows=20, cols=20, pixel_size=20)
    app.mainloop()
