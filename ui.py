import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from constants import ASSETS  # Correct import statement

class RangedSlider:
    def __init__(self, master, from_=0.0, to=1.0, value=0.0, step=0.01, label_text="", **kwargs):
        self.frame = ttk.Frame(master)

        # Label for slider section
        self.label = ttk.Label(self.frame, text=label_text, font=("Helvetica", 12))
        self.label.pack(pady=5)

        # Entry widget
        self.value_var = tk.DoubleVar(value=value)
        self.entry = ttk.Entry(self.frame, textvariable=self.value_var, bootstyle="primary", width=15)
        self.entry.pack(pady=(5, 1), fill='x')
        self.entry.bind("<KeyRelease>", self.on_entry_change)

        # Slider widget
        self.slider = ttk.Scale(self.frame, from_=from_, to=to, orient=HORIZONTAL, variable=self.value_var, bootstyle="success", command=self.on_slider_change, length=self.entry.winfo_reqwidth())
        self.slider.pack(pady=(1, 5), fill='x')

        self.frame.pack(pady=10)

    def on_entry_change(self, event):
        value = self.entry.get()
        if self.validate_input(value):
            self.value_var.set(float(value))
            self.slider.set(float(value))
        else:
            self.correct_entry(value)

    def on_slider_change(self, event):
        value = float(self.slider.get())
        self.value_var.set(value)
        self.entry.delete(0, tk.END)
        self.entry.insert(0, f"{value:.2f}")

    def get(self):
        return self.value_var.get()

    def validate_input(self, value):
        try:
            float(value)
            return value.count('.') <= 1
        except ValueError:
            return False

    def correct_entry(self, value):
        corrected = ''.join(c for c in value if c.isdigit() or c == '.')
        parts = corrected.split('.')
        if len(parts) > 2:
            corrected = parts[0] + '.' + ''.join(parts[1:])
        self.entry.delete(0, tk.END)
        self.entry.insert(0, corrected)

# Functions to update boolean variables
def update_check1():
    bool_var1 = check_var1.get()
    print(f"Checkbox 1: {bool_var1}")

def update_check2():
    bool_var2 = check_var2.get()
    print(f"Checkbox 2: {bool_var2}")

# Function to stop the while loop and close the window
def on_closing():
    global running
    running = False
    root.destroy()

# Function to update the trading strategy input field
def update_strategy(event):
    selected_strategy = strategy_var.get()
    if selected_strategy == "Static Bet":
        bet_amount_entry.config(state="normal")
    else:
        bet_amount_entry.config(state="disabled")

# Initialize the main window
root = ttk.Window(themename="flatly")  # Choose a light theme
root.title("Enhanced UI with Slider and Checkboxes")
root.geometry("400x700")  # Increase window size

# Global variables
running = True

# Section Title: Checkboxes Section
checkboxes_section_label = ttk.Label(root, text="Checkboxes Section", font=("Helvetica", 14, "bold"))
checkboxes_section_label.pack(pady=10)

# Checkboxes to update boolean variables
check_var1 = tk.BooleanVar()
check1 = ttk.Checkbutton(root, text="Option 1", variable=check_var1, command=update_check1, bootstyle="info")
check1.pack(pady=5)

check_var2 = tk.BooleanVar()
check2 = ttk.Checkbutton(root, text="Option 2", variable=check_var2, command=update_check2, bootstyle="info")
check2.pack(pady=5)

# Section Title: Dropdown Menus
dropdown_section_label = ttk.Label(root, text="Dropdown Menus", font=("Helvetica", 14, "bold"))
dropdown_section_label.pack(pady=10)

# Label for Trading Asset
asset_label = ttk.Label(root, text="Trading Asset", font=("Helvetica", 12))
asset_label.pack(pady=5)

# Dropdown for ASSETS
assets_var = tk.StringVar(value=ASSETS[0])
assets_dropdown = ttk.Combobox(root, textvariable=assets_var, values=ASSETS, state="readonly", bootstyle="primary")
assets_dropdown.pack(pady=5)
assets_dropdown.bind("<Button-1>", lambda event: assets_dropdown.event_generate('<Down>'))

# Label for Candle History
candle_label = ttk.Label(root, text="Candle History", font=("Helvetica", 12))
candle_label.pack(pady=5)

# Dropdown for time measurements in seconds
time_var = tk.StringVar(value="17")
time_dropdown = ttk.Combobox(root, textvariable=time_var, values=[17, 30, 60, 120, 240], state="readonly", bootstyle="primary")
time_dropdown.pack(pady=5)
time_dropdown.bind("<Button-1>", lambda event: time_dropdown.event_generate('<Down>'))

# Label for Trading Strategy
strategy_label = ttk.Label(root, text="Trading Strategy", font=("Helvetica", 12))
strategy_label.pack(pady=5)

# Dropdown for Trading Strategy
strategy_var = tk.StringVar(value="10%")
strategy_dropdown = ttk.Combobox(root, textvariable=strategy_var, values=["10%", "Static Bet", "Smart Bet"], state="readonly", bootstyle="primary")
strategy_dropdown.pack(pady=5)
strategy_dropdown.bind("<Button-1>", lambda event: strategy_dropdown.event_generate('<Down>'))
strategy_dropdown.bind("<<ComboboxSelected>>", update_strategy)

# Entry for Static Bet amount
bet_amount_var = tk.StringVar(value="1")
bet_amount_entry = ttk.Entry(root, textvariable=bet_amount_var, bootstyle="primary")
bet_amount_entry.pack(pady=5)
bet_amount_entry.config(state="disabled")

# Section Title: Sliders
slider_section_label = ttk.Label(root, text="Slider Section", font=("Helvetica", 14, "bold"))
slider_section_label.pack(pady=10)

# RangedSlider widget for Trading Slider
ranged_slider = RangedSlider(root, from_=0.6, to=1.0, value=0.6, label_text="Trading Slider")

# RangedSlider for Update Delay
update_delay_label = ttk.Label(root, text="Update Delay (s)", font=("Helvetica", 12))
update_delay_label.pack(pady=5)
update_delay = RangedSlider(root, from_=0.5, to=60, value=0.5, label_text="Update Delay (s)")

# Bind the close window event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the application and control the while loop
while running:
    root.update_idletasks()
    root.update()
    # Your loop code goes here

print("Window closed, loop stopped")
