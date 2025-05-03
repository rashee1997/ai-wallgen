"""Consolidated configuration file for AI Wallpaper Generator."""

# Define tag lists for prompt generation (from prompt_config.py)
nature_tags = [
    "landscape", "nature", "mountains", "forest", "trees", "waterfall", "ocean",
    "sea", "lake", "river", "sky", "clouds", "sunset", "sunrise", "stars",
    "moon", "flowers", "plants", "grass", "leaves", "wildlife", "animals",
    "birds", "insects", "butterfly", "deer", "fox", "bear", "wolf", "eagle",
    "meadow", "valley", "canyon", "desert", "rain", "snow", "ice", "mist",
    "fog", "rainbow", "aurora", "volcano", "cave", "beach", "coast", "island",
    "jungle", "rainforest", "savanna", "tundra", "alpine", "coral reef",
    "redwood forest", "bamboo forest", "cherry blossoms", "autumn leaves",
    "pine forest", "tropical island", "mountain peak", "rolling hills",
    "sand dunes", "oasis", "geysers", "hot springs", "glaciers", "icebergs"
]

space_tags = [
    "space", "planet", "galaxy", "star", "astronaut", "rocket", "planetarium",
    "cosmos", "universe", "nebula", "black hole", "supernova", "comet",
    "satellite", "telescope", "astronomy", "cosmic", "interstellar", "orbiter",
    "constellation", "celestial", "starry", "astral", "cosmic", "spacecraft",
    "space station", "spacewalk", "space shuttle", "space probe", "milky way",
    "solar system", "exoplanet", "asteroid field", "meteor shower", "lunar surface",
    "mars landscape", "jupiter clouds", "saturn rings", "deep space", "galactic core",
    "quasar", "pulsar", "wormhole", "space-time", "event horizon", "cosmic dust"
]

sea_tags = [
    "sea", "ocean", "beach", "coast", "waves", "sunset", "sunrise", "tide",
    "current", "ship", "boat", "fishing", "sailboat", "yacht", "maritime",
    "navigation", "shipwreck", "cruise", "sailing", "seafarer", "seafaring",
    "coral reef", "tropical fish", "underwater scene", "deep sea", "ocean floor",
    "marine life", "sea turtle", "dolphin", "whale", "shark", "jellyfish", "octopus",
    "seashell", "starfish", "seaweed", "anemone", "lagoon", "atoll", "bay", "cove",
    "harbor", "lighthouse", "pier", "dock", "marina", "sea cave", "cliff coast"
]

flowers_tags = [
    "flowers", "rose", "tulip", "daisy", "sunflower", "lily", "orchid",
    "dahlia", "chrysanthemum", "carnation", "aster", "iris", "lavender",
    "marigold", "petunia", "zinnia", "gerbera", "hydrangea", "begonia",
    "cherry blossom", "lotus", "poppy", "peony", "hibiscus", "magnolia",
    "wildflowers", "meadow flowers", "spring blooms", "flower garden",
    "floral arrangement", "bouquet", "flower field", "tropical flowers",
    "desert bloom", "alpine flowers", "water lily", "morning glory"
]

urban_tags = [
    "cityscape", "skyline", "skyscraper", "architecture", "building", "street",
    "urban", "city", "downtown", "metropolis", "bridge", "tower", "monument",
    "plaza", "avenue", "alley", "rooftop", "subway", "train station", "airport",
    "highway", "traffic", "neon lights", "street art", "graffiti", "urban decay",
    "industrial", "factory", "warehouse", "construction", "night city", "city lights",
    "urban park", "fountain", "statue", "historic building", "modern architecture"
]

fantasy_tags = [
    "fantasy", "magical", "enchanted", "mystical", "fairy tale", "surreal",
    "dreamlike", "ethereal", "mythical", "legendary", "dragon", "unicorn", "phoenix",
    "castle", "wizard", "sorceress", "enchanted forest", "crystal cave", "floating islands",
    "portal", "magic", "spell", "potion", "ancient ruins", "forgotten temple",
    "magical creatures", "glowing", "otherworldly", "fantasy landscape", "arcane",
    "mystical energy", "elemental", "spirit world", "parallel universe"
]

abstract_tags = [
    "abstract", "geometric", "pattern", "texture", "minimalist", "fractal",
    "kaleidoscope", "symmetry", "asymmetry", "chaos", "order", "flow", "wave",
    "spiral", "curve", "line", "shape", "form", "color field", "gradient",
    "digital abstract", "generative art", "algorithmic", "mathematical",
    "optical illusion", "perspective", "dimension", "space", "void", "infinity",
    "complexity", "simplicity", "contrast", "harmony", "discord", "balance"
]

mood_tags = [
    "peaceful", "serene", "tranquil", "calm", "relaxing", "soothing",
]

# --- Enhanced Categories for Prompt Generation ---

weather_tags = [
    "sunny", "cloudy", "rainy", "snowy", "stormy", "foggy", "misty", "clear sky",
    "overcast", "windy", "hazy", "drizzle", "light rain", "thunderstorm"
]

time_tags = [
    "morning", "noon", "afternoon", "sunset", "sunrise", "dusk", "twilight", "night", "midnight", "golden hour", "blue hour"
]

season_tags = [
    "spring", "summer", "autumn", "winter", "early spring", "late autumn"
]

color_tags = [
    "vivid", "soft pastels", "monochrome", "analogous colors", "complementary colors",
    "warm tones", "cool tones", "earth tones", "neon", "muted", "high contrast", "gradient"
]

material_tags = [
    "glass", "marble", "stone", "wood", "metallic", "ceramic", "silk", "bamboo", "sand", "ice", "paper"
]

lighting_tags = [
    "ambient light", "dramatic lighting", "backlit", "reflected light",
    "diffused lighting", "soft glow", "rim lighting", "shadow play", "volumetric light", "spotlight"
]

pattern_tags = [
    "dots", "chevrons", "mandala", "waves", "ripples", "kaleidoscope", "abstract lines",
    "spirals", "grid", "ornate", "geometric tessellation"
]

terrain_tags = [
    "desert", "plateau", "canyon", "island", "glacier", "tundra", "meadow", "savanna", "steppe", "wetland", "delta"
]

emotion_tags = [
    "mysterious", "majestic", "melancholic", "uplifting", "inspiring", "awe", "vibrant", "ominous",
    "playful", "inviting", "dynamic", "ethereal", "somber", "joyful"
]

architecture_tags = [
    "cathedral", "pagoda", "skyscraper", "chateau", "temple", "villa", "bridge", "castle",
    "palace", "fortress", "tower", "monastery", "colonnade", "dome", "archway"
]

# Style to tag category mapping (from prompt_config.py)
style_to_tags = {
    "nature": nature_tags,
    "landscape": nature_tags,
    "outdoor": nature_tags,
    "space": space_tags,
    "cosmic": space_tags,
    "galaxy": space_tags,
    "urban": urban_tags,
    "city": urban_tags,
    "architecture": urban_tags,
    "abstract": abstract_tags,
    "geometric": abstract_tags,
    "minimal": abstract_tags,
    "fantasy": fantasy_tags,
    "magical": fantasy_tags,
    "surreal": fantasy_tags
}

# Style Categories for generation and UI (from prompt_config.py)
STYLE_CATEGORIES = {
    "Artistic & Painterly": [
        "oil_painting", "watercolor", "pastel", "impressionism", "expressionism",
        "pointillism", "divisionism", "art_nouveau", "art_deco", "cubism",
        "constructivism", "futurism", "surrealism", "pop_art", "ukiyo_e", "woodcut"
    ],
    "Drawing & Sketching": [
        "pencil_sketch", "charcoal", "ink_drawing", "sketch", "line_art"
    ],
    "Digital & Modern": [
        "digital_art", "minimalist", "abstract", "geometric", "low_poly",
        "pixel_art", "glitch_art", "vaporwave", "retrowave"
    ],
    "Photographic & Realistic": [
        "photograph", "cinematic", "hyperrealism", "realism", "double_exposure",
        "landscape" # Landscape can be photographic
    ],
    "Illustrative & Cartoon": [
        "cartoon", "comic_book", "manga", "anime", "graffiti", "paper_cut",
        "stained_glass"
    ],
    "Themed & Fantasy": [
        "fantasy", "sci_fi", "cyberpunk", "steampunk", "gothic", "isometric"
    ]
}

# Available genres for prompt generation (from prompt_config.py)
available_genres = [
    "Nature & Landscapes", "Mountains & Peaks", "Forests & Woods", "Desert & Dunes",
    "Waterfalls & Rivers", "Fields & Meadows", "Autumn Scenes", "Winter Wonderlands",
    "Urban & Architecture", "Modern Cityscapes", "Historic Architecture", "Industrial Scenes",
    "Urban Night Scenes", "Bridges & Infrastructure", "Minimalist Architecture", "Ancient Ruins",
    "Sea & Ocean", "Under the Sea", "Coastal Scenes", "Lake Views", "Harbor & Marina",
    "Tropical Beaches", "Arctic Waters", "Space & Cosmos", "Night Sky", "Cloud Formations",
    "Aurora Scenes", "Celestial Bodies", "Weather Phenomena", "Astronomical Events",
    "Portrait & People", "Street Photography", "Cultural Portraits", "Sports & Action",
    "Fashion & Style", "Urban Lifestyle", "Working Life", "Abstract & 3D", "Geometric Patterns",
    "Color Abstractions", "Light & Shadow Play", "Minimal Abstract", "Architectural Abstract",
    "Material Studies", "Still Life & Objects", "Food Photography", "Product Photography",
    "Botanical Studies", "Vintage Objects", "Modern Objects", "Musical Instruments",
    "Japanese Gardens", "European Gardens", "Rural Farmland", "Volcanic Landscapes",
    "Cave Systems", "Wetlands & Marshes", "Alpine Meadows", "Golden Hour", "Blue Hour",
    "Sunrise Scenes", "Sunset Scenes", "Night Photography", "Morning Mist", "Stormy Weather",
    "Foggy Scenes", "Rain Photography", "Snow Scenes", "Rainbow Scenes", "Misty Mountains",
    "Fantasy Landscapes", "Sci-Fi Environments", "Cyberpunk Cities", "Steampunk Worlds",
    "Futuristic Architecture", "Retro-Futurism", "Digital Dreamscapes", "Surreal Landscapes"
]

# Prompt generation instructions (from prompt_config.py)
PROMPT_INSTRUCTIONS = """You are an expert prompt engineer for the Imagen 3 image generation model. Your task is to craft clear, focused, and highly detailed prompts that maximize Imagen 3's capabilities in generating both photorealistic and artistic images.

To achieve the best results, your prompts should be specific, detailed, and carefully consider the following elements:

1. **Style & Artistic Direction:**
   - Use the specified style (e.g., photorealistic, digital art, oil painting)
   - Incorporate artistic techniques and effects
   - Focus on style-specific elements and characteristics
   - Use appropriate style-specific terminology

2. **Camera & Technical Settings:**
   - Resolution: {resolution}
   - Aspect ratio: {aspect_ratio}
   - Color scheme: {color_scheme}
   - Lighting: {lighting}
   - Composition: {composition}
   - Depth of field: {depth_of_field}

3. **Mood & Atmosphere:**
   - Set the desired mood and emotional tone
   - Use appropriate lighting and color to convey mood
   - Include atmospheric elements that enhance the mood
   - Consider time of day and weather conditions

4. **Composition & Framing:**
   - Use the specified composition style
   - Define perspective and framing
   - Include leading lines and focal points
   - Consider rule of thirds or other composition rules

5. **Color & Tone:**
   - Use the specified color scheme
   - Consider color harmony and contrast
   - Include color temperature and mood
   - Use appropriate color terminology

6. **Negative Elements:**
   - Avoid specified negative elements
   - Exclude unwanted styles or effects
   - Prevent common issues
   - Maintain quality

Critical Requirements:
- Focus on a single, clear style
- Use descriptive, specific language
- Include all technical specifications
- Maintain artistic coherence
- Avoid mixing incompatible styles
- Ensure prompt clarity and focus

Output Format:
Generate a single, detailed sentence that incorporates:
1. Main subject and action/state
2. Style-specific technical specifications
3. Lighting conditions and style
4. Environmental context
5. Color/tone treatment
6. Compositional elements

The final prompt should read like a professional artist's or photographer's description, emphasizing the chosen style while maintaining clarity and focus."""

# Custom prompt enhancement instructions (from prompt_config.py)
CUSTOM_PROMPT_INSTRUCTIONS = """You are an expert prompt engineer for the Imagen 3 image generation model. Your task is to transform the given custom prompt into a highly detailed masterpiece that incorporates the following preferences:

1. **Style & Artistic Direction:**
   - Use the specified style: {style}
   - Incorporate artistic techniques and effects
   - Focus on style-specific elements
   - Use appropriate style-specific terminology

2. **Technical Specifications:**
   - Resolution: {resolution}
   - Aspect ratio: {aspect_ratio}
   - Color scheme: {color_scheme}
   - Lighting: {lighting}
   - Composition: {composition}
   - Depth of field: {depth_of_field}

3. **Mood & Atmosphere:**
   - Set the desired mood: {mood}
   - Use appropriate lighting and color
   - Include atmospheric elements
   - Consider time and weather

4. **Negative Elements:**
   - Avoid specified negative elements
   - Exclude unwanted styles or effects
   - Prevent common issues
   - Maintain quality

Your enhanced prompt should be a single, descriptive sentence that combines the original prompt with these preferences. Focus on creating a vivid and immersive experience that matches the desired style while maintaining clarity and focus."""
