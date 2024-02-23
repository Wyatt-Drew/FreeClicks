from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
import time
import pyautogui
from globals import global_state
import threading


def toggle_to_simple_autoclicker():
    global_state.advanced_ui_frame.pack_forget()
    global_state.simple_ui_frame.pack(side='top', fill='both', expand=True, padx=5, pady=5)
    global_state.root.minsize(200, 200)
    global_state.root.maxsize(200, 200)
    global_state.root.geometry("200x200")


def start_autoclicker(click_speed, stop_after_clicks, stop_after_minutes, start_button):

    def autoclicker():
        click_count = 0
        start_time = time.time()
        while global_state.running:
            pyautogui.click()
            time.sleep(click_speed/1000)
            click_count += 1
            if stop_after_clicks and click_count >= stop_after_clicks:
                break
            if stop_after_minutes and (time.time() - start_time) / 60 >= stop_after_minutes:
                break
        global_state.running = False
        start_button.config(state="normal")
    threading.Thread(target=autoclicker).start()
    

def start_countdown(click_speed, stop_after_clicks, stop_after_minutes, start_button, count=3):
    if count > 0:
        start_button.config(text=f"Start {count}")
        start_button.config(state="disabled") 
        global_state.root.after(1000, start_countdown, click_speed, stop_after_clicks, stop_after_minutes, start_button, count-1)
    else:
        start_button.config(text="Start")
        global_state.running = True
        start_autoclicker(click_speed, stop_after_clicks, stop_after_minutes, start_button)

def stop_autoclicker():
    global_state.running = False