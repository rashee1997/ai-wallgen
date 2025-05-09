"""
Main menu module for WallGen application.

This module provides the top-level menu functionality for the entire application,
including wallpaper generation, preference management, tools, and more.
"""

import os # Added import
from typing import List, Tuple
# Updated imports for modules moved into wall_gen
from wall_gen.ui_utils import (
    print_section,
    print_menu_options,
    get_menu_choice,
    print_info,
    print_warning,
    print_success,
    print_header,
    get_validated_input,
    show_ascii_art,
    print_error,
)
# Relative imports for sibling modules within menu_management are correct
from .wallpaper_settings_menu import manage_wallpaper_settings
from .advanced_options_menu import (
    configure_advanced_options,
    reset_all_settings_to_none,
)
from .generate_menu import run_generate_menu
from .tools_menu import run_tools_menu
from .image_preview_menu import run_image_preview_menu
# Use relative imports for parent package modules
from ..settings_manager import get_preferences
from ..settings_utils import update_history_with_filenames


def run_main_menu():
    """
    Run the main menu loop for the WallGen application.

    This function displays the main menu and handles top-level navigation
    to all other menus and functions of the application.
    """
    # Check and create necessary directories
    import os

    os.makedirs("genimage", exist_ok=True)

    # Update existing history entries with image filenames (silently)
    update_history_with_filenames(silent=True)

    # Show welcome message -- REMOVED, handled by run_wallgen.py
    # show_ascii_art()

    while True:
        menu_options: List[Tuple[str, str]] = [
            ("1", "Generate AI Wallpaper - Create custom wallpapers using AI"),
            ("2", "Generate Prompt Only - Create and save prompts without images"),
            ("3", "Manage Preferences - Customize wallpaper settings"),
            ("4", "Tools & Utilities"),
            ("5", "View Generation History"),
            ("7", "Preview Recent Images"),
            ("E", "Exit - Save and exit"),
        ]

        print_section("Main Menu")
        print_menu_options(menu_options)

        choice = get_menu_choice(
            "Select an option (1-5, 7, E)", ["1", "2", "3", "4", "5", "7", "E", "e"]
        )
        if choice == "_INTERRUPTED_":
            # Handle graceful exit
            print_info("Saving preferences before exit...")
            user_prefs = get_preferences()
            user_prefs.save_preferences()
            print_success("Goodbye!")
            break

        if choice in ["1", "2"]:  # Generate AI Wallpaper or Generate Prompt Only
            generate_only = choice == "2"
            run_generate_menu(generate_only)
        elif choice == "3":
            manage_preferences()
        elif choice == "4":
            run_tools_menu()
        elif choice == "5":
            # Import view_history using absolute package path
            try:
                from wall_gen.history.history_manager import view_history
                view_history()
            except ImportError:
                print_error("Could not load history module.")

        elif choice.upper() == "E":
            print_info("Saving preferences before exit...")
            user_prefs = get_preferences()
            user_prefs.save_preferences()
            print_success("Goodbye!")
            break
        elif choice == "7":
            run_image_preview_menu()


def manage_preferences():
    """
    Function to manage user preferences.

    This function displays a menu of preference categories and allows the user
    to select which category to manage. It then delegates to the appropriate
    function for that category.
    """
    menu_options: List[Tuple[str, str]] = [
        ("1", "Wallpaper Settings"),
        ("2", "Advanced Options"),
        ("3", "Reset All Settings to None"),
    ]

    while True:
        print_section("Manage Preferences")
        print_menu_options(menu_options)  # Display the options
        choice: str = get_menu_choice("Select option (1-3, b)", ["1", "2", "3", "b"])
        if choice == "_INTERRUPTED_":
            return  # Exit preference management if interrupted

        if choice == "b":
            return

        handlers = {
            "1": manage_wallpaper_settings,
            "2": configure_advanced_options,
            "3": lambda: confirm_and_reset(),
        }

        if choice in handlers:
            handlers[choice]()


def confirm_and_reset():
    """Helper function to handle reset confirmation."""
    confirm = get_validated_input(
        "Are you sure you want to reset ALL settings to None? This cannot be undone. (y/n)",
        ["y", "n"],
    )
    if confirm.lower() == "y":
        reset_all_settings_to_none()
    else:
        print_info("Reset cancelled.")
