import logging

def setup_logging(level, format):
    logger = logging.getLogger("my_logger")
    logger.setLevel(level)
    handler = logging.StreamHandler()    
    handler.setFormatter(format)
    logger.addHandler(handler)
    logger.info("Logger initialized!")