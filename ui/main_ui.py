# /ui/main_ui.py

from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QSize

# Project Logging
from logger.logger import LoggerFactory
logger = LoggerFactory("main_ui").get_logger()

# UI State Management
from ui.state.ui_state_manager import UIStateManager


class MainUI(QMainWindow):
    """
    Main application window for The Vassal Game UI.
    Sets the window title, default size, and minimum size constraints.
    Loads the UIStateManager as the central widget to manage screens.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("The Vassal Game")
        self.resize(QSize(1024, 768))
        self.setMinimumSize(QSize(800, 600))

        self.state_manager = UIStateManager(self)
        self.setCentralWidget(self.state_manager)

        logger.info("MainUI initialized with UIStateManager")
