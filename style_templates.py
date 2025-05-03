"""
Style Templates Module for AI Preset Generator

This module provides style-specific template generation for different art styles
to ensure settings are appropriate for each style category.
"""

from typing import Dict, Any, List, Optional, Union


def _priority_category_match(style_category: Union[str, List[str]]) -> str:
    """
    Return the best-matching style category based on a fixed priority list.
    When multiple categories are given, always choose the most specific/relevant one by priority.
    Fallback to first or 'default'.
    """
    priority_list = [
        "pop_surrealism",
        "psychedelic_surrealism",
        "dreamcore_weirdcore",
        "cyberpunk_cityscape",
        "cyberpunk_portrait",
        "fantasy_battle",
        "fantasy_portrait",
        "fantasy_landscape",
        "photorealism_glitch",
        "digital_painting",
        "minimalist_geometric",
        "abstract_expressionism_cubism_fusion",
        # Add other categories as needed
    ]

    # Normalize to a flat list of lowercase strings
    if isinstance(style_category, str):
        categories = [style_category.lower()]
    elif isinstance(style_category, list):
        categories = [str(cat).lower() for cat in style_category]
    else:
        categories = []

    main_category = None
    for pcat in priority_list:
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
    """
    main_category = _priority_category_match(style_category)

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
        },
        "environment_settings": {
            "weather": "[ current weather ]",
            "season": "[ current season ]",
            "location_type": "[ indoor/outdoor/etc ]",
            "atmospheric_effects": ["[ fog/rain/etc ]"]
        },
        "quality_settings": {
            "resolution": "[ target resolution e.g., 3840x2160 ]",
            "rendering_quality": "[ high/photorealistic/etc ]"
        },
        "negative_prompt": "[GENERATE_NEGATIVE_PROMPT_BASED_ON_STYLE]"
    }

    # -- Mixed/Hybrid Art Templates (creative blended settings) --
    if main_category == "kinetic_ascii":
        imagen_settings["kinetic_ascii_settings"] = {
            "motion_type": "[ animated/looped/text-based ]",
            "character_set": "[ ASCII/Unicode block/line ]",
            "visual_flow": "[ left-to-right/top-down/randomized ]",
            "energy_motif": "[ pulsing, blinking, flowing symbols ]",
            "articulation": "[ frame-based/continuous ]",
            "aesthetic_blend": "Kinetic movement visualized via ASCII symbols, pulsing text animating across grid; retro-tech/cyber fusion."
        }
        imagen_settings["composition_settings"]["technique"] = "[ ASCII kinetic motion grid ]"
        imagen_settings["color_settings"]["palette_type"] = "[ monochrome/neon ]"

    elif main_category == "watercolor_pencil":
        imagen_settings["watercolor_pencil_settings"] = {
            "layering_effect": "[ watercolor washes underlying sharp pencil ]",
            "stroke_quality": "[ loose pigment, fine overlay sketch ]",
            "blend_level": "[ soft <= watercolor; detail <= pencil ]",
            "paper_type": "[ textured/medium grain ]",
            "aesthetic_blend": "Painterly fluidity with crisp pencil edges; dreamy backgrounds with focused main objects."
        }
        imagen_settings["composition_settings"]["technique"] = "[ wash-and-sketch ]"
        imagen_settings["color_settings"]["color_interaction"] = "[ soft paint and linear grayscale ]"

    elif main_category == "hybrid_traditional_digital":
        imagen_settings["hybrid_traditional_digital_settings"] = {
            "media_fusion": "[ traditional painting, digital enhancement, mixed media ]",
            "techniques": "[ layering, digital brushwork, collage ]",
            "color_palette": "[ natural tones with digital vibrancy ]",
            "aesthetic_blend": "Seamless fusion of traditional and digital art techniques creating rich textures and depth."
        }
        imagen_settings["composition_settings"]["technique"] = "[ mixed media layering ]"
        imagen_settings["color_settings"]["palette_type"] = "[ natural, enhanced ]"

    elif main_category == "installation_art":
        imagen_settings["installation_art_settings"] = {
            "media": "[ mixed media, found objects, spatial elements ]",
            "scale": "[ large, immersive ]",
            "interaction": "[ physical, digital, participatory ]",
            "aesthetic_blend": "Spatial and immersive art combining physical materials with digital projections and interactivity."
        }
        imagen_settings["composition_settings"]["view_mode"] = "[ immersive, 3D space ]"
        imagen_settings["lighting_settings"]["lighting_type"] = "[ dynamic, projection-based ]"

    elif main_category == "scientific_technological_hybrid":
        imagen_settings["scientific_technological_hybrid_settings"] = {
            "media": "[ photography, film, digital media, scientific visualization ]",
            "concept": "[ data-driven, algorithmic, experimental ]",
            "technology": "[ AI, AR, VR, interactive software ]",
            "aesthetic_blend": "Artistic expression integrating scientific data and cutting-edge technology."
        }
        imagen_settings["composition_settings"]["technique"] = "[ algorithmic composition ]"
        imagen_settings["color_settings"]["palette_type"] = "[ high contrast, data-inspired ]"

    elif main_category == "augmented_reality_art":
        imagen_settings["augmented_reality_art_settings"] = {
            "media": "[ 3D modeling, digital overlays, physical space ]",
            "interaction": "[ user-driven, immersive ]",
            "technology": "[ AR devices, sensors, real-time rendering ]",
            "aesthetic_blend": "Blending virtual and physical realities through interactive digital art."
        }
        imagen_settings["composition_settings"]["view_mode"] = "[ mixed reality, interactive ]"
        imagen_settings["lighting_settings"]["lighting_type"] = "[ dynamic, real-time ]"

    elif main_category == "abstract_expressionism_cubism_fusion":
        imagen_settings["abstract_expressionism_cubism_fusion_settings"] = {
            "form_style": "[ gestural brushwork, fragmented geometry ]",
            "color_palette": "[ bold, contrasting, emotive ]",
            "composition": "[ layered, dynamic, abstract ]",
            "aesthetic_blend": "Fusion of abstract expressionism's emotion with cubism's structure."
        }
        imagen_settings["composition_settings"]["technique"] = "[ expressive abstraction with geometric fragmentation ]"
        imagen_settings["color_settings"]["palette_type"] = "[ bold, emotive ]"

    elif main_category == "collage_digital_overlay":
        imagen_settings["collage_digital_overlay_settings"] = {
            "media": "[ paper collage, digital textures, photo manipulation ]",
            "texture": "[ layered, tactile, digital enhancements ]",
            "color_palette": "[ eclectic, vibrant ]",
            "aesthetic_blend": "Combining tactile collage with digital overlays for rich visual narratives."
        }
        imagen_settings["composition_settings"]["technique"] = "[ mixed media collage with digital effects ]"
        imagen_settings["color_settings"]["palette_type"] = "[ vibrant, eclectic ]"

    elif main_category == "experimental_mixed_media":
        imagen_settings["experimental_mixed_media_settings"] = {
            "media": "[ unconventional materials, digital manipulation ]",
            "techniques": "[ layering, deconstruction, reassembly ]",
            "concept": "[ avant-garde, boundary-pushing ]",
            "aesthetic_blend": "Innovative combinations of materials and digital techniques challenging traditional art."
        }
        imagen_settings["composition_settings"]["mood"] = "[ experimental, avant-garde ]"
        imagen_settings["color_settings"]["palette_type"] = "[ varied, unpredictable ]"


    elif main_category == "patchwork_collage":
        imagen_settings["patchwork_collage_settings"] = {
            "material_mix": "[ fabric, paper, metal, wood ]",
            "assembly_style": "[ layered, stitched, glued ]",
            "texture_emphasis": "[ tactile, rough, varied ]",
            "color_palette": "[ bold, contrasting, folk-inspired ]",
            "aesthetic_blend": "Bold textures and patterns combined into cohesive compositions; folk and craft influences."
        }
        imagen_settings["composition_settings"]["technique"] = "[ collage assembly ]"
        imagen_settings["color_settings"]["palette_type"] = "[ vibrant, earthy ]"

    elif main_category == "paper_quilling":
        imagen_settings["paper_quilling_settings"] = {
            "coil_types": "[ tight, loose, shaped ]",
            "paper_strip_width": "[ narrow, medium, wide ]",
            "pattern_density": "[ sparse, dense ]",
            "color_scheme": "[ pastel, bright, monochrome ]",
            "aesthetic_blend": "Intricate rolled paper shapes forming delicate, decorative patterns."
        }
        imagen_settings["composition_settings"]["depth"] = "[ layered, dimensional ]"
        imagen_settings["color_settings"]["palette_type"] = "[ soft, bright ]"

    elif main_category == "tradigital_mixed_media":
        imagen_settings["tradigital_mixed_media_settings"] = {
            "media_fusion": "[ traditional painting + digital enhancement ]",
            "texture_blend": "[ brush strokes + digital overlays ]",
            "color_interaction": "[ natural + enhanced ]",
            "aesthetic_blend": "Seamless integration of traditional and digital techniques for rich textures."
        }
        imagen_settings["composition_settings"]["technique"] = "[ mixed media layering ]"
        imagen_settings["color_settings"]["palette_type"] = "[ natural, enhanced ]"

    elif main_category == "whimsical_mixed_media":
        imagen_settings["whimsical_mixed_media_settings"] = {
            "motifs": "[ mythical creatures, soft colors, playful elements ]",
            "texture": "[ light, airy, layered ]",
            "color_palette": "[ pastel, dreamy ]",
            "aesthetic_blend": "Lighthearted, dreamy compositions with fantasy and playful accents."
        }
        imagen_settings["composition_settings"]["mood"] = "[ playful, dreamy ]"
        imagen_settings["color_settings"]["palette_type"] = "[ pastel, soft ]"

    elif main_category == "sci_fi_futuristic":
        imagen_settings["sci_fi_futuristic_settings"] = {
            "technology_level": "[ advanced, cybernetic, space-age ]",
            "environment": "[ futuristic cities, space stations ]",
            "lighting": "[ neon, holographic, cold ]",
            "color_palette": "[ metallic, neon, dark ]",
            "aesthetic_blend": "Futuristic and cyberpunk elements with high-tech visuals."
        }
        imagen_settings["composition_settings"]["view_mode"] = "[ panoramic, dynamic ]"
        imagen_settings["lighting_settings"]["lighting_type"] = "[ neon, artificial ]"

    elif main_category == "mediterranean_style":
        imagen_settings["mediterranean_style_settings"] = {
            "environment": "[ sunny coastal scenes, vibrant landscapes ]",
            "color_palette": "[ warm, bright, natural ]",
            "lighting": "[ natural sunlight, warm glow ]",
            "aesthetic_blend": "Vivid, colorful depictions of Mediterranean life and scenery."
        }
        imagen_settings["composition_settings"]["mood"] = "[ lively, warm ]"
        imagen_settings["color_settings"]["palette_type"] = "[ warm, bright ]"

    elif main_category == "morphism_surreal":
        imagen_settings["morphism_surreal_settings"] = {
            "transformation_style": "[ surreal, fluid, fantastical ]",
            "color_palette": "[ vibrant, dreamlike ]",
            "composition": "[ morphing shapes, illogical progressions ]",
            "aesthetic_blend": "Surreal transformations with fantastical and dreamlike qualities."
        }
        imagen_settings["composition_settings"]["technique"] = "[ surreal morphing ]"
        imagen_settings["color_settings"]["palette_type"] = "[ vibrant, surreal ]"

    elif main_category == "cubism_mixed":
        imagen_settings["cubism_mixed_settings"] = {
            "form_style": "[ angular, fragmented, multiple perspectives ]",
            "color_palette": "[ muted, earthy, bold accents ]",
            "composition": "[ geometric abstraction, layered planes ]",
            "aesthetic_blend": "Cubist style with mixed media and modern influences."
        }
        imagen_settings["composition_settings"]["technique"] = "[ cubist fragmentation ]"
        imagen_settings["color_settings"]["palette_type"] = "[ muted, earthy ]"

    elif main_category == "pixel_patchwork":
        imagen_settings["pixel_patchwork_settings"] = {
            "pixel_style": "[ pixel art, voxel art, low poly ]",
            "color_palette": "[ limited, vibrant ]",
            "texture": "[ blocky, geometric ]",
            "aesthetic_blend": "Pixelated and geometric patchwork style combining digital and traditional motifs."
        }
        imagen_settings["composition_settings"]["view_mode"] = "[ isometric, grid-based ]"
        imagen_settings["color_settings"]["palette_type"] = "[ limited, vibrant ]"

    elif main_category == "phygital_hybrid":
        imagen_settings["phygital_hybrid_settings"] = {
            "media_fusion": "[ physical and digital art combined ]",
            "technology": "[ AR, 3D printing, mixed reality ]",
            "aesthetic_blend": "Hybrid physical/digital artworks blending real and virtual elements."
        }
        imagen_settings["composition_settings"]["technique"] = "[ hybrid layering ]"
        imagen_settings["color_settings"]["palette_type"] = "[ varied ]"

    elif main_category == "screen_printing_bold":
        imagen_settings["screen_printing_bold_settings"] = {
            "print_style": "[ bold, graphic, tactile ]",
            "color_palette": "[ limited, high contrast ]",
            "texture": "[ flat, layered ]",
            "aesthetic_blend": "Bold graphic prints with tactile qualities and strong contrasts."
        }
        imagen_settings["composition_settings"]["technique"] = "[ screen printing ]"
        imagen_settings["color_settings"]["palette_type"] = "[ limited, high contrast ]"

    elif main_category == "mixed_media_journaling":
        imagen_settings["mixed_media_journaling_settings"] = {
            "media": "[ collage, sketch, paint, stamps ]",
            "texture": "[ layered, varied ]",
            "color_palette": "[ eclectic, varied ]",
            "aesthetic_blend": "Eclectic, layered mixed media with personal and whimsical elements."
        }
        imagen_settings["composition_settings"]["mood"] = "[ personal, whimsical ]"
        imagen_settings["color_settings"]["palette_type"] = "[ varied ]"

    elif main_category == "digital_pixel_traditional":
        imagen_settings["digital_pixel_traditional_settings"] = {
            "media_fusion": "[ digital pixel art combined with traditional painting ]",
            "color_palette": "[ vibrant, mixed ]",
            "texture": "[ pixelated and painterly ]",
            "aesthetic_blend": "Fusion of pixel art and traditional painting techniques."
        }
        imagen_settings["composition_settings"]["technique"] = "[ hybrid media ]"
        imagen_settings["color_settings"]["palette_type"] = "[ vibrant, mixed ]"

    elif main_category == "patchwork_fabric":
        imagen_settings["patchwork_fabric_settings"] = {
            "material": "[ fabric, textile ]",
            "assembly": "[ sewn, layered ]",
            "texture": "[ soft, tactile ]",
            "color_palette": "[ warm, earthy ]",
            "aesthetic_blend": "Textile patchwork with warm, tactile qualities."
        }
        imagen_settings["composition_settings"]["technique"] = "[ fabric layering ]"
        imagen_settings["color_settings"]["palette_type"] = "[ warm, earthy ]"

    elif main_category == "mixed_media_collage":
        imagen_settings["mixed_media_collage_settings"] = {
            "media": "[ paper, paint, found objects ]",
            "texture": "[ layered, tactile ]",
            "color_palette": "[ varied, eclectic ]",
            "aesthetic_blend": "Eclectic collage combining diverse media and textures."
        }
        imagen_settings["composition_settings"]["technique"] = "[ collage assembly ]"
        imagen_settings["color_settings"]["palette_type"] = "[ varied ]"

    elif main_category == "whimsical_fantasy":
        imagen_settings["whimsical_fantasy_settings"] = {
            "motifs": "[ fantasy creatures, pastel colors, dreamy ]",
            "texture": "[ soft, layered ]",
            "color_palette": "[ pastel, soft ]",
            "aesthetic_blend": "Dreamy fantasy with playful and soft whimsical elements."
        }
        imagen_settings["composition_settings"]["mood"] = "[ dreamy, playful ]"
        imagen_settings["color_settings"]["palette_type"] = "[ pastel, soft ]"

    elif main_category == "cubism_futurism":
        imagen_settings["cubism_futurism_settings"] = {
            "form_style": "[ angular, geometric, dynamic ]",
            "color_palette": "[ muted, metallic ]",
            "composition": "[ layered, fragmented ]",
            "aesthetic_blend": "Fusion of cubist and futurist styles with dynamic geometry."
        }
        imagen_settings["composition_settings"]["technique"] = "[ cubist futurism ]"
        imagen_settings["color_settings"]["palette_type"] = "[ muted, metallic ]"

    elif main_category == "digital_traditional_fusion":
        imagen_settings["digital_traditional_fusion_settings"] = {
            "media_fusion": "[ digital and traditional art combined ]",
            "texture": "[ layered, mixed ]",
            "color_palette": "[ varied, rich ]",
            "aesthetic_blend": "Rich fusion of digital and traditional artistic techniques."
        }
        imagen_settings["composition_settings"]["technique"] = "[ hybrid media ]"
        imagen_settings["color_settings"]["palette_type"] = "[ varied ]"

    elif main_category == "retro_pixel_vaporwave":
        imagen_settings["retro_pixel_vaporwave_settings"] = {
            "style": "[ retro pixel art with vaporwave aesthetics ]",
            "color_palette": "[ neon, pastel, vibrant ]",
            "texture": "[ pixelated, glitch ]",
            "aesthetic_blend": "Retro pixel art infused with vaporwave neon and glitch effects."
        }
        imagen_settings["composition_settings"]["mood"] = "[ nostalgic, vibrant ]"
        imagen_settings["color_settings"]["palette_type"] = "[ neon, pastel ]"

    elif main_category == "psychedelic_surrealism":
        imagen_settings["psychedelic_surrealism_settings"] = {
            "motifs": "[ trippy, surreal, dreamlike ]",
            "color_palette": "[ vibrant, neon, contrasting ]",
            "visual_effects": "[ glowing, morphing, fractal ]",
            "aesthetic_blend": "Intense psychedelic visuals combined with surreal dreamscapes."
        }
        imagen_settings["composition_settings"]["technique"] = "[ psychedelic surrealism ]"
        imagen_settings["color_settings"]["palette_type"] = "[ vibrant, neon ]"

    elif style_category == "digital_painting":
        imagen_settings["digital_painting_settings"] = {
            "platform": "[ Procreate/Photoshop/Krita/custom ]",
            "brushwork": "[ simulated paint, digital smudge, opacity layering ]",
            "effect_blend": "[ overlays, filters, noise ]",
            "aesthetic_blend": "Traditional painting strokes digitally composited with effects and masks."
        }
        imagen_settings["lighting_settings"]["lighting_effects"] = "[ digital glow, painted shadows ]"

    elif style_category == "photorealism_glitch":
        imagen_settings["photorealism_glitch_settings"] = {
            "base_quality": "[ high-detail, high-contrast ]",
            "distortion_techniques": "[ RGB shift, scanline, datamosh ]",
            "fracture_level": "[ subtle/random/intense ]",
            "aesthetic_blend": "Hyperreal imagery corrupted with digital noise, fragment overlays."
        }
        imagen_settings["detail_settings"]["texture_quality"] = "[ glitch surface ]"
        imagen_settings["post_processing"] = {
            "effects": ["[ VHS artifact, color tear ]"]
        }

    elif style_category == "anime_oilpainting":
        imagen_settings["anime_oilpainting_settings"] = {
            "character_design": "[ large-eyed/shoujo, painterly highlights ]",
            "canvas_type": "[ linen/canvas texture ]",
            "lighting": "[ soft rim/oil brush glaze ]",
            "stroke_emphasis": "[ visible impasto, cell shading blend ]",
            "aesthetic_blend": "Anime forms with lush oil-paint volume and brushwork."
        }
        imagen_settings["color_settings"]["palette_type"] = "[ pastel + vivid ]"

    elif style_category == "minimalist_geometric":
        imagen_settings["minimalist_geometric_settings"] = {
            "geometry_focus": "[ circles/triangles/squares ]",
            "simplicity": "[ 3 or fewer shapes/limited lines ]",
            "style": "[ flat-projection, low noise, pastel palette ]",
            "aesthetic_blend": "Extreme geometric abstraction with negative space and proportional rhythm."
        }

    elif style_category == "pop_surrealism_ascii":
        imagen_settings["pop_surrealism_ascii_settings"] = {
            "icon_motif": "[ pop icon, cartoon, ASCII overlay ]",
            "visual_irony": "[ strange objects/characters with ASCII outlining ]",
            "pattern_density": "[ sparse/dense ]",
            "aesthetic_blend": "Cartoonish subjects re-rendered as digital character mosaics, bizarre and playful."
        }

    elif style_category == "dreamcore_weirdcore":
        imagen_settings["dreamcore_weirdcore_settings"] = {
            "atmosphere": "[ foggy, uncanny, low-sat color, liminal spaces ]",
            "distortion": "[ scan error, smudge, trailing effect ]",
            "motif": "[ ambiguous objects, portals, surreal geometry ]",
            "aesthetic_blend": "Blends nostalgic dreaminess with unsettling strange objects/highlights; ambiguous scenes."
        }
        imagen_settings["color_settings"]["color_scheme"] = "[ pale neon, desaturated ]"

    # Initialize style-specific settings based on the category
    if style_category == "3d_render":
        # For 3D/CGI/Rendered/Modeled art, provide full 3D-specific settings
        imagen_settings["software_settings"] = {
            "suite": "[ Blender/Maya/Cinema4D/3dsMax ]",
            "renderer": "[ Octane/Arnold/Cycles/Eevee ]",
            "version": "[ software version ]"
        }
        imagen_settings["render_settings"] = {
            "polycount": "[ high/medium/low ]",
            "sampling": "[ samples ]",
            "denoiser": "[ enabled/disabled ]",
            "resolution": "[ 1920x1080/4K/etc ]",
            "aspect_ratio": "[ 16:9/21:9/square ]",
            "frame_number": "[ if animated ]"
        }
        imagen_settings["lighting_setup"] = {
            "system": "[ HDRI/3-point/area lights ]",
            "intensity": "[ value ]",
            "color": "[ value ]",
            "shadows": "[ soft/hard ]"
        }
        imagen_settings["material_settings"] = {
            "shader_type": "[ PBR/toon/glossy ]",
            "subsurface_scattering": "[ value ]",
            "texture_maps": ["[ diffuse/normal/specular/etc ]"],
            "bump_map": "[ yes/no ]",
            "displacement": "[ yes/no ]"
        }
        imagen_settings["camera_settings"] = {
            "camera_type": "[ perspective/orthographic ]",
            "focal_length": "[ mm value ]",
            "depth_of_field": "[ enabled/disabled ]",
            "focus_distance": "[ value ]",
            "camera_position": "[ XYZ or relative ]"
        }
        imagen_settings["composition_settings"]["view_mode"] = "[ isometric/3rd person/1st person/freecam ]"
        imagen_settings["post_processing"] = {
            "effects": ["[ bloom/vignette/glare/lens flare ]"],
            "color_grading": "[ LUT/none/custom ]",
            "motion_blur": "[ enabled/disabled ]"
        }

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
    elif main_category == "photographic" or (isinstance(main_category, str) and main_category.startswith("cinematic")) or main_category == "realistic":
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
    elif style_category == "digital_art":
        # Enhanced digital art template with more unique settings
        imagen_settings["digital_settings"] = {
            "software": "[ Photoshop, Procreate, Krita, Clip Studio Paint ]",
            "rendering_technique": "[ digital painting, vector art, mixed media ]",
            "digital_effects": ["glow", "blur", "texture overlays", "layer masks"],
            "resolution": "4K or higher",
            "filter_usage": ["Gaussian blur", "color dodge", "noise"],
            "brush_type": "[ custom textured brushes, soft round, hard edge ]",
            "layer_complexity": "complex with multiple adjustment layers"
        }
        imagen_settings["composition_settings"]["viewport"] = "[ perspective, isometric, dynamic ]"
        imagen_settings["lighting_settings"]["lighting_effects"] = ["rim lighting", "volumetric light", "soft shadows"]
        imagen_settings["style_settings"]["art_movement"] = "Contemporary Digital Art"
        imagen_settings["style_settings"]["post_processing"] = ["0.7"]
        imagen_settings["style_settings"]["style_era"] = "Modern Digital Era"
        imagen_settings["color_settings"]["color_scheme"] = "Analogous with vibrant accents"
        imagen_settings["detail_settings"]["detail_level"] = "High"
        imagen_settings["detail_settings"]["texture_quality"] = "Stylized with digital brush textures"
        imagen_settings["environment_settings"]["location_type"] = "Digital studio or fantasy environment"
        imagen_settings["quality_settings"]["rendering_quality"] = "High"
        imagen_settings["negative_prompt"] = "pixelated, low resolution, blurry, poorly drawn, amateurish"

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
        # Enhanced fantasy battle scene settings with more unique details
        imagen_settings["fantasy_settings"] = {
            "combat_type": ["dragon rider", "arcane wizard", "armored knight", "orc warlord", "elven archer"],
            "environment": ["ancient battlefield with ruins", "enchanted forest clearing", "stormy mountain pass"],
            "action_elements": ["magical fireballs", "clashing swords", "dragon breath", "enchanted armor glow"],
            "atmosphere": ["chaotic, epic, intense, dramatic"],
            "special_effects": ["explosions, magical auras, glowing runes, enchanted weapons"],
            "lighting": ["dramatic chiaroscuro", "backlit silhouettes", "dynamic shadows"],
            "color_palette": ["rich saturated reds, blues, and golds"],
            "composition": ["dynamic angles, motion blur, focus on central combatants"]
        }
        imagen_settings["composition_settings"]["view_mode"] = "[ dynamic, action-packed ]"
        imagen_settings["composition_settings"]["motion_blur"] = "[ moderate, high ]"
        imagen_settings["lighting_settings"]["lighting_type"] = "[ dramatic, high contrast ]"
        imagen_settings["color_settings"]["palette_type"] = "[ rich, saturated ]"
        imagen_settings["detail_settings"]["detail_level"] = "Very High"
        imagen_settings["environment_settings"]["weather"] = "Stormy with magical effects"
        imagen_settings["quality_settings"]["rendering_quality"] = "Ultra High"
        imagen_settings["negative_prompt"] = "cartoonish, simplistic, blurry, low detail, flat lighting"


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

    elif style_category == "papercraft":
        imagen_settings["papercraft_settings"] = {
            "layering_technique": "[ stacked/cut/rolled ]",
            "paper_type": "[ construction/cardstock/tissue ]",
            "edge_quality": "[ sharp/rounded/deckled ]",
            "construction_method": "[ glued/slot/folding ]",
            "motif": "[ organic/geometric/abstract ]"
        }
        imagen_settings["composition_settings"]["depth"] = "[ low/medium/high ]"
        imagen_settings["texture_quality"] = "[ crisp paper/fibrous ]"

    elif style_category == "luna_photo":
        imagen_settings["luna_photo_settings"] = {
            "exposure_method": "[ double exposure/masking ]",
            "photographic_style": "[ ethereal/surreal ]",
            "subject_interaction": "[ blending/superimpose/separate ]",
            "light_quality": "[ diffuse/moonlit/glowing ]"
        }

    elif style_category == "pop_surrealism":
        imagen_settings["pop_surrealism_settings"] = {
            "motif": "[ cartoon/lowbrow/pop icons ]",
            "juxtaposition": "[ playful/subversive ]",
            "narrative_element": "[ overt/hidden ]",
            "color_palette": "[ saturated/vivid/unexpected ]"
        }

    elif style_category == "synesthesia_art":
        imagen_settings["synesthesia_settings"] = {
            "sensation_pairings": "[ color-sound/shape-taste ]",
            "expression_style": "[ blended/disjointed ]",
            "motif": "[ waves/flares/overlaps ]",
            "dynamic_emphasis": "[ motion/static ]"
        }

    elif style_category == "weirdcore":
        imagen_settings["weirdcore_settings"] = {
            "motif": "[ nostalgic/liminal/dreamlike ]",
            "distortion_type": "[ visual/glitch ]",
            "color_scheme": "[ muted/neon ]",
            "visual_emphasis": "[ surreal/uncanny/comforting ]"
        }

    elif style_category == "dreamcore":
        imagen_settings["dreamcore_settings"] = {
            "atmosphere": "[ foggy/diffuse/light beams ]",
            "motif": "[ ethereal/spacey/lost places ]",
            "color_scheme": "[ pastel/faded ]",
            "emotional_tone": "[ wistful/nostalgic ]"
        }

    elif style_category == "ferrofluid":
        imagen_settings["ferrofluid_settings"] = {
            "fluid_effect": "[ spiky/smooth ]",
            "magnetic_pattern": "[ geometric/organic ]",
            "lighting_direction": "[ high contrast/backlit ]",
            "motion_emphasis": "[ static/fluid/dynamic ]"
        }

    elif style_category == "animal_inspired":
        imagen_settings["animal_inspired_settings"] = {
            "theme_animal": "[ specify ]",
            "pattern_usage": "[ direct/motif/abstract ]",
            "texture_emphasis": "[ fur/scale/feather/carapace ]",
            "integration_level": "[ subtle/prominent ]"
        }

    elif style_category == "ascii_art":
        imagen_settings["ascii_art_settings"] = {
            "character_set": "[ restricted/full ]",
            "resolution": "[ low/medium/high ]",
            "mosaic_density": "[ sparse/dense ]",
            "contrast_method": "[ symbol/value/mix ]"
        }

    elif style_category == "biopunk":
        imagen_settings["biopunk_settings"] = {
            "bio_technology": "[ genetic/cybernetic/fungal ]",
            "integration_style": "[ seamless/grafted ]",
            "color_palette": "[ sickly/neon/muted ]",
            "mood": "[ unsettling/energetic ]"
        }
        imagen_settings["lighting_settings"]["highlight_color"] = "[ green/purple/pale blue ]"

    elif style_category == "kinetic_art":
        imagen_settings["kinetic_art_settings"] = {
            "motion_type": "[ mechanical/fluid/digital ]",
            "cycle_pattern": "[ looped/triggered ]",
            "audience_interaction": "[ passive/active ]",
            "visual_emphasis": "[ clean/geometric/organic ]"
        }

    elif style_category == "nightcore":
        imagen_settings["nightcore_settings"] = {
            "tempo": "[ fast/very fast ]",
            "color_palette": "[ neon/pastel/high-contrast ]",
            "audio_motif": "[ music/visual waves ]",
            "visual_emphasis": "[ high energy/edgy/futuristic ]"
        }

    elif style_category == "optic_art":
        imagen_settings["optic_art_settings"] = {
            "optical_illusion_type": "[ moiré/afterimage/grid ]",
            "pattern_density": "[ tight/loose ]",
            "movement_effect": "[ static/dynamic ]",
            "contrast_level": "[ high/medium ]"
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
