"""Portrait Style Templates Module for AI Preset Generator

This module provides style-specific template generation for different portrait
art styles to ensure settings are appropriate for each style category.
"""

from typing import Dict, Any, List, Optional, Union

def get_portrait_template(style_category: str) -> Dict[str, Any]:
    """
    Return the appropriate JSON template based on a specific portrait style category.
    """
    # Base template with common fields all styles have
    base_template = {
        "preset_name": "[ evocative name ]",
        "moods": ["[ one mood ]"],
        "aspect_ratio": "16:9",
        "description": "AI: create a description of this preset here."
    }

    # Common settings for all categories
    imagen_settings = {
        "style_settings": {
            "art_movement": "[ fitting movement ]",
            "post_processing": ["[ 0-1 effect ]"],
            "style_era": "[ appropriate era/period ]"
        },
        "lighting_settings": {
            "lighting_type": "[ appropriate lighting ]",
            "light_quality": "[ description ]",
            "light_direction": "[ direction of main light ]"
        },
        "composition_settings": {
            "technique": "[ composition technique ]",
            "focal_point": "[ main focus of composition ]"
        },
        "color_settings": {
            "color_scheme": "[ fitting scheme ]",
            "palette_type": "[ appropriate type ]",
            "color_temperature": "[ warm/cool/etc ]",
            "color_contrast": "[ high/low/medium ]"
        },
        "detail_settings": {
            "detail_level": "[ high/medium/low ]",
            "texture_quality": "[ realistic/stylized/smooth ]"
        },
        "environment_settings": {
            "weather": "[ current weather ]",
            "season": "[ current season ]",
            "location_type": "[ indoor/outdoor/etc ]",
            "atmospheric_effects": ["[ fog/rain/etc ]"]
        },
        "quality_settings": {
            "resolution": "[ target resolution e.g., 3840x2160 ]",
            "rendering_quality": "[ high/photorealistic/etc ]"
        },
        "negative_prompt": "[GENERATE_NEGATIVE_PROMPT_BASED_ON_STYLE]"
    }

    # --- Portrait Style Specific Settings ---
    if style_category == "photographic_portrait":
        imagen_settings["camera_settings"] = {
            "camera_model": "[ DSLR, Mirrorless, Medium Format ]",
            "lens_type": "[ prime, telephoto ]",
            "aperture": "[ f/1.2 - f/4 ]",
            "focal_length": "[ 50mm - 135mm ]",
            "shutter_speed": "[ 1/125s - 1/250s ]",
            "iso": "[ 100 - 800 ]",
            "filter_type": "[ polarizer, diffusion ]",
            "depth_of_field": "shallow",
            "white_balance": "[ auto, daylight, studio ]",
            "focus_mode": "autofocus",
            "exposure_mode": "aperture priority",
            "image_stabilization": "optical",
            "metering_mode": "spot",
            "flash_mode": "[ off, fill-in ]"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "studio, natural, softbox"
        imagen_settings["lighting_settings"]["light_quality"] = "soft, diffused"
        imagen_settings["lighting_settings"]["light_direction"] = "[ front, side, butterfly ]"
        imagen_settings["style_settings"]["photo_style"] = "portrait"
        imagen_settings["composition_settings"]["camera_angle"] = "eye-level"
        imagen_settings["quality_settings"]["rendering_quality"] = "photorealistic, high detail"

    elif style_category == "traditional_portrait":
        imagen_settings["medium_settings"] = {
            "painting_medium": "[ oil paint, watercolor, pastel, charcoal ]",
            "canvas_type": "[ canvas, linen, paper ]",
            "brushwork": "[ visible, blended, impasto ]",
            "texture": "[ textured, smooth ]",
            "layering_technique": "[ glazing, scumbling, washes ]",
            "stroke_style": "[ expressive, delicate ]",
            "detail_approach": "[ high, medium ]"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "natural, dramatic"
        imagen_settings["lighting_settings"]["light_quality"] = "chiaroscuro, soft"
        imagen_settings["style_settings"]["brush_style"] = "[ realistic, impressionist ]"
        imagen_settings["style_settings"]["painter_influence"] = "[ Rembrandt, Sargent, Degas ]"
        imagen_settings["style_settings"]["period"] = "[ Renaissance, Baroque, Impressionist ]"
        imagen_settings["color_settings"]["palette_type"] = "[ warm, muted, rich ]"

    elif style_category == "futuristic_portrait":
        imagen_settings["sci_fi_settings"] = {
            "character_type": "[ cybernetic, augmented, alien ]",
            "costuming": "[ tech-wear, armored, sleek ]",
            "cybernetic_elements": "[ implants, glowing eyes, digital tattoos ]",
            "environment": "[ futuristic interior, neon city backdrop ]",
            "mood": "[ stoic, intense, mysterious ]"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "neon, holographic, artificial"
        imagen_settings["lighting_settings"]["light_quality"] = "harsh, high contrast"
        imagen_settings["color_settings"]["palette_type"] = "[ neon, metallic, dark ]"
        imagen_settings["detail_settings"]["detail_level"] = "high, intricate"

    elif style_category == "illustration_portrait":
        imagen_settings["illustration_settings"] = {
            "line_work": "[ clean, sketchy, bold ]",
            "coloring_technique": "[ flat color, cell shading, soft shading ]",
            "visual_style": "[ stylized, cartoony, realistic ]",
            "detail_level": "[ detailed, simplified ]",
            "subject_treatment": "[ expressive, narrative ]"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "stylized, ambient"
        imagen_settings["color_settings"]["palette_type"] = "[ vibrant, limited, thematic ]"
        imagen_settings["style_settings"]["drawing_approach"] = "stylized"

    elif style_category == "pop_portrait":
        imagen_settings["pop_surrealism_settings"] = {
            "motif": "[ pop culture icons, lowbrow elements ]",
            "juxtaposition": "[ playful, unexpected ]",
            "narrative_element": "[ subtle, overt ]",
            "color_palette": "[ saturated, vivid, contrasting ]"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "flat, graphic"
        imagen_settings["color_settings"]["palette_type"] = "bold, vibrant"
        imagen_settings["style_settings"]["art_movement"] = "Pop Art, Lowbrow"

    elif style_category == "environmental_portrait":
        imagen_settings["environmental_settings"] = {
            "location_context": "[ subject's environment, workplace, home, urban, nature ]",
            "props": "[ key items related to subject ]",
            "storytelling_elements": "[ tell story with surroundings ]"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "natural, contextual, ambient"
        imagen_settings["lighting_settings"]["light_quality"] = "realistic, available light"
        imagen_settings["lighting_settings"]["light_direction"] = "[ window, side, backlit ]"
        imagen_settings["composition_settings"]["camera_angle"] = "environment-integrated"
        imagen_settings["style_settings"]["photo_style"] = "environmental"
        imagen_settings["quality_settings"]["rendering_quality"] = "realistic, documentary"

    elif style_category == "caricature_portrait":
        imagen_settings["caricature_settings"] = {
            "exaggeration_focus": "[ facial features, gestures, expressions ]",
            "humor_style": "[ satirical, playful ]",
            "line_quality": "[ bold, sketchy, exaggerated ]"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "cartoon, graphic"
        imagen_settings["lighting_settings"]["light_quality"] = "flat, simple"
        imagen_settings["color_settings"]["palette_type"] = "vibrant, loud, exaggerated"
        imagen_settings["style_settings"]["art_movement"] = "Caricature, cartoon"
        imagen_settings["composition_settings"]["technique"] = "[ exaggeration, distortion ]"
        imagen_settings["detail_settings"]["texture_quality"] = "stylized"

    elif style_category == "conceptual_portrait":
        imagen_settings["conceptual_settings"] = {
            "concept_theme": "[ identity, metaphor, symbolism, surrealism ]",
            "visual_motifs": "[ objects, patterns, overlays ]",
            "abstraction_level": "[ representational, abstract ]"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "artificial, dramatic, conceptual"
        imagen_settings["lighting_settings"]["light_quality"] = "moody, mysterious"
        imagen_settings["color_settings"]["palette_type"] = "[ muted, high-contrast, symbolic ]"
        imagen_settings["composition_settings"]["technique"] = "concept-driven, creative"
        imagen_settings["style_settings"]["art_movement"] = "Conceptual Art, Surrealism"

    elif style_category == "fashion_portrait":
        imagen_settings["fashion_settings"] = {
            "clothing_style": "[ haute couture, casual, editorial, avant-garde ]",
            "makeup_style": "[ bold, natural, stylized ]",
            "pose_direction": "[ directed, dynamic, expressive ]"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "studio, runway, editorial"
        imagen_settings["lighting_settings"]["light_quality"] = "high-fashion, diffusion"
        imagen_settings["color_settings"]["palette_type"] = "[ bold, trendy, monochrome ]"
        imagen_settings["style_settings"]["photo_style"] = "fashion, editorial"
        imagen_settings["composition_settings"]["camera_angle"] = "dynamic, fashion-driven"
        imagen_settings["quality_settings"]["resolution"] = "high, magazine-quality"

    elif style_category == "selfie_portrait":
        imagen_settings["selfie_settings"] = {
            "device_type": "[ smartphone, front camera ]",
            "pose_type": "[ candid, posed, spontaneous ]",
            "filters": "[ none, beauty, trend-based ]",
            "background": "[ casual, personal, social ]"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "natural, mixed"
        imagen_settings["lighting_settings"]["light_quality"] = "ambient, variable"
        imagen_settings["style_settings"]["photo_style"] = "selfie"
        imagen_settings["composition_settings"]["camera_angle"] = "arm's length, high-angle"
        imagen_settings["quality_settings"]["resolution"] = "[ phone, social-media ]"
        imagen_settings["color_settings"]["palette_type"] = "[ trendy, filtered, real-life ]"



    else:
        # Fallback for unknown portrait styles
        imagen_settings["other_portrait_settings"] = {
            "notable_features": "[ key features ]",
            "notes": "[ description/notes ]"
        }


    # Add the imagen_settings to the base template
    base_template["imagen_settings"] = imagen_settings

    return base_template
