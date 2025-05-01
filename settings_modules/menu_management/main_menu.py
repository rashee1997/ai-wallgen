"""
Main menu module for settings management.

This module provides the top-level menu functionality for managing user preferences
and settings in the wallpaper generation application.
"""

from typing import List, Tuple
from ui_utils import print_section, print_menu_options, get_menu_choice, print_info, print_success, get_validated_input
from .wallpaper_settings_menu import manage_wallpaper_settings
from .advanced_options_menu import configure_advanced_options, reset_all_settings_to_none

def manage_preferences():
    """
    Main function to manage user preferences.
    
    This function displays a menu of preference categories and allows the user
    to select which category to manage. It then delegates to the appropriate
    function for that category.
    """
    menu_options: List[Tuple[str, str]] = [
        ("1", "Wallpaper Settings"),
        ("2", "Advanced Options"),
        ("3", "Reset All Settings to None")
    ]

    while True:
        print_section("Manage Preferences")
        print_menu_options(menu_options) # Display the options
        choice: str = get_menu_choice("Select option (1-3, b)", ["1", "2", "3", "b"])
        if choice == "_INTERRUPTED_":
            return # Exit preference management if interrupted

        if choice == "b":
            return

        handlers = {
            "1": manage_wallpaper_settings,
            "2": configure_advanced_options,
            "3": lambda: confirm_and_reset()
        }

        if choice in handlers:
            handlers[choice]()

def confirm_and_reset():
    """Helper function to handle reset confirmation."""
    confirm = get_validated_input(
        "Are you sure you want to reset ALL settings to None? This cannot be undone. (y/n)",
        ["y", "n"]
    )
    if confirm.lower() == "y":
        reset_all_settings_to_none()
    else:
        print_info("Reset cancelled.")
