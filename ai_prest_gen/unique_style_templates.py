"""
Unique Style Templates Module for AI Preset Generator

This module contains unique style templates for all style categories,
each with concrete default values for all relevant settings.
"""

from typing import Dict, Any

def get_unique_style_template(style_category: str) -> Dict[str, Any]:
    style_category = style_category.lower()

    base_template = {
        "preset_name": f"{style_category.replace('_', ' ').title()} Unique Preset",
        "moods": ["Evocative"],
        "aspect_ratio": "16:9",
        "description": f"A unique preset tailored for the {style_category.replace('_', ' ')} style."
    }

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

    # Full list of style categories with specific customizations
    if style_category == "pop_surrealism_ascii":
        imagen_settings["style_settings"]["art_movement"] = "Pop Surrealism ASCII"
        imagen_settings["composition_settings"]["technique"] = "ASCII Art Composition"
        imagen_settings["color_settings"]["palette_type"] = "Monochrome"
        base_template["aspect_ratio"] = "4:3"

    elif style_category == "abstract_expressionism_cubism_fusion":
        imagen_settings["style_settings"]["art_movement"] = "Abstract Expressionism Cubism Fusion"
        imagen_settings["composition_settings"]["technique"] = "Fragmented Abstract"
        imagen_settings["color_settings"]["palette_type"] = "Bold and Contrasting"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "anime_oilpainting":
        imagen_settings["style_settings"]["art_movement"] = "Anime Oil Painting"
        imagen_settings["lighting_settings"]["lighting_type"] = "Soft Studio Lighting"
        imagen_settings["color_settings"]["palette_type"] = "Vibrant and Warm"
        base_template["aspect_ratio"] = "3:4"

    elif style_category == "retro_pixel_vaporwave":
        imagen_settings["style_settings"]["art_movement"] = "Retro Pixel Vaporwave"
        imagen_settings["color_settings"]["palette_type"] = "Neon Pastels"
        imagen_settings["composition_settings"]["technique"] = "Pixel Art"
        base_template["aspect_ratio"] = "1:1"

    elif style_category == "dreamcore_weirdcore":
        imagen_settings["style_settings"]["art_movement"] = "Dreamcore Weirdcore"
        imagen_settings["lighting_settings"]["lighting_type"] = "Soft and Diffused"
        imagen_settings["color_settings"]["palette_type"] = "Pastel and Muted"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "photorealism_glitch":
        imagen_settings["style_settings"]["art_movement"] = "Photorealism Glitch"
        imagen_settings["post_processing"] = ["glitch effects", "chromatic aberration"]
        imagen_settings["color_settings"]["palette_type"] = "Realistic with Digital Artifacts"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "watercolor_pencil":
        imagen_settings["style_settings"]["art_movement"] = "Watercolor Pencil"
        imagen_settings["lighting_settings"]["lighting_type"] = "Natural Window Light"
        imagen_settings["color_settings"]["palette_type"] = "Soft Pastels"
        base_template["aspect_ratio"] = "4:3"

    elif style_category == "cubism_futurism":
        imagen_settings["style_settings"]["art_movement"] = "Cubism Futurism"
        imagen_settings["composition_settings"]["technique"] = "Geometric and Dynamic"
        imagen_settings["color_settings"]["palette_type"] = "Bold and Metallic"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "digital_pixel_traditional":
        imagen_settings["style_settings"]["art_movement"] = "Digital Pixel Traditional"
        imagen_settings["composition_settings"]["technique"] = "Pixel Art with Traditional Elements"
        imagen_settings["color_settings"]["palette_type"] = "Mixed Palette"
        base_template["aspect_ratio"] = "1:1"

    elif style_category == "scientific_technological_hybrid":
        imagen_settings["style_settings"]["art_movement"] = "Scientific Technological Hybrid"
        imagen_settings["lighting_settings"]["lighting_type"] = "Artificial Lab Lighting"
        imagen_settings["color_settings"]["palette_type"] = "Cool Blues and Greys"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "psychedelic_surrealism":
        imagen_settings["style_settings"]["art_movement"] = "Psychedelic Surrealism"
        imagen_settings["post_processing"] = ["vibrant colors", "swirling patterns"]
        imagen_settings["color_settings"]["palette_type"] = "Vivid and Contrasting"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "morphism_surreal":
        imagen_settings["style_settings"]["art_movement"] = "Morphism Surreal"
        imagen_settings["composition_settings"]["technique"] = "Fluid Morphing Shapes"
        imagen_settings["color_settings"]["palette_type"] = "Soft and Dreamy"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "kinetic_ascii":
        imagen_settings["style_settings"]["art_movement"] = "Kinetic ASCII"
        imagen_settings["composition_settings"]["technique"] = "Animated ASCII Art"
        imagen_settings["color_settings"]["palette_type"] = "Monochrome"
        base_template["aspect_ratio"] = "4:3"

    elif style_category == "collage_digital_overlay":
        imagen_settings["style_settings"]["art_movement"] = "Collage Digital Overlay"
        imagen_settings["composition_settings"]["technique"] = "Layered Digital Collage"
        imagen_settings["color_settings"]["palette_type"] = "Eclectic"
        base_template["aspect_ratio"] = "1:1"

    elif style_category == "pixel_patchwork":
        imagen_settings["style_settings"]["art_movement"] = "Pixel Patchwork"
        imagen_settings["composition_settings"]["technique"] = "Patchwork Pixel Art"
        imagen_settings["color_settings"]["palette_type"] = "Varied"
        base_template["aspect_ratio"] = "1:1"

    elif style_category == "tradigital_mixed_media":
        imagen_settings["style_settings"]["art_movement"] = "Tradigital Mixed Media"
        imagen_settings["composition_settings"]["technique"] = "Mixed Traditional and Digital"
        imagen_settings["color_settings"]["palette_type"] = "Mixed Palette"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "hybrid_traditional_digital":
        imagen_settings["style_settings"]["art_movement"] = "Hybrid Traditional Digital"
        imagen_settings["composition_settings"]["technique"] = "Fusion of Traditional and Digital"
        imagen_settings["color_settings"]["palette_type"] = "Balanced"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "digital_traditional_fusion":
        imagen_settings["style_settings"]["art_movement"] = "Digital Traditional Fusion"
        imagen_settings["composition_settings"]["technique"] = "Blended Digital and Traditional"
        imagen_settings["color_settings"]["palette_type"] = "Balanced"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "caricature_portrait":
        imagen_settings["style_settings"]["art_movement"] = "Caricature Portrait"
        imagen_settings["composition_settings"]["technique"] = "Exaggerated Features"
        imagen_settings["color_settings"]["palette_type"] = "Vibrant"
        base_template["aspect_ratio"] = "3:4"

    elif style_category == "selfie_portrait":
        imagen_settings["style_settings"]["art_movement"] = "Selfie Portrait"
        imagen_settings["composition_settings"]["technique"] = "Casual and Spontaneous"
        imagen_settings["color_settings"]["palette_type"] = "Natural"
        base_template["aspect_ratio"] = "9:16"

    elif style_category == "environmental_portrait":
        imagen_settings["style_settings"]["art_movement"] = "Environmental Portrait"
        imagen_settings["composition_settings"]["technique"] = "Subject in Context"
        imagen_settings["color_settings"]["palette_type"] = "Natural"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "fashion_portrait":
        imagen_settings["style_settings"]["art_movement"] = "Fashion Portrait"
        imagen_settings["composition_settings"]["technique"] = "Editorial Style"
        imagen_settings["color_settings"]["palette_type"] = "Bold"
        base_template["aspect_ratio"] = "2:3"

    elif style_category == "conceptual_portrait":
        imagen_settings["style_settings"]["art_movement"] = "Conceptual Portrait"
        imagen_settings["composition_settings"]["technique"] = "Symbolic and Abstract"
        imagen_settings["color_settings"]["palette_type"] = "Muted"
        base_template["aspect_ratio"] = "1:1"

    elif style_category == "cyberpunk_portrait":
        imagen_settings["style_settings"]["art_movement"] = "Cyberpunk Portrait"
        imagen_settings["composition_settings"]["technique"] = "Neon and Tech"
        imagen_settings["color_settings"]["palette_type"] = "Electric Blues and Purples"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "futuristic_portrait":
        imagen_settings["style_settings"]["art_movement"] = "Futuristic Portrait"
        imagen_settings["composition_settings"]["technique"] = "Sci-Fi Elements"
        imagen_settings["color_settings"]["palette_type"] = "Cool Metallics"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "pop_portrait":
        imagen_settings["style_settings"]["art_movement"] = "Pop Portrait"
        imagen_settings["composition_settings"]["technique"] = "Bold Graphics"
        imagen_settings["color_settings"]["palette_type"] = "Primary Colors"
        base_template["aspect_ratio"] = "1:1"

    elif style_category == "illustration_portrait":
        imagen_settings["style_settings"]["art_movement"] = "Illustration Portrait"
        imagen_settings["composition_settings"]["technique"] = "Stylized Drawing"
        imagen_settings["color_settings"]["palette_type"] = "Vibrant"
        base_template["aspect_ratio"] = "4:5"

    elif style_category == "photographic_portrait":
        imagen_settings["style_settings"]["art_movement"] = "Photographic Portrait"
        imagen_settings["composition_settings"]["technique"] = "Realistic Photography"
        imagen_settings["color_settings"]["palette_type"] = "Natural"
        base_template["aspect_ratio"] = "3:4"

    elif style_category == "traditional_portrait":
        imagen_settings["style_settings"]["art_movement"] = "Traditional Portrait"
        imagen_settings["composition_settings"]["technique"] = "Classical Painting"
        imagen_settings["color_settings"]["palette_type"] = "Warm Earth Tones"
        base_template["aspect_ratio"] = "4:5"

    elif style_category == "fantasy_portrait":
        imagen_settings["style_settings"]["art_movement"] = "Fantasy Portrait"
        imagen_settings["composition_settings"]["technique"] = "Mythical and Magical"
        imagen_settings["color_settings"]["palette_type"] = "Rich Jewel Tones"
        base_template["aspect_ratio"] = "3:4"

    elif style_category == "noir_photography":
        imagen_settings["style_settings"]["art_movement"] = "Noir Photography"
        imagen_settings["composition_settings"]["technique"] = "High Contrast Black and White"
        imagen_settings["color_settings"]["palette_type"] = "Monochrome"
        base_template["aspect_ratio"] = "4:3"

    elif style_category == "art_deco_revival":
        imagen_settings["style_settings"]["art_movement"] = "Art Deco Revival"
        imagen_settings["composition_settings"]["technique"] = "Geometric and Glamorous"
        imagen_settings["color_settings"]["palette_type"] = "Gold and Black"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "augmented_reality_art":
        imagen_settings["style_settings"]["art_movement"] = "Augmented Reality Art"
        imagen_settings["composition_settings"]["technique"] = "Interactive and Immersive"
        imagen_settings["color_settings"]["palette_type"] = "Bright and Futuristic"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "biopunk":
        imagen_settings["style_settings"]["art_movement"] = "Biopunk"
        imagen_settings["composition_settings"]["technique"] = "Organic and Tech Fusion"
        imagen_settings["color_settings"]["palette_type"] = "Dark Greens and Metallics"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "ferrofluid":
        imagen_settings["style_settings"]["art_movement"] = "Ferrofluid"
        imagen_settings["composition_settings"]["technique"] = "Magnetic Liquid Patterns"
        imagen_settings["color_settings"]["palette_type"] = "Black and Silver"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "fractal_generative_art":
        imagen_settings["style_settings"]["art_movement"] = "Fractal Generative Art"
        imagen_settings["composition_settings"]["technique"] = "Recursive Patterns"
        imagen_settings["color_settings"]["palette_type"] = "Vibrant and Complex"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "installation_art":
        imagen_settings["style_settings"]["art_movement"] = "Installation Art"
        imagen_settings["composition_settings"]["technique"] = "Spatial and Environmental"
        imagen_settings["color_settings"]["palette_type"] = "Varied"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "kinetic_art":
        imagen_settings["style_settings"]["art_movement"] = "Kinetic Art"
        imagen_settings["composition_settings"]["technique"] = "Movement and Motion"
        imagen_settings["color_settings"]["palette_type"] = "Dynamic"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "luna_photo":
        imagen_settings["style_settings"]["art_movement"] = "Luna Photo"
        imagen_settings["composition_settings"]["technique"] = "Moonlit and Ethereal"
        imagen_settings["color_settings"]["palette_type"] = "Deep Blues and Silvers"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "mixed_media_journaling":
        imagen_settings["style_settings"]["art_movement"] = "Mixed Media Journaling"
        imagen_settings["composition_settings"]["technique"] = "Layered and Textured"
        imagen_settings["color_settings"]["palette_type"] = "Eclectic"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "nightcore":
        imagen_settings["style_settings"]["art_movement"] = "Nightcore"
        imagen_settings["composition_settings"]["technique"] = "High Energy and Vibrant"
        imagen_settings["color_settings"]["palette_type"] = "Neon and Pastels"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "optic_art":
        imagen_settings["style_settings"]["art_movement"] = "Optic Art"
        imagen_settings["composition_settings"]["technique"] = "Optical Illusions"
        imagen_settings["color_settings"]["palette_type"] = "Black and White"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "paper_quilling":
        imagen_settings["style_settings"]["art_movement"] = "Paper Quilling"
        imagen_settings["composition_settings"]["technique"] = "Rolled Paper Art"
        imagen_settings["color_settings"]["palette_type"] = "Bright and Pastel"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "phygital_hybrid":
        imagen_settings["style_settings"]["art_movement"] = "Phygital Hybrid"
        imagen_settings["composition_settings"]["technique"] = "Physical and Digital Fusion"
        imagen_settings["color_settings"]["palette_type"] = "Mixed"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "screen_printing_bold":
        imagen_settings["style_settings"]["art_movement"] = "Screen Printing Bold"
        imagen_settings["composition_settings"]["technique"] = "Bold Graphic Prints"
        imagen_settings["color_settings"]["palette_type"] = "High Contrast"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "synesthesia_art":
        imagen_settings["style_settings"]["art_movement"] = "Synesthesia Art"
        imagen_settings["composition_settings"]["technique"] = "Sensory Crossovers"
        imagen_settings["color_settings"]["palette_type"] = "Vibrant and Abstract"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "ink_punk":
        imagen_settings["style_settings"]["art_movement"] = "Ink Punk"
        imagen_settings["composition_settings"]["technique"] = "Raw Ink Sketches"
        imagen_settings["color_settings"]["palette_type"] = "Black and White"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "game_cel_shaded":
        imagen_settings["style_settings"]["art_movement"] = "Game Cel Shaded"
        imagen_settings["composition_settings"]["technique"] = "Toon Shading"
        imagen_settings["color_settings"]["palette_type"] = "Bright and Flat"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "game_retro":
        imagen_settings["style_settings"]["art_movement"] = "Game Retro"
        imagen_settings["composition_settings"]["technique"] = "Pixel Art"
        imagen_settings["color_settings"]["palette_type"] = "Limited Palette"
        base_template["aspect_ratio"] = "1:1"

    elif style_category == "game_style":
        imagen_settings["style_settings"]["art_movement"] = "Game Style"
        imagen_settings["composition_settings"]["technique"] = "Varied Game Aesthetics"
        imagen_settings["color_settings"]["palette_type"] = "Varied"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "cyberpunk_action":
        imagen_settings["style_settings"]["art_movement"] = "Cyberpunk Action"
        imagen_settings["composition_settings"]["technique"] = "Dynamic and Neon"
        imagen_settings["color_settings"]["palette_type"] = "Neon Colors"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "cyberpunk_cityscape":
        imagen_settings["style_settings"]["art_movement"] = "Cyberpunk Cityscape"
        imagen_settings["composition_settings"]["technique"] = "Dense Urban Neon"
        imagen_settings["color_settings"]["palette_type"] = "Vibrant Neon"
        base_template["aspect_ratio"] = "21:9"

    elif style_category == "cyberpunk_technology":
        imagen_settings["style_settings"]["art_movement"] = "Cyberpunk Technology"
        imagen_settings["composition_settings"]["technique"] = "Futuristic Tech"
        imagen_settings["color_settings"]["palette_type"] = "Cool Blues and Purples"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "cyberpunk":
        imagen_settings["style_settings"]["art_movement"] = "Cyberpunk"
        imagen_settings["composition_settings"]["technique"] = "High Tech Low Life"
        imagen_settings["color_settings"]["palette_type"] = "Neon and Dark"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "fantasy_battle":
        imagen_settings["style_settings"]["art_movement"] = "Fantasy Battle"
        imagen_settings["composition_settings"]["technique"] = "Epic Combat Scenes"
        imagen_settings["color_settings"]["palette_type"] = "Rich and Dramatic"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "fantasy_cityscape":
        imagen_settings["style_settings"]["art_movement"] = "Fantasy Cityscape"
        imagen_settings["composition_settings"]["technique"] = "Magical Urban Scenes"
        imagen_settings["color_settings"]["palette_type"] = "Warm and Mystical"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "fantasy_landscape":
        imagen_settings["style_settings"]["art_movement"] = "Fantasy Landscape"
        imagen_settings["composition_settings"]["technique"] = "Enchanted Nature"
        imagen_settings["color_settings"]["palette_type"] = "Jewel Tones"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "whimsical_fantasy":
        imagen_settings["style_settings"]["art_movement"] = "Whimsical Fantasy"
        imagen_settings["composition_settings"]["technique"] = "Playful and Dreamy"
        imagen_settings["color_settings"]["palette_type"] = "Pastels"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "fantasy":
        imagen_settings["style_settings"]["art_movement"] = "Fantasy"
        imagen_settings["composition_settings"]["technique"] = "Mythical and Magical"
        imagen_settings["color_settings"]["palette_type"] = "Rich and Vibrant"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "sci_fi_futuristic":
        imagen_settings["style_settings"]["art_movement"] = "Sci-Fi Futuristic"
        imagen_settings["composition_settings"]["technique"] = "Advanced Technology"
        imagen_settings["color_settings"]["palette_type"] = "Cool and Metallic"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "sci_fi":
        imagen_settings["style_settings"]["art_movement"] = "Sci-Fi"
        imagen_settings["composition_settings"]["technique"] = "Futuristic Concepts"
        imagen_settings["color_settings"]["palette_type"] = "Varied"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "claymation":
        imagen_settings["style_settings"]["art_movement"] = "Claymation"
        imagen_settings["composition_settings"]["technique"] = "Stop Motion Clay"
        imagen_settings["color_settings"]["palette_type"] = "Earthy and Soft"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "experimental_mixed_media":
        imagen_settings["style_settings"]["art_movement"] = "Experimental Mixed Media"
        imagen_settings["composition_settings"]["technique"] = "Innovative and Layered"
        imagen_settings["color_settings"]["palette_type"] = "Eclectic"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "patchwork_fabric":
        imagen_settings["style_settings"]["art_movement"] = "Patchwork Fabric"
        imagen_settings["composition_settings"]["technique"] = "Textile Patchwork"
        imagen_settings["color_settings"]["palette_type"] = "Warm and Varied"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "patchwork_collage":
        imagen_settings["style_settings"]["art_movement"] = "Patchwork Collage"
        imagen_settings["composition_settings"]["technique"] = "Layered Collage"
        imagen_settings["color_settings"]["palette_type"] = "Mixed"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "papercraft":
        imagen_settings["style_settings"]["art_movement"] = "Papercraft"
        imagen_settings["composition_settings"]["technique"] = "Paper Folding and Cutting"
        imagen_settings["color_settings"]["palette_type"] = "Bright and Clean"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "ascii_art":
        imagen_settings["style_settings"]["art_movement"] = "ASCII Art"
        imagen_settings["composition_settings"]["technique"] = "Text-based Imagery"
        imagen_settings["color_settings"]["palette_type"] = "Monochrome"
        base_template["aspect_ratio"] = "4:3"

    elif style_category == "line_art":
        imagen_settings["style_settings"]["art_movement"] = "Line Art"
        imagen_settings["composition_settings"]["technique"] = "Clean Outlines"
        imagen_settings["color_settings"]["palette_type"] = "Black and White"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "illustration_pixar":
        imagen_settings["style_settings"]["art_movement"] = "Illustration Pixar"
        imagen_settings["composition_settings"]["technique"] = "3D Animation Style"
        imagen_settings["color_settings"]["palette_type"] = "Bright and Warm"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "illustration_disney":
        imagen_settings["style_settings"]["art_movement"] = "Illustration Disney"
        imagen_settings["composition_settings"]["technique"] = "Classic Animation Style"
        imagen_settings["color_settings"]["palette_type"] = "Warm and Soft"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "illustration_tom_jerry":
        imagen_settings["style_settings"]["art_movement"] = "Illustration Tom Jerry"
        imagen_settings["composition_settings"]["technique"] = "Classic Cartoon Style"
        imagen_settings["color_settings"]["palette_type"] = "Bright and Bold"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "illustration_vintage_cartoon":
        imagen_settings["style_settings"]["art_movement"] = "Illustration Vintage Cartoon"
        imagen_settings["composition_settings"]["technique"] = "Rubber Hose Animation"
        imagen_settings["color_settings"]["palette_type"] = "Black and White"
        base_template["aspect_ratio"] = "4:3"

    elif style_category == "illustration_anime_manga":
        imagen_settings["style_settings"]["art_movement"] = "Illustration Anime Manga"
        imagen_settings["composition_settings"]["technique"] = "Stylized Anime"
        imagen_settings["color_settings"]["palette_type"] = "Vibrant and Saturated"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "illustration_comic":
        imagen_settings["style_settings"]["art_movement"] = "Illustration Comic"
        imagen_settings["composition_settings"]["technique"] = "Comic Book Style"
        imagen_settings["color_settings"]["palette_type"] = "Bold and Contrasting"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "illustration_pixel":
        imagen_settings["style_settings"]["art_movement"] = "Illustration Pixel"
        imagen_settings["composition_settings"]["technique"] = "Pixel Art"
        imagen_settings["color_settings"]["palette_type"] = "Limited Palette"
        base_template["aspect_ratio"] = "1:1"

    elif style_category == "illustration_steampunk":
        imagen_settings["style_settings"]["art_movement"] = "Illustration Steampunk"
        imagen_settings["composition_settings"]["technique"] = "Victorian Sci-Fi"
        imagen_settings["color_settings"]["palette_type"] = "Sepia and Bronze"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "illustration_cubist":
        imagen_settings["style_settings"]["art_movement"] = "Illustration Cubist"
        imagen_settings["composition_settings"]["technique"] = "Geometric Abstraction"
        imagen_settings["color_settings"]["palette_type"] = "Muted and Earthy"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "illustration_surreal":
        imagen_settings["style_settings"]["art_movement"] = "Illustration Surreal"
        imagen_settings["composition_settings"]["technique"] = "Dreamlike and Abstract"
        imagen_settings["color_settings"]["palette_type"] = "Vibrant and Contrasting"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "illustration_childrens":
        imagen_settings["style_settings"]["art_movement"] = "Illustration Childrens"
        imagen_settings["composition_settings"]["technique"] = "Playful and Colorful"
        imagen_settings["color_settings"]["palette_type"] = "Bright and Soft"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "illustration_fantasy":
        imagen_settings["style_settings"]["art_movement"] = "Illustration Fantasy"
        imagen_settings["composition_settings"]["technique"] = "Mythical and Magical"
        imagen_settings["color_settings"]["palette_type"] = "Rich and Vibrant"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "illustration_graphic":
        imagen_settings["style_settings"]["art_movement"] = "Illustration Graphic"
        imagen_settings["composition_settings"]["technique"] = "Bold Graphic Design"
        imagen_settings["color_settings"]["palette_type"] = "High Contrast"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "oil_painting":
        imagen_settings["style_settings"]["art_movement"] = "Oil Painting"
        imagen_settings["composition_settings"]["technique"] = "Classical Oil"
        imagen_settings["color_settings"]["palette_type"] = "Warm and Rich"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "watercolor":
        imagen_settings["style_settings"]["art_movement"] = "Watercolor"
        imagen_settings["composition_settings"]["technique"] = "Soft Washes"
        imagen_settings["color_settings"]["palette_type"] = "Pastel and Light"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "pastel":
        imagen_settings["style_settings"]["art_movement"] = "Pastel"
        imagen_settings["composition_settings"]["technique"] = "Soft and Blended"
        imagen_settings["color_settings"]["palette_type"] = "Soft and Muted"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "acrylic_painting":
        imagen_settings["style_settings"]["art_movement"] = "Acrylic Painting"
        imagen_settings["composition_settings"]["technique"] = "Bold and Textured"
        imagen_settings["color_settings"]["palette_type"] = "Vibrant and Opaque"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "digital_painting":
        imagen_settings["style_settings"]["art_movement"] = "Digital Painting"
        imagen_settings["composition_settings"]["technique"] = "Painterly Digital"
        imagen_settings["color_settings"]["palette_type"] = "Varied"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "pencil_sketch":
        imagen_settings["style_settings"]["art_movement"] = "Pencil Sketch"
        imagen_settings["composition_settings"]["technique"] = "Graphite Drawing"
        imagen_settings["color_settings"]["palette_type"] = "Monochrome"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "ink_drawing":
        imagen_settings["style_settings"]["art_movement"] = "Ink Drawing"
        imagen_settings["composition_settings"]["technique"] = "Pen and Ink"
        imagen_settings["color_settings"]["palette_type"] = "Black and White"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "charcoal":
        imagen_settings["style_settings"]["art_movement"] = "Charcoal"
        imagen_settings["composition_settings"]["technique"] = "Charcoal Sketch"
        imagen_settings["color_settings"]["palette_type"] = "Monochrome"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "drawing":
        imagen_settings["style_settings"]["art_movement"] = "Drawing"
        imagen_settings["composition_settings"]["technique"] = "Hand Drawing"
        imagen_settings["color_settings"]["palette_type"] = "Varied"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "street_photography":
        imagen_settings["style_settings"]["art_movement"] = "Street Photography"
        imagen_settings["composition_settings"]["technique"] = "Candid Urban"
        imagen_settings["color_settings"]["palette_type"] = "Natural"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "documentary":
        imagen_settings["style_settings"]["art_movement"] = "Documentary"
        imagen_settings["composition_settings"]["technique"] = "Real Life"
        imagen_settings["color_settings"]["palette_type"] = "Natural"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "cinematic":
        imagen_settings["style_settings"]["art_movement"] = "Cinematic"
        imagen_settings["composition_settings"]["technique"] = "Film Still"
        imagen_settings["color_settings"]["palette_type"] = "Teal and Orange"
        base_template["aspect_ratio"] = "2.39:1"

    elif style_category == "photographic":
        imagen_settings["style_settings"]["art_movement"] = "Photographic"
        imagen_settings["composition_settings"]["technique"] = "Realistic Photography"
        imagen_settings["color_settings"]["palette_type"] = "Natural"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "minimalist_geometric":
        imagen_settings["style_settings"]["art_movement"] = "Minimalist Geometric"
        imagen_settings["composition_settings"]["technique"] = "Simple Shapes"
        imagen_settings["color_settings"]["palette_type"] = "Monochrome"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "minimalist":
        imagen_settings["style_settings"]["art_movement"] = "Minimalist"
        imagen_settings["composition_settings"]["technique"] = "Clean and Simple"
        imagen_settings["color_settings"]["palette_type"] = "Neutral"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "geometric":
        imagen_settings["style_settings"]["art_movement"] = "Geometric"
        imagen_settings["composition_settings"]["technique"] = "Geometric Patterns"
        imagen_settings["color_settings"]["palette_type"] = "Varied"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "constructivism":
        imagen_settings["style_settings"]["art_movement"] = "Constructivism"
        imagen_settings["composition_settings"]["technique"] = "Geometric Avant-Garde"
        imagen_settings["color_settings"]["palette_type"] = "Red, Black, White"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "low_poly":
        imagen_settings["style_settings"]["art_movement"] = "Low Poly"
        imagen_settings["composition_settings"]["technique"] = "Faceted Polygon"
        imagen_settings["color_settings"]["palette_type"] = "Bright and Flat"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "abstract_conceptual":
        imagen_settings["style_settings"]["art_movement"] = "Abstract Conceptual"
        imagen_settings["composition_settings"]["technique"] = "Abstract Forms"
        imagen_settings["color_settings"]["palette_type"] = "Varied"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "abstract":
        imagen_settings["style_settings"]["art_movement"] = "Abstract"
        imagen_settings["composition_settings"]["technique"] = "Non-Objective"
        imagen_settings["color_settings"]["palette_type"] = "Varied"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "pop_surrealism":
        imagen_settings["style_settings"]["art_movement"] = "Pop Surrealism"
        imagen_settings["composition_settings"]["technique"] = "Surreal and Playful"
        imagen_settings["color_settings"]["palette_type"] = "Bright and Contrasting"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "surrealism":
        imagen_settings["style_settings"]["art_movement"] = "Surrealism"
        imagen_settings["composition_settings"]["technique"] = "Dreamlike and Bizarre"
        imagen_settings["color_settings"]["palette_type"] = "Varied"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "cubism":
        imagen_settings["style_settings"]["art_movement"] = "Cubism"
        imagen_settings["composition_settings"]["technique"] = "Fragmented Forms"
        imagen_settings["color_settings"]["palette_type"] = "Muted"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "expressionism":
        imagen_settings["style_settings"]["art_movement"] = "Expressionism"
        imagen_settings["composition_settings"]["technique"] = "Emotive Brushwork"
        imagen_settings["color_settings"]["palette_type"] = "Bold and Dark"
        base_template["aspect_ratio"] = "16:9"

    elif style_category == "fauvism":
        imagen_settings["style_settings"]["art_movement"] = "Fauvism"
        imagen_settings["composition_settings"]["technique"] = "Wild Brushwork"
        imagen_settings["color_settings"]["palette_type"] = "Bright and Vivid"
        base_template["aspect_ratio"] = "16:9"
