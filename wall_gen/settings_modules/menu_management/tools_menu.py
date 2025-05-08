"""
Tools & utilities menu module.

This module provides functionality for the Tools & Utilities menu,
including preset management, viewing history, exporting/importing settings, etc.
"""

import logging # Added logging
from typing import List, Tuple
# Updated imports
from wall_gen.ui_utils import (
    print_section,
    print_menu_options,
    get_menu_choice,
    print_info,
    print_warning,
    print_success,
    print_breadcrumb,
    get_validated_input,
)


def run_tools_menu():
    """
    Run the Tools & Utilities menu.

    Returns:
        None
    """
    menu_options: List[Tuple[str, str]] = [
        ("1", "Manage Presets"),
        ("2", "View Generation History"),
        ("3", "Export Settings"),
        ("4", "Import Settings"),
        ("5", "Update History Filenames"),
        ("b", "Return to Main Menu"),
    ]

    while True:
        print_section("Tools & Utilities")
        print_breadcrumb(["Main Menu", "Tools & Utilities"])
        print_menu_options(menu_options)

        choice = get_menu_choice(
            "Select option (1-5, b)", ["1", "2", "3", "4", "5", "b"]
        )
        if choice == "_INTERRUPTED_":
            return  # Exit if interrupted
        if choice == "_EOF_":
            print_info("Input closed. Returning to main menu.")
            return

        if choice == "b":
            return

        if choice == "1":
            # Manage presets (using relative import for parent package)
            try:
                from ..preset_management_tinydb import manage_presets_tinydb
                manage_presets_tinydb()
            except ImportError:
                print_error("Could not load preset management module.")
        elif choice == "2":
            # View generation history (using absolute import)
            try:
                from wall_gen.history.history_manager import view_history
                view_history()
            except ImportError:
                print_error("Could not load history module.")
        elif choice == "3":
            # Export settings (using relative import for parent package)
            try:
                from ..settings_import_export import export_settings
                export_settings()
            except ImportError:
                print_error("Could not load settings export module.")
        elif choice == "4":
            # Import settings (using relative import for parent package)
            try:
                from ..settings_import_export import import_settings
                import_settings()
            except ImportError:
                print_error("Could not load settings import module.")
        elif choice == "5":
            # Update history filenames (using relative import for parent package)
            try:
                from ..settings_utils import update_history_with_filenames
                print_info("Updating generation history with descriptive filenames...")
                update_history_with_filenames(silent=False)
            except ImportError:
                print_error("Could not load settings utils module.")
            update_history_with_filenames(silent=False)
