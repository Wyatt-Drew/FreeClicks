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
    root = global_state.root
    root.minsize(500, 500)

    # Main frame to hold all elements
    main_frame = tk.Frame(root)
    main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)



    # Create a frame for the buttons
    record_frame = tk.Frame(main_frame)
    record_frame.grid(row=1, column=0, sticky="ew")
    # Create a frame for the buttons
    playback_frame = tk.Frame(main_frame)
    playback_frame.grid(row=1, column=3, sticky="ew")

    #Labels
    recording_label = tk.Label(record_frame, text="Recording")
    playback_label = tk.Label(playback_frame, text="Playback")
    recording_label.grid(row=0, column=0, sticky="ew")
    playback_label.grid(row=0, column=0, sticky="ew")

    # Load icons and create buttons
    record_icon = load_icon('./assets/record.png')
    stop_record_icon = load_icon('./assets/stop-record.png')
    clear_macro_icon = load_icon('./assets/clear.png') 

    start_icon = load_icon('./assets/start.png')
    pause_icon = load_icon('./assets/pause.png')
    stop_icon = load_icon('./assets/stop.png')
    
    #Recording Options
    record_button = tk.Button(record_frame, image=record_icon, command=start_recording)
    stop_record_button = tk.Button(record_frame, image=stop_record_icon, command=stop_recording)
    clear_macro_button = tk.Button(record_frame, image=clear_macro_icon, command=clear_macro)
    #Playback options
    start_button = tk.Button(playback_frame, image=start_icon, command=start_autoclicker)
    pause_button = tk.Button(playback_frame, image=pause_icon, command=play_macro)
    stop_button = tk.Button(playback_frame, image=stop_icon, command=stop_autoclicker)
    
    
    
    # Labels
    recording_label.pack(side=tk.TOP, fill=tk.X)
    playback_label.pack(side=tk.TOP, fill=tk.X)
    # Pack the buttons into the button frame
    # recording options
    record_button.pack(side=tk.LEFT)
    stop_record_button.pack(side=tk.LEFT)
    clear_macro_button.pack(side=tk.LEFT)
    # Logo
    logo_photo = load_icon('./assets/logo.png', (100, 100))
    logo_label = tk.Label(main_frame, image=logo_photo)
    logo_label.place(relx=0.5, y=10, anchor='n')
    #Playback options
    stop_button.pack(side=tk.RIGHT)
    pause_button.pack(side=tk.RIGHT)
    start_button.pack(side=tk.RIGHT)




    # Ensure the buttons retain a reference to their images
    for widget in record_frame.winfo_children():
        widget.image = widget['image']

