# core/logging_config.py
import logging
import os
from logging.handlers import TimedRotatingFileHandler


def configure_logging(log_level=logging.INFO):
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=date_format,
    )

    log_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../logs")

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_file = os.path.join(log_directory, "app.log")

    rotating_handler = TimedRotatingFileHandler(
        log_file,
        when="midnight",  # Daily rotation
        interval=1,
        backupCount=5,
    )

    rotating_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
    logging.getLogger().addHandler(rotating_handler)
