# FreeClicks
FreeClicks is an open-source, free autoclicker tool designed to automate clicking tasks. Developed in Python, it offers both simplicity for basic autoclicking needs and advanced features for creating custom click macros. With FreeClicks, users can easily set up auto-clicking with customizable intervals, durations, and even complex sequences of mouse and keyboard actions.

# Features
Simple Autoclicker: Just set the click speed and let it run.
Macro Recording: Record sequences of mouse and keyboard actions to be replayed later.
Customizable: Adjust click speeds, set the number of clicks, or specify a duration for the autoclicker to run.
Cross-platform: Works on any platform that supports Python and tkinter.


# Creating a .exe file
To create an executable file for Windows, you can use PyInstaller. Run the following command in the project directory:

pyinstaller --onefile --windowed --icon=.\assets\icon.png --add-data ".\assets;assets" main.py

# Usage
Upon launching FreeClicks, you will be greeted with a macro for recording and playback.  You can also switch to a simple auto clicker.

# Simple Autoclicker Mode
Set your click speed and duration.
Press the "Start" button to begin auto-clicking.
Press "Stop" to halt the autoclicker.
Macro Recording and Playback
Switch to the macro UI.
Press "Record" to start capturing mouse and keyboard actions.
Press "Stop Recording" once done.
Use "Play" to replay the recorded macro.

# Contributing
Contributions to FreeClicks are welcome! Whether it's reporting bugs, suggesting enhancements, or adding new features, your input is valuable. Please refer to CONTRIBUTING.md for guidelines on how to contribute to this project.

# License
FreeClicks is released under the MIT License. See the LICENSE file for more details.