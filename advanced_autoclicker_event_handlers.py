from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
import time
import pyautogui
from globals import global_state
import threading
import tkinter as tk
from tkinter import filedialog
import pickle

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
    global_state.recording = True
    global_state.start_time = time.time()
    print(f"Recording started at {global_state.start_time}")
    global_state.mouse_listener = MouseListener(on_click=on_click)
    global_state.mouse_listener.start()

    global_state.keyboard_listener = KeyboardListener(on_press=on_press, on_release=on_release)
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
        action = 'mousedown' if pressed else 'mouseup'
        time_delta = time.time() - global_state.start_time
        global_state.start_time = time.time()
        # Convert the button to a string format compatible with pyautogui
        button_str = str(button).split('.')[-1].lower()
        event = (action, x, y, button_str, time_delta)
        global_state.events.append(event)
        refresh_listbox()

def on_press(key):
    try:
        key_char = key.char
    except AttributeError:
        key_char = str(key)
    if global_state.recording:
        time_delta = time.time() - global_state.start_time  
        global_state.start_time = time.time()
        event = ('press', key_char, time_delta)
        global_state.events.append(event)
        refresh_listbox()

def on_release(key):
    try:
        key_char = key.char
    except AttributeError:
        key_char = str(key)
    if global_state.recording:
        time_delta = time.time() - global_state.start_time  
        global_state.start_time = time.time()
        event = ('release', key_char, time_delta)
        global_state.events.append(event)
        refresh_listbox()

        
def convert_to_readable_text(event, event_number):
    event_type = event[0]
    timestamp = event[-1]
    readable_time = f"{timestamp * 1000:.0f} ms"
    if event_type in ['mousedown', 'mouseup']:
        # Handle mouse down and up events
        x, y, button, pressed = event[1:5]
        x, y = round(x), round(y)
        action = "down" if event_type == 'mousedown' else "up"
        button_name = str(button).split('.')[-1]  # Extract button name
        button_text = {
            'left': 'Left',
            'right': 'Right',
            'middle': 'Middle',
        }.get(button_name, 'Unknown') + ' button'
        return f"{event_number} | ({x}, {y}) | {readable_time} | {button_text} {action}"
    elif event_type in ['press', 'release']:
        # Handle key press and release events
        key_char = event[1]
        action = "pressed" if event_type == 'press' else "released"
        return f"{event_number} | Key {action}: {key_char} | {readable_time}"
    else:
        return f"{event_number} | Unknown Event | {readable_time}"




def refresh_listbox():
    if global_state.events_listbox:
        #clear
        global_state.events_listbox.delete(0, tk.END)
        # Insert each event into the listbox
        event_number = 1
        for event in global_state.events:
            global_state.events_listbox.insert(tk.END, convert_to_readable_text(event, event_number))
            event_number+=1

def play_macro(start_button):
    def macro():
        global_state.progress_frame.pack(side='bottom', fill='x', expand=False, padx=5, pady=5)
        start_button.config(relief="sunken")
        start_button.config(state="disabled")
        if global_state.events:
            global_state.playback_running = True


            while True: #Do while loop for loop_state variable
                for event in global_state.events:
                    start_time = time.time()
                    if not global_state.playback_running:
                        break
                    event_type, *args, timestamp = event
                    while time.time() < start_time + (timestamp - global_state.events[0][-1]):
                        while global_state.paused and global_state.playback_running:
                            time.sleep(0.01)
                        if not global_state.playback_running:  # Check again in case stop was pressed during wait
                            break
                        time.sleep(0.01)  # Sleep briefly to wait for the right time to trigger the event
                    if not global_state.playback_running:  # Exit if playback has been stopped
                        break
                    if event_type == 'mousedown':
                        pyautogui.mouseDown(x=args[0], y=args[1], button=args[2])
                    elif event_type == 'mouseup':
                        pyautogui.mouseUp(x=args[0], y=args[1], button=args[2])
                    elif event_type == 'press':
                        pyautogui.press(args[0])
                if not global_state.loop_state or not global_state.playback_running: #leave do while loop if loop_state = false
                    break
            global_state.playback_running = False
        start_button.config(state="normal")
        start_button.config(relief="raised")
        global_state.progress_frame.pack_forget()

    threading.Thread(target=macro).start() 

def stop_macro(start_button, pause_button):
    print("stopped")
    global_state.progress_frame.pack_forget()
    global_state.playback_running = False
    start_button.config(state="normal")
    global_state.paused = False
    pause_button.config(relief="raised")

def pause_macro(pause_button):
    # Toggle the paused state
    global_state.paused = not global_state.paused
    
    if global_state.paused:
        # Change the button's appearance to look "pressed"
        pause_button.config(relief="sunken")
    else:
        # Revert the button's appearance to look "normal"
        pause_button.config(relief="raised")

def save_macro(filename='default_macro.fclicks'):
    with open(filename, 'w') as file:
        for event in global_state.events:
            line = f"{event[0]},{event[1]},{event[2]},{event[3]},{event[4]}\n"  # Format based on your event structure
            file.write(line)
    print(f"Macro saved to {filename}")

def save_as():
    filename = filedialog.asksaveasfilename(
        defaultextension=".fclicks",
        filetypes=[("FClicks files", "*.fclicks"), ("All files", "*.*")],
        initialfile='default_macro.fclicks'  # Suggests a default filename in the dialog
    )
    if filename:
        save_macro(filename)
        print(f"Macro saved as {filename}")

def load_macro():
    filename = filedialog.askopenfilename(filetypes=[("FClicks files", "*.fclicks"), ("All files", "*.*")])
    if filename:
        with open(filename, 'r') as file:
            lines = file.readlines()
            global_state.events = []
            for line in lines:
                parts = line.strip().split(',')  # Adjust as per your event structure
                event = (parts[0], float(parts[1]), float(parts[2]), parts[3], float(parts[4]))
                global_state.events.append(event)
        print(f"Macro loaded from {filename}")
        refresh_listbox()



def delete_selected_event():
    selection = global_state.events_listbox.curselection()
    if selection:
        index = selection[0]
        del global_state.events[index]  # Delete from data
        global_state.events_listbox.delete(index)  # Delete from listbox view
        print(f"Event {index + 1} deleted")

def update_loop_state(loop_var):
    # Update the global loop_state based on the checkbox's BooleanVar value
    global_state.loop_state = loop_var.get()