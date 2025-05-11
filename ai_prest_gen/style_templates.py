"""
Style Templates Dispatcher Module for AI Preset Generator.

This module serves as the central dispatcher for retrieving style-specific
preset base templates. It imports template-generating functions from various
specialized modules (e.g., `digital_style_templates.py`, 
`photographic_style_templates.py`, etc.) and uses a prioritization logic 
to select and call the appropriate function based on a given style category.

The main function, `get_template_for_category`, determines the most relevant
category using `_priority_category_match` (which now relies on an externally
defined preferred order from `style_category_catalog.py`) and then delegates
to the corresponding `get_<style>_template` function.
"""

import re # Added for cleaning in preset name generation later if needed
from typing import Dict, Any, List, Optional, Union
from ai_prest_gen.camera_settings import get_dynamic_camera_settings
from .portrait_style_templates import get_portrait_template
from .photographic_style_templates import (
    get_photographic_template,
    get_cinematic_template,
    get_documentary_template,
    get_street_photography_template,
    get_noir_photography_template,
    get_luna_photo_template,
    get_macro_photography_template,
    get_wildlife_photography_template,
    get_food_photography_template,
)
from .hybrid_style_templates import (
    get_kinetic_ascii_template,
    get_watercolor_pencil_template,
    get_hybrid_traditional_digital_template,
    get_installation_art_template,
    get_scientific_technological_hybrid_template,
    get_augmented_reality_art_template,
    get_abstract_expressionism_cubism_fusion_template,
    get_collage_digital_overlay_template,
    get_claymation_template,
    get_experimental_mixed_media_template,
    get_patchwork_collage_template,
    get_paper_quilling_template,
    get_tradigital_mixed_media_template,
    get_whimsical_mixed_media_template,
    get_sci_fi_futuristic_template,
    get_mediterranean_style_template,
    get_morphism_surreal_template,
    get_cubism_mixed_template,
    get_pixel_patchwork_template,
    get_phygital_hybrid_template,
    get_screen_printing_bold_template,
    get_mixed_media_journaling_template,
    get_digital_pixel_traditional_template,
    get_patchwork_fabric_template,
    get_mixed_media_collage_template,
    get_whimsical_fantasy_template,
    get_anime_oilpainting_template,
    get_minimalist_geometric_template,
    get_pop_surrealism_ascii_template,
    get_dreamcore_weirdcore_template,
    get_fantasy_battle_template,
    get_fantasy_landscape_template,
    get_fantasy_cityscape_template,
    get_cyberpunk_action_template,
    get_cyberpunk_technology_template,
    get_game_retro_template,
    get_game_cel_shaded_template,
    get_photorealism_glitch_template, # Added import
)
from .illustration_style_templates import (
    get_illustration_cubist_template,
    get_illustration_surreal_template,
    get_illustration_steampunk_template,
    get_illustration_pixar_template,
    get_illustration_disney_template,
    get_illustration_tom_jerry_template,
    get_illustration_vintage_cartoon_template,
    get_illustration_anime_manga_template,
    get_illustration_comic_template,
    get_illustration_pixel_template,
    get_illustration_childrens_template,
    get_illustration_fantasy_template,
    get_illustration_graphic_template,
    get_illustration_template,
)
from .traditional_style_templates import (
    get_oil_painting_template,
    get_watercolor_template,
    get_pastel_template,
    get_acrylic_painting_template,
    get_charcoal_template,
    get_pencil_sketch_template,
    get_ink_drawing_template,
    get_drawing_template,
    get_gouache_template,
    get_tempera_template,
    get_mosaic_template,
    get_stained_glass_template,
    get_woodcut_template,
    get_traditional_collage_template,
    get_fresco_painting_template,
    get_pyrography_template,
    get_stone_carving_template,
)
from .digital_style_templates import (
    get_digital_art_template,
    get_digital_painting_template,
    # get_3d_render_template, # Moved to 3d_style_templates
    get_vector_art_template,
    get_ascii_art_template,
    get_isometric_template,
    get_game_style_template,
    get_pixel_art_template,
    get_vaporwave_template,
    get_glitch_art_template,
    get_surrealism_template,
    get_cubism_template,
    get_minimalist_template,
    get_sci_fi_template,
    get_steampunk_template,
    get_papercraft_template,
)
from .unique_style_templates import (
    get_psychedelic_template,
    get_art_deco_revival_template,
    get_fantasy_template,
    get_biopunk_template,
    get_kinetic_art_template,
    get_nightcore_template,
    get_optic_art_template,
    get_ferrofluid_template,
    get_animal_inspired_template,
    get_abstract_conceptual_template,
    get_material_sculptural_template,
    get_traditional_painting_drawing_template,
)
from .style_category_catalog import preferred_order as catalog_preferred_order # Added import
from .three_d_style_templates import ( # Imports for 3D styles
    get_3d_render_template,
    get_voxel_art_template,
    get_low_poly_3d_template,
    get_cartoon_3d_template,
    get_anime_3d_template,
    get_abstract_3d_template,
    get_wireframe_3d_template,
    get_clay_render_3d_template,
    get_surreal_3d_template,
    get_painterly_3d_template,
    get_technical_illustration_3d_template,
    get_minecraft_style_3d_template
)

# --- Main Template Generation Logic ---

def _priority_category_match(style_category: Union[str, List[str]]) -> str:
    """
    Return the best-matching style category based on the externally defined `catalog_preferred_order`.
    
    When multiple categories might match a style name, this function uses the
    `catalog_preferred_order` (sourced from `style_category_catalog.py`, which loads
    it from a JSON file) to select the single most appropriate category.
    If no specific match is found in the preferred order, it falls back to the
    first category in the input list or 'default' if the input is empty or invalid.

    Args:
        style_category (Union[str, List[str]]): A single style category string
                                                or a list of potential category strings.

    Returns:
        str: The determined primary style category.
    """
    # Use the imported preferred_order from style_category_catalog.py
    # This list is assumed to be pre-processed for uniqueness if necessary by its source.
    unique_priority_list = catalog_preferred_order

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
    Return the appropriate JSON template based on a style category or list of categories.

    This function first determines the single most relevant `main_category` using
    `_priority_category_match`. It then delegates to a specific `get_<style>_template`
    function (imported from specialized modules like `digital_style_templates.py`,
    `photographic_style_templates.py`, etc.) based on this `main_category`.

    All returned templates are fully defined with concrete default values, suitable
    for use as a base for AI preset generation.

    Args:
        style_category (Union[str, List[str]]): A single style category string or a
                                                list of potential category strings.

    Returns:
        Dict[str, Any]: A dictionary representing the JSON base template for the
                        determined style category. Returns a generic default
                        template if no specific match is found.
    """
    main_category = _priority_category_match(style_category)

    portrait_categories = {
        "photographic_portrait", "traditional_portrait", "futuristic_portrait",
        "illustration_portrait", "pop_portrait", "cyberpunk_portrait", "fantasy_portrait",
        "environmental_portrait", "caricature_portrait", "conceptual_portrait",
        "fashion_portrait", "selfie_portrait"
    }

    photographic_style_map = {
        "photographic": get_photographic_template,
        "cinematic": get_cinematic_template,
        "documentary": get_documentary_template,
        "street_photography": get_street_photography_template,
        "noir_photography": get_noir_photography_template,
        "luna_photo": get_luna_photo_template,
        "macro_photography": get_macro_photography_template,
        "wildlife_photography": get_wildlife_photography_template,
        "food_photography": get_food_photography_template,
    }

    if main_category in portrait_categories:
        return get_portrait_template(main_category)  # Delegated to portrait_style_templates

    if main_category in photographic_style_map:
        return photographic_style_map[main_category](main_category)

    # --- Delegation for Illustration Styles ---
    if main_category == "illustration_cubist":
        return get_illustration_cubist_template(main_category)
    elif main_category == "illustration_surreal":
        return get_illustration_surreal_template(main_category)
    elif main_category == "illustration_steampunk":
        return get_illustration_steampunk_template(main_category)
    elif main_category == "illustration_pixar":
        return get_illustration_pixar_template(main_category)
    elif main_category == "illustration_disney":
        return get_illustration_disney_template(main_category)
    elif main_category == "illustration_tom_jerry":
        return get_illustration_tom_jerry_template(main_category)
    elif main_category == "illustration_vintage_cartoon":
        return get_illustration_vintage_cartoon_template(main_category)
    elif main_category == "illustration_anime_manga":
        return get_illustration_anime_manga_template(main_category)
    elif main_category == "illustration_comic":
        return get_illustration_comic_template(main_category)
    elif main_category == "illustration_pixel":
        return get_illustration_pixel_template(main_category)
    elif main_category == "illustration_childrens":
        return get_illustration_childrens_template(main_category)
    elif main_category == "illustration_fantasy":
        return get_illustration_fantasy_template(main_category)
    elif main_category == "illustration_graphic":
        return get_illustration_graphic_template(main_category)
    elif main_category == "illustration":
        return get_illustration_template(main_category)
    elif main_category.startswith("illustration"):
        return get_illustration_template(main_category)

    # --- Common Settings & Camera Settings (No Placeholders) ---

    base_template = {
        "preset_name": f"{main_category.replace('_', ' ').title()} Preset",
        "moods": ["Evocative"],
        "aspect_ratio": "16:9",
        "description": f"A balanced preset for the {main_category.replace('_', ' ')} style, focusing on typical characteristics and a specific mood."
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

    # --- Traditional Art Templates Delegation ---
    if main_category == "oil_painting":
        return get_oil_painting_template(main_category)
    elif main_category == "watercolor":
        return get_watercolor_template(main_category)
    elif main_category == "pastel":
        return get_pastel_template(main_category)
    elif main_category == "acrylic_painting":
        return get_acrylic_painting_template(main_category)
    elif main_category == "charcoal":
        return get_charcoal_template(main_category)
    elif main_category == "pencil_sketch":
        return get_pencil_sketch_template(main_category)
    elif main_category == "ink_drawing":
        return get_ink_drawing_template(main_category)
    elif main_category == "drawing":
        return get_drawing_template(main_category)
    elif main_category == "fresco_painting":
        return get_fresco_painting_template(main_category)
    elif main_category == "pyrography":
        return get_pyrography_template(main_category)
    elif main_category == "stone_carving":
        return get_stone_carving_template(main_category)

    # --- Hybrids & Fusions ---
    if main_category == "kinetic_ascii":
        return get_kinetic_ascii_template(main_category)

    elif main_category == "watercolor_pencil":
        return get_watercolor_pencil_template(main_category)

    elif main_category == "hybrid_traditional_digital":
        return get_hybrid_traditional_digital_template(main_category)

    elif main_category == "installation_art":
        return get_installation_art_template(main_category)

    elif main_category == "scientific_technological_hybrid":
        return get_scientific_technological_hybrid_template(main_category)

    elif main_category == "augmented_reality_art":
        return get_augmented_reality_art_template(main_category)

    elif main_category == "abstract_expressionism_cubism_fusion":
        return get_abstract_expressionism_cubism_fusion_template(main_category)

    elif main_category == "collage_digital_overlay":
        return get_collage_digital_overlay_template(main_category)

    # --- Delegation for Newly Restored Hybrid/General Styles ---
    elif main_category == "claymation":
        return get_claymation_template(main_category)
    elif main_category == "experimental_mixed_media":
        return get_experimental_mixed_media_template(main_category)
    elif main_category == "patchwork_collage":
        return get_patchwork_collage_template(main_category)
    elif main_category == "paper_quilling":
        return get_paper_quilling_template(main_category)
    elif main_category == "tradigital_mixed_media":
        return get_tradigital_mixed_media_template(main_category)
    elif main_category == "whimsical_mixed_media":
        return get_whimsical_mixed_media_template(main_category)
    elif main_category == "sci_fi_futuristic":
        return get_sci_fi_futuristic_template(main_category)
    elif main_category == "mediterranean_style":
        return get_mediterranean_style_template(main_category)
    elif main_category == "morphism_surreal":
        return get_morphism_surreal_template(main_category)
    elif main_category == "cubism_mixed":
        return get_cubism_mixed_template(main_category)
    elif main_category == "pixel_patchwork":
        return get_pixel_patchwork_template(main_category)
    elif main_category == "phygital_hybrid":
        return get_phygital_hybrid_template(main_category)
    elif main_category == "screen_printing_bold":
        return get_screen_printing_bold_template(main_category)
    elif main_category == "mixed_media_journaling":
        return get_mixed_media_journaling_template(main_category)
    elif main_category == "digital_pixel_traditional":
        return get_digital_pixel_traditional_template(main_category)
    elif main_category == "patchwork_fabric":
        return get_patchwork_fabric_template(main_category)
    elif main_category == "mixed_media_collage":
        return get_mixed_media_collage_template(main_category)
    elif main_category == "whimsical_fantasy":
        return get_whimsical_fantasy_template(main_category)
    elif main_category == "anime_oilpainting":
        return get_anime_oilpainting_template(main_category)
    elif main_category == "minimalist_geometric":
        return get_minimalist_geometric_template(main_category)
    elif main_category == "pop_surrealism_ascii":
        return get_pop_surrealism_ascii_template(main_category)
    elif main_category == "dreamcore_weirdcore":
        return get_dreamcore_weirdcore_template(main_category)
    elif main_category == "photorealism_glitch": # Added condition
        return get_photorealism_glitch_template(main_category)
    elif main_category == "fantasy_battle":
        return get_fantasy_battle_template(main_category)
    elif main_category == "fantasy_landscape":
        return get_fantasy_landscape_template(main_category)
    elif main_category == "fantasy_cityscape":
        return get_fantasy_cityscape_template(main_category)
    elif main_category == "cyberpunk_action":
        return get_cyberpunk_action_template(main_category)
    elif main_category == "cyberpunk_technology":
        return get_cyberpunk_technology_template(main_category)
    elif main_category == "game_retro":
        return get_game_retro_template(main_category)
    elif main_category == "game_cel_shaded":
        return get_game_cel_shaded_template(main_category)
    elif main_category == "digital_painting":
        return get_digital_painting_template(main_category)
    elif main_category == "surrealism":
        return get_surrealism_template(main_category)
    elif main_category == "cubism":
        return get_cubism_template(main_category)
    elif main_category == "minimalist":
        return get_minimalist_template(main_category)
    elif main_category == "game_style":
        return get_game_style_template(main_category)
    elif main_category == "sci_fi":
        return get_sci_fi_template(main_category)
    elif main_category == "steampunk":
        return get_steampunk_template(main_category)
    elif main_category == "papercraft":
        return get_papercraft_template(main_category)
    elif main_category == "ascii_art":
        return get_ascii_art_template(main_category)
    elif main_category == "voxel_art":
        return get_voxel_art_template(main_category)
    elif main_category == "low_poly_3d":
        return get_low_poly_3d_template(main_category)
    elif main_category == "cartoon_3d":
        return get_cartoon_3d_template(main_category)
    elif main_category == "anime_3d":
        return get_anime_3d_template(main_category)
    elif main_category == "abstract_3d":
        return get_abstract_3d_template(main_category)
    elif main_category == "wireframe_3d":
        return get_wireframe_3d_template(main_category)
    elif main_category == "clay_render_3d":
        return get_clay_render_3d_template(main_category)
    elif main_category == "surreal_3d":
        return get_surreal_3d_template(main_category)
    elif main_category == "painterly_3d":
        return get_painterly_3d_template(main_category)
    elif main_category == "technical_illustration_3d":
        return get_technical_illustration_3d_template(main_category)
    elif main_category == "minecraft_style_3d":
        return get_minecraft_style_3d_template(main_category)
    elif main_category == "3d_render":
        return get_3d_render_template(main_category)
    elif main_category == "digital_art":
        return get_digital_art_template(main_category)
    elif main_category == "psychedelic":
        return get_psychedelic_template(main_category)
    elif main_category == "art_deco_revival":
        return get_art_deco_revival_template(main_category)
    elif main_category == "isometric":
        return get_isometric_template(main_category)
    elif main_category == "fantasy":
        return get_fantasy_template(main_category)
    elif main_category == "biopunk":
        return get_biopunk_template(main_category)
    elif main_category == "kinetic_art":
        return get_kinetic_art_template(main_category)
    elif main_category == "nightcore":
        return get_nightcore_template(main_category)
    elif main_category == "optic_art":
        return get_optic_art_template(main_category)
    elif main_category == "ferrofluid":
        return get_ferrofluid_template(main_category)
    elif main_category == "animal_inspired":
        return get_animal_inspired_template(main_category)
    elif main_category == "abstract_conceptual":
        return get_abstract_conceptual_template(main_category)
    elif main_category == "material_sculptural":
        return get_material_sculptural_template(main_category)
    elif main_category == "traditional_painting_drawing":
        return get_traditional_painting_drawing_template(main_category)

    # Final fallback for truly unknown or default
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
