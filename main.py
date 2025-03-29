# /main.py

import sys
from PySide6.QtWidgets import QApplication
from logger.logger import LoggerFactory
from ui.main_ui import MainUI
from ui import theme
from config import ACTIVE_THEME as THEME_NAME

# Dynamically select the active theme object from the theme module
ACTIVE_THEME = getattr(theme, THEME_NAME, theme.DARK_THEME)


def main():
    """
    Entry point for the application.
    Initializes a logger, applies the global stylesheet, and starts the UI.
    """
    logger = LoggerFactory(name="TVGApp").get_logger()
    logger.info("Starting the The Vassal Game UI...")

    # Create the Qt application context
    app = QApplication(sys.argv)
    app.setStyleSheet(ACTIVE_THEME)
    logger.info(f"Using theme: {THEME_NAME}")

    # Create and show the main window
    window = MainUI()
    window.show()

    # Run the application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
