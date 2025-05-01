import json
import os
import shutil
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# Local application imports
from ui_utils import print_section, print_success, print_error, print_warning, print_info, get_validated_input, print_option
from .settings_manager import get_preferences # Import the central preferences getter
# Assuming _apply_preset_settings is needed for import, it should be moved or imported appropriately.
# For now, importing from preset_management where it was moved in Phase 3.
from .preset_management import _apply_preset_settings

# Settings import/export functions moved from wallpaper_settings.py

def export_settings(filename: Optional[str] = None) -> None:
    """
    Export current settings to a JSON file.

    Args:
        filename (Optional[str], optional): Path to export the settings to.
                                             If None, prompts the user. Defaults to None.
    """
    user_prefs = get_preferences() # Get preferences object
    try:
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"wallgen_settings_backup_{timestamp}.json"
            print_info(f"Default filename: {default_filename}")
            filename_input = get_validated_input("Enter filename for export (or press Enter for default, 'b' to cancel)", allow_empty=True)

            if filename_input.lower() == 'b':
                print_info("Export cancelled.")
                return
            elif not filename_input:
                filename = default_filename
            else:
                # Ensure filename ends with .json
                if not filename_input.lower().endswith(".json"):
                    filename = filename_input + ".json"
                else:
                    filename = filename_input

        # Ensure the directory exists (using user's home directory for exports)
        export_dir = os.path.expanduser("~") # Or choose another sensible default directory
        full_path = os.path.join(export_dir, filename)
        # os.makedirs(os.path.dirname(full_path), exist_ok=True) # Not needed if exporting to home dir

        # Check for existing file
        if os.path.exists(full_path):
             confirm = get_validated_input(f"File '{filename}' already exists in {export_dir}. Overwrite? (y/n)", ["y", "n"])
             if confirm.lower() != 'y':
                 print_info("Export cancelled.")
                 return

        # Collect all relevant settings from user_prefs
        settings_to_export = {
            "metadata": {
                "export_version": "1.0", # Add a version for future compatibility
                "exported_at": datetime.now().isoformat(),
            },
            # Include all major settings attributes from UserPreferences
            "preferred_genres": user_prefs.preferred_genres,
            "preferred_styles": user_prefs.preferred_styles,
            "preferred_moods": user_prefs.preferred_moods,
            "negative_prompts": user_prefs.negative_prompts,
            "imagen_settings": user_prefs.imagen_settings,
            "wallpaper_settings": user_prefs.wallpaper_settings,
            "aspect_ratio": user_prefs.aspect_ratio,
            # Do not export history_file path or last_preset by default
        }

        # Write the settings to the file
        with open(full_path, "w") as f:
            json.dump(settings_to_export, f, indent=4)

        print_success(f"Settings successfully exported to {full_path}")

    except (IOError, OSError) as e:
        print_error(f"Error exporting settings to {filename}: {e}")
        logging.exception("Error during settings export")
    except Exception as e:
        print_error(f"An unexpected error occurred during export: {e}")
        logging.exception("Unexpected error during settings export")


def import_settings(filename: Optional[str] = None) -> None:
    """
    Import settings from a JSON file, allowing merge or replace.

    Args:
        filename (Optional[str], optional): Path to the settings file to import.
                                             If None, prompts the user. Defaults to None.
    """
    user_prefs = get_preferences() # Get preferences object
    try:
        if not filename:
            # Prompt user for the file path - consider using a file dialog in a GUI
            print_info("Enter the full path to the settings file (.json) to import.")
            filename_input = get_validated_input("File path (or 'b' to cancel)", allow_empty=False)

            if filename_input.lower() == 'b':
                print_info("Import cancelled.")
                return
            filename = filename_input

        # Expand user path (~) and check if file exists
        full_path = os.path.expanduser(filename)

        if not os.path.exists(full_path):
            print_error(f"Import file not found: {full_path}")
            return

        if not full_path.lower().endswith(".json"):
            print_warning("The selected file does not have a .json extension. Attempting to load anyway.")

        # Load settings from the file
        with open(full_path, "r") as f:
            imported_settings = json.load(f)

        # Basic validation: Check if it looks like a settings file (e.g., contains known keys)
        if not isinstance(imported_settings, dict) or not any(key in imported_settings for key in ["imagen_settings", "wallpaper_settings", "preferred_genres"]):
             confirm = get_validated_input("Warning: File does not look like a valid settings export. Continue anyway? (y/n)", ["y", "n"])
             if confirm.lower() != 'y':
                 print_info("Import cancelled.")
                 return

        # Ask user whether to merge or replace
        print_section("Import Mode")
        print_option("1", "Replace current settings with imported settings")
        print_option("2", "Merge imported settings into current settings (imported values overwrite)")
        print_option("b", "Cancel Import")

        choice = get_validated_input("Select import mode (1, 2, b)", ["1", "2", "b"])

        if choice == "b":
            print_info("Import cancelled.")
            return
        elif choice == "1": # Replace
            # Use the same logic as applying a preset in "replace" mode
            if _apply_preset_settings(imported_settings, replace=True):
                print_success(f"Settings successfully imported from {filename} (Replaced)")
                # Optionally clear last_preset as settings are now potentially different
                # user_prefs.last_preset = None
                # user_prefs.save_preferences()
            else:
                print_error("Failed to apply imported settings (Replace).")

        elif choice == "2": # Merge
             # Use the same logic as applying a preset in "merge" mode
             if _apply_preset_settings(imported_settings, replace=False):
                 print_success(f"Settings successfully imported from {filename} (Merged)")
                 # Optionally clear last_preset as settings are now potentially different
                 # user_prefs.last_preset = None
                 # user_prefs.save_preferences()
             else:
                 print_error("Failed to apply imported settings (Merge).")


    except (FileNotFoundError, json.JSONDecodeError, IOError, OSError) as e:
        print_error(f"Error importing settings from {filename}: {e}")
        logging.exception("Error during settings import")
    except Exception as e:
        print_error(f"An unexpected error occurred during import: {e}")
        logging.exception("Unexpected error during settings import")
