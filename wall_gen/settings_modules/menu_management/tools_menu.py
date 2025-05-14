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
    print_error,
    print_success,
    print_breadcrumb,
    get_validated_input,
    clear_screen, # Added
    print_header, # Added
)
# Import necessary modules for the new menu option
from ... import gemini_config # To access AVAILABLE_GEMINI_MODELS, set_selected_gemini_model, get_selected_gemini_model
from ..settings_manager import get_preferences # To get user_prefs instance


def handle_select_gemini_model():
    """Handles the UI for selecting the non-Imagen Gemini model."""
    user_prefs = get_preferences()
    current_model = gemini_config.get_selected_gemini_model(user_prefs)
    
    clear_screen()
    print_header("Select Gemini Model (Non-Imagen)")
    # print_section("Select Gemini Model (Non-Imagen Tasks)") # Replaced by print_header
    print_info(f"Current model: {current_model}")
    print_info("Available models:")
    
    for i, model_name in enumerate(gemini_config.AVAILABLE_GEMINI_MODELS, 1):
        print_menu_options([(str(i), model_name)]) # Re-using print_menu_options for consistent formatting

    prompt_text = f"Select model (1-{len(gemini_config.AVAILABLE_GEMINI_MODELS)}, or 'c' to cancel):"
    valid_choices = [str(i) for i in range(1, len(gemini_config.AVAILABLE_GEMINI_MODELS) + 1)] + ["c"]
    
    choice = get_validated_input(
        prompt_text, 
        options=valid_choices, # Ensure 'options' keyword is used
        help_context_id="TOOLS_SELECT_GEMINI_MODEL_CHOICE"
    )

    if choice == "_HELP_SHOWN_":
        # If help was shown, we want to re-display this sub-menu/prompt.
        # Since this function doesn't have its own loop, returning will go back to run_tools_menu,
        # which will then re-enter this function if the user chooses option '6' again.
        # This is an acceptable flow for now.
        return 
    if choice.lower() == 'c':
        print_info("Model selection cancelled.")
        return

    try:
        selected_index = int(choice) - 1
        chosen_model_name = gemini_config.AVAILABLE_GEMINI_MODELS[selected_index]
        
        if gemini_config.set_selected_gemini_model(chosen_model_name, user_prefs):
            print_success(f"Gemini model for non-Imagen tasks set to: {chosen_model_name}")
        else:
            print_error(f"Failed to set Gemini model to: {chosen_model_name}")
    except (ValueError, IndexError):
        print_error("Invalid selection. Please try again.")
    except Exception as e:
        print_error(f"An error occurred: {e}")
        logging.error(f"Error selecting Gemini model: {e}", exc_info=True)


def handle_toggle_structured_logo_prompt():
    """Handles toggling the structured logo prompt format preference."""
    user_prefs = get_preferences()
    current_status = user_prefs.use_structured_logo_prompt_format
    new_status = not current_status
    user_prefs.use_structured_logo_prompt_format = new_status
    # Attempt to save immediately if possible, or rely on atexit/menu save
    try:
        user_prefs.save_preferences()
        print_success(f"Structured Logo Prompt format set to: {'On' if new_status else 'Off'}. Preferences saved.")
    except Exception as e:
        print_warning(f"Structured Logo Prompt format set to: {'On' if new_status else 'Off'}. Error saving preferences immediately: {e}")
        logging.warning(f"Error saving preferences in handle_toggle_structured_logo_prompt: {e}", exc_info=True)
    
    # Pause to show message before screen clears
    get_validated_input("Press Enter to continue...", options=None, allow_empty=True, help_context_id="TOOLS_TOGGLE_LOGO_PROMPT_CONTINUE") 


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
        ("6", "Select Gemini Model (Non-Imagen)"), # New menu option
        ("7", "Toggle Structured Logo Prompt"), # New menu option for logo prompt format
        ("b", "Return to Main Menu"),
    ]

    while True:
        user_prefs = get_preferences() # Get latest prefs for display
        clear_screen()
        print_header("WallGen Tools & Utilities")
        # print_section("Tools & Utilities") # Replaced by print_header for consistency
        print_breadcrumb(["Main Menu", "Tools & Utilities"])
        
        # Update menu option text dynamically
        menu_options_display = []
        for key, text in menu_options:
            if key == "7":
                status = 'On' if getattr(user_prefs, 'use_structured_logo_prompt_format', False) else 'Off'
                menu_options_display.append((key, f"{text} (Currently: {status})"))
            else:
                menu_options_display.append((key, text))
        print_menu_options(menu_options_display)

        choice = get_menu_choice(
            prompt="Select an option", # Generic prompt
            valid_choices=["1", "2", "3", "4", "5", "6", "7", "b"], 
            help_context_id="TOOLS_MENU" 
        )
        if choice == "_HELP_SHOWN_":
            continue
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
        elif choice == "6": # New choice handler
            handle_select_gemini_model()
        elif choice == "7": # Handler for the new logo prompt format toggle
            handle_toggle_structured_logo_prompt()
