#!/usr/bin/env python3
"""Custom Prompt Generator Module - Functions for enhancing custom AI wallpaper prompts

This module contains functions for enhancing custom user-provided prompts with
additional details, style parameters, and technical specifications. It integrates
user preferences into the custom prompts to generate more detailed and consistent results.
"""
import logging
import os
import re
from typing import Dict, List, Optional, Any, Union

# Third-party imports
try:
    import google.generativeai as genai
except ImportError:
    logging.warning("google.generativeai module not found. Some features will be disabled.")

# Import types
from .types import SimplePrefs
from .. import gemini_config # Added for centralized Gemini config

# Import utilities
from .formatters import enforce_prompt_format

def enhance_custom_prompt(custom_prompt: str, user_prefs: Optional[Any] = None, description: Optional[str] = None) -> str:
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
            resolution = "3840x2160" # Default resolution
            aspect_ratio = "16:9"  # Default aspect ratio
            
            # Attempt to get resolution and aspect_ratio from SimplePrefs if available
            if hasattr(user_prefs, 'imagen_settings') and user_prefs.imagen_settings:
                quality_settings = user_prefs.imagen_settings.get("quality_settings", {})
                resolution = quality_settings.get("resolution", resolution)
            if hasattr(user_prefs, 'aspect_ratio') and user_prefs.aspect_ratio:
                aspect_ratio = user_prefs.aspect_ratio

            negative_prompt = "ugly, disfigured, low quality, blurry, nsfw, watermark, signature, out of frame, extra limbs"
            if hasattr(user_prefs, 'imagen_settings') and user_prefs.imagen_settings:
                 negative_prompt = user_prefs.imagen_settings.get("negative_prompt", negative_prompt)
            
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
            
            # Try to import no-preferences instructions for better subject preservation
            try:
                from no_preferences_prompt import (
                    NO_PREFS_PROMPT_INSTRUCTIONS,
                    enforce_art_medium
                )
            except ImportError:
                logging.warning("no_preferences_prompt.py not found. Using default instructions.")
                # Define fallbacks in case import fails
                NO_PREFS_PROMPT_INSTRUCTIONS = """
Generate a detailed and artistic prompt for a high-quality wallpaper image.

Technical parameters:
- Resolution: {resolution}
- Aspect ratio: {aspect_ratio}

The generated prompt should be detailed and descriptive, focusing on the subject provided.
Example format: "A detailed description of the image... {resolution} resolution, {aspect_ratio} aspect ratio"
Avoid: ugly, disfigured, low quality, blurry, nsfw, watermark, signature, out of frame, extra limbs
"""
                
                # Simple fallback enforce_art_medium function
                def enforce_art_medium(prompt, original_prompt):
                    return prompt  # Simply return prompt unchanged if module not found
            
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
            # Use the no preferences instruction template, but make it richer
            enhancement_instructions = original_prompt_prefix + f"""

ENHANCEMENT MISSION (No Specific User Preferences):
Your goal is to take the core subject "{custom_prompt}" and enrich it into a more vivid and descriptive prompt.
While no specific user preferences for style, camera, etc., are provided, you should creatively and subtly weave in general artistic and descriptive elements to add depth and detail.

CRITICAL:
- The original subject and any explicitly stated artistic medium in "{custom_prompt}" MUST be preserved and remain central.
- If a traditional medium (e.g., oil painting, watercolor) was in the original prompt, DO NOT convert it to digital art or 3D unless the original prompt implied it. Your enhancements should respect and build upon the stated medium.

CONSIDER ADDING DETAILS RELATED TO (if not conflicting with the original prompt):
- Visual Storytelling: What kind of scene or story does the subject imply? Expand on this.
- Atmosphere & Mood: What feeling should it evoke? (e.g., serene, dynamic, mysterious, tranquil, vibrant).
- Lighting Qualities: Describe potential lighting. (e.g., soft diffused light, dramatic directional light, ambient glow, sharp midday light, golden hour).
- Color Harmonies & Palette: Suggest general color ideas. (e.g., vibrant and contrasting, muted and analogous, monochromatic with accent, cool tones, warm tones).
- Compositional Elements: Hint at composition. (e.g., rule of thirds, leading lines, symmetry/asymmetry, sense of depth, focused subject, expansive view).
- Textural Details: Describe potential textures. (e.g., smooth and polished, rough and organic, detailed patterns, simple flat surfaces).
- Artistic Nuances: Subtly suggest general stylistic touches that complement the subject. (e.g., "a touch of painterly strokes," "clean digital rendering," "geometric forms," "flat shaded textures," "minimal detail"). These should be very general and complementary, and ALWAYS defer to any medium specified in the original prompt.

MANDATORY TECHNICAL PARAMETERS (MUST BE INCLUDED):
- Resolution: {resolution}
- Aspect Ratio: {aspect_ratio}

NEGATIVE PROMPT - ALWAYS INCLUDE:
The following elements must be avoided in the image: {negative_prompt}

OUTPUT FORMAT:
Your response must follow this exact format:
1. A single, detailed paragraph describing the image that FAITHFULLY preserves and ENRICHES the original prompt "{custom_prompt}".
2. The description MUST end with "{resolution} resolution, {aspect_ratio} aspect ratio".
3. The response MUST then end with "Avoid: [all elements from the negative prompt]".

Example of enriching (if original was "a red cube"):
"A vibrant red cube, exuding a sense of minimalist strength, resting on a subtly textured flat plane. The scene is bathed in soft, diffused morning light creating gentle highlights and shadows, emphasizing its clean geometric form. The color palette is primarily monochromatic focusing on shades of red with neutral undertones, creating a calm and focused composition. {resolution} resolution, {aspect_ratio} aspect ratio. Avoid: [negative elements]"
This is just an example; tailor your enrichment to the specific "{custom_prompt}".
"""
            
        else:
            # Get user preferences if they exist
            style = user_prefs.preferred_styles[0] if hasattr(user_prefs, 'preferred_styles') and user_prefs.preferred_styles else None
            mood = user_prefs.preferred_moods[0] if hasattr(user_prefs, 'preferred_moods') and user_prefs.preferred_moods else None
            
            # Get all settings from imagen_settings
            settings = user_prefs.imagen_settings if hasattr(user_prefs, 'imagen_settings') else {}

            
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

        # Try to use enforce_art_medium if it was imported
        enforce_medium = "enforce_art_medium" in locals() and callable(locals()["enforce_art_medium"])
        
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
        
        enhancement_instructions = original_prompt_prefix + f"""

🔮 CREATIVE ENHANCEMENT MISSION 🔮

Your task is to breathe life into this prompt while honoring its soul. Take the essence of "{custom_prompt}" and craft a vivid, immersive scene that elevates it to new heights without changing its fundamental spirit.

ARTISTIC VISION:
• Style: {style if style else "Be guided by what best serves the subject"}
• Mood: {mood if mood else "What emotions does this scene naturally evoke?"}
• Art Movement: {art_movement if art_movement else "Consider what artistic tradition would best frame this imagery"}
• Historical Context: {style_era if style_era else "What time period resonates with this scene?"}

CREATIVE METAMORPHOSIS GUIDANCE:
The original prompt seed "{custom_prompt}" is sacred—its core essence must remain intact and recognizable. Your challenge is to amplify its power through artistic interpretation, weaving in technical elements as natural characteristics of the scene, never as mechanical afterthoughts.

Imagine you're a master painter, cinematographer, and poet combined. Your canvas awaits the transformation of "{custom_prompt}" into something that retains its soul while gaining depth, atmosphere, and technical excellence.

ATMOSPHERE & ENVIRONMENT INSPIRATIONS:
• Weather conditions: {weather if weather else "What atmospheric conditions would heighten the scene's impact?"}
• Season: {season if season else "What time of year would create the perfect backdrop?"}
• Location essence: {location_type if location_type else "What setting would provide the ideal stage?"}
• Atmospheric qualities: {", ".join(atmospheric_effects) if atmospheric_effects else "Consider fog, mist, clear air, haze, or other atmospheric elements"}

VISUAL LANGUAGE ELEMENTS:
• Light character: {lighting_type if lighting_type else "How does light interact with this scene?"} with {light_quality if light_quality else "quality that enhances the subject"}
• Time of day: {time_of_day if time_of_day else "When would this scene be most striking?"}
• Color harmony: {color_scheme if color_scheme else "What color relationships would strengthen the scene?"} with {palette_type if palette_type else "palette reflecting the mood"} and {color_temperature if color_temperature else "temperature creating the right feeling"}
• Depth perception: {depth_of_field if depth_of_field else "How should focus be distributed across the scene?"}
• Spatial arrangement: {technique if technique else "What compositional technique would frame this best?"} with focus on {focal_point if focal_point else "the most important element"}

ARTISTIC EXECUTION SUGGESTIONS:
• Medium expression: {painting_medium if painting_medium else "Consider the perfect medium"} with {brushwork if brushwork else "technique that captures the right feeling"}
• Textural quality: {texture_quality if texture_quality else "What tactile qualities should be visible?"} with {texture if texture else "surface characteristics that enhance the scene"}
• Detail richness: {detail_level if detail_level else "How intricate should the scene be?"}
• Stylistic approach: {illustration_style if illustration_style else "What illustrative style would resonate?"} with {line_quality if line_quality else "line work that enhances the subject"}
• Dynamic elements: {abstract_composition if abstract_composition else "Consider compositional energy"} with {movement_type if movement_type else "movement qualities that bring life"}
• Material presence: {material_type if material_type else "What physical qualities should be emphasized?"} with {material_finish if material_finish else "surface finish that creates the right impression"}

TECHNICAL EXCELLENCE REQUIREMENTS:
• Digital realization: {digital_software if digital_software else "Consider digital execution"} with {", ".join(digital_effects) if digital_effects else "effects that elevate the scene"}
• Gaming aesthetic: {game_engine if game_engine else "Consider game-inspired visual language"} in {game_genre if game_genre else "a genre that fits"} using {game_shader if game_shader else "appropriate shader techniques"}
• Professional tooling: {suite if suite else "Consider industry-standard approaches"} with {renderer if renderer else "rendering techniques that excel"}

OPTICAL CHARACTERISTICS:
• Camera perspective: {camera_model if camera_model else "Imagine the perfect camera"} with {lens_type if lens_type else "optimal lens choice"}
• Optical settings: {aperture if aperture else "Consider aperture impact"} at {focal_length if focal_length else "focal length for ideal perspective"} with {shutter_speed if shutter_speed else "exposure timing that captures motion perfectly"} at {iso if iso else "sensitivity setting for ideal grain/noise"}
• Photographic enhancements: {filter_type if filter_type else "Consider filter effects"} and {special_lens if special_lens else "special lens characteristics"}

THE CREATIVE ALCHEMY PROCESS:
1. Begin with the essence of "{custom_prompt}" - its subject, mood, and intent are inviolable
2. Synthesize a heightened reality where technical elements become poetic qualities
3. Craft ONE flowing paragraph where every word serves the vision
4. Transform technical specifications into natural characteristics of the scene
5. End exactly with "{resolution} resolution, {aspect_ratio} aspect ratio"
6. Follow with "Avoid: [negative elements]"

CRITICAL REMINDER:
You are creating visual poetry, not a technical document. The technical elements should dissolve into the narrative flow, becoming qualities of light, space, and emotion rather than specifications. Be bold, be evocative, and let your creativity soar while honoring the original prompt's soul.

OUTPUT FORMAT:
[A single, flowing paragraph that transforms "{custom_prompt}" into a breathtaking scene, weaving in all relevant technical elements as natural qualities, ending precisely with "{resolution} resolution, {aspect_ratio} aspect ratio"]
Avoid: [negative elements]
"""

        # Add negative prompt if available
        if negative_prompt: # This negative_prompt is derived from user_prefs or default
            enhancement_instructions += f"\n\nNEGATIVE PROMPT - ALWAYS INCLUDE:\nThe following elements must be avoided in the image: {negative_prompt}"
        
        # Ensure Gemini is initialized
        if not gemini_config.is_initialized():
            if not gemini_config.initialize_gemini_globally():
                logging.error(f"Gemini not initialized for enhance_custom_prompt: {gemini_config.get_last_error()}")
                return enforce_prompt_format(custom_prompt, resolution, aspect_ratio, negative_prompt)

        # Determine effective_user_prefs for model selection
        effective_user_prefs = user_prefs
        if not use_user_preferences and user_prefs is None:
            effective_user_prefs = user_prefs # which is SimplePrefs instance here
        elif user_prefs is None and use_user_preferences:
             effective_user_prefs = SimplePrefs()
        elif user_prefs is None:
            effective_user_prefs = SimplePrefs()

        selected_model_name = gemini_config.get_selected_gemini_model(effective_user_prefs)
        logging.info(f"Using Gemini model for custom prompt enhancement: {selected_model_name}")

        # Generate enhanced prompt using Gemini
        try:
            # API key and configuration are handled by gemini_config.initialize_gemini_globally()
            model = genai.GenerativeModel(selected_model_name)
            response = model.generate_content(enhancement_instructions)

            if response.parts and len(response.parts) > 0 and hasattr(response.parts[0], 'text'):
                full_response = response.parts[0].text.strip()
                
                # If we're not using user preferences, apply the art medium enforcement
                if not use_user_preferences and enforce_medium:
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
                    # If not parsed properly and enforce_art_medium exists, use it
                    enhanced_prompt = full_response
                    if enforce_medium:
                        enhanced_prompt = enforce_art_medium(enhanced_prompt, custom_prompt)
                    
                    # Verify that the enhanced prompt still contains the core subject
                    if custom_prompt.lower() not in enhanced_prompt.lower():
                        logging.warning("Enhanced prompt doesn't contain original subject, prepending it")
                        enhanced_prompt = f"{custom_prompt}, {enhanced_prompt}"
                        
                    # Add negative prompt if it's not already included
                    if negative_prompt and "avoid:" not in enhanced_prompt.lower():
                        enhanced_prompt += f" Avoid: {negative_prompt}"
                        
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
