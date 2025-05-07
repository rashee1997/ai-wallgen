#!/usr/bin/env python3
import sys
import os
# Adjust system path if your project structure requires it.
# Example: If 'ai_prest_gen' is a package and this script is inside it,
# and you run scripts from the project root, this might not be needed.
# If run directly, and other modules are in parent/sibling dirs, it might be.
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

"""AI Preset Generator - Generate random wallpaper preferences using Gemini AI

This script uses Google's Gemini AI to create intelligent, coherent random presets
for the wallpaper generator application based on detected style categories.
"""

import json
import logging
import random
import hashlib
import re
import time
import argparse
from typing import Dict, Any, List, Optional, Union, Set

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
            return None # Or a dummy response object if your code expects one
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
            'BLOCK_NONE': 'BLOCK_NONE', # Use with caution
        })
        StopCandidateException = type('StopCandidateException', (Exception,), {})

    genai = DummyGenAI()
    genai_types = DummyGenAITypes()

# --- Local Application Imports & Fallbacks ---
# These fallbacks are used if the proper modules are not found.
# This structure assumes you might run this script directly or as part of a larger app.

def _print_section_fallback(x): print(f"\n--- {x} ---")
def _print_option_fallback(k, v): print(f"  {k}. {v}")
def _print_info_fallback(x): print(x)
def _print_error_fallback(x): print(f"ERROR: {x}")
def _print_success_fallback(x): print(f"SUCCESS: {x}")
def _print_warning_fallback(x): print(f"WARNING: {x}")

def _get_validated_input_fallback(prompt_msg: str, valid_options: List[str]) -> str:
    while True:
        val = input(f"{prompt_msg} {valid_options}: ").strip().lower()
        if val in [str(choice).lower() for choice in valid_options]:
            return val
        _print_error_fallback(f"Invalid input. Please enter one of {valid_options}")

class UserPreferencesPlaceholder:
    def __init__(self):
        # Add any default attributes your main script might expect
        self.some_preference = "default_value"

def initialize_settings_fallback(): return UserPreferencesPlaceholder()
def get_preferences_fallback(): return initialize_settings_fallback()
def generate_random_style_fallback(style_type="default"): return {"name": "Random Fallback Style"}
def initialize_style_gemini_fallback(api_key): pass
def deep_update_fallback(target, source): target.update(source); return target # Simplified

# Attempt to import actual modules
try:
    from wallpaper_settings import UserPreferences, get_preferences, initialize_settings
    SETTINGS_AVAILABLE = True
except ImportError:
    SETTINGS_AVAILABLE = False
    UserPreferences = UserPreferencesPlaceholder
    get_preferences = get_preferences_fallback
    initialize_settings = initialize_settings_fallback
    _print_warning_fallback("wallpaper_settings.py not found. Using placeholder UserPreferences.")

try:
    from ui_utils import get_validated_input, print_section, print_option, print_info, print_error, print_success, print_warning
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
    _print_warning_fallback("ui_utils not found. Using basic print/input for UI.")

try:
    # Assuming ai_style_generator is in the same package or accessible via sys.path
    from ai_style_generator import generate_random_style, initialize_gemini as initialize_style_gemini
    AI_STYLE_GEN_AVAILABLE = True
except ImportError:
    AI_STYLE_GEN_AVAILABLE = False
    generate_random_style = generate_random_style_fallback
    initialize_style_gemini = initialize_style_gemini_fallback
    _print_warning_fallback("Could not import ai_style_generator. AI style generation feature disabled.")

try:
    from file_utils import deep_update
    FILE_UTILS_AVAILABLE = True
except ImportError:
    FILE_UTILS_AVAILABLE = False
    deep_update = deep_update_fallback
    _print_warning_fallback("file_utils not found. Using placeholder deep_update.")

try:
    # Assuming config.py is in the same package or accessible
    from config import STYLE_CATEGORIES as CONFIG_STYLE_CATEGORIES
except ImportError:
    _print_warning_fallback("Could not import STYLE_CATEGORIES from config.py. Using empty dictionary.")
    CONFIG_STYLE_CATEGORIES = {}

try:
    # Assuming style_templates and style_category_catalog are in ai_prest_gen sub-package
    from ai_prest_gen.style_templates import get_template_for_category
    from ai_prest_gen.style_category_catalog import (
        hybrid_styles,
        hybrid_categories_keywords,
        categories_keywords,
        preferred_order,
        all_categories as catalog_all_categories, # Renamed to avoid conflict
        instructions_for_category
    )
    CATALOG_AVAILABLE = True
except ImportError as e:
    _print_error_fallback(f"FATAL: Could not import from ai_prest_gen submodules (style_templates, style_category_catalog): {e}")
    _print_error_fallback("Please ensure these files exist in an 'ai_prest_gen' subdirectory and it's a package (contains __init__.py).")
    CATALOG_AVAILABLE = False
    # Define fallbacks for catalog data if not available
    hybrid_styles = {}
    hybrid_categories_keywords = {}
    categories_keywords = {}
    preferred_order = ["default", "unknown"]
    catalog_all_categories = ["default", "unknown"]
    def instructions_for_category(cat, style): return "No specific instructions available."
    def get_template_for_category(cat): return {}


# --- Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("ai_preset_generator.log", mode='a')] # Append mode
)
PRESETS_CACHE_FILE = "generated_presets_cache.json"
PRESETS_DIR = "presets"
os.makedirs(PRESETS_DIR, exist_ok=True) # Ensure presets directory exists

gemini_initialized_main = False # For main preset generation model

# --- Helper Functions ---

def get_gemini_api_key() -> Optional[str]:
    """Retrieve the Gemini API key from environment variable."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        _print_warning_fallback("GEMINI_API_KEY environment variable not set.")
        logging.warning("GEMINI_API_KEY environment variable not set.")
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
        # Ensure 'styles' is a list for consistent hashing
        if "styles" in preset_data and not isinstance(preset_data["styles"], list):
             preset_data["styles"] = [preset_data["styles"]]
        preset_hash = hashlib.md5(json.dumps(preset_data, sort_keys=True).encode()).hexdigest()
        cached_presets = load_cached_presets()
        if preset_hash not in cached_presets:
            cached_presets.append(preset_hash)
            # Keep cache size manageable, e.g., last 100 presets
            if len(cached_presets) > 100:
                cached_presets = cached_presets[-100:]
            try:
                with open(PRESETS_CACHE_FILE, 'w') as f:
                    json.dump(cached_presets, f)
            except IOError as e:
                logging.error(f"Error writing to presets cache: {e}")
    except Exception as e:
        logging.error(f"Unexpected error in save_preset_to_cache: {e}")

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
        return True # Default to true to avoid blocking generation on error

def normalize_style_name(style_name: str) -> str:
    """Normalizes a style name for consistent matching."""
    name = str(style_name).lower()
    name = name.replace('_', ' ').replace('-', ' ')
    name = name.replace('colour', 'color') # UK to US English
    name = name.replace('water color', 'watercolor') # Spaced variant
    name = name.replace('sci fi', 'scifi') # Common abbreviation
    name = re.sub(r'\s+', ' ', name).strip() # Remove extra spaces
    return name

def categorize_style(style_name_input: Union[str, Dict]) -> str:
    """
    Categorize a style name using the comprehensive catalog.
    Detection prioritizes:
    1. Token-based hybrid styles.
    2. Keyword-based hybrid styles.
    3. Single-term general categories, resolved by preferred_order.
    """
    if not CATALOG_AVAILABLE:
        _print_warning_fallback("Style catalog not available, categorization will be basic.")
        return "unknown"

    if isinstance(style_name_input, dict):
        style_name_str = style_name_input.get('name', '')
    else:
        style_name_str = str(style_name_input)

    normalized_style = normalize_style_name(style_name_str)
    if not normalized_style:
        return "unknown"

    # 1. Token-based Hybrid Style Detection
    # Split by common delimiters for multi-style inputs like "impressionism / art nouveau"
    # Also consider simple space splitting for multi-word styles that form a hybrid key
    style_tokens_delimiters = set(re.split(r'[,+/&|]', normalized_style))
    style_tokens_delimiters = {token.strip() for token in style_tokens_delimiters if token.strip()}

    style_tokens_space = set(normalized_style.split()) # For frozensets based on space-separated words

    # Check against frozenset keys in hybrid_styles
    for hybrid_token_set, target_category in hybrid_styles.items():
        # Check if the defined hybrid_token_set is a subset of tokens derived from delimiter splitting
        if hybrid_token_set.issubset(style_tokens_delimiters):
            logging.info(f"Matched token-based hybrid (delimiter split): '{target_category}' for '{style_name_str}' from tokens '{style_tokens_delimiters}'")
            return target_category
        # Check if the defined hybrid_token_set is a subset of tokens derived from space splitting
        # This helps catch cases like "pop surrealism ascii" where "pop surrealism" might be one token in delimiter split
        if hybrid_token_set.issubset(style_tokens_space):
            logging.info(f"Matched token-based hybrid (space split): '{target_category}' for '{style_name_str}' from tokens '{style_tokens_space}'")
            return target_category


    # 2. Keyword-based Hybrid Style Detection
    for target_category, keyword_tuples in hybrid_categories_keywords.items():
        for keyword_set in keyword_tuples:
            if all(re.search(r'\b' + re.escape(kw) + r'\b', normalized_style) for kw in keyword_set):
                logging.info(f"Matched keyword-based hybrid: '{target_category}' for '{style_name_str}' using keywords '{keyword_set}'")
                return target_category

    # 3. General/Single-Term Category Keywords
    matched_categories: Set[str] = set()
    for target_category, keywords in categories_keywords.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', normalized_style):
                matched_categories.add(target_category)
                # Log individual keyword match for better debugging if needed
                # logging.debug(f"Keyword '{keyword}' matched for category '{target_category}' in style '{style_name_str}'")

    if not matched_categories:
        # Fallback: if no specific keywords match, check if the normalized style itself is a defined category
        # This helps for direct inputs like "cyberpunk" or "oil_painting"
        if normalized_style in catalog_all_categories: # Use the comprehensive list from catalog
             logging.info(f"Direct match for category: '{normalized_style}' for input '{style_name_str}'")
             return normalized_style

    # 4. Prioritize and Return
    if matched_categories:
        for preferred_cat in preferred_order: # Use the comprehensive preferred_order from the catalog
            if preferred_cat in matched_categories:
                logging.info(f"Prioritized match: '{preferred_cat}' for '{style_name_str}' from candidates {matched_categories}")
                return preferred_cat
        # If no preferred match, return the first one alphabetically from matched (consistent fallback)
        fallback_match = sorted(list(matched_categories))[0]
        logging.info(f"Fallback alphabetical match: '{fallback_match}' for '{style_name_str}' from candidates {matched_categories}")
        return fallback_match

    logging.warning(f"Could not categorize style: '{style_name_str}'. Falling back to 'unknown'.")
    return "unknown"


def initialize_main_gemini(api_key: str) -> bool:
    """Initializes the Gemini model for main preset generation."""
    global gemini_initialized_main
    if not GEMINI_AVAILABLE:
        _print_error_fallback("Gemini AI library not available. Cannot initialize.")
        return False
    if gemini_initialized_main:
        return True
    try:
        genai.configure(api_key=api_key)
        # Quick test to ensure API key is valid and service is reachable
        # list(genai.list_models()) # This can be slow, consider a lighter check or removing
        gemini_initialized_main = True
        logging.info("Gemini API initialized successfully for preset generation.")
        return True
    except Exception as init_err:
        logging.error(f"Failed to initialize Gemini API: {init_err}")
        _print_error_fallback(f"Failed to initialize Gemini API: {init_err}")
        gemini_initialized_main = False
        return False

def generate_ai_preset(user_prefs: Any, base_style_override: Optional[str] = None) -> Union[str, bool, None]:
    """Generate a random preset based on style category."""
    api_key = get_gemini_api_key()
    if not api_key:
        _print_error_fallback("Gemini API key not configured. Set GEMINI_API_KEY environment variable.")
        return False

    if not initialize_main_gemini(api_key): # Initialize Gemini for this specific task
        return False

    if not CATALOG_AVAILABLE:
        _print_error_fallback("Style catalog is not available. Cannot generate AI preset.")
        return False

    base_style: Optional[str] = None
    try:
        # --- Step 1: Get Base Style ---
        if base_style_override:
            base_style = base_style_override
            print_info(f"Using provided style: {base_style}")
        else:
            print_section("Choose Style Source for Preset")
            print_option("1", "Enter Custom Style")
            print_option("2", "Generate AI Style (if ai_style_generator is available)")
            print_option("b", "Back to Main Menu")

            valid_choices = ["1", "b"]
            if AI_STYLE_GEN_AVAILABLE:
                valid_choices.append("2")

            choice = get_validated_input("Select option:", valid_choices)

            if choice == "b":
                print_info("Preset generation cancelled.")
                return None
            elif choice == "1":
                base_style = input("Enter your custom style (e.g., 'impressionism', 'cyberpunk city', 'watercolor pencil sketch'): ").strip()
                if not base_style:
                    _print_error_fallback("No style entered.")
                    return False
            elif choice == "2" and AI_STYLE_GEN_AVAILABLE:
                print_info("Attempting to generate AI style (this may take a moment)...")
                # Ensure Gemini for style generation is also initialized if it's a separate instance/config
                if not initialize_style_gemini(api_key): # From ai_style_generator
                     _print_error_fallback("Failed to initialize Gemini for AI style generation.")
                     return False
                style_obj = generate_random_style(style_type="detailed_artistic_style") # Request a more complex style
                if not style_obj or not isinstance(style_obj, dict):
                    _print_error_fallback("Failed to generate AI style object.")
                    return False
                base_style = style_obj.get('name')
                if not base_style:
                    _print_error_fallback("AI generated style object lacked a 'name'.")
                    return False
                print_info(f"AI Generated Style: {base_style} (Description: {style_obj.get('description', 'N/A')})")


        if not base_style: # Should not happen if logic above is correct
            _print_error_fallback("Base style could not be determined.")
            return False

        # --- Step 2: Generate Settings ---
        print_info(f"\nGenerating settings for style: '{base_style}'...")
        style_category = categorize_style(base_style) # Uses the enhanced categorization
        print_info(f"(Detected category: {style_category})")

        model_name = 'gemini-1.5-flash-latest' # Or 'gemini-1.0-pro-latest' or 'gemini-1.5-pro-latest' if flash is too limited
        try:
            model = genai.GenerativeModel(model_name)
            print_info(f"Using Gemini model: {model_name}...")
        except Exception as err:
            logging.error(f"Failed to initialize Gemini model '{model_name}': {err}")
            _print_error_fallback(f"Could not initialize AI model '{model_name}'.")
            return False

        instruction_header = f"You are an expert in art history, digital art, and graphic design. Generate a coherent and aesthetically pleasing preset for the style: \"{base_style}\" (which has been categorized as: \"{style_category}\")."
        category_specific_instructions = instructions_for_category(style_category, base_style) # From catalog

        template = get_template_for_category(style_category) # From style_templates, uses portrait_style_templates
        if not template or not isinstance(template, dict):
             logging.error(f"No valid template found for category: {style_category}. Using a minimal default.")
             template = {
                 "preset_name": "[AI_GENERATED_NAME]",
                 "styles": [base_style],
                 "moods": ["[AI_CHOSEN_MOOD]"],
                 "description": "[AI_GENERATED_DESCRIPTION]",
                 "aspect_ratio": "16:9", # Ensure this is present
                 "imagen_settings": {
                     "negative_prompt": "[AI_NEGATIVE_PROMPT_CATEGORY]",
                     "style_negative_prompt": "[AI_NEGATIVE_PROMPT_STYLE]"
                 }
             }
        else: # Ensure base_style is the primary style
            template["styles"] = [base_style] # Override or set

        # Ensure description and aspect_ratio are in the base of the template for the prompt
        template.setdefault("description", "[AI_GENERATED_DESCRIPTION]")
        template.setdefault("aspect_ratio", "16:9")


        prompt = f"""
        {instruction_header}

        **Task:** Fill in the following JSON template with appropriate settings for the style "{base_style}".
        Pay close attention to the category-specific guidance provided.

        **Category Specific Guidance for "{style_category}"**:
        {category_specific_instructions}

        **General Instructions for Filling the Template:**
        1.  `preset_name`: Create a unique, evocative name inspired by "{base_style}" and "{style_category}". (e.g., "Neon Dreams Cyberpunk", "Minimalist Serenity Geo").
        2.  `description`: Write a concise (2-3 sentences) description of the overall preset, summarizing its mood, style, and key visual characteristics.
        3.  `moods`: Choose ONE primary mood (a single descriptive word or short phrase) that best fits "{base_style}" and place it as a string in this list.
        4.  `aspect_ratio`: Must be "16:9".
        5.  `imagen_settings.negative_prompt`: Generate a concise (10-15 words) negative prompt tailored to AVOID elements that conflict with the *category* "{style_category}". Examples:
            - Photographic: "cartoon, drawing, sketch, unrealistic, 2d"
            - Minimalist: "cluttered, detailed, messy, complex, ornate"
            - Watercolor: "photorealistic, 3d render, sharp focus, hyperdetailed, glossy"
        6.  `imagen_settings.style_negative_prompt`: Generate a concise (10-15 words) negative prompt tailored to AVOID elements that conflict with the *overall base style* "{base_style}". This might be similar but more specific to the nuances of the base style.
        7.  For all other fields with bracketed placeholders (e.g., `[ fitting movement ]`), replace them with specific, fitting values. Do NOT leave placeholders.
        8.  If a setting in the template seems irrelevant for "{base_style}", you can use a neutral or common default (e.g., "N/A" for weather if not applicable, or "medium" for a generic detail level if unsure).
        9.  Output ONLY the valid JSON object, starting with `{{` and ending with `}}`. Do not include "```json" or "```".

        **JSON Template to Fill:**
        ```json
        {json.dumps(template, indent=4)}
        ```
        """

        for attempt in range(3): # Retry mechanism
            print_info(f"Generating settings with AI (Attempt {attempt + 1}/3)...")
            try:
                safety_settings = { # Stricter safety settings
                    genai_types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai_types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    genai_types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai_types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    genai_types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai_types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    genai_types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai_types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                }
                generation_config = genai.types.GenerationConfig(
                    temperature=0.7, # Adjust for creativity vs. adherence
                    top_p=0.95,
                    top_k=40
                )
                response = model.generate_content(
                    prompt,
                    generation_config=generation_config,
                    safety_settings=safety_settings
                )

                if response and response.candidates and response.candidates[0].content.parts:
                    response_text = response.candidates[0].content.parts[0].text.strip()
                    # Extract JSON (robustly handles ```json ... ``` or just { ... })
                    json_match = re.search(r'```json\s*(\{.*?\})\s*```|(\{.*?\})', response_text, re.DOTALL)
                    if json_match:
                        json_str = json_match.group(1) or json_match.group(2)
                        try:
                            generated_settings = json.loads(json_str)

                            # --- Validation and Refinement of AI Output ---
                            final_preset = {"styles": [base_style]} # Start with base style

                            # Preset Name
                            preset_name = generated_settings.get("preset_name", f"{base_style.replace('_',' ').title()} Preset {random.randint(100,999)}")
                            if not isinstance(preset_name, str) or not preset_name.strip() or "[AI_GENERATED_NAME]" in preset_name:
                                preset_name = f"{base_style.replace('_',' ').title()} Preset {random.randint(100,999)}"
                            final_preset["preset_name"] = preset_name.strip()

                            # Moods
                            moods = generated_settings.get("moods", ["neutral"])
                            if not isinstance(moods, list) or not moods or not isinstance(moods[0], str) or not moods[0].strip() or "[AI_CHOSEN_MOOD]" in moods[0]:
                                moods = [random.choice(["serene", "energetic", "mysterious", "playful", "dramatic"])] # Sensible random default
                            final_preset["moods"] = [moods[0].strip()] # Ensure single mood string

                            # Description
                            description = generated_settings.get("description", f"A preset for the style: {base_style}")
                            if not isinstance(description, str) or not description.strip() or "[AI_GENERATED_DESCRIPTION]" in description:
                                description = f"An AI generated preset capturing the essence of {base_style} ({style_category}). Mood: {final_preset['moods'][0]}."
                            final_preset["description"] = description.strip()

                            # Aspect Ratio
                            final_preset["aspect_ratio"] = "16:9" # Enforce

                            # Imagen Settings (merge carefully)
                            final_preset["imagen_settings"] = template.get("imagen_settings", {}).copy() # Start with template's imagen_settings
                            ai_imagen_settings = generated_settings.get("imagen_settings", {})
                            if isinstance(ai_imagen_settings, dict):
                                deep_update(final_preset["imagen_settings"], ai_imagen_settings) # Update with AI's imagen_settings

                            # Negative Prompts
                            neg_prompt = final_preset["imagen_settings"].get("negative_prompt", "")
                            if not neg_prompt or "[AI_NEGATIVE_PROMPT_CATEGORY]" in neg_prompt or "[GENERATE_NEGATIVE_PROMPT_BASED_ON_STYLE]" in neg_prompt:
                                final_preset["imagen_settings"]["negative_prompt"] = f"avoid elements conflicting with {style_category} category"
                            style_neg_prompt = final_preset["imagen_settings"].get("style_negative_prompt", "")
                            if not style_neg_prompt or "[AI_NEGATIVE_PROMPT_STYLE]" in style_neg_prompt or "[GENERATE_STYLE_SPECIFIC_NEGATIVE_PROMPT]" in style_neg_prompt:
                                final_preset["imagen_settings"]["style_negative_prompt"] = f"avoid elements conflicting with {base_style} style"

                            # Merge other top-level keys from AI output if they were in the template
                            for key, value in generated_settings.items():
                                if key in template and key not in final_preset: # Only add if it was part of the original template structure
                                    final_preset[key] = value
                            
                            # Ensure all keys from the original template are present, using AI's value or template's if AI missed it
                            for key, t_value in template.items():
                                if key not in final_preset:
                                    final_preset[key] = t_value


                            if is_preset_unique(final_preset):
                                preview_text = json.dumps(final_preset, indent=4)
                                print_section("Preview of Generated Preset")
                                print_info(preview_text)
                                confirm = get_validated_input("Save this preset? (y/n):", ["y", "n", "yes", "no"])

                                if confirm.startswith('y'):
                                    save_preset_to_cache(final_preset)
                                    clean_preset_name = re.sub(r'[^\w\s-]', '', final_preset["preset_name"]).strip().replace(' ', '_')
                                    preset_filename = f"{clean_preset_name.lower()}_{int(time.time())}.json" # Add timestamp for uniqueness
                                    preset_path = os.path.join(PRESETS_DIR, preset_filename)
                                    with open(preset_path, 'w') as f:
                                        json.dump(final_preset, f, indent=4)
                                    print_success(f"Generated unique preset: '{final_preset['preset_name']}'")
                                    print_success(f"Saved to: {preset_path}")
                                    return preset_path
                                else:
                                    print_warning("Preset saving cancelled by user.")
                                    return None # User cancelled
                            else:
                                print_warning("Generated preset is too similar to a previous one. Retrying...")
                                if attempt == 2: # Last attempt
                                    print_error("Failed to generate a unique preset after 3 attempts.")
                                    return False
                                time.sleep(1) # Brief pause before retry
                                continue # To next attempt in the loop

                        except json.JSONDecodeError as json_err:
                            logging.error(f"Failed to parse JSON response: {json_err}\nResponse text was:\n{response_text}")
                            _print_error_fallback(f"AI response was not valid JSON (Attempt {attempt + 1}).")
                            if attempt == 2: return False
                            time.sleep(1)
                            continue
                    else: # No JSON found
                        logging.warning(f"Could not extract JSON from response (Attempt {attempt+1}). Response: {response_text}")
                        _print_warning_fallback(f"AI response format was unexpected (Attempt {attempt + 1}).")
                        if attempt == 2: return False
                        time.sleep(1)
                        continue
                elif response and response.prompt_feedback and response.prompt_feedback.block_reason:
                     block_reason = response.prompt_feedback.block_reason
                     logging.warning(f"Generation blocked by API. Reason: {block_reason} (Attempt {attempt + 1})")
                     _print_warning_fallback(f"Generation blocked (Reason: {block_reason}). Retrying...")
                     if attempt == 2: return False
                     time.sleep(2 + attempt * 2) # Exponential backoff for blocks
                     continue
                else: # Empty or problematic response
                    logging.warning(f"Received no valid response or candidates (Attempt {attempt+1}). Full response: {response}")
                    _print_warning_fallback(f"AI returned an empty or invalid response (Attempt {attempt + 1}).")
                    if attempt == 2: return False
                    time.sleep(1)
                    continue

            except genai_types.StopCandidateException as stop_err: # Should be caught by prompt_feedback now
                 logging.warning(f"Generation stopped by API (StopCandidateException): {stop_err} (Attempt {attempt + 1})")
                 _print_warning_fallback(f"Generation stopped by API: {stop_err}. Retrying...")
                 if attempt == 2: return False
                 time.sleep(2 + attempt * 2)
                 continue
            except Exception as api_err: # General API errors or other unexpected issues
                err_str = str(api_err).lower()
                if "api key not valid" in err_str or "authentication" in err_str:
                     logging.error(f"Authentication error: {api_err}")
                     _print_error_fallback("Authentication error. Check your GEMINI_API_KEY.")
                     return False # Fatal
                elif "rate limit" in err_str or "429" in err_str or "resource has been exhausted" in err_str:
                    logging.warning(f"Rate limit or resource exhaustion: {api_err}. Waiting... (Attempt {attempt + 1})")
                    _print_warning_fallback("API rate limit reached or resource exhausted. Waiting before retry...")
                    if attempt == 2: return False
                    time.sleep(10 + attempt * 10) # Longer backoff for rate limits
                    continue
                else:
                    logging.error(f"Generation failed with an unexpected API error: {api_err} (Attempt {attempt + 1})")
                    _print_error_fallback(f"Failed to generate settings due to an API error: {api_err}")
                    if attempt == 2: return False
                    time.sleep(2)
                    continue
        # If loop finishes without returning
        _print_error_fallback("Failed to generate a unique and valid preset after all attempts.")
        return False

    except Exception as e:
        logging.exception("An unexpected error occurred during AI preset generation:")
        _print_error_fallback(f"An unexpected error occurred: {e}")
        return False

# Assuming preset_management is a module you have for applying settings
# For now, creating a placeholder if it's not found.
class PresetManagementPlaceholder:
    def _apply_preset_settings(self, settings, replace=True):
        _print_info_fallback(f"Placeholder: Applying preset '{settings.get('preset_name', 'Unknown Preset')}'...")
        # In a real scenario, this would interact with your wallpaper_settings
        # For example: current_prefs = get_preferences(); deep_update(current_prefs.__dict__, settings)
        return True # Simulate success

try:
    from settings_modules import preset_management
    PRESET_MGMT_AVAILABLE = True
except ImportError:
    PRESET_MGMT_AVAILABLE = False
    preset_management = PresetManagementPlaceholder()
    _print_warning_fallback("settings_modules.preset_management not found. Preset application will be simulated.")


def main():
    """Main function to handle user interaction."""
    parser = argparse.ArgumentParser(description="Generate AI wallpaper presets.")
    parser.add_argument("--style", type=str, help="Specify a base style to generate a preset for directly.")
    parser.add_argument("--apply-preset", type=str, help="Apply a preset by name or full path directly from the terminal.")
    args = parser.parse_args()

    if not GEMINI_AVAILABLE:
        _print_error_fallback("Gemini AI library is not available. This script requires 'google-generativeai'.")
        _print_error_fallback("Please install it using: pip install google-generativeai")
        sys.exit(1)
    if not CATALOG_AVAILABLE:
        _print_error_fallback("Essential style catalog data is missing. Cannot proceed.")
        sys.exit(1)

    user_prefs = get_preferences()

    if args.apply_preset:
        preset_identifier = args.apply_preset
        print_info(f"Attempting to apply preset: {preset_identifier}")

        # Check if it's a full path first
        if os.path.exists(preset_identifier) and preset_identifier.lower().endswith(".json"):
            preset_path = preset_identifier
        else: # Assume it's a name in the PRESETS_DIR
            preset_name = preset_identifier
            if not preset_name.lower().endswith(".json"):
                preset_name += ".json"
            preset_path = os.path.join(PRESETS_DIR, preset_name)

        if not os.path.exists(preset_path):
            _print_error_fallback(f"Preset file '{preset_path}' not found.")
            sys.exit(1)

        try:
            with open(preset_path, 'r') as f:
                settings_to_apply = json.load(f)

            if PRESET_MGMT_AVAILABLE:
                success = preset_management._apply_preset_settings(settings_to_apply, replace=True) # type: ignore
            else: # Use placeholder
                success = preset_management._apply_preset_settings(settings_to_apply, replace=True)


            if success:
                print_success(f"Preset from '{os.path.basename(preset_path)}' applied successfully.")
                sys.exit(0)
            else:
                _print_error_fallback(f"Failed to apply preset from '{os.path.basename(preset_path)}'.")
                sys.exit(1)
        except Exception as e:
            _print_error_fallback(f"Error loading or applying preset from '{os.path.basename(preset_path)}': {e}")
            sys.exit(1)

    if args.style:
        print_info(f"Generating preset directly for style: {args.style}")
        result = generate_ai_preset(user_prefs, base_style_override=args.style)
        if isinstance(result, str):
             print_success(f"Preset generated and saved: {result}")
        elif result is None:
            print_info("Preset generation was cancelled or no unique preset could be made.")
        else: # False
             _print_error_fallback("Preset generation failed.")
    else:
        while True:
            print_section("AI Preset Generator Menu")
            print_option("1", "Generate New AI Preset")
            print_option("q", "Quit")
            choice = get_validated_input("Select option:", ["1", "q"])

            if choice == '1':
                result = generate_ai_preset(user_prefs)
                if isinstance(result, str): # Path to file returned
                     print_success(f"Preset generated and saved: {result}")
                elif result is None: # User cancelled save or no unique preset
                    print_info("Preset generation was cancelled or no unique preset could be made.")
                else: # False indicates failure
                     _print_error_fallback("Preset generation failed.")
                input("\nPress Enter to continue...")
            elif choice == 'q':
                print_info("Exiting AI Preset Generator.")
                break

if __name__ == "__main__":
    # Ensure the script's directory is in sys.path if it's not run as a module
    # This helps locate sibling packages like 'ai_prest_gen' if the structure is:
    # project_root/
    #   ai_preset_generator.py  <-- (if this script was here)
    #   ai_prest_gen/
    #     __init__.py
    #     style_category_catalog.py
    #     style_templates.py
    # However, the script seems to be intended to be inside 'ai_prest_gen' itself.
    # The initial sys.path.insert in the uploaded file was:
    # sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    # This implies the script is in a subdirectory and '..' is the project root.
    # If ai_prest_gen is a package, running `python -m ai_prest_gen.ai_preset_generator` from
    # the project root is often more robust for imports.

    # For direct execution, if ai_preset_generator.py is inside ai_prest_gen package,
    # and ai_prest_gen is inside a project root, then to import sibling modules of ai_prest_gen,
    # the project root needs to be in sys.path.
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root_dir = os.path.dirname(current_script_dir) # Assumes script is in 'ai_prest_gen' and 'ai_prest_gen' is in project root
    if project_root_dir not in sys.path:
        sys.path.insert(0, project_root_dir)

    main()
