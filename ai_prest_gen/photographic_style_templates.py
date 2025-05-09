"""Photographic Styles Templates Module for AI Preset Generator

This module provides template generation for all photographic-based styles:
- photographic
- cinematic
- documentary
- street_photography
- noir_photography
- luna_photo
- macro_photography (NEW)
- wildlife_photography (NEW)
- food_photography (NEW)

Each function preserves the distinct template logic for its style, using dynamic camera settings
where appropriate for realism and technical accuracy.
"""

from typing import Dict, Any
from ai_prest_gen.camera_settings import get_dynamic_camera_settings

def get_photographic_template(style_category: str) -> Dict[str, Any]:
    """Generic photographic template with dynamic camera settings."""
    base_template = {
        "preset_name": "General Photographic Preset",
        "moods": ["Authentic", "Realistic", "Well-Composed"],
        "aspect_ratio": "16:9", # Common, but 3:2 is also very standard for photography
        "description": "A versatile preset capturing a scene with the realism, depth, and optical qualities of a well-composed photograph."
    }
    imagen_settings = {
        "style_settings": {
            "art_movement": "General Photography / Realism",
            "post_processing": ["Subtle color grading (e.g., natural film look emulation)", "realistic sensor noise/film grain", "sharpening for clarity", "lens correction (vignetting, distortion)"],
            "style_era": "Contemporary Photography"
        },
        "lighting_settings": {
            "lighting_type": "Natural or Studio Lighting (balanced and well-controlled)",
            "light_quality": "Soft Diffused (e.g., overcast day, softbox) or Directional (e.g., golden hour, studio strobes with modifiers)",
            "light_direction": "Side-Front, Rim Light, Backlight, or as appropriate for subject",
            "time_of_day": "Any (appropriate for subject and desired mood)"
        },
        "composition_settings": {
            "technique": "Rule of Thirds, Leading Lines, Symmetry, Framing, Depth of Field considerations",
            "focal_point": "Main Subject, clearly defined",
            "camera_angle": "Eye-level, Low Angle, High Angle, as appropriate for subject",
            "perspective": "Natural Perspective (matching lens choice, e.g., 35mm, 50mm, 85mm)"
        },
        "color_settings": {
            "color_scheme": "Harmonious, Analogous, or Complementary based on subject",
            "palette_type": "Natural and True-to-life Color Palette, accurate skin tones",
            "color_temperature": "Neutral, Warm, or Cool, appropriate to lighting conditions",
            "color_contrast": "Medium, preserving detail in highlights and shadows",
            "dominant_colors": ["varied based on scene content"]
        },
        "detail_settings": {
            "detail_level": "High, with sharp focus on subject",
            "texture_quality": "Realistic, capturing material properties accurately"
        },
        "environment_settings": {
            "weather": "Varied, appropriate to scene",
            "season": "Varied, appropriate to scene",
            "location_type": "Outdoor, Indoor, Studio",
            "atmospheric_effects": ["Subtle atmospheric perspective", "natural depth of field effects (bokeh)", "lens flare (if appropriate and natural)"]
        },
        "quality_settings": {
            "resolution": "3840x2160 (4K) or higher for print quality",
            "rendering_quality": "High Photographic Quality"
        },
        "negative_prompt": "ugly, tiling, poorly drawn features, out of frame, extra limbs, disfigured, deformed, blurry (unless intentional DoF), bad anatomy, watermark, grainy (unless intentional film grain), signature, text, words, amateur, low quality, cartoon, painting, sketch, drawing, illustration, CGI, unrealistic, abstract, non-photographic elements, harsh flash",
        "style_negative_prompt": "clashing styles, inconsistent lighting, poor composition, unrealistic elements, generic, boring, flat, overly stylized, excessive saturation, unnatural distortion, HDR artifacts, motion blur (unless intentional)",
        "camera_settings": get_dynamic_camera_settings("photographic")
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_cinematic_template(style_category: str) -> Dict[str, Any]:
    """Cinematic style template with dynamic camera settings."""
    base_template = {
        "preset_name": "Cinematic Film Still Preset",
        "moods": ["Dramatic", "Narrative", "Atmospheric", "Tense", "Emotional"],
        "aspect_ratio": "16:9", # Common, or 2.35:1 for widescreen
        "description": "A preset emulating the look and feel of a film still, characterized by dramatic lighting, deliberate color grading (e.g., teal & orange), shallow depth of field, and a strong narrative atmosphere."
    }
    imagen_settings = {
        "style_settings": {
            "art_movement": "Cinematic Storytelling / Film Look",
            "post_processing": [
                "Cinematic color grading (e.g., teal and orange, bleach bypass, film stock emulation)",
                "Shallow depth of field (bokeh)",
                "Film grain (e.g., 16mm, 35mm simulation)",
                "Anamorphic lens flares (simulated)",
                "Letterboxing (optional, e.g., 2.35:1 aspect ratio within 16:9 frame)",
                "Subtle vignette"
            ],
            "style_era": "Modern Film / Classic Cinema (depending on grade)"
        },
        "lighting_settings": {
            "lighting_type": "Dramatic, motivated lighting (e.g., Key, Fill, Rim lights, practical lights)",
            "light_quality": "Often Hard or Controlled Soft light to shape subjects and create mood (e.g., chiaroscuro, Rembrandt lighting)",
            "light_direction": "Side, Backlight, Top, or specific motivated source within the scene",
            "time_of_day": "Late Afternoon (Golden Hour), Night, Twilight, or specific time dictated by narrative"
        },
        "composition_settings": {
            "technique": "Cinematic composition (Rule of Thirds, Golden Ratio, leading lines, framing, negative space, symmetry/asymmetry for effect)",
            "focal_point": "Main Subject (character expression, key object) or narrative element",
            "camera_angle": "Varied cinematic angles (low, high, eye-level, POV, Dutch angle) chosen for narrative impact and emotional tone",
            "perspective": "Two-point or Three-point perspective, often with lens compression or wide-angle distortion for effect"
        },
        "color_settings": {
            "color_scheme": "Complementary (e.g., Teal & Orange), Analogous, Monochromatic with accent, or specific mood-driven palettes",
            "palette_type": "High Contrast, Muted, or Saturated depending on genre and mood. Specific film stock emulation (e.g., Kodak Vision3, Fuji Eterna).",
            "color_temperature": "Mixed, often with distinct warm and cool zones, or overall cool/warm cast for mood",
            "color_contrast": "High, Medium, or Low (e.g., bleach bypass) depending on desired look",
            "dominant_colors": ["Teal and orange (common)", "mood-specific palettes (e.g., cool blues for suspense, warm golds for nostalgia, desaturated for grit)"]
        },
        "detail_settings": {
            "detail_level": "High, with focus on narrative-relevant details",
            "texture_quality": "Realistic, with attention to material properties and surface imperfections that tell a story"
        },
        "environment_settings": {
            "weather": "Clear, Rainy, Foggy, Snowy - chosen for atmosphere",
            "season": "Autumn, Winter, or specific season relevant to story",
            "location_type": "Urban Nightscape, Gritty Interior, Expansive Landscape, Sci-Fi Set, Period Drama Setting",
            "atmospheric_effects": ["Cinematic haze or fog (practical or digital)", "practical smoke/dust motes", "lens breathing (simulated)", "rain streaks, snow fall"]
        },
        "quality_settings": {
            "resolution": "3840x2160 (4K) or higher for cinematic detail",
            "rendering_quality": "High-Fidelity Film Emulation"
        },
        "negative_prompt": "ugly, tiling, poorly drawn features, out of frame, extra limbs, disfigured, deformed, blurry (except DoF), bad anatomy, watermark, signature, text, words, amateur, low quality, cartoon, illustration, painting, sketch, unrealistic rendering, flat tv look, amateur video, overly bright, mundane",
        "style_negative_prompt": "clashing styles, inconsistent lighting, poor composition, unrealistic elements, generic, boring, flat lighting, poor color grading, excessive digital artifacts, excessive noise (unless heavy grain is stylistic), lack of depth, lack of atmosphere, video game look",
        "camera_settings": get_dynamic_camera_settings("cinematic")
    }
    return {**base_template, "imagen_settings": imagen_settings}

def get_documentary_template(style_category: str) -> Dict[str, Any]:
    """Documentary style template with dynamic camera settings."""
    base_template = {
        "preset_name": "Documentary Photography Preset",
        "moods": ["Reportage", "Authentic", "Observational", "Candid"],
        "aspect_ratio": "16:9", # Or 3:2
        "description": "A preset emulating documentary photography, aiming to convey truthful, real-world stories with authentic color, available/natural lighting, and an observational, candid character."
    }
    imagen_settings = {
        "style_settings": {
            "art_movement": "Documentary Photography / Photojournalism",
            "post_processing": ["Minimal, ethical correction (exposure, contrast, white balance)", "true-to-life color rendition", "subtle sharpening if needed for clarity", "respectful cropping if necessary"],
            "style_era": "Contemporary or Classic (e.g., B&W Magnum Photos style)"
        },
        "lighting_settings": {
            "lighting_type": "Available Light (natural or existing artificial sources in the environment)",
            "light_quality": "Often mixed, uncontrolled, reflecting real-world conditions; can be harsh, soft, dim, or bright.",
            "light_direction": "Natural Available, often unpredictable",
            "time_of_day": "Variable, as dictated by the event or situation being documented"
        },
        "composition_settings": {
            "technique": "Candid, observational composition, often capturing decisive moments, environmental portraits, or storytelling scenes. Focus on context and subject interaction.",
            "focal_point": "People, events, social issues, or specific details that tell a larger story",
            "camera_angle": "Reporter’s POV, fly-on-the-wall, eye-level with subject, or unobtrusive perspective",
            "perspective": "Realistic, true-to-life, avoiding dramatic distortions unless inherent to the scene"
        },
        "color_settings": {
            "color_scheme": "Realistic, True-to-Life, or Gritty Monochromatic (B&W)",
            "palette_type": "Natural, often slightly desaturated or gritty depending on subject and mood. Accurate representation of environmental colors.",
            "color_temperature": "Mixed, reflecting actual lighting conditions (can be corrected for neutrality or left for authenticity)",
            "color_contrast": "Low to Medium, aiming for a balanced tonal range that preserves detail",
            "dominant_colors": ["Varied based on real-world scene: e.g., skin tones, environmental colors, urban grays, natural greens/browns"]
        },
        "detail_settings": {
            "detail_level": "Medium to High, sufficient to convey information and context clearly",
            "texture_quality": "Natural, unembellished textures, reflecting the reality of the subject and environment"
        },
        "environment_settings": {
            "weather": "Varies, reflecting actual conditions at the time of capture",
            "season": "Any, as per the documented event/story",
            "location_type": "On Location (real-world environments relevant to the story: streets, homes, conflict zones, workplaces, natural landscapes)",
            "atmospheric_effects": ["Authentic atmospheric conditions (e.g., dust, rain, humidity, smoke if present), not artificially added"]
        },
        "quality_settings": {
            "resolution": "3840x2160 or suitable for publication/exhibition",
            "rendering_quality": "High, Authentic Photographic Quality"
        },
        "negative_prompt": "posed, staged, overly edited, stylized, artificial, glamour lighting, studio setup, signature, watermark, low quality, blurry (unless for specific effect like motion), grainy (unless intentional high ISO look), cartoon, illustration, painting, CGI, unrealistic, abstract",
        "style_negative_prompt": "unrealistic color, excessive contrast/saturation, stylized or artificial lighting, overly shallow depth of field when inappropriate for context, heavy vignetting, HDR look, overly clean or perfected images, misrepresentation of reality"
    }
    imagen_settings["camera_settings"] = get_dynamic_camera_settings("documentary")
    return {**base_template, "imagen_settings": imagen_settings}

def get_street_photography_template(style_category: str) -> Dict[str, Any]:
    """Street photography template with dynamic camera settings."""
    base_template = {
        "preset_name": "Street Photography Preset",
        "moods": ["Candid", "Urban", "Observational", "Spontaneous"],
        "aspect_ratio": "3:2", # Classic for 35mm street photography
        "description": "A preset for capturing candid moments of urban life, emphasizing spontaneous composition, authentic human elements, available ambient light, and often a gritty or evocative atmosphere."
    }
    imagen_settings = {
        "style_settings": {
            "art_movement": "Street Photography (e.g., Henri Cartier-Bresson, Vivian Maier, Garry Winogrand)",
            "post_processing": ["Subtle film grain (e.g., Tri-X, HP5 look for B&W)", "contrast adjustments (classic B&W or gritty color)", "sharpening for street details", "dodging and burning for emphasis"],
            "style_era": "Classic to Contemporary Street Photography"
        },
        "lighting_settings": {
            "lighting_type": "Available Natural or Urban Ambient Light",
            "light_quality": "Ambient, often with strong contrasts from sunlight/shadows, artificial city lights (neon, streetlamps), or window light",
            "light_direction": "Mixed, unpredictable, opportunistic",
            "time_of_day": "Any (Day, Golden Hour, Blue Hour, Night)"
        },
        "composition_settings": {
            "technique": "Candid, decisive moment, juxtaposition, geometric interplay with urban environment, layering, reflections, leading lines",
            "focal_point": "Human subjects, street scenes, fleeting moments, urban details, expressions, interactions",
            "camera_angle": "Eye-level, hip shot, unobtrusive angles to maintain candor, or sometimes slightly low/high for perspective",
            "perspective": "Realistic, often with wide to normal focal lengths (e.g., 28mm, 35mm, 50mm)"
        },
        "color_settings": {
            "color_scheme": "Often Black & White, or Muted/Gritty Natural Colors",
            "palette_type": "Realistic urban palette (grays, browns, concrete, brick), or high-contrast monochrome for B&W. Can include pops of color from signs or clothing.",
            "color_temperature": "Neutral, Cool, or Warm depending on ambient light and desired mood",
            "color_contrast": "Medium to High, especially in B&W for graphic impact",
            "dominant_colors": ["Grey, asphalt, stone, skin tones, urban hues, or monochrome"]
        },
        "detail_settings": {
            "detail_level": "Medium to High, with sharp focus on the subject or key moment",
            "texture_quality": "Sharp focus on subject, capturing textures of the urban environment (concrete, metal, reflections, clothing)"
        },
        "environment_settings": {
            "weather": "Any (sunny, overcast, rainy, snowy), often adding to the mood",
            "season": "Any",
            "location_type": "Urban Outdoors (streets, sidewalks, parks, public transport, markets, alleyways)",
            "atmospheric_effects": ["Urban reflections (puddles, windows)", "steam from vents", "shadow patterns", "available light interplay", "rain or snow textures"]
        },
        "quality_settings": {
            "resolution": "3840x2160 or suitable for print/web",
            "rendering_quality": "High, Authentic Photographic Look"
        },
        "negative_prompt": "staged, posed, unnatural, studio lighting, glamour, painted, illustration, low quality, blurry (unless intentional motion), signature, watermark, cartoon, CGI, unrealistic depth, overly clean",
        "style_negative_prompt": "unrealistic color grading, excessive blurring, artificial studio lighting, posed subjects, lack of spontaneity, overly polished look"
    }
    imagen_settings["camera_settings"] = get_dynamic_camera_settings("street_photography")
    return {**base_template, "imagen_settings": imagen_settings}

def get_noir_photography_template(style_category: str) -> Dict[str, Any]:
    """Noir photography template with dynamic camera settings."""
    base_template = {
        "preset_name": "Film Noir Photography Preset",
        "moods": ["Moody", "Mysterious", "Suspenseful", "Gritty"],
        "aspect_ratio": "4:3", # Classic film aspect ratio, or 16:9 for modern noir
        "description": "A preset inspired by classic film noir photography, characterized by dramatic high-contrast monochrome, moody low-key lighting, and a sense of mystery or suspense."
    }
    imagen_settings = {
        "style_settings": {
            "art_movement": "Film Noir Photography / Cinematic Low-Key Monochrome",
            "post_processing": ["High contrast black and white conversion (deep blacks, bright whites)", "pronounced film grain (e.g., simulating high ISO B&W film)", "deep shadows with lost detail", "selective dodging/burning for emphasis", "subtle vignette", "halation/glow around highlights (optional)"],
            "style_era": "Mid-20th Century (Classic Noir Era, 1940s-1950s) / Neo-Noir (contemporary)"
        },
        "lighting_settings": {
            "lighting_type": "Low-Key Artificial Lighting (e.g., single hard source, practicals like desk lamps, streetlights)",
            "light_quality": "Hard, directional light creating deep, well-defined shadows and stark highlights. Often uses key light with minimal fill.",
            "light_direction": "Side, Top, Backlight (creating silhouettes), or through patterns (e.g., Venetian blinds, gobos)",
            "time_of_day": "Night, or dimly lit interiors suggesting night"
        },
        "composition_settings": {
            "technique": "Chiaroscuro (strong light/dark contrast), strong diagonals, off-kilter (Dutch) angles, use of shadows as active compositional elements, framing within frames, obscured views.",
            "focal_point": "Mysterious Character (often partially obscured), Significant Object (e.g., gun, letter), Shadowy Detail, or Reflective Surface",
            "camera_angle": "Oblique, Low Angle (to create dominance/unease), High Angle (for vulnerability), or through objects (creating voyeuristic feel)",
            "perspective": "Dramatic, often with wide-angle lenses for distorted perspective or telephoto for compressed depth"
        },
        "color_settings": {
            "color_scheme": "Black & White / Greyscale (High Contrast)",
            "palette_type": "Monochrome, rich blacks, bright whites, full range of grays",
            "color_temperature": "N/A (B&W), but implies cool or stark feel",
            "color_contrast": "Very High",
            "dominant_colors": ["black", "white", "deep grays"]
        },
        "detail_settings": {
            "detail_level": "High in focused areas, with large areas lost in shadow",
            "texture_quality": "Pronounced Film Grain, textures of wet streets, period clothing (wool, fedoras), smoke"
        },
        "environment_settings": {
            "weather": "Rainy, Foggy, or Clear Night",
            "season": "Any, often Autumn or Winter implied by clothing",
            "location_type": "Rain-slicked City Night Streets, Dimly Lit Interior (bar, office, hotel room), Foggy Alleyways, Industrial Areas",
            "atmospheric_effects": ["Dense fog or smoke (cigarette smoke, steam)", "deep shadows obscuring details", "streetlight glare on wet pavement", "Venetian blind shadows", "reflections in puddles/windows"]
        },
        "quality_settings": {
            "resolution": "3840x2160 or higher, maintaining grain structure",
            "rendering_quality": "High, Classic Film Emulation"
        },
        "negative_prompt": "colorful, cartoon, staged (unless a specific noir trope), unrealistic, painting, sketch, cgi, signature, watermark, low quality, blurry (except for motion/DoF), flat lighting, evenly lit, daytime",
        "style_negative_prompt": "flat lighting, no shadows, muted contrast, modern digital clarity (unless neo-noir), color, overly bright, cheerful atmosphere"
    }
    imagen_settings["camera_settings"] = get_dynamic_camera_settings("noir_photography")
    return {**base_template, "imagen_settings": imagen_settings}

def get_luna_photo_template(style_category: str) -> Dict[str, Any]:
    """Luna/moon-inspired photo template with dynamic camera settings."""
    base_template = {
        "preset_name": "Lunar Night Photography Preset",
        "moods": ["Ethereal", "Mysterious", "Serene", "Dreamlike", "Nocturnal"],
        "aspect_ratio": "16:9", # Or 3:2, 4:5 for vertical compositions
        "description": "A preset for ethereal moonlit or lunar-themed night photography, emphasizing cool tones, soft glows, atmospheric effects, and often minimalist or surreal compositions."
    }
    imagen_settings = {
        "style_settings": {
            "art_movement": "Nocturne Photography / Lunar Astrophotography / Ethereal Landscape / Surreal Nightscapes",
            "post_processing": ["Cool blue/cyan toning", "dreamy soft glow (halation around moon/highlights)", "subtle vignette", "noise reduction for long exposure look", "star trail effects (optional, if astrophotography focus)", "light painting elements (optional)", "contrast enhancement for lunar surface detail"],
            "style_era": "Modern Digital Photography"
        },
        "lighting_settings": {
            "lighting_type": "Actual or Simulated Moonlight, Starlight, Earthshine (for lunar surface shots)",
            "light_quality": "Soft, diffuse, and often low-intensity light, creating subtle highlights and long shadows. Can be crisp in vacuum (lunar surface).",
            "light_direction": "Top / Side, depending on moon phase and position",
            "time_of_day": "Night (various phases of moon, or deep space)"
        },
        "composition_settings": {
            "technique": "Wide Angle for landscapes, Telephoto for moon close-ups, Minimalist compositions, Negative Space, Silhouettes against moon/sky, Rule of Thirds for moon placement",
            "focal_point": "The Moon itself (full, crescent, eclipse), Silhouetted Landscape/Figure, Celestial Phenomena (stars, nebulae if astrophotography), Reflections of moon on water",
            "camera_angle": "Low Upward (emphasizing sky), Eye-level for landscapes, or Telephoto direct shot for moon details",
            "perspective": "Expansive, Deep Space, or Intimate Nocturne"
        },
        "color_settings": {
            "color_scheme": "Monochromatic Cool, Desaturated Blues, or Near-Monochrome with Subtle Color",
            "palette_type": "Deep blues, indigos, silvers, grays, with white/silver highlights from moon/stars. Lunar surface: grays, browns, whites.",
            "color_temperature": "Cool (blues, cyans)",
            "color_contrast": "Low to Medium for atmospheric scenes, High for crisp moon shots or astrophotography",
            "dominant_colors": ["Midnight blue", "slate grey", "silver", "white", "deep indigo"]
        },
        "detail_settings": {
            "detail_level": "Medium to High, depending on subject (e.g., high for moon surface, softer for dreamy landscapes)",
            "texture_quality": "Smooth for skies/water (long exposure effects), sharp for lunar details or foreground elements in focus. Minimal noise desired."
        },
        "environment_settings": {
            "weather": "Clear (for astrophotography/moon shots), Foggy or Misty (for atmospheric landscapes)",
            "season": "Any, winter can provide clearer skies",
            "location_type": "Remote Outdoors (deserts, mountains, coastlines), Open Fields, Lunar Surface (simulated), Deep Space",
            "atmospheric_effects": ["Moon glow/corona", "mist or low clouds creating diffusion", "star fields (sharp or trailed)", "auroras (if applicable)", "light pillars", "reflections on water"]
        },
        "quality_settings": {
            "resolution": "3840x2160 or higher for detailed night sky/lunar shots",
            "rendering_quality": "High, Low Noise, Sharp where intended"
        },
        "negative_prompt": "harsh daylight, direct sunlight, sun, crowded scenes, high contrast (unless stylistic for moon surface), warm colors, hand-drawn, signature, cartoon, painting, illustration, cgi, low quality, excessive noise, blurry moon (unless atmospheric effect)",
        "style_negative_prompt": "warm tones, harsh direct shadows (not from moon), chaotic compositions, daylight appearance, excessive digital artifacts, overly bright non-lunar light sources"
    }
    imagen_settings["camera_settings"] = get_dynamic_camera_settings("luna_photo")
    return {**base_template, "imagen_settings": imagen_settings}

def get_macro_photography_template(style_category: str) -> Dict[str, Any]:
    """Macro photography template with dynamic camera settings."""
    base_template = {
        "preset_name": "Macro Detail Photography Preset",
        "moods": ["Intricate", "Detailed", "Close-up", "Revealing"],
        "aspect_ratio": "3:2", # Common for dedicated macro shots
        "description": "Extreme close-up photography, revealing intricate details, textures, and patterns unseen by the naked eye. Shallow depth of field is a hallmark."
    }
    imagen_settings = {
        "style_settings": {
            "art_movement": "Macro Photography / Extreme Close-Up",
            "post_processing": ["Detail enhancement", "selective sharpening", "noise reduction"],
            "style_era": "Contemporary Digital Macro"
        },
        "lighting_settings": {
            "lighting_type": "Macro Ring Flash", # Specific example
            "light_quality": "Evenly Diffused",  # Specific example
            "light_direction": "Frontal",        # Specific example
            "time_of_day": "Controlled Studio"   # Specific example
        },
        "composition_settings": {
            "technique": "Extreme Close-Up Isolation", # Specific example
            "focal_point": "Insect Eye Detail",        # Specific example
            "camera_angle": "Perpendicular to Subject", # Specific example
            "perspective": "Magnified 1:1"             # Specific example
        },
        "color_settings": {
            "color_scheme": "Vibrant Natural",          # Specific example
            "palette_type": "Subject-focused True Colors", # Specific example
            "color_temperature": "5500K (Daylight/Flash)", # Specific example
            "color_contrast": "High Detail",             # Specific example
            "dominant_colors": ["Subject-Specific Brights"] # Specific example
        },
        "detail_settings": {
            "detail_level": "Extreme High",
            "texture_quality": "Microscopic Textures"
        },
        "environment_settings": {
            "weather": "Calm",
            "season": "Any",
            "location_type": "Studio or Nature Close-Up",
            "atmospheric_effects": ["Clean Background Bokeh"]
        },
        "quality_settings": {
            "resolution": "6000x4000",
            "rendering_quality": "Maximum Sharpness"
        },
        "negative_prompt": "out of focus subject, motion blur, distracting background, harsh shadows, insufficient detail, signature, watermark, low quality, landscape, portrait",
        "style_negative_prompt": "deep depth of field, lack of sharpness, poor lighting, cluttered composition, unnatural colors"
    }
    imagen_settings["camera_settings"] = get_dynamic_camera_settings("macro")
    return {**base_template, "imagen_settings": imagen_settings}

def get_wildlife_photography_template(style_category: str) -> Dict[str, Any]:
    """Wildlife photography template with dynamic camera settings."""
    base_template = {
        "preset_name": "Wildlife Photography Preset",
        "moods": ["Natural", "Untamed", "Observational", "Majestic", "Candid"],
        "aspect_ratio": "3:2", # Common for wildlife
        "description": "Capturing animals in their natural habitats, often requiring patience, camouflage, and telephoto lenses to document behavior and form."
    }
    imagen_settings = {
        "style_settings": {
            "art_movement": "Wildlife Photography / Nature Photography",
            "post_processing": ["Clarity enhancement", "natural color correction", "noise reduction"],
            "style_era": "Contemporary Digital Wildlife"
        },
        "lighting_settings": {
            "lighting_type": "Golden Hour Sunlight", # Specific example
            "light_quality": "Warm, Soft, Directional",  # Specific example
            "light_direction": "Side-lighting",        # Specific example
            "time_of_day": "Dawn or Dusk"   # Specific example
        },
        "composition_settings": {
            "technique": "Eye-Level Subject Isolation", # Specific example
            "focal_point": "Animal's Eyes",        # Specific example
            "camera_angle": "Eye-Level with Animal", # Specific example
            "perspective": "Telephoto Compression"             # Specific example
        },
        "color_settings": {
            "color_scheme": "Natural Tones",          # Specific example
            "palette_type": "Natural Habitat Colors", # Specific example
            "color_temperature": "Warm Golden", # Specific example
            "color_contrast": "Medium Natural",             # Specific example
            "dominant_colors": ["Browns", "Greens", "Sky Blue"] # Specific example
        },
        "detail_settings": {
            "detail_level": "High",
            "texture_quality": "Realistic Fur/Feathers"
        },
        "environment_settings": {
            "weather": "Clear",
            "season": "Autumn", # Example
            "location_type": "Savannah", # Example
            "atmospheric_effects": ["Morning Mist"]
        },
        "quality_settings": {
            "resolution": "5000x3333",
            "rendering_quality": "Naturalistic Detail"
        },
        "negative_prompt": "cages, fences, human presence, posed animals, unnatural colors, signature, watermark, low quality, blurry, cartoon, painting",
        "style_negative_prompt": "over-processed, excessive saturation, distracting elements, poor focus, artificial lighting"
    }
    imagen_settings["camera_settings"] = get_dynamic_camera_settings("wildlife")
    return {**base_template, "imagen_settings": imagen_settings}

def get_food_photography_template(style_category: str) -> Dict[str, Any]:
    """Food photography template with dynamic camera settings."""
    base_template = {
        "preset_name": "Food Photography Preset",
        "moods": ["Appetizing", "Delicious", "Styled", "Fresh", "Gourmet"],
        "aspect_ratio": "4:5", # Common for social media, also 3:2 or 1:1
        "description": "Artfully capturing food to make it look appealing and delicious, often involving careful styling, lighting, and composition."
    }
    imagen_settings = {
        "style_settings": {
            "art_movement": "Food Photography / Culinary Still Life",
            "post_processing": ["Color enhancement for vibrancy", "selective sharpening", "local contrast adjustments"],
            "style_era": "Contemporary Digital Food Photography"
        },
        "lighting_settings": {
            "lighting_type": "Natural Window Light (Diffused)", # Specific example
            "light_quality": "Soft, Appetizing Glow",  # Specific example
            "light_direction": "Back-Side Lighting",        # Specific example
            "time_of_day": "Daytime"   # Specific example
        },
        "composition_settings": {
            "technique": "Overhead Flat Lay Styling", # Specific example
            "focal_point": "Hero Ingredient or Dish Center",        # Specific example
            "camera_angle": "Top-Down (90-degree)", # Specific example
            "perspective": "Flat Lay Perspective"             # Specific example
        },
        "color_settings": {
            "color_scheme": "Complementary Colors",          # Specific example
            "palette_type": "Vibrant, Fresh Food Colors", # Specific example
            "color_temperature": "Neutral White Balance", # Specific example
            "color_contrast": "High Appetite Appeal",             # Specific example
            "dominant_colors": ["Reds", "Greens", "Yellows"] # Specific example
        },
        "detail_settings": {
            "detail_level": "High",
            "texture_quality": "Crisp Food Textures"
        },
        "environment_settings": {
            "weather": "N/A",
            "season": "Seasonal Ingredients", # Example
            "location_type": "Styled Tabletop", # Example
            "atmospheric_effects": ["Subtle Steam (if hot food)"]
        },
        "quality_settings": {
            "resolution": "4000x5000",
            "rendering_quality": "Crisp & Appetizing"
        },
        "negative_prompt": "unappetizing, messy, poorly lit, dull colors, signature, watermark, low quality, blurry, non-food items distracting",
        "style_negative_prompt": "harsh shadows, blown highlights, unnatural colors, poor styling, distracting props, out-of-focus"
    }
    imagen_settings["camera_settings"] = get_dynamic_camera_settings("food")
    return {**base_template, "imagen_settings": imagen_settings}
