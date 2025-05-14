#!/usr/bin/env python3
"""Core Prompt Generator Module - Main functions for generating AI wallpaper prompts

This module contains the central functions for generating prompts using
various methods and manages the global prompt generation settings.
"""
import logging
import os
import random
import re
from typing import Dict, List, Optional, Any, Union, Tuple, Set

# Import types
from .types import SimplePrefs
from .. import gemini_config # Added for centralized Gemini config

# Import utilities and formatting
from .formatters import enforce_prompt_format
from .negative_prompt import enhance_negative_prompt # infer_subject_negatives_gemini is more complex to call here.
                                                    # enhance_negative_prompt itself calls infer_subject_negatives_gemini
                                                    # and will need to be updated to pass user_prefs.

# Create a cache for generated prompts
prompt_cache = {}

# Set default Gemini model - REMOVED
# gemini_model_name = "gemini-2.5-flash-preview-04-17"

# Flag to determine whether to use user preferences or not
use_user_preferences = True

# Import the Google GenAI SDK
try:
    from google import genai # Use the new SDK import
    from google.genai import types # Import types for consistency
except ImportError:
    logging.warning("google.generativeai module not found. Some features will be disabled.")
    # Define a dummy function if import fails (Removed dummy classes as they are no longer needed with new SDK import)
    pass


def set_prompt_preferences(use_preferences: bool) -> None:
    """Set whether to use user preferences for prompt generation.
    
    Args:
        use_preferences: Boolean flag to indicate if user preferences should be used
    """
    global use_user_preferences
    use_user_preferences = use_preferences
    logging.info(f"Prompt generation with user preferences: {use_preferences}")


def generate_prompt_gemini(tags: List[str], user_prefs: Optional[Any] = None) -> str:
    """Generate a detailed prompt using Gemini and user preferences with enhanced style support.
    
    Args:
        tags: List of tags to include in the prompt
        user_prefs: Optional user preferences object. If None and use_user_preferences
                    is True, the function will use the global user_prefs.
    
    Returns:
        str: A detailed prompt for image generation
    """
    style_era = None
    try:
        global use_user_preferences
        
        # If user_prefs is not provided and we should use preferences, get them from global
        if user_prefs is None and use_user_preferences:
            # Import here to avoid circular imports
            try:
                from ..settings_modules import get_preferences
                user_prefs = get_preferences()
            except ImportError:
                logging.warning("Unable to import get_preferences from ..settings_modules.")
                user_prefs = None
        
        # If we shouldn't use user preferences and none were provided, use minimal settings
        if not use_user_preferences and user_prefs is None:
            # Create minimal preferences with just enough for the prompt to work
            user_prefs = SimplePrefs(
                aspect_ratio="16:9",
                imagen_settings={
                    "camera_settings": {},
                    "lighting_settings": {},
                    "composition_settings": {},
                    "environment_settings": {},
                    "style_settings": {},
                    "detail_settings": {},
                    "color_settings": {},
                    "quality_settings": {"resolution": "3840x2160"},
                    "digital_settings": {},
                    "game_engine_settings": {},
                    "medium_settings": {},
                    "illustration_settings": {},
                    "abstract_settings": {},
                    "material_settings": {}
                }
            )
        
        # Ensure Gemini is initialized
        if not gemini_config.is_initialized():
            if not gemini_config.initialize_gemini_globally():
                logging.error(f"Gemini not initialized for generate_prompt_gemini (core.py): {gemini_config.get_last_error()}")
                # Fallback to a simple prompt if Gemini cannot be used
                formatted_tags_str = ", ".join(tags)
                # Attempt to get user_prefs for negative prompt even in fallback
                neg_prompt_fallback = "ugly, disfigured"
                if user_prefs and hasattr(user_prefs, 'imagen_settings'):
                    neg_prompt_fallback = user_prefs.imagen_settings.get("negative_prompt", neg_prompt_fallback)
                elif hasattr(user_prefs, 'negative_prompt'): # Check root level if not in imagen_settings
                    neg_prompt_fallback = getattr(user_prefs, 'negative_prompt', neg_prompt_fallback)

                return enforce_prompt_format(formatted_tags_str, "3840x2160", "16:9", neg_prompt_fallback)

        # Determine the effective user_prefs to use (actual or SimplePrefs)
        effective_user_prefs = user_prefs
        if not use_user_preferences and user_prefs is None: # This condition was already handled for creating SimplePrefs
            effective_user_prefs = user_prefs # which is SimplePrefs instance here
        elif user_prefs is None and use_user_preferences: # If global user_prefs couldn't be loaded
             effective_user_prefs = SimplePrefs() # Fallback to SimplePrefs
        elif user_prefs is None: # General fallback if user_prefs is None for any other reason
            effective_user_prefs = SimplePrefs()


        selected_model = gemini_config.get_selected_gemini_model(effective_user_prefs)

        # Create cache key based on whether we're using user preferences and the selected model
        if use_user_preferences and user_prefs is not None: # user_prefs here refers to the original parameter
            cache_key = str(tags) + str(getattr(user_prefs, 'imagen_settings', {})) + selected_model
        else:
            cache_key = str(tags) + "no_user_prefs" + selected_model
            
        # Check if we have this prompt cached
        if cache_key in prompt_cache:
            return prompt_cache[cache_key]
            
        # Get user preferences if we should use them
        if use_user_preferences and user_prefs is not None and hasattr(user_prefs, 'preferred_styles') and hasattr(user_prefs, 'preferred_moods'):
            style = user_prefs.preferred_styles[0] if user_prefs.preferred_styles else None
            mood = user_prefs.preferred_moods[0] if user_prefs.preferred_moods else None
        else:
            style = None
            mood = None
        
        # Get all settings from imagen_settings
        if user_prefs is not None:
            settings = getattr(user_prefs, 'imagen_settings', {}) or {}
        else:
            settings = {}
        
        # Extract style-specific settings
        digital_settings = settings.get("digital_settings", {})
        game_engine_settings = settings.get("game_engine_settings", {})
        software_settings = settings.get("software_settings", {})
        medium_settings = settings.get("medium_settings", {})
        illustration_settings = settings.get("illustration_settings", {})
        abstract_settings = settings.get("abstract_settings", {})
        material_settings = settings.get("material_settings", {})
        
        # Digital art settings
        digital_software = digital_settings.get("software", "")
        digital_effects = digital_settings.get("digital_effects", [])
        
        # Game engine settings
        game_engine = game_engine_settings.get("engine_type", "")
        game_genre = game_engine_settings.get("game_genre", "")
        game_shader = game_engine_settings.get("shader_type", "")
        
        # Traditional medium settings
        painting_medium = medium_settings.get("painting_medium", "")
        brushwork = medium_settings.get("brushwork", "")
        texture = medium_settings.get("texture", "")
        
        # Illustration settings
        illustration_style = illustration_settings.get("style", "")
        line_quality = illustration_settings.get("line_quality", "")
        
        # Abstract settings
        abstract_composition = abstract_settings.get("composition_type", "")
        movement_type = abstract_settings.get("movement_type", "")
        
        # Material settings
        material_type = material_settings.get("material_type", "")
        material_finish = material_settings.get("finish", "")
        
        # Extract camera settings for the prompt (guarantee all variables are defined regardless of content)
        camera_settings = settings.get("camera_settings", {})
        camera_model = camera_settings.get("camera_model") if camera_settings else None
        lens_type = camera_settings.get("lens_type") if camera_settings else None
        aperture = camera_settings.get("aperture") if camera_settings else None
        special_lens = camera_settings.get("special_lens") if camera_settings else None
        depth_of_field = camera_settings.get("depth_of_field") if camera_settings else None
        focal_length = camera_settings.get("focal_length") if camera_settings else None
        shutter_speed = camera_settings.get("shutter_speed") if camera_settings else None
        iso = camera_settings.get("iso") if camera_settings else None
        filter_type = camera_settings.get("filter_type") if camera_settings else None

        # Extract lighting settings for the prompt
        lighting_settings = settings.get("lighting_settings", {})
        time_of_day = lighting_settings.get("time_of_day") if lighting_settings else None
        lighting_type = lighting_settings.get("lighting_type") if lighting_settings else None
        light_source = lighting_settings.get("light_source") if lighting_settings else None
        light_quality = lighting_settings.get("light_quality") if lighting_settings else None
        artificial_sources = lighting_settings.get("artificial_sources", []) if lighting_settings else []

        # Extract composition settings for the prompt
        composition_settings = settings.get("composition_settings", {})
        technique = composition_settings.get("technique") if composition_settings else None
        camera_angle = composition_settings.get("camera_angle") if composition_settings else None
        visual_flow = composition_settings.get("visual_flow") if composition_settings else None
        depth_layering = composition_settings.get("depth_layering") if composition_settings else None
        focal_point = composition_settings.get("focal_point") if composition_settings else None
        perspective = composition_settings.get("perspective") if composition_settings else None

        # Extract environment settings for the prompt
        environment_settings = settings.get("environment_settings", {})
        weather = environment_settings.get("weather") if environment_settings else None
        season = environment_settings.get("season") if environment_settings else None
        location_type = environment_settings.get("location_type") if environment_settings else None
        atmospheric_effects = environment_settings.get("atmospheric_effects", []) if environment_settings else []

        # Extract style settings for the prompt
        style_settings = settings.get("style_settings", {})
        art_movement = style_settings.get("art_movement") if style_settings else None
        style_era = style_settings.get("style_era") if style_settings else None
        post_processing = style_settings.get("post_processing", []) if style_settings else []

        # Extract detail settings for the prompt
        detail_settings = settings.get("detail_settings", {})
        detail_level = detail_settings.get("detail_level") if detail_settings else None
        texture_quality = detail_settings.get("texture_quality") if detail_settings else None
        special_effects = detail_settings.get("special_effects", []) if detail_settings else []

        # Extract color settings for the prompt
        color_settings = settings.get("color_settings", {})
        color_scheme = color_settings.get("color_scheme") if color_settings else None
        palette_type = color_settings.get("palette_type") if color_settings else None
        color_temperature = color_settings.get("color_temperature") if color_settings else None

        # Extract quality settings for the prompt
        quality_settings = settings.get("quality_settings", {})
        resolution = quality_settings.get("resolution", "3840x2160") if quality_settings else "3840x2160"
        rendering_quality = quality_settings.get("rendering_quality") if quality_settings else None
        aspect_ratio = getattr(user_prefs, 'aspect_ratio', "16:9") if user_prefs else "16:9"

        # Extract software settings
        suite = software_settings.get("suite") if software_settings else None
        renderer = software_settings.get("renderer") if software_settings else None
        version = software_settings.get("version") if software_settings else None

        # Ensure all style-specific variables for art/digital/games/medium are defined
        digital_software = digital_settings.get("software", "") if digital_settings else ""
        digital_effects = digital_settings.get("digital_effects", []) if digital_settings else []

        game_engine = game_engine_settings.get("engine_type", "") if game_engine_settings else ""
        game_genre = game_engine_settings.get("game_genre", "") if game_engine_settings else ""
        game_shader = game_engine_settings.get("shader_type", "") if game_engine_settings else ""

        painting_medium = medium_settings.get("painting_medium", "") if medium_settings else ""
        brushwork = medium_settings.get("brushwork", "") if medium_settings else ""
        texture = medium_settings.get("texture", "") if medium_settings else ""

        illustration_style = illustration_settings.get("style", "") if illustration_settings else ""
        line_quality = illustration_settings.get("line_quality", "") if illustration_settings else ""

        abstract_composition = abstract_settings.get("composition_type", "") if abstract_settings else ""
        movement_type = abstract_settings.get("movement_type", "") if abstract_settings else ""

        material_type = material_settings.get("material_type", "") if material_settings else ""
        material_finish = material_settings.get("finish", "") if material_settings else ""

        # Format tags for prompt
        formatted_tags = ", ".join(tags)
        
        # Get and enhance negative prompts
        default_negative_prompt = "ugly, disfigured, low quality, blurry, nsfw, watermark, signature, out of frame, extra limbs, poorly drawn face, twisted limbs, distorted face, bad proportions, bad anatomy"
        user_negative_prompt = settings.get("negative_prompt", "")
        
        # Split into individual terms
        default_terms = set(term.strip() for term in default_negative_prompt.split(',') if term.strip())
        user_terms = set(term.strip() for term in user_negative_prompt.split(',') if term.strip())
        
        # Enhance user terms first if they exist
        # enhance_negative_prompt will need user_prefs to pass to infer_subject_negatives_gemini
        # For now, assuming enhance_negative_prompt can fetch user_prefs if needed, or this part might need adjustment
        # if user_prefs is not consistently available/passed.
        # The current signature of enhance_negative_prompt only takes text.
        # For this refactor, we'll assume enhance_negative_prompt is updated separately or works.
        if user_terms:
            # Pass user_prefs to enhance_negative_prompt if its signature is updated
            # For now, calling as is:
            enhanced_user_terms = set(enhance_negative_prompt(term, user_prefs=effective_user_prefs) for term in user_terms)
            final_terms = enhanced_user_terms.union(default_terms)
            negative_prompt = ", ".join(sorted(list(final_terms)))
        else:
            negative_prompt = default_negative_prompt
        
        # Build style-specific technical context
        style_context = []
        
        # Software/3D context
        if suite or renderer or version:
            sw_description = "Created"
            if suite:
                sw_description += f" in {suite}"
            if renderer:
                sw_description += f", rendered with {renderer}"
            if version:
                sw_description += f" (v{version})"
            style_context.append(sw_description)

        # Digital art context
        if digital_software:
            style_context.append(f"Created using {digital_software}")
        if digital_effects:
            style_context.append(f"With digital effects: {', '.join(digital_effects)}")

        # Game art context
        if game_engine:
            style_context.append(f"Rendered in {game_engine}")
        if game_genre:
            style_context.append(f"Game genre: {game_genre}")
        if game_shader:
            style_context.append(f"Shader type: {game_shader}")

        # Traditional medium context
        if painting_medium:
            style_context.append(f"Medium: {painting_medium}")
        if brushwork:
            style_context.append(f"Brushwork: {brushwork}")
        if texture:
            style_context.append(f"Texture: {texture}")

        # Illustration context
        if illustration_style:
            style_context.append(f"Illustration style: {illustration_style}")
        if line_quality:
            style_context.append(f"Line quality: {line_quality}")

        # Abstract context
        if abstract_composition:
            style_context.append(f"Composition type: {abstract_composition}")
        if movement_type:
            style_context.append(f"Movement type: {movement_type}")

        # Material context
        if material_type:
            style_context.append(f"Material: {material_type}")
        if material_finish:
            style_context.append(f"Finish: {material_finish}")
        
        # Import configuration for prompt instructions
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
            style_context="\n".join(style_context) if style_context else ""
        )

        # Soft-inspire via description from user_prefs—encourage natural style flow
        description_instruction = ""
        if user_prefs and hasattr(user_prefs, "description") and user_prefs.description:
            description_text = user_prefs.description.strip()
            if description_text:
                description_instruction = f"\nSTYLE INSPIRATION:\nTo guide the atmosphere and visual narrative, the intended style and mood of this preset can be summarized as:\n\"{description_text}\"\n"

        # New, natural-flow-focused technical context with settings as inspiration cues—not as a list
        technical_context = f"""
Compose a single, immersive visual description for a wallpaper image featuring: {formatted_tags}
{description_instruction}

Let all camera, lighting, composition, environment, style, color, and quality settings below inspire the narrative organically.
Weave together the mood, geometric arrangement, lighting effects, and palette as a seamless scene—never recite settings, instead capture the feeling and intent they produce. If any specific attributes (e.g., 'rule of thirds', 'monochromatic muted palette', 'soft diffused ambient light') are mentioned, let them subtly but clearly influence the visual description. Everything should support the peaceful, minimalist, and modern geometric abstraction mood, and the narrative should have a harmonious, tranquil flow.

You are encouraged to creatively exaggerate or amplify any quality, feeling, visual motif, or stylistic effect using your own inspired style: magnify the sense of scale, serenity, negative space, geometric rhythm, lighting aura, or the emotional impact, blending together all user settings and preset cues so the wallpaper's mood and composition are powerfully felt.

Be bold and poetic in your writing: paint with metaphor, invent atmosphere, and lavish dramatic attention on the interplay of space, geometry, light, and calm. Use cinematic, sensorial, and emotional language to make the visual experience vivid—exaggerate silence, tension, tranquility, or awe to transform the scene into visual poetry.

Required: Conclude with the specified resolution and aspect ratio—"{resolution} resolution, {aspect_ratio} aspect ratio".
After the paragraph, include the phrase: "Avoid:" followed by the negative prompt.

Relevant scene inspiration:
- Mood: {mood if mood else "Not specified"}
- Styles: {style if style else "Not specified"}
- Art Movement: {art_movement if art_movement else "Not specified"}
- Style Era: {style_era if style_era else "Not specified"}
- Composition: {technique if technique else "Not specified"}; Focal point: {focal_point if focal_point else "Not specified"}; Balance: {composition_settings.get("balance_type", "") if composition_settings else ""}
- Shapes: {settings.get("minimalist_geometric_settings", {}).get("geometry_focus", "") if "minimalist_geometric_settings" in settings else ""}
- Color: {color_scheme if color_scheme else "Not specified"} palette, {palette_type if palette_type else "Not specified"}; {color_temperature if color_temperature else ""}
- Lighting: {lighting_type if lighting_type else "Not specified"}; {light_quality if light_quality else ""}
- Texture: {settings.get("detail_settings", {}).get("texture_quality", "") if "detail_settings" in settings else ""}
- Level of Detail: {detail_level if detail_level else "Not specified"}
- Anything unnecessary, repetitive, or technical should be omitted for maximal naturalness.

Example Output:
[One flowing, evocative paragraph visually describing the scene, smoothly integrating settings, ending with resolution and aspect ratio.]
Avoid: [negative prompt]
"""

        # Generate prompt using Gemini
        try:
            import google.genai as genai
        except ImportError:
            logging.warning("google.generativeai module not found. Some features will be disabled.")
            # Return a formatted version of the simple tags
            return enforce_prompt_format(formatted_tags, resolution, aspect_ratio, negative_prompt)
        
        # API key and configuration are handled by gemini_config.initialize_gemini_globally()
        # which was checked at the beginning of this function.
        
        try:
            # selected_model was already determined earlier
            client = gemini_config.get_gemini_client()
            if client is None:
                logging.error("Gemini client is not initialized, cannot generate prompt.")
                return enforce_prompt_format(formatted_tags, resolution, aspect_ratio, negative_prompt)
                
            response = client.generate_content(
                model=selected_model,
                contents=instruction_context + "\n\n" + technical_context
            )
            
            if hasattr(response, 'text') and response.text:
                full_response = response.text.strip()
                
                # Parse the response to separate prompt and negative prompt
                prompt_parts = full_response.split("Avoid:")
                
                if len(prompt_parts) > 1:
                    # If successfully parsed into two parts
                    main_prompt = prompt_parts[0].strip()
                    negative_part = prompt_parts[1].strip()
                    
                    # Combine them with "Avoid:" format
                    final_prompt = f"{main_prompt} Avoid: {negative_part}"
                else:
                    # If not in expected format, just add negative prompt
                    final_prompt = full_response
                    if "avoid" not in final_prompt.lower():
                        final_prompt += f" Avoid: {negative_prompt}"
                
                # Ensure proper formatting with resolution and aspect ratio
                final_prompt = enforce_prompt_format(final_prompt, resolution, aspect_ratio, negative_prompt)
                
                prompt_cache[cache_key] = final_prompt
                return final_prompt
            else:
                # Return a formatted version of the simple tags
                formatted_prompt = enforce_prompt_format(formatted_tags, resolution, aspect_ratio, negative_prompt)
                return formatted_prompt
        except Exception as e:
            logging.error(f"Error generating prompt with Gemini: {e}")
            # Return a formatted version of the simple tags
            return enforce_prompt_format(formatted_tags, resolution, aspect_ratio, negative_prompt)
    except Exception as e:
        logging.error(f"Error in generate_prompt_gemini: {e}")
        formatted_tags_str = ", ".join(tags) if isinstance(tags, list) else str(tags)
        # Return a formatted version of the simple tags
        return enforce_prompt_format(formatted_tags_str, "3840x2160", "16:9", "ugly, disfigured, low quality, blurry, nsfw")


def generate_prompt_random(tags: List[str], user_prefs: Optional[Any] = None) -> str:
    """Generate a random prompt using the provided tags.
    
    This function is a wrapper around the implementation in random_generator.py.
    
    Args:
        tags: List of tags to include in the prompt
        user_prefs: Optional user preferences object. If None and use_user_preferences
                    is True, the function will use the global user_prefs.
    
    Returns:
        str: A prompt for image generation
    """
    # Import here to avoid circular imports
    from .random_generator import generate_prompt_random as _generate_prompt_random
    return _generate_prompt_random(tags, user_prefs)


def enhance_custom_prompt(custom_prompt: str, user_prefs: Optional[Any] = None, description: Optional[str] = None) -> str:
    """Enhance the custom prompt using the Gemini model based on user preferences.
    
    This function is a wrapper around the implementation in custom_generator.py.
    
    Args:
        custom_prompt: The original prompt to enhance
        user_prefs: Optional user preferences object. If None and use_user_preferences
                   is True, the function will use the global user_prefs.
        description: Optional description string from preset to include in prompt generation.
    
    Returns:
        str: An enhanced version of the custom prompt
    """
    # Import here to avoid circular imports
    from .custom_generator import enhance_custom_prompt as _enhance_custom_prompt
    return _enhance_custom_prompt(custom_prompt, user_prefs, description)


def generate_random_style_mix(user_prefs: Optional[Any] = None) -> str:
    """Generate a random mix of artistic styles.
    
    This function combines styles from different categories to create unique
    style combinations for image generation prompts.
    
    Args:
        user_prefs: Optional user preferences object. If None and use_user_preferences
                   is True, the function will use the global user_prefs.
    
    Returns:
        str: A string containing a combination of artistic styles, joined with " + "
    """
    # Import here to avoid circular imports
    from .random_generator import generate_random_style_mix as _generate_random_style_mix
    return _generate_random_style_mix(user_prefs)


def select_random_tags() -> List[str]:
    """
    Select a diverse set of tags for Gemini prompt generation by sampling from multiple categories.
    Ensures broader creative diversity and theming.
    
    Returns:
        list: A deduplicated, randomized selection of tags from various conceptual categories.
    """
    # Import here to avoid circular imports
    from .tag_utils import select_random_tags as _select_random_tags
    return _select_random_tags()


def flatten_settings(settings: Dict, parent_key: str = "", sep: str = " - ", 
                    ignore_keys: Optional[Set[str]] = None) -> List[Tuple[str, str, str]]:
    """
    Recursively flatten a settings dictionary into a list of (section, field, value) tuples for prompt context.
    Allows for dynamic prompt generation accommodating arbitrary new fields/styles.
    Now handles non-standard settings from user_preferences.json by preserving all valid values.

    Args:
        settings (dict): Nested dictionary of settings.
        parent_key (str): Current section or parent prefix.
        sep (str): Separator between parent and child keys.
        ignore_keys (set): Keys to ignore from output.

    Returns:
        List of (section, field, value) tuples suitable for inclusion in a prompt.
    """
    ignore_keys = ignore_keys or set(["negative_prompt"])  # Negative prompt handled separately
    flattened = []
    if not isinstance(settings, dict):
        return flattened
    for k, v in settings.items():
        if k in ignore_keys:
            continue
        pretty_key = k.replace("_", " ").capitalize()
        full_key = f"{parent_key}{sep}{pretty_key}" if parent_key else pretty_key
        if isinstance(v, dict):
            sub = flatten_settings(v, parent_key=full_key, sep=sep, ignore_keys=ignore_keys)
            flattened.extend(sub)
        elif isinstance(v, list):
            list_val = ", ".join(str(x) for x in v if x)
            if list_val:
                flattened.append((parent_key if parent_key else pretty_key, pretty_key, list_val))
        elif v is not None and v != "" and v != "Not specified" and v != "none" and v != "None":
            flattened.append((parent_key if parent_key else pretty_key, pretty_key, str(v)))
    return flattened


def dynamic_technical_context(settings: Dict, aspect_ratio: str = "16:9", resolution: str = "3840x2160") -> str:
    """
    Build a narrative technical context for prompts from all user preferences/settings (dynamic, grouped),
    synthesizing each key/value pair into natural language descriptive phrases for the AI to integrate.
    
    Args:
        settings (dict): The settings to use for building the context
        aspect_ratio (str): The aspect ratio to use
        resolution (str): The resolution to use
        
    Returns:
        str: Natural language context built from the settings
    """
    def phrase_from_kv(section, field, value):
        # Natural language phrasing that blends settings into flowing descriptions
        # Now handles non-standard settings with more flexible matching
        key = field.lower()
        val = str(value)
        
        # Handle empty/null values
        if not val or val.lower() in ("none", "not specified", ""):
            return None
            
        # Standard settings
        if key in ["lighting type", "light quality"]:
            return f"illuminated by {val} lighting that"
        elif key in ["color scheme", "palette type", "color temperature"]:
            return f"using a {val} color palette that"
        elif "brush" in key or "painting" in key or "medium" in key or "canvas" in key:
            return f"rendered in {val} {key.replace('_',' ')} with"
        elif key in ["detail level", "texture quality"]:
            return f"featuring {val} {key.replace('_', ' ')} that"
        elif key in ["focal point"]:
            return f"centered around {val} with"
        elif key in ["season", "weather"]:
            return f"set in {val} conditions where"
        elif key in ["post processing", "special effects"]:
            return f"enhanced with {val} effects creating"
        elif key in ["movement type", "composition type"]:
            return f"composed with {val} movement that"
        elif "style" in key and "style era" not in key:
            return f"in {val} style featuring"
        elif key == "aspect ratio":
            return None
        elif key == "resolution":
            return None
            
        # Handle non-standard settings with flexible matching
        if "setting" in key or "preference" in key or "option" in key:
            return f"with {val} {key.replace('_', ' ')} that"
            
        # Default natural phrasing for any other fields
        return f"with {val} {key.replace('_', ' ')} that"
    
    flat = flatten_settings(settings)
    # Filter and phrase up all non-empty fields
    phrases = [phrase_from_kv(section, field, value) for section, field, value in flat]
    phrases = [p for p in phrases if p and not p.strip().lower().startswith("none")]
    # Remove redundancies
    deduped = []
    for p in phrases:
        if p not in deduped:
            deduped.append(p)
    if deduped:
        # Join phrases with natural language connectors
        if len(deduped) == 1:
            text = deduped[0]
        else:
            text = ", ".join(deduped[:-1]) + " and " + deduped[-1]
    else:
        text = ""
    # Always enforce aspect ratio/resolution at the end
    if text:
        text += " with "
    text += f"{resolution} resolution in {aspect_ratio} aspect ratio"
    return text
