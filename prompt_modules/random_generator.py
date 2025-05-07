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
        # Import from core to avoid circular imports
        from .core import use_user_preferences
        
        # If user_prefs is not provided and we should use preferences, get them from global
        if user_prefs is None and use_user_preferences:
            # Import here to avoid circular imports
            try:
                from wallpaper_generator import user_prefs as global_user_prefs
                user_prefs = global_user_prefs
            except ImportError:
                logging.warning("Unable to import user_prefs from wallpaper_generator.")
                user_prefs = None
            
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
            
            # Try to import no-preferences instructions for better subject preservation
            try:
                from no_preferences_prompt import (
                    NO_PREFS_RANDOM_INSTRUCTIONS
                )
            except ImportError:
                logging.warning("no_preferences_prompt.py not found. Using default instructions.")
                # Define fallbacks in case import fails
                NO_PREFS_RANDOM_INSTRUCTIONS = """
Generate a detailed and artistic prompt for a high-quality wallpaper image.

Technical parameters:
- Resolution: {resolution}
- Aspect ratio: {aspect_ratio}

The generated prompt should be detailed and descriptive, focusing on the subject tags provided.
Example format: "A detailed description of the image... {resolution} resolution, {aspect_ratio} aspect ratio"
Avoid: ugly, disfigured, low quality, blurry, nsfw, watermark, signature, out of frame, extra limbs
"""
            
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
            try:
                import google.generativeai as genai
            except ImportError:
                logging.warning("google.generativeai module not found. Some features will be disabled.")
                # Return formatted version of the basic tags
                return enforce_prompt_format(prompt, resolution, aspect_ratio, negative_prompt)
                
            gemini_api_key = os.environ.get("GEMINI_API_KEY")
            if not gemini_api_key:
                logging.warning("No Gemini API key configured")
                # Return formatted version of the basic tags
                return enforce_prompt_format(prompt, resolution, aspect_ratio, negative_prompt)
                
            try:
                genai.configure(api_key=gemini_api_key)
                model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')
                response = model.generate_content(instructions)

                if hasattr(response, 'parts') and response.parts:
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
        settings = user_prefs.imagen_settings if hasattr(user_prefs, 'imagen_settings') else {}
        
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
            from config import PROMPT_INSTRUCTIONS
        except ImportError:
            logging.warning("Could not import PROMPT_INSTRUCTIONS from config.")
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
            style_context=""
        )

        # Create a more evocative, artistic generation context
        technical_context = f"""
✨ CREATIVE VISION QUEST ✨

From the random constellation of elements: {formatted_tags}, you are tasked with weaving a single, coherent visual tapestry that harmonizes these seemingly disparate elements into one breathtaking scene.

🎨 ARTISTIC ESSENCE 🎨
• Creative Direction: {style if style else "Let the elements guide the perfect stylistic approach"}
• Emotional Resonance: {mood if mood else "What emotional atmosphere would unify these elements?"}
• Artistic Heritage: {art_movement if art_movement else "Which artistic movement would best harmonize these elements?"} 
• Historical Context: {style_era if style_era else "What time period would create the perfect backdrop?"}

💫 THE ALCHEMY CHALLENGE 💫
You're presented with seemingly unrelated elements: {formatted_tags}
Your mission is to discover the hidden connections between them and transform them into a single, coherent reality—a visual poem where each element feels essential and nothing feels forced.

Imagine you're a master illusionist who can bend reality to create impossible yet believable scenes. What magical realm could organically contain all these elements? How might they interact in a way that feels intentional rather than random?

🌎 WORLD-BUILDING FOUNDATIONS 🌎
• Atmospheric Canvas: {weather if weather else "What atmospheric conditions would unite these elements?"} during {season if season else "a season that enhances the mood"}
• Setting: {location_type if location_type else "A setting that naturally embraces all elements"}
• Environmental Poetry: {", ".join(atmospheric_effects) if atmospheric_effects else "Atmospheric qualities that enhance visual coherence"}

✨ VISUAL SYMPHONY ORCHESTRATION ✨
• Light Choreography: {lighting_type if lighting_type else "How does light dance through this scene?"} with {light_quality if light_quality else "qualities that harmonize the elements"} at {time_of_day if time_of_day else "the perfect moment of day"}
• Color Harmony: {color_scheme if color_scheme else "A palette that unifies the elements"} with {palette_type if palette_type else "tonal qualities that"} {color_temperature if color_temperature else "create the perfect visual temperature"}
• Spatial Narrative: {technique if technique else "A composition that guides the eye"} that leads to {focal_point if focal_point else "the most important element"}

🔍 ARTISTIC EXECUTION ELEMENTS 🔍
• Stylistic Approach: {painting_medium if painting_medium else "Consider what medium"} with {brushwork if brushwork else "techniques that enhance cohesion"}
• Tactile Atmosphere: {texture_quality if texture_quality else "Textural qualities"} with {texture if texture else "surface characteristics that unify the elements"}
• Detail Philosophy: {detail_level if detail_level else "A level of detail that"}
• Visual Language: {illustration_style if illustration_style else "A stylistic approach that"} with {line_quality if line_quality else "line characteristics that enhance cohesion"}
• Dynamism: {abstract_composition if abstract_composition else "Energy flows that"} with {movement_type if movement_type else "movement qualities that connect elements"}
• Material Presence: {material_type if material_type else "Physical qualities that"} with {material_finish if material_finish else "finish characteristics that elevate the scene"}

🎭 TECHNICAL MANIFESTATION 🎭
• Digital Creation: {digital_software if digital_software else "Digital techniques"} with {", ".join(digital_effects) if digital_effects else "effects that enhance unity"}
• Game-Inspired Aesthetics: {game_engine if game_engine else "Game-like qualities"} in {game_genre if game_genre else "a style that"} using {game_shader if game_shader else "rendering approaches that unify"}
• Professional Execution: {suite if suite else "Industry approaches"} with {renderer if renderer else "rendering that elevates"}

📷 OPTICAL STORYTELLING 📷
• Visual Lens: {camera_model if camera_model else "A perspective"} with {lens_type if lens_type else "optical characteristics that"}
• Technical Choices: {aperture if aperture else "Aperture choices"} at {focal_length if focal_length else "a focal length that"} with {shutter_speed if shutter_speed else "exposure timing that"} at {iso if iso else "sensitivity that captures perfectly"}
• Special Optics: {filter_type if filter_type else "Filtering effects"} with {special_lens if special_lens else "special optical characteristics"}

🌟 THE CREATIVE SYNTHESIS PROCESS 🌟
1. Discover the hidden logical connections between {formatted_tags}
2. Create a world where these elements naturally coexist
3. Craft ONE flowing paragraph where every element feels essential to the whole
4. Transform technical specifications into poetic qualities of the scene
5. End precisely with "{resolution} resolution, {aspect_ratio} aspect ratio"
6. Follow with "Avoid: [negative elements]"

⚠️ CREATIVE MANDATE ⚠️
You are writing visual poetry, not a technical document. The random elements must feel like they were always meant to be together. The technical aspects should dissolve into the narrative flow, becoming qualities of the world rather than specifications. Be bold, be imaginative, and make magic that transforms randomness into destiny.

OUTPUT FORMAT:
[A single, flowing paragraph that creates a coherent reality containing {formatted_tags}, weaving in all relevant technical elements naturally, ending exactly with "{resolution} resolution, {aspect_ratio} aspect ratio"]
Avoid: [negative elements]

NEGATIVE PROMPT - ALWAYS INCLUDE:
The following elements must be avoided: {negative_prompt}
"""

        # Generate prompt using Gemini
        try:
            gemini_api_key = os.environ.get("GEMINI_API_KEY")
            if not gemini_api_key:
                logging.warning("No Gemini API key configured")
                # Return a formatted version of the simple tags
                return enforce_prompt_format(formatted_tags, resolution, aspect_ratio, negative_prompt)

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
        formatted_tags_str = ", ".join(tags)
        # Fallback to basic tags if error occurs
        return enforce_prompt_format(formatted_tags_str, resolution, aspect_ratio, negative_prompt)


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
                from wallpaper_generator import user_prefs as global_user_prefs
                user_prefs = global_user_prefs
            except ImportError:
                logging.warning("Unable to import user_prefs from wallpaper_generator.")
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
