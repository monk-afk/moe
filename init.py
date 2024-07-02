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
