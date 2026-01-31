import logging

from app.config import LOGGER_CONFIG


def config_logger(name: str) -> logging.Logger:
    """
    Configure logger
    :param name:
    :return:
    """
    # Create Log
    log = logging.getLogger(name)
    # Create Handler
    fh = logging.FileHandler(LOGGER_CONFIG["file"])
    fh.setLevel(LOGGER_CONFIG["level"])
    fh.setFormatter(LOGGER_CONFIG["formatter"])
    # Apply
    log.addHandler(fh)
    log.setLevel(LOGGER_CONFIG["level"])

    return log
