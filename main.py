import tkinter as tk
from ui_helpers import setup_ui, load_icon, toggle_to_macro_ui
from globals import global_state

def main():
    root = tk.Tk()
    global_state.initialize_tkinter_variables(root)  # Initialize Tkinter variables
    root.title("FreeClicks")
    icon_image = tk.PhotoImage(file='./assets/logo_small.png')
    root.iconphoto(True, icon_image)
    setup_ui()
    toggle_to_macro_ui()

    root.mainloop()

if __name__ == "__main__":
    main()
