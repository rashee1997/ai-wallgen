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
    from google import genai # Use the new SDK import
    from google.genai import types # Import types for consistency
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
    # Initialize variables used in f-strings to avoid Pylance warnings
    style = None
    mood = None
    camera_model = None
    lens_type = None
    aperture = None
    special_lens = None
    depth_of_field = None
    focal_length = None
    shutter_speed = None
    iso = None
    filter_type = None
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
    resolution = "3840x2160" # Default value
    rendering_quality = None
    aspect_ratio = "16:9" # Default value
    digital_software = ""
    digital_effects = []
    game_engine = ""
    game_genre = ""
    game_shader = ""
    suite = None
    renderer = None
    version = None
    painting_medium = ""
    brushwork = ""
    texture = ""
    illustration_style = ""
    line_quality = ""
    abstract_composition = ""
    movement_type = ""
    material_type = ""
    material_finish = ""
    negative_prompt = "ugly, disfigured, low quality, blurry, nsfw, watermark, signature, out of frame, extra limbs, poorly drawn face, twisted limbs, distorted face, bad proportions, bad anatomy" # Default value

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

        # Check if user_prefs contains logo template data
        logo_template = getattr(user_prefs, 'logo_template_data', None)
        if logo_template and isinstance(logo_template, dict):
            logging.info("Logo preset detected. Using logo template for prompt generation.")

            # Extract necessary data from the logo template
            prompt_structure = logo_template.get("imagen3_prompt_structure", "")
            logo_negative_prompt = logo_template.get("negative_prompt_suggestions", "")
            logo_style_description = logo_template.get("logo_style_description", "")
            key_elements_guidance = logo_template.get("key_elements_guidance", "")
            color_palette_guidance = logo_template.get("color_palette_guidance", "")
            typography_guidance = logo_template.get("typography_guidance", "")

            # Get general negative prompt from user_prefs or default
            general_negative_prompt = getattr(user_prefs, 'imagen_settings', {}).get("negative_prompt", "ugly, disfigured, low quality, blurry, nsfw, watermark, signature, out of frame, extra limbs, poorly drawn face, twisted limbs, distorted face, bad proportions, bad anatomy")

            # Combine negative prompts, removing duplicates and empty strings
            combined_negative_prompt_list = [p.strip() for p in logo_negative_prompt.split(',') + general_negative_prompt.split(',') if p.strip()]
            combined_negative_prompt = ", ".join(sorted(list(set(combined_negative_prompt_list))))

            # Ensure Gemini is initialized
            if not gemini_config.is_initialized():
                if not gemini_config.initialize_gemini_globally():
                    logging.error(f"Gemini not initialized for enhance_custom_prompt (logo): {gemini_config.get_last_error()}")
                    # Fallback to basic formatting if Gemini fails
                    return enforce_prompt_format(custom_prompt, "3840x2160", "16:9", combined_negative_prompt)

            # Determine effective_user_prefs for model selection (using logo template data if available)
            effective_user_prefs = user_prefs
            selected_model_name = gemini_config.get_selected_gemini_model(effective_user_prefs)
            logging.info(f"Using Gemini model for logo prompt generation: {selected_model_name}")

            # Construct the Gemini instruction for logo generation
            # Corrected instruction to guide Gemini on filling placeholders
            logo_enhancement_instruction = f"""
You are a creative logo designer specializing in crafting unique, artistic prompt descriptions for Imagen 3 AI logo generation.

Given the user's custom prompt: "{custom_prompt}"
And the following creative guidelines:
Logo Style Description: {logo_style_description}
Key Elements Guidance: {key_elements_guidance}
Color Palette Guidance: {color_palette_guidance}
Typography Guidance: {typography_guidance}

🎨 CREATIVE LOGO DESIGN MISSION 🎨

Your task is to craft a rich, inspiring prompt for a logo design that captures the essence of "{custom_prompt}" while drawing inspiration from the creative guidelines. Unlike a rigid template-filling exercise, this is an opportunity to blend art and strategy to create a truly remarkable logo concept.

1. Deeply analyze the user's prompt "{custom_prompt}" to extract:
   - Brand name or key text elements that should appear in the logo
   - The industry, values, or core concepts the brand represents
   - Any implicit tone, personality, or stylistic preferences

2. Draw inspiration from (but don't be limited by) the style guidelines:
   - The minimalist aesthetic that emphasizes clean lines and negative space
   - Suggestions for visual elements that could subtly represent the industry
   - Color palette recommendations that would create the right mood and association
   - Typography approaches that would complement the overall design

3. Craft a detailed, evocative prompt that:
   - Creates a clear vision of the logo design
   - Focuses on the visual impact and storytelling power of the design
   - Balances simplicity with meaningful symbolism
   - Incorporates the technical specifications needed for Imagen 3 to generate effectively

4. Include these technical elements:
   - Specific colors with hex codes where appropriate
   - Clear typography recommendations
   - Resolution and format specifications
   - Negative elements to avoid: {combined_negative_prompt}

Rather than mechanically filling in a template, unleash your creativity to craft a prompt that will inspire Imagen 3 to generate a truly distinctive logo. The final output should be cohesive, compelling, and tailored to the essence of "{custom_prompt}".

Reference structure (inspire but don't constrain your creativity):
{prompt_structure}

IMPORTANT: Your response should be just the creative prompt text itself, without any explanations or meta-commentary. Make it flow naturally like an artistic description rather than a form filled with placeholders.
"""
            try:
                client = gemini_config.get_gemini_client()
                if client is None:
                    logging.error("Gemini client is not initialized, cannot generate logo prompt.")
                    return enforce_prompt_format(custom_prompt, "3840x2160", "16:9", combined_negative_prompt)

                response = client.generate_content(
                    model=selected_model_name,
                    contents=logo_enhancement_instruction
                )

                enhanced_prompt_text = None
                if hasattr(response, 'text') and response.text is not None:
                    enhanced_prompt_text = response.text.strip()
                
                if enhanced_prompt_text: # Checks if not None and not empty string
                    enhanced_prompt = enhanced_prompt_text
                    # Ensure the combined negative prompt is included (existing logic)
                    if "Avoid:" not in enhanced_prompt:
                         enhanced_prompt += f" Avoid: {combined_negative_prompt}"
                    elif combined_negative_prompt not in enhanced_prompt:
                         # If Avoid is present but doesn't contain the combined prompt, append it
                         enhanced_prompt = enhanced_prompt.replace("Avoid:", f"Avoid: {combined_negative_prompt}, ")
                    return enhanced_prompt
                else:
                    logging.warning("Gemini response for logo prompt was empty or text could not be retrieved.")
                    # Fallback to basic formatting if Gemini fails
                    return enforce_prompt_format(custom_prompt, "3840x2160", "16:9", combined_negative_prompt)

            except Exception as e:
                logging.error(f"Error generating logo prompt with Gemini: {str(e)}")
                # Fallback to basic formatting if Gemini fails
                return enforce_prompt_format(custom_prompt, "3840x2160", "16:9", combined_negative_prompt)



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

        # Basic artwork style for no preferences or general preferences
        style = getattr(user_prefs, 'preferred_styles', [None])[0]
        mood = getattr(user_prefs, 'preferred_moods', [None])[0]

        # Get all settings from imagen_settings
        settings = getattr(user_prefs, 'imagen_settings', {})

        # Camera Settings
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
        focal_point = composition_settings.get("focal_point")
        perspective = composition_settings.get("perspective")

        # Environment Settings
        environment_settings = settings.get("environment_settings", {})
        weather = environment_settings.get("weather")
        season = environment_settings.get("season")
        atmospheric_effects = environment_settings.get("atmospheric_effects", [])

        # Style Settings
        style_settings = settings.get("style_settings", {})
        art_movement = style_settings.get("art_movement")
        post_processing = style_settings.get("post_processing", [])
        style_era = style_settings.get("style_era")

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
        resolution = quality_settings.get("resolution", "3840x2160")
        rendering_quality = quality_settings.get("rendering_quality")
        aspect_ratio = getattr(user_prefs, 'aspect_ratio', "16:9")

        # Art style variables for f-string use (guaranteed assigned)
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

        # Get negative prompt if available
        negative_prompt = settings.get("negative_prompt", "")

        # Try to use enforce_art_medium if it was imported
        enforce_medium = "enforce_art_medium" in locals() and callable(locals()["enforce_art_medium"])

        # Detect specific art mediums in the prompt and preserve them (only for non-logo presets)
        art_mediums = {
            "watercolor": ["3d", "3d render", "3d art", "digital art", "oil painting", "acrylic", "photograph"],
            "oil painting": ["3d", "3d render", "3d art", "digital art", "watercolor", "acrylic", "photograph"],
            "sketch": ["3d", "3d render", "3d art", "digital art", "oil painting", "acrylic", "photograph"],
            "pencil": ["3d", "3d render", "3d art", "digital art", "oil painting", "acrylic", "photograph"],
            "acrylic": ["3d", "3d render", "3d art", "oil painting", "watercolor", "photograph"],
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
- For natural subjects: emphasize organic elements, textures, and environmental context
- For urban subjects: focus on architectural details, perspective, and urban atmosphere
- For abstract subjects: highlight patterns, shapes, and conceptual elements
- For space/cosmic subjects: emphasize scale, wonder, and celestial phenomena
- For fantasy subjects: create a cohesive magical or surreal atmosphere

MANDATORY TECHNICAL PARAMETERS:
Resolution: {resolution} - YOU MUST INCLUDE THIS IN YOUR FINAL PROMPT
Aspect Ratio: {aspect_ratio} - YOU MUST INCLUDE THIS IN YOUR FINAL PROMPT

"""
        # Use the no preferences instruction template, but make it richer
        enhancement_instructions = original_prompt_prefix + f"""

🔮 CREATIVE ENHANCEMENT MISSION 🔮

Your task is to breathe life into this prompt while honoring its soul. Take the essence of "{custom_prompt}" and craft a vivid, immersive scene that elevates it to new heights without changing its fundamental spirit, guided by the user's preferences and advanced prompt engineering techniques.

ARTISTIC VISION:
• Style: {style if style else "Be guided by what best serves the subject (e.g., photograph, painting, sketch, digital art, 3D render)"}. Consider specific art styles like {illustration_style if illustration_style else "e.g., anime, comic book, concept art"} or traditional styles like {painting_medium if painting_medium else "e.g., oil painting, watercolor"} with {brushwork if brushwork else "appropriate brushwork"}.
• Mood: {mood if mood else "What emotions does this scene naturally evoke? (e.g., epic, serene, mysterious, joyful)"}
• Art Movement: {art_movement if art_movement else "Consider what artistic tradition would best frame this imagery (e.g., Impressionism, Pop Art, Surrealism, Art Deco, Renaissance, Baroque)"}
• Historical Context: {style_era if style_era else "What time period resonates with this scene?"}
• Subject Focus: If depicting people, especially in portraits, ensure clear and well-rendered facial details. Use terms like "portrait" or "close-up on face" if appropriate.

CREATIVE METAMORPHOSIS GUIDANCE:
The original prompt seed "{custom_prompt}" is sacred—its core essence must remain intact and recognizable. Your challenge is to amplify its power through artistic interpretation, weaving in technical elements (derived from user preferences) as natural characteristics of the scene, never as mechanical afterthoughts.

Imagine you're a master painter, cinematographer, and poet combined. Your canvas awaits the transformation of "{custom_prompt}" into something that retains its soul while gaining depth, atmosphere, and technical excellence.

ATMOSPHERE & ENVIRONMENT INSPIRATIONS:
• Weather conditions: {weather if weather else "What atmospheric conditions would heighten the scene's impact? (e.g., sunny, overcast, rainy, snowy, foggy)"}
• Season: {season if season else "What time of year would create the perfect backdrop? (e.g., spring, summer, autumn, winter)"}
• Location essence: {location_type if location_type else "What setting would provide the ideal stage? (e.g., bustling city, tranquil forest, futuristic interior, alien planet)"}
• Atmospheric qualities: {", ".join(atmospheric_effects) if atmospheric_effects else "Consider fog, mist, clear air, haze, dust particles, or other atmospheric elements"}

VISUAL LANGUAGE ELEMENTS:
• Light character: {lighting_type if lighting_type else "How does light interact with this scene? (e.g., natural light, studio lighting, dramatic lighting, soft lighting, volumetric, rim lighting)"} with {light_quality if light_quality else "quality that enhances the subject (e.g., warm, cool, harsh, diffused)"}
• Time of day: {time_of_day if time_of_day else "When would this scene be most striking? (e.g., sunrise, golden hour, midday, twilight, night)"}
• Color harmony: {color_scheme if color_scheme else "What color relationships would strengthen the scene? (e.g., monochromatic, analogous, complementary, triadic)"} with {palette_type if palette_type else "palette reflecting the mood (e.g., vibrant, muted, pastel, neon)"} and {color_temperature if color_temperature else "temperature creating the right feeling (e.g., warm, cool, neutral)"}
• Depth perception: {depth_of_field if depth_of_field else "How should focus be distributed across the scene? (e.g., shallow depth of field, deep focus, bokeh)"}
• Spatial arrangement & Composition: {technique if technique else "What compositional technique would frame this best? (e.g., rule of thirds, leading lines, symmetry, golden ratio)"} with focus on {focal_point if focal_point else "the most important element"}. Consider {camera_angle if camera_angle else "camera angles like eye-level, low angle, high angle, bird's-eye view, worm's-eye view, Dutch angle"}.

ARTISTIC EXECUTION SUGGESTIONS:
• Medium expression: {painting_medium if painting_medium else "Consider the perfect medium (e.g., oil, watercolor, acrylic, pastel, charcoal, pencil sketch)"} with {brushwork if brushwork else "technique that captures the right feeling (e.g., impasto, scumbling, smooth blending)"}
• Textural quality: {texture_quality if texture_quality else "What tactile qualities should be visible? (e.g., high detail, smooth, rough, metallic, fabric)"} with {texture if texture else "surface characteristics that enhance the scene (e.g., wood grain, stone texture, brushed metal)"}
• Detail richness: {detail_level if detail_level else "How intricate should the scene be? (e.g., highly detailed, minimalist, intricate patterns)"}
• Stylistic approach: {illustration_style if illustration_style else "What illustrative style would resonate? (e.g., comic book art, anime, flat illustration, isometric)"} with {line_quality if line_quality else "line work that enhances the subject (e.g., clean lines, sketchy lines, bold outlines)"}
• Dynamic elements: {abstract_composition if abstract_composition else "Consider compositional energy (e.g., geometric, organic, flowing)"} with {movement_type if movement_type else "movement qualities that bring life (e.g., dynamic action, serene stillness)"}
• Material presence: {material_type if material_type else "What physical qualities should be emphasized? (e.g., glass, wood, metal, stone, fabric)"} with {material_finish if material_finish else "surface finish that creates the right impression (e.g., matte, glossy, polished, weathered)"}

TECHNICAL EXCELLENCE REQUIREMENTS:
• Digital realization: {digital_software if digital_software else "Consider digital execution (e.g., digital painting, 3D render)"} with {", ".join(digital_effects) if digital_effects else "effects that elevate the scene (e.g., bloom, motion blur, lens flare)"}
• Gaming aesthetic: {game_engine if game_engine else "Consider game-inspired visual language (e.g., Unreal Engine, Unity)"} in {game_genre if game_genre else "a genre that fits (e.g., RPG, sci-fi, fantasy)"} using {game_shader if game_shader else "appropriate shader techniques (e.g., cel shading, PBR)"}
• Professional tooling: {suite if suite else "Consider industry-standard approaches (e.g., Adobe Photoshop, Blender, Maya)"} with {renderer if renderer else "rendering techniques that excel (e.g., ray tracing, path tracing)"}
• Overall Quality Impression: Aim for terms like "{rendering_quality if rendering_quality else "high-quality"}", "photorealistic" (if style is photographic), "4K", "HDR", "Studio Photo", "professionally captured/rendered", "detailed masterpiece" where appropriate to the style and subject.

OPTICAL CHARACTERISTICS (Primarily for Photographic/Rendered Styles):
• Camera perspective: {camera_model if camera_model else "Imagine the perfect camera"} with {lens_type if lens_type else "optimal lens choice (e.g., 35mm, 50mm, 85mm for portraits; 16-35mm for wide-angle landscapes; 100mm macro for close-ups; fisheye for unique perspectives)"}.
• Optical settings: {aperture if aperture else "Consider aperture impact (e.g., f/1.8 for shallow depth of field, f/16 for deep focus)"} at {focal_length if focal_length else "focal length for ideal perspective"} with {shutter_speed if shutter_speed else "exposure timing that captures motion perfectly (e.g., fast shutter for freezing action, slow shutter for motion blur)"} at {iso if iso else "sensitivity setting for ideal grain/noise (e.g., ISO 100 for clean, ISO 3200 for low light)"}.
• Photographic enhancements: {filter_type if filter_type else "Consider filter effects (e.g., polarizing filter, ND filter)"} and {special_lens if special_lens else "special lens characteristics (e.g., anamorphic lens flare, tilt-shift)"}. Consider film types like "{'black and white film' if 'black and white' in style.lower() else 'color film'}", "polaroid".

TEXT IN IMAGE GENERATION (IF APPLICABLE):
If the prompt "{custom_prompt}" or user preferences imply or could benefit from text within the image:
- Keep text concise (ideally 1-3 words, maximum around 25 characters for clarity).
- If multiple phrases are needed, limit to 2-3 distinct short phrases.
- You can suggest general placement (e.g., "text 'Adventure Awaits' across the top," "a street sign reading 'Elm St'") but acknowledge that precise placement can vary.
- You can suggest a general font style (e.g., "bold sans-serif font," "elegant script font," "vintage lettering," "futuristic digital font") to influence the outcome.
- You can suggest general font size (e.g., "large prominent title text," "small subtle caption text").

THE CREATIVE ALCHEMY PROCESS:
1. Begin with the essence of "{custom_prompt}" - its subject, mood, and intent are inviolable.
2. Synthesize a heightened reality where technical elements (from user preferences) become poetic qualities of the scene.
3. Craft ONE flowing paragraph where every word serves the vision.
4. Transform technical specifications into natural characteristics of the scene (light, color, perspective, texture, etc.).
5. End exactly with "{resolution} resolution, {aspect_ratio} aspect ratio".
6. Follow with "Avoid: [negative elements]".

CRITICAL REMINDER:
You are creating visual poetry, not a technical document. The technical elements should dissolve into the narrative flow, becoming qualities of light, space, and emotion rather than specifications. Be bold, be evocative, and let your creativity soar while honoring the original prompt's soul and the user's preferences.

OUTPUT FORMAT:
[A single, flowing paragraph that transforms "{custom_prompt}" into a breathtaking scene, weaving in all relevant technical elements (guided by user_prefs) as natural qualities, ending precisely with "{resolution} resolution, {aspect_ratio} aspect ratio"]
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
            client = gemini_config.get_gemini_client()
            if client is None:
                logging.error("Gemini client is not initialized, cannot enhance custom prompt.")
                return enforce_prompt_format(custom_prompt, resolution, aspect_ratio, negative_prompt)
            
            response = client.generate_content(
                model=selected_model_name,
                contents=enhancement_instructions
            )

            full_response_text = None
            if hasattr(response, 'text') and response.text is not None:
                full_response_text = response.text.strip()

            if full_response_text:
                full_response = full_response_text

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
                logging.warning("Gemini response for custom prompt enhancement was empty or text could not be retrieved.")
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
