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
        "style_settings": {"art_movement": "Classical Realism", "post_processing": ["impasto effects", "glazing layers", "sfumato"], "style_era": "17th-19th Century"},
        "lighting_settings": {"lighting_type": "Studio Lighting", "light_quality": "Directional", "light_direction": "Side", "time_of_day": "Indoor"},
        "composition_settings": {"technique": "Rule of Thirds", "focal_point": "Main Subject", "camera_angle": "Eye-level", "perspective": "Linear Perspective"},
        "color_settings": {"color_scheme": "Harmonious", "palette_type": "Rich Saturated", "color_temperature": "Warm", "color_contrast": "High", "dominant_colors": ["earth tones", "deep reds", "rich blues"]},
        "detail_settings": {"detail_level": "Medium", "texture_quality": "Canvas Texture"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Indoor Studio", "atmospheric_effects": ["sfumato"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, text, words, amateur, low quality, digital artifacts, modern elements",
        "style_negative_prompt": "clashing styles, inconsistent lighting, poor composition, unrealistic elements (unless style dictates), generic, boring, flat, anachronistic details"
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
        "style_settings": {"art_movement": "Traditional Watercolor", "post_processing": ["wet-on-wet blending", "paper texture visible", "lifting techniques"], "style_era": "19th Century"},
        "lighting_settings": {"lighting_type": "Natural Backlight", "light_quality": "Luminous", "light_direction": "Behind Subject", "time_of_day": "Daytime"},
        "composition_settings": {"technique": "Negative Space Emphasis", "focal_point": "Main Subject", "camera_angle": "Eye-level", "perspective": "Atmospheric Perspective"},
        "color_settings": {"color_scheme": "Analogous with Complementary Accents", "palette_type": "Transparent Layered", "color_temperature": "Cool", "color_contrast": "Medium-Low", "dominant_colors": ["soft blues", "light greens", "pale yellows"]},
        "detail_settings": {"detail_level": "Medium-Low", "texture_quality": "Watercolor Paper Grain"},
        "environment_settings": {"weather": "Varied", "season": "Any", "location_type": "Outdoor Landscape", "atmospheric_effects": ["light bloom", "misty background"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, text, words, amateur, low quality, opaque paint, harsh lines",
        "style_negative_prompt": "clashing styles, inconsistent lighting, poor composition, muddy colors, overworked areas, lack of transparency"
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
        "style_settings": {"art_movement": "Impressionistic Pastel", "post_processing": ["layered strokes", "velvety texture", "scumbling"], "style_era": "Late 19th Century"},
        "lighting_settings": {"lighting_type": "Soft Natural Light", "light_quality": "Diffused", "light_direction": "Front-Side", "time_of_day": "Daytime"},
        "composition_settings": {"technique": "Broken Color", "focal_point": "Main Subject", "camera_angle": "Eye-level", "perspective": "One-point"},
        "color_settings": {"color_scheme": "Harmonious", "palette_type": "Soft and Powdery", "color_temperature": "Warm", "color_contrast": "Low", "dominant_colors": ["pinks", "lavenders", "light blues", "creams"]},
        "detail_settings": {"detail_level": "Medium", "texture_quality": "Chalky Pastel Texture"},
        "environment_settings": {"weather": "Pleasant", "season": "Spring/Summer", "location_type": "Portrait Setting", "atmospheric_effects": ["soft focus background"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, text, words, amateur, low quality, harsh outlines, muddy colors",
        "style_negative_prompt": "clashing styles, inconsistent lighting, poor composition, overworked pastel, lack of powdery texture"
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
        "style_settings": {"art_movement": "Expressive Realism", "post_processing": ["bold brushstrokes", "quick drying effects", "palette knife work"], "style_era": "Late 20th Century"},
        "lighting_settings": {"lighting_type": "Dynamic Studio Light", "light_quality": "Crisp", "light_direction": "Varied", "time_of_day": "Any"},
        "composition_settings": {"technique": "Strong Forms", "focal_point": "Main Subject", "camera_angle": "Eye-level", "perspective": "One-point"},
        "color_settings": {"color_scheme": "Bold Analogous", "palette_type": "Vibrant Opaque", "color_temperature": "Neutral", "color_contrast": "High", "dominant_colors": ["primary colors", "strong secondary colors"]},
        "detail_settings": {"detail_level": "Medium-High", "texture_quality": "Visible Acrylic Texture"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Contemporary Still Life", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, text, words, amateur, low quality, dull colors, overly blended",
        "style_negative_prompt": "clashing styles, inconsistent lighting, poor composition, lack of vibrancy, muddy colors, weak brushwork"
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
        "style_settings": {"art_movement": "Classical Drawing", "post_processing": ["smudging effects", "strong tonal values", "expressive lines"], "style_era": "Academic Tradition"},
        "lighting_settings": {"lighting_type": "Single Source Dramatic", "light_quality": "High Contrast", "light_direction": "Side", "time_of_day": "Indoor"},
        "composition_settings": {"technique": "Mass Drawing", "focal_point": "Figure/Portrait", "camera_angle": "Eye-level", "perspective": "Naturalistic"},
        "color_settings": {"color_scheme": "Monochromatic", "palette_type": "Grayscale", "color_temperature": "Neutral", "color_contrast": "Maximum", "dominant_colors": ["black", "white", "grey"]},
        "detail_settings": {"detail_level": "High", "texture_quality": "Charcoal Paper Texture"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Life Drawing Studio", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, text, words, amateur, low quality, colored elements, flat shading",
        "style_negative_prompt": "clashing styles, inconsistent lighting, poor composition, lack of tonal range, weak lines, smudged details (unintentionally)"
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
        "style_settings": {"art_movement": "Realistic Sketching", "post_processing": ["hatching", "cross-hatching", "graphite sheen", "varied line weight"], "style_era": "Traditional Sketchbook"},
        "lighting_settings": {"lighting_type": "Natural Ambient", "light_quality": "Soft", "light_direction": "Slightly Above", "time_of_day": "Any"},
        "composition_settings": {"technique": "Contour Drawing", "focal_point": "Subject Detail", "camera_angle": "Eye-level", "perspective": "Naturalistic"},
        "color_settings": {"color_scheme": "Monochromatic", "palette_type": "Grayscale", "color_temperature": "Neutral", "color_contrast": "Medium-High", "dominant_colors": ["graphite grey", "white"]},
        "detail_settings": {"detail_level": "Medium-High", "texture_quality": "Drawing Paper Texture"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Field Sketch", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, text, words, amateur, low quality, colored elements, painted look",
        "style_negative_prompt": "clashing styles, inconsistent lighting, poor composition, smudged lines (unintentionally), lack of detail, flat appearance"
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
        "style_settings": {"art_movement": "Line Art Illustration", "post_processing": ["stippling", "bold outlines", "ink wash", "nib textures"], "style_era": "Classic Illustration"},
        "lighting_settings": {"lighting_type": "Implied by Form", "light_quality": "N/A", "light_direction": "N/A", "time_of_day": "N/A"},
        "composition_settings": {"technique": "Dynamic Line Weight", "focal_point": "Key Elements", "camera_angle": "Direct", "perspective": "Flat or Stylized"},
        "color_settings": {"color_scheme": "Monochromatic", "palette_type": "High Contrast Ink", "color_temperature": "Neutral", "color_contrast": "Maximum", "dominant_colors": ["black", "white"]},
        "detail_settings": {"detail_level": "High", "texture_quality": "Smooth Paper Texture"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Illustration Page", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, text, words, amateur, low quality, colored elements, pencil marks, smudges",
        "style_negative_prompt": "clashing styles, inconsistent line weight, poor composition, broken lines, fuzzy edges, lack of definition"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_drawing_template(main_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Drawing Preset",
        "moods": ["Evocative"],
        "aspect_ratio": "16:9",
        "description": "A balanced preset for the drawing style, focusing on typical characteristics and a specific mood."
    }
    imagen_settings = { # Assuming this is for Colored Pencil Drawing
        "style_settings": {"art_movement": "Realistic Colored Pencil", "post_processing": ["burnishing effects", "layered colors", "solvent blending (simulated)"], "style_era": "Contemporary Realism"},
        "lighting_settings": {"lighting_type": "Soft Studio Light", "light_quality": "Even", "light_direction": "Front-Side", "time_of_day": "Any"},
        "composition_settings": {"technique": "Detailed Layering", "focal_point": "Main Subject", "camera_angle": "Eye-level", "perspective": "Naturalistic"},
        "color_settings": {"color_scheme": "Full Color Spectrum", "palette_type": "Richly Layered Colors", "color_temperature": "Neutral", "color_contrast": "Medium", "dominant_colors": ["varied based on subject"]},
        "detail_settings": {"detail_level": "High", "texture_quality": "Smooth Drawing Paper"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Still Life Setup", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, text, words, amateur, low quality, sketchy lines, flat colors",
        "style_negative_prompt": "clashing styles, inconsistent lighting, poor composition, muddy colors, lack of depth, visible pencil strokes (unless stylistic choice)"
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
        "style_settings": {"art_movement": "Contemporary Illustration", "post_processing": ["opaque layering", "matte finish detail"], "style_era": "Modern"},
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
        "style_settings": {"art_movement": "Early Renaissance", "post_processing": ["none"], "style_era": "Historical"}, # Or "Contemporary" if desired, "none" is good for tempera's clean look
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
        "style_settings": {"art_movement": "Decorative Art", "post_processing": ["sharpen details", "grout lines emphasis"], "style_era": "Ancient/Modern"},
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
        "style_settings": {"art_movement": "Printmaking", "post_processing": ["slight grain", "carved wood texture"], "style_era": "Historical/Modern"},
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
