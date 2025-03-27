# main.py

from logger.logger import LoggerFactory
from ui.main_ui import launch_ui


def main():
    """
    Entry point for the application.
    Initializes a logger and starts the UI.
    """
    logger = LoggerFactory(name="TVGApp").get_logger()
    logger.info("Starting the TVG Planet Generator UI...")
    launch_ui()


if __name__ == "__main__":
    main()
