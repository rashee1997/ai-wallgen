import os
import google.generativeai as genai
from wallpaper_settings import get_preferences
import sys
from ui_utils import print_warning, print_section, print_info, get_validated_input, print_success
import logging
from typing import Optional, Dict, Any
import json
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration constants
DEFAULT_MODEL = "gemini-2.0-flash"
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# Global state
class GeminiState:
    def __init__(self):
        self.initialized = False
        self.api_key = None
        self.model = None
        self.last_error = None
        self.retry_count = 0

gemini_state = GeminiState()

# Load configuration from environment
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_state.api_key = GEMINI_API_KEY
        gemini_state.initialized = True
        logger.info("Successfully initialized Gemini with API key")
    except Exception as e:
        logger.error(f"Failed to initialize Gemini: {e}")
        gemini_state.last_error = str(e)
else:
    logger.warning("GEMINI_API_KEY environment variable not set. AI style generation will not work.")

def initialize_gemini(api_key: str) -> bool:
    """
    Initialize the Gemini model with the provided API key.
    Returns True if initialization was successful, False otherwise.
    """
    try:
        genai.configure(api_key=api_key)
        gemini_state.api_key = api_key
        gemini_state.initialized = True
        gemini_state.retry_count = 0
        logger.info("Successfully initialized Gemini with new API key")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize Gemini: {e}")
        gemini_state.last_error = str(e)
        return False

def generate_style_prompt(category: str = None, style_type: str = "simple") -> str:
    """
    Generate a prompt for Gemini to create a random artistic style or descriptor.
    If category is provided, constrain to that art style family.
    If style_type is "simple", generate a style modifier (e.g. "vibrant cyberpunk neon").
    If style_type is "detailed", ask for a richer style title plus 1-2 characteristic notes.
    
    Args:
        category: Optional category to constrain the style generation
        style_type: Type of style to generate ('simple' or 'detailed')
    
    Returns:
        str: The generated prompt
    """
    base = "You are an expert AI art style generator. "
    if category:
        base += (
            f"Limit the style to the '{category}' category of art/design. "
            f"Focus on the distinctive characteristics, techniques, or traditions of this category."
        )
    
    if style_type == "simple":
        core = (
            "Generate a single cohesive artistic style description that represents ONE clear visual concept. "
            "The style must be simple and focused, avoiding multiple descriptive elements or comma-separated concepts. "
            "Example good response: 'vibrant cyberpunk neon' "
            "Example bad response: 'dark gothic, medieval architecture, with misty atmosphere' "
            "Focus on ONE primary visual style without combining multiple themes or elements. "
            "Keep it concise and avoid any additional explanations or variations."
        )
    else:
        core = (
            "Suggest a unique, evocative style name (2-4 words) as would be used for an AI art preset. "
            "Below the name, in one sentence, describe 1-2 visual or technical hallmarks of this style, inspired by its category."
            "Output structure: Name on first line; description on second line."
        )
    
    return base + core

def generate_random_style(category: str = None, style_type: str = "simple") -> Optional[Dict[str, str]]:
    """
    Use Gemini to generate a random style, optionally for a specific canonical category.
    Implements retry logic and improved error handling.
    
    Args:
        category: Optional category to constrain the style generation
        style_type: Type of style to generate ('simple' or 'detailed')
    
    Returns:
        Optional[Dict[str, str]]: The generated style as a dictionary with 'name' and 'description' keys,
        or None if generation fails
    """
    if not gemini_state.initialized:
        raise RuntimeError("Gemini model is not initialized. Please initialize with your API key first.")
    
    prompt = generate_style_prompt(category, style_type)
    
    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"Generating style (attempt {attempt + 1}/{MAX_RETRIES})")
            model = genai.GenerativeModel(DEFAULT_MODEL)
            response = model.generate_content(prompt)
            
            if not response:
                logger.warning("No response received from Gemini")
                continue
                
            style_text = None
            if hasattr(response, 'text') and response.text:
                style_text = response.text.strip()
            elif hasattr(response, 'candidates') and response.candidates:
                style_text = response.candidates[0].content.parts[0].text.strip()
            
            if not style_text:
                logger.warning("No style text found in response")
                continue
                
            style_text = style_text.strip(' "\'\n\r')
            
            if style_type == "simple":
                return {"name": style_text, "description": ""}
            elif "\n" in style_text:
                name, desc = style_text.split("\n", 1)
                return {"name": name.strip(), "description": desc.strip()}
            
        except Exception as e:
            gemini_state.retry_count += 1
            logger.error(f"Error generating style (attempt {attempt + 1}): {e}")
            if attempt < MAX_RETRIES - 1:
                logger.info(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                logger.error(f"Failed to generate style after {MAX_RETRIES} attempts")
                return None
    
    return None

def generate_random_style_by_category(category: str):
    """
    Generate a random style strictly within a given canonical category (for use in templates/UI).
    Returns the style string.
    """
    return generate_random_style(category=category, style_type="simple")
def canonicalize_style_name(style_name: str) -> str:
    """
    Map a generated/entered style string to a canonical category for validation or downstream use.
    Uses a more efficient and maintainable approach with dictionaries and sets.
    
    Args:
        style_name: The style name to categorize
    
    Returns:
        str: The canonical category name
    """
    # Convert to lowercase and split into words for better matching
    words = set(style_name.lower().split())
    
    # Define category mappings using sets for efficient lookup
    category_mappings = {
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
        "photographic": {"photo", "realistic", "photograph", "film", "kodak", "dslr", "cinematic", "fujifilm", "shot on", "hyperreal"},
        "game_style": {"game", "engine", "unreal", "unity", "fps", "rpg", "rendered", "in-engine"},
        "digital_art": {"digital", "vector", "glitch", "vaporwave", "retrowave", "3d", "render"},
        "abstract_conceptual": {"abstract", "conceptual", "cubist", "fauvist", "expressionist", "non-representational", "dreamscape", "surreal"},
        "material_sculptural": {"sculpture", "sculpted", "statue", "bust", "relief", "bronze", "marble", "clay"},
        "fantasy": {"fantasy", "mythical", "magical", "wizard", "fairy", "dragon", "unicorn", "castle"},
        "sci_fi": {"sci-fi", "science fiction", "cyberpunk", "futuristic", "spaceship", "space opera"}
    }
    
    # Check each category for matching terms
    for category, terms in category_mappings.items():
        if any(term in words for term in terms):
            return category
    
    return "unknown"

def handle_style_generation(user_prefs):
    """
    Interactive handler to generate AI styles and ask user to save them.
    Now always generates detailed (name + description) output for consistency with CLI.
    Each style is generated in a random (non-repeating) canonical category for greater diversity.
    """
    import random
    if not gemini_state.initialized:
        print_warning("Gemini model is not initialized. Please ensure GEMINI_API_KEY environment variable is set.")
        return
    all_categories = [
        "oil_painting", "watercolor", "pastel", "charcoal", "pencil_sketch", "ink_drawing",
        "minimalist", "geometric", "illustration_pixel", "illustration_anime_manga", "illustration_comic",
        "photographic", "game_style", "digital_art", "abstract_conceptual", "material_sculptural",
        "fantasy", "sci_fi"
    ]
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
        import re
        name = style['name']
        desc = style['description']

        # Extract style name: from the output, prefer first line, strip markdown and whitespace
        # Handles case where output is "**Style Name**\nDescription" or just "Style Name"
        import re
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

def main():
    """
    Main entry point for CLI usage of the AI style generator.
    Usage:
      --category CATEGORY     Generate a style in a specific canonical category.
      --detailed              Generate detailed style output (name + description).
      --save                  Automatically save the generated style to preferences.
    """
    import argparse
    from wallpaper_settings import initialize_settings, get_preferences

    user_prefs = initialize_settings()
    parser = argparse.ArgumentParser(description='Generate an AI art style description')
    parser.add_argument('--key', help='Gemini API key (optional if set via environment variable)')
    parser.add_argument('--category', help='Canonical category for targeted style generation (e.g., oil_painting, geometric)')
    parser.add_argument('--detailed', action='store_true', help='Produce detailed name/description output')
    parser.add_argument('--save', action='store_true', help='Automatically save the generated style to preferences')
    args = parser.parse_args()

    if args.key:
        initialize_gemini(args.key)
    user_prefs = get_preferences()

    try:
        style_type = "detailed" if args.detailed else "simple"
        style = generate_random_style(category=args.category, style_type=style_type)
        if style:
            if args.detailed and isinstance(style, dict):
                # Enhanced extraction for multi-option responses
                import re
                name = style['name']
                desc = style['description']
                # If typical "Here are a few" multi-style output, extract first markdown/asterisk or bold style name
                # Matches e.g.: **Baroque Luminosity**\nDescription...
                name_for_canon = name
                desc_for_canon = desc
                m = re.search(r"\*\*(.+?)\*\*", desc)
                if m:
                    name_for_canon = m.group(1)
                    # Grab the following description line if present
                    desc_match = re.search(r"\*\*.+?\*\*\n([^\*]+)", desc)
                    if desc_match:
                        desc_for_canon = desc_match.group(1).strip()
                print(f"Generated style name: {name_for_canon}\nDescription: {desc_for_canon}")
                canonical = canonicalize_style_name(name_for_canon)
                print(f"Canonical category (system): {canonical}")
                style_to_save = name_for_canon
            else:
                print(f"Generated style: {style}")
                canonical = canonicalize_style_name(style)
                print(f"Canonical category (system): {canonical}")
                style_to_save = style
            if args.save:
                user_prefs.add_style(style_to_save)
                print(f"Style saved to preferences: {style_to_save}")
        else:
            print("Failed to generate style", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
