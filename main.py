import tkinter as tk
from ui_helpers import setup_ui, toggle_to_macro_ui
from globals import global_state
import sys
import os

# Check if the application is running as a PyInstaller bundle
if getattr(sys, 'frozen', False):
    # If so, use the `_MEIPASS` directory, where PyInstaller unpacks the bundled files
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the assets directory
assets_path = os.path.join(application_path, 'assets', 'logo_small.png')


def main():
    root = tk.Tk()
    global_state.initialize_tkinter_variables(root)
    root.title("FreeClicks")
    # Use the constructed assets_path instead of the hardcoded path
    icon_image = tk.PhotoImage(file=assets_path)
    root.iconphoto(True, icon_image)
    setup_ui()
    toggle_to_macro_ui()

    root.mainloop()

if __name__ == "__main__":
    main()
