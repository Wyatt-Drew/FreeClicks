import tkinter as tk

class GlobalState:
    def __init__(self):
        self.root = None
        self.loop_macro = None
        self.interval = None
        self.events_listbox = None
        self.events = []
        self.recording = False
        self.mouse_listener = None
        self.keyboard_listener = None
        self.playback_running = False
        self.running = False  
        self.paused = False
        self.current_event_index = 0
        self.simple_ui_frame = None
        self.advanced_ui_frame = None
        self.start_time = None

    def initialize_tkinter_variables(self, root):
        self.root = root
        self.loop_macro = tk.BooleanVar(self.root, value=False)
        self.interval = tk.DoubleVar(self.root, value=0.5)

# Initialize the global state;
global_state = GlobalState()
