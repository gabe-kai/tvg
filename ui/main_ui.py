# /ui/main_ui.py

import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QSize

# Use project-wide logging system
from logger.logger import LoggerFactory
logger = LoggerFactory("main_ui").get_logger()

# Use the centralized screen manager
from ui.state.ui_state_manager import UIStateManager


class MainUI(QMainWindow):
    """
    Main application window for The Vassal Game UI.
    Sets the window title, default size, and minimum size constraints.
    Loads the UIStateManager as the central widget to manage screens.
    """

    def __init__(self):
        super().__init__()

        # Set window title
        self.setWindowTitle("The Vassal Game")

        # Set initial size to 1024x768
        self.resize(QSize(1024, 768))

        # Set minimum size to 800x600
        self.setMinimumSize(QSize(800, 600))

        # Use UIStateManager to control screens
        self.state_manager = UIStateManager(self)
        self.setCentralWidget(self.state_manager)

        logger.info("MainUI initialized with UIStateManager")


if __name__ == "__main__":
    """
    Run this file directly to launch the UI standalone.
    This is mostly useful for UI testing outside of the full app context.
    """
    app = QApplication(sys.argv)

    # Apply global stylesheet to entire application
    from ui.theme import DARK_THEME
    app.setStyleSheet(DARK_THEME)
    window = MainUI()
    window.show()
    sys.exit(app.exec())
