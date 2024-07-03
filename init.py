import sys
import time
from utils.logroll import log
import signal

print(f"Initializing moe")

def handle_signal(sig, frame):
    log.info('Received shutdown signal. Exiting...')
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    from utils.bot import run_bot

    while True:
        try:
            run_bot()
        except Exception as e:
            log.error(f'Bot process crashed with error: {e}')
            log.warning('Restarting bot process...')
            time.sleep(5)

if __name__ == '__main__':
    main()




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