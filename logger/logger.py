# logger/logger.py

import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional

import config  # assumes config.py exists at root level


class ColorFormatter(logging.Formatter):
    """
    Custom formatter to add ANSI colors to log output based on severity level.
    """
    COLOR_MAP = {
        logging.DEBUG: "\033[90m",     # Bright Black / Gray
        logging.INFO: "\033[94m",      # Blue
        logging.WARNING: "\033[93m",   # Yellow
        logging.ERROR: "\033[91m",     # Red
        logging.CRITICAL: "\033[1;91m" # Bold Red
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLOR_MAP.get(record.levelno, self.RESET)
        message = super().format(record)
        return f"{color}{message}{self.RESET}"


class LoggerFactory:
    """
    LoggerFactory creates and configures a logger instance for the application.

    This class supports different logging levels, output formats, and destinations
    (e.g. console, file), and is intended to be used throughout the application
    for consistent logging behavior.
    """

    def __init__(self, name: str, log_level: Optional[int] = None):
        """
        Initialize a new LoggerFactory.

        :param name: Name of the logger.
        :param log_level: Optional override for the logging level.
        """
        self.name = name
        self.log_level = log_level or getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
        self.logger = logging.getLogger(self.name)
        self._setup_logger()

    def _setup_logger(self):
        """
        Sets up the logger with formatting and handlers (console and rotating file).
        Prevents duplicate handlers if logger is re-initialized.
        """
        if not self.logger.hasHandlers():
            self.logger.setLevel(self.log_level)

            formatter = logging.Formatter(
                fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )

            if config.LOG_TO_CONSOLE:
                console_handler = logging.StreamHandler()
                console_formatter = ColorFormatter(
                    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S"
                )
                console_handler.setFormatter(console_formatter)
                self.logger.addHandler(console_handler)

            if config.LOG_TO_FILE:
                log_dir = Path(config.LOG_DIR)
                log_dir.mkdir(parents=True, exist_ok=True)
                file_path = log_dir / config.LOG_FILE_NAME

                file_handler = RotatingFileHandler(
                    encoding="utf-8",
                    filename=str(file_path),
                    maxBytes=config.LOG_FILE_MAX_BYTES,
                    backupCount=config.LOG_FILE_BACKUP_COUNT
                )
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        """
        Returns the configured logger instance.
        """
        return self.logger
