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
import sys
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
            model = genai.GenerativeModel('gemini-2.5-pro-preview-03-25')
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
        # Add random timestamp to make each request unique
        import time
        timestamp = int(time.time())
        
        # Define historically accurate style categories and their elements
        style_categories = {
            "classical_art": {
                "period": "15th-19th Century Traditional Art",
                "styles": ["oil_painting", "watercolor", "charcoal", "pencil_sketch"],
                "moods": ["serene", "contemplative", "romantic", "peaceful"],
                "art_movements": ["Renaissance", "Baroque", "Romanticism", "Realism"],
                "lighting": ["Natural light", "Chiaroscuro", "Golden hour", "Soft diffused"],
                "color_schemes": ["Earth tones", "Rich jewel tones", "Muted naturals", "Venetian palette"]
            },
            "asian_traditional": {
                "period": "Traditional East Asian Art",
                "styles": ["ink_drawing", "woodcut", "ukiyo_e"],
                "moods": ["tranquil", "philosophical", "contemplative", "peaceful"],
                "art_movements": ["Literati painting", "Ukiyo-e", "Sumi-e"],
                "lighting": ["Atmospheric", "Misty", "Dawn light", "Dusk light"],
                "color_schemes": ["Ink wash", "Limited palette", "Natural pigments"]
            },
            "modern_art": {
                "period": "20th Century Modern Art",
                "styles": ["abstract", "expressionism", "minimalist", "pop_art"],
                "moods": ["dynamic", "contemplative", "energetic", "dramatic"],
                "art_movements": ["Abstract Expressionism", "Minimalism", "Bauhaus", "De Stijl"],
                "lighting": ["Studio lighting", "High contrast", "Geometric shadows"],
                "color_schemes": ["Primary colors", "Monochromatic", "Color field", "Geometric"]
            },
            "digital_age": {
                "period": "Contemporary Digital Art",
                "styles": ["digital_art", "cyberpunk", "retrowave", "low_poly"],
                "moods": ["energetic", "mysterious", "dynamic", "futuristic"],
                "art_movements": ["Digital Minimalism", "Vaporwave", "Neo-cyberpunk"],
                "lighting": ["Neon", "Volumetric", "Ray traced", "Ambient occlusion"],
                "color_schemes": ["Synthwave palette", "RGB aesthetics", "Duotone", "Gradient"]
            }
        }

        # Select a random art period/category
        category_name = random.choice(list(style_categories.keys()))
        category = style_categories[category_name]

        prompt = f"""
        Generate a HISTORICALLY ACCURATE and ARTISTICALLY COHERENT set of wallpaper preferences.
        Focus on creating an authentic representation of {category['period']}.
        Use this random seed for inspiration: {timestamp}

        HISTORICAL CONTEXT:
        You are creating art in the style and tradition of {category['period']}.
        All elements must be historically appropriate for this period and tradition.
        
        AVAILABLE ELEMENTS (choose only from these period-appropriate options):
        - Artistic Styles: {', '.join(category['styles'])}
        - Cultural Moods: {', '.join(category['moods'])}
        - Art Movements: {', '.join(category['art_movements'])}
        - Period Lighting: {', '.join(category['lighting'])}
        - Historical Color Schemes: {', '.join(category['color_schemes'])}

        IMPORTANT RULES:
        1. ONLY use elements from the lists above
        2. ALL choices must be historically accurate to {category['period']}
        3. Create a preset name that reflects the specific period and style
        4. Ensure lighting and color choices match historical techniques

        The output should be valid JSON format with the following structure:
        {{
            "preset_name": "[create an evocative, unique name that captures the essence of the combination]",
            "styles": [pick 1 style from the list below, but interpret it in an unexpected way],
            "moods": [pick 1 mood that creates an interesting tension or harmony with the style],
            "imagen_settings": {{
                "style_settings": {{
                    "art_movement": "[pick an art movement that adds depth to the style, or 'None']",
                    "post_processing": [0-1 creative post-processing effects that enhance the concept]
                }},
                "camera_settings": {{
                    "camera_model": "[pick a camera that adds character, or 'None']",
                    "lens_type": "[choose a lens that creates a unique perspective, or 'None']",
                    "aperture": "[select an aperture that supports the mood, or 'None']",
                    "depth_of_field": "[pick a setting that enhances the composition, or 'None']"
                }},
                "lighting_settings": {{
                    "lighting_type": "[choose lighting that creates atmosphere, or 'None']",
                    "time_of_day": "[select a time that adds drama or subtlety, or 'None']",
                    "light_quality": "[pick quality that reinforces the mood, or 'None']"
                }},
                "composition_settings": {{
                    "technique": "[select a technique that adds visual interest, or 'None']",
                    "camera_angle": "[choose an angle that creates impact, or 'None']"
                }},
                "color_settings": {{
                    "color_scheme": "[pick a scheme that complements or contrasts effectively, or 'None']",
                    "palette_type": "[select a palette that enhances the theme, or 'None']",
                    "color_temperature": "[choose temperature that adds emotion, or 'None']"
                }}
            }},
            "aspect_ratio": "[choose from: 16:9, 4:3, 1:1, or 9:16 based on composition]"
        }}

        Style options (pick 1 and interpret creatively):
        ["traditional_art", "digital_art", "abstract", "anime", "art_deco", "art_nouveau", "cartoon", "charcoal", "cinematic", "comic_book", "cyberpunk", "divisionism", "double_exposure", "expressionism", "fantasy", "futurism", "glitch_art", "gothic", "graffiti", "hyperrealism", "impressionism", "ink_drawing", "isometric", "landscape", "line_art", "low_poly", "manga", "minimalist", "oil_painting", "paper_cut", "pastel", "pencil_sketch", "pixel_art", "pointillism", "pop_art", "realism", "retrowave", "sci_fi", "sketch", "stained_glass", "steampunk", "surrealism", "ukiyo_e", "vaporwave", "watercolor", "woodcut"]
        
        Mood options (pick 1 that creates interesting dynamics):
        ["peaceful", "serene", "tranquil", "calm", "relaxing", "soothing", "energetic", "vibrant", "dynamic", "exciting", "dramatic", "intense", "mysterious", "enigmatic", "cryptic", "eerie", "romantic", "passionate", "tender", "joyful", "cheerful", "happy", "playful", "whimsical", "dreamy", "contemplative", "thoughtful", "philosophical", "inspiring", "uplifting", "motivational"]

        Focus on creating SURPRISING and INNOVATIVE combinations that still work together artistically. Use "None" for settings that don't fit your vision, but make bold choices where they enhance the concept.
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
                            # Use the AI-generated preset name
                            save_name = preset_data.get("preset_name", "Unnamed AI Preset")
                            # Clean up name for file system
                            save_name = re.sub(r'[^a-zA-Z0-9 _-]', '', save_name).strip()
                            if not save_name:
                                save_name = "unnamed-preset"

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

def main():
    """Main entry point for CLI usage of the AI preset generator."""
    import argparse
    from wallpaper_settings import get_preferences, initialize_settings, load_preset, save_preset, delete_preset

    parser = argparse.ArgumentParser(description='Generate and manage AI presets for wallpaper generation')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Generate preset command
    gen_parser = subparsers.add_parser('generate', help='Generate a new preset')
    gen_parser.add_argument('--auto-save', action='store_true', help='Automatically save the preset')

    # List presets command
    subparsers.add_parser('list', help='List all available presets')

    # Load preset command
    load_parser = subparsers.add_parser('load', help='Load and display a preset')
    load_parser.add_argument('name', help='Name of the preset to load')

    # Delete preset command
    del_parser = subparsers.add_parser('delete', help='Delete a preset')
    del_parser.add_argument('name', help='Name of the preset to delete')

    args = parser.parse_args()
    user_prefs = initialize_settings()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == 'generate':
        result = generate_ai_preset(user_prefs)
        if isinstance(result, str):
            print(f"Preset saved to: {result}")
        elif result is None:
            print("Preset generated but not saved")
        else:
            print("Failed to generate preset")
            sys.exit(1)

    elif args.command == 'list':
        # List all presets in the presets directory
        presets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "presets")
        if os.path.exists(presets_dir):
            presets = [f[:-5] for f in os.listdir(presets_dir) if f.endswith('.json')]
            if presets:
                print("\nAvailable presets:")
                for preset in sorted(presets):
                    print(f"  {preset}")
            else:
                print("No presets found")
        else:
            print("No presets directory found")

    elif args.command == 'load':
        preset_path = os.path.join('presets', f"{args.name}.json")
        if os.path.exists(preset_path):
            try:
                with open(preset_path, 'r') as f:
                    preset_data = json.load(f)
                print("\nPreset contents:")
                print(json.dumps(preset_data, indent=2))
                
                # Apply the preset settings to user preferences
                if preset_data.get("styles"):
                    user_prefs.preferred_styles = preset_data["styles"]
                if preset_data.get("moods"):
                    user_prefs.preferred_moods = preset_data["moods"]
                if preset_data.get("imagen_settings"):
                    user_prefs.imagen_settings.update(preset_data["imagen_settings"])
                if preset_data.get("aspect_ratio"):
                    user_prefs.aspect_ratio = preset_data["aspect_ratio"]
                
                # Save the updated preferences
                user_prefs.save_preferences()
                print("Preset applied and saved to user preferences")
            except Exception as e:
                print(f"Error loading preset: {e}")
                sys.exit(1)
        else:
            print(f"Preset '{args.name}' not found")
            sys.exit(1)

    elif args.command == 'delete':
        preset_path = os.path.join('presets', f"{args.name}.json")
        if os.path.exists(preset_path):
            try:
                os.remove(preset_path)
                print(f"Preset '{args.name}' deleted successfully")
            except Exception as e:
                print(f"Error deleting preset: {e}")
                sys.exit(1)
        else:
            print(f"Preset '{args.name}' not found")
            sys.exit(1)

if __name__ == "__main__":
    main()