import tkinter as tk
from PIL import Image, ImageTk
from globals import global_state
from simple_autoclicker_event_handlers import toggle_to_simple_autoclicker, start_countdown, stop_autoclicker
from advanced_autoclicker_event_handlers import delete_selected_event, start_recording, stop_recording, play_macro, pause_macro, stop_macro, clear_macro, toggle_to_macro_ui, save_macro, save_as, load_macro
import os
import sys
if getattr(sys, 'frozen', False):
    # If so, use the `_MEIPASS` directory, where PyInstaller unpacks the bundled files
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
# Construct the full path to the image


def load_icon(relative_path, size=(32, 32)):
    """
    Loads an image from the specified path and resizes it to the specified size.
    Keeps a reference to the loaded image to prevent it from being garbage collected.
    """
    # Check if the application is running as a PyInstaller bundle
    full_path = os.path.join(application_path, relative_path)
    try:
        image = Image.open(full_path)
        image = image.resize(size, Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        if not hasattr(global_state, 'images'):
            global_state.images = {}
        global_state.images[full_path] = photo  # Use full_path as the key
        return photo
    except Exception as e:
        print(f"Error loading image from {full_path}: {e}")
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
    
    # Create a menubar
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    # Create the Options menu
    options_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Options", menu=options_menu)

    # Add items to the Options menu
    options_menu.add_command(label="Save Macro", command=save_macro)
    options_menu.add_command(label="Save As", command=save_as)
    options_menu.add_command(label="Load Macro", command=load_macro)

    # Header frame for buttons and logo, occupying minimal necessary vertical space
    header_frame = tk.Frame(main_frame)
    header_frame.pack(side='top', fill='x', padx=5)

    # Frame for the recording options
    record_frame = tk.Frame(header_frame)
    record_frame.pack(side='left', padx=5)

    # Frame for the logo and potentially other elements in the center
    center_frame = tk.Frame(header_frame)
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
    record_button.pack(side=tk.LEFT)
    stop_record_button.pack(side=tk.LEFT)
    clear_macro_button.pack(side=tk.LEFT)

    # Playback Options Widgets
    start_icon = load_icon('./assets/start.png')
    pause_icon = load_icon('./assets/pause.png')
    stop_icon = load_icon('./assets/stop.png')
    start_button = tk.Button(playback_frame, image=start_icon, command=lambda:play_macro(start_button))
    pause_button = tk.Button(playback_frame, image=pause_icon, command=lambda:pause_macro(pause_button))
    stop_button = tk.Button(playback_frame, image=stop_icon, command=lambda:stop_macro(start_button))
    start_button.pack(side=tk.LEFT)
    pause_button.pack(side=tk.LEFT)
    stop_button.pack(side=tk.LEFT)

    # Logo in the center frame
    logo_photo = load_icon('./assets/logo.png', (50, 50))
    logo_label = tk.Label(center_frame, image=logo_photo)
    logo_label.pack(side='top', expand=True)

    # Action area below the header
    action_frame = tk.Frame(main_frame)
    action_frame.pack(side='top', fill='both', expand=True, padx=5, pady=5)
    action_text = tk.Listbox(action_frame)
    action_text.pack(fill='both', expand=True, padx=10, pady=10)
    global_state.events_listbox = action_text

    #Toggle button
    footer_frame = tk.Frame(main_frame)
    footer_frame.pack(side='bottom', fill='x', expand=False, padx=5, pady=5) 
    toggle_button = tk.Button(footer_frame, text="Toggle to Simple Autoclicker", command=toggle_to_simple_autoclicker)
    toggle_button.pack() 

    # Ensure the buttons retain a reference to their images
    for widget in [record_button, stop_record_button, clear_macro_button, start_button, pause_button, stop_button]:
        widget.image = widget['image']

    # Create a context menu for the listbox
    context_menu = tk.Menu(global_state.root, tearoff=0)
    context_menu.add_command(label="Delete", command=delete_selected_event)
    # Function to display the context menu on right-click
    def on_right_click(event):
        try:
            global_state.events_listbox.selection_clear(0, tk.END)
            global_state.events_listbox.selection_set(global_state.events_listbox.nearest(event.y))
            global_state.events_listbox.activate(global_state.events_listbox.nearest(event.y))
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
    global_state.events_listbox.bind("<Button-3>", on_right_click)
    global_state.root.bind('<Delete>', lambda event: delete_selected_event())