#!/usr/bin/env python3
import sys
import os

"""
AI Preset Generator for the AI Wallpaper Generator project.

This script serves as the primary engine for generating AI-driven wallpaper presets. 
It utilizes Google's Gemini AI to interpret style inputs and produce coherent, 
creative preset configurations based on a comprehensive style catalog and 
template system.

Key functionalities include:
- Parsing command-line arguments for direct preset generation or application.
- Interactive menu for generating new presets.
- Determining a base style, either from user input or via an AI style generator.
- Categorizing the base style using `style_category_catalog.py`.
- Fetching appropriate base templates via `style_templates.py`.
- Constructing detailed prompts for the Gemini AI.
- Interacting with the Gemini API (managed by `gemini_config_preset.py`).
- Parsing, validating, and refining AI-generated JSON preset data.
- Ensuring preset uniqueness through a caching mechanism.
- Saving valid presets to disk and a database (via `preset_management`).
- Robust error handling and fallbacks for external dependencies.
"""

import json
import logging
import random
import hashlib
import re
import time
import argparse
from typing import Dict, Any, List, Optional, Union, Set # Added Set

# --- Gemini API Import ---
try:
    import google.generativeai as genai
    import google.generativeai.types as genai_types
    GEMINI_AVAILABLE = True
except ImportError as e:
    print(f"ERROR: Gemini API (google-generativeai) not installed. Please install it: pip install google-generativeai")
    print(f"Details: {e}")
    GEMINI_AVAILABLE = False
    # Define dummy genai and types for graceful failure
    class DummyGenAI:
        def configure(self, *args, **kwargs): pass
        def GenerativeModel(self, *args, **kwargs): return DummyGenerativeModel()
    class DummyGenerativeModel:
        def generate_content(self, *args, **kwargs):
            print("WARNING: Gemini AI not available. Returning dummy response.")
            return None
    class DummyGenAITypes:
        HarmCategory = type('HarmCategory', (object,), {
            'HARM_CATEGORY_HATE_SPEECH': 'HARM_CATEGORY_HATE_SPEECH',
            'HARM_CATEGORY_HARASSMENT': 'HARM_CATEGORY_HARASSMENT',
            'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
            'HARM_CATEGORY_DANGEROUS_CONTENT': 'HARM_CATEGORY_DANGEROUS_CONTENT',
        })
        HarmBlockThreshold = type('HarmBlockThreshold', (object,), {
            'BLOCK_ONLY_HIGH': 'BLOCK_ONLY_HIGH',
            'BLOCK_MEDIUM_AND_ABOVE': 'BLOCK_MEDIUM_AND_ABOVE',
            'BLOCK_LOW_AND_ABOVE': 'BLOCK_LOW_AND_ABOVE',
            'BLOCK_NONE': 'BLOCK_NONE',
        })
        StopCandidateException = type('StopCandidateException', (Exception,), {})

    genai = DummyGenAI()
    genai_types = DummyGenAITypes()


# --- Local Application Imports & Fallbacks ---

# Define fallbacks first
def _print_section_fallback(x): print(f"\n--- {x} ---")
def _print_option_fallback(k, v): print(f"  {k}. {v}")
def _print_info_fallback(x): print(x)
def _print_error_fallback(x): print(f"ERROR: {x}")
def _print_success_fallback(x): print(f"SUCCESS: {x}")
def _print_warning_fallback(x): print(f"WARNING: {x}")

def _get_validated_input_fallback(prompt_msg: str, valid_options: List[str]) -> str:
     while True:
         val = input(f"{prompt_msg} {valid_options}: ").strip().lower()
         is_valid = False
         if isinstance(valid_options, list): is_valid = val in [str(choice).lower() for choice in valid_options]
         if is_valid: return val
         else: _print_error_fallback(f"Invalid input. Please enter one of {valid_options}")

class UserPreferencesPlaceholder: pass
def initialize_settings_fallback(): return UserPreferencesPlaceholder()
def get_preferences_fallback(): return initialize_settings_fallback()
def generate_random_style_fallback(style_type="default"): return {"name": "Random Fallback Style"}
def initialize_style_gemini_fallback(api_key): pass
def deep_update_fallback(target, source): target.update(source); return target
# Fallback for the new save_preset function
def save_preset_fallback(preset_data: Dict[str, Any], preset_name_base: str) -> bool:
    _print_warning_fallback(f"save_preset function not found. Simulating save for '{preset_name_base}'.")
    # Simulate basic file save from placeholder
    try:
        preset_filename = f"{preset_name_base}.json"
        preset_path = os.path.join(PRESETS_DIR, preset_filename)
        with open(preset_path, 'w') as f:
            json.dump(preset_data, f, indent=4)
        logging.info(f"(Fallback) Preset saved to file: {preset_path}")
        return True
    except Exception as e:
        logging.error(f"(Fallback) Error saving preset file '{preset_path}': {e}")
        return False


# Attempt actual imports, falling back to above definitions
try:
    from wall_gen.settings_modules.user_preferences import UserPreferences
    from wall_gen.settings_modules.settings_manager import get_preferences, initialize_settings
    SETTINGS_AVAILABLE = True
except ImportError:
    SETTINGS_AVAILABLE = False
    UserPreferences = UserPreferencesPlaceholder
    get_preferences = get_preferences_fallback
    initialize_settings = initialize_settings_fallback
    _print_warning_fallback("wall_gen.settings_modules modules not found. Using placeholder UserPreferences.")

try:
    from wall_gen.ui_utils import get_validated_input, print_section, print_option, print_info, print_error, print_success, print_warning, clear_screen, print_header
    UI_UTILS_AVAILABLE = True
except ImportError:
    UI_UTILS_AVAILABLE = False
    get_validated_input = _get_validated_input_fallback
    print_section = _print_section_fallback
    print_option = _print_option_fallback
    print_info = _print_info_fallback
    print_error = _print_error_fallback
    print_success = _print_success_fallback
    print_warning = _print_warning_fallback
    _print_warning_fallback("wall_gen.ui_utils not found. Using basic print/input for UI.")

try:
    from wall_gen.ai_style_generator import generate_random_style, initialize_gemini as initialize_style_gemini
    AI_STYLE_GEN_AVAILABLE = True
except ImportError:
    AI_STYLE_GEN_AVAILABLE = False
    generate_random_style = generate_random_style_fallback
    initialize_style_gemini = initialize_style_gemini_fallback
    _print_warning_fallback("Could not import ai_style_generator. AI style generation feature disabled.")

try:
    from wall_gen.file_utils import deep_update
    FILE_UTILS_AVAILABLE = True
except ImportError:
    FILE_UTILS_AVAILABLE = False

    def deep_update(target: dict, source: dict) -> dict:
        """
        Recursively update target dict with source dict.
        """
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                deep_update(target[key], value)
            else:
                target[key] = value
        return target

    _print_warning_fallback("wall_gen.file_utils not found. Using custom recursive deep_update.")

try:
    from wall_gen.config import STYLE_CATEGORIES # Configuration moved to wall_gen
    CONFIG_STYLE_CATEGORIES_AVAILABLE = True
except ImportError:
    CONFIG_STYLE_CATEGORIES_AVAILABLE = False
    _print_warning_fallback("Could not import STYLE_CATEGORIES from wall_gen.config. Using empty dictionary.")
    STYLE_CATEGORIES = {} # Provide default empty dict

try:
    # Import from the restored catalog
    from .style_category_catalog import (
        hybrid_styles,
        hybrid_categories_keywords,
        categories_keywords,
        preferred_order,
        all_categories as catalog_all_categories,
        instructions_for_category
    )
    # Import the CONSOLIDATED template generator from style_templates.py
    from .style_templates import get_template_for_category
    CATALOG_AND_TEMPLATES_AVAILABLE = True
    # Import for new Gemini preset configuration
    from .gemini_config_preset import (
        initialize_preset_gemini,
        get_selected_preset_model,
        set_selected_preset_model,
        AVAILABLE_PRESET_MODELS,
        DEFAULT_PRESET_MODEL,
        is_preset_gemini_initialized,
        get_preset_last_error
    )
except ImportError as e:
    _print_error_fallback(f"FATAL: Could not import from ai_prest_gen submodules (style_category_catalog, style_templates): {e}")
    _print_error_fallback("Please ensure these files exist in an 'ai_prest_gen' subdirectory and it's a package (contains __init__.py).")
    CATALOG_AND_TEMPLATES_AVAILABLE = False
    # Define fallbacks for catalog data if not available
    hybrid_styles = {}
    hybrid_categories_keywords = {}
    categories_keywords = {}
    preferred_order = ["default", "unknown"]
    catalog_all_categories = ["default", "unknown"]
    def instructions_for_category(cat, style): return "No specific instructions available."
    def get_template_for_category(cat): return {}

# --- Import save_preset from preset_management ---
try:
    # Attempt to import the specific save_preset function
    from wall_gen.settings_modules.preset_management import save_preset
    SAVE_PRESET_AVAILABLE = True
except ImportError:
    SAVE_PRESET_AVAILABLE = False
    # Assign the fallback function if the import fails
    save_preset = save_preset_fallback
    _print_warning_fallback("wall_gen.settings_modules.preset_management.save_preset not found. Using fallback save.")


# --- Configuration ---
# --- Configuration ---
LOG_FILE_NAME = "ai_preset_generator.log"
PRESETS_CACHE_FILE = "generated_presets_cache.json"
PRESETS_DIR = "presets"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(LOG_FILE_NAME, mode='a')]
)
# PRESETS_CACHE_FILE = "generated_presets_cache.json" # Defined above
# PRESETS_DIR = "presets" # Defined above
os.makedirs(PRESETS_DIR, exist_ok=True)

# gemini_initialized flag is now managed by gemini_config_preset for this script's context
# gemini_initialized = False 

# --- Helper Functions ---

# get_gemini_api_key is now handled by gemini_config_preset.py
# def get_gemini_api_key() -> Optional[str]:
#     """Retrieve the Gemini API key from environment variable."""
#     api_key = os.environ.get("GEMINI_API_KEY")
#     if not api_key:
#         logging.warning("GEMINI_API_KEY environment variable not set.")
#         print_warning("GEMINI_API_KEY environment variable not set.")
#     return api_key

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

# --- Style Categorization (Restored Logic) ---

def normalize_style_name(style_name: str) -> str:
    """Normalizes a style name for consistent matching (Helper)."""
    name = str(style_name).lower()
    # Replace underscores and hyphens with spaces before further processing
    name = name.replace('_', ' ').replace('-', ' ')
    name = name.replace('colour', 'color')
    name = name.replace('water color', 'watercolor')
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def categorize_style(style_name_input: Union[str, Dict]) -> str:
    """
    Attempt to categorize a style name based on the restored catalog logic.
    """
    if not CATALOG_AND_TEMPLATES_AVAILABLE:
        print_warning("Style catalog/templates not available, categorization limited.")
        return "unknown"

    if isinstance(style_name_input, dict):
        style_name_str = style_name_input.get('name', '')
    else:
        style_name_str = str(style_name_input)

    normalized_style = normalize_style_name(style_name_str)
    if not normalized_style:
        return "unknown"

    style_lower = normalized_style

    # Split by all common delimiters *and* whitespace to get individual tokens
    tokens = [t.strip() for t in re.split(r'[,+/&|\s]+', style_lower) if t.strip()]
    tokens_set = frozenset(tokens)

    # 1. Token-based Hybrid Style Mapping (from restored catalog)
    for hybrid_set, hybrid_cat in hybrid_styles.items():
        if hybrid_set.issubset(tokens_set):
            logging.info(f"[Restored Logic] Matched token-based hybrid: '{hybrid_cat}' for '{style_name_str}'")
            return hybrid_cat

    # 2. Keyword-based Hybrid Category Definitions (from restored catalog)
    for category, keyword_list in hybrid_categories_keywords.items():
        for term in keyword_list:
            if re.search(r'\b' + re.escape(normalize_style_name(term)) + r'\b', style_lower):
                logging.info(f"[Restored Logic] Matched keyword-based hybrid: '{category}' using term '{term}' for '{style_name_str}'")
                return category

    # 3. General/Single-Term Category Keywords (from restored catalog)
    matched_categories: Set[str] = set()
    for category, keyword_list in categories_keywords.items():
        for term in keyword_list:
            if re.search(r'\b' + re.escape(normalize_style_name(term)) + r'\b', style_lower):
                mapped_category = category
                # Apply specific mappings if needed (restoring user's logic)
                if category == "3d_render": mapped_category = "3d_render"
                elif category in ["oil_painting", "watercolor", "pastel", "charcoal"]: pass
                elif category == "line_art": mapped_category = "line_art"
                elif category in ["pencil_sketch", "ink_drawing"]: mapped_category = "drawing"
                elif category.startswith("illustration"): pass
                elif category == "digital_art": mapped_category = "digital_art"
                elif category == "game_style": mapped_category = "game_style"
                elif category in ["photographic", "cinematic", "realism"]: pass
                elif category in ["abstract", "abstract_conceptual"]: mapped_category = "abstract_conceptual"
                elif category in ["material_sculptural", "sculpture"]: mapped_category = "material_sculptural"
                elif category in ["fantasy", "sci_fi"]: pass
                elif category == "traditional_painting_drawing": mapped_category = "traditional_painting_drawing"
                logging.info(f"[Restored Logic] Matched single-term: '{mapped_category}' using term '{term}' for '{style_name_str}'")
                matched_categories.add(mapped_category)

    # 4. Prioritize and Return (using restored catalog's preferred_order)
    if matched_categories:
        # Define portrait categories locally just for logging/understanding, not needed for function selection anymore
        portrait_categories = {
            "photographic_portrait", "traditional_portrait", "futuristic_portrait",
            "illustration_portrait", "pop_portrait", "cyberpunk_portrait", "fantasy_portrait",
            "environmental_portrait", "caricature_portrait", "conceptual_portrait",
            "fashion_portrait", "selfie_portrait"
        }
        # Check general preferred order
        for pref in preferred_order:
            if pref in matched_categories:
                logging.info(f"[Restored Logic] Prioritized match: '{pref}' for '{style_name_str}'")
                return pref
        # Fallback if no preferred match found
        fallback_match = sorted(list(matched_categories))[0]
        logging.info(f"[Restored Logic] Fallback alphabetical match: '{fallback_match}' for '{style_name_str}'")
        return fallback_match

    # Explicit final fallback for single-term categories (like 'charcoal', 'pastel', etc.)
    # If the normalized style directly matches a categories_keywords key, use it.
    single_term = style_lower.strip()
    if single_term in categories_keywords:
        logging.info(f"[Restored Logic] Final single-term direct match: '{single_term}' for '{style_name_str}'")
        return single_term

    logging.warning(f"[Restored Logic] Could not categorize style: '{style_name_str}'. Falling back to 'unknown'.")
    return "unknown"


# --- AI Preset Generation (using consolidated templates) ---

# Helper function to get base style
def _get_base_style_for_preset(user_prefs: Any, base_style_override: Optional[str]) -> Optional[str]:
    """
    Determines the base style for preset generation.

    This function either uses a `base_style_override` if provided, or prompts
    the user to choose between entering a custom style or generating one using
    the AI style generator (if available).

    Args:
        user_prefs: The user preferences object (currently unused in this helper but kept for potential future use).
        base_style_override: An optional string to directly use as the base style.

    Returns:
        Optional[str]: The determined base style string, or None if the user
                       cancels, provides no input, or if AI style generation fails.
    """
    if base_style_override:
        print_info(f"Using provided style: {base_style_override}")
        return base_style_override

    print_section("Choose Style Source for Preset")
    print_option("1", "Enter Custom Style")
    if AI_STYLE_GEN_AVAILABLE:
        print_option("2", "Generate AI Style")
    print_option("b", "Back")

    valid_choices = ["1", "b"]
    if AI_STYLE_GEN_AVAILABLE:
        valid_choices.append("2")

    choice = get_validated_input(
        "Select option:",
        valid_choices,
        help_context_id="AI_PRESET_STYLE_SOURCE_CHOICE"
    )

    if choice == "_HELP_SHOWN_":
        print_info("Help shown. Returning to AI Preset Generator menu.")
        return None
    if choice == "b":
        print_info("Preset generation cancelled.")
        return None
    elif choice == "1":
        base_style = input("Enter your custom style: ").strip()
        if not base_style:
            print_error("No style entered.")
            return None
        return base_style
    elif choice == "2" and AI_STYLE_GEN_AVAILABLE:
        print_info("Attempting to generate AI style (this may take a moment)...")
        if not initialize_style_gemini(None):
            print_error("Failed to initialize Gemini for AI style generation (via wall_gen.ai_style_generator).")
            return None
        style_obj = generate_random_style(style_type="detailed")
        if not style_obj or not isinstance(style_obj, dict):
            print_error("Failed to generate AI style object.")
            return None
        base_style = style_obj.get('name')
        if not base_style:
            print_error("AI generated style object lacked a 'name'.")
            return None
        print_info(f"AI Generated Style: {base_style} (Description: {style_obj.get('description', 'N/A')})")
        return base_style
    return None

# Helper function to build the prompt
def _build_preset_generation_prompt(base_style_name: str, style_category: str, category_instructions: str, template: Dict[str, Any]) -> str:
    """
    Constructs the detailed prompt string for the Gemini AI to generate preset settings.

    The prompt includes:
    - The base style name and its detected category.
    - Specific instructions tailored to the style category.
    - Critical instructions on JSON output format and key inclusion.
    - A JSON template structure that the AI should fill.

    Args:
        base_style_name: The name of the base style.
        style_category: The detected category for the base style.
        category_instructions: Specific AI guidance for the detected category.
        template: The base JSON template for the style category.

    Returns:
        str: The fully constructed prompt string for the Gemini API.
    """
    instruction_header = f"Select settings that work well with \"{base_style_name}\" (category: {style_category}):"
    
    # Ensure 'styles' key exists and is a list with the base_style_name
    # This modification should ideally happen before this function if template is pre-processed
    # but we ensure it here for robustness.
    template_for_prompt = template.copy() # Avoid modifying the original template dict
    template_for_prompt["styles"] = [base_style_name]
    template_for_prompt.setdefault("description", f"AI preset for {base_style_name}.")
    template_for_prompt.setdefault("aspect_ratio", "16:9")


    prompt = f"""
    Generate settings for a wallpaper with style: "{base_style_name}"

    Instructions:
    1. Create a unique `preset_name` inspired by the style "{base_style_name}" and category "{style_category}".
    2. Create a `description` field describing the preset.
    3. Choose ONE mood for the "moods" list.
    4. Follow the specific guidance for the detected category "{style_category}":
       {instruction_header}
       {category_instructions}
    5. For `negative_prompt`, generate text avoiding elements conflicting with the *category* "{style_category}".
    6. For `style_negative_prompt`, generate text avoiding elements conflicting with the *base style* "{base_style_name}".
    7. Ensure `aspect_ratio` is "16:9".
    8. Fill in ALL fields from the template below with specific, fitting values. Do NOT leave default template values unchanged unless they are truly appropriate. Do NOT use placeholders.
    9. **CRITICAL:** Ensure the output JSON includes ALL top-level keys (`preset_name`, `moods`, `aspect_ratio`, `description`, `styles`, `imagen_settings`) and ALL nested dictionaries (`style_settings`, `lighting_settings`, `composition_settings`, `color_settings`, `detail_settings`, `environment_settings`, `quality_settings`, `camera_settings` if present in the template, etc.) exactly as they appear in the template structure provided below. Do not omit any sections.
    10. Generate detailed and dynamic `camera_settings` including parameters such as aperture, shutter speed, ISO, focal length, lens type, camera model, and any other relevant photographic settings. Do NOT reuse static or default camera settings from the template; instead, create unique and contextually appropriate camera settings for this preset.
    11. Output ONLY the valid JSON object, starting with `{{` and ending with `}}`. No ```json.

    JSON Template to Fill:
    ```json
    {json.dumps(template_for_prompt, indent=4)}
    ```
    """
    return prompt

# Helper function to process Gemini response
def _process_gemini_preset_response(json_str: str, base_style: str, template: Dict[str, Any], style_category: str) -> Optional[Dict[str, Any]]:
    """
    Parses the JSON string from Gemini, validates it, and refines the settings.

    This function merges the AI-generated settings with the base template,
    ensures critical fields are present (e.g., preset_name, moods, aspect_ratio),
    validates negative prompts, and handles style-specific adjustments like
    removing camera settings for traditional art styles.

    Args:
        json_str: The JSON string received from the Gemini API.
        base_style: The name of the base style.
        template: The base template used for this style category.
        style_category: The detected category of the style.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the final, processed
                                   preset settings, or None if parsing or
                                   validation fails.
    """
    try:
        generated_settings = json.loads(json_str)
        final_preset = {"styles": [base_style]} # base_style here is the string name

        final_preset["preset_name"] = generated_settings.get("preset_name", template.get("preset_name", f"{base_style.replace('_',' ').title()} Fallback Preset"))
        
        moods = generated_settings.get("moods", template.get("moods", ["Neutral"]))
        if not isinstance(moods, list) or not moods or not isinstance(moods[0], str):
            final_preset["moods"] = template.get("moods", ["Neutral"])
        else:
            final_preset["moods"] = [moods[0]] # Take only the first mood

        final_preset["description"] = generated_settings.get("description", template.get("description", f"AI preset for {base_style}."))
        final_preset["aspect_ratio"] = "16:9" # Enforce

        # Merge imagen_settings
        ai_imagen = generated_settings.get("imagen_settings")
        template_imagen = template.get("imagen_settings", {})
        import copy
        merged_imagen_settings = copy.deepcopy(template_imagen)

        if isinstance(ai_imagen, dict):
            if 'deep_update' in globals(): # Check if deep_update is available
                deep_update(merged_imagen_settings, ai_imagen)
            else: # Fallback basic update
                merged_imagen_settings.update(ai_imagen)
                logging.warning("deep_update function not found, using basic dict.update for imagen_settings merge.")
        
        # Ensure camera_settings key exists if it was in either template or AI response,
        # but only if camera_settings itself is intended for this style category
        if "camera_settings" in template_imagen or ("camera_settings" in ai_imagen if isinstance(ai_imagen, dict) else False):
            merged_imagen_settings.setdefault("camera_settings", {})
        
        final_preset["imagen_settings"] = merged_imagen_settings
        
        # Validate/fallback negative prompts
        neg_prompt = final_preset["imagen_settings"].get("negative_prompt", "")
        if not neg_prompt or len(neg_prompt) < 5:
            final_preset["imagen_settings"]["negative_prompt"] = template_imagen.get("negative_prompt", "low quality, blurry")
        
        style_neg_prompt = final_preset["imagen_settings"].get("style_negative_prompt", "")
        if not style_neg_prompt or len(style_neg_prompt) < 5:
            final_preset["imagen_settings"]["style_negative_prompt"] = template_imagen.get("style_negative_prompt", "clashing styles")

        # Ensure all keys from the original template are present
        for key, t_value in template.items():
            if key not in final_preset and key != "styles": # 'styles' is already handled
                final_preset[key] = generated_settings.get(key, t_value)
        
        # Remove camera_settings for traditional art styles
        traditional_categories = [
            "oil_painting", "watercolor", "pastel", "acrylic_painting",
            "charcoal", "pencil_sketch", "ink_drawing", "drawing"
        ]
        if style_category in traditional_categories:
            if "camera_settings" in final_preset.get("imagen_settings", {}):
                del final_preset["imagen_settings"]["camera_settings"]
        
        return final_preset
    except json.JSONDecodeError as json_err:
        logging.error(f"Failed to parse JSON response: {json_err}\nResponse text was:\n{json_str}")
        print_error(f"AI response was not valid JSON.")
        return None

# Helper function to save preset
def _save_generated_preset(final_preset: Dict[str, Any], auto_save_flag: bool) -> Union[str, bool, None]:
    """
    Handles the saving process for a generated preset.

    This includes:
    - Checking if the preset is unique against a cache.
    - Displaying a preview to the user.
    - Asking for user confirmation to save (unless `auto_save_flag` is true).
    - Saving the preset to a cache file to prevent future duplicates.
    - Saving the preset to a JSON file in the presets directory and to the database
      (via the imported `save_preset` function).

    Args:
        final_preset: The dictionary containing the complete preset data.
        auto_save_flag: Boolean indicating if the preset should be saved without user confirmation.

    Returns:
        Union[str, bool, None]: 
            - The base name of the saved preset file (str) on successful save.
            - `False` if the preset was not unique and thus not saved (allowing for a retry).
            - `None` if the user cancelled saving or if the save operation failed.
    """
    if not is_preset_unique(final_preset):
        print_warning("Generated preset is too similar to a previous one.")
        return False # Indicate not unique, to allow retry in the main loop

    preview_text = json.dumps(final_preset, indent=4)
    print_section("Preview of Generated Preset")
    print_info(preview_text)

    confirm_decision = False
    if auto_save_flag:
        confirm_decision = True
        print_info("Auto-saving preset due to --auto-save flag.")
    else:
        confirm_input = get_validated_input(
            "Save this preset? (y/n):",
            ["y", "n", "yes", "no"],
            help_context_id="AI_PRESET_SAVE_CONFIRMATION"
        )
        if confirm_input == "_HELP_SHOWN_":
            print_info("Help shown for save confirmation. Treating as 'no' to save for this attempt.")
            confirm_decision = False # Or could return a specific value to re-prompt save
        else:
            confirm_decision = confirm_input.startswith('y')

    if confirm_decision:
        save_preset_to_cache(final_preset)
        clean_preset_name = re.sub(r'[^\w\s-]', '', final_preset["preset_name"]).strip().replace(' ', '_')
        preset_name_base = f"{clean_preset_name.lower()}_{int(time.time())}"
        
        success = save_preset(final_preset, preset_name_base)
        if success:
            print_success(f"Generated unique preset: '{final_preset['preset_name']}'")
            print_success(f"Saved preset '{preset_name_base}' to presets folder and database")
            return preset_name_base # Return name on success
        else:
            print_error(f"Failed to save preset '{preset_name_base}'")
            return None # Indicate save failure
    else:
        print_warning("Preset saving cancelled by user.")
        return None # Indicate cancelled by user

def generate_ai_preset(user_prefs: Any, base_style_override: Optional[str] = None, auto_save_flag: bool = False) -> Union[str, bool, None]:
    """
    Orchestrates the generation of an AI-driven wallpaper preset.

    This function manages the entire workflow:
    1. Initializes the Gemini API for preset generation if not already done.
    2. Determines the base style (either from override, user input, or AI generation).
    3. Categorizes the style and fetches the appropriate template and AI instructions.
    4. Constructs a detailed prompt for the Gemini AI.
    5. Calls the Gemini API to generate preset settings, with a retry mechanism.
    6. Parses, validates, and refines the AI's JSON response.
    7. Handles saving the unique preset (with user confirmation if not auto-saving).

    Args:
        user_prefs: The user preferences object, used for model selection.
        base_style_override (Optional[str]): If provided, this style name is used directly,
                                             bypassing user input for style selection.
        auto_save_flag (bool): If True, generated presets are saved without explicit
                               user confirmation.

    Returns:
        Union[str, bool, None]:
            - The base name of the saved preset file (str) if successful.
            - `False` if preset generation failed after all attempts or if a unique
              preset could not be generated.
            - `None` if the user cancelled the process at any stage (e.g., style selection,
              save confirmation).
    """
    if not is_preset_gemini_initialized():
        if not initialize_preset_gemini():
            print_error(f"Failed to initialize Gemini for preset generation: {get_preset_last_error()}")
            print_error("Ensure GEMINI_API_KEY environment variable is set.")
            return False
        logging.info("Gemini API initialized for preset generation via gemini_config_preset.")

    if not CATALOG_AND_TEMPLATES_AVAILABLE:
        print_error("Style catalog/templates are not available. Cannot generate AI preset.")
        return False

    base_style_name = _get_base_style_for_preset(user_prefs, base_style_override)
    if not base_style_name:
        # Error/cancel message already printed by helper
        return None if base_style_name is None else False # Propagate cancel or error

    try:
        # base_style_name is already correctly set by _get_base_style_for_preset
        # If base_style_override was provided, base_style_name will be that value.
        
        if base_style_override and base_style_override == base_style_name:
            # If CLI override is used (or any direct override),
            # normalize it to snake_case for internal use as category key.
            # This ensures it matches keys like "surreal_3d" used in templates/instructions.
            normalized_category_key = base_style_override.lower().replace(' ', '_').replace('-', '_')
            # Consolidate multiple underscores that might result from replacements (e.g., "style - name" -> "style___name")
            normalized_category_key = re.sub(r'_+', '_', normalized_category_key) 

            style_category = normalized_category_key
            # base_style_name holds the original override string (e.g., "surreal 3d") for display/prompting.
            print_info(f"\nUsing CLI/override specified style '{base_style_name}', normalized to category key: '{style_category}' for preset generation.")
        else:
            # For interactive input or AI generated style, categorize it
            print_info(f"\nGenerating settings for style: '{base_style_name}'...")
            style_category = categorize_style(base_style_name)
            print_info(f"(Detected category [Restored Logic]: {style_category})")

        selected_model_name = get_selected_preset_model(user_prefs)
        try:
            model = genai.GenerativeModel(selected_model_name)
            print_info(f"Using selected Gemini model for presets: {selected_model_name}...")
        except Exception as err:
            logging.error(f"Failed to initialize Gemini model '{selected_model_name}': {err}")
            print_error(f"Could not initialize AI model '{selected_model_name}'. Check configuration.")
            return False
        
        category_instructions = instructions_for_category(style_category, base_style_name)
        template = get_template_for_category(style_category)
        print_info(f"Using consolidated template for category: {style_category}")

        if not template or not isinstance(template, dict):
            logging.error(f"No valid template found for category: {style_category}. Using minimal default.")
            template = {
                 "preset_name": f"{base_style_name.replace('_',' ').title()} Default",
                 "styles": [base_style_name], "moods": ["Neutral"],
                 "description": f"Default preset for {base_style_name}.", "aspect_ratio": "16:9",
                 "imagen_settings": {"negative_prompt": "low quality", "style_negative_prompt": "clashing styles"}
            }
        # Note: _build_preset_generation_prompt now handles adding base_style_name to template["styles"]

        prompt = _build_preset_generation_prompt(base_style_name, style_category, category_instructions, template)

        for attempt in range(3):
            print_info(f"Generating settings (Attempt {attempt + 1}/3)...")
            try:
                safety_settings = {
                    genai_types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai_types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    genai_types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai_types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    genai_types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai_types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    genai_types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai_types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                }
                generation_config = genai.types.GenerationConfig(temperature=0.75, top_p=0.95, top_k=40)
                response = model.generate_content(prompt, generation_config=generation_config, safety_settings=safety_settings)

                if response and response.candidates and response.candidates[0].content.parts:
                    response_text = response.candidates[0].content.parts[0].text.strip()
                    json_match = re.search(r'```json\s*(\{.*?\})\s*```|(\{.*?\})', response_text, re.DOTALL)
                    if json_match:
                        json_str = json_match.group(1) or json_match.group(2)
                        final_preset = _process_gemini_preset_response(json_str, base_style_name, template, style_category)
                        
                        if final_preset:
                            save_result = _save_generated_preset(final_preset, auto_save_flag)
                            if save_result is True or isinstance(save_result, str): # Successfully saved (str is preset name)
                                return save_result
                            elif save_result is False: # Not unique, retry
                                if attempt == 2:
                                    print_error("Failed to generate a unique preset after 3 attempts.")
                                    return False
                                time.sleep(1)
                                continue 
                            else: # User cancelled save (save_result is None)
                                return None 
                        else: # JSON parsing/validation failed in helper
                            if attempt == 2: return False
                            time.sleep(1)
                            continue # Retry generation
                    else: # No JSON found
                        logging.warning(f"Could not extract JSON from response (Attempt {attempt+1}). Response: {response_text}")
                        print_warning(f"AI response format was unexpected (Attempt {attempt + 1}).")
                elif response and response.prompt_feedback and response.prompt_feedback.block_reason:
                     block_reason = response.prompt_feedback.block_reason
                     logging.warning(f"Generation blocked by API. Reason: {block_reason} (Attempt {attempt + 1})")
                     print_warning(f"Generation blocked (Reason: {block_reason}). Retrying...")
                else: # Empty or problematic response
                    logging.warning(f"Received no valid response or candidates (Attempt {attempt+1}). Full response: {response}")
                    print_warning(f"AI returned an empty or invalid response (Attempt {attempt + 1}).")

                if attempt == 2: # If loop is about to end after this failed attempt
                    print_error("Failed to generate a valid preset after 3 attempts due to API issues or response format.")
                    return False
                time.sleep(1 if not (response and response.prompt_feedback and response.prompt_feedback.block_reason) else (2 + attempt * 2) ) # Longer sleep if blocked
                continue

            except genai_types.StopCandidateException as stop_err:
                 logging.warning(f"Generation stopped by API (StopCandidateException): {stop_err} (Attempt {attempt + 1})")
                 print_warning(f"Generation stopped by API: {stop_err}. Retrying...")
                 if attempt == 2: return False
                 time.sleep(2 + attempt * 2)
                 continue
            except Exception as api_err: # General API error handling
                err_str = str(api_err).lower()
                if "api key not valid" in err_str or "authentication" in err_str:
                     logging.error(f"Authentication error: {api_err}")
                     print_error("Authentication error. Check your GEMINI_API_KEY.")
                     return False 
                elif "rate limit" in err_str or "429" in err_str or "resource has been exhausted" in err_str:
                    logging.warning(f"Rate limit or resource exhaustion: {api_err}. Waiting... (Attempt {attempt + 1})")
                    print_warning("API rate limit reached or resource exhausted. Waiting before retry...")
                    if attempt == 2: return False
                    time.sleep(10 + attempt * 10)
                    continue
                else:
                    logging.error(f"Generation failed with an unexpected API error: {api_err} (Attempt {attempt + 1})")
                    print_error(f"Failed to generate settings due to an API error: {api_err}")
                    if attempt == 2: return False
                    time.sleep(2)
                    continue
        
        # Fallthrough if all attempts fail
        print_error("Failed to generate a unique and valid preset after all attempts.")
        return False

    except Exception as e: # Catch-all for unexpected errors in the main try block
        logging.exception("An unexpected error occurred during AI preset generation:")
        print_error(f"An unexpected error occurred: {e}")
        return False

# --- Preset Management Placeholder ---
class PresetManagementPlaceholder:
    def _apply_preset_settings(self, settings, replace=True):
        _print_info_fallback(f"Placeholder: Applying preset '{settings.get('preset_name', 'Unknown Preset')}'...")
        return True

try:
    # Import the whole module for applying presets
    from wall_gen.settings_modules import preset_management
    PRESET_MGMT_AVAILABLE = True
    # For user_prefs access in menu
    from wall_gen.settings_modules.settings_manager import save_preferences 

except ImportError:
    PRESET_MGMT_AVAILABLE = False
    preset_management = PresetManagementPlaceholder()
    # _print_warning_fallback("wall_gen.settings_modules.preset_management not found. Preset application will be simulated.")


# --- Main Function ---
def main():
    """Main function to handle user interaction."""
    parser = argparse.ArgumentParser(description="Generate AI wallpaper presets.")
    parser.add_argument("--style", type=str, help="Specify a base style to generate a preset for directly.")
    parser.add_argument("--apply-preset", type=str, help="Apply a preset by name or full path directly from the terminal.")
    parser.add_argument("--auto-save", action="store_true", help="Automatically save generated preset without confirmation.")
    args = parser.parse_args()

    if not GEMINI_AVAILABLE:
        print_error("Gemini AI library is not available. This script requires 'google-generativeai'.")
        print_error("Please install it using: pip install google-generativeai")
        sys.exit(1)
    if not CATALOG_AND_TEMPLATES_AVAILABLE:
        print_error("Essential style catalog/template data is missing. Cannot proceed.")
        sys.exit(1)

    user_prefs = get_preferences()

    if args.apply_preset:
        preset_identifier = args.apply_preset
        print_info(f"Attempting to apply preset: {preset_identifier}")

        if os.path.exists(preset_identifier) and preset_identifier.lower().endswith(".json"):
            preset_path = preset_identifier
        else:
            preset_name = preset_identifier
            if not preset_name.lower().endswith(".json"):
                preset_name += ".json"
            preset_path = os.path.join(PRESETS_DIR, preset_name)

        if not os.path.exists(preset_path):
            print_error(f"Preset file '{preset_path}' not found.")
            sys.exit(1)

        try:
            with open(preset_path, 'r') as f:
                settings_to_apply = json.load(f)
            # Use the (potentially placeholder) preset_management object's method
            success = preset_management._apply_preset_settings(settings_to_apply, replace=True)
            if success:
                print_success(f"Preset from '{os.path.basename(preset_path)}' applied successfully.")
                sys.exit(0)
            else:
                print_error(f"Failed to apply preset from '{os.path.basename(preset_path)}'.")
                sys.exit(1)
        except Exception as e:
            print_error(f"Error loading or applying preset from '{os.path.basename(preset_path)}': {e}")
            sys.exit(1)

    if args.style:
        print_info(f"Generating preset directly for style: {args.style}")
        result = generate_ai_preset(user_prefs, base_style_override=args.style, auto_save_flag=args.auto_save)
        if isinstance(result, str):
             print_success(f"Preset generated and saved: {result}")
        elif result is None:
            print_info("Preset generation was cancelled or no unique preset could be made.")
        else:
             print_error("Preset generation failed.")
    else:
        while True:
            clear_screen()
            print_header("AI Preset Generator") 
            # print_section("AI Preset Generator Menu") # Replaced by print_header
            print_option("1", "Generate New AI Preset")
            # "Advanced Settings" option removed from here, will be in wall_gen's advanced menu
            print_option("q", "Quit")
            choice = get_validated_input(
                prompt="Select option:",
                options=["1", "q"],
                help_context_id="AI_PRESET_GENERATOR_MENU"
            )
            if choice == "_HELP_SHOWN_":
                continue
            if choice == '1':
                result = generate_ai_preset(user_prefs, auto_save_flag=args.auto_save)
                if isinstance(result, str):
                     print_success(f"Preset generated and saved: {result}")
                elif result is None:
                    print_info("Preset generation was cancelled or no unique preset could be made.")
                else:
                     print_error("Preset generation failed.")
                input("\nPress Enter to continue...")
            # elif choice == '2': # Removed advanced_settings_menu call
            #     advanced_settings_menu(user_prefs) 
            elif choice == 'q':
                print_info("Exiting AI Preset Generator.")
                break

# advanced_settings_menu and select_gemini_model_menu functions are removed from this file.
# This functionality will be moved to wall_gen.settings_modules.menu_management.advanced_options_menu.py


if __name__ == "__main__":
    # The sys.path modification has been moved to the top of the script.
    main()
# --- End of ai_preset_generator.py ---
