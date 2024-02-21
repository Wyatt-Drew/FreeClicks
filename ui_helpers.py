import tkinter as tk
from PIL import Image, ImageTk
from globals import global_state
# Make sure you have the necessary imports for your event handling functions
from event_handlers import start_recording, stop_recording, play_macro, stop_macro, clear_macro
from auto_clicker import start_autoclicker, stop_autoclicker


def load_icon(path, size=(50, 50)):
    """
    Loads an image from the specified path and resizes it to the specified size.
    Keeps a reference to the loaded image to prevent it from being garbage collected.

    :param path: The file path to the image.
    :param size: A tuple of (width, height) to resize the image.
    :return: A PhotoImage object of the loaded and resized image.
    """
    try:
        # Open the image file
        image = Image.open(path)
        # Resize the image
        image = image.resize(size, Image.Resampling.LANCZOS)
        # Convert the image to a PhotoImage
        photo = ImageTk.PhotoImage(image)
        # Store a reference to the image to prevent garbage collection
        if not hasattr(global_state, 'images'):
            global_state.images = {}
        global_state.images[path] = photo
        return photo
    except Exception as e:
        print(f"Error loading image from {path}: {e}")
        return None

def setup_ui():
    """
    Sets up the user interface for the application.
    """
    # Assuming global_state.root is your Tkinter root window
    root = global_state.root

    # Create a frame for the buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20, padx=20, fill=tk.X)

    # Load icons and create buttons
    start_icon = load_icon('./assets/start.png')
    stop_icon = load_icon('./assets/stop.png')
    record_icon = load_icon('./assets/record.png')
    stop_record_icon = load_icon('./assets/stop-record.png')
    playback_icon = load_icon('./assets/playback.png')
    clear_macro_icon = load_icon('./assets/clear.png')  # Assuming you have a clear icon

    start_button = tk.Button(button_frame, image=start_icon, command=start_autoclicker)
    stop_button = tk.Button(button_frame, image=stop_icon, command=stop_autoclicker)
    record_button = tk.Button(button_frame, image=record_icon, command=start_recording)
    stop_record_button = tk.Button(button_frame, image=stop_record_icon, command=stop_recording)
    playback_button = tk.Button(button_frame, image=playback_icon, command=play_macro)
    clear_macro_button = tk.Button(button_frame, image=clear_macro_icon, command=clear_macro)

    # Pack the buttons into the button frame
    start_button.pack(side=tk.LEFT)
    stop_button.pack(side=tk.LEFT)
    record_button.pack(side=tk.LEFT)
    stop_record_button.pack(side=tk.LEFT)
    playback_button.pack(side=tk.LEFT)
    clear_macro_button.pack(side=tk.LEFT)

    # Ensure the buttons retain a reference to their images
    for widget in button_frame.winfo_children():
        widget.image = widget['image']

    # Set up other UI components as needed...
