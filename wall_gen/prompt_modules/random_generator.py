#!/usr/bin/env python3
"""Random Prompt Generator Module - Functions for generating random AI wallpaper prompts

This module contains functions for generating random prompts using tags and style mixes.
"""
import logging
import os
import random
import re
from typing import Dict, List, Optional, Any, Union, Tuple, Set

# Import types
from .types import SimplePrefs
from .. import gemini_config # Added for centralized Gemini config

# Import utilities
from .formatters import enforce_prompt_format
from .tag_utils import select_random_tags

def generate_prompt_random(tags: List[str], user_prefs: Optional[Any] = None) -> str:
    """Generate a random prompt using the provided tags.
    
    Args:
        tags: List of tags to include in the prompt
        user_prefs: Optional user preferences object. If None and use_user_preferences
                    is True, the function will use the global user_prefs.
    
    Returns:
        str: A prompt for image generation
    """
    try:
        from .core import use_user_preferences
        
        if user_prefs is None and use_user_preferences:
            try:
                from ..settings_modules import get_preferences
                user_prefs = get_preferences()
            except ImportError:
                logging.warning("Unable to import get_preferences from ..settings_modules.")
                user_prefs = None
            
        if not use_user_preferences and user_prefs is None:
            user_prefs = SimplePrefs(
                aspect_ratio="16:9",
                imagen_settings={
                    "quality_settings": {"resolution": "7680x4320"},
                    "negative_prompt": "ugly, disfigured, low quality, blurry, nsfw, watermark"
                }
            )
            resolution = "7680x4320"
            aspect_ratio = "16:9"
            negative_prompt = "ugly, disfigured, low quality, blurry, nsfw, watermark, signature, out of frame, extra limbs"
            
            try:
                from no_preferences_prompt import (
                    NO_PREFS_RANDOM_INSTRUCTIONS
                )
            except ImportError:
                logging.warning("no_preferences_prompt.py not found. Using default instructions.")
                NO_PREFS_RANDOM_INSTRUCTIONS = """
You will be given a list of tags: "{formatted_tags}".
Your primary task is to transform these tags into a single, cohesive, and vivid descriptive paragraph suitable for an image generation model.
Weave these tags into a natural, flowing narrative, creating a unified scene.
Your generated output should be ONLY the creative descriptive paragraph.
DO NOT include any technical specifications like resolution, aspect ratio, or any 'Avoid:' clauses in YOUR response. These will be handled by the system separately.

ENHANCEMENT MISSION (No Specific User Preferences, Based on Tags):
Your goal is to take the core tags "{formatted_tags}" and enrich them into a more vivid and descriptive paragraph.
While no specific user preferences for style, camera, etc., are provided, you should creatively and subtly weave in general artistic and descriptive elements to add depth and detail, drawing inspiration from established prompt engineering techniques to make the tags form a coherent scene.

PROMPT CRAFTING PRINCIPLES:
- Tag Integration: All provided tags: "{formatted_tags}" MUST be incorporated naturally into the scene.
- Contextual Richness: Describe the setting or background. Where are these elements? What surrounds them?
- Style Coherence: Suggest a complementary style subtly that fits the combined tags.
- Descriptive Language: Use vivid adjectives and adverbs to paint a clear picture.
- Quality Modifiers: Incorporate terms like "high-quality," "detailed," "masterpiece," "sharp focus," "vivid colors" to guide towards better results.

CONSIDER ADDING DETAILS RELATED TO (if not conflicting with the tags, and inspired by best practices):
- Visual Storytelling: What kind of scene or story do the tags imply when combined?
- Atmosphere & Mood: What feeling should the combined scene evoke?
- Lighting Qualities: Describe potential lighting for the scene.
- Color Harmonies & Palette: Suggest general color ideas for the scene.
- Compositional Elements: Hint at composition for the combined elements.
- Textural Details: Describe potential textures within the scene.

OUTPUT FORMAT:
Your response MUST be ONLY the single, detailed descriptive paragraph.
DO NOT include resolution, aspect ratio, or any "Avoid:" clauses in YOUR response.
Example (if tags were "forest, dragon, moonlight"):
"A mystical ancient forest, where a colossal, iridescent-scaled dragon slumbers peacefully under the soft, ethereal glow of moonlight filtering through the dense canopy. The scene is filled with an air of quiet magic and ancient power, with detailed textures on the gnarled trees and the dragon's hide."
(The system will add resolution, aspect ratio, and negative prompts later.)
"""
            
            formatted_tags = ", ".join(tags)
            prompt_fallback = f"{formatted_tags}, artistic"

            def _cleanup_text_from_gemini(text: str) -> str:
                # Remove resolution and aspect ratio mentions
                text = re.sub(r'\b\d+x\d+\s+resolution\b[.,\s]*', '', text, flags=re.IGNORECASE)
                text = re.sub(r'\b\d+:\d+\s+aspect\s+ratio\b[.,\s]*', '', text, flags=re.IGNORECASE)
                # Remove "Avoid:" clauses
                text = re.sub(r'\bAvoid\s*:[^\n]*', '', text, flags=re.IGNORECASE)
                # Remove potential "TAGS PROVIDED:" or initial tag lists
                text = re.sub(r'^TAGS\s+PROVIDED\s*:[^\n]*\n*', '', text, flags=re.IGNORECASE | re.MULTILINE)
                # Remove any leading tag lists or comma-separated tags at the start of the text
                # This regex removes lines or parts that look like tag lists at the start
                text = re.sub(r'^(?:[\w\s,-]+,)+[\w\s,-]+\s*', '', text, flags=re.IGNORECASE)
                # Remove multiple newlines and join lines into a single paragraph
                text = " ".join(text.splitlines()).strip().strip('.').strip()
                return text

            # Simplify instructions to mention tags only once and explicitly exclude tags and technical details
            instructions = f"""
You will be given a list of tags: "{formatted_tags}".
Your primary task is to transform these tags into a single, cohesive, and vivid descriptive paragraph suitable for an image generation model.
Weave these tags into a natural, flowing narrative, creating a unified scene.
Your generated output should be ONLY the creative descriptive paragraph.
DO NOT include any tags, technical specifications like resolution, aspect ratio, or any 'Avoid:' clauses in YOUR response. These will be handled by the system separately.

Your output MUST NOT repeat the tags or any technical details.
"""
            
            try:
                from google import genai # Use the new SDK import
                from google.genai import types # Import types for consistency
            except ImportError:
                logging.warning("google.generativeai module not found. Some features will be disabled.")
                # Define a dummy function if import fails (Removed dummy classes as they are no longer needed with new SDK import)
                pass # Keep the pass statement for valid syntax

            if not gemini_config.is_initialized():
                if not gemini_config.initialize_gemini_globally():
                    logging.error(f"Gemini not initialized for random prompt enhancement: {gemini_config.get_last_error()}")
                    return enforce_prompt_format(prompt_fallback, resolution, aspect_ratio, negative_prompt)

            effective_user_prefs_for_model = user_prefs if user_prefs else SimplePrefs()
            selected_model_name = gemini_config.get_selected_gemini_model(effective_user_prefs_for_model)
            logging.info(f"Using Gemini model for random prompt enhancement (no_prefs path): {selected_model_name}")
                
            try:
                client = gemini_config.get_gemini_client()
                if client is None:
                    logging.error("Gemini client is not initialized, cannot generate random prompt.")
                    return enforce_prompt_format(prompt_fallback, resolution, aspect_ratio, negative_prompt)
                    
                response = client.generate_content(
                    model=selected_model_name,
                    contents=instructions
                )

                if hasattr(response, 'text') and response.text:
                    raw_gemini_text = response.text.strip()
                    enhanced_descriptive_text = _cleanup_text_from_gemini(raw_gemini_text)
                    if not enhanced_descriptive_text:
                        logging.warning("Gemini returned empty description after cleanup for random (no_prefs). Falling back.")
                        enhanced_descriptive_text = prompt_fallback
                else:
                    logging.warning("Gemini response issue for random (no_prefs). Falling back.")
                    enhanced_descriptive_text = prompt_fallback
            except Exception as e:
                logging.error(f"Error generating prompt with Gemini (no_prefs path): {str(e)}")
                enhanced_descriptive_text = prompt_fallback
            
            return enhanced_descriptive_text

        # User preferences are enabled or provided - use Gemini for enhancement
        # Get user preferences
        if user_prefs and hasattr(user_prefs, 'preferred_styles') and hasattr(user_prefs, 'preferred_moods'): # Check user_prefs exists
            style = user_prefs.preferred_styles[0] if user_prefs.preferred_styles else None
            mood = user_prefs.preferred_moods[0] if user_prefs.preferred_moods else None
        else: # Handles case where user_prefs might be None (e.g. if global_user_prefs import failed)
            style = None
            mood = None

        # Get all settings from imagen_settings
        settings = user_prefs.imagen_settings if user_prefs and hasattr(user_prefs, 'imagen_settings') else {}
        
        # Extract style-specific settings first as they might be needed below
        digital_settings = settings.get("digital_settings", {})
        game_engine_settings = settings.get("game_engine_settings", {})
        software_settings = settings.get("software_settings", {})
        medium_settings = settings.get("medium_settings", {})
        illustration_settings = settings.get("illustration_settings", {})
        abstract_settings = settings.get("abstract_settings", {})
        material_settings = settings.get("material_settings", {})

        # Extract camera settings for the prompt
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

        # Extract lighting settings for the prompt
        lighting_settings = settings.get("lighting_settings", {})
        time_of_day = lighting_settings.get("time_of_day")
        lighting_type = lighting_settings.get("lighting_type")
        light_source = lighting_settings.get("light_source")
        light_quality = lighting_settings.get("light_quality")
        artificial_sources = lighting_settings.get("artificial_sources", [])

        # Extract composition settings for the prompt
        composition_settings = settings.get("composition_settings", {})
        technique = composition_settings.get("technique")
        camera_angle = composition_settings.get("camera_angle")
        visual_flow = composition_settings.get("visual_flow")
        depth_layering = composition_settings.get("depth_layering")
        focal_point = composition_settings.get("focal_point")
        perspective = composition_settings.get("perspective")

        # Extract environment settings for the prompt
        environment_settings = settings.get("environment_settings", {})
        weather = environment_settings.get("weather")
        season = environment_settings.get("season")
        location_type = environment_settings.get("location_type")
        atmospheric_effects = environment_settings.get("atmospheric_effects", [])

        # Extract style settings for the prompt
        style_settings = settings.get("style_settings", {})
        art_movement = style_settings.get("art_movement")
        style_era = style_settings.get("style_era")
        post_processing = style_settings.get("post_processing", [])

        # Extract detail settings for the prompt
        detail_settings = settings.get("detail_settings", {})
        detail_level = detail_settings.get("detail_level")
        texture_quality = detail_settings.get("texture_quality")
        special_effects = detail_settings.get("special_effects", [])

        # Extract color settings for the prompt
        color_settings = settings.get("color_settings", {})
        color_scheme = color_settings.get("color_scheme")
        palette_type = color_settings.get("palette_type")
        color_temperature = color_settings.get("color_temperature")

        # Extract quality settings for the prompt
        quality_settings = settings.get("quality_settings", {})
        resolution = quality_settings.get("resolution", "3840x2160")
        rendering_quality = quality_settings.get("rendering_quality")
        aspect_ratio = user_prefs.aspect_ratio if hasattr(user_prefs, 'aspect_ratio') else "16:9"

        # Extract specific art style settings
        digital_software = digital_settings.get("software", "")
        digital_effects = digital_settings.get("digital_effects", [])
        game_engine = game_engine_settings.get("engine_type", "")
        game_genre = game_engine_settings.get("game_genre", "")
        game_shader = game_engine_settings.get("shader_type", "")
        suite = software_settings.get("suite")
        renderer = software_settings.get("renderer")
        version = software_settings.get("version")
        painting_medium = medium_settings.get("painting_medium", "")
        brushwork = medium_settings.get("brushwork", "")
        texture = medium_settings.get("texture", "")
        illustration_style = illustration_settings.get("style", "")
        line_quality = illustration_settings.get("line_quality", "")
        abstract_composition = abstract_settings.get("composition_type", "")
        movement_type = abstract_settings.get("movement_type", "")
        material_type = material_settings.get("material_type", "")
        material_finish = material_settings.get("finish", "")

        # Format tags for prompt
        formatted_tags = ", ".join(tags)

        # Get negative prompt if available
        negative_prompt = settings.get("negative_prompt", "")

        # If no negative prompt is specified, use default negative prompt
        if not negative_prompt:
            negative_prompt = "ugly, disfigured, low quality, blurry, nsfw, watermark, signature, out of frame, extra limbs, poorly drawn face, twisted limbs, distorted face, bad proportions, bad anatomy"

        # Try to import PROMPT_INSTRUCTIONS
        try:
            from ..config import PROMPT_INSTRUCTIONS
        except ImportError:
            logging.warning("Could not import PROMPT_INSTRUCTIONS from ..config.")
            # Define a fallback instruction if import fails
            PROMPT_INSTRUCTIONS = """
Generate a detailed and artistic prompt for a high-quality wallpaper image.

Technical parameters:
- Resolution: {resolution}
- Aspect ratio: {aspect_ratio}
- Color scheme: {color_scheme}
- Lighting: {lighting}
- Composition: {composition}
- Depth of field: {depth_of_field}

{style_context}

The generated prompt should be detailed and descriptive, focusing on creating a visually stunning wallpaper.
Example format: "A detailed description of the image... {resolution} resolution, {aspect_ratio} aspect ratio"
"""
        
        # Use PROMPT_INSTRUCTIONS with proper formatting
        instruction_context = PROMPT_INSTRUCTIONS.format(
            resolution=resolution if resolution else "Not specified",
            aspect_ratio=aspect_ratio if aspect_ratio else "16:9",
            color_scheme=color_scheme if color_scheme else "Not specified",
            lighting=lighting_type if lighting_type else "Not specified",
            composition=technique if technique else "Not specified",
            depth_of_field=depth_of_field if depth_of_field else "Not specified",
            style_context="" # Not strictly needed if PROMPT_INSTRUCTIONS is simple, but kept for compatibility
        )


        # Create a more evocative, artistic generation context for Gemini
        # This instruction tells Gemini to ONLY output the descriptive paragraph.
        
        # Helper function to clean Gemini's output (can be defined at module level or here if not already)
        # For simplicity, assuming it might be redefined or ensure it's accessible
        # If _cleanup_text_from_gemini was defined above for the no_prefs block, it's in scope.
        # Otherwise, it should be defined here or at module level.
        # Let's ensure it's available or defined if this path is taken independently.
        if '_cleanup_text_from_gemini' not in locals():
            def _cleanup_text_from_gemini(text: str) -> str:
                text = re.sub(r'\b\d+x\d+\s+resolution\b[.,\s]*', '', text, flags=re.IGNORECASE)
                text = re.sub(r'\b\d+:\d+\s+aspect\s+ratio\b[.,\s]*', '', text, flags=re.IGNORECASE)
                text = re.sub(r'\bAvoid\s*:[^\n]*', '', text, flags=re.IGNORECASE)
                text = re.sub(r'^TAGS\s+PROVIDED\s*:[^\n]*\n*', '', text, flags=re.IGNORECASE | re.MULTILINE)
                text = " ".join(text.splitlines()).strip().strip('.').strip()
                return text

        # Enhanced instructions to emphasize user's chosen style more strongly.
        gemini_instructions = f"""
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
- Compositional Sense: The composition ({technique if technique else "engaging"}) should serve the style and draw attention to {focal_point if focal_point else "the main subject derived from tags"}.
- Detail & Texture: Details ({detail_level if detail_level else "appropriate"}) and textures ({texture_quality if texture_quality else "fitting"}) must align with and enhance the chosen artistic style.

Specific Art Style Details (if provided, these are KEY to describing the style accurately):
- Digital Art: If the style is digital, mention qualities related to "{digital_software}" or effects like "{", ".join(digital_effects if digital_effects else ['N/A'])}".
- Game Art: If game-related, describe it as if from a "{game_genre}" game, perhaps using "{game_engine}" visuals with "{game_shader}" shaders.
- Traditional Medium: If a traditional medium like "{painting_medium}" is chosen, describe the "{brushwork}" and "{texture}" of the medium.
- Illustration: If an "{illustration_style}" is chosen, describe the "{line_quality}".
- Abstract: For abstract styles, focus on "{abstract_composition}" and "{movement_type}".
- Materials: If specific materials like "{material_type}" with a "{material_finish}" finish are relevant to the style, describe them.

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

        # Generate prompt using Gemini
        enhanced_descriptive_text = formatted_tags # Fallback to just tags
        try:
            # Ensure Gemini is initialized
            if not gemini_config.is_initialized():
                if not gemini_config.initialize_gemini_globally():
                    logging.error(f"Gemini not initialized for random prompt (user_prefs path): {gemini_config.get_last_error()}")
                    return enforce_prompt_format(formatted_tags, resolution, aspect_ratio, negative_prompt) # Fallback
            
            effective_user_prefs_for_model = user_prefs if user_prefs else SimplePrefs()
            selected_model_name = gemini_config.get_selected_gemini_model(effective_user_prefs_for_model)
            logging.info(f"Using Gemini model for random prompt (user_prefs path): {selected_model_name}")

            # API key and configuration are handled by gemini_config
            # Explicitly ensure 'genai' is in scope here, though it should be from top-level import.
            client = gemini_config.get_gemini_client()
            if client is None:
                logging.error("Gemini client is not initialized, cannot generate random prompt (user_prefs path).")
                return enforce_prompt_format(formatted_tags, resolution, aspect_ratio, negative_prompt) # Fallback
                
            # Send only the specific instructions for Gemini
            response = client.generate_content(
                model=selected_model_name,
                contents=gemini_instructions
            )

            if hasattr(response, 'text') and response.text:
                raw_gemini_text = response.text.strip()
                enhanced_descriptive_text = _cleanup_text_from_gemini(raw_gemini_text)
                if not enhanced_descriptive_text: # Check for empty response after cleanup
                    logging.warning("Gemini returned empty description after cleanup for random (user_prefs). Falling back.")
                    enhanced_descriptive_text = formatted_tags
            else:
                logging.warning("Gemini response issue for random (user_prefs). Falling back.")
                enhanced_descriptive_text = formatted_tags
        except Exception as e:
            logging.error(f"Error generating prompt with Gemini (user_prefs path): {e}")
            enhanced_descriptive_text = formatted_tags # Fallback is just tags
        
        # The function should consistently return just the descriptive text.
        # The calling code will be responsible for the final formatting using enforce_prompt_format.
        return enhanced_descriptive_text


    except Exception as e:
        logging.error(f"Error in generate_prompt_random: {e}")
        # Fallback to basic tags if a catastrophic error occurs before Gemini call
        # Need to define resolution, aspect_ratio, negative_prompt for this fallback
        fallback_resolution = "3840x2160"
        fallback_aspect_ratio = "16:9"
        fallback_negative_prompt = "ugly, disfigured, low quality, blurry, nsfw, watermark"
        if 'user_prefs' in locals() and user_prefs:
            if hasattr(user_prefs, 'imagen_settings') and user_prefs.imagen_settings:
                quality_settings = user_prefs.imagen_settings.get("quality_settings", {})
                fallback_resolution = quality_settings.get("resolution", fallback_resolution)
                fallback_negative_prompt = user_prefs.imagen_settings.get("negative_prompt", fallback_negative_prompt)
            if hasattr(user_prefs, 'aspect_ratio'):
                fallback_aspect_ratio = user_prefs.aspect_ratio
        
        formatted_tags_str = ", ".join(tags)
        return enforce_prompt_format(formatted_tags_str, fallback_resolution, fallback_aspect_ratio, fallback_negative_prompt)


def generate_random_style_mix(user_prefs=None):
    """Generate a random mix of artistic styles.
    
    This function combines styles from different categories to create unique
    style combinations for image generation prompts.
    
    Args:
        user_prefs: Optional user preferences object. If None and use_user_preferences
                   is True, the function will use the global user_prefs.
    
    Returns:
        str: A string containing a combination of artistic styles, joined with " + "
    """
    try:
        # Import from core to avoid circular imports
        from .core import use_user_preferences
        
        # If user_prefs is not provided and we should use preferences, get them from global
        if user_prefs is None and use_user_preferences:
            # Import here to avoid circular imports
            try:
                from ..settings_modules import get_preferences
                user_prefs = get_preferences()
            except ImportError:
                logging.warning("Unable to import get_preferences from ..settings_modules.")
                user_prefs = None
        
        # Define default style categories
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
        
        # Check if user has custom style categories in preferences
        custom_style_categories = {}
        if user_prefs and hasattr(user_prefs, 'imagen_settings'):
            settings = user_prefs.imagen_settings
            style_settings = settings.get("style_settings", {})
            custom_style_categories = style_settings.get("style_categories", {})
        
        # Use custom categories if available, otherwise use the default ones
        categories_to_use = custom_style_categories if custom_style_categories else default_style_categories
        
        # Select a random category
        category = random.choice(list(categories_to_use.keys()))
        # Select 2-3 compatible styles from the same category
        num_styles = random.randint(2, 3)
        available_styles = categories_to_use[category]
        if len(available_styles) < num_styles:
            num_styles = len(available_styles)
        selected_styles = random.sample(available_styles, num_styles)
        return " + ".join(selected_styles)
    except Exception as e:
        logging.error(f"Error in generate_random_style_mix: {e}")
        return "digital_art + fantasy"  # Fallback to basic style mix
