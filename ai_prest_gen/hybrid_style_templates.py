"""Hybrid & Fusion Style Templates Module for AI Preset Generator

This module includes a dedicated function with concrete template logic for each hybrid or fusion style,
migrated fully from style_templates.py. Each function is self-contained, with no placeholders or stubs.
"""

from typing import Dict, Any

def get_kinetic_ascii_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Kinetic ASCII Preset",
        "moods": ["Retro-Tech"],
        "aspect_ratio": "16:9",
        "description": "A dynamic preset blending ANSI/ASCII motion with kinetic text art for a pulsing retro effect."
    }
    imagen_settings = {
        "style_settings": {
            "art_movement": "Techno-Digital",
            "post_processing": ["ascii pattern overlay"],
            "style_era": "Digital"
        },
        "lighting_settings": {
            "lighting_type": "CRT-glow",
            "light_quality": "Simulated phosphor",
            "light_direction": "Grid scan"
        },
        "composition_settings": {
            "technique": "ASCII kinetic motion grid",
            "focal_point": "Animated Symbol Region"
        },
        "color_settings": {
            "color_scheme": "Green Monochrome",
            "palette_type": "monochrome green",
            "color_temperature": "Cool",
            "color_contrast": "Medium"
        },
        "detail_settings": {
            "detail_level": "ASCII Character Detail",
            "texture_quality": "CRT scanline"
        },
        "environment_settings": {
            "weather": "N/A",
            "season": "N/A",
            "location_type": "Console Terminal",
            "atmospheric_effects": ["phosphor flicker"]
        },
        "quality_settings": {
            "resolution": "1280x720",
            "rendering_quality": "Retro Digital"
        },
        "negative_prompt": "realism, full-color photography, smooth gradient, painted texture, signature, watermark, low quality",
        "style_negative_prompt": "natural photo, smooth curves, hand-drawn"
    }
    imagen_settings["kinetic_ascii_settings"] = {
        "motion_type": "animated text-based", "character_set": "ASCII",
        "visual_flow": "left-to-right", "energy_motif": "pulsing symbols",
        "articulation": "frame-based", "aesthetic_blend": "Kinetic movement via ASCII symbols, pulsing text animating; retro-tech/cyber fusion."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_watercolor_pencil_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Watercolor Pencil Preset",
        "moods": ["Dreamy"],
        "aspect_ratio": "4:3",
        "description": "A soft layered preset fusing watercolor washes and precise pencil overlay for a hand-crafted dreamy look."
    }
    imagen_settings = {
        "style_settings": {
            "art_movement": "Mixed Media",
            "post_processing": ["paper texture enhancement"],
            "style_era": "Contemporary"
        },
        "lighting_settings": {
            "lighting_type": "Soft Diffuse",
            "light_quality": "Natural Window",
            "light_direction": "Front"
        },
        "composition_settings": {
            "technique": "Wash-and-sketch layering",
            "focal_point": "Main Subject"
        },
        "color_settings": {
            "color_scheme": "Muted Pastels",
            "palette_type": "soft muted natural tones",
            "color_temperature": "Neutral",
            "color_contrast": "Low"
        },
        "detail_settings": {
            "detail_level": "Medium",
            "texture_quality": "watercolor paper texture with graphite sheen"
        },
        "environment_settings": {
            "weather": "N/A",
            "season": "N/A",
            "location_type": "Studio",
            "atmospheric_effects": ["paper grain"]
        },
        "quality_settings": {
            "resolution": "2048x1536",
            "rendering_quality": "Painterly Soft"
        },
        "negative_prompt": "digital photo, sharp realism, cg, signature, watermark, low quality",
        "style_negative_prompt": "no texture, computer rendering, harsh lines, comic ink",
    }
    imagen_settings["watercolor_pencil_settings"] = {
        "layering_effect": "watercolor washes underlying sharp pencil lines",
        "stroke_quality": "loose pigment wash, fine overlay sketch lines",
        "blend_level": "soft watercolor blend, detailed pencil overlay",
        "paper_type": "textured cold press",
        "aesthetic_blend": "Painterly fluidity with crisp pencil edges; dreamy backgrounds with focused main objects.",
        "color_palette": "soft muted natural tones",
        "brush_stroke": "fluid watercolor wash, precise pencil lines",
        "texture": "visible paper grain, light pigment granulation",
        "detail_level": "medium",
        "watercolor_transparency": "high transparency, layered washes",
        "pencil_shading": "cross-hatching",
        "color_bleeding": "subtle controlled bleeding"
    }
    imagen_settings["composition_settings"]["color_interaction"] = "soft paint washes and linear grayscale pencil marks"
    return {**base_template, "imagen_settings": imagen_settings}

def get_hybrid_traditional_digital_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Hybrid Traditional-Digital Preset",
        "moods": ["Innovative"],
        "aspect_ratio": "16:9",
        "description": "Seamlessly fuses oil painting textures with advanced digital enhancing techniques."
    }
    imagen_settings = {
        "style_settings": {
            "art_movement": "Hybrid",
            "post_processing": ["digital overlay", "contrast boost"],
            "style_era": "Contemporary"
        },
        "lighting_settings": {
            "lighting_type": "Mixed Studio",
            "light_quality": "Blended Source",
            "light_direction": "Front/Top"
        },
        "composition_settings": {
            "technique": "Mixed media layering",
            "focal_point": "Main Hybrid Subject"
        },
        "color_settings": {
            "color_scheme": "Natural Enhanced",
            "palette_type": "natural tones enhanced digitally",
            "color_temperature": "Balanced",
            "color_contrast": "Medium-High"
        },
        "detail_settings": {
            "detail_level": "High",
            "texture_quality": "Visible brush, digital depth"
        },
        "environment_settings": {
            "weather": "N/A",
            "season": "N/A",
            "location_type": "Studio",
            "atmospheric_effects": ["digital light scatter"]
        },
        "quality_settings": {
            "resolution": "3840x2160",
            "rendering_quality": "Hybrid Detail"
        },
        "negative_prompt": "pure digital, lack of texture, cartoon, messy, signature, watermark, low quality",
        "style_negative_prompt": "unblended, harsh digital/composite border, no hand-made elements"
    }
    imagen_settings["hybrid_traditional_digital_settings"] = {
        "media_fusion": "traditional painting (oil) enhanced with digital techniques",
        "techniques": ["digital layering", "digital brushwork enhancement"],
        "color_palette": "natural tones with added digital vibrancy",
        "aesthetic_blend": "Seamless fusion of traditional oil painting textures and digital enhancements for depth.",
        "digital_effects": ["subtle texture overlays", "blending modes for light"],
        "traditional_media": "oil paint on canvas", "digital_tools": "graphics tablet with custom brushes"
    }
    return {**base_template, "imagen_settings": imagen_settings}

# All other hybrid/fusion style template functions, fully implemented from style_templates.py, go below.
# Each function is named get_<hybrid_category>_template(style_category: str) and is a complete template.

def get_installation_art_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Installation Art Preset",
        "moods": ["Immersive"],
        "aspect_ratio": "16:9",
        "description": "A site-specific preset for spatial installation art, merging physical objects and digital projections."
    }
    imagen_settings = {
        "style_settings": {
            "art_movement": "Installation Art",
            "post_processing": ["projection mapping"],
            "style_era": "Contemporary"
        },
        "lighting_settings": {
            "lighting_type": "Dynamic projection-based lighting",
            "light_quality": "Variable",
            "light_direction": "All directions"
        },
        "composition_settings": {
            "view_mode": "immersive 3D space perspective",
            "focal_point": "Central Spatial Object"
        },
        "color_settings": {
            "color_scheme": "Eclectic",
            "palette_type": "site-specific",
            "color_temperature": "Neutral",
            "color_contrast": "Medium"
        },
        "detail_settings": {
            "detail_level": "High",
            "texture_quality": "Tactile/Physical"
        },
        "environment_settings": {
            "weather": "N/A",
            "season": "N/A",
            "location_type": "Exhibit Installation",
            "atmospheric_effects": ["room/floor reflections"]
        },
        "quality_settings": {
            "resolution": "Variable",
            "rendering_quality": "Spatial Detail"
        },
        "negative_prompt": "flat panel, small 2D, illustration, photo, low quality",
        "style_negative_prompt": "wall-hung only, generic sculpture, no digital/projection",
    }
    imagen_settings["installation_art_settings"] = {
        "media": "mixed media with found objects and spatial elements", "scale": "large room-scale",
        "interaction": "participatory digital interaction", "spatial_arrangement": "site-specific modular design",
        "technology_integration": "projection mapping and sensors",
        "aesthetic_blend": "Spatial and immersive art combining physical materials with digital projections and interactivity."
    }
    imagen_settings["lighting_settings"]["lighting_type"] = "dynamic projection-based lighting"
    return {**base_template, "imagen_settings": imagen_settings}

def get_scientific_technological_hybrid_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Technological Hybrid Preset",
        "moods": ["High-Tech"],
        "aspect_ratio": "16:9",
        "description": "A vivid preset for artistic expression marrying scientific data-visualization and generative AI techniques."
    }
    imagen_settings = {
        "style_settings": {
            "art_movement": "Technological Art",
            "post_processing": ["data-derived overlays"],
            "style_era": "Cutting-Edge"
        },
        "lighting_settings": {
            "lighting_type": "Luminous Highlighting",
            "light_quality": "High contrast",
            "light_direction": "Backlit"
        },
        "composition_settings": {
            "technique": "algorithmic composition",
            "focal_point": "Data Node"
        },
        "color_settings": {
            "color_scheme": "High contrast",
            "palette_type": "data-inspired",
            "color_temperature": "Cool",
            "color_contrast": "High"
        },
        "detail_settings": {
            "detail_level": "High",
            "texture_quality": "Digital"
        },
        "environment_settings": {
            "weather": "N/A",
            "season": "N/A",
            "location_type": "Tech Lab/Exhibit",
            "atmospheric_effects": ["digital aura"]
        },
        "quality_settings": {
            "resolution": "4096x2160",
            "rendering_quality": "High"
        },
        "negative_prompt": "organic, flat, bland, hand-drawn, signature, watermark, low quality",
        "style_negative_prompt": "non-digital, traditional only, no data",
    }
    imagen_settings["scientific_technological_hybrid_settings"] = {
        "media": "digital media and scientific visualization", "concept": "data-driven algorithmic generation",
        "technology": "AI generation with interactive software elements", "data_visualization_methods": "3D models derived from data",
        "interactivity_level": "interactive",
        "aesthetic_blend": "Artistic expression integrating scientific data visualization and cutting-edge technology."
    }
    imagen_settings["composition_settings"]["technique"] = "algorithmic composition"
    return {**base_template, "imagen_settings": imagen_settings}

def get_augmented_reality_art_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Augmented Reality Art Preset",
        "moods": ["Immersive"],
        "aspect_ratio": "16:9",
        "description": "A layered template for digital art built for AR overlays and mixed reality viewing."
    }
    imagen_settings = {
        "style_settings": {
            "art_movement": "Augmented/Mixed Reality",
            "post_processing": ["3D object overlay"],
            "style_era": "Contemporary"
        },
        "lighting_settings": {
            "lighting_type": "Environmental/AR matched",
            "light_quality": "Mixed real/virtual",
            "light_direction": "Matched to physical"
        },
        "composition_settings": {
            "view_mode": "mixed reality interactive view",
            "focal_point": "Main AR Subject"
        },
        "color_settings": {
            "color_scheme": "Physically Adaptive",
            "palette_type": "flexible",
            "color_temperature": "Adaptive",
            "color_contrast": "Variable"
        },
        "detail_settings": {
            "detail_level": "High",
            "texture_quality": "Crisp 3D"
        },
        "environment_settings": {
            "weather": "Adaptive",
            "season": "Adaptive",
            "location_type": "Physical/Simulated overlay",
            "atmospheric_effects": ["dynamic shadows", "motion transparency"]
        },
        "quality_settings": {
            "resolution": "Device Native",
            "rendering_quality": "Mixed Reality Polished"
        },
        "negative_prompt": "static flat art, 2D only, non-overlaid, signature, watermark, low quality",
        "style_negative_prompt": "hard-edged transition, non-adaptive"
    }
    imagen_settings["augmented_reality_art_settings"] = {
        "media": "3D modeling overlayed onto physical space", "interaction": "user-driven immersive experience",
        "technology": "AR devices with real-time rendering", "tracking_methods": "markerless location-based",
        "user_interface": "gesture control",
        "aesthetic_blend": "Blending virtual 3D models and physical realities through interactive digital art."
    }
    imagen_settings["lighting_settings"]["lighting_type"] = "dynamic real-time lighting matching environment"
    return {**base_template, "imagen_settings": imagen_settings}

def get_abstract_expressionism_cubism_fusion_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Abstract Expressionism/Cubism Fusion Preset",
        "moods": ["Chaotic"],
        "aspect_ratio": "16:9",
        "description": "Explosive abstraction and fragmenting geometry are fused in this raw, dynamic art style preset."
    }
    imagen_settings = {
        "style_settings": {
            "art_movement": "Abstract Expressionism, Cubism",
            "post_processing": ["dynamic composite"],
            "style_era": "Modern"
        },
        "lighting_settings": {
            "lighting_type": "Studio/Algorithmic",
            "light_quality": "Variable",
            "light_direction": "Multiple"
        },
        "composition_settings": {
            "technique": "expressive abstraction with geometric fragmentation",
            "focal_point": "Dynamic Confluence"
        },
        "color_settings": {
            "color_scheme": "Bold Contrasts",
            "palette_type": "bold emotive contrasting",
            "color_temperature": "Mixed",
            "color_contrast": "High"
        },
        "detail_settings": {
            "detail_level": "High",
            "texture_quality": "Brushstroke and Geometric"
        },
        "environment_settings": {
            "weather": "N/A",
            "season": "N/A",
            "location_type": "Abstract",
            "atmospheric_effects": ["energetic form"]
        },
        "quality_settings": {
            "resolution": "3840x2160",
            "rendering_quality": "Polished Modern"
        },
        "negative_prompt": "photoreal, staged, low intensity, flat, signature, watermark, low quality",
        "style_negative_prompt": "orderly, soft contrast, blended, realism"
    }
    imagen_settings["abstract_expressionism_cubism_fusion_settings"] = {
        "form_style": "gestural brushwork combined with fragmented geometry", "color_palette": "bold contrasting emotive colors",
        "composition": "layered dynamic abstract forms", "emotional_intensity": "high raw spontaneous energy",
        "spatial_distortion": "multiple perspectives and fractured planes",
        "aesthetic_blend": "Fusion of abstract expressionism's raw emotion with cubism's structured deconstruction."
    }
    imagen_settings["composition_settings"]["technique"] = "expressive abstraction with geometric fragmentation"
    return {**base_template, "imagen_settings": imagen_settings}

def get_collage_digital_overlay_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Collage Digital Overlay Preset",
        "moods": ["Eclectic"],
        "aspect_ratio": "16:9",
        "description": "A vibrant preset for collage-based art with integrated digital overlays and tactile paper textures."
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
    imagen_settings["collage_digital_overlay_settings"] = {
        "media": "paper collage base with digital textures and photo manipulation",
        "texture": "layered tactile paper with digital enhancements",
        "color_palette": "eclectic vibrant colors",
        "assembly_methods": "torn and layered paper with digital stitching effect",
        "digital_effects": ["blending modes", "opacity masks", "subtle filters"],
        "aesthetic_blend": "Combining tactile collage elements with seamless digital overlays for a rich visual narrative."
    }
    imagen_settings["composition_settings"]["technique"] = "mixed media collage with integrated digital effects"
    imagen_settings["color_settings"]["palette_type"] = "vibrant eclectic mixed palette"
    return {**base_template, "imagen_settings": imagen_settings}

def get_claymation_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Claymation Preset",
        "moods": ["Whimsical"],
        "aspect_ratio": "4:3",
        "description": "A whimsical preset for claymation style, focusing on tactile textures and playful character designs."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Claymation", "post_processing": ["visible fingerprints"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Miniature set studio lighting", "light_quality": "Soft warm directional", "light_direction": "Front"},
        "composition_settings": {"technique": "Stop-motion framing", "focal_point": "Character"},
        "color_settings": {"color_scheme": "Vibrant Saturated", "palette_type": "vibrant saturated primary colors", "color_temperature": "Warm", "color_contrast": "Medium"},
        "detail_settings": {"detail_level": "Medium", "texture_quality": "clay-like matte surface"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Miniature handcrafted whimsical set", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "1080p", "rendering_quality": "Handcrafted Look"},
        "negative_prompt": "smooth cg, photorealistic, sharp edges, signature, watermark, low quality",
        "style_negative_prompt": "digital rendering, no texture, realistic proportions"
    }
    imagen_settings["claymation_settings"] = {
        "media": "plasticine stop-motion animation look", "texture": "tactile hand-molded surface with visible fingerprints",
        "color_palette": "vibrant saturated playful colors", "lighting": "soft warm directional studio lighting",
        "animation_style": "stop-motion frame-by-frame appearance",
        "aesthetic_blend": "Whimsical handcrafted look with visible textures and playful character designs.",
        "character_design": "exaggerated features simple forms", "surface_detail": "fingerprints visible tool marks",
        "animation_style_hint": "stop-motion look", "set_design": "miniature handcrafted whimsical set"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_experimental_mixed_media_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Experimental Mixed Media Preset",
        "moods": ["Experimental", "Avant-Garde"],
        "aspect_ratio": "16:9",
        "description": "An avant-garde preset combining unconventional materials with digital manipulation."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Experimental Art", "post_processing": ["digital manipulation"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Varied", "light_quality": "Unpredictable", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Layering and deconstruction", "focal_point": "Abstract"},
        "color_settings": {"color_scheme": "Varied", "palette_type": "varied unpredictable palette", "color_temperature": "Mixed", "color_contrast": "High"},
        "detail_settings": {"detail_level": "High", "texture_quality": "Varied unconventional textures"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Abstract", "atmospheric_effects": ["unpredictable"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "conventional, realistic, boring, signature, watermark, low quality",
        "style_negative_prompt": "traditional media only, predictable composition"
    }
    imagen_settings["experimental_mixed_media_settings"] = {
        "media": "unconventional materials combined with digital manipulation", "techniques": ["layering", "deconstruction", "reassembly"],
        "concept": "avant-garde boundary-pushing exploration",
        "aesthetic_blend": "Innovative combinations of physical materials and digital techniques challenging traditional art forms."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_patchwork_collage_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Patchwork Collage Preset",
        "moods": ["Folk", "Textile"],
        "aspect_ratio": "1:1",
        "description": "A tactile preset combining fabric scraps, paper, and found objects with a layered, stitched appearance."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Folk Art", "post_processing": ["stitched seams"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Soft Ambient", "light_quality": "Diffuse", "light_direction": "Top"},
        "composition_settings": {"technique": "Patchwork collage assembly", "focal_point": "Pattern"},
        "color_settings": {"color_scheme": "Bold Contrasting", "palette_type": "bold contrasting folk-inspired colors", "color_temperature": "Warm", "color_contrast": "High"},
        "detail_settings": {"detail_level": "High", "texture_quality": "tactile rough varied textures"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Studio", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "2048x2048", "rendering_quality": "Textile Detail"},
        "negative_prompt": "smooth, digital, photorealistic, signature, watermark, low quality",
        "style_negative_prompt": "flat colors, no texture, uniform pattern"
    }
    imagen_settings["patchwork_collage_settings"] = {
        "material_mix": ["fabric scraps", "textured paper", "found objects"], "assembly_style": "layered and stitched appearance",
        "texture_emphasis": "tactile rough varied textures", "color_palette": "bold contrasting folk-inspired colors",
        "pattern_variation": "varied patch sizes shapes and colors",
        "aesthetic_blend": "Bold textures and patterns combined into cohesive compositions; folk art and craft influences."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_paper_quilling_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Paper Quilling Preset",
        "moods": ["Delicate", "Intricate"],
        "aspect_ratio": "1:1",
        "description": "An intricate preset for paper quilling art, focusing on delicate rolled paper shapes and patterns."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Paper Art", "post_processing": ["layered depth"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Soft Directional", "light_quality": "Highlights layers", "light_direction": "Side"},
        "composition_settings": {"technique": "Intricate pattern assembly", "focal_point": "Detail", "depth": "layered dimensional relief"},
        "color_settings": {"color_scheme": "Bright Contrasting", "palette_type": "bright and soft pastels", "color_temperature": "Neutral", "color_contrast": "Medium"},
        "detail_settings": {"detail_level": "Very High", "texture_quality": "crisp paper texture"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Studio", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "3000x3000", "rendering_quality": "Intricate Detail"},
        "negative_prompt": "flat, 2d, painting, drawing, signature, watermark, low quality",
        "style_negative_prompt": "no depth, blurry, unrealistic paper texture"
    }
    imagen_settings["paper_quilling_settings"] = {
        "coil_types": "tight and loose shaped coils", "paper_strip_width": "narrow strips",
        "pattern_density": "dense intricate patterns", "color_scheme": "bright contrasting colors",
        "aesthetic_blend": "Intricate rolled paper shapes forming delicate, decorative 3D patterns."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_tradigital_mixed_media_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Tradigital Mixed Media Preset",
        "moods": ["Textured", "Blended"],
        "aspect_ratio": "16:9",
        "description": "A rich preset fusing traditional acrylic painting with digital enhancement for seamless textures."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Mixed Media", "post_processing": ["digital enhancement"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Mixed Studio", "light_quality": "Blended", "light_direction": "Front"},
        "composition_settings": {"technique": "Mixed media layering with digital refinement", "focal_point": "Main Subject"},
        "color_settings": {"color_scheme": "Natural Enhanced", "palette_type": "natural enhanced palette", "color_temperature": "Balanced", "color_contrast": "Medium"},
        "detail_settings": {"detail_level": "High", "texture_quality": "visible brush strokes with subtle digital overlays"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Studio", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "Hybrid Detail"},
        "negative_prompt": "pure digital, lack of texture, cartoon, signature, watermark, low quality",
        "style_negative_prompt": "unblended, harsh digital/composite border"
    }
    imagen_settings["tradigital_mixed_media_settings"] = {
        "media_fusion": "traditional painting (acrylic) with digital enhancement", "texture_blend": "visible brush strokes with subtle digital overlays",
        "color_interaction": "natural painted colors with enhanced digital lighting",
        "aesthetic_blend": "Seamless integration of traditional acrylic painting and digital techniques for rich textures."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_whimsical_mixed_media_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Whimsical Mixed Media Preset",
        "moods": ["Playful", "Dreamy", "Whimsical"],
        "aspect_ratio": "1:1",
        "description": "A lighthearted preset combining various media with fantasy elements and playful accents."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Mixed Media", "post_processing": ["layered textures"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Soft Ambient", "light_quality": "Diffuse", "light_direction": "Front"},
        "composition_settings": {"technique": "Layered composition", "focal_point": "Playful elements"},
        "color_settings": {"color_scheme": "Pastel Dreamy", "palette_type": "pastel dreamy colors", "color_temperature": "Cool", "color_contrast": "Low"},
        "detail_settings": {"detail_level": "Medium", "texture_quality": "light airy layered textures"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Studio", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "2048x2048", "rendering_quality": "Painterly Soft"},
        "negative_prompt": "harsh, realistic, dark, signature, watermark, low quality",
        "style_negative_prompt": "serious mood, high contrast, sharp edges"
    }
    imagen_settings["whimsical_mixed_media_settings"] = {
        "motifs": ["mythical creatures", "soft colors", "playful elements", "stars"], "texture": "light airy layered textures",
        "color_palette": "pastel dreamy colors",
        "aesthetic_blend": "Lighthearted, dreamy compositions with fantasy elements and playful accents."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_sci_fi_futuristic_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Sci-Fi Futuristic Preset",
        "moods": ["High-Tech", "Futuristic"],
        "aspect_ratio": "16:9",
        "description": "A vivid preset for artistic expression marrying scientific data-visualization and generative AI techniques."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Technological Art", "post_processing": ["data-derived overlays"], "style_era": "Cutting-Edge"},
        "lighting_settings": {"lighting_type": "Luminous Highlighting", "light_quality": "High contrast", "light_direction": "Backlit"},
        "composition_settings": {"technique": "algorithmic composition", "focal_point": "Data Node", "view_mode": "panoramic dynamic perspective"},
        "color_settings": {"color_scheme": "High contrast", "palette_type": "data-inspired", "color_temperature": "Cool", "color_contrast": "High"},
        "detail_settings": {"detail_level": "High", "texture_quality": "Digital"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Tech Lab/Exhibit", "atmospheric_effects": ["digital aura"]},
        "quality_settings": {"resolution": "4096x2160", "rendering_quality": "High"},
        "negative_prompt": "organic, flat, bland, hand-drawn, signature, watermark, low quality",
        "style_negative_prompt": "non-digital, traditional only, no data"
    }
    imagen_settings["sci_fi_futuristic_settings"] = {
        "technology_level": "highly advanced cybernetic space-age", "environment": "futuristic cities space stations alien landscapes",
        "lighting": "neon holographic cold dynamic lighting", "color_palette": "metallic neon dark vibrant colors",
        "special_effects": ["holograms", "lens flares", "digital rain effects"],
        "aesthetic_blend": "Futuristic and cyberpunk visual elements combined with high-tech aesthetics."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_mediterranean_style_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Mediterranean Style Preset",
        "moods": ["Lively", "Warm", "Sunny"],
        "aspect_ratio": "16:9",
        "description": "A vibrant preset for Mediterranean style, focusing on coastal scenes and warm colors."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Regional Art", "post_processing": ["warm color grading"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Bright Natural Sunlight", "light_quality": "Warm glow", "light_direction": "Top"},
        "composition_settings": {"technique": "Rule of Thirds", "focal_point": "Landscape/Architecture"},
        "color_settings": {"color_scheme": "Warm Bright", "palette_type": "warm bright mediterranean blues and whites", "color_temperature": "Warm", "color_contrast": "Medium"},
        "detail_settings": {"detail_level": "Medium", "texture_quality": "Realistic"},
        "environment_settings": {"weather": "Clear", "season": "Summer", "location_type": "Coastal Village", "atmospheric_effects": ["subtle haze"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "dark, cold colors, industrial, signature, watermark, low quality",
        "style_negative_prompt": "unrealistic colors, wrong architecture"
    }
    imagen_settings["mediterranean_style_settings"] = {
        "environment": "sunny coastal scenes vibrant landscapes", "color_palette": "warm bright natural colors (blues, whites, terracotta)",
        "lighting": "bright natural sunlight warm glow",
        "aesthetic_blend": "Vivid, colorful depictions of Mediterranean life, architecture, and scenery."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_morphism_surreal_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Morphism Surreal Preset",
        "moods": ["Surreal", "Dreamlike"],
        "aspect_ratio": "16:9",
        "description": "A surreal preset focusing on fluid, fantastical morphing transformations."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Surrealism", "post_processing": ["fluid transformations"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Dreamlike", "light_quality": "Soft and shifting", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Surreal morphing composition", "focal_point": "Transformation"},
        "color_settings": {"color_scheme": "Vibrant Dreamlike", "palette_type": "vibrant dreamlike colors", "color_temperature": "Mixed", "color_contrast": "Medium"},
        "detail_settings": {"detail_level": "High", "texture_quality": "Smooth and fluid"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Dreamscape", "atmospheric_effects": ["mist", "glow"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "High"},
        "negative_prompt": "realistic, static, logical, signature, watermark, low quality",
        "style_negative_prompt": "rigid forms, clear boundaries"
    }
    imagen_settings["morphism_surreal_settings"] = {
        "transformation_style": "surreal fluid fantastical morphing", "color_palette": "vibrant dreamlike colors",
        "composition": "morphing shapes illogical progressions",
        "aesthetic_blend": "Surreal transformations where objects fluidly blend or change form with fantastical and dreamlike qualities."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_cubism_mixed_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Cubism Mixed Preset",
        "moods": ["Geometric", "Fragmented"],
        "aspect_ratio": "1:1",
        "description": "A geometric preset combining Cubist principles with mixed media textures."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Cubism", "post_processing": ["geometric fragmentation"], "style_era": "Modern"},
        "lighting_settings": {"lighting_type": "Geometric", "light_quality": "Hard-edged", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Cubist fragmentation with mixed media", "focal_point": "Fragmented Subject"},
        "color_settings": {"color_scheme": "Muted Earthy", "palette_type": "muted earthy tones with bold accents", "color_temperature": "Neutral", "color_contrast": "High"},
        "detail_settings": {"detail_level": "High", "texture_quality": "geometric abstraction with layered planes and mixed media textures"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Abstract", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "2048x2048", "rendering_quality": "Geometric Detail"},
        "negative_prompt": "realistic, smooth, organic, signature, watermark, low quality",
        "style_negative_prompt": "blended forms, soft edges"
    }
    imagen_settings["cubism_mixed_settings"] = {
        "form_style": "angular fragmented forms with multiple perspectives", "color_palette": "muted earthy tones with bold accents",
        "composition": "geometric abstraction with layered planes and mixed media textures",
        "aesthetic_blend": "Classic Cubist style principles combined with mixed media elements and modern influences."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_pixel_patchwork_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Pixel Patchwork Preset",
        "moods": ["Retro", "Geometric"],
        "aspect_ratio": "1:1",
        "description": "A retro preset combining pixel art and voxel art with a quilt-like composition."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Digital Art", "post_processing": ["pixelation", "voxelization"], "style_era": "Retro"},
        "lighting_settings": {"lighting_type": "Flat", "light_quality": "Hard-edged", "light_direction": "Top"},
        "composition_settings": {"technique": "Grid-based composition", "focal_point": "Pattern", "view_mode": "isometric grid-based view"},
        "color_settings": {"color_scheme": "Limited Vibrant", "palette_type": "limited vibrant 8-bit palette", "color_temperature": "Neutral", "color_contrast": "High"},
        "detail_settings": {"detail_level": "Low", "texture_quality": "blocky geometric pixelated texture"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Abstract Grid", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "512x512", "rendering_quality": "Pixelated"},
        "negative_prompt": "smooth, realistic, organic, signature, watermark, low quality",
        "style_negative_prompt": "high detail, blended colors"
    }
    imagen_settings["pixel_patchwork_settings"] = {
        "pixel_style": "pixel art combined with voxel art elements", "color_palette": "limited vibrant 8-bit palette",
        "texture": "blocky geometric pixelated texture",
        "aesthetic_blend": "Pixelated and geometric patchwork style combining digital retro motifs with quilt-like composition."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_phygital_hybrid_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Phygital Hybrid Preset",
        "moods": ["Innovative", "Interactive"],
        "aspect_ratio": "16:9",
        "description": "A hybrid preset blending physical sculpture with augmented reality digital art."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Hybrid Art", "post_processing": ["AR overlay"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Mixed Real/Virtual", "light_quality": "Adaptive", "light_direction": "Matched to physical"},
        "composition_settings": {"technique": "Hybrid physical-digital layering", "focal_point": "Integrated Subject"},
        "color_settings": {"color_scheme": "Varied", "palette_type": "varied palette bridging physical and digital", "color_temperature": "Adaptive", "color_contrast": "Variable"},
        "detail_settings": {"detail_level": "High", "texture_quality": "Mixed physical and digital"},
        "environment_settings": {"weather": "Adaptive", "season": "Adaptive", "location_type": "Physical Space with AR Overlay", "atmospheric_effects": ["dynamic shadows"]},
        "quality_settings": {"resolution": "Device Native", "rendering_quality": "Mixed Reality"},
        "negative_prompt": "purely physical, purely digital, flat, signature, watermark, low quality",
        "style_negative_prompt": "unblended, non-interactive"
    }
    imagen_settings["phygital_hybrid_settings"] = {
        "media_fusion": "physical sculpture combined with augmented reality digital art", "technology": "AR tracking with 3D printing elements",
        "aesthetic_blend": "Hybrid physical/digital artwork blending real object presence with interactive virtual elements."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_screen_printing_bold_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Screen Printing Bold Preset",
        "moods": ["Graphic", "Bold"],
        "aspect_ratio": "1:1",
        "description": "A bold graphic preset reminiscent of screen printing with tactile qualities and strong contrasts."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Graphic Design", "post_processing": ["layered ink effect"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Flat Graphic", "light_quality": "Hard-edged", "light_direction": "Top"},
        "composition_settings": {"technique": "Screen printing graphic style", "focal_point": "Bold shapes"},
        "color_settings": {"color_scheme": "Limited High Contrast", "palette_type": "limited high contrast colors (e.g., 2-3 colors)", "color_temperature": "Neutral", "color_contrast": "Very High"},
        "detail_settings": {"detail_level": "Medium", "texture_quality": "flat layered ink texture with slight misregistration effect"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Print Studio", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "2048x2048", "rendering_quality": "Graphic Print"},
        "negative_prompt": "gradients, blending, photorealistic, signature, watermark, low quality",
        "style_negative_prompt": "soft edges, many colors"
    }
    imagen_settings["screen_printing_bold_settings"] = {
        "print_style": "bold graphic tactile screen print", "color_palette": "limited high contrast colors (e.g., 2-3 colors)",
        "texture": "flat layered ink texture with slight misregistration effect",
        "aesthetic_blend": "Bold graphic prints reminiscent of serigraphy with tactile qualities and strong visual contrasts."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_mixed_media_journaling_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Mixed Media Journaling Preset",
        "moods": ["Personal", "Whimsical", "Creative"],
        "aspect_ratio": "4:5",
        "description": "An eclectic preset for art journal style, combining various media with personal and whimsical elements."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Art Journaling", "post_processing": ["layered textures"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Soft Ambient", "light_quality": "Diffuse", "light_direction": "Top"},
        "composition_settings": {"technique": "Layered composition", "focal_point": "Personal elements"},
        "color_settings": {"color_scheme": "Varied Eclectic", "palette_type": "varied eclectic personal palette", "color_temperature": "Mixed", "color_contrast": "Medium"},
        "detail_settings": {"detail_level": "High", "texture_quality": "layered varied textures (paper, paint, fabric)"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Studio/Desk", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "2048x2560", "rendering_quality": "Textured"},
        "negative_prompt": "clean, digital, photorealistic, signature, watermark, low quality",
        "style_negative_prompt": "uniform texture, predictable layout"
    }
    imagen_settings["mixed_media_journaling_settings"] = {
        "media": ["collage elements", "pencil sketch", "watercolor wash", "ink stamps", "handwritten text"],
        "texture": "layered varied textures (paper, paint, fabric)", "color_palette": "eclectic varied personal palette",
        "aesthetic_blend": "Eclectic, layered mixed media style typical of art journals, with personal and whimsical elements."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_digital_pixel_traditional_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Digital Pixel Traditional Preset",
        "moods": ["Retro", "Painterly"],
        "aspect_ratio": "16:9",
        "description": "A fusion preset combining digital pixel art characters with traditional painted backgrounds."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Hybrid Art", "post_processing": ["pixelation", "painterly effect"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Mixed", "light_quality": "Varied", "light_direction": "Front"},
        "composition_settings": {"technique": "Hybrid media juxtaposition", "focal_point": "Character"},
        "color_settings": {"color_scheme": "Vibrant Mixed", "palette_type": "vibrant mixed pixel/painterly palette", "color_temperature": "Mixed", "color_contrast": "High"},
        "detail_settings": {"detail_level": "Mixed", "texture_quality": "pixelated character texture contrasted with painterly background texture"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Fantasy Landscape", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "Hybrid"},
        "negative_prompt": "uniform style, photorealistic, signature, watermark, low quality",
        "style_negative_prompt": "unblended styles, inconsistent resolution"
    }
    imagen_settings["digital_pixel_traditional_settings"] = {
        "media_fusion": "digital pixel art characters combined with traditional painted background",
        "color_palette": "vibrant mixed palette (pixelated foreground, painterly background)",
        "texture": "pixelated character texture contrasted with painterly background texture",
        "aesthetic_blend": "Fusion of distinct pixel art style for subjects and traditional painting techniques for environment."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_patchwork_fabric_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Patchwork Fabric Preset",
        "moods": ["Textile", "Craft"],
        "aspect_ratio": "1:1",
        "description": "A tactile preset for textile patchwork art with warm, tactile qualities and visible stitching."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Textile Art", "post_processing": ["stitched seams"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Soft Ambient", "light_quality": "Diffuse", "light_direction": "Top"},
        "composition_settings": {"technique": "Fabric layering and quilting patterns", "focal_point": "Pattern"},
        "color_settings": {"color_scheme": "Warm Earthy", "palette_type": "warm earthy fabric colors", "color_temperature": "Warm", "color_contrast": "Medium"},
        "detail_settings": {"detail_level": "High", "texture_quality": "soft tactile fabric textures"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Studio", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "2048x2048", "rendering_quality": "Textile Detail"},
        "negative_prompt": "smooth, digital, photorealistic, signature, watermark, low quality",
        "style_negative_prompt": "flat colors, no texture, uniform pattern"
    }
    imagen_settings["patchwork_fabric_settings"] = {
        "material": "various fabric textiles", "assembly": "sewn and layered fabric patches",
        "texture": "soft tactile fabric textures", "color_palette": "warm earthy fabric colors",
        "aesthetic_blend": "Textile patchwork art with warm, tactile qualities and visible stitching."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_mixed_media_collage_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Mixed Media Collage Preset",
        "moods": ["Eclectic", "Textured"],
        "aspect_ratio": "1:1",
        "description": "An eclectic preset combining diverse physical media and textures into a cohesive piece."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Mixed Media", "post_processing": ["layered textures"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Soft Ambient", "light_quality": "Diffuse", "light_direction": "Top"},
        "composition_settings": {"technique": "Collage assembly and layering", "focal_point": "Pattern"},
        "color_settings": {"color_scheme": "Varied Eclectic", "palette_type": "varied eclectic color palette", "color_temperature": "Mixed", "color_contrast": "Medium"},
        "detail_settings": {"detail_level": "High", "texture_quality": "highly layered tactile textures"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Studio", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "2048x2048", "rendering_quality": "Textured"},
        "negative_prompt": "smooth, digital, photorealistic, signature, watermark, low quality",
        "style_negative_prompt": "uniform texture, predictable layout"
    }
    imagen_settings["mixed_media_collage_settings"] = {
        "media": ["paper cutouts", "acrylic paint", "found objects", "fabric scraps"], "texture": "highly layered tactile textures",
        "color_palette": "varied eclectic color palette",
        "aesthetic_blend": "Eclectic collage combining diverse physical media and textures into a cohesive piece."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_whimsical_fantasy_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Whimsical Fantasy Preset",
        "moods": ["Dreamy", "Playful", "Magical"],
        "aspect_ratio": "16:9",
        "description": "A dreamy preset for fantasy illustration with playful characters and soft, whimsical elements."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Fantasy Illustration", "post_processing": ["glittery effects"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Soft Ambient", "light_quality": "Ethereal", "light_direction": "Top"},
        "composition_settings": {"technique": "Layered composition", "focal_point": "Characters"},
        "color_settings": {"color_scheme": "Pastel Soft", "palette_type": "pastel soft fantasy palette", "color_temperature": "Cool", "color_contrast": "Low"},
        "detail_settings": {"detail_level": "High", "texture_quality": "soft layered textures with glittery effects"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Enchanted Forest", "atmospheric_effects": ["mist", "sparkles"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "Painterly Soft"},
        "negative_prompt": "harsh, realistic, dark, signature, watermark, low quality",
        "style_negative_prompt": "serious mood, high contrast, sharp edges"
    }
    imagen_settings["whimsical_fantasy_settings"] = {
        "motifs": ["fantasy creatures (fairies, sprites)", "pastel colors", "dreamy atmosphere", "sparkling elements"],
        "texture": "soft layered textures with glittery effects", "color_palette": "pastel soft color palette",
        "aesthetic_blend": "Dreamy fantasy illustration style with playful characters and soft, whimsical elements."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_anime_oilpainting_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Anime Oil Painting Preset",
        "moods": ["Painterly", "Stylized"],
        "aspect_ratio": "16:9",
        "description": "A fusion preset combining anime character forms with the texture and lighting of traditional oil painting."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Hybrid Art", "post_processing": ["oil brush glaze"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Soft Rim Lighting", "light_quality": "Oil brush glaze technique", "light_direction": "Side"},
        "composition_settings": {"technique": "Stylized character focus", "focal_point": "Character"},
        "color_settings": {"color_scheme": "Pastel with Vivid Accents", "palette_type": "pastel skin tones with vivid accent colors", "color_temperature": "Warm", "color_contrast": "Medium"},
        "detail_settings": {"detail_level": "High", "texture_quality": "oil paint impasto texture"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Studio", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "3840x2160", "rendering_quality": "Painterly Stylized"},
        "negative_prompt": "pure anime, pure oil painting, signature, watermark, low quality",
        "style_negative_prompt": "unblended styles, flat colors"
    }
    imagen_settings["anime_oilpainting_settings"] = {
        "character_design": "large-eyed shoujo style with painterly highlights", "canvas_type": "visible linen canvas texture",
        "lighting": "soft rim lighting with oil brush glaze technique", "stroke_emphasis": "visible impasto brush strokes blended with cell shading hints",
        "aesthetic_blend": "Classic anime character forms rendered with the volume, texture, and lighting of traditional oil painting."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_minimalist_geometric_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Minimalist Geometric Preset",
        "moods": ["Minimal", "Clean"],
        "aspect_ratio": "1:1",
        "description": "An abstract preset focusing on extreme geometric abstraction, negative space, and balance."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Minimalism", "post_processing": ["flat color projection"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Flat Ambient", "light_quality": "Low noise", "light_direction": "Top"},
        "composition_settings": {"technique": "Geometric abstraction with asymmetric balance", "focal_point": "Negative space"},
        "color_settings": {"color_scheme": "Pastel Monochrome", "palette_type": "pastel monochrome limited palette", "color_temperature": "Cool", "color_contrast": "Low"},
        "detail_settings": {"detail_level": "Low", "texture_quality": "Smooth"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Abstract", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "2048x2048", "rendering_quality": "Clean Graphic"},
        "negative_prompt": "high detail, complex, organic, signature, watermark, low quality",
        "style_negative_prompt": "busy composition, varied colors"
    }
    imagen_settings["minimalist_geometric_settings"] = {
        "geometry_focus": ["circles", "squares"],
        "simplicity": "3 or fewer primary shapes with limited lines", "style": "flat color projection low noise pastel palette",
        "aesthetic_blend": "Extreme geometric abstraction focusing on negative space, balance, and proportional rhythm."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_pop_surrealism_ascii_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Pop Surrealism ASCII Preset",
        "moods": ["Retro-Tech", "Surreal"],
        "aspect_ratio": "16:9",
        "description": "A bizarre preset combining pop surrealist subjects with ASCII character mosaics."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Pop Surrealism", "post_processing": ["ascii character overlay"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "CRT-glow", "light_quality": "Simulated phosphor", "light_direction": "Grid scan"},
        "composition_settings": {"technique": "ASCII mosaic composition", "focal_point": "Subject"},
        "color_settings": {"color_scheme": "Monochrome", "palette_type": "monochrome green on black (classic terminal)", "color_temperature": "Cool", "color_contrast": "High"},
        "detail_settings": {"detail_level": "Medium", "texture_quality": "ASCII character texture"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Console Terminal", "atmospheric_effects": ["phosphor flicker"]},
        "quality_settings": {"resolution": "1280x720", "rendering_quality": "Retro Digital"},
        "negative_prompt": "realism, full-color photography, smooth gradient, signature, watermark, low quality",
        "style_negative_prompt": "natural photo, smooth curves"
    }
    imagen_settings["pop_surrealism_ascii_settings"] = {
        "icon_motif": "pop culture icon rendered in ASCII", "visual_irony": "strange surreal objects outlined with ASCII characters",
        "pattern_density": "medium density ASCII pattern",
        "aesthetic_blend": "Cartoonish or lowbrow pop surrealist subjects re-rendered as digital character mosaics, creating a bizarre and playful fusion."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_dreamcore_weirdcore_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Dreamcore Weirdcore Preset",
        "moods": ["Nostalgic", "Uncanny", "Eerie"],
        "aspect_ratio": "16:9",
        "description": "A surreal preset blending nostalgic dreaminess with unsettling strange objects or environments."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Internet Art", "post_processing": ["scan error effect", "smudging"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Ambient", "light_quality": "Foggy", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Uncanny juxtaposition", "focal_point": "Ambiguous objects"},
        "color_settings": {"color_scheme": "Pale Neon Desaturated", "palette_type": "pale neon desaturated palette", "color_temperature": "Cool", "color_contrast": "Low"},
        "detail_settings": {"detail_level": "Medium", "texture_quality": "Smudged"},
        "environment_settings": {"weather": "Foggy", "season": "N/A", "location_type": "Liminal Space", "atmospheric_effects": ["fog"]},
        "quality_settings": {"resolution": "1080p", "rendering_quality": "Low-fidelity aesthetic"},
        "negative_prompt": "clear, realistic, logical, signature, watermark, high quality",
        "style_negative_prompt": "sharp detail, vibrant colors"
    }
    imagen_settings["dreamcore_weirdcore_settings"] = {
        "atmosphere": "foggy uncanny low-saturation color in liminal spaces", "distortion": "scan error effect with slight smudging",
        "motif": "ambiguous objects surreal geometry portals",
        "aesthetic_blend": "Blends nostalgic dreaminess (dreamcore) with unsettling strange objects or environments (weirdcore); ambiguous and slightly eerie scenes."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_fantasy_battle_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Fantasy Battle Preset",
        "moods": ["Epic", "Intense", "Dramatic"],
        "aspect_ratio": "16:9",
        "description": "An intense preset for epic fantasy battle scenes with magical effects and dynamic composition."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Fantasy Art", "post_processing": ["magical effects"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Dramatic High Contrast", "light_quality": "Magical", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Dynamic low angle", "focal_point": "Combatants", "view_mode": "dynamic action-packed perspective", "motion_blur": "medium motion blur"},
        "color_settings": {"color_scheme": "Rich Saturated", "palette_type": "rich saturated reds blues golds contrasted with darks", "color_temperature": "Mixed", "color_contrast": "Very High"},
        "detail_settings": {"detail_level": "Very High", "texture_quality": "Realistic"},
        "environment_settings": {"weather": "Stormy with magical energy effects", "season": "N/A", "location_type": "Ancient Battlefield", "atmospheric_effects": ["smoke", "magic glow"]},
        "quality_settings": {"resolution": "4096x2160", "rendering_quality": "Ultra High Detail"},
        "negative_prompt": "calm, peaceful, low detail, signature, watermark, low quality",
        "style_negative_prompt": "static composition, bland colors"
    }
    imagen_settings["fantasy_settings"] = {
        "combat_type": "wizard vs armored knight", "environment": "ancient battlefield ruins",
        "action_elements": ["magical spells clashing", "sword impacts", "glowing enchanted weapons"],
        "atmosphere": "chaotic epic intense dramatic", "special_effects": ["magical explosions", "glowing runes", "particle effects"],
        "lighting": "dramatic chiaroscuro with magical light sources", "color_palette": "rich saturated reds blues golds contrasted with darks",
        "composition": "dynamic low angle with motion blur focusing on central combatants"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_fantasy_landscape_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Fantasy Landscape Preset",
        "moods": ["Epic", "Mysterious", "Vast"],
        "aspect_ratio": "16:9",
        "description": "A vast preset for epic fantasy landscapes with magical elements and dramatic lighting."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Fantasy Art", "post_processing": ["magical atmosphere"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Dramatic", "light_quality": "Ethereal", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Wide-angle panoramic", "focal_point": "Landmark"},
        "color_settings": {"color_scheme": "Rich Saturated", "palette_type": "rich saturated fantasy palette", "color_temperature": "Mixed", "color_contrast": "High"},
        "detail_settings": {"detail_level": "Very High", "texture_quality": "Realistic"},
        "environment_settings": {"weather": "Mysterious", "season": "N/A", "location_type": "Enchanted Realm", "atmospheric_effects": ["mist", "glowing particles"]},
        "quality_settings": {"resolution": "4096x2160", "rendering_quality": "Ultra High Detail"},
        "negative_prompt": "mundane, realistic, low detail, signature, watermark, low quality",
        "style_negative_prompt": "boring composition, flat lighting"
    }
    imagen_settings["fantasy_settings"] = {
        "landscape_type": "floating islands with waterfalls", "magical_elements": ["glowing flora", "ancient ruins", "mythical creatures in distance"],
        "atmosphere": "enchanted mysterious vast", "lighting": "ethereal light rays breaking through clouds",
        "color_palette": "deep greens blues purples with golden light"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_fantasy_cityscape_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Fantasy Cityscape Preset",
        "moods": ["Magical", "Ancient", "Grand"],
        "aspect_ratio": "16:9",
        "description": "A grand preset for fantasy cityscapes with magical architecture and ethereal lighting."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Fantasy Art", "post_processing": ["magical glow"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Ethereal", "light_quality": "Magical", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Wide-angle panoramic", "focal_point": "Architecture", "view_mode": "wide-angle panoramic view"},
        "color_settings": {"color_scheme": "Rich Magical", "palette_type": "rich purples blues golds", "color_temperature": "Cool", "color_contrast": "High"},
        "detail_settings": {"detail_level": "Very High", "texture_quality": "Detailed Architecture"},
        "environment_settings": {"weather": "Clear", "season": "N/A", "location_type": "Floating City", "atmospheric_effects": ["glowing mist"]},
        "quality_settings": {"resolution": "4096x2160", "rendering_quality": "Ultra High Detail"},
        "negative_prompt": "mundane, realistic, low detail, signature, watermark, low quality",
        "style_negative_prompt": "boring architecture, flat lighting"
    }
    imagen_settings["fantasy_settings"] = {
        "architecture_style": "gothic magical architecture", "environment": "floating city in clouds",
        "magical_elements": ["flying ships", "magical lights", "floating platforms"], "time_of_day": "twilight with glowing elements",
        "atmosphere": "mysterious enchanted ancient magical"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_cyberpunk_action_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Cyberpunk Action Preset",
        "moods": ["Intense", "Chaotic", "Futuristic"],
        "aspect_ratio": "16:9",
        "description": "An intense preset for cyberpunk action scenes with digital effects and dynamic motion."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Cyberpunk Art", "post_processing": ["digital glitch effects", "motion blur"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Harsh Neon", "light_quality": "High contrast", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Dynamic low angle", "focal_point": "Action", "view_mode": "dynamic action-packed low angle", "motion_blur": "high motion blur"},
        "color_settings": {"color_scheme": "Neon Contrasting", "palette_type": "neon blues purples cyans with metallic sheens", "color_temperature": "Cool", "color_contrast": "Very High"},
        "detail_settings": {"detail_level": "Very High", "texture_quality": "Metallic and wet surfaces"},
        "environment_settings": {"weather": "Rainy", "season": "N/A", "location_type": "Neon City Streets", "atmospheric_effects": ["rain", "neon reflections"]},
        "quality_settings": {"resolution": "4096x2160", "rendering_quality": "Ultra High Detail"},
        "negative_prompt": "calm, peaceful, low detail, signature, watermark, low quality",
        "style_negative_prompt": "static composition, bland colors"
    }
    imagen_settings["cyberpunk_settings"] = {
        "action_type": "combat chase scene", "environment": "neon city streets at night during rain",
        "special_effects": ["digital glitch effects", "holograms flickering", "cybernetic enhancements sparking"],
        "atmosphere": "intense chaotic futuristic dystopian", "motion_elements": ["fast movement blur", "digital trail effects"]
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_cyberpunk_technology_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Cyberpunk Technology Preset",
        "moods": ["High-Tech", "Complex", "Digital"],
        "aspect_ratio": "16:9",
        "description": "A detailed preset focusing on cyberpunk technology, interfaces, and digital elements."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Cyberpunk Art", "post_processing": ["digital interfaces", "glitch effects"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Digital Screen Glow", "light_quality": "Neon highlights", "light_direction": "Front"},
        "composition_settings": {"technique": "Technical close-up", "focal_point": "Interface", "view_mode": "technical close-up focused on interface"},
        "color_settings": {"color_scheme": "Neon Digital", "palette_type": "neon blues purples cyans with metallic sheens", "color_temperature": "Cool", "color_contrast": "High"},
        "detail_settings": {"detail_level": "Very High", "texture_quality": "Digital and metallic"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "High-Tech Laboratory", "atmospheric_effects": ["glowing data streams"]},
        "quality_settings": {"resolution": "4096x2160", "rendering_quality": "Ultra High Detail"},
        "negative_prompt": "organic, low detail, signature, watermark, low quality",
        "style_negative_prompt": "analog, simple"
    }
    imagen_settings["cyberpunk_settings"] = {
        "technology_type": "AI core interface with holographic displays", "environment": "dark high-tech laboratory",
        "special_effects": ["glowing data streams", "glitch effects on screens", "holographic projections"],
        "atmosphere": "futuristic advanced complex digital cold", "technical_elements": ["complex circuitry", "glowing data nodes", "digital interfaces"]
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_game_retro_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Game Retro Preset",
        "moods": ["Nostalgic", "Pixelated"],
        "aspect_ratio": "4:3",
        "description": "A retro preset for pixelated game art reminiscent of the 16-bit console era."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Pixel Art", "post_processing": ["pixelation", "CRT filter"], "style_era": "Retro"},
        "lighting_settings": {"lighting_type": "Flat", "light_quality": "Hard-edged", "light_direction": "Top"},
        "composition_settings": {"technique": "Side-scrolling view", "focal_point": "Character", "camera_angle": "side-scrolling platformer view", "view_mode": "chunky pixel sprites"},
        "color_settings": {"color_scheme": "Limited 16-bit", "palette_type": "limited 16-bit color palette (e.g., SNES)", "color_temperature": "Neutral", "color_contrast": "High"},
        "detail_settings": {"detail_level": "Low", "texture_quality": "pixelated 16-bit style"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Game Level", "atmospheric_effects": ["scanlines"]},
        "quality_settings": {"resolution": "320x240", "rendering_quality": "Pixelated"},
        "negative_prompt": "smooth, realistic, high detail, signature, watermark, high quality",
        "style_negative_prompt": "blended colors, non-pixelated"
    }
    imagen_settings["game_engine_settings"] = {
        "engine_type": "Pixel Art Engine (simulated)", "render_quality": "pixelated 16-bit style",
        "special_effects": ["sprite-based animation", "retro CRT filter"], "shader_type": "pixel art palette limited shader",
        "post_effects": ["scanlines", "pixelation"], "resolution": "low resolution (e.g., 320x240 scaled up)",
        "color_palette": "limited 16-bit color palette (e.g., SNES)"
    }
    imagen_settings["game_settings"] = {
        "retro_style": "platformer game", "color_depth": "16-bit", "animation_style": "pixel sprite animation"
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_game_cel_shaded_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Game Cel Shaded Preset",
        "moods": ["Stylized", "Vibrant"],
        "aspect_ratio": "16:9",
        "description": "A stylized preset for cel-shaded game art with bold outlines and vibrant colors."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Cel Shading", "post_processing": ["bold ink outlines"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Soft Stylized", "light_quality": "Toon shading highlights", "light_direction": "Multiple"},
        "composition_settings": {"technique": "Dynamic action camera", "focal_point": "Character", "camera_angle": "dynamic action camera angle", "view_mode": "third-person action game view"},
        "color_settings": {"color_scheme": "Vibrant Saturated", "palette_type": "vibrant saturated anime colors", "color_temperature": "Neutral", "color_contrast": "High"},
        "detail_settings": {"detail_level": "Medium", "texture_quality": "Smooth clean edges"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Game Level", "atmospheric_effects": ["stylized bloom"]},
        "quality_settings": {"resolution": "1080p", "rendering_quality": "Cel Shaded"},
        "negative_prompt": "realistic, blurry, high detail texture, signature, watermark, low quality",
        "style_negative_prompt": "photorealistic shading, no outlines"
    }
    imagen_settings["game_engine_settings"] = {
        "engine_type": "Cel-Shading Engine (simulated)", "render_quality": "smooth clean edges flat shading",
        "special_effects": ["bold ink outlines", "toon shading highlights"], "shader_type": "cel-shaded toon shader",
        "post_effects": ["ink outline effect", "stylized bloom"], "resolution": "1080p",
        "color_palette": "vibrant saturated anime colors"
    }
    imagen_settings["game_settings"] = {
        "animation_style": "smooth cell animation look", "lighting_type": "soft stylized lighting",
        "character_style": "anime inspired characters"
    }
    return {**base_template, "imagen_settings": imagen_settings}
