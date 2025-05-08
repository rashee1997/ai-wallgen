"""Traditional Art Style Templates

Provides template generators for traditional art mediums.
Each function returns a fully-defined template dict for its style.
"""

from typing import Dict, Any

def get_oil_painting_template(main_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Oil Painting Preset",
        "moods": ["Evocative"],
        "aspect_ratio": "16:9",
        "description": "A balanced preset for the oil painting style, focusing on typical characteristics and a specific mood."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Contemporary", "post_processing": ["subtle sharpening"], "style_era": "Modern"},
        "lighting_settings": {"lighting_type": "Natural", "light_quality": "Soft Diffused", "light_direction": "Front", "time_of_day": "Daytime"},
        "composition_settings": {"technique": "Rule of Thirds", "focal_point": "Main Subject", "camera_angle": "Eye-level", "perspective": "One-point"},
        "color_settings": {"color_scheme": "Analogous", "palette_type": "Balanced", "color_temperature": "Neutral", "color_contrast": "Medium", "dominant_colors": ["blue", "green", "grey"]},
        "detail_settings": {"detail_level": "Medium", "texture_quality": "Realistic"},
        "environment_settings": {"weather": "Clear", "season": "Spring", "location_type": "Outdoor", "atmospheric_effects": ["subtle haze"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, text, words, amateur, low quality",
        "style_negative_prompt": "clashing styles, inconsistent lighting, poor composition, unrealistic elements (unless style dictates), generic, boring, flat"
    }
    # No camera_settings for traditional art styles.
    return {**base_template, "imagen_settings": imagen_settings}

def get_watercolor_template(main_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Watercolor Preset",
        "moods": ["Evocative"],
        "aspect_ratio": "16:9",
        "description": "A balanced preset for the watercolor style, focusing on typical characteristics and a specific mood."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Contemporary", "post_processing": ["subtle sharpening"], "style_era": "Modern"},
        "lighting_settings": {"lighting_type": "Natural", "light_quality": "Soft Diffused", "light_direction": "Front", "time_of_day": "Daytime"},
        "composition_settings": {"technique": "Rule of Thirds", "focal_point": "Main Subject", "camera_angle": "Eye-level", "perspective": "One-point"},
        "color_settings": {"color_scheme": "Analogous", "palette_type": "Balanced", "color_temperature": "Neutral", "color_contrast": "Medium", "dominant_colors": ["blue", "green", "grey"]},
        "detail_settings": {"detail_level": "Medium", "texture_quality": "Realistic"},
        "environment_settings": {"weather": "Clear", "season": "Spring", "location_type": "Outdoor", "atmospheric_effects": ["subtle haze"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, text, words, amateur, low quality",
        "style_negative_prompt": "clashing styles, inconsistent lighting, poor composition, unrealistic elements (unless style dictates), generic, boring, flat"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_pastel_template(main_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Pastel Preset",
        "moods": ["Evocative"],
        "aspect_ratio": "16:9",
        "description": "A balanced preset for the pastel style, focusing on typical characteristics and a specific mood."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Contemporary", "post_processing": ["subtle sharpening"], "style_era": "Modern"},
        "lighting_settings": {"lighting_type": "Natural", "light_quality": "Soft Diffused", "light_direction": "Front", "time_of_day": "Daytime"},
        "composition_settings": {"technique": "Rule of Thirds", "focal_point": "Main Subject", "camera_angle": "Eye-level", "perspective": "One-point"},
        "color_settings": {"color_scheme": "Analogous", "palette_type": "Balanced", "color_temperature": "Neutral", "color_contrast": "Medium", "dominant_colors": ["blue", "green", "grey"]},
        "detail_settings": {"detail_level": "Medium", "texture_quality": "Realistic"},
        "environment_settings": {"weather": "Clear", "season": "Spring", "location_type": "Outdoor", "atmospheric_effects": ["subtle haze"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, text, words, amateur, low quality",
        "style_negative_prompt": "clashing styles, inconsistent lighting, poor composition, unrealistic elements (unless style dictates), generic, boring, flat"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_acrylic_painting_template(main_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Acrylic Painting Preset",
        "moods": ["Evocative"],
        "aspect_ratio": "16:9",
        "description": "A balanced preset for the acrylic painting style, focusing on typical characteristics and a specific mood."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Contemporary", "post_processing": ["subtle sharpening"], "style_era": "Modern"},
        "lighting_settings": {"lighting_type": "Natural", "light_quality": "Soft Diffused", "light_direction": "Front", "time_of_day": "Daytime"},
        "composition_settings": {"technique": "Rule of Thirds", "focal_point": "Main Subject", "camera_angle": "Eye-level", "perspective": "One-point"},
        "color_settings": {"color_scheme": "Analogous", "palette_type": "Balanced", "color_temperature": "Neutral", "color_contrast": "Medium", "dominant_colors": ["blue", "green", "grey"]},
        "detail_settings": {"detail_level": "Medium", "texture_quality": "Realistic"},
        "environment_settings": {"weather": "Clear", "season": "Spring", "location_type": "Outdoor", "atmospheric_effects": ["subtle haze"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, text, words, amateur, low quality",
        "style_negative_prompt": "clashing styles, inconsistent lighting, poor composition, unrealistic elements (unless style dictates), generic, boring, flat"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_charcoal_template(main_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Charcoal Preset",
        "moods": ["Evocative"],
        "aspect_ratio": "16:9",
        "description": "A balanced preset for the charcoal style, focusing on typical characteristics and a specific mood."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Contemporary", "post_processing": ["subtle sharpening"], "style_era": "Modern"},
        "lighting_settings": {"lighting_type": "Natural", "light_quality": "Soft Diffused", "light_direction": "Front", "time_of_day": "Daytime"},
        "composition_settings": {"technique": "Rule of Thirds", "focal_point": "Main Subject", "camera_angle": "Eye-level", "perspective": "One-point"},
        "color_settings": {"color_scheme": "Analogous", "palette_type": "Balanced", "color_temperature": "Neutral", "color_contrast": "Medium", "dominant_colors": ["blue", "green", "grey"]},
        "detail_settings": {"detail_level": "Medium", "texture_quality": "Realistic"},
        "environment_settings": {"weather": "Clear", "season": "Spring", "location_type": "Outdoor", "atmospheric_effects": ["subtle haze"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, text, words, amateur, low quality",
        "style_negative_prompt": "clashing styles, inconsistent lighting, poor composition, unrealistic elements (unless style dictates), generic, boring, flat"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_pencil_sketch_template(main_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Pencil Sketch Preset",
        "moods": ["Evocative"],
        "aspect_ratio": "16:9",
        "description": "A balanced preset for the pencil sketch style, focusing on typical characteristics and a specific mood."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Contemporary", "post_processing": ["subtle sharpening"], "style_era": "Modern"},
        "lighting_settings": {"lighting_type": "Natural", "light_quality": "Soft Diffused", "light_direction": "Front", "time_of_day": "Daytime"},
        "composition_settings": {"technique": "Rule of Thirds", "focal_point": "Main Subject", "camera_angle": "Eye-level", "perspective": "One-point"},
        "color_settings": {"color_scheme": "Analogous", "palette_type": "Balanced", "color_temperature": "Neutral", "color_contrast": "Medium", "dominant_colors": ["blue", "green", "grey"]},
        "detail_settings": {"detail_level": "Medium", "texture_quality": "Realistic"},
        "environment_settings": {"weather": "Clear", "season": "Spring", "location_type": "Outdoor", "atmospheric_effects": ["subtle haze"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, text, words, amateur, low quality",
        "style_negative_prompt": "clashing styles, inconsistent lighting, poor composition, unrealistic elements (unless style dictates), generic, boring, flat"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_ink_drawing_template(main_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Ink Drawing Preset",
        "moods": ["Evocative"],
        "aspect_ratio": "16:9",
        "description": "A balanced preset for the ink drawing style, focusing on typical characteristics and a specific mood."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Contemporary", "post_processing": ["subtle sharpening"], "style_era": "Modern"},
        "lighting_settings": {"lighting_type": "Natural", "light_quality": "Soft Diffused", "light_direction": "Front", "time_of_day": "Daytime"},
        "composition_settings": {"technique": "Rule of Thirds", "focal_point": "Main Subject", "camera_angle": "Eye-level", "perspective": "One-point"},
        "color_settings": {"color_scheme": "Analogous", "palette_type": "Balanced", "color_temperature": "Neutral", "color_contrast": "Medium", "dominant_colors": ["blue", "green", "grey"]},
        "detail_settings": {"detail_level": "Medium", "texture_quality": "Realistic"},
        "environment_settings": {"weather": "Clear", "season": "Spring", "location_type": "Outdoor", "atmospheric_effects": ["subtle haze"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, text, words, amateur, low quality",
        "style_negative_prompt": "clashing styles, inconsistent lighting, poor composition, unrealistic elements (unless style dictates), generic, boring, flat"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_drawing_template(main_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Drawing Preset",
        "moods": ["Evocative"],
        "aspect_ratio": "16:9",
        "description": "A balanced preset for the drawing style, focusing on typical characteristics and a specific mood."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Contemporary", "post_processing": ["subtle sharpening"], "style_era": "Modern"},
        "lighting_settings": {"lighting_type": "Natural", "light_quality": "Soft Diffused", "light_direction": "Front", "time_of_day": "Daytime"},
        "composition_settings": {"technique": "Rule of Thirds", "focal_point": "Main Subject", "camera_angle": "Eye-level", "perspective": "One-point"},
        "color_settings": {"color_scheme": "Analogous", "palette_type": "Balanced", "color_temperature": "Neutral", "color_contrast": "Medium", "dominant_colors": ["blue", "green", "grey"]},
        "detail_settings": {"detail_level": "Medium", "texture_quality": "Realistic"},
        "environment_settings": {"weather": "Clear", "season": "Spring", "location_type": "Outdoor", "atmospheric_effects": ["subtle haze"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, text, words, amateur, low quality",
        "style_negative_prompt": "clashing styles, inconsistent lighting, poor composition, unrealistic elements (unless style dictates), generic, boring, flat"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_gouache_template(main_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Gouache Painting Preset",
        "moods": ["Vibrant", "Matte"],
        "aspect_ratio": "16:9",
        "description": "Preset for Gouache painting, emphasizing its opaque, matte finish and ability to create bold, flat colors or layered details."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Contemporary Illustration", "post_processing": ["subtle sharpening"], "style_era": "Modern"},
        "lighting_settings": {"lighting_type": "Natural", "light_quality": "Even Diffused", "light_direction": "Front", "time_of_day": "Daytime"},
        "composition_settings": {"technique": "Layering", "focal_point": "Main Subject", "camera_angle": "Eye-level", "perspective": "One-point"},
        "color_settings": {"color_scheme": "Analogous", "palette_type": "Vibrant Opaque", "color_temperature": "Neutral", "color_contrast": "Medium", "dominant_colors": ["varied"]},
        "detail_settings": {"detail_level": "Medium", "texture_quality": "Smooth Matte"},
        "environment_settings": {"weather": "Clear", "season": "Any", "location_type": "Indoor/Outdoor", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, text, words, amateur, low quality, too transparent, streaky, shiny",
        "style_negative_prompt": "clashing styles, inconsistent lighting, poor composition, muddy colors, unintentional transparency, overly shiny finish"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_tempera_template(main_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Tempera Painting Preset",
        "moods": ["Luminous", "Detailed"],
        "aspect_ratio": "4:3", # Often historical, different aspect
        "description": "Preset for Tempera painting, highlighting its matte finish, potential for fine detail, cross-hatching, and historical luminous quality."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Early Renaissance", "post_processing": ["none"], "style_era": "Historical"}, # Or "Contemporary" if desired
        "lighting_settings": {"lighting_type": "Natural", "light_quality": "Soft Clear", "light_direction": "Slightly Off-center", "time_of_day": "Daytime"},
        "composition_settings": {"technique": "Fine Detail", "focal_point": "Central Figure", "camera_angle": "Eye-level", "perspective": "One-point or Early Perspective"},
        "color_settings": {"color_scheme": "Harmonious", "palette_type": "Rich Matte", "color_temperature": "Warm Neutral", "color_contrast": "Medium", "dominant_colors": ["earthy tones", "golds", "blues"]},
        "detail_settings": {"detail_level": "High", "texture_quality": "Smooth Panel-like"},
        "environment_settings": {"weather": "Clear", "season": "Any", "location_type": "Interior/Iconographic", "atmospheric_effects": ["subtle glow"]},
        "quality_settings": {"resolution": "3072x2304", "rendering_quality": "High"},
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, text, words, amateur, low quality, overly dark, smudged",
        "style_negative_prompt": "clashing styles, inconsistent lighting, anachronistic elements, muddy colors, lack of fine detail, modern brushwork"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_mosaic_template(main_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Mosaic Art Preset",
        "moods": ["Textured", "Decorative"],
        "aspect_ratio": "1:1", # Common for decorative pieces
        "description": "Preset for Mosaic art, focusing on assembled pieces (tesserae) creating a textured, often figurative or geometric image."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Decorative Art", "post_processing": ["sharpen details"], "style_era": "Ancient/Modern"},
        "lighting_settings": {"lighting_type": "Directional", "light_quality": "Slightly Hard", "light_direction": "Front", "time_of_day": "Any"},
        "composition_settings": {"technique": "Segmented Composition", "focal_point": "Overall Pattern/Figure", "camera_angle": "Direct", "perspective": "Flat"},
        "color_settings": {"color_scheme": "Varied", "palette_type": "Bold Segmented", "color_temperature": "Neutral", "color_contrast": "High", "dominant_colors": ["varied stone", "glass colors"]},
        "detail_settings": {"detail_level": "High", "texture_quality": "Tessellated"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Wall/Floor Surface", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "3000x3000", "rendering_quality": "High"},
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, text, words, amateur, low quality, smooth surface, painted look",
        "style_negative_prompt": "clashing styles, inconsistent lighting, unrealistic elements, indistinct tesserae, blended colors, lack of texture"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_stained_glass_template(main_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Stained Glass Art Preset",
        "moods": ["Luminous", "Spiritual"],
        "aspect_ratio": "9:16", # Common for windows
        "description": "Preset for Stained Glass art, emphasizing vibrant, translucent colors and the interplay of light through leaded panes."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Gothic/Art Nouveau/Contemporary", "post_processing": ["bloom effect"], "style_era": "Varied"},
        "lighting_settings": {"lighting_type": "Backlit", "light_quality": "Transmitted Diffuse", "light_direction": "Behind", "time_of_day": "Daytime"},
        "composition_settings": {"technique": "Leaded Design", "focal_point": "Central Motif/Light Play", "camera_angle": "Eye-level", "perspective": "Flat"},
        "color_settings": {"color_scheme": "Complementary/Analogous", "palette_type": "Vibrant Translucent", "color_temperature": "Varied", "color_contrast": "High", "dominant_colors": ["jewel tones", "primary colors"]},
        "detail_settings": {"detail_level": "Medium", "texture_quality": "Leaded Glass"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Window/Interior", "atmospheric_effects": ["light rays"]},
        "quality_settings": {"resolution": "2160x3840", "rendering_quality": "High"},
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, text, words, amateur, low quality, opaque colors, dull light, painted look",
        "style_negative_prompt": "clashing styles, inconsistent lighting, muddy colors, lack of translucency, missing lead lines, unrealistic light"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_woodcut_template(main_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Woodcut Print Preset",
        "moods": ["Bold", "Graphic"],
        "aspect_ratio": "3:4",
        "description": "Preset for Woodcut prints, characterized by bold lines, strong contrasts, and the texture of relief printing. Often monochromatic."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Printmaking", "post_processing": ["slight grain"], "style_era": "Historical/Modern"},
        "lighting_settings": {"lighting_type": "Flat", "light_quality": "Even", "light_direction": "N/A", "time_of_day": "N/A"}, # Lighting inherent to print style
        "composition_settings": {"technique": "Relief Lines", "focal_point": "Main Subject/Negative Space", "camera_angle": "Direct", "perspective": "Flat"},
        "color_settings": {"color_scheme": "Monochromatic", "palette_type": "High Contrast", "color_temperature": "Neutral", "color_contrast": "Maximum", "dominant_colors": ["black", "white", "sepia"]}, # Or limited color
        "detail_settings": {"detail_level": "Medium", "texture_quality": "Relief Print Texture"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "N/A", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "3072x4096", "rendering_quality": "High"},
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, signature, cut off, draft, text, words, amateur, low quality, smooth shading, photographic, excessive detail",
        "style_negative_prompt": "clashing styles, inconsistent linework, muddy contrasts, pencil sketch look, unintended colors, lack of bold definition"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_traditional_collage_template(main_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Traditional Collage Preset",
        "moods": ["Eclectic", "Textured"],
        "aspect_ratio": "4:5",
        "description": "Preset for Traditional Collage, focusing on the assembly of physical materials like paper, fabric, and found objects, emphasizing texture and layering."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Mixed Media", "post_processing": ["subtle drop shadow for layers"], "style_era": "Modern/Contemporary"},
        "lighting_settings": {"lighting_type": "Studio", "light_quality": "Soft Directional", "light_direction": "Slightly Angled", "time_of_day": "Any"},
        "composition_settings": {"technique": "Juxtaposition of Elements", "focal_point": "Varied/Overall Composition", "camera_angle": "Slightly Above", "perspective": "Shallow Depth"},
        "color_settings": {"color_scheme": "Varied", "palette_type": "Eclectic Mix", "color_temperature": "Neutral", "color_contrast": "Medium-High", "dominant_colors": ["varied based on materials"]},
        "detail_settings": {"detail_level": "High", "texture_quality": "Layered Physical Materials"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Tabletop/Wall Display", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "3200x4000", "rendering_quality": "High"},
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, text, words, amateur, low quality, digital look, seamless blending, flat",
        "style_negative_prompt": "clashing styles, inconsistent lighting, poor composition, unrealistic material interaction, digitally manipulated look (unless intended hybrid), lack of texture definition"
    }
    return {**base_template, "imagen_settings": imagen_settings}
