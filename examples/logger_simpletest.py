from adafruit_logger import Logger, ERROR, INFO
logger = Logger()

logger.level = ERROR
logger.log(INFO, 'Info message')
logger.log(ERROR, 'Error message')
