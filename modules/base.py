#setup logging
import logging


class BaseClass:
    logger = None
    logger_name = None

    def __init__(self):
        from modules.logger import logger

        self.logger = logger
        if None != self.logger_name:
            #define a sub-logger just for this code
            log_name = 'logs.' + self.logger_name
            print(log_name)
            logger = logging.getLogger(log_name)

    def info(self, str):
        self.logger.info("  %s", str)

    def warning(self, str):
        self.logger.warning("  %s", str)

    def debug(self, str):
        self.logger.debug("  %s", str)

    def error(self, str):
        self.logger.error("  %s", str)

    def critical(self, str):
        self.logger.critical("  %s", str)