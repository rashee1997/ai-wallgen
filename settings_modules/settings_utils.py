import json
import os
import logging
from typing import Optional
from file_utils import get_generated_image_path
from ui_utils import print_info, print_error, print_warning, print_success

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
