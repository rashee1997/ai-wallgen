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
from typing import Optional, Dict, List, Any, Tuple

# Local application imports
from ui_utils import (
    print_header, print_section, print_option, print_success, print_error,
    print_warning, print_info, print_prompt, get_validated_input, show_spinner,
    print_breadcrumb
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
    def __init__(self):
        """
        Initialize user preferences with default values.
        
        Sets up the initial state of user preferences with default values for all
        settings. This includes empty lists for preferred genres, styles, and moods,
        and default dictionaries for imagen_settings and wallpaper_settings.
        """
        # Initialize with default values
        self.preferred_genres = []
        self.preferred_styles = []
        self.preferred_moods = []
        self.negative_prompts = []
        
        # Default Imagen settings
        self.imagen_settings = {
            "number_of_images": 1,
            "seed": None,  # None means random seed
            "negative_prompt": "blurry, ugly, text, watermark, logo, signature, deformed, out of frame, low quality, multiple images",
            "quality_settings": {
                "resolution": "1920x1080",
                "detail_level": "rich_details",
                "rendering_quality": "photorealistic"
            },
            "style_settings": {},
            "camera_settings": {},
            "lighting_settings": {},
            "composition_settings": {},
            "color_settings": {}
        }
        
        # Default wallpaper settings
        self.wallpaper_settings = {
            "auto_set": True,
            "cache_duration": 30,  # days
            "fit_mode": "center",  # center, fit, fill, stretch, etc.
            "background_color": "#000000",
            "multi_monitor": "same",  # same, extend, etc.
            "refresh_rate": "daily"
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
                    self.preferred_genres = data["preferred_genres"]
                if "preferred_styles" in data:
                    self.preferred_styles = data["preferred_styles"]
                if "preferred_moods" in data:
                    self.preferred_moods = data["preferred_moods"]
                if "negative_prompts" in data:
                    self.negative_prompts = data["negative_prompts"]
                if "imagen_settings" in data:
                    # Merge with defaults to ensure all keys are present
                    for key, value in data["imagen_settings"].items():
                        if key in self.imagen_settings:
                            self.imagen_settings[key] = value
                if "wallpaper_settings" in data:
                    # Merge with defaults
                    for key, value in data["wallpaper_settings"].items():
                        if key in self.wallpaper_settings:
                            self.wallpaper_settings[key] = value
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
        except (IOError, OSError) as e:
            logging.error(f"Error saving preferences: {e}")

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

# Helper functions
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

def generate_random_style_mix(style_categories: Optional[List[str]] = None) -> str:
    """
    Generate a random mix of artistic styles.
    
    This function combines styles from different categories to create unique
    style combinations for image generation prompts.
    
    Args:
        style_categories (Optional[List[str]], optional): List of style categories to include.
                                                         If None, uses all available categories.
    
    Returns:
        str: A string containing a combination of artistic styles, joined with " + "
    """
    if style_categories is None:
        # Define style categories if not provided
        style_categories = {
            "traditional_art": ["art_deco", "art_nouveau", "charcoal", "expressionism", 
                               "gothic", "impressionism", "oil_painting", "pastel", 
                               "pencil_sketch", "realism", "sketch", "watercolor", "woodcut"],
            "digital_art": ["abstract", "cinematic", "cyberpunk", "digital_art", "double_exposure", 
                           "fantasy", "futurism", "glitch_art", "hyperrealism", "isometric", 
                           "landscape", "low_poly", "minimalist", "retrowave", "sci_fi",
                           "stained_glass", "steampunk", "surrealism", "vaporwave"],
            "illustration": ["anime", "cartoon", "comic_book", "divisionism", "graffiti", 
                            "ink_drawing", "line_art", "manga", "paper_cut", "pixel_art", 
                            "pointillism", "pop_art", "ukiyo_e"]
        }
    
    # Select a random category
    category = random.choice(list(style_categories.keys()))
    # Select 2-3 compatible styles from the same category
    num_styles = random.randint(2, 3)
    available_styles = style_categories[category]
    if len(available_styles) < num_styles:
        num_styles = len(available_styles)
    selected_styles = random.sample(available_styles, num_styles)
    return " + ".join(selected_styles)

# Settings management functions will be implemented here
def manage_preferences():
    """
    Display and manage user preferences through an interactive menu.
    
    This function provides a user interface for modifying various preference
    settings including genres, styles, and moods. It allows users to add,
    remove, and manage their preferred creative elements.
    """
    global user_prefs
    print_header("Wallpaper Preferences")
    
    while True:
        print_section("Options")
        print_option("1", "Manage Genres")
        print_option("2", "Manage Styles")
        print_option("3", "Manage Moods")
        print_option("4", "Manage Wallpaper Settings")
        print_option("5", "View Current Preferences")
        print_option("6", "Reset to Defaults")
        print_option("7", "Return to Main Menu")
                
        choice = get_validated_input("Select an option (1-7)", ["1", "2", "3", "4", "5", "6", "7"])
        
        if choice == "1":
            print_section("Manage Genres")
            print_info("Current preferred genres:")
            for genre in user_prefs.preferred_genres:
                print_info(f"- {genre}")
            
            print_info("\nAvailable genres:")
            for i, genre in enumerate(available_genres, 1):
                print_option(str(i), genre)
            
            print_option("a", "Add genre")
            print_option("r", "Remove genre")
            print_option("c", "Clear all")
            print_option("b", "Back")
            
            action = get_validated_input("Select action", ["a", "r", "c", "b"] + [str(i) for i in range(1, len(available_genres) + 1)])
            
            if action == "a":
                genre = input("Enter genre to add: ").strip()
                if genre in available_genres and genre not in user_prefs.preferred_genres:
                    user_prefs.preferred_genres.append(genre)
                    print_success(f"Added genre: {genre}")
                else:
                    print_warning("Invalid genre or already in preferences")
            elif action == "r":
                if user_prefs.preferred_genres:
                    print_info("Select genre to remove:")
                    for i, genre in enumerate(user_prefs.preferred_genres, 1):
                        print_option(str(i), genre)
                    idx = int(get_validated_input("Enter number", [str(i) for i in range(1, len(user_prefs.preferred_genres) + 1)])) - 1
                    removed = user_prefs.preferred_genres.pop(idx)
                    print_success(f"Removed genre: {removed}")
                else:
                    print_warning("No genres to remove")
            elif action == "c":
                user_prefs.preferred_genres.clear()
                print_success("Cleared all genres")
            elif action == "b":
                continue
            else:
                idx = int(action) - 1
                if 0 <= idx < len(available_genres):
                    genre = available_genres[idx]
                    if genre not in user_prefs.preferred_genres:
                        user_prefs.preferred_genres.append(genre)
                        print_success(f"Added genre: {genre}")
                    else:
                        print_warning("Genre already in preferences")
        
        elif choice == "2":
            print_section("Manage Styles")
            print_info("Current preferred styles:")
            for style in user_prefs.preferred_styles:
                print_info(f"- {style}")
            
            print_info("\nAvailable styles:")
            style_options = ["abstract", "anime", "art_deco", "art_nouveau", "cartoon", "charcoal", 
                           "cinematic", "comic_book", "constructivism", "cubism", "cyberpunk", 
                           "digital_art", "divisionism", "double_exposure", "expressionism", 
                           "fantasy", "futurism", "glitch_art", "gothic", "graffiti", 
                           "hyperrealism", "impressionism", "ink_drawing", "isometric", "landscape", 
                           "line_art", "low_poly", "manga", "minimalist", "oil_painting", 
                           "paper_cut", "pastel", "pencil_sketch", "photograph", "pixel_art", 
                           "pointillism", "pop_art", "realism", "retrowave", "sci_fi", 
                           "sketch", "stained_glass", "steampunk", "surrealism", "ukiyo_e", 
                           "vaporwave", "watercolor", "woodcut"]
            
            # Group styles by compatibility for random mixing
            style_categories = {
                "traditional_art": ["art_deco", "art_nouveau", "charcoal", "expressionism", 
                                   "gothic", "impressionism", "oil_painting", "pastel", 
                                   "pencil_sketch", "realism", "sketch", "watercolor", "woodcut"],
                "digital_art": ["abstract", "cinematic", "cyberpunk", "digital_art", "double_exposure", 
                               "fantasy", "futurism", "glitch_art", "hyperrealism", "isometric", 
                               "landscape", "low_poly", "minimalist", "retrowave", "sci_fi",
                               "stained_glass", "steampunk", "surrealism", "vaporwave"],
                "illustration": ["anime", "cartoon", "comic_book", "divisionism", "graffiti", 
                                "ink_drawing", "line_art", "manga", "paper_cut", "pixel_art", 
                                "pointillism", "pop_art", "ukiyo_e"]
            }
            
            for i, style in enumerate(style_options, 1):
                print_option(str(i), style)
            
            print_option(str(len(style_options) + 1), "Random Style Mix (combines 2-3 compatible styles)")
            print_option("a", "Add style")
            print_option("r", "Remove style")
            print_option("c", "Clear all")
            print_option("b", "Back")
            
            style_choice = get_validated_input("Select an option", 
                                              [str(i) for i in range(1, len(style_options) + 2)] + ["a", "r", "c", "b"])
            
            if style_choice == "b":
                continue
            elif style_choice == "a":
                style = input("Enter style to add: ").strip()
                if style:
                    if style not in user_prefs.preferred_styles:
                        user_prefs.preferred_styles.append(style)
                        user_prefs.save_preferences()
                        print_success(f"Added '{style}' to preferred styles")
                    else:
                        print_warning(f"'{style}' is already in your preferred styles")
            elif style_choice == "r":
                if not user_prefs.preferred_styles:
                    print_warning("You don't have any preferred styles to remove")
                    continue
                
                print_info("Select style to remove:")
                for i, style in enumerate(user_prefs.preferred_styles, 1):
                    print_option(str(i), style)
                
                remove_choice = get_validated_input("Select style to remove (or 'c' to cancel)", 
                                                   [str(i) for i in range(1, len(user_prefs.preferred_styles) + 1)] + ["c"])
                
                if remove_choice == "c":
                    continue
                
                style_to_remove = user_prefs.preferred_styles[int(remove_choice) - 1]
                user_prefs.preferred_styles.remove(style_to_remove)
                user_prefs.save_preferences()
                print_success(f"Removed '{style_to_remove}' from preferred styles")
            elif style_choice == "c":
                confirm = get_validated_input("Are you sure you want to clear all styles? (y/n)", ["y", "n"])
                if confirm == "y":
                    user_prefs.preferred_styles.clear()
                    user_prefs.save_preferences()
                    print_success("Cleared all preferred styles")
            elif style_choice == str(len(style_options) + 1):
                # Random style mix option
                style_mix = generate_random_style_mix(style_categories)
                print_info(f"Generated random style mix: {style_mix}")
                add_to_preferences = get_validated_input("Add this mix to your preferred styles? (y/n)", ["y", "n"])
                if add_to_preferences == "y":
                    if style_mix not in user_prefs.preferred_styles:
                        user_prefs.preferred_styles.append(style_mix)
                        user_prefs.save_preferences()
                        print_success(f"Added '{style_mix}' to preferred styles")
                    else:
                        print_warning(f"'{style_mix}' is already in your preferred styles")
            else:
                # Add the selected style from the list
                try:
                    selected_style = style_options[int(style_choice) - 1]
                    if selected_style not in user_prefs.preferred_styles:
                        user_prefs.preferred_styles.append(selected_style)
                        user_prefs.save_preferences()
                        print_success(f"Added '{selected_style}' to preferred styles")
                    else:
                        print_warning(f"'{selected_style}' is already in your preferred styles")
                except (ValueError, IndexError):
                    print_error(f"Invalid selection: {style_choice}")
        
        elif choice == "3":
            print_section("Manage Moods")
            print_info("Current preferred moods:")
            for mood in user_prefs.preferred_moods:
                print_info(f"- {mood}")
            
            print_info("\nAvailable moods:")
            mood_options = ["peaceful", "dramatic", "mysterious", "energetic", "melancholic",
                          "joyful", "romantic", "eerie", "nostalgic", "contemplative"]
            for i, mood in enumerate(mood_options, 1):
                print_option(str(i), mood)
            
            print_option("a", "Add mood")
            print_option("r", "Remove mood")
            print_option("c", "Clear all")
            print_option("b", "Back")
            
            action = get_validated_input("Select action", ["a", "r", "c", "b"] + [str(i) for i in range(1, len(mood_options) + 1)])
            
            if action == "a":
                mood = input("Enter mood to add: ").strip()
                if mood in mood_options and mood not in user_prefs.preferred_moods:
                    user_prefs.preferred_moods.append(mood)
                    print_success(f"Added mood: {mood}")
                else:
                    print_warning("Invalid mood or already in preferences")
            elif action == "r":
                if user_prefs.preferred_moods:
                    print_info("Select mood to remove:")
                    for i, mood in enumerate(user_prefs.preferred_moods, 1):
                        print_option(str(i), mood)
                    idx = int(get_validated_input("Enter number", [str(i) for i in range(1, len(user_prefs.preferred_moods) + 1)])) - 1
                    removed = user_prefs.preferred_moods.pop(idx)
                    print_success(f"Removed mood: {removed}")
                else:
                    print_warning("No moods to remove")
            elif action == "c":
                user_prefs.preferred_moods.clear()
                print_success("Cleared all moods")
            elif action == "b":
                continue
            else:
                idx = int(action) - 1
                if 0 <= idx < len(mood_options):
                    mood = mood_options[idx]
                    if mood not in user_prefs.preferred_moods:
                        user_prefs.preferred_moods.append(mood)
                        print_success(f"Added mood: {mood}")
                    else:
                        print_warning("Mood already in preferences")
        
        elif choice == "4":
            print_section("Wallpaper Settings")
            print_option("1", "Auto-set wallpaper")
            print_option("2", "Cache duration")
            print_option("3", "Fit mode")
            print_option("4", "Background color")
            print_option("5", "Multi-monitor mode")
            print_option("6", "Refresh rate")
            print_option("7", "Back")
            
            setting_choice = get_validated_input("Select setting to configure (1-7)", ["1", "2", "3", "4", "5", "6", "7"])
            
            if setting_choice == "1":
                print_info("Auto-set wallpaper after generation")
                print_option("1", "Enabled")
                print_option("2", "Disabled")
                auto_set = get_validated_input("Select option (1-2)", ["1", "2"])
                user_prefs.wallpaper_settings["auto_set"] = (auto_set == "1")
                print_success(f"Auto-set wallpaper {'enabled' if user_prefs.wallpaper_settings['auto_set'] else 'disabled'}")
            
            elif setting_choice == "2":
                print_info("Set cache duration (days)")
                try:
                    days = int(input("Enter number of days (1-365): ").strip())
                    days = max(1, min(365, days))
                    user_prefs.wallpaper_settings["cache_duration"] = days
                    print_success(f"Cache duration set to {days} days")
                except ValueError:
                    print_warning("Invalid input. Using default value.")
            
            elif setting_choice == "3":
                print_info("Select wallpaper fit mode")
                print_option("1", "Fill (stretch to fill)")
                print_option("2", "Fit (maintain aspect ratio)")
                print_option("3", "Center (no scaling)")
                print_option("4", "Tile (repeat pattern)")
                fit_mode = get_validated_input("Select option (1-4)", ["1", "2", "3", "4"])
                modes = ["fill", "fit", "center", "tile"]
                user_prefs.wallpaper_settings["fit_mode"] = modes[int(fit_mode) - 1]
                print_success(f"Fit mode set to {user_prefs.wallpaper_settings['fit_mode']}")
            
            elif setting_choice == "4":
                print_info("Set background color (hex format)")
                print_info("Example: #000000 for black")
                color = input("Enter hex color code: ").strip()
                if color.startswith("#") and len(color) == 7:
                    try:
                        int(color[1:], 16)  # Validate hex
                        user_prefs.wallpaper_settings["background_color"] = color
                        print_success(f"Background color set to {color}")
                    except ValueError:
                        print_warning("Invalid hex color code")
                else:
                    print_warning("Invalid color format")
            
            elif setting_choice == "5":
                print_info("Select multi-monitor mode")
                print_option("1", "Mirror (same wallpaper on all monitors)")
                print_option("2", "Extend (different wallpapers)")
                print_option("3", "Individual (customize per monitor)")
                monitor_mode = get_validated_input("Select option (1-3)", ["1", "2", "3"])
                modes = ["mirror", "extend", "individual"]
                user_prefs.wallpaper_settings["multi_monitor"] = modes[int(monitor_mode) - 1]
                print_success(f"Multi-monitor mode set to {user_prefs.wallpaper_settings['multi_monitor']}")
            
            elif setting_choice == "6":
                print_info("Select wallpaper refresh rate")
                print_option("1", "Daily")
                print_option("2", "Weekly")
                print_option("3", "Monthly")
                print_option("4", "Never")
                refresh_rate = get_validated_input("Select option (1-4)", ["1", "2", "3", "4"])
                rates = ["daily", "weekly", "monthly", "never"]
                user_prefs.wallpaper_settings["refresh_rate"] = rates[int(refresh_rate) - 1]
                print_success(f"Refresh rate set to {user_prefs.wallpaper_settings['refresh_rate']}")
        
        elif choice == "5":
            print_section("Current Preferences")
            print_info("Preferred Genres:")
            for genre in user_prefs.preferred_genres:
                print_info(f"- {genre}")
            
            print_info("\nPreferred Styles:")
            for style in user_prefs.preferred_styles:
                print_info(f"- {style}")
            
            print_info("\nPreferred Moods:")
            for mood in user_prefs.preferred_moods:
                print_info(f"- {mood}")
            
            print_info("\nWallpaper Settings:")
            print_info(f"- Auto-set: {'Enabled' if user_prefs.wallpaper_settings['auto_set'] else 'Disabled'}")
            print_info(f"- Cache Duration: {user_prefs.wallpaper_settings['cache_duration']} days")
            print_info(f"- Fit Mode: {user_prefs.wallpaper_settings['fit_mode']}")
            print_info(f"- Background Color: {user_prefs.wallpaper_settings['background_color']}")
            print_info(f"- Multi-monitor Mode: {user_prefs.wallpaper_settings['multi_monitor']}")
            print_info(f"- Refresh Rate: {user_prefs.wallpaper_settings['refresh_rate']}")
        
        elif choice == "6":
            print_section("Reset to Defaults")
            confirm = get_validated_input("Are you sure you want to reset all preferences? (yes/no)", ["yes", "no"])
            if confirm == "yes":
                user_prefs.preferred_genres = []
                user_prefs.preferred_styles = ["photograph"]  # Default to photograph style
                user_prefs.preferred_moods = []
                user_prefs.wallpaper_settings = {
                    "auto_set": True,
                    "cache_duration": 30,
                    "fit_mode": "fill",
                    "background_color": "#000000",
                    "multi_monitor": "mirror",
                    "refresh_rate": "daily"
                }
                user_prefs.save_preferences()
                print_success("All preferences reset to defaults")
        
        elif choice == "7":
            break
        
        user_prefs.save_preferences()

# Preset management functions will be implemented here
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
        
        print_option("1", "Save Current Settings as Preset")
        print_option("2", "Load Preset")
        print_option("3", "Delete Preset")
        print_option("4", "View Current Preset Details")
        print_option("5", "Back to Main Menu")
        
        choice = get_validated_input("Select option (1-5)", ["1", "2", "3", "4", "5"])
        
        if choice == "1":
            # Get preset name from user
            preset_name = get_validated_input("Enter preset name (or 'b' to go back)", allow_empty=False)
            if preset_name.lower() == 'b':
                continue
                
            # Validate preset name
            if not preset_name.strip() or any(c in r'\/:*?"<>|' for c in preset_name):
                print_error("Invalid preset name. Please avoid special characters.")
                continue
                
            # Check if preset already exists
            if os.path.exists(os.path.join("presets", f"{preset_name}.json")):
                confirm = get_validated_input(f"Preset '{preset_name}' already exists. Overwrite? (y/n)", ["y", "n"])
                if confirm.lower() != "y":
                    continue
            
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
            
        elif choice == "2":
            # Load preset
            result = load_preset()
            if result:
                settings, preset_name = result  # Unpack the returned tuple
                try:
                    print_section("Load Settings")
                    print_option("1", "Replace current settings with preset")
                    print_option("2", "Merge preset with current settings")
                    print_option("b", "Back")
                    
                    load_choice = get_validated_input("Select option (1-2 or b)", ["1", "2", "b"])
                    if load_choice == "b":
                        continue
                    
                    if load_choice == "1":
                        # Replace settings completely
                        if "imagen_settings" in settings and hasattr(user_prefs, 'imagen_settings'):
                            user_prefs.imagen_settings = settings["imagen_settings"].copy()
                        if "wallpaper_settings" in settings and hasattr(user_prefs, 'wallpaper_settings'):
                            user_prefs.wallpaper_settings = settings["wallpaper_settings"].copy()
                        print_success("Settings replaced with preset")
                    else:
                        # Merge settings (update existing)
                        if "imagen_settings" in settings and hasattr(user_prefs, 'imagen_settings'):
                            user_prefs.imagen_settings.update(settings["imagen_settings"])
                        if "wallpaper_settings" in settings and hasattr(user_prefs, 'wallpaper_settings'):
                            user_prefs.wallpaper_settings.update(settings["wallpaper_settings"])
                        print_success("Settings merged with preset")
                    
                    # Update current preset name
                    user_prefs.last_preset = preset_name
                    user_prefs.save_preferences()
                    
                except Exception as e:
                    print_error(f"Error applying preset settings: {e}")
            
        elif choice == "3":
            delete_preset()
            # If deleted preset was current, clear current preset
            if current_preset and not os.path.exists(os.path.join("presets", f"{current_preset}.json")):
                user_prefs.last_preset = None
                user_prefs.save_preferences()
            
        elif choice == "4":
            # View current preset details
            if not current_preset:
                print_warning("No preset currently loaded")
                continue
                
            print_section(f"Current Preset: {current_preset}")
            try:
                preset_file = os.path.join("presets", f"{current_preset}.json")
                if os.path.exists(preset_file):
                    with open(preset_file) as f:
                        settings = json.load(f)
                        
                    # Display metadata if available
                    if "metadata" in settings:
                        print_info("Metadata:")
                        for key, value in settings["metadata"].items():
                            print_info(f"  {key}: {value}")
                        print()
                        
                    # Display imagen settings
                    if "imagen_settings" in settings:
                        print_info("Imagen Settings:")
                        for key, value in settings["imagen_settings"].items():
                            if isinstance(value, dict):
                                print_info(f"  {key}:")
                                for k, v in value.items():
                                    print_info(f"    {k}: {v}")
                            else:
                                print_info(f"  {key}: {value}")
                        print()
                        
                    # Display wallpaper settings
                    if "wallpaper_settings" in settings:
                        print_info("Wallpaper Settings:")
                        for key, value in settings["wallpaper_settings"].items():
                            print_info(f"  {key}: {value}")
                    
                    input("\nPress Enter to continue...")
                else:
                    print_error(f"Preset file not found: {preset_file}")
            except Exception as e:
                print_error(f"Error reading preset details: {e}")
            
        else:  # choice == "5"
            return

def load_preset() -> bool:
    """
    Load a preset from a file and apply it to the current user preferences.
    
    This function displays available presets, allows the user to select one,
    and then applies the selected preset either by replacing or merging with
    the current settings.
    
    Returns:
        bool: True if a preset was successfully loaded, False otherwise
    """
    if not os.path.exists("presets"):
        os.makedirs("presets")
    
    presets = [f for f in os.listdir("presets") if f.endswith(".json")]
    if not presets:
        print_warning("No saved presets found")
        return False
    
    print_section("Available Presets")
    for i, preset in enumerate(presets, 1):
        print_option(str(i), preset.replace(".json", ""))
    print_option("b", "Back")
    
    choice = get_validated_input("Select preset to load", ["b"] + [str(i) for i in range(1, len(presets) + 1)])
    if choice == "b":
        return False
    
    preset_file = presets[int(choice) - 1]
    preset_name = os.path.splitext(preset_file)[0]
    
    try:
        with open(os.path.join("presets", preset_file)) as f:
            settings = json.load(f)
        return settings, preset_name
    except Exception as e:
        print_error(f"Error loading preset: {e}")
        return False

def save_preset(settings: Dict[str, Any], name: str) -> bool:
    """
    Save the current settings as a preset.
    
    This function takes the current settings and saves them to a file in the
    presets directory with the given name.
    
    Args:
        settings (Dict[str, Any]): The settings to save
        name (str): The name to give the preset
    
    Returns:
        bool: True if the preset was successfully saved, False otherwise
    """
    if not os.path.exists("presets"):
        try:
            os.makedirs("presets")
            print_info("Created presets directory")
        except Exception as e:
            print_error(f"Error creating presets directory: {e}")
            return False
    
    filename = f"{name}.json"
    temp_file = os.path.join("presets", f"{filename}.tmp")
    final_file = os.path.join("presets", filename)
    
    print_info(f"Saving preset to {final_file}")
    
    try:
        # First write to a temporary file
        with open(temp_file, "w") as f:
            json.dump(settings, f, indent=4)
            f.flush()
            os.fsync(f.fileno())  # Ensure data is written to disk
            
        print_info("Temporary file written successfully")
            
        # If successful, rename to final filename (atomic operation)
        if os.path.exists(final_file):
            backup_file = os.path.join("presets", f"{filename}.bak")
            if os.path.exists(backup_file):
                os.remove(backup_file)
                print_info("Removed old backup file")
            os.rename(final_file, backup_file)
            print_info("Created backup of existing preset")
            
        os.rename(temp_file, final_file)
        print_info("Renamed temporary file to final preset file")
        return True
        
    except Exception as e:
        print_error(f"Error saving preset: {e}")
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
                print_info("Cleaned up temporary file after error")
            except:
                pass
        return False

def delete_preset() -> bool:
    """
    Delete a preset file.
    
    This function displays available presets, allows the user to select one,
    and then deletes the selected preset file after confirmation.
    
    Returns:
        bool: True if a preset was successfully deleted, False otherwise
    """
    if not os.path.exists("presets"):
        os.makedirs("presets")
    
    presets = [f for f in os.listdir("presets") if f.endswith(".json")]
    if not presets:
        print_warning("No saved presets found")
        return False
    
    print_section("Available Presets")
    for i, preset in enumerate(presets, 1):
        print_option(str(i), preset.replace(".json", ""))
    print_option("b", "Back")
    
    choice = get_validated_input("Select preset to delete", ["b"] + [str(i) for i in range(1, len(presets) + 1)])
    if choice == "b":
        return False
    
    preset_file = presets[int(choice) - 1]
    preset_name = os.path.splitext(preset_file)[0]
    
    confirm = get_validated_input(f"Are you sure you want to delete preset '{preset_name}'? (y/n)", ["y", "n"])
    if confirm.lower() != "y":
        print_info("Deletion cancelled")
        return False
    
    try:
        os.remove(os.path.join("presets", preset_file))
        print_success(f"Preset '{preset_name}' deleted")
        return True
    except Exception as e:
        print_error(f"Error deleting preset: {e}")
        return False

# Settings import/export functions will be implemented here 
def export_settings() -> str:
    """
    Export user settings to a JSON file.
    
    This function saves the current user preferences and imagen settings to a
    JSON file, creating a backup that can be later imported.
    
    Returns:
        str: The path to the exported settings file, or empty string if export failed
    """
    print_section("Export Settings")
    try:
        filename = get_validated_input("Enter filename for export (without extension)", allow_empty=False)
        filename = f"{filename}.json"
        
        settings = {
            "preferences": user_prefs.__dict__,
            "imagen_settings": user_prefs.imagen_settings,
            "export_date": datetime.now().isoformat()
        }
        
        with open(filename, "w") as f:
            json.dump(settings, f, indent=4)
        print_success(f"Settings exported to {filename}")
        return filename
    except Exception as e:
        print_error(f"Error exporting settings: {e}")
        return ""

def import_settings() -> bool:
    """
    Import user settings from a JSON file.
    
    This function loads user preferences and imagen settings from a previously
    exported JSON file and applies them to the current user preferences.
    
    Returns:
        bool: True if settings were successfully imported, False otherwise
    """
    print_section("Import Settings")
    try:
        filename = get_validated_input("Enter filename to import (with extension)", allow_empty=False)
        if not os.path.exists(filename):
            print_error("File not found")
            return False
        
        with open(filename) as f:
            settings = json.load(f)
        
        # Update preferences
        for key, value in settings["preferences"].items():
            setattr(user_prefs, key, value)
        
        # Update imagen settings
        user_prefs.imagen_settings.update(settings["imagen_settings"])
        
        user_prefs.save_preferences()
        print_success("Settings imported successfully")
        return True
    except Exception as e:
        print_error(f"Error importing settings: {e}")
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
    """
    Display and manage Imagen model settings through an interactive menu.
    
    This function provides a user interface for modifying various image generation
    settings including number of images, seed, resolution, and model-specific parameters.
    """
    global user_prefs
    print_header("Imagen 3 Settings")
    
    while True:
        print_section("Options")
        print_option("1", "View Current Settings")
        print_option("2", "Number of Images")
        print_option("3", "Seed")
        print_option("4", "Negative Prompt")
        print_option("5", "Quality Settings")
        print_option("6", "Reset to Defaults")
        print_option("7", "Return to Main Menu")
        
        choice = get_validated_input("Select an option (1-7)", ["1", "2", "3", "4", "5", "6", "7"])
        
        if choice == "1":
            print_section("Current Settings")
            print_info(f"Number of Images: {user_prefs.imagen_settings.get('number_of_images', 1)}")
            print_info(f"Seed: {user_prefs.imagen_settings.get('seed') or 'Random'}")
            print_info(f"Negative Prompt: {user_prefs.imagen_settings.get('negative_prompt', '') or 'None'}")
            
            # Display quality settings if they exist
            quality_settings = user_prefs.imagen_settings.get('quality_settings', {})
            if quality_settings:
                print_info("\nQuality Settings:")
                print_info(f"  Resolution: {quality_settings.get('resolution', '1920x1080')}")
                print_info(f"  Detail Level: {quality_settings.get('detail_level', 'medium_detail')}")
                print_info(f"  Rendering Quality: {quality_settings.get('rendering_quality', 'medium_quality')}")
            
            input("\nPress Enter to continue...")
            
        elif choice == "2":
            print_section("Number of Images")
            print_info("Set the number of images to generate (1-4)")
            try:
                num = input("Enter number of images: ").strip()
                num = int(num)
                if 1 <= num <= 4:
                    user_prefs.imagen_settings["number_of_images"] = num
                    print_success(f"Number of images set to {num}")
                else:
                    print_warning("Value must be between 1 and 4. Setting to 1.")
                    user_prefs.imagen_settings["number_of_images"] = 1
            except ValueError:
                print_warning("Invalid input. Setting to default (1).")
                user_prefs.imagen_settings["number_of_images"] = 1
            
            user_prefs.save_preferences()
            
        elif choice == "3":
            print_section("Generation Seed")
            print_info("Set a seed for reproducible results")
            print_info("Leave empty for random seed")
            
            seed_input = input("Enter seed (integer) or leave empty: ").strip()
            if not seed_input:
                user_prefs.imagen_settings["seed"] = None
                print_success("Seed set to random")
            else:
                try:
                    seed = int(seed_input)
                    user_prefs.imagen_settings["seed"] = seed
                    print_success(f"Seed set to {seed}")
                except ValueError:
                    print_warning("Invalid input. Setting to random.")
                    user_prefs.imagen_settings["seed"] = None
            
            user_prefs.save_preferences()
            
        elif choice == "4":
            print_section("Negative Prompt")
            print_info("Set negative prompt (things to exclude from generation)")
            
            current = user_prefs.imagen_settings.get("negative_prompt", "")
            print_info(f"Current negative prompt: {current or 'None'}")
            
            negative_prompt = input("Enter negative prompt or leave empty to clear: ").strip()
            user_prefs.imagen_settings["negative_prompt"] = negative_prompt
            
            if negative_prompt:
                print_success(f"Negative prompt set to: {negative_prompt}")
            else:
                print_success("Negative prompt cleared")
            
            user_prefs.save_preferences()
            
        elif choice == "5":
            manage_quality_settings()
            
        elif choice == "6":
            print_section("Reset to Defaults")
            confirm = get_validated_input("Are you sure you want to reset Imagen settings? (yes/no)", ["yes", "no"])
            if confirm == "yes":
                user_prefs.imagen_settings = {
                    "number_of_images": 1,
                    "seed": None,
                    "negative_prompt": "",
                    "quality_settings": {
                        "resolution": "1920x1080",
                        "detail_level": "medium_detail",
                        "rendering_quality": "medium_quality"
                    }
                }
                user_prefs.save_preferences()
                print_success("Settings reset to defaults")
            
        elif choice == "7":
            return
        
def manage_quality_settings():
    """
    Display and manage image quality settings through an interactive menu.
    
    This function provides a user interface for modifying various quality-related
    settings including resolution, detail level, and rendering quality.
    """
    global user_prefs
    
    # Ensure quality_settings exists in imagen_settings
    if "quality_settings" not in user_prefs.imagen_settings:
        user_prefs.imagen_settings["quality_settings"] = {
            "resolution": "1920x1080",
            "detail_level": "medium_detail",
            "rendering_quality": "medium_quality"
        }
    
    while True:
        print_section("Quality Settings")
        print_option("1", "Resolution")
        print_option("2", "Detail Level")
        print_option("3", "Rendering Quality")
        print_option("4", "Return")
        
        quality_choice = get_validated_input("Select option (1-4)", ["1", "2", "3", "4"])
        
        if quality_choice == "4":
            return
            
        if quality_choice == "1":
            print_info("Select resolution:")
            print_option("1", "1920x1080 (Full HD)")
            print_option("2", "2560x1440 (2K)")
            print_option("3", "3840x2160 (4K)")
            print_option("4", "5120x2880 (5K)")
            print_option("5", "7680x4320 (8K)")
            print_option("6", "Custom")
            
            res_choice = get_validated_input("Select resolution (1-6)", ["1", "2", "3", "4", "5", "6"])
            
            if res_choice == "6":
                custom_res = input("Enter custom resolution (e.g., 1920x1080): ").strip()
                if "x" in custom_res:
                    user_prefs.imagen_settings["quality_settings"]["resolution"] = custom_res
                    print_success(f"Custom resolution set to: {custom_res}")
                else:
                    print_warning("Invalid format. Using default 1920x1080.")
                    user_prefs.imagen_settings["quality_settings"]["resolution"] = "1920x1080"
            else:
                resolutions = {
                    "1": "1920x1080",
                    "2": "2560x1440",
                    "3": "3840x2160", 
                    "4": "5120x2880",
                    "5": "7680x4320"
                }
                
                user_prefs.imagen_settings["quality_settings"]["resolution"] = resolutions[res_choice]
                print_success(f"Resolution set to {resolutions[res_choice]}")
            
        elif quality_choice == "2":
            print_info("Select detail level:")
            print_option("1", "Ultra Detailed")
            print_option("2", "High Detail")
            print_option("3", "Medium Detail")
            print_option("4", "Low Detail")
            print_option("5", "Custom")
            
            detail_choice = get_validated_input("Select detail level (1-5)", ["1", "2", "3", "4", "5"])
            
            if detail_choice == "5":
                custom_detail = input("Enter custom detail level: ").strip()
                if custom_detail:
                    user_prefs.imagen_settings["quality_settings"]["detail_level"] = custom_detail
                    print_success(f"Custom detail level set to: {custom_detail}")
                else:
                    print_warning("Invalid input. Using medium_detail.")
                    user_prefs.imagen_settings["quality_settings"]["detail_level"] = "medium_detail"
            else:
                detail_levels = {
                    "1": "ultra_detailed",
                    "2": "high_detail",
                    "3": "medium_detail",
                    "4": "low_detail"
                }
                
                user_prefs.imagen_settings["quality_settings"]["detail_level"] = detail_levels[detail_choice]
                print_success(f"Detail level set to {detail_levels[detail_choice]}")
            
        elif quality_choice == "3":
            print_info("Select rendering quality:")
            print_option("1", "Photorealistic")
            print_option("2", "High Quality")
            print_option("3", "Medium Quality")
            print_option("4", "Custom")
            
            render_choice = get_validated_input("Select rendering quality (1-4)", ["1", "2", "3", "4"])
            
            if render_choice == "4":
                custom_render = input("Enter custom rendering quality: ").strip()
                if custom_render:
                    user_prefs.imagen_settings["quality_settings"]["rendering_quality"] = custom_render
                    print_success(f"Custom rendering quality set to: {custom_render}")
                else:
                    print_warning("Invalid input. Using medium_quality.")
                    user_prefs.imagen_settings["quality_settings"]["rendering_quality"] = "medium_quality"
            else:
                render_qualities = {
                    "1": "photorealistic",
                    "2": "high_quality",
                    "3": "medium_quality"
                }
                
                user_prefs.imagen_settings["quality_settings"]["rendering_quality"] = render_qualities[render_choice]
                print_success(f"Rendering quality set to {render_qualities[render_choice]}")
        
        user_prefs.save_preferences()

def configure_advanced_options():
    """
    Display and manage advanced configuration options through an interactive menu.
    
    This function provides a user interface for modifying advanced options
    including negative prompts, advanced settings categories, and other
    specialized configuration options.
    """
    global user_prefs
    print_section("Advanced Options")
    print_info("Fine-tune the generation parameters:")
    
    while True:
        print_option("1", "Style & Artistic Settings")
        print_option("2", "Camera & Technical Settings")
        print_option("3", "Lighting & Atmosphere")
        print_option("4", "Composition & Environment")
        print_option("5", "Color & Detail Settings")
        print_option("6", "Show Current Settings")
        print_option("7", "Return to previous menu")
        
        advanced_choice = get_validated_input("Select option (1-7)", ["1", "2", "3", "4", "5", "6", "7"])
        
        if advanced_choice == "1":
            manage_style_settings()
        elif advanced_choice == "2":
            manage_camera_settings()
        elif advanced_choice == "3":
            manage_lighting_settings()
        elif advanced_choice == "4":
            manage_composition_settings()
        elif advanced_choice == "5":
            manage_color_settings()
        elif advanced_choice == "6":
            show_advanced_settings()
        elif advanced_choice == "7":
            return

def manage_style_settings():
    """
    Display and manage style settings through an interactive menu.
    
    This function provides a user interface for modifying various style-related
    settings including artistic styles, visual treatments, and aesthetic preferences.
    """
    global user_prefs
    # Ensure style_settings exists
    if "style_settings" not in user_prefs.imagen_settings:
        user_prefs.imagen_settings["style_settings"] = {
            "art_movement": "Abstract Expressionism",
            "post_processing": []
        }
    
    print_section("Style & Artistic Settings")
    print_info("Choose the artistic style and style-specific settings:")
    
    while True:
        print_option("1", "Art Movement")
        print_option("2", "Post-processing Effects")
        print_option("3", "Return")
        
        style_choice = get_validated_input("Select option (1-3)", ["1", "2", "3"])
        
        if style_choice == "3":
            return
            
        if style_choice == "1":
            print_info("Select art movement:")
            print_option("1", "Abstract Expressionism")
            print_option("2", "Impressionism")
            print_option("3", "Surrealism")
            print_option("4", "Minimalism")
            print_option("5", "Cubism")
            print_option("6", "Custom")
            
            movement_choice = get_validated_input("Select movement (1-6)", ["1", "2", "3", "4", "5", "6"])
            
            if movement_choice == "6":
                custom_movement = input("Enter custom art movement: ").strip()
                if custom_movement:
                    user_prefs.imagen_settings["style_settings"]["art_movement"] = custom_movement
                    print_success(f"Custom art movement set to: {custom_movement}")
            else:
                movements = {
                    "1": "Abstract Expressionism",
                    "2": "Impressionism",
                    "3": "Surrealism",
                    "4": "Minimalism",
                    "5": "Cubism"
                }
                
                user_prefs.imagen_settings["style_settings"]["art_movement"] = movements[movement_choice]
                print_success(f"Art movement set to {movements[movement_choice]}")
                
        elif style_choice == "2":
            print_info("Select post-processing effects (comma-separated):")
            print_option("1", "Vintage")
            print_option("2", "HDR")
            print_option("3", "Film Grain")
            print_option("4", "Color Grading")
            print_option("5", "Custom")
            print_option("6", "None/Clear")
            
            effects_choice = get_validated_input("Select option (1-6)", ["1", "2", "3", "4", "5", "6"])
            
            if effects_choice == "5":
                custom_effects = input("Enter custom effects (comma-separated): ").strip()
                if custom_effects:
                    user_prefs.imagen_settings["style_settings"]["post_processing"] = [e.strip() for e in custom_effects.split(",")]
                    print_success(f"Custom effects set to: {custom_effects}")
            elif effects_choice == "6":
                user_prefs.imagen_settings["style_settings"]["post_processing"] = []
                print_success("Post-processing effects cleared")
            else:
                effects = {
                    "1": ["vintage"],
                    "2": ["hdr"],
                    "3": ["film_grain"],
                    "4": ["color_grading"]
                }
                
                user_prefs.imagen_settings["style_settings"]["post_processing"] = effects[effects_choice]
                print_success(f"Post-processing effects set to {effects[effects_choice]}")
        
        user_prefs.save_preferences()

# Additional helper functions would be implemented here
# These functions would handle camera settings, lighting settings, etc.
# For brevity, they are not included in this implementation
def show_advanced_settings():
    """
    Display detailed information about advanced settings.
    
    This function shows a comprehensive overview of all advanced settings
    categories and their current values.
    """
    print_section("Current Advanced Settings")
    
    # Display style settings
    style_settings = user_prefs.imagen_settings.get("style_settings", {})
    if style_settings:
        print_info("Style Settings:")
        print_info(f"  Art Movement: {style_settings.get('art_movement', 'Not set')}")
        post_processing = style_settings.get('post_processing', [])
        print_info(f"  Post-processing: {', '.join(post_processing) if post_processing else 'None'}")
    
    # Display quality settings
    quality_settings = user_prefs.imagen_settings.get("quality_settings", {})
    if quality_settings:
        print_info("\nQuality Settings:")
        print_info(f"  Resolution: {quality_settings.get('resolution', 'Not set')}")
        print_info(f"  Detail Level: {quality_settings.get('detail_level', 'Not set')}")
        print_info(f"  Rendering Quality: {quality_settings.get('rendering_quality', 'Not set')}")
    
    # Display other categories of settings
    camera_settings = user_prefs.imagen_settings.get("camera_settings", {})
    if camera_settings:
        print_info("\nCamera Settings:")
        for key, value in camera_settings.items():
            print_info(f"  {key}: {value}")
    
    lighting_settings = user_prefs.imagen_settings.get("lighting_settings", {})
    if lighting_settings:
        print_info("\nLighting Settings:")
        for key, value in lighting_settings.items():
            if isinstance(value, list):
                print_info(f"  {key}: {', '.join(value) if value else 'None'}")
            else:
                print_info(f"  {key}: {value}")
    
    composition_settings = user_prefs.imagen_settings.get("composition_settings", {})
    if composition_settings:
        print_info("\nComposition Settings:")
        for key, value in composition_settings.items():
            print_info(f"  {key}: {value}")
    
    # Wait for user acknowledgment
    input("\nPress Enter to continue...")

# Placeholder functions for the remaining settings categories that would be implemented later
def manage_camera_settings(): 
    print_info("Camera settings management not fully implemented yet")
    input("Press Enter to continue...")

def manage_lighting_settings():
    print_info("Lighting settings management not fully implemented yet")
    input("Press Enter to continue...")

def manage_composition_settings():
    print_info("Composition settings management not fully implemented yet")
    input("Press Enter to continue...")

def manage_color_settings():
    print_info("Color settings management not fully implemented yet")
    input("Press Enter to continue...") 