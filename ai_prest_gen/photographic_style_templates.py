"""Photographic Styles Templates Module for AI Preset Generator

This module provides template generation for all photographic-based styles:
- photographic
- cinematic
- documentary
- street_photography
- noir_photography
- luna_photo

Each function preserves the distinct template logic for its style, using dynamic camera settings
where appropriate for realism and technical accuracy.
"""

from typing import Dict, Any
from ai_prest_gen.camera_settings import get_dynamic_camera_settings

def get_photographic_template(style_category: str) -> Dict[str, Any]:
    """Generic photographic template with dynamic camera settings."""
    base_template = {
        "preset_name": "Photographic Preset",
        "moods": ["Authentic"],
        "aspect_ratio": "16:9",
        "description": "A preset capturing a scene with the realism and feel of a camera photograph."
    }
    imagen_settings = {
        "style_settings": {
            "art_movement": "Contemporary",
            "post_processing": ["subtle color grading", "realistic noise grain"],
            "style_era": "Modern Photography"
        },
        "lighting_settings": {
            "lighting_type": "Natural",
            "light_quality": "Soft Diffused",
            "light_direction": "Side-Front",
            "time_of_day": "Day"
        },
        "composition_settings": {
            "technique": "Rule of Thirds",
            "focal_point": "Main Subject",
            "camera_angle": "Eye-level",
            "perspective": "Normal"
        },
        "color_settings": {
            "color_scheme": "Harmonious",
            "palette_type": "Natural",
            "color_temperature": "Neutral",
            "color_contrast": "Medium",
            "dominant_colors": ["green", "brown", "blue"]
        },
        "detail_settings": {
            "detail_level": "High",
            "texture_quality": "Realistic"
        },
        "environment_settings": {
            "weather": "Clear",
            "season": "Summer",
            "location_type": "Outdoor",
            "atmospheric_effects": ["none"]
        },
        "quality_settings": {
            "resolution": "3840x2160",
            "rendering_quality": "High"
        },
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, text, words, amateur, low quality, cartoon, painting, sketch, drawing, illustration, CGI, unrealistic, abstract",
        "style_negative_prompt": "clashing styles, inconsistent lighting, poor composition, unrealistic elements, generic, boring, flat, overly stylized, excessive saturation, unnatural distortion",
        "camera_settings": get_dynamic_camera_settings("photographic")
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_cinematic_template(style_category: str) -> Dict[str, Any]:
    """Cinematic style template with dynamic camera settings."""
    base_template = {
        "preset_name": "Cinematic Drama",
        "moods": ["Dramatic"],
        "aspect_ratio": "16:9",
        "description": "A preset emulating film stills with dramatic lighting, color (teal & orange), and cinematic atmosphere."
    }
    imagen_settings = {
        "style_settings": {
            "art_movement": "Contemporary Cinema",
            "post_processing": [
                "cinematic color grading",
                "shallow depth of field",
                "film grain"
            ],
            "style_era": "Modern Film"
        },
        "lighting_settings": {
            "lighting_type": "Dramatic",
            "light_quality": "Hard",
            "light_direction": "Side",
            "time_of_day": "Late Afternoon"
        },
        "composition_settings": {
            "technique": "Rule of Thirds",
            "focal_point": "Main Subject",
            "camera_angle": "Low Angle",
            "perspective": "Two-point"
        },
        "color_settings": {
            "color_scheme": "Complementary",
            "palette_type": "High Contrast",
            "color_temperature": "Mixed",
            "color_contrast": "High",
            "dominant_colors": ["teal", "orange"]
        },
        "detail_settings": {
            "detail_level": "High",
            "texture_quality": "Realistic"
        },
        "environment_settings": {
            "weather": "Clear",
            "season": "Autumn",
            "location_type": "Urban",
            "atmospheric_effects": ["cinematic haze", "dust motes"]
        },
        "quality_settings": {
            "resolution": "3840x2160",
            "rendering_quality": "High"
        },
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, text, words, amateur, low quality, cartoon, illustration, painting, sketch, unrealistic rendering",
        "style_negative_prompt": "clashing styles, inconsistent lighting, poor composition, unrealistic elements, generic, boring, flat lighting, poor color grading, digital artifacts, excessive noise, lack of depth, lack of atmosphere",
        "camera_settings": get_dynamic_camera_settings("cinematic")
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_documentary_template(style_category: str) -> Dict[str, Any]:
    """Documentary style template with dynamic camera settings."""
    base_template = {
        "preset_name": "Documentary Style Preset",
        "moods": ["Reportage"],
        "aspect_ratio": "16:9",
        "description": "A preset that conveys truthful, real-world stories with authentic color, natural lighting, and photographic character."
    }
    imagen_settings = {
        "style_settings": {
            "art_movement": "Documentary Photography",
            "post_processing": ["minimal correction"],
            "style_era": "Contemporary"
        },
        "lighting_settings": {
            "lighting_type": "Ambient",
            "light_quality": "Mixed",
            "light_direction": "Natural Available",
            "time_of_day": "Variable"
        },
        "composition_settings": {
            "technique": "Candid Composition",
            "focal_point": "People or event",
            "camera_angle": "Reporter’s POV",
            "perspective": "Realistic"
        },
        "color_settings": {
            "color_scheme": "Realistic",
            "palette_type": "Desaturated",
            "color_temperature": "Mixed",
            "color_contrast": "Low",
            "dominant_colors": ["grey", "flesh tones", "muted blue"]
        },
        "detail_settings": {
            "detail_level": "Medium",
            "texture_quality": "Natural"
        },
        "environment_settings": {
            "weather": "Varies",
            "season": "Any",
            "location_type": "On Location",
            "atmospheric_effects": ["none"]
        },
        "quality_settings": {
            "resolution": "3840x2160",
            "rendering_quality": "High"
        },
        "negative_prompt": "posed, staged, overly edited, stylized, artificial, low quality, blurry, grainy, signature, watermark, cartoon, illustration, painting, CGI, unrealistic, abstract",
        "style_negative_prompt": "unrealistic color, excessive contrast, stylized lighting, shallow depth of field when inappropriate",
        "camera_settings": get_dynamic_camera_settings("documentary")
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_street_photography_template(style_category: str) -> Dict[str, Any]:
    """Street photography template with dynamic camera settings."""
    base_template = {
        "preset_name": "Street Photography Preset",
        "moods": ["Candid"],
        "aspect_ratio": "16:9",
        "description": "A preset designed to capture urban life with spontaneous composition, realistic textures, and natural ambient light."
    }
    imagen_settings = {
        "style_settings": {
            "art_movement": "Street Photography",
            "post_processing": ["subtle grain"],
            "style_era": "Modern"
        },
        "lighting_settings": {
            "lighting_type": "Natural",
            "light_quality": "Ambient",
            "light_direction": "Mixed",
            "time_of_day": "Any"
        },
        "composition_settings": {
            "technique": "Candid",
            "focal_point": "Street Action",
            "camera_angle": "Eye-level / Hip shot",
            "perspective": "Realistic"
        },
        "color_settings": {
            "color_scheme": "Muted and Natural",
            "palette_type": "Realistic Urban",
            "color_temperature": "Neutral or Cool",
            "color_contrast": "Low",
            "dominant_colors": ["grey", "asphalt", "stone", "skin", "urban hues"]
        },
        "detail_settings": {
            "detail_level": "Medium",
            "texture_quality": "Sharp"
        },
        "environment_settings": {
            "weather": "Any",
            "season": "Any",
            "location_type": "Urban Outdoors",
            "atmospheric_effects": ["none"]
        },
        "quality_settings": {
            "resolution": "3840x2160",
            "rendering_quality": "High"
        },
        "negative_prompt": "staged, unnatural, painted, illustration, low quality, blurry, signature, watermark, cartoon, CGI, unrealistic depth",
        "style_negative_prompt": "unrealistic color grading, excessive blurring, artificial lighting",
        "camera_settings": get_dynamic_camera_settings("street_photography")
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_noir_photography_template(style_category: str) -> Dict[str, Any]:
    """Noir photography template with dynamic camera settings."""
    base_template = {
        "preset_name": "Noir Photography Preset",
        "moods": ["Moody"],
        "aspect_ratio": "16:9",
        "description": "A preset inspired by noir film photography with high contrast, moody lighting, and monochrome palette."
    }
    imagen_settings = {
        "style_settings": {
            "art_movement": "Film Noir",
            "post_processing": ["high contrast", "grain", "vignette", "black and white"],
            "style_era": "20th Century"
        },
        "lighting_settings": {
            "lighting_type": "Artificial",
            "light_quality": "Hard Shadow",
            "light_direction": "Side / Top",
            "time_of_day": "Night"
        },
        "composition_settings": {
            "technique": "Chiaroscuro",
            "focal_point": "Character or Object",
            "camera_angle": "Oblique / Low",
            "perspective": "Dramatic"
        },
        "color_settings": {
            "color_scheme": "Black & White / Greyscale",
            "palette_type": "Monochrome",
            "color_temperature": "Cool",
            "color_contrast": "High",
            "dominant_colors": ["black", "white", "grey"]
        },
        "detail_settings": {
            "detail_level": "High",
            "texture_quality": "Film Grain"
        },
        "environment_settings": {
            "weather": "Foggy or Clear",
            "season": "Any",
            "location_type": "City Night",
            "atmospheric_effects": ["fog", "shadow", "streetlight glare"]
        },
        "quality_settings": {
            "resolution": "3840x2160",
            "rendering_quality": "High"
        },
        "negative_prompt": "colorful, cartoon, staged, unrealistic, painting, sketch, cgi, signature, watermark, low quality, blurry",
        "style_negative_prompt": "flat lighting, no shadows, muted contrast, modern digital clarity",
        "camera_settings": get_dynamic_camera_settings("noir_photography")
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_luna_photo_template(style_category: str) -> Dict[str, Any]:
    """Luna/moon-inspired photo template with dynamic camera settings."""
    base_template = {
        "preset_name": "Luna Photo Preset",
        "moods": ["Ethereal"],
        "aspect_ratio": "16:9",
        "description": "A preset for moonlit or lunar-themed night photography: dreamy, with cool tones and atmospheric effects."
    }
    imagen_settings = {
        "style_settings": {
            "art_movement": "Surreal Nocturne",
            "post_processing": ["blue tone", "dreamy glow", "subtle vignette", "double exposure"],
            "style_era": "Modern"
        },
        "lighting_settings": {
            "lighting_type": "Moonlight",
            "light_quality": "Soft Diffuse",
            "light_direction": "Top / Side",
            "time_of_day": "Night"
        },
        "composition_settings": {
            "technique": "Wide Angle / Minimalist",
            "focal_point": "Moon or Main Figure",
            "camera_angle": "Low Upward",
            "perspective": "Expansive"
        },
        "color_settings": {
            "color_scheme": "Monochromatic Cool",
            "palette_type": "Blue/Grey Mood",
            "color_temperature": "Cool",
            "color_contrast": "Low",
            "dominant_colors": ["midnight blue", "slate", "white"]
        },
        "detail_settings": {
            "detail_level": "Medium",
            "texture_quality": "Smooth"
        },
        "environment_settings": {
            "weather": "Clear or Foggy",
            "season": "Any",
            "location_type": "Outdoors Night",
            "atmospheric_effects": ["moon glow", "mist", "bokeh"]
        },
        "quality_settings": {
            "resolution": "3840x2160",
            "rendering_quality": "High"
        },
        "negative_prompt": "harsh daylight, sunlight, crowded, high contrast, warmth, hand-drawn, signature, cartoon, painting, illustration, cgi, low quality, blurry",
        "style_negative_prompt": "warm tones, harsh shadows, chaos, daylight, excessive digital clarity",
        "camera_settings": get_dynamic_camera_settings("luna_photo")
    }
    return {**base_template, "imagen_settings": imagen_settings}
