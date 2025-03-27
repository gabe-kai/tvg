# /ui/screens/welcome_screen.py

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.state_manager import UIStateManager

class WelcomeScreen(tk.Frame):
    """
    The initial welcome screen for the application.
    Presents options to start a new game, load a game, or open settings.
    Currently, only the "New Game" button is wired to proceed to the planet generation screen.
    """

    def __init__(self, master, state_manager: "UIStateManager"):
        """
        Initializes the WelcomeScreen.

        Args:
            master (tk.Tk or tk.Frame): The parent widget.
            state_manager (UIStateManager): Object managing screen transitions.
        """
        super().__init__(master)
        self.state_manager = state_manager
        self.configure(padx=50, pady=50)

        self._build_widgets()

    def _build_widgets(self):
        """
        Builds and places the UI widgets on the screen.
        """
        title = ttk.Label(self, text="Welcome to TVG Planet Generator", font=("Arial", 20, "bold"))
        title.pack(pady=(0, 20))

        new_game_btn = ttk.Button(self, text="New Game", command=self._start_new_game)
        new_game_btn.pack(fill="x", pady=5)

        load_game_btn = ttk.Button(self, text="Load Game (Coming Soon)", state="disabled")
        load_game_btn.pack(fill="x", pady=5)

        settings_btn = ttk.Button(self, text="Settings (Coming Soon)", state="disabled")
        settings_btn.pack(fill="x", pady=5)

    def _start_new_game(self):
        """
        Called when the "New Game" button is pressed.
        Switches to the planet generation screen using the state manager.
        """
        self.state_manager.switch_screen("planetgen")
