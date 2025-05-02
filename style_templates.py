"""
Style Templates Module for AI Preset Generator

This module provides style-specific template generation for different art styles
to ensure settings are appropriate for each style category.
"""

from typing import Dict, Any, List, Optional

def get_template_for_category(style_category: str) -> Dict[str, Any]:
    """
    Return the appropriate JSON template based on style category.
    
    Each template includes only the relevant settings for the specific style category.
    For example, camera settings only for photographic styles, digital software settings
    for digital art, etc.
    
    Args:
        style_category (str): The detected style category

    Returns:
        Dict[str, Any]: A JSON template with appropriate fields for the style category
    """
    # Base template with common fields all styles have
    base_template = {
        "preset_name": "[ evocative name ]",
        "moods": ["[ one mood ]"],
        "aspect_ratio": "16:9"
    }
    
    # Common settings for all categories
    imagen_settings = {
        "style_settings": {
            "art_movement": "[ fitting movement ]",
            "post_processing": ["[ 0-1 effect ]"],
            "style_era": "[ appropriate era/period ]"
        },
        "lighting_settings": {
            "lighting_type": "[ appropriate lighting ]",
            "light_quality": "[ description ]",
            "light_direction": "[ direction of main light ]"
        },
        "composition_settings": {
            "technique": "[ composition technique ]",
            "focal_point": "[ main focus of composition ]"
        },
        "color_settings": {
            "color_scheme": "[ fitting scheme ]",
            "palette_type": "[ appropriate type ]",
            "color_temperature": "[ warm/cool/etc ]",
            "color_contrast": "[ high/low/medium ]"
        },
        "detail_settings": {
            "detail_level": "[ high/medium/low ]",
            "texture_quality": "[ realistic/stylized/smooth ]"
        }
    }

    # Initialize style-specific settings based on the category
    if style_category == "photographic" or style_category.startswith("cinematic") or style_category == "realistic":
        # For photographic/cinematic/realistic styles, include camera settings
        imagen_settings["camera_settings"] = {
            "camera_model": "[ appropriate camera model ]",
            "lens_type": "[ fitting lens ]",
            "aperture": "[ f-stop value ]",
            "focal_length": "[ mm value ]",
            "shutter_speed": "[ appropriate speed ]",
            "iso": "[ iso value ]",
            "filter_type": "[ any lens filter ]",
            "depth_of_field": "[ shallow/deep/etc ]"
        }
        imagen_settings["composition_settings"]["camera_angle"] = "[ appropriate angle ]"
        imagen_settings["lighting_settings"]["time_of_day"] = "[ golden hour/blue hour/etc ]"
        imagen_settings["style_settings"]["photo_style"] = "[ documentary/fashion/landscape/etc ]"
        
        # Add additional settings for cinematic specifically
        if style_category.startswith("cinematic"):
            imagen_settings["cinematic_settings"] = {
                "aspect_ratio": "[ cinema ratio: 2.39:1/1.85:1/etc ]",
                "film_grain": "[ amount of grain ]",
                "color_grading": "[ grading style ]",
                "framing": "[ wide/medium/close-up ]",
                "camera_movement": "[ static/tracking/etc ]",
                "film_stock": "[ specific film stock if applicable ]"
            }
            imagen_settings["style_settings"]["film_era"] = "[ classical/modern/new wave/etc ]"

    elif style_category == "digital_art":
        # For digital art, replace camera with digital-specific settings
        imagen_settings["digital_settings"] = {
            "software": "[ appropriate software ]",
            "rendering_technique": "[ technique ]", 
            "digital_effects": ["[ effect ]"],
            "resolution": "[ appropriate resolution ]",
            "filter_usage": ["[ digital filters ]"],
            "brush_type": "[ digital brush style ]",
            "layer_complexity": "[ simple/complex ]"
        }
        # Add viewport settings instead of camera angle
        imagen_settings["composition_settings"]["viewport"] = "[ perspective/isometric/etc ]"
        # Digital art specific lighting
        imagen_settings["lighting_settings"]["lighting_effects"] = ["[ rim lighting/volumetric/etc ]"]

    elif style_category == "minimalist" or style_category == "minimal" or style_category == "geometric" or style_category == "minimalist_geometric":
        # For minimalist and geometric styles including new minimalist_geometric
        imagen_settings["minimalist_settings"] = {
            "simplicity_level": "[ extreme/moderate ]",
            "geometric_elements": ["[ shapes used ]"],
            "negative_space": "[ abundant/limited ]",
            "line_type": "[ clean/rough/etc ]"
        }
        imagen_settings["color_settings"]["color_count"] = "[ very limited number ]"
        imagen_settings["composition_settings"]["balance_type"] = "[ symmetric/asymmetric ]"
        # Remove settings that don't apply to minimalist art
        if "camera_settings" in imagen_settings:
            del imagen_settings["camera_settings"]

    elif style_category == "psychedelic":
        # Psychedelic style settings
        imagen_settings["psychedelic_settings"] = {
            "color_palette": "[ vibrant, neon, contrasting ]",
            "patterns": "[ swirling, fractal, kaleidoscopic ]",
            "visual_effects": "[ glowing, pulsating, morphing ]",
            "mood": "[ trippy, surreal, intense ]"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "[ dynamic, colorful ]"
        imagen_settings["composition_settings"]["technique"] = "[ abstract, flowing ]"

    elif style_category == "surrealism":
        # Surrealism style settings
        imagen_settings["surrealism_settings"] = {
            "conceptual_approach": "[ dreamlike, bizarre, unexpected juxtapositions ]",
            "color_scheme": "[ muted, contrasting, symbolic ]",
            "composition": "[ layered, symbolic, narrative ]",
            "mood": "[ mysterious, uncanny, thought-provoking ]"
        }
        imagen_settings["lighting_settings"]["lighting_type"] = "[ dramatic, chiaroscuro ]"

    elif style_category == "fantasy_landscape":
        # Fantasy landscape style settings
        imagen_settings["fantasy_settings"] = {
            "environment": "[ mystical forests, floating islands, enchanted castles ]",
            "lighting": "[ ethereal, glowing, magical ]",
            "color_palette": "[ rich, vibrant, otherworldly ]",
            "mood": "[ epic, adventurous, mysterious ]",
            "magical_elements": ["glowing runes", "floating crystals", "enchanted flora"],
            "atmospheric_effects": ["mist", "aurora", "magical particles"]
        }
        imagen_settings["composition_settings"]["view_mode"] = "[ panoramic, wide-angle ]"
        imagen_settings["composition_settings"]["perspective"] = "[ grand, dramatic ]"

    elif style_category == "fantasy_portrait":
        # Fantasy portrait style settings
        imagen_settings["fantasy_settings"] = {
            "character_type": ["elf", "dwarf", "dragon", "wizard", "mythical creature"],
            "costuming": ["elaborate", "ancient", "mystical", "regal"],
            "accessories": ["magical staff", "crown", "amulet", "winged helm"],
            "mood": ["majestic", "mysterious", "powerful", "ancient wisdom"],
            "background_elements": ["ancient runes", "magical symbols", "enchanted forest", "castle ruins"]
        }
        imagen_settings["composition_settings"]["view_mode"] = "[ close-up, portrait ]"
        imagen_settings["composition_settings"]["lighting_setup"] = "[ dramatic, chiaroscuro ]"

    elif style_category == "fantasy_battle":
        # Fantasy battle scene settings
        imagen_settings["fantasy_settings"] = {
            "combat_type": ["dragon", "wizard", "knight", "orc", "elf"],
            "environment": ["ancient battlefield", "ruined castle", "enchanted forest"],
            "action_elements": ["magical spells", "sword combat", "dragon fire", "enchanted weapons"],
            "atmosphere": ["chaotic", "epic", "dramatic", "intense"],
            "special_effects": ["explosions", "magical auras", "glowing runes", "enchanted weapons"]
        }
        imagen_settings["composition_settings"]["view_mode"] = "[ dynamic, action-packed ]"
        imagen_settings["composition_settings"]["motion_blur"] = "[ moderate, high ]"

    elif style_category == "fantasy_cityscape":
        # Fantasy cityscape settings
        imagen_settings["fantasy_settings"] = {
            "architecture_style": ["gothic", "medieval", "ancient", "magical"],
            "environment": ["floating city", "underground cavern", "enchanted forest", "magical harbor"],
            "magical_elements": ["flying ships", "magical lights", "enchanted architecture", "floating platforms"],
            "time_of_day": ["twilight", "moonlit", "magical dawn"],
            "atmosphere": ["mysterious", "enchanted", "ancient", "magical"]
        }
        imagen_settings["composition_settings"]["view_mode"] = "[ wide-angle, panoramic ]"
        imagen_settings["lighting_settings"]["light_quality"] = "[ magical, ethereal ]"

    elif style_category == "cyberpunk_cityscape":
        # Cyberpunk cityscape style settings
        imagen_settings["cyberpunk_settings"] = {
            "environment": "[ neon-lit streets, futuristic skyscrapers, rainy nights ]",
            "lighting": "[ neon, reflective, high contrast ]",
            "color_palette": "[ dark, neon, saturated ]",
            "mood": "[ gritty, futuristic, dystopian ]",
            "atmospheric_effects": ["rain", "fog", "neon glow", "digital noise"],
            "architectural_elements": ["skyscrapers", "billboards", "corporate towers", "alleyways"],
            "special_effects": ["digital overlays", "holograms", "glitch effects", "cybernetic elements"]
        }
        imagen_settings["composition_settings"]["view_mode"] = "[ street-level, aerial ]"
        imagen_settings["lighting_settings"]["light_quality"] = "[ harsh, neon, reflective ]"

    elif style_category == "cyberpunk_portrait":
        # Cyberpunk portrait style settings
        imagen_settings["cyberpunk_settings"] = {
            "character_type": ["hacker", "cybernetic", "corporate", "street samurai"],
            "costuming": ["tech-infused", "streetwear", "corporate", "military"],
            "cybernetic_elements": ["cybernetic implants", "digital overlays", "glowing tattoos", "enhanced eyes"],
            "environment": ["urban", "industrial", "corporate", "underground"],
            "mood": ["cold", "dystopian", "rebellious", "mysterious"]
        }
        imagen_settings["composition_settings"]["view_mode"] = "[ close-up, portrait ]"
        imagen_settings["lighting_settings"]["light_quality"] = "[ harsh, neon, digital ]"

    elif style_category == "cyberpunk_action":
        # Cyberpunk action scene settings
        imagen_settings["cyberpunk_settings"] = {
            "action_type": ["combat", "hacking", "chase", "assault"],
            "environment": ["city streets", "corporate tower", "underground", "cybernetic lab"],
            "special_effects": ["digital overlays", "holograms", "glitch effects", "cybernetic enhancements"],
            "atmosphere": ["intense", "chaotic", "futuristic", "dystopian"],
            "motion_elements": ["fast movement", "digital effects", "cybernetic enhancements", "glitch effects"]
        }
        imagen_settings["composition_settings"]["view_mode"] = "[ dynamic, action-packed ]"
        imagen_settings["composition_settings"]["motion_blur"] = "[ high ]"

    elif style_category == "cyberpunk_technology":
        # Cyberpunk technology scene settings
        imagen_settings["cyberpunk_settings"] = {
            "technology_type": ["AI", "cybernetics", "holograms", "quantum computing"],
            "environment": ["lab", "data center", "network", "cybernetic interface"],
            "special_effects": ["digital overlays", "glitch effects", "data streams", "holographic displays"],
            "atmosphere": ["futuristic", "advanced", "complex", "digital"],
            "technical_elements": ["circuitry", "data streams", "holograms", "digital interfaces"]
        }
        imagen_settings["composition_settings"]["view_mode"] = "[ technical, focused ]"
        imagen_settings["lighting_settings"]["light_quality"] = "[ digital, neon, technical ]"

    elif style_category == "game_style":
        # For game styles, use game engine-specific settings
        imagen_settings["game_engine_settings"] = {
            "engine_type": "[ game engine ]",
            "render_quality": "[ quality level ]",
            "special_effects": ["[ effect ]"],
            "shader_type": "[ PBR/stylized/cel ]",
            "post_effects": ["[ bloom/ambient occlusion/etc ]"],
            "resolution": "[ game appropriate resolution ]",
            "physics_settings": ["[ realistic/arcade/etc ]"],
            "animation_style": "[ smooth/stylized/cel-shaded ]"
        }
        imagen_settings["composition_settings"]["camera_angle"] = "[ game camera perspective ]"
        imagen_settings["composition_settings"]["view_mode"] = "[ first-person/third-person/isometric/top-down ]"
        # Add polygonal detail for game styles
        imagen_settings["style_settings"]["poly_detail"] = "[ high/low/stylized ]"
        imagen_settings["style_settings"]["game_genre"] = "[ RPG/FPS/strategy/etc ]"
        imagen_settings["style_settings"]["game_era"] = "[ 8-bit/16-bit/modern/next-gen ]"
        imagen_settings["game_settings"] = {
            "interactivity": ["high/medium/low"],
            "environment_type": ["indoor/outdoor/urban/fantasy"],
            "character_style": ["realistic/stylized/cartoony"],
            "lighting_type": ["dynamic/static/ambient"]
        }

    elif style_category == "game_retro":
        # Retro game style settings
        imagen_settings["game_engine_settings"] = {
            "engine_type": ["retro", "pixel", "8-bit", "16-bit"],
            "render_quality": ["pixelated", "chunky", "chunky pixels"],
            "special_effects": ["sprite-based", "pixel animations", "retro filters"],
            "shader_type": ["pixel", "chunky", "retro"],
            "post_effects": ["CRT", "scanlines", "pixelation"],
            "resolution": ["low", "medium", "chunky"],
            "color_palette": ["limited", "chunky", "retro"]
        }
        imagen_settings["composition_settings"]["camera_angle"] = "[ top-down, side-scrolling ]"
        imagen_settings["composition_settings"]["view_mode"] = "[ chunky pixels, chunky sprites ]"
        imagen_settings["style_settings"]["poly_detail"] = "[ chunky pixels, chunky sprites ]"
        imagen_settings["style_settings"]["game_era"] = "[ 8-bit, 16-bit, chunky pixels ]"
        imagen_settings["game_settings"] = {
            "retro_style": ["arcade", "platformer", "shmup"],
            "color_depth": ["chunky", "chunky pixels", "chunky sprites"],
            "animation_style": ["chunky", "chunky pixels", "chunky sprites"]
        }

    elif style_category == "game_cel_shaded":
        # Cel-shaded game style settings
        imagen_settings["game_engine_settings"] = {
            "engine_type": ["cel-shaded", "toon", "anime"],
            "render_quality": ["smooth", "clean edges", "flat shading"],
            "special_effects": ["ink outlines", "cell animation", "toon shading"],
            "shader_type": ["cel-shaded", "toon", "anime"],
            "post_effects": ["ink outlines", "cell animation", "toon shading"],
            "resolution": ["high", "medium", "chunky"],
            "color_palette": ["vibrant", "chunky", "chunky pixels"]
        }
        imagen_settings["composition_settings"]["camera_angle"] = "[ cinematic, dynamic ]"
        imagen_settings["composition_settings"]["view_mode"] = "[ third-person, cinematic ]"
        imagen_settings["style_settings"]["poly_detail"] = "[ high, chunky pixels ]"
        imagen_settings["style_settings"]["game_genre"] = "[ RPG, action, adventure ]"
        imagen_settings["game_settings"] = {
            "animation_style": ["cell animation", "chunky pixels", "chunky sprites"],
            "lighting_type": ["soft", "chunky pixels", "chunky sprites"],
            "character_style": ["anime", "chunky pixels", "chunky sprites"]
        }

    elif style_category == "traditional_painting_drawing" or style_category in ["oil_painting", "watercolor", "pastel", "charcoal"]:
        # Determine medium based on category name if applicable
        medium = None
        if style_category == "oil_painting":
            medium = "oil paint"
            imagen_settings["medium_settings"] = {
                "painting_medium": "oil paint",
                "canvas_type": ["canvas", "panel", "linen"],
                "brushwork": ["impasto", "glazing", "scumbling", "dry brush"],
                "texture": ["thick", "layered", "smooth", "textured"],
                "layering_technique": ["fat over lean", "glazing", "scumbling", "impasto"],
                "stroke_style": ["visible", "blended", "textured", "layered"],
                "detail_approach": ["high", "medium", "low"]
            }
        elif style_category == "watercolor":
            medium = "watercolor"
            imagen_settings["medium_settings"] = {
                "painting_medium": "watercolor",
                "paper_type": ["cold press", "hot press", "rough"],
                "technique": ["wet-on-wet", "wet-on-dry", "dry brush", "glazing"],
                "texture": ["smooth", "textured", "organic"],
                "layering_technique": ["layered", "washes", "glazing"],
                "stroke_style": ["soft", "blended", "organic", "watery"],
                "detail_approach": ["high", "medium", "low"]
            }
        elif style_category == "pastel":
            medium = "pastel"
            imagen_settings["medium_settings"] = {
                "painting_medium": "pastel",
                "paper_type": ["sanded", "textured", "smooth"],
                "technique": ["layering", "scumbling", "blending"],
                "texture": ["soft", "layered", "textured"],
                "layering_technique": ["layered", "blended", "scumbled"],
                "stroke_style": ["soft", "layered", "textured"],
                "detail_approach": ["high", "medium", "low"]
            }
        elif style_category == "charcoal":
            medium = "charcoal"
            imagen_settings["medium_settings"] = {
                "painting_medium": "charcoal",
                "paper_type": ["smooth", "textured", "newsprint"],
                "technique": ["hatching", "cross-hatching", "smudging"],
                "texture": ["smooth", "textured", "gritty"],
                "layering_technique": ["layered", "hatched", "smudged"],
                "stroke_style": ["sharp", "soft", "textured"],
                "detail_approach": ["high", "medium", "low"]
            }
        
        # Add stylistic choices common in traditional painting
        imagen_settings["style_settings"]["brush_style"] = ["impressionist", "realistic", "expressionist", "abstract"]
        imagen_settings["style_settings"]["painter_influence"] = ["Rembrandt", "Van Gogh", "Monet", "Picasso", "Degas"]
        imagen_settings["style_settings"]["period"] = ["Renaissance", "Baroque", "Impressionist", "Modern", "Contemporary"]
        imagen_settings["style_settings"]["movement"] = ["Realism", "Impressionism", "Expressionism", "Cubism", "Surrealism"]

    elif style_category == "drawing" or style_category in ["pencil_sketch", "ink_drawing", "line_art"]:
        # Drawing specific settings
        drawing_medium = None
        if style_category == "pencil_sketch":
            drawing_medium = "pencil"
        elif style_category == "ink_drawing":
            drawing_medium = "ink"

        imagen_settings["drawing_settings"] = {
            "medium": drawing_medium if drawing_medium else "[ pencil/ink/charcoal/etc ]",
            "paper_type": "[ smooth/textured/etc ]",
            "line_quality": "[ clean/rough/gestural ]",
            "shading_technique": "[ hatching/cross-hatching/etc ]",
            "pressure_variation": "[ uniform/varied ]",
            "detail_level": "[ detailed/suggestive/minimal ]"
        }
        imagen_settings["style_settings"]["drawing_approach"] = "[ realistic/stylized/abstract ]"

    elif style_category.startswith("illustration"):
        # For illustration styles, include illustration-specific settings
        imagen_settings["illustration_settings"] = {
            "line_work": "[ style ]",
            "coloring_technique": "[ technique ]",
            "visual_style": "[ realistic/stylized/cartoony ]",
            "detail_level": "[ detailed/simplified ]",
            "subject_treatment": "[ literal/metaphorical ]"
        }
        if "anime" in style_category or "manga" in style_category:
            # Anime/manga specific
            imagen_settings["illustration_settings"]["manga_style"] = "[ shonen/shojo/seinen/etc ]"
            imagen_settings["illustration_settings"]["manga_era"] = "[ 80s/90s/modern/etc ]"
            imagen_settings["illustration_settings"]["panel_layout"] = "[ single panel/multi-panel ]"
            imagen_settings["style_settings"]["line_weight"] = "[ thin/thick/variable ]"
            
        elif "pixel_art" in style_category or "8-bit" in style_category or "16-bit" in style_category:
            # Pixel art specific
            imagen_settings["pixel_art_settings"] = {
                "resolution": "[ low/medium/high ]",
                "pixel_size": "[ small/large ]",
                "color_palette": "[ limited/extended ]",
                "dithering": "[ none/subtle/heavy ]",
                "art_era": "[ 8-bit/16-bit/32-bit/modern ]"
            }
            # Remove settings that don't apply to pixel art
            if "camera_settings" in imagen_settings:
                del imagen_settings["camera_settings"]
                
        elif "comic" in style_category or "comic_book" in style_category:
            # Comic book specific
            imagen_settings["comic_settings"] = {
                "style_era": "[ golden age/silver age/modern/etc ]",
                "ink_style": "[ clean/gritty ]",
                "panel_layout": "[ single/multi ]",
                "text_elements": "[ speech bubbles/captions/sound effects ]"
            }
            imagen_settings["style_settings"]["publisher_style"] = "[ DC/Marvel/indie ]"
            
        elif "pixar" in style_category or "disney" in style_category:
            # Animation studio specific
            imagen_settings["illustration_settings"]["animation_style"] = "[ studio signature look ]"
            imagen_settings["illustration_settings"]["character_design"] = "[ humanoid/animal/object ]"
            imagen_settings["illustration_settings"]["rendering_style"] = "[ 3D/2D ]"
            imagen_settings["illustration_settings"]["animation_era"] = "[ classic/renaissance/CG era ]"

    elif style_category == "abstract_conceptual" or style_category == "abstract":
        # For abstract art, focus on composition and conceptual elements
        imagen_settings["abstract_settings"] = {
            "visual_elements": ["[ shapes/forms/lines ]"],
            "conceptual_approach": "[ approach ]",
            "balance_type": "[ symmetric/asymmetric/radial ]",
            "movement_type": "[ static/dynamic ]",
            "abstraction_level": "[ partial/complete ]",
            "composition_complexity": "[ simple/complex ]"
        }
        # Enhanced color settings for abstract art
        imagen_settings["color_settings"]["color_interaction"] = "[ contrasting/harmonious ]"
        imagen_settings["color_settings"]["color_emotion"] = "[ expressive/subdued ]"
        
        # Remove techniques that don't apply to abstract art
        if "camera_settings" in imagen_settings:
            del imagen_settings["camera_settings"]

    elif style_category == "material_sculptural" or style_category == "sculpture":
        # For sculptural and material-based styles
        imagen_settings["material_settings"] = {
            "primary_material": "[ material ]",
            "technique": "[ sculpting technique ]",
            "surface_quality": "[ polished/rough/textured ]",
            "form_type": "[ organic/geometric/abstract ]",
            "dimensionality": "[ relief/full-3D ]",
            "scale": "[ intimate/monumental ]",
            "finishing": "[ natural/painted/patina ]"
        }
        # Lighting specifically for showing sculptural forms
        imagen_settings["lighting_settings"]["highlight_shadows"] = "[ dramatic/subtle ]"
        imagen_settings["lighting_settings"]["material_response"] = "[ reflective/matte ]"

    elif style_category.startswith("fantasy") or style_category.startswith("sci_fi"):
        # Fantasy or sci-fi specific settings
        imagen_settings["conceptual_settings"] = {
            "world_building": "[ detailed/suggestive ]",
            "technological_level": "[ primitive/advanced/futuristic ]",
            "reality_distortion": "[ subtle/extreme ]",
            "atmosphere": "[ mysterious/wondrous/ominous ]"
        }

    else:
        # Fallback template for unknown or general styles
        imagen_settings["other_category_settings"] = {
            "notable_features": "[ key features ]",
            "notes": "[ description/notes ]"
        }

    # Add the imagen_settings to the base template
    base_template["imagen_settings"] = imagen_settings

    return base_template
