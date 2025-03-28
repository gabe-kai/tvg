# /main.py

from logger.logger import LoggerFactory
from ui.main_ui import MainUI
from PySide6.QtWidgets import QApplication
import sys


def main():
    """
    Entry point for the application.
    Initializes a logger and starts the UI.
    """
    logger = LoggerFactory(name="TVGApp").get_logger()
    logger.info("Starting the TVG Planet Generator UI...")

    # Create the Qt application context
    app = QApplication(sys.argv)

    # Create and show the main window
    window = MainUI()
    window.show()

    # Run the application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
