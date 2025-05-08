"""
Unique Style Templates Module for AI Preset Generator

This module contains unique style templates for various non-portrait style categories,
each with concrete default values for all relevant settings. Portrait styles
should be handled by the get_portrait_template function in style_templates.py.
"""

from typing import Dict, Any

# Note: This function assumes portrait styles are handled elsewhere.
# It provides templates for the specific non-portrait styles defined below.
def get_unique_style_template(style_category: str) -> Dict[str, Any]:
    """
    Returns a unique, detailed template with concrete defaults for a given
    non-portrait style category defined within this module.

    Args:
        style_category (str): The normalized (lowercase) style category name.

    Returns:
        Dict[str, Any]: A dictionary representing the JSON template for the style,
                      or a default fallback if the category is not defined here.
    """
    style_category = style_category.lower()

    # Base structure, values will be heavily overridden by specific styles
    base_template = {
        "preset_name": f"{style_category.replace('_', ' ').title()} Unique Preset",
        "moods": ["Evocative"],
        "aspect_ratio": "16:9",
        "description": f"A unique preset tailored for the {style_category.replace('_', ' ')} style."
    }

    # Default imagen settings, will be customized per style
    imagen_settings = {
        "style_settings": {
            "art_movement": "Contemporary",
            "post_processing": ["subtle sharpening"],
            "style_era": "Modern"
        },
        "lighting_settings": {
            "lighting_type": "Natural",
            "light_quality": "Soft Diffused",
            "light_direction": "Front",
            "time_of_day": "Daytime"
        },
        "composition_settings": {
            "technique": "Rule of Thirds",
            "focal_point": "Main Subject",
            "camera_angle": "Eye-level",
            "perspective": "One-point"
        },
        "color_settings": {
            "color_scheme": "Analogous",
            "palette_type": "Balanced",
            "color_temperature": "Neutral",
            "color_contrast": "Medium",
            "dominant_colors": ["blue", "green", "grey"]
        },
        "detail_settings": {
            "detail_level": "Medium",
            "texture_quality": "Realistic"
        },
        "environment_settings": {
            "weather": "Clear",
            "season": "Spring",
            "location_type": "Outdoor",
            "atmospheric_effects": ["subtle haze"]
        },
        "quality_settings": {
            "resolution": "3840x2160",
            "rendering_quality": "High"
        },
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, text, words, amateur, low quality",
        "style_negative_prompt": "clashing styles, inconsistent lighting, poor composition, unrealistic elements (unless style dictates), generic, boring, flat"
    }

    # --- Define Common Camera Settings with concrete defaults ---
    # Shared across photographic styles defined within this function
    COMMON_CAMERA_SETTINGS = {
        "camera_model": "DSLR", "lens_type": "Prime (50mm)", "aperture": "f/2.8",
        "focal_length": "50mm", "shutter_speed": "1/125s", "iso": "ISO 200",
        "filter_type": "None", "depth_of_field": "Medium", "white_balance": "Auto",
        "focus_mode": "Autofocus Single (AF-S/One-Shot)", "exposure_mode": "Aperture Priority (Av/A)",
        "image_stabilization": "Optical (OIS in lens)", "metering_mode": "Evaluative/Matrix",
        "flash_mode": "Off", "shooting_mode": "Single Shot",
        "focus_point_selection": "Single Point AF", "image_format": "RAW", "color_space": "sRGB"
    }
    # PORTRAIT_CAMERA_SETTINGS removed as portrait logic is removed


    # --- Full list of NON-PORTRAIT style categories with specific customizations ---
    # Based on the structure in unique_style_templates.py upload

    if style_category == "pop_surrealism_ascii":
        imagen_settings["style_settings"]["art_movement"] = "Pop Surrealism ASCII"
        imagen_settings["composition_settings"]["technique"] = "ASCII Art Composition"
        imagen_settings["color_settings"]["palette_type"] = "Monochrome Green on Black"
        imagen_settings["detail_settings"]["texture_quality"] = "ASCII Character Texture"
        base_template["aspect_ratio"] = "4:3"
        base_template["moods"] = ["Retro", "Playful", "Bizarre"]

    elif style_category == "abstract_expressionism_cubism_fusion":
        imagen_settings["style_settings"]["art_movement"] = "Abstract Expressionism Cubism Fusion"
        imagen_settings["composition_settings"]["technique"] = "Fragmented Abstract with Gestural Elements"
        imagen_settings["color_settings"]["palette_type"] = "Bold Contrasting Emotive"
        imagen_settings["detail_settings"]["texture_quality"] = "Visible Brushstrokes and Geometric Planes"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Dynamic", "Emotional", "Complex"]

    elif style_category == "anime_oilpainting":
        imagen_settings["style_settings"]["art_movement"] = "Anime Oil Painting Fusion"
        imagen_settings["lighting_settings"]["lighting_type"] = "Soft Studio Lighting with Rim Highlights"
        imagen_settings["color_settings"]["palette_type"] = "Vibrant Anime Colors with Oil Paint Blending"
        imagen_settings["detail_settings"]["texture_quality"] = "Oil Paint Impasto Texture on Anime Forms"
        imagen_settings["detail_settings"]["detail_level"] = "Medium High"
        base_template["aspect_ratio"] = "3:4" # Often character focused
        base_template["moods"] = ["Painterly", "Expressive", "Stylized"]

    elif style_category == "retro_pixel_vaporwave":
        imagen_settings["style_settings"]["art_movement"] = "Retro Pixel Vaporwave"
        imagen_settings["color_settings"]["palette_type"] = "Neon Pastels with Glitch Accents"
        imagen_settings["composition_settings"]["technique"] = "16-bit Pixel Art with Vaporwave Motifs"
        imagen_settings["detail_settings"]["texture_quality"] = "Pixelated with CRT Scanlines"
        imagen_settings["environment_settings"]["atmospheric_effects"] = ["subtle glitch", "neon glow"]
        base_template["aspect_ratio"] = "1:1"
        base_template["moods"] = ["Nostalgic", "Surreal", "Aesthetic"]

    elif style_category == "dreamcore_weirdcore":
        imagen_settings["style_settings"]["art_movement"] = "Dreamcore Weirdcore"
        imagen_settings["lighting_settings"]["lighting_type"] = "Soft Diffused Eerie Light"
        imagen_settings["color_settings"]["palette_type"] = "Desaturated Pastels with Occasional Neon"
        imagen_settings["composition_settings"]["technique"] = "Liminal Space Composition"
        imagen_settings["environment_settings"]["location_type"] = "Empty Familiar Places (e.g., mall, school)"
        imagen_settings["quality_settings"]["rendering_quality"] = "Low-fidelity VHS aesthetic"
        imagen_settings["post_processing"] = ["slight blur", "film grain", "light leaks"]
        base_template["aspect_ratio"] = "4:3"
        base_template["moods"] = ["Nostalgic", "Uncanny", "Eerie", "Dreamlike"]

    elif style_category == "photorealism_glitch":
        imagen_settings["style_settings"]["art_movement"] = "Photorealism Glitch Art"
        imagen_settings["post_processing"] = ["moderate glitch effects", "RGB shift", "pixel sorting"]
        imagen_settings["color_settings"]["palette_type"] = "Realistic Colors with Digital Artifacts"
        imagen_settings["detail_settings"]["detail_level"] = "Hyperrealistic Base"
        imagen_settings["detail_settings"]["texture_quality"] = "Sharp Photographic Detail with Glitch Textures"
        imagen_settings["camera_settings"] = COMMON_CAMERA_SETTINGS.copy() # CORRECTED: Added camera settings
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Deconstructed", "Digital", "Chaotic"]

    elif style_category == "watercolor_pencil":
        imagen_settings["style_settings"]["art_movement"] = "Watercolor Pencil Illustration"
        imagen_settings["lighting_settings"]["lighting_type"] = "Natural Soft Window Light"
        imagen_settings["color_settings"]["palette_type"] = "Soft Transparent Pastels"
        imagen_settings["detail_settings"]["texture_quality"] = "Watercolor Paper Texture with Graphite Lines"
        imagen_settings["composition_settings"]["technique"] = "Wash and Sketch Layering"
        imagen_settings["detail_settings"]["detail_level"] = "Medium"
        base_template["aspect_ratio"] = "4:3"
        base_template["moods"] = ["Delicate", "Illustrative", "Gentle"]

    elif style_category == "cubism_futurism":
        imagen_settings["style_settings"]["art_movement"] = "Cubism Futurism Fusion"
        imagen_settings["composition_settings"]["technique"] = "Geometric Fragmentation Suggesting Motion"
        imagen_settings["color_settings"]["palette_type"] = "Bold Metallic Dynamic Palette"
        imagen_settings["detail_settings"]["texture_quality"] = "Sharp Geometric Planes with Motion Lines"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Dynamic", "Mechanical", "Energetic"]

    elif style_category == "digital_pixel_traditional":
        imagen_settings["style_settings"]["art_movement"] = "Digital Pixel Traditional Fusion"
        imagen_settings["composition_settings"]["technique"] = "Pixel Art Characters on Painted Background"
        imagen_settings["color_settings"]["palette_type"] = "Vibrant Mixed Pixel/Painterly Palette"
        imagen_settings["detail_settings"]["texture_quality"] = "Contrasting Pixelated and Painterly Textures"
        base_template["aspect_ratio"] = "1:1"
        base_template["moods"] = ["Hybrid", "Retro", "Artistic"]

    elif style_category == "scientific_technological_hybrid":
        imagen_settings["style_settings"]["art_movement"] = "Scientific Technological Hybrid Art"
        imagen_settings["lighting_settings"]["lighting_type"] = "Artificial Clean Lab Lighting"
        imagen_settings["color_settings"]["palette_type"] = "Cool Blues Greys and Data-Inspired Highlights"
        imagen_settings["composition_settings"]["technique"] = "Algorithmic Composition or Data Visualization"
        imagen_settings["detail_settings"]["detail_level"] = "High Technical Detail"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Analytical", "Complex", "Futuristic"]

    elif style_category == "psychedelic_surrealism":
        imagen_settings["style_settings"]["art_movement"] = "Psychedelic Surrealism"
        imagen_settings["post_processing"] = ["vibrant swirling colors", "morphing fractal patterns"]
        imagen_settings["color_settings"]["palette_type"] = "Vivid Contrasting Neon Palette"
        imagen_settings["composition_settings"]["technique"] = "Illogical Dreamscape Composition"
        imagen_settings["detail_settings"]["texture_quality"] = "Fluid and Glossy Textures"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Trippy", "Mind-bending", "Surreal", "Vibrant"]

    elif style_category == "morphism_surreal":
        imagen_settings["style_settings"]["art_movement"] = "Morphism Surrealism"
        imagen_settings["composition_settings"]["technique"] = "Fluid Morphing Shapes and Objects"
        imagen_settings["color_settings"]["palette_type"] = "Soft Dreamy Pastel Palette"
        imagen_settings["detail_settings"]["texture_quality"] = "Smooth Blended Textures"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Dreamlike", "Fluid", "Fantastical"]

    elif style_category == "kinetic_ascii":
        imagen_settings["style_settings"]["art_movement"] = "Kinetic ASCII Art"
        imagen_settings["composition_settings"]["technique"] = "Animated ASCII Grid Composition"
        imagen_settings["color_settings"]["palette_type"] = "Monochrome Green on Black"
        imagen_settings["detail_settings"]["texture_quality"] = "ASCII Character Texture"
        base_template["aspect_ratio"] = "4:3"
        base_template["moods"] = ["Retro", "Digital", "Animated"]

    elif style_category == "collage_digital_overlay":
        imagen_settings["style_settings"]["art_movement"] = "Collage with Digital Overlay"
        imagen_settings["composition_settings"]["technique"] = "Layered Mixed Media Collage with Digital Effects"
        imagen_settings["color_settings"]["palette_type"] = "Eclectic Vibrant Mixed Palette"
        imagen_settings["detail_settings"]["texture_quality"] = "Tactile Paper Texture with Digital Gloss/Glow"
        base_template["aspect_ratio"] = "1:1"
        base_template["moods"] = ["Layered", "Textured", "Contemporary"]

    elif style_category == "pixel_patchwork":
        imagen_settings["style_settings"]["art_movement"] = "Pixel Patchwork"
        imagen_settings["composition_settings"]["technique"] = "Patchwork Composition using Pixel Art Blocks"
        imagen_settings["color_settings"]["palette_type"] = "Varied Limited Color Palettes per Patch"
        imagen_settings["detail_settings"]["texture_quality"] = "Pixelated Blocky Texture"
        base_template["aspect_ratio"] = "1:1"
        base_template["moods"] = ["Retro", "Crafted", "Geometric"]

    elif style_category == "tradigital_mixed_media":
        imagen_settings["style_settings"]["art_movement"] = "Tradigital Mixed Media"
        imagen_settings["composition_settings"]["technique"] = "Mixed Traditional Painting and Digital Layering"
        imagen_settings["color_settings"]["palette_type"] = "Natural Palette Enhanced with Digital Light"
        imagen_settings["detail_settings"]["texture_quality"] = "Visible Brushstrokes with Digital Texture Overlays"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Hybrid", "Textured", "Contemporary"]

    elif style_category == "hybrid_traditional_digital":
        imagen_settings["style_settings"]["art_movement"] = "Hybrid Traditional Digital Art"
        imagen_settings["composition_settings"]["technique"] = "Fusion of Traditional Drawing and Digital Coloring/Effects"
        imagen_settings["color_settings"]["palette_type"] = "Balanced Natural and Digital Palette"
        imagen_settings["detail_settings"]["texture_quality"] = "Traditional Paper Texture with Digital Smoothness"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Integrated", "Modern", "Artistic"]

    elif style_category == "digital_traditional_fusion":
        imagen_settings["style_settings"]["art_movement"] = "Digital Traditional Fusion"
        imagen_settings["composition_settings"]["technique"] = "Blended Digital Painting with Traditional Aesthetics"
        imagen_settings["color_settings"]["palette_type"] = "Rich Varied Palette"
        imagen_settings["detail_settings"]["texture_quality"] = "Digital Textures Mimicking Traditional Media"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Fusion", "Rich", "Expressive"]

    # --- Portrait Handling Removed ---

    # --- Other Specific Styles ---
    elif style_category == "noir_photography":
        imagen_settings["style_settings"]["art_movement"] = "Film Noir Photography"
        imagen_settings["composition_settings"]["technique"] = "High Contrast Black and White Chiaroscuro"
        imagen_settings["color_settings"]["palette_type"] = "Monochrome Greyscale"
        imagen_settings["lighting_settings"]["light_quality"] = "Hard Directional Shadows"
        imagen_settings["post_processing"] = ["heavy film grain", "vignette"]
        imagen_settings["camera_settings"] = COMMON_CAMERA_SETTINGS.copy() # CORRECTED: Added camera settings
        base_template["aspect_ratio"] = "4:3"
        base_template["moods"] = ["Mysterious", "Gritty", "Suspenseful"]

    elif style_category == "art_deco_revival":
        imagen_settings["style_settings"]["art_movement"] = "Art Deco Revival"
        imagen_settings["composition_settings"]["technique"] = "Geometric Symmetry and Streamlined Forms"
        imagen_settings["color_settings"]["palette_type"] = "Gold Black Silver Jewel Tones"
        imagen_settings["detail_settings"]["texture_quality"] = "Polished Metallic and Lacquered Surfaces"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Glamorous", "Sophisticated", "Modernist"]

    elif style_category == "augmented_reality_art":
        imagen_settings["style_settings"]["art_movement"] = "Augmented Reality Art"
        imagen_settings["composition_settings"]["technique"] = "Interactive Immersive Digital Overlay"
        imagen_settings["color_settings"]["palette_type"] = "Bright Futuristic Digital Palette"
        imagen_settings["quality_settings"]["rendering_quality"] = "Real-time 3D Render"
        base_template["aspect_ratio"] = "16:9" # Often viewed on screens
        base_template["moods"] = ["Interactive", "Futuristic", "Immersive"]

    elif style_category == "biopunk":
        imagen_settings["style_settings"]["art_movement"] = "Biopunk"
        imagen_settings["composition_settings"]["technique"] = "Organic Technology Fusion with Body Horror Elements"
        imagen_settings["color_settings"]["palette_type"] = "Dark Greens Browns Metallics with Sickly Neon Highlights"
        imagen_settings["detail_settings"]["texture_quality"] = "Organic Slimy Textured Surfaces with Metal"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Unsettling", "Gritty", "Organic", "Dystopian"]

    elif style_category == "ferrofluid":
        imagen_settings["style_settings"]["art_movement"] = "Ferrofluid Art"
        imagen_settings["composition_settings"]["technique"] = "Magnetic Liquid Abstract Patterns"
        imagen_settings["color_settings"]["palette_type"] = "Black Silver Metallic"
        imagen_settings["detail_settings"]["texture_quality"] = "Spiky Glossy Liquid Metal Texture"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Mesmerizing", "Scientific", "Abstract"]

    elif style_category == "fractal_generative_art":
        imagen_settings["style_settings"]["art_movement"] = "Fractal Generative Art"
        imagen_settings["composition_settings"]["technique"] = "Algorithmic Recursive Mathematical Patterns"
        imagen_settings["color_settings"]["palette_type"] = "Vibrant Complex Gradient Palettes"
        imagen_settings["detail_settings"]["detail_level"] = "Infinitely Complex Detail"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Hypnotic", "Mathematical", "Infinite"]

    elif style_category == "installation_art":
        imagen_settings["style_settings"]["art_movement"] = "Installation Art"
        imagen_settings["composition_settings"]["technique"] = "Spatial Environmental Site-Specific Composition"
        imagen_settings["color_settings"]["palette_type"] = "Varied depending on materials and concept"
        imagen_settings["detail_settings"]["texture_quality"] = "Varied based on physical materials used"
        base_template["aspect_ratio"] = "N/A (Spatial)" # Aspect ratio less relevant
        base_template["moods"] = ["Immersive", "Experiential", "Conceptual"]

    elif style_category == "kinetic_art":
        imagen_settings["style_settings"]["art_movement"] = "Kinetic Art"
        imagen_settings["composition_settings"]["technique"] = "Art Incorporating Physical Movement or Illusion of Motion"
        imagen_settings["color_settings"]["palette_type"] = "Dynamic Contrasting Colors"
        imagen_settings["detail_settings"]["detail_level"] = "Medium to High Mechanical Detail"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Dynamic", "Moving", "Mechanical"]

    elif style_category == "luna_photo":
        imagen_settings["style_settings"]["art_movement"] = "Luna Photo Surrealism"
        imagen_settings["composition_settings"]["technique"] = "Moon Photography with Double Exposure/Composite"
        imagen_settings["color_settings"]["palette_type"] = "Deep Blues Silvers Ethereal Tones"
        imagen_settings["lighting_settings"]["light_quality"] = "Soft Diffuse Moonlit Glow"
        imagen_settings["camera_settings"] = COMMON_CAMERA_SETTINGS.copy() # CORRECTED: Added camera settings
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Mystical", "Ethereal", "Dreamlike"]

    elif style_category == "mixed_media_journaling":
        imagen_settings["style_settings"]["art_movement"] = "Mixed Media Journaling / Art Journal"
        imagen_settings["composition_settings"]["technique"] = "Layered Textured Composition with Text and Found Objects"
        imagen_settings["color_settings"]["palette_type"] = "Eclectic Personal Varied Palette"
        imagen_settings["detail_settings"]["texture_quality"] = "Layered Paper Paint Ink Fabric Textures"
        base_template["aspect_ratio"] = "4:5" # Common journal page ratio
        base_template["moods"] = ["Personal", "Creative", "Layered", "Textured"]

    elif style_category == "nightcore":
        imagen_settings["style_settings"]["art_movement"] = "Nightcore Aesthetic"
        imagen_settings["composition_settings"]["technique"] = "High Energy Anime Visuals with Music Motifs"
        imagen_settings["color_settings"]["palette_type"] = "Neon Pastels High-Contrast Palette"
        imagen_settings["post_processing"] = ["glow effects", "fast motion blur", "audio visualizer elements"]
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Energetic", "Fast-paced", "Edgy", "Futuristic"]

    elif style_category == "optic_art":
        imagen_settings["style_settings"]["art_movement"] = "Op Art (Optical Art)"
        imagen_settings["composition_settings"]["technique"] = "Geometric Patterns Creating Optical Illusions (e.g., Moiré)"
        imagen_settings["color_settings"]["palette_type"] = "High Contrast Black and White or Complementary Colors"
        imagen_settings["detail_settings"]["detail_level"] = "Precise Geometric Detail"
        base_template["aspect_ratio"] = "1:1" # Often square
        base_template["moods"] = ["Dizzying", "Geometric", "Illusionary"]

    elif style_category == "paper_quilling":
        imagen_settings["style_settings"]["art_movement"] = "Paper Quilling Art"
        imagen_settings["composition_settings"]["technique"] = "Intricate Rolled Paper Coil Patterns"
        imagen_settings["color_settings"]["palette_type"] = "Bright Pastel Contrasting Colors"
        imagen_settings["detail_settings"]["texture_quality"] = "Delicate 3D Paper Texture"
        imagen_settings["detail_settings"]["detail_level"] = "Highly Intricate Detail"
        base_template["aspect_ratio"] = "1:1" # Often framed square
        base_template["moods"] = ["Delicate", "Intricate", "Decorative"]

    elif style_category == "phygital_hybrid":
        imagen_settings["style_settings"]["art_movement"] = "Phygital Hybrid Art"
        imagen_settings["composition_settings"]["technique"] = "Fusion of Physical Object and Digital Augmentation (e.g., AR)"
        imagen_settings["color_settings"]["palette_type"] = "Mixed Palette Bridging Physical and Digital"
        imagen_settings["detail_settings"]["texture_quality"] = "Contrast between Physical Material and Digital Overlay"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Hybrid", "Interactive", "Modern"]

    elif style_category == "screen_printing_bold":
        imagen_settings["style_settings"]["art_movement"] = "Bold Screen Printing Style"
        imagen_settings["composition_settings"]["technique"] = "Bold Graphic Design with Layered Flat Colors"
        imagen_settings["color_settings"]["palette_type"] = "Limited High Contrast Color Palette (2-4 colors)"
        imagen_settings["detail_settings"]["texture_quality"] = "Flat Ink Texture with Slight Misregistration"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Graphic", "Bold", "Retro", "Tactile"]

    elif style_category == "synesthesia_art":
        imagen_settings["style_settings"]["art_movement"] = "Synesthesia Inspired Art"
        imagen_settings["composition_settings"]["technique"] = "Abstract Representation of Sensory Crossovers (e.g., Sound to Color)"
        imagen_settings["color_settings"]["palette_type"] = "Vibrant Abstract Expressive Palette"
        imagen_settings["detail_settings"]["texture_quality"] = "Fluid Dynamic Textures"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Sensory", "Abstract", "Vibrant", "Fluid"]

    elif style_category == "ink_punk":
        imagen_settings["style_settings"]["art_movement"] = "Ink Punk Illustration"
        imagen_settings["composition_settings"]["technique"] = "Raw Sketchy High-Contrast Ink Lines"
        imagen_settings["color_settings"]["palette_type"] = "Black and White with Occasional Bold Color Splash"
        imagen_settings["detail_settings"]["texture_quality"] = "Rough Ink Splatter Texture"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Edgy", "Raw", "Energetic", "Sketchy"]

    # --- Game Styles ---
    elif style_category == "game_cel_shaded":
        imagen_settings["style_settings"]["art_movement"] = "Cel-Shaded Game Art"
        imagen_settings["composition_settings"]["technique"] = "Toon Shading with Bold Outlines"
        imagen_settings["color_settings"]["palette_type"] = "Bright Flat Anime-style Colors"
        imagen_settings["detail_settings"]["texture_quality"] = "Clean Flat Shading"
        imagen_settings["quality_settings"]["rendering_quality"] = "Stylized Game Render"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Stylized", "Anime", "Clean"]

    elif style_category == "game_retro":
        imagen_settings["style_settings"]["art_movement"] = "Retro Game Art (16-bit)"
        imagen_settings["composition_settings"]["technique"] = "Pixel Art Sprites and Backgrounds"
        imagen_settings["color_settings"]["palette_type"] = "Limited 16-bit Color Palette"
        imagen_settings["detail_settings"]["texture_quality"] = "Pixelated Texture"
        imagen_settings["quality_settings"]["rendering_quality"] = "Pixel Perfect"
        base_template["aspect_ratio"] = "4:3" # Common retro ratio
        base_template["moods"] = ["Retro", "Nostalgic", "Pixelated"]

    elif style_category == "game_style": # General Game Style
        imagen_settings["style_settings"]["art_movement"] = "Modern Game Concept Art"
        imagen_settings["composition_settings"]["technique"] = "Dynamic Composition for Games"
        imagen_settings["color_settings"]["palette_type"] = "Realistic or Stylized Game Palette"
        imagen_settings["detail_settings"]["detail_level"] = "High Detail for AAA Game"
        imagen_settings["quality_settings"]["rendering_quality"] = "High Quality Game Engine Render (Unreal Engine 5)"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Epic", "Adventurous", "Immersive"]

    # --- Cyberpunk ---
    elif style_category == "cyberpunk_action":
        imagen_settings["style_settings"]["art_movement"] = "Cyberpunk Action Scene"
        imagen_settings["composition_settings"]["technique"] = "Dynamic High-Energy Composition with Motion Blur"
        imagen_settings["color_settings"]["palette_type"] = "Neon Colors Contrasting with Dark Backgrounds"
        imagen_settings["lighting_settings"]["lighting_type"] = "Flashing Neon Lights and Muzzle Flashes"
        imagen_settings["environment_settings"]["atmospheric_effects"] = ["rain", "smoke", "glitch effects"]
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Intense", "Chaotic", "Futuristic"]

    # cyberpunk_cityscape handled above
    elif style_category == "cyberpunk_technology":
        imagen_settings["style_settings"]["art_movement"] = "Cyberpunk Technology Focus"
        imagen_settings["composition_settings"]["technique"] = "Detailed Close-up on Futuristic Tech/Interfaces"
        imagen_settings["color_settings"]["palette_type"] = "Cool Blues Purples with Glowing UI Elements"
        imagen_settings["lighting_settings"]["lighting_type"] = "Screen Glow and Holographic Light"
        imagen_settings["detail_settings"]["texture_quality"] = "Clean Metallic and Circuit Textures"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Futuristic", "Complex", "Digital"]

    elif style_category == "cyberpunk": # General Cyberpunk
        imagen_settings["style_settings"]["art_movement"] = "Cyberpunk"
        imagen_settings["composition_settings"]["technique"] = "High Tech Low Life Scene"
        imagen_settings["color_settings"]["palette_type"] = "Neon and Dark Moody Palette"
        imagen_settings["lighting_settings"]["lighting_type"] = "Neon Ambient Lighting"
        imagen_settings["environment_settings"]["location_type"] = "Gritty Futuristic City Street"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Dystopian", "Gritty", "Futuristic"]

    # --- Fantasy ---
    elif style_category == "fantasy_battle":
        imagen_settings["style_settings"]["art_movement"] = "Epic Fantasy Battle Scene"
        imagen_settings["composition_settings"]["technique"] = "Dynamic Multi-Figure Combat Composition"
        imagen_settings["color_settings"]["palette_type"] = "Rich Dramatic Contrasting Colors"
        imagen_settings["lighting_settings"]["lighting_type"] = "Dramatic Magical Lighting Effects"
        imagen_settings["environment_settings"]["atmospheric_effects"] = ["smoke", "magical energy", "debris"]
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Epic", "Chaotic", "Heroic"]

    elif style_category == "fantasy_cityscape":
        imagen_settings["style_settings"]["art_movement"] = "Fantasy Cityscape Architecture"
        imagen_settings["composition_settings"]["technique"] = "Wide Angle View of Magical City"
        imagen_settings["color_settings"]["palette_type"] = "Warm Mystical Jewel Tones"
        imagen_settings["lighting_settings"]["lighting_type"] = "Magical Ambient Glow and Torches"
        imagen_settings["environment_settings"]["location_type"] = "Elven or Ancient Magical City"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Magical", "Ancient", "Awe-inspiring"]

    # fantasy_landscape handled above
    elif style_category == "whimsical_fantasy":
        imagen_settings["style_settings"]["art_movement"] = "Whimsical Fantasy Illustration"
        imagen_settings["composition_settings"]["technique"] = "Playful Composition with Fantasy Elements"
        imagen_settings["color_settings"]["palette_type"] = "Soft Pastel Dreamy Palette"
        imagen_settings["lighting_settings"]["light_quality"] = "Soft Glowing Magical Light"
        imagen_settings["detail_settings"]["texture_quality"] = "Soft Painterly Textures"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Dreamy", "Playful", "Enchanting"]

    elif style_category == "fantasy": # General Fantasy
        imagen_settings["style_settings"]["art_movement"] = "High Fantasy Art"
        imagen_settings["composition_settings"]["technique"] = "Mythical Scene Composition"
        imagen_settings["color_settings"]["palette_type"] = "Rich Vibrant Fantasy Palette"
        imagen_settings["lighting_settings"]["lighting_type"] = "Dramatic Magical Lighting"
        imagen_settings["environment_settings"]["location_type"] = "Mythical Realm or Enchanted Forest"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Epic", "Magical", "Adventurous"]

    # --- Sci-Fi ---
    elif style_category == "sci_fi_futuristic":
        imagen_settings["style_settings"]["art_movement"] = "Futuristic Science Fiction"
        imagen_settings["composition_settings"]["technique"] = "Advanced Technology Focused Composition"
        imagen_settings["color_settings"]["palette_type"] = "Cool Metallic and Blue Palette with Neon Accents"
        imagen_settings["lighting_settings"]["lighting_type"] = "Artificial Clean Futuristic Lighting"
        imagen_settings["detail_settings"]["texture_quality"] = "Sleek Metal and Glass Textures"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Advanced", "Futuristic", "Clean"]

    elif style_category == "sci_fi": # General Sci-Fi
        imagen_settings["style_settings"]["art_movement"] = "Science Fiction Concept Art"
        imagen_settings["composition_settings"]["technique"] = "Futuristic Scene Composition"
        imagen_settings["color_settings"]["palette_type"] = "Varied Sci-Fi Palette (can be gritty or clean)"
        imagen_settings["lighting_settings"]["lighting_type"] = "Artificial or Alien World Lighting"
        imagen_settings["environment_settings"]["location_type"] = "Spaceship Interior or Alien Planet"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Futuristic", "Exploratory", "Technological"]

    # --- Specific Mediums/Techniques ---
    # claymation handled above
    # digital_collage handled above
    elif style_category == "experimental_mixed_media":
        imagen_settings["style_settings"]["art_movement"] = "Experimental Mixed Media Art"
        imagen_settings["composition_settings"]["technique"] = "Innovative Layering and Deconstruction"
        imagen_settings["color_settings"]["palette_type"] = "Eclectic Unpredictable Palette"
        imagen_settings["detail_settings"]["texture_quality"] = "Highly Varied and Contrasting Textures"
        base_template["aspect_ratio"] = "1:1" # Often experimental formats
        base_template["moods"] = ["Avant-Garde", "Unconventional", "Experimental"]

    # patchwork_fabric handled above
    # patchwork_collage handled above
    # papercraft handled above
    # ascii_art handled above
    # line_art handled above

    # --- Illustration Styles ---
    elif style_category == "illustration_pixar":
        imagen_settings["style_settings"]["art_movement"] = "Pixar Style 3D Illustration"
        imagen_settings["composition_settings"]["technique"] = "Appealing Character Design and Storytelling Composition"
        imagen_settings["color_settings"]["palette_type"] = "Bright Warm Saturated Palette"
        imagen_settings["lighting_settings"]["light_quality"] = "Soft Realistic 3D Lighting"
        imagen_settings["detail_settings"]["texture_quality"] = "Smooth Appealing 3D Textures"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Heartwarming", "Adventurous", "Family-Friendly"]

    elif style_category == "illustration_disney":
        imagen_settings["style_settings"]["art_movement"] = "Disney Style Illustration (Modern)"
        imagen_settings["composition_settings"]["technique"] = "Expressive Character Poses and Environments"
        imagen_settings["color_settings"]["palette_type"] = "Warm Soft Storybook Palette"
        imagen_settings["lighting_settings"]["light_quality"] = "Soft Magical Lighting"
        imagen_settings["detail_settings"]["texture_quality"] = "Clean Smooth Animation Textures"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Magical", "Charming", "Classic"]

    elif style_category == "illustration_tom_jerry":
        imagen_settings["style_settings"]["art_movement"] = "Classic Cartoon (Tom & Jerry Style)"
        imagen_settings["composition_settings"]["technique"] = "Slapstick Action Poses and Exaggerated Expressions"
        imagen_settings["color_settings"]["palette_type"] = "Bright Bold Primary Cartoon Colors"
        imagen_settings["lighting_settings"]["light_quality"] = "Flat Cartoon Lighting"
        imagen_settings["detail_settings"]["texture_quality"] = "Clean Flat Cartoon Textures"
        base_template["aspect_ratio"] = "4:3"
        base_template["moods"] = ["Comedic", "Energetic", "Slapstick"]

    elif style_category == "illustration_vintage_cartoon":
        imagen_settings["style_settings"]["art_movement"] = "Vintage Cartoon (Rubber Hose)"
        imagen_settings["composition_settings"]["technique"] = "Rubber Hose Limbs and Simple Character Designs"
        imagen_settings["color_settings"]["palette_type"] = "Black and White or Limited Muted Colors"
        imagen_settings["lighting_settings"]["light_quality"] = "Flat Simple Lighting"
        imagen_settings["post_processing"] = ["film grain", "slight flicker"]
        base_template["aspect_ratio"] = "4:3"
        base_template["moods"] = ["Nostalgic", "Bouncy", "Classic"]

    elif style_category == "illustration_anime_manga":
        imagen_settings["style_settings"]["art_movement"] = "Anime/Manga Illustration Style"
        imagen_settings["composition_settings"]["technique"] = "Dynamic Angles and Expressive Characters (Shonen Style)"
        imagen_settings["color_settings"]["palette_type"] = "Vibrant Saturated Anime Palette"
        imagen_settings["lighting_settings"]["light_quality"] = "Cel Shading with Sharp Highlights"
        imagen_settings["detail_settings"]["texture_quality"] = "Clean Lines and Flat Colors/Gradients"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Dynamic", "Expressive", "Action-Oriented"]

    elif style_category == "illustration_comic":
        imagen_settings["style_settings"]["art_movement"] = "Comic Book Art (Modern Age)"
        imagen_settings["composition_settings"]["technique"] = "Dynamic Panel-like Composition with Bold Lines"
        imagen_settings["color_settings"]["palette_type"] = "Bold Contrasting Comic Colors"
        imagen_settings["lighting_settings"]["light_quality"] = "Dramatic High Contrast Inking Shadows"
        imagen_settings["detail_settings"]["texture_quality"] = "Clean Inked Lines with Digital Coloring"
        base_template["aspect_ratio"] = "16:9" # Can vary
        base_template["moods"] = ["Heroic", "Dramatic", "Action-Packed"]

    elif style_category == "illustration_pixel":
        imagen_settings["style_settings"]["art_movement"] = "Pixel Art Illustration (16-bit)"
        imagen_settings["composition_settings"]["technique"] = "Careful Pixel Placement Isometric View"
        imagen_settings["color_settings"]["palette_type"] = "Limited 16-bit Color Palette (e.g., SNES/Genesis)"
        imagen_settings["detail_settings"]["texture_quality"] = "Pixelated Texture with Dithering"
        imagen_settings["quality_settings"]["rendering_quality"] = "Pixel Perfect"
        base_template["aspect_ratio"] = "1:1"
        base_template["moods"] = ["Retro", "Nostalgic", "Charming"]

    elif style_category == "illustration_steampunk":
        imagen_settings["style_settings"]["art_movement"] = "Steampunk Illustration"
        imagen_settings["composition_settings"]["technique"] = "Detailed Victorian Sci-Fi Scene"
        imagen_settings["color_settings"]["palette_type"] = "Sepia Tones Bronze and Brass Colors"
        imagen_settings["lighting_settings"]["light_quality"] = "Warm Atmospheric Gaslight"
        imagen_settings["detail_settings"]["texture_quality"] = "Intricate Mechanical Details Aged Metal"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Adventurous", "Mechanical", "Nostalgic"]

    elif style_category == "illustration_cubist":
        imagen_settings["style_settings"]["art_movement"] = "Cubist Illustration Style"
        imagen_settings["composition_settings"]["technique"] = "Geometric Abstraction Fragmented Perspective"
        imagen_settings["color_settings"]["palette_type"] = "Muted Earthy Tones with Geometric Accents"
        imagen_settings["detail_settings"]["texture_quality"] = "Flat Color Planes with Sharp Edges"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Abstract", "Analytical", "Geometric"]

    elif style_category == "illustration_surreal":
        imagen_settings["style_settings"]["art_movement"] = "Surrealist Illustration"
        imagen_settings["composition_settings"]["technique"] = "Dreamlike Narrative with Unexpected Juxtapositions"
        imagen_settings["color_settings"]["palette_type"] = "Vibrant Contrasting Dreamlike Palette"
        imagen_settings["lighting_settings"]["light_quality"] = "Mysterious Dramatic Lighting"
        imagen_settings["detail_settings"]["texture_quality"] = "Smooth Blended Textures with Sharp Details"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Dreamlike", "Mysterious", "Whimsical", "Uncanny"]

    elif style_category == "illustration_childrens":
        imagen_settings["style_settings"]["art_movement"] = "Children's Book Illustration"
        imagen_settings["composition_settings"]["technique"] = "Playful Characters in Simple Scenes"
        imagen_settings["color_settings"]["palette_type"] = "Bright Soft Primary Colors"
        imagen_settings["lighting_settings"]["light_quality"] = "Soft Flat Friendly Lighting"
        imagen_settings["detail_settings"]["texture_quality"] = "Clean Simple Textures often with Outlines"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Charming", "Friendly", "Playful", "Innocent"]

    elif style_category == "illustration_fantasy": # Non-portrait
        imagen_settings["style_settings"]["art_movement"] = "Fantasy Illustration"
        imagen_settings["composition_settings"]["technique"] = "Epic Scene with Mythical Creatures/Magic"
        imagen_settings["color_settings"]["palette_type"] = "Rich Jewel Tones and Earthy Colors"
        imagen_settings["lighting_settings"]["light_quality"] = "Dramatic Magical Light Source"
        imagen_settings["detail_settings"]["texture_quality"] = "Painterly Textures with Detailed Elements"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Epic", "Magical", "Adventurous"]

    elif style_category == "illustration_graphic":
        imagen_settings["style_settings"]["art_movement"] = "Graphic Illustration / Vector Art"
        imagen_settings["composition_settings"]["technique"] = "Bold Shapes Flat Design Principles"
        imagen_settings["color_settings"]["palette_type"] = "High Contrast Limited Color Palette"
        imagen_settings["lighting_settings"]["light_quality"] = "Flat Lighting Minimal Shading"
        imagen_settings["detail_settings"]["texture_quality"] = "Clean Vector Lines and Shapes"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Modern", "Clean", "Bold", "Graphic"]

    elif style_category == "illustration": # General Illustration
        imagen_settings["style_settings"]["art_movement"] = "Contemporary Illustration"
        imagen_settings["composition_settings"]["technique"] = "Stylized Representational Art"
        imagen_settings["color_settings"]["palette_type"] = "Balanced Expressive Palette"
        imagen_settings["lighting_settings"]["light_quality"] = "Stylized Lighting"
        imagen_settings["detail_settings"]["texture_quality"] = "Digital Painting or Ink Textures"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Expressive", "Narrative", "Stylized"]

    # --- Painting Styles ---
    elif style_category == "oil_painting":
        imagen_settings["style_settings"]["art_movement"] = "Traditional Oil Painting (Realism)"
        imagen_settings["composition_settings"]["technique"] = "Classical Composition with Realistic Detail"
        imagen_settings["color_settings"]["palette_type"] = "Warm Rich Traditional Oil Palette"
        imagen_settings["lighting_settings"]["light_quality"] = "Chiaroscuro Soft Transitions"
        imagen_settings["detail_settings"]["texture_quality"] = "Visible Canvas Texture and Oil Paint Impasto"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Classic", "Rich", "Realistic"]

    elif style_category == "watercolor":
        imagen_settings["style_settings"]["art_movement"] = "Watercolor Painting"
        imagen_settings["composition_settings"]["technique"] = "Transparent Washes and Wet-on-Wet Blending"
        imagen_settings["color_settings"]["palette_type"] = "Soft Light Translucent Palette"
        imagen_settings["lighting_settings"]["light_quality"] = "Natural Diffuse Light Preserving Whites"
        imagen_settings["detail_settings"]["texture_quality"] = "Watercolor Paper Grain and Pigment Granulation"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Light", "Fluid", "Transparent", "Delicate"]

    elif style_category == "pastel":
        imagen_settings["style_settings"]["art_movement"] = "Pastel Painting/Drawing"
        imagen_settings["composition_settings"]["technique"] = "Layered Blended Pastel Strokes"
        imagen_settings["color_settings"]["palette_type"] = "Soft Vibrant Pastel Palette"
        imagen_settings["lighting_settings"]["light_quality"] = "Soft Ambient Light"
        imagen_settings["detail_settings"]["texture_quality"] = "Soft Velvety Pastel Texture on Textured Paper"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Soft", "Vibrant", "Textured"]

    elif style_category == "acrylic_painting":
        imagen_settings["style_settings"]["art_movement"] = "Acrylic Painting (Modern)"
        imagen_settings["composition_settings"]["technique"] = "Bold Textured Brushwork or Flat Color Areas"
        imagen_settings["color_settings"]["palette_type"] = "Vibrant Opaque Acrylic Palette"
        imagen_settings["lighting_settings"]["light_quality"] = "Direct Bold Lighting"
        imagen_settings["detail_settings"]["texture_quality"] = "Visible Acrylic Texture or Smooth Flat Finish"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Bold", "Vibrant", "Modern"]

    elif style_category == "digital_painting":
        imagen_settings["style_settings"]["art_movement"] = "Digital Painting"
        imagen_settings["composition_settings"]["technique"] = "Painterly Style using Digital Brushes"
        imagen_settings["color_settings"]["palette_type"] = "Full Color Range with Digital Blending"
        imagen_settings["lighting_settings"]["light_quality"] = "Atmospheric Digital Lighting Effects"
        imagen_settings["detail_settings"]["texture_quality"] = "Custom Digital Brush Textures"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Painterly", "Digital", "Atmospheric"]

    # --- Drawing Styles ---
    elif style_category == "pencil_sketch":
        imagen_settings["style_settings"]["art_movement"] = "Pencil Sketch Realism"
        imagen_settings["composition_settings"]["technique"] = "Detailed Graphite Shading and Line Work"
        imagen_settings["color_settings"]["palette_type"] = "Monochrome Grayscale"
        imagen_settings["lighting_settings"]["light_quality"] = "Soft Natural Light Rendering Form"
        imagen_settings["detail_settings"]["texture_quality"] = "Graphite on Paper Texture"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Realistic", "Detailed", "Subtle"]

    elif style_category == "ink_drawing":
        imagen_settings["style_settings"]["art_movement"] = "Ink Drawing / Illustration"
        imagen_settings["composition_settings"]["technique"] = "Pen and Ink Linework with Cross-Hatching"
        imagen_settings["color_settings"]["palette_type"] = "High Contrast Black and White"
        imagen_settings["lighting_settings"]["light_quality"] = "Graphic High Contrast Lighting"
        imagen_settings["detail_settings"]["texture_quality"] = "Clean Ink Lines on Smooth Paper"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Graphic", "Bold", "Contrasting"]

    elif style_category == "charcoal":
        imagen_settings["style_settings"]["art_movement"] = "Charcoal Drawing"
        imagen_settings["composition_settings"]["technique"] = "Expressive Charcoal Smudging and Line Work"
        imagen_settings["color_settings"]["palette_type"] = "Rich Black and White Monochrome"
        imagen_settings["lighting_settings"]["light_quality"] = "Dramatic Chiaroscuro Lighting"
        imagen_settings["detail_settings"]["texture_quality"] = "Gritty Charcoal Texture on Textured Paper"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Dramatic", "Expressive", "Textured"]

    elif style_category == "drawing": # General Drawing
        imagen_settings["style_settings"]["art_movement"] = "Observational Drawing"
        imagen_settings["composition_settings"]["technique"] = "Hand-Drawn Sketch Composition"
        imagen_settings["color_settings"]["palette_type"] = "Grayscale or Limited Color"
        imagen_settings["lighting_settings"]["light_quality"] = "Natural Lighting"
        imagen_settings["detail_settings"]["texture_quality"] = "Sketchy Paper Texture"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Sketchy", "Observational", "Informal"]

    # --- Photographic Styles ---
    # street_photography, documentary, cinematic, photographic handled above by adding COMMON_CAMERA_SETTINGS

    # --- Abstract & Conceptual ---
    # minimalist_geometric handled above
    elif style_category == "minimalist":
        imagen_settings["style_settings"]["art_movement"] = "Minimalism"
        imagen_settings["composition_settings"]["technique"] = "Extreme Simplicity and Negative Space"
        imagen_settings["color_settings"]["palette_type"] = "Neutral Monochrome Palette"
        imagen_settings["lighting_settings"]["light_quality"] = "Flat Even Lighting"
        imagen_settings["detail_settings"]["detail_level"] = "Very Low"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Calm", "Clean", "Simple", "Elegant"]

    elif style_category == "geometric":
        imagen_settings["style_settings"]["art_movement"] = "Geometric Abstraction"
        imagen_settings["composition_settings"]["technique"] = "Composition based on Geometric Shapes and Patterns"
        imagen_settings["color_settings"]["palette_type"] = "Bold Contrasting Geometric Palette"
        imagen_settings["lighting_settings"]["light_quality"] = "Flat Graphic Lighting"
        imagen_settings["detail_settings"]["texture_quality"] = "Clean Sharp Edges Flat Colors"
        base_template["aspect_ratio"] = "1:1"
        base_template["moods"] = ["Structured", "Mathematical", "Modern"]

    elif style_category == "constructivism":
        imagen_settings["style_settings"]["art_movement"] = "Constructivism"
        imagen_settings["composition_settings"]["technique"] = "Geometric Industrial Design with Dynamic Angles"
        imagen_settings["color_settings"]["palette_type"] = "Limited Palette (Red, Black, White)"
        imagen_settings["lighting_settings"]["light_quality"] = "High Contrast Graphic"
        imagen_settings["detail_settings"]["texture_quality"] = "Clean Lines Bold Shapes"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Industrial", "Dynamic", "Avant-Garde"]

    elif style_category == "low_poly":
        imagen_settings["style_settings"]["art_movement"] = "Low Poly 3D Art"
        imagen_settings["composition_settings"]["technique"] = "Faceted Polygonal Mesh Composition"
        imagen_settings["color_settings"]["palette_type"] = "Bright Flat Color Palette"
        imagen_settings["lighting_settings"]["light_quality"] = "Simple Directional Lighting Showing Facets"
        imagen_settings["detail_settings"]["texture_quality"] = "Flat Shaded Polygon Texture"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Geometric", "Stylized", "Digital", "Retro 3D"]

    elif style_category == "abstract_conceptual":
        imagen_settings["style_settings"]["art_movement"] = "Abstract Conceptual Art"
        imagen_settings["composition_settings"]["technique"] = "Idea-Based Abstract Composition"
        imagen_settings["color_settings"]["palette_type"] = "Symbolic or Expressive Palette"
        imagen_settings["lighting_settings"]["light_quality"] = "Conceptual Lighting"
        imagen_settings["detail_settings"]["detail_level"] = "Varied based on concept"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Thought-provoking", "Symbolic", "Intellectual"]

    elif style_category == "abstract": # General Abstract
        imagen_settings["style_settings"]["art_movement"] = "Abstract Art (General)"
        imagen_settings["composition_settings"]["technique"] = "Non-Representational Forms and Colors"
        imagen_settings["color_settings"]["palette_type"] = "Expressive Varied Palette"
        imagen_settings["lighting_settings"]["light_quality"] = "Atmospheric or Flat Lighting"
        imagen_settings["detail_settings"]["texture_quality"] = "Painterly or Geometric Textures"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Expressive", "Dynamic", "Non-Objective"]

    # --- Other Distinct Styles ---
    elif style_category == "pop_surrealism":
        imagen_settings["style_settings"]["art_movement"] = "Pop Surrealism / Lowbrow Art"
        imagen_settings["composition_settings"]["technique"] = "Surreal Juxtaposition with Pop Culture/Cartoon Elements"
        imagen_settings["color_settings"]["palette_type"] = "Bright Saturated Contrasting Palette"
        imagen_settings["lighting_settings"]["light_quality"] = "Often Flat or Stylized Lighting"
        imagen_settings["detail_settings"]["detail_level"] = "Medium to High Detail"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Playful", "Bizarre", "Ironic", "Contemporary"]

    elif style_category == "surrealism":
        imagen_settings["style_settings"]["art_movement"] = "Surrealism"
        imagen_settings["composition_settings"]["technique"] = "Dreamlike Illogical Juxtapositions and Scenes"
        imagen_settings["color_settings"]["palette_type"] = "Varied, often Muted or Symbolic Palette"
        imagen_settings["lighting_settings"]["light_quality"] = "Dramatic Mysterious Lighting (Chiaroscuro)"
        imagen_settings["detail_settings"]["detail_level"] = "Often High Realistic Detail on Unreal Subjects"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Dreamlike", "Uncanny", "Mysterious", "Subconscious"]

    elif style_category == "cubism":
        imagen_settings["style_settings"]["art_movement"] = "Cubism (Analytical/Synthetic)"
        imagen_settings["composition_settings"]["technique"] = "Fragmented Forms Multiple Viewpoints Geometric Abstraction"
        imagen_settings["color_settings"]["palette_type"] = "Muted Earthy Tones or Later Bolder Colors"
        imagen_settings["lighting_settings"]["light_quality"] = "Simplified Abstracted Light"
        imagen_settings["detail_settings"]["texture_quality"] = "Geometric Planes Flat or Textured"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Analytical", "Fragmented", "Geometric", "Abstract"]

    elif style_category == "expressionism":
        imagen_settings["style_settings"]["art_movement"] = "Expressionism (e.g., German Expressionism)"
        imagen_settings["composition_settings"]["technique"] = "Emotive Distorted Forms and Bold Brushwork"
        imagen_settings["color_settings"]["palette_type"] = "Bold Dark Intense Emotional Palette"
        imagen_settings["lighting_settings"]["light_quality"] = "High Contrast Dramatic Lighting"
        imagen_settings["detail_settings"]["texture_quality"] = "Visible Impasto Energetic Brushstrokes"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Emotional", "Intense", "Subjective", "Anxious"]

    elif style_category == "fauvism":
        imagen_settings["style_settings"]["art_movement"] = "Fauvism"
        imagen_settings["composition_settings"]["technique"] = "Wild Brushwork Simplified Forms"
        imagen_settings["color_settings"]["palette_type"] = "Bright Vivid Non-Naturalistic Colors"
        imagen_settings["lighting_settings"]["light_quality"] = "Flat Strong Color Areas"
        imagen_settings["detail_settings"]["texture_quality"] = "Bold Visible Brushstrokes"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Wild", "Vibrant", "Expressive", "Bold"]

    elif style_category == "art_nouveau":
        imagen_settings["style_settings"]["art_movement"] = "Art Nouveau / Jugendstil"
        imagen_settings["composition_settings"]["technique"] = "Organic Flowing Lines Asymmetrical Composition"
        imagen_settings["color_settings"]["palette_type"] = "Muted Earthy Tones Pastels Gold Accents"
        imagen_settings["lighting_settings"]["light_quality"] = "Soft Decorative Lighting"
        imagen_settings["detail_settings"]["texture_quality"] = "Detailed Decorative Patterns Whiplash Lines"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Organic", "Decorative", "Elegant", "Flowing"]

    elif style_category == "art_deco":
        imagen_settings["style_settings"]["art_movement"] = "Art Deco"
        imagen_settings["composition_settings"]["technique"] = "Geometric Symmetry Streamlined Forms Rich Ornamentation"
        imagen_settings["color_settings"]["palette_type"] = "Bold Contrasting Colors Gold Silver Black"
        imagen_settings["lighting_settings"]["light_quality"] = "Glamorous Artificial Lighting"
        imagen_settings["detail_settings"]["texture_quality"] = "Luxurious Materials (simulated) Polished Surfaces"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Glamorous", "Luxurious", "Modernist", "Geometric"]

    elif style_category == "psychedelic":
        imagen_settings["style_settings"]["art_movement"] = "Psychedelic Art"
        imagen_settings["composition_settings"]["technique"] = "Swirling Fractal Kaleidoscopic Patterns Abstract Forms"
        imagen_settings["color_settings"]["palette_type"] = "Highly Saturated Vibrant Neon Contrasting Palette"
        imagen_settings["lighting_settings"]["light_quality"] = "Glowing Pulsating Light Effects"
        imagen_settings["post_processing"] = ["morphing effects", "vibrant color shifts"]
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Trippy", "Mind-Altering", "Vibrant", "Hallucinatory"]

    # steampunk handled above
    elif style_category == "dystopian":
        imagen_settings["style_settings"]["art_movement"] = "Dystopian Art"
        imagen_settings["composition_settings"]["technique"] = "Oppressive Environments Post-Apocalyptic Scenes Control vs Rebellion"
        imagen_settings["color_settings"]["palette_type"] = "Desaturated Gritty Muted Palette with Stark Contrasts"
        imagen_settings["lighting_settings"]["light_quality"] = "Harsh Artificial or Polluted Natural Light"
        imagen_settings["environment_settings"]["location_type"] = "Decaying Urban Landscape or Controlled Facility"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Oppressive", "Gritty", "Bleak", "Rebellious"]

    elif style_category == "glitch_art":
        imagen_settings["style_settings"]["art_movement"] = "Glitch Art"
        imagen_settings["composition_settings"]["technique"] = "Digital Errors Data Corruption Artifacts"
        imagen_settings["color_settings"]["palette_type"] = "Digital RGB/CMYK with Artifacts and Shifts"
        imagen_settings["lighting_settings"]["light_quality"] = "Digital Screen Glow with Errors"
        imagen_settings["post_processing"] = ["pixel sorting", "databending", "scanlines", "compression artifacts"]
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Digital", "Chaotic", "Deconstructed", "Erroneous"]

    elif style_category == "retrowave":
        imagen_settings["style_settings"]["art_movement"] = "Retrowave / Synthwave / Outrun"
        imagen_settings["composition_settings"]["technique"] = "80s Retrofuturism Neon Grids Sunsets Chrome"
        imagen_settings["color_settings"]["palette_type"] = "Neon Pinks Purples Cyans Oranges"
        imagen_settings["lighting_settings"]["light_quality"] = "Neon Glow Sunset Gradient"
        imagen_settings["environment_settings"]["location_type"] = "Retro Highway or Cityscape at Sunset"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Nostalgic", "Retro", "Futuristic (80s)", "Synth"]

    elif style_category == "vaporwave":
        imagen_settings["style_settings"]["art_movement"] = "Vaporwave"
        imagen_settings["composition_settings"]["technique"] = "90s Internet Aesthetics Classical Statues Glitch Japanese Text"
        imagen_settings["color_settings"]["palette_type"] = "Pastel Pinks Cyans Purples with Glitch"
        imagen_settings["lighting_settings"]["light_quality"] = "Soft Neon Glow Screen Glare"
        imagen_settings["post_processing"] = ["VHS artifacts", "glitch effects", "anemoia filters"]
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Nostalgic", "Surreal", "Ironic", "Aesthetic"]

    elif style_category == "dreamcore":
        imagen_settings["style_settings"]["art_movement"] = "Dreamcore"
        imagen_settings["composition_settings"]["technique"] = "Liminal Spaces Empty Environments Familiar but Off"
        imagen_settings["color_settings"]["palette_type"] = "Soft Pastels Desaturated Faded Colors"
        imagen_settings["lighting_settings"]["light_quality"] = "Soft Diffuse Hazy Ethereal Light"
        imagen_settings["quality_settings"]["rendering_quality"] = "Low-fidelity Soft Focus"
        base_template["aspect_ratio"] = "4:3" # Often has older aspect ratio feel
        base_template["moods"] = ["Dreamlike", "Nostalgic", "Eerie", "Liminal"]

    elif style_category == "weirdcore":
        imagen_settings["style_settings"]["art_movement"] = "Weirdcore"
        imagen_settings["composition_settings"]["technique"] = "Uncanny Juxtapositions Amateurish Aesthetic Found Images"
        imagen_settings["color_settings"]["palette_type"] = "Varied, often Muted or with Harsh Digital Colors"
        imagen_settings["lighting_settings"]["light_quality"] = "Often Flat Poor or Unsettling Lighting"
        imagen_settings["quality_settings"]["rendering_quality"] = "Low Quality Digital Artifacts Compression"
        base_template["aspect_ratio"] = "4:3" # Often uses older digital ratios
        base_template["moods"] = ["Uncanny", "Unsettling", "Absurd", "Nostalgic (distorted)"]

    elif style_category == "folk_art":
        imagen_settings["style_settings"]["art_movement"] = "Folk Art (e.g., Scandinavian, Mexican)"
        imagen_settings["composition_settings"]["technique"] = "Stylized Traditional Motifs Repetitive Patterns"
        imagen_settings["color_settings"]["palette_type"] = "Bold Simple Traditional Color Palette"
        imagen_settings["lighting_settings"]["light_quality"] = "Flat Decorative Lighting"
        imagen_settings["detail_settings"]["texture_quality"] = "Handcrafted Painted or Carved Texture"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Traditional", "Decorative", "Cultural", "Handcrafted"]

    elif style_category == "mediterranean_style":
        imagen_settings["style_settings"]["art_movement"] = "Mediterranean Style Painting"
        imagen_settings["composition_settings"]["technique"] = "Sunny Coastal Scenes Architecture Landscapes"
        imagen_settings["color_settings"]["palette_type"] = "Warm Bright Blues Whites Terracotta Ochre"
        imagen_settings["lighting_settings"]["light_quality"] = "Bright Natural Sunlight Strong Shadows"
        imagen_settings["detail_settings"]["texture_quality"] = "Stucco Texture Terracotta Tiles Painted Wood"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Sunny", "Warm", "Vibrant", "Coastal"]

    # --- Material/Sculptural ---
    elif style_category == "material_sculptural":
        imagen_settings["style_settings"]["art_movement"] = "Contemporary Sculpture"
        imagen_settings["composition_settings"]["technique"] = "Focus on Material Form and Texture in 3D Space"
        imagen_settings["color_settings"]["palette_type"] = "Natural Material Colors or Applied Patina/Paint"
        imagen_settings["lighting_settings"]["light_quality"] = "Dramatic Lighting to Emphasize Form and Texture"
        imagen_settings["detail_settings"]["texture_quality"] = "Realistic Material Texture (e.g., wood grain, metal sheen)"
        base_template["aspect_ratio"] = "1:1" # Often focused shots
        base_template["moods"] = ["Tactile", "Solid", "Form-focused"]

    elif style_category == "sculpture":
        imagen_settings["style_settings"]["art_movement"] = "Classical Sculpture (Simulated)"
        imagen_settings["composition_settings"]["technique"] = "Figurative Form in Marble or Bronze (Simulated)"
        imagen_settings["color_settings"]["palette_type"] = "Monochrome (Marble White or Bronze Patina)"
        imagen_settings["lighting_settings"]["light_quality"] = "Soft Directional Lighting Highlighting Form"
        imagen_settings["detail_settings"]["texture_quality"] = "Smooth Stone or Metal Texture"
        base_template["aspect_ratio"] = "3:4" # Common for statues
        base_template["moods"] = ["Classical", "Timeless", "Figurative"]

    # --- Broad Digital/Traditional ---
    # 3d_render handled above
    elif style_category == "vector_art":
        imagen_settings["style_settings"]["art_movement"] = "Vector Art / Graphic Design"
        imagen_settings["composition_settings"]["technique"] = "Clean Lines Flat Colors Gradients Geometric Shapes"
        imagen_settings["color_settings"]["palette_type"] = "Bright Graphic Design Palette or Limited Colors"
        imagen_settings["lighting_settings"]["light_quality"] = "Flat or Simple Gradient Shading"
        imagen_settings["detail_settings"]["texture_quality"] = "Smooth Scalable Vector Texture"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Clean", "Modern", "Graphic", "Scalable"]

    # digital_art handled above
    elif style_category == "traditional_painting_drawing":
        imagen_settings["style_settings"]["art_movement"] = "Traditional Art (General)"
        imagen_settings["composition_settings"]["technique"] = "Classical Composition Techniques"
        imagen_settings["color_settings"]["palette_type"] = "Traditional Pigment Palette"
        imagen_settings["lighting_settings"]["light_quality"] = "Naturalistic or Studio Lighting"
        imagen_settings["detail_settings"]["texture_quality"] = "Medium-Specific Texture (Canvas, Paper, Paint)"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Classic", "Timeless", "Handcrafted"]

    # --- Meta/Other ---
    elif style_category == "animal_inspired":
        imagen_settings["style_settings"]["art_movement"] = "Animal Inspired Art/Design"
        imagen_settings["composition_settings"]["technique"] = "Incorporating Animal Motifs Patterns or Forms"
        imagen_settings["color_settings"]["palette_type"] = "Palette Derived from Animal Colors/Environment"
        imagen_settings["detail_settings"]["texture_quality"] = "Textures Mimicking Fur Feathers Scales"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Natural", "Wild", "Organic"]

    elif style_category == "space_art":
        imagen_settings["style_settings"]["art_movement"] = "Space Art / Astronomical Art"
        imagen_settings["composition_settings"]["technique"] = "Depicting Nebulae Galaxies Planets Spaceships"
        imagen_settings["color_settings"]["palette_type"] = "Deep Blues Purples with Bright Stars/Nebulae Colors"
        imagen_settings["lighting_settings"]["light_quality"] = "Cosmic Glow Starlight Engine Glow"
        imagen_settings["environment_settings"]["location_type"] = "Outer Space Deep Space"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Awe-inspiring", "Cosmic", "Vast", "Mysterious"]

    elif style_category == "robot_art":
        imagen_settings["style_settings"]["art_movement"] = "Robot / Mecha Concept Art"
        imagen_settings["composition_settings"]["technique"] = "Detailed Mechanical Design Dynamic Poses"
        imagen_settings["color_settings"]["palette_type"] = "Metallic Greys Blues with Accent Colors (e.g., red lights)"
        imagen_settings["lighting_settings"]["light_quality"] = "Hard Lighting Showing Metal Sheen and Form"
        imagen_settings["detail_settings"]["texture_quality"] = "Metal Textures Wires Joints Weathering"
        base_template["aspect_ratio"] = "16:9"
        base_template["moods"] = ["Mechanical", "Futuristic", "Powerful", "Industrial"]

    # --- Default Fallback ---
    else: # Covers 'default' and 'unknown' or any other unhandled category
        # Provide a generic but complete structure
        imagen_settings[f"{style_category}_specific_settings"] = {
            "notable_features": f"Key features typical of the {style_category.replace('_',' ')} style.",
            "notes": f"Settings reflect common principles for {style_category.replace('_',' ')}."
        }
        if style_category == "default":
             base_template["preset_name"] = "Default Versatile Preset"
             imagen_settings["style_settings"]["art_movement"] = "General Purpose"
        elif style_category == "unknown":
             base_template["preset_name"] = "Unknown Style Exploration Preset"
             base_template["description"] = "A generic preset attempting to capture an undefined style."
             imagen_settings["style_settings"]["art_movement"] = "Undefined / Experimental"


    # Combine base and imagen settings
    final_template = {**base_template, "imagen_settings": imagen_settings}
    return final_template

# --- General Style Template Functions ---

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

def get_psychedelic_template(style_category: str) -> Dict[str, Any]:
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

def get_fantasy_template(style_category: str) -> Dict[str, Any]:
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
    imagen_settings["biopunk_settings"] = {
        "style_settings": {"art_movement": "Biopunk"},
        "composition_settings": {"technique": "Organic Technology Fusion with Body Horror Elements"},
        "color_settings": {"palette_type": "Dark Greens Browns Metallics with Sickly Neon Highlights"},
        "detail_settings": {"texture_quality": "Organic Slimy Textured Surfaces with Metal"},
        "base_template": {"aspect_ratio": "16:9"},
        "moods": ["Unsettling", "Gritty", "Organic", "Dystopian"]
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_kinetic_art_template(style_category: str) -> Dict[str, Any]:
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
    imagen_settings["kinetic_art_settings"] = {
        "style_settings": {"art_movement": "Kinetic Art"},
        "composition_settings": {"technique": "Art Incorporating Physical Movement or Illusion of Motion"},
        "color_settings": {"palette_type": "Dynamic Contrasting Colors"},
        "detail_settings": {"detail_level": "Medium to High Mechanical Detail"},
        "base_template": {"aspect_ratio": "16:9"},
        "moods": ["Dynamic", "Moving", "Mechanical"]
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_nightcore_template(style_category: str) -> Dict[str, Any]:
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
    imagen_settings["nightcore_settings"] = {
        "style_settings": {"art_movement": "Nightcore Aesthetic"},
        "composition_settings": {"technique": "High Energy Anime Visuals with Music Motifs"},
        "color_settings": {"palette_type": "Neon Pastels High-Contrast Palette"},
        "post_processing": ["glow effects", "fast motion blur", "audio visualizer elements"],
        "base_template": {"aspect_ratio": "16:9"},
        "moods": ["Energetic", "Fast-paced", "Edgy", "Futuristic"]
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_optic_art_template(style_category: str) -> Dict[str, Any]:
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
    imagen_settings["optic_art_settings"] = {
        "style_settings": {"art_movement": "Op Art (Optical Art)"},
        "composition_settings": {"technique": "Geometric Patterns Creating Optical Illusions (e.g., Moiré)"},
        "color_settings": {"palette_type": "High Contrast Black and White or Complementary Colors"},
        "detail_settings": {"detail_level": "Precise Geometric Detail"},
        "base_template": {"aspect_ratio": "1:1"},
        "moods": ["Dizzying", "Geometric", "Illusionary"]
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_ferrofluid_template(style_category: str) -> Dict[str, Any]:
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
    imagen_settings["ferrofluid_settings"] = {
        "style_settings": {"art_movement": "Ferrofluid Art"},
        "composition_settings": {"technique": "Magnetic Liquid Abstract Patterns"},
        "color_settings": {"palette_type": "Black Silver Metallic"},
        "detail_settings": {"texture_quality": "Spiky Glossy Liquid Metal Texture"},
        "base_template": {"aspect_ratio": "16:9"},
        "moods": ["Mesmerizing", "Scientific", "Abstract"]
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_animal_inspired_template(style_category: str) -> Dict[str, Any]:
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
    imagen_settings["animal_inspired_settings"] = {
        "style_settings": {"art_movement": "Animal Inspired Art/Design"},
        "composition_settings": {"technique": "Incorporating Animal Motifs Patterns or Forms"},
        "color_settings": {"palette_type": "Palette Derived from Animal Colors/Environment"},
        "detail_settings": {"texture_quality": "Textures Mimicking Fur Feathers Scales"},
        "base_template": {"aspect_ratio": "16:9"},
        "moods": ["Natural", "Wild", "Organic"]
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_abstract_conceptual_template(style_category: str) -> Dict[str, Any]:
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
    imagen_settings["abstract_settings"] = {
        "visual_elements": ["geometric shapes", "organic forms", "expressive lines"], "conceptual_approach": "exploring emotion through color and form",
        "balance_type": "asymmetric dynamic balance", "movement_type": "dynamic visual flow",
        "abstraction_level": "complete abstraction", "composition_complexity": "complex layered composition"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_material_sculptural_template(style_category: str) -> Dict[str, Any]:
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
    imagen_settings["material_settings"] = {
        "primary_material": "bronze (simulated)", "technique": "casting and carving (simulated)",
        "surface_quality": "polished with patina", "form_type": "organic figurative form",
        "dimensionality": "full-3D sculpture", "scale": "life-size scale", "finishing": "natural bronze patina"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_traditional_painting_drawing_template(style_category: str) -> Dict[str, Any]:
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
    imagen_settings["medium_settings"] = {
        "painting_medium": "oil paint", "support_type": "textured paper" if style_category == "charcoal" else "canvas",
        "technique": "hatching and smudging" if style_category == "charcoal" else "glazing and blending",
        "texture": "gritty charcoal texture" if style_category == "charcoal" else "oil paint texture",
        "layering_technique": "layered charcoal tones" if style_category == "charcoal" else "fat over lean",
        "stroke_style": "expressive textured strokes", "detail_approach": "medium realistic detail"
    }
    return {**base_template, "imagen_settings": imagen_settings}

# Example usage:
# if __name__ == '__main__':
#     # Need to define get_portrait_template here for testing if run standalone
#     # This is just a basic placeholder for the test block
#     def get_portrait_template(category: str) -> Dict[str, Any]:
#         return {"preset_name": f"{category} Portrait", "moods": ["Test"], "aspect_ratio": "3:4", "description": "Test", "imagen_settings": {}}
#
#     import json
#     test_style = "street_photography"
#     template = get_unique_style_template(test_style)
#     print(f"--- Template for: {test_style} ---")
#     print(json.dumps(template, indent=4)) # Should include camera_settings now
#
#     test_style_2 = "oil_painting" # Non-photographic
#     template_2 = get_unique_style_template(test_style_2)
#     print(f"\n--- Template for: {test_style_2} ---")
#     print(json.dumps(template_2, indent=4)) # Should NOT include camera_settings
