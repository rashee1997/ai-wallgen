"""
Style Category Catalog for AI Preset Generator (Merged & Improved)

This module contains the merged and refined data structures for categorizing
style names, combining the strengths of the user's original upload and the
enhanced V3 catalog. It aims for maximum style detection coverage.

Includes:
- A comprehensive preferred order for resolving category conflicts.
- Definitions for hybrid styles (token-based and keyword-based).
- Extensive keywords for identifying various art styles and categories.
- Instructions for the AI when generating presets for specific categories.
- A list of all defined categories for reference.
"""
import re
from typing import Dict, List, Set, Tuple, Union

# --- Comprehensive Preferred Order of Categories (Merged) ---
# Prioritizes specific styles, hybrids, portraits, then broader categories.
# Combines V3 order with unique entries from the restored version.
preferred_order: List[str] = [
    # Highly Specific Hybrids/Fusions (From V3 & Restored)
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
    "collage_digital_overlay",
    "pixel_patchwork",
    "tradigital_mixed_media",
    "hybrid_traditional_digital",
    "digital_traditional_fusion",
    "cubism_mixed", # From restored, specific mixed media

    # Specific Portraits (From V3 & Restored)
    "caricature_portrait",
    "selfie_portrait",
    "environmental_portrait",
    "fashion_portrait",
    "conceptual_portrait",
    "cyberpunk_portrait",
    "futuristic_portrait",
    "pop_portrait",
    "illustration_portrait",
    "photographic_portrait",
    "traditional_portrait",
    "fantasy_portrait",

    # Specific Thematic/Technical Styles (From V3 & Restored)
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
    "ink_punk",

    # Game Styles (From V3 & Restored)
    "game_cel_shaded",
    "game_retro", # (8-bit, 16-bit, pixel game art)
    "game_3d", # From restored
    "game_indie", # From restored
    "game_style", # General (Unity, Unreal, FPS, RPG etc.)

    # Cyberpunk (non-portrait) (From V3 & Restored)
    "cyberpunk_action",
    "cyberpunk_cityscape",
    "cyberpunk_technology",
    "cyberpunk", # General

    # Fantasy (non-portrait) (From V3 & Restored)
    "fantasy_battle",
    "fantasy_cityscape",
    "fantasy_landscape",
    "whimsical_fantasy",
    "fantasy", # General

    # Sci-Fi (non-portrait) (From V3 & Restored)
    "sci_fi_futuristic",
    "sci_fi", # General

    # Specific Mediums/Techniques (From V3 & Restored)
    "claymation",
    "digital_collage", # If not collage_digital_overlay
    "experimental_mixed_media",
    "patchwork_fabric",
    "patchwork_collage", # If not pixel_patchwork
    "mixed_media_collage", # From restored, broader than patchwork/digital
    "traditional_collage",        # NEW
    "papercraft", # General papercraft (if not quilling)
    "ascii_art", # If not kinetic_ascii or pop_surrealism_ascii
    "line_art", # Distinct from general drawing

    # Illustration Styles (non-portrait) (From V3 & Restored)
    "illustration_pixar",
    "illustration_disney",
    "illustration_tom_jerry",
    "illustration_vintage_cartoon",
    "illustration_anime_manga",
    "illustration_comic",
    "illustration_pixel", # if not game_retro or retro_pixel_vaporwave
    "illustration_steampunk",
    "illustration_cubist",
    "illustration_surreal",
    "illustration_childrens",
    "illustration_fantasy", # if not fantasy_portrait and more general fantasy
    "illustration_graphic", # General graphic illustration
    "illustration", # Broadest illustration

    # Painting Styles (Specific Mediums) (From V3 & Restored)
    "oil_painting", # if not anime_oilpainting
    "watercolor", # if not watercolor_pencil
    "pastel",
    "acrylic_painting",
    "gouache_painting",           # NEW
    "tempera_painting",           # NEW
    "digital_painting",

    # Drawing Styles (Specific Mediums) (From V3 & Restored)
    "pencil_sketch",
    "ink_drawing", # if not ink_punk or line_art
    "charcoal",
    "woodcut_print",              # NEW
    "drawing", # Broadest drawing

    # Photographic Styles (non-portrait) (From V3 & Restored)
    "street_photography",
    "documentary", # Photo style
    "cinematic",
    "macro_photography",        # NEW
    "wildlife_photography",     # NEW
    "food_photography",         # NEW
    "photographic", # General photographic

    # Abstract & Conceptual (non-portrait) (From V3 & Restored)
    "minimalist_geometric",
    "minimalist", # or "minimal"
    "geometric", # if not minimalist_geometric
    "constructivism",
    "low_poly",
    "abstract_conceptual", # Includes abstract from restored
    "abstract", # Keep as fallback if needed

    # Other Distinct Styles (From V3 & Restored)
    "pop_surrealism", # if not pop_surrealism_ascii or pop_portrait
    "surrealism", # if not specific hybrids/illustrations
    "cubism", # if not specific hybrids/illustrations
    "expressionism",
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

    # Material/Sculptural (From V3 & Restored)
    "material_sculptural",
    "sculpture",
    "mosaic_art",                 # NEW
    "stained_glass_art",          # NEW

    # Broad Digital/Traditional Categories (Fallbacks) (From V3 & Restored)
    "3d_render", # CGI, modeling
    "vector_art",
    "digital_art", # General digital art
    "traditional_painting_drawing", # Very broad

    # Meta/Other (From V3 & Restored)
    "animal_inspired",
    "space_art",
    "robot_art",

    "default",
    "unknown"
]
# De-duplicate the list while preserving order (important after merging)
seen_order = set()
preferred_order = [x for x in preferred_order if not (x in seen_order or seen_order.add(x))]


# --- Hybrid Style Definitions (Token-based - Merged) ---
hybrid_styles: Dict[frozenset[str], str] = {
    # From V3
    frozenset(["abstract", "expressionism", "cubism"]): "abstract_expressionism_cubism_fusion",
    frozenset(["anime", "oil", "painting"]): "anime_oilpainting",
    frozenset(["anime", "oilpaint"]): "anime_oilpainting",
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
    frozenset(["watercolour", "pencil"]): "watercolor_pencil",
    frozenset(["dreamcore", "weirdcore"]): "dreamcore_weirdcore",
    frozenset(["minimalist", "geometric"]): "minimalist_geometric",
    frozenset(["minimal", "geometric"]): "minimalist_geometric",
    frozenset(["photorealism", "glitch"]): "photorealism_glitch",
    frozenset(["photorealistic", "glitch"]): "photorealism_glitch",
    frozenset(["luna", "photo"]): "luna_photo",
    frozenset(["pop", "art", "portrait"]): "pop_portrait",
    frozenset(["cyberpunk", "city"]): "cyberpunk_cityscape",
    frozenset(["cyberpunk", "portrait"]): "cyberpunk_portrait",
    frozenset(["fantasy", "battle"]): "fantasy_battle",
    frozenset(["fantasy", "landscape"]): "fantasy_landscape",
    frozenset(["fantasy", "portrait"]): "fantasy_portrait",
    frozenset(["fantasy", "city"]): "fantasy_cityscape",
    frozenset(["sci", "fi", "futuristic"]): "sci_fi_futuristic",
    frozenset(["scifi", "futuristic"]): "sci_fi_futuristic",
    frozenset(["sci", "fi", "portrait"]): "futuristic_portrait",
    frozenset(["scifi", "portrait"]): "futuristic_portrait",
    frozenset(["mixed", "media", "collage"]): "mixed_media_collage",
    frozenset(["mixed", "media", "journaling"]): "mixed_media_journaling",
    frozenset(["sketchbook", "mixed", "media"]): "mixed_media_journaling",
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
    frozenset(["virtual", "reality", "art"]): "augmented_reality_art",
    frozenset(["augmented", "reality", "art"]): "augmented_reality_art",
    # From Restored (if not already present)
    frozenset({'pop', 'surrealism'}): 'pop_surrealism', # Already present in V3 keywords
    frozenset({'traditional', 'digital'}): 'hybrid_traditional_digital', # Already present
    frozenset({'collage', 'digital'}): 'collage_digital_overlay', # Already present
    frozenset({'sci-fi', 'futuristic'}): 'sci_fi_futuristic', # Already present
}

# --- Keyword-based Hybrid Category Definitions (Merged) ---
# Using V3 structure (List of Tuples) and merging keywords
hybrid_categories_keywords: Dict[str, List[Tuple[str, ...]]] = {
    "kinetic_ascii": [("kinetic", "ascii")],
    "watercolor_pencil": [("watercolor", "pencil"), ("watercolour", "pencil sketch"), ("watercolor", "pencil sketch")],
    "photorealism_glitch": [("photorealism", "glitch"), ("photorealistic", "glitch art")],
    "anime_oilpainting": [("anime", "oil painting"), ("manga", "oil painting")],
    "minimalist_geometric": [("minimalist", "geometric"), ("minimal", "geometric"), ("minimalism", "geometric")],
    "pop_surrealism_ascii": [("pop surrealism", "ascii")],
    "dreamcore_weirdcore": [("dreamcore", "weirdcore")],
    "patchwork_collage": [("patchwork", "collage"), ("fabric", "collage"), ("paper", "collage")], # Added from restored keywords
    "paper_quilling": [("paper", "quilling"), ("quilling", "art"), ("rolled", "paper"), ("coil", "paper")], # Added from restored
    "tradigital_mixed_media": [("tradigital", "mixed media"), ("tradigital", "art")], # Added from restored
    "whimsical_mixed_media": [("whimsical", "mixed media"), ("whimsical", "art"), ("dreamy", "mixed media"), ("fantasy", "mixed media")], # Added from restored
    "sci_fi_futuristic": [("sci-fi", "futuristic"), ("science fiction", "futuristic"), ("futuristic", "digital art"), ("cyberpunk", "futuristic"), ("dystopian", "futuristic")], # Merged
    "mediterranean_style": [("mediterranean", "style"), ("sunny", "coastal"), ("vivid", "mediterranean")], # Added from restored
    "morphism_surreal": [("morphism", "surreal"), ("surreal", "morphing"), ("fantastical", "transformation")], # Added from restored
    "cubism_mixed": [("cubism", "mixed media"), ("cubist", "mixed media"), ("angular", "mixed media")], # Added from restored
    "pixel_patchwork": [("pixel", "patchwork"), ("voxel", "patchwork"), ("low poly", "pixel")], # Added from restored
    "phygital_hybrid": [("phygital", "hybrid"), ("physical", "digital", "hybrid"), ("ar", "physical")], # Added from restored
    "screen_printing_bold": [("screen printing", "bold graphic"), ("serigraphy", "bold print"), ("tactile", "print")], # Added from restored
    "mixed_media_journaling": [("mixed media", "journaling"), ("art", "journaling"), ("sketchbook", "mixed media")],
    "digital_pixel_traditional": [("digital pixel", "traditional art"), ("pixel art", "traditional painting"), ("pixel", "paint", "hybrid")], # Added from restored
    "patchwork_fabric": [("patchwork", "fabric"), ("fabric", "collage"), ("textile", "patchwork")], # Added from restored
    "mixed_media_collage": [("mixed media", "collage"), ("collage", "art"), ("assemblage", "mixed media"), ("combined", "media")], # Added from restored
    "whimsical_fantasy": [("whimsical", "fantasy"), ("fantasy", "whimsical"), ("dreamlike", "whimsical")], # Added from restored
    "cubism_futurism": [("cubism", "futurism"), ("angular", "futurism"), ("geometric", "futurism")],
    "digital_traditional_fusion": [("digital", "traditional", "fusion"), ("hybrid", "digital", "traditional"), ("mixed media", "fusion")], # Added from restored
    "retro_pixel_vaporwave": [("retro pixel", "vaporwave"), ("pixel art", "vaporwave aesthetic"), ("synthwave", "pixel")], # Added from restored
    "psychedelic_surrealism": [("psychedelic", "surrealism"), ("trippy", "surreal art"), ("dreamlike", "psychedelic")], # Added from restored
    "hybrid_traditional_digital": [("hybrid", "traditional", "digital"), ("traditional", "digital", "fusion"), ("mixed", "traditional", "digital")], # Added from restored
    "installation_art": [("installation", "art"), ("immersive", "art"), ("spatial", "art"), ("mixed media", "installation")], # Added from restored
    "scientific_technological_hybrid": [("scientific", "technological", "hybrid"), ("data driven", "art"), ("algorithmic", "art"), ("ai", "art"), ("ar", "tech art"), ("vr", "tech art")], # Added from restored
    "augmented_reality_art": [("augmented reality", "art"), ("ar", "art"), ("mixed reality", "art"), ("interactive", "digital art")], # Added from restored
    "abstract_expressionism_cubism_fusion": [("abstract expressionism", "cubism"), ("abstract", "cubism", "fusion"), ("expressionist", "cubism")], # Added from restored
    "collage_digital_overlay": [("collage", "digital overlay"), ("digital", "collage"), ("photo manipulation", "collage")], # Added from restored
    "experimental_mixed_media": [("experimental", "mixed media"), ("avant-garde", "mixed media"), ("boundary pushing", "mixed media")], # Added from restored
}

# --- General Category Keywords (Merged) ---
# Combines keywords from both V3 and Restored catalogs for broader matching.
# Duplicates are removed automatically by converting to set and back to list.
_categories_keywords_v3 = { # Copied from V3 for merging
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
    "mediterranean_style": ["mediterranean painting", "tuscan scenery", "greek island visuals"],
    "animal_inspired": ["animal-inspired patterns", "animal motif artwork", "wildlife themed design"],
    "space_art": ["space exploration art", "astronomical illustration", "cosmic nebula painting", "galaxy artwork"],
    "robot_art": ["robot concept design", "mech warrior art", "cybernetic android illustration", "mecha drawing"],
    "game_cel_shaded": ["cel shaded game graphics", "toon shaded 3d models", "anime style video game"],
    "game_retro": ["retro video game art", "8-bit pixel graphics", "16-bit game design", "classic arcade style"],
    "game_style": ["video game concept art", "game environment design", "game character model", "unity game screenshot", "unreal engine visuals"],
    "cyberpunk_cityscape": ["cyberpunk city skyline", "neon lit urban future", "blade runner style city"],
    "cyberpunk_action": ["cyberpunk combat art", "sci-fi gunfight scene", "future fight concept"],
    "cyberpunk_technology": ["cyberpunk ui design", "holographic interface art", "future tech gadgets display"],
    "cyberpunk": ["cyberpunk genre art", "high tech low life visuals", "dystopian neon future"],
    "fantasy_battle": ["epic fantasy battle art", "mythical combat illustration", "dragon fight scene"],
    "fantasy_cityscape": ["magical city concept", "elven architecture design", "dwarven city illustration", "floating fantasy city"],
    "fantasy_landscape": ["enchanted forest painting", "mystical mountain range art", "alien planet environment"],
    "whimsical_fantasy": ["whimsical fairy tale art", "dreamy fantasy illustration", "lighthearted magical scene"],
    "fantasy": ["high fantasy art", "mythical creature illustration", "epic world building art", "sword and sorcery visuals"],
    "sci_fi_futuristic": ["advanced scifi technology", "space opera concept art", "far future civilization design"],
    "sci_fi": ["science fiction concept art", "futuristic vehicle design", "alien planet exploration", "spaceship interior"],
    "illustration_pixar": ["pixar animation style", "pixar character concept"],
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
    "oil_painting": ["oil painting technique", "oil on canvas art", "traditional oils"],
    "watercolor": ["watercolor painting", "watercolour art", "aquarelle technique"],
    "pastel": ["pastel portrait drawing", "pastel landscape art", "soft pastel technique", "oil pastel artwork"],
    "acrylic_painting": ["acrylic abstract painting", "acrylic on board", "modern acrylic art"],
    "digital_painting": ["digital painting illustration", "photoshop concept art", "procreate character design", "painterly digital art"],
    "pencil_sketch": ["graphite pencil sketch", "detailed pencil drawing", "realistic pencil portrait"],
    "ink_drawing": ["pen and ink illustration", "ink wash drawing", "black and white ink art", "hatching ink technique"],
    "charcoal": ["charcoal drawing medium", "charcoal art piece", "charcoal portrait sketch"],
    "line_art": ["clean line art", "outline illustration", "inking comic art", "vector line drawing"],
    "drawing": ["hand-drawn illustration", "traditional sketch artwork", "observational drawing"],
    "street_photography": ["candid street photography", "urban environment photos", "city life documentation"],
    "documentary": ["documentary photo series", "photojournalistic story", "reportage imagery"],
    "cinematic": ["cinematic shot composition", "film still photography", "movie scene aesthetic", "dramatic lighting photo"],
    "photographic": ["general photographic style", "realistic photo image", "dslr camera shot"],
    "constructivism": ["constructivist poster design", "geometric avant-garde art", "russian constructivism"],
    "low_poly": ["low poly 3d art", "faceted polygon design", "geometric minimalist 3d"],
    "abstract_conceptual": ["abstract conceptual painting", "idea-based visual representation", "symbolic abstract forms"],
    "abstract": ["abstract artwork", "non-objective painting", "abstract geometric patterns design"],
    "expressionism": ["expressionist painting", "emotive art style", "german expressionism"],
    "fauvism": ["fauvist color painting", "wild beast art movement", "matisse style fauvism"],
    "art_nouveau": ["art nouveau design", "jugendstil illustration", "organic flowing lines art"],
    "art_deco": ["art deco architecture", "gatsby style design", "modernist geometric patterns"],
    "material_sculptural": ["mixed material sculpture", "3d form installation", "textured sculptural art"],
    "sculpture": ["bronze sculpture", "marble statue", "clay modeling figure", "wood carving art"],
    "3d_render": ["3d render cgi", "computer generated imagery", "blender 3d scene", "maya character model", "3d visualization"],
    "vector_art": ["vector graphics illustration", "adobe illustrator art", "scalable vector design"],
    "digital_art": ["general digital artwork", "computer created art piece", "digital media creation"],
    "traditional_painting_drawing": ["classic art techniques", "traditional art media painting", "non-digital drawing methods"],
    "papercraft": ["3d papercraft model", "paper art sculpture", "kirigami cut paper", "origami animal"],
    "ascii_art": ["ascii text picture", "character art graphic", "terminal art image"],
    "default": ["standard style", "generic artwork", "basic visual design"],
    "unknown": ["undefined art style", "other category", "unclassified visual"],
}
_categories_keywords_restored = { # Copied from Restored for merging
    "3d_render": ["3d", "3d render", "3d modeling", "3d model", "3d illustration", "cgi", "c.g.i", "cg render", "clay render", "octane render", "arnold render", "blender", "maya", "cinema 4d", "unreal engine", "3ds max", "zbrush", "keyshot", "pixar style 3d", "toon 3d", "stylized 3d", "photoreal 3d", "3d portrait", "3d scene", "3d composition", "3d character", "3d environment"],
    "digital_collage": ["digital collage", "collage", "layered composition", "cut and paste", "scanned elements", "digital scraps", "montage", "composite", "mixed material collage"],
    "noir_photography": ["noir", "noir photography", "film noir", "black and white", "high contrast", "grainy", "low key lighting", "shadowy", "moody", "hardboiled"],
    "fractal_generative_art": ["fractal", "generative", "mandelbrot", "julia set", "recursion", "algorithmic art", "mathematical", "iterative pattern", "fractal gradient"],
    "folk_art": ["folk art", "traditional motif", "ethnic art", "decorative", "regional", "naive art", "cultural art", "handcrafted look", "ornamental"],
    "vr_ar_art": ["vr art", "ar art", "virtual reality", "augmented reality", "360 art", "immersive art", "3d immersive", "interactive media", "xr experience"],
    "sketchbook_mixed_media": ["sketchbook", "mixed media sketch", "pencil and ink", "wash and mark", "journaling art", "studio work-in-progress", "scribble layered", "inline notes", "informal study"],
    "line_art": ["line art", "lineart", "clean lines", "ink lines", "digital line art", "line drawing"],
    "illustration_pixar": ["pixar", "pixar style", "pixar animation"],
    "illustration_disney": ["disney", "disney style", "disney animation"],
    "illustration_tom_jerry": ["tom & jerry", "tom and jerry", "hanna-barbera"],
    "illustration_vintage_cartoon": ["vintage cartoon", "rubber hose", "1930s cartoon", "classic cartoon"],
    "illustration_anime_manga": ["anime", "manga", "shonen", "shojo", "seinen", "japanese animation"],
    "illustration_comic": ["comic", "comic book", "comic strip", "sequential art"],
    "illustration_pixel": ["pixel art", "8-bit", "16-bit", "pixelated", "retro game art"],
    "illustration_graphic": ["illustration", "cartoon", "cartoony", "graphic novel"],
    "illustration_childrens": ["children's book", "picture book", "kids illustration"],
    "illustration_fantasy": ["fantasy illustration", "mythical", "magical creatures"],
    "illustration_cubist": ["cubist illustration", "geometric illustration", "fragmented illustration", "cubist", "cubism"],
    "illustration_surreal": ["surreal illustration", "dreamlike illustration", "fantastical illustration", "surreal"],
    "illustration_steampunk": ["steampunk illustration", "victorian sci-fi illustration", "industrial fantasy illustration", "steampunk"],
    "ink_punk": ["ink punk", "inkpunk", "hand-drawn sketchy", "unfinished look"],
    "photographic_portrait": ["photographic portrait", "photo portrait", "realistic portrait"],
    "traditional_portrait": ["traditional portrait", "oil portrait", "watercolor portrait", "pastel portrait", "charcoal portrait"],
    "futuristic_portrait": ["futuristic portrait", "sci-fi portrait", "cyberpunk portrait"],
    "illustration_portrait": ["illustration portrait", "cartoon portrait", "anime portrait", "manga portrait"],
    "pop_portrait": ["pop portrait", "pop art portrait"],
    "environmental_portrait": ["environmental portrait", "on-location portrait", "location portrait", "in environment", "surroundings portrait", "contextual portrait"],
    "caricature_portrait": ["caricature", "caricature portrait", "exaggerated portrait", "satirical portrait", "comic portrait"],
    "conceptual_portrait": ["conceptual portrait", "concept portrait", "symbolic portrait", "metaphorical portrait", "abstract portrait", "idea-driven portrait"],
    "fashion_portrait": ["fashion portrait", "editorial portrait", "runway portrait", "stylish portrait", "high-fashion portrait", "magazine portrait"],
    "selfie_portrait": ["selfie", "selfie portrait", "self-portrait", "arm's length portrait", "smartphone portrait", "front camera portrait"],
    "oil_painting": ["oil painting", "oil paint", "impasto", "alla prima", "wet-on-wet"],
    "watercolor": ["watercolor", "watercolour", "wet-on-wet", "wet-on-dry"],
    "pastel": ["pastel", "pastel drawing", "pastel painting"],
    "charcoal": ["charcoal sketch", "charcoal drawing", "charcoal art"],
    "pencil_sketch": ["pencil", "pencil sketch", "graphite", "pencil drawing"],
    "ink_drawing": ["ink drawing", "ink sketch", "pen and ink", "line drawing", "line art", "ink wash"],
    "acrylic_painting": ["acrylic", "acrylic paint", "acrylic painting"],
    "digital_painting": ["digital painting", "digital illustration", "digital art"],
    "traditional_painting_drawing": ["impressionist", "renaissance", "baroque", "rococo", "acrylic", "tempera", "art nouveau", "art deco", "cubism", "constructivism", "futurism", "pointillism", "divisionism", "ukiyo-e", "woodcut", "linocut", "etching"],
    "realism": ["realism", "realistic", "photoreal", "hyperrealism", "photorealistic"],
    "abstract": ["abstract", "abstract art", "non-representational"],
    "expressionism": ["expressionism", "expressionist", "emotional art"],
    "surrealism": ["surrealism", "surreal", "dreamlike", "fantastical"],
    "cubism": ["cubism", "cubist", "geometric abstraction"],
    "fauvism": ["fauvism", "fauvist", "wild beasts"],
    "art_nouveau": ["art nouveau", "new art", "modern style"],
    "art_deco": ["art deco", "decop", "modernist"],
    "art_deco_revival": ["art deco revival", "art deco revival", "art deco style", "art deco architecture"],
    "constructivism": ["constructivism", "constructivist", "industrial art"],
    "low_poly": ["low poly", "low polygon", "polygonal art"],
    "isometric": ["isometric", "isometric view", "axonometric"],
    "digital_art": ["digital art", "digital painting", "vector art", "glitch art", "vaporwave", "retrowave", "rendered", "digital illustration", "digital media"],
    "psychedelic": ["psychedelic", "trippy", "hallucinogenic", "psychedelia", "acid art"],
    "cyberpunk": ["cyberpunk", "cyberpunk art", "futuristic", "neon city"],
    "retrowave": ["retrowave", "vaporwave", "80s revival", "synthwave"],
    "glitch_art": ["glitch art", "glitch effect", "digital glitch", "error art"],
    "vector_art": ["vector art", "vector illustration", "vector graphics"],
    "game_style": ["game style", "game art", "game engine", "unity", "unreal", "unreal engine", "unity engine", "pubg", "cyberpunk game", "fps", "rpg", "in-engine", "cel-shaded", "cyberpunk cityscape"],
    "game_retro": ["retro game", "8-bit", "16-bit", "pixel art", "chunky pixels"],
    "game_cel_shaded": ["cel-shaded", "toon shading", "anime style", "cartoon style"],
    "game_3d": ["3d game", "3d engine", "realistic game", "next-gen game"],
    "game_indie": ["indie game", "indie art", "hand-drawn game"],
    "photographic": ["photo", "photograph", "photographic", "shot on", "dslr", "camera", "realistic", "film", "kodak", "fujifilm", "cinematic", "hyperrealism", "realism", "portrait photography", "landscape photography", "street photography"],
    "cinematic": ["cinematic", "film look", "movie style", "motion picture"],
    "documentary": ["documentary", "documentary style", "journalistic"],
    "street_photography": ["street photography", "urban photography", "candid photography"],
    "fantasy": ["fantasy", "mythical", "magical", "wizard", "fairy", "dragon", "unicorn", "fairy tale", "castle", "fantasy landscape"],
    "sci_fi": ["sci-fi", "science fiction", "spaceship", "space opera"],
    "space_art": ["space art", "astronomy art", "cosmic", "galaxy"],
    "robot_art": ["robot art", "mech art", "cybernetic", "mecha"],
    "steampunk": ["steampunk", "victorian sci-fi", "industrial fantasy"],
    "dystopian": ["dystopian", "post-apocalyptic", "dark future", "ruined world"],
    "papercraft": ["papercraft", "paper cut", "folded paper", "layered paper", "glued paper"],
    "luna_photo": ["luna photo", "double exposure", "surreal photographic", "ethereal photo"],
    "pop_surrealism": ["pop surrealism", "lowbrow art", "cartoon surrealism", "fantastical pop art"],
    "synesthesia_art": ["synesthesia art", "color sound fusion", "sensory blending art"],
    "weirdcore": ["weirdcore", "surreal glitch", "dreamlike glitch", "uncanny art"],
    "dreamcore": ["dreamcore", "dreamlike aesthetic", "ethereal dream art"],
    "ferrofluid": ["ferrofluid", "magnetic fluid art", "liquid metal art"],
    "animal_inspired": ["animal inspired", "animal motif", "fauna art", "wildlife art"],
    "ascii_art": ["ascii art", "text art", "character art", "typographic art"],
    "biopunk": ["biopunk", "biological cyberpunk", "genetic art", "bio-tech art"],
    "kinetic_art": ["kinetic art", "moving art", "dynamic sculpture", "motion art"],
    "nightcore": ["nightcore", "fast paced art", "high energy art", "vibrant neon art"],
    "optic_art": ["optic art", "op art", "optical illusion art", "visual trickery"],
    "claymation": ["claymation", "stop motion", "clay animation", "clay figure animation"],
    "unknown": []
}

# Add new keywords here, before the categories_keywords initialization loop
_new_traditional_keywords = {
    "gouache_painting": ["gouache", "gouache painting", "opaque watercolor", "bodycolor", "designer's gouache"],
    "tempera_painting": ["tempera", "tempera painting", "egg tempera", "casein tempera"],
    "mosaic_art": ["mosaic", "mosaic art", "tessellation", "tesserae", "tile mosaic", "glass mosaic", "stone mosaic", "byzantine mosaic", "roman mosaic"],
    "stained_glass_art": ["stained glass", "stained glass art", "leaded glass", "cathedral glass", "glass painting (traditional)"],
    "woodcut_print": ["woodcut", "woodcut print", "woodblock print", "relief print wood", "xylography"],
    "traditional_collage": ["traditional collage", "physical collage", "paper collage", "fabric collage", "analog collage", "assemblage art", "found object collage", "cut and paste (physical)"]
}

categories_keywords: Dict[str, List[str]] = {}
for cat, keywords in _categories_keywords_v3.items():
    categories_keywords.setdefault(cat, []).extend(keywords)
for cat, keywords in _categories_keywords_restored.items(): # This will include the "unknown" placeholder
    categories_keywords.setdefault(cat, []).extend(keywords)
for cat, keywords in _new_traditional_keywords.items(): # Add new traditional keywords
    categories_keywords.setdefault(cat, []).extend(keywords)

_new_photographic_keywords = {
    "macro_photography": ["macro", "macro photo", "macro photography", "extreme close up", "close-up photography", "micro photography", "tiny details", "insect eye", "flower stamen"],
    "wildlife_photography": ["wildlife", "wildlife photo", "wildlife photography", "animal photography", "nature photography animals", "safari photography", "birdwatching photo", "animal in habitat"],
    "food_photography": ["food photography", "culinary photography", "food styling", "appetizing food shot", "delicious food", "gourmet dish photo", "food blog photo", "menu photo", "foodie"]
}
for cat, keywords in _new_photographic_keywords.items(): # Add new photographic keywords
    categories_keywords.setdefault(cat, []).extend(keywords)

# De-duplicate keywords within each category (ensure this loop runs AFTER all additions)
for cat in categories_keywords:
    seen_keywords = set()
    categories_keywords[cat] = [kw for kw in categories_keywords[cat] if not (kw in seen_keywords or seen_keywords.add(kw))]

# --- All Categories List (Dynamically Generated - Merged) ---
def get_all_defined_categories() -> List[str]:
    """Returns a sorted list of all unique category names defined in this merged catalog."""
    _all_cats: Set[str] = set(preferred_order) # Start with merged preferred order
    _all_cats.update(hybrid_styles.values())
    _all_cats.update(hybrid_categories_keywords.keys())
    _all_cats.update(categories_keywords.keys())
    return sorted(list(_all_cats))

all_categories: List[str] = get_all_defined_categories()

# --- Instructions for AI based on Category (Merged) ---
# Using the more detailed V3 version and adding/merging instructions from restored if needed
def instructions_for_category(category: str, base_style: str) -> str:
    """Return specific instructions for the AI based on the detected style category."""
    category = category.lower()
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

    # Base instructions from V3 (more comprehensive)
    cat_instructions_v3: Dict[str, str] = {
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
        "patchwork_collage": """* **Patchwork Collage Focus:**
        - Technique: Combine different textures/patterns like fabric scraps, paper cutouts. Layering.
        - Texture: Visible seams, fabric weave, paper edges, tactile feel.
        - Colors: Varied, can be harmonious or contrasting based on 'patches'.
        - Mood: Handcrafted, textured, eclectic, potentially folk-art inspired.""", # From restored
        "whimsical_mixed_media": """* **Whimsical Mixed Media Focus:**
        - Motifs: mythical creatures, soft colors, playful elements, stars
        - Texture: light airy layered textures
        - Color Palette: pastel dreamy colors
        - Aesthetic Blend: Lighthearted, dreamy compositions with fantasy elements and playful accents.""", # Merged
        "mediterranean_style": """* **Mediterranean Style Focus:**
        - Environment: sunny coastal scenes vibrant landscapes
        - Color Palette: warm bright natural colors (blues, whites, terracotta)
        - Lighting: bright natural sunlight warm glow
        - Aesthetic Blend: Vivid, colorful depictions of Mediterranean life, architecture, and scenery.""", # Merged
        "morphism_surreal": """* **Morphism Surreal Focus:**
        - Transformation Style: surreal fluid fantastical morphing
        - Color Palette: vibrant dreamlike colors
        - Composition: morphing shapes illogical progressions
        - Aesthetic Blend: Surreal transformations where objects fluidly blend or change form with fantastical and dreamlike qualities.""", # Merged
        "cubism_mixed": """* **Cubism Mixed Focus:**
        - Form Style: angular fragmented forms with multiple perspectives
        - Color Palette: muted earthy tones with bold accents
        - Composition: geometric abstraction with layered planes and mixed media textures
        - Aesthetic Blend: Classic Cubist style principles combined with mixed media elements and modern influences.""", # Merged
        "pixel_patchwork": """* **Pixel Patchwork Focus:**
        - Pixel Style: pixel art combined with voxel art elements
        - Color Palette: limited vibrant 8-bit palette
        - Texture: blocky geometric pixelated texture
        - Aesthetic Blend: Pixelated and geometric patchwork style combining digital retro motifs with quilt-like composition.""", # Merged
        "phygital_hybrid": """* **Phygital Hybrid Focus:**
        - Media Fusion: physical sculpture combined with augmented reality digital art
        - Technology: AR tracking with 3D printing elements
        - Aesthetic Blend: Hybrid physical/digital artwork blending real object presence with interactive virtual elements.""", # Merged
        "screen_printing_bold": """* **Screen Printing Bold Focus:**
        - Print Style: bold graphic tactile screen print
        - Color Palette: limited high contrast colors (e.g., 2-3 colors)
        - Texture: flat layered ink texture with slight misregistration effect
        - Aesthetic Blend: Bold graphic prints reminiscent of serigraphy with tactile qualities and strong visual contrasts.""", # Merged
        "digital_pixel_traditional": """* **Digital Pixel Traditional Focus:**
        - Media Fusion: digital pixel art characters combined with traditional painted background
        - Color Palette: vibrant mixed palette (pixelated foreground, painterly background)
        - Texture: pixelated character texture contrasted with painterly background texture
        - Aesthetic Blend: Fusion of distinct pixel art style for subjects and traditional painting techniques for environment.""", # Merged
        "patchwork_fabric": """* **Patchwork Fabric Focus:**
        - Material: various fabric textiles
        - Assembly: sewn and layered fabric patches
        - Texture: soft tactile fabric textures
        - Color Palette: warm earthy fabric colors
        - Aesthetic Blend: Textile patchwork art with warm, tactile qualities and visible stitching.""", # Merged
        "mixed_media_collage": """* **Mixed Media Collage Focus:**
        - Media: paper cutouts, acrylic paint, found objects, fabric scraps
        - Texture: highly layered tactile textures
        - Color Palette: varied eclectic color palette
        - Aesthetic Blend: Eclectic collage combining diverse physical media and textures into a cohesive piece.""", # Merged
        "whimsical_fantasy": """* **Whimsical Fantasy Focus:**
        - Motifs: fantasy creatures (fairies, sprites), pastel colors, dreamy atmosphere, sparkling elements
        - Texture: soft layered textures with glittery effects
        - Color Palette: pastel soft color palette
        - Aesthetic Blend: Dreamy fantasy illustration style with playful characters and soft, whimsical elements.""", # Merged
        "cubism_futurism": """* **Cubism Futurism Focus:**
        - Form Style: angular geometric dynamic forms
        - Color Palette: muted metallic colors with dynamic lines
        - Composition: layered fragmented planes suggesting motion
        - Aesthetic Blend: Fusion of cubist fragmentation and futurist dynamism/speed.""", # Merged
        "digital_traditional_fusion": """* **Digital Traditional Fusion Focus:**
        - Media Fusion: digital painting techniques combined with traditional drawing aesthetics
        - Texture: layered digital textures mimicking traditional media
        - Color Palette: varied rich color palette blending digital and traditional hues
        - Aesthetic Blend: Rich fusion of digital painting capabilities and traditional artistic sensibilities.""", # Merged
        "retro_pixel_vaporwave": """* **Retro Pixel Vaporwave Focus:**
        - Style: retro pixel art combined with vaporwave aesthetics
        - Color Palette: neon pastel vibrant vaporwave colors
        - Texture: pixelated texture with glitch effects
        - Aesthetic Blend: Retro pixel art (e.g., 16-bit style) infused with vaporwave elements like neon grids, classical statues, and glitch artifacts.""", # Merged
        "psychedelic_surrealism": """* **Psychedelic Surrealism Focus:**
        - Motifs: trippy surreal dreamlike imagery
        - Color Palette: vibrant neon contrasting psychedelic colors
        - Visual Effects: glowing elements, morphing shapes, fractal patterns
        - Aesthetic Blend: Intense, swirling psychedelic visuals combined with illogical surreal dreamscapes and transformations.""", # Merged
        "digital_painting": "* **Digital Painting Focus:** Flexible techniques (painting, vector, 3D non-game), studio/atmospheric lighting, digital effects, full color range.", # From restored
        "traditional_painting_drawing": "* **Traditional Medium:** Emphasize texture/brushwork, natural/atmospheric light, consider historical movements, traditional palettes.", # From restored
        "abstract_conceptual": "* **Abstract Focus:** Non-representational form, expressive color, unconventional composition, modern art influences.", # From restored
        "abstract": "* **Abstract Focus:** Non-representational form, expressive color, unconventional composition, modern art influences.", # Alias
        "default": default_instruction,
        "gouache_painting": (
            f"For '{base_style_clean}', emphasize its unique opaque watercolor quality. "
            "Characteristics: matte finish, vibrant flat colors, ability to layer light over dark. "
            "Lighting: Even, diffused to show off matte surface. "
            "Colors: Opaque, bold, good for illustration or expressive work. "
            "Detail: Can range from graphic shapes to fine details. "
            "Avoid: Streaky application, unintended transparency, overly shiny effects."
        ),
        "tempera_painting": (
            f"For '{base_style_clean}', capture the essence of tempera, often egg tempera. "
            "Characteristics: Matte or subtle satin sheen, luminous colors, fine detail, cross-hatching for modeling. "
            "Lighting: Soft, clear, directional to show form. "
            "Colors: Rich, can be built up in thin layers. Historically important palette. "
            "Detail: Excellent for precise lines and intricate work. "
            "Avoid: Oily look, modern impasto, smudging (it dries fast)."
        ),
        "mosaic_art": (
            f"For '{base_style_clean}', focus on the assembled nature of mosaic. "
            "Characteristics: Composed of small pieces (tesserae – tiles, glass, stone), visible grout lines, textured surface. "
            "Lighting: Directional to highlight texture and individual pieces. "
            "Colors: Segmented, can be vibrant or earthy depending on materials. "
            "Composition: Often figurative, geometric, or decorative patterns. "
            "Avoid: Smooth, painted appearance; indistinct tesserae; blended colors between pieces."
        ),
        "stained_glass_art": (
            f"For '{base_style_clean}', convey the effect of light passing through colored glass. "
            "Characteristics: Translucent, vibrant jewel-like colors, strong black outlines (leading). "
            "Lighting: Backlit, emphasizing transmitted light, potential for caustics or light rays. "
            "Colors: Pure, luminous, often with high contrast. "
            "Composition: Figurative or abstract, designed by lead lines. "
            "Avoid: Opaque appearance, muddy colors, missing lead lines, front lighting that negates translucency."
        ),
        "woodcut_print": (
            f"For '{base_style_clean}', emulate the relief printmaking technique of woodcut. "
            "Characteristics: Bold lines, strong contrast (often black and white), visible wood grain texture sometimes, areas of flat color if multi-block. "
            "Lighting: Not directly applicable; style is about ink on paper. "
            "Colors: Typically monochromatic or limited color palette. "
            "Composition: Graphic, relies on positive/negative space. "
            "Avoid: Fine shading, photographic realism, pencil sketch appearance, excessive detail not typical of the medium."
        ),
        "traditional_collage": (
            f"For '{base_style_clean}', emphasize the physical assembly of materials. "
            "Characteristics: Layered paper, fabric, found objects; visible cut or torn edges; varied textures. "
            "Lighting: Soft studio lighting to show texture and slight depth between layers. "
            "Colors: Eclectic, depends on the source materials. "
            "Composition: Juxtaposition of disparate elements. "
            "Avoid: Digital appearance, seamless blending of elements, flat look without depth cues. Distinguish from purely digital collage."
        ),
        "whimsical_mixed_media": """* **Whimsical Mixed Media Focus:**
        - Motifs: mythical creatures, soft colors, playful elements, stars
        - Texture: light airy layered textures
        - Color Palette: pastel dreamy colors
        - Aesthetic Blend: Lighthearted, dreamy compositions with fantasy elements and playful accents."""
    }

    # Get instruction from the merged dictionary, fallback to default
    instruction = cat_instructions_v3.get(category)

    # If not found in V3, check the simpler restored instructions (less likely needed now but for safety)
    if not instruction:
         if category == "watercolor_pencil": instruction = cat_instructions_v3.get("watercolor_pencil") # Already covered
         elif category == "minimalist_geometric": instruction = cat_instructions_v3.get("minimalist_geometric") # Already covered
         elif category == "patchwork_collage": instruction = cat_instructions_v3.get("patchwork_collage") # Already covered
         # ... add other specific fallbacks from restored if necessary ...
         elif category == "macro_photography":
            instruction = (
                f"For '{base_style_clean}', generate settings for extreme close-up photography. "
                "Key Characteristics: Reveal intricate details, textures, and patterns of tiny subjects. Extremely shallow depth of field is a hallmark, isolating the subject against a blurred background (bokeh). "
                "Lighting: Precise and often artificial (ring flash, twin flash, diffused LED) to illuminate tiny subjects without harsh shadows, or soft, diffused natural light. "
                "Composition: Fill the frame with the subject, focus on abstract patterns, or isolate a single minute detail. "
                "Subject Matter: Insects, flower parts (stamens, petals), water droplets, snowflakes, textures of everyday objects, miniature worlds. "
                "Camera Settings: True macro lens (1:1 magnification or greater), small apertures (e.g., f/8-f/16) if focus stacking is implied for greater DoF, or wider for extreme shallow DoF. Fast shutter speed if subject is mobile or to counter camera shake. Low ISO. "
                "Focus: Critically sharp on the primary point of interest. "
                "Avoid: Distracting backgrounds, deep depth of field (unless focus stacked), motion blur (unless intentional)."
            )
         elif category == "wildlife_photography":
            instruction = (
                f"For '{base_style_clean}', generate settings for capturing animals in their natural habitat. "
                "Key Characteristics: Authentic depiction of animal behavior and appearance. Patience and respect for the subject are paramount. Often uses telephoto lenses. "
                "Lighting: Natural available light. Golden hours (early morning, late afternoon) are preferred for warm, dimensional light. Overcast days for soft, even light. Avoid harsh midday sun. "
                "Composition: Eye-level with the subject for connection. Rule of thirds, leading lines, negative space. Show animal interacting with its environment. Capture behavior (hunting, playing, resting). "
                "Subject Matter: Mammals, birds, reptiles, amphibians, fish, insects in their native environments. "
                "Camera Settings: Telephoto lens (e.g., 200mm to 600mm+). Fast shutter speed to freeze action. Aperture chosen for desired DoF (isolate subject or show habitat). ISO may be higher in low light. Continuous autofocus and burst mode are common. "
                "Focus: Critically sharp on the animal's eyes. "
                "Avoid: Cages, human interference (unless part of a specific documentary narrative), unnatural poses, overly intrusive presence."
            )
         elif category == "food_photography":
            instruction = (
                f"For '{base_style_clean}', generate settings to make the food look as appetizing as possible. "
                "Key Characteristics: Careful styling of food and props. Emphasis on texture, color, and freshness. "
                "Lighting: Soft, diffused natural light (e.g., window light) is popular. Controlled studio light (softboxes, reflectors, scrims) for specific moods. Avoid direct on-camera flash. "
                "Light Direction: Side lighting or backlighting is common to create texture, highlights, and dimension. Top-down for flat lays. "
                "Composition: Overhead flat lay, 45-degree angle, eye-level for drinks/tall dishes, close-ups on textures. Rule of thirds, leading lines, use of negative space. Props (cutlery, linens, ingredients) should complement, not distract. "
                "Subject Matter: Plated dishes, ingredients, drinks, culinary processes. "
                "Camera Settings: Macro or short telephoto lenses are common. Aperture chosen for desired DoF (f/2.8-f/8 typical). Low ISO. Tripod often used. "
                "Focus: Sharp focus on the 'hero' element of the dish. "
                "Color: Vibrant, appetizing, and true to the food. White balance is critical. "
                "Avoid: Unappetizing colors, harsh shadows, distracting reflections, messy presentation (unless intentionally rustic), wilted or stale-looking food."
            )
         else: instruction = default_instruction + f" Pay close attention to the nuances of '{base_style_clean}' when generating settings."

    return instruction
