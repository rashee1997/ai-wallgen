#!/usr/bin/env python3
"""Custom Prompt Generator Module - Functions for enhancing custom AI wallpaper prompts

This module contains functions for enhancing custom user-provided prompts with
additional details, style parameters, and technical specifications. It integrates
user preferences into the custom prompts to generate more detailed and consistent results,
utilizing the latest Google Generative AI SDK.
"""
import logging
import os
import re # Retained from original structure, though not explicitly used in visible logic
from typing import Dict, List, Optional, Any, Union # Retained from original

# Third-party imports for the new Google Generative AI SDK
try:
    from google import genai  # New SDK import style
    from google.genai import types # Import types for consistency with original usage
except ImportError:
    logging.warning(
        "The 'google-genai' SDK (specifically 'from google import genai') could not be imported. "
        "AI-powered prompt enhancement features will be disabled or may not function correctly."
    )
    # Define placeholders if the import fails, so later checks don't raise NameError
    genai = None
    types = None # Placeholder for google.genai.types

# Import types from the current package
from .types import SimplePrefs # Assuming this exists in your project structure
# Import centralized Gemini configuration
# This module is assumed to handle initialization and client provision for the new SDK.
from .. import gemini_config # Assuming this exists in your project structure

# Import utilities
from .formatters import enforce_prompt_format # Assuming this exists

def generate_logo(
    logo_text: str,
    tag_lines: str = None,
    logo_style: str = "minimalist",
    logo_color: str = None,
    logo_industry: str = None,
    save_template: bool = False,
    user_prefs: object = None,
    generate_only: bool = False,
) -> str:
    """
    Generate a logo prompt string based on inputs and user preferences.

    Args:
        logo_text: The main text/brand name for the logo.
        tag_lines: Optional taglines or secondary text.
        logo_style: Style template to use.
        logo_color: Primary color for the logo.
        logo_industry: Industry context for design influence.
        save_template: Whether to save the generated prompt as a template.
        user_prefs: User preferences object.
        generate_only: If True, only generate the prompt string without image generation.

    Returns:
        str: The generated logo prompt string.
    """
    # Basic prompt construction
    prompt_parts = [f"Logo design for '{logo_text}'"]

    if tag_lines:
        prompt_parts.append(f"with taglines: {tag_lines}")

    if logo_style:
        prompt_parts.append(f"in {logo_style} style")

    if logo_color:
        prompt_parts.append(f"using primary color {logo_color}")

    if logo_industry:
        prompt_parts.append(f"for the {logo_industry} industry")

    prompt = ", ".join(prompt_parts) + "."

    # Optionally, enhance the prompt using enhance_custom_prompt
    # This function is responsible for the Gemini API interaction.
    try:
        # The original code had `from .custom_generator import enhance_custom_prompt`.
        # If enhance_custom_prompt is this very function, this might be a recursive design
        # or a call to a different module. For this modification, we assume
        # enhance_custom_prompt is the function defined below in this file.
        # If it's meant to be from another module, the import path should be correct.
        prompt = enhance_custom_prompt(prompt, user_prefs=user_prefs, tag_lines=tag_lines, logo_industry_for_template=logo_industry)
    except ImportError: # This would be if enhance_custom_prompt was in another module and failed to import
        logging.warning("enhance_custom_prompt (or its dependencies) not found. Using basic logo prompt.")
    except Exception as e:
        logging.error(f"Error during logo prompt enhancement: {e}. Using basic logo prompt.")


    if save_template:
        # Placeholder for saving logic
        logging.info(f"Placeholder: Save template requested for prompt: {prompt}")
        pass

    if generate_only:
        return prompt

    # If generate_only is False, image generation is handled elsewhere.
    # This function returns the (potentially enhanced) prompt string.
    return prompt


def enhance_custom_prompt(custom_prompt: str, user_prefs: Optional[Any] = None, description: Optional[str] = None, tag_lines: Optional[str] = None, logo_industry_for_template: Optional[str] = None) -> str:
    """Enhance the custom prompt using the Gemini model based on user preferences.
    
    Args:
        custom_prompt: The original prompt to enhance.
        user_prefs: Optional user preferences object.
        description: Optional description string from preset to include in prompt generation.
        tag_lines: Optional taglines to include in the prompt generation.
        logo_industry_for_template: Optional industry context, specifically for logo template generation.
    
    Returns:
        str: An enhanced version of the custom prompt.
    """
    # Initialize variables (as in original code)
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
    # Default negative prompt, can be overridden by user_prefs or logo_template
    negative_prompt_default = "ugly, disfigured, low quality, blurry, nsfw, watermark, signature, out of frame, extra limbs, poorly drawn face, twisted limbs, distorted face, bad proportions, bad anatomy"
    current_negative_prompt = negative_prompt_default # Initialize with default
    style_era = None

    try:
        # Import from core to avoid circular imports
        from .core import use_user_preferences # Assuming .core exists in your project

        # If user_prefs is not provided and we should use preferences, get them from global
        if user_prefs is None and use_user_preferences:
            try:
                # Import here to avoid circular imports
                from ..settings_modules import get_preferences # Assuming this exists
                user_prefs = get_preferences()
            except ImportError:
                logging.warning("Unable to import get_preferences from ..settings_modules. User preferences will not be loaded automatically.")
                user_prefs = None # Proceed without global preferences

        # Check if user_prefs contains logo template data
        logo_template = getattr(user_prefs, 'logo_template_data', None)
        
        # TODO: Add 'use_structured_logo_prompt_format' to UserPreferences class and relevant UI/menu options.
        use_structured_format = getattr(user_prefs, 'use_structured_logo_prompt_format', False)

        # --- LOGO PROMPT ENHANCEMENT ---
        if logo_template and isinstance(logo_template, dict):
            logging.info(f"Logo preset detected. Using logo template for prompt generation. Structured format: {use_structured_format}")

            # Extract necessary data from the logo template
            prompt_structure = logo_template.get("imagen3_prompt_structure", "")
            logo_negative_prompt_str = logo_template.get("negative_prompt_suggestions", "")
            logo_style_description = logo_template.get("logo_style_description", "")
            key_elements_guidance = logo_template.get("key_elements_guidance", "")
            color_palette_guidance = logo_template.get("color_palette_guidance", "")
            typography_guidance = logo_template.get("typography_guidance", "")
            composition_guidance = logo_template.get("composition_guidance", "")

            preset_description = logo_template.get("description", "")
            preset_moods = logo_template.get("moods", [])
            preset_aspect_ratio = logo_template.get("aspect_ratio", "1:1") # Default for logos
            
            preset_imagen_settings = logo_template.get("imagen_settings", {})
            quality_settings = preset_imagen_settings.get("quality_settings", {})
            preset_resolution = quality_settings.get("resolution", "1024x1024") # Default for logos
            style_settings = preset_imagen_settings.get("style_settings", {})
            lighting_settings = preset_imagen_settings.get("lighting_settings", {})
            composition_settings_general = preset_imagen_settings.get("composition_settings", {})
            color_settings_general = preset_imagen_settings.get("color_settings", {})
            detail_settings = preset_imagen_settings.get("detail_settings", {})
            environment_settings = preset_imagen_settings.get("environment_settings", {})
            style_negative_prompt_from_settings = preset_imagen_settings.get("style_negative_prompt", "")

            # Get general negative prompt from preset_imagen_settings or fallback to class default
            general_negative_prompt_from_preset = preset_imagen_settings.get("negative_prompt", negative_prompt_default)

            # Combine negative prompts, removing duplicates and empty strings
            combined_negative_prompt_list = [
                p.strip() for p in (
                    str(logo_negative_prompt_str).split(',') + 
                    str(general_negative_prompt_from_preset).split(',') + 
                    str(style_negative_prompt_from_settings).split(',')
                ) if p.strip()
            ]
            current_negative_prompt = ", ".join(sorted(list(set(combined_negative_prompt_list))))
            if not current_negative_prompt: # Ensure it's not empty if all sources were empty
                 current_negative_prompt = negative_prompt_default


            # Ensure resolution and aspect_ratio for this block are from the logo preset
            resolution = preset_resolution
            aspect_ratio = preset_aspect_ratio
            
            if not gemini_config.is_initialized():
                if not gemini_config.initialize_gemini_globally():
                    logging.error(f"Gemini not initialized for enhance_custom_prompt (logo): {gemini_config.get_last_error()}")
                    return enforce_prompt_format(custom_prompt, resolution, aspect_ratio, current_negative_prompt)

            effective_user_prefs = user_prefs # For model selection
            selected_model_name = gemini_config.get_selected_gemini_model(effective_user_prefs)
            logging.info(f"Using Gemini model for logo prompt generation: {selected_model_name}")

            # CLASSIC (single paragraph) logo enhancement instruction template
            logo_enhancement_instruction_classic_template_str = f"""
Given the user's core logo subject/text: "{custom_prompt}"
{f'Associated Taglines: "{tag_lines}"' if tag_lines else ""} 
Preset Description: {preset_description if preset_description else 'Not specified.'}
Overall Moods: {', '.join(preset_moods) if preset_moods else 'Not specified.'}

🎨 PRIMARY LOGO DESIGN DIRECTIVES (from Logo Template) 🎨
These are the core creative guidelines for this specific type of logo:
- Logo Style Concept: {logo_style_description if logo_style_description else 'Focus on a unique and memorable design.'}
- Key Visual Elements: {key_elements_guidance if key_elements_guidance else 'Suggest 1-2 core visual elements representing the core concept.'}
- Color Palette Concept: {color_palette_guidance if color_palette_guidance else 'Suggest a suitable color palette.'}
- Typography Concept: {typography_guidance if typography_guidance else 'Suggest a clean, modern font style for the main text.'}
{f'- Tagline Typography & Integration: If taglines ("{tag_lines}") are provided, suggest how they should be integrated (e.g., below main text, curved around an element) and what complementary font style they should use (e.g., lighter weight, different case).' if tag_lines else ""}
- Composition Concept for this Logo Type: {composition_guidance if composition_guidance else 'Emphasize balance and proportion.'}

⚙️ GENERAL USER PREFERENCES & REFINEMENTS (from Preset Settings) ⚙️
Refine the primary directives using these general preferences. If any general preference seems to conflict with a primary directive, prioritize the primary directive or find a creative synthesis.

- General Style Settings:
    - Overall Style: {style_settings.get('style', 'Not specified.')}
    - Art Movement: {style_settings.get('art_movement', 'Not specified.')}
    - Style Era: {style_settings.get('style_era', 'Not specified.')}

- General Lighting Settings:
    - Lighting Type: {lighting_settings.get('lighting_type', 'Not specified.')}
    - Light Quality: {lighting_settings.get('light_quality', 'Not specified.')}
    - Light Source: {lighting_settings.get('light_source', 'Not specified.')}

- General Composition Settings (to complement the logo-type specific composition concept):
    - Technique: {composition_settings_general.get('technique', 'Not specified.')}
    - Visual Flow: {composition_settings_general.get('visual_flow', 'Not specified.')}
    - Focal Point: {composition_settings_general.get('focal_point', 'Not specified.')}

- General Color Settings (to complement the logo-type specific color concept):
    - Color Scheme: {color_settings_general.get('color_scheme', 'Not specified.')}
    - Palette Type: {color_settings_general.get('palette_type', 'Not specified.')}
    - Color Temperature: {color_settings_general.get('color_temperature', 'Not specified.')}

- Desired Detail Level:
    - Detail Level: {detail_settings.get('detail_level', 'Not specified.')}
    - Texture Quality: {detail_settings.get('texture_quality', 'Not specified.')}

- Background & Environment:
    - Environment: {environment_settings.get('environment', 'Isolated on a white background.')}

✨ CREATIVE LOGO DESIGN MISSION ✨
Your task is to craft a rich, inspiring prompt for a logo design. This prompt will be used by Google's Imagen 3 model.
1. Deeply analyze the user's core logo subject/text ("{custom_prompt}") {f'and associated taglines ("{tag_lines}")' if tag_lines else ""}. Extract:
   - The primary brand name from "{custom_prompt}".
   {f'- Taglines: "{tag_lines}".' if tag_lines else ""}
   - The industry, values, or core concepts the brand represents (from "{custom_prompt}", taglines if any, and preset context).
   - Any implicit tone, personality, or stylistic preferences.
2. Synthesize the PRIMARY LOGO DESIGN DIRECTIVES with the GENERAL USER PREFERENCES & REFINEMENTS to create a cohesive and detailed vision.
3. The final output should be a single, coherent, and detailed text prompt for Imagen 3, emphasizing how the logo should achieve a balance of distinctiveness, versatility, and timeless design, suitable for the brand identified.

📐 TECHNICAL SPECIFICATIONS FOR IMAGEN 3 OUTPUT 📐
- Desired Output Format: Flat vector illustration, isolated on a white background (unless environment settings suggest otherwise). Ensure clean edges and precise forms suitable for a scalable logo.
- Resolution: {resolution}
- Aspect Ratio: {aspect_ratio}

REFERENCE PROMPT STRUCTURE (Use as a guide for detail level and tone, but adapt creatively based on all inputs above):
{prompt_structure}

🚫 NEGATIVE ELEMENTS TO AVOID (Strictly Adhere):
{current_negative_prompt}

IMPORTANT: Your response should be just the creative prompt text itself, without any explanations, meta-commentary, or repeating these instructions. Make it flow naturally like an artistic description for Imagen 3. Do not use markdown in your response.
"""

            # STRUCTURED logo enhancement instruction template
            logo_enhancement_instruction_structured_template_str = f"""
You are an AI assistant generating a detailed, structured prompt for Google's Imagen 3 model to create a logo.
The user's core logo subject/text is: "{custom_prompt}"
{f'Associated Taglines: "{tag_lines}"' if tag_lines else ""}
Preset Description for context: {preset_description if preset_description else 'Not specified.'}
Overall Moods for context: {', '.join(preset_moods) if preset_moods else 'Not specified.'}
Specific Logo Style Concept: {logo_style_description if logo_style_description else 'Not specified, focus on a unique and memorable design.'}
Key Visual Elements Guidance: {key_elements_guidance if key_elements_guidance else 'Not specified, suggest 1-2 core visual elements representing the core concept.'}
Color Palette Guidance: {color_palette_guidance if color_palette_guidance else 'Not specified, suggest a suitable professional color palette with example Hex codes.'}
Typography Guidance: {typography_guidance if typography_guidance else 'Not specified, suggest a clean, modern font style for the main text and any taglines.'}
Composition Guidance for this Logo Type: {composition_guidance if composition_guidance else 'Not specified, emphasize balance and proportion.'}
General Style Setting (Overall): {style_settings.get('style', 'Not specified.')}
General Style Setting (Art Movement): {style_settings.get('art_movement', 'Not specified.')}
General Style Setting (Style Era): {style_settings.get('style_era', 'Not specified.')}
Industry specified (if any, for context): {logo_industry_for_template if logo_industry_for_template else "Not specified."}


Based on ALL the information provided above (core subject, taglines, preset description, moods, specific logo template directives, general style settings, industry), generate a prompt for an Imagen 3 logo by filling in the following structured format.
Do NOT add any extra conversation, preamble, or explanation. Only output the structured prompt.

**Logo Text/Initials:** {custom_prompt}{f', {tag_lines}' if tag_lines else ""}
**Core Concept/Industry:** [Synthesize a concise description of the brand's essence, industry, and values based on all provided inputs. E.g., "Medical home healthcare services, emphasizing professionalism, reliability, accessibility, care, comfort, health, and wellness."]
**Style Hint (if any):** [{style_settings.get('style', 'Not specified.')}. If the logo style is more specific like 'minimalist', 'emblem', 'wordmark', etc., state it here. Otherwise, describe the general feeling, e.g., "Modern and clean" or "Playful and illustrative".]
**Style Description:** [Provide a detailed description of the desired logo style, drawing from `Logo Style Concept` and other inputs. E.g., "A versatile, professional, modern, and clean logo design suitable for a medical home healthcare company. It should be easily recognizable at various sizes and work effectively in both color and monochrome, adapting seamlessly across digital and physical applications."]
**Key Visual Elements:** [Describe the core visual components, guided by `Key Visual Elements Guidance`. E.g., "A simple, stylized icon that abstractly combines a medical symbol (like a pulse line or simplified cross) with a subtle representation of a home or roof outline. Focus on clean lines, essential forms, and balanced proportions that remain distinct and legible even at small sizes."]
**Color Palette (Hex Codes):** [Suggest a specific color palette with Hex codes, drawing from `Color Palette Guidance`. E.g., "Use a professional palette including #0056B3 (Deep Blue for trust and authority), #28A745 (Medical Green for health and vitality), and #6C757D (Medium Grey for stability and professionalism)."]
**Typography Style:** [Describe font characteristics for main text and taglines, guided by `Typography Guidance`. E.g., "Employ a clean, modern sans-serif font. Use a medium weight for the main company name '{custom_prompt}' to ensure prominence and impact, while using a lighter weight for the tagline '{tag_lines if tag_lines else "tagline"}' to maintain hierarchy and legibility. Focus on clear letterforms and balanced spacing."]
**Composition Guidance:** [Explain the arrangement of elements, guided by `Composition Guidance for this Logo Type`. E.g., "The logo should feature a balanced composition where the stylized symbol is integrated with or positioned clearly alongside the '{custom_prompt}' text. The tagline '{tag_lines if tag_lines else "tagline"}' should be placed below the main lockup in a legible and harmonious manner, ensuring the overall design feels stable and well-proportioned."]
**Desired Output Format:** Flat vector illustration, isolated on a white background. Ensure clean edges, precise forms, and scalability suitable for a professional logo design. Resolution: {resolution}, Aspect Ratio: {aspect_ratio}.
**Negative Prompt:** {current_negative_prompt}

IMPORTANT: Your response MUST strictly follow the structured format above, using markdown bold for headings (e.g., `**Field Name:**`). Do not repeat these instructions. Ensure all fields are filled appropriately and thoughtfully based on all the input details.
"""

            logo_enhancement_instruction_to_use = (
                logo_enhancement_instruction_structured_template_str
                if use_structured_format
                else logo_enhancement_instruction_classic_template_str
            )

            try:
                client = gemini_config.get_gemini_client()
                if client is None or genai is None: # Check if genai SDK itself was imported
                    logging.error("Gemini client or SDK is not initialized/imported, cannot generate logo prompt.")
                    return enforce_prompt_format(custom_prompt, resolution, aspect_ratio, current_negative_prompt)

                response = client.models.generate_content(
                    model=selected_model_name,
                    contents=logo_enhancement_instruction_to_use # Use selected instruction
                )
                
                enhanced_prompt_text = response.text.strip() if hasattr(response, 'text') and response.text else None

                if enhanced_prompt_text:
                    if use_structured_format:
                        enhanced_prompt = enhanced_prompt_text
                        # For structured format, assume Gemini placed current_negative_prompt in the correct field.
                        # We can add a check here later if needed, to ensure the **Negative Prompt:** field is not empty
                        # and contains what we expect, but for now, we'll trust the instruction.
                    else: # Classic format
                        enhanced_prompt = enhanced_prompt_text
                        # Ensure the combined negative prompt is included using "Avoid:" for classic format
                        if "Avoid:" not in enhanced_prompt and current_negative_prompt:
                            enhanced_prompt += f" Avoid: {current_negative_prompt}"
                        elif current_negative_prompt and current_negative_prompt not in enhanced_prompt:
                            # This complex merging logic is for when the model might produce its own "Avoid:"
                            # and we need to ensure our comprehensive negative prompt is also there.
                            if "Avoid:" in enhanced_prompt: 
                                base_avoid_text = enhanced_prompt.split("Avoid:", 1)[1].strip()
                                current_neg_set = set(p.strip() for p in current_negative_prompt.split(',') if p.strip())
                                base_avoid_set = set(p.strip() for p in base_avoid_text.split(',') if p.strip())
                                missing_negatives = current_neg_set - base_avoid_set
                                if missing_negatives:
                                    enhanced_prompt += ", " + ", ".join(sorted(list(missing_negatives)))
                            else: # "Avoid:" not in prompt, but current_negative_prompt exists
                                 enhanced_prompt += f" Avoid: {current_negative_prompt}"
                    return enhanced_prompt
                else:
                    logging.warning("Gemini response for logo prompt was empty or text could not be retrieved.")
                    return enforce_prompt_format(custom_prompt, resolution, aspect_ratio, current_negative_prompt)

            except Exception as e:
                logging.error(f"Error generating logo prompt with Gemini: {str(e)}", exc_info=True)
        
        # --- GENERAL PROMPT ENHANCEMENT (Non-Logo) ---
        # If not a logo template, proceed with general enhancement
        
        if not use_user_preferences and user_prefs is None:
            # Create minimal preferences if none are to be used and none were passed
            user_prefs = SimplePrefs(
                aspect_ratio="16:9", # Default aspect_ratio
                imagen_settings={
                    "camera_settings": {},
                    "lighting_settings": {},
                    "composition_settings": {},
                    "environment_settings": {},
                    "style_settings": {},
                    "detail_settings": {},
                    "color_settings": {},
                    "quality_settings": {"resolution": "3840x2160"}, # Default resolution
                    "negative_prompt": negative_prompt_default # Use the module's default
                    # Add other minimal defaults if necessary for the f-strings below
                }
            )
        
        # Populate variables from user_prefs for the general prompt
        # This part remains largely the same, as it's about preference extraction
        settings = getattr(user_prefs, 'imagen_settings', {})
        
        style = getattr(user_prefs, 'preferred_styles', [None])[0]
        mood = getattr(user_prefs, 'preferred_moods', [None])[0]

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
        light_quality = lighting_settings.get("light_quality")
        light_source = lighting_settings.get("light_source")
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
        atmospheric_effects = environment_settings.get("atmospheric_effects", [])
        location_type = environment_settings.get("location_type") # Added from original

        style_settings = settings.get("style_settings", {})
        art_movement = style_settings.get("art_movement")
        post_processing = style_settings.get("post_processing", [])
        style_era = style_settings.get("style_era")

        detail_settings = settings.get("detail_settings", {})
        detail_level = detail_settings.get("detail_level")
        texture_quality = detail_settings.get("texture_quality")
        special_effects = detail_settings.get("special_effects", [])

        color_settings = settings.get("color_settings", {})
        color_scheme = color_settings.get("color_scheme")
        palette_type = color_settings.get("palette_type")
        color_temperature = color_settings.get("color_temperature")

        quality_settings = settings.get("quality_settings", {})
        resolution = quality_settings.get("resolution", "3840x2160") # Default if not in prefs
        rendering_quality = quality_settings.get("rendering_quality")
        aspect_ratio = getattr(user_prefs, 'aspect_ratio', "16:9") # Default if not in prefs

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
        
        # Get negative prompt from user_prefs settings, or fallback to module default
        current_negative_prompt = settings.get("negative_prompt", negative_prompt_default)


        # Art medium detection logic
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
        detected_medium = None
        # Ensure current_negative_prompt is a string before splitting
        temp_negative_prompt_list = [p.strip() for p in str(current_negative_prompt).split(',') if p.strip()]

        for medium_key, competing_mediums_list in art_mediums.items():
            if medium_key.lower() in custom_prompt.lower():
                detected_medium = medium_key
                for competing in competing_mediums_list:
                    if competing not in temp_negative_prompt_list:
                        temp_negative_prompt_list.append(competing)
                logging.info(f"Detected art medium: {medium_key}, updated negative prompt list for general enhancement.")
                break
        current_negative_prompt = ", ".join(sorted(list(set(temp_negative_prompt_list))))
        if not current_negative_prompt: # Ensure it's not empty
            current_negative_prompt = negative_prompt_default

        medium_instruction_text = "" # Renamed to avoid conflict with f-string variable
        if detected_medium:
            medium_instruction_text = f"""
CRITICAL: This prompt explicitly mentions the art medium "{detected_medium}".
You MUST preserve this EXACT medium in your enhancement.
DO NOT convert it to any other medium (especially not 3D or digital art if traditional medium was specified).
Use terminology specific to {detected_medium} in your enhancement.
The negative prompt has been configured to exclude competing art styles.
"""
        # Fallback for no_preferences_prompt
        enforce_medium_fn = None
        try:
            from no_preferences_prompt import NO_PREFS_PROMPT_INSTRUCTIONS, enforce_art_medium
            enforce_medium_fn = enforce_art_medium
        except ImportError:
            logging.warning("no_preferences_prompt.py not found. Using default instructions for general enhancement.")
            NO_PREFS_PROMPT_INSTRUCTIONS = """
Generate a detailed and artistic prompt for a high-quality wallpaper image.
Technical parameters:
- Resolution: {resolution}
- Aspect ratio: {aspect_ratio}
The generated prompt should be detailed and descriptive, focusing on the subject provided.
Example format: "A detailed description of the image... {resolution} resolution, {aspect_ratio} aspect ratio"
Avoid: {negative_prompt}
"""
            def fallback_enforce_art_medium(prompt_text, original_prompt_text): return prompt_text
            enforce_medium_fn = fallback_enforce_art_medium
        

        # Construct general enhancement instructions
        original_prompt_prefix = f"""ENHANCE THIS EXACT PROMPT: "{custom_prompt}"

CRITICAL INSTRUCTION:
If this prompt specifies ANY artistic medium (watercolor, oil painting, 3D, digital art, etc.), you MUST PRESERVE IT EXACTLY.
DO NOT convert between mediums - a watercolor must stay watercolor, an oil painting must stay oil painting, etc.
{medium_instruction_text}
"""
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
        # Using the detailed enhancement instructions from the original provided code
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
• Photographic enhancements: {filter_type if filter_type else "Consider filter effects (e.g., polarizing filter, ND filter)"} and {special_lens if special_lens else "special lens characteristics (e.g., anamorphic lens flare, tilt-shift)"}. Consider film types like "{'black and white film' if style and 'black and white' in str(style).lower() else 'color film'}", "polaroid".

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
Avoid: {current_negative_prompt}
"""
        if not gemini_config.is_initialized():
            if not gemini_config.initialize_gemini_globally():
                logging.error(f"Gemini not initialized for general prompt enhancement: {gemini_config.get_last_error()}")
                return enforce_prompt_format(custom_prompt, resolution, aspect_ratio, current_negative_prompt)

        effective_user_prefs_general = user_prefs
        if user_prefs is None: # Should be SimplePrefs if it was None and use_user_preferences was false
             effective_user_prefs_general = SimplePrefs() # Fallback to minimal prefs for model selection

        selected_model_name = gemini_config.get_selected_gemini_model(effective_user_prefs_general)
        logging.info(f"Using Gemini model for general custom prompt enhancement: {selected_model_name}")

        try:
            client = gemini_config.get_gemini_client()
            if client is None or genai is None: # Check if genai SDK itself was imported
                logging.error("Gemini client or SDK is not initialized/imported, cannot enhance general prompt.")
                return enforce_prompt_format(custom_prompt, resolution, aspect_ratio, current_negative_prompt)
            
            response = client.models.generate_content(
                model=selected_model_name,
                contents=enhancement_instructions
            )
            
            full_response_text = response.text.strip() if hasattr(response, 'text') and response.text else None

            if full_response_text:
                full_response = full_response_text
                if not use_user_preferences and enforce_medium_fn:
                    full_response = enforce_medium_fn(full_response, custom_prompt)

                prompt_parts = full_response.split("Avoid:")
                if len(prompt_parts) > 1:
                    main_prompt = prompt_parts[0].strip()
                    negative_part = prompt_parts[1].strip()
                    if custom_prompt.lower() not in main_prompt.lower():
                        logging.warning("Enhanced general prompt doesn't contain original subject, prepending it.")
                        main_prompt = f"{custom_prompt}, {main_prompt}"
                    # Ensure the negative part from the model is combined with our current_negative_prompt
                    combined_negatives_set = set(p.strip() for p in str(current_negative_prompt).split(',') if p.strip())
                    model_negatives_set = set(p.strip() for p in negative_part.split(',') if p.strip())
                    final_negatives = ", ".join(sorted(list(combined_negatives_set.union(model_negatives_set))))
                    if not final_negatives: final_negatives = negative_prompt_default

                    return f"{main_prompt}. Avoid: {final_negatives}"
                else: # "Avoid:" not found in model response
                    enhanced_prompt = full_response
                    if enforce_medium_fn:
                         enhanced_prompt = enforce_medium_fn(enhanced_prompt, custom_prompt)
                    if custom_prompt.lower() not in enhanced_prompt.lower():
                        logging.warning("Enhanced general prompt doesn't contain original subject, prepending it.")
                        enhanced_prompt = f"{custom_prompt}, {enhanced_prompt}"
                    
                    # Add current_negative_prompt if not already included by model (unlikely if "Avoid:" was missing)
                    if current_negative_prompt and "avoid:" not in enhanced_prompt.lower():
                        enhanced_prompt += f" Avoid: {current_negative_prompt}"
                    elif not current_negative_prompt and "avoid:" not in enhanced_prompt.lower():
                        enhanced_prompt += f" Avoid: {negative_prompt_default}" # Add default if none specified and model missed it
                    return enhanced_prompt
            else:
                logging.warning("Gemini response for general prompt enhancement was empty.")
                return enforce_prompt_format(custom_prompt, resolution, aspect_ratio, current_negative_prompt)

        except Exception as e:
            logging.error(f"Error generating general prompt with Gemini: {str(e)}", exc_info=True)
            return enforce_prompt_format(custom_prompt, resolution, aspect_ratio, current_negative_prompt)

    except Exception as e:
        logging.exception(f"General error in enhance_custom_prompt: {e}")
        # Fallback to basic formatting, ensuring resolution, aspect_ratio, and negative_prompt are defined
        final_resolution = resolution if 'resolution' in locals() and resolution else "3840x2160"
        final_aspect_ratio = aspect_ratio if 'aspect_ratio' in locals() and aspect_ratio else "16:9"
        # Use current_negative_prompt if defined, else the module default
        final_negative_prompt = current_negative_prompt if 'current_negative_prompt' in locals() and current_negative_prompt else negative_prompt_default
        return enforce_prompt_format(custom_prompt, final_resolution, final_aspect_ratio, final_negative_prompt)

