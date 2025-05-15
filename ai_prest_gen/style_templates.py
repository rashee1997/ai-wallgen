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
    get_generative_art_template,
    get_fractal_art_template,
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
from .logo_style_templates import ( # Imports for Logo styles
    get_logo_minimalist_template,
    get_logo_emblem_template,
    get_logo_wordmark_template,
    get_logo_lettermark_template,
    get_logo_abstract_template,
    get_logo_mascot_template,
    get_logo_illustrative_template,
    get_logo_3d_template,
    get_logo_default_template
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

# Registration dictionary for template functions
_template_registry = {}

def register_template(category_name):
    def decorator(func):
        _template_registry[category_name] = func
        return func
    return decorator

# Registering template functions
# Portrait categories
portrait_categories = {
    "photographic_portrait", "traditional_portrait", "futuristic_portrait",
    "illustration_portrait", "pop_portrait", "cyberpunk_portrait", "fantasy_portrait",
    "environmental_portrait", "caricature_portrait", "conceptual_portrait",
    "fashion_portrait", "selfie_portrait"
}
for cat in portrait_categories:
    _template_registry[cat] = get_portrait_template

# Photographic styles
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
_template_registry.update(photographic_style_map)

# Logo styles
logo_styles = {
    "logo_minimalist": get_logo_minimalist_template,
    "logo_emblem": get_logo_emblem_template,
    "logo_wordmark": get_logo_wordmark_template,
    "logo_lettermark": get_logo_lettermark_template,
    "logo_abstract": get_logo_abstract_template,
    "logo_mascot": get_logo_mascot_template,
    "logo_illustrative": get_logo_illustrative_template,
    "logo_3d": get_logo_3d_template,
    "logo": get_logo_default_template,
}
_template_registry.update(logo_styles)

# Illustration styles
illustration_styles = {
    "illustration_cubist": get_illustration_cubist_template,
    "illustration_surreal": get_illustration_surreal_template,
    "illustration_steampunk": get_illustration_steampunk_template,
    "illustration_pixar": get_illustration_pixar_template,
    "illustration_disney": get_illustration_disney_template,
    "illustration_tom_jerry": get_illustration_tom_jerry_template,
    "illustration_vintage_cartoon": get_illustration_vintage_cartoon_template,
    "illustration_anime_manga": get_illustration_anime_manga_template,
    "illustration_comic": get_illustration_comic_template,
    "illustration_pixel": get_illustration_pixel_template,
    "illustration_childrens": get_illustration_childrens_template,
    "illustration_fantasy": get_illustration_fantasy_template,
    "illustration_graphic": get_illustration_graphic_template,
    "illustration": get_illustration_template,
}
_template_registry.update(illustration_styles)

# Traditional art styles
traditional_styles = {
    "oil_painting": get_oil_painting_template,
    "watercolor": get_watercolor_template,
    "pastel": get_pastel_template,
    "acrylic_painting": get_acrylic_painting_template,
    "charcoal": get_charcoal_template,
    "pencil_sketch": get_pencil_sketch_template,
    "ink_drawing": get_ink_drawing_template,
    "drawing": get_drawing_template,
    "fresco_painting": get_fresco_painting_template,
    "pyrography": get_pyrography_template,
    "stone_carving": get_stone_carving_template,
}
_template_registry.update(traditional_styles)

# Hybrid and other styles
hybrid_styles = {
    "kinetic_ascii": get_kinetic_ascii_template,
    "watercolor_pencil": get_watercolor_pencil_template,
    "hybrid_traditional_digital": get_hybrid_traditional_digital_template,
    "installation_art": get_installation_art_template,
    "scientific_technological_hybrid": get_scientific_technological_hybrid_template,
    "augmented_reality_art": get_augmented_reality_art_template,
    "abstract_expressionism_cubism_fusion": get_abstract_expressionism_cubism_fusion_template,
    "collage_digital_overlay": get_collage_digital_overlay_template,
    "claymation": get_claymation_template,
    "experimental_mixed_media": get_experimental_mixed_media_template,
    "patchwork_collage": get_patchwork_collage_template,
    "paper_quilling": get_paper_quilling_template,
    "tradigital_mixed_media": get_tradigital_mixed_media_template,
    "whimsical_mixed_media": get_whimsical_mixed_media_template,
    "sci_fi_futuristic": get_sci_fi_futuristic_template,
    "mediterranean_style": get_mediterranean_style_template,
    "morphism_surreal": get_morphism_surreal_template,
    "cubism_mixed": get_cubism_mixed_template,
    "pixel_patchwork": get_pixel_patchwork_template,
    "phygital_hybrid": get_phygital_hybrid_template,
    "screen_printing_bold": get_screen_printing_bold_template,
    "mixed_media_journaling": get_mixed_media_journaling_template,
    "digital_pixel_traditional": get_digital_pixel_traditional_template,
    "patchwork_fabric": get_patchwork_fabric_template,
    "mixed_media_collage": get_mixed_media_collage_template,
    "whimsical_fantasy": get_whimsical_fantasy_template,
    "anime_oilpainting": get_anime_oilpainting_template,
    "minimalist_geometric": get_minimalist_geometric_template,
    "pop_surrealism_ascii": get_pop_surrealism_ascii_template,
    "dreamcore_weirdcore": get_dreamcore_weirdcore_template,
    "fantasy_battle": get_fantasy_battle_template,
    "fantasy_landscape": get_fantasy_landscape_template,
    "fantasy_cityscape": get_fantasy_cityscape_template,
    "cyberpunk_action": get_cyberpunk_action_template,
    "cyberpunk_technology": get_cyberpunk_technology_template,
    "game_retro": get_game_retro_template,
    "game_cel_shaded": get_game_cel_shaded_template,
    "photorealism_glitch": get_photorealism_glitch_template,
}
_template_registry.update(hybrid_styles)

# Digital styles
digital_styles = {
    "digital_art": get_digital_art_template,
    "digital_painting": get_digital_painting_template,
    "vector_art": get_vector_art_template,
    "ascii_art": get_ascii_art_template,
    "isometric": get_isometric_template,
    "game_style": get_game_style_template,
    "pixel_art": get_pixel_art_template,
    "vaporwave": get_vaporwave_template,
    "glitch_art": get_glitch_art_template,
    "surrealism": get_surrealism_template,
    "cubism": get_cubism_template,
    "minimalist": get_minimalist_template,
    "sci_fi": get_sci_fi_template,
    "steampunk": get_steampunk_template,
    "papercraft": get_papercraft_template,
    "generative_art": get_generative_art_template,
    "fractal_art": get_fractal_art_template,
}
_template_registry.update(digital_styles)

# Unique styles
unique_styles = {
    "psychedelic": get_psychedelic_template,
    "art_deco_revival": get_art_deco_revival_template,
    "fantasy": get_fantasy_template,
    "biopunk": get_biopunk_template,
    "kinetic_art": get_kinetic_art_template,
    "nightcore": get_nightcore_template,
    "optic_art": get_optic_art_template,
    "ferrofluid": get_ferrofluid_template,
    "animal_inspired": get_animal_inspired_template,
    "abstract_conceptual": get_abstract_conceptual_template,
    "material_sculptural": get_material_sculptural_template,
    "traditional_painting_drawing": get_traditional_painting_drawing_template,
}
_template_registry.update(unique_styles)

# 3D styles
three_d_styles = {
    "3d_render": get_3d_render_template,
    "voxel_art": get_voxel_art_template,
    "low_poly_3d": get_low_poly_3d_template,
    "cartoon_3d": get_cartoon_3d_template,
    "anime_3d": get_anime_3d_template,
    "abstract_3d": get_abstract_3d_template,
    "wireframe_3d": get_wireframe_3d_template,
    "clay_render_3d": get_clay_render_3d_template,
    "surreal_3d": get_surreal_3d_template,
    "painterly_3d": get_painterly_3d_template,
    "technical_illustration_3d": get_technical_illustration_3d_template,
    "minecraft_style_3d": get_minecraft_style_3d_template,
}
_template_registry.update(three_d_styles)

from ai_prest_gen.style_categorizer import StyleCategorizer

def get_template_for_category(style_category: Union[str, List[str]]) -> Dict[str, Any]:
    """
    Return the appropriate JSON template based on a style category or list of categories.

    This function first determines the single most relevant `main_category` using
    `_priority_category_match`. It then delegates to a specific registered template
    function based on this `main_category`.

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
    # Determine if AI selector toggle is enabled from user preferences or config
    # For now, assume a global or config flag; this should be replaced with actual user prefs access
    use_ai_selector = False
    # Removed reading use_ai_template_selector from user preferences as it no longer exists

    categorizer = StyleCategorizer(use_ai_selector=use_ai_selector)

    # If input is list, pick first or join for detection
    if isinstance(style_category, list):
        # Join list to a single string for AI detection or pick first for classic
        style_name_for_categorization = " ".join([str(s) for s in style_category if s])
    else:
        style_name_for_categorization = str(style_category)

    main_category = categorizer.categorize_style(style_name_for_categorization)

    if main_category in _template_registry:
        return _template_registry[main_category](main_category)

    # Default base template if no specific category match
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

    final_template = {**base_template, "imagen_settings": imagen_settings}
    return final_template
