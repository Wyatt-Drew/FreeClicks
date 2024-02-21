import tkinter as tk

class GlobalState:
    def __init__(self):
        self.root = None
        self.loop_macro = None
        self.interval = None
        self.events_listbox = None
        self.events = []
        self.recording = False
        self.playback_running = False
        self.current_event_index = 0

    def initialize_tkinter_variables(self, root):
        self.root = root
        self.loop_macro = tk.BooleanVar(self.root, value=False)
        self.interval = tk.DoubleVar(self.root, value=0.5)
        # Any additional Tkinter variable initialization should go here

# Initialize the global state; Tkinter variables will be initialized later.
global_state = GlobalState()
