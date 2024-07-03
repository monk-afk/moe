# logroll.py
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

logging.basicConfig(level=logging.DEBUG,
                    handlers=[log_handler],
                    format='%(asctime)s: %(name)s[%(levelname)s]: %(message)s')

log = logging.getLogger(__name__)

# log.debug("This is a debug message")
# log.info("This is an info message")
# log.warning("This is a warning message")
# log.error("This is an error message")
# log.critical("This is a critical message")



####################################################################################
# MIT License                                                                      #
#                                                                                  #
# Copyright (c) 2024 monk                                                          #
#                                                                                  #
# Permission is hereby granted, free of charge, to any person obtaining a copy     #
# of this software and associated documentation files (the "Software"), to deal    #
# in the Software without restriction, including without limitation the rights     #
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell        #
# copies of the Software, and to permit persons to whom the Software is            #
# furnished to do so, subject to the following conditions:                         #
#                                                                                  #
# The above copyright notice and this permission notice shall be included in all   #
# copies or substantial portions of the Software.                                  #
#                                                                                  #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR       #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,         #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE      #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER           #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,    #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE    #
# SOFTWARE.                                                                        #
####################################################################################