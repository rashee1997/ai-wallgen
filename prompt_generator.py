#!/usr/bin/env python3
"""Prompt Generator Module - Functions for generating AI wallpaper prompts

This module contains functions for generating and enhancing prompts using
the Gemini API, random tags, and custom user input. It supports using user
preferences or generating prompts independently of user preferences.
"""
# Standard library imports
import re
import random
import logging
import os
from typing import Dict, List, Optional, Any, Union

# Third-party imports
try:
    import google.generativeai as genai
except ImportError:
    logging.warning("google.generativeai module not found. Some features will be disabled.")

# Import configuration
from config import (
    nature_tags, space_tags, sea_tags, flowers_tags, urban_tags,
    fantasy_tags, abstract_tags, mood_tags, available_genres,
    PROMPT_INSTRUCTIONS, CUSTOM_PROMPT_INSTRUCTIONS,
    STYLE_CATEGORIES # STYLE_CATEGORIES is now in config
)

# Import no-preferences prompt instructions
try:
    from no_preferences_prompt import (
        NO_PREFS_PROMPT_INSTRUCTIONS,
        NO_PREFS_RANDOM_INSTRUCTIONS,
        enforce_art_medium
    )
except ImportError:
    logging.warning("no_preferences_prompt.py not found. Using default instructions.")
    # Define fallbacks in case import fails
    NO_PREFS_PROMPT_INSTRUCTIONS = CUSTOM_PROMPT_INSTRUCTIONS
    NO_PREFS_RANDOM_INSTRUCTIONS = PROMPT_INSTRUCTIONS
    
    # Define a simple fallback enforce_art_medium function if import fails
    def enforce_art_medium(prompt, original_prompt):
        return prompt  # Simply return prompt unchanged if module not found

# Create a cache for generated prompts
prompt_cache = {}

# Set default Gemini model
gemini_model_name = "gemini-2.5-flash-preview-04-17"

# Flag to determine whether to use user preferences or not
use_user_preferences = True

def flatten_settings(settings, parent_key="", sep=" - ", ignore_keys=None):
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

def dynamic_technical_context(settings, aspect_ratio="16:9", resolution="3840x2160"):
    """
    Build a narrative technical context for prompts from all user preferences/settings (dynamic, grouped),
    synthesizing each key/value pair into natural language descriptive phrases for the AI to integrate.
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

# Configure signal handler for the module
# Removed local signal handler; global handler in graceful_exit.py will manage exit.

def set_prompt_preferences(use_preferences: bool):
    """Set whether to use user preferences for prompt generation.
    
    Args:
        use_preferences: Boolean flag to indicate if user preferences should be used
    """
    global use_user_preferences
    use_user_preferences = use_preferences
    logging.info(f"Prompt generation with user preferences: {use_preferences}")

def generate_prompt_gemini(tags, user_prefs=None):
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
            from wallpaper_generator import user_prefs as global_user_prefs
            user_prefs = global_user_prefs
        
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
        
        # Create cache key based on whether we're using user preferences
        if use_user_preferences:
            cache_key = str(tags) + str(user_prefs.imagen_settings) + str(gemini_model_name)
        else:
            cache_key = str(tags) + "no_user_prefs" + str(gemini_model_name)
            
        # Check if we have this prompt cached
        if cache_key in prompt_cache:
            return prompt_cache[cache_key]
            
        # Get user preferences if we should use them
        if use_user_preferences and hasattr(user_prefs, 'preferred_styles') and hasattr(user_prefs, 'preferred_moods'):
            style = user_prefs.preferred_styles[0] if user_prefs.preferred_styles else None
            mood = user_prefs.preferred_moods[0] if user_prefs.preferred_moods else None
        else:
            style = None
            mood = None
        
        # Get all settings from imagen_settings
        settings = user_prefs.imagen_settings
        
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
        aspect_ratio = user_prefs.aspect_ratio if hasattr(user_prefs, 'aspect_ratio') else "16:9"

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
        if user_terms:
            enhanced_user_terms = set(enhance_negative_prompt(term) for term in user_terms)
            final_terms = enhanced_user_terms.union(default_terms)
            negative_prompt = ", ".join(sorted(list(final_terms)))  # Sort for consistency
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
        
        # Use PROMPT_INSTRUCTIONS from prompt_config.py with proper formatting
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
        if hasattr(user_prefs, "description") and user_prefs.description:
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

Required: Conclude with the specified resolution and aspect ratio—"3840x2160 resolution, 16:9 aspect ratio".
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
        gemini_api_key = os.environ.get("GEMINI_API_KEY")
        if not gemini_api_key:
            logging.warning("No Gemini API key configured")
            # Return a formatted version of the simple tags
            return enforce_prompt_format(formatted_tags, resolution, aspect_ratio, negative_prompt)
        
        try:
            genai.configure(api_key=gemini_api_key)
            model = genai.GenerativeModel(gemini_model_name)
            response = model.generate_content(instruction_context + "\n\n" + technical_context)
            
            if response.text:
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
        formatted_tags_str = ", ".join(tags)
        # Return a formatted version of the simple tags
        return enforce_prompt_format(formatted_tags_str, "3840x2160", "16:9", negative_prompt)

def generate_prompt_random(tags, user_prefs=None):
    """Generate a random prompt using the provided tags."""
    style_era = None
    try:
        global use_user_preferences
        
        # If user_prefs is not provided and we should use preferences, get them from global
        if user_prefs is None and use_user_preferences:
            # Import here to avoid circular imports
            from wallpaper_generator import user_prefs as global_user_prefs
            user_prefs = global_user_prefs
            
        # If we shouldn't use user preferences and none were provided, use minimal settings
        if not use_user_preferences and user_prefs is None:
            # Create minimal preferences
            user_prefs = SimplePrefs(
                aspect_ratio="16:9",
                imagen_settings={
                    "quality_settings": {"resolution": "7680x4320"},
                    "negative_prompt": "ugly, disfigured, low quality, blurry, nsfw, watermark"
                }
            )
            # Get basic settings
            resolution = "7680x4320"
            aspect_ratio = "16:9"
            negative_prompt = "ugly, disfigured, low quality, blurry, nsfw, watermark, signature, out of frame, extra limbs"
            
            # Use no-preferences instructions for better subject preservation
            # Format simple tags into a prompt
            formatted_tags = ", ".join(tags)
            
            # Create a simple base prompt
            prompt = f"{formatted_tags}, artistic"
            
            # Use NO_PREFS_RANDOM_INSTRUCTIONS for the prompt enhancement
            instructions = NO_PREFS_RANDOM_INSTRUCTIONS.format(
                resolution=resolution,
                aspect_ratio=aspect_ratio
            )
            
            # Add specific guidance for random tag generation
            instructions += f"""

TAGS PROVIDED: {formatted_tags}

Your prompt MUST incorporate all of these tags while maintaining coherence.
Focus on creating a unified scene that naturally includes these elements.
Choose an artistic style that best showcases these subjects together.

OUTPUT FORMAT:
Your response must follow this exact format:
1. A single, detailed paragraph describing the image that incorporates ALL provided tags
2. MUST end the description with "{resolution} resolution, {aspect_ratio} aspect ratio"
3. End with "Avoid: {negative_prompt}"
"""
            
            # Try to use Gemini to enhance the prompt
            gemini_api_key = os.environ.get("GEMINI_API_KEY")
            if not gemini_api_key:
                logging.warning("No Gemini API key configured")
                # Return formatted version of the basic tags
                return enforce_prompt_format(prompt, resolution, aspect_ratio, negative_prompt)
                
            try:
                genai.configure(api_key=gemini_api_key)
                model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')
                response = model.generate_content(instructions)

                if response.parts:
                    full_response = response.parts[0].text.strip()

                    # Find the start of the enhanced prompt after the introductory phrase
                    intro_phrase = "Here's the enhanced prompt:"
                    intro_index = full_response.find(intro_phrase)

                    if intro_index != -1:
                        # Extract the text after the introductory phrase
                        enhanced_prompt_text = full_response[intro_index + len(intro_phrase):].strip()
                    else:
                        # Fallback: If the phrase is not found, assume the whole response is the prompt
                        enhanced_prompt_text = full_response

                    # Ensure proper formatting with resolution and aspect ratio
                    final_prompt = enforce_prompt_format(enhanced_prompt_text, resolution, aspect_ratio, negative_prompt)

                    return final_prompt
                else:
                    # Fallback to basic prompt formatting if no response
                    return enforce_prompt_format(prompt, resolution, aspect_ratio, negative_prompt)
            except Exception as e:
                logging.error(f"Error generating prompt with Gemini: {str(e)}")
                # Fallback to basic prompt formatting in case of error
                return enforce_prompt_format(prompt, resolution, aspect_ratio, negative_prompt)

        # User preferences are enabled or provided - use Gemini for enhancement
        # Get user preferences
        if hasattr(user_prefs, 'preferred_styles') and hasattr(user_prefs, 'preferred_moods'):
            style = user_prefs.preferred_styles[0] if user_prefs.preferred_styles else None
            mood = user_prefs.preferred_moods[0] if user_prefs.preferred_moods else None
        else:
            style = None
            mood = None

        # Get all settings from imagen_settings
        settings = user_prefs.imagen_settings
        
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
        style_era = style_settings.get("style_era") # Added style_era
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
        texture = medium_settings.get("texture", "") # Note: 'texture' might conflict if also in detail_settings
        illustration_style = illustration_settings.get("style", "")
        line_quality = illustration_settings.get("line_quality", "")
        abstract_composition = abstract_settings.get("composition_type", "")
        movement_type = abstract_settings.get("movement_type", "")
        material_type = material_settings.get("material_type", "")
        material_finish = material_settings.get("finish", "")

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
        style_era = style_settings.get("style_era") # Added style_era
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
        texture = medium_settings.get("texture", "") # Note: 'texture' might conflict if also in detail_settings
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

        # Use PROMPT_INSTRUCTIONS from prompt_config.py with proper formatting
        instruction_context = PROMPT_INSTRUCTIONS.format(
            resolution=resolution if resolution else "Not specified",
            aspect_ratio=aspect_ratio if aspect_ratio else "16:9",
            color_scheme=color_scheme if color_scheme else "Not specified",
            lighting=lighting_type if lighting_type else "Not specified",
            composition=technique if technique else "Not specified",
            depth_of_field=depth_of_field if depth_of_field else "Not specified"
        )

        # Create a more comprehensive technical context with all settings
        technical_context = f"""
Create a detailed description for a wallpaper image featuring: {formatted_tags}

SUBJECT ANALYSIS:
Carefully analyze the subject "{formatted_tags}" and tailor your description to highlight its unique characteristics:
- For natural subjects: emphasize organic elements, textures, and environmental context
- For urban subjects: focus on architectural details, perspective, and urban atmosphere
- For abstract subjects: highlight patterns, shapes, and conceptual elements
- For space/cosmic subjects: emphasize scale, wonder, and celestial phenomena
- For fantasy subjects: create a cohesive magical or surreal atmosphere

USER STYLE PREFERENCES - ABSOLUTELY MANDATORY:
- Style: {style if style else "Not specified - adapt to subject unless overridden by other style settings"}
- Mood: {mood if mood else "Not specified - adapt to subject unless overridden by other style settings"}
- Art Movement: {art_movement if art_movement else "Not specified"}
- Style Era: {style_era if style_era else "Not specified"}

CRITICAL: You MUST fully integrate ALL provided user preferences below into your descriptive paragraph. Do not merely list them. Weave them naturally into the scene's description. Prioritize explicit user preferences (Style, Mood, Art Movement, Style Era) above all else.

MANDATORY TECHNICAL PARAMETERS:
Resolution: {resolution} - YOU MUST INCLUDE THIS EXACTLY AT THE END OF THE DESCRIPTION
Aspect Ratio: {aspect_ratio} - YOU MUST INCLUDE THIS EXACTLY AT THE END OF THE DESCRIPTION

TECHNICAL SPECIFICATIONS - FULLY INTEGRATE ALL PROVIDED VALUES:
# Camera
- Camera model: {camera_model if camera_model else "Not specified"}
- Lens: {lens_type if lens_type else "Not specified"}
- Focal length: {focal_length if focal_length else "Not specified"}
- Aperture: {aperture if aperture else "Not specified"}
- Shutter speed: {shutter_speed if shutter_speed else "Not specified"}
- ISO: {iso if iso else "Not specified"}
- Filter type: {filter_type if filter_type else "Not specified"}
- Special lens: {special_lens if special_lens else "Not specified"}
- Depth of field: {depth_of_field if depth_of_field else "Not specified"}
# Lighting
- Lighting type: {lighting_type if lighting_type else "Not specified"}
- Light quality: {light_quality if light_quality else "Not specified"}
- Time of day: {time_of_day if time_of_day else "Not specified"}
- Light source: {light_source if light_source else "Not specified"}
- Artificial lighting: {", ".join(artificial_sources) if artificial_sources else "None"}
# Composition
- Composition technique: {technique if technique else "Not specified"}
- Camera angle: {camera_angle if camera_angle else "Not specified"}
- Focal point: {focal_point if focal_point else "Not specified"}
- Perspective: {perspective if perspective else "Not specified"}
- Visual flow: {visual_flow if visual_flow else "Not specified"}
- Depth layering: {depth_layering if depth_layering else "Not specified"}
# Environment
- Weather: {weather if weather else "Not specified"}
- Season: {season if season else "Not specified"}
- Location type: {location_type if location_type else "Not specified"}
- Atmospheric effects: {", ".join(atmospheric_effects) if atmospheric_effects else "None"}
# Style Details
- Post-processing: {", ".join(post_processing) if post_processing else "None"}
# Detail & Quality
- Detail level: {detail_level if detail_level else "Not specified"}
- Texture quality: {texture_quality if texture_quality else "Not specified"}
- Special effects: {", ".join(special_effects) if special_effects else "None"}
- Rendering quality: {rendering_quality if rendering_quality else "Not specified"}
# Color
- Color scheme: {color_scheme if color_scheme else "Not specified"}
- Palette type: {palette_type if palette_type else "Not specified"}
- Color temperature: {color_temperature if color_temperature else "Not specified"}
# Specific Art Styles (Integrate if provided)
- Digital Software: {digital_software if digital_software else "Not specified"}
- Digital Effects: {", ".join(digital_effects) if digital_effects else "None"}
- Game Engine: {game_engine if game_engine else "Not specified"}
- Game Genre: {game_genre if game_genre else "Not specified"}
- Game Shader: {game_shader if game_shader else "Not specified"}
- Software Suite: {suite if suite else "Not specified"}
- Software Renderer: {renderer if renderer else "Not specified"}
- Software Version: {version if version else "Not specified"}
- Painting Medium: {painting_medium if painting_medium else "Not specified"}
- Brushwork: {brushwork if brushwork else "Not specified"}
- Medium Texture: {texture if texture else "Not specified"}
- Illustration Style: {illustration_style if illustration_style else "Not specified"}
- Line Quality: {line_quality if line_quality else "Not specified"}
- Abstract Composition: {abstract_composition if abstract_composition else "Not specified"}
- Abstract Movement: {movement_type if movement_type else "Not specified"}
- Material Type: {material_type if material_type else "Not specified"}
- Material Finish: {material_finish if material_finish else "Not specified"}

IMPORTANT GUIDELINES - FOLLOW WITHOUT FAIL:
1. Create ONE SINGLE, detailed paragraph describing the image.
2. NATURALLY INTEGRATE *ALL* provided User Preferences and Technical Specifications (except Resolution/Aspect Ratio) into the descriptive paragraph. Do NOT just list them. Describe *how* they affect the scene.
3. The subject "{formatted_tags}" MUST remain the central focus.
4. IGNORE any "Not specified" or "None" settings - do not mention them in the output.
5. The description MUST end *exactly* with "{resolution} resolution, {aspect_ratio} aspect ratio". No extra words before or after this phrase at the very end of the paragraph.
6. After the description paragraph, you MUST include the negative prompt section starting exactly with "Avoid: ".

OUTPUT FORMAT:
Your response MUST follow this exact format:
1. A single, detailed paragraph describing the image, integrating all preferences, ending with the resolution and aspect ratio.
2. A newline.
3. The negative prompt section, starting exactly with "Avoid: ".

Example Structure:
[Detailed descriptive paragraph incorporating all settings naturally...] {resolution} resolution, {aspect_ratio} aspect ratio
Avoid: [negative elements]

NEGATIVE PROMPT - ALWAYS INCLUDE:
The following elements MUST be avoided in the image: {negative_prompt}
"""

        # Generate prompt using Gemini
        gemini_api_key = os.environ.get("GEMINI_API_KEY")
        if not gemini_api_key:
            logging.warning("No Gemini API key configured")
            # Return a formatted version of the simple tags
            return enforce_prompt_format(formatted_tags, resolution, aspect_ratio, negative_prompt)

        try:
            genai.configure(api_key=gemini_api_key)
            # Use gemini-2.0-flash as in the no-prefs path
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(instruction_context + "\n\n" + technical_context)

            if response.text:
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

                # No caching here for random prompts, as they are inherently random
                # prompt_cache[cache_key] = final_prompt # Removed caching
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
        logging.error(f"Error in generate_prompt_random: {e}")
        return ", ".join(tags)  # Fallback to basic tags if error occurs

def enhance_custom_prompt(custom_prompt, user_prefs=None, description=None):
    """Enhance the custom prompt using the Gemini model based on user preferences.
    
    Args:
        custom_prompt: The original prompt to enhance
        user_prefs: Optional user preferences object. If None and use_user_preferences
                   is True, the function will use the global user_prefs.
        description: Optional description string from preset to include in prompt generation.
    
    Returns:
        str: An enhanced version of the custom prompt
    """
    style_era = None
    try:
        global use_user_preferences
        
        # If user_prefs is not provided and we should use preferences, get them from global
        if user_prefs is None and use_user_preferences:
            # Import here to avoid circular imports
            from wallpaper_generator import user_prefs as global_user_prefs
            user_prefs = global_user_prefs
        
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
                    "negative_prompt": "ugly, disfigured, low quality, blurry, nsfw, watermark, signature, out of frame, extra limbs, poorly drawn face, twisted limbs, distorted face, bad proportions, bad anatomy"
                }
            )
            # Don't return early - continue with enhancement using minimal preferences
            # Basic artwork style for no preferences
            style = None  # Don't enforce a style when no preferences
            mood = None
            resolution = "3840x2160"
            aspect_ratio = "16:9"
            negative_prompt = "ugly, disfigured, low quality, blurry, nsfw, watermark, signature, out of frame, extra limbs"
            
            # Detect specific art mediums in the prompt and preserve them
            art_mediums = {
                "watercolor": ["3d", "3d render", "3d art", "digital art", "oil painting", "acrylic", "photograph"],
                "oil painting": ["3d", "3d render", "3d art", "digital art", "watercolor", "acrylic", "photograph"],
                "sketch": ["3d", "3d render", "3d art", "digital art", "oil painting", "acrylic", "photograph"],
                "pencil": ["3d", "3d render", "3d art", "digital art", "oil painting", "acrylic", "photograph"],
                "acrylic": ["3d", "3d render", "3d art", "digital art", "oil painting", "watercolor", "photograph"],
                "drawing": ["3d", "3d render", "3d art", "digital art", "oil painting", "acrylic", "photograph"],
                "illustration": ["3d", "3d render", "3d art", "photograph"],
                "photograph": ["3d", "3d render", "3d art", "digital art", "oil painting", "acrylic", "watercolor"],
                "3d": ["oil painting", "watercolor", "acrylic", "pencil", "sketch", "drawing", "photograph"],
                "digital art": ["oil painting", "watercolor", "acrylic", "pencil", "sketch", "photograph"],
            }
            
            # Check if any medium is mentioned in the prompt
            detected_medium = None
            for medium, competing_mediums in art_mediums.items():
                if medium.lower() in custom_prompt.lower():
                    detected_medium = medium
                    # Add competing mediums to negative prompt to ensure preservation
                    for competing in competing_mediums:
                        if competing not in negative_prompt:
                            negative_prompt += f", {competing}"
                    logging.info(f"Detected art medium: {medium}, added competing mediums to negative prompt")
                    break
            
            # If a medium was detected, add it explicitly to the instruction
            medium_instruction = ""
            if detected_medium:
                medium_instruction = f"""
CRITICAL: This prompt explicitly mentions the art medium "{detected_medium}".
You MUST preserve this EXACT medium in your enhancement.
DO NOT convert it to any other medium (especially not 3D or digital art if traditional medium was specified).
Use terminology specific to {detected_medium} in your enhancement.
The negative prompt has been configured to exclude competing art styles.
"""
            
            # Initialize all variables needed for formatting to avoid reference errors
            camera_model = None
            lens_type = None
            aperture = None
            special_lens = None
            depth_of_field = None
            time_of_day = None
            lighting_type = None
            light_quality = None
            light_source = None
            artificial_sources = []
            technique = None
            camera_angle = None
            visual_flow = None
            depth_layering = None
            focal_point = None
            perspective = None
            weather = None
            season = None
            atmospheric_effects = []
            location_type = None
            art_movement = None
            post_processing = []
            detail_level = None
            texture_quality = None
            special_effects = []
            color_scheme = None
            palette_type = None
            color_temperature = None
            rendering_quality = None
            settings = user_prefs.imagen_settings
            
            # Use the strict no-preferences instructions instead of standard ones
            original_prompt_prefix = f"""ENHANCE THIS EXACT PROMPT: "{custom_prompt}"

CRITICAL INSTRUCTION: 
If this prompt specifies ANY artistic medium (watercolor, oil painting, 3D, digital art, etc.), you MUST PRESERVE IT EXACTLY.
DO NOT convert between mediums - a watercolor must stay watercolor, an oil painting must stay oil painting, etc.
{medium_instruction}
"""
            # Add description if provided
            if description:
                original_prompt_prefix += f"\nPRESET DESCRIPTION:\n{description}\n"

            original_prompt_prefix += f"""
SUBJECT ANALYSIS:
Carefully analyze the subject "{custom_prompt}" and tailor your enhancement while STRICTLY PRESERVING the original content:
- If it mentions a specific art style or medium (watercolor, oil painting, etc.), you MUST maintain that EXACT style/medium
- The style/medium mentioned is THE MOST IMPORTANT aspect to preserve
- If it describes specific subjects, they MUST remain the central focus
- All descriptive elements MUST be preserved exactly as specified

MANDATORY TECHNICAL PARAMETERS:
Resolution: {resolution} - YOU MUST INCLUDE THIS IN YOUR FINAL PROMPT
Aspect Ratio: {aspect_ratio} - YOU MUST INCLUDE THIS IN YOUR FINAL PROMPT

"""
            # Use the no preferences instruction template
            enhancement_instructions = original_prompt_prefix + NO_PREFS_PROMPT_INSTRUCTIONS.format(
                resolution=resolution,
                aspect_ratio=aspect_ratio
            )
            
            # Add explicit negative prompt section
            enhancement_instructions += f"""

NEGATIVE PROMPT - ALWAYS INCLUDE:
The following elements must be avoided in the image: {negative_prompt}

OUTPUT FORMAT:
Your response must follow this exact format:
1. A single, detailed paragraph describing the image that FAITHFULLY preserves the original prompt
2. MUST end the description with "{resolution} resolution, {aspect_ratio} aspect ratio"
3. End with "Avoid: [negative elements]"
"""
            
        else:
            # Get user preferences if they exist
            style = user_prefs.preferred_styles[0] if hasattr(user_prefs, 'preferred_styles') and user_prefs.preferred_styles else None
            mood = user_prefs.preferred_moods[0] if hasattr(user_prefs, 'preferred_moods') and user_prefs.preferred_moods else None
            
            # Get all settings from imagen_settings
            settings = user_prefs.imagen_settings

            
        # Camera Settings
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

        # Lighting Settings
        lighting_settings = settings.get("lighting_settings", {})
        time_of_day = lighting_settings.get("time_of_day") if lighting_settings else None
        lighting_type = lighting_settings.get("lighting_type") if lighting_settings else None
        light_quality = lighting_settings.get("light_quality") if lighting_settings else None
        light_source = lighting_settings.get("light_source") if lighting_settings else None
        artificial_sources = lighting_settings.get("artificial_sources", []) if lighting_settings else []

        # Composition Settings
        composition_settings = settings.get("composition_settings", {})
        technique = composition_settings.get("technique") if composition_settings else None
        camera_angle = composition_settings.get("camera_angle") if composition_settings else None
        visual_flow = composition_settings.get("visual_flow") if composition_settings else None
        depth_layering = composition_settings.get("depth_layering") if composition_settings else None
        focal_point = composition_settings.get("focal_point") if composition_settings else None
        perspective = composition_settings.get("perspective") if composition_settings else None

        # Environment Settings
        environment_settings = settings.get("environment_settings", {})
        weather = environment_settings.get("weather") if environment_settings else None
        season = environment_settings.get("season") if environment_settings else None
        atmospheric_effects = environment_settings.get("atmospheric_effects", []) if environment_settings else []
        location_type = environment_settings.get("location_type") if environment_settings else None

        # Style Settings
        style_settings = settings.get("style_settings", {})
        art_movement = style_settings.get("art_movement") if style_settings else None
        post_processing = style_settings.get("post_processing", []) if style_settings else []
        style_era = style_settings.get("style_era") if style_settings else None

        # Detail Settings
        detail_settings = settings.get("detail_settings", {})
        detail_level = detail_settings.get("detail_level") if detail_settings else None
        texture_quality = detail_settings.get("texture_quality") if detail_settings else None
        special_effects = detail_settings.get("special_effects", []) if detail_settings else []

        # Color Settings
        color_settings = settings.get("color_settings", {})
        color_scheme = color_settings.get("color_scheme") if color_settings else None
        palette_type = color_settings.get("palette_type") if color_settings else None
        color_temperature = color_settings.get("color_temperature") if color_settings else None

        # Quality Settings
        quality_settings = settings.get("quality_settings", {})
        resolution = quality_settings.get("resolution", "3840x2160") if quality_settings else "3840x2160"
        rendering_quality = quality_settings.get("rendering_quality") if quality_settings else None
        aspect_ratio = user_prefs.aspect_ratio if hasattr(user_prefs, 'aspect_ratio') else "16:9"

        # Art style variables for f-string use (guaranteed assigned)
        digital_settings = settings.get("digital_settings", {})
        digital_software = digital_settings.get("software", "") if digital_settings else ""
        digital_effects = digital_settings.get("digital_effects", []) if digital_settings else []
        game_engine_settings = settings.get("game_engine_settings", {})
        game_engine = game_engine_settings.get("engine_type", "") if game_engine_settings else ""
        game_genre = game_engine_settings.get("game_genre", "") if game_engine_settings else ""
        game_shader = game_engine_settings.get("shader_type", "") if game_engine_settings else ""
        software_settings = settings.get("software_settings", {})
        suite = software_settings.get("suite") if software_settings else None
        renderer = software_settings.get("renderer") if software_settings else None
        version = software_settings.get("version") if software_settings else None
        medium_settings = settings.get("medium_settings", {})
        painting_medium = medium_settings.get("painting_medium", "") if medium_settings else ""
        brushwork = medium_settings.get("brushwork", "") if medium_settings else ""
        texture = medium_settings.get("texture", "") if medium_settings else ""
        illustration_settings = settings.get("illustration_settings", {})
        illustration_style = illustration_settings.get("style", "") if illustration_settings else ""
        line_quality = illustration_settings.get("line_quality", "") if illustration_settings else ""
        abstract_settings = settings.get("abstract_settings", {})
        abstract_composition = abstract_settings.get("composition_type", "") if abstract_settings else ""
        movement_type = abstract_settings.get("movement_type", "") if abstract_settings else ""
        material_settings = settings.get("material_settings", {})
        material_type = material_settings.get("material_type", "") if material_settings else ""
        material_finish = material_settings.get("finish", "") if material_settings else ""

        # Get negative prompt if available
        negative_prompt = settings.get("negative_prompt", "")
        
        # Use CUSTOM_PROMPT_INSTRUCTIONS from prompt_config.py with proper formatting
        # Add a prefix to make extra sure the prompt is preserved

        style_settings = settings.get("style_settings", {}) if 'settings' in locals() else {}
        art_movement = style_settings.get("art_movement") if style_settings else None
        style_era = style_settings.get("style_era") if style_settings else None

        if 'style_era' not in locals():
            style_era = None

        original_prompt_prefix = f"""ENHANCE THIS EXACT PROMPT: "{custom_prompt}"

SUBJECT ANALYSIS:
Carefully analyze the subject "{custom_prompt}" and tailor your enhancement to highlight its unique characteristics:
- For natural subjects: emphasize organic elements, textures, and environmental context
- For urban subjects: focus on architectural details, perspective, and urban atmosphere
- For abstract subjects: highlight patterns, shapes, and conceptual elements
- For space/cosmic subjects: emphasize scale, wonder, and celestial phenomena
- For fantasy subjects: create a cohesive magical or surreal atmosphere

MANDATORY TECHNICAL PARAMETERS:
Resolution: {resolution} - YOU MUST INCLUDE THIS IN YOUR FINAL PROMPT
Aspect Ratio: {aspect_ratio} - YOU MUST INCLUDE THIS IN YOUR FINAL PROMPT

"""
        
        enhancement_instructions = original_prompt_prefix + f"""
        
        USER STYLE PREFERENCES - ABSOLUTELY MANDATORY:
        - Style: {style if style else "Not specified - adapt to subject unless overridden by other style settings"}
        - Mood: {mood if mood else "Not specified - adapt to subject unless overridden by other style settings"}
        - Art Movement: {art_movement if art_movement else "Not specified"}
        - Style Era: {style_era if style_era else "Not specified"}
        
        CRITICAL: You MUST enhance the original prompt ("{custom_prompt}") by fully integrating ALL provided user preferences below into the descriptive paragraph. Do not merely list them. Weave them naturally into the scene's description. Prioritize explicit user preferences (Style, Mood, Art Movement, Style Era) and the original prompt's core subject/intent above all else. DO NOT change the core subject.
        
        MANDATORY TECHNICAL PARAMETERS:
        Resolution: {resolution} - YOU MUST INCLUDE THIS EXACTLY AT THE END OF THE DESCRIPTION
        Aspect Ratio: {aspect_ratio} - YOU MUST INCLUDE THIS EXACTLY AT THE END OF THE DESCRIPTION
        
        TECHNICAL SPECIFICATIONS - FULLY INTEGRATE ALL PROVIDED VALUES INTO THE ENHANCEMENT:
        # Camera
        - Camera model: {camera_model if camera_model else "Not specified"}
        - Lens: {lens_type if lens_type else "Not specified"}
        - Focal length: {focal_length if focal_length else "Not specified"}
        - Aperture: {aperture if aperture else "Not specified"}
        - Shutter speed: {shutter_speed if shutter_speed else "Not specified"}
        - ISO: {iso if iso else "Not specified"}
        - Filter type: {filter_type if filter_type else "Not specified"}
        - Special lens: {special_lens if special_lens else "Not specified"}
        - Depth of field: {depth_of_field if depth_of_field else "Not specified"}
        # Lighting
        - Lighting type: {lighting_type if lighting_type else "Not specified"}
        - Light quality: {light_quality if light_quality else "Not specified"}
        - Time of day: {time_of_day if time_of_day else "Not specified"}
        - Light source: {light_source if light_source else "Not specified"}
        - Artificial lighting: {", ".join(artificial_sources) if artificial_sources else "None"}
        # Composition
        - Composition technique: {technique if technique else "Not specified"}
        - Camera angle: {camera_angle if camera_angle else "Not specified"}
        - Focal point: {focal_point if focal_point else "Not specified"}
        - Perspective: {perspective if perspective else "Not specified"}
        - Visual flow: {visual_flow if visual_flow else "Not specified"}
        - Depth layering: {depth_layering if depth_layering else "Not specified"}
        # Environment
        - Weather: {weather if weather else "Not specified"}
        - Season: {season if season else "Not specified"}
        - Location type: {location_type if location_type else "Not specified"}
        - Atmospheric effects: {", ".join(atmospheric_effects) if atmospheric_effects else "None"}
        # Style Details
        - Post-processing: {", ".join(post_processing) if post_processing else "None"}
        # Detail & Quality
        - Detail level: {detail_level if detail_level else "Not specified"}
        - Texture quality: {texture_quality if texture_quality else "Not specified"}
        - Special effects: {", ".join(special_effects) if special_effects else "None"}
        - Rendering quality: {rendering_quality if rendering_quality else "Not specified"}
        # Color
        - Color scheme: {color_scheme if color_scheme else "Not specified"}
        - Palette type: {palette_type if palette_type else "Not specified"}
        - Color temperature: {color_temperature if color_temperature else "Not specified"}
        # Specific Art Styles (Integrate if provided)
        - Digital Software: {digital_software if digital_software else "Not specified"}
        - Digital Effects: {", ".join(digital_effects) if digital_effects else "None"}
        - Game Engine: {game_engine if game_engine else "Not specified"}
        - Game Genre: {game_genre if game_genre else "Not specified"}
        - Game Shader: {game_shader if game_shader else "Not specified"}
        - Software Suite: {suite if suite else "Not specified"}
        - Software Renderer: {renderer if renderer else "Not specified"}
        - Software Version: {version if version else "Not specified"}
        - Painting Medium: {painting_medium if painting_medium else "Not specified"}
        - Brushwork: {brushwork if brushwork else "Not specified"}
        - Medium Texture: {texture if texture else "Not specified"}
        - Illustration Style: {illustration_style if illustration_style else "Not specified"}
        - Line Quality: {line_quality if line_quality else "Not specified"}
        - Abstract Composition: {abstract_composition if abstract_composition else "Not specified"}
        - Abstract Movement: {movement_type if movement_type else "Not specified"}
        - Material Type: {material_type if material_type else "Not specified"}
        - Material Finish: {material_finish if material_finish else "Not specified"}
        
        IMPORTANT GUIDELINES - FOLLOW WITHOUT FAIL:
        1. Create ONE SINGLE, detailed paragraph enhancing the original prompt "{custom_prompt}".
        2. NATURALLY INTEGRATE *ALL* provided User Preferences and Technical Specifications (except Resolution/Aspect Ratio) into the descriptive paragraph. Do NOT just list them. Describe *how* they affect the scene.
        3. The CORE SUBJECT AND INTENT of the original prompt "{custom_prompt}" MUST be preserved.
        4. IGNORE any "Not specified" or "None" settings - do not mention them in the output.
        5. The description MUST end *exactly* with "{resolution} resolution, {aspect_ratio} aspect ratio". No extra words before or after this phrase at the very end of the paragraph.
        6. After the description paragraph, you MUST include the negative prompt section starting exactly with "Avoid: ".
        
        OUTPUT FORMAT:
        Your response MUST follow this exact format:
        1. A single, detailed paragraph describing the image, enhancing the original prompt, integrating all preferences, ending with the resolution and aspect ratio.
        2. A newline.
        3. The negative prompt section, starting exactly with "Avoid: ".
        
        Example Structure:
        [Detailed descriptive paragraph enhancing "{custom_prompt}" incorporating all settings naturally...] {resolution} resolution, {aspect_ratio} aspect ratio
        Avoid: [negative elements]
        
        NEGATIVE PROMPT - ALWAYS INCLUDE:
        The following elements MUST be avoided in the image: {negative_prompt}
        # Merged negative prompt and output format directly into the main f-string
        
                    NEGATIVE PROMPT - ALWAYS INCLUDE:
                    The following elements must be avoided in the image: {negative_prompt}
                    
                    OUTPUT FORMAT:
                    Your response must follow this exact format:
                    1. A single, detailed paragraph describing the image
                    2. MUST end the description with "{resolution} resolution, {aspect_ratio} aspect ratio"
                    3. End with "Avoid: [negative elements]"
                    """

        
        if negative_prompt:
            enhancement_instructions += f"\n\nAvoid the following negative elements: {negative_prompt}"
        
        # Generate enhanced prompt using Gemini
        gemini_api_key = os.environ.get("GEMINI_API_KEY")
        if not gemini_api_key:
            logging.warning("No Gemini API key configured")
            # Return formatted version of the original prompt
            return enforce_prompt_format(custom_prompt, resolution, aspect_ratio, negative_prompt)
        
        try:
            genai.configure(api_key=gemini_api_key)
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(enhancement_instructions)

            if response.parts and len(response.parts) > 0:
                full_response = response.parts[0].text.strip()
                
                # If we're not using user preferences, apply the art medium enforcement
                if not use_user_preferences:
                    full_response = enforce_art_medium(full_response, custom_prompt)
                
                # Parse the response to separate prompt and negative prompt
                prompt_parts = full_response.split("Avoid:")
                
                if len(prompt_parts) > 1:
                    # If successfully parsed into two parts
                    main_prompt = prompt_parts[0].strip()
                    negative_part = prompt_parts[1].strip()
                    
                    # Verify that the enhanced prompt still contains the core subject
                    if custom_prompt.lower() not in main_prompt.lower():
                        logging.warning("Enhanced prompt doesn't contain original subject, prepending it")
                        main_prompt = f"{custom_prompt}, {main_prompt}"
                        
                    # Reassemble the prompt
                    return f"{main_prompt}. Avoid: {negative_part}"
                else:
                    # If not parsed properly, enforce art medium directly
                    enhanced_prompt = enforce_art_medium(full_response, custom_prompt)
                    
                    # Verify that the enhanced prompt still contains the core subject
                    if custom_prompt.lower() not in enhanced_prompt.lower():
                        logging.warning("Enhanced prompt doesn't contain original subject, prepending it")
                        enhanced_prompt = f"{custom_prompt}, {enhanced_prompt}"
                    return enhanced_prompt
            else:
                # Return formatted version of the original prompt if no parts in response
                return enforce_prompt_format(custom_prompt, resolution, aspect_ratio, negative_prompt)

        except Exception as e:
            logging.error(f"Error generating prompt with Gemini: {str(e)}")
            # Return formatted version of the original prompt
            return enforce_prompt_format(custom_prompt, resolution, aspect_ratio, negative_prompt)

    except Exception as e:
        logging.exception(f"Error enhancing prompt with Gemini: {e}")
        logging.warning(f"Error enhancing prompt with Gemini: {e}")
        # Return formatted version of the original prompt
        return enforce_prompt_format(custom_prompt, resolution, aspect_ratio, negative_prompt)


def enforce_prompt_format(prompt, resolution, aspect_ratio, negative_prompt=""):
    """
    Enforce a consistent format for all prompts to ensure technical parameters are included.
    
    Args:
        prompt (str): The original prompt text
        resolution (str): Resolution setting (e.g., "1920x1080")
        aspect_ratio (str): Aspect ratio setting (e.g., "16:9")
        negative_prompt (str): Negative prompt text
        
    Returns:
        str: A properly formatted prompt that includes all required parameters
    """
    # Start by splitting the prompt into main and negative parts
    main_prompt = prompt
    neg_prompt = negative_prompt
    
    # Check if the prompt already contains a negative prompt section
    if "avoid:" in prompt.lower():
        parts = prompt.lower().split("avoid:")
        main_prompt = parts[0].strip()
        
        # If there's already a negative part, use it (but don't include any resolution/aspect ratio from it)
        if len(parts) > 1:
            neg_part = parts[1].strip()
            
            # Remove any resolution information from the negative part
            if resolution.lower() in neg_part.lower():
                neg_part = re.sub(r'(?i)' + re.escape(resolution) + r'(?:\s+resolution)?', '', neg_part)
            
            # Remove any aspect ratio information from the negative part
            if aspect_ratio.lower() in neg_part.lower():
                neg_part = re.sub(r'(?i)' + re.escape(aspect_ratio) + r'(?:\s+aspect\s+ratio)?', '', neg_part)
            
            # Use this cleaned negative part
            neg_prompt = neg_part
    else:
        # No negative part in the prompt, use main_prompt as is
        main_prompt = prompt
    
    # Clean up the main prompt
    clean_prompt = main_prompt.strip()
    
    # Remove any existing resolution mentions to avoid duplication
    if resolution.lower() in clean_prompt.lower():
        clean_prompt = re.sub(r'(?i)' + re.escape(resolution) + r'(?:\s+resolution)?', '', clean_prompt)
    
    # Remove any existing aspect ratio mentions to avoid duplication
    if aspect_ratio.lower() in clean_prompt.lower():
        clean_prompt = re.sub(r'(?i)' + re.escape(aspect_ratio) + r'(?:\s+aspect\s+ratio)?', '', clean_prompt)
    
    # Remove any trailing placeholder words without values
    clean_prompt = re.sub(r'(?i)resolution\s*$', '', clean_prompt)
    clean_prompt = re.sub(r'(?i)aspect\s+ratio\s*$', '', clean_prompt)
    
    # Clean up any resulting double commas or trailing commas
    clean_prompt = re.sub(r',\s*,', ',', clean_prompt)
    clean_prompt = re.sub(r',\s*$', '', clean_prompt)
    
    # Add resolution to main prompt
    if not clean_prompt.endswith(".") and not clean_prompt.endswith(","):
        clean_prompt += ","
    clean_prompt += f" {resolution} resolution"
    
    # Add aspect ratio to main prompt
    if not clean_prompt.endswith(".") and not clean_prompt.endswith(","):
        clean_prompt += ","
    clean_prompt += f" {aspect_ratio} aspect ratio"
    
    # Clean up any additional trailing commas before adding negative prompt
    clean_prompt = re.sub(r',\s*$', '', clean_prompt)
    
    # Add the negative prompt
    if neg_prompt:
        clean_prompt += f". Avoid: {neg_prompt}"
    
    return clean_prompt

def select_random_tags():
    """
    Select a diverse set of tags for Gemini prompt generation by sampling from multiple categories.
    Ensures broader creative diversity and theming.
    Returns:
        list: A deduplicated, randomized selection of tags from various conceptual categories.
    """
    from config import (
        nature_tags, space_tags, sea_tags, flowers_tags, urban_tags, fantasy_tags, abstract_tags, mood_tags,
        weather_tags, time_tags, season_tags, color_tags, material_tags, lighting_tags, pattern_tags,
        terrain_tags, emotion_tags, architecture_tags
    )

    # Define desired categories to sample from
    categories = [
        nature_tags, space_tags, sea_tags, flowers_tags, urban_tags, fantasy_tags,
        abstract_tags, mood_tags, weather_tags, time_tags, season_tags, color_tags,
        material_tags, lighting_tags, pattern_tags, terrain_tags, emotion_tags, architecture_tags
    ]

    # Sample one tag from each category (if non-empty)
    selected = []
    for cat in categories:
        if cat:
            selected.append(random.choice(cat))

    # Deduplicate and shuffle order
    deduped = list(set(selected))
    random.shuffle(deduped)

    # Choose a final count (e.g., 5–8) for best prompt focus
    final_count = random.randint(6, 9)
    return deduped[:final_count]

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
    global use_user_preferences
    
    # If user_prefs is not provided and we should use preferences, get them from global
    if user_prefs is None and use_user_preferences:
        # Import here to avoid circular imports
        from wallpaper_generator import user_prefs as global_user_prefs
        user_prefs = global_user_prefs
    
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
    if user_prefs and use_user_preferences:
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

# Simple class for minimal user preferences when not using the full user preferences
class SimplePrefs:
    def __init__(self, aspect_ratio="16:9", imagen_settings=None):
        self.aspect_ratio = aspect_ratio
        self.imagen_settings = imagen_settings or {}

def enhance_negative_prompt(negative_prompt_text: str) -> str:
    """
    Enhance a given negative prompt string using Gemini.

    Args:
        negative_prompt_text: The original negative prompt text.

    Returns:
        str: An enhanced version of the negative prompt.
    """
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        logging.warning("No Gemini API key configured for negative prompt enhancement.")
        return negative_prompt_text # Return original if no API key

    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-2.0-flash') # Use a fast model for this
        instruction = f"""
Enhance the following negative prompt by adding related terms and synonyms to make it more comprehensive.
Keep the output as a comma-separated list. Do not add any introductory or concluding phrases.

Original negative prompt: {negative_prompt_text}

Enhanced negative prompt:
"""
        response = model.generate_content(instruction)

        if response.text:
            enhanced_text = response.text.strip()
            # Clean up potential unwanted characters or formatting from Gemini
            enhanced_text = re.sub(r'^["\']|["\']$', '', enhanced_text) # Remove leading/trailing quotes
            enhanced_text = re.sub(r'\s*,\s*', ', ', enhanced_text) # Standardize comma spacing
            return enhanced_text
        else:
            logging.warning("Gemini returned empty response for negative prompt enhancement.")
            return negative_prompt_text # Return original if response is empty

    except Exception as e:
        logging.error(f"Error enhancing negative prompt with Gemini: {e}")
        return negative_prompt_text # Return original in case of error
