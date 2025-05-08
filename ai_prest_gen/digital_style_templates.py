#!/usr/bin/env python3
"""
Digital Style Templates for AI Preset Generator

This module contains template functions for digital art styles, including:
- Digital painting
- Digital art (general)
- 3D render
- Vector art
- ASCII art
- Isometric art
- Game-style art
- Pixel art
- And other digital-related styles

Each function returns a dictionary with preset settings optimized for the given style.
"""

from typing import Dict, Any


def get_digital_art_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Digital Art Preset",
        "moods": ["Expressive", "Dynamic"],
        "aspect_ratio": "16:9",
        "description": "A general preset for digital art, focusing on expressive and dynamic visuals."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Contemporary Digital Art", "post_processing": ["color grading", "sharpening"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Varied", "light_quality": "Varied", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Dynamic composition", "focal_point": "Main Subject"},
        "color_settings": {"color_scheme": "Varied", "palette_type": "Balanced Expressive Palette", "color_temperature": "Mixed", "color_contrast": "High"},
        "detail_settings": {"detail_level": "High", "texture_quality": "Digital textures"},
        "environment_settings": {"weather": "Varied", "season": "Varied", "location_type": "Varied", "atmospheric_effects": ["varied"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High Polished"},
        "negative_prompt": "traditional art, low detail, signature, watermark, low quality",
        "style_negative_prompt": "unblended styles, flat colors"
    }
    imagen_settings["digital_settings"] = {
        "software": "Photoshop", "rendering_technique": "digital painting with photo elements",
        "digital_effects": ["glow effects", "texture overlays", "layer masks"], "resolution": "4K",
        "filter_usage": ["Gaussian blur for depth", "color dodge for highlights"], "brush_type": "custom textured brushes",
        "layer_complexity": "complex with multiple adjustment layers"
    }
    return {**base_template, "imagen_settings": imagen_settings}


def get_digital_painting_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Digital Painting Preset",
        "moods": ["Painterly", "Digital"],
        "aspect_ratio": "16:9",
        "description": "A preset for digital painting style, focusing on painterly techniques using digital tools."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Digital Painting", "post_processing": ["digital brushwork"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Atmospheric Digital", "light_quality": "Varied", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Painterly composition", "focal_point": "Main Subject"},
        "color_settings": {"color_scheme": "Varied", "palette_type": "Full color range with digital blending", "color_temperature": "Mixed", "color_contrast": "Medium"},
        "detail_settings": {"detail_level": "High", "texture_quality": "Custom digital brush textures"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Abstract", "atmospheric_effects": ["digital glow"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "traditional painting, lack of digital effects, signature, watermark, low quality",
        "style_negative_prompt": "unblended colors, flat lighting"
    }
    imagen_settings["digital_painting_settings"] = {
        "platform": "Photoshop/Procreate/Krita",
        "brushwork": "simulated paint brush strokes with opacity layering", "effect_blend": ["texture overlays", "color dodge/glow effects"],
        "aesthetic_blend": "Traditional painting appearance achieved through digital tools, often with enhanced lighting or effects."
    }
    return {**base_template, "imagen_settings": imagen_settings}


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
    imagen_settings["composition_settings"]["view_mode"] = "standard perspective view"
    imagen_settings["style_settings"]["post_processing"] = ["bloom effect", "vignette", "color grading (filmic LUT)"]
    return {**base_template, "imagen_settings": imagen_settings}


def get_vector_art_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Vector Art Preset",
        "moods": ["Clean", "Modern", "Graphic"],
        "aspect_ratio": "16:9",
        "description": "A preset for vector art, focusing on clean lines, flat colors, and scalable graphics."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Vector Art / Graphic Design", "post_processing": ["clean edges"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Flat", "light_quality": "Even", "light_direction": "N/A"},
        "composition_settings": {"technique": "Clean geometric composition", "focal_point": "Main shape/form"},
        "color_settings": {"color_scheme": "Bright Graphic", "palette_type": "Limited clean colors", "color_temperature": "Varied", "color_contrast": "High"},
        "detail_settings": {"detail_level": "Medium", "texture_quality": "Smooth vector texture"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Abstract", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "Crisp edges"},
        "negative_prompt": "noisy, sketchy, grainy, textured, brushstrokes, signature, watermark, low quality",
        "style_negative_prompt": "handdrawn look, traditional media"
    }
    imagen_settings["vector_settings"] = {
        "software": "Adobe Illustrator/Inkscape",
        "line_quality": "clean crisp paths with perfect curves",
        "fill_type": "flat color fills or simple gradients",
        "design_elements": ["geometric shapes", "clean icons", "precise curves"],
        "aesthetic_blend": "Modern graphic design with mathematically precise paths, sharp edges, and unlimited scalability."
    }
    return {**base_template, "imagen_settings": imagen_settings}


def get_ascii_art_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "ASCII Art Preset",
        "moods": ["Retro", "Digital"],
        "aspect_ratio": "4:3",
        "description": "A general preset for ASCII art, using text characters to form images."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "ASCII Art", "post_processing": ["character mosaic"], "style_era": "Retro"},
        "lighting_settings": {"lighting_type": "Flat", "light_quality": "Hard-edged", "light_direction": "Top"},
        "composition_settings": {"technique": "Grid-based mosaic composition", "focal_point": "Image formed by characters"},
        "color_settings": {"color_scheme": "Monochrome", "palette_type": "monochrome green on black", "color_temperature": "Cool", "color_contrast": "High"},
        "detail_settings": {"detail_level": "Medium", "texture_quality": "ASCII character texture"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Console Terminal", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "1280x720", "rendering_quality": "Retro Digital"},
        "negative_prompt": "realism, full-color photography, smooth gradient, signature, watermark, low quality",
        "style_negative_prompt": "natural photo, smooth curves"
    }
    imagen_settings["ascii_art_settings"] = {
        "character_set": "full ASCII character set", "resolution": "medium character resolution",
        "mosaic_density": "dense character placement", "contrast_method": "symbol value mix for shading",
        "aesthetic_blend": "Text-based art using ASCII characters to form recognizable images, retro computer aesthetic."
    }
    return {**base_template, "imagen_settings": imagen_settings}


def get_isometric_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Isometric Preset",
        "moods": ["Geometric", "Structured"],
        "aspect_ratio": "1:1",
        "description": "A preset for Isometric art, focusing on a 30-degree view and geometric composition."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Isometric Art", "post_processing": ["flat shading"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Simple Directional", "light_quality": "Flat", "light_direction": "Top-down"},
        "composition_settings": {"technique": "Isometric grid-based composition", "focal_point": "Objects", "perspective": "Isometric (No vanishing point)"},
        "color_settings": {"color_scheme": "Pastel Muted", "palette_type": "pastel muted color scheme", "color_temperature": "Neutral", "color_contrast": "Medium"},
        "detail_settings": {"detail_level": "Medium", "texture_quality": "Clean flat surfaces"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Abstract Grid", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "2048x2048", "rendering_quality": "Clean Graphic"},
        "negative_prompt": "perspective distortion, realistic shading, signature, watermark, low quality",
        "style_negative_prompt": "non-isometric view, complex textures"
    }
    imagen_settings["isometric_settings"] = {
        "view_angle": "30 degrees standard isometric", "object_arrangement": "organized stacked layered objects",
        "color_palette": "pastel muted color scheme", "detail_level": "medium detail clean lines"
    }
    return {**base_template, "imagen_settings": imagen_settings}


def get_game_style_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Game Style Preset",
        "moods": ["Epic", "Adventurous", "Immersive"],
        "aspect_ratio": "16:9",
        "description": "A general preset for modern game concept art, focusing on dynamic composition and high detail."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Modern Game Concept Art", "post_processing": ["cinematic LUT"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Dynamic Real-time", "light_quality": "Varied", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Dynamic composition for games", "focal_point": "Main Subject"},
        "color_settings": {"color_scheme": "Varied", "palette_type": "Realistic or Stylized Game Palette", "color_temperature": "Mixed", "color_contrast": "High"},
        "detail_settings": {"detail_level": "High", "texture_quality": "High polygon count models"},
        "environment_settings": {"weather": "Varied", "season": "Varied", "location_type": "Game Environment", "atmospheric_effects": ["volumetric lighting"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High Quality Game Engine Render (Unreal Engine 5)"},
        "negative_prompt": "low detail, flat lighting, signature, watermark, low quality",
        "style_negative_prompt": "static composition, unrealistic rendering"
    }
    imagen_settings["game_engine_settings"] = {
        "engine_type": "Unreal Engine 5", "render_quality": "high cinematic quality",
        "shader_type": "Physically Based Rendering (PBR)", "special_effects": ["bloom", "ambient occlusion", "volumetric lighting"],
        "post_effects": ["depth of field", "color grading (cinematic LUT)"], "resolution": "4K (3840x2160)",
        "physics_settings": ["realistic physics simulation"], "animation_style": "smooth realistic character animation"
    }
    imagen_settings["game_settings"] = {
        "interactivity": "high interactivity implied", "environment_type": "detailed outdoor fantasy environment",
        "character_style": "realistic stylized characters", "lighting_type": "dynamic real-time lighting"
    }
    return {**base_template, "imagen_settings": imagen_settings}


def get_pixel_art_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Pixel Art Preset",
        "moods": ["Retro", "Nostalgic", "Graphic"],
        "aspect_ratio": "1:1",
        "description": "A preset for pixel art, focusing on low-resolution aesthetics with deliberately visible pixels."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Pixel Art", "post_processing": ["pixelation"], "style_era": "Retro"},
        "lighting_settings": {"lighting_type": "Simplified", "light_quality": "Highly limited", "light_direction": "Simplified"},
        "composition_settings": {"technique": "Grid-based pixel composition", "focal_point": "Character or scene"},
        "color_settings": {"color_scheme": "Limited Palette", "palette_type": "Limited color palette (8-32 colors)", "color_temperature": "Varied", "color_contrast": "High"},
        "detail_settings": {"detail_level": "Low (by design)", "texture_quality": "Deliberate pixel texture"},
        "environment_settings": {"weather": "Simplified", "season": "Simplified", "location_type": "Game Scene", "atmospheric_effects": ["minimal"]},
        "quality_settings": {"resolution": "Low (scaled up)", "rendering_quality": "Pixel Perfect"},
        "negative_prompt": "high resolution, smooth edges, gradient, blurry, signature, watermark, low quality",
        "style_negative_prompt": "anti-aliasing, high resolution details"
    }
    imagen_settings["pixel_art_settings"] = {
        "resolution": "low base resolution scaled up",
        "color_count": "limited palette (8-32 colors)",
        "pixel_technique": "precise pixel placement with no anti-aliasing",
        "shading_method": "limited color dithering for gradients",
        "aesthetic_blend": "Deliberately low-resolution art with carefully placed individual pixels, emulating classic video game style."
    }
    return {**base_template, "imagen_settings": imagen_settings}


def get_vaporwave_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Vaporwave Preset",
        "moods": ["Nostalgic", "Surreal", "Retro-futuristic"],
        "aspect_ratio": "16:9",
        "description": "A preset for Vaporwave aesthetics, focusing on 80s-90s nostalgia, glitch effects, and surreal juxtapositions."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Vaporwave", "post_processing": ["glitch effects", "VHS artifacts"], "style_era": "1980s-90s Nostalgia"},
        "lighting_settings": {"lighting_type": "Neon Glow", "light_quality": "Diffused", "light_direction": "Multiple sources"},
        "composition_settings": {"technique": "Surreal retro composition", "focal_point": "Nostalgic elements"},
        "color_settings": {"color_scheme": "Pastel and Neon", "palette_type": "Pink, purple, blue, teal pastel palette", "color_temperature": "Cool", "color_contrast": "Medium"},
        "detail_settings": {"detail_level": "Medium", "texture_quality": "Digital glitch textures"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Digital Landscape", "atmospheric_effects": ["digital haze"]},
        "quality_settings": {"resolution": "1920x1080", "rendering_quality": "Intentional digital artifacts"},
        "negative_prompt": "modern, realistic, sharp detail, signature, watermark, low quality",
        "style_negative_prompt": "natural lighting, realistic environment"
    }
    imagen_settings["vaporwave_settings"] = {
        "nostalgic_elements": ["80s-90s technology", "classical statues", "tropical/palm imagery", "grid patterns"],
        "digital_effects": ["VHS artifacts", "glitch effects", "CRT scanlines", "low resolution"],
        "typography": "kanji/katakana characters, Windows 95 aesthetics",
        "aesthetic_blend": "Dreamlike retro-futuristic aesthetic combining 80s-90s nostalgia with digital artifacts and surreal elements."
    }
    return {**base_template, "imagen_settings": imagen_settings}


def get_glitch_art_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Glitch Art Preset",
        "moods": ["Distorted", "Digital", "Chaotic"],
        "aspect_ratio": "16:9",
        "description": "A preset for Glitch Art, focusing on digital errors, corruption, and data manipulation."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Glitch Art", "post_processing": ["data corruption effects"], "style_era": "Digital"},
        "lighting_settings": {"lighting_type": "Corrupted", "light_quality": "Distorted", "light_direction": "Glitched"},
        "composition_settings": {"technique": "Digital corruption composition", "focal_point": "Glitch effects"},
        "color_settings": {"color_scheme": "RGB Splits", "palette_type": "RGB channel splits and corrupted data colors", "color_temperature": "Varied", "color_contrast": "High"},
        "detail_settings": {"detail_level": "Varied", "texture_quality": "Digital noise and artifacts"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Digital", "atmospheric_effects": ["corruption"]},
        "quality_settings": {"resolution": "1920x1080", "rendering_quality": "Deliberately corrupted"},
        "negative_prompt": "clean, error-free, orderly, signature, watermark, low quality",
        "style_negative_prompt": "realistic rendering, smooth gradients"
    }
    imagen_settings["glitch_art_settings"] = {
        "glitch_techniques": ["datamoshing", "pixel sorting", "RGB splitting", "binary manipulation"],
        "corruption_level": "medium to heavy digital corruption",
        "artifacts": ["JPEG artifacts", "scan lines", "visual noise", "tearing"],
        "base_image": "partially recognizable corrupted base image",
        "aesthetic_blend": "The aesthetics of digital errors and data corruption turned into artistic expression."
    }
    return {**base_template, "imagen_settings": imagen_settings}


def get_surrealism_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Surrealism Preset",
        "moods": ["Dreamlike", "Uncanny", "Mysterious"],
        "aspect_ratio": "16:9",
        "description": "A preset for Surrealism, focusing on dreamlike illogical juxtapositions and scenes."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Surrealism", "post_processing": ["dreamlike effects"], "style_era": "Modern"},
        "lighting_settings": {"lighting_type": "Dramatic Mysterious", "light_quality": "Chiaroscuro", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Illogical juxtaposition", "focal_point": "Unexpected elements"},
        "color_settings": {"color_scheme": "Varied", "palette_type": "Varied, often Muted or Symbolic Palette", "color_temperature": "Mixed", "color_contrast": "Medium"},
        "detail_settings": {"detail_level": "High", "texture_quality": "Realistic on unreal subjects"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Dreamscape", "atmospheric_effects": ["mist", "shadows"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "realistic, logical, mundane, signature, watermark, low quality",
        "style_negative_prompt": "predictable composition, flat lighting"
    }
    imagen_settings["surrealism_settings"] = {
        "conceptual_approach": "dreamlike bizarre unexpected juxtapositions", "color_scheme": "muted contrasting symbolic colors",
        "composition": "layered symbolic narrative structure", "mood": "mysterious uncanny thought-provoking"
    }
    return {**base_template, "imagen_settings": imagen_settings}


def get_cubism_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Cubism Preset",
        "moods": ["Analytical", "Geometric", "Abstract"],
        "aspect_ratio": "16:9",
        "description": "A preset for Cubism, focusing on fragmented forms and multiple viewpoints."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Cubism", "post_processing": ["geometric fragmentation"], "style_era": "Modern"},
        "lighting_settings": {"lighting_type": "Simplified Abstracted", "light_quality": "Geometric", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Fragmented forms multiple viewpoints", "focal_point": "Subject"},
        "color_settings": {"color_scheme": "Muted Earthy", "palette_type": "Muted Earthy Tones or Later Bolder Colors", "color_temperature": "Neutral", "color_contrast": "Medium"},
        "detail_settings": {"detail_level": "Medium", "texture_quality": "Geometric planes flat or textured"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Abstract", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "realistic, smooth, organic, signature, watermark, low quality",
        "style_negative_prompt": "blended forms, soft edges"
    }
    imagen_settings["cubism_settings"] = {
        "form_style": "angular fragmented multiple perspectives", "color_palette": "muted earthy tones with bold geometric accents",
        "composition": "geometric abstraction layered planes",
        "aesthetic_blend": "Classic Cubist style with geometric fragmentation and abstract representation."
    }
    return {**base_template, "imagen_settings": imagen_settings}


def get_minimalist_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Minimalist Preset",
        "moods": ["Calm", "Clean", "Simple"],
        "aspect_ratio": "16:9",
        "description": "A preset for Minimalism, focusing on extreme simplicity and negative space."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Minimalism", "post_processing": ["flat color"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Flat Even", "light_quality": "Minimal shadows", "light_direction": "Top"},
        "composition_settings": {"technique": "Extreme simplicity and negative space", "focal_point": "Negative space"},
        "color_settings": {"color_scheme": "Neutral Monochrome", "palette_type": "Neutral Monochrome Palette", "color_temperature": "Neutral", "color_contrast": "High"},
        "detail_settings": {"detail_level": "Very Low", "texture_quality": "Smooth"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Abstract", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "Clean Graphic"},
        "negative_prompt": "high detail, complex, organic, signature, watermark, low quality",
        "style_negative_prompt": "busy composition, varied colors"
    }
    imagen_settings["minimalist_settings"] = {
        "simplicity_level": "extreme simplicity", "geometric_elements": ["lines", "simple squares"],
        "negative_space": "abundant negative space", "line_type": "clean precise thin lines",
        "color_count": "monochrome or two colors", "composition_balance": "asymmetric balance"
    }
    return {**base_template, "imagen_settings": imagen_settings}


def get_sci_fi_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Sci-Fi Preset",
        "moods": ["Futuristic", "Exploratory", "Technological"],
        "aspect_ratio": "16:9",
        "description": "A general preset for Science Fiction concept art, focusing on futuristic scenes."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Science Fiction Concept Art", "post_processing": ["lens flares"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Artificial or Alien World", "light_quality": "Varied", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Futuristic scene composition", "focal_point": "Technology or Environment"},
        "color_settings": {"color_scheme": "Varied", "palette_type": "Varied Sci-Fi Palette (can be gritty or clean)", "color_temperature": "Mixed", "color_contrast": "High"},
        "detail_settings": {"detail_level": "High", "texture_quality": "Metallic and Digital Textures"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Spaceship Interior or Alien Planet", "atmospheric_effects": ["space dust", "nebulae"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "organic, low detail, signature, watermark, low quality",
        "style_negative_prompt": "traditional art, realistic environment"
    }
    imagen_settings["sci_fi_settings"] = {
        "technology_level": "advanced futuristic technology", "environment": "space station interior or alien landscape",
        "lighting": "artificial cold lighting with lens flares", "color_palette": "metallic blues silvers with warning lights",
        "aesthetic_blend": "Clean futuristic design with elements of space exploration or advanced technology."
    }
    return {**base_template, "imagen_settings": imagen_settings}


def get_steampunk_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Steampunk Preset",
        "moods": ["Adventurous", "Mechanical", "Nostalgic"],
        "aspect_ratio": "16:9",
        "description": "A general preset for Steampunk, focusing on Victorian industrial retro-futurism."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Steampunk", "post_processing": ["aged metal effects"], "style_era": "Victorian Retro-Futuristic"},
        "lighting_settings": {"lighting_type": "Warm Ambient Gaslight", "light_quality": "Soft Glow", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Victorian industrial scene", "focal_point": "Mechanical elements"},
        "color_settings": {"color_scheme": "Sepia Tones", "palette_type": "sepia tones bronze browns deep reds", "color_temperature": "Warm", "color_contrast": "Medium"},
        "detail_settings": {"detail_level": "High", "texture_quality": "aged metal wood leather textures"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Victorian Cityscape or Airship Interior", "atmospheric_effects": ["steam", "gears"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "modern technology, clean lines, signature, watermark, low quality",
        "style_negative_prompt": "smooth textures, bright colors"
    }
    imagen_settings["steampunk_settings"] = {
        "technology_style": "Victorian industrial retro-futuristic", "materials": ["brass", "copper", "leather", "wood", "glass"],
        "mechanical_elements": ["gears", "steam pipes", "clockwork mechanisms", "goggles"],
        "color_palette": "sepia tones bronze browns deep reds",
        "aesthetic_blend": "Industrial Victorian era fused with imaginative steam-powered technology and intricate mechanical motifs."
    }
    return {**base_template, "imagen_settings": imagen_settings}


def get_papercraft_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Papercraft Preset",
        "moods": ["Crafted", "Textured"],
        "aspect_ratio": "1:1",
        "description": "A general preset for papercraft art, focusing on layered cut paper."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Paper Art", "post_processing": ["layered depth"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Soft Directional", "light_quality": "Highlights layers", "light_direction": "Side"},
        "composition_settings": {"technique": "Layered cut paper composition", "focal_point": "Detail"},
        "color_settings": {"color_scheme": "Varied", "palette_type": "Bright contrasting colors", "color_temperature": "Neutral", "color_contrast": "Medium"},
        "detail_settings": {"detail_level": "High", "texture_quality": "Crisp paper texture"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Studio", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "2048x2048", "rendering_quality": "Intricate Detail"},
        "negative_prompt": "flat, 2d, painting, drawing, signature, watermark, low quality",
        "style_negative_prompt": "no depth, blurry, unrealistic paper texture"
    }
    imagen_settings["papercraft_settings"] = {
        "layering_technique": "stacked cut paper layers", "paper_type": "colored cardstock paper",
        "edge_quality": "sharp precise cut edges", "construction_method": "glued layers with visible depth",
        "motif": "geometric stylized animals or scenes",
        "aesthetic_blend": "Layered paper art creating a 3D effect with tactile textures and precise cuts."
    }
    return {**base_template, "imagen_settings": imagen_settings} 