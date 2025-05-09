"""3D Style Templates Module for AI Preset Generator

This module provides template generation for 3D rendering styles.
"""

from typing import Dict, Any
from ai_prest_gen.camera_settings import get_dynamic_camera_settings # Assuming this path is correct relative to project root

def get_3d_render_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "3D Render Preset",
        "moods": ["Realistic", "Digital"],
        "aspect_ratio": "16:9",
        "description": "A general preset for 3D rendering, focusing on realistic digital imagery."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Digital Art", "post_processing": ["realistic rendering"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Studio or Environmental", "light_quality": "Realistic", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Standard perspective view", "focal_point": "Main Subject"},
        "color_settings": {"color_scheme": "Realistic", "palette_type": "Realistic Color Palette", "color_temperature": "Neutral", "color_contrast": "Medium"},
        "detail_settings": {"detail_level": "Very High", "texture_quality": "Realistic 3D textures"},
        "environment_settings": {"weather": "Varied", "season": "Varied", "location_type": "Varied", "atmospheric_effects": ["realistic"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High Fidelity"},
        "negative_prompt": "painting, drawing, low poly, signature, watermark, low quality",
        "style_negative_prompt": "stylized rendering, unrealistic lighting"
    }
    imagen_settings["software_settings"] = {
        "suite": "Blender", "renderer": "Cycles", "version": "4.0"
    }
    imagen_settings["render_settings"] = {
        "polycount": "high polygon count", "sampling": "1024 samples", "denoiser": "enabled (OptiX)",
        "resolution": "3840x2160", "aspect_ratio": "16:9", "frame_number": "1"
    }
    imagen_settings["lighting_setup"] = {
        "system": "HDRI environment lighting with 3-point area lights", "intensity": "1.5 Strength HDRI",
        "color": "Neutral White (5500K)", "shadows": "soft realistic shadows"
    }
    imagen_settings["material_settings"] = {
        "shader_type": "Principled BSDF (PBR)", "subsurface_scattering": "0.1 (for skin if applicable)",
        "texture_maps": ["diffuse", "normal", "roughness", "metallic"], "bump_map": "yes", "displacement": "yes (micro-displacement)"
    }
    imagen_settings["camera_settings"] = {
        "camera_type": "perspective", "focal_length": "50mm", "depth_of_field": "enabled (f/2.8)",
        "focus_distance": "focused on main subject", "camera_position": "standard eye-level view"
    }
    # imagen_settings["composition_settings"]["view_mode"] = "standard perspective view" # Redundant with technique
    imagen_settings["style_settings"]["post_processing"] = ["bloom effect", "vignette", "color grading (filmic LUT)", "lens distortion (subtle)"]
    return {**base_template, "imagen_settings": imagen_settings}

# Add other 3D-specific templates here in the future if needed, e.g.:
# def get_voxel_art_template(style_category: str) -> Dict[str, Any]:
#     ...
# def get_low_poly_3d_template(style_category: str) -> Dict[str, Any]:
#     ...
