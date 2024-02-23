from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
import time
import pyautogui
from globals import global_state
import threading
import tkinter as tk

def toggle_to_macro_ui():
    global_state.simple_ui_frame.pack_forget()
    global_state.advanced_ui_frame.pack(side='top', fill='both', expand=True, padx=5, pady=5)
    global_state.root.minsize(500, 550)
    global_state.root.geometry("500x550")

def clear_macro():
    global_state.events.clear()
    if global_state.events_listbox:
        global_state.events_listbox.delete(0, 'end')

def start_recording():
    # Logic to start recording events
    global_state.recording = True
     # Start Mouse Listener
    global_state.mouse_listener = MouseListener(on_click=on_click)
    global_state.mouse_listener.start()
    
    # Start Keyboard Listener
    global_state.keyboard_listener = KeyboardListener(on_press=on_press)
    global_state.keyboard_listener.start()
    print("Recording started...")

def stop_recording():
    # Stop recording events
    global_state.recording = False
    print("Recording stopped.")
    
    # Stop Listeners
    if hasattr(global_state, 'mouse_listener'):
        global_state.mouse_listener.stop()
    if hasattr(global_state, 'keyboard_listener'):
        global_state.keyboard_listener.stop()

def on_click(x, y, button, pressed):
    if global_state.recording:
        event = ('click', x, y, button, pressed, time.time())
        global_state.events.append(event)
        update_listbox(f"Click at ({x}, {y})")

def on_press(key):
    try:
        key_char = key.char
    except AttributeError:
        key_char = str(key)
    if global_state.recording:
        event = ('press', key_char, time.time())
        global_state.events.append(event)
        update_listbox(f"Key press: {key_char}")

def update_listbox(text):
    if global_state.events_listbox:
        global_state.events_listbox.insert(tk.END, text)



def play_macro(start_button):
    def macro():

        start_button.config(relief="sunken")
        start_button.config(state="disabled")
        if global_state.events:
            global_state.playback_running = True
            start_time = time.time()
            for event in global_state.events:
                if not global_state.playback_running:
                    break
                event_type, *args, timestamp = event
                while time.time() < start_time + (timestamp - global_state.events[0][-1]):
                    while global_state.paused:
                        time.sleep(0.01)
                    if not global_state.playback_running:  # Check again in case stop was pressed during wait
                        break
                    time.sleep(0.01)  # Sleep briefly to wait for the right time to trigger the event
                if not global_state.playback_running:  # Exit if playback has been stopped
                    break
                if event_type == 'click':
                    pyautogui.click(x=args[0], y=args[1])
                elif event_type == 'press':
                    pyautogui.press(args[0])
            global_state.playback_running = False
        start_button.config(state="normal")
        start_button.config(relief="raised")

    threading.Thread(target=macro).start() 

def stop_macro(start_button):
    print("stopped")
    global_state.playback_running = False
    start_button.config(state="normal")

def pause_macro(pause_button):
    # Toggle the paused state
    global_state.paused = not global_state.paused
    
    if global_state.paused:
        # Change the button's appearance to look "pressed"
        pause_button.config(relief="sunken")
    else:
        # Revert the button's appearance to look "normal"
        pause_button.config(relief="raised")

def save_macro():
    print("Save Macro clicked")

def save_as():
    print("Save As clicked")

def load_macro():
    print("Load Macro clicked")



