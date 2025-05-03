
#!/usr/bin/env python3
"""AI Preset Generator - Generate random wallpaper preferences using Gemini AI

This script uses Google's Gemini AI to create intelligent, coherent random presets
for the wallpaper generator application based on detected style categories.
Digital art and game styles are kept completely separate.
"""

import os
import json
import logging
import random
import hashlib
import sys
import re
import time
import argparse
from typing import Dict, Any, List, Optional, Union

# --- Gemini API Import ---
try:
    import google.generativeai as genai
    import google.generativeai.types as genai_types
except ImportError:
    print("Error: google-generativeai package not installed")
    print("Please install it with: pip install google-generativeai")
    sys.exit(1)

# --- Local Imports & Fallbacks ---
# Define fallbacks first
def print_section(x): print(f"\n--- {x} ---")
def print_option(k, v): print(f"  {k}. {v}")
def print_info(x): print(x)
def print_error(x): print(f"ERROR: {x}")
def print_success(x): print(f"SUCCESS: {x}")
def print_warning(x): print(f"WARNING: {x}")
def get_validated_input(p, v):
    while True:
        val = input(f"{p} {v}: ").strip().lower()
        is_valid = False
        if isinstance(v, list): is_valid = val in [str(choice).lower() for choice in v]
        if is_valid: return val
        else: print(f"Invalid input. Please enter one of {v}")

class UserPreferences: pass # Minimal placeholder
def initialize_settings(): return UserPreferences()
def get_preferences(): return initialize_settings()

try:
    from wallpaper_settings import UserPreferences, get_preferences, initialize_settings
    SETTINGS_AVAILABLE = True
except ImportError:
    SETTINGS_AVAILABLE = False
    logging.warning("wallpaper_settings.py not found. Using placeholder UserPreferences.")

try:
    from ui_utils import get_validated_input, print_section, print_option, print_info, print_error, print_success, print_warning
    UI_UTILS_AVAILABLE = True
except ImportError:
    UI_UTILS_AVAILABLE = False
    logging.warning("ui_utils not found. Using basic print/input for UI.")

try:
    from ai_style_generator import generate_random_style, initialize_gemini as initialize_style_gemini
    AI_STYLE_GEN_AVAILABLE = True
except ImportError:
    AI_STYLE_GEN_AVAILABLE = False
    logging.warning("Could not import ai_style_generator. AI style generation feature disabled.")
    generate_random_style = lambda: None
    initialize_style_gemini = lambda x: None

# Import utility functions
from file_utils import deep_update

# Import configuration
try:
    from config import STYLE_CATEGORIES
except ImportError:
    logging.warning("Could not import STYLE_CATEGORIES from config.py. Using empty dictionary.")
    STYLE_CATEGORIES = {}

# Import style templates
from style_templates import get_template_for_category

# --- Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[ logging.FileHandler("ai_preset_generator.log") ]
)
PRESETS_CACHE_FILE = "generated_presets_cache.json"
PRESETS_DIR = "presets"

# --- Helper Functions ---

def get_gemini_api_key() -> Optional[str]:
    """Retrieve the Gemini API key from environment variable."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key: logging.warning("GEMINI_API_KEY environment variable not set.")
    return api_key

def load_cached_presets() -> List[str]:
    """Load previously generated preset hashes from cache file."""
    if os.path.exists(PRESETS_CACHE_FILE):
        try:
            with open(PRESETS_CACHE_FILE, 'r') as f:
                content = json.load(f)
                return content if isinstance(content, list) else []
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error loading presets cache: {e}")
    return []

def save_preset_to_cache(preset_data: Dict[str, Any]) -> None:
    """Save a preset hash to the cache file to avoid regenerating it."""
    try:
        if "styles" in preset_data and not isinstance(preset_data["styles"], list):
             preset_data["styles"] = [preset_data["styles"]]
        preset_hash = hashlib.md5(json.dumps(preset_data, sort_keys=True).encode()).hexdigest()
        cached_presets = load_cached_presets()
        if preset_hash not in cached_presets:
            cached_presets.append(preset_hash)
            if len(cached_presets) > 50: cached_presets = cached_presets[-50:]
            try:
                with open(PRESETS_CACHE_FILE, 'w') as f: json.dump(cached_presets, f)
            except IOError as e: logging.error(f"Error writing to presets cache: {e}")
    except Exception as e: logging.error(f"Unexpected error in save_preset_to_cache: {e}")

def is_preset_unique(preset_data: Dict[str, Any]) -> bool:
    """Check if a preset is unique compared to previously generated ones."""
    try:
        if "styles" in preset_data and not isinstance(preset_data["styles"], list):
            preset_data["styles"] = [preset_data["styles"]]
        preset_hash = hashlib.md5(json.dumps(preset_data, sort_keys=True).encode()).hexdigest()
        cached_presets = load_cached_presets()
        return preset_hash not in cached_presets
    except Exception as e:
        logging.error(f"Error checking preset uniqueness: {e}")
        return True

def categorize_style(style_name: Union[str, Dict]) -> str:
    """
    Attempt to categorize a style name. Digital art and game styles are kept completely separate.
    
    Args:
        style_name: Either a string style name or a dictionary with 'name' key
    """
    if isinstance(style_name, dict):
        style_name = style_name.get('name', '')
    
    # Normalize style_name by replacing underscores with spaces to improve matching
    style_name = str(style_name).replace('_', ' ')
    style_lower = style_name.lower()
    
    # Define keywords for each distinct category
    categories_keywords = {
        # --- 3D Render/CGI Categories ---
        "3d_render": [
            "3d", "3d render", "3d modeling", "3d model", "3d illustration",
            "cgi", "c.g.i", "cg render", "clay render", "octane render", "arnold render",
            "blender", "maya", "cinema 4d", "unreal engine", "3ds max",
            "zbrush", "keyshot", "pixar style 3d", "toon 3d", "stylized 3d",
            "photoreal 3d", "3d portrait", "3d scene", "3d composition", "3d character", "3d environment"
        ],

        # --- Illustration/Cartoon Categories ---
        "illustration_pixar": ["pixar", "pixar style", "pixar animation"],
        "illustration_disney": ["disney", "disney style", "disney animation"],
        "illustration_tom_jerry": ["tom & jerry", "tom and jerry", "hanna-barbera"],
        "illustration_vintage_cartoon": ["vintage cartoon", "rubber hose", "1930s cartoon", "classic cartoon"],
        "illustration_anime_manga": ["anime", "manga", "shonen", "shojo", "seinen", "japanese animation"],
        "illustration_comic": ["comic", "comic book", "comic strip", "sequential art"],
        "illustration_pixel": ["pixel art", "8-bit", "16-bit", "pixelated", "retro game art"],
        "illustration_graphic": ["illustration", "cartoon", "cartoony", "graphic novel"],
        "illustration_childrens": ["children's book", "picture book", "kids illustration"],
        "illustration_fantasy": ["fantasy illustration", "mythical", "magical creatures"],
        "ink_punk": ["ink punk", "inkpunk", "hand-drawn sketchy", "unfinished look"],

        # --- Painting/Drawing Categories ---
        "oil_painting": ["oil painting", "oil paint", "impasto", "alla prima", "wet-on-wet"],
        "watercolor": ["watercolor", "watercolour", "wet-on-wet", "wet-on-dry"],
        "pastel": ["pastel", "pastel drawing", "pastel painting"],
        "charcoal": ["charcoal sketch", "charcoal drawing", "charcoal art"],
        "pencil_sketch": ["pencil", "pencil sketch", "graphite", "pencil drawing"],
        "ink_drawing": ["ink drawing", "ink sketch", "pen and ink", "line drawing", "line art", "ink wash"],
        "acrylic_painting": ["acrylic", "acrylic paint", "acrylic painting"],
        "mixed_media": ["mixed media", "collage", "assemblage", "combined media"],
        "digital_painting": ["digital painting", "digital illustration", "digital art"],

        # --- Traditional Art Categories ---
        "traditional_painting_drawing": [
            "impressionist", "renaissance", "baroque", "rococo",
            "acrylic", "tempera", "art nouveau", "art deco",
            "cubism", "constructivism", "futurism", "pointillism", "divisionism",
            "ukiyo-e", "woodcut", "linocut", "etching"
        ],
        "realism": ["realism", "realistic", "photoreal", "hyperrealism", "photorealistic"],
        "abstract": ["abstract", "abstract art", "non-representational"],
        "expressionism": ["expressionism", "expressionist", "emotional art"],
        "surrealism": ["surrealism", "surreal", "dreamlike", "fantastical"],
        "cubism": ["cubism", "cubist", "geometric abstraction"],
        "fauvism": ["fauvism", "fauvist", "wild beasts"],
        "art_nouveau": ["art nouveau", "new art", "modern style"],
        "art_deco": ["art deco", "decop", "modernist"],
        "art_deco_revival": ["art deco revival", "art deco revival", "art deco style", "art deco architecture"],

        # --- Minimalist/Geometric Categories ---
        "minimalist": ["minimalism", "minimalist", "minimal", "minimal art"],
        "geometric": ["geometric", "geometry", "geometric abstract", "low poly"],
        "minimalist_geometric": ["minimalist geometric", "minimal geometric", "geometric minimalism"],
        "constructivism": ["constructivism", "constructivist", "industrial art"],
        "low_poly": ["low poly", "low polygon", "polygonal art"],
        "isometric": ["isometric", "isometric view", "axonometric"],

        # --- Digital/Modern Categories ---
        "digital_art": [
            "digital art", "digital painting", "3d render", "3d art", 
            "vector art", "glitch art", "vaporwave", "retrowave", "rendered",
            "digital illustration", "digital media"
        ],
        "psychedelic": ["psychedelic", "trippy", "hallucinogenic", "psychedelia", "acid art"],
        "cyberpunk": ["cyberpunk", "cyberpunk art", "futuristic", "neon city"],
        "retrowave": ["retrowave", "vaporwave", "80s revival", "synthwave"],
        "glitch_art": ["glitch art", "glitch effect", "digital glitch", "error art"],
        "vector_art": ["vector art", "vector illustration", "vector graphics"],
        "3d_render": ["3d render", "3d art", "3d modeling", "3d illustration"],

        # --- Game Art Categories ---
        "game_style": [
            "game style", "game art", "game engine", "unity", "unreal", 
            "unreal engine", "unity engine", "pubg", "cyberpunk game", 
            "fps", "rpg", "in-engine", "cel-shaded", "cyberpunk cityscape"
        ],
        "game_retro": ["retro game", "8-bit", "16-bit", "pixel art", "chunky pixels"],
        "game_cel_shaded": ["cel-shaded", "toon shading", "anime style", "cartoon style"],
        "game_3d": ["3d game", "3d engine", "realistic game", "next-gen game"],
        "game_indie": ["indie game", "indie art", "hand-drawn game", "pixel art"],

        # --- Photographic/Realism Categories ---
        "photographic": [
            "photo", "photograph", "shot on", "dslr", "camera", "realistic", 
            "film", "kodak", "fujifilm", "cinematic", "hyperrealism", "realism",
            "portrait photography", "landscape photography", "street photography"
        ],
        "cinematic": ["cinematic", "film look", "movie style", "motion picture"],
        "documentary": ["documentary", "documentary style", "journalistic"],
        "street_photography": ["street photography", "urban photography", "candid photography"],

        # --- Fantasy/Sci-Fi Categories ---
        "fantasy": ["fantasy", "mythical", "magical", "wizard", "fairy", "dragon", "unicorn", "fairy tale", "castle", "fantasy landscape"],
        "sci_fi": ["sci-fi", "science fiction", "cyberpunk", "futuristic", "spaceship", "space opera"],
        "space_art": ["space art", "astronomy art", "cosmic", "galaxy"],
        "robot_art": ["robot art", "mech art", "cybernetic", "mecha"],
        "steampunk": ["steampunk", "victorian sci-fi", "industrial fantasy"],
        "dystopian": ["dystopian", "post-apocalyptic", "dark future", "ruined world"],

        # --- New Categories from Tavily Search ---
        "papercraft": ["papercraft", "paper cut", "folded paper", "layered paper", "glued paper"],
        "luna_photo": ["luna photo", "double exposure", "surreal photographic", "ethereal photo"],
        "pop_surrealism": ["pop surrealism", "lowbrow art", "cartoon surrealism", "fantastical pop art"],
        "synesthesia_art": ["synesthesia art", "color sound fusion", "sensory blending art"],
        "weirdcore": ["weirdcore", "surreal glitch", "dreamlike glitch", "uncanny art"],
        "dreamcore": ["dreamcore", "dreamlike aesthetic", "ethereal dream art"],
        "ferrofluid": ["ferrofluid", "magnetic fluid art", "liquid metal art"],
        "animal_inspired": ["animal inspired", "animal motif", "fauna art", "wildlife art"],
        "ascii_art": ["ascii art", "text art", "character art", "typographic art"],
        "biopunk": ["biopunk", "biological cyberpunk", "genetic art", "bio-tech art"],
        "kinetic_art": ["kinetic art", "moving art", "dynamic sculpture", "motion art"],
        "nightcore": ["nightcore", "fast paced art", "high energy art", "vibrant neon art"],
        "optic_art": ["optic art", "op art", "optical illusion art", "visual trickery"]
        # Fallback for generics - last so specific matches win first
        ,"unknown": []
    }

    # Check each category's keywords
    for category, keywords in categories_keywords.items():
        for term in keywords:
            if term in style_lower:
                # Map subcategories to canonical template categories
                if category == "3d_render":
                    return "3d_render"
                if category in [
                    "oil_painting", "watercolor", "pastel", "charcoal"
                ]:
                    return category
                if category in [
                    "pencil_sketch", "ink_drawing"
                ]:
                    return "drawing"
                if category == "minimalist":
                    return "minimalist"
                if category == "geometric":
                    return "geometric"
                if category.startswith("illustration"):
                    return category
                if category == "digital_art":
                    return "digital_art"
                if category == "game_style":
                    return "game_style"
                if category in ["photographic", "cinematic", "realistic"]:
                    # Pass through as is for template
                    return category
                if category in [
                    "abstract_conceptual", "abstract"
                ]:
                    return "abstract_conceptual"
                if category in ["material_sculptural", "sculpture"]:
                    return "material_sculptural"
                if category in ["fantasy", "sci_fi"]:
                    return category
                if category == "traditional_painting_drawing":
                    return "traditional_painting_drawing"
                if category in [
                    "papercraft", "luna_photo", "pop_surrealism", "synesthesia_art",
                    "weirdcore", "dreamcore", "ferrofluid", "animal_inspired",
                    "ascii_art", "biopunk", "kinetic_art", "nightcore", "optic_art"
                ]:
                    return category
        # Don't break early -- let most specific win first
    return "unknown"




def generate_ai_style(api_key: str) -> Optional[str]:
    """Generate an AI style name using Gemini AI."""
    if not AI_STYLE_GEN_AVAILABLE:
        print_error("AI Style Generator not available.")
        return None
    print_info("Generating AI style...")
    initialize_style_gemini(api_key)
    import random
    all_categories = [
        "oil_painting", "watercolor", "pastel", "charcoal", "pencil_sketch", "ink_drawing",
        "minimalist", "geometric", "illustration_pixel", "illustration_anime_manga", "illustration_comic",
        "photographic", "game_style", "digital_art", "abstract_conceptual", "material_sculptural",
        "fantasy", "sci_fi"
    ]
    chosen_category = random.choice(all_categories)
    print_info(f"Chose style category: {chosen_category}")
    style_obj = generate_random_style(category=chosen_category, style_type="detailed")
    if not style_obj or not isinstance(style_obj, dict):
        print_error("Failed to generate AI style.")
        return None
    name = style_obj['name']
    print_success(f"Generated AI style: {name}")
    return name


def generate_ai_preset(user_prefs: UserPreferences, base_style_override: Optional[str] = None) -> Union[str, bool, None]:
    """Generate a random preset based on style category."""
    api_key = get_gemini_api_key()
    if not api_key:
        print_error("Gemini API key not configured. Set GEMINI_API_KEY environment variable.")
        return False

    base_style = None
    try:
        # --- Step 1: Get Base Style ---
        if base_style_override:
            base_style = base_style_override
            print_info(f"Using provided style: {base_style}")
        else:
            print_section("Choose Style Source for Preset")
            print_option("1", "Enter Custom Style")
            print_option("2", "Generate AI Style")
            print_option("b", "Back")
            choice = get_validated_input("Select option (1-2, b)", ["1", "2", "b"])

            if choice == "b":
                print_info("Preset generation cancelled.")
                return None
            elif choice == "1":
                base_style = input("Enter your custom style: ").strip()
                if not base_style:
                    print_error("No style entered.")
                    return False
                # Use the entered custom style directly without generating AI style
            elif choice == "2":
                print_info("Attempting to generate AI preset (this may take a moment)...")
                base_style = generate_ai_style(api_key)
                if not base_style:
                    print_error("Failed to generate AI style.")
                    return False

        global gemini_initialized
        if 'gemini_initialized' not in globals():
            gemini_initialized = False

        if not gemini_initialized:
            if not initialize_style_gemini(api_key):
                print_error("Failed to initialize Gemini API.")
                return False
        gemini_initialized = True

        # --- Step 2: Generate Settings ---
        print_info(f"\nGenerating settings for style: '{base_style}'...")
        style_category = categorize_style(base_style)
        print_info(f"(Detected category: {style_category})")

        # Initialize Gemini with Fallback
        genai.configure(api_key=api_key)
        model = None

        try:
            model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')  # Use updated Gemini Flash model directly
            print_info("Using Gemini Flash model...")
        except Exception as err:
            logging.error(f"Failed to initialize Gemini Flash model: {err}")
            print_error("Could not initialize AI model.")
            return False

        # Build category-specific instructions
        instruction_header = f"Select settings that work well with \"{base_style}\" ({style_category}):"
        category_instructions = ""

        if style_category == "digital_art":
            category_instructions = """*   **Digital Art Focus:**
            - Art Movement: Consider 'Digital Art', 'Contemporary Digital'
            - Techniques: Digital painting, vector art, 3D modeling (non-game)
            - Lighting: Studio lighting, dramatic, atmospheric
            - Effects: Digital effects (glow, particles) but avoid game-specific effects
            - Colors: Full range available, from realistic to vibrant
            - Camera/View: Flexible, based on artistic vision"""

        elif style_category == "minimalist_geometric":
            category_instructions = """*   **Minimalist Geometric Focus:**
            - Style: Clean, simple geometric shapes
            - Colors: Muted pastels or monochrome
            - Composition: Balanced with negative space
            - Mood: Calm, orderly, modern"""

        elif style_category == "psychedelic":
            category_instructions = """*   **Psychedelic Focus:**
            - Colors: Vibrant, neon, contrasting
            - Patterns: Swirling, fractal, kaleidoscopic
            - Effects: Glowing, pulsating, morphing visuals
            - Mood: Trippy, surreal, intense"""

        elif style_category == "surrealism":
            category_instructions = """*   **Surrealism Focus:**
            - Concept: Dreamlike, bizarre, unexpected juxtapositions
            - Colors: Muted, contrasting, symbolic
            - Composition: Layered, symbolic, narrative
            - Mood: Mysterious, uncanny, thought-provoking"""

        elif style_category == "fantasy_landscape":
            category_instructions = """*   **Fantasy Landscape Focus:**
            - Environment: Mystical forests, floating islands, enchanted castles
            - Lighting: Ethereal, glowing, magical
            - Colors: Rich, vibrant, otherworldly
            - Mood: Epic, adventurous, mysterious"""

        elif style_category == "cyberpunk_cityscape":
            category_instructions = """*   **Cyberpunk Cityscape Focus:**
            - Environment: Neon-lit streets, futuristic skyscrapers, rainy nights
            - Lighting: Neon, reflective, high contrast
            - Colors: Dark, neon, saturated
            - Mood: Gritty, futuristic, dystopian"""

        elif style_category == "game_style":
            category_instructions = """*   **Game Style Focus:**
            - Art Movement: 'Game Art', specific game genre styles
            - Engine Focus: Unreal/Unity style renders
            - Lighting: Game-engine specific (volumetric, real-time GI)
            - Effects: Game-specific (bloom, ambient occlusion)
            - View: Game camera perspectives
            - Polish: High-end game engine look"""

        elif style_category == "photographic":
            is_film = any(x in base_style.lower() for x in ["film", "kodak", "analog"])
            camera = "Film Camera" if is_film else "Digital Camera (e.g., Canon EOS R5)"
            category_instructions = f"""*   **Photographic Focus:**
            - Camera: Suggest {camera}
            - Lens: Appropriate focal length (e.g., 35mm, 85mm)
            - Lighting: Natural or studio lighting
            - Style: {', '.join(['film grain', 'analog look'] if is_film else ['sharp', 'realistic'])}"""

        elif style_category.startswith("illustration"):
            if style_category == "illustration_pixar":
                category_instructions = """*   **Pixar Style:**
                - Colors: Vibrant, saturated
                - Lighting: Cinematic, warm depth
                - Textures: Detailed, 'touchable'
                - Mood: Usually uplifting"""
            elif style_category == "illustration_disney":
                category_instructions = """*   **Disney Style:**
                - Style: Traditional animation look
                - Characters: Expressive, fluid
                - Backgrounds: Often watercolor-inspired
                - Mood: Nostalgic, magical"""
            elif style_category == "illustration_vintage_cartoon":
                category_instructions = """*   **Vintage Cartoon:**
                - Style: Rubber hose animation
                - Forms: Simple, rounded shapes
                - Colors: Limited palette
                - Mood: Playful, nostalgic"""
            elif style_category == "illustration_anime_manga":
                category_instructions = """*   **Anime/Manga:**
                - Style: Characteristic linework
                - Lighting: Often cel-shaded
                - Eyes: Large, expressive
                - Colors: Can be vibrant or muted"""
            else:
                category_instructions = """*   **General Illustration:**
                - Style: Clean linework
                - Colors: Usually flat or cel-shaded
                - Lighting: Stylized
                - View: Artistic perspective"""

        elif style_category == "traditional_painting_drawing":
            category_instructions = """*   **Traditional Medium:**
            - Technique: Emphasize texture, brushwork
            - Lighting: Natural, atmospheric
            - Movement: Consider historical styles
            - Colors: Often earth tones or traditional palettes"""

        elif style_category == "abstract_conceptual":
            category_instructions = """*   **Abstract Focus:**
            - Form: Non-representational
            - Color: Expressive use
            - Composition: Can be unconventional
            - Movement: Consider modern art influences"""

        else:
            category_instructions = """*   **General Guidance:**
            - Choose settings that match the style
            - Consider the mood and atmosphere
            - Select appropriate technical parameters"""

        # Get the appropriate template for this style category
        template = get_template_for_category(style_category)

        # Build the complete prompt
        prompt = f"""
        Generate settings for a wallpaper with style: "{base_style}"

        Instructions:
        1. Create a unique `preset_name` inspired by the style
        2. Choose ONE mood from: peaceful, serene, energetic, dramatic, mysterious, romantic, playful, dreamy
        3. {instruction_header}
           {category_instructions}
        4. For the `negative_prompt` field in `imagen_settings`, generate a negative prompt that is specifically tailored to AVOID elements that would clash with or detract from the "{base_style}" style and its category "{style_category}". Consider common issues or undesirable elements for this type of art. Replace the placeholder "[GENERATE_NEGATIVE_PROMPT_BASED_ON_STYLE]" with this generated negative prompt.
        5. Use aspect ratio 16:9 for desktop wallpaper
        6. Output ONLY valid JSON matching this structure:

        {json.dumps(template, indent=4)}
        """

        # Generate settings with fallback
        using_flash = False
        for attempt in range(3):
            print_info(f"Generating settings (Attempt {attempt + 1}/3)...")
            try:
                response = model.generate_content(prompt)
            except Exception as api_err:
                if "429" in str(api_err) and not using_flash and model.model_name == 'gemini-2.5-pro-preview-03-25':
                    # Switch to Flash model only if not already using it
                    print_warning("Pro model quota exceeded, switching to Gemini Flash...")
                    model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')
                    using_flash = True
                    print_info("Using Gemini Flash model...")
                    continue  # Retry the same attempt with Flash

                else:
                    # Either already using Flash or different error
                    logging.error(f"Generation failed: {api_err}")
                    print_error(f"Failed to generate settings: {api_err}")
                    if attempt == 2:  # Last attempt
                        return False
                    continue  # Try next attempt

            # Process response if we got one
            if response and response.text:
                response_text = response.text.strip()
                json_match = re.search(r'```json\s*({[\s\S]*?})\s*```|({[\s\S]*})', response_text)
                if json_match:
                    try:
                        settings_data = json.loads(json_match.group(1) or json_match.group(2))
                        # Construct preset data
                        preset_data = {
                            "preset_name": settings_data.get("preset_name", f"{base_style} Preset"),
                            "styles": [base_style],
                            "moods": settings_data.get("moods", []),
                            "imagen_settings": settings_data.get("imagen_settings", {}),
                            "aspect_ratio": settings_data.get("aspect_ratio", "16:9")
                        }

                        if not isinstance(preset_data.get("imagen_settings"), dict):
                            raise ValueError("Invalid imagen_settings structure")

                        if is_preset_unique(preset_data):
                            # Show the generated preset
                            print_section(f"AI Generated Preset: {preset_data['preset_name']}")
                            print(json.dumps(preset_data, indent=2))
                            print("-" * 50)

                            # Ask to save with more user guidance
                            if get_validated_input("Do you want to save this preset? (Y/N): ", ["y", "n"]) == "y":
                                save_name = re.sub(r'[^\w\s-]', '', preset_data["preset_name"]).strip().replace(' ', '_')
                                if not save_name:
                                    save_name = "unnamed_preset"

                                presets_dir = os.path.join(os.path.dirname(__file__), PRESETS_DIR)
                                os.makedirs(presets_dir, exist_ok=True)

                                preset_path = os.path.join(presets_dir, f"{save_name}.json")
                                if os.path.exists(preset_path):
                                    if get_validated_input(f"Preset '{save_name}' exists. Overwrite? (Y/N): ", ["y", "n"]) != "y":
                                        print_info("Preset not saved.")
                                        return None

                                with open(preset_path, 'w') as f:
                                    json.dump(preset_data, f, indent=4)
                                save_preset_to_cache(preset_data)
                                print_success(f"\n✅ Preset saved to: {preset_path}\n")
                                return preset_path
                            else:
                                print_warning("Preset discarded by user.")
                                return None

                        elif attempt < 2:
                            print_warning("Generated non-unique preset, trying again...")
                            continue
                        else:
                            print_warning("Could not generate unique preset after 3 attempts.")
                            return False

                    except (json.JSONDecodeError, ValueError) as e:
                        if attempt < 2:
                            print_warning(f"Invalid response format ({e}), retrying...")
                            continue
                        print_error("Failed to get valid response format after 3 attempts.")
                        return False

                else: # No JSON found
                    if attempt < 2:
                        print_warning("Could not extract settings JSON, retrying...")
                        continue
                    print_error("Failed to get valid JSON after 3 attempts.")
                    return False

            else: # Empty response
                if attempt < 2:
                    print_warning("Empty response from AI, retrying...")
                    continue
                print_error("Failed to get response after 3 attempts.")
                return False

        return False # If we get here, all attempts failed

    except Exception as e:
        logging.exception(f"Unexpected error in preset generation: {e}")
        print_error(f"An unexpected error occurred: {e}")
        return False

# --- Main CLI Interface ---

def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(description='Generate and manage AI presets')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate a new preset')
    gen_parser.add_argument('--style', help='Custom style to use')

    # List command
    list_parser = subparsers.add_parser('list', help='List available presets')

    # Load command
    load_parser = subparsers.add_parser('load', help='Load a preset')
    load_parser.add_argument('name', help='Preset name (without .json)')

    # Delete command
    del_parser = subparsers.add_parser('delete', help='Delete a preset')
    del_parser.add_argument('name', help='Preset name (without .json)')

    args = parser.parse_args()

    if args.command == 'generate':
        if not SETTINGS_AVAILABLE:
            print_error("wallpaper_settings.py required for generation.")
            sys.exit(1)
        user_prefs = initialize_settings()
        result = generate_ai_preset(user_prefs, args.style)
        if isinstance(result, str):
            print(f"\nPreset generated and saved: {result}")
        elif result is None:
            print("\nPreset generation cancelled or discarded.")
        else:
            print("\nPreset generation failed.")
            sys.exit(1)

    elif args.command == 'list':
        presets_dir = os.path.join(os.path.dirname(__file__), PRESETS_DIR)
        if os.path.exists(presets_dir):
            presets = [f[:-5] for f in os.listdir(presets_dir) if f.endswith('.json')]
            if presets:
                print("\nAvailable presets:")
                for preset in sorted(presets):
                    print(f"  {preset}")
            else:
                print_info("No presets found.")
        else:
            print_info(f"Presets directory not found at: {presets_dir}")

    elif args.command == 'load':
        if not SETTINGS_AVAILABLE:
            print_error("wallpaper_settings.py required for loading presets.")
            sys.exit(1)

        preset_path = os.path.join(os.path.dirname(__file__), PRESETS_DIR, f"{args.name}.json")
        if os.path.exists(preset_path):
            try:
                with open(preset_path) as f:
                    preset_data = json.load(f)
                user_prefs = initialize_settings()

                # Use _apply_preset_settings from wallpaper_settings.py to apply preset
                from wallpaper_settings import _apply_preset_settings

                if not _apply_preset_settings(preset_data, replace=True):
                    print_error("Failed to apply preset settings.")
                    sys.exit(1)

                # Save preferences
                user_prefs.save_preferences()
                print_success(f"Loaded and applied preset: {args.name}")

            except Exception as e:
                print_error(f"Error loading preset: {e}")
                sys.exit(1)
        else:
            print_error(f"Preset not found: {args.name}")
            sys.exit(1)

    elif args.command == 'delete':
        preset_path = os.path.join(os.path.dirname(__file__), PRESETS_DIR, f"{args.name}.json")
        if os.path.exists(preset_path):
            if get_validated_input(f"Delete preset '{args.name}'? (Y/N): ", ["y", "n"]) == "y":
                try:
                    # Use delete_preset from wallpaper_settings.py
                    from wallpaper_settings import delete_preset

                    # Call delete_preset with the preset name
                    if delete_preset(args.name):
                        print_success(f"Deleted preset: {args.name}")
                    else:
                        print_error(f"Failed to delete preset: {args.name}")
                        sys.exit(1)
                except Exception as e:
                    print_error(f"Error deleting preset: {e}")
                    sys.exit(1)
            else:
                print_info("Deletion cancelled.")
        else:
            print_error(f"Preset not found: {args.name}")
            sys.exit(1)

if __name__ == "__main__":
    main()
