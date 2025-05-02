import json
import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Tuple

from .utils import deep_update

class UserPreferences:
    """
    Class to manage user preferences for the wallpaper generator.

    Handles loading, saving, and providing access to user preferences
    including image generation settings, style preferences, and application configuration.
    Maintains persistent storage of settings between application runs.
    """
    def __init__(self):
        """
        Initialize user preferences with minimal default values.
        
        Sets up the initial state of user preferences with minimal values for required
        settings. This prevents loading all options in the settings menu.
        """
        # Initialize with empty collections
        self.preferred_genres = []
        self.preferred_styles: List[str] = []  # List to store styles
        self.preferred_moods = []
        self.negative_prompts = []
        
        # Minimal default Imagen settings
        self.imagen_settings = {
            "number_of_images": 1,
            "seed": None,
            "negative_prompt": "",
            "quality_settings": {
                "resolution": "3840x2160",
                "rendering_quality": "high"
            },
            "style_settings": {
                "art_movement": None,
                "post_processing": [],
                "style_era": None
            },
            "camera_settings": {
                "camera_model": None,
                "lens_type": None,
                "aperture": None,
                "focal_length": None,
                "shutter_speed": None,
                "iso": None,
                "filter_type": None,
                "depth_of_field": None
            },
            "lighting_settings": {
                "lighting_type": None,
                "light_quality": None,
                "light_direction": None,
                "time_of_day": None
            },
            "composition_settings": {
                "technique": None,
                "focal_point": None,
                "camera_angle": None,
                "perspective": None
            },
            "environment_settings": {
                "environment_type": None,
                "atmospheric_effects": [],
                "special_effects": []
            },
            "color_settings": {
                "color_scheme": None,
                "palette_type": None,
                "color_temperature": None,
                "color_contrast": None
            },
            "detail_settings": {
                "detail_level": None,
                "texture_quality": None
            },
            "digital_settings": {
                "software": None,
                "rendering_technique": None,
                "digital_effects": [],
                "resolution": None,
                "filter_usage": [],
                "brush_type": None,
                "layer_complexity": None
            },
            "software_settings": {
                "suite": None,
                "renderer": None,
                "version": None
            },
            "game_engine_settings": {
                "engine_type": None,
                "render_quality": None,
                "special_effects": [],
                "shader_type": None,
                "post_effects": [],
                "resolution": None,
                "poly_detail": None,
                "game_genre": None,
                "game_era": None
            },
            "medium_settings": {
                "painting_medium": None,
                "canvas_type": None,
                "brushwork": None,
                "texture": None,
                "layering_technique": None,
                "stroke_style": None,
                "detail_approach": None
            },
            "illustration_settings": {
                "style": None,
                "line_quality": None,
                "color_approach": None,
                "shading_style": None
            },
            "abstract_settings": {
                "composition_type": None,
                "color_scheme": None,
                "texture_style": None,
                "movement_type": None
            },
            "material_settings": {
                "material_type": None,
                "finish": None,
                "texture": None,
                "light_interaction": None
            }
        }
        
        # Default wallpaper settings
        self.wallpaper_settings = {
            "auto_set": False,
            "skip_preview": False,  # Default to showing preview
            "gui_preview_backend": "qt" # Default to Qt preview
        }
        
        # Default aspect ratio
        self.aspect_ratio = "16:9"
        
        # Set history file path
        import os
        script_dir = os.getcwd()
        self.history_file = os.path.join(script_dir, "generation_history.json")
        
        # Track last used preset
        self.last_preset = None
        
        # Load existing preferences if available
        logging.debug("UserPreferences: Initializing and loading preferences.")
        self.load_preferences()
        logging.debug("UserPreferences: Initialization complete.")


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
        logging.debug(f"UserPreferences: Attempting to load preferences from {filename}.")
        try:
            import os
            script_dir = os.getcwd()
            pref_file_path = os.path.join(script_dir, filename)
            logging.debug(f"UserPreferences: Full preferences file path: {pref_file_path}")

            if os.path.exists(pref_file_path):
                logging.debug("UserPreferences: Preferences file found. Reading...")
                with open(pref_file_path, "r") as f:
                    data = json.load(f)
                logging.debug(f"UserPreferences: Loaded data: {data}")

                # Handle preferred_genres or genres
                if "preferred_genres" in data:
                    self.preferred_genres = list(dict.fromkeys(data["preferred_genres"]))
                    logging.debug(f"UserPreferences: Loaded preferred_genres: {self.preferred_genres}")
                elif "genres" in data:
                    self.preferred_genres = list(dict.fromkeys(data["genres"]))
                    logging.debug(f"UserPreferences: Loaded genres as preferred_genres: {self.preferred_genres}")

                # Handle preferred_styles or styles
                if "preferred_styles" in data and isinstance(data["preferred_styles"], list):
                    self.preferred_styles = data["preferred_styles"]
                    logging.debug(f"UserPreferences: Loaded preferred_styles (list): {self.preferred_styles}")
                elif "preferred_styles" in data and isinstance(data["preferred_styles"], str):
                    # Convert old string format to list
                    self.preferred_styles = [data["preferred_styles"]]
                    logging.debug(f"UserPreferences: Converted preferred_styles string to list: {self.preferred_styles}")
                elif "styles" in data and isinstance(data["styles"], list):
                    # Load styles from preset format
                    self.preferred_styles = data["styles"]
                    logging.debug(f"UserPreferences: Loaded styles as preferred_styles: {self.preferred_styles}")
                elif "styles" in data and isinstance(data["styles"], str):
                    # Convert old string format to list
                    self.preferred_styles = [data["styles"]]
                    logging.debug(f"UserPreferences: Converted styles string to preferred_styles list: {self.preferred_styles}")
                else:
                    self.preferred_styles = []
                    logging.debug("UserPreferences: No styles or preferred_styles found, set to empty list.")

                # Handle preferred_moods or moods
                if "preferred_moods" in data:
                    self.preferred_moods = list(dict.fromkeys(data["preferred_moods"]))
                    logging.debug(f"UserPreferences: Loaded preferred_moods: {self.preferred_moods}")
                elif "moods" in data and isinstance(data["moods"], list):
                    self.preferred_moods = list(dict.fromkeys(data["moods"]))
                    logging.debug(f"UserPreferences: Loaded moods as preferred_moods: {self.preferred_moods}")

                # Handle negative_prompts
                if "negative_prompts" in data:
                    self.negative_prompts = data["negative_prompts"]
                    logging.debug(f"UserPreferences: Loaded negative_prompts: {self.negative_prompts}")
                if "imagen_settings" in data:
                    imagen_data = data["imagen_settings"]
                    for key in self.imagen_settings.keys():
                        if key in imagen_data:
                            self.imagen_settings[key] = imagen_data[key]
                    logging.debug(f"UserPreferences: Loaded imagen_settings: {self.imagen_settings}")
                if "wallpaper_settings" in data:
                    wallpaper_data = data["wallpaper_settings"]
                    for key in self.wallpaper_settings.keys():
                        if key in wallpaper_data:
                            self.wallpaper_settings[key] = wallpaper_data[key]
                    logging.debug(f"UserPreferences: Loaded wallpaper_settings: {self.wallpaper_settings}")
                if "gui_preview_backend" in data.get("wallpaper_settings", {}):
                    self.wallpaper_settings["gui_preview_backend"] = data["wallpaper_settings"]["gui_preview_backend"]
                    logging.debug(f"UserPreferences: Loaded gui_preview_backend: {self.wallpaper_settings['gui_preview_backend']}")
                if "history_file" in data:
                    self.history_file = data["history_file"]
                    logging.debug(f"UserPreferences: Loaded history_file: {self.history_file}")
                if "last_preset" in data:
                    self.last_preset = data["last_preset"]
                    logging.debug(f"UserPreferences: Loaded last_preset: {self.last_preset}")
                if "aspect_ratio" in data:
                    self.aspect_ratio = data["aspect_ratio"]
                    logging.debug(f"UserPreferences: Loaded aspect_ratio: {self.aspect_ratio}")

                logging.debug("UserPreferences: Preferences loaded successfully.")
            else:
                logging.debug("UserPreferences: Preferences file not found. Using default settings.")
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logging.error(f"UserPreferences: Error loading preferences from {pref_file_path}: {e}")
        except Exception as e:
            logging.error(f"UserPreferences: An unexpected error occurred during loading: {e}")


    def save_preferences(self, filename: str = "user_preferences.json") -> None:
        """
        Save user preferences to a JSON file.
        
        This method serializes the current user preferences to a JSON file
        for persistence across sessions.
        
        Args:
            filename (str, optional): Path where the preferences should be saved.
                                     Defaults to "user_preferences.json".
        """
        logging.debug(f"UserPreferences: Attempting to save preferences to {filename}.")
        import os
        script_dir = os.getcwd()
        pref_file_path = os.path.join(script_dir, filename)
        logging.debug(f"UserPreferences: Full preferences file path for saving: {pref_file_path}")
        try:
            # Clean duplicates before saving
            self.preferred_genres = list(dict.fromkeys(self.preferred_genres))
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
            logging.debug(f"UserPreferences: Data to be saved: {data}")
            
            # Write to file
            with open(pref_file_path, "w") as f:
                json.dump(data, f, indent=4)
            logging.debug("UserPreferences: Preferences saved successfully. Reloading...")
            
            # Reload preferences after saving to update in-memory state
            self.load_preferences(filename)
            logging.debug("UserPreferences: Preferences reloaded after saving.")
        except (IOError, OSError) as e:
            logging.error(f"UserPreferences: Error saving preferences to {pref_file_path}: {e}")
        except Exception as e:
            logging.error(f"UserPreferences: An unexpected error occurred during saving: {e}")

    def add_style(self, style: str):
        """
        Add a style to preferred_styles, avoiding duplicates.
        
        This method adds the provided style string to the preferred_styles
        list if it's not already present, then saves the updated preferences.
        
        Args:
            style (str): The style to add to the preferred_styles list
        """
        if style:
            if style not in self.preferred_styles:
                self.preferred_styles.append(style)
                self.save_preferences()

    def clear_style(self):
        """
        Clears all preferred styles.
        
        This method resets the preferred_styles list to empty
        and saves the updated preferences.
        """
        self.preferred_styles = []
        self.save_preferences()

    def add_genre(self, genre: str):
        """
        Add a genre to preferred_genres, avoiding duplicates.
        
        This method adds the provided genre string to the preferred_genres
        list if it's not already present, then saves the updated preferences.
        
        Args:
            genre (str): The genre to add to the preferred_genres list
        """
        if genre:
            if genre not in self.preferred_genres:
                self.preferred_genres.append(genre)
                self.save_preferences()

    def add_mood(self, mood: str):
        """
        Add a mood to preferred_moods, avoiding duplicates.
        
        This method adds the provided mood string to the preferred_moods
        list if it's not already present, then saves the updated preferences.
        
        Args:
            mood (str): The mood to add to the preferred_moods list
        """
        if mood:
            if mood not in self.preferred_moods:
                self.preferred_moods.append(mood)
                self.save_preferences()

    def clear_moods(self):
        """
        Clears all preferred moods.
        
        This method resets the preferred_moods list to empty
        and saves the updated preferences.
        """
        self.preferred_moods = []
        self.save_preferences()
    
    def add_negative_prompt(self, negative_prompt: str):
        """
        Add a negative prompt, avoiding duplicates.
        
        This method adds the provided negative prompt string to the negative_prompts
        list if it's not already present, then saves the updated preferences.
        
        Args:
            negative_prompt (str): The negative prompt to add to the list
        """
        if negative_prompt:
            if negative_prompt not in self.negative_prompts:
                self.negative_prompts.append(negative_prompt)
                self.save_preferences()

    def clear_negative_prompts(self):
        """
        Clears all negative prompts.
        
        This method resets the negative_prompts list to empty
        and saves the updated preferences.
        """
        self.negative_prompts = []
        self.save_preferences()
