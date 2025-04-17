#!/usr/bin/env python3
"""AI Preset Generator - Generate random wallpaper preferences using Gemini AI

This script uses Google's Gemini AI to create intelligent, coherent random presets 
for the wallpaper generator application.
"""

import os
import json
import logging
import random
import hashlib
from typing import Dict, Any, List, Optional, Union # <-- Add Union

# Import Gemini API
try:
    import google.generativeai as genai
except ImportError:
    print("Error: google-generativeai package not installed")
    print("Please install it with: pip install google-generativeai")
    exit(1)

# Import from wallpaper_settings for user preferences
from wallpaper_settings import UserPreferences, get_preferences, initialize_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ai_preset_generator.log")
    ]
)

# Default style categories for style mixing
DEFAULT_STYLE_CATEGORIES = {
    "photographic": ["cinematic", "documentary", "film_grain", "polaroid", 
                  "analog_film", "lomography", "long_exposure"],
    "artistic": ["abstract", "impressionism", "expressionism", "cubism", 
                 "minimalism", "watercolor", "oil_painting", "acrylic", 
                 "stained_glass", "steampunk", "surrealism", "vaporwave"],
    "illustration": ["anime", "cartoon", "comic_book", "divisionism", "graffiti", 
                   "ink_drawing", "line_art", "manga", "paper_cut", "pixel_art", 
                   "pointillism", "pop_art", "ukiyo_e"]
}

# Cache file for storing previously generated presets
PRESETS_CACHE_FILE = "generated_presets_cache.json"

def get_gemini_api_key() -> Optional[str]:
    """
    Retrieve the Gemini API key from environment variable or config file.
    
    Returns:
        str: The API key if found, None otherwise
    """
    # First try environment variable
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        return api_key
    
    # Then try config file
    try:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                config = json.load(f)
                return config.get("gemini_api_key")
    except Exception as e:
        logging.error(f"Error reading config file: {e}")
    
    return None

def generate_random_style_mix() -> str:
    """Generate a random style mix from compatible styles.
    
    Returns:
        str: A string containing 2-3 compatible styles joined with " + "
    """
    # Select a random category
    category = random.choice(list(DEFAULT_STYLE_CATEGORIES.keys()))
    
    # Select 2-3 compatible styles from the same category
    num_styles = random.randint(2, 3)
    available_styles = DEFAULT_STYLE_CATEGORIES[category]
    if len(available_styles) < num_styles:
        num_styles = len(available_styles)
    
    selected_styles = random.sample(available_styles, num_styles)
    return " + ".join(selected_styles)

def load_cached_presets() -> List[str]:
    """Load previously generated preset hashes from cache file."""
    if os.path.exists(PRESETS_CACHE_FILE):
        try:
            with open(PRESETS_CACHE_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading presets cache: {e}")
    return []

def save_preset_to_cache(preset_data: Dict[str, Any]) -> None:
    """Save a preset hash to the cache file to avoid regenerating it."""
    preset_hash = hashlib.md5(json.dumps(preset_data, sort_keys=True).encode()).hexdigest()
    
    cached_presets = load_cached_presets()
    cached_presets.append(preset_hash)
    
    # Keep only the last 50 presets to avoid infinite growth
    if len(cached_presets) > 50:
        cached_presets = cached_presets[-50:]
    
    try:
        with open(PRESETS_CACHE_FILE, 'w') as f:
            json.dump(cached_presets, f)
    except Exception as e:
        logging.error(f"Error saving to presets cache: {e}")

def is_preset_unique(preset_data: Dict[str, Any]) -> bool:
    """Check if a preset is unique compared to previously generated ones."""
    preset_hash = hashlib.md5(json.dumps(preset_data, sort_keys=True).encode()).hexdigest()
    cached_presets = load_cached_presets()
    return preset_hash not in cached_presets

# Modify the return type hint and docstring
def generate_ai_preset(user_prefs: UserPreferences) -> Union[str, bool, None]: # <-- Modified return type
    """
    Generate a random preset with coherent settings using Gemini AI.

    This function uses Gemini to create a set of preferences that are coherent
    and stylistically matched, rather than just randomly selecting values.

    Args:
        user_prefs: The UserPreferences object (used for context, not modified directly)

    Returns:
        Union[str, bool, None]:
            - str: The path to the saved preset file if saved by the user.
            - None: If the preset was generated but the user chose not to save it.
            - False: If generation failed (API error, no unique preset found).
    """
    api_key = get_gemini_api_key()
    if not api_key:
        logging.error("No Gemini API key found. Please set GEMINI_API_KEY environment variable or add it to config.json")
        print("Error: Gemini API key not configured.") # User-facing message
        return False

    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        # Ensure the model name is correct, adjust if needed based on availability
        try:
            # Using flash for potentially faster/cheaper generation, consider making this configurable
            model = genai.GenerativeModel('gemini-1.5-flash')
        except Exception as model_err:
            logging.error(f"Failed to initialize Gemini model: {model_err}")
            print(f"Error: Could not initialize AI model. Please check configuration and model availability.")
            return False

        # Decide whether to use mixed styles (50% chance) - Removed as prompt now handles single style selection
        # use_mixed_styles = random.choice([True, False])
        # mixed_style = None
        # if use_mixed_styles:
        #     mixed_style = generate_random_style_mix()
        #     logging.info(f"Using mixed style: {mixed_style}")

        # Create the request for a coherent set of preferences
        # Updated prompt for clarity and to request "None" for inapplicable fields
        prompt = """
        Generate a random but coherent set of wallpaper generation preferences. Create settings that would work well together artistically.
        The output should be valid JSON format with the following structure:
        {
            "preset_name": "[a creative name for this preset, e.g., 'Cyberpunk Sunset' or 'Minimalist Forest']",
            # "genres" field removed as requested
            "styles": [list of 1 artistic style],
            "moods": [list of 1 mood],
            "imagen_settings": {
                "style_settings": {
                    "art_movement": "[a fitting art movement or 'None']",
                    "post_processing": [list of 0-1 post-processing effects]
                },
                "camera_settings": {
                    "camera_model": "[appropriate camera model or 'None']",
                    "lens_type": "[appropriate lens type or 'None']",
                    "aperture": "[appropriate aperture setting or 'None']",
                    "depth_of_field": "[appropriate depth setting or 'None']"
                },
                "lighting_settings": {
                    "lighting_type": "[appropriate lighting type or 'None']",
                    "time_of_day": "[appropriate time of day or 'None']",
                    "light_quality": "[appropriate light quality or 'None']"
                },
                "composition_settings": {
                    "technique": "[appropriate composition technique or 'None']",
                    "camera_angle": "[appropriate camera angle or 'None']"
                },
                "color_settings": {
                    "color_scheme": "[appropriate color scheme or 'None']",
                    "palette_type": "[appropriate palette type or 'None']",
                    "color_temperature": "[appropriate color temperature or 'None']"
                }
            },
            "aspect_ratio": "[choose ONLY from these specific values: 16:9, 4:3, 1:1, or 9:16]"
        }

        # Genre options removed as requested

        Choose 1 from these style options:
        ["traditional_art", "digital_art", "abstract", "anime", "art_deco", "art_nouveau", "cartoon", "charcoal", "cinematic", "comic_book", "cyberpunk", "divisionism", "double_exposure", "expressionism", "fantasy", "futurism", "glitch_art", "gothic", "graffiti", "hyperrealism", "impressionism", "ink_drawing", "isometric", "landscape", "line_art", "low_poly", "manga", "minimalist", "oil_painting", "paper_cut", "pastel", "pencil_sketch", "pixel_art", "pointillism", "pop_art", "realism", "retrowave", "sci_fi", "sketch", "stained_glass", "steampunk", "surrealism", "ukiyo_e", "vaporwave", "watercolor", "woodcut"]
        
        Choose 1 from these mood options:
        ["peaceful", "serene", "tranquil", "calm", "relaxing", "soothing", "energetic", "vibrant", "dynamic", "exciting", "dramatic", "intense", "mysterious", "enigmatic", "cryptic", "eerie", "romantic", "passionate", "tender", "joyful", "cheerful", "happy", "playful", "whimsical", "dreamy", "contemplative", "thoughtful", "philosophical", "inspiring", "uplifting", "motivational"]

        Ensure all settings are coherent and artistically compatible. Use "None" (as a string) for settings where no specific value is appropriate for the generated theme.
        """

        # Removed mixed style logic from prompt generation

        # Try up to 3 times to generate a unique preset
        for attempt in range(3):
            # Get the response
            try:
                response = model.generate_content(contents=prompt)
            except Exception as api_err:
                 logging.error(f"Error during Gemini API call: {api_err}")
                 print(f"Error: Failed to communicate with AI service ({api_err}).")
                 return False # Treat API errors as failure

            if response and response.text:
                # Extract the JSON from the response
                response_text = response.text.strip()
                import re
                # Handle optional markdown code block ```json ... ```
                json_match = re.search(r'```json\s*({[\s\S]*?})\s*```|({[\s\S]*})', response_text)

                if json_match:
                    json_content = json_match.group(1) or json_match.group(2) # Get content from either group
                    try:
                        preset_data = json.loads(json_content)
                        # Basic validation of structure
                        if not isinstance(preset_data, dict) or "preset_name" not in preset_data:
                             raise json.JSONDecodeError("Missing required fields", json_content, 0)
                    except json.JSONDecodeError as json_err:
                        logging.error(f"Failed to decode JSON from Gemini response: {json_err}\nResponse: {json_content}")
                        if attempt < 2:
                            print("Warning: Received invalid data format from AI, retrying...")
                            continue # Go to next attempt
                        else:
                            print("Error: Received invalid data format from AI service after multiple attempts.")
                            return False

                    # Check if this preset is unique compared to previous ones
                    if is_preset_unique(preset_data):
                        preset_name = preset_data.get("preset_name", "Unnamed AI Preset")
                        print(f"\n--- AI Generated Preset: '{preset_name}' ---")
                        # Display the generated preset details nicely
                        try:
                            print(json.dumps(preset_data, indent=2))
                        except Exception: # Catch potential errors during printing complex data
                            print("[Could not display full preset details]")
                        print("------------------------------------------")

                        # --- MODIFICATION START: User confirmation and saving ---
                        # Ask user for confirmation
                        while True:
                            confirm = input(f"Save this generated preset? (Y/N): ").strip().lower()
                            if confirm in ['y', 'n']:
                                break
                            print("Invalid input. Please enter 'Y' or 'N'.")

                        if confirm == 'y':
                            # Ask for preset name
                            while True:
                                save_name = input("Enter a name for this preset (alphanumeric, spaces, hyphens allowed): ").strip()
                                # Basic validation for filename safety
                                if re.match(r"^[a-zA-Z0-9 _-]+$", save_name) and save_name:
                                    break
                                print("Invalid name. Please use only letters, numbers, spaces, or hyphens.")

                            # Define presets directory and ensure it exists
                            presets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "presets")
                            os.makedirs(presets_dir, exist_ok=True)

                            # Construct file path
                            preset_filename = f"{save_name}.json"
                            preset_filepath = os.path.join(presets_dir, preset_filename)

                            # Check for existing file
                            if os.path.exists(preset_filepath):
                                overwrite = input(f"Preset '{save_name}' already exists. Overwrite? (Y/N): ").strip().lower()
                                if overwrite != 'y':
                                    print("Preset not saved.")
                                    return None # User chose not to overwrite

                            # Save the preset data (the dictionary) to the file
                            try:
                                with open(preset_filepath, 'w') as f:
                                    json.dump(preset_data, f, indent=4)
                                print(f"Preset '{save_name}' saved successfully to {preset_filepath}")

                                # Save this preset to cache so we don't generate it again
                                save_preset_to_cache(preset_data)
                                return preset_filepath # Return the path on successful save
                            except IOError as e:
                                logging.error(f"Error saving preset file {preset_filepath}: {e}")
                                print(f"Error: Could not save preset file. Check permissions.")
                                return False # Indicate failure

                        else:
                            print("Preset discarded.")
                            # Don't save to cache if discarded
                            return None # Return None if user chose not to save
                        # --- MODIFICATION END ---

                    else:
                        logging.info(f"Generated preset was not unique, trying again (attempt {attempt+1}/3)")
                        # Continue to the next attempt
                else:
                    logging.error(f"Could not extract JSON from Gemini response. Response: {response_text}")
                    if attempt < 2:
                        print("Warning: Received unexpected data from AI, retrying...")
                    else:
                        print("Error: Failed to get valid data from AI after multiple attempts.")
                        return False # Failed after retries
            else:
                # Handle cases where response exists but response.text is None or empty
                err_msg = f"Empty or invalid response text from Gemini (Attempt {attempt+1}/3)."
                if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                     err_msg += f" Feedback: {response.prompt_feedback}"
                logging.error(err_msg)

                if attempt < 2:
                    print("Warning: Received empty response from AI, retrying...")
                else:
                    print("Error: Failed to get response from AI after multiple attempts.")
                    # Check for specific blocking reason if available
                    if hasattr(response, 'prompt_feedback') and response.prompt_feedback.block_reason:
                         print(f"Reason: Request blocked due to {response.prompt_feedback.block_reason.name}")
                    return False # Failed after retries

        # If we get here, we failed to generate a unique preset after 3 attempts
        logging.warning("Could not generate a unique preset after 3 attempts")
        print("Failed to generate a unique AI preset after multiple attempts.")
        return False # Indicate failure

    except genai.types.generation_types.BlockedPromptException as e:
        logging.error(f"Gemini prompt blocked: {e}")
        print(f"Error: AI generation request was blocked. Please try different settings or check content policies. Details: {e}")
        return False
    except Exception as e:
        logging.exception(f"An unexpected error occurred during AI preset generation: {e}") # Log full traceback
        print(f"An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    # For testing
    from wallpaper_settings import get_preferences, initialize_settings
    
    # Make sure preferences are initialized
    user_prefs = get_preferences()
    if user_prefs is None:
        user_prefs = initialize_settings()
        
    # Test the modified function
    result = generate_ai_preset(user_prefs)
    
    # Handle the new return types from the modified function
    if isinstance(result, str):
        print(f"\nTest successful: Preset saved to {result}")
    elif result is None:
        print("\nTest successful: Preset generated but discarded by user.")
    else: # result is False
        print("\nTest failed: Preset generation failed.")
    if isinstance(result, str):
        print(f"\nTest successful: Preset saved to {result}")
    elif result is None:
        print("\nTest successful: Preset generated but discarded by user.")
    else: # result is False
        print("\nTest failed: Preset generation failed.")