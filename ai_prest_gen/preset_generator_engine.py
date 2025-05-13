#!/usr/bin/env python3
"""
Core Preset Generation Engine for the AI Wallpaper Generator project.

This module defines the PresetGenerator class, which encapsulates the logic
for generating AI-driven wallpaper presets.
"""

import json
import logging
import random # Though not directly used in moved methods, good to keep if logic evolves
import hashlib # Used by preset_cache_manager, not directly here
import re
import time
import os # For os.path.join if save_preset_fallback were part of this class
from typing import Dict, Any, List, Optional, Union

# Gemini API related imports
try:
    import google.generativeai as genai
    import google.generativeai.types as genai_types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    # Define dummy genai and types for graceful failure if not available
    class DummyGenAI:
        def configure(self, *args, **kwargs): pass
        def GenerativeModel(self, *args, **kwargs): return DummyGenerativeModel() # type: ignore
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

    genai = DummyGenAI() # type: ignore
    genai_types = DummyGenAITypes() # type: ignore


from . import config # For PRESETS_DIR_NAME etc.
from .style_categorizer import StyleCategorizer
from .prompt_builder import PresetPromptBuilder
from .preset_cache_manager import PresetCacheManager

# Imports that were previously in ai_preset_generator.py and are needed by methods
# from .style_category_catalog import instructions_for_category # Now handled by prompt_builder
from .style_templates import get_template_for_category # Needed by _process_gemini_preset_response
from .gemini_config_preset import (
    initialize_preset_gemini,
    get_selected_preset_model,
    is_preset_gemini_initialized,
    get_preset_last_error
)

# UI and File Utils - these are crucial.
# The main script (ai_preset_generator.py) will ensure these are the "real" ones or fallbacks.
# This engine class will assume they are available via these import paths.
try:
    from wall_gen.ui_utils import get_validated_input, print_section, print_option, print_info, print_error, print_success, print_warning
    UI_UTILS_AVAILABLE = True
except ImportError:
    UI_UTILS_AVAILABLE = False
    def print_info(x): print(x)
    def print_error(x): print(f"ERROR: {x}")
    def print_warning(x): print(f"WARNING: {x}")
    def print_success(x): print(f"SUCCESS: {x}")
    def print_section(x): print(f"\n--- {x} ---")
    def print_option(k, v): print(f"  {k}. {v}")
    def get_validated_input(prompt_msg: str, options: List[str], **kwargs) -> str:
        while True:
            val = input(f"{prompt_msg} {options}: ").strip().lower()
            if val in [str(choice).lower() for choice in options]: return val
            print_error(f"Invalid input. Please enter one of {options}")

try:
    from wall_gen.file_utils import deep_update
    FILE_UTILS_AVAILABLE = True
except ImportError:
    FILE_UTILS_AVAILABLE = False
    def deep_update(target: dict, source: dict) -> dict:
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                deep_update(target[key], value)
            else:
                target[key] = value
        return target
    print_warning_fallback = lambda x: print(f"WARNING: {x}") # type: ignore
    print_warning_fallback("wall_gen.file_utils not found. Using custom recursive deep_update.")


try:
    from wall_gen.settings_modules.preset_management import save_preset
    SAVE_PRESET_AVAILABLE = True
except ImportError:
    SAVE_PRESET_AVAILABLE = False
    def save_preset_fallback(preset_data: Dict[str, Any], preset_name_base: str) -> bool: # type: ignore
        print_warning(f"save_preset function not found. Simulating save for '{preset_name_base}'.")
        try:
            preset_filename = f"{preset_name_base}.json"
            # Ensure config.PRESETS_DIR_NAME is accessible; might need to pass config or use a fixed path
            preset_path = os.path.join(getattr(config, "PRESETS_DIR_NAME", "presets"), preset_filename)
            os.makedirs(os.path.dirname(preset_path), exist_ok=True)
            with open(preset_path, 'w') as f:
                json.dump(preset_data, f, indent=4)
            logging.info(f"(Fallback) Preset saved to file: {preset_path}")
            return True
        except Exception as e:
            logging.error(f"(Fallback) Error saving preset file '{preset_path}': {e}") # type: ignore
            return False
    save_preset = save_preset_fallback # type: ignore
    print_warning_fallback = lambda x: print(f"WARNING: {x}") # type: ignore
    print_warning_fallback("wall_gen.settings_modules.preset_management.save_preset not found. Using fallback save.")


    try:
        from wall_gen.ai_style_generator import generate_random_style, initialize_gemini as initialize_style_gemini
        AI_STYLE_GEN_AVAILABLE = True
    except ImportError:
        AI_STYLE_GEN_AVAILABLE = False
        def generate_random_style_fallback(style_type="default"): return {"name": "Random Fallback Style"} # type: ignore
        def initialize_style_gemini_fallback(api_key): pass # type: ignore
        generate_random_style = generate_random_style_fallback # type: ignore
        initialize_style_gemini = initialize_style_gemini_fallback # type: ignore
        import traceback
        def print_warning_fallback(msg):
            print(f"WARNING: {msg}")
            print("Traceback for import failure:")
            traceback.print_exc()
        print_warning_fallback("Could not import ai_style_generator. AI style generation feature disabled.")




class PresetGenerator:
    def __init__(self, style_categorizer: StyleCategorizer,
                 prompt_builder: PresetPromptBuilder,
                 preset_cache_manager: PresetCacheManager):
        self.style_categorizer = style_categorizer
        self.prompt_builder = prompt_builder
        self.preset_cache_manager = preset_cache_manager
        self.gemini_available = GEMINI_AVAILABLE
        if not self.gemini_available:
            print_error("PresetGenerator: Gemini AI library is not available. Generation will likely fail.")

    def _get_base_style_for_preset(self, user_prefs: Any, base_style_override: Optional[str]) -> Optional[str]:
        """
        Determines the base style for preset generation.
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
            help_context_id="AI_PRESET_STYLE_SOURCE_CHOICE" # Assuming get_validated_input handles this
        )

        if choice == "_HELP_SHOWN_": # Assuming get_validated_input might return this
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
            if not initialize_style_gemini(None): # type: ignore
                print_error("Failed to initialize Gemini for AI style generation (via wall_gen.ai_style_generator).")
                return None
            style_obj = generate_random_style(style_type="detailed") # type: ignore
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

    def _process_gemini_preset_response(self, json_str: str, base_style: str, style_category: str) -> Optional[Dict[str, Any]]:
        """
        Parses the JSON string from Gemini, validates it, and refines the settings.
        """
        try:
            template = get_template_for_category(style_category)
            if not template or not isinstance(template, dict):
                logging.warning(f"Template for {style_category} missing or invalid in _process_gemini_preset_response. Using minimal fallback.")
                template = {
                    "preset_name": f"{base_style.replace('_',' ').title()} Default",
                    "styles": [base_style], "moods": ["Neutral"],
                    "description": f"Default preset for {base_style}.", "aspect_ratio": "16:9",
                    "imagen_settings": {"negative_prompt": "low quality", "style_negative_prompt": "clashing styles"}
                }

            generated_settings = json.loads(json_str)
            final_preset = {"styles": [base_style]}

            final_preset["preset_name"] = generated_settings.get("preset_name", template.get("preset_name", f"{base_style.replace('_',' ').title()} Fallback Preset"))
            
            moods = generated_settings.get("moods", template.get("moods", ["Neutral"]))
            if not isinstance(moods, list) or not moods or not isinstance(moods[0], str):
                final_preset["moods"] = template.get("moods", ["Neutral"])
            else:
                final_preset["moods"] = [moods[0]]

            final_preset["description"] = generated_settings.get("description", template.get("description", f"AI preset for {base_style}."))
            final_preset["aspect_ratio"] = "16:9"

            ai_imagen = generated_settings.get("imagen_settings")
            template_imagen = template.get("imagen_settings", {})
            import copy # Keep import local if only used here
            merged_imagen_settings = copy.deepcopy(template_imagen)

            if isinstance(ai_imagen, dict):
                deep_update(merged_imagen_settings, ai_imagen)
            
            if "camera_settings" in template_imagen or ("camera_settings" in ai_imagen if isinstance(ai_imagen, dict) else False):
                merged_imagen_settings.setdefault("camera_settings", {})
            
            final_preset["imagen_settings"] = merged_imagen_settings
            
            neg_prompt = final_preset["imagen_settings"].get("negative_prompt", "")
            if not neg_prompt or len(neg_prompt) < 5:
                final_preset["imagen_settings"]["negative_prompt"] = template_imagen.get("negative_prompt", "low quality, blurry")
            
            style_neg_prompt = final_preset["imagen_settings"].get("style_negative_prompt", "")
            if not style_neg_prompt or len(style_neg_prompt) < 5:
                final_preset["imagen_settings"]["style_negative_prompt"] = template_imagen.get("style_negative_prompt", "clashing styles")

            for key, t_value in template.items():
                if key not in final_preset and key != "styles":
                    final_preset[key] = generated_settings.get(key, t_value)
            
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
        except Exception as e:
            logging.error(f"Unexpected error in _process_gemini_preset_response: {e}", exc_info=True)
            print_error(f"Unexpected error processing AI response: {e}")
            return None


    def _save_generated_preset(self, final_preset: Dict[str, Any], auto_save_flag: bool) -> Union[str, bool, None]:
        """
        Handles the saving process for a generated preset.
        """
        if not self.preset_cache_manager.is_preset_unique(final_preset):
           print_warning("Generated preset is too similar to a previous one.")
           return False

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
                confirm_decision = False
            else:
                confirm_decision = confirm_input.startswith('y')

        if confirm_decision:
            self.preset_cache_manager.save_preset_hash_to_cache(final_preset)
            clean_preset_name = re.sub(r'[^\w\s-]', '', final_preset["preset_name"]).strip().replace(' ', '_')
            preset_name_base = f"{clean_preset_name.lower()}_{int(time.time())}"
            
            success = save_preset(final_preset, preset_name_base) # Uses imported or fallback save_preset
            if success:
                print_success(f"Generated unique preset: '{final_preset['preset_name']}'")
                print_success(f"Saved preset '{preset_name_base}' to presets folder and database")
                return preset_name_base
            else:
                print_error(f"Failed to save preset '{preset_name_base}'")
                return None
        else:
            print_warning("Preset saving cancelled by user.")
            return None

    def generate_ai_preset(self, user_prefs: Any, base_style_override: Optional[str] = None, auto_save_flag: bool = False) -> Union[str, bool, None]:
        """
        Orchestrates the generation of an AI-driven wallpaper preset.
        """
        if not self.gemini_available: # Check instance variable
            print_error("Gemini AI library is not available. This script requires 'google-generativeai'.")
            return False # Cannot proceed

        if not is_preset_gemini_initialized():
            if not initialize_preset_gemini(): # Assumes API key is in env or handled by this call
                print_error(f"Failed to initialize Gemini for preset generation: {get_preset_last_error()}")
                print_error("Ensure GEMINI_API_KEY environment variable is set.")
                return False
            logging.info("Gemini API initialized for preset generation via gemini_config_preset.")

        # CATALOG_AND_TEMPLATES_AVAILABLE check is implicitly handled by prompt_builder and _process_gemini_preset_response

        base_style_name = self._get_base_style_for_preset(user_prefs, base_style_override)
        if not base_style_name:
            return None if base_style_name is None else False

        try:
            if base_style_override and base_style_override == base_style_name:
                normalized_category_key = base_style_override.lower().replace(' ', '_').replace('-', '_')
                normalized_category_key = re.sub(r'_+', '_', normalized_category_key)
                style_category = normalized_category_key
                print_info(f"\nUsing CLI/override specified style '{base_style_name}', normalized to category key: '{style_category}' for preset generation.")
            else:
                print_info(f"\nGenerating settings for style: '{base_style_name}'...")
                style_category = self.style_categorizer.categorize_style(base_style_name)
                print_info(f"(Detected category: {style_category})")

            selected_model_name = get_selected_preset_model(user_prefs)
            try:
                model = genai.GenerativeModel(selected_model_name) # type: ignore
                print_info(f"Using selected Gemini model for presets: {selected_model_name}...")
            except Exception as err:
                logging.error(f"Failed to initialize Gemini model '{selected_model_name}': {err}")
                print_error(f"Could not initialize AI model '{selected_model_name}'. Check configuration.")
                return False
            
            prompt = self.prompt_builder.build_preset_generation_prompt(base_style_name, style_category)
            if "Error: PresetPromptBuilder dependencies" in prompt: # Check if prompt builder failed
                print_error(prompt)
                return False

            for attempt in range(config.MAX_GENERATION_ATTEMPTS): # Use config
                print_info(f"Generating settings (Attempt {attempt + 1}/{config.MAX_GENERATION_ATTEMPTS})...")
                try:
                    safety_settings = {
                        genai_types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai_types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE, # type: ignore
                        genai_types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai_types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE, # type: ignore
                        genai_types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai_types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE, # type: ignore
                        genai_types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai_types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE, # type: ignore
                    }
                    generation_config_obj = genai.types.GenerationConfig(temperature=0.75, top_p=0.95, top_k=40) # type: ignore
                    response = model.generate_content(prompt, generation_config=generation_config_obj, safety_settings=safety_settings) # type: ignore

                    if response and response.candidates and response.candidates[0].content.parts:
                        response_text = response.candidates[0].content.parts[0].text.strip()
                        json_match = re.search(r'```json\s*(\{.*?\})\s*```|(\{.*?\})', response_text, re.DOTALL)
                        if json_match:
                            json_str = json_match.group(1) or json_match.group(2)
                            final_preset = self._process_gemini_preset_response(json_str, base_style_name, style_category)
                            
                            if final_preset:
                                save_result = self._save_generated_preset(final_preset, auto_save_flag)
                                if save_result is True or isinstance(save_result, str):
                                    return save_result
                                elif save_result is False:
                                    if attempt == config.MAX_GENERATION_ATTEMPTS - 1:
                                        print_error(f"Failed to generate a unique preset after {config.MAX_GENERATION_ATTEMPTS} attempts.")
                                        return False
                                    time.sleep(1)
                                    continue 
                                else: 
                                    return None 
                            else:
                                if attempt == config.MAX_GENERATION_ATTEMPTS - 1: return False
                                time.sleep(1)
                                continue
                        else:
                            logging.warning(f"Could not extract JSON from response (Attempt {attempt+1}). Response: {response_text}")
                            print_warning(f"AI response format was unexpected (Attempt {attempt + 1}).")
                    elif response and response.prompt_feedback and response.prompt_feedback.block_reason:
                         block_reason = response.prompt_feedback.block_reason
                         logging.warning(f"Generation blocked by API. Reason: {block_reason} (Attempt {attempt + 1})")
                         print_warning(f"Generation blocked (Reason: {block_reason}). Retrying...")
                    else:
                        logging.warning(f"Received no valid response or candidates (Attempt {attempt+1}). Full response: {response}")
                        print_warning(f"AI returned an empty or invalid response (Attempt {attempt + 1}).")

                    if attempt == config.MAX_GENERATION_ATTEMPTS - 1:
                        print_error(f"Failed to generate a valid preset after {config.MAX_GENERATION_ATTEMPTS} attempts due to API issues or response format.")
                        return False
                    time.sleep(1 if not (response and response.prompt_feedback and response.prompt_feedback.block_reason) else (2 + attempt * 2) )
                    continue

                except genai_types.StopCandidateException as stop_err: # type: ignore
                     logging.warning(f"Generation stopped by API (StopCandidateException): {stop_err} (Attempt {attempt + 1})")
                     print_warning(f"Generation stopped by API: {stop_err}. Retrying...")
                     if attempt == config.MAX_GENERATION_ATTEMPTS - 1: return False
                     time.sleep(2 + attempt * 2)
                     continue
                except Exception as api_err:
                    err_str = str(api_err).lower()
                    if "api key not valid" in err_str or "authentication" in err_str:
                         logging.error(f"Authentication error: {api_err}")
                         print_error("Authentication error. Check your GEMINI_API_KEY.")
                         return False 
                    elif "rate limit" in err_str or "429" in err_str or "resource has been exhausted" in err_str:
                        logging.warning(f"Rate limit or resource exhaustion: {api_err}. Waiting... (Attempt {attempt + 1})")
                        print_warning("API rate limit reached or resource exhausted. Waiting before retry...")
                        if attempt == config.MAX_GENERATION_ATTEMPTS - 1: return False
                        time.sleep(10 + attempt * 10)
                        continue
                    else:
                        logging.error(f"Generation failed with an unexpected API error: {api_err} (Attempt {attempt + 1})", exc_info=True)
                        print_error(f"Failed to generate settings due to an API error: {api_err}")
                        if attempt == config.MAX_GENERATION_ATTEMPTS - 1: return False
                        time.sleep(2)
                        continue
            
            print_error(f"Failed to generate a unique and valid preset after all {config.MAX_GENERATION_ATTEMPTS} attempts.")
            return False

        except Exception as e:
            logging.exception("An unexpected error occurred during AI preset generation:")
            print_error(f"An unexpected error occurred: {e}")
            return False
