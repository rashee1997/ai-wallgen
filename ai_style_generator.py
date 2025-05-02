import os
import google.generativeai as genai
from wallpaper_settings import get_preferences
import sys
from ui_utils import print_warning, print_section, print_info, get_validated_input, print_success

# Global variable to track if Gemini is initialized
gemini_initialized = False

# Attempt to get GEMINI_API_KEY from environment and configure Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_initialized = True
else:
    print("Warning: GEMINI_API_KEY environment variable not set. AI style generation will not work.")

def initialize_gemini(api_key: str):
    """
    Initialize the Gemini model with the provided API key.
    """
    global gemini_initialized
    genai.configure(api_key=api_key)
    gemini_initialized = True

def generate_style_prompt(category: str = None, style_type: str = "simple") -> str:
    """
    Generate a prompt for Gemini to create a random artistic style or descriptor.
    If category is provided, constrain to that art style family.
    If style_type is "simple", generate a style modifier (e.g. "vibrant cyberpunk neon").
    If style_type is "detailed", ask for a richer style title plus 1-2 characteristic notes.
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

def generate_random_style(category: str = None, style_type: str = "simple"):
    """
    Use Gemini to generate a random style, optionally for a specific canonical category.
    Returns the generated style string or a detailed description.
    """
    if not gemini_initialized:
        raise RuntimeError("Gemini model is not initialized. Please initialize with your API key first.")
    prompt = generate_style_prompt(category, style_type)
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        style_text = None
        if response and hasattr(response, 'text') and response.text:
            style_text = response.text.strip()
        elif response and hasattr(response, 'candidates') and response.candidates:
            style_text = response.candidates[0].content.parts[0].text.strip()
        if style_text:
            style_text = style_text.strip(' "\'\n\r')
            if style_type != "simple" and "\n" in style_text:
                name, desc = style_text.split("\n", 1)
                return {"name": name.strip(), "description": desc.strip()}
            return style_text
        print("No style text returned from Gemini response.")
        return None
    except Exception as e:
        print(f"Error generating style with Gemini: {e}")
        return None

def generate_random_style_by_category(category: str):
    """
    Generate a random style strictly within a given canonical category (for use in templates/UI).
    Returns the style string.
    """
    return generate_random_style(category=category, style_type="simple")
def canonicalize_style_name(style_name: str):
    """
    Map a generated/entered style string to a canonical category for validation or downstream use.
    Enhanced: Map art movements/eras/techniques to canonical media categories!
    """
    name = style_name.lower()
    # Oil painting detection (includes major oil eras/movements)
    oil_terms = ["oil", "impasto", "baroque", "impression", "post-impression", "romanticism",
                 "expressionism", "fauvism", "pointillism", "divisionism", "van gogh", "renoir", "manet"]
    if any(term in name for term in oil_terms):
        return "oil_painting"
    watercolor_terms = ["watercolor", "watercolour", "aquarelle"]
    if any(term in name for term in watercolor_terms):
        return "watercolor"
    pastel_terms = ["pastel", "degas"]
    if any(term in name for term in pastel_terms):
        return "pastel"
    charcoal_terms = ["charcoal", "carboncillo"]
    if any(term in name for term in charcoal_terms):
        return "charcoal"
    pencil_terms = ["pencil", "graphite", "colored pencil"]
    if any(term in name for term in pencil_terms):
        return "pencil_sketch"
    ink_terms = ["ink", "pen & ink", "line", "pen and ink"]
    if any(term in name for term in ink_terms):
        return "ink_drawing"
    minimal_terms = ["minimal", "minimalism", "reductive"]
    if any(term in name for term in minimal_terms):
        return "minimalist"
    geometric_terms = ["geometric", "geometry", "polygon", "low poly", "constructivism"]
    if any(term in name for term in geometric_terms):
        return "geometric"
    minimalist_geometric_terms = ["minimalist geometric", "minimal geometric", "geometric minimalism"]
    if any(term in name for term in minimalist_geometric_terms):
        return "minimalist_geometric"
    psychedelic_terms = ["psychedelic", "trippy", "hallucinogenic", "psychedelia"]
    if any(term in name for term in psychedelic_terms):
        return "psychedelic"
    surrealism_terms = ["surrealism", "surreal", "dreamlike", "fantastical"]
    if any(term in name for term in surrealism_terms):
        return "surrealism"
    fantasy_landscape_terms = ["fantasy landscape", "fantastical landscape", "enchanted landscape"]
    if any(term in name for term in fantasy_landscape_terms):
        return "fantasy_landscape"
    cyberpunk_cityscape_terms = ["cyberpunk cityscape", "neon city", "futuristic cityscape"]
    if any(term in name for term in cyberpunk_cityscape_terms):
        return "cyberpunk_cityscape"
    pixel_terms = ["pixel", "8-bit", "16-bit", "pixelated"]
    if any(term in name for term in pixel_terms):
        return "illustration_pixel"
    anime_terms = ["anime", "manga", "shojo", "shonen", "seinen"]
    if any(term in name for term in anime_terms):
        return "illustration_anime_manga"
    comic_terms = ["comic", "graphic novel"]
    if any(term in name for term in comic_terms):
        return "illustration_comic"
    photo_terms = ["photo", "realistic", "photograph", "film", "kodak", "dslr", "cinematic", "fujifilm", "shot on", "hyperreal"]
    if any(term in name for term in photo_terms):
        return "photographic"
    game_terms = ["game", "engine", "unreal", "unity", "fps", "rpg", "rendered", "in-engine"]
    if any(term in name for term in game_terms):
        return "game_style"
    digital_terms = ["digital", "vector", "glitch", "vaporwave", "retrowave", "3d", "render"]
    if any(term in name for term in digital_terms):
        return "digital_art"
    abstract_terms = ["abstract", "conceptual", "cubist", "fauvist", "expressionist", "non-representational", "dreamscape", "surreal"]
    if any(term in name for term in abstract_terms):
        return "abstract_conceptual"
    sculptural_terms = ["sculpture", "sculpted", "statue", "bust", "relief", "bronze", "marble", "clay"]
    if any(term in name for term in sculptural_terms):
        return "material_sculptural"
    fantasy_terms = ["fantasy", "mythical", "magical", "wizard", "fairy", "dragon", "unicorn", "castle"]
    if any(term in name for term in fantasy_terms):
        return "fantasy"
    sci_fi_terms = ["sci-fi", "science fiction", "cyberpunk", "futuristic", "spaceship", "space opera"]
    if any(term in name for term in sci_fi_terms):
        return "sci_fi"
    return "unknown"

def handle_style_generation(user_prefs):
    """
    Interactive handler to generate AI styles and ask user to save them.
    Now always generates detailed (name + description) output for consistency with CLI.
    Each style is generated in a random (non-repeating) canonical category for greater diversity.
    """
    import random
    if not gemini_initialized:
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
        name_for_show = name
        desc_for_show = desc
        m = re.search(r"\*\*(.+?)\*\*", desc)
        if m:
            name_for_show = m.group(1)
            desc_match = re.search(r"\*\*.+?\*\*\n([^\*]+)", desc)
            if desc_match:
                desc_for_show = desc_match.group(1).strip()
            else:
                desc_for_show = desc
        print_info(f"Generated AI Style (Category: {chosen_category}):\n  {name_for_show}\n  {desc_for_show}")

        save_choice = get_validated_input("Save this style to your preferences? (y/n/q)", ["y", "n", "q"])
        if save_choice == "y":
            user_prefs.add_style(name_for_show)
            print_success(f"Style set to: {name_for_show}")
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
