import argparse
import difflib
import json
import logging
import os
import random
import re
import sys
import time
from typing import Dict, Optional

from google import genai # Use the new SDK import
from google.genai import types # Import types for consistency

# NOTE: This module assumes wallpaper_settings.py is part of the wall_gen package.
from . import gemini_config # Import the new centralized configuration
from .ui_utils import (
    get_validated_input,
    print_info,
    print_section,
    print_success,
    print_warning,
)
# UserPreferences is obtained via get_preferences, initialize_settings also used in main
from .wallpaper_settings import get_preferences, initialize_settings

# Configure logging for this module
# logging.basicConfig( # BasicConfig should ideally be called once at app entry.
#     level=logging.INFO, # Assuming it's handled by app_utils or main script.
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )
logger = logging.getLogger(__name__) # Get logger instance

# --- Constants ---
# DEFAULT_MODEL is now in gemini_config
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# --- Global State ---
# GeminiState class and gemini_state instance are removed.
# Initialization and state are handled by gemini_config.

# _attempt_init_from_env() is removed. gemini_config handles auto-init.

# Module-level constant for category mappings
CATEGORY_MAPPINGS = {
    "oil_painting": {
        "oil", "impasto", "baroque", "impression", "post-impression", "romanticism",
        "expressionism", "fauvism", "pointillism", "divisionism", "van gogh", "renoir", "manet"
    },
    "watercolor": {"watercolor", "watercolour", "aquarelle"},
    "pastel": {"pastel", "degas"},
    "charcoal": {"charcoal", "carboncillo"},
    "pencil_sketch": {"pencil", "graphite", "colored pencil"},
    "ink_drawing": {"ink", "pen & ink", "line", "pen and ink"},
    "minimalist": {"minimal", "minimalism", "reductive"},
    "geometric": {"geometric", "geometry", "polygon", "low poly", "constructivism"},
    "minimalist_geometric": {"minimalist geometric", "minimal geometric", "geometric minimalism"},
    "psychedelic": {"psychedelic", "trippy", "hallucinogenic", "psychedelia"},
    "surrealism": {"surrealism", "surreal", "dreamlike", "fantastical"},
    "fantasy_landscape": {"fantasy landscape", "fantastical landscape", "enchanted landscape"},
    "cyberpunk_cityscape": {"cyberpunk cityscape", "neon city", "futuristic cityscape"},
    "illustration_pixel": {"pixel", "8-bit", "16-bit", "pixelated"},
    "illustration_anime_manga": {"anime", "manga", "shojo", "shonen", "seinen"},
    "illustration_comic": {"comic", "graphic novel"},
    "illustration_cubist": {"cubist", "geometric", "fragmented"},
    "illustration_surreal": {"surreal", "dreamlike", "fantastical"},
    "illustration_steampunk": {"steampunk", "victorian", "industrial fantasy"},
    "photographic": {"photo", "realistic", "photograph", "film", "kodak", "dslr", "cinematic", "fujifilm", "shot on", "hyperreal"},
    "game_style": {"game", "engine", "unreal", "unity", "fps", "rpg", "rendered", "in-engine"},
    "digital_art": {"digital", "vector", "glitch", "vaporwave", "retrowave", "3d", "render"},
    "abstract_conceptual": {"abstract", "conceptual", "cubist", "fauvist", "expressionist", "non-representational", "dreamscape", "surreal"},
    "material_sculptural": {"sculpture", "sculpted", "statue", "bust", "relief", "bronze", "marble", "clay"},
    "fantasy": {"fantasy", "mythical", "magical", "wizard", "fairy", "dragon", "unicorn", "castle"},
    "sci_fi": {"sci-fi", "science fiction", "cyberpunk", "futuristic", "spaceship", "space opera"}
}

def initialize_gemini(api_key: str) -> bool:
    """
    Initialize the Gemini model globally using the centralized configuration.
    Returns True if initialization was successful, False otherwise.
    """
    logger.info(f"Attempting to initialize Gemini globally with provided API key.")
    success = gemini_config.initialize_gemini_globally(api_key_override=api_key)
    if success:
        logger.info("Gemini globally initialized successfully with new API key.")
    else:
        logger.error(f"Failed to initialize Gemini globally: {gemini_config.get_last_error()}")
    return success

def generate_style_prompt(category: Optional[str] = None, style_type: str = "simple") -> str:
    """
    Construct a prompt string for the Gemini model to generate an art style or descriptor.

    This function builds a prompt that instructs Gemini to generate either a simple style phrase
    or a detailed style name and description, optionally constrained to a specific art category.

    Args:
        category (Optional[str]): Optional art style category to constrain the generation.
        style_type (str): 'simple' for a single style phrase, 'detailed' for name + description.

    Returns:
        str: The constructed prompt string for Gemini.
    """
    base = "You are an expert AI art style generator. "
    if category and category == "illustration_cubist":
        base += (
            "Limit the style to the 'cubist' style of illustration. "
            "Focus on the distinctive characteristics, techniques, or traditions of cubism in illustration."
        )
    elif category:
        base += (
            f"Limit the style to the '{category}' category of art/design. "
            "Focus on the distinctive characteristics, techniques, or traditions of this category."
        )

    if style_type == "simple":
        core = (
            "Generate one clear, focused artistic style description representing a single visual concept. "
            "No multiple descriptive elements or comma-separated themes. "
            "Good: 'vibrant cyberpunk neon'. "
            "Bad: 'dark gothic, medieval architecture, with misty atmosphere'. "
            "Focus on one main style. Output only the style phrase."
        )
    else:
        core = (
            "Suggest a style name (2-4 words) suitable for an AI art preset, and a 1-2 sentence description of its visual or technical hallmarks. "
            "Format the output as a JSON object with two keys: \"name\" and \"description\". "
            "Example: {\"name\": \"Vibrant Dreamscape\", \"description\": \"Characterized by vivid, surreal colors and flowing, organic shapes. Often evokes a sense of wonder and ethereal beauty.\"}"
            "Output only the JSON object."
        )
    return base + core

def generate_random_style(category: Optional[str] = None, style_type: str = "simple") -> Optional[Dict[str, str]]:
    """
    Use Gemini to generate a random style, optionally for a specific canonical category.
    Implements retry logic with exponential backoff and improved error handling.
    
    Args:
        category: Optional category to constrain the style generation
        style_type: Type of style to generate ('simple' or 'detailed')
    
    Returns:
        Optional[Dict[str, str]]: The generated style as a dictionary with 'name' and 'description' keys,
        or None if generation fails
    """
    user_prefs = get_preferences() # Get user_prefs to pass to model selection
    if not gemini_config.is_initialized():
        # Attempt to initialize if not already (e.g. if env var was set after module load)
        if not gemini_config.initialize_gemini_globally():
            error_msg = gemini_config.get_last_error() or "Unknown initialization error."
            logger.error(f"Gemini not initialized for generate_random_style: {error_msg}")
            raise RuntimeError(f"Gemini model is not initialized. Please initialize globally or ensure GEMINI_API_KEY is set. Last error: {error_msg}")

    prompt = generate_style_prompt(category, style_type)
    selected_model_name = gemini_config.get_selected_gemini_model(user_prefs)
    logger.info(f"Using Gemini model for style generation: {selected_model_name}")
    logger.debug(f"Generated Gemini prompt for style_type '{style_type}', category '{category}':\n{prompt}")

    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"Generating style (attempt {attempt + 1}/{MAX_RETRIES}) with model {selected_model_name}")
            model = genai.GenerativeModel(selected_model_name)
            response = model.generate_content(prompt)

            style_text = None
            if hasattr(response, 'text') and response.text:
                style_text = response.text.strip()
            elif hasattr(response, 'candidates') and response.candidates and \
                 hasattr(response.candidates[0], 'content') and hasattr(response.candidates[0].content, 'parts') and \
                 response.candidates[0].content.parts and hasattr(response.candidates[0].content.parts[0], 'text'):
                style_text = response.candidates[0].content.parts[0].text.strip()
            else:
                logger.warning("No valid response text or candidates structure from Gemini.")
                # Log the full response if possible and not too large, for debugging
                # logger.debug(f"Full Gemini response: {response}")
                continue # Try next attempt or fail

            style_text = style_text.strip(' "\'\n\r') # Clean the raw text

            if style_type == "detailed":
                parsed_style = None
                # Try to extract and parse JSON
                # Ensure re and json are imported at the top of the file
                json_match = re.search(r'```json\s*(\{.*?\})\s*```|(\{.*?\})', style_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1) or json_match.group(2)
                    try:
                        data = json.loads(json_str)
                        if isinstance(data, dict) and "name" in data and "description" in data:
                            name = str(data["name"]).strip()
                            description = str(data["description"]).strip()
                            if name: # Ensure name is not empty
                                parsed_style = {"name": name, "description": description}
                                logger.info(f"Successfully parsed detailed style: {name}")
                            else:
                                logger.warning(f"Parsed JSON but 'name' field was empty. JSON: {json_str}")
                        else:
                            logger.warning(f"Parsed JSON but required keys ('name', 'description') missing or invalid structure. JSON: {json_str}")
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to decode extracted JSON string: '{json_str}'. Original text: '{style_text}'")
                else:
                    logger.warning(f"No JSON block found in detailed style response: '{style_text}'")

                if parsed_style:
                    return parsed_style # Successfully parsed, exit function
                else:
                    # This attempt for detailed style failed to yield valid JSON.
                    logger.warning(f"Attempt {attempt + 1} failed to get valid detailed JSON. Raw text: '{style_text}'")
                    if attempt < MAX_RETRIES - 1:
                        delay = RETRY_DELAY * (2 ** attempt) # Exponential backoff for parsing failure too
                        logger.info(f"Retrying style generation due to parsing/validation issue in {delay} seconds...")
                        time.sleep(delay)
                        continue # Explicitly continue to next attempt in the for loop
                    else: # Last attempt failed to parse
                        logger.error(f"Failed to generate valid detailed style JSON after {MAX_RETRIES} attempts (parsing/validation failed on last attempt).")
                        return None # Exit function with None

            elif style_type == "simple":
                if style_text: # Ensure simple style text is not empty
                    return {"name": style_text, "description": ""}
                else:
                    logger.warning(f"Attempt {attempt + 1} for simple style returned empty text.")
                    if attempt < MAX_RETRIES - 1:
                        delay = RETRY_DELAY * (2 ** attempt)
                        logger.info(f"Retrying simple style generation due to empty text in {delay} seconds...")
                        time.sleep(delay)
                        continue # Explicitly continue to next attempt
                    else:
                        logger.error(f"Failed to generate simple style after {MAX_RETRIES} attempts (empty text).")
                        return None

        except Exception as e:
            # gemini_state.retry_count removed
            logger.error(f"Error generating style (attempt {attempt + 1}): {e}", exc_info=True)
            if attempt < MAX_RETRIES - 1:
                delay = RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logger.error(f"Failed to generate style after {MAX_RETRIES} attempts.")

    return None

def generate_random_style_by_category(category: str) -> Optional[Dict[str, str]]:
    """
    Generate a random style strictly within a given canonical category (for use in templates/UI).
    Returns the style string.
    """
    return generate_random_style(category=category, style_type="simple")
def canonicalize_style_name(style_name: str) -> str:
    """
    Map a generated/entered style string to a canonical category name.

    This matches incoming style to one of the system-recognized art categories, based on
    fuzzy or partial matching of words/phrases.

    :param style_name: Human/computer-generated style string
    :return: Canonical category, or "unknown"
    """
    # import difflib # Moved to top

    style_name_lower = style_name.lower()
    words = set(style_name_lower.split())

    # Use module-level CATEGORY_MAPPINGS
    all_terms = {term for terms in CATEGORY_MAPPINGS.values() for term in terms}

    # Use difflib to find close matches in the style_name string
    close_matches = difflib.get_close_matches(style_name_lower, all_terms, n=5, cutoff=0.6)

    # Check if any close match belongs to a category
    for match in close_matches:
        for category, terms in CATEGORY_MAPPINGS.items():
            if match in terms:
                return category

    # Fallback to existing exact word matching
    for category, terms in CATEGORY_MAPPINGS.items():
        if any(term in words for term in terms):
            return category

    return "unknown"

def handle_style_generation(user_prefs):
    """
    Interactive handler to generate AI styles and ask user to save them.
    Now always generates detailed (name + description) output for consistency with CLI.
    Each style is generated in a random (non-repeating) canonical category for greater diversity.
    """
    # import random # Moved to top
    if not gemini_config.is_initialized():
        # Attempt to initialize if not already
        if not gemini_config.initialize_gemini_globally():
            error_msg = gemini_config.get_last_error() or "Unknown initialization error."
            print_warning(f"Gemini model is not initialized: {error_msg}. Please ensure GEMINI_API_KEY is set or provide key.")
            return
    # user_prefs is already passed to this function
    all_categories = list(CATEGORY_MAPPINGS.keys())
    prev_category = None
    while True:
        print_section("AI Style Generation")
        # Choose a random category, not the previous one
        possible_cats = [cat for cat in all_categories if cat != prev_category] or all_categories
        chosen_category = random.choice(possible_cats)
        prev_category = chosen_category
        print_info(f"Using category: {chosen_category}")
        print_info("Generating AI style...")
        style = generate_random_style(category=chosen_category, style_type="detailed")
        if not style or not isinstance(style, dict):
            print_warning("Failed to generate style. Please try again later.")
            return
        # import re # Moved to top
        name = style['name']
        desc = style['description']

        # Extract style name: from the output, prefer first line, strip markdown and whitespace
        # Handles case where output is "**Style Name**\nDescription" or just "Style Name"
        # import re # Moved to top
        first_line = name.splitlines()[0] if name else ""
        name_extracted = re.sub(r"^\*+|\*+$", "", first_line).strip()
        print_info(f"Generated AI Style (Category: {chosen_category}):\n  {name_extracted}\n  {desc.strip()}")

        save_choice = get_validated_input("Save this style to your preferences? (y/n/q)", ["y", "n", "q"])
        if save_choice == "y":
            user_prefs.add_style(name_extracted)
            print_success(f"Style set to: {name_extracted}")
        elif save_choice == "q":
            print_info("Exiting AI style generator.")
            break

        next_choice = get_validated_input("Generate next style? (y/n)", ["y", "n"])
        if next_choice != "y":
            print_info("Exiting AI style generator.")
            break

def export_style_to_file(style: Dict[str, str], filename: str) -> None:
    """
    Export the generated style to a file in JSON or text format based on filename extension.

    Args:
        style: Dictionary with 'name' and 'description' keys.
        filename: Path to the output file.

    Raises:
        IOError: If file cannot be written.
    """
    # import json # Moved to top
    # import os # Moved to top

    try:
        ext = os.path.splitext(filename)[1].lower()
        print(f"Exporting style to {filename}...")
        if ext == '.json':
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(style, f, indent=2, ensure_ascii=False)
        else:
            # Default to text format
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Name: {style.get('name', '')}\n")
                f.write(f"Description: {style.get('description', '')}\n")
        print(f"Style exported successfully to {filename}")
    except IOError as e:
        print(f"Failed to export style to {filename}: {e}")

def main():
    """
    Main entry point for CLI usage of the AI style generator.
    Usage:
      --category CATEGORY     Generate a style in a specific canonical category.
      --detailed              Generate detailed style output (name + description).
      --save                  Automatically save the generated style to preferences.
      --export FILENAME       Export the generated style to a file (JSON or text).
    """
    # import argparse # Moved to top
    # NOTE: This module assumes wallpaper_settings.py is part of the wall_gen package.
    # from wall_gen.wallpaper_settings import initialize_settings, get_preferences # Moved to top

    user_prefs = initialize_settings()
    parser = argparse.ArgumentParser(description='Generate an AI art style description')
    parser.add_argument('--key', help='Gemini API key (optional if set via environment variable)')
    parser.add_argument('--category', help='Canonical category for targeted style generation (e.g., oil_painting, geometric)')
    parser.add_argument('--detailed', action='store_true', help='Produce detailed name/description output')
    parser.add_argument('--save', action='store_true', help='Automatically save the generated style to preferences')
    parser.add_argument('--export', metavar='FILENAME', help='Export the generated style to a file (JSON or text)')
    args = parser.parse_args()

    if args.key:
        initialize_gemini(args.key)
    user_prefs = get_preferences()

    try:
        style_type = "detailed" if args.detailed else "simple"
        style = generate_random_style(category=args.category, style_type=style_type)

        if style and isinstance(style, dict) and "name" in style:
            generated_name = style['name']
            generated_desc = style.get('description', "")

            name_to_process = generated_name
            desc_to_print = generated_desc
            style_name_to_save = generated_name # Default to generated_name

            if args.detailed:
                # Optional: If style['name'] is very generic and style['description'] contains a bolded name (old fallback)
                # This part can be simplified or removed if JSON parsing is reliable
                if not name_to_process or name_to_process.lower() == "style name": # Example of a poor name
                    m_desc_name = re.search(r"\*\*(.+?)\*\*", generated_desc)
                    if m_desc_name:
                        name_from_desc = m_desc_name.group(1).strip()
                        if name_from_desc: # If a valid name is found in description
                            name_to_process = name_from_desc
                            # Try to get description following this bolded name
                            desc_match = re.search(r"\*\*" + re.escape(name_from_desc) + r"\*\*\s*\n([^\*].*)", generated_desc, re.DOTALL)
                            if desc_match:
                                desc_to_print = desc_match.group(1).strip()
                            # else desc_to_print remains generated_desc
                
                print(f"Generated style name: {name_to_process}\nDescription: {desc_to_print}")
                canonical = canonicalize_style_name(name_to_process)
                print(f"Canonical category (system): {canonical}")
                style_name_to_save = name_to_process
            else: # Simple style
                # For simple style, name_to_process is already generated_name, desc_to_print is ""
                print(f"Generated style: {name_to_process}")
                canonical = canonicalize_style_name(name_to_process)
                print(f"Canonical category (system): {canonical}")
                # style_name_to_save is already name_to_process (generated_name)
                desc_to_print = "" # Ensure description is empty for simple style export

            if args.save:
                user_prefs.add_style(style_name_to_save) # Always pass the string name
                print(f"Style saved to preferences: {style_name_to_save}")
            
            if args.export:
                # export_style_to_file expects a dict. Reconstruct it.
                export_dict = {"name": style_name_to_save, "description": desc_to_print}
                export_style_to_file(export_dict, args.export)
        
        elif style: # Handle cases where style might not be the expected dict (e.g. if generate_random_style changes unexpectedly)
             logger.error(f"Generated style has unexpected structure: {style}")
             print(f"Failed to process generated style due to unexpected structure.", file=sys.stderr)
             sys.exit(1)
        else:
            # This case is hit if generate_random_style returns None
            print("Failed to generate style.", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
