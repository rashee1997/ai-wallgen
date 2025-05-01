"""
Style Templates Module for AI Preset Generator

This module provides style-specific template generation for different art styles
to ensure settings are appropriate for each style category.
"""

from typing import Dict, Any

def get_template_for_category(style_category: str) -> Dict[str, Any]:
    """
    Return the appropriate JSON template based on style category.
    
    Each template includes only the relevant settings for the specific style category.
    For example, camera settings only for photographic styles, digital software settings
    for digital art, etc.
    
    Args:
        style_category (str): The detected style category

    Returns:
        Dict[str, Any]: A JSON template with appropriate fields for the style category
    """
    # Base template with common fields all styles have
    base_template = {
        "preset_name": "[ evocative name ]",
        "moods": ["[ one mood ]"],
        "aspect_ratio": "16:9"
    }
    
    # Common settings for all categories
    imagen_settings = {
        "style_settings": {
            "art_movement": "[ fitting movement ]",
            "post_processing": ["[ 0-1 effect ]"]
        },
        "lighting_settings": {
            "lighting_type": "[ appropriate lighting ]",
            "light_quality": "[ description ]"
        },
        "composition_settings": {
            "technique": "[ composition technique ]"
        },
        "color_settings": {
            "color_scheme": "[ fitting scheme ]",
            "palette_type": "[ appropriate type ]",
            "color_temperature": "[ warm/cool/etc ]"
        }
    }
    
    # Add category-specific settings
    if style_category == "photographic" or style_category.startswith("cinematic"):
        # For photographic/cinematic styles, include camera settings
        imagen_settings["camera_settings"] = {
            "camera_model": "[ appropriate camera model ]",
            "lens_type": "[ fitting lens ]",
            "aperture": "[ f-stop value ]",
            "depth_of_field": "[ shallow/deep/etc ]"
        }
        imagen_settings["composition_settings"]["camera_angle"] = "[ appropriate angle ]"
        imagen_settings["lighting_settings"]["time_of_day"] = "[ golden hour/blue hour/etc ]"
    
    elif style_category == "digital_art":
        # For digital art, replace camera with digital-specific settings
        imagen_settings["digital_settings"] = {
            "software": "[ appropriate software ]",
            "rendering_technique": "[ technique ]", 
            "digital_effects": ["[ effect ]"]
        }
        # Add viewport settings instead of camera angle
        imagen_settings["composition_settings"]["viewport"] = "[ perspective/isometric/etc ]"
    
    elif style_category == "game_style":
        # For game styles, use game engine-specific settings
        imagen_settings["game_engine_settings"] = {
            "engine_type": "[ game engine ]",
            "render_quality": "[ quality level ]",
            "special_effects": ["[ effect ]"]
        }
        imagen_settings["composition_settings"]["camera_angle"] = "[ game camera perspective ]"
        # Add polygonal detail for game styles
        imagen_settings["style_settings"]["poly_detail"] = "[ high/low/stylized ]"
    
    elif style_category == "traditional_painting_drawing":
        # For traditional painting, add medium-specific settings
        imagen_settings["medium_settings"] = {
            "painting_medium": "[ oil/watercolor/acrylic/etc ]",
            "canvas_type": "[ canvas/paper/wood/etc ]",
            "brushwork": "[ technique ]",
            "texture": "[ texture quality ]"
        }
        # Add stylistic choices common in traditional painting
        imagen_settings["style_settings"]["brush_style"] = "[ impressionist/detailed/rough/etc ]"
    
    elif style_category.startswith("illustration"):
        # For illustration styles, include illustration-specific settings
        imagen_settings["illustration_settings"] = {
            "line_work": "[ style ]",
            "coloring_technique": "[ technique ]"
        }
        if "anime" in style_category or "manga" in style_category:
            # Anime/manga specific
            imagen_settings["illustration_settings"]["manga_style"] = "[ shonen/shojo/seinen/etc ]"
        elif "pixar" in style_category or "disney" in style_category:
            # Animation studio specific
            imagen_settings["illustration_settings"]["animation_style"] = "[ studio signature look ]"
    
    elif style_category == "abstract_conceptual":
        # For abstract art, focus on composition and conceptual elements
        imagen_settings["abstract_settings"] = {
            "visual_elements": ["[ shapes/forms/lines ]"],
            "conceptual_approach": "[ approach ]",
            "balance_type": "[ symmetric/asymmetric/radial ]"
        }
        # Remove techniques that don't apply to abstract art
        if "camera_settings" in imagen_settings:
            del imagen_settings["camera_settings"]
    
    elif style_category == "material_sculptural":
        # For sculptural and material-based styles
        imagen_settings["material_settings"] = {
            "primary_material": "[ material ]",
            "technique": "[ sculpting technique ]",
            "surface_quality": "[ polished/rough/textured ]",
            "form_type": "[ organic/geometric/abstract ]"
        }
    
    # Add the imagen_settings to the base template
    base_template["imagen_settings"] = imagen_settings
    
    return base_template
