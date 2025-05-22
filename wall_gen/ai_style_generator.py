import argparse
import difflib
import json
import logging
import os
import random
import re
import sys
import time
from typing import Dict, Optional, Any

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
STYLE_TYPE_SIMPLE = "simple"
STYLE_TYPE_DETAILED = "detailed"
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
    Initializes the Gemini model globally using a provided API key override.

    This function acts as a wrapper for `gemini_config.initialize_gemini_globally`,
    primarily used when an API key is passed directly via CLI arguments.

    Args:
        api_key (str): The Gemini API key to use for initialization.

    Returns:
        bool: True if initialization was successful, False otherwise.
    """
    logger.info(f"Attempting to initialize Gemini globally with provided API key.")
    success = gemini_config.initialize_gemini_globally(api_key_override=api_key)
    if success:
        logger.info("Gemini globally initialized successfully with new API key.")
    else:
        logger.error(f"Failed to initialize Gemini globally: {gemini_config.get_last_error()}")
    return success

def _extract_style_text_from_response(response: types.GenerateContentResponse) -> Optional[str]:
    """
    Extracts the style text from a Gemini API response object.

    Handles different response structures (e.g., direct 'text' attribute or nested 'candidates').

    Args:
        response: The Gemini API response object.

    Returns:
        Optional[str]: The extracted style text, or None if not found.
    """
    if hasattr(response, 'text') and response.text:
        return response.text.strip()
    elif hasattr(response, 'candidates') and response.candidates and \
         hasattr(response.candidates[0], 'content') and hasattr(response.candidates[0].content, 'parts') and \
         response.candidates[0].content.parts and hasattr(response.candidates[0].content.parts[0], 'text'):
        return response.candidates[0].content.parts[0].text.strip()
    else:
        logger.warning("No valid response text or candidates structure from Gemini.")
        # logger.debug(f"Full Gemini response: {response}") # Uncomment for detailed debugging
        return None

def generate_style_prompt(category: Optional[str] = None, style_type: str = STYLE_TYPE_SIMPLE) -> str:
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

    if style_type == STYLE_TYPE_SIMPLE:
        core = (
            "Generate one clear, focused artistic style description representing a single visual concept. "
            "No multiple descriptive elements or comma-separated themes. "
            "Good: 'vibrant cyberpunk neon'. "
            "Bad: 'dark gothic, medieval architecture, with misty atmosphere'. "
            "Focus on one main style. Output only the style phrase."
        )
    elif style_type == STYLE_TYPE_DETAILED:
        core = (
            "Suggest a style name (2-4 words) suitable for an AI art preset, and a 1-2 sentence description of its visual or technical hallmarks. "
            "Format the output as a JSON object with two keys: \"name\" and \"description\". "
            "Example: {\"name\": \"Vibrant Dreamscape\", \"description\": \"Characterized by vivid, surreal colors and flowing, organic shapes. Often evokes a sense of wonder and ethereal beauty.\"}"
            "Output only the JSON object."
        )
    else:
        logger.warning(f"Unknown style_type '{style_type}' provided to generate_style_prompt. Defaulting to simple.")
        core = (
            "Generate one clear, focused artistic style description representing a single visual concept. "
            "No multiple descriptive elements or comma-separated themes. "
            "Good: 'vibrant cyberpunk neon'. "
            "Bad: 'dark gothic, medieval architecture, with misty atmosphere'. "
            "Focus on one main style. Output only the style phrase."
        )
    return base + core

def generate_random_style(category: Optional[str] = None, style_type: str = STYLE_TYPE_SIMPLE) -> Optional[Dict[str, str]]:
    """
    Generates a random AI art style using the Gemini model.

    This function constructs a prompt based on the desired category and style type,
    then calls the Gemini API to generate a style. It includes retry logic with
    exponential backoff for robustness and handles different Gemini response formats.

    Args:
        category (Optional[str]): An optional canonical art style category to constrain
                                  the generation (e.g., "oil_painting", "minimalist").
        style_type (str): The type of style to generate.
                          Use `STYLE_TYPE_SIMPLE` for a single style phrase,
                          or `STYLE_TYPE_DETAILED` for a name and description.

    Returns:
        Optional[Dict[str, str]]: A dictionary containing the generated style.
                                  For `STYLE_TYPE_SIMPLE`, it will have a "name" key
                                  and an empty "description" key.
                                  For `STYLE_TYPE_DETAILED`, it will have "name" and
                                  "description" keys.
                                  Returns `None` if style generation fails after retries.
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
            client = gemini_config.get_gemini_client()
            if client is None:
                logger.error("Gemini client is not initialized, cannot generate style.")
                raise RuntimeError("Gemini client initialization failed. Check API key.")
            
            # Use get_model() to get the model object, then call generate_content()
            model_instance = client.get_model(selected_model_name)
            response = model_instance.generate_content(
                prompt
            )

            style_text = _extract_style_text_from_response(response)
            if style_text is None:
                continue # Try next attempt or fail

            style_text = style_text.strip(' "\'\n\r') # Clean the raw text

            if style_type == STYLE_TYPE_DETAILED:
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

            elif style_type == STYLE_TYPE_SIMPLE:
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

        except (genai.types.BlockedPromptException, genai.types.BlockedGenerationException) as e:
            logger.error(f"Gemini API blocked content (attempt {attempt + 1}): {e}", exc_info=True)
            # For blocked content, retrying might not help unless prompt changes.
            # Consider if a different error handling strategy is needed here (e.g., prompt modification).
            # For now, we'll log and fail after retries.
            if attempt < MAX_RETRIES - 1:
                delay = RETRY_DELAY * (2 ** attempt)
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logger.error(f"Failed to generate style after {MAX_RETRIES} attempts due to blocked content.")
                return None # Explicitly return None for blocked content

        except Exception as e:
            logger.error(f"Unexpected error generating style (attempt {attempt + 1}): {e}", exc_info=True)
            if attempt < MAX_RETRIES - 1:
                delay = RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logger.error(f"Failed to generate style after {MAX_RETRIES} attempts due to unexpected error.")

    return None

def generate_random_style_by_category(category: str) -> Optional[Dict[str, str]]:
    """
    Generates a simple random style strictly within a given canonical category.

    This function is a wrapper around `generate_random_style` specifically for
    generating simple style phrases for use in templates or UI elements.

    Args:
        category (str): The canonical category to constrain the style generation.

    Returns:
        Optional[Dict[str, str]]: A dictionary containing the generated style with
                                  a "name" key and an empty "description" key,
                                  or `None` if generation fails.
    """
    return generate_random_style(category=category, style_type=STYLE_TYPE_SIMPLE)

def canonicalize_style_name(style_name: str) -> str:
    """
    Maps a generated or entered style string to a canonical category name.

    This function uses fuzzy matching (difflib) and exact word matching to associate
    an arbitrary style string with one of the predefined art categories in
    `CATEGORY_MAPPINGS`.

    Args:
        style_name (str): The human or AI-generated style string to canonicalize.

    Returns:
        str: The canonical category name (e.g., "oil_painting", "minimalist"),
             or "unknown" if no suitable match is found.
    """

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

def handle_style_generation(user_prefs: Any) -> None:
    """
    Provides an interactive command-line interface for generating and saving AI art styles.

    This function guides the user through generating detailed AI styles (name + description)
    from random canonical categories, allowing them to save preferred styles to their
    user preferences. It ensures Gemini is initialized before proceeding.

    Args:
        user_prefs (Any): An object representing user preferences, expected to have
                          an `add_style` method.
    """
    if not gemini_config.is_initialized():
        if not gemini_config.initialize_gemini_globally():
            error_msg = gemini_config.get_last_error() or "Unknown initialization error."
            print_warning(f"Gemini model is not initialized: {error_msg}. Please ensure GEMINI_API_KEY is set or provide key.")
            return

    all_categories = list(CATEGORY_MAPPINGS.keys())
    prev_category: Optional[str] = None

    while True:
        print_section("AI Style Generation")
        possible_cats = [cat for cat in all_categories if cat != prev_category] or all_categories
        chosen_category = random.choice(possible_cats)
        prev_category = chosen_category

        print_info(f"Using category: {chosen_category}")
        print_info("Generating AI style...")

        style = generate_random_style(category=chosen_category, style_type=STYLE_TYPE_DETAILED)

        if not style or not isinstance(style, dict):
            print_warning("Failed to generate style. Please try again later.")
            return

        name: str = style.get('name', '')
        desc: str = style.get('description', '')

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
    Exports a generated AI style (name and description) to a specified file.

    The export format (JSON or plain text) is determined by the file extension.

    Args:
        style (Dict[str, str]): A dictionary containing the style's "name" and "description".
        filename (str): The path to the output file. Supported extensions are '.json' for JSON
                        output, and any other extension for plain text.

    Raises:
        IOError: If the file cannot be written to (e.g., due to permissions or invalid path).
    """

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

def main() -> None:
    """
    Main entry point for the AI style generator CLI.

    This function parses command-line arguments, initializes Gemini, generates
    an AI style based on user input, and optionally saves or exports the style.

    Command-line arguments:
        --key KEY: Gemini API key (optional if set via environment variable).
        --category CATEGORY: Canonical category for targeted style generation
                             (e.g., 'oil_painting', 'geometric').
        --detailed: Produce detailed name/description output instead of a simple phrase.
        --save: Automatically save the generated style to user preferences.
        --export FILENAME: Export the generated style to a file (JSON or text format
                           based on file extension).
    """
    user_prefs = initialize_settings()
    parser = argparse.ArgumentParser(
        description='Generate an AI art style description',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--key', help='Gemini API key (optional if set via environment variable)')
    parser.add_argument('--category', help='Canonical category for targeted style generation (e.g., oil_painting, geometric)')
    parser.add_argument('--detailed', action='store_true', help='Produce detailed name/description output')
    parser.add_argument('--save', action='store_true', help='Automatically save the generated style to preferences')
    parser.add_argument('--export', metavar='FILENAME', help='Export the generated style to a file (JSON or text)')
    args = parser.parse_args()

    if args.key:
        if not initialize_gemini(args.key):
            print("Failed to initialize Gemini with provided API key.", file=sys.stderr)
            sys.exit(2)
    user_prefs = get_preferences()

    try:
        style_type = STYLE_TYPE_DETAILED if args.detailed else STYLE_TYPE_SIMPLE
        style = generate_random_style(category=args.category, style_type=style_type)

        if not (style and isinstance(style, dict) and "name" in style):
            logger.error(f"Failed to generate style or style has unexpected structure: {style}")
            print("Failed to generate style or style has unexpected structure.", file=sys.stderr)
            sys.exit(1)

        generated_name: str = style['name']
        generated_desc: str = style.get('description', "")
        name_to_process: str = generated_name
        desc_to_print: str = generated_desc
        style_name_to_save: str = generated_name

        if args.detailed:
            # If style['name'] is generic, try to extract a better name from description
            if not name_to_process or name_to_process.lower() == "style name":
                m_desc_name = re.search(r"\*\*(.+?)\*\*", generated_desc)
                if m_desc_name:
                    name_from_desc = m_desc_name.group(1).strip()
                    if name_from_desc:
                        name_to_process = name_from_desc
                        desc_match = re.search(r"\*\*" + re.escape(name_from_desc) + r"\*\*\s*\n([^\*].*)", generated_desc, re.DOTALL)
                        if desc_match:
                            desc_to_print = desc_match.group(1).strip()
            print(f"Generated style name: {name_to_process}\nDescription: {desc_to_print}")
        else:
            print(f"Generated style: {name_to_process}")
            desc_to_print = ""

        canonical = canonicalize_style_name(name_to_process)
        print(f"Canonical category (system): {canonical}")
        style_name_to_save = name_to_process

        if args.save:
            user_prefs.add_style(style_name_to_save)
            print(f"Style saved to preferences: {style_name_to_save}")

        if args.export:
            export_dict = {"name": style_name_to_save, "description": desc_to_print}
            export_style_to_file(export_dict, args.export)

        sys.exit(0)

    except Exception as e:
        logger.error(f"Error in main(): {e}", exc_info=True)
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(3)

if __name__ == '__main__':
    main()
