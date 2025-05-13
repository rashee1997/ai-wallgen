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

from . import config # Added import for configuration
from .preset_cache_manager import PresetCacheManager # Added import
from .style_categorizer import StyleCategorizer # Added import
from .prompt_builder import PresetPromptBuilder # Added import
from .preset_generator_engine import PresetGenerator # Added import

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
        preset_path = os.path.join(config.PRESETS_DIR_NAME, preset_filename) # Use config
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
# Constants are now sourced from config.py

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(config.LOG_FILE_NAME, mode='a')] # Use config
)
# Ensure presets directory exists
os.makedirs(config.PRESETS_DIR_NAME, exist_ok=True) # Use config

# Initialize PresetCacheManager
preset_cache_manager = PresetCacheManager(config.PRESETS_CACHE_FILE_NAME)

# Initialize StyleCategorizer
style_categorizer = StyleCategorizer()

# Initialize PresetPromptBuilder
prompt_builder = PresetPromptBuilder()

# gemini_initialized flag is now managed by gemini_config_preset for this script's context

# --- AI Preset Generation Logic ---
# The core functions (_get_base_style_for_preset, _process_gemini_preset_response, 
# _save_generated_preset, and generate_ai_preset) have been moved to 
# the PresetGenerator class in preset_generator_engine.py.
# This script will now import and use PresetGenerator.


# --- Preset Management Placeholder ---
# This remains as it's used by the --apply-preset CLI arg in main(),
# and is not part of the PresetGenerator's direct responsibilities.
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

    # Initialize core components
    # StyleCategorizer, PresetPromptBuilder, PresetCacheManager are already initialized globally
    # Create an instance of PresetGenerator
    preset_generator_instance = PresetGenerator(
        style_categorizer=style_categorizer,
        prompt_builder=prompt_builder,
        preset_cache_manager=preset_cache_manager
    )

    if not preset_generator_instance.gemini_available:
        if not GEMINI_AVAILABLE: 
             print_error("Gemini AI library is not available. This script requires 'google-generativeai'.")
             print_error("Please install it using: pip install google-generativeai")
             sys.exit(1)
    
    # CATALOG_AND_TEMPLATES_AVAILABLE check is implicitly handled by the components.
    # For safety, one could add a check here for CATALOG_AND_TEMPLATES_AVAILABLE if critical for CLI operations
    # not covered by PresetGenerator. However, for generation, PresetGenerator's internal checks suffice.
    # if not CATALOG_AND_TEMPLATES_AVAILABLE:
    #     print_error("Essential style catalog/template data is missing. Cannot proceed with some operations.")
    #     # Decide if sys.exit(1) is needed based on what CLI args might still function.

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
            preset_path = os.path.join(config.PRESETS_DIR_NAME, preset_name)

        if not os.path.exists(preset_path):
            print_error(f"Preset file '{preset_path}' not found.")
            sys.exit(1)

        try:
            with open(preset_path, 'r') as f:
                settings_to_apply = json.load(f)
            # Note: preset_management is still a global/module level import here
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
        result = preset_generator_instance.generate_ai_preset(user_prefs, base_style_override=args.style, auto_save_flag=args.auto_save)
        if isinstance(result, str):
             print_success(f"Preset generated and saved: {result}")
        elif result is None:
            print_info("Preset generation was cancelled or no unique preset could be made.")
        else: 
             print_error("Preset generation failed.")
    else:
        # Interactive Menu Loop
        while True:
            if UI_UTILS_AVAILABLE: 
                try:
                    clear_screen()
                    print_header("AI Preset Generator")
                except NameError: # Fallback if clear_screen or print_header not truly available
                    print("\n--- AI Preset Generator Menu ---")

            print_option("1", "Generate New AI Preset")
            print_option("q", "Quit")
            
            choice = get_validated_input( # Relies on global get_validated_input or its fallback
                prompt="Select option:",
                options=["1", "q"],
                help_context_id="AI_PRESET_GENERATOR_MENU"
            )
            if choice == "_HELP_SHOWN_": # If get_validated_input supports this
                continue
            if choice == '1':
                result = preset_generator_instance.generate_ai_preset(user_prefs, auto_save_flag=args.auto_save)
                if isinstance(result, str):
                     print_success(f"Preset generated and saved: {result}")
                elif result is None:
                    print_info("Preset generation was cancelled or no unique preset could be made.")
                else: 
                     print_error("Preset generation failed.")
                input("\nPress Enter to continue...")
            elif choice == 'q':
                print_info("Exiting AI Preset Generator.")
                break

# advanced_settings_menu and select_gemini_model_menu functions are removed from this file.
# This functionality will be moved to wall_gen.settings_modules.menu_management.advanced_options_menu.py


if __name__ == "__main__":
    main()
# --- End of ai_preset_generator.py ---
