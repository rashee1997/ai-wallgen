# settings_modules/menu_management/advanced_options_menu.py

import os
import json
import re
import logging
from typing import List, Tuple, Dict, Any, Optional
from ui_utils import (
    print_section,
    print_option,
    print_info,
    print_success,
    print_warning,
    print_error,
    get_validated_input,
    print_colored,
)
from config import available_genres, STYLE_CATEGORIES
from ..settings_manager import get_preferences

try:
    from prompt_generator import set_prompt_preferences, PROMPT_GENERATOR_AVAILABLE
except ImportError:
    PROMPT_GENERATOR_AVAILABLE = False

try:
    from ai_style_generator import (
        handle_style_generation,
        initialize_gemini,
        AI_STYLE_GEN_AVAILABLE,
    )
except ImportError:
    AI_STYLE_GEN_AVAILABLE = False

# Inter-menu imports
from .genres_menu import manage_genres
from .styles_menu import manage_styles
from .moods_menu import manage_moods
from ..ai_preset_generation import generate_ai_preset
from .camera_menu import manage_camera_settings
from .output_quality_menu import manage_output_quality_settings
from .lighting_menu import manage_lighting_settings
from .composition_menu import manage_composition_settings
from .color_menu import manage_color_settings
from .negative_prompt_menu import manage_negative_prompt
from .imagen_settings_menu import manage_imagen_settings
from .software_settings_menu import manage_software_settings


def configure_advanced_options():
    """
    Menu for advanced options configuration, calling appropriate sub-menus.
    """
    while True:
        print_section("Advanced Options")
        print_option("1", "Genres")
        print_option("2", "Style Settings & Options")
        print_option("3", "Moods")
        print_option("4", "Aspect Ratio")
        print_option("5", "Negative Prompt")
        print_option("6", "Imagen Settings")
        print_option("7", "Prompt Generation Settings")
        print_option("8", "Camera & Technical Settings")
        print_option("9", "Output Quality Settings")
        print_option("10", "Lighting & Atmosphere")
        print_option("11", "Composition & Environment")
        print_option("12", "Color & Detail Settings")
        print_option("13", "View Current Settings")
        print_option("14", "Generate AI Preset")
        print_option("15", "Reset to Default")
        print_option("16", "Software Settings & Renderer")
        print_option("b", "Back")

        valid_options = [str(i) for i in range(1, 17)] + ["b"]
        choice = get_validated_input("Choose: ", valid_options)

        menu_map = {
            "1": manage_genres,
            "2": manage_styles,
            "3": manage_moods,
            "4": change_aspect_ratio,
            "5": manage_negative_prompt,
            "6": manage_imagen_settings,
            "7": manage_prompt_generation_settings,
            "8": manage_camera_settings,
            "9": manage_output_quality_settings,
            "10": manage_lighting_settings,
            "11": manage_composition_settings,
            "12": manage_color_settings,
            "13": view_current_settings,
            "14": generate_ai_preset,
            "15": reset_to_default,
            "16": manage_software_settings,
        }
        if choice in menu_map:
            menu_map[choice]()
        elif choice == "b":
            return


def manage_prompt_generation_settings():
    """
    Interactive menu for configuring prompt generation preferences.
    May delegate to prompt_generator module if available.
    """
    if PROMPT_GENERATOR_AVAILABLE:
        print_section("Prompt Generator Settings")
        set_prompt_preferences()
    else:
        print_warning("Prompt generator module not available.")


def reset_all_settings_to_none():
    """
    Reset all user preferences settings to None or initial state.
    """
    user_prefs = get_preferences()
    user_prefs.preferred_genres.clear()
    user_prefs.preferred_styles.clear()
    user_prefs.preferred_moods.clear()
    user_prefs.negative_prompts.clear()
    for d in [user_prefs.imagen_settings, user_prefs.wallpaper_settings]:
        for k in d.keys():
            d[k] = None
    user_prefs.save_preferences()
    print_success("All settings have been reset to None.")


def view_current_settings():
    """
    Display all current settings for the user.
    """
    user_prefs = get_preferences()
    # Display primary attributes for review
    print_info("Preferred Genres: " + str(getattr(user_prefs, "preferred_genres", [])))
    print_info("Preferred Styles: " + str(getattr(user_prefs, "preferred_styles", [])))
    print_info("Preferred Moods: " + str(getattr(user_prefs, "preferred_moods", [])))
    print_info("Negative Prompts: " + str(getattr(user_prefs, "negative_prompts", [])))
    print_info(
        "Wallpaper Settings: " + str(getattr(user_prefs, "wallpaper_settings", {}))
    )
    print_info("Imagen Settings: " + str(getattr(user_prefs, "imagen_settings", {})))
    print_info("Aspect Ratio: " + str(getattr(user_prefs, "aspect_ratio", "")))
    print_info("Last Preset: " + str(getattr(user_prefs, "last_preset", "")))
    input("\nPress Enter to continue...")


def reset_to_default():
    """
    Reset core settings to project defaults (not None, but original values).
    """
    user_prefs = get_preferences()
    user_prefs.__init__()  # Reinitialize to defaults
    user_prefs.save_preferences()
    print_success("Settings reset to default values.")


def change_aspect_ratio():
    """
    Change the current preferred wallpaper aspect ratio.
    """
    user_prefs = get_preferences()
    options = ["16:9", "21:9", "4:3", "3:2", "1:1"]
    print_section("Available Aspect Ratios:")
    for idx, val in enumerate(options, 1):
        print_option(str(idx), val)
    idx_map = {str(i + 1): v for i, v in enumerate(options)}
    choice = get_validated_input(
        "Choose (or 'b' to cancel): ", list(idx_map.keys()) + ["b"]
    )
    if choice != "b":
        value = idx_map[choice]
        user_prefs.aspect_ratio = value
        user_prefs.save_preferences()
        print_success(f"Aspect ratio set to {value}.")
