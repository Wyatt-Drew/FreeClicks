import tkinter as tk
from ui_helpers import setup_ui, load_icon
from globals import global_state

def main():
    root = tk.Tk()
    global_state.initialize_tkinter_variables(root)  # Initialize Tkinter variables
    root.title("FreeClicks")

    logo_photo = load_icon('./assets/logo.png', (100, 100))
    logo_label = tk.Label(root, image=logo_photo)
    logo_label.pack(pady=10)

    setup_ui()

    root.mainloop()

if __name__ == "__main__":
    main()
