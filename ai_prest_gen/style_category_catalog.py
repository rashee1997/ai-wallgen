"""
Style Category Catalog for AI Preset Generator (Enhanced V3)

This module contains the data structures used for categorizing style names.
It includes:
- A comprehensive preferred order for resolving category conflicts.
- Definitions for hybrid (compound) styles (token-based and keyword-based).
- Extensive keywords for identifying various art styles and categories.
- Instructions for the AI when generating presets for specific categories.
- A list of all defined categories for reference.
"""
import re
from typing import Dict, List, Set, Tuple, Union

# --- Comprehensive Preferred Order of Categories ---
# This list is crucial for disambiguation. More specific categories MUST come before broader ones.
# This order is synthesized from style_templates.py, portrait_style_templates.py, and user-provided catalogs.
preferred_order: List[str] = [
    # Highly Specific Hybrids/Fusions
    "pop_surrealism_ascii",
    "abstract_expressionism_cubism_fusion",
    "anime_oilpainting",
    "retro_pixel_vaporwave",
    "dreamcore_weirdcore",
    "photorealism_glitch",
    "watercolor_pencil",
    "cubism_futurism",
    "digital_pixel_traditional",
    "scientific_technological_hybrid",
    "psychedelic_surrealism",
    "morphism_surreal",
    "kinetic_ascii",
    "collage_digital_overlay", # More specific than digital_collage
    "pixel_patchwork",
    "tradigital_mixed_media",
    "hybrid_traditional_digital", # Similar to above, order might not matter much between these two
    "digital_traditional_fusion", # Similar to above

    # Specific Portraits
    "caricature_portrait",
    "selfie_portrait",
    "environmental_portrait",
    "fashion_portrait",
    "conceptual_portrait",
    "cyberpunk_portrait",
    "futuristic_portrait", # Includes sci_fi_portrait
    "pop_portrait",
    "illustration_portrait",
    "photographic_portrait",
    "traditional_portrait",
    "fantasy_portrait",

    # Specific Thematic/Technical Styles
    "noir_photography",
    "art_deco_revival",
    "augmented_reality_art", # Includes vr_ar_art
    "biopunk",
    "ferrofluid",
    "fractal_generative_art",
    "installation_art",
    "kinetic_art", # if not kinetic_ascii
    "luna_photo",
    "mixed_media_journaling", # Includes sketchbook_mixed_media
    "nightcore",
    "optic_art",
    "paper_quilling",
    "phygital_hybrid",
    "screen_printing_bold",
    "synesthesia_art",
    "ink_punk", # Specific illustrative style

    # Game Styles
    "game_cel_shaded",
    "game_retro", # (8-bit, 16-bit, pixel game art)
    "game_style", # General (Unity, Unreal, FPS, RPG etc.)

    # Cyberpunk (non-portrait)
    "cyberpunk_action",
    "cyberpunk_cityscape",
    "cyberpunk_technology",
    "cyberpunk", # General

    # Fantasy (non-portrait)
    "fantasy_battle",
    "fantasy_cityscape",
    "fantasy_landscape",
    "whimsical_fantasy",
    "fantasy", # General

    # Sci-Fi (non-portrait)
    "sci_fi_futuristic", # More specific than sci_fi
    "sci_fi", # General

    # Specific Mediums/Techniques
    "claymation",
    "digital_collage", # If not collage_digital_overlay
    "experimental_mixed_media",
    "patchwork_fabric",
    "patchwork_collage", # If not pixel_patchwork
    "papercraft", # General papercraft (if not quilling)
    "ascii_art", # If not kinetic_ascii or pop_surrealism_ascii
    "line_art", # Distinct from general drawing

    # Illustration Styles (non-portrait)
    "illustration_pixar",
    "illustration_disney",
    "illustration_tom_jerry",
    "illustration_vintage_cartoon",
    "illustration_anime_manga", # Broad anime/manga illustration
    "illustration_comic",
    "illustration_pixel", # if not game_retro or retro_pixel_vaporwave
    "illustration_steampunk",
    "illustration_cubist",
    "illustration_surreal",
    "illustration_childrens",
    "illustration_fantasy", # if not fantasy_portrait and more general fantasy
    "illustration_graphic", # General graphic illustration
    "illustration", # Broadest illustration

    # Painting Styles (Specific Mediums)
    "oil_painting", # if not anime_oilpainting
    "watercolor", # if not watercolor_pencil
    "pastel",
    "acrylic_painting",
    "digital_painting",

    # Drawing Styles (Specific Mediums)
    "pencil_sketch",
    "ink_drawing", # if not ink_punk or line_art
    "charcoal",
    "drawing", # Broadest drawing

    # Photographic Styles (non-portrait)
    "street_photography",
    "documentary", # Photo style
    "cinematic", # Can be photo or 3D; specific photo types are higher
    "photographic", # General photographic

    # Abstract & Conceptual (non-portrait)
    "minimalist_geometric",
    "minimalist", # or "minimal"
    "geometric", # if not minimalist_geometric
    "constructivism",
    "low_poly", # Often 3D but can be abstract geometric
    "abstract_conceptual",
    "abstract", # General abstract

    # Other Distinct Styles
    "pop_surrealism", # if not pop_surrealism_ascii or pop_portrait
    "surrealism", # if not psychedelic_surrealism or illustration_surreal
    "cubism", # if not various cubism fusions or illustration_cubist
    "expressionism", # if not part of a fusion
    "fauvism",
    "art_nouveau",
    "art_deco", # if not art_deco_revival
    "psychedelic", # if not psychedelic_surrealism
    "steampunk", # if not illustration_steampunk
    "dystopian",
    "glitch_art", # if not photorealism_glitch
    "retrowave", # if not retro_pixel_vaporwave (Synthwave, Outrun)
    "vaporwave", # if not retro_pixel_vaporwave
    "dreamcore", # if not dreamcore_weirdcore
    "weirdcore", # if not dreamcore_weirdcore
    "folk_art",
    "mediterranean_style",

    # Material/Sculptural
    "material_sculptural",
    "sculpture",

    # Broad Digital/Traditional Categories (Fallbacks)
    "3d_render", # CGI, modeling (if not game_style or specific 3D like low_poly)
    "vector_art",
    "digital_art", # General digital art
    "traditional_painting_drawing", # Very broad

    # Meta/Other
    "animal_inspired",
    "space_art",
    "robot_art",

    "default",
    "unknown"
]

# --- Hybrid Style Definitions (Token-based) ---
# Key: frozenset of normalized style name parts, Value: target hybrid category.
# Order within the frozenset does not matter.
hybrid_styles: Dict[frozenset[str], str] = {
    # From user's catalog & previous context
    frozenset(["abstract", "expressionism", "cubism"]): "abstract_expressionism_cubism_fusion",
    frozenset(["anime", "oil", "painting"]): "anime_oilpainting",
    frozenset(["anime", "oilpaint"]): "anime_oilpainting", # Variant
    frozenset(["collage", "digital", "overlay"]): "collage_digital_overlay",
    frozenset(["cubism", "futurism"]): "cubism_futurism",
    frozenset(["digital", "pixel", "traditional"]): "digital_pixel_traditional",
    frozenset(["digital", "traditional", "fusion"]): "digital_traditional_fusion",
    frozenset(["hybrid", "traditional", "digital"]): "hybrid_traditional_digital",
    frozenset(["kinetic", "ascii"]): "kinetic_ascii",
    frozenset(["morphism", "surreal"]): "morphism_surreal",
    frozenset(["pixel", "patchwork"]): "pixel_patchwork",
    frozenset(["pop", "surrealism", "ascii"]): "pop_surrealism_ascii",
    frozenset(["psychedelic", "surrealism"]): "psychedelic_surrealism",
    frozenset(["retro", "pixel", "vaporwave"]): "retro_pixel_vaporwave",
    frozenset(["scientific", "technological", "hybrid"]): "scientific_technological_hybrid",
    frozenset(["tradigital", "mixed", "media"]): "tradigital_mixed_media",
    frozenset(["watercolor", "pencil"]): "watercolor_pencil",
    frozenset(["watercolour", "pencil"]): "watercolor_pencil", # UK spelling
    frozenset(["dreamcore", "weirdcore"]): "dreamcore_weirdcore",
    frozenset(["minimalist", "geometric"]): "minimalist_geometric",
    frozenset(["minimal", "geometric"]): "minimalist_geometric", # Variant
    frozenset(["photorealism", "glitch"]): "photorealism_glitch",
    frozenset(["photorealistic", "glitch"]): "photorealism_glitch", # Variant
    frozenset(["luna", "photo"]): "luna_photo",
    frozenset(["pop", "art", "portrait"]): "pop_portrait",
    frozenset(["cyberpunk", "city"]): "cyberpunk_cityscape",
    frozenset(["cyberpunk", "portrait"]): "cyberpunk_portrait",
    frozenset(["fantasy", "battle"]): "fantasy_battle",
    frozenset(["fantasy", "landscape"]): "fantasy_landscape",
    frozenset(["fantasy", "portrait"]): "fantasy_portrait",
    frozenset(["fantasy", "city"]): "fantasy_cityscape",
    frozenset(["sci", "fi", "futuristic"]): "sci_fi_futuristic", # Ensure 'scifi' normalization handles this
    frozenset(["scifi", "futuristic"]): "sci_fi_futuristic", # Alternative
    frozenset(["sci", "fi", "portrait"]): "futuristic_portrait",
    frozenset(["scifi", "portrait"]): "futuristic_portrait", # Alternative
    frozenset(["mixed", "media", "collage"]): "mixed_media_collage",
    frozenset(["mixed", "media", "journaling"]): "mixed_media_journaling",
    frozenset(["sketchbook", "mixed", "media"]): "mixed_media_journaling", # Alias
    frozenset(["whimsical", "mixed", "media"]): "whimsical_mixed_media",
    frozenset(["whimsical", "fantasy"]): "whimsical_fantasy",
    frozenset(["screen", "printing", "bold"]): "screen_printing_bold",
    frozenset(["phygital", "hybrid"]): "phygital_hybrid",
    frozenset(["cubism", "mixed", "media"]): "cubism_mixed",
    frozenset(["illustration", "cubist"]): "illustration_cubist",
    frozenset(["illustration", "surreal"]): "illustration_surreal",
    frozenset(["illustration", "steampunk"]): "illustration_steampunk",
    frozenset(["illustration", "portrait"]): "illustration_portrait",
    frozenset(["photographic", "portrait"]): "photographic_portrait",
    frozenset(["traditional", "portrait"]): "traditional_portrait",
    frozenset(["environmental", "portrait"]): "environmental_portrait",
    frozenset(["caricature", "portrait"]): "caricature_portrait",
    frozenset(["conceptual", "portrait"]): "conceptual_portrait",
    frozenset(["fashion", "portrait"]): "fashion_portrait",
    frozenset(["selfie", "portrait"]): "selfie_portrait",
    frozenset(["experimental", "mixed", "media"]): "experimental_mixed_media",
    frozenset(["vr", "ar", "art"]): "augmented_reality_art",
    frozenset(["virtual", "reality", "art"]): "augmented_reality_art", # Alias for VR
    frozenset(["augmented", "reality", "art"]): "augmented_reality_art", # Alias for AR
}

# --- Keyword-based Hybrid Category Definitions ---
# For cases where tokenization might not be ideal or for more complex phrases.
# Key: target hybrid category, Value: list of keyword tuples (all keywords in a tuple must be present).
hybrid_categories_keywords: Dict[str, List[Tuple[str, ...]]] = {
    "kinetic_ascii": [("kinetic", "ascii")],
    "watercolor_pencil": [("watercolor", "pencil"), ("watercolour", "pencil sketch"), ("watercolor", "pencil sketch")],
    "photorealism_glitch": [("photorealism", "glitch"), ("photorealistic", "glitch art")],
    "anime_oilpainting": [("anime", "oil painting"), ("manga", "oil painting")],
    "minimalist_geometric": [("minimalist", "geometric"), ("minimal", "geometric"), ("minimalism", "geometric")],
    "pop_surrealism_ascii": [("pop surrealism", "ascii")],
    "dreamcore_weirdcore": [("dreamcore", "weirdcore")],
    "patchwork_collage": [("patchwork", "collage")],
    "tradigital_mixed_media": [("tradigital", "mixed media")],
    "whimsical_mixed_media": [("whimsical", "mixed media")],
    "cubism_mixed": [("cubism", "mixed media")],
    "pixel_patchwork": [("pixel", "patchwork")],
    "phygital_hybrid": [("phygital", "hybrid")],
    "screen_printing_bold": [("screen printing", "bold graphic"), ("serigraphy", "bold")],
    "mixed_media_journaling": [("mixed media", "journaling"), ("art", "journaling"), ("sketchbook", "mixed media")],
    "digital_pixel_traditional": [("digital pixel", "traditional art"), ("pixel art", "traditional painting")],
    "cubism_futurism": [("cubism", "futurism")],
    "digital_traditional_fusion": [("digital", "traditional", "fusion"), ("digital painting", "traditional elements")],
    "retro_pixel_vaporwave": [("retro pixel", "vaporwave"), ("pixel art", "vaporwave aesthetic")],
    "psychedelic_surrealism": [("psychedelic", "surrealism"), ("trippy", "surreal")],
    "hybrid_traditional_digital": [("hybrid", "traditional", "digital"), ("traditional art", "digital enhancement")],
    "installation_art": [("installation", "art"), ("art installation", "immersive art piece")],
    "scientific_technological_hybrid": [("scientific", "technological", "hybrid"), ("data driven", "art"), ("algorithmic", "art installation")],
    "augmented_reality_art": [("augmented reality", "art"), ("ar", "art"), ("mixed reality", "art piece"), ("vr", "art experience")],
    "abstract_expressionism_cubism_fusion": [("abstract expressionism", "cubism"), ("expressionist", "cubist forms")],
    "collage_digital_overlay": [("collage", "digital overlay"), ("photomontage", "digital effects")],
    "experimental_mixed_media": [("experimental", "mixed media"), ("avant garde", "combined media")],
}

# --- General Category Keywords ---
# Maps broader categories to a list of identifying keywords/phrases (normalized lowercase).
categories_keywords: Dict[str, List[str]] = {
    # Portraits
    "photographic_portrait": ["photographic portrait", "photo realistic portrait", "dslr portrait"],
    "traditional_portrait": ["traditional portrait painting", "classic painted portrait", "oil on canvas portrait"],
    "futuristic_portrait": ["futuristic character portrait", "scifi human portrait", "future concept portrait"],
    "cyberpunk_portrait": ["cyberpunk character portrait", "cyborg face", "neon noir portrait"],
    "illustration_portrait": ["illustrated face", "character art portrait", "stylized digital portrait"],
    "pop_portrait": ["pop art style portrait", "warholesque portrait", "graphic pop character"],
    "environmental_portrait": ["environmental portraiture", "subject in context photo", "location based portrait"],
    "caricature_portrait": ["caricature drawing", "exaggerated features portrait", "cartoon likeness"],
    "conceptual_portrait": ["conceptual art portrait", "symbolic self portrait", "idea driven face"],
    "fashion_portrait": ["fashion photography portrait", "editorial model shot", "vogue style image", "beauty shot"],
    "selfie_portrait": ["selfie style", "phone self portrait", "social media selfie"],
    "fantasy_portrait": ["fantasy character portrait", "elf face", "wizard depiction", "mythical being portrait"],

    # Specific Styles
    "noir_photography": ["noir film photography", "black and white crime photo", "chiaroscuro detective"],
    "digital_collage": ["digital collage art", "photomontage composition", "layered digital graphics"],
    "claymation": ["claymation style", "stop motion clay model", "plasticine animation"],
    "art_deco_revival": ["art deco revival design", "modern deco pattern", "gatsby era update"],
    "biopunk": ["biopunk aesthetic", "bio-punk art", "organic tech visuals", "genetic horror"],
    "dreamcore": ["dreamcore images", "dreamy surreal aesthetic", "liminal space visuals"],
    "ferrofluid": ["ferrofluid sculpture", "magnetic liquid display", "iron fluid patterns"],
    "fractal_generative_art": ["fractal geometry art", "generative algorithm patterns", "mandelbrot visuals"],
    "folk_art": ["traditional folk art", "ethnic pattern design", "naive decorative painting", "cultural craft art"],
    "ink_punk": ["ink punk illustration", "raw sketchy ink art", "gritty ink style"],
    "isometric": ["isometric projection", "isometric illustration", "2.5d game view", "axonometric art"],
    "kinetic_art": ["kinetic sculpture", "moving art installation", "art in motion design"],
    "mixed_media_collage": ["mixed media collage art", "assemblage artwork", "found object collage"],
    "nightcore": ["nightcore visuals", "fast paced anime graphics", "high energy music video style"],
    "optic_art": ["op art patterns", "optical illusion design", "visual geometric tricks"],
    "paper_quilling": ["paper quilling designs", "quilled paper craft", "rolled paper art forms"],
    "patchwork_fabric": ["fabric patchwork design", "textile art quilt", "sewn fabric collage"],
    "pop_surrealism": ["pop surrealism painting", "lowbrow art movement", "new contemporary characters"],
    "psychedelic": ["psychedelic art experience", "trippy visual patterns", "acid trip graphics", "visionary abstract painting"],
    "surrealism": ["surrealist painting", "surreal dreamscape art", "dali-esque imagery", "magritte style"],
    "cubism": ["cubist artwork", "picasso style cubism", "geometric abstract painting", "braque cubism"],
    "minimalist": ["minimalist artwork", "minimal design style", "simple abstract forms", "clean aesthetic"],
    "geometric": ["geometric abstract art", "geometric shape patterns", "mathematical design"],
    "steampunk": ["steampunk aesthetic art", "victorian futuristic tech", "clockwork machinery design", "industrial fantasy art"],
    "dystopian": ["dystopian world art", "post-apocalyptic landscape", "dark future society visuals"],
    "glitch_art": ["glitch effect art", "databending images", "digital distortion graphics"],
    "retrowave": ["retrowave design style", "synthwave visuals", "outrun aesthetic graphics", "80s neon future"],
    "vaporwave": ["vaporwave art style", "90s internet aesthetic", "glitchy pastel nostalgia", "classical statue glitch"],
    "mediterranean_style": ["mediterranean painting", "tuscan landscape art", "greek island scenery"],
    "animal_inspired": ["animal-inspired patterns", "animal motif artwork", "wildlife themed design"],
    "space_art": ["space exploration art", "astronomical illustration", "cosmic nebula painting", "galaxy artwork"],
    "robot_art": ["robot concept design", "mech warrior art", "cybernetic android illustration", "mecha drawing"],

    # Game Styles
    "game_cel_shaded": ["cel shaded game graphics", "toon shaded 3d models", "anime style video game"],
    "game_retro": ["retro video game art", "8-bit pixel graphics", "16-bit game design", "classic arcade style"],
    "game_style": ["video game concept art", "game environment design", "game character model", "unity game screenshot", "unreal engine visuals"],

    # Cyberpunk
    "cyberpunk_cityscape": ["cyberpunk city skyline", "neon lit urban future", "blade runner style city"],
    "cyberpunk_action": ["cyberpunk combat art", "sci-fi gunfight scene", "futuristic battle concept"],
    "cyberpunk_technology": ["cyberpunk ui design", "holographic interface art", "future tech gadgets display"],
    "cyberpunk": ["cyberpunk genre art", "high tech low life visuals", "dystopian neon future"],

    # Fantasy
    "fantasy_battle": ["epic fantasy battle art", "mythical combat illustration", "dragon fight scene"],
    "fantasy_cityscape": ["magical city concept", "elven architecture design", "dwarven city illustration", "floating fantasy city"],
    "fantasy_landscape": ["enchanted forest painting", "mystical mountain range art", "alien planet environment"],
    "whimsical_fantasy": ["whimsical fairy tale art", "dreamy fantasy illustration", "lighthearted magical scene"],
    "fantasy": ["high fantasy art", "mythical creature illustration", "epic world building art", "sword and sorcery visuals"],

    # Sci-Fi
    "sci_fi_futuristic": ["advanced scifi technology", "space opera concept art", "far future civilization design"],
    "sci_fi": ["science fiction concept art", "futuristic vehicle design", "alien planet exploration", "spaceship interior"],

    # Illustration
    "illustration_pixar": ["pixar style 3d animation", "pixar character concept"],
    "illustration_disney": ["disney animation style", "classic disney character art"],
    "illustration_tom_jerry": ["tom and jerry style cartoon", "hanna-barbera character design"],
    "illustration_vintage_cartoon": ["vintage cartoon animation", "rubber hose style art", "1930s character art"],
    "illustration_anime_manga": ["anime illustration style", "manga comic art", "japanese animation character"],
    "illustration_comic": ["comic book panel art", "graphic novel page", "superhero comic style"],
    "illustration_pixel": ["pixel art character sprite", "8-bit scene illustration", "16-bit game background"],
    "illustration_childrens": ["childrens book artwork", "picture book style illustration", "kids story characters"],
    "illustration_graphic": ["graphic design illustration", "bold vector art style", "modern flat illustration"],
    "illustration_steampunk": ["steampunk character illustration", "victorian sci-fi drawing"],
    "illustration_cubist": ["cubist style illustration", "geometric character design"],
    "illustration_surreal": ["surreal narrative illustration", "dreamlike character art"],
    "illustration_fantasy": ["fantasy story illustration", "mythical creature drawing"],
    "illustration": ["general illustrative art", "stylized representational art", "narrative drawing"],

    # Painting
    "oil_painting": ["oil painting artwork", "oil on canvas piece", "traditional oil medium"],
    "watercolor": ["watercolor wash painting", "watercolour illustration", "aquarelle landscape"],
    "pastel": ["pastel portrait drawing", "pastel landscape art", "soft pastel technique", "oil pastel artwork"],
    "acrylic_painting": ["acrylic abstract painting", "acrylic on board", "modern acrylic art"],
    "digital_painting": ["digital painting illustration", "photoshop concept art", "procreate character design", "painterly digital art"],

    # Drawing
    "pencil_sketch": ["graphite pencil sketch", "detailed pencil drawing", "realistic pencil portrait"],
    "ink_drawing": ["pen and ink illustration", "ink wash drawing", "black and white ink art", "hatching ink technique"],
    "charcoal": ["charcoal figure drawing", "charcoal landscape sketch", "expressive charcoal art"],
    "line_art": ["clean line art", "outline illustration", "inking comic art", "vector line drawing"],
    "drawing": ["hand-drawn illustration", "traditional sketch artwork", "observational drawing"],

    # Photographic
    "street_photography": ["candid street photography", "urban environment photos", "city life documentation"],
    "documentary": ["documentary photo series", "photojournalistic story", "reportage photography style"],
    "cinematic": ["cinematic shot composition", "film still photography", "movie scene aesthetic", "dramatic lighting photo"],
    "photographic": ["realistic photograph", "dslr camera image", "high quality photo print"],

    # Abstract & Conceptual
    "constructivism": ["constructivist poster design", "geometric avant-garde art", "russian constructivism"],
    "low_poly": ["low poly 3d art", "faceted polygon design", "geometric minimalist 3d"],
    "abstract_conceptual": ["abstract conceptual painting", "idea-based visual representation", "symbolic abstract forms"],
    "abstract": ["abstract expressionist art", "non-objective painting", "geometric abstract patterns design"],
    "expressionism": ["expressionist painting", "emotive art style", "german expressionism"],
    "fauvism": ["fauvist color painting", "wild beast art movement", "matisse style fauvism"],
    "art_nouveau": ["art nouveau design", "jugendstil illustration", "organic flowing lines art"],
    "art_deco": ["art deco architecture", "gatsby style design", "modernist geometric patterns"],

    # Material/Sculptural
    "material_sculptural": ["mixed material sculpture", "3d form installation", "textured sculptural art"],
    "sculpture": ["bronze sculpture", "marble statue", "clay modeling figure", "wood carving art"],

    # Broad Digital/Traditional
    "3d_render": ["3d architectural render", "cgi product visualization", "computer graphics animation still", "photorealistic 3d scene"],
    "vector_art": ["vector illustration design", "adobe illustrator graphics", "scalable vector logo"],
    "digital_art": ["general digital artwork", "computer generated art piece", "digital media creation"],
    "traditional_painting_drawing": ["classic art techniques", "traditional art media painting", "non-digital drawing methods"],

    # Other techniques/themes
    "papercraft": ["3d papercraft model", "paper art sculpture", "kirigami cut paper", "origami animal"],
    "ascii_art": ["ascii text picture", "character art graphic", "terminal art image"],
    "default": ["standard style", "generic artwork", "basic visual design"],
    "unknown": ["undefined art style", "other category", "unclassified visual"],
}

# --- All Categories List (Dynamically Generated) ---
def get_all_defined_categories() -> List[str]:
    """Returns a sorted list of all unique category names defined in this catalog."""
    _all_cats: Set[str] = set(preferred_order)
    _all_cats.update(hybrid_styles.values())
    _all_cats.update(hybrid_categories_keywords.keys())
    _all_cats.update(categories_keywords.keys())
    return sorted(list(_all_cats))

all_categories: List[str] = get_all_defined_categories()

# --- Instructions for AI based on Category ---
def instructions_for_category(category: str, base_style: str) -> str:
    """Return specific instructions for the AI based on the detected style category."""
    category = category.lower() # Ensure lowercase for matching
    base_style_clean = base_style.replace('_', ' ').title()
    default_instruction = (
        f"Emphasize the core characteristics of '{base_style_clean}'. "
        "Ensure settings like lighting, color, and composition enhance its unique aesthetic. "
        "Avoid clichés unless specifically part of the style."
    )
    portrait_base_instruction = (
        "For this portrait, focus on subject emphasis. Lighting should sculpt the subject. "
        "Composition should draw attention to the face/expression. Colors should be appropriate "
        "for skin tones and mood. Detail should be fitting for the specific portrait style."
    )

    cat_instructions: Dict[str, str] = {
        # Portraits
        "photographic_portrait": f"{portrait_base_instruction} Prioritize realism, natural skin textures, and appropriate depth of field. Camera settings (aperture, lens) are crucial.",
        "traditional_portrait": f"{portrait_base_instruction} Emulate classical painting techniques. Consider medium (oil, watercolor, etc.), brushwork, and traditional lighting (Rembrandt, Chiaroscuro).",
        "futuristic_portrait": f"{portrait_base_instruction} Incorporate sci-fi or cyberpunk elements: cybernetics, neon lighting, advanced tech aesthetics. Mood: stoic, intense, mysterious.",
        "cyberpunk_portrait": f"{portrait_base_instruction} Focus on gritty, neon-lit environments, cybernetic enhancements, and a dystopian mood. High contrast and tech details are key.",
        "illustration_portrait": f"{portrait_base_instruction} Style can range from stylized realism to cartoonish. Emphasize line work, coloring technique, and expressive features. Not photorealistic.",
        "pop_portrait": f"{portrait_base_instruction} Use bold colors, graphic elements, and potentially pop culture references (Warhol, Lichtenstein). Flat lighting is common.",
        "environmental_portrait": f"{portrait_base_instruction} The subject's surroundings are key to telling their story. Integrate subject with their environment. Lighting should feel natural to the location.",
        "caricature_portrait": f"{portrait_base_instruction} Exaggerate key facial features and expressions for comedic or satirical effect. Line work is often bold and expressive.",
        "conceptual_portrait": f"{portrait_base_instruction} Convey a specific idea, metaphor, or emotion. Use symbolism, surreal elements, or unconventional compositions. Mood is paramount.",
        "fashion_portrait": f"{portrait_base_instruction} Showcase clothing, style, and attitude. Posing, makeup, and lighting should be editorial and impactful. Can be studio or location.",
        "selfie_portrait": f"{portrait_base_instruction} Capture the informal, often spontaneous feel of a self-taken photo. Consider phone camera aesthetics, common filters, and casual backgrounds.",
        "fantasy_portrait": f"{portrait_base_instruction} Depict characters from fantasy genres (elves, wizards, warriors). Include magical elements, ornate costumes, and an epic or mystical mood.",

        # Hybrids & Fusions
        "abstract_expressionism_cubism_fusion": "Combine gestural, emotive brushwork of abstract expressionism with the fragmented, multi-perspective forms of cubism. Dynamic and layered.",
        "anime_oilpainting": "Merge anime/manga character styles (large eyes, distinct hair) with the rich textures, blending, and volumetric lighting of oil painting. Avoid flat cel-shading.",
        "minimalist_geometric": "Focus on extreme simplicity using basic geometric shapes (lines, circles, squares). Emphasis on negative space. Limited color palette, often monochrome or pastels.",
        "photorealism_glitch": "Start with a hyperrealistic photographic base, then introduce digital glitch effects (RGB shifts, scanlines, datamoshing, pixelation) for a corrupted, deconstructed look.",
        "dreamcore_weirdcore": "Create unsettling, uncanny, and nostalgic scenes. Often uses liminal spaces, low-fi aesthetics, soft or distorted visuals, and ambiguous objects. Mood is key: dreamy yet eerie.",
        "watercolor_pencil": "Blend soft, transparent watercolor washes with the defined lines and textures of pencil sketching. Watercolor for backgrounds/underlayers, pencil for details/outlines.",
        "retro_pixel_vaporwave": "Combine 8-bit or 16-bit pixel art aesthetics with vaporwave elements: neon pastels, classical statues, retro UI, glitch effects, and a nostalgic, surreal mood.",
        "pop_surrealism_ascii": "Render pop surrealist subjects (cartoony, lowbrow, iconic) using ASCII characters. The overall image should be recognizable but composed of text/symbols.",
        "psychedelic_surrealism": "Fuse intense, vibrant, swirling psychedelic patterns and colors with dreamlike, illogical, and bizarre surrealist imagery. Focus on transformation and altered perception.",
        "kinetic_ascii": "Visualize kinetic movement or animation using only ASCII characters. Think pulsing text, flowing symbols, or simple character-based animations on a grid. Retro-tech or cyber fusion feel.",
        "collage_digital_overlay": "Start with a physical collage base (paper, fabric) and then enhance it with digital overlays, textures, or effects. Blend tactile and digital aesthetics.",
        "pixel_patchwork": "Create a visual style resembling a patchwork quilt, but where each 'patch' is made of pixel art or has a distinct pixelated texture. Varied colors and patterns.",
        "tradigital_mixed_media": "A seamless blend of traditional art techniques (painting, drawing) with digital tools and enhancements. The goal is a cohesive piece where both origins are visible but harmonious.",
        "hybrid_traditional_digital": "Similar to tradigital, emphasizing the fusion of hand-made traditional elements with digital manipulation or additions. Focus on texture and layering.",
        "digital_traditional_fusion": "Another variant focusing on the integration of digital art creation with the aesthetics or processes of traditional art forms.",
        "cubism_futurism": "Combine the fragmented, multi-perspective views of Cubism with the dynamic lines, speed, and technological themes of Futurism.",
        "digital_pixel_traditional": "Merge pixel art aesthetics with traditional painting or drawing techniques. For example, a painted scene with pixelated characters, or a pixel art base with painted textures.",
        "scientific_technological_hybrid": "Art that integrates scientific data, concepts, or technological processes (like AI, algorithms, biotech) into its visual form or creation method.",
        "morphism_surreal": "Focus on surreal transformations where objects or figures fluidly morph into one another or into abstract shapes. Dreamlike and fantastical.",

        # Specific Styles
        "noir_photography": "Monochrome, deep shadows, moody lighting, strong contrasts. Motif: Dramatic, cinematic, shadow play, mysterious subject matter. Film grain and analog authenticity. Mood: Suspenseful, introspective, classic.",
        "digital_collage": "Assemble disparate digital elements (photos, textures, graphics) into a cohesive new image. Emphasize layering, juxtaposition, and possibly surreal or abstract compositions.",
        "claymation": "Emulate the look of stop-motion clay animation. Visible textures like fingerprints or tool marks are good. Characters often have simple, expressive forms. Lighting is usually practical/studio.",
        "art_deco_revival": "Modern take on Art Deco. Luxurious materials (simulated), geometric patterns (chevrons, sunbursts), symmetry, and a glamorous, sophisticated feel.",
        "augmented_reality_art": "Designed for immersive/interactive display, often overlaying digital elements onto the real world. Consider 3D depth, interaction, and how it's viewed (e.g., through a screen).",
        "biopunk": "Explore biological themes, genetic modification, organic technology, often with a dark or unsettling tone. Visuals can include mutations, bio-mechanical fusions, and overgrown organic matter.",
        "dreamcore": "Nostalgic, eerie, and often low-fidelity visuals of liminal spaces or vaguely familiar, empty environments. Soft focus, pastel or desaturated colors, and a sense of longing or unease.",
        "ferrofluid": "Mimic the appearance of ferrofluid: black, spiky, magnetic liquid. Focus on its unique reaction to magnetic fields, creating complex organic or geometric patterns.",
        "fractal_generative_art": "Algorithmic, recursive patterns (Mandelbrot, Julia sets). Iteration depth and color maps drive visual complexity. Organic or geometric shapes, radiating or spiraling forms. Mood: Hypnotic, mathematical, vibrant.",
        "folk_art": "Reflects traditional cultural art forms. Often characterized by stylized motifs, bold colors, handcrafted appearance, and narrative or symbolic content specific to a region or culture.",
        "ink_punk": "Raw, energetic, and sketchy ink style. Often high contrast, with a rebellious or unfinished aesthetic. Think street art or edgy comic book inking.",
        "installation_art": "Focus on art that transforms a space or creates an environment. Consider scale, materials, and how the viewer interacts with or moves through the piece.",
        "isometric": "Use an isometric projection (equal angles, no perspective vanishing). Creates a stylized 2.5D look common in technical drawings, pixel art, and some game designs.",
        "kinetic_art": "Art that involves physical movement or the illusion of movement. Can be mechanical, wind-powered, or digitally animated. Focus on the dynamic aspect.",
        "luna_photo": "Photographic style often involving the moon as a key element, possibly with double exposures, ethereal lighting, or surreal juxtapositions to create a dreamlike or mystical mood.",
        "mixed_media_journaling": "Simulate an art journal page. Combine sketches, paint, collage, text, stamps, and found objects. Layered, personal, and often experimental.",
        "nightcore": "Visuals associated with the Nightcore music subgenre. Often features anime characters, fast-paced effects, vibrant neon or pastel colors, and a high-energy, edgy, or futuristic feel.",
        "optic_art": "Op Art. Uses geometric patterns, precise lines, and color contrasts to create optical illusions of movement, vibration, or hidden imagery. Often black and white or high-contrast colors.",
        "paper_quilling": "Create images or patterns by rolling, shaping, and gluing strips of paper. Focus on intricate coils, delicate forms, and a 3D relief effect.",
        "patchwork_fabric": "Simulate a textile artwork made by sewing together pieces of fabric (patches). Emphasize fabric textures, stitch details, and varied patterns/colors.",
        "phygital_hybrid": "Art that blends physical and digital elements. Could be a physical object with digital projections, or a digital work that references or interacts with a physical counterpart.",
        "screen_printing_bold": "Emulate the look of screen printing (serigraphy). Bold graphics, flat areas of color (often limited palette), high contrast, and a slightly tactile, layered appearance.",
        "synesthesia_art": "Attempt to visually represent the experience of synesthesia (e.g., seeing sounds, tasting colors). Abstract, with color, shape, and movement used to evoke sensory crossovers.",
        "weirdcore": "Similar to dreamcore but often more unsettling, absurd, or amateurish in aesthetic. Uses found images, low-quality digital artifacts, and nonsensical juxtapositions to create an uncanny feeling.",

        # General Styles
        "cyberpunk_cityscape": "Vast, dense futuristic city with towering skyscrapers, abundant neon signs, holographic ads, rain, and a gritty, dystopian atmosphere. Night or perpetual twilight scenes are common.",
        "fantasy_landscape": "Depict magical, otherworldly environments: enchanted forests, floating islands, mystical mountains, ancient ruins. Lighting can be ethereal, with god rays or magical glows.",
        "line_art": "Focus on clean, precise outlines. Minimal to no shading or color fills. Emphasis is on the quality and expressiveness of the line itself. Can be technical or illustrative.",
        "3d_render": "Specify 3D software look (Blender, Maya), renderer (Cycles, Arnold, Octane), polycount, material properties (PBR, toon), and advanced lighting (HDRI, area lights).",
        "game_style": "Emulate the visual aesthetic of video games. Specify genre (RPG, FPS, retro), era (8-bit, modern AAA), or a specific game's style. Consider poly detail, shaders, and UI elements if relevant.",
        "cinematic": "Aim for a film still look. Consider aspect ratio (e.g., 2.39:1), color grading (e.g., teal & orange), depth of field, lens choice (anamorphic flares), and dramatic lighting.",
        "steampunk": "Victorian-era aesthetics combined with steam-powered machinery, gears, brass, copper, and intricate mechanical details. Colors are often muted browns, sepia, and bronze.",
        "illustration_pixar": "Vibrant colors, expressive characters with appealing designs, smooth 3D animation style, family-friendly mood. Focus on storytelling through visuals.",
        "illustration_disney": "Classic 2D or modern 3D animation style, warm colors, expressive faces, often with a storybook or musical feel. Strong character appeal.",
        "illustration_tom_jerry": "Classic slapstick cartoon style of Hanna-Barbera. Exaggerated expressions, dynamic poses, physical comedy, and a vintage feel.",
        "illustration_vintage_cartoon": "Rubber hose animation style (e.g., 1920s-1930s). Simple characters, often black and white or limited color, bouncy movements, nostalgic mood.",
        "illustration_anime_manga": "Distinctive character designs (large eyes, stylized hair), cel-shaded or soft shading, dynamic action poses or emotional close-ups. Backgrounds can be detailed or stylistic.",
        "illustration_comic": "Bold outlines, panel layouts (even if single image), dynamic compositions, often with dramatic lighting or action. Consider specific eras (Golden Age, Modern).",
        "illustration_pixel": "Low-resolution aesthetic, composed of individual pixels. Limited color palette typical of retro games (8-bit, 16-bit). Can be for characters, scenes, or UI elements.",
        "default": default_instruction
    }
    # Fallback for categories not explicitly listed
    return cat_instructions.get(category, default_instruction + f" Pay close attention to the nuances of '{base_style_clean}' when generating settings.")

