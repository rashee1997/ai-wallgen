import json
import os
import sys
import shutil
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# Local application imports
from ui_utils import (
    print_section, print_option, print_success, print_error, print_warning, print_info, get_validated_input,
    print_menu_options, get_menu_choice
)
from file_utils import deep_update
from .settings_manager import get_preferences # Import the central preferences getter

# Preset management functions moved from wallpaper_settings.py

def manage_presets():
    """
    Display and manage preset settings through an interactive menu.
    """
    user_prefs = get_preferences() # Get preferences object
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

        choice = get_validated_input(f"Select option (1-4, b)", [key for key, _ in menu_options])

        if choice == "b":
            return

        handlers = {
            "1": save_current_preset,
            "2": handle_load_preset,
            "3": handle_delete_preset,
            "4": view_preset_details
        }

        if choice in handlers:
            handlers[choice]() # Call the appropriate handler

def save_current_preset():
    """Helper function to handle saving current settings as preset."""
    user_prefs = get_preferences() # Get preferences object
    preset_name = get_validated_input("Enter preset name (or 'b' to go back)", allow_empty=False)
    if preset_name.lower() == 'b':
        return

    # Validate preset name
    if not preset_name.strip() or any(c in r'\/:*?"<>|' for c in preset_name):
        print_error("Invalid preset name. Please avoid special characters.")
        return

    preset_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "presets") # Assuming presets dir is one level up from settings_modules
    os.makedirs(preset_dir, exist_ok=True) # Ensure presets directory exists
    preset_path = os.path.join(preset_dir, f"{preset_name}.json")

    # Check if preset already exists
    if os.path.exists(preset_path):
        confirm = get_validated_input(f"Preset '{preset_name}' already exists. Overwrite? (y/n)", ["y", "n"])
        if confirm.lower() != "y":
            return

    try:
        # Collect current settings from user_prefs
        current_settings = {
            "imagen_settings": user_prefs.imagen_settings if hasattr(user_prefs, 'imagen_settings') else {},
            "wallpaper_settings": user_prefs.wallpaper_settings if hasattr(user_prefs, 'wallpaper_settings') else {},
            "aspect_ratio": user_prefs.aspect_ratio if hasattr(user_prefs, 'aspect_ratio') else "16:9",
            "preferred_genres": user_prefs.preferred_genres if hasattr(user_prefs, 'preferred_genres') else [],
            "preferred_styles": user_prefs.preferred_styles if hasattr(user_prefs, 'preferred_styles') else [],
            "preferred_moods": user_prefs.preferred_moods if hasattr(user_prefs, 'preferred_moods') else [],
            "negative_prompts": user_prefs.negative_prompts if hasattr(user_prefs, 'negative_prompts') else [],
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "description": "User preset"
            }
        }

        # Save the preset
        if save_preset(current_settings, preset_name):
            print_success(f"Preset '{preset_name}' saved successfully")
            user_prefs.last_preset = preset_name
            user_prefs.save_preferences() # Save updated last_preset info
        else:
            print_error("Failed to save preset")

    except Exception as e:
        print_error(f"Error preparing preset data: {e}")
        logging.exception("Error in save_current_preset")


def handle_load_preset():
    """Helper function to handle loading a preset."""
    user_prefs = get_preferences() # Get preferences object
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
            if _apply_preset_settings(settings, replace=True):
                print_success("Settings replaced with preset")
            else:
                print_error("Failed to apply preset settings (replace)")
                return # Don't update last_preset on failure
        elif load_choice == "2":  # Merge
            if _apply_preset_settings(settings, replace=False):
                 print_success("Settings merged with preset")
            else:
                 print_error("Failed to apply preset settings (merge)")
                 return # Don't update last_preset on failure


        user_prefs.last_preset = preset_name
        user_prefs.save_preferences() # Save updated last_preset info

    except Exception as e:
        print_error(f"Error applying preset settings: {e}")
        logging.exception("Error in handle_load_preset")

def _apply_preset_settings(settings: Dict[str, Any], replace: bool = True) -> bool:
    """
    Helper function to apply preset settings to the global user_prefs with enhanced style category support.

    Args:
        settings: Dictionary containing settings to apply
        replace: If True, replace existing settings; if False, merge with existing

    Returns:
        bool: True if settings were applied successfully, False otherwise
    """
    user_prefs = get_preferences() # Get preferences object
    try:
        # Define comprehensive default structure for all settings
        default_imagen_structure = {
            "number_of_images": 1,
            "seed": None,
            "negative_prompt": "",
            "quality_settings": {
                "art_movement": "",
                "post_processing": [],
                "style_era": ""
            },
            "style_settings": {
                "art_movement": "",
                "post_processing": [],
                "style_era": ""
            },
            "camera_settings": {
                "camera_model": "",
                "lens_type": "",
                "aperture": "",
                "focal_length": "",
                "shutter_speed": "",
                "iso": "",
                "filter_type": "",
                "depth_of_field": ""
            },
            "lighting_settings": {
                "lighting_type": "",
                "light_quality": "",
                "light_direction": "",
                "time_of_day": ""
            },
            "composition_settings": {
                "technique": "",
                "focal_point": "",
                "camera_angle": "",
                "perspective": ""
            },
            "environment_settings": {
                "environment_type": "",
                "atmospheric_effects": [],
                "special_effects": []
            },
            "color_settings": {
                "color_scheme": "",
                "palette_type": "",
                "color_temperature": "",
                "color_contrast": ""
            },
            "detail_settings": {
                "detail_level": "",
                "texture_quality": ""
            },
            # Style-specific settings
            "digital_settings": {
                "software": "",
                "rendering_technique": "",
                "digital_effects": [],
                "resolution": "",
                "filter_usage": [],
                "brush_type": "",
                "layer_complexity": ""
            },
            "game_engine_settings": {
                "engine_type": "",
                "render_quality": "",
                "special_effects": [],
                "shader_type": "",
                "post_effects": [],
                "resolution": "",
                "poly_detail": "",
                "game_genre": "",
                "game_era": ""
            },
            "medium_settings": {
                "painting_medium": "",
                "canvas_type": "",
                "brushwork": "",
                "texture": "",
                "layering_technique": "",
                "stroke_style": "",
                "detail_approach": ""
            },
            "illustration_settings": {
                "style": "",
                "line_quality": "",
                "color_approach": "",
                "shading_style": ""
            },
            "abstract_settings": {
                "composition_type": "",
                "color_scheme": "",
                "texture_style": "",
                "movement_type": ""
            },
            "material_settings": {
                "material_type": "",
                "finish": "",
                "texture": "",
                "light_interaction": ""
            }
        }
        default_wallpaper_structure = {
            "auto_set": False,
            "skip_preview": False,
            "gui_preview_backend": "qt",
            "aspect_ratio": "16:9",
            "preferred_genres": [],
            "preferred_styles": [],
            "preferred_moods": [],
            "negative_prompts": []
        }

        # Apply imagen_settings and wallpaper_settings
        for setting_type, default_structure in [('imagen_settings', default_imagen_structure), ('wallpaper_settings', default_wallpaper_structure)]:
            if hasattr(user_prefs, setting_type):
                current_settings_dict = getattr(user_prefs, setting_type)
                # Optional: Ensure current settings have the default structure if UserPreferences doesn't
                # for key, default_value in default_structure.items():
                #     current_settings_dict.setdefault(key, default_value)

                if setting_type in settings:
                    preset_settings_dict = settings[setting_type]
                    if isinstance(preset_settings_dict, dict):
                        # Remove "description" key if present to avoid applying it
                        if replace:
                            # Start with defaults, then update with preset (or just assign)
                            # setattr(user_prefs, setting_type, preset_settings_dict.copy()) # Simple replace
                            new_settings = default_structure.copy() # More robust replace
                            deep_update(new_settings, preset_settings_dict)
                            
                            # Handle both old and new style presets
                            # First, copy all settings from the preset to the new settings
                            for key in preset_settings_dict:
                                # Copy all settings directly, ensuring compatibility with both old and new preset formats
                                new_settings[key] = preset_settings_dict[key]
                                
                            # Log the new settings structure after applying preset
                            logging.debug(f"New settings after applying preset: {json.dumps(new_settings, indent=2)}")
                            
                            setattr(user_prefs, setting_type, new_settings)
                        else:
                            # Merge preset into current
                            deep_update(current_settings_dict, preset_settings_dict)
                    else:
                         logging.warning(f"Preset value for {setting_type} is not a dictionary. Skipping.")
            elif setting_type in settings: # If user_prefs doesn't have the attr, but preset does
                if isinstance(settings[setting_type], dict):
                     setattr(user_prefs, setting_type, settings[setting_type].copy())
                else:
                     logging.warning(f"Preset provided {setting_type} but it's not a dict. Skipping.")


        # Explicitly apply top-level settings if present in the preset
        # Handle styles - check both "preferred_styles" and "styles" fields
        if "preferred_styles" in settings and isinstance(settings.get("preferred_styles"), list):
            if replace:
                user_prefs.preferred_styles = settings["preferred_styles"][:]
            else:
                existing = set(user_prefs.preferred_styles)
                new = set(settings["preferred_styles"])
                user_prefs.preferred_styles = list(existing.union(new))
        elif "styles" in settings and isinstance(settings.get("styles"), list):
            if replace:
                user_prefs.preferred_styles = settings["styles"][:]
            else:
                existing = set(user_prefs.preferred_styles)
                new = set(settings["styles"])
                user_prefs.preferred_styles = list(existing.union(new))

        # Handle moods - check both "preferred_moods" and "moods" fields
        if "preferred_moods" in settings and isinstance(settings.get("preferred_moods"), list):
             if replace:
                 user_prefs.preferred_moods = settings["preferred_moods"][:]
             else:
                 existing = set(user_prefs.preferred_moods)
                 new = set(settings["preferred_moods"])
                 user_prefs.preferred_moods = list(existing.union(new))
        elif "moods" in settings and isinstance(settings.get("moods"), list):
             if replace:
                 user_prefs.preferred_moods = settings["moods"][:]
             else:
                 existing = set(user_prefs.preferred_moods)
                 new = set(settings["moods"])
                 user_prefs.preferred_moods = list(existing.union(new))

        if "aspect_ratio" in settings:
             user_prefs.aspect_ratio = settings["aspect_ratio"]

        if "negative_prompts" in settings and isinstance(settings.get("negative_prompts"), list):
             if replace:
                 user_prefs.negative_prompts = settings["negative_prompts"][:]
             else:
                 existing = set(user_prefs.negative_prompts)
                 new = set(settings["negative_prompts"])
                 user_prefs.negative_prompts = list(existing.union(new))

        if "preferred_genres" in settings and isinstance(settings.get("preferred_genres"), list):
             if replace:
                 user_prefs.preferred_genres = settings["preferred_genres"][:]
             else:
                 existing = set(user_prefs.preferred_genres)
                 new = set(settings["preferred_genres"])
                 user_prefs.preferred_genres = list(existing.union(new))

        # Save preferences after applying changes
        user_prefs.save_preferences()
        return True # Indicate success

    except Exception as e:
        logging.exception(f"Error applying preset settings: {e}")
        return False # Indicate failure


def handle_delete_preset():
    """Helper function to handle deleting a preset."""
    user_prefs = get_preferences() # Get preferences object
    current_preset = getattr(user_prefs, 'last_preset', None)
    preset_name_deleted = delete_preset() # delete_preset returns the name if successful
    if preset_name_deleted:
        # If the deleted preset was the currently loaded one, clear it
        if current_preset and current_preset == preset_name_deleted:
            user_prefs.last_preset = None
            user_prefs.save_preferences() # Save the cleared last_preset


def _display_settings_section(settings: Dict[str, Any], section: str, title: str, indent: int = 0) -> None:
    """
    Helper function to display a section of settings recursively.
    """
    if section not in settings:
        return

    data = settings.get(section)
    if data is None:
        return

    print_info(f"\n{'  ' * indent}{title}:")

    if isinstance(data, dict):
        for key, value in data.items():
            # Recursively display nested dictionaries
            if isinstance(value, dict):
                 _display_settings_section({key: value}, key, f"{key}", indent + 1)
            # Handle lists - print each item on a new line
            elif isinstance(value, list):
                 print_info(f"{'  ' * (indent + 1)}{key}:")
                 if value:
                     for item in value:
                         print_info(f"{'  ' * (indent + 2)}- {item}")
                 else:
                      print_info(f"{'  ' * (indent + 2)}<empty>")
            # Print simple key-value pairs
            else:
                print_info(f"{'  ' * (indent + 1)}{key}: {value}")
    # Handle cases where the section itself is not a dict (e.g., just a string or list)
    elif isinstance(data, list):
         if data:
             for item in data:
                 print_info(f"{'  ' * (indent + 1)}- {item}")
         else:
             print_info(f"{'  ' * (indent + 1)}<empty>")
    else:
        print_info(f"{'  ' * (indent + 1)}{data}")


def view_preset_details():
    """Helper function to view current preset details."""
    user_prefs = get_preferences() # Get preferences object
    current_preset = getattr(user_prefs, 'last_preset', None)
    if not current_preset:
        print_warning("No preset currently loaded")
        input("\nPress Enter to continue...")
        return

    try:
        preset_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "presets") # Consistent path finding
        preset_file = os.path.join(preset_dir, f"{current_preset}.json")
        if not os.path.exists(preset_file):
            print_error(f"Preset file not found: {preset_file}")
            user_prefs.last_preset = None # Clear invalid preset
            user_prefs.save_preferences()
            return

        with open(preset_file) as f:
            settings = json.load(f)

        # Display preset information using the helper
        print_section(f"Preset Details: {current_preset}")
        # Display key sections found in presets
        _display_settings_section(settings, "metadata", "Metadata")
        _display_settings_section(settings, "imagen_settings", "Imagen Settings")
        _display_settings_section(settings, "wallpaper_settings", "Wallpaper Settings")
        _display_settings_section(settings, "preferred_genres", "Preferred Genres")
        _display_settings_section(settings, "preferred_styles", "Preferred Styles")
        _display_settings_section(settings, "preferred_moods", "Preferred Moods")
        _display_settings_section(settings, "negative_prompts", "Negative Prompts")
        if "aspect_ratio" in settings:
             _display_settings_section(settings, "aspect_ratio", "Aspect Ratio")

        input("\nPress Enter to continue...")
    except (json.JSONDecodeError, IOError, OSError) as e:
        print_error(f"Error reading preset details: {e}")
        logging.exception(f"Error in view_preset_details for {current_preset}")
    except Exception as e: # Catch unexpected errors
         print_error(f"An unexpected error occurred: {e}")
         logging.exception(f"Unexpected error in view_preset_details for {current_preset}")

def load_preset():
    """
    Load a preset from a file with enhanced style category support.

    Returns:
        Optional[Tuple[Dict[str, Any], str]]: A tuple of (settings, preset_name) if successful,
        None if no presets found or user cancels
    """
    preset_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "presets")
    if not os.path.exists(preset_dir):
        print_error("No presets directory found")
        return None

    presets = [f for f in os.listdir(preset_dir) if f.endswith('.json')]
    if not presets:
        print_error("No presets found")
        return None

    print_section("Available Presets")
    for i, preset in enumerate(presets, 1):
        preset_path = os.path.join(preset_dir, preset)
        try:
            with open(preset_path, 'r') as f:
                preset_data = json.load(f)
                metadata = preset_data.get('metadata', {})
                description = metadata.get('description', 'User preset')
                created_at = metadata.get('created_at', 'Unknown date')
                
                # Get style categories from the preset
                style_categories = []
                if 'imagen_settings' in preset_data:
                    if 'style_settings' in preset_data['imagen_settings']:
                        style_categories.extend(preset_data['imagen_settings']['style_settings'].get('art_movement', []))
                    if 'game_engine_settings' in preset_data['imagen_settings']:
                        style_categories.extend(['game_' + s for s in preset_data['imagen_settings']['game_engine_settings'].get('game_genre', [])])
                    if 'digital_settings' in preset_data['imagen_settings']:
                        style_categories.extend(['digital_' + s for s in preset_data['imagen_settings']['digital_settings'].get('software', [])])
                    
                style_categories = list(set(style_categories))[:3]  # Show up to 3 unique categories
                style_str = f" ({', '.join(style_categories)})" if style_categories else ""
                
                print(f"{i}. {preset[:-5]} - {description}{style_str} (Created: {created_at})")
        except Exception as e:
            print_error(f"Error reading preset {preset}: {e}")
            continue

    print("b. Back")
    choice = get_validated_input("Select preset (1-{}, b)".format(len(presets)), 
                              [str(i+1) for i in range(len(presets))] + ['b'])

    if choice == 'b':
        return None

    try:
        preset_path = os.path.join(preset_dir, presets[int(choice)-1])
        with open(preset_path, 'r') as f:
            settings = json.load(f)
            return settings, presets[int(choice)-1][:-5]
    except Exception as e:
        print_error(f"Error loading preset: {e}")
        return None
    except Exception as e: # Catch unexpected errors
         print_error(f"An unexpected error occurred: {e}")
         logging.exception("Unexpected error in load_preset")
         input("Press Enter to continue...")
         return None

def save_preset(settings: Dict[str, Any], preset_name: str) -> bool:
    """
    Save settings to a preset file.

    Args:
        settings: Dictionary containing settings to save
        preset_name: Name for the preset file (without extension)

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        preset_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "presets") # Consistent path finding
        os.makedirs(preset_dir, exist_ok=True) # Ensure presets directory exists
        preset_path = os.path.join(preset_dir, f"{preset_name}.json")

        with open(preset_path, "w") as f:
            json.dump(settings, f, indent=4)
        return True
    except (IOError, OSError) as e:
        print_error(f"Error saving preset '{preset_name}': {e}")
        logging.exception(f"Error in save_preset for {preset_name}")
        return False
    except Exception as e: # Catch unexpected errors
         print_error(f"An unexpected error occurred while saving preset '{preset_name}': {e}")
         logging.exception(f"Unexpected error in save_preset for {preset_name}")
         return False


def delete_preset() -> Optional[str]:
    """
    Delete a preset file.

    Returns:
        Optional[str]: The name of the deleted preset if successful, None otherwise.
    """
    try:
        preset_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "presets") # Consistent path finding
        os.makedirs(preset_dir, exist_ok=True) # Ensure presets directory exists

        # Get list of presets
        presets = sorted([f for f in os.listdir(preset_dir) if f.endswith(".json")])
        if not presets:
            print_warning("No saved presets found to delete")
            input("Press Enter to continue...")
            return None

        # Show preset options
        print_section("Available Presets to Delete")
        for i, preset in enumerate(presets, 1):
            print_option(str(i), preset.replace(".json", ""))
        print_option("b", "Back")

        # Get user choice
        valid_choices = ["b"] + [str(i) for i in range(1, len(presets) + 1)]
        choice = get_validated_input("Select preset to delete", valid_choices)
        if choice == "b":
            return None

        preset_file = presets[int(choice) - 1]
        preset_path = os.path.join(preset_dir, preset_file)
        preset_name = preset_file.replace(".json", "")

        confirm = get_validated_input(f"Are you sure you want to delete preset '{preset_name}'? (y/n)", ["y", "n"])
        if confirm.lower() == "y":
            os.remove(preset_path)
            print_success(f"Preset '{preset_name}' deleted")
            return preset_name # Return name on success
        else:
            print_info("Deletion cancelled")
            return None

    except (FileNotFoundError, IOError, OSError) as e:
        print_error(f"Error deleting preset: {e}")
        logging.exception("Error in delete_preset")
        input("Press Enter to continue...")
        return None
    except Exception as e: # Catch unexpected errors
        print_error(f"An unexpected error occurred: {e}")
        logging.exception("Unexpected error in delete_preset")
        input("Press Enter to continue...")
        return None
