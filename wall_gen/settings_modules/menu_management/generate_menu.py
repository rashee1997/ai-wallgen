"""
Generate menu module for wallpaper generation.

This module provides functionality for generating wallpapers and prompts,
including options to use Gemini AI, random prompts, or custom prompts.
"""

import logging # Added logging
from typing import List, Tuple, Dict, Any, Optional
# Updated imports
from wall_gen.ui_utils import (
    print_section,
    print_menu_options,
    get_menu_choice,
    print_info,
    print_warning,
    print_success,
    print_breadcrumb,
    print_error,
    get_validated_input,
    show_spinner,
)

# Import from other internal modules (updated paths)
from ..settings_manager import get_preferences # Relative import for parent package
from ..preset_management_tinydb import load_preset_tinydb # Relative import for parent package
# Relative import for sibling module is correct
from .advanced_options_menu import (
    configure_advanced_options,
)
# Import from root module is correct
from prompt_generator import (
    use_user_preferences,
    # enhance_custom_prompt, # This is now likely handled by prompt_service
    generate_random_style_mix,
)


def run_generate_menu(generate_only: bool = False):
    """
    Run the Generate menu for wallpaper or prompt generation.

    Args:
        generate_only: If True, only generate the prompt without creating an image

    Returns:
        None
    """
    section_title = "Generate Prompt Only" if generate_only else "Generate AI Wallpaper"
    breadcrumb = ["Main Menu", section_title]

    menu_options: List[Tuple[str, str]] = [
        ("1", "Use Gemini AI to generate a prompt"),
        ("2", "Use a random prompt"),
        ("3", "Enter your own custom prompt"),
        ("4", "Advanced Options - Fine-tune generation parameters"),
        ("5", "Load Saved Preset"),
        ("B", "Back to Main Menu"),
    ]

    while True:
        print_section(section_title)
        print_breadcrumb(breadcrumb)
        print_menu_options(menu_options)

        choice = get_menu_choice(
            "Select option (1-5, B)", ["1", "2", "3", "4", "5", "B", "b"]
        )
        if choice == "_INTERRUPTED_":
            raise KeyboardInterrupt

        if choice.lower() == "b":
            return

        if choice == "5":
            # Load preset menu
            # Load preset using TinyDB function
            preset_result = load_preset_tinydb() # Returns tuple (settings, name) or None
            if preset_result:
                settings, preset_name = preset_result
                print_info(f"Preset '{preset_name}' loaded. Generating wallpaper...")
                # WARNING: Calling orchestrator from run_wallgen is fragile.
                # Ideally, this menu should call services directly.
                try:
                    from run_wallgen import orchestrate_wallpaper_generation
                    user_prefs = get_preferences() # Get current prefs
                    # Pass necessary info. orchestrate_wallpaper_generation needs refactoring
                    # to accept preset settings directly or this menu needs more logic.
                    # For now, assuming it can handle a 'preset' type or similar.
                    # This call likely needs adjustment based on orchestrate_wallpaper_generation signature.
                    orchestrate_wallpaper_generation("preset", user_prefs, preset_name=preset_name, generate_only=generate_only)
                except ImportError:
                    print_error("Could not import main generation function from run_wallgen.py")
                except Exception as e:
                    print_error(f"Error running generation with preset: {e}")
            else:
                print_warning("Preset loading cancelled or failed.")
            continue # Go back to generate menu after attempting preset load/gen

        if choice == "4":
            # Advanced options menu
            configure_advanced_options()
            continue

        if choice in ["1", "2", "3"]:
            if choice == "1":
                handle_gemini_generation(generate_only)
            elif choice == "2":
                handle_random_generation(generate_only)
            elif choice == "3":
                handle_custom_generation(generate_only)


def handle_gemini_generation(generate_only: bool):
    """Handle Gemini AI prompt generation."""
    user_prefs = get_preferences()

    # Now call the main orchestrator function from run_wallgen
    # WARNING: Calling orchestrator from run_wallgen is fragile.
    try:
        from run_wallgen import orchestrate_wallpaper_generation
        # Pass prompt_type="gemini", user_prefs, and potentially mood/style if orchestrator handles them
        # This call signature needs to match orchestrate_wallpaper_generation
        # Assuming orchestrate_wallpaper_generation handles None for custom_prompt/preset_name
        orchestrate_wallpaper_generation("gemini", user_prefs, generate_only=generate_only) # Mood/Style might need separate handling or be part of user_prefs update
    except ImportError:
        print_error("Could not import main generation function from run_wallgen.py")
    except Exception as e:
        print_error(f"Error running Gemini generation: {e}")


def handle_random_generation(generate_only: bool):
    """Handle random prompt generation."""
    # WARNING: Calling orchestrator from run_wallgen is fragile.
    try:
        from run_wallgen import orchestrate_wallpaper_generation
        user_prefs = get_preferences()
        orchestrate_wallpaper_generation("random", user_prefs, generate_only=generate_only)
    except ImportError:
        print_error("Could not import main generation function from run_wallgen.py")
    except Exception as e:
        print_error(f"Error running random generation: {e}")


def handle_custom_generation(generate_only: bool):
    """Handle custom prompt entry and generation."""
    custom_prompt = get_validated_input(
        "Enter your custom prompt (or 'b' to go back)", allow_empty=False
    )
    if custom_prompt.lower() == "b":
        return

    print_info("Processing custom prompt...")
    # WARNING: Calling orchestrator from run_wallgen is fragile.
    try:
        from run_wallgen import orchestrate_wallpaper_generation
        user_prefs = get_preferences()
        orchestrate_wallpaper_generation("custom", user_prefs, custom_prompt=custom_prompt, generate_only=generate_only)
    except ImportError:
        print_error("Could not import main generation function from run_wallgen.py")
    except Exception as e:
        print_error(f"Error running custom generation: {e}")
