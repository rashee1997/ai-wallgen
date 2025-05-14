#!/usr/bin/env python3
"""Random Prompt Generator Module - Functions for generating random AI wallpaper prompts

This module contains functions for generating random prompts using tags and style mixes,
utilizing the latest Google Generative AI SDK.
"""
import logging
import os
import random
import re
from typing import Dict, List, Optional, Any, Union, Tuple, Set # Retained from original

# Third-party imports for the new Google Generative AI SDK
try:
    from google import genai  # New SDK import style
    from google.genai import types # Import types for consistency with original usage
except ImportError:
    logging.warning(
        "The 'google-genai' SDK (specifically 'from google import genai') could not be imported. "
        "AI-powered prompt enhancement features will be disabled or may not function correctly."
    )
    # Define placeholders if the import fails
    genai = None
    types = None # Placeholder for google.genai.types

# Import types from the current package
from .types import SimplePrefs # Assuming this exists
# Import centralized Gemini configuration
from .. import gemini_config # Assuming this exists

# Import utilities
from .formatters import enforce_prompt_format # Assuming this exists
from .tag_utils import select_random_tags # Assuming this exists

def generate_prompt_random(tags: List[str], user_prefs: Optional[Any] = None) -> str:
    """Generate a random prompt using the provided tags, potentially enhanced by Gemini.
    
    Args:
        tags: List of tags to include in the prompt.
        user_prefs: Optional user preferences object.
    
    Returns:
        str: A prompt for image generation. The prompt returned by this function
             is the core descriptive text. Final formatting (adding resolution,
             aspect ratio, and negative prompts) is expected to be done by
             the calling function using `enforce_prompt_format`.
    """

    # Helper function to clean Gemini's output
    def _cleanup_text_from_gemini(text: str) -> str:
        # Remove resolution and aspect ratio mentions
        text = re.sub(r'\b\d+x\d+\s+resolution\b[.,\s]*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\b\d+:\d+\s+aspect\s+ratio\b[.,\s]*', '', text, flags=re.IGNORECASE)
        # Remove "Avoid:" clauses
        text = re.sub(r'\bAvoid\s*:[^\n]*', '', text, flags=re.IGNORECASE)
        # Remove potential "TAGS PROVIDED:" or initial tag lists
        text = re.sub(r'^TAGS\s+PROVIDED\s*:[^\n]*\n*', '', text, flags=re.IGNORECASE | re.MULTILINE)
        # Remove any leading tag lists or comma-separated tags at the start of the text
        text = re.sub(r'^(?:[\w\s,-]+,)+[\w\s,-]+\s*', '', text, flags=re.IGNORECASE)
        # Remove multiple newlines and join lines into a single paragraph
        text = " ".join(text.splitlines()).strip().strip('.').strip()
        return text

    resolution = "7680x4320" # Default, might be overridden by user_prefs
    aspect_ratio = "16:9"   # Default, might be overridden by user_prefs
    negative_prompt_default = "ugly, disfigured, low quality, blurry, nsfw, watermark, signature, out of frame, extra limbs, poorly drawn face, twisted limbs, distorted face, bad proportions, bad anatomy"
    current_negative_prompt = negative_prompt_default # Initialize with default

    formatted_tags = ", ".join(tags) if tags else "a beautiful scene" # Ensure formatted_tags is not empty
    prompt_fallback = f"{formatted_tags}, artistic" # Basic fallback

    try:
        from .core import use_user_preferences # Assuming this exists

        if user_prefs is None and use_user_preferences:
            try:
                from ..settings_modules import get_preferences # Assuming this exists
                user_prefs = get_preferences()
            except ImportError:
                logging.warning("Unable to import get_preferences from ..settings_modules. Proceeding without global user preferences.")
                user_prefs = None
        # Path 1: No user preferences are to be used
        if not use_user_preferences and user_prefs is None:
            logging.info("Generating random prompt without specific user preferences.")
            current_user_prefs_for_model = SimplePrefs(
                aspect_ratio=aspect_ratio, 
                imagen_settings={
                    "quality_settings": {"resolution": resolution}, 
                    "negative_prompt": current_negative_prompt 
                }
            )
            
            gemini_instructions_no_prefs = f"""
You will be given a list of tags: "{formatted_tags}".
Your primary task is to transform these tags into a single, cohesive, and vivid descriptive paragraph suitable for an image generation model.
Weave these tags into a natural, flowing narrative, creating a unified scene.
Your generated output should be ONLY the creative descriptive paragraph.
DO NOT include any tags, technical specifications like resolution, aspect ratio, or any 'Avoid:' clauses in YOUR response. These will be handled by the system separately.
Incorporate terms like "high-quality," "detailed," "masterpiece," "sharp focus," "vivid colors" to guide towards better results if appropriate for the scene.
Your output MUST NOT repeat the tags or any technical details.
"""
            
            if not gemini_config.is_initialized():
                if not gemini_config.initialize_gemini_globally():
                    logging.error(f"Gemini not initialized for random prompt (no_prefs path): {gemini_config.get_last_error()}")
                    return prompt_fallback 

            selected_model_name = gemini_config.get_selected_gemini_model(current_user_prefs_for_model)
            logging.info(f"Using Gemini model for random prompt enhancement (no_prefs path): {selected_model_name}")
                
            try:
                client = gemini_config.get_gemini_client()
                if client is None or genai is None:
                    logging.error("Gemini client or SDK not initialized/imported, cannot generate random prompt (no_prefs path).")
                    return prompt_fallback

                response = client.models.generate_content(
                    model=selected_model_name,
                    contents=gemini_instructions_no_prefs 
                )

                if hasattr(response, 'text') and response.text:
                    raw_gemini_text = response.text.strip()
                    enhanced_descriptive_text = _cleanup_text_from_gemini(raw_gemini_text)
                    if not enhanced_descriptive_text:
                        logging.warning("Gemini returned empty description after cleanup for random (no_prefs). Falling back.")
                        return prompt_fallback
                    return enhanced_descriptive_text 
                else:
                    logging.warning("Gemini response issue for random (no_prefs). Falling back.")
                    return prompt_fallback
            except Exception as e:
                logging.error(f"Error generating prompt with Gemini (no_prefs path): {str(e)}", exc_info=True)
                return prompt_fallback
        
        # Path 2: User preferences are enabled or provided
        logging.info("Generating random prompt using user preferences.")
        
        if user_prefs is None: 
            logging.warning("User preferences object is None, but preferences are to be used. Using minimal defaults for Gemini call.")
            user_prefs = SimplePrefs(
                aspect_ratio="16:9",
                imagen_settings={"quality_settings": {"resolution": "3840x2160"}, "negative_prompt": negative_prompt_default}
            )

        style = getattr(user_prefs, 'preferred_styles', [None])[0]
        mood = getattr(user_prefs, 'preferred_moods', [None])[0]
        settings = getattr(user_prefs, 'imagen_settings', {})

        camera_settings = settings.get("camera_settings", {})
        camera_model = camera_settings.get("camera_model")
        lens_type = camera_settings.get("lens_type")
        aperture = camera_settings.get("aperture")
        special_lens = camera_settings.get("special_lens")
        depth_of_field = camera_settings.get("depth_of_field")
        focal_length = camera_settings.get("focal_length")
        shutter_speed = camera_settings.get("shutter_speed")
        iso = camera_settings.get("iso")
        filter_type = camera_settings.get("filter_type")

        lighting_settings = settings.get("lighting_settings", {})
        time_of_day = lighting_settings.get("time_of_day")
        lighting_type = lighting_settings.get("lighting_type")
        light_source = lighting_settings.get("light_source")
        light_quality = lighting_settings.get("light_quality")
        artificial_sources = lighting_settings.get("artificial_sources", [])

        composition_settings = settings.get("composition_settings", {})
        technique = composition_settings.get("technique")
        camera_angle = composition_settings.get("camera_angle")
        visual_flow = composition_settings.get("visual_flow")
        depth_layering = composition_settings.get("depth_layering")
        focal_point = composition_settings.get("focal_point")
        perspective = composition_settings.get("perspective")

        environment_settings = settings.get("environment_settings", {})
        weather = environment_settings.get("weather")
        season = environment_settings.get("season")
        location_type = environment_settings.get("location_type")
        atmospheric_effects = environment_settings.get("atmospheric_effects", [])

        style_settings = settings.get("style_settings", {})
        art_movement = style_settings.get("art_movement")
        style_era = style_settings.get("style_era")
        post_processing = style_settings.get("post_processing", [])

        detail_settings = settings.get("detail_settings", {})
        detail_level = detail_settings.get("detail_level")
        texture_quality = detail_settings.get("texture_quality")
        special_effects = detail_settings.get("special_effects", [])

        color_settings = settings.get("color_settings", {})
        color_scheme = color_settings.get("color_scheme")
        palette_type = color_settings.get("palette_type")
        color_temperature = color_settings.get("color_temperature")

        quality_settings = settings.get("quality_settings", {})
        resolution = quality_settings.get("resolution", resolution) 
        rendering_quality = quality_settings.get("rendering_quality")
        aspect_ratio = getattr(user_prefs, 'aspect_ratio', aspect_ratio) 

        digital_settings = settings.get("digital_settings", {})
        digital_software = digital_settings.get("software", "")
        digital_effects = digital_settings.get("digital_effects", [])
        game_engine_settings = settings.get("game_engine_settings", {})
        game_engine = game_engine_settings.get("engine_type", "")
        game_genre = game_engine_settings.get("game_genre", "")
        game_shader = game_engine_settings.get("shader_type", "")
        software_settings = settings.get("software_settings", {})
        suite = software_settings.get("suite")
        renderer = software_settings.get("renderer")
        version = software_settings.get("version")
        medium_settings = settings.get("medium_settings", {})
        painting_medium = medium_settings.get("painting_medium", "")
        brushwork = medium_settings.get("brushwork", "")
        texture = medium_settings.get("texture", "")
        illustration_settings = settings.get("illustration_settings", {})
        illustration_style = illustration_settings.get("style", "")
        line_quality = illustration_settings.get("line_quality", "")
        abstract_settings = settings.get("abstract_settings", {})
        abstract_composition = abstract_settings.get("composition_type", "")
        movement_type = abstract_settings.get("movement_type", "")
        material_settings = settings.get("material_settings", {})
        material_type = material_settings.get("material_type", "")
        material_finish = material_settings.get("finish", "")
        
        current_negative_prompt = settings.get("negative_prompt", negative_prompt_default)
        if not current_negative_prompt: 
            current_negative_prompt = negative_prompt_default

        try:
            from ..config import PROMPT_INSTRUCTIONS 
        except ImportError:
            logging.warning("Could not import PROMPT_INSTRUCTIONS from ..config. Using a basic fallback.")
            PROMPT_INSTRUCTIONS = "Create an image based on: {formatted_tags}. Style: {style}, Mood: {mood}. Details: {instruction_context}"

        # This instruction_context_simple seems less used if gemini_instructions_with_prefs is the main one.
        # Ensure all keys are present for the .format() call.
        instruction_context_simple = PROMPT_INSTRUCTIONS.format(
            resolution=resolution if resolution else "Not specified",
            aspect_ratio=aspect_ratio if aspect_ratio else "Not specified",
            color_scheme=color_scheme if color_scheme else "Not specified",
            lighting=lighting_type if lighting_type else "Not specified", 
            composition=technique if technique else "Not specified",     
            depth_of_field=depth_of_field if depth_of_field else "Not specified",
            style_context=f"Style: {style if style else 'N/A'}, Mood: {mood if mood else 'N/A'}", 
            formatted_tags=formatted_tags,
            style=style if style else "appropriate", # Added for placeholder if PROMPT_INSTRUCTIONS uses it
            mood=mood if mood else "fitting" # Added for placeholder
        )

        gemini_instructions_with_prefs = f"""
As an expert prompt engineer, your task is to craft a single, vivid, and highly descriptive paragraph for an AI image generator.
The core subject elements to be woven into this scene are: "{formatted_tags}".

Your primary mission is to create a captivating visual narrative that *prominently features the user's chosen artistic style and mood*, while seamlessly integrating the input tags.
Do not just list tags or preference keywords. Synthesize them into a rich, imaginative scene that *clearly embodies* the specified style.
Think like an art director guiding a concept artist.

Input Tags (to be woven into the scene): {formatted_tags}

User Preferences (these are CRITICAL guides for the artistic direction):
- **Primary Artistic Style**: "{style if style else "An artistically fitting style should be chosen based on tags and mood."}" - This style MUST be evident in your description. Use descriptive language characteristic of this style.
- **Desired Emotional Atmosphere/Mood**: "{mood if mood else "Evocative and fitting for the scene."}" - The overall feeling of the scene should strongly reflect this mood.
- **Art Movement Influence** (if specified): "{art_movement if art_movement else "None specific; focus on the primary style."}" - If an art movement is named, the scene should clearly echo its characteristics.
- **Historical Era Feel** (if specified): "{style_era if style_era else "Timeless or modern, as appropriate for the style."}" - If an era is named, let it influence the setting and details.

Other Guiding Details (use these to enrich the scene *within the chosen style*):
- Lighting Impression: The lighting ({lighting_type if lighting_type else "natural"}, {light_quality if light_quality else "clear"}) should enhance the specified style and mood. Time of day: {time_of_day if time_of_day else "chosen to best suit style/mood"}.
- Color Story: The colors ({color_scheme if color_scheme else "harmonious"}, {palette_type if palette_type else "expressive"}) should strongly support the chosen style and mood. Color temperature: {color_temperature if color_temperature else "fitting"}.
- Compositional Sense: The composition ({technique if technique else "engaging"}) should serve the style and draw attention to {focal_point if focal_point else "the main subject derived from tags"}. Camera Angle: {camera_angle if camera_angle else "fitting"}. Perspective: {perspective if perspective else "natural"}.
- Detail & Texture: Details ({detail_level if detail_level else "appropriate"}) and textures ({texture_quality if texture_quality else "fitting"}) must align with and enhance the chosen artistic style. Special Effects: {", ".join(special_effects) if special_effects else "None"}.
- Environment: Weather: {weather if weather else "fitting"}. Season: {season if season else "appropriate"}. Location Type: {location_type if location_type else "suitable backdrop"}. Atmospheric Effects: {", ".join(atmospheric_effects) if atmospheric_effects else "clear air"}.
- Camera (if photographic/cinematic style): Model: {camera_model if camera_model else "N/A"}. Lens: {lens_type if lens_type else "N/A"} ({focal_length if focal_length else "N/A"}). Aperture: {aperture if aperture else "N/A"}. Shutter: {shutter_speed if shutter_speed else "N/A"}. ISO: {iso if iso else "N/A"}. Filter: {filter_type if filter_type else "N/A"}. Special Lens: {special_lens if special_lens else "N/A"}. Depth of Field: {depth_of_field if depth_of_field else "natural"}.

Specific Art Style Details (if provided, these are KEY to describing the style accurately):
- Digital Art: If the style is digital, mention qualities related to "{digital_software}" or effects like "{', '.join(digital_effects if digital_effects else ['N/A'])}".
- Game Art: If game-related, describe it as if from a "{game_genre}" game, perhaps using "{game_engine}" visuals with "{game_shader}" shaders.
- Traditional Medium: If a traditional medium like "{painting_medium}" is chosen, describe the "{brushwork}" and "{texture}" of the medium.
- Illustration: If an "{illustration_style}" is chosen, describe the "{line_quality}".
- Abstract: For abstract styles, focus on "{abstract_composition}" and "{movement_type}".
- Materials: If specific materials like "{material_type}" with a "{material_finish}" finish are relevant to the style, describe them.
- Post-Processing: Effects like {", ".join(post_processing) if post_processing else "None"}.

Creative Mandate:
1.  Weave all "{formatted_tags}" into a single, flowing narrative paragraph.
2.  The User's **Primary Artistic Style and Mood** MUST be the dominant characteristics of your description. Use adjectives and verbs that clearly evoke this style.
3.  All other preferences should serve to enrich this primary style.
4.  The output MUST be a single descriptive paragraph.
5.  DO NOT include the original tags list, resolution, aspect ratio, or any "Avoid:" clauses in YOUR response. These are handled separately.

Example (Tags: "cityscape, rain, neon lights". Prefs: Style="Cyberpunk", Mood="Melancholic", Lighting="Reflective wet surfaces"):
"A melancholic cyberpunk cityscape unfolds, drenched in a persistent, cold rain. Towering, oppressive skyscrapers, adorned with flickering holographic advertisements, disappear into the smog-choked upper atmosphere. Neon lights from countless signs bleed across the rain-slicked streets, their vibrant blues, pinks, and electric greens reflecting in puddles that mirror the desolation. The scene evokes a sense of lonely beauty and technological decay, characteristic of the cyberpunk genre, with a focus on the reflective interplay of light on wet, metallic surfaces."

Now, generate the prompt for the tags: "{formatted_tags}", ensuring the user's stylistic preferences are paramount.
"""
        
        if not gemini_config.is_initialized():
            if not gemini_config.initialize_gemini_globally():
                logging.error(f"Gemini not initialized for random prompt (user_prefs path): {gemini_config.get_last_error()}")
                return prompt_fallback 

        selected_model_name = gemini_config.get_selected_gemini_model(user_prefs) 
        logging.info(f"Using Gemini model for random prompt (user_prefs path): {selected_model_name}")

        try:
            client = gemini_config.get_gemini_client()
            if client is None or genai is None:
                logging.error("Gemini client or SDK not initialized/imported, cannot generate random prompt (user_prefs path).")
                return prompt_fallback

            response = client.models.generate_content( 
                model=selected_model_name,
                contents=gemini_instructions_with_prefs 
            )

            if hasattr(response, 'text') and response.text:
                raw_gemini_text = response.text.strip()
                enhanced_descriptive_text = _cleanup_text_from_gemini(raw_gemini_text)
                if not enhanced_descriptive_text:
                    logging.warning("Gemini returned empty description after cleanup for random (user_prefs). Falling back.")
                    return prompt_fallback
                return enhanced_descriptive_text 
            else:
                logging.warning("Gemini response issue for random (user_prefs). Falling back.")
                return prompt_fallback
        except Exception as e:
            logging.error(f"Error generating prompt with Gemini (user_prefs path): {str(e)}", exc_info=True)
            return prompt_fallback
            
    except Exception as e: # Catching potential import errors for .core or other broad issues
        logging.error(f"Outer error in generate_prompt_random: {str(e)}", exc_info=True)
        # Fallback logic for when user_prefs might not be available or other setup issues
        final_resolution = "3840x2160"
        final_aspect_ratio = "16:9"
        final_negative_prompt = negative_prompt_default # Use the module default

        # Try to get from user_prefs if it was defined before the error
        if 'user_prefs' in locals() and user_prefs is not None: 
            if hasattr(user_prefs, 'imagen_settings') and isinstance(getattr(user_prefs, 'imagen_settings', None), dict):
                quality_settings = user_prefs.imagen_settings.get("quality_settings", {})
                final_resolution = quality_settings.get("resolution", final_resolution)
                final_negative_prompt = user_prefs.imagen_settings.get("negative_prompt", final_negative_prompt)
            if hasattr(user_prefs, 'aspect_ratio') and getattr(user_prefs, 'aspect_ratio', None):
                final_aspect_ratio = user_prefs.aspect_ratio
        
        formatted_tags_str = ", ".join(tags) if tags else "random artistic scene"
        # This function should return the core descriptive text.
        # If all else fails, return the basic formatted tags.
        # The caller will handle enforce_prompt_format.
        return formatted_tags_str


def generate_random_style_mix(user_prefs=None) -> str:
    """Generate a random mix of artistic styles.
    
    This function combines styles from different categories to create unique
    style combinations for image generation prompts.
    
    Args:
        user_prefs: Optional user preferences object.
    
    Returns:
        str: A string containing a combination of artistic styles, joined with " + "
    """
    try:
        from .core import use_user_preferences 
        
        if user_prefs is None and use_user_preferences:
            try:
                from ..settings_modules import get_preferences 
                user_prefs = get_preferences()
            except ImportError:
                logging.warning("Unable to import get_preferences from ..settings_modules for style mix.")
                user_prefs = None
            
        default_style_categories = {
            "traditional_art": ["art_deco", "art_nouveau", "charcoal", "expressionism", 
                                "gothic", "impressionism", "oil_painting", "pastel", 
                                "pencil_sketch", "realism", "sketch", "watercolor", "woodcut"],
            "digital_art": ["abstract", "cinematic", "cyberpunk", "digital_art", "double_exposure", 
                            "fantasy", "futurism", "glitch_art", "hyperrealism", "isometric", 
                            "landscape", "low_poly", "minimalist", "retrowave", "sci_fi",
                            "stained_glass", "steampunk", "surrealism", "vaporwave"],
            "illustration": ["anime", "cartoon", "comic_book", "divisionism", "graffiti", 
                             "ink_drawing", "line_art", "manga", "paper_cut", "pixel_art", 
                             "pointillism", "pop_art", "ukiyo_e"]
        }
        
        custom_style_categories = {}
        if user_prefs and hasattr(user_prefs, 'imagen_settings'):
            settings = getattr(user_prefs, 'imagen_settings', {}) 
            if isinstance(settings, dict):
                style_settings = settings.get("style_settings", {})
                if isinstance(style_settings, dict):
                     custom_style_categories = style_settings.get("style_categories", {})
        
        categories_to_use = custom_style_categories if isinstance(custom_style_categories, dict) and custom_style_categories else default_style_categories
        
        if not categories_to_use: 
            logging.warning("No style categories available for random mix. Falling back.")
            return "digital_art + fantasy"

        category_name = random.choice(list(categories_to_use.keys()))
        available_styles = categories_to_use.get(category_name, [])

        if not available_styles: 
            logging.warning(f"Selected style category '{category_name}' is empty. Falling back.")
            # Try another category or use a hardcoded default
            alt_category_keys = [k for k in categories_to_use.keys() if k != category_name]
            if alt_category_keys: 
                alt_category_name = random.choice(alt_category_keys)
                available_styles = categories_to_use.get(alt_category_name, []) 
                if not available_styles: # If the alternative is also empty
                    available_styles = ["digital_art", "fantasy"]
            else: 
                 available_styles = ["digital_art", "fantasy"] 
        
        num_styles_to_select = random.randint(2, 3)
        # Ensure num_styles_to_select is not greater than the number of available styles
        if len(available_styles) < num_styles_to_select:
            num_styles_to_select = len(available_styles)
        
        # Ensure num_styles_to_select is at least 1 if styles are available, or handle empty available_styles
        if not available_styles: # If after all fallbacks, available_styles is empty
            selected_styles = ["digital_art", "fantasy"] # Ultimate fallback
        elif num_styles_to_select == 0 and available_styles: # Should not happen if len(available_styles) >= num_styles_to_select
            selected_styles = [random.choice(available_styles)] # Pick at least one if available
        elif num_styles_to_select == 0 and not available_styles:
            selected_styles = ["digital_art", "fantasy"]
        else:
             selected_styles = random.sample(available_styles, num_styles_to_select)

        return " + ".join(selected_styles)
    except Exception as e:
        logging.error(f"Error in generate_random_style_mix: {str(e)}", exc_info=True)
        return "digital_art + fantasy" 

