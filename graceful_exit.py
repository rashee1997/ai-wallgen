import signal
import sys
import logging

# Import necessary components for preference saving
try:
    from wallpaper_settings import UserPreferences
    from ui_utils import print_info, print_success, print_warning, print_error
    # Import user_prefs inside the handler to avoid circular dependencies
    # and ensure it's initialized when the handler is called.
except ImportError as e:
    logging.error(f"Failed to import necessary modules for graceful exit: {e}")
    # Define dummy functions if imports fail, so the handler doesn't crash
    class UserPreferences: pass
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
        # Avoid running the full exit logic again if already exiting
        print("\nExit process already initiated.")
        # Don't exit immediately here, let the first call handle it
        return
        
    _exiting = True
    print("\nThank you and good boy!")

    try:
        # Import user_prefs here to get the potentially initialized object
        # This assumes wallpaper_generator has initialized it.
        from wallpaper_generator import user_prefs
        
        if 'user_prefs' in locals() and isinstance(user_prefs, UserPreferences):
            print_info("Attempting to save current preferences...")
            user_prefs.save_preferences()
            print_success("Preferences saved successfully.")
        else:
            # Check if user_prefs exists globally but is None or wrong type
            if 'user_prefs' in globals():
                 print_warning(f"User preferences object found but is not valid type ({type(user_prefs)}), cannot save.")
            else:
                 print_warning("User preferences object ('user_prefs') not found globally, cannot save.")
            
    except ImportError:
         print_warning("Could not import 'user_prefs' from wallpaper_generator. Cannot save preferences.")
    except NameError:
         # This might happen if wallpaper_generator hasn't defined user_prefs yet
         print_warning("'user_prefs' not defined in wallpaper_generator. Cannot save preferences.")
    except Exception as e:
        print_error(f"An error occurred while saving preferences: {str(e)}")
        logging.error(f"Error during interrupt save: {e}", exc_info=True)

    print_info("Exiting application.")
    sys.exit(0)

# --- Global Exception Hook for KeyboardInterrupt ---
_original_excepthook = sys.excepthook

def custom_excepthook(exc_type, exc_value, exc_traceback):
    """
    Custom exception hook to catch unhandled KeyboardInterrupts
    and trigger the graceful exit logic.
    """
    if issubclass(exc_type, KeyboardInterrupt):
        # Call our custom exit handler for Ctrl+C
        handle_exit_interrupt()
    else:
        # Call the original excepthook for all other exceptions
        _original_excepthook(exc_type, exc_value, exc_traceback)

# Set the custom excepthook globally when this module is imported
sys.excepthook = custom_excepthook
logging.info("Custom exception hook set for KeyboardInterrupt.")
