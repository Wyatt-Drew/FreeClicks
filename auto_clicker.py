import threading
import time
import pyautogui
from globals import global_state

def autoclicker():
    while global_state.running:
        pyautogui.click()
        time.sleep(global_state.interval.get())

def start_autoclicker():
    global_state.running = True
    threading.Thread(target=autoclicker, daemon=True).start()

def stop_autoclicker():
    global_state.running = False
def start_autoclicker():
    # Implementation
    pass

def stop_autoclicker():
    # Implementation
    pass