#!/usr/bin/env python3
"""
Settings management module for AI Wallpaper Generator.

This module centralizes all settings-related functionality for the wallpaper generator application,
including user preferences, preset management, and settings import/export functionality.

Main components:
- UserPreferences class: Core class for managing and persisting user settings
- Preset management: Functions for saving, loading, and deleting configuration presets
- Settings import/export: Functions for backing up and restoring user configuration
- UI management functions: Interactive menus for configuring various settings categories

This module is designed to be imported by the main wallpaper_generator.py script,
providing a clean separation of concerns between generation logic and settings management.
"""

# Standard library imports
import json
import os
import sys
import glob
import random
import logging
import shutil
import re
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple
from pathlib import Path
from textwrap import wrap

# Try to import prompt_generator module
try:
    from prompt_generator import (
        set_prompt_preferences, 
        generate_prompt_gemini, 
        generate_prompt_random, 
        enhance_custom_prompt,
        enforce_prompt_format
    )
    PROMPT_GENERATOR_AVAILABLE = True
except ImportError:
    logging.warning("Could not import prompt_generator module. Some features will be disabled.")
    PROMPT_GENERATOR_AVAILABLE = False

# Try to import Google's GenerativeAI module and AI Style Generator
# Try to import Google's GenerativeAI module first
try:
    import google.generativeai as genai
except ImportError:
    logging.warning("google.generativeai module not found. Some features will be disabled.")
    genai = None

# Separately try to import AI Style Generator
try:
    from ai_style_generator import handle_style_generation, initialize_gemini
    AI_STYLE_GEN_AVAILABLE = True
except ImportError:
    AI_STYLE_GEN_AVAILABLE = False
    logging.warning("Could not import ai_style_generator. AI style generation feature disabled.")

# Local application imports
from wallpaper_config import (
    TEXT_LOGO_INSTRUCTIONS, LOGO_TEMPLATES, TEXT_TEMPLATES,
    TEXT_LOGO_QUALITY_MODIFIERS, TEXT_LOGO_STYLE_MODIFIERS, TEXT_LOGO_BACKGROUND_MODIFIERS,
    STYLE_CATEGORIES # Added STYLE_CATEGORIES
)
from ui_utils import (
    print_header, print_section, print_option, print_success, print_error,
    print_warning, print_info, print_prompt, get_validated_input, show_spinner,
    print_breadcrumb, print_colored
)

# Configuration imports
try:
    from prompt_config import (
        nature_tags, space_tags, sea_tags, flowers_tags, urban_tags,
        fantasy_tags, abstract_tags, mood_tags, available_genres
    )
except ImportError:
    # Fallback if prompt_config.py is not available
    print_warning("Could not import prompt_config.py. Using empty tag lists.")
    nature_tags = []
    space_tags = []
    sea_tags = []
    flowers_tags = []
    urban_tags = []
    fantasy_tags = []
    abstract_tags = []
    mood_tags = []
    available_genres = []

# Global variables
user_prefs = None

# UserPreferences class
class UserPreferences:
    """
    Class to manage user preferences for the wallpaper generator.
    
    This class handles loading, saving, and providing access to user preferences
    including image generation settings, style preferences, and application configuration.
    It maintains persistent storage of settings between application runs.
    
    Attributes:
        preferred_genres (List[str]): List of genres the user prefers for generation
        preferred_styles (List[str]): List of style combinations the user prefers
        preferred_moods (List[str]): List of mood modifiers the user prefers
        negative_prompts (List[str]): List of negative prompts the user prefers
        imagen_settings (Dict): Dictionary of settings for the image generation model
        wallpaper_settings (Dict): Dictionary of settings for wallpaper handling
        history_file (str): Path to the generation history file
        last_preset (str): Name of the last loaded preset, if any
        aspect_ratio (str): The aspect ratio of the wallpaper
    """
    # No predefined style categories as they are not used for prompt generation

    def __init__(self):
        """
        Initialize user preferences with minimal default values.
        
        Sets up the initial state of user preferences with minimal values for required
        settings. This prevents loading all options in the settings menu.
        """
        # Initialize with empty collections
        self.preferred_genres = []
        self.preferred_styles = []
        self.preferred_moods = []
        self.negative_prompts = []
        
        # Minimal default Imagen settings
        self.imagen_settings = {
            "number_of_images": 1,
            "seed": None,
            "negative_prompt": "",
            "quality_settings": {},
            "style_settings": {
                # Don't initialize with style_categories to keep them out of preferences
                "art_movement": None,
                "post_processing": []
            },
            "camera_settings": {},
            "lighting_settings": {},
            "composition_settings": {},
            "environment_settings": {},
            "color_settings": {},
            "detail_settings": {}
        }
        
        # Default wallpaper settings
        self.wallpaper_settings = {
            "auto_set": False,
            "skip_preview": False  # Default to showing preview
        }
        
        # Default aspect ratio
        self.aspect_ratio = "16:9"
        
        # Set history file path
        history_file = "generation_history.json"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.history_file = os.path.join(script_dir, history_file)
        
        # Track last used preset
        self.last_preset = None
        
        # Load existing preferences if available
        self.load_preferences()
    
    def load_preferences(self, filename: str = "user_preferences.json") -> None:
        """
        Load user preferences from a JSON file.
        
        This method attempts to load previously saved user preferences from the
        specified file. If the file exists and contains valid JSON, the attributes
        of this instance are updated with the loaded values. If the file does not
        exist or cannot be parsed, the default values from __init__ are kept.
        
        Args:
            filename (str, optional): Path to the preferences file.
                                     Defaults to "user_preferences.json".
        """
        try:
            # Get the absolute path to the preferences file
            script_dir = os.path.dirname(os.path.abspath(__file__))
            pref_file_path = os.path.join(script_dir, filename)
            
            logging.debug(f"Loading preferences from {pref_file_path}")
            
            if os.path.exists(pref_file_path):
                with open(pref_file_path, "r") as f:
                    data = json.load(f)
                
                # Update fields from loaded data
                if "preferred_genres" in data:
                    self.preferred_genres = list(dict.fromkeys(data["preferred_genres"]))
                if "preferred_styles" in data:
                    self.preferred_styles = list(dict.fromkeys(data["preferred_styles"]))
                if "preferred_moods" in data:
                    self.preferred_moods = list(dict.fromkeys(data["preferred_moods"]))
                if "negative_prompts" in data:
                    self.negative_prompts = data["negative_prompts"]
                if "imagen_settings" in data:
                    # Only update the top level keys that exist in our current settings
                    imagen_data = data["imagen_settings"]
                    for key in self.imagen_settings.keys():
                        if key in imagen_data:
                            self.imagen_settings[key] = imagen_data[key]
                if "wallpaper_settings" in data:
                    # Only update existing keys
                    wallpaper_data = data["wallpaper_settings"]
                    for key in self.wallpaper_settings.keys():
                        if key in wallpaper_data:
                            self.wallpaper_settings[key] = wallpaper_data[key]
                if "history_file" in data:
                    self.history_file = data["history_file"]
                if "last_preset" in data:
                    self.last_preset = data["last_preset"]
                if "aspect_ratio" in data:
                    self.aspect_ratio = data["aspect_ratio"]
                
                logging.debug(f"Preferred genres: {self.preferred_genres}")
                logging.debug(f"Preferred styles: {self.preferred_styles}")
                logging.debug(f"Preferred moods: {self.preferred_moods}")
            else:
                logging.debug(f"No preferences file found at {pref_file_path}, using defaults")
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logging.error(f"Error loading preferences: {e}")
            # Keep default values from __init__
    
    def save_preferences(self, filename: str = "user_preferences.json") -> None:
        """
        Save user preferences to a JSON file.
        
        This method serializes the current user preferences to a JSON file
        for persistence across sessions.
        
        Args:
            filename (str, optional): Path where the preferences should be saved.
                                     Defaults to "user_preferences.json".
        """
        # Get the absolute path to the preferences file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        pref_file_path = os.path.join(script_dir, filename)
        
        try:
            # Clean duplicates before saving
            self.preferred_genres = list(dict.fromkeys(self.preferred_genres))
            self.preferred_styles = list(dict.fromkeys(self.preferred_styles))
            self.preferred_moods = list(dict.fromkeys(self.preferred_moods))
            
            # Prepare data for serialization
            data = {
                "preferred_genres": self.preferred_genres,
                "preferred_styles": self.preferred_styles,
                "preferred_moods": self.preferred_moods,
                "negative_prompts": self.negative_prompts,
                "imagen_settings": self.imagen_settings,
                "wallpaper_settings": self.wallpaper_settings,
                "history_file": self.history_file,
                "last_preset": self.last_preset,
                "aspect_ratio": self.aspect_ratio
            }
            
            # Write to file
            with open(pref_file_path, "w") as f:
                json.dump(data, f, indent=4)
            
            logging.debug(f"Saved preferences to {pref_file_path}")
            logging.debug(f"Preferred genres: {self.preferred_genres}")
            logging.debug(f"Preferred styles: {self.preferred_styles}")
            logging.debug(f"Preferred moods: {self.preferred_moods}")
            
            # Reload preferences after saving to update in-memory state
            self.load_preferences(filename)
        except (IOError, OSError) as e:
            logging.error(f"Error saving preferences: {e}")


    def add_style(self, style: str):
        """Set preferred_styles to contain only the given style."""
        if style:
            self.preferred_styles = [style]
            self.save_preferences()

    def add_genre(self, genre: str):
        """Set preferred_genres to contain only the given genre."""
        if genre:
            self.preferred_genres = [genre]
            self.save_preferences()

    def add_mood(self, mood: str):
        """Set preferred_moods to contain only the given mood."""
        if mood:
            self.preferred_moods = [mood]
            self.save_preferences()

# Interface functions
def initialize_settings() -> 'UserPreferences':
    """
    Initialize and return the user preferences object.
    
    This function creates a UserPreferences instance, loads saved preferences
    from disk if available, and returns the initialized object. It also sets
    the global user_prefs variable for module-level access.
    
    Returns:
        UserPreferences: The initialized user preferences object
    """
    global user_prefs
    user_prefs = UserPreferences()

    return user_prefs

def get_preferences() -> 'UserPreferences':
    """
    Get the current user preferences object.
    
    This function returns the global user preferences object. If it hasn't been
    initialized yet, it calls initialize_settings() first.
    
    Returns:
        UserPreferences: The current user preferences object
    """
    return user_prefs

# Helper functions for menus
def print_menu_options(options: List[Tuple[str, str]]) -> None:
    """
    Print menu options given a list of (key, description) tuples.

    Args:
        options: List of tuples where each tuple is (key, description)
    """
    for key, description in options:
        print_option(key, description)

def get_menu_choice(prompt: str, valid_choices: List[str], allow_empty: bool = False) -> str:
    """
    Get a validated menu choice from the user.

    Args:
        prompt: The prompt to display to the user
        valid_choices: List of valid input choices
        allow_empty: Whether to allow empty input (default False)

    Returns:
        The user's validated choice as a string
    """
    return get_validated_input(prompt, valid_choices, allow_empty=allow_empty)


def load_last_genre(filename: str = "last_genre.json") -> Optional[str]:
    """
    Load the most recently used genre from a file.
    
    Args:
        filename (str, optional): Path to the file storing the last genre. 
                                 Defaults to "last_genre.json".
    
    Returns:
        Optional[str]: The last used genre, or None if the file doesn't exist or is invalid
    """
    try:
        # Get the absolute path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(script_dir, filename)
        
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                return json.load(f).get("last_genre")
    except (FileNotFoundError, json.JSONDecodeError, IOError) as e:
        logging.error(f"Error loading last genre from {filepath}: {e}")
    return None

def save_last_genre(genre: str, filename: str = "last_genre.json") -> None:
    """
    Save the most recently used genre to a file.
    
    Args:
        genre (str): The genre to save
        filename (str, optional): Path to the file to save the genre to. 
                                 Defaults to "last_genre.json".
    """
    try:
        # Get the absolute path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(script_dir, filename)
        
        with open(filepath, "w") as f:
            json.dump({"last_genre": genre}, f, indent=2)
    except Exception as e:
        logging.error(f"Error saving last genre to {filepath}: {e}")

def generate_random_style_mix() -> str:
    """
    Generate a random mix of artistic styles.

    This function combines styles from different categories to create unique
    style combinations for image generation prompts.

    Returns:
        str: A string containing a combination of artistic styles, joined with " + "
    """
    # Use the imported style categories
    style_categories = STYLE_CATEGORIES

    # Select a random category
    category = random.choice(list(style_categories.keys()))

    # Select 2-3 compatible styles from the same category
    available_styles = style_categories[category]
    num_styles = min(random.randint(2, 3), len(available_styles))
    selected_styles = random.sample(available_styles, num_styles)

    return " + ".join(selected_styles)

# Settings management functions will be implemented here
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
        choice: str = get_menu_choice(f"Select option (1-{len(menu_options)}, b)", [key for key, _ in menu_options] + ["b"])
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

def manage_presets():
    """
    Display and manage preset settings through an interactive menu.
    
    This function provides a user interface for creating, loading, and deleting
    presets. Presets allow users to save and restore specific configurations
    for different use cases.
    """
    global user_prefs
    while True:
        print_section("Manage Presets")
        
        # Show current preset if one is loaded
        current_preset = getattr(user_prefs, 'last_preset', None)
        if current_preset:
            print_info(f"Current Preset: {current_preset}")
        print()
        
        menu_options: List[Tuple[str, str]] = [
            ("1", "Save Current Settings as Preset"),
            ("2", "Load Preset"),
            ("3", "Delete Preset"),
            ("4", "View Current Preset Details"),
            ("b", "Back")
        ]
        print_menu_options(menu_options)
        
        choice = get_menu_choice(f"Select option (1-4, b)", [key for key, _ in menu_options])
        
        if choice == "b":
            return

        handlers = {
            "1": save_current_preset,
            "2": handle_load_preset,
            "3": handle_delete_preset,
            "4": view_preset_details
        }

        if choice in handlers:
            handlers[choice]()

def save_current_preset():
    """Helper function to handle saving current settings as preset."""
    preset_name = get_validated_input("Enter preset name (or 'b' to go back)", allow_empty=False)
    if preset_name.lower() == 'b':
        return

    # Validate preset name
    if not preset_name.strip() or any(c in r'\/:*?"<>|' for c in preset_name):
        print_error("Invalid preset name. Please avoid special characters.")
        return

    # Check if preset already exists
    if os.path.exists(os.path.join("presets", f"{preset_name}.json")):
        confirm = get_validated_input(f"Preset '{preset_name}' already exists. Overwrite? (y/n)", ["y", "n"])
        if confirm.lower() != "y":
            return

    try:
        # Collect current settings
        current_settings = {
            "imagen_settings": user_prefs.imagen_settings if hasattr(user_prefs, 'imagen_settings') else {},
            "wallpaper_settings": user_prefs.wallpaper_settings if hasattr(user_prefs, 'wallpaper_settings') else {},
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "description": "User preset"
            }
        }

        # Save the preset
        if save_preset(current_settings, preset_name):
            print_success(f"Preset '{preset_name}' saved successfully")
            user_prefs.last_preset = preset_name
            user_prefs.save_preferences()
        else:
            print_error("Failed to save preset")

    except Exception as e:
        print_error(f"Error preparing preset data: {e}")

def handle_load_preset():
    """Helper function to handle loading a preset."""
    result = load_preset()
    if not result:
        return

    settings, preset_name = result  # Unpack the returned tuple
    try:
        print_section("Load Settings")
        load_options: List[str] = ["Replace current settings with preset", "Merge preset with current settings"]
        print_menu_options([(str(i+1), option) for i, option in enumerate(load_options)])
        valid_choices = ["b"] + [str(i+1) for i in range(len(load_options))]
        load_choice: str = get_menu_choice(f"Select option (1-{len(load_options)}, b)", valid_choices)
        if load_choice == "_INTERRUPTED_":
            return # Exit preset loading if interrupted

        if load_choice == "b":
            return

        if load_choice == "1":  # Replace
            _apply_preset_settings(settings, replace=True)
            print_success("Settings replaced with preset")
        elif load_choice == "2":  # Merge
            _apply_preset_settings(settings, replace=False)
            print_success("Settings merged with preset")

        user_prefs.last_preset = preset_name
        user_prefs.save_preferences()

    except Exception as e:
        print_error(f"Error applying preset settings: {e}")

def _apply_preset_settings(settings: Dict[str, Any], replace: bool = True) -> bool:
    """
    Helper function to apply preset settings.

    Args:
        settings: Dictionary containing settings to apply
        replace: If True, replace existing settings; if False, merge with existing

    Returns:
        bool: True if settings were applied successfully, False otherwise
    """
    try:
        # Define default structure for essential settings
        default_imagen_structure = {
            "number_of_images": 1,
            "seed": None,
            "negative_prompt": "",
            "quality_settings": {},
            "style_settings": {},
            "camera_settings": {},
            "lighting_settings": {},
            "composition_settings": {},
            "environment_settings": {},
            "color_settings": {},
            "detail_settings": {}
        }
        default_wallpaper_structure = {
             "auto_set": False,
             "skip_preview": False
        }

        # Apply imagen_settings and wallpaper_settings
        for setting_type, default_structure in [('imagen_settings', default_imagen_structure), ('wallpaper_settings', default_wallpaper_structure)]:
            if hasattr(user_prefs, setting_type):
                current_settings_dict = getattr(user_prefs, setting_type)
                # Ensure current settings have the default structure
                # Use setdefault to add missing keys without overwriting existing ones
                for key, default_value in default_structure.items():
                    current_settings_dict.setdefault(key, default_value)

                if setting_type in settings:
                    preset_settings_dict = settings[setting_type]
                    if isinstance(preset_settings_dict, dict):
                        if replace:
                            # Start with defaults, then update with preset
                            new_settings = default_structure.copy()
                            new_settings.update(preset_settings_dict)
                            setattr(user_prefs, setting_type, new_settings)
                        else:
                            # Merge preset into current (which already has defaults)
                            def deep_update(d, u):
                                for k, v in u.items():
                                    if isinstance(v, dict):
                                        # Ensure the key exists in d before recursing
                                        # Use get(k, {}) to handle potentially missing keys in d during recursion
                                        d[k] = deep_update(d.get(k, {}), v)
                                    else:
                                        d[k] = v
                                return d
                            deep_update(current_settings_dict, preset_settings_dict)
                    else: # Preset value is not a dict, log warning
                         logging.warning(f"Preset value for {setting_type} is not a dictionary. Skipping.")
                # If setting_type not in preset, current_settings_dict (with defaults) remains unchanged


        # Explicitly apply top-level styles and moods (always replace for these)
        if "styles" in settings and isinstance(settings["styles"], list):
            user_prefs.preferred_styles = settings["styles"][:] # Replace with a copy
        if "moods" in settings and isinstance(settings["moods"], list):
            user_prefs.preferred_moods = settings["moods"][:] # Replace with a copy

        # Apply aspect ratio if present
        if "aspect_ratio" in settings:
             user_prefs.aspect_ratio = settings["aspect_ratio"]

        # Apply negative prompts if present
        if "negative_prompts" in settings and isinstance(settings["negative_prompts"], list):
             if replace:
                 user_prefs.negative_prompts = settings["negative_prompts"][:]
             else: # Merge mode for negative prompts could append unique ones
                 existing_neg = set(user_prefs.negative_prompts)
                 new_neg = set(settings["negative_prompts"])
                 user_prefs.negative_prompts = list(existing_neg.union(new_neg))

        # Apply preferred genres if present
        if "preferred_genres" in settings and isinstance(settings["preferred_genres"], list):
             if replace:
                 user_prefs.preferred_genres = settings["preferred_genres"][:]
             else: # Merge mode for genres could append unique ones
                 existing_genres = set(user_prefs.preferred_genres)
                 new_genres = set(settings["preferred_genres"])
                 user_prefs.preferred_genres = list(existing_genres.union(new_genres))

        # Note: wallpaper_settings are handled in the loop above
        # Note: history_file and last_preset are managed elsewhere, not applied from preset file

        return True # Indicate success

    except Exception as e:
        logging.error(f"Error applying preset settings: {e}")
        return False # Indicate failure

def handle_delete_preset():
    """Helper function to handle deleting a preset."""
    current_preset = getattr(user_prefs, 'last_preset', None)
    if delete_preset():
        if current_preset and not os.path.exists(os.path.join("presets", f"{current_preset}.json")):
            user_prefs.last_preset = None
            user_prefs.save_preferences()

def _display_settings_section(settings: Dict[str, Any], section: str, title: str, indent: int = 0) -> None:
    """
    Helper function to display a section of settings recursively.
    
    Args:
        settings: Dictionary containing settings
        section: Name of the section to display
        title: Title to display for the section
        indent: Current indentation level (default: 0)
    """
    if section not in settings:
        return
        
    data = settings[section]
    print_info(f"\n{'  ' * indent}{title}:")
    
    if not isinstance(data, dict):
        print_info(f"{'  ' * (indent + 1)}{data}")
        return
        
    for key, value in data.items():
        if isinstance(value, dict):
            _display_settings_section({key: value}, key, key, indent + 1)
        else:
            print_info(f"{'  ' * (indent + 1)}{key}: {value}")

def view_preset_details():
    """Helper function to view current preset details."""
    current_preset = getattr(user_prefs, 'last_preset', None)
    if not current_preset:
        print_warning("No preset currently loaded")
        input("\nPress Enter to continue...")
        return

    try:
        preset_file = os.path.join("presets", f"{current_preset}.json")
        if not os.path.exists(preset_file):
            print_error(f"Preset file not found: {preset_file}")
            return

        with open(preset_file) as f:
            settings = json.load(f)

        # Display preset information
        print_section(f"Current Preset: {current_preset}")
        _display_settings_section(settings, "metadata", "Metadata")
        _display_settings_section(settings, "imagen_settings", "Imagen Settings")
        _display_settings_section(settings, "wallpaper_settings", "Wallpaper Settings")
        
        input("\nPress Enter to continue...")
    except Exception as e:
        print_error(f"Error reading preset details: {e}")

def load_preset() -> Optional[Tuple[Dict[str, Any], str]]:
    """
    Load a preset from a file.
    
    Returns:
        Optional[Tuple[Dict[str, Any], str]]: A tuple of (settings, preset_name) if successful,
        None if no presets found or user cancels
    """
    try:
        # Ensure presets directory exists
        os.makedirs("presets", exist_ok=True)
        
        # Get list of presets
        presets = [f for f in os.listdir("presets") if f.endswith(".json")]
        if not presets:
            print_warning("No saved presets found")
            return None

        # Show preset options
        print_section("Available Presets")
        for i, preset in enumerate(presets, 1):
            print_option(str(i), preset.replace(".json", ""))
        print_option("b", "Back")

        # Get user choice
        valid_choices = ["b"] + [str(i) for i in range(1, len(presets) + 1)]
        choice = get_validated_input("Select preset to load", valid_choices)
        if choice == "b":
            return None

        # Load selected preset
        preset_file = presets[int(choice) - 1]
        preset_path = os.path.join("presets", preset_file)
        preset_name = os.path.splitext(preset_file)[0]

        with open(preset_path) as f:
            settings = json.load(f)
        
        return settings, preset_name

    except Exception as e:
        print_error(f"Error loading preset: {e}")
        return None

def save_preset(settings: Dict[str, Any], name: str) -> bool:
    """
    Save the current settings as a preset.
    
    This function takes the current settings and saves them to a file in the
    presets directory with the given name, using a temporary file and atomic
    rename for safety.
    
    Args:
        settings: Dictionary containing settings to save
        name: Name to give the preset
    
    Returns:
        bool: True if preset was successfully saved, False otherwise
    
    Raises:
        ValueError: If preset name is empty or contains invalid characters
    """
    if not name or not name.strip():
        raise ValueError("Preset name cannot be empty")
    
    try:
        # Ensure presets directory exists
        os.makedirs("presets", exist_ok=True)

        # Set up file paths
        filename = f"{name}.json"
        temp_file = os.path.join("presets", f"{filename}.tmp")
        final_file = os.path.join("presets", filename)
        backup_file = os.path.join("presets", f"{filename}.bak")
        
        print_info(f"Saving preset to {final_file}")
        
        # Write settings to temporary file
        with open(temp_file, "w") as f:
            json.dump(settings, f, indent=4)
            f.flush()
            os.fsync(f.fileno())  # Ensure data is written to disk
        
        # Backup existing preset if it exists
        if os.path.exists(final_file):
            if os.path.exists(backup_file):
                os.remove(backup_file)
            os.rename(final_file, backup_file)
            print_info("Created backup of existing preset")
        
        # Atomically rename temporary file to final name
        os.rename(temp_file, final_file)
        print_info("Preset saved successfully")
        return True
        
    except Exception as e:
        print_error(f"Error saving preset: {e}")
        # Clean up temporary file if it exists
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass
        return False

def delete_preset() -> bool:
    """
    Delete a preset file.
    
    Displays available presets and allows user to select one for deletion.
    Creates a backup before deletion and handles errors gracefully.
    
    Returns:
        bool: True if preset was successfully deleted, False otherwise
    """
    try:
        # Ensure presets directory exists
        os.makedirs("presets", exist_ok=True)

        # Get list of presets
        presets = [f for f in os.listdir("presets") if f.endswith(".json")]
        if not presets:
            print_warning("No saved presets found")
            return False

        # Display preset options
        print_section("Available Presets")
        for i, preset in enumerate(presets, 1):
            print_option(str(i), preset.replace(".json", ""))
        print_option("b", "Back")

        # Get user choice
        valid_choices = ["b"] + [str(i) for i in range(1, len(presets) + 1)]
        choice = get_validated_input("Select preset to delete", valid_choices)
        if choice == "b":
            return False

        # Get preset file paths
        preset_file = presets[int(choice) - 1]
        preset_path = os.path.join("presets", preset_file)
        backup_path = os.path.join("presets", f"{preset_file}.bak")
        preset_name = os.path.splitext(preset_file)[0]

        # Confirm deletion
        confirm = get_validated_input(
            f"Are you sure you want to delete preset '{preset_name}'? (y/n)",
            ["y", "n"]
        )
        if confirm.lower() != "y":
            print_info("Deletion cancelled")
            return False

        # Create backup and delete file
        shutil.copy2(preset_path, backup_path)
        os.remove(preset_path)
        print_success(f"Preset '{preset_name}' deleted (backup created)")
        return True

    except Exception as e:
        print_error(f"Error in delete_preset: {e}")
        # Try to restore from backup if it exists
        if 'backup_path' in locals() and 'preset_path' in locals():
            if os.path.exists(backup_path) and not os.path.exists(preset_path):
                try:
                    shutil.move(backup_path, preset_path)
                    print_info("Restored preset from backup after error")
                except Exception:
                    pass
        return False

# Settings import/export functions will be implemented here 
def export_settings(user_prefs=None) -> str:
    """
    Export user settings to a JSON file.
    
    Creates a temporary file and uses atomic rename for safety.
    Includes backup handling if a file with the same name exists.
    
    Args:
        user_prefs: Optional UserPreferences object. If not provided, uses global user_prefs.
        
    Returns:
        str: The path to the exported settings file, or empty string if export failed
    """
    try:
        # Get user preferences object
        if user_prefs is None:
            user_prefs = globals().get('user_prefs')
            if user_prefs is None:
                print_error("No user preferences object available")
                return ""

        # Create exports directory if it doesn't exist
        os.makedirs("exports", exist_ok=True)

        # Get filename from user
        print_section("Export Settings")
        filename = get_validated_input("Enter filename for export (without extension)", allow_empty=False)
        if not filename:
            return ""

        # Set up file paths
        final_path = os.path.join("exports", f"{filename}.json")
        temp_path = os.path.join("exports", f"{filename}.json.tmp")
        backup_path = os.path.join("exports", f"{filename}.json.bak")

        # Prepare settings data
        settings = {
            "preferences": user_prefs.__dict__,
            "imagen_settings": user_prefs.imagen_settings,
            "export_date": datetime.now().isoformat(),
            "version": "1.0"  # Add version for future compatibility
        }

        # Write to temporary file first
        with open(temp_path, "w") as f:
            json.dump(settings, f, indent=4)
            f.flush()
            os.fsync(f.fileno())

        # Backup existing file if it exists
        if os.path.exists(final_path):
            if os.path.exists(backup_path):
                os.remove(backup_path)
            shutil.copy2(final_path, backup_path)
            print_info(f"Created backup of existing file: {backup_path}")

        # Atomic rename to final filename
        os.replace(temp_path, final_path)
        print_success(f"Settings exported to {final_path}")
        return final_path

    except Exception as e:
        print_error(f"Error exporting settings: {e}")
        if 'temp_path' in locals() and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
        return ""

def import_settings() -> bool:
    """
    Import user settings from a JSON file.
    
    This function loads user preferences and imagen settings from a previously
    exported JSON file and applies them to the current user preferences.
    Creates a backup of current settings before import and supports rollback
    on failure.
    
    Returns:
        bool: True if settings were successfully imported, False otherwise
    """
    try:
        global user_prefs
        if user_prefs is None:
            print_error("No user preferences object available")
            return False

        # Create backup of current settings
        backup_settings = {
            "preferences": user_prefs.__dict__.copy(),
            "imagen_settings": user_prefs.imagen_settings.copy(),
            "backup_date": datetime.now().isoformat()
        }

        # Ensure exports directory exists
        os.makedirs("exports", exist_ok=True)

        # List available export files
        print_section("Import Settings")
        exports = [f for f in os.listdir("exports") if f.endswith(".json") and not f.endswith((".tmp", ".bak"))]
        
        if not exports:
            print_warning("No exported settings files found in exports directory")
            return False

        # Display available exports
        for i, export in enumerate(exports, 1):
            print_option(str(i), export)
        print_option("b", "Back")

        # Get user choice
        valid_choices = ["b"] + [str(i) for i in range(1, len(exports) + 1)]
        choice = get_validated_input("Select settings file to import", valid_choices)
        if choice == "b":
            return False

        # Load and validate selected file
        import_file = exports[int(choice) - 1]
        import_path = os.path.join("exports", import_file)
        
        with open(import_path) as f:
            settings = json.load(f)

        # Validate settings structure
        required_keys = {"preferences", "imagen_settings"}
        if not all(key in settings for key in required_keys):
            print_error("Invalid settings file format")
            return False

        # Ask user about import mode
        print_section("Import Mode")
        print_option("1", "Replace all current settings")
        print_option("2", "Merge with current settings")
        print_option("b", "Back")

        mode = get_validated_input("Select import mode", ["1", "2", "b"])
        if mode == "_INTERRUPTED_":
            return False # Indicate cancellation
        if mode == "b":
            return False

        # Apply settings based on mode
        try:
            if mode == "1":  # Replace
                user_prefs.__dict__.update(settings["preferences"])
                user_prefs.imagen_settings = settings["imagen_settings"]
            else:  # Merge
                user_prefs.__dict__.update(settings["preferences"])
                user_prefs.imagen_settings.update(settings["imagen_settings"])

            # Save the imported settings
            user_prefs.save_preferences()
            print_success("Settings imported successfully")
            return True

        except Exception as e:
            print_error(f"Error applying settings: {e}")
            # Restore from backup
            user_prefs.__dict__.update(backup_settings["preferences"])
            user_prefs.imagen_settings = backup_settings["imagen_settings"]
            user_prefs.save_preferences()
            print_info("Settings restored from backup after import failure")
            return False

    except Exception as e:
        print_error(f"Error during import: {e}")
        return False

def get_generated_image_path(prompt: str) -> str:
    """
    Generate a file path for an image based on its prompt.
    
    This function creates a sanitized filename from the image prompt and
    generates a unique hash to ensure filenames are both descriptive and unique.
    
    Args:
        prompt (str): The prompt used to generate the image
    
    Returns:
        str: The file path where the generated image should be saved
    """
    # Create a simple filename from the prompt
    # Remove special characters and replace spaces with underscores
    sanitized = re.sub(r'[^\w\s-]', '', prompt.lower())
    sanitized = re.sub(r'[-\s]+', '_', sanitized)
    
    # Truncate to the maximum length (30 characters)
    if len(sanitized) > 30:
        # Try to cut at a word boundary
        sanitized = sanitized[:30].rsplit('_', 1)[0]
    
    # Add a unique identifier (first 8 chars of the hash)
    hash_object = hashlib.sha256(prompt.encode())
    short_hash = hash_object.hexdigest()[:8]
    
    filename = f"{sanitized}_{short_hash}.png"
    
    # Ensure the genimage directory exists with absolute path
    genimage_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "genimage")
    try:
        os.makedirs(genimage_dir, exist_ok=True)
    except Exception as e:
        logging.error(f"Error creating genimage directory: {e}")
    
    return os.path.join(genimage_dir, filename)

def update_history_with_filenames(silent: bool = False) -> None:
    """
    Update the generation history with filenames for each entry.
    
    This function processes the generation history file, adds a filename
    field to each entry based on its prompt, and saves the updated history.
    This is useful when migrating from older versions that didn't store filenames.
    
    Args:
        silent (bool, optional): If True, suppresses output messages. Defaults to False.
    """
    try:
        history_file = "generation_history.json"
        # Get the absolute path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        history_filepath = os.path.join(script_dir, history_file)
        
        if os.path.exists(history_filepath):
            with open(history_filepath, "r") as f:
                history = json.load(f)
            
            updated = False
            for entry in history:
                if "image_filename" not in entry and entry.get("enhanced_prompt"):
                    image_path = get_generated_image_path(entry["enhanced_prompt"])
                    if os.path.exists(image_path) or True:  # Include even if file doesn't exist
                        entry["image_filename"] = os.path.basename(image_path)
                        updated = True
            
            if updated:
                with open(history_filepath, "w") as f:
                    json.dump(history, f, indent=4)
                if not silent:
                    print_info("Generation history updated with image filenames")
    except Exception as e:
        logging.error(f"Error updating history with filenames: {e}")

def manage_imagen_settings():
    """Manage Imagen 3 specific settings like number of images, seed, etc."""
    while True:
        print_section("Imagen 3 Settings")
        print_option("1", "Number of Images")
        print_option("2", "Set Specific Seed")
        print_option("3", "Model Version")
        print_option("4", "View Current Settings")
        print_option("5", "Reset to Defaults")
        print_option("b", "Back")
        
        choice = get_validated_input("Select an option (1-5, b)", ["1", "2", "3", "4", "5", "b"])
        
        if choice == "b":
            return
        
        if choice == "1":
            print_section("Number of Images")
            print_info(f"Current setting: {user_prefs.imagen_settings.get('number_of_images', 1)}")
            print_option("1", "1 image")
            print_option("2", "2 images")
            print_option("3", "3 images")
            print_option("4", "4 images")
            print_option("b", "Back")
            
            num_choice = get_validated_input("Select number of images (1-4, b)", ["1", "2", "3", "4", "b"])
            if num_choice == "_INTERRUPTED_":
                continue
            if num_choice == "b":
                continue
            user_prefs.imagen_settings["number_of_images"] = int(num_choice)
            print_success(f"Number of images set to {num_choice}")
            user_prefs.save_preferences()
            
        elif choice == "2":
            print_section("Set Specific Seed")
            print_info(f"Current seed: {user_prefs.imagen_settings.get('seed') or 'Random (None)'}")
            print_info("Setting a specific seed allows you to reproduce the same image style.")
            print_option("1", "Use Random Seed (None)")
            print_option("2", "Set Specific Seed")
            print_option("b", "Back")
            
            seed_choice = get_validated_input("Select option (1-2, b)", ["1", "2", "b"])
            if seed_choice == "_INTERRUPTED_":
                continue
            
            if seed_choice == "b":
                continue
            elif seed_choice == "1":
                user_prefs.imagen_settings["seed"] = None
                print_success("Seed set to Random (None)")
                user_prefs.save_preferences()
            else:
                try:
                    new_seed = input("Enter seed (integer number): ").strip()
                    if new_seed:
                        user_prefs.imagen_settings["seed"] = int(new_seed)
                        print_success(f"Seed set to {new_seed}")
                    else:
                        user_prefs.imagen_settings["seed"] = None
                        print_success("Seed set to Random (None)")
                    user_prefs.save_preferences()
                except ValueError:
                    print_error("Invalid seed value. Please enter a valid integer.")
            
        elif choice == "3":
            print_section("Model Version")
            print_info("Select Imagen model version:")
            print_option("1", "imagen-3.0-generate-002 (Default)")
            print_option("2", "imagen-3.0-generate-001 (Legacy)")
            print_option("b", "Back")
            
            model_choice = get_validated_input("Select model version (1-2, b)", ["1", "2", "b"])
            if model_choice == "_INTERRUPTED_":
                continue
            if model_choice == "b":
                continue
            models = {
                "1": "imagen-3.0-generate-002",
                "2": "imagen-3.0-generate-001"
            }
            
            user_prefs.imagen_settings["model_version"] = models[model_choice]
            print_success(f"Model version set to {models[model_choice]}")
            user_prefs.save_preferences()
            
        elif choice == "4":
            print_section("Current Settings")
            print_info(f"Number of Images: {user_prefs.imagen_settings.get('number_of_images', 1)}")
            print_info(f"Seed: {user_prefs.imagen_settings.get('seed') or 'Random (None)'}")
            print_info(f"Model Version: {user_prefs.imagen_settings.get('model_version', 'imagen-3.0-generate-002')}")
            print_info(f"Negative Prompt: {user_prefs.imagen_settings.get('negative_prompt', '') or 'None'}")
            print_info(f"Aspect Ratio: {user_prefs.aspect_ratio}")
            
            print("\nPress Enter to continue...")
            input()
            
        elif choice == "5":
            print_section("Reset to Defaults")
            confirm = get_validated_input("Are you sure you want to reset Imagen settings to defaults? (y/n)", ["y", "n"])
            
            if confirm.lower() == "y":
                # Reset only specific imagen settings, not all settings
                user_prefs.imagen_settings["number_of_images"] = 1
                user_prefs.imagen_settings["seed"] = None
                user_prefs.imagen_settings["model_version"] = "imagen-3.0-generate-002"
                user_prefs.imagen_settings["negative_prompt"] = ""
                user_prefs.aspect_ratio = "16:9"
                
                user_prefs.save_preferences()
                print_success("Imagen settings reset to defaults")

def manage_genres():
    """Manage user's preferred genres for wallpaper generation."""
    while True:
        print_header("Manage Genres")
        print_section("Current Preferred Genres")
        
        if not user_prefs.preferred_genres:
            print_info("No preferred genres set yet.")
        else:
            for i, genre in enumerate(user_prefs.preferred_genres, 1):
                print_option(str(i), genre)
        
        print_section("Available Genres")
        for i, genre in enumerate(available_genres, 1):
            print_option(str(i), genre)
        
        print_section("Options")
        print_option("1", "Add genre")
        print_option("2", "Remove genre")
        print_option("3", "Clear all genres")
        print_option("b", "Back")
        
        choice = get_validated_input("\nEnter your choice (1-3, b): ", ["1", "2", "3", "b"])
        if choice == "_INTERRUPTED_":
            return # Exit genre management

        if choice == "b":
            return
            
        if choice == "1":
            print_prompt("\nEnter the number of the genre to add (or 'b' to go back): ")
            genre_choice = input().strip().lower()
            
            if genre_choice == 'b':
                continue
            
            try:
                genre_index = int(genre_choice) - 1
                if 0 <= genre_index < len(available_genres):
                    genre = available_genres[genre_index]
                    if genre not in user_prefs.preferred_genres:
                        user_prefs.add_genre(genre)
                        print_success(f"\nAdded '{genre}' to preferred genres.")
                    else:
                        print_warning(f"\n'{genre}' is already in your preferred genres.")
                else:
                    print_error("\nInvalid genre number.")
            except ValueError:
                print_error("\nPlease enter a valid number.")
        
        elif choice == "2":
            if not user_prefs.preferred_genres:
                print_warning("\nNo genres to remove.")
                continue
            
            print_prompt("\nEnter the number of the genre to remove (or 'b' to go back): ")
            genre_choice = input().strip().lower()
            
            if genre_choice == 'b':
                continue
            
            try:
                genre_index = int(genre_choice) - 1
                if 0 <= genre_index < len(user_prefs.preferred_genres):
                    removed_genre = user_prefs.preferred_genres.pop(genre_index)
                    user_prefs.save_preferences()
                    print_success(f"\nRemoved '{removed_genre}' from preferred genres.")
                else:
                    print_error("\nInvalid genre number.")
            except ValueError:
                print_error("\nPlease enter a valid number.")
        
        elif choice == "3":
            if not user_prefs.preferred_genres:
                print_warning("\nNo genres to clear.")
                continue
            
            print_warning("\nAre you sure you want to clear all preferred genres? (y/n): ")
            if input().strip().lower() == 'y':
                user_prefs.preferred_genres.clear()
                user_prefs.save_preferences()
                print_success("\nCleared all preferred genres.")

def manage_styles():
    """Manage user's preferred styles for wallpaper generation."""
    while True:
        try:
            print_section("Manage Styles")
            print_info("Current preferred styles:")
            for style in user_prefs.preferred_styles:
                print_info(f"- {style}")

            print_info("\nAvailable styles (by category):")
            all_styles = []
            for category, styles in STYLE_CATEGORIES.items():
                print_info(f"\n  {category}:")
                print_info("    " + ", ".join(styles))
                all_styles.extend(styles)  # Collect all styles for validation later

            print_section("Options")
            print_option("rand", "Random Style Mix (combines 2-3 compatible styles)")
            print_option("ai", "AI-Generated Style")
            print_option("custom", "Custom Style")
            print_option("a", "Add style (type name)")
            print_option("r", "Remove style (type name)")
            print_option("c", "Clear all")
            print_option("b", "Back")

            valid_choices = ["a", "r", "c", "b", "rand", "ai", "custom"]  # Use string options
            style_choice = get_validated_input(
                "Select an option (or type a style name to add/remove)",
                valid_choices,
                allow_empty=True,
            )  # Allow typing style name

            if style_choice == "_INTERRUPTED_":
                return  # Exit style management

            # Handle direct style name input for adding
            if style_choice and style_choice not in valid_choices:
                style_name_input = style_choice  # User typed a style name directly
                if style_name_input in all_styles:  # Check if it's a known style
                    if style_name_input not in user_prefs.preferred_styles:
                        user_prefs.add_style(style_name_input)
                        print_success(f"Added '{style_name_input}' to preferred styles")
                    else:
                        print_warning(f"'{style_name_input}' is already in your preferred styles")
                else:
                    print_warning(
                        f"Unknown style: '{style_name_input}'. Use 'a' to add a custom style."
                    )
                continue  # Continue the loop after handling direct input

            # Handle letter/special options
            if style_choice == "b":
                return
            elif style_choice == "a":
                style = input("Enter style to add: ").strip()
                if style:
                    if style not in user_prefs.preferred_styles:
                        user_prefs.add_style(style)
                        print_success(f"Added '{style}' to preferred styles")
                    else:
                        print_warning(f"'{style}' is already in your preferred styles")
            elif style_choice == "r":
                if not user_prefs.preferred_styles:
                    print_warning("You don't have any preferred styles to remove")
                    continue

                print_info("Current preferred styles:")
                for i, style in enumerate(user_prefs.preferred_styles, 1):
                    print_option(str(i), style)

                remove_choice = get_validated_input(
                    "Select style number to remove (or 'c' to cancel)",
                    [str(i) for i in range(1, len(user_prefs.preferred_styles) + 1)]
                    + ["c"],
                )

                if remove_choice == "c":
                    continue

                style_to_remove = user_prefs.preferred_styles[int(remove_choice) - 1]
                user_prefs.preferred_styles.remove(style_to_remove)
                user_prefs.save_preferences()
                print_success(f"Removed '{style_to_remove}' from preferred styles")
            elif style_choice == "c":
                confirm = get_validated_input(
                    "Are you sure you want to clear all styles? (y/n)", ["y", "n"]
                )
                if confirm == "y":
                    user_prefs.preferred_styles.clear()
                    user_prefs.save_preferences()
                    print_success("Cleared all preferred styles")
            elif style_choice == "rand":
                # Random style mix option
                style_mix = generate_random_style_mix()
                print_info(f"Generated random style mix: {style_mix}")
                add_to_preferences = get_validated_input(
                    "Add this mix to your preferred styles? (y/n)", ["y", "n"]
                )
                if add_to_preferences == "y":
                    if style_mix not in user_prefs.preferred_styles:
                        user_prefs.add_style(style_mix)
                        print_success(f"Added '{style_mix}' to preferred styles")
                    else:
                        print_warning(f"'{style_mix}' is already in your preferred styles")
            elif style_choice == "ai":
                # AI-Generated Style option
                try:
                    from ai_style_generator import handle_style_generation, initialize_gemini

                    if "GEMINI_API_KEY" in os.environ:
                        initialize_gemini(os.environ["GEMINI_API_KEY"])
                        handle_style_generation(user_prefs)
                    else:
                        print_error(
                            "Gemini API key not found. Please set GEMINI_API_KEY environment variable."
                        )
                except ImportError:
                    print_error(
                        "AI style generation requires google-generativeai package."
                    )
                    print_info("Install with: pip install google-generativeai")
                continue  # Stay in the style management menu
            elif style_choice == "custom":
                # Custom style option
                print_info(
                    "Enter your custom style (e.g., 'mix of water colour and pastel paint')"
                )
                custom_style = input().strip()
                if custom_style:
                    if custom_style not in user_prefs.preferred_styles:
                        user_prefs.add_style(custom_style)
                        print_success(f"Added custom style: {custom_style}")
                    else:
                        print_warning(
                            f"'{custom_style}' is already in your preferred styles"
                        )
        except Exception as e:
            print_error(f"An error occurred: {e}")
            return

def manage_moods():
    """Manage user's preferred moods for wallpaper generation."""
    while True:
        print_section("Manage Moods")
        print_info("Current preferred moods:")
        for mood in user_prefs.preferred_moods:
            print_info(f"- {mood}")
        
        print_info("\nAvailable moods:")
        mood_options = ["peaceful", "dramatic", "mysterious", "energetic", "melancholic",
                      "joyful", "romantic", "eerie", "nostalgic", "contemplative"]
        for i, mood in enumerate(mood_options, 1):
            print_option(str(i), mood)
        
        print_option("b", "Back")
        
        action = get_validated_input(f"Select mood (1-{len(mood_options)}, b)", ["b"] + [str(i) for i in range(1, len(mood_options) + 1)])
        if action == "_INTERRUPTED_":
            continue # Go back to the Manage Moods menu loop

        if action == "b":
            return
            
        # Action is a number corresponding to a mood
        idx = int(action) - 1
        if 0 <= idx < len(mood_options):
            mood = mood_options[idx]
            # Use add_mood to replace the existing mood
            user_prefs.add_mood(mood)
            print_success(f"Set preferred mood to: {mood}")
            # add_mood already calls save_preferences, no need to call it again here
        else:
            # This case should ideally not be reached due to get_validated_input
            print_error("Invalid selection.")

def manage_wallpaper_settings():
    """Manage wallpaper-specific settings."""
    while True:
        print_section("Manage Wallpaper Settings")
        print_option("1", "Auto-set wallpaper")
        print_option("2", "Cache duration")
        print_option("3", "Fit mode")
        print_option("4", "Background color")
        print_option("5", "Multi-monitor mode")
        print_option("6", "Refresh rate")
        print_option("7", "Preview before setting")
        print_option("b", "Back")
        
        setting_choice = get_validated_input("Select an option (1-7, b)", ["1", "2", "3", "4", "5", "6", "7", "b"])
        
        if setting_choice == "b":
            return
        
        if setting_choice == "1":
            print_info("Enable or disable automatic wallpaper setting")
            print_option("1", "Enable")
            print_option("2", "Disable")
            print_option("b", "Back")
            auto_set = get_validated_input("Select option (1-2, b)", ["1", "2", "b"])
            if auto_set == "_INTERRUPTED_":
                continue
            if auto_set == "b":
                continue
            user_prefs.wallpaper_settings["auto_set"] = (auto_set == "1")
            print_success(f"Auto-set wallpaper {'enabled' if user_prefs.wallpaper_settings['auto_set'] else 'disabled'}")
        
        elif setting_choice == "2":
            print_info("Set how long to keep generated wallpapers (in days)")
            print_option("1", "7 days")
            print_option("2", "14 days")
            print_option("3", "30 days")
            print_option("4", "60 days")
            print_option("5", "90 days")
            print_option("6", "Custom duration")
            print_option("b", "Back")
            duration_choice = get_validated_input("Select option (1-6, b)", ["1", "2", "3", "4", "5", "6", "b"])
            if duration_choice == "_INTERRUPTED_":
                continue
            
            if duration_choice == "b":
                continue
            elif duration_choice == "6":
                while True:
                    try:
                        days = int(input("Enter number of days (1-365): "))
                        if 1 <= days <= 365:
                            user_prefs.wallpaper_settings["cache_duration"] = days
                            print_success(f"Cache duration set to {days} days")
                            break
                        else:
                            print_warning("Please enter a number between 1 and 365")
                    except ValueError:
                        print_warning("Please enter a valid number")
            else:
                durations = [7, 14, 30, 60, 90]
                user_prefs.wallpaper_settings["cache_duration"] = durations[int(duration_choice) - 1]
                print_success(f"Cache duration set to {user_prefs.wallpaper_settings['cache_duration']} days")
        
        elif setting_choice == "3":
            print_info("Select how the wallpaper should fit the screen")
            print_option("1", "Center")
            print_option("2", "Fit")
            print_option("3", "Fill")
            print_option("4", "Stretch")
            print_option("b", "Back")
            fit_mode = get_validated_input("Select option (1-4, b)", ["1", "2", "3", "4", "b"])
            if fit_mode == "_INTERRUPTED_":
                continue
            if fit_mode == "b":
                continue
            modes = ["center", "fit", "fill", "stretch"]
            user_prefs.wallpaper_settings["fit_mode"] = modes[int(fit_mode) - 1]
            print_success(f"Fit mode set to {user_prefs.wallpaper_settings['fit_mode']}")
        
        elif setting_choice == "4":
            print_info("Select background color (shown when wallpaper doesn't fill screen)")
            print_option("1", "Black")
            print_option("2", "White")
            print_option("3", "Custom color")
            print_option("b", "Back")
            color_choice = get_validated_input("Select option (1-3, b)", ["1", "2", "3", "b"])
            if color_choice == "_INTERRUPTED_":
                continue
            
            if color_choice == "b":
                continue
            elif color_choice == "1":
                user_prefs.wallpaper_settings["background_color"] = "#000000"
                print_success("Background color set to black")
            elif color_choice == "2":
                user_prefs.wallpaper_settings["background_color"] = "#FFFFFF"
                print_success("Background color set to white")
            else:
                while True:
                    color = input("Enter hex color code (e.g., #FF0000 for red): ").strip()
                    if re.match(r'^#[0-9A-Fa-f]{6}$', color):
                        user_prefs.wallpaper_settings["background_color"] = color
                        print_success(f"Background color set to {color}")
                        break
                    else:
                        print_warning("Please enter a valid hex color code (e.g., #FF0000)")
        
        elif setting_choice == "5":
            print_info("Select multi-monitor mode")
            print_option("1", "Mirror (same wallpaper on all monitors)")
            print_option("2", "Extend (different wallpapers)")
            print_option("3", "Individual (customize per monitor)")
            print_option("b", "Back")
            monitor_mode = get_validated_input("Select option (1-3, b)", ["1", "2", "3", "b"])
            if monitor_mode == "_INTERRUPTED_":
                continue
            if monitor_mode == "b":
                continue
            modes = ["mirror", "extend", "individual"]
            user_prefs.wallpaper_settings["multi_monitor"] = modes[int(monitor_mode) - 1]
            print_success(f"Multi-monitor mode set to {user_prefs.wallpaper_settings['multi_monitor']}")
        
        elif setting_choice == "6":
            print_info("Select wallpaper refresh rate")
            print_option("1", "Daily")
            print_option("2", "Weekly")
            print_option("3", "Monthly")
            print_option("4", "Never")
            print_option("b", "Back")
            refresh_rate = get_validated_input("Select option (1-4, b)", ["1", "2", "3", "4", "b"])
            if refresh_rate == "_INTERRUPTED_":
                continue
            if refresh_rate == "b":
                continue
            rates = ["daily", "weekly", "monthly", "never"]
            user_prefs.wallpaper_settings["refresh_rate"] = rates[int(refresh_rate) - 1]
            print_success(f"Refresh rate set to {user_prefs.wallpaper_settings['refresh_rate']}")
        
        elif setting_choice == "7":
            print_info("Enable or disable previewing images before setting as wallpaper")
            print_option("1", "Always preview (recommended)")
            print_option("2", "Skip preview")
            print_option("b", "Back")
            preview_choice = get_validated_input("Select option (1-2, b)", ["1", "2", "b"])
            if preview_choice == "_INTERRUPTED_":
                continue
            if preview_choice == "b":
                continue
            user_prefs.wallpaper_settings["skip_preview"] = (preview_choice == "2")
            print_success(f"Preview before setting {'disabled' if user_prefs.wallpaper_settings['skip_preview'] else 'enabled'}")
            
            # For compatibility with command line arg
            user_prefs.skip_preview = user_prefs.wallpaper_settings["skip_preview"]
        
        elif setting_choice == "8":
            print_info("Toggle preview functionality")
            print_option("1", "Enable preview")
            print_option("2", "Disable preview")
            print_option("b", "Back")
            preview_choice = get_validated_input("Select option (1-2, b)", ["1", "2", "b"])
            if preview_choice == "_INTERRUPTED_":
                continue
            if preview_choice == "b":
                continue
            skip_preview = (preview_choice == "2")
            user_prefs.wallpaper_settings["skip_preview"] = skip_preview
            print_success(f"Preview {'disabled' if skip_preview else 'enabled'}")
        
        user_prefs.save_preferences()

def configure_advanced_options():
    while True:  # Advanced Options menu loop
        print_section("Advanced Options")
        print_option("1", "Genres")
        print_option("2", "Style Settings & Options")
        print_option("3", "Moods")
        print_option("4", "Aspect Ratio")
        print_option("5", "Negative Prompt")
        print_option("6", "Imagen Settings")
        print_option("7", "Prompt Generation Settings")
        print_option("8", "Style & Artistic Settings")
        print_option("9", "Camera & Technical Settings")
        print_option("10", "Output Quality Settings")
        print_option("11", "Lighting & Atmosphere")
        print_option("12", "Composition & Environment")
        print_option("13", "Color & Detail Settings")
        print_option("14", "View Current Settings")
        print_option("15", "Customize All Parameters")
        print_option("16", "Generate AI Preset")
        print_option("17", "Reset to Default")
        print_option("b", "Back")
        
        advanced_choice = get_validated_input("Select option (1-17, b)",
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "b"])
        if advanced_choice == "_INTERRUPTED_":
            break # Exit advanced options loop

        if advanced_choice == "b":
            break  # Return to previous menu
        
        if advanced_choice == "1":
            manage_genres()
            
        elif advanced_choice == "2": # Styles
            manage_styles()  # Directly show the styles list
                
        elif advanced_choice == "3": # Moods
            manage_moods()
            
        elif advanced_choice == "4":
            change_aspect_ratio()
            
        elif advanced_choice == "5":
            manage_negative_prompt()
            
        elif advanced_choice == "6":
            manage_imagen_settings()
        
        elif advanced_choice == "7":
            manage_prompt_generation_settings()
            
        elif advanced_choice == "8":  # Style & Artistic Settings
            manage_style_settings()
            
        elif advanced_choice == "9":  # Camera & Technical Settings
            manage_camera_settings()
            
        elif advanced_choice == "10":  # Output Quality Settings
            manage_output_quality_settings()
            
        elif advanced_choice == "11":  # Lighting & Atmosphere
            manage_lighting_settings()
            
        elif advanced_choice == "12":  # Composition & Environment
            manage_composition_settings()
            
        elif advanced_choice == "13":  # Color & Detail Settings
            manage_color_settings()
            
        elif advanced_choice == "14":
            view_current_settings()
            
        elif advanced_choice == "15":
            customize_all_parameters()
            
        elif advanced_choice == "16":
            generate_ai_preset()
            
        elif advanced_choice == "17":
            reset_to_default()

def manage_prompt_generation_settings():
    """Manage settings for prompt generation."""
    # Check if prompt generator module is available
    if not PROMPT_GENERATOR_AVAILABLE:
        print_warning("Prompt generation settings are not available.")
        print_info("The prompt_generator module could not be imported.")
        input("Press Enter to continue...")
        return
    
    while True:  # Prompt Generation Settings menu loop
        print_section("Prompt Generation Settings")
        print_info("Choose how prompts are generated:")
        print_option("1", "Generate or enhance prompts WITH user preferences")
        print_option("2", "Generate or enhance prompts WITHOUT user preferences")
        print_option("b", "Back")
        
        choice = get_validated_input("Select option (1-2, b)", ["1", "2", "b"])
        if choice == "_INTERRUPTED_":
            break # Exit prompt generation settings loop

        if choice == "b":
            break  # Return to Advanced Options menu
        
        if choice == "1":
            set_prompt_preferences(True)
            print_success("Prompts will now be generated and enhanced using your preferences.")
            break
        
        elif choice == "2":
            set_prompt_preferences(False)
            print_success("Prompts will now be generated and enhanced without using your preferences.")
            print_info("This will create simple, generic prompts based only on the selected subject or tags.")
            break

def manage_style_settings():
    """Manage style-specific settings."""
    while True:  # Style & Artistic Settings menu loop
        print_section("Style & Artistic Settings")
        print_option("1", "Style Selection")
        print_option("2", "Art Movement")
        print_option("3", "Post-Processing Effects")
        print_option("b", "Back")
        
        style_choice = get_validated_input("Select option (1-3, b)", ["1", "2", "3", "b"])
        if style_choice == "_INTERRUPTED_":
            break # Exit style settings loop
        if style_choice == "b":
            break  # Return to Style & Artistic Settings menu
        
        if style_choice == "1":
            while True:  # Style Selection submenu loop
                print_info("Select style:")
                print_option("1", "Traditional Art")
                print_option("2", "Digital Art")
                print_option("3", "Illustration")
                print_option("4", "Random Style Mix")
                print_option("5", "See More Styles")
                print_option("6", "Custom Style")
                print_option("b", "Back")
                
                selection_choice = get_validated_input("Select style (1-6, b)", ["1", "2", "3", "4", "5", "6", "b"])
                if selection_choice == "b":
                    break  # Return to Style & Artistic Settings menu
                
                if selection_choice == "4":  # Random Style Mix
                    style_mix = generate_random_style_mix()
                    print_info(f"Generated random style mix: {style_mix}")
                    confirm = get_validated_input("Use this style mix? (y/n)", ["y", "n"])
                    if confirm == "y":
                        user_prefs.preferred_styles = [style_mix]
                        print_success(f"Style set to: {style_mix}")
                        user_prefs.save_preferences()
                    continue
                
                if selection_choice == "5":  # See More Styles
                    print_info("Additional available styles:")
                    additional_styles = [
                        "Photography", "Pixel Art", "Watercolor", "Oil Painting", 
                        "Sketch", "Cartoon", "Manga", "Anime", "3D Render", 
                        "Concept Art", "Graffiti", "Minimalist", "Abstract", 
                        "Impressionist", "Surrealist", "Pop Art", "Cyberpunk",
                        "Steampunk", "Gothic", "Fantasy", "Sci-Fi"
                    ]
                    for i, style in enumerate(additional_styles, 1):
                        print_option(str(i), style)
                    
                    print_option("b", "Back to Style Selection")
                    
                    more_choice = get_validated_input(
                        f"Select style (1-{len(additional_styles)}, b)", 
                        [str(i) for i in range(1, len(additional_styles) + 1)] + ["b"]
                    )
                    
                    if more_choice == "b":
                        continue  # Return to main style selection menu
                    
                    selected_style = additional_styles[int(more_choice) - 1].lower().replace(" ", "_")
                    user_prefs.preferred_styles = [selected_style]
                    print_success(f"Style set to {selected_style}")
                    user_prefs.save_preferences()
                    continue
                
                if selection_choice == "6":  # Custom Style
                    custom_style = input("Enter custom style: ").strip()
                    if custom_style:
                        user_prefs.preferred_styles = [custom_style]
                        print_success(f"Custom style set to: {custom_style}")
                        user_prefs.save_preferences()
                    continue
                
                styles = {
                    "1": "traditional_art",
                    "2": "digital_art",
                    "3": "illustration"
                }
                
                selected_style = styles[selection_choice]
                user_prefs.preferred_styles = [selected_style]
                print_success(f"Style set to {selected_style}")
                user_prefs.save_preferences()
        
        elif style_choice == "2":
            while True:  # Art Movement submenu loop
                print_info("Select art movement:")
                print_option("0", "None (No specific art movement)")
                print_option("1", "Abstract Expressionism")
                print_option("2", "Impressionism")
                print_option("3", "Surrealism")
                print_option("4", "Cubism")
                print_option("5", "Pop Art")
                print_option("6", "Custom Movement")
                print_option("b", "Back")
                
                movement_choice = get_validated_input("Select art movement (0-6, b)", ["0", "1", "2", "3", "4", "5", "6", "b"])
                if movement_choice == "b":
                    break  # Return to Style & Artistic menu
                
                if movement_choice == "0":
                    user_prefs.imagen_settings.setdefault("style_settings", {})["art_movement"] = None
                    print_success("Art movement set to None")
                    user_prefs.save_preferences()
                    continue
                
                if movement_choice == "6":
                    custom_movement = input("Enter custom art movement: ").strip()
                    if custom_movement:
                        user_prefs.imagen_settings.setdefault("style_settings", {})["art_movement"] = custom_movement
                        print_success(f"Custom art movement set to: {custom_movement}")
                        user_prefs.save_preferences()
                    continue
                
                movements = {
                    "1": "Abstract Expressionism",
                    "2": "Impressionism",
                    "3": "Surrealism",
                    "4": "Cubism",
                    "5": "Pop Art"
                }
                
                user_prefs.imagen_settings.setdefault("style_settings", {})["art_movement"] = movements[movement_choice]
                print_success(f"Art movement set to {movements[movement_choice]}")
                user_prefs.save_preferences()
        
        elif style_choice == "3":
            while True:  # Post-Processing Effects submenu loop
                print_info("Select post-processing effects:")
                print_option("1", "Bloom Effect")
                print_option("2", "Vignette Effect")
                print_option("3", "Color Grading")
                print_option("4", "Depth of Field")
                print_option("5", "Motion Blur")
                print_option("6", "Film Grain")
                print_option("7", "Lens Flare")
                print_option("8", "Chromatic Aberration")
                print_option("9", "Sharpening")
                print_option("10", "Tone Mapping")
                print_option("11", "HDR Effect")
                print_option("12", "Light Leaks")
                print_option("13", "No Post-Processing")
                print_option("14", "Custom Effects")
                print_option("b", "Back")
                
                effects_choice = get_validated_input("Select post-processing effects (1-14, b)", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "b"])
                if effects_choice == "b":
                    break  # Return to Style & Artistic Settings menu
                
                if effects_choice == "13":
                    user_prefs.imagen_settings["style_settings"]["post_processing"] = []
                    print_success("Post-processing effects cleared")
                    user_prefs.save_preferences()
                    continue
                
                if effects_choice == "14":
                    custom_effects = input("Enter custom post-processing effects (comma-separated): ").strip()
                    if custom_effects:
                        effects_list = [e.strip() for e in custom_effects.split(",")]
                        user_prefs.imagen_settings["style_settings"]["post_processing"] = effects_list
                        print_success(f"Custom post-processing effects set to: {', '.join(effects_list)}")
                        user_prefs.save_preferences()
                    continue
                
                effects = {
                    "1": ["bloom"],
                    "2": ["vignette"],
                    "3": ["color_grading"],
                    "4": ["depth_of_field"],
                    "5": ["motion_blur"],
                    "6": ["film_grain"],
                    "7": ["lens_flare"],
                    "8": ["chromatic_aberration"],
                    "9": ["sharpening"],
                    "10": ["tone_mapping"],
                    "11": ["hdr"],
                    "12": ["light_leaks"]
                }
                
                user_prefs.imagen_settings["style_settings"]["post_processing"] = effects[effects_choice]
                print_success(f"Post-processing effects set to {effects[effects_choice][0]}")
                user_prefs.save_preferences()
    
def reset_all_settings_to_none():
    """
    Reset all user preference settings to None (null).
    
    This function sets all configurable settings in user_prefs to None,
    effectively nullifying all settings while maintaining the structure.
    """
    global user_prefs
    
    # Reset main preferences
    user_prefs.preferred_genres = []
    user_prefs.preferred_styles = []
    user_prefs.preferred_moods = []
    user_prefs.negative_prompts = []
    
    # Reset imagen settings - Camera settings
    user_prefs.imagen_settings["camera_settings"] = {
        "camera_model": None,
        "lens_type": None,
        "aperture": None,
        "depth_of_field": None,
        "special_lens": None,
        "camera_brand": None,
        "focal_length": None,
        "sensor_type": None
    }
    
    # Reset imagen settings - Style settings
    user_prefs.imagen_settings["style_settings"] = {
        "art_movement": None,
        "post_processing": []
    }
    
    # Reset imagen settings - Lighting settings
    user_prefs.imagen_settings["lighting_settings"] = {
        "lighting_type": None,
        "time_of_day": None,
        "light_source": None,
        "light_quality": None,
        "artificial_sources": []
    }
    
    # Reset imagen settings - Composition settings
    user_prefs.imagen_settings["composition_settings"] = {
        "technique": None,
        "camera_angle": None,
        "visual_flow": None,
        "depth_layering": None
    }
    
    # Reset imagen settings - Environment settings
    user_prefs.imagen_settings["environment_settings"] = {
        "weather": None,
        "season": None,
        "atmospheric_effects": [],
        "location_type": None
    }
    
    # Reset imagen settings - Color settings
    user_prefs.imagen_settings["color_settings"] = {
        "color_scheme": None,
        "palette_type": None,
        "color_temperature": None
    }
    
    # Reset imagen settings - Detail settings
    user_prefs.imagen_settings["detail_settings"] = {
        "texture_quality": None,
        "special_effects": []
    }
    
    # Reset imagen settings - Quality settings
    user_prefs.imagen_settings["quality_settings"] = {
        "resolution": "1920x1080",  # Keep a default resolution
        "detail_level": None,
        "rendering_quality": None
    }
    
    # Reset other imagen settings
    user_prefs.imagen_settings["negative_prompt"] = ""
    
    # Save the reset preferences
    user_prefs.save_preferences()
    
    print_success("All settings have been reset to None (null).")
    print_info("Your preferences have been updated and saved.")

def manage_camera_settings():
    """Manage camera-specific settings."""
    while True:
        print_section("Camera & Technical Settings")
        print_option("1", "Camera Model")
        print_option("2", "Lens Type")
        print_option("3", "Aperture")
        print_option("4", "Depth of Field")
        print_option("5", "Special Lens Effects")
        print_option("b", "Back")
        
        choice = get_validated_input("Select option (1-5, b)", ["1", "2", "3", "4", "5", "b"])
        if choice == "_INTERRUPTED_":
            return # Exit camera settings

        if choice == "b":
            return
            
        if choice == "1":
            print_info("Select camera model:")
            print_option("1", "DSLR")
            print_option("2", "Mirrorless")
            print_option("3", "Medium Format")
            print_option("4", "Film Camera")
            print_option("5", "Custom Model")
            print_option("b", "Back")
            
            model_choice = get_validated_input("Select camera model (1-5, b)", ["1", "2", "3", "4", "5", "b"])
            if model_choice == "_INTERRUPTED_":
                continue

            if model_choice == "b":
                continue
            models = {
                "1": "dslr",
                "2": "mirrorless",
                "3": "medium_format",
                "4": "film_camera"
            }
            
            if model_choice == "5":
                custom_model = input("Enter custom camera model: ").strip()
                if custom_model:
                    user_prefs.imagen_settings["camera_settings"]["camera_model"] = custom_model
                    print_success(f"Camera model set to: {custom_model}")
            else:
                user_prefs.imagen_settings["camera_settings"]["camera_model"] = models[model_choice]
                print_success(f"Camera model set to: {models[model_choice]}")
            
            user_prefs.save_preferences()
            
        elif choice == "2":
            print_info("Select lens type:")
            print_option("1", "Wide Angle")
            print_option("2", "Standard")
            print_option("3", "Telephoto")
            print_option("4", "Macro")
            print_option("5", "Fish Eye")
            print_option("6", "Custom Lens")
            print_option("b", "Back")
            
            lens_choice = get_validated_input("Select lens type (1-6, b)", ["1", "2", "3", "4", "5", "6", "b"])
            if lens_choice == "_INTERRUPTED_":
                continue

            if lens_choice == "b":
                continue
            lenses = {
                "1": "wide_angle",
                "2": "standard",
                "3": "telephoto",
                "4": "macro",
                "5": "fish_eye"
            }
            
            if lens_choice == "6":
                custom_lens = input("Enter custom lens type: ").strip()
                if custom_lens:
                    user_prefs.imagen_settings["camera_settings"]["lens_type"] = custom_lens
                    print_success(f"Lens type set to: {custom_lens}")
            else:
                user_prefs.imagen_settings["camera_settings"]["lens_type"] = lenses[lens_choice]
                print_success(f"Lens type set to: {lenses[lens_choice]}")
            
            user_prefs.save_preferences()
            
        elif choice == "3":
            print_info("Select aperture:")
            print_option("1", "f/1.4 (Very shallow depth of field)")
            print_option("2", "f/2.8 (Shallow depth of field)")
            print_option("3", "f/4 (Moderate depth of field)")
            print_option("4", "f/8 (Deep depth of field)")
            print_option("5", "f/16 (Very deep depth of field)")
            print_option("6", "Custom Aperture")
            print_option("b", "Back")
            
            aperture_choice = get_validated_input("Select aperture (1-6, b)", ["1", "2", "3", "4", "5", "6", "b"])
            if aperture_choice == "_INTERRUPTED_":
                continue

            if aperture_choice == "b":
                continue
            apertures = {
                "1": "f/1.4",
                "2": "f/2.8",
                "3": "f/4",
                "4": "f/8",
                "5": "f/16"
            }
            
            if aperture_choice == "6":
                custom_aperture = input("Enter custom aperture (e.g., f/5.6): ").strip()
                if custom_aperture:
                    user_prefs.imagen_settings["camera_settings"]["aperture"] = custom_aperture
                    print_success(f"Aperture set to: {custom_aperture}")
            else:
                user_prefs.imagen_settings["camera_settings"]["aperture"] = apertures[aperture_choice]
                print_success(f"Aperture set to: {apertures[aperture_choice]}")
            
            user_prefs.save_preferences()
            
        elif choice == "4":
            print_info("Select depth of field:")
            print_option("1", "Very Shallow")
            print_option("2", "Shallow")
            print_option("3", "Moderate")
            print_option("4", "Deep")
            print_option("5", "Very Deep")
            print_option("6", "Custom Setting")
            print_option("b", "Back")
            
            dof_choice = get_validated_input("Select depth of field (1-6, b)", ["1", "2", "3", "4", "5", "6", "b"])
            if dof_choice == "_INTERRUPTED_":
                continue

            if dof_choice == "b":
                continue
            dof_settings = {
                "1": "very_shallow",
                "2": "shallow",
                "3": "moderate",
                "4": "deep",
                "5": "very_deep"
            }
            
            if dof_choice == "6":
                custom_dof = input("Enter custom depth of field setting: ").strip()
                if custom_dof:
                    user_prefs.imagen_settings["camera_settings"]["depth_of_field"] = custom_dof
                    print_success(f"Depth of field set to: {custom_dof}")
            else:
                user_prefs.imagen_settings["camera_settings"]["depth_of_field"] = dof_settings[dof_choice]
                print_success(f"Depth of field set to: {dof_settings[dof_choice]}")
            
            user_prefs.save_preferences()
            
        elif choice == "5":
            print_info("Select special lens effects:")
            print_option("1", "Bokeh")
            print_option("2", "Lens Flare")
            print_option("3", "Soft Focus")
            print_option("4", "Tilt-Shift")
            print_option("5", "Chromatic Aberration")
            print_option("6", "Custom Effect")
            print_option("7", "No Special Effects")
            print_option("b", "Back")
            
            effect_choice = get_validated_input("Select special effect (1-7, b)", ["1", "2", "3", "4", "5", "6", "7", "b"])
            if effect_choice == "_INTERRUPTED_":
                continue

            if effect_choice == "b":
                continue
            effects = {
                "1": "bokeh",
                "2": "lens_flare",
                "3": "soft_focus",
                "4": "tilt_shift",
                "5": "chromatic_aberration"
            }
            
            if effect_choice == "6":
                custom_effect = input("Enter custom lens effect: ").strip()
                if custom_effect:
                    user_prefs.imagen_settings["camera_settings"]["special_lens"] = custom_effect
                    print_success(f"Special lens effect set to: {custom_effect}")
            elif effect_choice == "7":
                user_prefs.imagen_settings["camera_settings"]["special_lens"] = None
                print_success("Special lens effects cleared")
            else:
                user_prefs.imagen_settings["camera_settings"]["special_lens"] = effects[effect_choice]
                print_success(f"Special lens effect set to: {effects[effect_choice]}")
            
            user_prefs.save_preferences()

def manage_output_quality_settings():
    """Manage output quality settings."""
    while True:
        print_section("Output Quality Settings")
        print_option("1", "Resolution")
        print_option("2", "Detail Level")
        print_option("3", "Rendering Quality")
        print_option("b", "Back")
        
        choice = get_validated_input("Select option (1-3, b)", ["1", "2", "3", "b"])
        if choice == "_INTERRUPTED_":
            return # Exit output quality settings

        if choice == "b":
            return
            
        if choice == "1":
            print_info("Select resolution:")
            print_option("1", "HD (1280x720)")
            print_option("2", "Full HD (1920x1080)")
            print_option("3", "2K (2560x1440)")
            print_option("4", "4K (3840x2160)")
            print_option("5", "8K (7680x4320)")
            print_option("6", "Custom Resolution")
            print_option("b", "Back")
            
            res_choice = get_validated_input("Select resolution (1-6, b)", ["1", "2", "3", "4", "5", "6", "b"])
            if res_choice == "_INTERRUPTED_":
                continue

            if res_choice == "b":
                continue
            resolutions = {
                "1": "1280x720",
                "2": "1920x1080",
                "3": "2560x1440",
                "4": "3840x2160",
                "5": "7680x4320"
            }
            
            if res_choice == "6":
                while True:
                    custom_res = input("Enter custom resolution (width x height, e.g. 1920x1080): ").strip()
                    if re.match(r'^\d+x\d+$', custom_res):
                        user_prefs.imagen_settings["quality_settings"]["resolution"] = custom_res
                        print_success(f"Resolution set to: {custom_res}")
                        break
                    else:
                        print_error("Invalid resolution format. Please use width x height (e.g., 1920x1080)")
            else:
                user_prefs.imagen_settings["quality_settings"]["resolution"] = resolutions[res_choice]
                print_success(f"Resolution set to: {resolutions[res_choice]}")
            
            user_prefs.save_preferences()
            
        elif choice == "2":
            print_info("Select detail level:")
            print_option("1", "Low")
            print_option("2", "Medium")
            print_option("3", "High")
            print_option("4", "Ultra")
            print_option("5", "None")
            print_option("b", "Back")
            
            detail_choice = get_validated_input("Select detail level (1-5, b)", ["1", "2", "3", "4", "5", "b"])
            if detail_choice == "_INTERRUPTED_":
                continue

            if detail_choice == "b":
                continue
            detail_levels = {
                "1": "low",
                "2": "medium",
                "3": "high",
                "4": "ultra",
                "5": None
            }
            
            user_prefs.imagen_settings["quality_settings"]["detail_level"] = detail_levels[detail_choice]
            print_success(f"Detail level set to: {detail_levels[detail_choice] if detail_levels[detail_choice] else 'None'}")
            user_prefs.save_preferences()
            
        elif choice == "3":
            print_info("Select rendering quality:")
            print_option("1", "Draft")
            print_option("2", "Standard")
            print_option("3", "High")
            print_option("4", "Maximum")
            print_option("5", "None")
            print_option("b", "Back")
            
            quality_choice = get_validated_input("Select rendering quality (1-5, b)", ["1", "2", "3", "4", "5", "b"])
            if quality_choice == "_INTERRUPTED_":
                continue

            if quality_choice == "b":
                continue
            quality_levels = {
                "1": "draft",
                "2": "standard",
                "3": "high",
                "4": "maximum",
                "5": None
            }
            
            user_prefs.imagen_settings["quality_settings"]["rendering_quality"] = quality_levels[quality_choice]
            print_success(f"Rendering quality set to: {quality_levels[quality_choice] if quality_levels[quality_choice] else 'None'}")
            user_prefs.save_preferences()

def manage_lighting_settings():
    """Manage lighting and atmosphere settings."""
    while True:
        print_section("Lighting & Atmosphere Settings")
        print_option("1", "Lighting Type")
        print_option("2", "Time of Day")
        print_option("3", "Light Source")
        print_option("4", "Light Quality")
        print_option("5", "Artificial Light Sources")
        print_option("b", "Back")
        
        choice = get_validated_input("Select option (1-5, b)", ["1", "2", "3", "4", "5", "b"])
        if choice == "_INTERRUPTED_":
            return # Exit lighting settings

        if choice == "b":
            return
            
        if choice == "1":
            print_info("Select lighting type:")
            print_option("1", "Natural")
            print_option("2", "Artificial")
            print_option("3", "Mixed")
            print_option("4", "Dramatic")
            print_option("5", "Ambient")
            print_option("6", "Custom")
            print_option("b", "Back")
            
            type_choice = get_validated_input("Select lighting type (1-6, b)", ["1", "2", "3", "4", "5", "6", "b"])
            if type_choice == "_INTERRUPTED_":
                continue

            if type_choice == "b":
                continue
            lighting_types = {
                "1": "natural",
                "2": "artificial",
                "3": "mixed",
                "4": "dramatic",
                "5": "ambient"
            }
            
            if type_choice == "6":
                custom_type = input("Enter custom lighting type: ").strip()
                if custom_type:
                    user_prefs.imagen_settings["lighting_settings"]["lighting_type"] = custom_type
                    print_success(f"Lighting type set to: {custom_type}")
            else:
                user_prefs.imagen_settings["lighting_settings"]["lighting_type"] = lighting_types[type_choice]
                print_success(f"Lighting type set to: {lighting_types[type_choice]}")
            
            user_prefs.save_preferences()
            
        elif choice == "2":
            print_info("Select time of day:")
            print_option("1", "Dawn")
            print_option("2", "Morning")
            print_option("3", "Noon")
            print_option("4", "Afternoon")
            print_option("5", "Sunset")
            print_option("6", "Dusk")
            print_option("7", "Night")
            print_option("8", "Custom")
            print_option("b", "Back")
            
            time_choice = get_validated_input("Select time of day (1-8, b)", ["1", "2", "3", "4", "5", "6", "7", "8", "b"])
            if time_choice == "_INTERRUPTED_":
                continue

            if time_choice == "b":
                continue
            times = {
                "1": "dawn",
                "2": "morning",
                "3": "noon",
                "4": "afternoon",
                "5": "sunset",
                "6": "dusk",
                "7": "night"
            }
            
            if time_choice == "8":
                custom_time = input("Enter custom time of day: ").strip()
                if custom_time:
                    user_prefs.imagen_settings["lighting_settings"]["time_of_day"] = custom_time
                    print_success(f"Time of day set to: {custom_time}")
            else:
                user_prefs.imagen_settings["lighting_settings"]["time_of_day"] = times[time_choice]
                print_success(f"Time of day set to: {times[time_choice]}")
            
            user_prefs.save_preferences()
            
        elif choice == "3":
            print_info("Select light source:")
            print_option("1", "Sun")
            print_option("2", "Moon")
            print_option("3", "Fire")
            print_option("4", "Electric")
            print_option("5", "Multiple Sources")
            print_option("6", "Custom")
            print_option("b", "Back")
            
            source_choice = get_validated_input("Select light source (1-6, b)", ["1", "2", "3", "4", "5", "6", "b"])
            if source_choice == "_INTERRUPTED_":
                continue

            if source_choice == "b":
                continue
            sources = {
                "1": "sun",
                "2": "moon",
                "3": "fire",
                "4": "electric",
                "5": "multiple"
            }
            
            if source_choice == "6":
                custom_source = input("Enter custom light source: ").strip()
                if custom_source:
                    user_prefs.imagen_settings["lighting_settings"]["light_source"] = custom_source
                    print_success(f"Light source set to: {custom_source}")
            else:
                user_prefs.imagen_settings["lighting_settings"]["light_source"] = sources[source_choice]
                print_success(f"Light source set to: {sources[source_choice]}")
            
            user_prefs.save_preferences()
            
        elif choice == "4":
            print_info("Select light quality:")
            print_option("1", "Soft")
            print_option("2", "Hard")
            print_option("3", "Diffused")
            print_option("4", "Directional")
            print_option("5", "Atmospheric")
            print_option("6", "Custom")
            print_option("b", "Back")
            
            quality_choice = get_validated_input("Select light quality (1-6, b)", ["1", "2", "3", "4", "5", "6", "b"])
            if quality_choice == "_INTERRUPTED_":
                continue

            if quality_choice == "b":
                continue
            qualities = {
                "1": "soft",
                "2": "hard",
                "3": "diffused",
                "4": "directional",
                "5": "atmospheric"
            }
            
            if quality_choice == "6":
                custom_quality = input("Enter custom light quality: ").strip()
                if custom_quality:
                    user_prefs.imagen_settings["lighting_settings"]["light_quality"] = custom_quality
                    print_success(f"Light quality set to: {custom_quality}")
            else:
                user_prefs.imagen_settings["lighting_settings"]["light_quality"] = qualities[quality_choice]
                print_success(f"Light quality set to: {qualities[quality_choice]}")
            
            user_prefs.save_preferences()
            
        elif choice == "5":
            while True:
                print_info("Manage artificial light sources:")
                current_sources = user_prefs.imagen_settings["lighting_settings"].get("artificial_sources", [])
                if current_sources:
                    print_info("Current artificial sources:")
                    for i, source in enumerate(current_sources, 1):
                        print(f"{i}. {source}")
                else:
                    print_info("No artificial light sources set")
                
                print_option("1", "Add Source")
                print_option("2", "Remove Source")
                print_option("3", "Clear All Sources")
                print_option("b", "Back")
                
                source_choice = get_validated_input("Select option (1-3, b)", ["1", "2", "3", "b"])
                if source_choice == "_INTERRUPTED_":
                    break # Exit artificial sources loop

                if source_choice == "b":
                    break
                    
                if source_choice == "1":
                    print_info("Select source to add:")
                    print_option("1", "Lamp")
                    print_option("2", "LED")
                    print_option("3", "Neon")
                    print_option("4", "Fluorescent")
                    print_option("5", "Candle")
                    print_option("6", "Custom")
                    
                    add_choice = get_validated_input("Select source (1-6)", ["1", "2", "3", "4", "5", "6"])
                    
                    sources = {
                        "1": "lamp",
                        "2": "led",
                        "3": "neon",
                        "4": "fluorescent",
                        "5": "candle"
                    }
                    
                    if add_choice == "6":
                        custom_source = input("Enter custom light source: ").strip()
                        if custom_source and custom_source not in current_sources:
                            current_sources.append(custom_source)
                            print_success(f"Added artificial source: {custom_source}")
                    else:
                        source = sources[add_choice]
                        if source not in current_sources:
                            current_sources.append(source)
                            print_success(f"Added artificial source: {source}")
                        else:
                            print_warning(f"{source} is already in the list")
                    
                    user_prefs.imagen_settings["lighting_settings"]["artificial_sources"] = current_sources
                    user_prefs.save_preferences()
                    
                elif source_choice == "2":
                    if current_sources:
                        try:
                            idx = int(input("Enter number of source to remove: ")) - 1
                            if 0 <= idx < len(current_sources):
                                removed = current_sources.pop(idx)
                                print_success(f"Removed artificial source: {removed}")
                                user_prefs.imagen_settings["lighting_settings"]["artificial_sources"] = current_sources
                                user_prefs.save_preferences()
                            else:
                                print_error("Invalid source number")
                        except ValueError:
                            print_error("Please enter a valid number")
                    else:
                        print_warning("No sources to remove")
                        
                elif source_choice == "3":
                    if current_sources:
                        confirm = get_validated_input("Are you sure you want to clear all sources? (y/n)", ["y", "n"])
                        if confirm.lower() == "y":
                            user_prefs.imagen_settings["lighting_settings"]["artificial_sources"] = []
                            print_success("Cleared all artificial sources")
                            user_prefs.save_preferences()
                    else:
                        print_warning("No sources to clear")

def manage_composition_settings():
    """Manage composition and environment settings."""
    while True:
        print_section("Composition & Environment Settings")
        print_option("1", "Composition Technique")
        print_option("2", "Camera Angle")
        print_option("3", "Visual Flow")
        print_option("4", "Depth Layering")
        print_option("5", "Environment Settings")
        print_option("b", "Back")
        
        choice = get_validated_input("Select option (1-5, b)", ["1", "2", "3", "4", "5", "b"])
        
        if choice == "b":
            return
            
        if choice == "1":
            print_info("Select composition technique:")
            print_option("1", "Rule of Thirds")
            print_option("2", "Golden Ratio")
            print_option("3", "Symmetry")
            print_option("4", "Leading Lines")
            print_option("5", "Framing")
            print_option("6", "Custom")
            print_option("b", "Back")
            
            technique_choice = get_validated_input("Select technique (1-6, b)", ["1", "2", "3", "4", "5", "6", "b"])
            
            if technique_choice == "b":
                continue
            techniques = {
                "1": "rule_of_thirds",
                "2": "golden_ratio",
                "3": "symmetry",
                "4": "leading_lines",
                "5": "framing"
            }
            
            if technique_choice == "6":
                custom_technique = input("Enter custom composition technique: ").strip()
                if custom_technique:
                    user_prefs.imagen_settings["composition_settings"]["technique"] = custom_technique
                    print_success(f"Composition technique set to: {custom_technique}")
            else:
                user_prefs.imagen_settings["composition_settings"]["technique"] = techniques[technique_choice]
                print_success(f"Composition technique set to: {techniques[technique_choice]}")
            
            user_prefs.save_preferences()
            
        elif choice == "2":
            print_info("Select camera angle:")
            print_option("1", "Eye Level")
            print_option("2", "Low Angle")
            print_option("3", "High Angle")
            print_option("4", "Bird's Eye")
            print_option("5", "Dutch Angle")
            print_option("6", "Custom")
            print_option("b", "Back")
            
            angle_choice = get_validated_input("Select camera angle (1-6, b)", ["1", "2", "3", "4", "5", "6", "b"])
            
            if angle_choice == "b":
                continue
            angles = {
                "1": "eye_level",
                "2": "low_angle",
                "3": "high_angle",
                "4": "birds_eye",
                "5": "dutch_angle"
            }
            
            if angle_choice == "6":
                custom_angle = input("Enter custom camera angle: ").strip()
                if custom_angle:
                    user_prefs.imagen_settings["composition_settings"]["camera_angle"] = custom_angle
                    print_success(f"Camera angle set to: {custom_angle}")
            else:
                user_prefs.imagen_settings["composition_settings"]["camera_angle"] = angles[angle_choice]
                print_success(f"Camera angle set to: {angles[angle_choice]}")
            
            user_prefs.save_preferences()
            
        elif choice == "3":
            print_info("Select visual flow:")
            print_option("1", "Linear")
            print_option("2", "Circular")
            print_option("3", "Diagonal")
            print_option("4", "Triangular")
            print_option("5", "Z-Pattern")
            print_option("6", "Custom")
            print_option("b", "Back")
            
            flow_choice = get_validated_input("Select visual flow (1-6, b)", ["1", "2", "3", "4", "5", "6", "b"])
            
            if flow_choice == "b":
                continue
            flows = {
                "1": "linear",
                "2": "circular",
                "3": "diagonal",
                "4": "triangular",
                "5": "z_pattern"
            }
            
            if flow_choice == "6":
                custom_flow = input("Enter custom visual flow: ").strip()
                if custom_flow:
                    user_prefs.imagen_settings["composition_settings"]["visual_flow"] = custom_flow
                    print_success(f"Visual flow set to: {custom_flow}")
            else:
                user_prefs.imagen_settings["composition_settings"]["visual_flow"] = flows[flow_choice]
                print_success(f"Visual flow set to: {flows[flow_choice]}")
            
            user_prefs.save_preferences()
            
        elif choice == "4":
            print_info("Select depth layering:")
            print_option("1", "Foreground Focus")
            print_option("2", "Middle Ground Focus")
            print_option("3", "Background Focus")
            print_option("4", "Multi-Layer")
            print_option("5", "Flat")
            print_option("6", "Custom")
            print_option("b", "Back")
            
            depth_choice = get_validated_input("Select depth layering (1-6, b)", ["1", "2", "3", "4", "5", "6", "b"])
            
            if depth_choice == "b":
                continue
            depths = {
                "1": "foreground_focus",
                "2": "middle_ground_focus",
                "3": "background_focus",
                "4": "multi_layer",
                "5": "flat"
            }
            
            if depth_choice == "6":
                custom_depth = input("Enter custom depth layering: ").strip()
                if custom_depth:
                    user_prefs.imagen_settings["composition_settings"]["depth_layering"] = custom_depth
                    print_success(f"Depth layering set to: {custom_depth}")
            else:
                user_prefs.imagen_settings["composition_settings"]["depth_layering"] = depths[depth_choice]
                print_success(f"Depth layering set to: {depths[depth_choice]}")
            
            user_prefs.save_preferences()
            
        elif choice == "5":
            while True:
                print_info("Environment Settings:")
                print_option("1", "Weather")
                print_option("2", "Season")
                print_option("3", "Atmospheric Effects")
                print_option("4", "Location Type")
                print_option("b", "Back")
                
                env_choice = get_validated_input("Select option (1-4, b)", ["1", "2", "3", "4", "b"])
                if env_choice == "_INTERRUPTED_":
                    break # Exit environment settings loop

                if env_choice == "b":
                    break
                    
                if env_choice == "1":
                    print_info("Select weather:")
                    print_option("1", "Clear")
                    print_option("2", "Cloudy")
                    print_option("3", "Rainy")
                    print_option("4", "Stormy")
                    print_option("5", "Snowy")
                    print_option("6", "Foggy")
                    print_option("7", "Custom")
                    print_option("b", "Back")
                    
                    weather_choice = get_validated_input("Select weather (1-7, b)", ["1", "2", "3", "4", "5", "6", "7", "b"])
                    
                    if weather_choice == "b":
                        continue
                    weather_types = {
                        "1": "clear",
                        "2": "cloudy",
                        "3": "rainy",
                        "4": "stormy",
                        "5": "snowy",
                        "6": "foggy"
                    }
                    
                    if weather_choice == "7":
                        custom_weather = input("Enter custom weather: ").strip()
                        if custom_weather:
                            user_prefs.imagen_settings["environment_settings"]["weather"] = custom_weather
                            print_success(f"Weather set to: {custom_weather}")
                    else:
                        user_prefs.imagen_settings["environment_settings"]["weather"] = weather_types[weather_choice]
                        print_success(f"Weather set to: {weather_types[weather_choice]}")
                    
                    user_prefs.save_preferences()
                    
                elif env_choice == "2":
                    print_info("Select season:")
                    print_option("1", "Spring")
                    print_option("2", "Summer")
                    print_option("3", "Autumn")
                    print_option("4", "Winter")
                    print_option("5", "Custom")
                    print_option("b", "Back")
                    
                    season_choice = get_validated_input("Select season (1-5, b)", ["1", "2", "3", "4", "5", "b"])
                    
                    if season_choice == "b":
                        continue
                    seasons = {
                        "1": "spring",
                        "2": "summer",
                        "3": "autumn",
                        "4": "winter"
                    }
                    
                    if season_choice == "5":
                        custom_season = input("Enter custom season: ").strip()
                        if custom_season:
                            user_prefs.imagen_settings["environment_settings"]["season"] = custom_season
                            print_success(f"Season set to: {custom_season}")
                    else:
                        user_prefs.imagen_settings["environment_settings"]["season"] = seasons[season_choice]
                        print_success(f"Season set to: {seasons[season_choice]}")
                    
                    user_prefs.save_preferences()
                    
                elif env_choice == "3":
                    while True:
                        print_info("Manage atmospheric effects:")
                        current_effects = user_prefs.imagen_settings["environment_settings"].get("atmospheric_effects", [])
                        if current_effects:
                            print_info("Current effects:")
                            for i, effect in enumerate(current_effects, 1):
                                print(f"{i}. {effect}")
                        else:
                            print_info("No atmospheric effects set")
                        
                        print_option("1", "Add Effect")
                        print_option("2", "Remove Effect")
                        print_option("3", "Clear All Effects")
                        print_option("b", "Back")
                        
                        effect_choice = get_validated_input("Select option (1-3, b)", ["1", "2", "3", "b"])
                        
                        if effect_choice == "b":
                            break
                            
                        if effect_choice == "1":
                            print_info("Select effect to add:")
                            print_option("1", "Mist")
                            print_option("2", "Rain")
                            print_option("3", "Snow")
                            print_option("4", "Dust")
                            print_option("5", "Haze")
                            print_option("6", "Custom")
                            
                            add_choice = get_validated_input("Select effect (1-6)", ["1", "2", "3", "4", "5", "6"])
                            
                            effects = {
                                "1": "mist",
                                "2": "rain",
                                "3": "snow",
                                "4": "dust",
                                "5": "haze"
                            }
                            
                            if add_choice == "6":
                                custom_effect = input("Enter custom atmospheric effect: ").strip()
                                if custom_effect and custom_effect not in current_effects:
                                    current_effects.append(custom_effect)
                                    print_success(f"Added effect: {custom_effect}")
                            else:
                                effect = effects[add_choice]
                                if effect not in current_effects:
                                    current_effects.append(effect)
                                    print_success(f"Added effect: {effect}")
                                else:
                                    print_warning(f"{effect} is already in the list")
                            
                            user_prefs.imagen_settings["environment_settings"]["atmospheric_effects"] = current_effects
                            user_prefs.save_preferences()
                            
                        elif effect_choice == "2":
                            if current_effects:
                                try:
                                    idx = int(input("Enter number of effect to remove: ")) - 1
                                    if 0 <= idx < len(current_effects):
                                        removed = current_effects.pop(idx)
                                        print_success(f"Removed effect: {removed}")
                                        user_prefs.imagen_settings["environment_settings"]["atmospheric_effects"] = current_effects
                                        user_prefs.save_preferences()
                                    else:
                                        print_error("Invalid effect number")
                                except ValueError:
                                    print_error("Please enter a valid number")
                            else:
                                print_warning("No effects to remove")
                                
                        elif effect_choice == "3":
                            if current_effects:
                                confirm = get_validated_input("Are you sure you want to clear all effects? (y/n)", ["y", "n"])
                                if confirm.lower() == "y":
                                    user_prefs.imagen_settings["environment_settings"]["atmospheric_effects"] = []
                                    print_success("Cleared all atmospheric effects")
                                    user_prefs.save_preferences()
                            else:
                                print_warning("No effects to clear")
                                
                elif env_choice == "4":
                    print_info("Select location type:")
                    print_option("1", "Indoor")
                    print_option("2", "Outdoor")
                    print_option("3", "Urban")
                    print_option("4", "Rural")
                    print_option("5", "Underwater")
                    print_option("6", "Space")
                    print_option("7", "Custom")
                    print_option("b", "Back")
                    
                    location_choice = get_validated_input("Select location type (1-7, b)", ["1", "2", "3", "4", "5", "6", "7", "b"])
                    
                    if location_choice == "b":
                        continue
                    locations = {
                        "1": "indoor",
                        "2": "outdoor",
                        "3": "urban",
                        "4": "rural",
                        "5": "underwater",
                        "6": "space"
                    }
                    
                    if location_choice == "7":
                        custom_location = input("Enter custom location type: ").strip()
                        if custom_location:
                            user_prefs.imagen_settings["environment_settings"]["location_type"] = custom_location
                            print_success(f"Location type set to: {custom_location}")
                    else:
                        user_prefs.imagen_settings["environment_settings"]["location_type"] = locations[location_choice]
                        print_success(f"Location type set to: {locations[location_choice]}")
                    
                    user_prefs.save_preferences()

def manage_color_settings():
    """Manage color and detail settings."""
    while True:
        print_section("Color & Detail Settings")
        print_option("1", "Color Scheme")
        print_option("2", "Palette Type")
        print_option("3", "Color Temperature")
        print_option("4", "Detail Level")
        print_option("5", "Texture Quality")
        print_option("b", "Back")
        
        choice = get_validated_input("Select option (1-5, b)", ["1", "2", "3", "4", "5", "b"])
        
        if choice == "b":
            return
            
        if choice == "1":
            print_info("Select color scheme:")
            print_option("1", "Monochromatic")
            print_option("2", "Complementary")
            print_option("3", "Analogous")
            print_option("4", "Triadic")
            print_option("5", "Split Complementary")
            print_option("6", "Tetradic")
            print_option("7", "Custom")
            print_option("b", "Back")
            
            # Removed try...except block; KeyboardInterrupt is handled globally
            scheme_choice = get_validated_input("Select color scheme (1-7, b)", ["1", "2", "3", "4", "5", "6", "7", "b"])

            if scheme_choice == "b":
                continue # Go back to the Color & Detail Settings menu

            schemes = {
                "1": "monochromatic",
                "2": "complementary",
                "3": "analogous",
                "4": "triadic",
                "5": "split_complementary",
                "6": "tetradic"
            }
            
            if scheme_choice == "7":
                custom_scheme = input("Enter custom color scheme: ").strip()
                if custom_scheme:
                    user_prefs.imagen_settings["color_settings"]["color_scheme"] = custom_scheme
                    print_success(f"Color scheme set to: {custom_scheme}")
            else:
                user_prefs.imagen_settings["color_settings"]["color_scheme"] = schemes[scheme_choice]
                print_success(f"Color scheme set to: {schemes[scheme_choice]}")
            
            user_prefs.save_preferences()
            
        elif choice == "2":
            print_info("Select palette type:")
            print_option("1", "Warm")
            print_option("2", "Cool")
            print_option("3", "Neutral")
            print_option("4", "Pastel")
            print_option("5", "Vibrant")
            print_option("6", "Muted")
            print_option("7", "Custom")
            print_option("b", "Back")
            
            # Removed try...except block; KeyboardInterrupt is handled globally
            palette_choice = get_validated_input("Select palette type (1-7, b)", ["1", "2", "3", "4", "5", "6", "7", "b"])

            if palette_choice == "b":
                continue # Go back to the Color & Detail Settings menu

            palettes = {
                "1": "warm",
                "2": "cool",
                "3": "neutral",
                "4": "pastel",
                "5": "vibrant",
                "6": "muted"
            }
            
            if palette_choice == "7":
                custom_palette = input("Enter custom palette type: ").strip()
                if custom_palette:
                    user_prefs.imagen_settings["color_settings"]["palette_type"] = custom_palette
                    print_success(f"Palette type set to: {custom_palette}")
            else:
                user_prefs.imagen_settings["color_settings"]["palette_type"] = palettes[palette_choice]
                print_success(f"Palette type set to: {palettes[palette_choice]}")
            
            user_prefs.save_preferences()
            
        elif choice == "3":
            print_info("Select color temperature:")
            print_option("1", "Warm (Red/Yellow)")
            print_option("2", "Cool (Blue/Cyan)")
            print_option("3", "Neutral")
            print_option("4", "Mixed")
            print_option("5", "Custom")
            print_option("b", "Back")
            
            temp_choice = get_validated_input("Select color temperature (1-5, b)", ["1", "2", "3", "4", "5", "b"])
            
            if temp_choice == "b":
                continue # Go back to the Color & Detail Settings menu

            temperatures = {
                "1": "warm",
                "2": "cool",
                "3": "neutral",
                "4": "mixed"
            }
            
            if temp_choice == "5":
                custom_temp = input("Enter custom color temperature: ").strip()
                if custom_temp:
                    user_prefs.imagen_settings["color_settings"]["color_temperature"] = custom_temp
                    print_success(f"Color temperature set to: {custom_temp}")
            else:
                user_prefs.imagen_settings["color_settings"]["color_temperature"] = temperatures[temp_choice]
                print_success(f"Color temperature set to: {temperatures[temp_choice]}")
            
            user_prefs.save_preferences()
            
        elif choice == "4":
            print_info("Select detail level:")
            print_option("1", "Fine")
            print_option("2", "Medium")
            print_option("3", "Coarse")
            print_option("4", "None")
            print_option("5", "Custom")
            print_option("b", "Back")
            
            detail_choice = get_validated_input("Select detail level (1-5, b)", ["1", "2", "3", "4", "5", "b"])
            
            if detail_choice == "b":
                continue # Go back to the Color & Detail Settings menu

            detail_levels = {
                "1": "fine",
                "2": "medium",
                "3": "coarse",
                "4": None
            }
            
            if detail_choice == "5":
                custom_detail = input("Enter custom detail level: ").strip()
                if custom_detail:
                    user_prefs.imagen_settings["detail_settings"]["detail_level"] = custom_detail
                    print_success(f"Detail level set to: {custom_detail}")
            else:
                user_prefs.imagen_settings["detail_settings"]["detail_level"] = detail_levels[detail_choice]
                print_success(f"Detail level set to: {detail_levels[detail_choice] if detail_levels[detail_choice] else 'None'}")
            
            user_prefs.save_preferences()
            
        elif choice == "5":
            print_info("Select texture quality:")
            print_option("1", "High")
            print_option("2", "Medium")
            print_option("3", "Low")
            print_option("4", "None")
            print_option("5", "Custom")
            print_option("b", "Back")
            
            texture_choice = get_validated_input("Select texture quality (1-5, b)", ["1", "2", "3", "4", "5", "b"])
            if texture_choice == "_INTERRUPTED_":
                continue

            if texture_choice == "b":
                continue # Go back to the Color & Detail Settings menu

            texture_qualities = {
                "1": "high",
                "2": "medium",
                "3": "low",
                "4": None
            }
            
            if texture_choice == "5":
                custom_texture = input("Enter custom texture quality: ").strip()
                if custom_texture:
                    user_prefs.imagen_settings["detail_settings"]["texture_quality"] = custom_texture
                    print_success(f"Texture quality set to: {custom_texture}")
            else:
                user_prefs.imagen_settings["detail_settings"]["texture_quality"] = texture_qualities[texture_choice]
                print_success(f"Texture quality set to: {texture_qualities[texture_choice] if texture_qualities[texture_choice] else 'None'}")
            
            user_prefs.save_preferences()

def view_current_settings():
    """View all current settings."""
    while True:
        print_section("Current Settings")
        print_info("Aspect Ratio: " + user_prefs.aspect_ratio)
        
        # Display preferred genres, styles, and moods
        if user_prefs.preferred_genres:
            print_info("Preferred Genres: " + ", ".join(user_prefs.preferred_genres))
        else:
            print_info("Preferred Genres: None")
            
        if user_prefs.preferred_styles:
            print_info("Preferred Styles: " + ", ".join(user_prefs.preferred_styles))
        else:
            print_info("Preferred Styles: None")
            
        if user_prefs.preferred_moods:
            print_info("Preferred Moods: " + ", ".join(user_prefs.preferred_moods))
        else:
            print_info("Preferred Moods: None")
        
        # Display negative prompt if set
        negative_prompt = user_prefs.imagen_settings.get("negative_prompt", "")
        print_info("Negative Prompt: " + (negative_prompt if negative_prompt else "None"))
        
        # Display imagen settings (simplified)
        print_info("\nImagen Settings:")
        for category, settings in user_prefs.imagen_settings.items():
            if isinstance(settings, dict) and settings:
                print_info(f"  {category.replace('_', ' ').title()}:")
                for key, value in settings.items():
                    if value:  # Only show non-empty values
                        if isinstance(value, list):
                            print_info(f"    {key.replace('_', ' ').title()}: {', '.join(value)}")
                        else:
                            print_info(f"    {key.replace('_', ' ').title()}: {value}")
        
        print("\n")
        print_option("b", "Back")
        
        choice = get_validated_input("Select option (b)", ["b"])
        
        if choice == "b":
            return

def customize_all_parameters():
    """Customize all generation parameters."""
    while True:
        print_section("Customize All Parameters")
        print_option("1", "Aspect Ratio & Resolution")
        print_option("2", "Style Settings")
        print_option("3", "Camera Settings")
        print_option("4", "Lighting Settings")
        print_option("5", "Composition Settings")
        print_option("6", "Color Settings")
        print_option("7", "Negative Prompt")
        print_option("b", "Back")
        
        choice = get_validated_input("Select option (1-7, b)", ["1", "2", "3", "4", "5", "6", "7", "b"])
        
        if choice == "b":
            return
            
        if choice == "1":
            change_aspect_ratio()
            manage_output_quality_settings()
        elif choice == "2":
            manage_style_settings()
        elif choice == "3":
            manage_camera_settings()
        elif choice == "4":
            manage_lighting_settings()
        elif choice == "5":
            manage_composition_settings()
        elif choice == "6":
            manage_color_settings()
        elif choice == "7":
            manage_negative_prompt()

def generate_ai_preset():
    """Generate an AI-based preset using Gemini."""
    while True:
        print_section("Generate AI Preset")
        
        print_option("1", "Generate New AI Preset using Gemini")
        # Removed option 2 (Fallback)
        print_option("b", "Back")
        
        choice = get_validated_input("Select option (1, b)", ["1", "b"]) # Updated validation
        
        if choice == "b":
            return
            
        if choice == "1":
            try:
                # Ensure ai_preset_generator is importable
                from ai_preset_generator import generate_ai_preset as ai_gen_preset
                
                print_info("Attempting to generate AI preset (this may take a moment)...")
                
                # Call the modified generator function from ai_preset_generator.py
                # It now returns: path (str) if saved, None if discarded, False if failed
                result = ai_gen_preset(user_prefs)
                
                # Handle the new return types
                if isinstance(result, str):
                    # Preset was generated and saved by the user
                    print_success(f"AI preset generated and saved successfully!")
                    print_info(f"Saved to: {result}")
                    # No need to save user_prefs here anymore, as the preset is saved as a file
                elif result is None:
                    # Preset was generated but user chose not to save
                    print_info("AI preset generated but discarded by user.")
                else: # result is False
                    # Preset generation failed (API error, uniqueness issue, etc.)
                    print_warning("Failed to generate AI preset. See logs or previous messages for details.")
                    
            except ImportError:
                print_warning("AI preset generator module (ai_preset_generator.py) not found or google-generativeai is not installed.")
                print_info("Please ensure the file exists and run: pip install google-generativeai")
                # Optional: Add automatic installation prompt back if desired
            except Exception as e:
                # Catch any other unexpected errors during the process
                print_error(f"An unexpected error occurred during AI preset generation: {e}")
                logging.exception("Error in wallpaper_settings.generate_ai_preset wrapper") # Log traceback

        # Removed elif choice == "2" block entirely
                
        input("\nPress Enter to return to the AI Preset menu...") # Keep user in the menu

def reset_to_default():
    """Reset all settings to default values."""
    while True:
        print_section("Reset to Default")
        print_warning("This will reset all settings to their default values.")
        print_option("1", "Reset All Settings")
        print_option("b", "Back")
        
        choice = get_validated_input("Select option (1, b)", ["1", "b"])
        
        if choice == "b":
            return
            
        if choice == "1":
            confirmation = get_validated_input("Are you sure you want to proceed? (y/n)", ["y", "n"])
            
            if confirmation.lower() == "y":
                # Delete the existing preferences file first
                try:
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    pref_file_path = os.path.join(script_dir, "user_preferences.json")
                    if os.path.exists(pref_file_path):
                        os.remove(pref_file_path)
                        logging.info(f"Deleted existing preferences file: {pref_file_path}")
                except OSError as e:
                    logging.error(f"Error deleting preferences file: {e}")
                    print_error(f"Could not delete existing preferences file: {e}")
                    # Continue anyway, maybe it wasn't there

                # Initialize a new UserPreferences object (will now use defaults)
                global user_prefs
                user_prefs = UserPreferences()
                
                # Save the reset preferences
                user_prefs.save_preferences()
                
                print_success("All settings have been reset to default values.")
            else:
                print_info("Reset cancelled.")

def change_aspect_ratio():
    """Change the aspect ratio of generated wallpapers."""
    while True:
        print_section("Change Aspect Ratio")
        print_info(f"Current aspect ratio: {user_prefs.aspect_ratio}")
        
        print_option("1", "16:9 (Widescreen)")
        print_option("2", "16:10")
        print_option("3", "4:3 (Standard)")
        print_option("4", "21:9 (Ultrawide)")
        print_option("5", "32:9 (Super Ultrawide)")
        print_option("6", "1:1 (Square)")
        print_option("7", "9:16 (Mobile Portrait)")
        print_option("8", "Custom Aspect Ratio")
        print_option("b", "Back")
        
        choice = get_validated_input("Select aspect ratio (1-8, b)", ["1", "2", "3", "4", "5", "6", "7", "8", "b"])
        
        if choice == "b":
            return
            
        aspect_ratios = {
            "1": "16:9",
            "2": "16:10",
            "3": "4:3",
            "4": "21:9",
            "5": "32:9",
            "6": "1:1",
            "7": "9:16"
        }
        
        if choice == "8":
            custom_ratio = input("Enter custom aspect ratio (width:height): ").strip()
            if re.match(r'^\d+:\d+$', custom_ratio):
                user_prefs.aspect_ratio = custom_ratio
                print_success(f"Aspect ratio set to {custom_ratio}")
            else:
                print_error("Invalid aspect ratio format. Please use width:height (e.g., 16:9)")
        else:
            user_prefs.aspect_ratio = aspect_ratios[choice]
            print_success(f"Aspect ratio set to {aspect_ratios[choice]}")
        
        user_prefs.save_preferences()

def manage_negative_prompt():
    """Manage negative prompt settings."""
    while True:
        print_section("Negative Prompt Settings")
        print_info("Negative prompts tell the AI what NOT to include in the image.")
        
        current_negative = user_prefs.imagen_settings.get("negative_prompt", "")
        print_info(f"Current negative prompt: {current_negative if current_negative else 'None'}")
        
        print_option("1", "Set Custom Negative Prompt")
        print_option("2", "Use Default Negative Prompt")
        print_option("3", "Clear Negative Prompt")
        print_option("b", "Back")
        
        choice = get_validated_input("Select option (1-3, b)", ["1", "2", "3", "b"])
        if choice == "_INTERRUPTED_":
            return # Exit manage negative prompt

        if choice == "b":
            return
        
        if choice == "1":
            print_info("Enter your custom negative prompt (what you want to avoid in the image):")
            custom_negative = input("> ").strip()
            
            if custom_negative:
                user_prefs.imagen_settings["negative_prompt"] = custom_negative
                print_success("Custom negative prompt set successfully.")
            else:
                print_warning("Empty input. Negative prompt not changed.")
        
        elif choice == "2":
            default_negative = "ugly, disfigured, low quality, blurry, nsfw, watermark, signature, out of frame, extra limbs, poorly drawn face, twisted limbs, distorted face, bad proportions, bad anatomy"
            user_prefs.imagen_settings["negative_prompt"] = default_negative
            print_success("Default negative prompt set successfully.")
        
        elif choice == "3":
            user_prefs.imagen_settings["negative_prompt"] = ""
            print_success("Negative prompt cleared.")
        
        user_prefs.save_preferences()
