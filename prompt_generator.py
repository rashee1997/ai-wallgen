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
import signal
import sys
from typing import Dict, List, Optional, Any, Union

# Third-party imports
try:
    import google.generativeai as genai
except ImportError:
    logging.warning("google.generativeai module not found. Some features will be disabled.")

# Import prompt configuration
from prompt_config import (
    nature_tags, space_tags, sea_tags, flowers_tags, urban_tags,
    fantasy_tags, abstract_tags, mood_tags, available_genres,
    PROMPT_INSTRUCTIONS, CUSTOM_PROMPT_INSTRUCTIONS
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
gemini_model_name = "gemini-2.0-flash"

# Flag to determine whether to use user preferences or not
use_user_preferences = True

# Configure signal handler for the module
def prompt_signal_handler(sig, frame):
    """Handle Ctrl+C interrupts during prompt generation.
    
    This function allows for a clean exit when Ctrl+C is pressed during
    long-running API calls like prompt generation.
    """
    logging.info("Keyboard interrupt detected during prompt generation.")
    print("\nInterrupted during prompt generation. Exiting...")
    sys.exit(0)

# Register the signal handler for this module
signal.signal(signal.SIGINT, prompt_signal_handler)

def set_prompt_preferences(use_preferences: bool):
    """Set whether to use user preferences for prompt generation.
    
    Args:
        use_preferences: Boolean flag to indicate if user preferences should be used
    """
    global use_user_preferences
    use_user_preferences = use_preferences
    logging.info(f"Prompt generation with user preferences: {use_preferences}")

def generate_prompt_gemini(tags, user_prefs=None):
    """Generate a detailed prompt using Gemini and user preferences.
    
    Args:
        tags: List of tags to include in the prompt
        user_prefs: Optional user preferences object. If None and use_user_preferences
                    is True, the function will use the global user_prefs.
    
    Returns:
        str: A detailed prompt for image generation
    """
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
                    "quality_settings": {"resolution": "1920x1080"}
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
        
        # Extract camera settings for the prompt
        camera_settings = settings.get("camera_settings", {})
        camera_model = camera_settings.get("camera_model")
        lens_type = camera_settings.get("lens_type")
        aperture = camera_settings.get("aperture")
        special_lens = camera_settings.get("special_lens")
        depth_of_field = camera_settings.get("depth_of_field")
        
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
        
        # Extract environment settings for the prompt
        environment_settings = settings.get("environment_settings", {})
        weather = environment_settings.get("weather")
        season = environment_settings.get("season")
        location_type = environment_settings.get("location_type")
        atmospheric_effects = environment_settings.get("atmospheric_effects", [])
        
        # Extract style settings for the prompt
        style_settings = settings.get("style_settings", {})
        art_movement = style_settings.get("art_movement")
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
        resolution = quality_settings.get("resolution", "1920x1080")
        rendering_quality = quality_settings.get("rendering_quality")
        aspect_ratio = user_prefs.aspect_ratio if hasattr(user_prefs, 'aspect_ratio') else "16:9"
        
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

USER STYLE PREFERENCES:
- Style: {style if style else "Use what makes sense for the subject"}
- Mood: {mood if mood else "Use what makes sense for the subject"}
- Art Movement: {art_movement if art_movement else "Use what makes sense for the subject"}

MANDATORY TECHNICAL PARAMETERS:
Resolution: {resolution} - YOU MUST INCLUDE THIS IN YOUR FINAL PROMPT
Aspect Ratio: {aspect_ratio} - YOU MUST INCLUDE THIS IN YOUR FINAL PROMPT

TECHNICAL SPECIFICATIONS:
- Camera model: {camera_model if camera_model else "Not specified"}
- Lens: {lens_type if lens_type else "Not specified"}
- Aperture: {aperture if aperture else "Not specified"}
- Special lens: {special_lens if special_lens else "Not specified"}
- Depth of field: {depth_of_field if depth_of_field else "Not specified"}
- Lighting type: {lighting_type if lighting_type else "Not specified"}
- Light quality: {light_quality if light_quality else "Not specified"}
- Time of day: {time_of_day if time_of_day else "Not specified"}
- Light source: {light_source if light_source else "Not specified"}
- Artificial lighting: {", ".join(artificial_sources) if artificial_sources else "None"}
- Composition technique: {technique if technique else "Not specified"}
- Camera angle: {camera_angle if camera_angle else "Not specified"}
- Visual flow: {visual_flow if visual_flow else "Not specified"}
- Depth layering: {depth_layering if depth_layering else "Not specified"}
- Weather: {weather if weather else "Not specified"}
- Season: {season if season else "Not specified"}
- Location type: {location_type if location_type else "Not specified"}
- Atmospheric effects: {", ".join(atmospheric_effects) if atmospheric_effects else "None"}
- Post-processing: {", ".join(post_processing) if post_processing else "None"}
- Detail level: {detail_level if detail_level else "Not specified"}
- Texture quality: {texture_quality if texture_quality else "Not specified"}
- Special effects: {", ".join(special_effects) if special_effects else "None"}
- Color scheme: {color_scheme if color_scheme else "Not specified"}
- Palette type: {palette_type if palette_type else "Not specified"}
- Color temperature: {color_temperature if color_temperature else "Not specified"}
- Resolution: {resolution if resolution else "Not specified"}
- Rendering quality: {rendering_quality if rendering_quality else "Not specified"}
- Aspect ratio: {aspect_ratio if aspect_ratio else "16:9"}

IMPORTANT GUIDELINES:
1. Create a cohesive, detailed prompt that incorporates all specified settings naturally
2. IGNORE any "Not specified" or "None" settings - do not include them
3. Focus on creating a visually striking image suitable for a desktop wallpaper
4. Ensure the subject "{formatted_tags}" remains the central focus
5. Adapt the style and technical details to suit the specific subject matter
6. MUST end the description with "{resolution} resolution, {aspect_ratio} aspect ratio"
7. Always include a negative prompt section at the end

OUTPUT FORMAT:
Your response must follow this exact format:
1. A single, detailed paragraph describing the image
2. MUST end the description with "{resolution} resolution, {aspect_ratio} aspect ratio"
3. End with "Avoid: [negative elements]"

NEGATIVE PROMPT - ALWAYS INCLUDE:
The following elements must be avoided in the image: {negative_prompt}
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
        return enforce_prompt_format(formatted_tags_str, "1920x1080", "16:9", negative_prompt)

def generate_prompt_random(tags, user_prefs=None):
    """Generate a random prompt using the provided tags."""
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
                model = genai.GenerativeModel('gemini-2.0-flash')
                response = model.generate_content(instructions)

                if response.parts:
                    full_response = response.parts[0].text.strip()
                    
                    # Check if the enhanced prompt contains the original tags
                    # If not, prepend them to ensure they're included
                    if not all(tag.lower() in full_response.lower() for tag in tags):
                        logging.warning("Enhanced prompt doesn't contain original subject, prepending it")
                        full_response = f"{formatted_tags}, {full_response}"
                        
                    return full_response
                else:
                    # Fallback to basic prompt formatting if no response
                    return enforce_prompt_format(prompt, resolution, aspect_ratio, negative_prompt)
            except Exception as e:
                logging.error(f"Error generating prompt with Gemini: {str(e)}")
                # Fallback to basic prompt formatting in case of error
                return enforce_prompt_format(prompt, resolution, aspect_ratio, negative_prompt)
            
        # User preferences are enabled - use the original implementation
        # Get user preferences
        if hasattr(user_prefs, 'preferred_styles') and hasattr(user_prefs, 'preferred_moods'):
            style = user_prefs.preferred_styles[0] if user_prefs.preferred_styles else None
            mood = user_prefs.preferred_moods[0] if user_prefs.preferred_moods else None
        else:
            style = None
            mood = None
        
        # Get all settings from imagen_settings
        settings = user_prefs.imagen_settings
        
        # Extract camera settings
        camera_settings = settings.get("camera_settings", {})
        camera_model = camera_settings.get("camera_model")
        lens_type = camera_settings.get("lens_type")
        
        # Extract lighting settings
        lighting_settings = settings.get("lighting_settings", {})
        time_of_day = lighting_settings.get("time_of_day")
        lighting_type = lighting_settings.get("lighting_type")
        
        # Extract quality settings
        quality_settings = settings.get("quality_settings", {})
        detail_level = quality_settings.get("detail_level")
        rendering_quality = quality_settings.get("rendering_quality")
        
        # Extract style settings
        style_settings = settings.get("style_settings", {})
        art_movement = style_settings.get("art_movement")
        
        # Extract color settings
        color_settings = settings.get("color_settings", {})
        color_scheme = color_settings.get("color_scheme")
        
        # Build the prompt
        prompt_parts = []
        for tag in tags:
            # Try to enhance tag selection based on user preferences
            prompt_parts.append(tag)
            
        prompt = ", ".join(prompt_parts)
        
        # Add image quality enhancers
        quality_enhancers = []
        
        if style:
            quality_enhancers.append(style)
        if mood:
            quality_enhancers.append(mood)
        if art_movement:
            quality_enhancers.append(art_movement)
        if rendering_quality:
            quality_enhancers.append(rendering_quality)
        if detail_level:
            quality_enhancers.append(detail_level)
        if color_scheme:
            quality_enhancers.append(color_scheme)
        if camera_model:
            quality_enhancers.append(f"shot on {camera_model}")
        if lens_type:
            quality_enhancers.append(f"{lens_type} lens")
        if time_of_day:
            quality_enhancers.append(time_of_day.replace('_', ' '))
        if lighting_type:
            quality_enhancers.append(lighting_type.replace('_', ' '))
        
        # Add quality enhancers if available
        if quality_enhancers:
            prompt += ", " + ", ".join(quality_enhancers)
        
        return prompt
    except Exception as e:
        logging.error(f"Error in generate_prompt_random: {e}")
        return ", ".join(tags)  # Fallback to basic tags if error occurs

def enhance_custom_prompt(custom_prompt, user_prefs=None):
    """Enhance the custom prompt using the Gemini model based on user preferences.
    
    Args:
        custom_prompt: The original prompt to enhance
        user_prefs: Optional user preferences object. If None and use_user_preferences
                   is True, the function will use the global user_prefs.
    
    Returns:
        str: An enhanced version of the custom prompt
    """
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
                    "quality_settings": {"resolution": "1920x1080"},
                    "negative_prompt": "ugly, disfigured, low quality, blurry, nsfw, watermark, signature, out of frame, extra limbs, poorly drawn face, twisted limbs, distorted face, bad proportions, bad anatomy"
                }
            )
            # Don't return early - continue with enhancement using minimal preferences
            # Basic artwork style for no preferences
            style = None  # Don't enforce a style when no preferences
            mood = None
            resolution = "1920x1080"
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
            camera_model = camera_settings.get("camera_model")
            lens_type = camera_settings.get("lens_type")
            aperture = camera_settings.get("aperture")
            special_lens = camera_settings.get("special_lens")
            depth_of_field = camera_settings.get("depth_of_field")
            
            # Lighting Settings
            lighting_settings = settings.get("lighting_settings", {})
            time_of_day = lighting_settings.get("time_of_day")
            lighting_type = lighting_settings.get("lighting_type")
            light_quality = lighting_settings.get("light_quality")
            light_source = lighting_settings.get("light_source")
            artificial_sources = lighting_settings.get("artificial_sources", [])
            
            # Composition Settings
            composition_settings = settings.get("composition_settings", {})
            technique = composition_settings.get("technique")
            camera_angle = composition_settings.get("camera_angle")
            visual_flow = composition_settings.get("visual_flow")
            depth_layering = composition_settings.get("depth_layering")
            
            # Environment Settings
            environment_settings = settings.get("environment_settings", {})
            weather = environment_settings.get("weather")
            season = environment_settings.get("season")
            atmospheric_effects = environment_settings.get("atmospheric_effects", [])
            location_type = environment_settings.get("location_type")
            
            # Style Settings
            style_settings = settings.get("style_settings", {})
            art_movement = style_settings.get("art_movement")
            post_processing = style_settings.get("post_processing", [])
            
            # Detail Settings
            detail_settings = settings.get("detail_settings", {})
            detail_level = detail_settings.get("detail_level")
            texture_quality = detail_settings.get("texture_quality")
            special_effects = detail_settings.get("special_effects", [])
            
            # Color Settings
            color_settings = settings.get("color_settings", {})
            color_scheme = color_settings.get("color_scheme")
            palette_type = color_settings.get("palette_type")
            color_temperature = color_settings.get("color_temperature")
            
            # Quality Settings
            quality_settings = settings.get("quality_settings", {})
            resolution = quality_settings.get("resolution", "1920x1080")
            rendering_quality = quality_settings.get("rendering_quality")
            aspect_ratio = user_prefs.aspect_ratio if hasattr(user_prefs, 'aspect_ratio') else "16:9"
            
            # Get negative prompt if available
            negative_prompt = settings.get("negative_prompt", "")
        
        # Use CUSTOM_PROMPT_INSTRUCTIONS from prompt_config.py with proper formatting
        # Add a prefix to make extra sure the prompt is preserved
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
        
        enhancement_instructions = original_prompt_prefix + CUSTOM_PROMPT_INSTRUCTIONS.format(
            style=style if style else "Use what makes sense for the prompt",
            mood=mood if mood else "Use what makes sense for the prompt",
            resolution=resolution if resolution else "None specified",
            aspect_ratio=aspect_ratio if aspect_ratio else "16:9",
            color_scheme=color_scheme if color_scheme else "None specified",
            lighting=lighting_type if lighting_type else "None specified",
            composition=technique if technique else "None specified",
            depth_of_field=depth_of_field if depth_of_field else "None specified",
            camera_model=camera_model if camera_model else "None specified",
            lens_type=lens_type if lens_type else "None specified",
            aperture=aperture if aperture else "None specified",
            special_lens=special_lens if special_lens else "None specified",
            light_quality=light_quality if light_quality else "None specified",
            time_of_day=time_of_day if time_of_day else "None specified",
            artificial_sources=", ".join(artificial_sources) if artificial_sources else "None",
            camera_angle=camera_angle if camera_angle else "None specified",
            visual_flow=visual_flow if visual_flow else "None specified",
            depth_layering=depth_layering if depth_layering else "None specified",
            weather=weather if weather else "None specified",
            season=season if season else "None specified",
            atmospheric_effects=", ".join(atmospheric_effects) if atmospheric_effects else "None",
            location_type=location_type if location_type else "None specified",
            art_movement=art_movement if art_movement else "None specified",
            post_processing=", ".join(post_processing) if post_processing else "None",
            detail_level=detail_level if detail_level else "None specified",
            texture_quality=texture_quality if texture_quality else "None specified",
            special_effects=", ".join(special_effects) if special_effects else "None",
            palette_type=palette_type if palette_type else "None specified",
            color_temperature=color_temperature if color_temperature else "None specified",
            rendering_quality=rendering_quality if rendering_quality else "None specified",
            prompt=custom_prompt
        )
        
        # Add explicit negative prompt section
        enhancement_instructions += f"""

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

            if response.parts:
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
        logging.error(f"Error enhancing prompt with Gemini: {e}")
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
    """Select a random set of tags from all available tag categories.
    
    Returns:
        list: A random selection of 3-6 tags
    """
    all_tags = nature_tags + space_tags + sea_tags + flowers_tags + urban_tags + fantasy_tags + abstract_tags
    num_tags = random.randint(3, 6)  # Select between 3-6 tags
    return random.sample(all_tags, min(num_tags, len(all_tags)))

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