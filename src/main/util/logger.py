import logging

def log(level, message):
    logger = logging.getLogger("my_logger")
    logger.log(level, message)