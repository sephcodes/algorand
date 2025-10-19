import tkinter as tk
from tkinter import colorchooser
import logging
from algokit_utils import AlgorandClient, PaymentParams, AlgoAmount

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


class PixelGrid(tk.Tk):
    def __init__(self, rows=16, cols=16, pixel_size=25):
        super().__init__()
        self.title("Pixel Selection & Coloring")
        self.rows = rows
        self.cols = cols
        self.pixel_size = pixel_size

        # State
        self.mode = "idle"  # can be "idle", "selecting", or "coloring"
        self.selected_pixels = set()
        self.colored_pixels = {}  # {(r,c): color}

        self.pixels = {}  # {(row,col): frame}
        self.create_ui()
        self.create_grid()

        # --- Algorand client & deployer ---
        self.algorand = AlgorandClient.from_environment()
        self.deployer = self.algorand.account.from_environment("DEPLOYER")

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
        self.confirm_button = tk.Button(self.bottom_frame, text="Confirm selection", command=self.toggle_confirm)
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
        if self.mode == "idle":
            self.mode = "selecting"
            self.participate_button.config(state="disabled")
            self.confirm_button.config(state="normal")
            self.selection_label.config(text="Select pixels you want")
            self.selected_pixels.clear()

    def on_pixel_click(self, row, col):
        if self.mode == "selecting":
            # selecting pixels
            if (row, col) not in self.selected_pixels:
                self.selected_pixels.add((row, col))
                self.pixels[(row, col)].config(bg="lightblue")
            else:
                self.selected_pixels.remove((row, col))
                prev_color = self.colored_pixels.get((row, col), "white")
                self.pixels[(row, col)].config(bg=prev_color)
            self.selection_label.config(text=f"Selected pixels: {len(self.selected_pixels)}")

        elif self.mode == "coloring":
            # coloring mode: only selected pixels are clickable
            if (row, col) in self.selected_pixels:
                color = colorchooser.askcolor(title="Choose color")[1]
                if color:
                    self.pixels[(row, col)].config(bg=color)
                    self.colored_pixels[(row, col)] = color
                    logger.info(
                        f"Populating row: {row} and col: {col}. "
                        f"All pixels = {self.colored_pixels}"
                    )

    def toggle_confirm(self):
        if self.mode == "selecting":
            # Move to coloring mode
            if len(self.selected_pixels) == 0:
                self.selection_label.config(text="Select at least one pixel before confirming.")
                return
            self.mode = "coloring"
            self.selection_label.config(text=f"{len(self.selected_pixels)} pixels confirmed. Now color only these.")
            self.confirm_button.config(text="Finish session")

        elif self.mode == "coloring":
            # Finish session → send payment
            self.send_payment_for_colored_pixels()

            # Reset to idle mode
            self.mode = "idle"
            self.selection_label.config(text="")
            self.confirm_button.config(state="disabled", text="Confirm selection")
            self.participate_button.config(state="normal")

            # Reset grid visuals but keep colored pixels
            for (r, c), frame in self.pixels.items():
                if (r, c) in self.colored_pixels:
                    frame.config(bg=self.colored_pixels[(r, c)])
                else:
                    frame.config(bg="white")

            self.selected_pixels.clear()

    def send_payment_for_colored_pixels(self):
        num_pixels = len(self.colored_pixels)
        if num_pixels == 0:
            return

        try:
            self.algorand.send.payment(
                PaymentParams(
                    amount=AlgoAmount(algo=2*num_pixels),  # 2 Algos per colored pixel
                    sender=self.deployer.address,
                    receiver="KIJ4QO2B7IHFJXSBBN2VIALRLCA3XIOFQZZFAWL4H2B3GOAWJ52ENE7NTI"
                )
            )
            logger.info(f"✅ Sent payment for {num_pixels} colored pixels.")
        except Exception as e:
            logger.error(f"❌ Failed to send payment: {e}")


if __name__ == "__main__":
    app = PixelGrid(rows=5, cols=5, pixel_size=40)
    app.mainloop()
