"""
Menu management subpackage for settings modules.

This subpackage contains modules for handling the various settings menus
in the wallpaper generation application.
"""

from wall_gen.settings_modules.menu_management.main_menu import manage_preferences
from wall_gen.settings_modules.menu_management.genres_menu import manage_genres
from wall_gen.settings_modules.menu_management.styles_menu import manage_styles
from wall_gen.settings_modules.menu_management.moods_menu import manage_moods
from wall_gen.settings_modules.menu_management.wallpaper_settings_menu import manage_wallpaper_settings
from wall_gen.settings_modules.menu_management.advanced_options_menu import configure_advanced_options

__all__ = [
    # Main menu
    "manage_preferences",
    # Category menus
    "manage_genres",
    "manage_styles",
    "manage_moods",
    "manage_wallpaper_settings",
    "configure_advanced_options",
]
