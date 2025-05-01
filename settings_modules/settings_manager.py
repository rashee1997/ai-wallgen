import logging
from .user_preferences import UserPreferences

user_prefs = None

def initialize_settings() -> UserPreferences:
    """
    Initialize and return the user preferences object.
    This creates a UserPreferences instance, loads preferences from file,
    and sets the global user_prefs variable.
    """
    global user_prefs
    user_prefs = UserPreferences()
    return user_prefs

def get_preferences() -> UserPreferences:
    """
    Get the current user preferences object. If not initialized, call initialize_settings().
    """
    global user_prefs
    if user_prefs is None:
        return initialize_settings()
    return user_prefs