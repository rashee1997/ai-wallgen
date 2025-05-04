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

def categorize_style(style_name: Union[str, Dict]) -> Union[str, List[str]]:
    """
    Attempt to categorize a style name. Digital art and game styles are kept completely separate.
    Now supports prioritized hybrid (compound) style detection.
    Args:
        style_name: Either a string style name or a dictionary with 'name' key
    """
    if isinstance(style_name, dict):
        style_name = style_name.get('name', '')

    # Normalize style_name by replacing underscores and hyphens with spaces to improve matching
    style_name = str(style_name).replace('_', ' ').replace('-', ' ')
    # Normalize British English spelling variants to American English for consistent matching
    style_name = style_name.replace('colour', 'color')
    # Normalize spaced variant "water color" to "watercolor"
    style_name = style_name.replace('water color', 'watercolor')
    style_lower = style_name.lower()

    # Split and normalize tokens for hybrid detection
    tokens = [t.strip() for t in re.split(r'[,+/&|]', style_lower) if t.strip()]
    tokens_set = frozenset(tokens)

    # --- Hybrid/Compound Style Mapping (Token-based) ---
    hybrid_styles = {
        frozenset({'pop', 'surrealism'}): 'pop_surrealism',
        frozenset({'abstract', 'expressionism', 'cubism'}): 'abstract_expressionism_cubism_fusion',
        # Removed watercolor_pencil as it's now keyword-based below
        # frozenset({'watercolor', 'pencil'}): 'watercolor_pencil',
        frozenset({'traditional', 'digital'}): 'hybrid_traditional_digital',
        frozenset({'collage', 'digital'}): 'collage_digital_overlay',
        frozenset({'experimental', 'mixed media'}): 'experimental_mixed_media',
        # Removed patchwork_collage as it's keyword-based below
        # frozenset({'patchwork', 'collage'}): 'patchwork_collage',
        # Removed paper_quilling as it's keyword-based below
        # frozenset({'paper', 'quilling'}): 'paper_quilling',
        frozenset({'tradigital', 'mixed media'}): 'tradigital_mixed_media',
        frozenset({'whimsical', 'mixed media'}): 'whimsical_mixed_media',
        frozenset({'sci-fi', 'futuristic'}): 'sci_fi_futuristic',
        # Add more token-based hybrids as needed
    }
    # Prioritized token-based hybrid detection
    for hybrid_set, hybrid_cat in hybrid_styles.items():
        if hybrid_set == tokens_set:
            logging.info(f"Matched token-based hybrid style: {hybrid_cat} for '{style_name}'")
            return hybrid_cat

    # --- Keyword-based Hybrid Category Definitions ---
    # Priority: Check these *after* token-based hybrids, *before* general single-term keywords.
    hybrid_categories_keywords = {
        # Copied from user request
        "kinetic_ascii": [ "kinetic + ascii", "ascii + kinetic", "kinetic art + ascii art", "ascii art + kinetic art", "kinetic with ascii", "ascii with kinetic", "ascii kinetic", "kinetic ascii" ],
        "watercolor_pencil": [
            "watercolor + pencil", "pencil + watercolor", "watercolor and pencil", "pencil and watercolor",
            "watercolor pencil", "pencil watercolor", "watercolor with pencil sketch", "pencil sketch with watercolor",
            "water colour + pencil", "pencil + water colour", "water colour and pencil", "pencil and water colour",
            "water colour pencil", "pencil water colour", "water colour with pencil sketch", "pencil sketch with water colour"
        ],
        "photorealism_glitch": [ "photorealism + glitch", "glitch + photorealism", "glitch art + photorealism", "photorealism and glitch", "glitch realistic", "realistic glitch art" ],
        "anime_oilpainting": [ "anime + oil painting", "oil painting + anime", "anime oil painting", "oil painting anime", "anime with oil painting", "oil painting with anime" ],
        "minimalist_geometric": [ "minimalist + geometric", "geometric + minimalist", "minimalist geometric", "geometric minimalist", "minimal geometric shapes", "minimalism", "minimalist", "minimal", "minimal art", "geometric", "geometry", "geometric abstract", "low poly", "minimalist geometric", "minimal geometric", "geometric minimalism" ], # Includes base terms
        "pop_surrealism_ascii": [ "pop surrealism + ascii", "ascii + pop surrealism", "pop surrealism ascii", "ascii pop surrealism" ],
        "dreamcore_weirdcore": [ "dreamcore + weirdcore", "weirdcore + dreamcore", "dreamcore and weirdcore", "weirdcore and dreamcore" ],
        "patchwork_collage": [ "patchwork collage", "collage patchwork", "fabric collage", "mixed media collage", "paper collage" ],
        "paper_quilling": [ "paper quilling", "quilling art", "rolled paper art", "coil paper art" ],
        "tradigital_mixed_media": [ "tradigital mixed media", "digital and traditional mixed media", "tradigital art" ],
        "whimsical_mixed_media": [ "whimsical mixed media", "whimsical art", "dreamy mixed media", "fantasy mixed media" ],
        "sci_fi_futuristic": [ "sci-fi", "science fiction", "futuristic digital art", "cyberpunk", "dystopian digital art" ], # Includes base terms
        "mediterranean_style": [ "mediterranean style", "sunny coastal art", "vivid colorful mediterranean" ],
        "morphism_surreal": [ "morphism", "surreal morphing art", "fantastical transformations" ],
        "cubism_mixed": [ "cubism", "cubist mixed media", "angular forms", "multiple perspectives" ], # Includes base term
        "pixel_patchwork": [ "pixel art", "pixel patchwork", "voxel art", "low poly pixel" ], # Includes base term
        "phygital_hybrid": [ "phygital art", "physical digital hybrid", "augmented reality art", "3d printing art" ],
        "screen_printing_bold": [ "screen printing", "bold graphic art", "tactile print art" ],
        "mixed_media_journaling": [ "mixed media journaling", "art journaling", "sketchbook mixed media" ],
        "digital_pixel_traditional": [ "digital pixel art", "pixel art with traditional media", "pixel and paint hybrid" ],
        "patchwork_fabric": [ "patchwork fabric", "fabric collage", "textile patchwork" ],
        "mixed_media_collage": [ "mixed media collage", "collage art", "assemblage mixed media", "mixed media", "collage", "assemblage", "combined media" ], # Includes base terms
        "whimsical_fantasy": [ "whimsical fantasy", "fantasy whimsical art", "dreamlike whimsical" ],
        "cubism_futurism": [ "cubism futurism", "angular futurism", "geometric futurism" ],
        "digital_traditional_fusion": [ "digital traditional fusion", "hybrid digital traditional", "mixed media fusion" ],
        "retro_pixel_vaporwave": [ "retro pixel", "vaporwave pixel art", "synthwave pixel" ],
        "psychedelic_surrealism": [ "psychedelic surrealism", "trippy surreal art", "dreamlike psychedelic" ],
        "hybrid_traditional_digital": [ "hybrid traditional digital", "traditional digital fusion", "mixed traditional digital" ],
        "installation_art": [ "installation art", "immersive art", "spatial art", "mixed media installation" ],
        "scientific_technological_hybrid": [ "scientific hybrid art", "technological art", "data driven art", "algorithmic art", "ai art", "ar art", "vr art" ],
        "augmented_reality_art": [ "augmented reality art", "ar art", "mixed reality art", "interactive digital art" ],
        "abstract_expressionism_cubism_fusion": [ "abstract expressionism cubism", "abstract cubism fusion", "expressionist cubism" ],
        "collage_digital_overlay": [ "collage digital overlay", "digital collage", "photo manipulation collage" ],
        "experimental_mixed_media": [ "experimental mixed media", "avant-garde mixed media", "boundary pushing mixed media" ],
    }

    # Check keyword-based hybrid categories
    for category, keywords in hybrid_categories_keywords.items():
        for term in keywords:
            # Use \b for word boundaries to avoid partial matches (e.g., 'art' in 'earth')
            if re.search(r'\b' + re.escape(term) + r'\b', style_lower):
                logging.info(f"Matched keyword-based hybrid style: {category} using term '{term}' for '{style_name}'")
                return category

    # --- General/Single-Term Category Keywords ---
    # Fallback: legacy multi-style support (accumulate all matches)
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
        "illustration_pixel": ["pixel art", "8-bit", "16-bit", "pixelated", "retro game art"], # Moved from hybrid list
        "illustration_graphic": ["illustration", "cartoon", "cartoony", "graphic novel"],
        "illustration_childrens": ["children's book", "picture book", "kids illustration"],
        "illustration_fantasy": ["fantasy illustration", "mythical", "magical creatures"],
        "ink_punk": ["ink punk", "inkpunk", "hand-drawn sketchy", "unfinished look"],

        # --- Portrait Categories ---
        "photographic_portrait": ["photographic portrait", "photo portrait", "realistic portrait"],
        "traditional_portrait": ["traditional portrait", "oil portrait", "watercolor portrait", "pastel portrait", "charcoal portrait"],
        "futuristic_portrait": ["futuristic portrait", "sci-fi portrait", "cyberpunk portrait"],
        "illustration_portrait": ["illustration portrait", "cartoon portrait", "anime portrait", "manga portrait"],
        "pop_portrait": ["pop portrait", "pop art portrait"],

        # --- Painting/Drawing Categories ---
        "oil_painting": ["oil painting", "oil paint", "impasto", "alla prima", "wet-on-wet"],
        "watercolor": ["watercolor", "watercolour", "wet-on-wet", "wet-on-dry"], # Base term
        "pastel": ["pastel", "pastel drawing", "pastel painting"],
        "charcoal": ["charcoal sketch", "charcoal drawing", "charcoal art"],
        "pencil_sketch": ["pencil", "pencil sketch", "graphite", "pencil drawing"], # Base term
        "ink_drawing": ["ink drawing", "ink sketch", "pen and ink", "line drawing", "line art", "ink wash"],
        "acrylic_painting": ["acrylic", "acrylic paint", "acrylic painting"],
        # "mixed_media": ["mixed media", "collage", "assemblage", "combined media"], # Moved to hybrid "mixed_media_collage"
        "digital_painting": ["digital painting", "digital illustration", "digital art"], # Base term

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
        "surrealism": ["surrealism", "surreal", "dreamlike", "fantastical"], # Base term
        "cubism": ["cubism", "cubist", "geometric abstraction"], # Base term
        "fauvism": ["fauvism", "fauvist", "wild beasts"],
        "art_nouveau": ["art nouveau", "new art", "modern style"],
        "art_deco": ["art deco", "decop", "modernist"],
        "art_deco_revival": ["art deco revival", "art deco revival", "art deco style", "art deco architecture"],

        # --- Minimalist/Geometric Categories ---
        # "minimalist": ["minimalism", "minimalist", "minimal", "minimal art"], # Covered by hybrid "minimalist_geometric"
        # "geometric": ["geometric", "geometry", "geometric abstract", "low poly"], # Covered by hybrid "minimalist_geometric"
        "constructivism": ["constructivism", "constructivist", "industrial art"],
        "low_poly": ["low poly", "low polygon", "polygonal art"], # Base term
        "isometric": ["isometric", "isometric view", "axonometric"],

        # --- Digital/Modern Categories ---
        "digital_art": [ # Broad category
            "digital art", "digital painting", "vector art", "glitch art",
            "vaporwave", "retrowave", "rendered", "digital illustration", "digital media"
        ],
        "psychedelic": ["psychedelic", "trippy", "hallucinogenic", "psychedelia", "acid art"], # Base term
        "cyberpunk": ["cyberpunk", "cyberpunk art", "futuristic", "neon city"], # Base term
        "retrowave": ["retrowave", "vaporwave", "80s revival", "synthwave"], # Base term
        "glitch_art": ["glitch art", "glitch effect", "digital glitch", "error art"], # Base term
        "vector_art": ["vector art", "vector illustration", "vector graphics"],
        # "3d_render": ["3d render", "3d art", "3d modeling", "3d illustration"], # Already defined above

        # --- Game Art Categories ---
        "game_style": [
            "game style", "game art", "game engine", "unity", "unreal",
            "unreal engine", "unity engine", "pubg", "cyberpunk game",
            "fps", "rpg", "in-engine", "cel-shaded", "cyberpunk cityscape"
        ],
        "game_retro": ["retro game", "8-bit", "16-bit", "pixel art", "chunky pixels"],
        "game_cel_shaded": ["cel-shaded", "toon shading", "anime style", "cartoon style"],
        "game_3d": ["3d game", "3d engine", "realistic game", "next-gen game"],
        "game_indie": ["indie game", "indie art", "hand-drawn game"], # Removed "pixel art" as it's in illustration_pixel

        # --- Photographic/Realism Categories ---
        "photographic": [
            "photo", "photograph", "photographic", "shot on", "dslr", "camera", "realistic",
            "film", "kodak", "fujifilm", "cinematic", "hyperrealism", "realism",
            "portrait photography", "landscape photography", "street photography"
        ],
        "cinematic": ["cinematic", "film look", "movie style", "motion picture"],
        "documentary": ["documentary", "documentary style", "journalistic"],
        "street_photography": ["street photography", "urban photography", "candid photography"],

        # --- Fantasy/Sci-Fi Categories ---
        "fantasy": ["fantasy", "mythical", "magical", "wizard", "fairy", "dragon", "unicorn", "fairy tale", "castle", "fantasy landscape"], # Base term
        "sci_fi": ["sci-fi", "science fiction", "spaceship", "space opera"], # Base term, subset of hybrid sci_fi_futuristic
        "space_art": ["space art", "astronomy art", "cosmic", "galaxy"],
        "robot_art": ["robot art", "mech art", "cybernetic", "mecha"],
        "steampunk": ["steampunk", "victorian sci-fi", "industrial fantasy"],
        "dystopian": ["dystopian", "post-apocalyptic", "dark future", "ruined world"], # Base term

        # --- New Single-Term Categories (from Tavily research, if not covered by hybrids) ---
        "papercraft": ["papercraft", "paper cut", "folded paper", "layered paper", "glued paper"], # Base term
        "luna_photo": ["luna photo", "double exposure", "surreal photographic", "ethereal photo"],
        "pop_surrealism": ["pop surrealism", "lowbrow art", "cartoon surrealism", "fantastical pop art"], # Base term
        "synesthesia_art": ["synesthesia art", "color sound fusion", "sensory blending art"],
        "weirdcore": ["weirdcore", "surreal glitch", "dreamlike glitch", "uncanny art"], # Base term
        "dreamcore": ["dreamcore", "dreamlike aesthetic", "ethereal dream art"], # Base term
        "ferrofluid": ["ferrofluid", "magnetic fluid art", "liquid metal art"],
        "animal_inspired": ["animal inspired", "animal motif", "fauna art", "wildlife art"],
        "ascii_art": ["ascii art", "text art", "character art", "typographic art"], # Base term
        "biopunk": ["biopunk", "biological cyberpunk", "genetic art", "bio-tech art"],
        "kinetic_art": ["kinetic art", "moving art", "dynamic sculpture", "motion art"], # Base term
        "nightcore": ["nightcore", "fast paced art", "high energy art", "vibrant neon art"],
        "optic_art": ["optic art", "op art", "optical illusion art", "visual trickery"],
        # Fallback for generics - last so specific matches win first
        "unknown": []
    }

    # Check each general category's keywords
    matched_categories = set()
    for category, keywords in categories_keywords.items():
        for term in keywords:
            # Use word boundaries for better matching
            if re.search(r'\b' + re.escape(term) + r'\b', style_lower):
                # Map subcategories to canonical template categories
                mapped_category = category # Default to the matched category name

                if category == "3d_render": mapped_category = "3d_render"
                elif category in ["oil_painting", "watercolor", "pastel", "charcoal"]: pass # Keep as is
                elif category in ["pencil_sketch", "ink_drawing"]: mapped_category = "drawing"
                # elif category == "minimalist": mapped_category = "minimalist" # Handled by hybrid
                # elif category == "geometric": mapped_category = "geometric" # Handled by hybrid
                elif category.startswith("illustration"): pass # Keep as is (e.g., illustration_pixar)
                elif category == "digital_art": mapped_category = "digital_art"
                elif category == "game_style": mapped_category = "game_style"
                elif category in ["photographic", "cinematic", "realism"]: pass # Keep as is
                elif category in ["abstract", "abstract_conceptual"]: mapped_category = "abstract_conceptual"
                # elif category == "mixed_media": mapped_category = "mixed_media_collage" # Handled by hybrid
                elif category in ["material_sculptural", "sculpture"]: mapped_category = "material_sculptural"
                elif category in ["fantasy", "sci_fi"]: pass # Keep as is
                elif category == "traditional_painting_drawing": mapped_category = "traditional_painting_drawing"
                elif category in [ # New single-term categories
                    "papercraft", "luna_photo", "pop_surrealism", "synesthesia_art",
                    "weirdcore", "dreamcore", "ferrofluid", "animal_inspired",
                    "ascii_art", "biopunk", "kinetic_art", "nightcore", "optic_art",
                    # Other base terms
                    "surrealism", "cubism", "psychedelic", "cyberpunk", "retrowave", "glitch_art",
                    "steampunk", "dystopian",
                    # New Portrait Categories - explicitly map them
                    "photographic_portrait", "traditional_portrait", "futuristic_portrait",
                    "illustration_portrait", "pop_portrait"
                ]: pass # Keep as is

                logging.info(f"Matched single-term style: {mapped_category} using term '{term}' for '{style_name}'")
                matched_categories.add(mapped_category)
                # Don't break inner loop - allow multiple keywords for same category
                # Don't break outer loop - allow matching multiple categories if needed later, though we currently return first

    # --- Prioritize and Return ---
    # If multiple single-term categories matched, apply some prioritization logic if needed
    # For now, just return the first one found alphabetically (or based on dict order, which is insertion order in Py 3.7+)
    if matched_categories:
        # Simple prioritization: maybe prefer more specific illustrations?
        preferred_order = [
            "illustration_pixar", "illustration_disney", "illustration_vintage_cartoon",
            "illustration_anime_manga", "illustration_comic", "illustration_pixel",
            "illustration_graphic", "illustration_childrens", "illustration_fantasy"
        ]
        for pref in preferred_order:
            if pref in matched_categories:
                return pref
        # Otherwise, return any match (sorted for consistency)
        return sorted(list(matched_categories))[0]

    # If no specific, hybrid, or single-term match found
    logging.warning(f"Could not categorize style: '{style_name}'. Falling back to 'unknown'.")
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
        "minimalist_geometric", # Use hybrid category
        "illustration_pixel", "illustration_anime_manga", "illustration_comic",
        "photographic", "game_style", "digital_art", "abstract_conceptual", "material_sculptural",
        "fantasy", "sci_fi", "sci_fi_futuristic", "cyberpunk", # Added more specifics
        "pop_surrealism", "papercraft", "kinetic_art", "watercolor_pencil", # Added some new ones
        # Add new portrait categories
        "photographic_portrait", "traditional_portrait", "futuristic_portrait",
        "illustration_portrait", "pop_portrait"
    ]
    chosen_category = random.choice(all_categories)
    print_info(f"Chose style category: {chosen_category}")
    # Assuming generate_random_style can handle these category names
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
            # Initialize Gemini for preset generation here if needed
            # Note: initialize_style_gemini might already do this.
            # If separate initialization is needed:
            try:
                genai.configure(api_key=api_key)
                # Test connection if needed
                # list(genai.list_models())
                gemini_initialized = True
            except Exception as init_err:
                 logging.error(f"Failed to initialize Gemini API: {init_err}")
                 print_error(f"Failed to initialize Gemini API: {init_err}")
                 return False
            # Consider moving initialize_style_gemini call here if it covers both uses

        # --- Step 2: Generate Settings ---
        print_info(f"\nGenerating settings for style: '{base_style}'...")
        style_category = categorize_style(base_style)
        print_info(f"(Detected category: {style_category})")

        # Initialize Gemini Model
        model = None
        using_flash = False # Track if we switched to flash
        preferred_model = 'gemini-2.0-flash' # Use the latest flash model alias

        try:
            model = genai.GenerativeModel(preferred_model)
            print_info(f"Using Gemini model: {preferred_model}...")
        except Exception as err:
            logging.error(f"Failed to initialize Gemini model '{preferred_model}': {err}")
            print_error("Could not initialize AI model.")
            return False

        # Build category-specific instructions
        instruction_header = f"Select settings that work well with \"{base_style}\" (category: {style_category}):"
        category_instructions = ""

        # --- Add instructions for NEW categories ---
        if style_category == "watercolor_pencil":
            category_instructions = """*   **Watercolor Pencil Focus:**
            - Technique: Blend watercolor washes with distinct pencil lines. Soft edges vs sharp details.
            - Texture: Visible paper texture, light watercolor grain, graphite sheen.
            - Colors: Transparent washes, buildable layers, pencil shading.
            - Mood: Delicate, illustrative, sketched."""
        elif style_category == "minimalist_geometric":
            category_instructions = """*   **Minimalist Geometric Focus:**
            - Style: Clean, simple geometric shapes (lines, circles, squares). Emphasis on negative space.
            - Colors: Often monochrome, muted palettes, or limited accent colors.
            - Composition: Balanced, orderly, potentially asymmetric.
            - Mood: Calm, modern, sophisticated, uncluttered."""
        elif style_category == "patchwork_collage":
            category_instructions = """*   **Patchwork Collage Focus:**
            - Technique: Combine different textures/patterns like fabric scraps, paper cutouts. Layering.
            - Texture: Visible seams, fabric weave, paper edges, tactile feel.
            - Colors: Varied, can be harmonious or contrasting based on 'patches'.
            - Mood: Handcrafted, textured, eclectic, potentially folk-art inspired."""
        elif style_category == "sci_fi_futuristic":
             category_instructions = """*   **Sci-Fi/Futuristic Focus:**
            - Elements: Advanced technology, spaceships, futuristic cities, cybernetics, aliens.
            - Lighting: Often high-contrast, neon glows, lens flares, artificial sources.
            - Colors: Can range from sleek monochrome/metallics to vibrant neon palettes.
            - Mood: Awe-inspiring, advanced, potentially dystopian or utopian."""
        # --- Existing category instructions (condensed for brevity) ---
        elif style_category == "digital_art": category_instructions = "*   **Digital Art Focus:** Flexible techniques (painting, vector, 3D non-game), studio/atmospheric lighting, digital effects, full color range."
        elif style_category == "psychedelic": category_instructions = "*   **Psychedelic Focus:** Vibrant/neon colors, swirling/fractal patterns, glowing/morphing effects, trippy/surreal mood."
        elif style_category == "surrealism": category_instructions = "*   **Surrealism Focus:** Dreamlike/bizarre concepts, symbolic colors/composition, mysterious/uncanny mood."
        elif style_category == "fantasy": category_instructions = "*   **Fantasy Focus:** Mystical environments, magical lighting, rich/otherworldly colors, epic/adventurous mood."
        elif style_category == "cyberpunk": category_instructions = "*   **Cyberpunk Focus:** Neon cities, high contrast lighting, dark/saturated colors, gritty/futuristic mood." # Could merge with sci-fi?
        elif style_category == "game_style": category_instructions = "*   **Game Style Focus:** Game engine look (Unreal/Unity), game lighting/effects, game camera views, polished."
        elif style_category == "photographic":
            is_film = any(x in base_style.lower() for x in ["film", "kodak", "analog"])
            camera = "Film Camera" if is_film else "Digital Camera (e.g., Canon EOS R5)"
            category_instructions = f"*   **Photographic Focus:** Suggest {camera}, appropriate lens, natural/studio light, {'film grain/analog look' if is_film else 'sharp/realistic'}."
        elif style_category.startswith("illustration"): category_instructions = "*   **Illustration Focus:** Style-specific linework/colors (Pixar: vibrant, Disney: expressive, Anime: cel-shaded, Vintage: rubber hose), stylized lighting/perspective."
        elif style_category == "traditional_painting_drawing": category_instructions = "*   **Traditional Medium:** Emphasize texture/brushwork, natural/atmospheric light, consider historical movements, traditional palettes."
        elif style_category == "abstract_conceptual": category_instructions = "*   **Abstract Focus:** Non-representational form, expressive color, unconventional composition, modern art influences."
        else: category_instructions = "*   **General Guidance:** Choose settings matching the style, mood, and technical parameters."


        # Get the appropriate template for this style category
        # Ensure get_template_for_category handles the new categories or falls back gracefully
        template = get_template_for_category(style_category)
        if not template:
             logging.error(f"No template found for category: {style_category}. Using default.")
             # Define a default template structure here if needed
             template = { # Example default
                 "preset_name": "[GENERATED_NAME]",
                 "styles": [base_style],
                 "moods": ["[CHOOSE_ONE: peaceful, serene, energetic, dramatic, mysterious, romantic, playful, dreamy]"],
                 "composition": { "aspect_ratio": "16:9" },
                 "imagen_settings": { "negative_prompt": "[GENERATE_NEGATIVE_PROMPT_BASED_ON_STYLE]" }
             }

        # Build the complete prompt
        prompt = f"""
        Generate settings for a wallpaper with style: "{base_style}"

        Instructions:
        1. Create a unique `preset_name` inspired by the style "{base_style}" and category "{style_category}". Be creative and descriptive (e.g., "Neon Dreams Cyberpunk", "Minimalist Serenity Geo", "Watercolor Sketch Whimsy").
        2. Create a `description` field that describes the preset as a whole, including mood, style, and key settings. The description should summarize the preset, not just the style.
        3. Choose EXACTLY ONE mood from this list: peaceful, serene, energetic, dramatic, mysterious, romantic, playful, dreamy. **Choose a mood that is appropriate for the style "{base_style}".** Place it as a single string value in the "moods" list.
        4. Follow the specific guidance for the detected category "{style_category}":
           {instruction_header}
           {category_instructions}
        5. For the `negative_prompt` field in `imagen_settings`, generate a concise (10-20 words) negative prompt that specifically AVOIDS elements conflicting with the style "{base_style}" (category: "{style_category}"). Tailor the negative prompt to exclude styles, textures, or features that clash or reduce coherence. For example:
           - Photorealistic: avoid "cartoon, drawing, sketch, unrealistic"
           - Minimalist: avoid "cluttered, detailed, messy, complex"
           - Watercolor: avoid "photorealistic, 3D render, sharp focus, hyperdetailed"
           - Cyberpunk: avoid "pastel colors, soft lighting, natural landscapes"
           - Fantasy: avoid "modern technology, urban scenes, dull colors"
           - Surrealism: avoid "realistic, photographic, literal"
           - Game Style: avoid "blurry, low resolution, photo"
           - Illustration: avoid "photorealistic, 3D render, grainy"
           Replace the placeholder "[GENERATE_NEGATIVE_PROMPT_BASED_ON_STYLE]" with this tailored negative prompt.
        6. For the `style_negative_prompt` field in `imagen_settings`, generate a concise (10-20 words) negative prompt that specifically AVOIDS elements conflicting with the *overall* style "{base_style}". This should be a more general negative prompt based on the core style, not just the category.
           Replace the placeholder "[GENERATE_STYLE_SPECIFIC_NEGATIVE_PROMPT]" with this tailored negative prompt.
        7. Ensure the `composition.aspect_ratio` is exactly "16:9".
        8. Fill in any other relevant fields from the template below based on the style and instructions.
        9. Output ONLY the valid JSON object, starting with {{ and ending with }}, matching this structure exactly:

        ```json
        {json.dumps(template, indent=4)}
        ```
        """

        # Generate settings with retries and fallback
        for attempt in range(3):
            print_info(f"Generating settings (Attempt {attempt + 1}/3)...")
            try:
                # Use safety_settings to reduce refusals if applicable
                safety_settings = {
                    # Adjust levels if needed, e.g., BLOCK_MEDIUM_AND_ABOVE or BLOCK_LOW_AND_ABOVE
                    # Use BLOCK_NONE carefully, understand risks.
                    genai_types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai_types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                    genai_types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai_types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                    genai_types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai_types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE, # Stricter here maybe
                    genai_types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai_types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                }
                response = model.generate_content(prompt, safety_settings=safety_settings)

                # --- Response Processing ---
                if response and response.candidates and response.candidates[0].content.parts:
                    response_text = response.candidates[0].content.parts[0].text.strip()
                    # Improved JSON extraction
                    json_match = re.search(r'```json\s*({.*?})\s*```|({.*?})', response_text, re.DOTALL)
                    if json_match:
                        json_str = json_match.group(1) or json_match.group(2)
                        try:
                            settings_data = json.loads(json_str)

                            # --- Validation and Refinement ---
                            # 1. Ensure base_style is correctly in styles list
                            if "styles" not in settings_data or not isinstance(settings_data["styles"], list):
                                settings_data["styles"] = [base_style]
                            elif base_style not in settings_data["styles"]:
                                settings_data["styles"].insert(0, base_style) # Add if missing

                            # 2. Ensure moods is a list with one string
                            if "moods" not in settings_data or not isinstance(settings_data["moods"], list) or len(settings_data["moods"]) != 1:
                                # Try to extract mood from prompt or default
                                default_mood = "peaceful" # Or another sensible default
                                settings_data["moods"] = [default_mood]
                                logging.warning(f"Mood formatting incorrect, defaulting to {default_mood}")
                            else:
                                # Ensure the mood is valid
                                valid_moods = ["peaceful", "serene", "energetic", "dramatic", "mysterious", "romantic", "playful", "dreamy"]
                                if settings_data["moods"][0].lower() not in valid_moods:
                                     logging.warning(f"Invalid mood '{settings_data['moods'][0]}', defaulting.")
                                     settings_data["moods"] = [random.choice(valid_moods)] # Pick a random valid one

                            # 3. Check preset_name
                            if not settings_data.get("preset_name") or "[GENERATED_NAME]" in settings_data.get("preset_name", ""):
                                settings_data["preset_name"] = f"{base_style.replace('_',' ').title()} Preset {random.randint(10,99)}"
                                logging.warning("Preset name invalid, generating default.")

                            # 4. Check negative prompt placeholder
                            neg_prompt = settings_data.get("imagen_settings", {}).get("negative_prompt", "")
                            if not neg_prompt or "[GENERATE_NEGATIVE_PROMPT_BASED_ON_STYLE]" in neg_prompt:
                                # Generate a simple default based on category
                                default_negatives = {
                                    "photographic": "drawing, illustration, cartoon, sketch, unrealistic",
                                    "minimalist": "cluttered, detailed, complex, messy, intricate",
                                    "watercolor": "photorealistic, 3d render, sharp focus, hyperdetailed",
                                    "default": "ugly, deformed, blurry, bad anatomy, text, words, signature"
                                }
                                settings_data.setdefault("imagen_settings", {})["negative_prompt"] = default_negatives.get(style_category, default_negatives["default"])
                                logging.warning("Negative prompt placeholder found, generating default.")

                            # 5. Check style negative prompt placeholder
                            style_neg_prompt = settings_data.get("imagen_settings", {}).get("style_negative_prompt", "")
                            if not style_neg_prompt or "[GENERATE_STYLE_SPECIFIC_NEGATIVE_PROMPT]" in style_neg_prompt:
                                # Generate a simple default based on the base style
                                settings_data.setdefault("imagen_settings", {})["style_negative_prompt"] = f"avoid elements conflicting with {base_style}"
                                logging.warning("Style negative prompt placeholder found, generating default.")


                            # 6. Ensure aspect ratio
                            settings_data.setdefault("composition", {})["aspect_ratio"] = "16:9"


                            # --- Final Preset Construction ---
                            preset_data = {
                                "preset_name": settings_data.get("preset_name"),
                                "styles": settings_data.get("styles"),
                                "moods": settings_data.get("moods"),
                                # Merge the rest of the generated settings, potentially excluding duplicates
                                **{k: v for k, v in settings_data.items() if k not in ["preset_name", "styles", "moods"]}
                            }

                            # Check uniqueness and save
                            if is_preset_unique(preset_data):
                                # Preview the preset before saving
                                preview_text = json.dumps(preset_data, indent=4)
                                if UI_UTILS_AVAILABLE:
                                    print_section("Preview of Generated Preset")
                                    print_info(preview_text)
                                    confirm = input("Save this preset? (y/n): ").strip().lower()
                                else:
                                    print("\n--- Preview of Generated Preset ---")
                                    print(preview_text)
                                    confirm = input("Save this preset? (y/n): ").strip().lower()

                                if confirm not in ['y', 'yes']:
                                    print_warning("Preset saving cancelled by user.")
                                    return None

                                save_preset_to_cache(preset_data)
                                # Save the full preset to a file
                                preset_filename = f"{settings_data['preset_name'].replace(' ', '_').lower()}.json"
                                preset_path = os.path.join(PRESETS_DIR, preset_filename)
                                os.makedirs(PRESETS_DIR, exist_ok=True)
                                with open(preset_path, 'w') as f:
                                    json.dump(preset_data, f, indent=4)
                                print_success(f"Generated unique preset: '{settings_data['preset_name']}'")
                                print_success(f"Saved to: {preset_path}")
                                return preset_path # Return the path to the saved file
                            else:
                                print_warning("Generated preset is too similar to a previous one. Retrying...")
                                # Continue to the next attempt in the loop

                        except json.JSONDecodeError as json_err:
                            logging.error(f"Failed to parse JSON response: {json_err}\nResponse text:\n{response_text}")
                            print_error("AI response was not valid JSON.")
                            # Continue to the next attempt

                    else:
                        logging.warning(f"Could not extract JSON from response.\nResponse text:\n{response_text}")
                        print_warning("AI response format was unexpected.")
                        # Continue to the next attempt
                elif response and response.prompt_feedback:
                     # Handle blocked content based on prompt_feedback
                     block_reason = response.prompt_feedback.block_reason
                     logging.warning(f"Generation blocked. Reason: {block_reason}")
                     print_warning(f"Generation blocked due to safety settings (Reason: {block_reason}). Trying again might help, or adjust the style prompt.")
                     # Optionally, could modify prompt slightly and retry here
                     # Continue to next attempt

                else:
                    # Handle other potential issues like empty response
                    logging.warning(f"Received no valid response text or candidates. Full response: {response}")
                    print_warning("AI returned an empty or invalid response.")
                    # Continue to next attempt


            except genai_types.StopCandidateException as stop_err:
                 logging.warning(f"Generation stopped unexpectedly: {stop_err}")
                 print_warning(f"Generation stopped: {stop_err}. Retrying...")
                 time.sleep(2) # Wait before retrying
            except Exception as api_err:
                # Handle specific API errors like rate limits, authentication
                err_str = str(api_err).lower()
                if "rate limit" in err_str or "429" in err_str:
                    logging.warning(f"Rate limit hit: {api_err}. Switching model or waiting...")
                    print_warning("Rate limit reached. Waiting before retry...")
                    time.sleep(5 + attempt * 5) # Exponential backoff
                    # Optionally switch model if not already Flash
                    if not using_flash and model.model_name != preferred_model:
                         try:
                             model = genai.GenerativeModel(preferred_model)
                             using_flash = True
                             print_info(f"Switched to Gemini model: {preferred_model}...")
                         except Exception as switch_err:
                              logging.error(f"Failed to switch to {preferred_model}: {switch_err}")
                              # Stick with the current model and hope the wait helps
                    # Continue to next attempt
                elif "api key not valid" in err_str or "authentication" in err_str:
                     logging.error(f"Authentication error: {api_err}")
                     print_error("Authentication error. Check your GEMINI_API_KEY.")
                     return False # Fatal error, don't retry
                else:
                    # General API error
                    logging.error(f"Generation failed with API error: {api_err}")
                    print_error(f"Failed to generate settings: {api_err}")
                    # Continue to next attempt


        # If all attempts failed
        print_error("Failed to generate a unique preset after multiple attempts.")
        return False

    except Exception as e:
        logging.exception("An unexpected error occurred during preset generation:")
        print_error(f"An unexpected error occurred: {e}")
        return False


def main():
    """Main function to handle user interaction."""
    parser = argparse.ArgumentParser(description="Generate AI wallpaper presets.")
    parser.add_argument("--style", type=str, help="Specify a base style to generate a preset for directly.")
    args = parser.parse_args()

    if not SETTINGS_AVAILABLE:
        print_warning("Wallpaper settings not fully available. Using defaults.")
    if not UI_UTILS_AVAILABLE:
        print_warning("UI Utils not available. Using basic console output.")

    user_prefs = get_preferences() # Load current preferences if needed

    if args.style:
        print_info(f"Generating preset directly for style: {args.style}")
        result = generate_ai_preset(user_prefs, base_style_override=args.style)
        if isinstance(result, str): # Check if it returned a file path
             print_success(f"Preset generated successfully: {result}")
        elif result is False:
             print_error("Preset generation failed.")
        # No need for menu if style is provided via command line
    else:
        # Interactive Menu (kept simple as an example)
        while True:
            print_section("AI Preset Generator")
            print_option("1", "Generate New AI Preset")
            print_option("q", "Quit")
            choice = get_validated_input("Select option (1, q)", ["1", "q"])

            if choice == '1':
                result = generate_ai_preset(user_prefs)
                if isinstance(result, str):
                     print_success(f"Preset generated successfully: {result}")
                elif result is False:
                     print_error("Preset generation failed.")
                # Pause or prompt user before showing menu again
                input("\nPress Enter to continue...")
            elif choice == 'q':
                print_info("Exiting AI Preset Generator.")
                break

if __name__ == "__main__":
    main()
