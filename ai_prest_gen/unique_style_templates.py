"""
Unique and Miscellaneous Style Templates Module for AI Preset Generator.

This module provides specific template functions for a variety of distinct,
often niche, or thematically unique non-portrait art styles. Each function
generates a base dictionary structure tailored to the nuances of a
particular style, intended to be used by the AI for preset generation.

Examples of styles covered:
- Psychedelic
- Art Deco Revival
- Biopunk
- Kinetic Art
- Ferrofluid Art
- Abstract Conceptual
- And other specific thematic or material-based styles.

Note: Portrait styles are handled by `portrait_style_templates.py`.
Photographic styles requiring specific camera settings are in `photographic_style_templates.py`.
"""

from typing import Dict, Any

# Note: Portrait styles are handled by portrait_style_templates.py
# Photographic styles requiring specific camera settings are handled by photographic_style_templates.py

def get_psychedelic_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Psychedelic' art style.

    Args:
        style_category (str): The specific style category (e.g., "psychedelic").

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Psychedelic Preset",
        "moods": ["Trippy", "Vibrant", "Abstract"],
        "aspect_ratio": "16:9",
        "description": "A general preset for Psychedelic art, focusing on swirling patterns and vibrant colors."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Psychedelic Art", "post_processing": ["morphing effects", "color shifts"], "style_era": "60s/70s Revival"},
        "lighting_settings": {"lighting_type": "Glowing Pulsating", "light_quality": "Varied", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Swirling fractal patterns", "focal_point": "Abstract forms"},
        "color_settings": {"color_scheme": "Highly Saturated", "palette_type": "Highly Saturated Vibrant Neon Contrasting Palette", "color_temperature": "Mixed", "color_contrast": "Very High"},
        "detail_settings": {"detail_level": "High", "texture_quality": "Fluid dynamic textures"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Abstract", "atmospheric_effects": ["vibrant glow"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "realistic, mundane, signature, watermark, low quality",
        "style_negative_prompt": "rigid forms, muted colors"
    }
    imagen_settings["psychedelic_settings"] = {
        "color_palette": "vibrant neon contrasting colors", "patterns": "swirling fractal kaleidoscopic patterns",
        "visual_effects": ["glowing pulsating morphing effects"], "mood": "trippy surreal intense mind-bending"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_art_deco_revival_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Art Deco Revival' style.

    Args:
        style_category (str): The specific style category (e.g., "art_deco_revival").

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Art Deco Revival Preset",
        "moods": ["Glamorous", "Sophisticated", "Modernist"],
        "aspect_ratio": "16:9",
        "description": "A preset for Art Deco Revival, focusing on geometric symmetry and streamlined forms."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Art Deco Revival", "post_processing": ["streamlined forms"], "style_era": "Contemporary Revival"},
        "lighting_settings": {"lighting_type": "Glamorous Artificial", "light_quality": "High Contrast", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Geometric symmetry and streamlined forms", "focal_point": "Architectural or Figure"},
        "color_settings": {"color_scheme": "Gold Black Silver", "palette_type": "Gold Black Silver Jewel Tones", "color_temperature": "Neutral", "color_contrast": "High"},
        "detail_settings": {"detail_level": "High", "texture_quality": "Polished metallic and lacquered surfaces"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Luxurious Interior or Skyscraper", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "organic, messy, low detail, signature, watermark, low quality",
        "style_negative_prompt": "asymmetric composition, muted colors"
    }
    imagen_settings["art_deco_revival_settings"] = {
        "geometric_shapes": ["streamlined curves", "zigzags", "stepped forms"], "ornate_details": ["sunburst motifs", "chevrons", "geometric inlays"],
        "color_palette": ["gold", "black", "silver", "rich jewel tones"], "material_usage": ["chrome", "glass", "lacquer", "exotic woods (simulated)"]
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_fantasy_template(style_category: str) -> Dict[str, Any]: # General Fantasy
    """
    Generates a base template for a general 'Fantasy' art style.

    Args:
        style_category (str): The specific style category (e.g., "fantasy").

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Fantasy Preset",
        "moods": ["Epic", "Magical", "Adventurous"],
        "aspect_ratio": "16:9",
        "description": "A general preset for High Fantasy art, focusing on mythical scenes."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "High Fantasy Art", "post_processing": ["magical effects"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Dramatic Magical", "light_quality": "Varied", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Mythical scene composition", "focal_point": "Characters or Creatures"},
        "color_settings": {"color_scheme": "Rich Vibrant", "palette_type": "Rich Vibrant Fantasy Palette", "color_temperature": "Mixed", "color_contrast": "High"},
        "detail_settings": {"detail_level": "High", "texture_quality": "Realistic or Painterly"},
        "environment_settings": {"weather": "Varied", "season": "Varied", "location_type": "Mythical Realm or Enchanted Forest", "atmospheric_effects": ["mist", "glow"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "mundane, realistic, low detail, signature, watermark, low quality",
        "style_negative_prompt": "boring composition, flat lighting"
    }
    imagen_settings["conceptual_settings"] = {
        "world_building": "detailed world building elements",
        "technological_level": "magical medieval",
        "reality_distortion": "subtle magical or technological elements",
        "atmosphere": "wondrous and mysterious atmosphere"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_biopunk_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Biopunk' art style.

    Args:
        style_category (str): The specific style category (e.g., "biopunk").

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Biopunk Preset",
        "moods": ["Unsettling", "Organic", "Dystopian"],
        "aspect_ratio": "16:9",
        "description": "A preset for Biopunk, focusing on organic technology fusion and body horror elements."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Biopunk", "post_processing": ["organic textures"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Gritty", "light_quality": "Harsh", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Organic technology fusion", "focal_point": "Mutated forms"},
        "color_settings": {"color_scheme": "Dark Organic", "palette_type": "Dark Greens Browns Metallics with Sickly Neon Highlights", "color_temperature": "Cool", "color_contrast": "High"},
        "detail_settings": {"detail_level": "Very High", "texture_quality": "Organic slimy textured surfaces with metal"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Mutated Urban Landscape or Lab", "atmospheric_effects": ["organic haze"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "clean, mechanical only, signature, watermark, low quality",
        "style_negative_prompt": "smooth textures, bright colors"
    }
    imagen_settings["biopunk_settings"] = { # This nested key was from the original file, keeping for consistency if used
        "style_settings": {"art_movement": "Biopunk"},
        "composition_settings": {"technique": "Organic Technology Fusion with Body Horror Elements"},
        "color_settings": {"palette_type": "Dark Greens Browns Metallics with Sickly Neon Highlights"},
        "detail_settings": {"texture_quality": "Organic Slimy Textured Surfaces with Metal"},
        "base_template": {"aspect_ratio": "16:9"}, # This seems like an error in original, base_template is outer
        "moods": ["Unsettling", "Gritty", "Organic", "Dystopian"]
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_kinetic_art_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Kinetic Art' style.

    Args:
        style_category (str): The specific style category (e.g., "kinetic_art").

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Kinetic Art Preset",
        "moods": ["Dynamic", "Moving", "Mechanical"],
        "aspect_ratio": "16:9",
        "description": "A general preset for Kinetic Art, incorporating physical movement or illusion of motion."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Kinetic Art", "post_processing": ["motion effects"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Dynamic", "light_quality": "Varied", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Art incorporating physical movement or illusion of motion", "focal_point": "Movement"},
        "color_settings": {"color_scheme": "Dynamic Contrasting", "palette_type": "Dynamic Contrasting Colors", "color_temperature": "Mixed", "color_contrast": "High"},
        "detail_settings": {"detail_level": "Medium to High", "texture_quality": "Mechanical or Abstract"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Gallery or Public Space", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "static, still, signature, watermark, low quality",
        "style_negative_prompt": "lack of movement, boring composition"
    }
    imagen_settings["kinetic_art_settings"] = { # From original
        "style_settings": {"art_movement": "Kinetic Art"},
        "composition_settings": {"technique": "Art Incorporating Physical Movement or Illusion of Motion"},
        "color_settings": {"palette_type": "Dynamic Contrasting Colors"},
        "detail_settings": {"detail_level": "Medium to High Mechanical Detail"},
        "base_template": {"aspect_ratio": "16:9"},
        "moods": ["Dynamic", "Moving", "Mechanical"]
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_nightcore_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Nightcore' aesthetic style.

    Args:
        style_category (str): The specific style category (e.g., "nightcore").

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Nightcore Preset",
        "moods": ["Energetic", "Fast-paced", "Edgy"],
        "aspect_ratio": "16:9",
        "description": "A preset for Nightcore aesthetic, focusing on high energy anime visuals with music motifs."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Nightcore Aesthetic", "post_processing": ["glow effects", "motion blur"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Neon", "light_quality": "High Contrast", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Dynamic anime visuals", "focal_point": "Characters"},
        "color_settings": {"color_scheme": "Neon Pastels", "palette_type": "Neon Pastels High-Contrast Palette", "color_temperature": "Cool", "color_contrast": "High"},
        "detail_settings": {"detail_level": "High", "texture_quality": "Clean digital"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Abstract Digital Space", "atmospheric_effects": ["audio visualizer elements"]},
        "quality_settings": {"resolution": "1920x1080", "rendering_quality": "High"},
        "negative_prompt": "realistic, low energy, signature, watermark, low quality",
        "style_negative_prompt": "static visuals, muted colors"
    }
    imagen_settings["nightcore_settings"] = { # From original
        "style_settings": {"art_movement": "Nightcore Aesthetic"},
        "composition_settings": {"technique": "High Energy Anime Visuals with Music Motifs"},
        "color_settings": {"palette_type": "Neon Pastels High-Contrast Palette"},
        "post_processing": ["glow effects", "fast motion blur", "audio visualizer elements"],
        "base_template": {"aspect_ratio": "16:9"},
        "moods": ["Energetic", "Fast-paced", "Edgy", "Futuristic"]
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_optic_art_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Op Art' (Optical Art) style.

    Args:
        style_category (str): The specific style category (e.g., "optic_art").

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Optic Art Preset",
        "moods": ["Dizzying", "Geometric", "Illusionary"],
        "aspect_ratio": "1:1",
        "description": "A preset for Op Art, focusing on geometric patterns creating optical illusions."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Op Art (Optical Art)", "post_processing": ["optical illusions"], "style_era": "60s Revival"},
        "lighting_settings": {"lighting_type": "Flat Graphic", "light_quality": "Hard-edged", "light_direction": "Top"},
        "composition_settings": {"technique": "Geometric patterns creating optical illusions (e.g., Moiré)", "focal_point": "Illusion"},
        "color_settings": {"color_scheme": "High Contrast", "palette_type": "High Contrast Black and White or Complementary Colors", "color_temperature": "Neutral", "color_contrast": "Very High"},
        "detail_settings": {"detail_level": "Precise Geometric Detail", "texture_quality": "Clean sharp edges"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Abstract", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "2048x2048", "rendering_quality": "High"},
        "negative_prompt": "realistic, organic, signature, watermark, low quality",
        "style_negative_prompt": "soft edges, blended colors"
    }
    imagen_settings["optic_art_settings"] = { # From original
        "style_settings": {"art_movement": "Op Art (Optical Art)"},
        "composition_settings": {"technique": "Geometric Patterns Creating Optical Illusions (e.g., Moiré)"},
        "color_settings": {"palette_type": "High Contrast Black and White or Complementary Colors"},
        "detail_settings": {"detail_level": "Precise Geometric Detail"},
        "base_template": {"aspect_ratio": "1:1"},
        "moods": ["Dizzying", "Geometric", "Illusionary"]
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_ferrofluid_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Ferrofluid' art style.

    Args:
        style_category (str): The specific style category (e.g., "ferrofluid").

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Ferrofluid Preset",
        "moods": ["Mesmerizing", "Scientific", "Abstract"],
        "aspect_ratio": "16:9",
        "description": "A preset for Ferrofluid art, focusing on magnetic liquid abstract patterns."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Ferrofluid Art", "post_processing": ["magnetic patterns"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Dramatic", "light_quality": "Highlighting Spikes", "light_direction": "Top"},
        "composition_settings": {"technique": "Magnetic liquid abstract patterns", "focal_point": "Spikes"},
        "color_settings": {"color_scheme": "Black Silver", "palette_type": "Black Silver Metallic", "color_temperature": "Cool", "color_contrast": "High"},
        "detail_settings": {"detail_level": "Very High", "texture_quality": "Spiky glossy liquid metal texture"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Abstract", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "organic, soft, signature, watermark, low quality",
        "style_negative_prompt": "smooth texture, varied colors"
    }
    imagen_settings["ferrofluid_settings"] = { # From original
        "style_settings": {"art_movement": "Ferrofluid Art"},
        "composition_settings": {"technique": "Magnetic Liquid Abstract Patterns"},
        "color_settings": {"palette_type": "Black Silver Metallic"},
        "detail_settings": {"texture_quality": "Spiky Glossy Liquid Metal Texture"},
        "base_template": {"aspect_ratio": "16:9"},
        "moods": ["Mesmerizing", "Scientific", "Abstract"]
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_animal_inspired_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for 'Animal Inspired' art/design.

    Args:
        style_category (str): The specific style category (e.g., "animal_inspired").

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Animal Inspired Preset",
        "moods": ["Natural", "Wild", "Organic"],
        "aspect_ratio": "16:9",
        "description": "A preset for Animal Inspired art/design, incorporating animal motifs, patterns, or forms."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Animal Inspired Art/Design", "post_processing": ["texture mimicry"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Natural", "light_quality": "Varied", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Incorporating animal motifs patterns or forms", "focal_point": "Animal elements"},
        "color_settings": {"color_scheme": "Natural", "palette_type": "Palette Derived from Animal Colors/Environment", "color_temperature": "Varied", "color_contrast": "Medium"},
        "detail_settings": {"detail_level": "High", "texture_quality": "Textures mimicking fur feathers scales"},
        "environment_settings": {"weather": "Varied", "season": "Varied", "location_type": "Natural Habitat", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "mechanical, artificial, signature, watermark, low quality",
        "style_negative_prompt": "unrealistic textures, geometric forms"
    }
    imagen_settings["animal_inspired_settings"] = { # From original
        "style_settings": {"art_movement": "Animal Inspired Art/Design"},
        "composition_settings": {"technique": "Incorporating Animal Motifs Patterns or Forms"},
        "color_settings": {"palette_type": "Palette Derived from Animal Colors/Environment"},
        "detail_settings": {"texture_quality": "Textures Mimicking Fur Feathers Scales"},
        "base_template": {"aspect_ratio": "16:9"},
        "moods": ["Natural", "Wild", "Organic"]
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_abstract_conceptual_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for 'Abstract Conceptual' art.

    Args:
        style_category (str): The specific style category (e.g., "abstract_conceptual").

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Abstract Conceptual Preset",
        "moods": ["Thought-provoking", "Symbolic", "Intellectual"],
        "aspect_ratio": "16:9",
        "description": "A preset for Abstract Conceptual art, focusing on idea-based abstract composition."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Abstract Conceptual Art", "post_processing": ["conceptual effects"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Conceptual", "light_quality": "Varied", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Idea-based abstract composition", "focal_point": "Concept"},
        "color_settings": {"color_scheme": "Varied", "palette_type": "Symbolic or Expressive Palette", "color_temperature": "Mixed", "color_contrast": "Varied"},
        "detail_settings": {"detail_level": "Varied", "texture_quality": "Varied based on concept"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Abstract", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "realistic, literal, signature, watermark, low quality",
        "style_negative_prompt": "concrete representation, predictable composition"
    }
    imagen_settings["abstract_settings"] = { # From original
        "visual_elements": ["geometric shapes", "organic forms", "expressive lines"], "conceptual_approach": "exploring emotion through color and form",
        "balance_type": "asymmetric dynamic balance", "movement_type": "dynamic visual flow",
        "abstraction_level": "complete abstraction", "composition_complexity": "complex layered composition"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_material_sculptural_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for 'Material Sculptural' art.

    Args:
        style_category (str): The specific style category (e.g., "material_sculptural").

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Material Sculptural Preset",
        "moods": ["Tactile", "Solid", "Form-focused"],
        "aspect_ratio": "1:1",
        "description": "A preset for Material Sculptural art, focusing on material form and texture in 3D space."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Contemporary Sculpture", "post_processing": ["material rendering"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Dramatic", "light_quality": "Highlighting Form and Texture", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Focus on material form and texture in 3D space", "focal_point": "Material"},
        "color_settings": {"color_scheme": "Natural Material", "palette_type": "Natural Material Colors or Applied Patina/Paint", "color_temperature": "Varied", "color_contrast": "High"},
        "detail_settings": {"detail_level": "Very High", "texture_quality": "Realistic material texture (e.g., wood grain, metal sheen)"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Gallery or Studio", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "2048x2048", "rendering_quality": "High Fidelity"},
        "negative_prompt": "flat, 2d, painting, drawing, signature, watermark, low quality",
        "style_negative_prompt": "unrealistic material texture, lack of form"
    }
    imagen_settings["material_settings"] = { # From original
        "primary_material": "bronze (simulated)", "technique": "casting and carving (simulated)",
        "surface_quality": "polished with patina", "form_type": "organic figurative form",
        "dimensionality": "full-3D sculpture", "scale": "life-size scale", "finishing": "natural bronze patina"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_traditional_painting_drawing_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for general 'Traditional Painting/Drawing' styles.

    Args:
        style_category (str): The specific style category (e.g., "traditional_painting_drawing").

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Traditional Painting/Drawing Preset",
        "moods": ["Classic", "Timeless", "Handcrafted"],
        "aspect_ratio": "16:9",
        "description": "A general preset for Traditional Painting/Drawing, focusing on classical techniques."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Traditional Art (General)", "post_processing": ["medium texture"], "style_era": "Varied"},
        "lighting_settings": {"lighting_type": "Naturalistic or Studio", "light_quality": "Varied", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Classical composition techniques", "focal_point": "Main Subject"},
        "color_settings": {"color_scheme": "Varied", "palette_type": "Traditional Pigment Palette", "color_temperature": "Varied", "color_contrast": "Medium"},
        "detail_settings": {"detail_level": "High", "texture_quality": "Medium-specific texture (Canvas, Paper, Paint)"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Studio", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "digital, cg, signature, watermark, low quality",
        "style_negative_prompt": "lack of texture, unrealistic rendering"
    }
    imagen_settings["medium_settings"] = { # From original
        "painting_medium": "oil paint", "support_type": "textured paper" if style_category == "charcoal" else "canvas",
        "technique": "hatching and smudging" if style_category == "charcoal" else "glazing and blending",
        "texture": "gritty charcoal texture" if style_category == "charcoal" else "oil paint texture",
        "layering_technique": "layered charcoal tones" if style_category == "charcoal" else "fat over lean",
        "stroke_style": "expressive textured strokes", "detail_approach": "medium realistic detail"
    }
    return {**base_template, "imagen_settings": imagen_settings}
