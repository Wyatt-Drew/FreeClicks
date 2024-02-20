import tkinter as tk
from tkinter import ttk  # Enhanced UI elements
from PIL import Image, ImageTk  # Image processing
import threading
import pyautogui
from pynput import mouse, keyboard
import time

# GUI setup
root = tk.Tk()
root.title("FreeClicks")

# Initialize global variables
running = False
recording = False
events = []
mode = 1  # Default to Autoclicker mode
loop_macro = tk.BooleanVar(value=False)  # For looping the macro
playback_running = False
current_event_index = 0


# Load and display logo image
logo_image = Image.open('./assets/logo.png')  # Adjust path as needed
logo_image = logo_image.resize((100, 100), Image.Resampling.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(root, image=logo_photo)
logo_label.pack(pady=10)

# Function to load and resize icons
def load_icon(path, size=(50, 50)):
    image = Image.open(path)
    image = image.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(image)

# Load icons for buttons
start_icon = load_icon('./assets/start.png')
stop_icon = load_icon('./assets/stop.png')
record_icon = load_icon('./assets/record.png')
stop_record_icon = load_icon('./assets/stop-record.png')
playback_icon = load_icon('./assets/start.png') 

# Interval for Autoclicker (in seconds)
interval = tk.DoubleVar(value=0.5)

# Update listbox with events
def update_listbox(event_info):
    events_listbox.insert(tk.END, event_info)
    events_listbox.see(tk.END)

# Autoclicker functionality
def autoclicker():
    global running
    while running:
        pyautogui.click()
        time.sleep(interval.get())

def start_autoclicker():
    global running
    if not running:
        running = True
        threading.Thread(target=autoclicker, daemon=True).start()

def stop_autoclicker():
    global running
    running = False

# Macro recording and playback functionalities
def start_recording():
    global recording, events
    if not recording:
        recording = True
        events = []
        mouse_listener = mouse.Listener(on_click=on_click)
        keyboard_listener = keyboard.Listener(on_press=on_press)
        mouse_listener.start()
        keyboard_listener.start()

def stop_recording():
    global recording
    recording = False

def on_click(x, y, button, pressed):
    if recording:
        events.append(('click', x, y, button, pressed, time.time()))
        update_listbox(f"Click at ({x}, {y})")

def on_press(key):
    if recording:
        try:
            events.append(('press', key.char, time.time()))
            update_listbox(f"Key press: {key.char}")
        except AttributeError:
            events.append(('press', key, time.time()))
            update_listbox(f"Special key press: {key}")

def clear_macro():
    global events
    events.clear()
    events_listbox.delete(0, tk.END)

def play_macro():
    global playback_running, current_event_index
    playback_running = True
    play_events = events[current_event_index:] if current_event_index < len(events) else events

    def playback():
        global current_event_index
        start_time = time.time()
        for index, event in enumerate(play_events, start=current_event_index):
            if not playback_running:
                break
            current_event_index = index
            event_type, *args = event
            if event_type == 'click':
                x, y, button, pressed, event_time = args
                if pressed:
                    pyautogui.click(x=x, y=y)
            elif event_type == 'press':
                key, event_time = args
                if hasattr(key, 'char'):
                    pyautogui.press(key.char)
                else:
                    pyautogui.press(key)
            next_event_time = play_events[index + 1][-1] if index + 1 < len(play_events) else 0
            sleep_time = next_event_time - event_time if next_event_time else 0
            time.sleep(sleep_time)
        if loop_macro.get() and playback_running:
            current_event_index = 0
            playback()

    if play_events:
        threading.Thread(target=playback, daemon=True).start()

def stop_macro():
    global playback_running
    playback_running = False

def pause_macro():
    stop_macro()  # Reusing stop_macro function for simplicity

# Toggle mode functionality
def toggle_mode():
    global mode
    mode = 2 if mode == 1 else 1
    update_ui_for_mode()

def update_ui_for_mode():
    if mode == 1:  # Autoclicker Mode
        for widget in macro_buttons:
            widget.pack_forget()
        for widget in autoclicker_buttons:
            widget.pack(side=tk.LEFT, padx=2)
    else:  # Macro Mode
        for widget in autoclicker_buttons:
            widget.pack_forget()
        for widget in macro_buttons:
            widget.pack(side=tk.LEFT, padx=2)

# Button setup
button_frame = tk.Frame(root)
button_frame.pack(pady=20, padx=20, fill=tk.X)

start_button = tk.Button(button_frame, image=start_icon, command=start_autoclicker)
stop_button = tk.Button(button_frame, image=stop_icon, command=stop_autoclicker)
record_button = tk.Button(button_frame, image=record_icon, command=start_recording)
stop_record_button = tk.Button(button_frame, image=stop_record_icon, command=stop_recording)
playback_button = tk.Button(button_frame, image=playback_icon, command=play_macro)
clear_macro_button = tk.Button(button_frame, text="Clear Macro", command=clear_macro)
stop_macro_button = tk.Button(button_frame, text="Stop Macro", command=stop_macro)
pause_macro_button = tk.Button(button_frame, text="Pause Macro", command=pause_macro)
loop_macro_checkbox = tk.Checkbutton(button_frame, text="Loop Macro", var=loop_macro)

autoclicker_buttons = [start_button, stop_button]
macro_buttons = [record_button, stop_record_button, playback_button, clear_macro_button, stop_macro_button, pause_macro_button, loop_macro_checkbox]

mode_toggle_button = tk.Button(root, text="Toggle Mode", command=toggle_mode)
mode_toggle_button.pack(pady=10)

# Event list display
events_frame = tk.Frame(root)
events_frame.pack(pady=10)
events_listbox = tk.Listbox(events_frame, width=50, height=10)
events_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
events_scroll = tk.Scrollbar(events_frame, orient="vertical", command=events_listbox.yview)
events_scroll.pack(side=tk.RIGHT, fill="y")
events_listbox.config(yscrollcommand=events_scroll.set)

# Initial UI setup
update_ui_for_mode()

root.mainloop()
