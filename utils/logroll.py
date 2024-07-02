# logroll.py
import os
import sys
import logging
from logging.handlers import RotatingFileHandler

if not os.path.exists('logs'):
    os.makedirs('logs')

log_handler = RotatingFileHandler(
    os.path.join('logs', 'debug.log'),
    maxBytes = 32 * 1024 * 1024,
    backupCount = 5,
    encoding = 'utf-8'
)

logging.basicConfig(level=logging.DEBUG,
                    handlers=[log_handler],
                    format='%(asctime)s: %(name)s[%(levelname)s]: %(message)s')

log = logging.getLogger(__name__)

# log.debug("This is a debug message")
# log.info("This is an info message")
# log.warning("This is a warning message")
# log.error("This is an error message")
# log.critical("This is a critical message")