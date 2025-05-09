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
            "art_movement": "Kinetic Typography and ASCII Art Fusion",
            "post_processing": ["ascii pattern overlay", "simulated screen refresh"],
            "style_era": "Digital Retro-Futurism"
        },
        "lighting_settings": {
            "lighting_type": "CRT-glow",
            "light_quality": "Simulated phosphor bloom",
            "light_direction": "Screen emission"
        },
        "composition_settings": {
            "technique": "ASCII kinetic motion grid, text flow dynamics",
            "focal_point": "Animated Symbol Region or Key Text Element"
        },
        "color_settings": {
            "color_scheme": "Monochrome or Limited ANSI",
            "palette_type": "classic terminal monochrome (green, amber, white) or limited ANSI colors",
            "color_temperature": "Cool",
            "color_contrast": "High"
        },
        "detail_settings": {
            "detail_level": "ASCII Character Detail",
            "texture_quality": "CRT scanline, pixel grid"
        },
        "environment_settings": {
            "weather": "N/A",
            "season": "N/A",
            "location_type": "Digital Console Interface",
            "atmospheric_effects": ["phosphor flicker", "data stream visuals"]
        },
        "quality_settings": {
            "resolution": "Character-based (e.g. 80x40 characters) scaled for HD viewing",
            "rendering_quality": "Crisp Retro Digital"
        },
        "negative_prompt": "realism, full-color photography, smooth gradient, painted texture, signature, watermark, low quality, anti-aliasing",
        "style_negative_prompt": "natural photo, smooth curves, hand-drawn, high-resolution graphics"
    }
    imagen_settings["kinetic_ascii_settings"] = {
        "motion_type": "animated text-based, symbol cycling, scrolling text",
        "character_set": "Extended ASCII, Block Elements, Custom Symbols for motion",
        "visual_flow": "left-to-right, top-to-bottom, or procedural",
        "energy_motif": "pulsing symbols, flowing data, glitch transitions",
        "articulation": "frame-based animation, procedural text generation",
        "aesthetic_blend": "Dynamic kinetic typography using ASCII and extended characters, creating pulsing, animated text and symbols with a strong retro-tech or cyber terminal fusion."
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
            "art_movement": "Mixed Media Illustration",
            "post_processing": ["subtle paper grain enhancement", "watercolor bloom control", "delicate pencil rendering"],
            "style_era": "Contemporary"
        },
        "lighting_settings": {
            "lighting_type": "Soft Diffuse Natural Light",
            "light_quality": "Natural Window Light or equivalent",
            "light_direction": "Front or Front-Side"
        },
        "composition_settings": {
            "technique": "Wash-and-sketch layering, delicate balance between mediums",
            "focal_point": "Main Subject, often with softer background",
            "color_interaction": "Soft transparent watercolor washes interacting with precise grayscale or colored pencil marks"
        },
        "color_settings": {
            "color_scheme": "Muted Pastels, Soft Naturals, or Monochromatic with color accents",
            "palette_type": "Soft, muted, natural tones; can include selective vibrant pencil accents",
            "color_temperature": "Neutral to Warm",
            "color_contrast": "Low to Medium-Low"
        },
        "detail_settings": {
            "detail_level": "Medium, with areas of fine pencil detail",
            "texture_quality": "Visible watercolor paper grain (cold-press or rough), potential for light pigment granulation, distinct graphite or colored pencil sheen"
        },
        "environment_settings": {
            "weather": "N/A",
            "season": "N/A",
            "location_type": "Studio, Botanical Illustration, Character Sketch",
            "atmospheric_effects": ["paper grain highlights", "soft focus elements"]
        },
        "quality_settings": {
            "resolution": "2048x1536 or higher for print",
            "rendering_quality": "Painterly Soft, Delicate Detail"
        },
        "negative_prompt": "digital photo, sharp realism, cg, harsh digital look, signature, watermark, low quality, muddy colors, overworked",
        "style_negative_prompt": "no texture, computer rendering, harsh lines, comic ink, overly bold, purely digital appearance, clashing textures"
    }
    imagen_settings["watercolor_pencil_settings"] = {
        "layering_interaction": "Soft watercolor washes forming base tones and atmosphere, with precise pencil lines defining details, contours, and adding texture.",
        "stroke_characteristics": "Loose watercolor washes contrasted with fine, detailed pencil linework and shading (e.g., cross-hatching, stippling).",
        "medium_blend_focus": "Achieving a harmonious balance where neither medium entirely overpowers the other, showcasing qualities of both.",
        "paper_type_influence": "Textured cold-press or similar paper, with grain visible and interacting with both watercolor and pencil.",
        "watercolor_properties": "High transparency in washes, potential for subtle granulation and controlled bleeding or distinct watermarks.",
        "pencil_properties": "Precise linework for definition and detail, options for delicate shading or bold accents, visible graphite/pigment sheen.",
        "aesthetic_goal": "Dreamy, illustrative, often delicate and ethereal; suitable for botanical art, character studies, storybook visuals, and expressive sketches."
    }
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
            "art_movement": "Tradigital Art (Oil Base)",
            "post_processing": ["digital overlay", "contrast boost", "texture refinement", "color correction", "selective sharpening"],
            "style_era": "Contemporary"
        },
        "lighting_settings": {
            "lighting_type": "Blended Traditional & Digital Studio Lighting",
            "light_quality": "Enhanced Naturalism with Digital Accents (e.g., rim lights, specular highlights)",
            "light_direction": "Artist Defined, often mimicking classical lighting enhanced digitally"
        },
        "composition_settings": {
            "technique": "Mixed media layering, classical composition principles with digital flexibility",
            "focal_point": "Main Hybrid Subject with clear visual hierarchy"
        },
        "color_settings": {
            "color_scheme": "Natural Enhanced, Rich Saturation",
            "palette_type": "Rich oil colors with expanded digital gamut for vibrancy and depth",
            "color_temperature": "Balanced, or artistically chosen for mood",
            "color_contrast": "Medium-High, digitally enhanced for impact"
        },
        "detail_settings": {
            "detail_level": "High to Very High",
            "texture_quality": "Visible oil brushstrokes, canvas texture, enhanced with digital sharpness and refined depth"
        },
        "environment_settings": {
            "weather": "N/A",
            "season": "N/A",
            "location_type": "Studio, Digitally Enhanced Environment, or Photorealistic Composite",
            "atmospheric_effects": ["digital light scatter", "subtle digital bloom", "enhanced depth of field"]
        },
        "quality_settings": {
            "resolution": "3840x2160 or higher for print quality",
            "rendering_quality": "Photorealistic Hybrid Detail"
        },
        "negative_prompt": "purely digital look, lack of traditional texture, cartoonish, messy, signature, watermark, low quality, flat lighting, unconvincing material fusion",
        "style_negative_prompt": "unblended styles, harsh digital artifacts, obvious composite borders, loss of traditional media character, inconsistent lighting between layers"
    }
    imagen_settings["hybrid_traditional_digital_settings"] = {
        "media_fusion": "Traditional oil painting techniques and textures as a base, enhanced and refined with digital tools.",
        "traditional_elements_emphasis": "Preservation and enhancement of oil paint's characteristic impasto, glazing, brushwork, and canvas texture.",
        "digital_enhancements": ["Non-destructive digital layering", "digital brushwork for fine details or glazing", "advanced color grading and correction", "selective sharpening or blurring for focus control", "atmospheric effects (e.g., subtle glow, enhanced shadows, volumetric light)", "texture overlays for consistency or specific material effects"],
        "workflow_implication": "Physical painting potentially scanned or photographed at high resolution, then meticulously manipulated and perfected digitally.",
        "aesthetic_goal": "Achieve a look that honors traditional oil painting's richness and depth while leveraging digital precision for unmatched detail, vibrancy, and atmospheric effects.",
        "digital_tools_suite": "Graphics tablet (e.g., Wacom), professional painting software (e.g., Photoshop, Corel Painter, Krita), custom brushes mimicking traditional tools, adjustment layers, advanced masking techniques, and blending modes."
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
            "art_movement": "Contemporary Installation Art",
            "post_processing": ["projection mapping", "interactive element calibration", "spatial audio design"],
            "style_era": "Contemporary"
        },
        "lighting_settings": {
            "lighting_type": "Dynamic projection-based and integrated physical lighting",
            "light_quality": "Variable, often dramatic or atmospheric",
            "light_direction": "All directions, site-specific"
        },
        "composition_settings": {
            "view_mode": "Immersive 3D space perspective, viewer path consideration",
            "focal_point": "Central Spatial Object, Overall Environment, or Interactive Zone"
        },
        "color_settings": {
            "color_scheme": "Eclectic, Thematic, or Site-Responsive",
            "palette_type": "Site-specific, often involving projected light colors and material colors",
            "color_temperature": "Variable, mood-dependent",
            "color_contrast": "Variable, often high for projected elements"
        },
        "detail_settings": {
            "detail_level": "High in both physical and digital components",
            "texture_quality": "Tactile/Physical materials, Crisp Digital Projections"
        },
        "environment_settings": {
            "weather": "N/A (typically indoor or controlled environment)",
            "season": "N/A",
            "location_type": "Gallery, Public Space, Custom-built Exhibit Installation",
            "atmospheric_effects": ["room/floor reflections", "projected light spill", "soundscapes"]
        },
        "quality_settings": {
            "resolution": "Site-specific, often high-resolution for projections and detailed physical elements",
            "rendering_quality": "Immersive Spatial Detail, Seamless Integration"
        },
        "negative_prompt": "flat panel, small 2D, illustration, photo, low quality, purely digital screen-based, poorly integrated elements",
        "style_negative_prompt": "wall-hung only, generic sculpture, no digital/projection elements, disjointed experience, technical glitches visible"
    }
    imagen_settings["installation_art_settings"] = {
        "media_components": "Mixed media (physical objects, light, sound, video), spatial elements, custom structures.",
        "scale_and_space": "Large room-scale, site-specific design, consideration of viewer movement.",
        "interactivity_type": "Participatory digital interaction, sensor-based responses, audience-triggered events.",
        "spatial_arrangement_logic": "Site-specific modular design, narrative environments, experiential pathways.",
        "technology_integration_tools": "Projection mapping software, microcontrollers (e.g., Arduino, Raspberry Pi), sensors (motion, touch, sound), interactive displays, custom software (e.g., Max/MSP, TouchDesigner).",
        "aesthetic_blend": "Immersive and often site-specific experiences combining physical materials, space, light, sound, and interactive digital technologies to engage multiple senses and invite viewer participation."
    }
    # Redundant line removed: imagen_settings["lighting_settings"]["lighting_type"] = "dynamic projection-based lighting"
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
            "art_movement": "Data-Driven Art / Algorithmic Art / Generative Art",
            "post_processing": ["data-derived overlays", "generative patterns", "interactive visualization elements", "vector field visualizations"],
            "style_era": "Cutting-Edge Digital"
        },
        "lighting_settings": {
            "lighting_type": "Luminous Data-Driven Highlighting, Abstract Digital Light",
            "light_quality": "High contrast, often emissive or procedural",
            "light_direction": "Backlit, Internal, or Algorithmically Determined"
        },
        "composition_settings": {
            "technique": "Algorithmic composition, emergent patterns, rule-based systems",
            "focal_point": "Data Node, Emergent Structure, or Interactive Element"
        },
        "color_settings": {
            "color_scheme": "High contrast, Spectral, or Mapped from Data Values",
            "palette_type": "Data-inspired, often high-contrast, spectral, or procedurally generated",
            "color_temperature": "Cool, Neutral, or Variable based on data",
            "color_contrast": "High to Very High"
        },
        "detail_settings": {
            "detail_level": "High, often intricate and complex due to generative processes",
            "texture_quality": "Digital, Procedural, Abstract, or Data-Mapped Textures"
        },
        "environment_settings": {
            "weather": "N/A",
            "season": "N/A",
            "location_type": "Abstract Digital Space, Tech Lab, Science Exhibit, Virtual Environment",
            "atmospheric_effects": ["digital aura", "particle flows", "data trails", "network visualizations"]
        },
        "quality_settings": {
            "resolution": "4096x2160 or higher, scalable for large displays",
            "rendering_quality": "High Precision Digital, Real-time Interactive (if applicable)"
        },
        "negative_prompt": "organic, flat, bland, hand-drawn, purely traditional, signature, watermark, low quality, chaotic noise (unless intended)",
        "style_negative_prompt": "non-digital, traditional media only, no data representation, static imagery (if interactivity is key), random unformed noise"
    }
    imagen_settings["scientific_technological_hybrid_settings"] = {
        "media_and_tools": "Digital media, scientific visualization software (e.g., ParaView, VTK), generative art frameworks (e.g., Processing, p5.js, TouchDesigner), programming languages (e.g., Python with data science libraries).",
        "conceptual_basis": "Data-driven algorithmic generation, sonification, simulation visualization, AI-assisted creation.",
        "technology_involved": "AI (e.g., GANs, VAEs for generation; ML for pattern recognition), custom algorithms, real-time data feeds, APIs for data sourcing.",
        "data_visualization_techniques": "3D models derived from data, network graphs, particle systems, heatmaps, flow fields, abstract geometric representations.",
        "interactivity_options": "Interactive data exploration, user-input influencing generation, real-time updates based on external data.",
        "aesthetic_blend": "Artistic expression that translates complex scientific data, mathematical formulas, or technological processes into compelling visual and interactive forms, often revealing hidden patterns and beauty within the data."
    }
    # Redundant line removed: imagen_settings["composition_settings"]["technique"] = "algorithmic composition"
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
            "art_movement": "Augmented Reality (AR) Art / Mixed Reality (MR)",
            "post_processing": ["Real-time 3D object overlay", "Occlusion handling", "Light estimation matching", "Shader effects for virtual objects"],
            "style_era": "Contemporary / Emerging Tech"
        },
        "lighting_settings": {
            "lighting_type": "Dynamic Environmental Lighting Matched by AR System",
            "light_quality": "Seamless Blend of Real-world and Virtual Lighting on AR elements",
            "light_direction": "Matched to physical environment, real-time adjustments"
        },
        "composition_settings": {
            "view_mode": "Interactive Mixed Reality View (e.g., through mobile device screen or AR headset)",
            "focal_point": "Main AR Subject or Interactive Element, considering user's perspective"
        },
        "color_settings": {
            "color_scheme": "Physically Adaptive or Thematically Contrasting/Harmonizing",
            "palette_type": "Flexible, adapting to real-world environment or artist-defined for virtual objects",
            "color_temperature": "Adaptive to real-world lighting or intentionally stylized",
            "color_contrast": "Variable, ensuring visibility and integration of AR elements"
        },
        "detail_settings": {
            "detail_level": "High for virtual assets, dependent on device capabilities",
            "texture_quality": "Crisp 3D textures for AR objects, PBR materials for realism if desired"
        },
        "environment_settings": {
            "weather": "Adaptive to real-world conditions",
            "season": "Adaptive to real-world conditions",
            "location_type": "Physical space augmented by digital overlays (e.g., room, outdoor park, cityscape)",
            "atmospheric_effects": ["Dynamic shadows from virtual objects", "motion transparency for AR elements", "virtual particle effects interacting with real space"]
        },
        "quality_settings": {
            "resolution": "Device Native (e.g., phone screen resolution, AR headset display resolution)",
            "rendering_quality": "Mixed Reality Polished, Real-time performance optimized"
        },
        "negative_prompt": "static flat art, 2D only, non-overlaid, poor tracking, signature, watermark, low quality, unrealistic integration, laggy performance",
        "style_negative_prompt": "hard-edged transition, non-adaptive lighting, virtual objects not grounded in reality, poor occlusion, obvious digital artifacts"
    }
    imagen_settings["augmented_reality_art_settings"] = {
        "media_components": "Interactive 3D models, animations, visual effects, and soundscapes overlayed onto the user's physical space.",
        "interaction_methods": "User-driven immersive experience via touch, gesture, voice commands, or physical movement.",
        "core_technology": "AR SDKs (e.g., ARKit, ARCore, Vuforia), 3D game engines (e.g., Unity, Unreal Engine), AR-capable mobile devices or dedicated AR/MR headsets.",
        "tracking_and_mapping": "Markerless (e.g., SLAM, plane detection, image recognition) or marker-based tracking; GPS for location-based AR; real-time environment mapping.",
        "user_interface_design": "Intuitive gesture control, minimalist UI elements, contextual information display.",
        "aesthetic_blend": "Seamlessly blending interactive virtual 3D models, animations, and effects with the user's physical environment, creating an enhanced, altered, or entirely new perception of reality."
    }
    # Redundant line removed: imagen_settings["lighting_settings"]["lighting_type"] = "dynamic real-time lighting matching environment"
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
            "art_movement": "Abstract Expressionism / Cubism Fusion",
            "post_processing": ["Dynamic gestural overlays", "geometric fragmentation effects", "textured layering", "simulated impasto"],
            "style_era": "Modernist Fusion / Contemporary Abstract"
        },
        "lighting_settings": {
            "lighting_type": "Abstracted, Multi-faceted Lighting, often non-naturalistic",
            "light_quality": "Often harsh or contrasting to define forms and create dynamism",
            "light_direction": "Multiple, conflicting, or implied by form and color"
        },
        "composition_settings": {
            "technique": "Expressive abstraction with geometric fragmentation, dynamic interplay of forms and space",
            "focal_point": "Dynamic Confluence of energy, or shifting focal points"
        },
        "color_settings": {
            "color_scheme": "Bold Contrasts, Monochromatic with Accents, or Emotionally Driven Palettes",
            "palette_type": "Bold, emotive, often contrasting; can range from monochromatic (analytical cubism influence) to vibrant (expressionist influence)",
            "color_temperature": "Mixed, often clashing for dynamic effect",
            "color_contrast": "High to Very High"
        },
        "detail_settings": {
            "detail_level": "High in terms of textural complexity and formal interplay",
            "texture_quality": "Visible energetic brushstrokes, simulated impasto, hard-edged geometric planes, collaged elements (simulated)"
        },
        "environment_settings": {
            "weather": "N/A",
            "season": "N/A",
            "location_type": "Abstract, Internal Emotional Landscape, Deconstructed Space",
            "atmospheric_effects": ["energetic form fields", "visual representation of movement and force"]
        },
        "quality_settings": {
            "resolution": "3840x2160 or suitable for large format display",
            "rendering_quality": "Polished Modern, emphasizing textural and formal richness"
        },
        "negative_prompt": "photorealistic, staged, calm, serene, low intensity, flat, overly blended, signature, watermark, low quality, purely decorative",
        "style_negative_prompt": "orderly without tension, soft contrast, overly harmonious, realism, single perspective, lack of energy"
    }
    imagen_settings["abstract_expressionism_cubism_fusion_settings"] = {
        "form_style": "Spontaneous gestural brushwork and mark-making (Expressionism) combined with deconstructed, multi-perspective geometric forms and overlapping planes (Cubism).",
        "color_palette_dynamics": "Utilizes bold, contrasting, and emotive colors characteristic of Expressionism, potentially structured or limited by Cubist sensibilities (e.g., earthy analytical tones or brighter synthetic cubism colors).",
        "compositional_tension": "Layered, dynamic abstract forms creating a sense of depth and movement; interplay between spontaneous marks and structured geometric elements.",
        "emotional_intensity_focus": "High raw spontaneous energy from Expressionism, channeled or fractured through Cubist deconstruction.",
        "spatial_representation": "Multiple perspectives, fractured planes, and a flattened or ambiguous sense of space, challenging traditional representation.",
        "aesthetic_blend": "A dynamic fusion capturing the raw, spontaneous energy and emotional intensity of Abstract Expressionism with the analytical, multi-perspective deconstruction and formal innovation of Cubism."
    }
    # Redundant line removed: imagen_settings["composition_settings"]["technique"] = "expressive abstraction with geometric fragmentation"
    return {**base_template, "imagen_settings": imagen_settings}

def get_collage_digital_overlay_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Collage Digital Overlay Preset",
        "moods": ["Eclectic"],
        "aspect_ratio": "16:9",
        "description": "A vibrant preset for collage-based art with integrated digital overlays and tactile paper textures."
    }
    imagen_settings = {
        "style_settings": {
            "art_movement": "Mixed Media Collage / Digital Hybrid",
            "post_processing": ["seamless digital integration", "texture blending", "depth effects (e.g., subtle drop shadows)", "color grading"],
            "style_era": "Contemporary"
        },
        "lighting_settings": {
            "lighting_type": "Studio Lighting for Physical Elements, Digitally Enhanced",
            "light_quality": "Soft Directional to highlight textures, with digital light effects (e.g., glows, overlays)",
            "light_direction": "Varied, to suit collage layers and digital additions, often slightly from above or side"
        },
        "composition_settings": {
            "technique": "Layered physical collage elements with integrated digital overlays and manipulations, juxtaposition of forms and textures",
            "focal_point": "Key Juxtaposed Elements or Overall Compositional Harmony"
        },
        "color_settings": {
            "color_scheme": "Eclectic and Harmonized, or Intentionally Contrasting",
            "palette_type": "Varied based on collage materials, unified or contrasted by digital color grading and overlays",
            "color_temperature": "Mixed or Artist Defined to evoke mood",
            "color_contrast": "Medium to High, depending on desired impact and material interplay"
        },
        "detail_settings": {
            "detail_level": "High, showcasing both physical material textures (paper, fabric, print) and digital precision",
            "texture_quality": "Tangible paper/fabric/object textures, combined with digital textures, brushstrokes, or illustrative effects"
        },
        "environment_settings": {
            "weather": "N/A",
            "season": "N/A",
            "location_type": "Abstract, Thematic Background, or simulated surface",
            "atmospheric_effects": ["subtle digital glow", "texture overlays", "simulated depth of field for layers"]
        },
        "quality_settings": {
            "resolution": "3000x3000 or higher for detailed print work",
            "rendering_quality": "High Detail Hybrid, emphasizing textural richness"
        },
        "negative_prompt": "flat, purely digital, untextured, poorly integrated elements, signature, watermark, low quality, clashing styles (unintentionally), blurry, pixelated",
        "style_negative_prompt": "obvious digital seams, lack of physical texture, generic digital look, elements don't interact believably, muddy colors, poor layering"
    }
    imagen_settings["collage_digital_overlay_settings"] = {
        "physical_media_base": "Paper cutouts (magazines, photos, handmade paper), photographs, fabric scraps, found objects, ephemera, drawings, paintings.",
        "digital_overlay_techniques": "Digital painting, illustrative linework, graphic elements, vector shapes, texture overlays (digital grunge, noise), photo manipulation (blending modes, adjustments), glitch effects, typographic elements.",
        "integration_style": "Seamless blending for a cohesive look, stark juxtaposition for conceptual contrast, or interactive layering where digital elements respond to or alter physical ones.",
        "texture_play": "Emphasis on the contrast and harmony between physical material textures (e.g., torn paper edges, fabric weave, wood grain) and digital textures (e.g., clean vector lines, pixelation, procedural noise) or smoothness.",
        "narrative_or_theme": "Often thematic, narrative, conceptual, or purely aesthetic, using juxtaposition of disparate elements to create new meanings or visual interest.",
        "aesthetic_blend": "A rich visual tapestry combining the tactile, often irregular nature of physical collage with the precision, flexibility, and transformative effects of digital art, resulting in a unique layered reality."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_claymation_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Claymation Preset",
        "moods": ["Whimsical"],
        "aspect_ratio": "4:3",
        "description": "A whimsical preset for claymation style, focusing on tactile textures and playful character designs."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Claymation / Stop-Motion Animation", "post_processing": ["subtle motion blur (stop-motion style)", "depth of field (miniature look)", "visible fingerprints/tool marks", "slight boiling/texture flicker"], "style_era": "Classic to Contemporary"},
        "lighting_settings": {"lighting_type": "Miniature Set Studio Lighting (e.g., small spotlights, softboxes, practical lights)", "light_quality": "Soft warm directional, can be dramatic for mood", "light_direction": "Front, Side, or Three-point setup"},
        "composition_settings": {"technique": "Stop-motion framing, rule of thirds for character placement", "focal_point": "Character expressions and actions"},
        "color_settings": {"color_scheme": "Vibrant Saturated or Thematic Palette", "palette_type": "Vibrant saturated primary and secondary colors, or specific mood-driven palettes", "color_temperature": "Warm or Neutral, depending on scene", "color_contrast": "Medium to High"},
        "detail_settings": {"detail_level": "Medium, with emphasis on tactile qualities", "texture_quality": "Tactile clay-like matte or slightly glossy surface, slight imperfections, fabric textures for clothing"},
        "environment_settings": {"weather": "N/A (unless part of miniature set)", "season": "N/A (unless part of miniature set)", "location_type": "Miniature handcrafted whimsical or detailed set", "atmospheric_effects": ["none, or practical effects like cotton smoke"]},
        "quality_settings": {"resolution": "1920x1080 (1080p) or 2048x1536 (4:3 HD), upscaled if needed", "rendering_quality": "Handcrafted Look, Charming Imperfection"},
        "negative_prompt": "smooth cg, photorealistic, sharp digital edges, perfect symmetry, signature, watermark, low quality, overly polished, motion vector blur",
        "style_negative_prompt": "digital rendering, no texture, realistic human proportions (unless stylized that way), CGI look, fluid animation (non-stop-motion)"
    }
    imagen_settings["claymation_settings"] = {
        "clay_type_simulation": "Plasticine or modeling clay appearance, possibly polymer clay for more rigid elements.",
        "surface_details": "Tactile hand-molded surface with visible fingerprints, tool marks, slight smudges, and characteristic clay texture.",
        "character_design_style": "Often exaggerated features, simple forms, expressive, and unique designs tailored for clay medium.",
        "animation_style_emulation": "Stop-motion frame-by-frame appearance, slight 'boiling' or jitter in static parts, characteristic poses and movement.",
        "set_and_prop_design": "Miniature handcrafted whimsical or detailed sets, often with a slightly 'rough' or handmade quality, using various craft materials.",
        "lighting_approach": "Soft warm directional studio lighting, mimicking physical miniature set illumination.",
        "color_palette_choice": "Vibrant saturated playful colors, or specific thematic palettes that enhance the handcrafted feel.",
        "aesthetic_blend": "Whimsical, charmingly imperfect handcrafted look with visible textures (fingerprints, tool marks), and playful, often exaggerated character designs, emulating traditional stop-motion clay animation."
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
        "style_settings": {"art_movement": "Experimental Mixed Media / Avant-Garde Digital Fusion", "post_processing": ["Abstract digital manipulation", "glitch effects (optional)", "procedural texturing", "algorithmic alteration", "data bending"], "style_era": "Contemporary Avant-Garde"},
        "lighting_settings": {"lighting_type": "Varied, Unconventional, often abstract or digitally generated", "light_quality": "Unpredictable, can be harsh, soft, or purely conceptual", "light_direction": "Multiple, non-naturalistic, or algorithmically determined"},
        "composition_settings": {"technique": "Non-traditional layering, deconstruction, juxtaposition of disparate elements, rule-based or chaotic assembly", "focal_point": "Abstract, Process-oriented, or Conceptual Core"},
        "color_settings": {"color_scheme": "Varied, often Dissonant or Symbolic", "palette_type": "Varied, unpredictable, often dissonant, symbolic, or algorithmically generated palette", "color_temperature": "Mixed, often clashing or extreme", "color_contrast": "High or Low, used expressively"},
        "detail_settings": {"detail_level": "Variable, from raw to hyper-detailed in sections", "texture_quality": "Varied unconventional physical textures (e.g., found objects, resin, metal, organic matter) combined with digital textures, noise, or artifacts"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Abstract, Conceptual Space, Digital Realm, or Simulated Environment", "atmospheric_effects": ["unpredictable digital artifacts", "warped perspectives", "simulated material decay or transformation", "glitches"]},
        "quality_settings": {"resolution": "3840x2160 or adaptable to installation/screen needs", "rendering_quality": "High, emphasizing experimental nature"},
        "negative_prompt": "conventional, realistic, boring, traditional, predictable, harmonious, signature, watermark, low quality, purely representational",
        "style_negative_prompt": "traditional media only without digital intervention, predictable composition, lack of innovation, purely decorative without concept"
    }
    imagen_settings["experimental_mixed_media_settings"] = {
        "physical_materials": "Unconventional items: plastics, e-waste, organic matter, textiles, found objects, industrial materials, liquids, powders.",
        "digital_processes": "3D scanning of physical forms, algorithmic processing, generative adversarial networks (GANs), data bending, custom software, AR/VR integration, interactive elements.",
        "core_techniques": "Physical layering and assembly, digital deconstruction and reassembly, glitching physical or digital data, procedural generation based on physical inputs, sonification of visual data or vice-versa.",
        "conceptual_focus": "Avant-garde, boundary-pushing exploration of materials, processes, and concepts; often challenging perception, societal norms, or the nature of art itself.",
        "aesthetic_blend": "Innovative, often surprising or unsettling, combinations of physical materials and digital techniques that challenge traditional art forms, explore new aesthetic possibilities, question the digital-physical divide, and provoke thought or visceral reactions."
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
        "style_settings": {"art_movement": "Textile Art / Mixed Media Collage (Patchwork Focus)", "post_processing": ["Visible stitched seams (simulated or actual)", "fabric texture enhancement", "subtle shadowing for depth between layers", "appliqué details"], "style_era": "Contemporary Craft / Folk Art Revival"},
        "lighting_settings": {"lighting_type": "Soft, slightly directional lighting (simulating gallery or craft studio illumination)", "light_quality": "Diffuse, accentuating textures and layers", "light_direction": "Top-Side or slightly angled front"},
        "composition_settings": {"technique": "Patchwork assembly, appliqué, layering of materials, often with repeating motifs or narrative scenes", "focal_point": "Central Pattern, Figurative Element, or Textural Interplay"},
        "color_settings": {"color_scheme": "Bold Contrasting, Harmonious Earthy, or Thematic Folk Palettes", "palette_type": "Bold contrasting or harmonious folk-inspired colors, often with an emphasis on material's original color and pattern", "color_temperature": "Warm, Neutral, or Cool depending on theme", "color_contrast": "Medium to High"},
        "detail_settings": {"detail_level": "High, focusing on material details and construction", "texture_quality": "Tactile, rough, and varied textures (fabric weaves like cotton, linen, felt; paper grain; button/bead surfaces), with visible stitching and appliqué edges"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Studio Setting, Wall Hanging Display, or Abstract Textured Background", "atmospheric_effects": ["none, or subtle depth cues"]},
        "quality_settings": {"resolution": "2048x2048 or higher for print/display", "rendering_quality": "Rich Textile Detail, Handcrafted Appearance"},
        "negative_prompt": "smooth, purely digital, photorealistic rendering, glossy, metallic, signature, watermark, low quality, blurry textures, flat colors",
        "style_negative_prompt": "flat colors without texture, uniform pattern without variation, lack of handcrafted feel, overly perfect or symmetrical (unless intentional geometric design)"
    }
    imagen_settings["patchwork_collage_settings"] = {
        "material_simulation": "Fabric scraps (cotton, felt, silk, burlap, denim), textured paper, buttons, beads, yarn, embroidery floss, small found objects like charms or keys.",
        "assembly_techniques": "Layered and stitched appearance (running stitch, blanket stitch, zigzag), appliqué techniques, quilting elements (optional), raw edges or neatly turned edges.",
        "texture_emphasis_details": "Highlighting tactile qualities: rough weaves, soft felts, smooth silks, matte papers, shiny beads/buttons. Visible thread details.",
        "color_and_pattern_logic": "Bold contrasting folk-inspired colors, harmonious analogous schemes, or thematic palettes. Use of patterned fabrics and papers.",
        "pattern_and_motif_types": "Varied patch sizes and shapes, geometric patterns, figurative elements (animals, people, houses), floral motifs, abstract designs.",
        "aesthetic_blend": "A tactile and visually rich composition emphasizing the textures, patterns, and colors of combined materials, often with a handcrafted, folk art, or narrative quality. Celebrates imperfection and the handmade."
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
        "style_settings": {"art_movement": "Paper Quilling / Paper Filigree Art", "post_processing": ["Subtle drop shadows for depth", "highlighting paper edges", "crisp focus on coils"], "style_era": "Contemporary Craft"},
        "lighting_settings": {"lighting_type": "Soft Directional Studio Light", "light_quality": "Highlights layers and coil dimensionality", "light_direction": "Side or slightly above to cast subtle shadows"},
        "composition_settings": {"technique": "Intricate pattern assembly with rolled, shaped, and glued paper strips, creating dimensional relief", "focal_point": "Intricate Details, Overall Pattern, or Central Motif"},
        "color_settings": {"color_scheme": "Bright Contrasting, Monochromatic, or Analogous", "palette_type": "Bright, soft pastels, jewel tones, or monochromatic with colored paper edges", "color_temperature": "Neutral or as per design", "color_contrast": "Medium to High, emphasizing shapes"},
        "detail_settings": {"detail_level": "Very High, focusing on precision of coils and placement", "texture_quality": "Crisp paper edge texture, smooth surface of rolled strips, subtle paper grain"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Studio Setting, Shadow Box Frame, or Clean Background", "atmospheric_effects": ["none, focus on the artwork itself"]},
        "quality_settings": {"resolution": "3000x3000 or higher for intricate detail", "rendering_quality": "Intricate Detail, Sharp Focus"},
        "negative_prompt": "flat, 2d, painting, drawing, blurry, smudged, signature, watermark, low quality, messy coils, uneven strips",
        "style_negative_prompt": "no depth, blurry details, unrealistic paper texture, poorly formed coils, haphazard arrangement"
    }
    imagen_settings["paper_quilling_settings"] = {
        "coil_and_shape_types": "Tight coils, loose coils, teardrops, marquises, hearts, S-scrolls, C-scrolls, fringed flowers, husking.",
        "paper_strip_characteristics": "Narrow paper strips (e.g., 1/8 inch, 3mm; 1/4 inch, 6mm), consistent width, varied colors.",
        "pattern_density_and_style": "Dense intricate patterns, delicate openwork, figurative designs, abstract motifs, mandalas, lettering.",
        "dimensionality_focus": "Emphasis on the 3D relief created by the height, angle, and arrangement of quilled elements against a background.",
        "construction_details": "Precision in rolling, shaping, and gluing; clean edges; harmonious color combinations.",
        "aesthetic_blend": "Delicate and intricate three-dimensional designs created by rolling, shaping, and gluing strips of paper, often forming floral motifs, abstract patterns, lettering, or miniature scenes, showcasing patience and precision."
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
        "style_settings": {"art_movement": "Tradigital Art (Acrylic Base)", "post_processing": ["Digital glazing", "texture blending", "color correction", "selective lighting adjustments", "sharpening details"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Mixed Studio or Enhanced Natural Light", "light_quality": "Blended, enhancing acrylic's natural appearance with digital precision and highlights", "light_direction": "Artist-defined, often to accentuate texture and form"},
        "composition_settings": {"technique": "Traditional acrylic painting composition (e.g., layering, impasto) digitally refined for impact, clarity, and depth", "focal_point": "Main Subject, enhanced by digital focus techniques"},
        "color_settings": {"color_scheme": "Natural Enhanced, Vibrant, or Thematic", "palette_type": "Acrylic paint palette (known for vibrancy and opacity) expanded and enhanced with digital color tools for wider gamut and subtle shifts", "color_temperature": "Balanced or artistically chosen", "color_contrast": "Medium to High, often boosted digitally"},
        "detail_settings": {"detail_level": "High to Very High", "texture_quality": "Visible acrylic brush strokes, canvas/board texture, and paint body, seamlessly integrated with digital details, sharpness, and effects"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Studio, Digitally Composited Background, or Abstract Setting", "atmospheric_effects": ["Subtle digital glow", "atmospheric perspective enhancement", "particle effects if applicable"]},
        "quality_settings": {"resolution": "3840x2160 or higher", "rendering_quality": "High-Fidelity Hybrid Detail"},
        "negative_prompt": "purely digital look, lack of traditional texture, cartoonish, flat, muddy colors, signature, watermark, low quality, unconvincing material blend",
        "style_negative_prompt": "unblended styles, harsh digital artifacts, obvious composite borders, loss of acrylic paint character, inconsistent lighting, pixelation"
    }
    imagen_settings["tradigital_mixed_media_settings"] = {
        "media_fusion_process": "Traditional acrylic painting techniques (layering, impasto, washes, dry brushing) as a foundational layer, subsequently scanned or photographed and enhanced using digital painting software.",
        "acrylic_characteristics_preserved": "Emphasis on acrylic paint's vibrancy, quick-drying nature (allowing for distinct layers), textural possibilities (from smooth to impasto), and versatility on various surfaces.",
        "digital_enhancement_techniques": "Digital glazing for depth and color richness, texture blending for seamless integration, precise color correction and grading, selective lighting adjustments (dodging/burning), sharpening of key details, adding subtle digital effects (e.g., glows, particles).",
        "texture_interaction": "Preservation and enhancement of visible brush strokes and canvas/board textures, with digital overlays or refinements that complement rather than obscure the physical paint qualities.",
        "color_palette_synergy": "Natural acrylic paint colors are enriched and expanded through digital tools, allowing for a wider gamut, more nuanced gradients, and precise color harmonies.",
        "digital_tools_employed": "Graphics tablet, professional digital painting software (e.g., Photoshop, Krita, Corel Painter), custom brushes designed to mimic or complement acrylics, adjustment layers, masking, and blending modes.",
        "aesthetic_blend": "A seamless and sophisticated integration that leverages the tactile qualities, vibrancy, and layering capabilities of acrylics with the precision, flexibility, and transformative power of digital tools, resulting in richly textured, visually dynamic, and highly detailed artwork."
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
        "style_settings": {"art_movement": "Whimsical Mixed Media / Fantasy Craft", "post_processing": ["Layered textures (e.g., paper, fabric, paint)", "subtle glitter/sparkle effects", "soft focus elements", "hand-drawn accents"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Soft Ambient or Gentle Directional", "light_quality": "Soft, ethereal, or magical glow", "light_direction": "Front or slightly angled to highlight layers"},
        "composition_settings": {"technique": "Layered composition, often with a central charming figure or scene", "focal_point": "Playful characters, mythical creatures, or enchanting scenes"},
        "color_settings": {"color_scheme": "Pastel Dreamy, Soft Analogous, or Split-Complementary with Iridescent Accents", "palette_type": "Pastel dreamy colors, iridescent accents, soft gradients, muted brights", "color_temperature": "Cool to Neutral, or Warm for cozy scenes", "color_contrast": "Low to Medium-Low"},
        "detail_settings": {"detail_level": "Medium to High, with attention to handcrafted details", "texture_quality": "Light, airy, layered textures (e.g., translucent paper, delicate fabrics, soft paint strokes, felt), with optional glitter, beads, or metallic accents"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Storybook Setting, Enchanted Forest, Dreamscape, Craft Tabletop", "atmospheric_effects": ["soft glows", "sparkles", "magical dust motes"]},
        "quality_settings": {"resolution": "2048x2048 or higher for detailed textures", "rendering_quality": "Painterly Soft, Tactile Charm"},
        "negative_prompt": "harsh, realistic, dark, gritty, overly complex, signature, watermark, low quality, purely digital, sharp edges (unless stylistic choice)",
        "style_negative_prompt": "serious mood, high contrast (unless intentional accent), flat textures, lack of charm, overly polished or sterile"
    }
    imagen_settings["whimsical_mixed_media_settings"] = {
        "core_motifs": ["Mythical creatures (fairies, unicorns, friendly monsters, dragons)", "soft pastel and iridescent colors", "playful and charming elements (stars, hearts, swirls, bubbles)", "nature motifs (flowers, mushrooms, enchanted trees, animals)."],
        "material_palette": "Combination of light and airy textures: layered paper (handmade, patterned, translucent), delicate fabrics (tulle, lace, felt), watercolor washes, gouache, colored pencil, ink, with possible additions of glitter, beads, sequins, buttons, or small found objects.",
        "technique_emphasis": "Focus on layering, collage, appliqué, simple hand-stitching (simulated), and hand-drawn or painted details to create a sense of depth and handcrafted appeal.",
        "overall_feeling": "Evokes a sense of lightheartedness, dreaminess, enchantment, and childlike wonder.",
        "aesthetic_blend": "Lighthearted, dreamy, and enchanting compositions that combine various physical and simulated physical media to create a sense of wonder, often featuring fantasy elements, charming characters, and playful narrative accents. Celebrates the joy of creation and imagination."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_sci_fi_futuristic_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Sci-Fi Futuristic Preset",
        "moods": ["High-Tech", "Futuristic", "Cyberpunk", "Expansive"],
        "aspect_ratio": "16:9",
        "description": "A vivid preset for futuristic sci-fi scenes, emphasizing advanced technology, cybernetics, and sprawling cityscapes or space environments."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Sci-Fi Concept Art / Cyberpunk Aesthetic", "post_processing": ["Holographic effects", "lens flares", "digital interface overlays", "chromatic aberration", "atmospheric haze"], "style_era": "Near to Far Future"},
        "lighting_settings": {"lighting_type": "Neon, Holographic, and Artificial Environmental Lighting", "light_quality": "High contrast, emissive glows, volumetric shafts", "light_direction": "Multiple, often from screens, signs, or technological sources"},
        "composition_settings": {"technique": "Dynamic, cinematic composition showcasing scale or action, rule of thirds, leading lines", "focal_point": "Advanced Technology, Cybernetic Character, Futuristic Vehicle/Architecture, or Expansive Vista"},
        "color_settings": {"color_scheme": "Cool Metallic Tones with Vibrant Neon Accents", "palette_type": "Metallic sheens (blues, silvers, gunmetal), neon glows (blues, purples, pinks, cyans, oranges), dark contrasting backgrounds", "color_temperature": "Predominantly Cool with Warm Accents", "color_contrast": "High to Very High"},
        "detail_settings": {"detail_level": "Very High, intricate mechanical and digital details", "texture_quality": "Polished metals, carbon fiber, glass, glowing circuits, worn urban textures"},
        "environment_settings": {"weather": "Rainy, Smoggy, or Clear Space Views", "season": "N/A", "location_type": "Futuristic Megacity (Neo-Tokyo, Blade Runner-esque), Space Station Interior, Alien Planet Surface, Cybernetic Underworld, Spaceship Bridge", "atmospheric_effects": ["Rain-slicked streets with reflections", "smog/haze", "digital noise/artifacts", "energy fields", "anamorphic lens flares", "floating data particles"]},
        "quality_settings": {"resolution": "4096x2160 (4K) or higher", "rendering_quality": "Cinematic, Photorealistic with Stylized Elements"},
        "negative_prompt": "organic (unless alien/bio-tech), mundane, contemporary, low-tech, fantasy elements, signature, watermark, low quality, blurry, poorly rendered",
        "style_negative_prompt": "traditional art style, lack of technological detail, overly bright or sunny (unless specific alien environment), simple designs, inconsistent tech levels"
    }
    imagen_settings["sci_fi_futuristic_settings"] = {
        "core_technology_themes": "Highly advanced cybernetics, artificial intelligence, robotics, energy weapons, FTL spacecraft, virtual reality interfaces, bio-engineering, massive data networks.",
        "environment_archetypes": "Sprawling futuristic megacities with towering skyscrapers and flying vehicles, gritty cyberpunk back alleys and markets, sleek and sterile space station interiors, desolate alien landscapes with advanced outposts, vast spaceship bridges.",
        "lighting_and_atmosphere_details": "Dominated by neon signs, holographic projections, emissive surfaces on tech, and dynamic artificial lights creating strong contrasts, reflections, and volumetric effects. Often includes rain, fog, or atmospheric particles.",
        "color_palette_emphasis": "Cool metallic blues, silvers, and greys contrasted with vibrant neon pinks, purples, cyans, oranges, and yellows; often set against dark, atmospheric backgrounds to make lights pop.",
        "key_visual_elements": "Interactive holograms, anamorphic lens flares, glitching digital interfaces, energy weapon effects, cybernetic augmentation glows, intricate greebling on tech surfaces, data streams.",
        "aesthetic_blend": "A blend of sleek, highly advanced futuristic design and/or gritty, dystopian cyberpunk elements, showcasing advanced technology, complex machinery, and immersive, often awe-inspiring or oppressive, environments."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_mediterranean_style_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Mediterranean Digital Painting Preset",
        "moods": ["Lively", "Warm", "Sunny", "Picturesque"],
        "aspect_ratio": "16:9",
        "description": "A vibrant preset capturing the essence of Mediterranean style through digital painting, focusing on sun-drenched coastal scenes, rustic architecture, and warm, inviting colors."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Mediterranean Digital Painting / Scenic Illustration", "post_processing": ["Warm color grading", "sun bloom effects", "texture enhancement for stucco/stone", "sharpening for clarity"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Bright, Clear Natural Sunlight (simulated or enhanced)", "light_quality": "Warm golden hour glow or bright midday sun with defined shadows", "light_direction": "Top, Side, or slightly angled to create depth"},
        "composition_settings": {"technique": "Rule of Thirds, leading lines, picturesque framing", "focal_point": "Coastal Landscape, Rustic Architecture, or Vibrant Flora"},
        "color_settings": {"color_scheme": "Warm Bright Analogous with Complementary Accents", "palette_type": "Warm bright Mediterranean palette: azure/cerulean blues, terracotta, ochre, olive greens, brilliant whites, bougainvillea pinks/purples", "color_temperature": "Warm", "color_contrast": "Medium to High"},
        "detail_settings": {"detail_level": "Medium to High, with painterly or realistic details", "texture_quality": "Realistic or painterly textures for stone, stucco, wood, water, and foliage; digitally enhanced for clarity and vibrancy"},
        "environment_settings": {"weather": "Clear, Sunny", "season": "Summer, late Spring", "location_type": "Coastal Village (Greek Isles, Italian Riviera), Olive Groves, Vineyards, Ancient Ruins by the sea", "atmospheric_effects": ["Subtle heat haze", "sparkling water reflections", "clear air perspective", "light bloom"]},
        "quality_settings": {"resolution": "3840x2160 or higher", "rendering_quality": "High, Vibrant Digital Painting"},
        "negative_prompt": "dark, cold colors, industrial, gloomy, overcast, signature, watermark, low quality, blurry, generic landscape",
        "style_negative_prompt": "unrealistic colors for the region, wrong architectural styles, flat lighting, muddy textures, overly digital look (unless intended as stylized)"
    }
    imagen_settings["mediterranean_style_settings"] = {
        "key_environments": "Sun-drenched coastal scenes, vibrant landscapes with characteristic flora (olive trees, cypress, bougainvillea, citrus groves), rustic architecture (whitewashed walls, terracotta roofs, blue shutters, stone pathways).",
        "color_palette_emphasis": "Emphasis on warm, bright, and natural colors: deep azure and cerulean blues of the sea and sky, brilliant whites of buildings, warm terracotta and ochre of earth and pottery, vibrant greens of foliage, and pops of color from flowers like bougainvillea.",
        "lighting_characteristics": "Bright natural sunlight creating a warm, inviting glow, often depicting golden hour light or the clear brightness of midday. Strong, defined shadows can add depth.",
        "digital_painting_techniques": "May involve painterly brushstrokes, textured rendering to simulate traditional media, or a cleaner, more illustrative style with digital precision. Focus on capturing light and color vibrancy.",
        "aesthetic_blend": "Vivid, colorful, and light-filled depictions of Mediterranean life, architecture, and scenery, achieved with digital painting techniques that may incorporate photorealistic details or expressive painterly textures to evoke a sense of warmth, beauty, and tranquility."
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
        "style_settings": {"art_movement": "Digital Surrealism / Morphing Art / Biomorphic Art", "post_processing": ["Seamless fluid transformations", "organic blending", "reality distortion effects", "subtle textural shifts during morph", "temporal displacement effects"], "style_era": "Contemporary Digital"},
        "lighting_settings": {"lighting_type": "Dreamlike, often with internal luminescence or shifting, illogical light sources", "light_quality": "Soft and shifting, ethereal, or dramatically contrasting", "light_direction": "Multiple, often unconventional or impossible"},
        "composition_settings": {"technique": "Surreal composition centered on the process or result of morphing elements, often with a focus on organic or impossible forms", "focal_point": "The Transformation itself, or the newly formed/forming entity"},
        "color_settings": {"color_scheme": "Vibrant Dreamlike, Unearthly, or Monochromatic with Accents", "palette_type": "Vibrant, dreamlike, often iridescent or bioluminescent colors; can also be desaturated or monochromatic for uncanny or unsettling effects", "color_temperature": "Mixed, often shifting or unnatural", "color_contrast": "Variable, from soft and blended to starkly contrasting"},
        "detail_settings": {"detail_level": "High, especially in the transitioning textures and forms", "texture_quality": "Smooth, fluid, and often organic or liquid-like textures; can incorporate unexpected textural juxtapositions (e.g., stone melting like wax, flesh turning to smoke)"},
        "environment_settings": {"weather": "N/A or Unnatural (e.g., raining indoors)", "season": "N/A or Timeless", "location_type": "Dreamscape, Liminal Space, Abstract Environment facilitating morphosis, or familiar settings made strange by transformations", "atmospheric_effects": ["Ethereal mist", "internal glows", "warping atmospheric effects", "temporal distortions", "impossible physics"]},
        "quality_settings": {"resolution": "3840x2160 or higher for detailed morphs", "rendering_quality": "High, emphasizing fluidity and surreal detail"},
        "negative_prompt": "realistic, static, logical, rigid, geometric (unless being morphed), signature, watermark, low quality, poorly blended transitions, mundane",
        "style_negative_prompt": "rigid forms, clear boundaries between objects (unless part of the morph concept), predictable transformations, lack of imagination, clunky or obvious digital manipulation"
    }
    imagen_settings["morphism_surreal_settings"] = {
        "transformation_style_details": "Surreal, fluid, and fantastical morphing of objects, figures, environments, or abstract concepts into one another, often defying logic, physics, and material properties.",
        "morphing_dynamics_and_flow": "Can be slow and seamless like melting or growing, or rapid and glitch-like; involves stretching, melting, interpenetrating, reconfiguring elements, or dissolving boundaries.",
        "conceptual_underpinnings": "Often explores themes of identity, subconscious, dreams, metamorphosis, the uncanny, or the instability of reality.",
        "color_and_texture_in_morphing": "Colors may bleed, shift, or become iridescent during transformation; textures may change from solid to liquid, organic to inorganic, smooth to rough, etc.",
        "compositional_focus": "Composition emphasizes the flow and transition between states, illogical progressions, the ambiguity of form, and the uncanny nature of the transformation.",
        "aesthetic_blend": "Visually striking surreal transformations where objects, figures, or entire scenes fluidly blend, melt, or evolve into new, often biomorphic or impossible forms, characterized by dreamlike logic, organic transitions, and often unsettling or wondrous juxtapositions. Aims to evoke a sense of wonder, unease, or a glimpse into the subconscious."
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
        "style_settings": {"art_movement": "Cubism / Mixed Media Fusion", "post_processing": ["Geometric fragmentation", "textured plane overlays", "collage element integration", "digital texturing on facets"], "style_era": "Modern / Contemporary"},
        "lighting_settings": {"lighting_type": "Abstracted, faceted lighting emphasizing planes and material interplay", "light_quality": "Hard-edged or diffused depending on mixed media elements", "light_direction": "Multiple, often non-naturalistic to highlight different facets and textures"},
        "composition_settings": {"technique": "Cubist fragmentation with integrated mixed media textures and elements, multi-perspective views", "focal_point": "Fragmented Subject, interplay of textures and forms"},
        "color_settings": {"color_scheme": "Muted Earthy Tones with Textural Accents, or Bold Contrasts", "palette_type": "Muted earthy tones (ochres, browns, grays) typical of Analytical Cubism, or bolder colors of Synthetic Cubism, enhanced by colors of integrated media", "color_temperature": "Neutral, Warm, or Cool depending on media and mood", "color_contrast": "Medium to High, emphasizing form and texture"},
        "detail_settings": {"detail_level": "High, showcasing both geometric deconstruction and material textures", "texture_quality": "Geometric planes with varied textures (e.g., simulated wood grain, newsprint, fabric, metallic sheens, digital noise) integrated into Cubist forms"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Abstract, Still Life, or Deconstructed Portrait Setting", "atmospheric_effects": ["none, or subtle digital texturing"]},
        "quality_settings": {"resolution": "2048x2048 or higher for textural detail", "rendering_quality": "Sharp Geometric Detail with Rich Textures"},
        "negative_prompt": "realistic, smooth, organic, traditional perspective, signature, watermark, low quality, overly blended, photorealism",
        "style_negative_prompt": "blended forms, soft edges, single viewpoint, lack of fragmentation, purely digital without texture"
    }
    imagen_settings["cubism_mixed_settings"] = {
        "cubist_principles": "Angular fragmented forms, multiple simultaneous perspectives, deconstruction of subject, flattened picture plane.",
        "mixed_media_elements": "Simulated or actual paper collage (newsprint, sheet music, wallpaper), fabric swatches, wood grain, metallic textures, digital textures (noise, patterns), typographic fragments, found object textures.",
        "textural_interplay": "Emphasis on the contrast and integration of smooth geometric planes with the tactile qualities of various materials.",
        "compositional_approach": "Geometric abstraction with layered planes, where different facets of an object or scene are shown simultaneously, incorporating textures from diverse media into the fragmented forms.",
        "aesthetic_blend": "Classic Cubist principles of deconstruction and multiple perspectives, enriched and recontextualized by the tactile qualities and visual diversity of mixed media elements, creating a contemporary, textured, and often more materially rich take on the style."
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
        "style_settings": {"art_movement": "Pixel Art / Voxel Art / Patchwork Fusion", "post_processing": ["Pixelation", "Voxelization", "Grid-based texture mapping", "Quilt-like seam effects (optional)", "Limited color palette enforcement"], "style_era": "Retro Digital / Contemporary Craft Hybrid"},
        "lighting_settings": {"lighting_type": "Flat, Simplified, or Basic Directional", "light_quality": "Hard-edged, uniform within blocks/pixels", "light_direction": "Often Top-down or Frontal for clarity"},
        "composition_settings": {"technique": "Grid-based composition, modular design, often isometric or orthographic projection", "focal_point": "Overall Pattern, Central Motif, or Character Sprite", "view_mode": "Isometric, orthographic, or 2D side-scrolling/top-down grid-based view"},
        "color_settings": {"color_scheme": "Limited Vibrant, Retro Game Palette, or Thematic Patchwork Colors", "palette_type": "Limited vibrant 8-bit or 16-bit color palette, or carefully chosen thematic colors for patchwork effect", "color_temperature": "Neutral or dependent on palette theme", "color_contrast": "High, emphasizing distinct blocks/pixels"},
        "detail_settings": {"detail_level": "Low to Medium (defined by pixel/voxel size)", "texture_quality": "Blocky geometric pixelated and voxelated textures, distinct color regions, simulated fabric/stitch textures for patchwork elements"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Abstract Grid, Tiled Landscape, Voxel World, or Digital Quilt Surface", "atmospheric_effects": ["None, or subtle scanlines/CRT effects for retro feel"]},
        "quality_settings": {"resolution": "Low base resolution (e.g., 64x64, 128x128, 256x256) scaled up for viewing, maintaining crisp pixels/voxels", "rendering_quality": "Crisp Pixelated/Voxelated, Deliberately Low-Fidelity"},
        "negative_prompt": "smooth, realistic, organic, anti-aliasing, gradients, high-resolution textures, signature, watermark, low quality, blurry",
        "style_negative_prompt": "high detail, blended colors, photographic realism, smooth curves, complex shading (unless dithered)"
    }
    imagen_settings["pixel_patchwork_settings"] = {
        "art_style_fusion": "Combines 2D pixel art sprites/tiles and/or 3D voxel art blocks with the compositional structure and aesthetic of patchwork quilting or mosaic art.",
        "color_palette_constraints": "Strict adherence to a limited color palette (e.g., NES, SNES, Game Boy, or custom folk art palettes) with dithering for intermediate shades if used.",
        "textural_qualities": "Blocky geometric pixelated and voxelated textures. For patchwork, this can be augmented with simulated fabric textures or stitch lines between 'patches' of pixels/voxels.",
        "compositional_structure": "Often arranged in a grid or tiled manner, resembling a quilt, mosaic, or a level map from a retro game. Can be figurative or abstract.",
        "dimensional_play": "May involve flat 2D pixel designs, isometric voxel constructions, or a mix, creating a unique interplay of 2D and pseudo-3D forms.",
        "aesthetic_blend": "A retro-inspired digital style combining the charming blockiness of pixel art and/or voxel art with the structured, patterned composition of patchwork or quilting. Results in geometric, colorful, and often nostalgic scenes, characters, or abstract designs."
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
        "style_settings": {"art_movement": "Phygital Art (Physical Object + Augmented Reality)", "post_processing": ["Real-time AR overlay rendering", "Physical-digital interaction effects", "Light and shadow matching between physical and virtual components", "Occlusion of AR by physical elements"], "style_era": "Contemporary / Emerging Tech"},
        "lighting_settings": {"lighting_type": "Coordinated Real-World and Augmented Reality Lighting", "light_quality": "Adaptive, ensuring AR elements integrate believably with physical object's illumination", "light_direction": "Matched to physical environment and dynamically updated for AR"},
        "composition_settings": {"technique": "Hybrid composition integrating a physical sculpture's form with dynamic, interactive AR digital layers and extensions", "focal_point": "The Integrated Phygital Subject, or the interaction point between physical and digital"},
        "color_settings": {"color_scheme": "Harmonious or Contrasting Physical/Digital Palette", "palette_type": "Palette considers physical material colors (wood, metal, ceramic, plastic) and digitally projected/overlaid colors, aiming for seamless integration or intentional juxtaposition", "color_temperature": "Adaptive to real-world lighting for AR, physical object's color inherent", "color_contrast": "Variable, designed for clarity of both physical and AR components"},
        "detail_settings": {"detail_level": "High in both physical sculpture and AR digital assets", "texture_quality": "High-fidelity physical sculpture textures (e.g., wood grain, metallic polish, ceramic glaze) augmented by crisp, well-rendered digital AR textures and effects"},
        "environment_settings": {"weather": "N/A (typically for indoor display, AR adapts to ambient conditions)", "season": "N/A", "location_type": "Gallery, Public Installation, or any space where the physical object is viewed with an AR device", "atmospheric_effects": ["Dynamic shadows cast by/on AR elements", "AR visual effects (particles, glows) interacting with physical object's perceived space"]},
        "quality_settings": {"resolution": "Device Native for AR (phone/tablet/headset screen), High Detail for physical sculpture", "rendering_quality": "Seamless Mixed Reality Integration, Real-time AR performance"},
        "negative_prompt": "purely physical without AR, purely digital AR without physical anchor, flat 2D, poorly tracked AR, signature, watermark, low quality, disjointed elements",
        "style_negative_prompt": "unblended appearance, non-interactive AR, AR elements not anchored to physical object, inconsistent lighting/shadows, laggy or glitchy AR"
    }
    imagen_settings["phygital_hybrid_settings"] = {
        "physical_component": "A tangible sculpture or object crafted from materials like wood, metal, ceramic, 3D printed resin, textiles, etc.",
        "digital_component_AR": "Interactive 3D models, animations, particle effects, soundscapes, or data visualizations experienced as an overlay or extension of the physical object via an AR-enabled device.",
        "media_fusion_concept": "Physical sculpture as a tangible anchor, augmented, transformed, or given new layers of meaning by interactive and dynamic digital art overlays experienced in real-time through AR.",
        "technology_stack": "AR-enabled devices (smartphones, tablets, AR headsets), 3D scanning of physical object (optional), 3D modeling software (Blender, Maya, ZBrush) for AR assets, AR development platforms (e.g., Unity with ARFoundation/MARS, Unreal Engine with ARKit/ARCore support, Spark AR, Adobe Aero).",
        "interaction_modalities": "AR elements can react to viewer proximity, gestures on device screen, real-world lighting changes, or even direct interaction with parts of the physical sculpture if sensorized.",
        "aesthetic_blend": "A true hybrid artwork that exists and is experienced simultaneously in physical and digital realms. The piece leverages the unique affordances of both tangible materials and interactive virtual elements to create a layered, often participatory, and context-aware experience that transcends either medium alone."
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
        "style_settings": {"art_movement": "Screen Printing / Serigraphy / Graphic Art", "post_processing": ["Layered ink effect", "slight misregistration simulation", "paper texture influence", "halftone pattern (optional)"], "style_era": "Contemporary or Retro Poster Art"},
        "lighting_settings": {"lighting_type": "Flat, even lighting (as inherent in the print medium)", "light_quality": "Hard-edged, emphasizing flat color planes", "light_direction": "N/A (light is part of the print's color, not external illumination)"},
        "composition_settings": {"technique": "Screen printing graphic style, bold shapes, negative space utilization", "focal_point": "Bold Shapes, Typographic Elements, or Central Graphic"},
        "color_settings": {"color_scheme": "Limited High Contrast, often 2-4 spot colors", "palette_type": "Limited high contrast colors (e.g., 2-4 distinct, often opaque, spot colors), can include metallic or fluorescent inks (simulated)", "color_temperature": "Neutral or as per design palette", "color_contrast": "Very High"},
        "detail_settings": {"detail_level": "Medium, defined by stencil edges and color layers", "texture_quality": "Flat layered ink texture, slight misregistration, paper texture interaction, halftone patterns (optional for shading)"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Print Studio, Poster Display, Abstract Graphic Background", "atmospheric_effects": ["none"]},
        "quality_settings": {"resolution": "2048x2048 or higher for crisp graphics", "rendering_quality": "Sharp Graphic Print, Clean Edges"},
        "negative_prompt": "gradients, blending, photorealistic, painterly strokes, excessive colors, signature, watermark, low quality, blurry edges",
        "style_negative_prompt": "soft edges, many colors, complex shading (unless halftone), photographic realism, lack of distinct layers"
    }
    imagen_settings["screen_printing_bold_settings"] = {
        "print_style_characteristics": "Bold graphic style with flat color areas, sharp edges, and distinct layers characteristic of screen printing (serigraphy).",
        "color_palette_details": "Limited high contrast color palette, often 2-4 spot colors. May include simulated metallic or fluorescent inks. Colors are typically opaque.",
        "ink_and_texture_properties": "Flat, opaque layered ink texture. Potential for slight, intentional misregistration between color layers. Interaction with paper texture (e.g., tooth of the paper showing through). Halftone dot patterns can be used for creating tones or gradients.",
        "ink_properties": "Opaque or semi-opaque ink layers, potential for overprinting effects where colors interact.",
        "design_elements": "Strong use of positive and negative space, bold typography, iconic imagery, geometric shapes, or stylized illustrations.",
        "aesthetic_blend": "Bold graphic prints reminiscent of serigraphy, characterized by flat areas of color, sharp edges, layered inks, and strong visual contrasts, often with a tactile quality and a handmade yet precise feel."
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
        "style_settings": {"art_movement": "Art Journaling / Mixed Media Expression", "post_processing": ["Layered textures", "handwritten text integration", "collage element blending", "distressing (optional)", "ink splatters"], "style_era": "Contemporary"},
        "lighting_settings": {"lighting_type": "Soft Ambient or Natural Desk Light", "light_quality": "Diffuse, even lighting suitable for viewing detailed pages", "light_direction": "Top or slightly angled front"},
        "composition_settings": {"technique": "Layered, often asymmetrical composition, intuitive arrangement of elements", "focal_point": "Personal themes, text, central imagery, or overall textural feel"},
        "color_settings": {"color_scheme": "Varied Eclectic, often Personal and Expressive", "palette_type": "Varied eclectic personal palette, often with a mix of muted and vibrant colors, can be thematic or spontaneous", "color_temperature": "Mixed, depending on mood and materials", "color_contrast": "Variable, from subtle to bold"},
        "detail_settings": {"detail_level": "High, with focus on individual elements and their textures", "texture_quality": "Layered varied textures (paper, paint, fabric, ink, found objects), often with visible brushstrokes, pen marks, material edges, and imperfections"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Studio/Desk, Flat Lay Perspective, or Open Journal Spread", "atmospheric_effects": ["none, or subtle depth from layering"]},
        "quality_settings": {"resolution": "2048x2560 or higher for print/scan quality", "rendering_quality": "Richly Textured, Handcrafted Feel"},
        "negative_prompt": "clean, purely digital, photorealistic, overly polished, signature (unless part of art), watermark, low quality, sterile, unlayered",
        "style_negative_prompt": "uniform texture, predictable layout, lack of personal touch, overly symmetrical, no visible layering, digitally perfect"
    }
    imagen_settings["mixed_media_journaling_settings"] = {
        "common_media": ["Collage elements (ephemera, photos, patterned paper, book pages, maps)", "drawing (pencil, ink pens, markers)", "painting (watercolor, acrylic, gouache, ink washes)", "ink stamps and stencils", "handwritten or typed text (quotes, personal reflections)", "fabric scraps, threads, ribbons", "washi tape", "stickers", "small found objects (buttons, dried flowers)."],
        "layering_style": "Overlapping, sometimes translucent layers, creating depth and visual interest. Elements may be partially obscured or revealed, building a history on the page.",
        "text_integration": "Handwritten journaling, calligraphy, typed text, cut-out words, rubber-stamped phrases, often integral to the meaning and composition.",
        "textural_qualities": "Emphasis on tactile experience: torn edges, crinkled paper, lumpy paint, fabric weave, smooth photo surfaces, metallic sheens.",
        "expressive_marks": "Doodles, scribbles, splatters, drips, intentional imperfections that add character.",
        "aesthetic_blend": "An eclectic, layered, and often deeply personal mixed media style typical of art journals, combining various materials and techniques to express thoughts, memories, creative explorations, or document life. Can be whimsical, introspective, grungy, or experimental."
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
        "style_settings": {"art_movement": "Pixel Art / Traditional Painting Fusion", "post_processing": ["Pixelation for characters", "painterly effects for background", "subtle integration effects (e.g., shared lighting influence, color harmony adjustments)", "bloom on painted areas"], "style_era": "Contemporary Hybrid"},
        "lighting_settings": {"lighting_type": "Mixed - Simplified/Pixelated for Characters, Complex/Painterly for Backgrounds", "light_quality": "Pixel art characters may have flat, dithered, or simple cel-style shading; backgrounds with rich, painterly light and shadow (e.g., chiaroscuro, atmospheric perspective).", "light_direction": "Consistent overall direction, but rendered differently per medium."},
        "composition_settings": {"technique": "Juxtaposition of pixel art characters/elements within traditionally painted environments or scenes", "focal_point": "Pixel Art Character(s) or key pixelated element, often contrasted against the background."},
        "color_settings": {"color_scheme": "Vibrant Mixed Palette, often with distinct palettes for pixel vs. painted areas", "palette_type": "Vibrant mixed palette: limited, often indexed, pixel art colors for characters; broader, richer painterly palette for backgrounds, with consideration for overall visual harmony or intentional contrast.", "color_temperature": "Mixed, can vary between foreground and background to enhance separation or mood", "color_contrast": "High between pixel elements and painted background, variable within each style."},
        "detail_settings": {"detail_level": "Mixed: Low-to-medium for pixel art (defined by pixel size), medium-to-high for painted background", "texture_quality": "Crisp pixelated character texture (blocky, aliased edges) contrasted with rich painterly background textures (e.g., canvas weave, visible brushstrokes, impasto, glazing)."},
        "environment_settings": {"weather": "N/A or as depicted in painted background", "season": "N/A or as depicted in painted background", "location_type": "Fantasy Landscape, Sci-Fi Setting, Surreal Dreamscape, or Reimagined Classical Scene", "atmospheric_effects": ["Painterly atmospheric perspective in background", "pixelated particle effects (optional)"]},
        "quality_settings": {"resolution": "3840x2160 or higher to appreciate both pixel detail and painterly texture", "rendering_quality": "High-Fidelity Hybrid, clear distinction and/or artful blending of styles"},
        "negative_prompt": "uniform style throughout, purely photorealistic, purely pixel art, signature, watermark, low quality, blurry pixels, muddy paint, poorly integrated elements",
        "style_negative_prompt": "unblended or clashing styles, inconsistent resolution or detail levels (unintentionally), pixelated background, overly smooth characters, lack of distinct media characteristics"
    }
    imagen_settings["digital_pixel_traditional_settings"] = {
        "pixel_art_component": "Characters, objects, or UI elements rendered in a distinct pixel art style (e.g., 8-bit, 16-bit, isometric pixel art) with limited color palettes and visible pixels.",
        "traditional_painting_component": "Backgrounds, environments, or specific elements rendered with techniques emulating traditional media like oil painting, acrylics, watercolor, or gouache, showcasing brushwork, texture, and complex lighting.",
        "integration_strategy": "Can range from stark juxtaposition (pixel elements clearly 'on top' of a painted scene) to more integrated approaches where lighting and color from the painted environment subtly affect the pixel art, or vice-versa.",
        "thematic_purpose": "Often used to evoke nostalgia, create a unique visual dissonance or harmony, or explore themes of digital vs. analog, retro vs. contemporary.",
        "aesthetic_blend": "A striking fusion where sharply defined, retro-style pixel art characters or elements inhabit lush, textured environments rendered with traditional painting techniques. This creates a unique visual and thematic contrast or an unexpected harmony between two distinct artistic languages."
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
        "style_settings": {"art_movement": "Textile Art / Patchwork Quilting / Fiber Art", "post_processing": ["Visible stitched seams (simulated)", "fabric texture highlights", "subtle depth between patches", "appliqué detailing"], "style_era": "Contemporary Craft / Traditional Folk"},
        "lighting_settings": {"lighting_type": "Soft Ambient or Gentle Directional (simulating gallery or natural light on textile)", "light_quality": "Diffuse, accentuating fabric textures and layered depth", "light_direction": "Top or slightly angled front"},
        "composition_settings": {"technique": "Fabric layering, quilting patterns, appliqué techniques, piecing", "focal_point": "Overall Pattern, Central Motif, or Textural Interplay"},
        "color_settings": {"color_scheme": "Warm Earthy, Traditional Folk, Contemporary Bold, or Monochromatic with Textural Contrast", "palette_type": "Warm earthy, traditional folk (e.g., Amish quilts), or contemporary fabric color palettes; can be patterned or solid", "color_temperature": "Warm, Neutral, or Cool depending on chosen fabrics and theme", "color_contrast": "Medium to High, depending on pattern complexity"},
        "detail_settings": {"detail_level": "High, focusing on fabric weave, stitch detail, and material edges", "texture_quality": "Soft tactile fabric textures (cotton, linen, felt, silk, wool), visible weave, thread details, batting puffiness (if quilted)"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Studio Setting, Wall Hanging Display, or Abstract Textured Background", "atmospheric_effects": ["None, or subtle shadows indicating layers"]},
        "quality_settings": {"resolution": "2048x2048 or higher for detailed textile work", "rendering_quality": "Rich Textile Detail, Handcrafted Appearance"},
        "negative_prompt": "smooth, purely digital, photorealistic rendering, glossy, metallic, signature, watermark, low quality, blurry textures, flat colors (unintentionally)",
        "style_negative_prompt": "flat colors without texture, uniform pattern without variation, lack of handcrafted feel, no visible stitching or fabric qualities"
    }
    imagen_settings["patchwork_fabric_settings"] = {
        "fabric_types_simulated": "Various fabric textiles like cotton prints, solids, linen, silk, wool, felt, denim, corduroy; consideration of fabric weight and drape.",
        "assembly_techniques_simulated": "Sewn and layered fabric patches, appliqué (hand or machine look), quilting stitches (e.g., running stitch, backstitch, free-motion quilting, decorative stitches), piecing (e.g., log cabin, flying geese patterns).",
        "textural_details": "Emphasis on soft tactile fabric textures, visible weave of different materials, thread thickness and color, slight puckering from stitches, batting loft if quilted.",
        "color_and_pattern_choices": "Warm earthy tones, traditional folk colorways, contemporary bold graphics, or subtle monochromatic schemes. Use of patterned fabrics (florals, geometrics, stripes) alongside solids.",
        "aesthetic_blend": "Textile art emphasizing the tactile qualities of fabric, visible stitching, and the compositional arrangement of patterned or solid-color patches. Often evokes craft traditions, quilting, folk art, or contemporary fiber art, celebrating the beauty of textile construction."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_mixed_media_collage_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Physical Mixed Media Collage Preset",
        "moods": ["Eclectic", "Textured", "Found Object Art"],
        "aspect_ratio": "1:1",
        "description": "An eclectic preset for purely physical mixed media collage, combining diverse materials and textures into a cohesive, tactile piece."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Physical Mixed Media Collage / Assemblage", "post_processing": ["Emphasis on layered physical textures", "shadows from overlapping materials", "material edge definition", "tactile surface quality"], "style_era": "Contemporary / Modern"},
        "lighting_settings": {"lighting_type": "Studio lighting simulating how a physical collage would be lit (e.g., raking light to show texture, softbox for even illumination)", "light_quality": "Directional or Diffuse, chosen to enhance material properties", "light_direction": "Often slightly angled to reveal depth and texture"},
        "composition_settings": {"technique": "Collage assembly and layering of physical materials, juxtaposition of forms and textures", "focal_point": "Key Juxtaposed Elements, Textural Contrast, or Overall Compositional Balance"},
        "color_settings": {"color_scheme": "Varied Eclectic, Thematic, or Material-Driven", "palette_type": "Varied eclectic color palette derived from the inherent colors of the materials used, can be harmonious or intentionally dissonant", "color_temperature": "Mixed, dependent on materials and artistic intent", "color_contrast": "Variable, from subtle textural shifts to bold material contrasts"},
        "detail_settings": {"detail_level": "High, focusing on the intrinsic qualities of each material", "texture_quality": "Highly layered tactile textures from physical materials (paper, fabric, paint, found objects, wood, metal), emphasizing their inherent qualities like roughness, smoothness, transparency, opacity."},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Studio Setting, Flat Lay, or Wall-Mounted Display Perspective", "atmospheric_effects": ["Subtle shadows between layers indicating depth"]},
        "quality_settings": {"resolution": "2048x2048 or higher for capturing material detail", "rendering_quality": "Richly Textured, Tactile, Hand-Assembled Look"},
        "negative_prompt": "smooth, purely digital, flat, signature, watermark, low quality, CGI, 3D render, unconvincing materials",
        "style_negative_prompt": "uniform texture, predictable layout, lack of material diversity, elements appearing flat or digitally drawn, no sense of physical layering"
    }
    imagen_settings["mixed_media_collage_settings"] = {
        "physical_materials_palette": ["Paper cutouts (magazines, newspapers, photos, handmade paper, maps, ephemera)", "acrylic paint, oil pastels, ink, charcoal", "fabric scraps, threads, yarn", "found objects (buttons, keys, bottle caps, natural elements like leaves or twigs, metal pieces, plastic bits)", "wood, cardboard, metal foil."],
        "assembly_methods_simulated": "Gluing (visible or hidden), stitching, stapling, riveting, layering, weaving, embedding objects into a substrate (e.g., gesso, modeling paste).",
        "textural_emphasis": "Focus on the inherent textures of diverse materials: torn edges of paper, weave of fabric, roughness of wood, smoothness of plastic, impasto of paint.",
        "dimensional_aspects": "Can range from relatively flat layered compositions to more dimensional assemblage with protruding elements.",
        "conceptual_approach": "Often involves juxtaposition of disparate materials and images to create new meanings, narratives, or abstract compositions. Can be thematic, symbolic, or purely formal.",
        "aesthetic_blend": "An eclectic and tactile collage style that combines diverse physical media and textures into a cohesive and layered artwork, celebrating material interplay, the history of found objects, and often resulting in narrative, abstract, or symbolic expressions. Emphasizes the handcrafted and unique nature of assembled art."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_whimsical_fantasy_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Whimsical Fantasy Illustration Preset",
        "moods": ["Dreamy", "Playful", "Magical", "Enchanting"],
        "aspect_ratio": "16:9",
        "description": "A dreamy preset for fantasy illustration with playful characters, soft whimsical elements, and a touch of magic, often digitally painted."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Whimsical Fantasy Illustration / Storybook Art", "post_processing": ["Soft glows", "sparkle effects", "iridescent highlights", "dreamy blurs", "subtle lens flare"], "style_era": "Contemporary Digital Illustration"},
        "lighting_settings": {"lighting_type": "Soft Ambient, Magical, or Dappled Light", "light_quality": "Soft, ethereal, magical glow, often with luminous elements", "light_direction": "Top, Front, or Backlit for ethereal feel"},
        "composition_settings": {"technique": "Layered composition, often with a clear narrative or character focus, dynamic or gentle poses", "focal_point": "Charming Characters, Mythical Creatures, or Enchanting Scenes"},
        "color_settings": {"color_scheme": "Pastel Soft, Luminous Analogous, or Split-Complementary with Iridescent Accents", "palette_type": "Pastel, soft, and luminous fantasy palette, often with iridescent, pearlescent, or glowing qualities; can include muted brights for accents", "color_temperature": "Cool to Neutral, or Warm for cozy/golden hour scenes", "color_contrast": "Low to Medium, emphasizing softness and harmony"},
        "detail_settings": {"detail_level": "Medium to High, with attention to expressive character details and charming environmental touches", "texture_quality": "Soft layered textures (digital painterly, airbrushed, or clean cel-shaded), with optional glittery, glowing, or magical particle effects. Smooth skin, flowing hair/fabric."},
        "environment_settings": {"weather": "Magical (e.g., gentle glowing rain, sparkling snow)", "season": "Perpetual Spring/Summer, or Mystical Autumn/Winter", "location_type": "Enchanted Forest, Fairy Tale Kingdom, Dreamscape, Magical Realm, Cozy Cottage Interior", "atmospheric_effects": ["Mist", "sparkles", "glowing dust motes", "soft lens flares", "bokeh backgrounds"]},
        "quality_settings": {"resolution": "3840x2160 or higher for detailed illustration", "rendering_quality": "Painterly Soft, Luminous, and Polished Digital"},
        "negative_prompt": "harsh, realistic, dark, gritty, overly complex, photorealistic, signature, watermark, low quality, mundane, violent",
        "style_negative_prompt": "serious or somber mood, high contrast without purpose, sharp aggressive edges, flat or muddy colors, lack of charm or magic, overly simplistic or crude"
    }
    imagen_settings["whimsical_fantasy_settings"] = {
        "character_archetypes": "Charming fantasy creatures (fairies, sprites, talking animals, gentle dragons, gnomes, elves), innocent or adventurous child/young adult protagonists.",
        "common_motifs": "Soft pastel and luminous color palettes, dreamy and magical atmosphere, sparkling/glowing elements (stars, hearts, swirls, bubbles, magical trails), enchanted nature (glowing mushrooms, whimsical trees, friendly animals), floating islands, crystal formations.",
        "textural_approach": "Soft, blended digital painting textures, possibly with clean cel-shading elements for characters, enhanced by magical glows, sparkles, iridescent effects, and soft focus backgrounds.",
        "emotional_tone": "Evokes a sense of lightheartedness, dreaminess, enchantment, childlike wonder, comfort, and gentle adventure.",
        "narrative_style": "Often illustrative of a story or concept, suitable for children's books, fantasy game concept art (lighthearted), or charming standalone fantasy pieces.",
        "aesthetic_blend": "A dreamy and enchanting digital illustration style characterized by playful characters, magical elements, soft pastel or luminous color palettes, and an overall sense of wonder and lighthearted fantasy. Celebrates imagination, kindness, and the beauty of magical worlds."
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
        "style_settings": {"art_movement": "Anime / Oil Painting Fusion", "post_processing": ["Simulated oil brush glaze", "impasto texture effects", "canvas texture overlay", "painterly edge blending"], "style_era": "Contemporary Hybrid"},
        "lighting_settings": {"lighting_type": "Soft Rim Lighting, Chiaroscuro, or Classical Portrait Lighting", "light_quality": "Soft, painterly light with visible brushwork in highlights and shadows, mimicking oil glazing and impasto techniques", "light_direction": "Side, three-quarter, or as per classical portraiture"},
        "composition_settings": {"technique": "Stylized character focus, often portrait or bust, with painterly background considerations", "focal_point": "Character's face and expression"},
        "color_settings": {"color_scheme": "Pastel with Vivid Accents, or Rich Oil Colors", "palette_type": "Anime-style character colors (e.g., vibrant hair, expressive eye colors, fair skin tones) rendered with the depth, richness, and blending capabilities of an oil palette", "color_temperature": "Warm, Cool, or Neutral depending on mood", "color_contrast": "Medium to High, with soft transitions"},
        "detail_settings": {"detail_level": "High, capturing both anime stylization and oil paint texture", "texture_quality": "Visible oil paint impasto texture, canvas grain, and brushstroke details, particularly on clothing, hair, and background elements, contrasted with smoother rendering on faces if desired."},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Studio, Abstract Painterly Background, or Stylized Scenic Backdrop", "atmospheric_effects": ["Subtle sfumato", "painterly depth of field"]},
        "quality_settings": {"resolution": "3840x2160 or higher for detail", "rendering_quality": "Painterly Stylized Fusion, Rich Textures"},
        "negative_prompt": "pure anime cel-shading, pure photorealistic oil painting, flat colors, signature, watermark, low quality, inconsistent styles, digital artifacts",
        "style_negative_prompt": "unblended styles, harsh digital lines on painted areas, flat anime look without painterly depth, muddy colors, loss of character stylization"
    }
    imagen_settings["anime_oilpainting_settings"] = {
        "character_design_approach": "Classic anime or manga character designs (e.g., large expressive eyes, stylized hair, specific costume elements) rendered with the volumetric forms, subtle color transitions, and lighting characteristic of oil painting.",
        "canvas_and_brushwork_simulation": "Visible linen or cotton canvas texture, simulated impasto effects, varied brushstrokes (e.g., fine details, broad strokes, glazing layers).",
        "lighting_and_shading_style": "Soft rim lighting, chiaroscuro, or classical portrait lighting to create depth and volume, with painterly highlights and shadows rather than flat cel-shading.",
        "color_palette_fusion": "Anime character color schemes (often vibrant or pastel) interpreted through the richer, more nuanced blending possibilities of oil paints.",
        "aesthetic_blend": "A unique fusion where stylized anime or manga character forms are rendered with the rich textures, volumetric lighting, painterly brushwork, and color depth characteristic of traditional oil painting, creating a bridge between two distinct artistic traditions."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_minimalist_geometric_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Digital Geometric Minimalism Preset",
        "moods": ["Minimal", "Clean", "Abstract", "Precise"],
        "aspect_ratio": "1:1", # Often square or simple ratios
        "description": "An abstract preset for Digital Geometric Minimalism, focusing on extreme simplicity, precise geometric forms, negative space, and balanced compositions, often with a clean, vector-like aesthetic."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Digital Geometric Minimalism / Abstract Constructivism / Neo-Geo", "post_processing": ["Crisp vector rendering", "perfectly flat color fields", "subtle paper/screen texture (optional)", "anti-aliasing for sharp edges"], "style_era": "Contemporary Digital"},
        "lighting_settings": {"lighting_type": "Flat, Even, or Subtly Graded Ambient Lighting", "light_quality": "Often shadowless or with highly stylized, hard-edged geometric shadows that become part of the composition", "light_direction": "N/A or uniform to emphasize flatness"},
        "composition_settings": {"technique": "Geometric abstraction with asymmetric or symmetric balance, precise alignment, use of grids (implied or explicit)", "focal_point": "Negative Space, Interplay of Forms, or Overall Compositional Harmony"},
        "color_settings": {"color_scheme": "Monochromatic, Analogous, or Severely Limited Palette", "palette_type": "Monochromatic (shades of one color), analogous, or a severely limited palette (e.g., 2-3 distinct colors) of pastel, neutral, bold primary, or black/white.", "color_temperature": "Neutral, Cool, or Warm based on palette choice", "color_contrast": "Variable, can be low for subtlety or high for graphic impact"},
        "detail_settings": {"detail_level": "Very Low in terms of ornamentation, Very High in terms of precision", "texture_quality": "Perfectly smooth, or with a very subtle, uniform digital texture (e.g., fine grain, simulated paper, LCD screen pixel grid)"},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Abstract, Non-representational Space", "atmospheric_effects": ["None, emphasizing clarity and purity of form"]},
        "quality_settings": {"resolution": "2048x2048 or scalable vector output", "rendering_quality": "Clean Graphic, Vector Precision"},
        "negative_prompt": "high detail, complex ornamentation, organic shapes, painterly textures, gradients (unless intentionally stylized), signature, watermark, low quality, clutter, messiness",
        "style_negative_prompt": "busy composition, varied uncontrolled colors, hand-drawn look, lack of precision, representational elements (unless highly abstracted)"
    }
    imagen_settings["minimalist_geometric_settings"] = {
        "geometric_primitives": "Emphasis on basic geometric shapes: circles, squares, rectangles, triangles, lines, points, arcs.",
        "compositional_principles": "Extreme simplicity, reduction to essential forms, significant use of negative space, precise alignment and spacing, exploration of balance (symmetrical or asymmetrical) and proportional relationships.",
        "color_usage": "Flat color fields, often a limited palette. Color choices are deliberate and contribute to the overall compositional structure and mood.",
        "line_quality": "Clean, precise, often thin lines with uniform weight, or no lines at all (shapes defined by color boundaries).",
        "digital_execution_emphasis": "Leverages digital tools for perfect geometric forms, sharp edges, uniform colors, and precise arrangements not easily achievable by hand. May simulate vector art.",
        "aesthetic_blend": "Extreme geometric abstraction achieved with digital precision, focusing on negative space, balance, proportional rhythm, and a clean, uncluttered, often serene or intellectually stimulating aesthetic. It's about 'less is more' executed perfectly."
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
        "style_settings": {"art_movement": "Pop Surrealism / ASCII Art Fusion / Lowbrow Tech", "post_processing": ["ASCII character mosaic overlay", "retro terminal effects (optional scanlines, bloom)", "color palette quantization for ASCII layer"], "style_era": "Contemporary Digital Hybrid"},
        "lighting_settings": {"lighting_type": "Implied by ASCII character density and/or simulated CRT glow; underlying Pop Surrealist image may have its own distinct lighting", "light_quality": "Simulated phosphor for ASCII, potentially painterly or illustrative for underlying image", "light_direction": "Grid scan for ASCII, varied for underlying image"},
        "composition_settings": {"technique": "ASCII mosaic composition overlaying or forming Pop Surrealist imagery", "focal_point": "Central Pop Surrealist Subject rendered/filtered through ASCII"},
        "color_settings": {"color_scheme": "Monochrome ASCII over Full Color, or Limited ANSI Color ASCII", "palette_type": "Classic terminal monochrome (green, amber, white on black/blue) or limited ANSI colors for ASCII elements. Underlying Pop Surrealist image may have vibrant, candy-colored, or muted palette.", "color_temperature": "Cool for ASCII, varied for Pop Surrealism base", "color_contrast": "High for ASCII readability, variable for underlying image"},
        "detail_settings": {"detail_level": "Medium, defined by character resolution of ASCII; underlying image may be detailed", "texture_quality": "Distinct ASCII character texture forming the image, potential for dithered shading with characters. Underlying image may have smooth or painterly textures."},
        "environment_settings": {"weather": "N/A", "season": "N/A", "location_type": "Digital Space, Retro Console Screen, or Abstract representation of Pop Surrealist scene", "atmospheric_effects": ["Phosphor flicker", "scanlines", "digital noise for ASCII layer; dreamlike or mundane for Pop Surrealist layer"]},
        "quality_settings": {"resolution": "1280x720 or higher, to balance ASCII clarity and underlying image detail", "rendering_quality": "Retro Digital Fusion, Intentional Lo-Fi elements"},
        "negative_prompt": "pure realism, full-color photography without ASCII, smooth gradients (unless dithered in ASCII), signature, watermark, low quality, unreadable ASCII, poorly integrated styles",
        "style_negative_prompt": "natural photo, smooth curves (unless part of Pop Surrealist subject), generic ASCII art without Pop Surrealist theme, clashing palettes"
    }
    imagen_settings["pop_surrealism_ascii_settings"] = {
        "pop_surrealist_subject_matter": "Pop culture icons, cartoonish figures, kitschy objects, anthropomorphic animals, or lowbrow art subjects, often with a narrative, humorous, or unsettling twist.",
        "ascii_rendering_technique": "The Pop Surrealist image is translated into an ASCII mosaic, where characters of varying brightness or different characters represent tones and forms. Can be a direct overlay or a more integrated reinterpretation.",
        "visual_irony_and_juxtaposition": "The core of the style lies in the juxtaposition of playful, cute, or unsettling Pop Surrealist imagery with the rigid, retro-tech, and often impersonal aesthetic of ASCII art.",
        "color_interaction": "If the underlying Pop Surrealist image is in color, the monochrome or limited-color ASCII layer creates a distinct visual filter or reinterpretation. ANSI colors in ASCII can interact with the base image's palette.",
        "pattern_and_density": "Medium to high density ASCII patterns to form recognizable images, with character choice contributing to texture and shading.",
        "aesthetic_blend": "A bizarre and playful fusion where cartoonish, lowbrow, or dreamlike Pop Surrealist subjects are re-rendered as digital character mosaics. This combines whimsical, cute, or unsettling themes with a retro-tech, text-based visual style, often creating a humorous or thought-provoking commentary on digital culture and art."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_dreamcore_weirdcore_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Dreamcore/Weirdcore Aesthetic Preset",
        "moods": ["Nostalgic", "Uncanny", "Eerie", "Liminal", "Surreal"],
        "aspect_ratio": "16:9", # Common, but 4:3 also seen for retro feel
        "description": "A surreal preset blending nostalgic dreaminess (Dreamcore) with unsettling, bizarre, or inexplicable objects and environments (Weirdcore), often evoking liminal spaces and low-fidelity aesthetics."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Dreamcore / Weirdcore / Liminal Space Aesthetic / Internet Art", "post_processing": ["VHS/low-fi artifacts", "scan error effects", "smudging", "slight chromatic aberration", "soft focus/blur", "JPEG compression artifacts"], "style_era": "Contemporary Internet Aesthetic (influenced by late 90s/early 2000s digital imagery)"},
        "lighting_settings": {"lighting_type": "Ambient, often dim, or unnaturally even/flat", "light_quality": "Often dim, foggy, or unnaturally even; can feature isolated, unexplained, or flickering light sources (e.g., fluorescent hum)", "light_direction": "Multiple, ambiguous, or non-directional"},
        "composition_settings": {"technique": "Uncanny juxtaposition, empty or sparsely populated spaces, familiar places made unsettling, off-kilter perspectives", "focal_point": "Ambiguous objects, unsettling voids, distorted familiar items, or the overall unsettling atmosphere"},
        "color_settings": {"color_scheme": "Pale, Neon, Desaturated, or Off-Key", "palette_type": "Desaturated, pale, or off-key color palette; sometimes with isolated neon, primary color accents, or sickly greens/yellows. Often involves color shifts or bleeding.", "color_temperature": "Cool, or unnaturally mixed", "color_contrast": "Low to Medium, sometimes with harsh digital contrast"},
        "detail_settings": {"detail_level": "Medium to Low, often intentionally obscured or low-resolution", "texture_quality": "Often smudged, blurry, or low-resolution textures; can have digital noise, JPEG artifacts, or simulated analog static"},
        "environment_settings": {"weather": "Foggy, Overcast, or Indeterminate Night", "season": "N/A or ambiguously out-of-season", "location_type": "Liminal Spaces (e.g., empty hallways, abandoned malls, playgrounds at night, infinite rooms), familiar yet unsettling domestic interiors, or abstract digital voids", "atmospheric_effects": ["Fog, mist, digital haze, unexplained glows, visual static, lens flares from unknown sources"]},
        "quality_settings": {"resolution": "1920x1080 or lower, often emulating older digital formats", "rendering_quality": "Low-fidelity aesthetic, intentionally imperfect"},
        "negative_prompt": "clear, realistic, logical, well-lit, sharp focus, high definition, signature, watermark, high quality, comforting, normal",
        "style_negative_prompt": "sharp detail, vibrant healthy colors, conventional composition, clear narrative, lack of ambiguity or unease"
    }
    imagen_settings["dreamcore_weirdcore_settings"] = {
        "dominant_atmosphere": "Nostalgic, uncanny, eerie, dreamlike, sometimes unsettling, melancholic, or strangely comforting. Evokes feelings of being lost, isolated, disoriented, or in a transitional state.",
        "visual_distortion_techniques": "Low-fidelity digital artifacts (VHS tracking errors, old camera footage, JPEG compression), scan errors, slight smudging or blurring, lens distortion, fisheye, chromatic aberration, pixelation.",
        "common_motifs_and_iconography": "Ambiguous objects, surreal geometry, portals, eyes (often staring or hidden), empty rooms, long corridors, staircases to nowhere, playgrounds, pools, arcades, outdated technology, familiar places devoid of people or rendered strange.",
        "liminality_aspect": "Focus on transitional spaces, thresholds, or states of being - places or times that are 'in-between'.",
        "aesthetic_blend": "A digital aesthetic blending nostalgic, often childhood-related dreaminess and familiarity (Dreamcore) with unsettling, bizarre, or inexplicable objects, entities, and environments (Weirdcore). Characterized by liminal spaces, low-fidelity visuals, anachronistic elements, and an uncanny, slightly eerie, or melancholic mood that taps into collective subconscious or forgotten memories."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_fantasy_battle_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Fantasy Battle Digital Painting Preset",
        "moods": ["Epic", "Intense", "Dramatic", "Action-Packed"],
        "aspect_ratio": "16:9",
        "description": "An intense preset for epic fantasy battle scenes, realized through dynamic digital painting with magical effects and cinematic composition."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Fantasy Battle Digital Painting / Concept Art", "post_processing": ["Dynamic magical effects (spells, explosions, energy blasts)", "motion blur (action-focused)", "atmospheric particle effects (dust, debris, embers)", "cinematic color grading", "lens flares from magical sources"], "style_era": "Contemporary Digital"},
        "lighting_settings": {"lighting_type": "Dramatic, high-contrast lighting, often with multiple sources (e.g., clashing spells, fiery explosions, divine light, moonlit battlefield)", "light_quality": "Magical, intense, casting long shadows and bright highlights", "light_direction": "Multiple, dynamic, emphasizing action and key figures"},
        "composition_settings": {"technique": "Dynamic, action-oriented composition (e.g., low angles, Dutch angles, leading lines towards conflict, strong diagonals)", "focal_point": "Central Combatants, Climax of Action, or Key Magical Event", "view_mode": "Dynamic action-packed perspective, often wide to show scale or close-up for impact", "motion_blur": "Medium to high motion blur on fast-moving elements"},
        "color_settings": {"color_scheme": "Rich Saturated, often with Contrasting Warm and Cool Tones", "palette_type": "Rich saturated reds, oranges, blues, purples, golds, contrasted with dark, shadowy areas. Palette often reflects magical energies or faction colors.", "color_temperature": "Mixed, often with clashing warm (fire, explosions) and cool (magic, night) light", "color_contrast": "Very High, for dramatic impact"},
        "detail_settings": {"detail_level": "Very High, especially on characters, armor, weapons, and magical effects", "texture_quality": "Realistic or stylized textures for armor, cloth, skin, magical energy, and environmental elements (stone, metal, fire)."},
        "environment_settings": {"weather": "Stormy, Fiery, or magically altered weather; dust clouds, magical energy storms", "season": "N/A, or thematic to the battle setting", "location_type": "Ancient Battlefield, Castle Siege, Dragon's Lair, Mystical Forest Clearing, Hellish Landscape", "atmospheric_effects": ["Smoke, fire, magical glow, energy ripples, debris, dust, rain, snow (if thematic)"]},
        "quality_settings": {"resolution": "4096x2160 (4K) or higher for epic detail", "rendering_quality": "Ultra High Detail, Cinematic Digital Painting"},
        "negative_prompt": "calm, peaceful, static, low detail, mundane, signature, watermark, low quality, bright daylight (unless specific concept), cartoony",
        "style_negative_prompt": "static composition, bland colors, lack of action or intensity, poorly rendered magical effects, unconvincing combat poses"
    }
    imagen_settings["fantasy_battle_settings"] = {
        "combatant_types": "Wizards vs. knights, dragons vs. heroes, armies clashing, mythical beasts in combat, angelic vs. demonic forces.",
        "environmental_context": "Ancient battlefield ruins, besieged castle walls, volcanic plains, enchanted forests, celestial arenas.",
        "action_and_impact_elements": "Magical spells clashing (fireballs, lightning, force fields), sword impacts with sparks, arrows in flight, dynamic poses, characters leaping or falling, environmental destruction.",
        "overall_atmosphere": "Chaotic, epic, intense, dramatic, often with a sense of urgency, high stakes, and grand scale.",
        "magical_special_effects": "Magical explosions, glowing runes, particle effects (embers, magical dust), energy beams, protective wards, summoning portals.",
        "lighting_dynamics": "Dramatic chiaroscuro emphasizing action, with magical light sources (fire, spells, enchanted weapons) casting strong, often colored, highlights and deep shadows.",
        "compositional_strategy": "Dynamic angles (low, high, tilted) with motion blur, particle effects, and strong compositional lines (diagonals, S-curves) focusing on the central conflict and conveying movement and energy."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_fantasy_landscape_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Fantasy Landscape Digital Painting Preset",
        "moods": ["Epic", "Mysterious", "Vast", "Awe-inspiring", "Enchanting"],
        "aspect_ratio": "16:9", # Or other cinematic ratios like 2.35:1
        "description": "A vast preset for epic fantasy landscapes, brought to life through evocative digital painting with magical elements, unique geography, and dramatic lighting."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Fantasy Landscape Digital Painting / Environment Concept Art", "post_processing": ["Magical atmospheric effects (e.g., god rays, glowing particles, aurora)", "painterly textures", "cinematic color grading for mood", "depth of field"], "style_era": "Contemporary Digital"},
        "lighting_settings": {"lighting_type": "Dramatic natural or magical lighting (e.g., epic sunsets, dual moons, bioluminescence, celestial events)", "light_quality": "Ethereal, volumetric, casting long shadows, creating strong highlights", "light_direction": "Multiple, often from grand sources like setting suns, magical artifacts, or otherworldly skies"},
        "composition_settings": {"technique": "Wide-angle panoramic, establishing shots, rule of thirds, leading lines to guide the eye through the vista, strong foreground/midground/background elements", "focal_point": "Majestic Landmark (e.g., floating castle, ancient tree, colossal statue), Unique Geographical Feature, or Portal to another realm"},
        "color_settings": {"color_scheme": "Rich Saturated, Muted and Atmospheric, or Unearthly Palettes", "palette_type": "Rich saturated fantasy palette (deep blues, purples, greens, golds), or more muted and atmospheric for mysterious scenes. Colors often reflect magical properties or time of day.", "color_temperature": "Mixed, often with strong warm/cool contrasts", "color_contrast": "High, to emphasize scale and drama"},
        "detail_settings": {"detail_level": "Very High in focal areas, painterly or slightly abstracted in distant elements to convey scale", "texture_quality": "Realistic or stylized textures for rock, foliage, water, clouds, and fantastical structures. Digital painting brushwork evident."},
        "environment_settings": {"weather": "Mysterious, Magical, Stormy, Serene, or Alien", "season": "N/A, or fantastical seasons (e.g., eternal twilight, crystal winter)", "location_type": "Enchanted Realm, Floating Islands, Alien World, Ancient Lost Civilization, Dragon's Peak, Underworld Vista", "atmospheric_effects": ["Mist, fog, glowing particles, aurora borealis, magical energy fields, unusual cloud formations, multiple moons/suns"]},
        "quality_settings": {"resolution": "4096x2160 (4K) or higher for sweeping vistas", "rendering_quality": "Ultra High Detail, Painterly Finish, Cinematic Feel"},
        "negative_prompt": "mundane, realistic Earth-like (unless intended), low detail, flat lighting, signature, watermark, low quality, boring composition, modern human elements",
        "style_negative_prompt": "boring or generic composition, flat or uninspired lighting, lack of scale or wonder, overly cartoony (unless specific style), clashing colors"
    }
    imagen_settings["fantasy_landscape_settings"] = {
        "geographical_features": "Floating islands with waterfalls, colossal ancient trees, crystal mountains, impossible rock formations, glowing rivers, alien flora and fauna.",
        "architectural_elements": "Ancient ruins, majestic castles, hidden temples, ethereal cities, monolithic structures of unknown origin.",
        "magical_phenomena": "Glowing flora/fauna, visible magic energies, portals, celestial anomalies, mythical creatures in the distance (dragons, griffins, etc.).",
        "overall_atmosphere": "Enchanted, mysterious, vast, awe-inspiring, serene, perilous, or ancient and forgotten.",
        "lighting_and_sky_details": "Ethereal light rays (god rays) breaking through clouds, dramatic sunsets/sunrises with multiple suns/moons, star-filled skies with nebulae, bioluminescent light sources from plants or creatures.",
        "color_palette_mood": "Deep greens, blues, and purples for mystical forests or night scenes; warm golds, oranges, and reds for epic sunsets or volcanic regions; unearthly palettes for alien worlds.",
        "compositional_emphasis": "Creating a sense of immense scale, depth, and wonder, often using atmospheric perspective and strong foreground elements to lead the viewer into the scene."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_fantasy_cityscape_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Fantasy Cityscape Digital Painting Preset",
        "moods": ["Magical", "Ancient", "Grand", "Awe-inspiring", "Mystical"],
        "aspect_ratio": "16:9", # Or other cinematic ratios
        "description": "A grand preset for depicting breathtaking fantasy cityscapes through digital painting, emphasizing magical architecture, unique designs, and ethereal or dramatic lighting."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Fantasy Cityscape Digital Painting / Environment Concept Art", "post_processing": ["Magical glows and atmospheric effects", "painterly textures on architecture", "cinematic color grading", "architectural detail enhancement", "volumetric lighting"], "style_era": "Contemporary Digital"},
        "lighting_settings": {"lighting_type": "Ethereal, Magical, or Dramatic Environmental Lighting (e.g., moonlight, bioluminescent city lights, magical energy sources, dawn/dusk)", "light_quality": "Often soft and glowing for magical elements, contrasted with defined shadows for architectural forms", "light_direction": "Multiple, to highlight scale and complexity; can be from below for floating cities or above for grand vistas"},
        "composition_settings": {"technique": "Wide-angle panoramic, establishing shots, dynamic perspectives (high angle, low angle, aerial) to convey scale and grandeur, leading lines through city structures", "focal_point": "Majestic Central Structure, Sprawling City Vista, or Unique Architectural Feature"},
        "color_settings": {"color_scheme": "Rich Magical, Monochromatic with Accents, or Thematic (e.g., 'City of Brass', 'Crystal Spires')", "palette_type": "Rich purples, deep blues, golds, silvers, emerald greens, often with glowing emissive colors for magical elements or city lights", "color_temperature": "Cool, Warm, or Mixed depending on time of day and magical influences", "color_contrast": "High, to define architectural forms and create dramatic lighting"},
        "detail_settings": {"detail_level": "Very High, showcasing intricate architectural details, textures, and atmospheric elements", "texture_quality": "Detailed textures for stone, crystal, metal, organic structures, magical energy; digital painting brushwork may be visible"},
        "environment_settings": {"weather": "Clear, Mystical Fog, Magical Storms, or Perpetual Twilight", "season": "N/A or fantastical seasons", "location_type": "Floating City in Clouds, City Built into a Colossal Tree/Mountain, Underwater Metropolis, Ancient Sky-Temple Complex, Sprawling Magical Capital on Impossible Terrain", "atmospheric_effects": ["Glowing mist or fog, magical energy fields, auroras, visible spell effects, floating particles, unusual celestial bodies in the sky"]},
        "quality_settings": {"resolution": "4096x2160 (4K) or higher for detailed cityscapes", "rendering_quality": "Ultra High Detail, Cinematic Digital Painting"},
        "negative_prompt": "mundane, realistic modern city, low detail, flat lighting, signature, watermark, low quality, boring architecture, simple structures",
        "style_negative_prompt": "boring or generic architecture, flat or uninspired lighting, lack of scale or wonder, overly cartoony (unless specific style), clashing architectural styles (unintentionally)"
    }
    imagen_settings["fantasy_cityscape_settings"] = {
        "architecture_styles_envisioned": "Varied fantastical architectural styles: e.g., soaring Gothic spires infused with magic, organic Elven structures woven from living wood, crystalline Dwarven underground cities, impossible gravity-defying alien geometries, Art Nouveau-inspired magical towers.",
        "environmental_context_details": "Floating cities amidst swirling clouds, metropolises carved into colossal mountains or trees, underwater domed cities, ancient sky-temples accessible only by flight, sprawling capitals powered by visible magic.",
        "key_magical_elements": "Flying ships or creatures navigating cityscapes, magical energy conduits or protective wards, floating platforms and pathways, visible spell effects or enchantments on buildings, unusual light sources.",
        "time_of_day_and_atmosphere": "Often depicted at twilight, night, or dawn to emphasize magical lights and create a mysterious or grand atmosphere. Can be bustling with activity or eerily ancient and deserted.",
        "sense_of_scale_and_wonder": "Compositions aim to evoke a sense of awe, emphasizing the vastness, complexity, and magical nature of the city.",
        "aesthetic_blend": "Combines imaginative architectural design with painterly digital techniques to create breathtaking and believable (within a fantasy context) urban environments, rich in detail, atmosphere, and a sense of history or magic."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_cyberpunk_action_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Cyberpunk Action Digital Painting Preset",
        "moods": ["Intense", "Chaotic", "Futuristic", "Gritty", "Dynamic"],
        "aspect_ratio": "16:9",
        "description": "An intense preset for dynamic cyberpunk action scenes, captured through digital painting with a focus on high-tech environments, energetic motion, and neon-drenched visuals."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Cyberpunk Action Digital Painting / Scene Illustration", "post_processing": ["Digital glitch effects", "dynamic motion blur", "anamorphic lens flares", "rain/atmospheric particle effects", "cinematic color grading", "bloom on neon lights"], "style_era": "Contemporary Cyberpunk"},
        "lighting_settings": {"lighting_type": "Harsh Neon, Reflective Surfaces, Volumetric Light from screens, advertisements, and vehicle lights", "light_quality": "High contrast, specular highlights on wet surfaces, deep shadows", "light_direction": "Multiple, often from below or side, creating dramatic silhouettes and rim lighting"},
        "composition_settings": {"technique": "Dynamic, cinematic angles (low, high, Dutch tilts), emphasizing speed, impact, and perspective distortion. Strong use of leading lines and diagonals.", "focal_point": "Peak of Action, Character in Motion, or Technological Hazard", "view_mode": "Dynamic action-packed low angle, close-up on action, or wide shot showing chaos", "motion_blur": "High motion blur for fast actions, medium for environmental elements"},
        "color_settings": {"color_scheme": "Neon Contrasting with Dark Muted Tones", "palette_type": "Vibrant neon blues, purples, pinks, cyans, and oranges contrasted with dark, desaturated urban grays, blacks, and metallic sheens. Often features strong color contrasts.", "color_temperature": "Predominantly Cool with pockets of intense Warm light (e.g., explosions, warning lights)", "color_contrast": "Very High"},
        "detail_settings": {"detail_level": "Very High, focusing on cybernetic details, weapon effects, and environmental textures", "texture_quality": "Metallic and wet surfaces, worn concrete, glowing circuitry, holographic displays, detailed character clothing/armor"},
        "environment_settings": {"weather": "Rainy, Smoggy, or Polluted Night", "season": "N/A", "location_type": "Neon-lit City Streets, Grimy Back Alleys, Rooftops of Towering Skyscrapers, Underground Bunkers, Corporate Espionage Settings", "atmospheric_effects": ["Heavy rain with strong reflections", "dense smog or fog, digital noise, light bloom from neon signs, steam from vents, electrical sparks"]},
        "quality_settings": {"resolution": "4096x2160 (4K) or higher for cinematic detail", "rendering_quality": "Ultra High Detail, Gritty Cinematic Digital Painting"},
        "negative_prompt": "calm, peaceful, static, low detail, bright daylight, signature, watermark, low quality, clean utopian, cartoony",
        "style_negative_prompt": "static composition, bland or overly harmonious colors, lack of energy or grit, poorly rendered effects, unconvincing technology"
    }
    imagen_settings["cyberpunk_action_settings"] = {
        "action_sequence_types": "High-speed chases (vehicles or on foot through crowded streets), intense firefights with futuristic weaponry, acrobatic close-quarters combat with cybernetic enhancements, dynamic hacking sequences with visual feedback in the environment.",
        "environmental_interaction": "Rain-slicked neon city streets reflecting chaotic lights, grimy back alleys filled with refuse and steam, high-tech corporate interiors during a breach, crowded markets with panicked civilians.",
        "technological_and_fx_details": "Digital glitch effects on surroundings or characters' vision, flickering or malfunctioning holograms, sparking and damaged cybernetic enhancements, muzzle flashes from energy weapons, energy weapon trails and impacts, explosions with debris.",
        "prevailing_atmosphere": "Intense, chaotic, gritty, futuristic, dystopian, high-energy, dangerous, oppressive, urgent.",
        "motion_and_dynamics": "Emphasis on fast movement blur, digital trail effects from characters or vehicles, dynamic particle effects (rain, sparks, smoke), dramatic camera shakes or impacts (implied)."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_cyberpunk_technology_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Cyberpunk Technology Focus Preset",
        "moods": ["High-Tech", "Complex", "Digital", "Intricate", "Sleek"],
        "aspect_ratio": "16:9", # Or 1:1 for specific device closeups
        "description": "A detailed preset for showcasing cyberpunk technology, intricate interfaces, cybernetic enhancements, and complex digital elements through digital painting or illustration."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Cyberpunk Technology Digital Illustration / Prop Design / UI Concept Art", "post_processing": ["Crisp digital interface rendering", "subtle glitch effects on screens", "holographic projections with depth", "emissive light bloom", "anisotropic reflections on metals"], "style_era": "Contemporary Cyberpunk / Near Future Tech"},
        "lighting_settings": {"lighting_type": "Dominated by screen glows, holographic emissions, internal tech lighting, and subtle ambient occlusion", "light_quality": "Neon highlights, emissive light from LEDs and displays, soft glows from data streams", "light_direction": "Often internal to the tech, or from multiple small sources, creating complex light patterns"},
        "composition_settings": {"technique": "Technical close-up, detailed cutaways, focused still life of technological objects/interfaces, exploded views, or user interaction shots", "focal_point": "Key Interface Element, Cybernetic Implant Detail, Weapon Mechanism, or Data Display"},
        "color_settings": {"color_scheme": "Neon Digital, Monochromatic with Neon Accents, or Dark Metallic with Emissive Highlights", "palette_type": "Neon blues, purples, cyans, pinks, oranges, often contrasted with dark metallic grays, blacks, and silvers. Emissive colors are key.", "color_temperature": "Predominantly Cool, with targeted warm emissives", "color_contrast": "High, especially between emissive elements and dark backgrounds"},
        "detail_settings": {"detail_level": "Extremely High, focusing on intricate details of circuits, wires, materials, and UI elements", "texture_quality": "Clean digital displays, polished or worn metals, carbon fiber, translucent plastics, glowing circuits, complex wiring"},
        "environment_settings": {"weather": "N/A (typically focused on object)", "season": "N/A", "location_type": "High-Tech Laboratory, Hacker's Den, Corporate R&D Facility, Inside a Mech or Vehicle Cockpit, Clean Room, or Abstract Digital Background", "atmospheric_effects": ["Glowing data streams", "subtle digital noise", "lens flares from point lights", "depth of field for focus"]},
        "quality_settings": {"resolution": "4096x2160 (4K) or higher for extreme detail", "rendering_quality": "Ultra High Detail, Crisp and Clean Digital Rendering"},
        "negative_prompt": "organic (unless bio-tech), low detail, blurry, painterly, signature, watermark, low quality, simple or outdated technology",
        "style_negative_prompt": "analog look, simple forms, lack of intricacy, cartoony, hand-drawn (unless a stylistic choice for UI elements)"
    }
    imagen_settings["cyberpunk_tech_settings"] = {
        "specific_technology_examples": "AI core interfaces with complex holographic displays, intricate cybernetic implants (eyes, limbs, neural ports), advanced weaponry with glowing components, futuristic vehicle dashboards, complex data terminals, virtual reality or neural interface rigs.",
        "ui_ux_elements_focus": "Detailed depiction of holographic user interfaces, complex data readouts, glowing iconography, intricate data visualizations, touch panels, neural jack-in points.",
        "materiality_and_finish": "Emphasis on materials like polished chrome, brushed aluminum, carbon fiber, translucent plastics, glowing LED strips, exposed wiring, and complex circuitry. Surfaces can be sleek and new, or worn and modified.",
        "lighting_on_technology": "Internal light sources from screens, LEDs, and energy conduits. Reflections and refractions on glass and metallic surfaces. Subtle bloom around emissive elements.",
        "level_of_complexity": "High level of detail suggesting advanced functionality and intricate design, often with many small parts, wires, and interface elements.",
        "aesthetic_blend": "A detailed and often sleek or gritty portrayal of advanced futuristic technology, focusing on the intricate beauty and complexity of cybernetic enhancements, digital interfaces, and high-tech hardware. Aims to feel both futuristic and believable within its established world."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_game_retro_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Retro Pixel Game Art Preset",
        "moods": ["Nostalgic", "Pixelated", "Retro", "Arcade"],
        "aspect_ratio": "4:3", # Classic CRT ratio
        "description": "A retro preset for pixelated game art emulating 8-bit or 16-bit console aesthetics, focusing on chunky sprites, limited palettes, and classic game views."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Retro Pixel Art / 8-bit & 16-bit Game Graphics", "post_processing": ["Strict pixel grid adherence", "limited color palette enforcement", "CRT screen simulation (scanlines, curvature, phosphor glow - optional)", "dithering for shading"], "style_era": "Retro (1980s-1990s Console/Arcade Era)"},
        "lighting_settings": {"lighting_type": "Flat or Simple Directional (implied by sprite shading)", "light_quality": "Hard-edged, minimal, often just 1-2 levels of shading", "light_direction": "Typically Top-Left or Frontal for sprites"},
        "composition_settings": {"technique": "Side-scrolling, top-down, or fixed isometric view common in retro games. Tile-based environments.", "focal_point": "Player Character Sprite, Key Enemies, or Game Objective", "camera_angle": "Side-scrolling platformer, top-down RPG/shooter, or fixed isometric perspective", "view_mode": "Chunky pixel sprites and tiled backgrounds"},
        "color_settings": {"color_scheme": "Limited 8-bit or 16-bit Palette", "palette_type": "Limited 8-bit (e.g., NES, C64 - often 3-4 colors per sprite) or 16-bit (e.g., SNES, Genesis - more colors but still restricted) color palette, often with dithering for perceived color depth.", "color_temperature": "Neutral or specific to console limitations", "color_contrast": "High, for clarity of sprites against backgrounds"},
        "detail_settings": {"detail_level": "Low (defined by pixel resolution)", "texture_quality": "Pixelated 8-bit or 16-bit style, with dithered shading or flat color blocks. No anti-aliasing."},
        "environment_settings": {"weather": "N/A or simplified pixel representation", "season": "N/A or simplified pixel representation", "location_type": "Pixelated Game Level (e.g., forest, castle, spaceship, abstract)", "atmospheric_effects": ["Scanlines (optional CRT effect)", "palette cycling for simple animations (e.g., water)"]},
        "quality_settings": {"resolution": "Low native resolution (e.g., 256x224, 320x240, 256x192) scaled up with nearest-neighbor for crisp pixels", "rendering_quality": "Crisp Pixelated, True to Retro Hardware Limitations"},
        "negative_prompt": "smooth, realistic, high detail, anti-aliasing, gradients (unless dithered), modern graphics, signature, watermark, high quality (in modern sense), vector art",
        "style_negative_prompt": "blended colors, non-pixelated, high-resolution textures, complex lighting, modern UI elements"
    }
    imagen_settings["game_engine_settings"] = {
        "simulated_engine_type": "Simulated Retro Game Engine / Pixel Art Framework (e.g., PICO-8, Aseprite style).",
        "rendering_characteristics": "Crisp pixelated 8-bit/16-bit style, no anti-aliasing, strict adherence to pixel grid.",
        "sprite_and_tile_animation": "Sprite-based animation (limited frames), tile-based scrolling backgrounds, simple particle effects.",
        "crt_simulation_effects": "Optional CRT filter including scanlines, screen curvature, phosphor glow, and slight color bleeding.",
        "color_palette_management": "Strict limited color palette (e.g., NES, SNES, C64, Amiga, Game Boy) with dithering techniques for creating illusion of more colors or smooth transitions.",
        "resolution_handling": "Low native resolution (e.g., 256x224 for NES-like, 320x240 for SNES-like) scaled up using nearest-neighbor interpolation to preserve sharp pixels."
    }
    imagen_settings["game_settings"] = {
        "target_retro_style": "Platformer, RPG, Shoot 'em up, Arcade-style game, Puzzle game.",
        "emulated_color_depth": "8-bit or 16-bit color depth, with specific console palette limitations if desired.",
        "animation_techniques": "Pixel sprite animation with limited frames, color cycling for environmental effects."
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_game_cel_shaded_template(style_category: str) -> Dict[str, Any]:
    base_template = {
        "preset_name": "Cel-Shaded Game Art Preset",
        "moods": ["Stylized", "Vibrant", "Anime-esque", "Comic Book"],
        "aspect_ratio": "16:9",
        "description": "A stylized preset for cel-shaded (toon-shaded) game art, emphasizing bold ink-like outlines, flat or stepped color shading, and vibrant, often anime-inspired visuals."
    }
    imagen_settings = {
        "style_settings": {"art_movement": "Cel Shading / Toon Shading / Anime-Inspired Game Art", "post_processing": ["Bold ink-like outlines (edge detection)", "stepped color quantization for shading", "stylized highlights and shadows", "optional halftone/crosshatch shading effects", "impact frames/effects"], "style_era": "Contemporary Game Art"},
        "lighting_settings": {"lighting_type": "Soft Stylized or Dynamic Directional", "light_quality": "Toon shading with distinct highlight and shadow bands, minimal blending, hard or soft shadow edges depending on style", "light_direction": "Multiple, often dramatic to emphasize form and action"},
        "composition_settings": {"technique": "Dynamic action camera angles, classic JRPG/anime cinematic framing, strong character poses", "focal_point": "Character actions, expressions, or key environmental elements", "camera_angle": "Dynamic action camera angles (low, high, close-ups), or traditional animation-style framing", "view_mode": "Third-person action, JRPG-style cutscenes, or 2.5D perspectives"},
        "color_settings": {"color_scheme": "Vibrant Saturated, Thematic, or Anime-Inspired", "palette_type": "Vibrant saturated anime-inspired colors, or thematic palettes suitable for comic book/cartoon styles. Often uses bold primary and secondary colors.", "color_temperature": "Neutral, or stylized Warm/Cool based on scene mood", "color_contrast": "High, with clear separation between color bands"},
        "detail_settings": {"detail_level": "Medium to High, with clean lines and distinct color areas", "texture_quality": "Smooth clean edges, flat color fills, or simple stylized textures (e.g., cross-hatching for shadows, subtle fabric patterns). Avoid photorealistic textures."},
        "environment_settings": {"weather": "Stylized (e.g., dramatic rain, cartoony snow)", "season": "N/A or thematically stylized", "location_type": "Anime-style Fantasy World, Sci-Fi Setting, Modern Urban Environment, or Abstract Game Level", "atmospheric_effects": ["Stylized bloom", "speed lines for action", "impact starbursts", "lens flares (stylized)", "particle effects for magic/tech"]},
        "quality_settings": {"resolution": "1920x1080 (1080p) or higher", "rendering_quality": "Crisp Cel Shaded / Toon Rendered, Anti-aliased outlines"},
        "negative_prompt": "realistic shading, photorealism, blurry visuals, high detail photorealistic textures, signature, watermark, low quality, muddy colors, blended shadows",
        "style_negative_prompt": "photorealistic shading, no outlines, overly complex textures, subtle color transitions (unless part of a specific toon shader), realistic lighting"
    }
    imagen_settings["game_engine_settings"] = {
        "simulated_engine_pipeline": "Simulated Cel-Shading/Toon Rendering Pipeline.",
        "shading_model": "Custom cel-shaded/toon shader with configurable outline thickness/color, number of color steps for shadows/highlights, and control over specular highlights.",
        "outline_method": "Edge detection post-process, inverted hull method, or geometry-based outlines.",
        "special_effects_rendering": "Stylized rendering for particle effects (magic, explosions), bloom, speed lines, and impact effects to match the toon aesthetic.",
        "post_processing_stack": "Ink outline effect, stylized bloom, color grading for vibrancy, optional depth-based outlining or fog.",
        "target_resolution_and_aa": "Typically 1080p or higher, with anti-aliasing applied to outlines and geometry for smoothness."
    }
    imagen_settings["game_settings"] = {
        "character_and_animation_style": "Smooth cel animation look, often with exaggerated poses, expressive character designs (anime-inspired, western cartoon, comic book).",
        "lighting_philosophy": "Soft stylized lighting to create clear bands of color for shading, or more dynamic lighting with hard toon shadows for dramatic effect.",
        "overall_aesthetic_goal": "Achieve a look reminiscent of traditional 2D animation, comic books, or stylized anime, with clean lines, vibrant colors, and expressive visuals."
    }
    return {**base_template, "imagen_settings": imagen_settings}
