"""Style Templates Module for AI Preset Generator

This module provides style-specific template generation for different art styles
to ensure settings are appropriate for each style category.
All templates are fully defined with concrete default values.
"""

from typing import Dict, Any, List, Optional, Union

# This function is now defined directly in this module.
# from ai_prest_gen.portrait_style_templates import get_portrait_template # Removed import

def get_portrait_template(style_category: str) -> Dict[str, Any]:
    """
    Return the appropriate JSON template based on a specific portrait style category.
    All placeholders are replaced with concrete default values.
    """
    style_category = style_category.lower() # Normalize for matching

    # Base template common to all portraits
    base_template = {
        "preset_name": f"{style_category.replace('_', ' ').title()} Portrait",
        "moods": ["Expressive"], # Default mood as a list with one string
        "aspect_ratio": "3:4", # Common default for portraits
        "description": f"A detailed portrait preset in the {style_category.replace('_', ' ')} style, focusing on character and mood."
    }

    # Common imagen settings for all portrait categories, to be potentially overridden
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
            "weather": "N/A", # Not typically relevant for studio portraits
            "season": "N/A",
            "location_type": "Studio Backdrop (neutral)",
            "atmospheric_effects": ["none"]
        },
        "quality_settings": {
            "resolution": "4000x5000", # High resolution for 3:4 portrait
            "rendering_quality": "Photorealistic"
        },
        "negative_prompt": "blurry, deformed, extra limbs, poorly drawn face, bad anatomy, signature, text, watermark, low quality, unrealistic features (unless style dictates), distorted eyes",
        "style_negative_prompt": "clashing art styles, inconsistent lighting for portraiture, unflattering angles, generic look"
    }

    # Define Common Camera Settings with concrete defaults for photographic portraits
    PORTRAIT_CAMERA_SETTINGS = {
        "camera_model": "DSLR (e.g., Canon EOS 5D Mark IV)",
        "lens_type": "Prime Lens (e.g., 85mm)",
        "aperture": "f/1.8",
        "focal_length": "85mm",
        "shutter_speed": "1/160s",
        "iso": "ISO 100",
        "filter_type": "None",
        "depth_of_field": "Shallow (bokeh background)",
        "white_balance": "Daylight (5500K)",
        "focus_mode": "Eye Autofocus (Eye AF)",
        "exposure_mode": "Manual (M)",
        "image_stabilization": "In-Lens (IS)",
        "metering_mode": "Spot Metering (on face)",
        "flash_mode": "Off-Camera Flash (Softbox Key Light)",
        "shooting_mode": "Single Shot",
        "focus_point_selection": "Single Point AF (on eye)",
        "image_format": "RAW",
        "color_space": "Adobe RGB"
    }

    # --- Portrait Style Specific Settings (No Placeholders) ---
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
            "painting_medium": "Oil Paint",
            "support_type": "Canvas",
            "brushwork_style": "Visible Brushstrokes with Blending",
            "texture_application": "Textured Canvas with Layered Paint",
            "layering_technique": "Glazing and Scumbling",
            "stroke_style": "Expressive and Deliberate",
            "detail_approach": "High Realism with Artistic Interpretation"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "Natural Window Light (North Light)"
        imagen_settings["lighting_settings"]["light_quality"] = "Chiaroscuro with Soft Transitions"
        imagen_settings["style_settings"]["art_movement"] = "Realism (e.g., 19th Century)"
        imagen_settings["style_settings"]["painter_influence"] = "John Singer Sargent"
        imagen_settings["style_settings"]["period"] = "Late 19th Century"
        imagen_settings["color_settings"]["palette_type"] = "Warm Earth Tones and Rich Colors"
        imagen_settings["detail_settings"]["texture_quality"] = "Painted Fabric Textures, Rendered Skin and Hair"

    elif style_category == "futuristic_portrait" or style_category == "cyberpunk_portrait": # Grouped similar styles
        base_template["aspect_ratio"] = "16:9" # Can be wider for environmental context
        imagen_settings["futuristic_elements"] = {
            "character_archetype": "Cyborg with Visible Augmentations",
            "costuming_details": "Tech-wear with Integrated LED Elements",
            "cybernetic_enhancements": "Glowing Optical Sensors and Data Ports",
            "background_setting": "Neon-drenched Cityscape Alleyway",
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
            "line_work_style": "Clean and Crisp Outlines",
            "coloring_method": "Cel Shading with Soft Gradient Highlights",
            "overall_visual_style": "Stylized Realism (Anime-inspired)",
            "level_of_detail": "Medium, focusing on character expression",
            "subject_portrayal": "Expressive Character with a Narrative Hint"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "Stylized Rim Lighting and Ambient Occlusion"
        imagen_settings["color_settings"]["palette_type"] = "Vibrant and Saturated Thematic Palette"
        imagen_settings["style_settings"]["art_movement"] = "Contemporary Digital Illustration"
        imagen_settings["style_settings"]["drawing_approach"] = "Stylized Graphic"

    elif style_category == "pop_portrait":
        base_template["aspect_ratio"] = "1:1"
        imagen_settings["pop_art_elements"] = {
            "iconic_motifs": "Bold Graphic Shapes and Pop Culture Reference",
            "element_juxtaposition": "Playful and Unexpected Combination",
            "narrative_style": "Subtle Social Commentary",
            "color_palette_pop": "Highly Saturated Primary Colors with Ben Day Dots"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "Flat Graphic Lighting (Minimal Shadows)"
        imagen_settings["color_settings"]["palette_type"] = "Bold Primaries and High Contrast"
        imagen_settings["style_settings"]["art_movement"] = "Pop Art (Warhol Influence)"
        imagen_settings["detail_settings"]["texture_quality"] = "Smooth Flat Colors, Screen-Print Look"

    elif style_category == "environmental_portrait":
        base_template["aspect_ratio"] = "16:9" # Wider to show environment
        imagen_settings["camera_settings"] = PORTRAIT_CAMERA_SETTINGS.copy()
        imagen_settings["camera_settings"]["lens_type"] = "Wide-Angle Prime (e.g., 35mm)"
        imagen_settings["camera_settings"]["aperture"] = "f/4.0" # More DoF for environment
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
            "humor_approach": "Playful and Satirical",
            "line_art_quality": "Bold and Expressive Outlines with Dynamic Curves"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "Cartoonish Graphic Lighting with Rim Highlights"
        imagen_settings["color_settings"]["palette_type"] = "Vibrant and Loud Exaggerated Colors"
        imagen_settings["style_settings"]["art_movement"] = "Caricature Art and Cartooning"
        imagen_settings["composition_settings"]["technique"] = "Extreme Exaggeration and Comedic Distortion"
        imagen_settings["detail_settings"]["texture_quality"] = "Stylized Smooth Shading"

    elif style_category == "conceptual_portrait":
        base_template["aspect_ratio"] = "1:1" # Often square for impact
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
        base_template["aspect_ratio"] = "2:3" # Common fashion magazine ratio
        imagen_settings["camera_settings"] = PORTRAIT_CAMERA_SETTINGS.copy()
        imagen_settings["camera_settings"]["lens_type"] = "Telephoto Prime (e.g., 135mm)"
        imagen_settings["camera_settings"]["aperture"] = "f/2.8"
        imagen_settings["fashion_shoot_elements"] = {
            "apparel_style_focus": "Haute Couture Editorial",
            "hair_and_makeup_style": "Bold and Artistic High Fashion Makeup",
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
        base_template["aspect_ratio"] = "9:16" # Common phone screen ratio
        imagen_settings["selfie_characteristics"] = {
            "capture_device_hint": "Smartphone Front Camera",
            "posing_style": "Candid and Spontaneous with a Specific Trend Pose",
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
            "primary_medium_hint": "Digital Painting", # Generic default
            "artistic_intent": f"To capture the essence of a {style_category.replace('_', ' ')} portrait.",
            "notes": f"Settings should be tailored to the specific nuances of the {style_category.replace('_', ' ')} portrait style."
        }
        base_template["preset_name"] = f"{style_category.replace('_', ' ').title()} (Custom Portrait Style)"
        imagen_settings["style_settings"]["art_movement"] = style_category.replace('_', ' ').title() # Use the style itself

    final_template = {**base_template, "imagen_settings": imagen_settings}
    return final_template


def _priority_category_match(style_category: Union[str, List[str]]) -> str:
    """
    Return the best-matching style category based on a fixed priority list.
    When multiple categories are given, always choose the most specific/relevant one by priority.
    Fallback to first or 'default'.
    """
    priority_list = [
        # Copied from the latest style_category_catalog.py for consistency
        "pop_surrealism_ascii", "abstract_expressionism_cubism_fusion", "anime_oilpainting",
        "retro_pixel_vaporwave", "dreamcore_weirdcore", "photorealism_glitch", "watercolor_pencil",
        "cubism_futurism", "digital_pixel_traditional", "scientific_technological_hybrid",
        "psychedelic_surrealism", "morphism_surreal", "kinetic_ascii", "collage_digital_overlay",
        "pixel_patchwork", "tradigital_mixed_media", "hybrid_traditional_digital", "digital_traditional_fusion",
        "caricature_portrait", "selfie_portrait", "environmental_portrait", "fashion_portrait",
        "conceptual_portrait", "cyberpunk_portrait", "futuristic_portrait", "pop_portrait",
        "illustration_portrait", "photographic_portrait", "traditional_portrait", "fantasy_portrait",
        "noir_photography", "art_deco_revival", "augmented_reality_art", "biopunk", "ferrofluid",
        "fractal_generative_art", "installation_art", "kinetic_art", "luna_photo",
        "mixed_media_journaling", "nightcore", "optic_art", "paper_quilling", "phygital_hybrid",
        "screen_printing_bold", "synesthesia_art", "ink_punk", "game_cel_shaded", "game_retro",
        "game_style", "cyberpunk_action", "cyberpunk_cityscape", "cyberpunk_technology", "cyberpunk",
        "fantasy_battle", "fantasy_cityscape", "fantasy_landscape", "whimsical_fantasy", "fantasy",
        "sci_fi_futuristic", "sci_fi", "claymation", "digital_collage", "experimental_mixed_media",
        "patchwork_fabric", "patchwork_collage", "papercraft", "ascii_art", "line_art",
        "illustration_pixar", "illustration_disney", "illustration_tom_jerry",
        "illustration_vintage_cartoon", "illustration_anime_manga", "illustration_comic",
        "illustration_pixel", "illustration_steampunk", "illustration_cubist", "illustration_surreal",
        "illustration_childrens", "illustration_fantasy", "illustration_graphic", "illustration",
        "oil_painting", "watercolor", "pastel", "acrylic_painting", "digital_painting", "pencil_sketch",
        "ink_drawing", "charcoal", "drawing", "street_photography", "documentary", "cinematic",
        "photographic", "minimalist_geometric", "minimalist", "geometric", "constructivism", "low_poly",
        "abstract_conceptual", "abstract", "pop_surrealism", "surrealism", "cubism", "expressionism",
        "fauvism", "art_nouveau", "art_deco", "psychedelic", "steampunk", "dystopian", "glitch_art",
        "retrowave", "vaporwave", "dreamcore", "weirdcore", "folk_art", "mediterranean_style",
        "material_sculptural", "sculpture", "3d_render", "vector_art", "digital_art",
        "traditional_painting_drawing", "animal_inspired", "space_art", "robot_art",
        "default", "unknown"
    ]
    seen = set()
    unique_priority_list = [x for x in priority_list if not (x in seen or seen.add(x))]

    if isinstance(style_category, str):
        categories = [style_category.lower()]
    elif isinstance(style_category, list):
        categories = [str(cat).lower() for cat in style_category if isinstance(cat, (str, int, float))]
    else:
        categories = []

    main_category = None
    for pcat in unique_priority_list:
        if pcat in categories:
            main_category = pcat
            break
    if main_category is None and categories:
        main_category = categories[0]
    elif main_category is None:
        main_category = "default"
    return main_category

def get_template_for_category(style_category: Union[str, List[str]]) -> Dict[str, Any]:
    """
    Return the appropriate JSON template based on style category or list of style categories.
    Uses priority to select the most relevant category when several are given, for enhanced preset compatibility.
    All placeholders are replaced with concrete default values.
    """
    main_category = _priority_category_match(style_category)

    portrait_categories = {
        "photographic_portrait", "traditional_portrait", "futuristic_portrait",
        "illustration_portrait", "pop_portrait", "cyberpunk_portrait", "fantasy_portrait",
        "environmental_portrait", "caricature_portrait", "conceptual_portrait",
        "fashion_portrait", "selfie_portrait"
    }

    if main_category in portrait_categories:
        # Delegate to portrait-specific template generation
        return get_portrait_template(main_category) # Now calls the self-contained version

    # Define Common Camera Settings with concrete defaults
    COMMON_CAMERA_SETTINGS = {
        "camera_model": "DSLR",
        "lens_type": "Prime (50mm)",
        "aperture": "f/2.8",
        "focal_length": "50mm",
        "shutter_speed": "1/125s",
        "iso": "ISO 200",
        "filter_type": "None",
        "depth_of_field": "Medium",
        "white_balance": "Auto",
        "focus_mode": "Autofocus Single (AF-S/One-Shot)",
        "exposure_mode": "Aperture Priority (Av/A)",
        "image_stabilization": "Optical (OIS in lens)",
        "metering_mode": "Evaluative/Matrix",
        "flash_mode": "Off",
        "shooting_mode": "Single Shot",
        "focus_point_selection": "Single Point AF",
        "image_format": "RAW",
        "color_space": "sRGB"
    }

    base_template = {
        "preset_name": f"{main_category.replace('_', ' ').title()} Preset",
        "moods": ["Evocative"], # Default mood as a list with one string
        "aspect_ratio": "16:9",
        "description": f"A balanced preset for the {main_category.replace('_', ' ')} style, focusing on typical characteristics and a specific mood."
    }

    imagen_settings = {
        "style_settings": {
            "art_movement": "Contemporary", # General default
            "post_processing": ["subtle sharpening"], # Default effect as a list
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
            "palette_type": "Balanced", # General descriptive term
            "color_temperature": "Neutral",
            "color_contrast": "Medium",
            "dominant_colors": ["blue", "green", "grey"] # Generic list of dominant colors
        },
        "detail_settings": {
            "detail_level": "Medium",
            "texture_quality": "Realistic"
        },
        "environment_settings": {
            "weather": "Clear",
            "season": "Spring",
            "location_type": "Outdoor",
            "atmospheric_effects": ["subtle haze"] # Default effect as a list
        },
        "quality_settings": {
            "resolution": "3840x2160", # 4K UHD
            "rendering_quality": "High"
        },
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, text, words, amateur, low quality",
        "style_negative_prompt": "clashing styles, inconsistent lighting, poor composition, unrealistic elements (unless style dictates), generic, boring, flat"
    }

    # --- Style-Specific Template Customizations (No Placeholders) ---

    if main_category == "digital_collage":
        imagen_settings["digital_collage_specifics"] = {
            "elements_source": ["photographed elements", "digital renders", "typography"],
            "layer_count": "7",
            "edge_treatment": "digital mask",
            "montage_style": "surreal",
            "overall_texture": "paper fibers"
        }
        imagen_settings["composition_settings"]["technique"] = "layered digital montage"
        imagen_settings["color_settings"]["palette_type"] = "eclectic and sample-based"
        imagen_settings["style_settings"]["art_movement"] = "Contemporary Digital Art"
        base_template["aspect_ratio"] = "1:1"

    elif main_category == "noir_photography":
        imagen_settings["camera_settings"] = COMMON_CAMERA_SETTINGS.copy()
        imagen_settings["noir_photography_specifics"] = {
            "monochrome_style": True,
            "contrast_level": "Very High",
            "film_grain_type": "simulated medium",
            "key_lighting_setup": "Low-key lighting (Chiaroscuro)",
            "shadow_play": "deep expressive shadows and cast shadows (e.g., Venetian blinds)",
            "common_subjects_or_themes": "detective, femme fatale, crime scene, urban loneliness",
            "era_influence": "1940s Classic Noir"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "Chiaroscuro Single Source Hard Light"
        imagen_settings["lighting_settings"]["light_quality"] = "Hard dramatic directional"
        imagen_settings["color_settings"]["color_scheme"] = "Monochromatic (Black & White)"
        imagen_settings["color_settings"]["palette_type"] = "High Contrast Greyscale"
        imagen_settings["style_settings"]["art_movement"] = "Film Noir"
        imagen_settings["style_settings"]["post_processing"] = ["film grain emulation", "strong vignette", "dodging and burning"]
        imagen_settings["environment_settings"]["atmospheric_effects"] = ["smoke", "fog", "rain slicked streets"]
        base_template["aspect_ratio"] = "4:3"

    elif main_category == "photorealism_glitch":
        imagen_settings["camera_settings"] = COMMON_CAMERA_SETTINGS.copy()
        imagen_settings["photorealism_glitch_specifics"] = {
            "base_image_quality": "hyperrealistic high-detail sharp focus",
            "glitch_techniques": ["datamoshing", "pixel sorting", "RGB shift"],
            "intensity_of_glitch": "moderate and localized",
            "aesthetic_blend": "Juxtaposition of perfect photorealism with chaotic digital deconstruction and artifacts."
        }
        imagen_settings["detail_settings"]["texture_quality"] = "realistic base textures with overlaid digital glitch patterns"
        imagen_settings["style_settings"]["post_processing"] = ["glitch effects", "chromatic aberration artifacts", "databending emulation"]
        imagen_settings["style_settings"]["art_movement"] = "Glitch Art"

    elif main_category == "luna_photo":
        imagen_settings["camera_settings"] = COMMON_CAMERA_SETTINGS.copy()
        imagen_settings["luna_photo_settings"] = {
            "exposure_method": "double exposure",
            "photographic_style": "ethereal and surreal",
            "subject_interaction_with_moon": "subject silhouetted against a large moon",
            "moon_phase_or_appearance": "full moon"
        }
        imagen_settings["lighting_settings"]["light_quality"] = "diffuse moonlit glow"
        imagen_settings["color_settings"]["palette_type"] = "deep blues and silvers"
        imagen_settings["environment_settings"]["atmospheric_effects"] = ["mist", "starlight"]

    elif main_category == "photographic":
        imagen_settings["camera_settings"] = COMMON_CAMERA_SETTINGS.copy()
        imagen_settings["style_settings"]["photo_style"] = "landscape photography"
        imagen_settings["quality_settings"]["rendering_quality"] = "photorealistic ultra-detailed"

    elif main_category == "cinematic":
        imagen_settings["camera_settings"] = COMMON_CAMERA_SETTINGS.copy()
        imagen_settings["camera_settings"]["lens_type"] = "Anamorphic"
        imagen_settings["camera_settings"]["image_format"] = "RAW (CinemaDNG)"
        imagen_settings["cinematic_specifics"] = {
            "color_grading_style": "teal and orange",
            "framing_and_composition": "rule of thirds with leading lines and depth",
            "camera_movement_hint": "static shot with subtle focus pull",
            "film_grain_level": "subtle film grain"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "dramatic three-point lighting"
        imagen_settings["style_settings"]["film_era_influence"] = "Modern Blockbuster"
        base_template["aspect_ratio"] = "2.39:1"
        imagen_settings["quality_settings"]["resolution"] = "4K"

    elif main_category == "documentary":
        imagen_settings["camera_settings"] = COMMON_CAMERA_SETTINGS.copy()
        imagen_settings["documentary_specifics"] = {
            "subject_matter_focus": "real-life events and social issues",
            "narrative_approach": "observational",
            "authenticity_level": "raw and unfiltered"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "available natural light"
        imagen_settings["style_settings"]["photo_style"] = "candid reportage"
        imagen_settings["composition_settings"]["camera_angle"] = "eye-level observational"
        imagen_settings["quality_settings"]["rendering_quality"] = "realistic true-to-life"

    elif main_category == "street_photography":
        imagen_settings["camera_settings"] = COMMON_CAMERA_SETTINGS.copy()
        imagen_settings["camera_settings"]["lens_type"] = "Prime (35mm)"
        imagen_settings["street_photo_specifics"] = {
            "moment_capture": "decisive moment candid interactions",
            "urban_elements": "cityscapes architecture people in urban settings",
            "compositional_themes": "juxtaposition geometry reflections"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "natural ambient and street lights"
        imagen_settings["style_settings"]["photo_style"] = "candid urban black and white street"
        imagen_settings["composition_settings"]["camera_angle"] = "hip-level"
        imagen_settings["quality_settings"]["rendering_quality"] = "gritty authentic high contrast"

    elif main_category == "cyberpunk_cityscape":
        imagen_settings["cyberpunk_cityscape_specifics"] = {
            "time_of_day": "perpetual night with acid rain",
            "architectural_style": "towering skyscrapers with Kowloon Walled City density",
            "lighting_elements": "pervasive neon signs and holographic advertisements",
            "atmospheric_conditions": "constant rain and smog with digital artifacts",
            "level_of_decay_or_advancement": "gritty and worn with hyper-advanced tech pockets",
            "presence_of_nature": "absent or entirely artificial"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "neon and holographic volumetric light"
        imagen_settings["color_settings"]["palette_type"] = "vibrant neon blues, purples, and pinks with dark undertones"
        imagen_settings["environment_settings"]["location_type"] = "dystopian megalopolis"
        imagen_settings["detail_settings"]["detail_level"] = "intricate and dense with visual information"
        imagen_settings["style_settings"]["art_movement"] = "Cyberpunk Art"
        base_template["aspect_ratio"] = "21:9"

    elif main_category == "fantasy_landscape":
        imagen_settings["fantasy_landscape_specifics"] = {
            "dominant_biome_or_feature": "enchanted forest with mystical mountains",
            "magical_elements_present": ["glowing flora", "distant mythical creatures", "ancient magical artifacts"],
            "time_period_or_civilization_hint": "timeless magical realm",
            "sky_features": ["multiple moons", "aurora borealis"],
            "architectural_presence_type": "distant elven cities integrated with nature"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "ethereal glow with god rays"
        imagen_settings["color_settings"]["palette_type"] = "rich jewel tones with magical highlights"
        imagen_settings["environment_settings"]["location_type"] = "mythical world"
        imagen_settings["detail_settings"]["texture_quality"] = "painterly with fantastical elements"
        imagen_settings["style_settings"]["art_movement"] = "High Fantasy Concept Art"
        # base_template["aspect_ratio"] = "16:9" # Default is fine, no need to override if same

    # Default fallback for categories not explicitly handled above
    else:
        imagen_settings[f"{main_category}_specific_settings"] = {
            "notable_features": f"Key features typical of the {main_category.replace('_',' ')} style.",
            "notes": f"Settings should reflect common artistic principles and typical associations for the {main_category.replace('_',' ')} style."
        }
        if main_category == "default":
             base_template["preset_name"] = "Default Versatile Preset"
             imagen_settings["style_settings"]["art_movement"] = "General Purpose"


    final_template = {**base_template, "imagen_settings": imagen_settings}
    return final_template

# Example of how this function might be called (for testing purposes):
# if __name__ == '__main__':
#     test_styles = [
#         "noir_photography",
#         "cinematic",
#         "photorealism_glitch",
#         "digital_collage",
#         "fantasy_landscape",
#         "default",
#         "photographic_portrait" # Test portrait delegation
#     ]
#     import json
#     for style in test_styles:
#         print(f"\n--- Template for: {style} (Category: {_priority_category_match(style)}) ---")
#         template = get_template_for_category(style)
#         print(json.dumps(template, indent=4))
