import os
import logging
import sys

def setup_logging(log_dir="logs", log_file="trading.log"):
    """
    Configures standard Python logging to output to a file and console.
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_path = os.path.join(log_dir, log_file)
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        # Create file handler
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)

        # Console handler for immediate feedback (errors mainly, rich handles stdout)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.ERROR)

        # Formatter capturing required info
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Create a default logger instance
logger = setup_logging()
