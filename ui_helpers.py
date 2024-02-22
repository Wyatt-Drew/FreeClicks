import tkinter as tk
from PIL import Image, ImageTk
from globals import global_state
from simple_autoclicker_event_handlers import toggle_to_simple_autoclicker, start_autoclicker, start_countdown, stop_autoclicker
from advanced_autoclicker_event_handlers import start_recording, stop_recording, play_macro, stop_macro, clear_macro, toggle_to_macro_ui




def load_icon(path, size=(32, 32)):
    """
    Loads an image from the specified path and resizes it to the specified size.
    Keeps a reference to the loaded image to prevent it from being garbage collected.
    """
    try:
        image = Image.open(path)
        image = image.resize(size, Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        if not hasattr(global_state, 'images'):
            global_state.images = {}
        global_state.images[path] = photo
        return photo
    except Exception as e:
        print(f"Error loading image from {path}: {e}")
        return None

def setup_ui():
    setup_advanced_autoclicker_ui()
    setup_simple_autoclicker_ui()
    toggle_to_macro_ui()


def setup_simple_autoclicker_ui():
    global root
    global simple_ui_frame

    # Main frame to hold all elements
    main_frame = tk.Frame(global_state.root)
    main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
    global_state.simple_ui_frame = main_frame

    # Click Speed Entry
    click_speed_frame = tk.Frame(main_frame)
    click_speed_frame.pack(side=tk.TOP, fill='x')
    tk.Label(click_speed_frame, text="Click Speed (ms):").pack(side=tk.LEFT)
    click_speed_var = tk.IntVar(value=1000)
    click_speed_entry = tk.Entry(click_speed_frame, textvariable=click_speed_var)
    click_speed_entry.pack(side=tk.LEFT, padx=5)

    # Stop After Frame for Clicks and Minutes
    stop_after_frame = tk.Frame(main_frame)
    stop_after_frame.pack(side=tk.TOP, fill='x')
    tk.Label(stop_after_frame, text="Stop After:").grid(row=0, column=0, columnspan=2)

    stop_after_clicks_var = tk.IntVar(value=0)
    stop_after_minutes_var = tk.IntVar(value=0)

    # Clicks Entry
    tk.Label(stop_after_frame, text="Clicks:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
    tk.Entry(stop_after_frame, textvariable=stop_after_clicks_var).grid(row=1, column=1, sticky='ew', padx=5, pady=2)

    # Minutes Entry
    tk.Label(stop_after_frame, text="Minutes:").grid(row=2, column=0, sticky='w', padx=5, pady=2)
    tk.Entry(stop_after_frame, textvariable=stop_after_minutes_var).grid(row=2, column=1, sticky='ew', padx=5, pady=2)

    stop_after_frame.columnconfigure(1, weight=1) 

    # Play and Stop buttons
    button_frame = tk.Frame(main_frame)
    button_frame.pack(side=tk.TOP)
    play_button = tk.Button(button_frame, text="Start", command=lambda: start_countdown(click_speed_var.get(), stop_after_clicks_var.get(), stop_after_minutes_var.get(), play_button))
    stop_button = tk.Button(button_frame, text="Stop", command=stop_autoclicker)
    play_button.pack(side=tk.LEFT, pady=2)
    stop_button.pack(side=tk.LEFT, pady=2)

    # Button to switch to macro
    switch_to_macro_button = tk.Button(main_frame, text="Switch to Macro", command=toggle_to_macro_ui)
    switch_to_macro_button.pack(side=tk.TOP, pady=20)




def setup_advanced_autoclicker_ui():
    global advanced_ui_frame
    root = global_state.root
    
    # Main frame to hold all elements
    main_frame = tk.Frame(root)
    main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
    global_state.advanced_ui_frame = main_frame
    

    # Header frame for buttons and logo, occupying minimal necessary vertical space
    header_frame = tk.Frame(main_frame, height=50, bg='grey')
    header_frame.pack(side='top', fill='x', padx=5, pady=5)

    # Frame for the recording options
    record_frame = tk.Frame(header_frame, bg='red')
    record_frame.pack(side='left', padx=5)

    # Frame for the logo and potentially other elements in the center
    center_frame = tk.Frame(header_frame, bg='blue')
    center_frame.pack(side='left', fill='both', expand=True, padx=5)

    # Frame for the playback options
    playback_frame = tk.Frame(header_frame)
    playback_frame.pack(side='left', padx=5)

    # Recording Options Widgets
    record_icon = load_icon('./assets/record.png')
    stop_record_icon = load_icon('./assets/stop-record.png')
    clear_macro_icon = load_icon('./assets/clear.png')
    record_button = tk.Button(record_frame, image=record_icon, command=start_recording)
    stop_record_button = tk.Button(record_frame, image=stop_record_icon, command=stop_recording)
    clear_macro_button = tk.Button(record_frame, image=clear_macro_icon, command=clear_macro)
    record_button.pack(side=tk.LEFT, pady=2)
    stop_record_button.pack(side=tk.LEFT, pady=2)
    clear_macro_button.pack(side=tk.LEFT, pady=2)

    # Playback Options Widgets
    start_icon = load_icon('./assets/start.png')
    pause_icon = load_icon('./assets/pause.png')
    stop_icon = load_icon('./assets/stop.png')
    start_button = tk.Button(playback_frame, image=start_icon, command=start_autoclicker)
    pause_button = tk.Button(playback_frame, image=pause_icon, command=play_macro)
    stop_button = tk.Button(playback_frame, image=stop_icon, command=stop_autoclicker)
    start_button.pack(side=tk.LEFT, pady=2)
    pause_button.pack(side=tk.LEFT, pady=2)
    stop_button.pack(side=tk.LEFT, pady=2)

    # Logo in the center frame
    logo_photo = load_icon('./assets/logo.png', (50, 50))
    logo_label = tk.Label(center_frame, image=logo_photo)
    logo_label.pack(side='top', expand=True)

    # Action area below the header
    action_frame = tk.Frame(main_frame, bg='orange')
    action_frame.pack(side='top', fill='both', expand=True, padx=5, pady=5)
    action_text = tk.Listbox(action_frame)
    action_text.pack(fill='both', expand=True, padx=10, pady=10)
    global_state.events_listbox = action_text

    #Toggle button
    footer_frame = tk.Frame(main_frame, bg = 'purple')
    footer_frame.pack(side='bottom', fill='x', expand=False, padx=5, pady=5) 
    toggle_button = tk.Button(footer_frame, text="Toggle to simple autoclicker", command=toggle_to_simple_autoclicker)
    toggle_button.pack() 

    # Ensure the buttons retain a reference to their images
    for widget in [record_button, stop_record_button, clear_macro_button, start_button, pause_button, stop_button]:
        widget.image = widget['image']