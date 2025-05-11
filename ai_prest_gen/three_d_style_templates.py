"""
3D Style Templates Module for AI Preset Generator.

This module provides specific template functions for various 3D rendering styles.
Each function generates a base dictionary structure tailored to the nuances of a
particular 3D style, intended to be used by the AI for preset generation.

Styles covered include:
- General 3D Render
- Voxel Art
- Low Poly 3D
- Cartoon 3D
- Anime 3D
- Abstract 3D
- Wireframe 3D
- Clay Render 3D
"""

from typing import Dict, Any
from ai_prest_gen.camera_settings import get_dynamic_camera_settings # Assuming this path is correct relative to project root

def get_3d_render_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for a general '3D Render' style.

    Args:
        style_category (str): The specific style category (e.g., "3d_render").

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
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


def get_voxel_art_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Voxel Art' style.

    Args:
        style_category (str): The specific style category (e.g., "voxel_art").

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Voxel Art Preset",
        "moods": ["Pixelated", "Retro", "Blocky", "Geometric"],
        "aspect_ratio": "16:9",  # Or "1:1" often common for voxel showcases
        "description": "A preset for generating voxel art, characterized by its blocky, cubic aesthetic."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Voxel Art", "post_processing": ["sharp pixels", "no anti-aliasing (optional)"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Simple Directional or Ambient", "light_quality": "Hard or Flat", "light_direction": "Varied", "time_of_day": "Varied"},
        "composition_settings": {"technique": "Isometric or Perspective", "focal_point": "Main Subject", "camera_angle": "Varied", "perspective": "One-point or Isometric"},
        "color_settings": {"color_scheme": "Vibrant or Thematic", "palette_type": "Limited Color Palette", "color_temperature": "Neutral", "color_contrast": "High", "dominant_colors": ["varied based on theme"]},
        "detail_settings": {"detail_level": "Block Level", "texture_quality": "Flat Color Per Voxel"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Abstract or Scene", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "1920x1080 or 2048x2048", "rendering_quality": "Standard"},
        "negative_prompt": "photorealistic, smooth shading, complex textures, high poly, detailed sculpting, anti-aliasing, soft shadows, gradients, blur, depth of field",
        "style_negative_prompt": "realistic rendering, intricate details beyond voxel resolution, smooth surfaces"
    }
    imagen_settings["software_settings"] = {
        "suite": "MagicaVoxel, Blender, Qubicle", "renderer": "MagicaVoxel Renderer, Eevee (with emission/simple diffuse)", "version": "Latest"
    }
    imagen_settings["render_settings"] = {
        "polycount": "N/A (Voxel-based)", "sampling": "Low (e.g., 64-128 samples)", "denoiser": "Often disabled",
        "resolution": "1920x1080", "aspect_ratio": "16:9", "frame_number": "1"
    }
    imagen_settings["lighting_setup"] = {
        "system": "Simple sun lamp or ambient occlusion", "intensity": "Varied",
        "color": "White or Thematic", "shadows": "hard blocky shadows or none"
    }
    imagen_settings["material_settings"] = {
        "shader_type": "Emission or Diffuse BSDF (Unlit)", "subsurface_scattering": "0",
        "texture_maps": ["diffuse (solid color per voxel)"], "bump_map": "no", "displacement": "no"
    }
    imagen_settings["camera_settings"] = get_dynamic_camera_settings(style_category)
    return {**base_template, "imagen_settings": imagen_settings}

def get_surreal_3d_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Surreal 3D' style.
    Args:
        style_category (str): The specific style category (e.g., "surreal_3d").
    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Surreal 3D Dreamscape Preset",
        "moods": ["Dreamlike", "Ethereal", "Symbolic", "Unconventional", "Mysterious"],
        "aspect_ratio": "16:9",
        "description": "A preset for Surreal 3D art, focusing on dreamlike, illogical scenes and symbolic imagery."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Digital Surrealism", "post_processing": ["dreamy glow", "chromatic aberration (subtle)", "film grain", "soft focus"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Symbolic & Dramatic", "light_quality": "Varied (soft ethereal, hard dramatic)", "light_direction": "Unconventional, to enhance mood", "time_of_day": "Twilight or Abstract Time"},
        "composition_settings": {"technique": "Juxtaposition of unrelated elements, rule of thirds (loosely)", "focal_point": "Key symbolic object or anomaly", "camera_angle": "Unusual, disorienting", "perspective": "Distorted or exaggerated"},
        "color_settings": {"color_scheme": "Symbolic (muted with accent, or vivid contrasting)", "palette_type": "Custom, mood-driven", "color_temperature": "Varied (often cool or mixed)", "color_contrast": "Medium to High", "dominant_colors": ["deep blues", "purples", "muted earth tones", "vibrant accents"]},
        "detail_settings": {"detail_level": "Medium to High (realistic detail on surreal forms)", "texture_quality": "Varied (realistic, smooth, or bizarre)"},
        "environment_settings": {"weather": "N/A or Symbolic (e.g., perpetual rain)", "season": "N/A", "location_type": "Dreamscape, Illogical Space, Impossible Architecture", "atmospheric_effects": ["mist", "volumetric light", "floating particles"]},
        "quality_settings": {"resolution": "2560x1440", "rendering_quality": "High"},
        "negative_prompt": "boring, mundane, realistic everyday scene, symmetrical (unless intentional), flat lighting, simple composition, purely abstract (no recognizable forms)",
        "style_negative_prompt": "logical consistency, predictable elements, overly bright and cheerful (unless ironic), lack of depth or atmosphere"
    }
    imagen_settings["software_settings"] = {"suite": "Blender, Cinema 4D, Houdini", "renderer": "Cycles, Octane, Redshift", "version": "Latest"}
    imagen_settings["render_settings"] = {"polycount": "Varied", "sampling": "High", "denoiser": "Enabled"}
    imagen_settings["lighting_setup"] = {"system": "HDRI, spotlights, emissive materials for symbolic lighting", "intensity": "Varied", "color": "Thematic", "shadows": "Soft or hard, emphasizing mood"}
    imagen_settings["material_settings"] = {"shader_type": "Principled BSDF, Glass, Emissive", "texture_maps": ["diffuse", "normal", "custom for surreal effects"]}
    imagen_settings["camera_settings"] = get_dynamic_camera_settings(style_category)
    return {**base_template, "imagen_settings": imagen_settings}

def get_painterly_3d_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Painterly 3D (NPR)' style.
    Args:
        style_category (str): The specific style category (e.g., "painterly_3d").
    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Painterly 3D NPR Preset",
        "moods": ["Artistic", "Impressionistic", "Stylized", "Textured", "Non-Photorealistic"],
        "aspect_ratio": "4:3",
        "description": "A preset for Painterly 3D (NPR), simulating traditional painting techniques with visible brushstrokes and textures."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Digital Impressionism / Painterly NPR", "post_processing": ["simulated brushstrokes filter", "canvas texture overlay", "palette knife effect simulation"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Soft Natural or Studio", "light_quality": "Diffused, painterly highlights", "light_direction": "Classic art lighting (e.g., side light)", "time_of_day": "Varied"},
        "composition_settings": {"technique": "Artistic composition (rule of thirds, golden ratio)", "focal_point": "Main subject with painterly emphasis", "camera_angle": "Eye-level or slightly artistic", "perspective": "Naturalistic or slightly stylized"},
        "color_settings": {"color_scheme": "Harmonious or Broken Color (Impressionistic)", "palette_type": "Rich, blended colors", "color_temperature": "Warm or Cool, thematic", "color_contrast": "Medium", "dominant_colors": ["varied, mimicking paint pigments"]},
        "detail_settings": {"detail_level": "Medium (form over micro-detail)", "texture_quality": "Visible Brushstrokes, Canvas/Paper Weave, Impasto"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Stylized Scene or Portrait Setting", "atmospheric_effects": ["painterly depth, soft focus background"]},
        "quality_settings": {"resolution": "2560x1920", "rendering_quality": "High"},
        "negative_prompt": "photorealistic, 3d render look, smooth shading, crisp digital lines, CGI artifacts, perfect geometry, flat colors (unless stylized flat painting)",
        "style_negative_prompt": "overly clean, digital precision, lack of texture, photographic realism, hard CGI shadows"
    }
    imagen_settings["software_settings"] = {"suite": "Blender (NPR shaders, Eevee/Cycles), Substance Painter (for textures), Krita/Photoshop (for texture painting)", "renderer": "Eevee (with custom shaders), Cycles (with NPR nodes), specialized NPR renderers", "version": "Latest"}
    imagen_settings["render_settings"] = {"polycount": "Medium", "sampling": "Medium", "denoiser": "Enabled"}
    imagen_settings["lighting_setup"] = {"system": "Softboxes, HDRI with artistic tones", "intensity": "Moderate", "color": "Natural or slightly tinted", "shadows": "Soft, painterly"}
    imagen_settings["material_settings"] = {"shader_type": "Custom NPR shaders, Diffuse with painted textures", "texture_maps": ["hand-painted diffuse", "normal map from brushstrokes", "roughness simulating paint sheen"]}
    imagen_settings["camera_settings"] = get_dynamic_camera_settings(style_category)
    return {**base_template, "imagen_settings": imagen_settings}

def get_technical_illustration_3d_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Technical Illustration 3D' style.
    Args:
        style_category (str): The specific style category (e.g., "technical_illustration_3d").
    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Technical Illustration 3D Preset",
        "moods": ["Informative", "Clean", "Precise", "Schematic", "Blueprint-like"],
        "aspect_ratio": "16:9",
        "description": "A preset for Technical Illustration 3D, emphasizing clarity, precision, and often showcasing internal components or structure."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Technical Illustration / Infographics", "post_processing": ["crisp outlines", "ambient occlusion pass for clarity", "subtle cel shading (optional)"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Even Studio or Ambient Occlusion focus", "light_quality": "Clear, Uniform", "light_direction": "Omnidirectional or specific to highlight features", "time_of_day": "N/A"},
        "composition_settings": {"technique": "Exploded views, cutaways, orthographic projection", "focal_point": "Key components or overall structure", "camera_angle": "Isometric, top, front, side, or clear perspective", "perspective": "Orthographic or Perspective (low distortion)"},
        "color_settings": {"color_scheme": "Limited, Functional (e.g., greyscale with accent colors)", "palette_type": "Clean, often desaturated with highlights", "color_temperature": "Neutral", "color_contrast": "High (for readability)", "dominant_colors": ["greys", "whites", "blues", "accent color (e.g., red, orange)"]},
        "detail_settings": {"detail_level": "High (precision in geometry)", "texture_quality": "Clean, Simple Materials (matte plastic, metal, glass)"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Neutral Background (white, grey, gradient, blueprint grid)", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "1920x1080 or higher for print", "rendering_quality": "High"},
        "negative_prompt": "photorealistic scene, artistic stylization (unless clean NPR), complex textures, organic forms (unless the subject is organic), busy background, dramatic lighting",
        "style_negative_prompt": "cluttered, unclear, overly artistic rendering, distracting elements, poor readability, complex PBR materials"
    }
    imagen_settings["software_settings"] = {"suite": "Blender, SolidWorks, AutoCAD, Keyshot, Fusion 360", "renderer": "Eevee, Cycles (with toon/AO), Keyshot, specialized technical renderers", "version": "Latest"}
    imagen_settings["render_settings"] = {"polycount": "Precise to model", "sampling": "Medium", "denoiser": "Enabled"}
    imagen_settings["lighting_setup"] = {"system": "Ambient occlusion, dome light, or clean studio setup", "intensity": "Even", "color": "White", "shadows": "Subtle contact shadows or none for pure orthographic"}
    imagen_settings["material_settings"] = {"shader_type": "Diffuse, Principled BSDF (simplified), Toon BSDF (for outlines/cel look)", "texture_maps": ["minimal, flat colors, simple procedural for metals"]}
    imagen_settings["camera_settings"] = get_dynamic_camera_settings(style_category)
    imagen_settings["camera_settings"]["camera_type"] = "orthographic"
    imagen_settings["camera_settings"]["focal_length"] = "N/A (orthographic)"
    imagen_settings["camera_settings"]["depth_of_field"] = "disabled"
    return {**base_template, "imagen_settings": imagen_settings}

def get_minecraft_style_3d_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Minecraft Style 3D' art.
    Args:
        style_category (str): The specific style category (e.g., "minecraft_style_3d").
    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Minecraft Blocky World Preset",
        "moods": ["Adventurous", "Creative", "Blocky", "Pixelated"],
        "aspect_ratio": "16:9",
        "description": "A preset for generating 3D art in the iconic blocky, pixel-art style of Minecraft."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Minecraft Voxel Style", "post_processing": ["sharp pixelated textures", "distinct block forms", "no anti-aliasing"], "style_era": "Contemporary Gaming"},
        "lighting_settings": {"lighting_type": "Simple Directional (Sun)", "light_quality": "Hard, blocky shadows", "light_direction": "Overhead or Angled", "time_of_day": "Daytime (classic Minecraft)"},
        "composition_settings": {"technique": "Perspective or Isometric View", "focal_point": "Player-built structure or Landscape Feature", "camera_angle": "First-person or Third-person view", "perspective": "Block-based Grid"},
        "color_settings": {"color_scheme": "Minecraft Palette (earthy, vibrant greens, blues)", "palette_type": "Pixel Art Texture Palette", "color_temperature": "Neutral", "color_contrast": "Medium-High", "dominant_colors": ["green (grass)", "brown (dirt/wood)", "grey (stone)", "blue (sky/water)"]},
        "detail_settings": {"detail_level": "Block Resolution", "texture_quality": "Pixelated Block Textures (16x16 style)"},
        "environment_settings": {"weather": "Clear or Minecraft weather (rain, snow)", "season": "Varied (matching biome)", "location_type": "Minecraft Biome (Plains, Forest, Mountains, Caves)", "atmospheric_effects": ["simple skybox", "blocky clouds"]},
        "quality_settings": {"resolution": "1920x1080", "rendering_quality": "Standard (emphasizing style over realism)"},
        "negative_prompt": "photorealistic, smooth shading, high poly models, complex curves, detailed organic forms (non-blocky), soft shadows, anti-aliasing, realistic water",
        "style_negative_prompt": "round objects, smooth terrain, realistic textures, detailed foliage (non-blocky), non-pixelated textures"
    }
    imagen_settings["software_settings"] = {"suite": "Blender (with custom block shaders), MagicaVoxel, Mineways", "renderer": "Eevee or Cycles (stylized), Minecraft Java/Bedrock (screenshots)", "version": "Latest"}
    imagen_settings["render_settings"] = {"polycount": "N/A (Voxel/Block-based)", "sampling": "Low", "denoiser": "Disabled"}
    imagen_settings["lighting_setup"] = {"system": "Directional sun lamp, simple ambient light", "intensity": "Bright", "color": "White/Yellowish", "shadows": "Hard, distinct block shadows"}
    imagen_settings["material_settings"] = {"shader_type": "Diffuse with pixel art texture maps", "texture_maps": ["pixel art diffuse (e.g., 16x16 per block type)"], "bump_map": "no", "displacement": "no"}
    imagen_settings["camera_settings"] = get_dynamic_camera_settings(style_category)
    # Override some camera settings for Minecraft feel
    imagen_settings["camera_settings"]["camera_type"] = "perspective"
    imagen_settings["camera_settings"]["field_of_view"] = "70-90 degrees (typical for games)" # Minecraft default is around 70
    imagen_settings["camera_settings"]["focal_length"] = "N/A (use FoV)"
    imagen_settings["camera_settings"]["depth_of_field"] = "disabled"

    return {**base_template, "imagen_settings": imagen_settings}


def get_anime_3d_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Anime 3D' style.

    Args:
        style_category (str): The specific style category (e.g., "anime_3d").

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Anime 3D Preset",
        "moods": ["Anime", "Cel Shaded", "Japanese Animation", "Stylized", "Vibrant"],
        "aspect_ratio": "16:9",
        "description": "A preset for 3D art in a Japanese Anime style, featuring cel shading, distinct outlines, and characteristic visual tropes."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Anime Style 3D / Cel Shading", "post_processing": ["strong outlines", "anime-style specular highlights", "color grading for anime look"], "style_era": "Modern Anime"},
        "lighting_settings": {"lighting_type": "Directional (Sun) + Rim lights + Area fills", "light_quality": "Hard Cel Shading Ramps / Soft stylized", "light_direction": "Key + Rim + Subtle Fill", "time_of_day": "Varied"},
        "composition_settings": {"technique": "Dynamic angles, character focus, rule of thirds", "focal_point": "Character eyes/face or key action", "camera_angle": "Varied, expressive (low, high, dutch)", "perspective": "Dynamic"},
        "color_settings": {"color_scheme": "Vibrant & Thematic (anime palettes)", "palette_type": "Saturated, specific character/scene palettes", "color_temperature": "Neutral to Cool", "color_contrast": "High", "dominant_colors": ["varied based on scene/character"]},
        "detail_settings": {"detail_level": "Medium (stylized forms, clean lines)", "texture_quality": "Flat Colors, Simple Gradients, Stylized (e.g., painted details for clothes, hair strands)"},
        "environment_settings": {"weather": "Varied (matching scene mood)", "season": "Varied", "location_type": "Anime-style environments (city, school, fantasy)", "atmospheric_effects": ["stylized speed lines", "lens flares", "sakura petals"]},
        "quality_settings": {"resolution": "1920x1080 or 2560x1440", "rendering_quality": "High"},
        "negative_prompt": "photorealistic, western cartoon, realistic textures, soft shading, complex PBR materials, gritty, overly detailed, messy lines, bad anatomy (unless stylized)",
        "style_negative_prompt": "realistic lighting, subtle details, non-anime proportions, muddy colors, overly complex geometry"
    }
    imagen_settings["software_settings"] = {
        "suite": "Blender (Eevee with Shader Nodes), Maya (with Toon shaders), Unity/Unreal (with NPR shaders)", "renderer": "Eevee, specialized anime NPR renderers", "version": "Latest"
    }
    imagen_settings["render_settings"] = {
        "polycount": "Medium (optimized for style)", "sampling": "128-512 samples", "denoiser": "Enabled",
        "resolution": "1920x1080", "aspect_ratio": "16:9", "frame_number": "1"
    }
    imagen_settings["lighting_setup"] = {
        "system": "Key light (sun/spot), Fill light (area/hemi), Rim light (spot/directional)", "intensity": "Strong key, subtle fill, pronounced rim",
        "color": "White key, thematic fill/rim", "shadows": "crisp cel shadows, minimal ambient occlusion"
    }
    imagen_settings["material_settings"] = {
        "shader_type": "Toon BSDF with custom ramps, Emission for effects, specialized hair/eye shaders", "subsurface_scattering": "minimal for skin (stylized)",
        "texture_maps": ["diffuse (flat/gradient/stylized)", "specular map (anime highlights)", "outline mask"],
        "outlines_settings": {"method": "Freestyle, Inverted Hull, or advanced post-processing Sobel filter", "thickness": "1.0-2.5px", "color": "dark contrasting (often black or near-black)"},
        "hair_shader_specifics": {"type": "Kajiya-Kay based or similar, with banded specular highlights", "base_color": "character specific", "highlight_color": "lighter shade or white"}
    }
    imagen_settings["camera_settings"] = get_dynamic_camera_settings(style_category)
    return {**base_template, "imagen_settings": imagen_settings}


def get_abstract_3d_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Abstract 3D' style.

    Args:
        style_category (str): The specific style category (e.g., "abstract_3d").

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Abstract 3D Preset",
        "moods": ["Conceptual", "Geometric Abstract", "Organic Abstract", "Experimental", "Surreal", "Minimalist", "Complex"],
        "aspect_ratio": "16:9", # Or "1:1", "4:5" for artistic pieces
        "description": "A preset for abstract 3D art, focusing on non-representational forms, experimental lighting, and unique material compositions."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Abstract Digital Art / Generative Art / Non-representational", "post_processing": ["color grading", "depth effects (DoF, fog)", "glow/bloom for emissives", "film grain (optional)"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Experimental (emissive materials, volumetric, spotlights, HDRI with strong colors)", "light_quality": "Varied (hard, soft, colored, textured)", "light_direction": "Unconventional, dramatic, to create form and mood", "time_of_day": "N/A"},
        "composition_settings": {"technique": "Rule of Thirds (loosely), Golden Ratio, Dynamic Symmetry, Centered, Asymmetrical Balance, or purely intuitive/generative", "focal_point": "Key visual element, overall flow, or negative space", "camera_angle": "Unusual, macro, wide, or distorted", "perspective": "Varied"},
        "color_settings": {"color_scheme": "Monochromatic, Analogous, Complementary, Triadic, Custom Experimental", "palette_type": "Bold, Muted, Gradient-based, Metallic, Iridescent", "color_temperature": "Varied (warm, cool, mixed)", "color_contrast": "Varied (low to high)", "dominant_colors": ["user-defined or procedurally generated"]},
        "detail_settings": {"detail_level": "Varied (can be minimal with simple forms or highly complex with intricate details/fractals)", "texture_quality": "Procedural (noise, voronoi), Metallic, Glass, Emissive, Matte, Glossy, or Simple Diffuse"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Abstract Space, Infinite Void, Studio", "atmospheric_effects": ["volumetric fog/light", "particle systems", "abstract refractions"]},
        "quality_settings": {"resolution": "1920x1080 up to 4K+", "rendering_quality": "High to Very High"},
        "negative_prompt": "representational, figurative, realistic scene, character, landscape, product shot, symmetrical (unless intended as core concept), recognizable objects (unless abstracted)",
        "style_negative_prompt": "boring composition, flat lighting (unless intentional for minimalism), standard PBR materials (unless used abstractly), predictable forms"
    }
    imagen_settings["software_settings"] = {
        "suite": "Blender (Geometry Nodes, Cycles/Eevee), Houdini, Cinema 4D (MoGraph), TouchDesigner", "renderer": "Cycles, Eevee, Octane, Redshift, Arnold", "version": "Latest"
    }
    imagen_settings["render_settings"] = {
        "polycount": "Varied (low for geometric, high for organic/fractal)", "sampling": "High (e.g., 512-2048+ samples for Cycles)", "denoiser": "Enabled (OptiX/OIDN)",
        "resolution": "1920x1080", "aspect_ratio": "16:9", "frame_number": "1"
    }
    imagen_settings["lighting_setup"] = {
        "system": "HDRI, mesh lights, spotlights, emissive materials, volumetric lighting", "intensity": "Varied, often high contrast or subtle gradients",
        "color": "Monochromatic or full spectrum, often thematic", "shadows": "Sharp, soft, or non-existent (for unlit styles)"
    }
    imagen_settings["material_settings"] = {
        "shader_type": "Principled BSDF (for PBR abstract), Emission, Glass BSDF, Transparent BSDF, Velvet BSDF, Anisotropic BSDF, Volumetric shaders (absorption/scatter)",
        "subsurface_scattering": "Can be used for organic abstract effects",
        "texture_maps": ["procedural noise (musgrave, voronoi)", "gradients", "image textures for displacement/emission/alpha", "vertex colors"],
        "displacement": "Often used for complex geometric or organic forms"
    }
    imagen_settings["camera_settings"] = get_dynamic_camera_settings(style_category)
    return {**base_template, "imagen_settings": imagen_settings}


def get_wireframe_3d_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Wireframe 3D' style.

    Args:
        style_category (str): The specific style category (e.g., "wireframe_3d").

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Wireframe 3D Preset",
        "moods": ["Technical", "Blueprint", "Structural", "Minimalist", "Digital", "Schematic"],
        "aspect_ratio": "16:9",
        "description": "A preset for rendering 3D models in a wireframe style, showcasing their underlying geometry and topology."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Wireframe Display / Technical Illustration", "post_processing": ["optional glow on lines", "anti-aliasing for clean lines", "background contrast enhancement"], "style_era": "N/A"},
        "lighting_settings": {"lighting_type": "Flat Ambient or Unlit (lines are self-illuminated or base color)", "light_quality": "Even", "light_direction": "N/A", "time_of_day": "N/A"},
        "composition_settings": {"technique": "Clear object view (orthographic often preferred for technical, perspective for dynamic)", "focal_point": "Entire object structure", "camera_angle": "Standard views (front, side, top, iso) or dynamic", "perspective": "Orthographic or Perspective"},
        "color_settings": {"color_scheme": "Monochromatic (e.g., white/green/blue lines on black/dark background) or Thematic", "palette_type": "Single color for lines, optional subtle face colors if 'wire on shaded'", "color_temperature": "N/A", "color_contrast": "Very High (lines vs background)", "dominant_colors": ["line color, background color"]},
        "detail_settings": {"detail_level": "Edge/Vertex Level (shows all topology)", "texture_quality": "None (lines only, or simple flat face color if shaded)"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Neutral Background (solid color, gradient, or transparent)", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "1920x1080 or higher for print", "rendering_quality": "High (for clean lines)"},
        "negative_prompt": "fully shaded, textured surfaces, realistic materials, rendered scene details, raster graphics, painting, complex lighting, shadows",
        "style_negative_prompt": "filled polygons (unless 'wireframe on shaded' with transparency), textures, PBR materials, complex lighting, photographic realism"
    }
    imagen_settings["software_settings"] = {
        "suite": "Blender, Maya, 3ds Max, Cinema 4D, Houdini", "renderer": "Viewport Render (OpenGL/DirectX), Eevee/Cycles (wireframe node/modifier, Freestyle), Arnold (aiWireframe)", "version": "Latest"
    }
    imagen_settings["render_settings"] = {
        "polycount": "N/A (shows existing polys)", "sampling": "Low (e.g., 1-64 samples, as shading is minimal)", "denoiser": "Usually not needed",
        "resolution": "1920x1080", "aspect_ratio": "16:9", "frame_number": "1"
    }
    imagen_settings["lighting_setup"] = { # Less relevant for pure wireframe, more for 'wire on shaded'
        "system": "Ambient light or unlit material for lines", "intensity": "N/A for unlit",
        "color": "N/A for unlit", "shadows": "none for pure wireframe"
    }
    imagen_settings["material_settings"] = { # Focuses on how wires are displayed
        "shader_type": "Emission (for self-illuminated lines), Diffuse (for line color if lit), or specialized Wireframe Shader Node/Material",
        "wireframe_options": {
            "line_thickness": "0.5-2.0 pixels (screen space) or world units",
            "line_color": "User-defined (e.g., white, green, blue, black)",
            "face_visibility": "Hidden, Transparent, or Solid Flat Color (for 'wire on shaded')",
            "face_color": "Dark contrasting color or transparent if faces shown",
            "vertex_dots": "Optional, small dots at vertices",
            "crease_threshold": "Show only sharp edges (optional)"
        },
        "background_options": {"color": "Solid (e.g., black, dark grey) or Transparent (for compositing)"}
    }
    imagen_settings["camera_settings"] = get_dynamic_camera_settings(style_category)
    return {**base_template, "imagen_settings": imagen_settings}


def get_clay_render_3d_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Clay Render 3D' style.

    Args:
        style_category (str): The specific style category (e.g., "clay_render_3d").

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Clay Render 3D Preset",
        "moods": ["Neutral", "Draft", "Sculptural", "Monochromatic", "Work-in-progress", "Clean", "Minimalist"],
        "aspect_ratio": "16:9",
        "description": "A preset for a clay render style, typically used for model previews, showcasing form with a simple, uniform clay-like material."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Clay Render / Sculpt Preview / Maquette Style", "post_processing": ["subtle ambient occlusion pass (optional)", "depth of field (optional for focus)", "vignette (subtle)"], "style_era": "N/A"},
        "lighting_settings": {"lighting_type": "Studio (3-point, HDRI, or dome light)", "light_quality": "Soft Diffused (to show form without harshness)", "light_direction": "Key + Fill + Rim (classic setup)", "time_of_day": "N/A"},
        "composition_settings": {"technique": "Turntable view, posed model, centered subject, rule of thirds", "focal_point": "Overall model form and sculptural detail", "camera_angle": "Slightly low or eye-level to give presence", "perspective": "Perspective"},
        "color_settings": {"color_scheme": "Monochromatic (grey, beige, terracotta, off-white)", "palette_type": "Single clay color, or subtle variations", "color_temperature": "Neutral or slightly warm", "color_contrast": "Medium (form defined by light/shadow)", "dominant_colors": ["chosen clay color"]},
        "detail_settings": {"detail_level": "Matches model's sculpted detail", "texture_quality": "Uniform Clay (no specific texture maps, just base material properties)"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Studio Background (infinite cyclorama, simple plane, gradient)", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "1920x1080 or higher", "rendering_quality": "Good to High (for smooth AO and shadows)"},
        "negative_prompt": "textured surfaces, colored PBR materials, final render look, vibrant colors, patterns, decals, metallic, glass, emissive materials, busy background",
        "style_negative_prompt": "complex materials, reflections (unless very subtle and diffuse), strong colors, distracting textures, overly dark or flat lighting"
    }
    imagen_settings["software_settings"] = {
        "suite": "Blender, ZBrush (with BPR), Maya, Keyshot, Marmoset Toolbag", "renderer": "Cycles, Eevee, Arnold, Keyshot, Redshift", "version": "Latest"
    }
    imagen_settings["render_settings"] = {
        "polycount": "Matches model (can be high for sculpts)", "sampling": "Medium to High (e.g., 256-1024 samples for Cycles)", "denoiser": "Enabled",
        "resolution": "1920x1080", "aspect_ratio": "16:9", "frame_number": "1"
    }
    imagen_settings["lighting_setup"] = {
        "system": "Classic 3-point lighting (Key, Fill, Rim), or HDRI with softbox emulation", "intensity": "Balanced to reveal form",
        "color": "Neutral white lights", "shadows": "Soft, diffused contact shadows, ambient occlusion is key"
    }
    imagen_settings["material_settings"] = {
        "shader_type": "Diffuse BSDF or Principled BSDF (simplified)",
        "material_properties": {
            "base_color": "Light grey (e.g., RGB 0.7, 0.7, 0.7), Beige, or Terracotta",
            "metallic": "0.0",
            "specular": "0.2-0.5 (for slight sheen)",
            "roughness": "0.6-0.8 (matte to slightly satin)",
            "subsurface_scattering": "0.0 (or very minimal for some clay types)",
            "clearcoat": "0.0"
        },
        "texture_maps": ["none (or a very subtle procedural noise/fingerprints for added realism if desired, but typically clean)"],
        "ambient_occlusion": {"distance": "0.1-0.5m (scene scale dependent)", "factor": "0.5-1.0"}
    }
    imagen_settings["camera_settings"] = get_dynamic_camera_settings(style_category)
    return {**base_template, "imagen_settings": imagen_settings}


def get_low_poly_3d_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Low Poly 3D' style.

    Args:
        style_category (str): The specific style category (e.g., "low_poly_3d").

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Low Poly 3D Preset",
        "moods": ["Stylized", "Geometric", "Minimalist", "Retro", "Clean"],
        "aspect_ratio": "16:9",
        "description": "A preset for low polygon 3D art, featuring simplified geometric shapes and often flat or simple gradient shading."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Low Poly Style", "post_processing": ["sharp edges", "flat shading look (optional)"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Simple Directional, Ambient, or Studio", "light_quality": "Flat, Soft, or Stylized Hard", "light_direction": "Varied", "time_of_day": "Varied"},
        "composition_settings": {"technique": "Rule of Thirds, Centered, or Dynamic", "focal_point": "Main Subject", "camera_angle": "Varied", "perspective": "One-point or Two-point"},
        "color_settings": {"color_scheme": "Analogous, Monochromatic, or Contrasting", "palette_type": "Flat Colors or Simple Gradients", "color_temperature": "Neutral or Thematic", "color_contrast": "Medium to High", "dominant_colors": ["varied based on theme"]},
        "detail_settings": {"detail_level": "Low (faceted)", "texture_quality": "Flat Colors, Simple Gradients, or Minimal Textures"},
        "environment_settings": {"weather": "Varied or N/A", "season": "Varied or N/A", "location_type": "Abstract, Stylized Scene, or Studio", "atmospheric_effects": ["none or subtle stylized fog"]},
        "quality_settings": {"resolution": "1920x1080 or 2560x1440", "rendering_quality": "Good"},
        "negative_prompt": "photorealistic, complex textures, high poly count, detailed sculpting, intricate details, ray tracing realism, excessive noise, blurry",
        "style_negative_prompt": "hyperrealism, excessive surface detail, complex PBR shaders, photoreal lighting"
    }
    imagen_settings["software_settings"] = {
        "suite": "Blender, Maya, Cinema 4D", "renderer": "Eevee, Cycles (with flat/smooth shading as per sub-style), Arnold (toon)", "version": "Latest"
    }
    imagen_settings["render_settings"] = {
        "polycount": "low polygon count (e.g., 500-20,000 polys)", "sampling": "Low to Medium (e.g., 128-512 samples)", "denoiser": "Enabled if needed",
        "resolution": "1920x1080", "aspect_ratio": "16:9", "frame_number": "1"
    }
    imagen_settings["lighting_setup"] = {
        "system": "Simple sun lamp, area lights, or HDRI (stylized)", "intensity": "Varied",
        "color": "White or Thematic", "shadows": "simple hard or soft shadows"
    }
    imagen_settings["material_settings"] = {
        "shader_type": "Diffuse BSDF, Principled BSDF (simplified), Emission, or Toon BSDF (optional)", "subsurface_scattering": "0",
        "texture_maps": ["diffuse (solid/gradient)"], "bump_map": "no", "displacement": "no"
    }
    imagen_settings["camera_settings"] = get_dynamic_camera_settings(style_category)
    return {**base_template, "imagen_settings": imagen_settings}


def get_cartoon_3d_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Cartoon 3D' (Toon Shaded) style.

    Args:
        style_category (str): The specific style category (e.g., "cartoon_3d").

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Cartoon 3D Preset",
        "moods": ["Stylized", "Animated", "Playful", "Cel Shaded", "Fun"],
        "aspect_ratio": "16:9",
        "description": "A preset for cartoonish 3D art, often featuring cel shading, outlines, and expressive forms."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Toon Shading / Cartoon Style", "post_processing": ["outlines (Freestyle/inverted hull)", "cel shading effect"], "style_era": "Contemporary / Classic Animation"},
        "lighting_settings": {"lighting_type": "Directional (Sun lamp) for hard shadows, Rim lighting", "light_quality": "Hard or Banded (cel shaded)", "light_direction": "Key light emphasis, rim light", "time_of_day": "Varied"},
        "composition_settings": {"technique": "Dynamic Poses, Clear Silhouettes", "focal_point": "Character or Main Action", "camera_angle": "Varied, expressive", "perspective": "One-point or Dynamic"},
        "color_settings": {"color_scheme": "Vibrant, Contrasting, or Thematic", "palette_type": "Saturated Colors, Limited Palette per character/scene", "color_temperature": "Neutral or Warm", "color_contrast": "High", "dominant_colors": ["varied based on theme"]},
        "detail_settings": {"detail_level": "Medium (stylized forms, not overly complex)", "texture_quality": "Flat Colors, Stylized Textures, Hand-painted look (optional)"},
        "environment_settings": {"weather": "Varied or N/A", "season": "Varied or N/A", "location_type": "Stylized Scene, Abstract Background", "atmospheric_effects": ["none or stylized (e.g., speed lines)"]},
        "quality_settings": {"resolution": "1920x1080 or 2560x1440", "rendering_quality": "Good"},
        "negative_prompt": "photorealistic shading, complex realistic textures, soft shadows (unless stylized), ray traced global illumination, gritty realism, excessive detail",
        "style_negative_prompt": "realistic rendering, subtle lighting, photographic look, PBR materials, complex shaders (unless for specific effect)"
    }
    imagen_settings["software_settings"] = {
        "suite": "Blender, Maya, Toon Boom (for 2D/3D mix)", "renderer": "Eevee (with Toon BSDF), Blender Render (classic Freestyle), specialized toon renderers", "version": "Latest"
    }
    imagen_settings["render_settings"] = {
        "polycount": "medium polygon count (optimized for animation)", "sampling": "Medium (e.g., 128-512 samples)", "denoiser": "Enabled if needed",
        "resolution": "1920x1080", "aspect_ratio": "16:9", "frame_number": "1 (or sequence for animation)"
    }
    imagen_settings["lighting_setup"] = {
        "system": "Key light (sun/spot), Fill light (area/hemi), Rim light (spot)", "intensity": "Varied, strong key light",
        "color": "White or Thematic", "shadows": "hard cel shadows, stylized shadow shapes"
    }
    imagen_settings["material_settings"] = {
        "shader_type": "Toon BSDF, Shader to RGB for custom ramps, Emission (for effects)", "subsurface_scattering": "minimal or none",
        "texture_maps": ["diffuse (flat/stylized colors)", "specular map (stylized highlights)"], "bump_map": "minimal or stylized", "displacement": "no",
        "outlines_settings": {"method": "Freestyle, Inverted Hull, or Post-processing Sobel filter", "thickness": "varied (e.g., 1-3px)", "color": "black or dark contrasting color"}
    }
    imagen_settings["camera_settings"] = get_dynamic_camera_settings(style_category)
    return {**base_template, "imagen_settings": imagen_settings}
