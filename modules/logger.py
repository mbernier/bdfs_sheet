# setup_logger.py
import logging
from modules.config import config

#get the log_level from the config.ini
#we are grabbing the attribute of the log_level from the logging object here, not just setting a string
logging_level = getattr(logging, config["log_level"])
#setup the level of logging we care about
logging.basicConfig(level=logging_level)
#define the main logger object
logger = logging.getLogger('logs')