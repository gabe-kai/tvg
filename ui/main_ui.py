# /ui/main_ui.py

import tkinter as tk
from ui.state_manager import UIStateManager

def launch_ui():
    """
    Launches the main UI application window.
    Initializes the Tkinter root window and starts the event loop.
    """
    root = tk.Tk()
    root.title("TVG Planet Generator")
    root.geometry("1024x768")  # Can be adjusted as needed

    # Initialize and launch the UI state manager
    state_manager = UIStateManager(root)

    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    launch_ui()
