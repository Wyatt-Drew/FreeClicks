import tkinter as tk
from PIL import Image, ImageTk

class AutoClickerBase:
    def __init__(self, root):
        self.root = root
        self.running = False
        self.setup_gui()

    def setup_gui(self):
        # Setup common GUI components here
        pass

    def start_autoclicker(self):
        self.running = True
        # Start autoclicker logic
        pass

    def stop_autoclicker(self):
        self.running = False
        # Stop autoclicker logic
        pass
