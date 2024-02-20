import tkinter as tk
from auto_clicker_controller import AutoClickerController

if __name__ == "__main__":
    root = tk.Tk()
    root.title("FreeClicks")
    controller = AutoClickerController(root)
    root.mainloop()
