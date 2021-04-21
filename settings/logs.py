import logging
from settings.setting import DEBUG

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(".log", 'w'),
              logging.StreamHandler()
              ]
)

logger = logging.getLogger()

if DEBUG:
    logger.setLevel(logging.DEBUG)
