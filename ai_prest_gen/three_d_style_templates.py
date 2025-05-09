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


def get_voxel_art_template(style_category: str) -> Dict[str, Any]:
    """Generates a preset template for Voxel Art style."""
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


def get_anime_3d_template(style_category: str) -> Dict[str, Any]:
    """Generates a preset template for Anime 3D style."""
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
    """Generates a preset template for Abstract 3D style."""
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
    """Generates a preset template for Wireframe 3D style."""
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
    """Generates a preset template for Clay Render 3D style."""
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
    """Generates a preset template for Low Poly 3D style."""
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
    """Generates a preset template for Cartoon 3D / Toon Shaded style."""
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
