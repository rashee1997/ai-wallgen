"""
Settings management module for AI Wallpaper Generator (Refactored).

This file now serves primarily as a placeholder after refactoring.
All core settings functionality has been moved to the wall_gen/settings_modules package.
The main application entry point (wallpaper_generator.py) should now import
and use functions directly from the wall_gen.settings_modules package.
"""

# Import the main entry points from the new modules for potential backward compatibility
# These imports might be removed if wallpaper_generator.py is fully updated.
from wall_gen.settings_modules.settings_manager import initialize_settings, get_preferences
# Re-export key functions for potential backward compatibility during transition
# This helps if other parts of the code still import directly from wallpaper_settings
# These re-exports can be removed after all code is updated to import from wall_gen.settings_modules
from wall_gen.settings_modules.user_preferences import UserPreferences
from wall_gen.settings_modules.preset_management import manage_presets, load_preset, save_preset, delete_preset
from wall_gen.settings_modules.settings_import_export import export_settings, import_settings
from wall_gen.settings_modules.settings_utils import update_history_with_filenames, load_last_genre, save_last_genre
from wall_gen.settings_modules.menu_management.genres_menu import manage_genres
from wall_gen.settings_modules.menu_management.styles_menu import manage_styles
from wall_gen.settings_modules.menu_management.moods_menu import manage_moods
from wall_gen.settings_modules.menu_management.wallpaper_settings_menu import manage_wallpaper_settings
from wall_gen.settings_modules.menu_management.advanced_options_menu import (
    configure_advanced_options, 
    manage_imagen_settings, 
    manage_prompt_generation_settings, 
    reset_all_settings_to_none, 
    manage_camera_settings, 
    manage_output_quality_settings, 
    manage_lighting_settings, 
    manage_composition_settings, 
    manage_color_settings, 
    view_current_settings, 
    reset_to_default, 
    change_aspect_ratio, 
    manage_negative_prompt
)
from wall_gen.settings_modules.ai_preset_generation import generate_ai_preset

# The global user_prefs variable is now managed within wall_gen.settings_modules.settings_manager
# Access it via get_preferences()

# The main application entry point (wallpaper_generator.py) should now call
# initialize_settings() and manage_preferences() directly from their new locations.
# This file no longer contains the implementation of these functions.
