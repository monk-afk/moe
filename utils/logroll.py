# moe/utils/logroll.py
# Copyright © 2026 2015-present Rapptz
# SPDX-License-Identifier: MIT
# https://discordpy.readthedocs.io/en/latest/logging.html#logging-setup
import os
import sys
import logging
from logging.handlers import RotatingFileHandler

if not os.path.exists('logs'):
    os.makedirs('logs')

log_handler = RotatingFileHandler(
    os.path.join('logs', 'debug.log'),
    maxBytes = 32 * 1024 * 1024,  # 32 MiB
    backupCount = 5,  # Rotate through 5 files
    encoding = 'utf-8'
)

logging.basicConfig(level=logging.ERROR,
                    handlers=[log_handler],
                    format='%(asctime)s: %(name)s[%(levelname)s]: %(message)s')

logging = logging
