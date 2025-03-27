# main.py

from logger.logger import LoggerFactory


def main():
    """
    Entry point for the application.
    Initializes a logger and logs messages at various levels.
    """
    logger = LoggerFactory(name="TVGApp").get_logger()

    logger.debug("This is a DEBUG message.")
    logger.info("This is an INFO message.")
    logger.warning("This is a WARNING message.")
    logger.error("This is an ERROR message.")
    logger.critical("This is a CRITICAL message.")


if __name__ == "__main__":
    main()
