#!/usr/bin/env python3
"""
Digital Style Templates Module for AI Preset Generator.

This module provides specific template functions for a variety of digital art styles.
Each function generates a base dictionary structure tailored to the nuances of a
particular digital style, intended to be used by the AI for preset generation.

Styles covered include:
- General Digital Art
- Digital Painting
- Vector Art
- ASCII Art
- Isometric Art
- Game Styles (General)
- Pixel Art
- Vaporwave
- Glitch Art
- Surrealism (Digital Context)
- Cubism (Digital Context)
- Minimalism (Digital Context)
- Sci-Fi (Digital Concept Art)
- Steampunk (Digital Illustration)
- Papercraft (Digital Simulation)
- AI Generated Art
- Interactive Digital Art

Note: 3D rendering styles (like general 3D, voxel, low-poly) are handled in 
`three_d_style_templates.py`.
"""


from typing import Dict, Any


def get_digital_art_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for a general 'Digital Art' style.

    Args:
        style_category (str): The specific style category (unused in this function
                              but maintained for consistency with dispatcher).

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Digital Art Preset",
        "moods": ["Expressive", "Dynamic"],
        "aspect_ratio": "16:9",
        "description": "A general preset for digital art, focusing on expressive and dynamic visuals."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Contemporary Digital Art", "post_processing": ["color grading", "sharpening", "subtle chromatic aberration"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Flexible Digital Lighting", "light_quality": "Dynamic and Controllable", "light_direction": "Multiple or Artist Defined"},
        "composition_settings": {"technique": "Dynamic Composition", "focal_point": "Main Subject"},
        "color_settings": {"color_scheme": "Full Spectrum Digital Palette", "palette_type": "Balanced Expressive Palette", "color_temperature": "Mixed", "color_contrast": "High"},
        "detail_settings": {"detail_level": "High", "texture_quality": "Varied Digital Textures"},
        "environment_settings": {"weather": "Artist Defined", "season": "Artist Defined", "location_type": "Conceptual or Abstract", "atmospheric_effects": ["digital haze", "particle effects"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High Polished"},
        "negative_prompt": "traditional art, low detail, signature, watermark, low quality, blurry, jpeg artifacts",
        "style_negative_prompt": "unblended styles, flat colors, poor execution"
    }
    imagen_settings["digital_settings"] = {
        "software": "Common digital art software (e.g., Photoshop, Procreate, Krita, GIMP)", "rendering_technique": "Versatile raster and vector techniques, including photobashing and digital painting",
        "digital_effects": ["glow effects", "texture overlays", "layer masks", "particle systems"], "resolution": "4K",
        "filter_usage": ["Gaussian blur for depth", "color dodge for highlights", "noise generation for texture"], "brush_type": "custom textured brushes, procedural brushes",
        "layer_complexity": "complex with multiple adjustment layers, non-destructive workflow"
    }
    return {**base_template, "imagen_settings": imagen_settings}


def get_generative_art_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Generative Art' style.

    Args:
        style_category (str): The specific style category.

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Generative Art Preset",
        "moods": ["Algorithmic", "Systematic", "Experimental", "Abstract", "Emergent"],
        "aspect_ratio": "1:1", # Often square for abstract patterns
        "description": "A preset for generative art, focusing on algorithmic patterns, rule-based visual creation, and emergent complexity."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Generative Art", "post_processing": ["algorithmic refinement", "parameter variation renders", "vector output if applicable"], "style_era": "Contemporary Digital"},
        "lighting_settings": {"lighting_type": "Algorithmic or Abstract", "light_quality": "Defined by algorithm, can be flat or complex", "light_direction": "N/A or Algorithmic"},
        "composition_settings": {"technique": "Rule-based, emergent composition, grid systems, flow fields, cellular automata", "focal_point": "Overall pattern or emergent structures"},
        "color_settings": {"color_scheme": "Algorithmic Palette", "palette_type": "Custom algorithm-defined, monochrome, or vibrant spectrum", "color_temperature": "Varied", "color_contrast": "Varied by algorithm"},
        "detail_settings": {"detail_level": "Variable, from simple to highly intricate", "texture_quality": "Algorithmic, procedural, or smooth"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Abstract Digital Space", "atmospheric_effects": ["none or procedurally generated"]},
        "quality_settings": {"resolution": "Scalable (vector) or High Resolution (raster, e.g., 4096x4096)", "rendering_quality": "Crisp Algorithmic Precision"},
        "negative_prompt": "manual drawing, hand-painted, chaotic (unless intended by algorithm), purely figurative (unless generated by rules), blurry, imprecise, organic without structure",
        "style_negative_prompt": "random scribbles without rules, lack of system, purely emotional without logic, photographic realism"
    }
    imagen_settings["generative_art_settings"] = {
        "algorithm_type": "Mathematical formulas, logical rules, cellular automata, L-systems, agent-based systems, flow fields, noise algorithms, reaction-diffusion",
        "software_tools": "Processing, p5.js, TouchDesigner, OpenFrameworks, Houdini (algorithmic parts), Python (e.g., Matplotlib, NumPy, Pillow, Scikit-image), C++, GLSL shaders, custom scripts",
        "visual_complexity": "Ranges from minimalist patterns to deeply intricate and emergent systems, often exploring complexity from simple rules",
        "artist_control": "Algorithm design, parameter tuning, seed manipulation, rule definition, interaction design (for interactive pieces), curation of outputs",
        "output_forms": "Still images, animations, interactive installations, data visualizations, plotter art",
        "aesthetic_blend": "Art where the process of creation, often involving code and algorithms, is central to the outcome, leading to systematic, often abstract, and potentially surprising visuals. Explores themes of order, chaos, emergence, and computation."
    }
    return {**base_template, "imagen_settings": imagen_settings}


def get_fractal_art_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Fractal Art' style.

    Args:
        style_category (str): The specific style category.

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Fractal Art Preset",
        "moods": ["Intricate", "Mathematical", "Psychedelic", "Mesmerizing", "Infinite", "Hypnotic"],
        "aspect_ratio": "16:9", # Common for landscape-like fractals, or 1:1
        "description": "A preset for fractal art, emphasizing intricate mathematical patterns, self-similarity, and mesmerizing visual depth."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Fractal Art", "post_processing": ["depth coloring algorithms", "iteration scaling effects", "lighting on 3D fractals", "anti-aliasing", "bloom for highlights"], "style_era": "Contemporary Digital"},
        "lighting_settings": {"lighting_type": "Internal Fractal Illumination or Abstract", "light_quality": "Often emissive or derived from fractal structure, can include volumetric effects for 3D fractals", "light_direction": "N/A or from fractal 'light sources' / global illumination in 3D"},
        "composition_settings": {"technique": "Recursive patterns, self-similarity, infinite zoom explorations, spiral motifs, geometric tessellations", "focal_point": "Center of spiral, intricate detail sections, overall pattern, points of high iteration"},
        "color_settings": {"color_scheme": "Vibrant Psychedelic or Muted Technical", "palette_type": "Iteration-based, orbit trap coloring, custom gradients, procedural palettes, distance estimation coloring", "color_temperature": "Varied, can be cool or warm", "color_contrast": "High to Very High"},
        "detail_settings": {"detail_level": "Extremely High, potentially infinite detail due to recursive nature", "texture_quality": "Mathematical precision, smooth or granular based on algorithm, can simulate metallic or glasslike surfaces"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Abstract Mathematical Space, Otherworldly Landscape", "atmospheric_effects": ["depth haze (simulated)", "glows", "nebula-like formations in 3D fractals"]},
        "quality_settings": {"resolution": "High Resolution (e.g., 4K, 8K, or higher for print)", "rendering_quality": "High Precision, Deep Iteration, Anti-aliased"},
        "negative_prompt": "simple shapes, flat colors, non-mathematical, blurry, low iteration, organic hand-drawn look, figurative art (unless fractal is used as texture/element), pixelated (unless intentional low-res fractal style)",
        "style_negative_prompt": "smudged details, broken algorithms, non-recursive patterns, photographic realism of non-fractal objects, chaotic noise without structure"
    }
    imagen_settings["fractal_art_settings"] = {
        "software": "Apophysis, Ultra Fractal, Mandelbulb3D, Chaotica, JWildfire, Kalles Fraktaler, Fragmentarium, Incendia, Xenodream",
        "fractal_type": "Mandelbrot set, Julia set, Burning Ship, Newton fractals, Lyapunov fractals, Iterated Function Systems (IFS), Flame fractals, Quaternion fractals, Kleinian groups, 3D fractals (Mandelbulb, Mandelbox, Menger Sponge, Kaleidoscopic IFS)",
        "coloring_techniques": "Smooth iteration count, distance estimator, orbit trap, potential field, custom gradients, procedural textures mapped to fractal, interior/exterior coloring",
        "rendering_parameters": "High iteration depth (e.g., 1000 to millions), anti-aliasing (supersampling), deep zoom capabilities, custom formulas or scripts, 3D ray marching parameters (for 3D fractals)",
        "mathematical_basis": "Complex numbers, iterative functions, recursive algorithms, geometric transformations, non-linear equations, chaos theory",
        "aesthetic_blend": "Visually stunning art derived from precise mathematical formulas, showcasing infinite complexity, self-similarity, and often psychedelic, abstract geometric, or otherworldly organic forms. Can range from 2D intricate patterns to immersive 3D landscapes."
    }
    return {**base_template, "imagen_settings": imagen_settings}


def get_digital_painting_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Digital Painting' style.

    Args:
        style_category (str): The specific style category.

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Digital Painting Preset",
        "moods": ["Painterly", "Digital"],
        "aspect_ratio": "16:9",
        "description": "A preset for digital painting style, focusing on painterly techniques using digital tools."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Digital Painting", "post_processing": ["visible brush strokes", "texture blending", "glazing techniques (digital)"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Atmospheric Digital", "light_quality": "Painterly Light", "light_direction": "Artist Defined"},
        "composition_settings": {"technique": "Painterly composition", "focal_point": "Main Subject"},
        "color_settings": {"color_scheme": "Rich and Expressive", "palette_type": "Full color range with digital blending and color harmonies", "color_temperature": "Mixed", "color_contrast": "Medium to High"},
        "detail_settings": {"detail_level": "High", "texture_quality": "Custom digital brush textures, simulated canvas/paper texture"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Abstract or Stylized Scene", "atmospheric_effects": ["digital glow", "soft focus"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "traditional painting artifacts (unintentional), lack of digital finesse, signature, watermark, low quality, 3D render look",
        "style_negative_prompt": "unblended colors, flat lighting, overly smooth, vector look"
    }
    imagen_settings["digital_painting_settings"] = {
        "platform": "Photoshop, Procreate, Krita, Clip Studio Paint",
        "brushwork": "simulated natural media brush strokes (oil, watercolor, acrylic) with opacity and flow dynamics, textured brushes",
        "canvas_texture_simulation": "subtle digital canvas or paper texture integrated",
        "layering_techniques": "extensive use of layers, blending modes, adjustment layers for depth and color complexity",
        "aesthetic_blend": "Traditional painting appearance achieved through digital tools, often with enhanced lighting, color vibrancy, or unique digital effects."
    }
    return {**base_template, "imagen_settings": imagen_settings}


def get_vector_art_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Vector Art' style.

    Args:
        style_category (str): The specific style category.

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
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
    """
    Generates a base template for the 'ASCII Art' style.

    Args:
        style_category (str): The specific style category.

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "ASCII Art Preset",
        "moods": ["Retro", "Digital"],
        "aspect_ratio": "4:3",
        "description": "A general preset for ASCII art, using text characters to form images."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "ASCII Art", "post_processing": ["character mosaic effect", "scanlines (optional)"], "style_era": "Retro Computing"},
        "lighting_settings": {"lighting_type": "Flat / Implied by Character Density", "light_quality": "Hard-edged", "light_direction": "N/A"},
        "composition_settings": {"technique": "Grid-based character composition", "focal_point": "Image formed by characters"},
        "color_settings": {"color_scheme": "Monochrome or Limited Color", "palette_type": "classic monochrome (e.g., green on black, white on black, amber) or ANSI colors", "color_temperature": "Cool or Neutral", "color_contrast": "High"},
        "detail_settings": {"detail_level": "Character-defined", "texture_quality": "ASCII character texture, fixed-width font look"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Console Terminal Screen", "atmospheric_effects": ["phosphor glow (optional)"]},
        "quality_settings": {"resolution": "Character-based (e.g., 80x25, 132x50 characters) scaled for viewing", "rendering_quality": "Retro Digital, Crisp Characters"},
        "negative_prompt": "realism, full-color photography, smooth gradient, anti-aliasing, signature, watermark, low quality, vector art",
        "style_negative_prompt": "natural photo, smooth curves, photographic detail, blended colors"
    }
    imagen_settings["ascii_art_settings"] = {
        "character_set": "standard ASCII, extended ASCII, block characters", "font_style": "fixed-width, monospace (e.g., Courier, Terminal)",
        "character_resolution": "medium to high character density", "contrast_method": "character brightness/density for shading",
        "color_depth": "monochrome, 2-bit, 4-bit (16 colors), or 8-bit (256 colors) if using ANSI/extended",
        "aesthetic_blend": "Text-based art using ASCII/extended characters to form recognizable images, evoking a retro computer or terminal aesthetic."
    }
    return {**base_template, "imagen_settings": imagen_settings}


def get_isometric_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Isometric' art style.

    Args:
        style_category (str): The specific style category.

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
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
    """
    Generates a base template for a general 'Game Style' (concept art/cinematic).

    Args:
        style_category (str): The specific style category.

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Game Style Preset",
        "moods": ["Epic", "Adventurous", "Immersive"],
        "aspect_ratio": "16:9",
        "description": "A general preset for modern game concept art, focusing on dynamic composition and high detail."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Modern Game Concept Art / In-Engine Cinematics", "post_processing": ["cinematic color grading (LUTs)", "bloom", "lens flares"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Dynamic Real-time Global Illumination", "light_quality": "Photorealistic or Stylized High Fidelity", "light_direction": "Multiple, Volumetric"},
        "composition_settings": {"technique": "Dynamic composition for games, rule of thirds, leading lines", "focal_point": "Main Character or Environmental Storytelling Element"},
        "color_settings": {"color_scheme": "Harmonious or Contrasting based on mood", "palette_type": "Realistic or Stylized Game Palette with PBR materials", "color_temperature": "Mixed, scene-dependent", "color_contrast": "High"},
        "detail_settings": {"detail_level": "Very High", "texture_quality": "High-fidelity PBR textures (4K-8K)"},
        "environment_settings": {"weather": "Dynamic Weather Systems", "season": "Varied", "location_type": "Immersive Game Environment (Fantasy, Sci-Fi, Realistic)", "atmospheric_effects": ["volumetric lighting", "fog", "particle effects (rain, snow, dust)"]},
        "quality_settings": {"resolution": "3840x2160 (4K) or higher", "rendering_quality": "Cinematic In-Engine Quality (e.g., Unreal Engine, Unity)"},
        "negative_prompt": "low detail, flat lighting, 2D look, signature, watermark, low quality, poor texturing, obvious tiling",
        "style_negative_prompt": "static composition, unrealistic rendering (unless stylized), non-PBR materials, poor performance look"
    }
    imagen_settings["game_engine_settings"] = {
        "engine_type": "Modern Game Engine (e.g., Unreal Engine, Unity, CryEngine)", "render_quality": "High Cinematic / Real-time Ray Tracing (if applicable)",
        "shader_type": "Physically Based Rendering (PBR) with advanced material graphs", "special_effects": ["bloom", "screen space reflections (SSR)", "ambient occlusion (SSAO/HBAO)", "volumetric lighting/fog"],
        "post_effects": ["depth of field (cinematic DoF)", "motion blur", "color grading (ACES, Filmic LUTs)", "anti-aliasing (TAA, MSAA)"], "resolution": "4K (3840x2160) or target platform resolution",
        "physics_settings": ["realistic physics simulation (e.g., Chaos Physics, PhysX)"], "animation_style": "smooth realistic character animation, procedural animation elements"
    }
    imagen_settings["game_settings"] = {
        "interactivity": "high interactivity implied by scene elements", "environment_type": "detailed outdoor fantasy environment, sci-fi cityscape, realistic interior",
        "character_style": "realistic or stylized high-detail characters with PBR materials", "lighting_type": "dynamic real-time lighting with global illumination and reflections"
    }
    return {**base_template, "imagen_settings": imagen_settings}


def get_pixel_art_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Pixel Art' style.

    Args:
        style_category (str): The specific style category.

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
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
    """
    Generates a base template for the 'Vaporwave' aesthetic.

    Args:
        style_category (str): The specific style category.

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
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
    """
    Generates a base template for the 'Glitch Art' style.

    Args:
        style_category (str): The specific style category.

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
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
    """
    Generates a base template for the 'Digital Surrealism' style.

    Args:
        style_category (str): The specific style category.

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Surrealism Preset",
        "moods": ["Dreamlike", "Uncanny", "Mysterious"],
        "aspect_ratio": "16:9",
        "description": "A preset for Surrealism, focusing on dreamlike illogical juxtapositions and scenes."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Digital Surrealism", "post_processing": ["dreamlike effects", "seamless compositing", "subtle distortions"], "style_era": "Contemporary Digital"},
        "lighting_settings": {"lighting_type": "Dramatic Mysterious or Ethereal", "light_quality": "Chiaroscuro or Soft Glow", "light_direction": "Multiple, often unconventional"},
        "composition_settings": {"technique": "Illogical juxtaposition, symbolic arrangements", "focal_point": "Unexpected or symbolic elements"},
        "color_settings": {"color_scheme": "Symbolic and Evocative", "palette_type": "Varied, often Muted or Contrasting Symbolic Palette", "color_temperature": "Mixed", "color_contrast": "Medium to High"},
        "detail_settings": {"detail_level": "High, often hyperrealistic detail on unreal subjects", "texture_quality": "Realistic or digitally manipulated textures"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Dreamscape, subconscious landscapes", "atmospheric_effects": ["mist", "unusual shadows", "warped reality"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High, polished digital finish"},
        "negative_prompt": "realistic, logical, mundane, predictable, signature, watermark, low quality, poorly composited",
        "style_negative_prompt": "predictable composition, flat lighting, obvious digital seams, lack of mystery"
    }
    imagen_settings["surrealism_settings"] = {
        "conceptual_approach": "dreamlike, bizarre, unexpected juxtapositions, Freudian symbolism", "color_scheme": "muted, contrasting, or symbolic colors to evoke mood",
        "composition": "layered symbolic narrative structure, transformation of objects", "mood": "mysterious, uncanny, thought-provoking, unsettling",
        "digital_techniques": ["photorealistic rendering of impossible scenes", "seamless photobashing", "3D elements integration", "advanced masking and blending"]
    }
    return {**base_template, "imagen_settings": imagen_settings}


def get_cubism_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Digital Cubism' style.

    Args:
        style_category (str): The specific style category.

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Cubism Preset",
        "moods": ["Analytical", "Geometric", "Abstract"],
        "aspect_ratio": "16:9",
        "description": "A preset for Cubism, focusing on fragmented forms and multiple viewpoints."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Digital Cubism", "post_processing": ["geometric fragmentation", "sharp vector-like edges", "textured planes"], "style_era": "Contemporary Digital"},
        "lighting_settings": {"lighting_type": "Simplified Abstracted, Faceted Lighting", "light_quality": "Geometric, hard-edged shadows", "light_direction": "Multiple, non-naturalistic"},
        "composition_settings": {"technique": "Fragmented forms, multiple viewpoints, overlapping planes", "focal_point": "Deconstructed Subject"},
        "color_settings": {"color_scheme": "Muted Earthy (Analytical) or Bold Contrasting (Synthetic)", "palette_type": "Muted Earthy Tones or Later Bolder Colors, often with digital precision", "color_temperature": "Neutral or Mixed", "color_contrast": "Medium to High"},
        "detail_settings": {"detail_level": "Medium to High within fragments", "texture_quality": "Geometric planes, flat, or digitally textured (e.g., simulated wood grain, newsprint)"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Abstract, Deconstructed Space", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High, crisp digital rendering"},
        "negative_prompt": "realistic, smooth, organic, traditional perspective, signature, watermark, low quality, blurry edges",
        "style_negative_prompt": "blended forms, soft edges, single viewpoint, photographic realism"
    }
    imagen_settings["cubism_settings"] = {
        "form_style": "angular, fragmented, multiple simultaneous perspectives, deconstruction of subject", "color_palette": "muted earthy tones (analytical) or bold, flat colors (synthetic), often with black outlines",
        "composition": "geometric abstraction, layered and overlapping planes, interplay of positive and negative space",
        "digital_techniques": ["3D model fragmentation effects", "vector-sharp geometric planes", "digital texture application", "algorithmic deconstruction"],
        "aesthetic_blend": "Classic Cubist principles (Analytical/Synthetic) reinterpreted with digital tools, emphasizing geometric precision and complex spatial relationships."
    }
    return {**base_template, "imagen_settings": imagen_settings}


def get_minimalist_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Digital Minimalism' style.

    Args:
        style_category (str): The specific style category.

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
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
    """
    Generates a base template for a general 'Science Fiction' concept art style.

    Args:
        style_category (str): The specific style category.

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Sci-Fi Preset",
        "moods": ["Futuristic", "Exploratory", "Technological"],
        "aspect_ratio": "16:9",
        "description": "A general preset for Science Fiction concept art, focusing on futuristic scenes."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Science Fiction Concept Art", "post_processing": ["lens flares", "chromatic aberration", "holographic interface elements"], "style_era": "Contemporary / Near Future / Far Future"},
        "lighting_settings": {"lighting_type": "Artificial, Alien World, or Starship Interior Lighting", "light_quality": "Often high contrast, emissive lights", "light_direction": "Multiple, dynamic"},
        "composition_settings": {"technique": "Futuristic scene composition, cinematic framing", "focal_point": "Advanced Technology, Alien Structures, or Character Interaction with Environment"},
        "color_settings": {"color_scheme": "Cool Blues and Cyans with Warm Accents, or Alien Color Palettes", "palette_type": "Varied Sci-Fi Palette (gritty, sleek, or bioluminescent)", "color_temperature": "Mixed, often cool with warm emissives", "color_contrast": "High"},
        "detail_settings": {"detail_level": "High to Very High", "texture_quality": "Metallic, Composite Materials, Digital Screens, Alien Textures"},
        "environment_settings": {"weather": "N/A or Alien Atmospheric Conditions", "season": "N/A", "location_type": "Spaceship Interior, Alien Planet, Futuristic Cityscape, Dyson Sphere", "atmospheric_effects": ["space dust", "nebulae", "energy fields", "atmospheric distortion"]},
        "quality_settings": {"resolution": "3840x2160 or higher for concept art", "rendering_quality": "High, cinematic digital painting or 3D render"},
        "negative_prompt": "organic (unless alien biology), low detail, contemporary mundane objects, signature, watermark, low quality, fantasy elements (unless sci-fantasy)",
        "style_negative_prompt": "traditional art style, unrealistic technology (for the established tech level), overly simple designs"
    }
    imagen_settings["sci_fi_settings"] = {
        "technology_level": "advanced futuristic technology (e.g., FTL travel, AI, cybernetics, energy weapons)", "environment_theme": "space station interior, alien landscape, dystopian city, utopian enclave",
        "lighting_style": "artificial cold lighting, neon glows, emissive panels, lens flares from bright sources", "color_palette": "metallic blues, silvers, greys with accents of orange, red, or vibrant alien colors",
        "visual_elements": ["glowing energy effects", "holographic displays", "intricate machinery", "sleek spacecraft", "complex user interfaces"],
        "aesthetic_blend": "Clean futuristic design, gritty realism, or fantastical alien worlds, emphasizing technological advancement and speculative concepts."
    }
    return {**base_template, "imagen_settings": imagen_settings}


def get_steampunk_template(style_category: str) -> Dict[str, Any]:
    """
    Generates a base template for the 'Steampunk' digital illustration style.

    Args:
        style_category (str): The specific style category.

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
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
    """
    Generates a base template for the 'Digital Papercraft' style.

    Args:
        style_category (str): The specific style category.

    Returns:
        Dict[str, Any]: A dictionary containing the preset template.
    """
    base_template = {
        "preset_name": "Papercraft Preset",
        "moods": ["Crafted", "Textured"],
        "aspect_ratio": "1:1",
        "description": "A general preset for papercraft art, focusing on layered cut paper."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Digital Paper Art / Papercraft Illustration", "post_processing": ["layered depth effects", "subtle drop shadows", "paper texture overlay"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Soft Directional Studio Light", "light_quality": "Highlights layers and paper texture", "light_direction": "Slightly Angled / Top-Side"},
        "composition_settings": {"technique": "Layered cut paper composition, diorama-like", "focal_point": "Central Subject or Intricate Detail"},
        "color_settings": {"color_scheme": "Bright and Playful or Muted and Elegant", "palette_type": "Bright contrasting colors or harmonious analogous colors", "color_temperature": "Neutral to Warm", "color_contrast": "Medium to High"},
        "detail_settings": {"detail_level": "High", "texture_quality": "Crisp paper texture, subtle grain, folded edges"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Studio Setting or Abstract Background", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "2048x2048 or higher", "rendering_quality": "Intricate Detail, Clean Edges"},
        "negative_prompt": "flat, 2d (unintentionally), painting, drawing, photorealistic, signature, watermark, low quality, blurry edges",
        "style_negative_prompt": "no depth, blurry textures, unrealistic paper interaction, overly smooth, digitally flat"
    }
    imagen_settings["papercraft_settings"] = {
        "layering_technique": "stacked and overlapping cut paper layers, quilling elements (optional)", "paper_type": "simulated colored cardstock, textured paper, vellum",
        "edge_quality": "sharp precise cut edges, slightly beveled edges for depth", "construction_method": "simulated glued or spaced layers with visible depth and shadow play",
        "motif": "geometric patterns, stylized figures, animals, scenes, typography",
        "aesthetic_blend": "Digitally rendered art emulating the tactile qualities of physical papercraft, emphasizing layers, texture, and precise cuts to create a 3D illusion."
    }
    return {**base_template, "imagen_settings": imagen_settings}
