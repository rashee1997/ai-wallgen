"""Illustration Style Templates Module for AI Preset Generator

All illustrative template functions migrated from style_templates.py, one for each illustration* category.
"""

from typing import Dict, Any

def get_illustration_cubist_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Cubist Illustration Preset",
        "moods": ["Analytical"],
        "aspect_ratio": "16:9",
        "description": "A stylized template capturing fragmented geometric forms inspired by Cubist illustration."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Cubist Illustration"},
        "line_work": "bold geometric lines",
        "coloring_technique": "flat color planes muted palette",
        "visual_style": "stylized abstract geometric",
        "detail_level": "simplified forms",
        "subject_treatment": "fragmented multiple perspectives"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_illustration_surreal_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Surrealist Illustration Preset",
        "moods": ["Dreamlike"],
        "aspect_ratio": "16:9",
        "description": "Narrative dreamlike template for surrealist subject matter and metamorphosis in illustration."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Surrealist Illustration"},
        "line_work": "smooth flowing lines",
        "coloring_technique": "soft shading dreamlike colors",
        "visual_style": "stylized realistic surreal",
        "detail_level": "medium detailed bizarre elements",
        "subject_treatment": "metaphorical dream narrative"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_illustration_steampunk_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Steampunk Illustration Preset",
        "moods": ["Inventive"],
        "aspect_ratio": "16:9",
        "description": "Highly detailed template for techno-Victorian steampunk illustration."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Steampunk Illustration"},
        "line_work": "detailed intricate ink lines",
        "coloring_technique": "watercolor wash sepia tones",
        "visual_style": "stylized realistic victorian tech",
        "detail_level": "highly detailed mechanical elements",
        "subject_treatment": "literal depiction of steampunk concepts"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_illustration_pixar_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Pixar Style Illustration Preset",
        "moods": ["Warmth"],
        "aspect_ratio": "16:9",
        "description": "Vivid, expressive, and character-driven Pixar animation-based illustration template."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Pixar Animation Style"},
        "line_work": "soft digital lines",
        "coloring_technique": "vibrant digital color blending",
        "visual_style": "3D stylized animation",
        "detail_level": "medium",
        "subject_treatment": "expressive storytelling characters"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_illustration_disney_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Disney Style Illustration Preset",
        "moods": ["Magical"],
        "aspect_ratio": "16:9",
        "description": "Classic, musical, and optimistic Disney illustration template."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Disney Animation Style"},
        "line_work": "smooth bold digital lines",
        "coloring_technique": "rich digital color, shaded",
        "visual_style": "classic 2D or 3D animation",
        "detail_level": "medium",
        "subject_treatment": "charming characters, storybook settings"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_illustration_tom_jerry_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Tom & Jerry Cartoon Illustration Preset",
        "moods": ["Playful"],
        "aspect_ratio": "4:3",
        "description": "Slapstick, vintage cartoon, Hanna-Barbera-style illustration template."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Vintage Cartoon"},
        "line_work": "thick bold lines",
        "coloring_technique": "cel shading, flat classic cartoon color",
        "visual_style": "vintage energetic animation",
        "detail_level": "medium",
        "subject_treatment": "dynamic pranks, cartoon animals"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_illustration_vintage_cartoon_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Vintage Cartoon Illustration Preset",
        "moods": ["Nostalgic"],
        "aspect_ratio": "4:3",
        "description": "Rubber hose, 1930s classic cartoon style template."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Rubber Hose Animation"},
        "line_work": "rubbery black lines",
        "coloring_technique": "limited palette, flat classic cartoon color",
        "visual_style": "retro bouncy cartoon",
        "detail_level": "low",
        "subject_treatment": "exaggerated movement, playful scenes"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_illustration_anime_manga_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Anime/Manga Illustration Preset",
        "moods": ["Dramatic"],
        "aspect_ratio": "16:9",
        "description": "High-impact anime or manga style illustration template."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Anime/Manga Style"},
        "line_work": "fine dynamic digital lines",
        "coloring_technique": "cel shading, soft diffuse highlights",
        "visual_style": "stylized characters, expressive faces",
        "detail_level": "medium",
        "subject_treatment": "anime visual storytelling"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_illustration_comic_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Comic Illustration Preset",
        "moods": ["Dynamic"],
        "aspect_ratio": "16:9",
        "description": "Bold panel-based comic illustration template."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Comic Book Art"},
        "line_work": "dark digital inking",
        "coloring_technique": "high-contrast pop colors, halftone dots",
        "visual_style": "action scenes, dramatic foreshortening",
        "detail_level": "medium",
        "subject_treatment": "heroic or narrative comic panels"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_illustration_pixel_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Pixel Illustration Preset",
        "moods": ["Retro"],
        "aspect_ratio": "16:9",
        "description": "Low-resolution pixel art and sprite illustration template."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Pixel Art"},
        "line_work": "blocky 1px lines or none",
        "coloring_technique": "limited 8-bit or 16-bit palette",
        "visual_style": "sprite-based, grid pixel illustration",
        "detail_level": "low",
        "subject_treatment": "retro game visuals"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_illustration_childrens_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Children's Book Illustration Preset",
        "moods": ["Playful"],
        "aspect_ratio": "4:3",
        "description": "Picture book, whimsical and gentle illustration template."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Children's Illustration"},
        "line_work": "soft, rounded, colored",
        "coloring_technique": "pastel, watercolor-style soft fills",
        "visual_style": "simple, storybook",
        "detail_level": "low-medium",
        "subject_treatment": "friendly, inviting characters"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_illustration_fantasy_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Fantasy Illustration Preset",
        "moods": ["Magical"],
        "aspect_ratio": "16:9",
        "description": "Mythical, epic, and magical fantasy illustration template."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Fantasy Illustration"},
        "line_work": "dynamic fantasy lines",
        "coloring_technique": "rich, glowing digital paint",
        "visual_style": "fantasy painting, magical light",
        "detail_level": "medium-high",
        "subject_treatment": "mythical creatures and realms"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_illustration_graphic_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Graphic Illustration Preset",
        "moods": ["Bold"],
        "aspect_ratio": "16:9",
        "description": "Modern, bold, and graphical illustration template."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Graphic Design Illustration"},
        "line_work": "clean geometric lines",
        "coloring_technique": "vector, flat, bold palette",
        "visual_style": "graphic, high-contrast",
        "detail_level": "medium",
        "subject_treatment": "poster or editorial illustration"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_illustration_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Generic Illustration Preset",
        "moods": ["Storytelling"],
        "aspect_ratio": "16:9",
        "description": "A customizable template for narrative or stylized creative illustrations."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Contemporary Illustration"},
        "line_work": "clean digital lines",
        "coloring_technique": "soft digital shading",
        "visual_style": "stylized realistic",
        "detail_level": "medium detail",
        "subject_treatment": "narrative illustration"
    }
    return {**base_template, "imagen_settings": imagen_settings}
