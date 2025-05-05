"""
style_category_catalog.py

This module contains all style category lists, hybrid mappings,
keyword definitions, AI prompt instructions per category, and utility 
functions for use in ai_preset_generator.py.
"""

import re

# --- Hybrid/Compound Style Mapping (Token-based) ---
hybrid_styles = {
    frozenset({'pop', 'surrealism'}): 'pop_surrealism',
    frozenset({'abstract', 'expressionism', 'cubism'}): 'abstract_expressionism_cubism_fusion',
    frozenset({'traditional', 'digital'}): 'hybrid_traditional_digital',
    frozenset({'collage', 'digital'}): 'collage_digital_overlay',
    frozenset({'experimental', 'mixed media'}): 'experimental_mixed_media',
    frozenset({'tradigital', 'mixed media'}): 'tradigital_mixed_media',
    frozenset({'whimsical', 'mixed media'}): 'whimsical_mixed_media',
    frozenset({'sci-fi', 'futuristic'}): 'sci_fi_futuristic'
    # Extend as needed
}

# --- Keyword-based Hybrid Category Definitions ---
hybrid_categories_keywords = {
    "kinetic_ascii": [ "kinetic + ascii", "ascii + kinetic", "kinetic art + ascii art", "ascii art + kinetic art", "kinetic with ascii", "ascii with kinetic", "ascii kinetic", "kinetic ascii" ],
    "watercolor_pencil": [
        "watercolor + pencil", "pencil + watercolor", "watercolor and pencil", "pencil and watercolor",
        "watercolor pencil", "pencil watercolor", "watercolor with pencil sketch", "pencil sketch with watercolor",
        "water colour + pencil", "pencil + water colour", "water colour and pencil", "pencil and water colour",
        "water colour pencil", "pencil water colour", "water colour with pencil sketch", "pencil sketch with water colour"
    ],
    "photorealism_glitch": [ "photorealism + glitch", "glitch + photorealism", "glitch art + photorealism", "photorealism and glitch", "glitch realistic", "realistic glitch art" ],
    "anime_oilpainting": [ "anime + oil painting", "oil painting + anime", "anime oil painting", "oil painting anime", "anime with oil painting", "oil painting with anime" ],
    "minimalist_geometric": [ "minimalist + geometric", "geometric + minimalist", "minimalist geometric", "geometric minimalist", "minimal geometric shapes", "minimalism", "minimalist", "minimal", "minimal art", "geometric", "geometry", "geometric abstract", "low poly", "minimalist geometric", "minimal geometric", "geometric minimalism" ],
    "pop_surrealism_ascii": [ "pop surrealism + ascii", "ascii + pop surrealism", "pop surrealism ascii", "ascii pop surrealism" ],
    "dreamcore_weirdcore": [ "dreamcore + weirdcore", "weirdcore + dreamcore", "dreamcore and weirdcore", "weirdcore and dreamcore" ],
    "patchwork_collage": [ "patchwork collage", "collage patchwork", "fabric collage", "mixed media collage", "paper collage" ],
    "paper_quilling": [ "paper quilling", "quilling art", "rolled paper art", "coil paper art" ],
    "tradigital_mixed_media": [ "tradigital mixed media", "digital and traditional mixed media", "tradigital art" ],
    "whimsical_mixed_media": [ "whimsical mixed media", "whimsical art", "dreamy mixed media", "fantasy mixed media" ],
    "sci_fi_futuristic": [ "sci-fi", "science fiction", "futuristic digital art", "cyberpunk", "dystopian digital art" ],
    "mediterranean_style": [ "mediterranean style", "sunny coastal art", "vivid colorful mediterranean" ],
    "morphism_surreal": [ "morphism", "surreal morphing art", "fantastical transformations" ],
    "cubism_mixed": [ "cubism", "cubist mixed media", "angular forms", "multiple perspectives" ],
    "pixel_patchwork": [ "pixel art", "pixel patchwork", "voxel art", "low poly pixel" ],
    "phygital_hybrid": [ "phygital art", "physical digital hybrid", "augmented reality art", "3d printing art" ],
    "screen_printing_bold": [ "screen printing", "bold graphic art", "tactile print art" ],
    "mixed_media_journaling": [ "mixed media journaling", "art journaling", "sketchbook mixed media" ],
    "digital_pixel_traditional": [ "digital pixel art", "pixel art with traditional media", "pixel and paint hybrid" ],
    "patchwork_fabric": [ "patchwork fabric", "fabric collage", "textile patchwork" ],
    "mixed_media_collage": [ "mixed media collage", "collage art", "assemblage mixed media", "mixed media", "collage", "assemblage", "combined media" ],
    "whimsical_fantasy": [ "whimsical fantasy", "fantasy whimsical art", "dreamlike whimsical" ],
    "cubism_futurism": [ "cubism futurism", "angular futurism", "geometric futurism" ],
    "digital_traditional_fusion": [ "digital traditional fusion", "hybrid digital traditional", "mixed media fusion" ],
    "retro_pixel_vaporwave": [ "retro pixel", "vaporwave pixel art", "synthwave pixel" ],
    "psychedelic_surrealism": [ "psychedelic surrealism", "trippy surreal art", "dreamlike psychedelic" ],
    "hybrid_traditional_digital": [ "hybrid traditional digital", "traditional digital fusion", "mixed traditional digital" ],
    "installation_art": [ "installation art", "immersive art", "spatial art", "mixed media installation" ],
    "scientific_technological_hybrid": [ "scientific hybrid art", "technological art", "data driven art", "algorithmic art", "ai art", "ar art", "vr art" ],
    "augmented_reality_art": [ "augmented reality art", "ar art", "mixed reality art", "interactive digital art" ],
    "abstract_expressionism_cubism_fusion": [ "abstract expressionism cubism", "abstract cubism fusion", "expressionist cubism" ],
    "collage_digital_overlay": [ "collage digital overlay", "digital collage", "photo manipulation collage" ],
    "experimental_mixed_media": [ "experimental mixed media", "avant-garde mixed media", "boundary pushing mixed media" ],
}

# --- General/Single-Term Category Keywords ---
categories_keywords = {
    # --- 3D Render/CGI Categories ---
    "3d_render": [
        "3d", "3d render", "3d modeling", "3d model", "3d illustration",
        "cgi", "c.g.i", "cg render", "clay render", "octane render", "arnold render",
        "blender", "maya", "cinema 4d", "unreal engine", "3ds max",
        "zbrush", "keyshot", "pixar style 3d", "toon 3d", "stylized 3d",
        "photoreal 3d", "3d portrait", "3d scene", "3d composition", "3d character", "3d environment"
    ],

    # --- Illustration/Cartoon Categories ---
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
    "ink_punk": ["ink punk", "inkpunk", "hand-drawn sketchy", "unfinished look"],

    # --- Portrait Categories ---
    "photographic_portrait": ["photographic portrait", "photo portrait", "realistic portrait"],
    "traditional_portrait": ["traditional portrait", "oil portrait", "watercolor portrait", "pastel portrait", "charcoal portrait"],
    "futuristic_portrait": ["futuristic portrait", "sci-fi portrait", "cyberpunk portrait"],
    "illustration_portrait": ["illustration portrait", "cartoon portrait", "anime portrait", "manga portrait"],
    "pop_portrait": ["pop portrait", "pop art portrait"],
    "environmental_portrait": [
        "environmental portrait", "on-location portrait", "location portrait", "in environment", "surroundings portrait", "contextual portrait"
    ],
    "caricature_portrait": [
        "caricature", "caricature portrait", "exaggerated portrait", "satirical portrait", "comic portrait"
    ],
    "conceptual_portrait": [
        "conceptual portrait", "concept portrait", "symbolic portrait", "metaphorical portrait", "abstract portrait", "idea-driven portrait"
    ],
    "fashion_portrait": [
        "fashion portrait", "editorial portrait", "runway portrait", "stylish portrait", "high-fashion portrait", "magazine portrait"
    ],
    "selfie_portrait": [
        "selfie", "selfie portrait", "self-portrait", "arm's length portrait", "smartphone portrait", "front camera portrait"
    ],

    # --- Painting/Drawing Categories ---
    "oil_painting": ["oil painting", "oil paint", "impasto", "alla prima", "wet-on-wet"],
    "watercolor": ["watercolor", "watercolour", "wet-on-wet", "wet-on-dry"],
    "pastel": ["pastel", "pastel drawing", "pastel painting"],
    "charcoal": ["charcoal sketch", "charcoal drawing", "charcoal art"],
    "pencil_sketch": ["pencil", "pencil sketch", "graphite", "pencil drawing"],
    "ink_drawing": ["ink drawing", "ink sketch", "pen and ink", "line drawing", "line art", "ink wash"],
    "acrylic_painting": ["acrylic", "acrylic paint", "acrylic painting"],
    "digital_painting": ["digital painting", "digital illustration", "digital art"],

    # --- Traditional Art Categories ---
    "traditional_painting_drawing": [
        "impressionist", "renaissance", "baroque", "rococo",
        "acrylic", "tempera", "art nouveau", "art deco",
        "cubism", "constructivism", "futurism", "pointillism", "divisionism",
        "ukiyo-e", "woodcut", "linocut", "etching"
    ],
    "realism": ["realism", "realistic", "photoreal", "hyperrealism", "photorealistic"],
    "abstract": ["abstract", "abstract art", "non-representational"],
    "expressionism": ["expressionism", "expressionist", "emotional art"],
    "surrealism": ["surrealism", "surreal", "dreamlike", "fantastical"],
    "cubism": ["cubism", "cubist", "geometric abstraction"],
    "fauvism": ["fauvism", "fauvist", "wild beasts"],
    "art_nouveau": ["art nouveau", "new art", "modern style"],
    "art_deco": ["art deco", "decop", "modernist"],
    "art_deco_revival": ["art deco revival", "art deco revival", "art deco style", "art deco architecture"],

    # --- Minimalist/Geometric Categories ---
    "constructivism": ["constructivism", "constructivist", "industrial art"],
    "low_poly": ["low poly", "low polygon", "polygonal art"],
    "isometric": ["isometric", "isometric view", "axonometric"],

    # --- Digital/Modern Categories ---
    "digital_art": [
        "digital art", "digital painting", "vector art", "glitch art",
        "vaporwave", "retrowave", "rendered", "digital illustration", "digital media"
    ],
    "psychedelic": ["psychedelic", "trippy", "hallucinogenic", "psychedelia", "acid art"],
    "cyberpunk": ["cyberpunk", "cyberpunk art", "futuristic", "neon city"],
    "retrowave": ["retrowave", "vaporwave", "80s revival", "synthwave"],
    "glitch_art": ["glitch art", "glitch effect", "digital glitch", "error art"],
    "vector_art": ["vector art", "vector illustration", "vector graphics"],

    # --- Game Art Categories ---
    "game_style": [
        "game style", "game art", "game engine", "unity", "unreal",
        "unreal engine", "unity engine", "pubg", "cyberpunk game",
        "fps", "rpg", "in-engine", "cel-shaded", "cyberpunk cityscape"
    ],
    "game_retro": ["retro game", "8-bit", "16-bit", "pixel art", "chunky pixels"],
    "game_cel_shaded": ["cel-shaded", "toon shading", "anime style", "cartoon style"],
    "game_3d": ["3d game", "3d engine", "realistic game", "next-gen game"],
    "game_indie": ["indie game", "indie art", "hand-drawn game"],

    # --- Photographic/Realism Categories ---
    "photographic": [
        "photo", "photograph", "photographic", "shot on", "dslr", "camera", "realistic",
        "film", "kodak", "fujifilm", "cinematic", "hyperrealism", "realism",
        "portrait photography", "landscape photography", "street photography"
    ],
    "cinematic": ["cinematic", "film look", "movie style", "motion picture"],
    "documentary": ["documentary", "documentary style", "journalistic"],
    "street_photography": ["street photography", "urban photography", "candid photography"],

    # --- Fantasy/Sci-Fi Categories ---
    "fantasy": ["fantasy", "mythical", "magical", "wizard", "fairy", "dragon", "unicorn", "fairy tale", "castle", "fantasy landscape"],
    "sci_fi": ["sci-fi", "science fiction", "spaceship", "space opera"],
    "space_art": ["space art", "astronomy art", "cosmic", "galaxy"],
    "robot_art": ["robot art", "mech art", "cybernetic", "mecha"],
    "steampunk": ["steampunk", "victorian sci-fi", "industrial fantasy"],
    "dystopian": ["dystopian", "post-apocalyptic", "dark future", "ruined world"],

    # --- New Single-Term Categories ---
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

preferred_order = [
    "illustration_pixar", "illustration_disney", "illustration_vintage_cartoon",
    "illustration_anime_manga", "illustration_comic", "illustration_pixel",
    "illustration_graphic", "illustration_childrens", "illustration_fantasy"
]

# The list of all style categories for random generation
all_categories = [
    "oil_painting", "watercolor", "pastel", "charcoal", "pencil_sketch", "ink_drawing",
    "minimalist_geometric", "illustration_pixel", "illustration_anime_manga", "illustration_comic",
    "photographic", "game_style", "digital_art", "abstract_conceptual", "material_sculptural",
    "fantasy", "sci_fi", "sci_fi_futuristic", "cyberpunk",
    "pop_surrealism", "papercraft", "kinetic_art", "watercolor_pencil",
    "photographic_portrait", "traditional_portrait", "futuristic_portrait",
    "illustration_portrait", "pop_portrait", "environmental_portrait",
    "caricature_portrait", "conceptual_portrait", "fashion_portrait", "selfie_portrait"
]

def instructions_for_category(style_category, base_style):
    # Centralizes per-category instruction messages as used by the AI prompt
    if style_category == "watercolor_pencil":
        return """*   **Watercolor Pencil Focus:**
        - Technique: Blend watercolor washes with distinct pencil lines. Soft edges vs sharp details.
        - Texture: Visible paper texture, light watercolor grain, graphite sheen.
        - Colors: Transparent washes, buildable layers, pencil shading.
        - Mood: Delicate, illustrative, sketched."""
    elif style_category == "minimalist_geometric":
        return """*   **Minimalist Geometric Focus:**
        - Style: Clean, simple geometric shapes (lines, circles, squares). Emphasis on negative space.
        - Colors: Often monochrome, muted palettes, or limited accent colors.
        - Composition: Balanced, orderly, potentially asymmetric.
        - Mood: Calm, modern, sophisticated, uncluttered."""
    elif style_category == "patchwork_collage":
        return """*   **Patchwork Collage Focus:**
        - Technique: Combine different textures/patterns like fabric scraps, paper cutouts. Layering.
        - Texture: Visible seams, fabric weave, paper edges, tactile feel.
        - Colors: Varied, can be harmonious or contrasting based on 'patches'.
        - Mood: Handcrafted, textured, eclectic, potentially folk-art inspired."""
    elif style_category == "sci_fi_futuristic":
        return """*   **Sci-Fi/Futuristic Focus:**
        - Elements: Advanced technology, spaceships, futuristic cities, cybernetics, aliens.
        - Lighting: Often high-contrast, neon glows, lens flares, artificial sources.
        - Colors: Can range from sleek monochrome/metallics to vibrant neon palettes.
        - Mood: Awe-inspiring, advanced, potentially dystopian or utopian."""
    elif style_category == "environmental_portrait":
        return """*   **Environmental Portrait Focus:**
        - Capture subject in meaningful surroundings; props and context add narrative.
        - Lighting: Use ambient/natural; situate subject in real environment (office, nature, city).
        - Storytelling: Emphasize environment/setting, not just face."""
    elif style_category == "caricature_portrait":
        return """*   **Caricature Portrait Focus:**
        - Exaggerate facial features for humor or satire.
        - Style: Bold lines, stylized exaggeration, cartoonish emotion.
        - Mood: Playful, humorous, comic-driven."""
    elif style_category == "conceptual_portrait":
        return """*   **Conceptual Portrait Focus:**
        - Center around an idea/concept; use symbols, surreal elements.
        - Style: Expressive, may include metaphors & visual motifs.
        - Mood: Thought-provoking, mysterious, abstract."""
    elif style_category == "fashion_portrait":
        return """*   **Fashion Portrait Focus:**
        - Emphasize clothing, accessories, and styling.
        - Lighting: Studio, runway, or high-fashion editorial.
        - Mood: Glamorous, trendy, striking poses."""
    elif style_category == "selfie_portrait":
        return """*   **Selfie Portrait Focus:**
        - Typically shot with phones, candid or posed.
        - Angle: Arm's length, playful, contemporary mood.
        - Often informal setting/background; may use filters."""
    elif style_category == "digital_art":
        return "*   **Digital Art Focus:** Flexible techniques (painting, vector, 3D non-game), studio/atmospheric lighting, digital effects, full color range."
    elif style_category == "psychedelic":
        return "*   **Psychedelic Focus:** Vibrant/neon colors, swirling/fractal patterns, glowing/morphing effects, trippy/surreal mood."
    elif style_category == "surrealism":
        return "*   **Surrealism Focus:** Dreamlike/bizarre concepts, symbolic colors/composition, mysterious/uncanny mood."
    elif style_category == "fantasy":
        return "*   **Fantasy Focus:** Mystical environments, magical lighting, rich/otherworldly colors, epic/adventurous mood."
    elif style_category == "cyberpunk":
        return "*   **Cyberpunk Focus:** Neon cities, high contrast lighting, dark/saturated colors, gritty/futuristic mood."
    elif style_category == "game_style":
        return "*   **Game Style Focus:** Game engine look (Unreal/Unity), game lighting/effects, game camera views, polished."
    elif style_category == "photographic":
        is_film = any(x in base_style.lower() for x in ["film", "kodak", "analog"])
        camera = "Film Camera" if is_film else "Digital Camera (e.g., Canon EOS R5)"
        return f"*   **Photographic Focus:** Suggest {camera}, appropriate lens, natural/studio light, {'film grain/analog look' if is_film else 'sharp/realistic'}."
    elif style_category.startswith("illustration"):
        return "*   **Illustration Focus:** Style-specific linework/colors (Pixar: vibrant, Disney: expressive, Anime: cel-shaded, Vintage: rubber hose), stylized lighting/perspective."
    elif style_category == "traditional_painting_drawing":
        return "*   **Traditional Medium:** Emphasize texture/brushwork, natural/atmospheric light, consider historical movements, traditional palettes."
    elif style_category == "abstract_conceptual":
        return "*   **Abstract Focus:** Non-representational form, expressive color, unconventional composition, modern art influences."
    elif style_category == "3d_render":
        return "*   **3D Render Focus:** Realistic or stylized 3D models, advanced lighting, detailed textures, cinematic composition."
    elif style_category == "illustration_pixar":
        return "*   **Pixar Illustration Focus:** Vibrant colors, expressive characters, smooth animation style, family-friendly mood."
    elif style_category == "illustration_disney":
        return "*   **Disney Illustration Focus:** Classic animation style, warm colors, expressive faces, storybook feel."
    elif style_category == "illustration_tom_jerry":
        return "*   **Tom & Jerry Style:** Classic slapstick cartoon, exaggerated expressions, dynamic poses, vintage feel."
    elif style_category == "illustration_vintage_cartoon":
        return "*   **Vintage Cartoon Focus:** Rubber hose animation style, muted colors, nostalgic mood."
    elif style_category == "illustration_anime_manga":
        return "*   **Anime/Manga Focus:** Cel-shaded characters, dynamic action poses, stylized backgrounds."
    elif style_category == "illustration_comic":
        return "*   **Comic Book Focus:** Bold lines, panel layouts, dramatic lighting, action-oriented."
    elif style_category == "illustration_pixel":
        return "*   **Pixel Art Focus:** Low resolution, limited color palette, retro game style."
    elif style_category == "illustration_graphic":
        return "*   **Graphic Illustration Focus:** Bold shapes, flat colors, modern design elements."
    elif style_category == "illustration_childrens":
        return "*   **Children's Book Illustration:** Soft colors, friendly characters, simple shapes."
    elif style_category == "illustration_fantasy":
        return "*   **Fantasy Illustration:** Mythical creatures, magical environments, rich colors."
    elif style_category == "ink_punk":
        return "*   **Ink Punk Focus:** Hand-drawn, sketchy lines, unfinished look, edgy style."
    elif style_category == "photographic_portrait":
        return "*   **Photographic Portrait:** Sharp focus, natural lighting, expressive subject."
    elif style_category == "traditional_portrait":
        return "*   **Traditional Portrait:** Oil or watercolor style, soft lighting, classic composition."
    elif style_category == "futuristic_portrait":
        return "*   **Futuristic Portrait:** Sci-fi elements, neon lighting, cyberpunk influences."
    elif style_category == "illustration_portrait":
        return "*   **Illustration Portrait:** Stylized features, bold lines, expressive colors."
    elif style_category == "pop_portrait":
        return "*   **Pop Art Portrait:** Bright colors, graphic style, bold shapes."
    elif style_category == "environmental_portrait":
        return """*   **Environmental Portrait Focus:**
        - Capture subject in meaningful surroundings; props and context add narrative.
        - Lighting: Use ambient/natural; situate subject in real environment (office, nature, city).
        - Storytelling: Emphasize environment/setting, not just face."""
    elif style_category == "caricature_portrait":
        return """*   **Caricature Portrait Focus:**
        - Exaggerate facial features for humor or satire.
        - Style: Bold lines, stylized exaggeration, cartoonish emotion.
        - Mood: Playful, humorous, comic-driven."""
    elif style_category == "conceptual_portrait":
        return """*   **Conceptual Portrait Focus:**
        - Center around an idea/concept; use symbols, surreal elements.
        - Style: Expressive, may include metaphors & visual motifs.
        - Mood: Thought-provoking, mysterious, abstract."""
    elif style_category == "fashion_portrait":
        return """*   **Fashion Portrait Focus:**
        - Emphasize clothing, accessories, and styling.
        - Lighting: Studio, runway, or high-fashion editorial.
        - Mood: Glamorous, trendy, striking poses."""
    elif style_category == "selfie_portrait":
        return """*   **Selfie Portrait Focus:**
        - Typically shot with phones, candid or posed.
        - Angle: Arm's length, playful, contemporary mood.
        - Often informal setting/background; may use filters."""
    elif style_category == "claymation":
        return """*   **Claymation Focus:**
        - Technique: Stop-motion animation using clay models.
        - Texture: Visible clay surface, fingerprints, and handcrafted details.
        - Colors: Earthy, muted tones with occasional bright accents.
        - Mood: Playful, tactile, handcrafted, nostalgic."""
    else:
        return "*   **General Guidance:** Choose settings matching the style, mood, and technical parameters."
