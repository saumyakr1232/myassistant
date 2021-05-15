import logging
from settings.setting import DEBUG

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(".log", 'w'),
              logging.StreamHandler()
              ],

)

def get_logger():
    logger = logging.getLogger()
    if DEBUG:
        logger.setLevel(10)
    return logger