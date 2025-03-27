# config.py

import os

# Logging configuration
LOG_LEVEL = "DEBUG"                # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_TO_CONSOLE = True
LOG_TO_FILE = True

# Absolute path to centralized logs folder (always under tvg/logs/)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(ROOT_DIR, "logs")
LOG_FILE_NAME = "tvg.log"
LOG_FILE_MAX_BYTES = 5 * 1024 * 1024  # 5 MB
LOG_FILE_BACKUP_COUNT = 3             # Keep 3 backups
