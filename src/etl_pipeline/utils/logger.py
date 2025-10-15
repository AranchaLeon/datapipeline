import logging
import os
import sys
from logging.handlers import RotatingFileHandler


def get_logger(name="src", level=None):
    """
    Configure and return a logger with standard formatting and file rotation.
    If the logger already has handlers, it returns the existing logger.

    Args:
        name (str): Logger name. Default is 'src'.
        level (str, optional): Logging level ('INFO', 'DEBUG', etc).
            If not specified, uses LOG_LEVEL from environment or 'INFO'.

    Returns:
        logging.Logger: Configured logger instance.
    """
    level = level or os.getenv("LOG_LEVEL", "INFO")
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(getattr(logging, level.upper()))
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    # optional file rotating
    fh = RotatingFileHandler("src.log", maxBytes=5_000_000, backupCount=3)
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    return logger
