"""
Menu management subpackage for settings modules.

This subpackage contains modules for handling the various settings menus
in the wallpaper generation application.
"""

from .main_menu import manage_preferences
from .genres_menu import manage_genres
from .styles_menu import manage_styles
from .moods_menu import manage_moods
from .wallpaper_settings_menu import manage_wallpaper_settings
from .advanced_options_menu import configure_advanced_options

__all__ = [
    # Main menu
    'manage_preferences',
    
    # Category menus
    'manage_genres',
    'manage_styles',
    'manage_moods',
    'manage_wallpaper_settings',
    'configure_advanced_options',
]
