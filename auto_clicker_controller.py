import tkinter as tk
from simple_auto_clicker import SimpleAutoClicker
from advanced_auto_clicker import AdvancedAutoClicker

class AutoClickerController:
    def __init__(self, root):
        self.mode = 1  # Default mode
        self.root = root
        self.autoclicker = SimpleAutoClicker(root)
        self.setup_mode_toggle()

    def setup_mode_toggle(self):
        self.mode_toggle_button = tk.Button(self.root, text="Toggle Mode", command=self.toggle_mode)
        self.mode_toggle_button.pack(pady=10)

    def toggle_mode(self):
        if self.mode == 1:
            self.autoclicker = AdvancedAutoClicker(self.root)
            self.mode = 2
        else:
            self.autoclicker = SimpleAutoClicker(self.root)
            self.mode = 1
        # Update the GUI or perform additional setup as needed
