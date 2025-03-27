# /ui/state_manager.py

import tkinter as tk
from ui.screens.welcome_screen import WelcomeScreen
from ui.screens.planetgen_screen import PlanetGenScreen

class UIStateManager:
    """
    Manages transitions between different UI screens.
    Holds a reference to the root window and handles showing/hiding frames.
    """

    def __init__(self, root: tk.Tk):
        """
        Initializes the UIStateManager with the root Tkinter window.

        Args:
            root (tk.Tk): The main application window.
        """
        self.root = root
        self.screens = {}
        self.active_screen = None

        self._register_screens()
        self.switch_screen("welcome")

    def _register_screens(self):
        """
        Initializes and registers all screen objects.
        Each screen is stored in a dictionary for easy access.
        """
        self.screens["welcome"] = WelcomeScreen(self.root, self)
        self.screens["planetgen"] = PlanetGenScreen(self.root, self)

    def switch_screen(self, screen_name: str):
        """
        Switches to the specified screen by name.
        Hides the current screen and displays the new one.

        Args:
            screen_name (str): The key name of the screen to display.
        """
        if self.active_screen:
            self.active_screen.pack_forget()

        self.active_screen = self.screens.get(screen_name)

        if self.active_screen:
            self.active_screen.pack(fill="both", expand=True)
        else:
            raise ValueError(f"Screen '{screen_name}' not found in state manager.")
