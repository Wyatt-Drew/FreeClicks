import sys
import os
# Add the parent directory to the PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
import time
import pyautogui
from globals import global_state
import threading
from tkinter import filedialog
from PIL import Image, ImageTk
from simple_autoclicker_event_handlers import toggle_to_macro_ui, start_countdown, stop_autoclicker
from advanced_autoclicker_event_handlers import toggle_to_simple_autoclicker, update_loop_state, delete_selected_event, start_recording, stop_recording, play_macro, pause_macro, stop_macro, clear_macro, save_macro, save_as, load_macro
from ui_helpers import setup_ui

from timer import Timer
import os
import sys
import unittest
import tkinter as tk

class TestToggleToMacroUI(unittest.TestCase):
    def setUp(self):
        # Initialize the Tkinter root element
        root = tk.Tk()
        global_state.initialize_tkinter_variables(root)
        root.title("FreeClicks")
        setup_ui()
        toggle_to_macro_ui()
        global_state.root.update() 
        # Ensure the setup is correct (simple = not visible, macro = visible)
        self.assertFalse(global_state.simple_ui_frame.winfo_ismapped())
        self.assertTrue(global_state.advanced_ui_frame.winfo_ismapped())

    def find_button_by_text(self, container, text):
        """
        Recursively search for a button with the given text in the specified container and its children.

        :param container: The container (tkinter widget) to start the search from.
        :param text: The text of the button to search for.
        :return: The button widget if found, else None.
        """
        for widget in container.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget('text') == text:
                return widget
            else:
                found_widget = self.find_button_by_text(widget, text)
                if found_widget:
                    return found_widget
        return None


    def test_toggle_to_simple_autoclicker(self):
        # Simulate the button click that triggers toggle_to_simple_autoclicker
        toggle_to_simple_autoclicker()
        global_state.root.update() 
        # Assert advanced_ui_frame is not visible
        self.assertFalse(global_state.advanced_ui_frame.winfo_ismapped())
        # Assert simple_ui_frame is visible
        self.assertTrue(global_state.simple_ui_frame.winfo_ismapped())

    def test_start_stop_autoclicker(self):
        # Ensure the auto clicker is not running initially
        global_state.root.update() 
        self.assertFalse(global_state.running)
        #Initialize buttons
        start_button = self.find_button_by_text(global_state.simple_ui_frame, "Start")
        stop_button = self.find_button_by_text(global_state.simple_ui_frame, "Stop")
        self.assertIsNotNone(start_button, "Start button not found")
        self.assertIsNotNone(stop_button, "Stop button not found")
        global_state.root.update() 
        # Simulate click on the start button
        start_button.invoke()

        # Delay to ensure the start process has initiated
        global_state.root.after(6000)

        # Check if the auto clicker started
        global_state.root.update() 
        self.assertTrue(global_state.running)

        # Simulate click on the stop button
        stop_button.invoke()

        # Check if the auto clicker stopped
        global_state.root.update() 
        self.assertFalse(global_state.running)




    def test_toggle_to_macro_ui(self):
        # Simulate the button click that triggers toggle_to_macro_ui
        toggle_to_macro_ui()
        global_state.root.update() 
        # Assert advanced_ui_frame is visible
        self.assertTrue(global_state.advanced_ui_frame.winfo_ismapped())
        # Assert simple_ui_frame is not visible 
        self.assertFalse(global_state.simple_ui_frame.winfo_ismapped())

    def tearDown(self):
        # Destroy the root element to clean up after tests
        global_state.root.destroy()

if __name__ == "__main__":
    unittest.main()
