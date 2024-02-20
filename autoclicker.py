import tkinter as tk
from time import sleep, time
import threading
import pyautogui
from pynput import mouse, keyboard

# Global variables to manage the autoclicker state and events
running = False
recording = False
events = []

# GUI setup
root = tk.Tk()
root.title("Simple Autoclicker with Record & Playback")

# Load icons for buttons
start_icon = tk.PhotoImage(file='./assets/start.png')
stop_icon = tk.PhotoImage(file='./assets/stop.png')
record_icon = tk.PhotoImage(file='./assets/logo.png')
stop_record_icon = tk.PhotoImage(file='./assets/logo.png')
playback_icon = tk.PhotoImage(file='./assets/logo.png')

interval = tk.DoubleVar(value=2)  # Default click interval in seconds

def update_listbox(event_info):
    """Function to update the GUI with recorded events."""
    events_listbox.insert(tk.END, event_info)
    events_listbox.see(tk.END)

def autoclicker():
    """Function to perform automatic clicking."""
    try:
        while running:
            pyautogui.click()
            sleep(interval.get())
    except Exception as e:
        print(e)

def start_autoclicker():
    """Starts the autoclicker."""
    global running
    running = True
    t = threading.Thread(target=autoclicker)
    t.daemon = True
    t.start()

def stop_autoclicker():
    """Stops the autoclicker."""
    global running
    running = False

def start_recording():
    """Starts recording mouse and keyboard events."""
    global recording, events
    recording = True
    events = []
    mouse_listener = mouse.Listener(on_click=on_click)
    keyboard_listener = keyboard.Listener(on_press=on_press)
    mouse_listener.start()
    keyboard_listener.start()

def stop_recording():
    """Stops recording events."""
    global recording
    recording = False

def on_click(x, y, button, pressed):
    """Handles mouse click events."""
    if recording and pressed:  # Record only press events to simplify
        events.append(('click', x, y, button, pressed, time()))
        update_listbox(f"Click at ({x}, {y})")

def on_press(key):
    """Handles keyboard press events."""
    if key == keyboard.Key.p:  # Check if 'p' key is pressed
        shutdown_application()  # Call the shutdown function
    elif recording:
        try:
            event_info = ('press', key.char, time())
            events.append(event_info)
            update_listbox(f"Key press: {key.char}")
        except AttributeError:
            # Special keys
            event_info = ('press', key, time())
            events.append(event_info)
            update_listbox(f"Special key press: {key}")

def shutdown_application():
    """Shuts down the application safely."""
    stop_autoclicker()  # Stop the autoclicker
    stop_recording()    # Stop recording if it's happening
    root.destroy()      # Close the tkinter window

def playback():
    """Plays back recorded events."""
    if events:
        start_time = events[0][-1]  # Get the timestamp of the first event
        for event in events:
            event_type, *args, timestamp = event
            sleep(timestamp - start_time)  # Wait until this event should occur
            start_time = timestamp
            if event_type == 'click':
                x, y, button, pressed = args
                if pressed:
                    pyautogui.click(x=x, y=y)
            elif event_type == 'press':
                key = args[0]
                if isinstance(key, str):
                    pyautogui.press(key)
                else:
                    print(f"Cannot playback special key: {key}")

# Layout setup for buttons with icons
button_frame = tk.Frame(root)
button_frame.pack(pady=20, padx=20, fill=tk.X)

start_button = tk.Button(button_frame, image=start_icon, command=start_autoclicker)
start_button.pack(side=tk.LEFT, padx=2)

stop_button = tk.Button(button_frame, image=stop_icon, command=stop_autoclicker)
stop_button.pack(side=tk.LEFT, padx=2)

record_button = tk.Button(button_frame, image=record_icon, command=start_recording)
record_button.pack(side=tk.LEFT, padx=2)

stop_record_button = tk.Button(button_frame, image=stop_record_icon, command=stop_recording)
stop_record_button.pack(side=tk.LEFT, padx=2)

playback_button = tk.Button(button_frame, image=playback_icon, command=playback)
playback_button.pack(side=tk.LEFT, padx=2)

# Add a listbox to display recorded events, placed below the button frame
events_frame = tk.Frame(root)
events_frame.pack(pady=10)
events_listbox = tk.Listbox(events_frame, width=50, height=10)
events_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
events_scroll = tk.Scrollbar(events_frame, orient="vertical", command=events_listbox.yview)
events_scroll.pack(side=tk.RIGHT, fill="y")
events_listbox.config(yscrollcommand=events_scroll.set)

root.mainloop()