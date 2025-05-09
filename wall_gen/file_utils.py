# wall_gen/file_utils.py
"""Utility functions for file operations, path manipulations, and temp file management."""
# NOTE: This module assumes the project root is on sys.path for certain imports if not run as part of the wall_gen package.

import os
import hashlib
import re
import logging
import html
import json # For save_json_data
import shutil # For move_temp_image_to_cache
import tempfile # For create_temp_file
import atexit # For cleanup_all_temp_files registration (though registration itself is in app_utils)
from datetime import datetime # For list_sorted_generated_images

import google.generativeai as genai # Needed for extract_subject_from_prompt
from typing import Dict, Any, List, Set, Optional # Added Optional for type hinting user_prefs
from wall_gen import gemini_config # Import the new centralized configuration
# wallpaper_settings is not directly used here for UserPreferences,
# but UserPreferences instance will be passed to functions needing it.
# NOTE: This module assumes wallpaper_settings.py is part of the wall_gen package.
# from wall_gen.wallpaper_settings import get_preferences # If needed directly

# --- Temporary File Management ---
_temp_files: Set[str] = set()

def _cleanup_all_temp_files():
    """
    Cleans up all registered temporary files.
    Intended to be registered with atexit by app_utils.
    (Moved from wallpaper_generator.py)
    """
    logging.info(f"Cleaning up temporary files. Current count: {len(_temp_files)}")
    # Iterate over a copy of the set as we are modifying it
    for temp_file_path in list(_temp_files):
        try:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                logging.info(f"Temporary file removed at exit: {temp_file_path}")
            _temp_files.discard(temp_file_path) # Remove from set even if not found (already deleted)
        except OSError as e: # Catch specific OS errors like permission denied
            logging.warning(f"Failed to remove temporary file '{temp_file_path}' at exit: {e}")
        except Exception as e: # Catch any other unexpected errors
            logging.error(f"Unexpected error removing temporary file '{temp_file_path}': {e}", exc_info=True)
    logging.info("Temporary file cleanup process finished.")


def create_temp_file(suffix=".png", delete_on_close=False) -> str:
    """
    Creates a named temporary file and registers it for cleanup.
    (Moved and refactored from create_temp_image_file in wallpaper_generator.py)
    Args:
        suffix (str): Suffix for the temporary file.
        delete_on_close (bool): If True, tempfile module handles deletion. If False (default),
                                our atexit handler handles it. For images, False is better.
    Returns:
        str: The absolute path to the created temporary file.
    """
    # Create temp file in the system's default temporary directory
    # delete=False means we manage deletion via _cleanup_all_temp_files
    # This is important if the file needs to exist after the handle is closed (e.g., for an external program to read it)
    fd, temp_file_path = tempfile.mkstemp(suffix=suffix)
    os.close(fd) # Close the file descriptor immediately, we only need the path.
    
    abs_temp_file_path = os.path.abspath(temp_file_path)
    _temp_files.add(abs_temp_file_path)
    logging.debug(f"Temporary file created and registered for cleanup: {abs_temp_file_path}")
    return abs_temp_file_path


def remove_temp_file(path: str):
    """
    Removes a specific temporary file and unregisters it.
    (Moved from remove_temp_image_file in wallpaper_generator.py)
    """
    abs_path = os.path.abspath(path)
    try:
        if os.path.exists(abs_path):
            os.remove(abs_path)
            logging.info(f"Temporary file explicitly removed: {abs_path}")
        _temp_files.discard(abs_path)
    except OSError as e:
        logging.warning(f"Could not remove temporary file '{abs_path}': {e}")
    except Exception as e:
        logging.error(f"Unexpected error removing temp file '{abs_path}': {e}", exc_info=True)


# --- Filename and Path Generation ---

def extract_subject_from_prompt_for_filename(prompt: str, user_prefs=None) -> Optional[str]:
    """
    Extract the main subject from a prompt using Gemini, for filename use.
    (Moved from extract_subject_from_prompt in wallpaper_generator.py, assumes genai is configured)
    Now uses the selected Gemini model from gemini_config.
    Args:
        prompt (str): The prompt to analyze.
        user_prefs (UserPreferences, optional): User preferences instance. If None, will try to get it.
    """
    current_user_prefs = user_prefs # Use a local variable to manage user_prefs

    if current_user_prefs is None:
        try:
            from wall_gen.wallpaper_settings import get_preferences
            current_user_prefs = get_preferences()
            logging.debug("Successfully fetched user_prefs in extract_subject_from_prompt_for_filename.")
        except ImportError:
            logging.warning("Could not import or call get_preferences. User preferences will not be used for model selection in filename generation.")
            # current_user_prefs remains None

    # Initialize Gemini model based on available user_prefs or fallback to default
    if not gemini_config.is_initialized():
        if not gemini_config.initialize_gemini_globally():
            logging.error(f"Gemini not initialized for filename extraction: {gemini_config.get_last_error()}")
            return None

    if current_user_prefs:
        selected_model_name = gemini_config.get_selected_gemini_model(current_user_prefs)
        logging.info(f"Using Gemini model for filename extraction: {selected_model_name}")
    else:
        selected_model_name = gemini_config.DEFAULT_GEMINI_MODEL
        logging.warning(f"UserPreferences not available or failed to load, using default model for filename extraction: {selected_model_name}")
    
    model = genai.GenerativeModel(selected_model_name)

    try:
        analysis_prompt_text = f"""
        Extract the main subject or theme from this wallpaper description in 2-5 words.
        Only return the extracted subject - no explanations or additional text.
        Make it suitable for use as a filename (e.g., lowercase, underscores for spaces).

        Description: {prompt}
        """
        response = model.generate_content(contents=analysis_prompt_text)

        if response and hasattr(response, 'text') and response.text:
            subject = response.text.strip().lower()
            subject = subject.replace('"', '').replace("'", "") # Remove quotes
            subject = re.sub(r'[^\w\s-]', '', subject) # Remove non-alphanumeric (keep spaces, hyphens)
            subject = re.sub(r'[-\s]+', '_', subject) # Replace spaces/hyphens with underscores
            subject = subject.strip('_') # Remove leading/trailing underscores
            logging.debug(f"Extracted subject for filename: {subject} from prompt: '{prompt[:50]}...'")
            return subject if subject else None
        else:
            logging.warning(f"Empty response from Gemini for subject extraction (filename). Prompt: '{prompt[:50]}...'")
            return None
    except Exception as e:
        logging.error(f"Error extracting subject with Gemini for filename: {e}", exc_info=True)
        return None


def create_filename_from_prompt(prompt: str, max_length: int = 30) -> str:
    """
    Create a descriptive filename from the prompt (fallback if subject extraction fails).
    (Moved from wallpaper_generator.py)
    """
    sanitized = html.unescape(prompt) # Decode HTML entities first
    sanitized = re.sub(r'[^\w\s-]', '', sanitized.lower()) # Keep alphanumeric, spaces, hyphens
    sanitized = re.sub(r'[-\s]+', '_', sanitized).strip('_')

    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
        # Try to cut at a word boundary if possible
        if '_' in sanitized:
            sanitized = sanitized.rsplit('_', 1)[0]
    
    if not sanitized: # If prompt was all special characters
        sanitized = "generated_image"

    hash_object = hashlib.sha256(prompt.encode('utf-8')) # Ensure consistent encoding
    short_hash = hash_object.hexdigest()[:8]
    return f"{sanitized}_{short_hash}.png"


def get_image_cache_path(prompt: str, project_root_dir: str) -> str:
    """
    Get the full cache path for a generated image based on the prompt.
    Does NOT create the directory. Directory creation is handled by cache_utils.
    (Refactored from get_generated_image_path in wallpaper_generator.py)
    Args:
        prompt (str): The prompt used for generation.
        project_root_dir (str): Absolute path to the project's root directory.
    Returns:
        str: The absolute path where the image should be cached.
    """
    genimage_dir_name = "genimage" # Name of the image cache subdirectory
    
    # Attempt to get a meaningful filename part from the prompt's subject
    subject_part = extract_subject_from_prompt_for_filename(prompt)
    
    if subject_part:
        base_filename = re.sub(r'[^\w-]', '', subject_part) # Further sanitize
        base_filename = base_filename[:25] # Limit length of subject part
        hash_object = hashlib.sha256(prompt.encode('utf-8'))
        short_hash = hash_object.hexdigest()[:8]
        filename = f"{base_filename}_{short_hash}.png"
    else:
        # Fallback to general filename creation if subject extraction fails
        filename = create_filename_from_prompt(prompt)

    # Path construction: <project_root>/genimage/<filename>
    # This assumes 'genimage' is directly under the project root.
    cache_dir = os.path.join(project_root_dir, genimage_dir_name)
    return os.path.join(cache_dir, filename)


# --- Image Cache and File Operations ---

def check_image_cache(image_path: str) -> bool:
    """
    Checks if an image exists at the given path.
    (New function as per plan)
    """
    return os.path.exists(image_path)


def move_temp_image_to_cache(temp_image_path: str, final_cache_path: str) -> bool:
    """
    Moves/copies a temporary image file to its final cache location.
    Creates the destination directory if it doesn't exist.
    (New function as per plan)
    """
    try:
        if not os.path.exists(temp_image_path):
            logging.error(f"Temporary image not found at {temp_image_path}, cannot move to cache.")
            return False
            
        cache_dir = os.path.dirname(final_cache_path)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir, exist_ok=True)
            logging.info(f"Created cache directory: {cache_dir}")
        
        # Use shutil.move for atomicity if on the same filesystem,
        # or shutil.copy2 then os.remove for cross-filesystem compatibility.
        # shutil.move handles cross-filesystem by copying and deleting.
        shutil.move(temp_image_path, final_cache_path)
        logging.info(f"Image moved from temporary location {temp_image_path} to cache: {final_cache_path}")
        _temp_files.discard(os.path.abspath(temp_image_path)) # Unregister from temp cleanup
        return True
    except Exception as e:
        logging.error(f"Error moving temp image {temp_image_path} to cache {final_cache_path}: {e}", exc_info=True)
        return False


def list_sorted_generated_images(image_directory_path: str) -> List[str]:
    """
    List and sort image files in a directory by modification time (newest first).
    (Moved from list_sorted_genimages in wallpaper_generator.py)
    Args:
        image_directory_path (str): Absolute path to the directory containing images.
    Returns:
        List[str]: Sorted list of image filenames.
    """
    try:
        if not os.path.isdir(image_directory_path):
            logging.warning(f"Image directory not found: {image_directory_path}")
            return []

        # Get list of image files with full paths for sorting
        files_with_paths = [
            os.path.join(image_directory_path, f)
            for f in os.listdir(image_directory_path)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")) # Added webp
        ]

        if not files_with_paths:
            return []

        # Sort by modification time (newest first)
        sorted_files_with_paths = sorted(
            files_with_paths, key=lambda f: os.path.getmtime(f), reverse=True
        )
        
        image_filenames = [os.path.basename(f) for f in sorted_files_with_paths]
        return image_filenames
        
    except OSError as e: # Catch permission errors etc.
        logging.error(f"OS error listing images in '{image_directory_path}': {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error listing images in '{image_directory_path}': {e}", exc_info=True)
        return []


# --- Generic JSON Saving ---

def save_json_data(data: Dict[Any, Any], filename: str, project_root_dir: str) -> bool:
    """
    Saves dictionary data to a JSON file in the project root.
    (Moved from save_prompts_to_json in wallpaper_generator.py, made generic)
    Args:
        data (dict): The dictionary to save.
        filename (str): The name of the JSON file (e.g., "prompts.json").
        project_root_dir (str): Absolute path to the project's root directory.
    Returns:
        bool: True if successful, False otherwise.
    """
    file_path = os.path.join(project_root_dir, filename)
    try:
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logging.info(f"Data successfully saved to JSON file: {file_path}")
        return True
    except IOError as e: # Catch file write errors
        logging.error(f"IOError saving data to JSON file '{file_path}': {e}")
        return False
    except TypeError as e: # Catch issues with data not being JSON serializable
        logging.error(f"TypeError: Data not JSON serializable for file '{file_path}': {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error saving data to JSON file '{file_path}': {e}", exc_info=True)
        return False


# --- Original deep_update from existing file_utils.py ---
def deep_update(d: Dict, u: Dict) -> Dict:
    """
    Recursively update nested dictionaries.
    (Existing in file_utils.py)
    """
    for k, v in u.items():
        if isinstance(v, dict): # Check if v is a dictionary itself
            d[k] = deep_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

# It's good practice to have a way to explicitly register the cleanup
# if app_utils is not guaranteed to be imported first or if this module is used standalone.
# However, the plan is for app_utils to handle this.
# atexit.register(_cleanup_all_temp_files) # This should be called ONCE by the application.
