"""
Portrait Style Templates Module for AI Preset Generator.

This module is dedicated to providing detailed and nuanced base templates for a
wide variety of portrait styles. The primary function, `get_portrait_template`,
acts as a dispatcher, returning a specific template dictionary based on the
provided `style_category`.

Styles covered include:
- Photographic Portrait (and various sub-genres like environmental, fashion)
- Traditional Portrait (e.g., oil painting likeness)
- Futuristic/Cyberpunk Portrait
- Illustrative Portrait
- Pop Art Portrait
- Caricature Portrait
- Conceptual Portrait
- Selfie Portrait
And more, each with tailored settings.
"""

from typing import Dict, Any

def get_portrait_template(style_category: str) -> Dict[str, Any]:
    """
    Returns a detailed JSON-like template for a specific portrait style category.

    The function normalizes the input `style_category` and then uses a series
    of conditional checks to select and customize a base template for that
    particular portrait sub-style (e.g., "photographic_portrait", 
    "traditional_portrait", "cyberpunk_portrait").

    Each returned template includes a `preset_name`, `moods`, `aspect_ratio`,
    `description`, and a comprehensive `imagen_settings` dictionary with
    style-specific configurations for art movement, lighting, composition,
    color, detail, environment, quality, negative prompts, and potentially
    camera settings or medium-specific details.

    Args:
        style_category (str): The normalized (lowercase) name of the specific
                              portrait style category for which to generate a template.

    Returns:
        Dict[str, Any]: A dictionary containing the preset template tailored
                        for the specified portrait style.
    """
    style_category = style_category.lower() # Normalize for matching

    base_template = {
        "preset_name": f"{style_category.replace('_', ' ').title()} Portrait",
        "moods": ["Expressive"],
        "aspect_ratio": "3:4",
        "description": f"A detailed portrait preset in the {style_category.replace('_', ' ')} style, focusing on character and mood."
    }

    imagen_settings = {
        "style_settings": {
            "art_movement": "Contemporary Portraiture",
            "post_processing": ["subtle skin smoothing", "sharpening eyes"],
            "style_era": "Modern"
        },
        "lighting_settings": {
            "lighting_type": "Studio Lighting",
            "light_quality": "Soft and Diffused",
            "light_direction": "Front-Side (45 degrees)"
        },
        "composition_settings": {
            "technique": "Close-up Headshot",
            "focal_point": "Eyes and Facial Expression"
        },
        "color_settings": {
            "color_scheme": "Natural Skin Tones",
            "palette_type": "Realistic and Balanced",
            "color_temperature": "Neutral",
            "color_contrast": "Medium"
        },
        "detail_settings": {
            "detail_level": "High",
            "texture_quality": "Realistic Skin Texture"
        },
        "environment_settings": {
            "weather": "N/A",
            "season": "N/A",
            "location_type": "Studio Backdrop (neutral)",
            "atmospheric_effects": ["none"]
        },
        "quality_settings": {
            "resolution": "4000x5000",
            "rendering_quality": "Photorealistic"
        },
        "negative_prompt": "blurry, deformed, extra limbs, poorly drawn face, bad anatomy, signature, text, watermark, low quality, unrealistic features (unless style dictates), distorted eyes",
        "style_negative_prompt": "clashing art styles, inconsistent lighting for portraiture, unflattering angles, generic look"
    }

    PORTRAIT_CAMERA_SETTINGS = {
        "camera_model": "DSLR (e.g., Canon EOS 5D Mark IV)", "lens_type": "Prime Lens (e.g., 85mm)",
        "aperture": "f/1.8", "focal_length": "85mm", "shutter_speed": "1/160s", "iso": "ISO 100",
        "filter_type": "None", "depth_of_field": "Shallow (bokeh background)", "white_balance": "Daylight (5500K)",
        "focus_mode": "Eye Autofocus (Eye AF)", "exposure_mode": "Manual (M)", "image_stabilization": "In-Lens (IS)",
        "metering_mode": "Spot Metering (on face)", "flash_mode": "Off-Camera Flash (Softbox Key Light)",
        "shooting_mode": "Single Shot", "focus_point_selection": "Single Point AF (on eye)",
        "image_format": "RAW", "color_space": "Adobe RGB"
    }

    if style_category == "photographic_portrait":
        imagen_settings["camera_settings"] = PORTRAIT_CAMERA_SETTINGS.copy()
        imagen_settings["lighting_settings"]["lighting_type"] = "Studio Strobe with Softbox"
        imagen_settings["lighting_settings"]["light_quality"] = "Soft and Diffused with Catchlights"
        imagen_settings["style_settings"]["photo_style"] = "Contemporary Photographic Portrait"
        imagen_settings["quality_settings"]["rendering_quality"] = "High-Fidelity Photorealistic"
        imagen_settings["detail_settings"]["texture_quality"] = "Natural Skin Pores and Hair Detail"
        imagen_settings["color_settings"]["palette_type"] = "Accurate and Rich Skin Tones"
        imagen_settings["environment_settings"]["location_type"] = "Studio with Plain Backdrop (e.g., grey, white)"

    elif style_category == "traditional_portrait":
        base_template["aspect_ratio"] = "4:5"
        imagen_settings["medium_settings"] = {
            "painting_medium": "Oil Paint", "support_type": "Canvas",
            "brushwork_style": "Visible Brushstrokes with Blending", "texture_application": "Textured Canvas with Layered Paint",
            "layering_technique": "Glazing and Scumbling", "stroke_style": "Expressive and Deliberate",
            "detail_approach": "High Realism with Artistic Interpretation"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "Natural Window Light (North Light)"
        imagen_settings["lighting_settings"]["light_quality"] = "Chiaroscuro with Soft Transitions"
        imagen_settings["style_settings"]["art_movement"] = "Realism (e.g., 19th Century)"
        imagen_settings["style_settings"]["painter_influence"] = "John Singer Sargent"
        imagen_settings["style_settings"]["period"] = "Late 19th Century"
        imagen_settings["color_settings"]["palette_type"] = "Warm Earth Tones and Rich Colors"
        imagen_settings["detail_settings"]["texture_quality"] = "Painted Fabric Textures, Rendered Skin and Hair"

    elif style_category == "futuristic_portrait" or style_category == "cyberpunk_portrait":
        base_template["aspect_ratio"] = "16:9"
        imagen_settings["futuristic_elements"] = {
            "character_archetype": "Cyborg with Visible Augmentations", "costuming_details": "Tech-wear with Integrated LED Elements",
            "cybernetic_enhancements": "Glowing Optical Sensors and Data Ports", "background_setting": "Neon-drenched Cityscape Alleyway",
            "dominant_mood": "Stoic and Intense"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "Neon Glow and Holographic Projections"
        imagen_settings["lighting_settings"]["light_quality"] = "Harsh Contrast with Rim Lighting"
        imagen_settings["color_settings"]["palette_type"] = "Electric Blues, Purples, and Cyans with Metallic Sheens"
        imagen_settings["detail_settings"]["detail_level"] = "Intricate Tech Details and Textures"
        imagen_settings["detail_settings"]["texture_quality"] = "Metallic Surfaces, Carbon Fiber, Glowing Circuits"
        imagen_settings["style_settings"]["art_movement"] = "Cyberpunk Art"

    elif style_category == "illustration_portrait":
        base_template["aspect_ratio"] = "4:5"
        imagen_settings["illustration_specifics"] = {
            "line_work_style": "Clean and Crisp Outlines", "coloring_method": "Cel Shading with Soft Gradient Highlights",
            "overall_visual_style": "Stylized Realism (Anime-inspired)", "level_of_detail": "Medium, focusing on character expression",
            "subject_portrayal": "Expressive Character with a Narrative Hint"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "Stylized Rim Lighting and Ambient Occlusion"
        imagen_settings["color_settings"]["palette_type"] = "Vibrant and Saturated Thematic Palette"
        imagen_settings["style_settings"]["art_movement"] = "Contemporary Digital Illustration"
        imagen_settings["style_settings"]["drawing_approach"] = "Stylized Graphic"

    elif style_category == "pop_portrait":
        base_template["aspect_ratio"] = "1:1"
        imagen_settings["pop_art_elements"] = {
            "iconic_motifs": "Bold Graphic Shapes and Pop Culture Reference", "element_juxtaposition": "Playful and Unexpected Combination",
            "narrative_style": "Subtle Social Commentary", "color_palette_pop": "Highly Saturated Primary Colors with Ben Day Dots"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "Flat Graphic Lighting (Minimal Shadows)"
        imagen_settings["color_settings"]["palette_type"] = "Bold Primaries and High Contrast"
        imagen_settings["style_settings"]["art_movement"] = "Pop Art (Warhol Influence)"
        imagen_settings["detail_settings"]["texture_quality"] = "Smooth Flat Colors, Screen-Print Look"

    elif style_category == "environmental_portrait":
        base_template["aspect_ratio"] = "16:9"
        imagen_settings["camera_settings"] = PORTRAIT_CAMERA_SETTINGS.copy()
        imagen_settings["camera_settings"]["lens_type"] = "Wide-Angle Prime (e.g., 35mm)"
        imagen_settings["camera_settings"]["aperture"] = "f/4.0"
        imagen_settings["camera_settings"]["depth_of_field"] = "Medium to Deep"
        imagen_settings["environmental_context"] = {
            "location_significance": "Subject's Workplace (e.g., artist studio, workshop)",
            "contextual_props": "Tools of Trade and Personal Belongings relevant to subject",
            "storytelling_focus": "Conveying personality and profession through surroundings"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "Natural Available Light (Large Window)"
        imagen_settings["lighting_settings"]["light_quality"] = "Realistic to the Environment, Softly Directional"
        imagen_settings["composition_settings"]["technique"] = "Subject Integrated with Background, Leading Lines from Environment"
        imagen_settings["style_settings"]["photo_style"] = "Environmental Portraiture"
        imagen_settings["quality_settings"]["rendering_quality"] = "Realistic Documentary Feel"

    elif style_category == "caricature_portrait":
        base_template["aspect_ratio"] = "3:4"
        imagen_settings["caricature_elements"] = {
            "exaggeration_targets": "Prominent Facial Features (e.g., nose, eyes) and Characteristic Expressions",
            "humor_approach": "Playful and Satirical", "line_art_quality": "Bold and Expressive Outlines with Dynamic Curves"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "Cartoonish Graphic Lighting with Rim Highlights"
        imagen_settings["color_settings"]["palette_type"] = "Vibrant and Loud Exaggerated Colors"
        imagen_settings["style_settings"]["art_movement"] = "Caricature Art and Cartooning"
        imagen_settings["composition_settings"]["technique"] = "Extreme Exaggeration and Comedic Distortion"
        imagen_settings["detail_settings"]["texture_quality"] = "Stylized Smooth Shading"

    elif style_category == "conceptual_portrait":
        base_template["aspect_ratio"] = "1:1"
        imagen_settings["conceptual_elements"] = {
            "central_concept_or_theme": "Identity and Metaphorical Representation",
            "symbolic_visual_motifs": "Specific Objects and Textural Overlays representing an idea",
            "degree_of_abstraction": "Representational with Strong Symbolic Layers"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "Artificial and Controlled Dramatic Lighting"
        imagen_settings["lighting_settings"]["light_quality"] = "Moody and Mysterious with High Contrast"
        imagen_settings["color_settings"]["palette_type"] = "Muted and Desaturated with Symbolic Accent Color"
        imagen_settings["composition_settings"]["technique"] = "Concept-driven Unconventional Framing with Negative Space"
        imagen_settings["style_settings"]["art_movement"] = "Conceptual Art and Fine Art Photography"

    elif style_category == "fashion_portrait":
        base_template["aspect_ratio"] = "2:3"
        imagen_settings["camera_settings"] = PORTRAIT_CAMERA_SETTINGS.copy()
        imagen_settings["camera_settings"]["lens_type"] = "Telephoto Prime (e.g., 135mm)"
        imagen_settings["camera_settings"]["aperture"] = "f/2.8"
        imagen_settings["fashion_shoot_elements"] = {
            "apparel_style_focus": "Haute Couture Editorial", "hair_and_makeup_style": "Bold and Artistic High Fashion Makeup",
            "posing_and_direction": "Dynamic and Expressive Editorial Poses"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "Studio Strobes with Beauty Dish and Reflectors"
        imagen_settings["lighting_settings"]["light_quality"] = "High-Fashion Crisp with Soft Falloff"
        imagen_settings["color_settings"]["palette_type"] = "Bold and Trendy with Artistic Color Grading"
        imagen_settings["style_settings"]["photo_style"] = "Fashion Editorial Portraiture"
        imagen_settings["composition_settings"]["camera_angle"] = "Dynamic Fashion-driven Angles (e.g., low angle for power)"
        imagen_settings["quality_settings"]["resolution"] = "High-Resolution Magazine Quality"
        imagen_settings["environment_settings"]["location_type"] = "Minimalist Studio Set or Unique Architectural Backdrop"

    elif style_category == "selfie_portrait":
        base_template["aspect_ratio"] = "9:16"
        imagen_settings["selfie_characteristics"] = {
            "capture_device_hint": "Smartphone Front Camera", "posing_style": "Candid and Spontaneous with a Specific Trend Pose",
            "digital_filters_or_effects": "Subtle Beauty Filter and Popular Social Media Color Filter",
            "typical_background": "Casual Home Setting or Travel Location Landmark"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "Natural Ambient Light (e.g., near window)"
        imagen_settings["lighting_settings"]["light_quality"] = "Variable, often Soft if indoors or Golden Hour if outdoors"
        imagen_settings["style_settings"]["photo_style"] = "Modern Selfie Aesthetic"
        imagen_settings["composition_settings"]["camera_angle"] = "Arm's Length High-Angle"
        imagen_settings["quality_settings"]["resolution"] = "Typical Smartphone Resolution (e.g., 12MP)"
        imagen_settings["color_settings"]["palette_type"] = "Real-life Colors Enhanced by Filters"
        imagen_settings["moods"] = ["Playful and Casual"]

    else: # Fallback for any other unlisted portrait style
        imagen_settings["other_portrait_specifics"] = {
            "notable_features": f"Unique characteristics defining a {style_category.replace('_', ' ')} portrait.",
            "primary_medium_hint": "Digital Painting", "artistic_intent": f"To capture the essence of a {style_category.replace('_', ' ')} portrait.",
            "notes": f"Settings should be tailored to the specific nuances of the {style_category.replace('_', ' ')} portrait style."
        }
        base_template["preset_name"] = f"{style_category.replace('_', ' ').title()} (Custom Portrait Style)"
        imagen_settings["style_settings"]["art_movement"] = style_category.replace('_', ' ').title()

    final_template = {**base_template, "imagen_settings": imagen_settings}
    return final_template
