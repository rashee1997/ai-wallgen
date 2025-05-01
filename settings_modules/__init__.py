"""
Settings modules package for WallGen.

This package contains modules for handling user settings, preferences,
presets, and menu functionality for the wallpaper generation application.
"""

from .settings_manager import initialize_settings, get_preferences
from .user_preferences import UserPreferences
from .menu_management.main_menu import manage_preferences

__all__ = [
    # Core settings management
    'initialize_settings',
    'get_preferences',
    'UserPreferences',
    
    # Menu functions
    'manage_preferences',
    
    # Preset management
    'preset_management',  # Access functions like manage_presets, load_preset, save_preset, delete_preset
    
    # Settings import/export
    'settings_import_export',  # Access functions like export_settings, import_settings
    
    # AI preset generation
    'ai_preset_generation',  # Access functions like generate_ai_preset
    
    # Utility functions
    'settings_utils',  # Access functions like load_last_genre, save_last_genre, update_history_with_filenames
]
