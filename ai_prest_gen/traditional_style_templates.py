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
