# /ui/screens/welcome.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QLabel
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import sys
from logger.logger import LoggerFactory
from ui.theme import DARK_THEME

logger = LoggerFactory("welcome_screen").get_logger()


class WelcomeScreen(QWidget):
    """
    The welcome screen of the game. Displays a full background and
    a left-side column with navigation buttons.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(DARK_THEME)  # Apply global dark theme
        self.setup_ui()
        logger.info("WelcomeScreen initialized")

    def setup_ui(self):
        # Create main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # --- Context Panel (Left) ---
        self.left_panel = QWidget()
        self.left_panel.setObjectName("ContextPanel")  # For theme-based styling
        self.left_panel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        button_column = QVBoxLayout(self.left_panel)
        button_column.addStretch(3)  # Push buttons to the bottom

        # Create buttons
        self.new_game_button = QPushButton("New Game")
        self.load_game_button = QPushButton("Load Game")
        self.settings_button = QPushButton("Settings")
        self.about_button = QPushButton("About")
        self.quit_button = QPushButton("Quit to Desktop")

        # Add buttons to column
        for button in [
            self.new_game_button,
            self.load_game_button,
            self.settings_button,
            self.about_button,
            self.quit_button
        ]:
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button_column.addWidget(button)

        # Connect buttons
        self.new_game_button.clicked.connect(self.start_new_game)
        self.quit_button.clicked.connect(self.quit_to_desktop)

        button_column.addStretch(1)  # Spacer after buttons

        # --- Content Panel (Right) ---
        self.main_content = QWidget()
        self.main_content.setObjectName("ContentPanel")  # For theme-based styling
        self.main_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_content.setAttribute(Qt.WA_StyledBackground, True)

        # Add a title label to the top-center
        content_layout = QVBoxLayout(self.main_content)
        content_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        title = QLabel("The Vassal Game")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 32, QFont.Bold))
        title.setStyleSheet("color: white;")
        content_layout.addWidget(title)

        # --- Assemble main layout ---
        main_layout.addWidget(self.left_panel, stretch=1)
        main_layout.addWidget(self.main_content, stretch=3)

    def start_new_game(self):
        """
        Slot: Transition to the Planet Generator screen.
        """
        logger.info("User selected New Game. Switching to PlanetGen screen.")

        # Import locally to avoid circular import
        from ui.state.ui_state_manager import UIState

        parent = self.parent()
        if parent:
            parent.set_state(UIState.PLANETGEN)
        else:
            logger.warning("No parent UIStateManager found to switch screens.")

    def quit_to_desktop(self):
        """
        Slot: Handle graceful shutdown when Quit button is pressed.
        """
        logger.info("Quit to Desktop triggered by user.")
        sys.exit(0)
