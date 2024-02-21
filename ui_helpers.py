import tkinter as tk
from PIL import Image, ImageTk
from globals import global_state
from event_handlers import start_recording, stop_recording, play_macro, stop_macro, clear_macro
from auto_clicker import start_autoclicker, stop_autoclicker

def load_icon(path, size=(50, 50)):
    image = Image.open(path)
    image = image.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(image)

def setup_ui():
    root = global_state.root
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20, padx=20, fill=tk.X)

    start_icon = load_icon('./assets/start.png')
    stop_icon = load_icon('./assets/stop.png')
    record_icon = load_icon('./assets/record.png')
    stop_record_icon = load_icon('./assets/stop-record.png')
    playback_icon = load_icon('./assets/start.png')  

    start_button = tk.Button(button_frame, image=start_icon, command=start_autoclicker)
    stop_button = tk.Button(button_frame, image=stop_icon, command=stop_autoclicker)
    record_button = tk.Button(button_frame, image=record_icon, command=start_recording)
    stop_record_button = tk.Button(button_frame, image=stop_record_icon, command=stop_recording)
    playback_button = tk.Button(button_frame, image=playback_icon, command=play_macro)
    clear_macro_button = tk.Button(button_frame, text="Clear Macro", command=clear_macro)
    stop_macro_button = tk.Button(button_frame, text="Stop Macro", command=stop_macro)
    loop_macro_checkbox = tk.Checkbutton(button_frame, text="Loop Macro", var=global_state.loop_macro)

    start_button.pack(side=tk.LEFT)
    stop_button.pack(side=tk.LEFT)
    record_button.pack(side=tk.LEFT)
    stop_record_button.pack(side=tk.LEFT)
    playback_button.pack(side=tk.LEFT)
    clear_macro_button.pack(side=tk.LEFT)
    stop_macro_button.pack(side=tk.LEFT)
    loop_macro_checkbox.pack(side=tk.LEFT)

    events_frame = tk.Frame(root)
    events_frame.pack(pady=10)
    global_state.events_listbox = tk.Listbox(events_frame, width=50, height=10)
    global_state.events_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    events_scroll = tk.Scrollbar(events_frame, orient="vertical", command=global_state.events_listbox.yview)
    events_scroll.pack(side=tk.RIGHT, fill="y")
    global_state.events_listbox.config(yscrollcommand=events_scroll.set)
