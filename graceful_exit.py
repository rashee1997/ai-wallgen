import signal
import sys

def _signal_handler(sig, frame):
    print("\nGraceful exit on user interrupt.")
    sys.exit(0)

def setup_graceful_exit():
    signal.signal(signal.SIGINT, _signal_handler)

# Automatically set up the handler when this module is imported
setup_graceful_exit()
