# wall_gen/prompt_service.py
"""
Service module for all prompt generation logic.
NOTE: This module uses absolute imports assuming it's part of the 'wall_gen' package.
It may not run correctly as a standalone script without sys.path adjustments.
"""
import logging
import random
import os
import google.generativeai as genai
import hashlib # Added for cache key hashing
from . import gemini_config # Import the new centralized configuration
# from wallpaper_settings import get_preferences # If UserPreferences needed directly

# Use absolute imports for modules within the wall_gen package
try:
    from wall_gen.cache_utils import prompt_cache # For LRUCache instance
    from wall_gen.config import (
        PROMPT_INSTRUCTIONS, CUSTOM_PROMPT_INSTRUCTIONS,
        nature_tags, space_tags, sea_tags, flowers_tags, urban_tags,
        fantasy_tags, abstract_tags, mood_tags, style_to_tags, STYLE_CATEGORIES
    )
    # Functions from prompt_generator.py using absolute import
    from wall_gen.prompt_generator import ( # This seems to be an alias or older structure
        enhance_custom_prompt as old_enhance_custom_prompt, # aliasing to avoid conflict if used elsewhere
        enforce_prompt_format, # This is likely wall_gen.prompt_modules.formatters.enforce_prompt_format
        set_prompt_preferences, 
        use_user_preferences, 
        enhance_negative_prompt,
    )
    # Explicitly import from the new modules structure
    from wall_gen.prompt_modules.custom_generator import enhance_custom_prompt
    from wall_gen.prompt_modules.random_generator import generate_prompt_random
except ImportError:
    # This block is reached if 'wall_gen' is not in sys.path or not installed.
    # Critical dependencies are missing.
    logging.critical("Core imports (cache_utils, config, prompt_generator) failed in prompt_service.py. "
                     "Ensure 'wall_gen' package is correctly installed and in PYTHONPATH.")
    # Define dummy/fallback versions of critical components if possible, or raise an error.
    # For this example, we'll let subsequent NameErrors occur if these aren't found,
    # as the module is unlikely to function.
    class DummyCache:
        def __contains__(self, key): return False
        def __getitem__(self, key): raise KeyError
        def __setitem__(self, key, value): pass
    prompt_cache = DummyCache()
    PROMPT_INSTRUCTIONS, CUSTOM_PROMPT_INSTRUCTIONS = "", ""
    nature_tags, space_tags, sea_tags, flowers_tags, urban_tags = [], [], [], [], []
    fantasy_tags, abstract_tags, mood_tags, style_to_tags, STYLE_CATEGORIES = [], [], [], {}, {}
    def enhance_custom_prompt(p, up=None): return p
    def enforce_prompt_format(p, r, ar, np): return p
    def set_prompt_preferences(v): pass
    def use_user_preferences(): return True
    def enhance_negative_prompt(p, np): return np


# GEMINI_API_KEY and PROMPT_GEMINI_MODEL_NAME are now managed by gemini_config
# Initialization is also handled by gemini_config (auto-init on its import)
# We just need to ensure it's checked before use if not relying on auto-init success.

# Example: Ensure Gemini is initialized before proceeding if critical operations depend on it here.
# if not gemini_config.is_initialized():
#     if not gemini_config.initialize_gemini_globally():
#         logging.error(f"Prompt Service: Failed to initialize Gemini: {gemini_config.get_last_error()}")
# else:
#     logging.info("Prompt Service: Gemini already initialized.")


def flatten_settings(settings, parent_key="", sep=" - ", ignore_keys=None):
    """
    Recursively flatten a settings dictionary. (Moved from wallpaper_generator.py)
    """
    ignore_keys = ignore_keys or set(["negative_prompt"])
    flattened = []
    if not isinstance(settings, dict):
        return flattened
    for k, v in settings.items():
        if k in ignore_keys:
            continue
        pretty_key = k.replace("_", " ").capitalize()
        full_key = f"{parent_key}{sep}{pretty_key}" if parent_key else pretty_key
        if isinstance(v, dict):
            sub = flatten_settings(
                v, parent_key=full_key, sep=sep, ignore_keys=ignore_keys
            )
            flattened.extend(sub)
        elif isinstance(v, list):
            list_val = ", ".join(str(x) for x in v if x)
            if list_val:
                flattened.append(
                    (parent_key if parent_key else pretty_key, pretty_key, list_val)
                )
        elif v is not None and v != "" and v != "Not specified":
            flattened.append(
                (parent_key if parent_key else pretty_key, pretty_key, str(v))
            )
    return flattened

def dynamic_technical_context(settings, aspect_ratio="16:9", resolution="3840x2160"):
    """
    Build a narrative technical context for prompts. (Moved from wallpaper_generator.py)
    """
    def phrase_from_kv(section, field, value):
        key = field.lower()
        val = str(value)
        if key in [
            "lighting type", "light quality", "color scheme",
            "palette type", "color temperature",
        ]:
            return f"{val} lighting" if "light" in key else f"{val} color palette"
        elif "brush" in key or "painting" in key or "medium" in key or "canvas" in key:
            return f"{val} {key.replace('_',' ')}"
        elif key in ["detail level", "texture quality"]:
            return f"{val} {key.replace('_', ' ')}"
        elif key in ["focal point"]:
            return f"focal point: {val}"
        elif key in ["season", "weather"]:
            return f"{val} conditions"
        elif key in ["post processing", "special effects"]:
            return f"{key.replace('_',' ')} of {val}"
        elif key in ["movement type", "composition type"]:
            return f"{val} composition"
        elif "style" in key and "style era" not in key:
            return f"{val} style"
        elif key == "aspect ratio" or key == "resolution" or key in ("", "none", "not specified"):
            return None
        return f"{val} {key.replace('_', ' ')}"

    flat = flatten_settings(settings)
    phrases = [phrase_from_kv(section, field, value) for section, field, value in flat]
    phrases = [p for p in phrases if p and not p.strip().lower().startswith("none")]
    deduped = []
    for p in phrases:
        if p not in deduped:
            deduped.append(p)
    
    text = "; ".join(deduped) if deduped else ""
    text = text.rstrip("; ")
    if text:
        text += ". "
    text += f"{resolution} resolution, {aspect_ratio} aspect ratio"
    return text

def _build_gemini_prompt_from_settings(tags, user_prefs):
    """
    Generate a detailed prompt using Gemini and user preferences.
    (Refactored from local generate_prompt_gemini in wallpaper_generator.py)
    """
    try:
        if not gemini_config.is_initialized():
            if not gemini_config.initialize_gemini_globally(): # Attempt to initialize
                logging.error(f"Gemini not initialized for _build_gemini_prompt_from_settings: {gemini_config.get_last_error()}")
                # Fallback to a simple prompt if Gemini cannot be used
                formatted_tags_str = ", ".join(tags)
                return enforce_prompt_format(formatted_tags_str, "3840x2160", "16:9", user_prefs.imagen_settings.get("negative_prompt", ""))
        
        # If still not initialized (e.g. no API key), then fallback.
        if not gemini_config.is_initialized():
            logging.warning("Gemini could not be initialized (e.g. no API key). Falling back to basic prompt formatting.")
            formatted_tags_str = ", ".join(tags)
            return enforce_prompt_format(formatted_tags_str, "3840x2160", "16:9", user_prefs.imagen_settings.get("negative_prompt", ""))

        selected_model_name = gemini_config.get_selected_gemini_model(user_prefs)
        logging.info(f"Using Gemini model for prompt building: {selected_model_name}")

        # Consistent cache key generation, now including the selected model name
        cache_key_parts = [str(tags), str(user_prefs.imagen_settings), selected_model_name]
        cache_key = hashlib.sha256("".join(cache_key_parts).encode()).hexdigest()

        if cache_key in prompt_cache:
            logging.info(f"Using cached prompt for key: {cache_key[:10]}...")
            return prompt_cache[cache_key]

        settings = user_prefs.imagen_settings
        aspect_ratio = getattr(user_prefs, "aspect_ratio", "16:9")
        resolution = settings.get("quality_settings", {}).get("resolution", "3840x2160")
        
        style = user_prefs.preferred_styles[0] if user_prefs.preferred_styles else "artist's choice"
        mood = user_prefs.preferred_moods[0] if user_prefs.preferred_moods else "artist's choice"
        art_movement = settings.get("style_settings", {}).get("art_movement", "artist's choice")
        
        formatted_tags = ", ".join(tags)
        all_technical_details = dynamic_technical_context(settings, aspect_ratio, resolution)
        user_negative_prompt = settings.get("negative_prompt", "")
        
        instruction_context = f"""
You are an expert prompt engineer for an AI image generator. Your task is to create a vivid, detailed, and coherent single-paragraph description for a desktop wallpaper.
The main subject of the wallpaper is: "{formatted_tags}".
The desired style is "{style}", mood is "{mood}", and art movement is "{art_movement}".

Incorporate the following technical and artistic specifications naturally into your description:
{all_technical_details}

Guidelines:
1.  Focus on creating a visually striking and aesthetically pleasing image.
2.  The description must be a single, flowing paragraph.
3.  Ensure the subject "{formatted_tags}" remains the central focus.
4.  Adapt style and technical details to suit the subject matter.
5.  The description MUST end with the exact phrase: "{resolution} resolution, {aspect_ratio} aspect ratio".
6.  After the main description, you MUST include a section starting with "Avoid: " followed by elements to exclude.
    The elements to avoid are: {user_negative_prompt if user_negative_prompt else "common artifacts, poor quality, text, watermarks"}.

Example of desired output format:
A breathtaking landscape of {formatted_tags}, bathed in the {settings.get("lighting_settings", {}).get("time_of_day", "golden hour")} light... (many more details)... {resolution} resolution, {aspect_ratio} aspect_ratio.
Avoid: blurry, low quality, text, watermarks, ugly.
---
Now, generate the prompt for: "{formatted_tags}"
"""
        model = genai.GenerativeModel(selected_model_name) # Use selected model
        response = model.generate_content(instruction_context)

        if hasattr(response, 'text') and response.text:
            full_response = response.text.strip()
            final_prompt = enforce_prompt_format(
                full_response, resolution, aspect_ratio, user_negative_prompt
            )
            prompt_cache[cache_key] = final_prompt
            logging.info(f"Generated and cached prompt for key: {cache_key[:10]}...")
            return final_prompt
        else:
            logging.warning(f"Gemini returned empty response for prompt generation. Tags: {tags}")
            # Fallback to basic formatting if Gemini fails
            formatted_tags_str = ", ".join(tags)
            return enforce_prompt_format(formatted_tags_str, resolution, aspect_ratio, user_negative_prompt)

    except Exception as e:
        logging.error(f"Error in _build_gemini_prompt_from_settings: {e}", exc_info=True)
        formatted_tags_str = ", ".join(tags)
        return enforce_prompt_format(formatted_tags_str, "3840x2160", "16:9", user_prefs.imagen_settings.get("negative_prompt", ""))


def _build_random_prompt_from_settings(tags, user_prefs):
    """
    Generate a random prompt. (Refactored from local generate_prompt_random)
    """
    try:
        settings = user_prefs.imagen_settings
        quality_settings = settings.get("quality_settings", {})
        resolution = quality_settings.get("resolution", "3840x2160")
        aspect_ratio = getattr(user_prefs, "aspect_ratio", "16:9")
        negative_prompt = settings.get("negative_prompt", "")

        prompt_parts = list(tags) 

        if user_prefs.preferred_styles:
            prompt_parts.append(random.choice(user_prefs.preferred_styles))
        if user_prefs.preferred_moods:
            prompt_parts.append(random.choice(user_prefs.preferred_moods))

        enhancers = []
        for category, cat_settings in settings.items():
            if isinstance(cat_settings, dict):
                for key, value in cat_settings.items():
                    if key not in ["negative_prompt", "resolution", "number_of_images", "seed"] and value and isinstance(value, (str, int, float)):
                        if random.random() < 0.3: 
                            enhancers.append(str(value))
                    elif isinstance(value, list) and value:
                         if random.random() < 0.3:
                            enhancers.append(random.choice(value))
        
        if enhancers:
            prompt_parts.extend(random.sample(enhancers, min(len(enhancers), random.randint(2,5))))

        raw_prompt = ", ".join(prompt_parts)
        final_prompt = enforce_prompt_format(raw_prompt, resolution, aspect_ratio, negative_prompt)
        return final_prompt
    except Exception as e:
        logging.error(f"Error in _build_random_prompt_from_settings: {e}")
        return enforce_prompt_format(", ".join(tags), "3840x2160", "16:9", "")


def sanitize_prompt_text(prompt):
    """Sanitize prompt text."""
    return prompt.strip() if prompt else ""

def select_random_tags_for_prompt(count_min=3, count_max=6):
    """Select random tags."""
    all_tags_source = (
        nature_tags + space_tags + sea_tags + flowers_tags +
        urban_tags + fantasy_tags + abstract_tags
    )
    if not all_tags_source:
        logging.warning("No tags available in config for random selection.")
        return ["default wallpaper subject"]
        
    num_tags = random.randint(count_min, count_max)
    return random.sample(all_tags_source, min(num_tags, len(all_tags_source)))

def generate_random_style_mix_for_prompt(user_prefs):
    """Generate a random style mix."""
    try:
        # Import ai_style_generator from the root directory
        # Ensure ai_style_generator is also refactored to use gemini_config
        from wall_gen.ai_style_generator import generate_random_style
        if gemini_config.is_initialized(): # Check if Gemini is usable
            # generate_random_style in ai_style_generator now handles its own model selection via gemini_config
            ai_style = generate_random_style() # It will use get_preferences() internally
            if ai_style:
                return ai_style['name'] if isinstance(ai_style, dict) and 'name' in ai_style else str(ai_style)
        else:
            logging.warning("Gemini not initialized, cannot use AI for random style mix.")
    except (ImportError, ModuleNotFoundError, Exception) as e:
        logging.debug(f"AI style generation not available or failed in prompt_service: {e}")

    settings = user_prefs.imagen_settings
    style_settings = settings.get("style_settings", {})
    
    # Use the STYLE_CATEGORIES imported from wall_gen.config
    default_style_categories = STYLE_CATEGORIES
    current_style_categories = style_settings.get("style_categories", default_style_categories)

    if not current_style_categories:
        logging.warning("No style categories found for random mix.")
        return "interesting style"

    category_name = random.choice(list(current_style_categories.keys()))
    available_styles_in_category = current_style_categories[category_name]
    
    if not available_styles_in_category:
        return "unique style"

    num_styles_to_mix = random.randint(1, min(3, len(available_styles_in_category)))
    selected_styles = random.sample(available_styles_in_category, num_styles_to_mix)
    return " + ".join(selected_styles)


def generate_final_prompt(prompt_type, user_prefs, custom_prompt_text=None):
    """Main dispatcher for generating prompts."""
    gemini_generated_prompt = None 
    final_enhanced_prompt = None   

    should_use_prefs = use_user_preferences() if callable(use_user_preferences) else True

    if prompt_type == "custom" and custom_prompt_text:
        logging.info("Processing custom prompt for final generation...")
        sanitized_custom_prompt = sanitize_prompt_text(custom_prompt_text)
        
        if should_use_prefs:
            final_enhanced_prompt = enhance_custom_prompt(sanitized_custom_prompt, user_prefs)
        else:
            final_enhanced_prompt = enhance_custom_prompt(sanitized_custom_prompt)

        if not final_enhanced_prompt:
            logging.warning("Failed to enhance custom prompt, using sanitized original.")
            final_enhanced_prompt = sanitized_custom_prompt
        gemini_generated_prompt = sanitized_custom_prompt 

    elif prompt_type == "random":
        logging.info("Generating random prompt for final generation using 'random_generator.generate_prompt_random'...")
        random_tags = select_random_tags_for_prompt()
        
        # The base prompt for history will be the raw tags
        gemini_generated_prompt = ", ".join(random_tags)

        if should_use_prefs:
            # generate_prompt_random now returns only the descriptive text
            descriptive_text = generate_prompt_random(random_tags, user_prefs)
        else:
            # generate_prompt_random now returns only the descriptive text
            descriptive_text = generate_prompt_random(random_tags, SimplePrefs())
        
        # final_enhanced_prompt is the descriptive text.
        # The calling function in run_wallgen.py (`orchestrate_wallpaper_generation` via `_generate_prompt`)
        # will handle the final formatting with resolution, aspect ratio, and avoid clause using enforce_prompt_format.
        # For clarity, ensure descriptive_text is not None.
        final_enhanced_prompt = descriptive_text if descriptive_text else gemini_generated_prompt

    else: 
        logging.info("Generating AI (Gemini) prompt for final generation...")
        tags_for_gemini = []
        if should_use_prefs and user_prefs.preferred_genres:
            tags_for_gemini.extend(user_prefs.preferred_genres)
        if should_use_prefs and user_prefs.preferred_moods:
             tags_for_gemini.append(f"mood: {random.choice(user_prefs.preferred_moods)}")
        if should_use_prefs and user_prefs.preferred_styles:
             tags_for_gemini.append(f"style: {random.choice(user_prefs.preferred_styles)}")
        if not tags_for_gemini: 
            tags_for_gemini = select_random_tags_for_prompt()

        if should_use_prefs:
            gemini_generated_prompt = _build_gemini_prompt_from_settings(tags_for_gemini, user_prefs)
        else:
            gemini_generated_prompt = _build_gemini_prompt_from_settings(tags_for_gemini, SimplePrefs())

        if not gemini_generated_prompt:
            logging.warning("Gemini prompt generation failed, falling back to random.")
            random_tags_fallback = select_random_tags_for_prompt()
            if should_use_prefs:
                gemini_generated_prompt = _build_random_prompt_from_settings(random_tags_fallback, user_prefs)
            else:
                gemini_generated_prompt = _build_random_prompt_from_settings(random_tags_fallback, SimplePrefs())
        final_enhanced_prompt = gemini_generated_prompt
    
    if not isinstance(final_enhanced_prompt, str):
        logging.error(f"final_enhanced_prompt is not a string: {final_enhanced_prompt}. Falling back.")
        final_enhanced_prompt = "A beautiful wallpaper"
    if not isinstance(gemini_generated_prompt, str) and gemini_generated_prompt is not None:
         gemini_generated_prompt = str(gemini_generated_prompt)

    return final_enhanced_prompt, gemini_generated_prompt


class SimplePrefs:
    """A simple mock for user_prefs if none are to be used."""
    def __init__(self):
        self.imagen_settings = {"negative_prompt": "ugly, blurry, bad quality", "quality_settings": {"resolution":"1920x1080"}}
        self.aspect_ratio = "16:9"
        self.preferred_genres = []
        self.preferred_styles = []
        self.preferred_moods = []
