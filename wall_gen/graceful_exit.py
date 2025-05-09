# wall_gen/graceful_exit.py
"""
Handles graceful exit on KeyboardInterrupt.
NOTE: This module uses absolute imports assuming it's part of the 'wall_gen' package.
It may not run correctly as a standalone script without sys.path adjustments.
"""
import signal
import sys
import logging

# Import necessary components
try:
    # Use absolute imports from the wall_gen package
    # from wall_gen.settings_modules import UserPreferences # Removed as saving logic is removed
    from wall_gen.ui_utils import print_info, print_success, print_warning, print_error
except ImportError as e:
    # This error message should now be less likely with absolute imports,
    # but keep it as a fallback during development.
    logging.error(f"Failed to import necessary modules for graceful exit using absolute paths: {e}")
    # Define dummy functions if imports fail
    # class UserPreferences: pass # Removed as saving logic is removed
    def print_info(msg): print(f"INFO: {msg}")
    def print_success(msg): print(f"SUCCESS: {msg}")
    def print_warning(msg): print(f"WARNING: {msg}")
    def print_error(msg): print(f"ERROR: {msg}")

# Flag to prevent double execution if interrupt occurs during saving
_exiting = False

def handle_exit_interrupt():
    """Handles the logic for graceful exit on interrupt."""
    global _exiting
    if _exiting:
        return # Already handling exit

    _exiting = True
    # Simplified exit message. Preference saving should be handled elsewhere (e.g., main script via atexit).
    print("\nCtrl+C detected. Exiting application.")
    logging.info("KeyboardInterrupt caught by custom hook. Exiting.")

    # Attempting to save preferences here is unreliable due to import context and potential state issues.
    # Removed the preference saving logic from this handler.

    # Perform minimal cleanup if necessary, then exit.
    # For example, could call a generic cleanup function if one exists.
    sys.exit(0) # Exit cleanly

# --- Global Exception Hook for KeyboardInterrupt ---
_original_excepthook = sys.excepthook

def custom_excepthook(exc_type, exc_value, exc_traceback):
    """
    Custom exception hook to catch unhandled KeyboardInterrupts
    and trigger the graceful exit logic.
    """
    if issubclass(exc_type, KeyboardInterrupt):
        handle_exit_interrupt()
    else:
        _original_excepthook(exc_type, exc_value, exc_traceback)

# Set the custom excepthook globally when this module is imported
# The main script (wallpaper_generator.py) will need to import this module
# for the hook to be set, e.g., 'from wall_gen import graceful_exit'
sys.excepthook = custom_excepthook
logging.info("Custom exception hook set for KeyboardInterrupt by graceful_exit module.")
