"""Configuration file for wallpaper generator containing tags and prompt instructions."""

# Define tag lists for prompt generation
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
    "energetic", "vibrant", "dynamic", "exciting", "dramatic", "intense",
    "mysterious", "enigmatic", "cryptic", "eerie", "spooky", "haunting",
    "melancholic", "nostalgic", "wistful", "romantic", "passionate", "tender",
    "joyful", "cheerful", "happy", "playful", "whimsical", "dreamy",
    "contemplative", "thoughtful", "philosophical", "inspiring", "uplifting", "motivational"
]

# Available genres for prompt generation
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

# Prompt generation instructions
PROMPT_INSTRUCTIONS = """You are an expert prompt engineer for the Imagen 3 image generation model. Your task is to craft clear, focused, and highly detailed prompts that maximize Imagen 3's capabilities in generating both photorealistic and artistic images.

To achieve the best results, your prompts should be specific, detailed, and carefully consider the following elements:

1. **Style & Artistic Settings:**
   - Overall style (e.g., photorealistic, digital art, oil painting)
   - Art movement (e.g., Abstract Expressionism, Impressionism, Realism)
   - Post-processing effects (e.g., vintage, HDR, film grain, color grading)
   - Style-specific elements and characteristics
   - Appropriate style-specific terminology
   - Artistic coherence and consistency

2. **Camera & Technical Settings:**
   - Camera model (e.g., ARRI Alexa, RED Digital Cinema, Sony Venice)
   - Lens type and focal length (e.g., 50mm, 85mm, 24mm)
   - Aperture settings (e.g., f/1.8, f/2.8, f/4, f/8)
   - Special lens effects (e.g., tilt-shift, fisheye, macro)
   - Resolution and quality settings
   - Detail level and rendering quality
   - Technical specifications for the chosen style

3. **Lighting & Atmosphere:**
   - Time of day (e.g., golden hour, blue hour, twilight)
   - Lighting style (e.g., natural, studio, dramatic, ambient)
   - Light quality (e.g., soft, hard, diffused, directional)
   - Artificial light sources (e.g., LED, neon, tungsten)
   - Light direction and intensity
   - Shadow characteristics
   - Atmospheric conditions

4. **Composition & Environment:**
   - Composition technique (e.g., rule of thirds, leading lines, golden ratio)
   - Camera angle (e.g., eye-level, low angle, high angle, dutch angle)
   - Perspective (e.g., wide, telephoto, aerial, ground-level)
   - Weather conditions (e.g., clear, cloudy, rainy, foggy)
   - Season (e.g., spring, summer, autumn, winter)
   - Atmospheric effects (e.g., fog, mist, rain, snow)
   - Environmental context and setting

5. **Color & Detail Settings:**
   - Color scheme (e.g., monochromatic, complementary, analogous)
   - Palette type (e.g., warm, cool, neutral, vibrant)
   - Color temperature (e.g., warm, cool, neutral)
   - Detail level (e.g., ultra-detailed, high-detail, medium-detail)
   - Texture quality (e.g., high, medium, low)
   - Special effects (e.g., bloom, glow, motion blur, depth of field)
   - Material properties and surface characteristics

6. **Quality Settings:**
   - Resolution (e.g., 8K, 4K, 2K, 1920x1080)
   - Aspect ratio (e.g., 16:9, 21:9, 4:3, 1:1)
   - Rendering quality (e.g., photorealistic, high-quality, ultra-high-quality)
   - Overall image quality and sharpness
   - Noise reduction and clarity
   - Dynamic range and contrast

7. **Mood & Atmosphere:**
   - Overall mood (e.g., peaceful, dramatic, mysterious, energetic)
   - Emotional impact and atmosphere
   - Narrative elements and storytelling
   - Cultural and contextual elements
   - Time period and historical accuracy
   - Environmental mood and ambiance

Critical Requirements:
- Focus on a single, clear style and vision
- Use descriptive, specific language
- Include all technical specifications
- Maintain artistic coherence
- Avoid mixing incompatible styles
- Ensure prompt clarity and focus
- Consider the relationship between different settings
- Balance technical accuracy with artistic expression
- Ensure all settings complement each other
- Maintain consistency across all elements

Output Format:
Generate a single, detailed sentence that incorporates:
1. Main subject and action/state
2. Style and artistic direction
3. Camera and technical specifications
4. Lighting and atmospheric conditions
5. Composition and environmental context
6. Color treatment and special effects
7. Quality and detail specifications
8. Mood and emotional impact

The final prompt should read like a professional artist's or photographer's description, emphasizing the chosen style while maintaining clarity and focus. Ensure all technical specifications are accurate and appropriate for the chosen style. The prompt should be detailed but concise, focusing on the most important elements that will contribute to the final image quality."""

# Custom prompt enhancement instructions
CUSTOM_PROMPT_INSTRUCTIONS = """Enhance the following prompt for generating a high-quality wallpaper image. Consider the following specifications:

Style & Artistic Settings:
- Style: {style}
- Mood: {mood}
- Art Movement: {art_movement}
- Post-processing: {post_processing}

Camera & Technical Settings:
- Camera Model: {camera_model}
- Lens Type: {lens_type}
- Aperture: {aperture}
- Special Lens: {special_lens}
- Depth of Field: {depth_of_field}

Lighting & Atmosphere:
- Time of Day: {time_of_day}
- Lighting Style: {lighting}
- Light Quality: {light_quality}
- Artificial Sources: {artificial_sources}

Composition & Environment:
- Technique: {composition}
- Camera Angle: {camera_angle}
- Perspective: {perspective}
- Weather: {weather}
- Season: {season}
- Atmospheric Effects: {atmospheric_effects}

Color & Detail Settings:
- Color Scheme: {color_scheme}
- Palette Type: {palette_type}
- Color Temperature: {color_temperature}
- Detail Level: {detail_level}
- Texture Quality: {texture_quality}
- Special Effects: {special_effects}

Quality Settings:
- Resolution: {resolution}
- Aspect Ratio: {aspect_ratio}
- Rendering Quality: {rendering_quality}

Please enhance the following prompt while maintaining its core concept and incorporating these specifications:

{prompt}

Output only the enhanced prompt without any additional explanations or formatting."""

# Text and Logo Generation Instructions
TEXT_LOGO_INSTRUCTIONS = """You are an expert prompt engineer for the Imagen 3 image generation model, specializing in text and logo generation. Your task is to craft clear, focused prompts that will generate high-quality text and logos in images.

Key Guidelines for Text Generation:
1. **Text Clarity & Readability:**
   - Keep text short and concise (25 characters or less)
   - Use clear, legible fonts
   - Ensure good contrast with background
   - Consider text placement and spacing

2. **Logo Design Elements:**
   - Include brand identity elements
   - Specify logo style (minimalist, modern, vintage, etc.)
   - Define color scheme and typography
   - Consider logo placement and composition

3. **Technical Specifications:**
   - Resolution: {resolution}
   - Aspect ratio: {aspect_ratio}
   - Color scheme: {color_scheme}
   - Background style: {background_style}

4. **Quality Modifiers:**
   - Use appropriate quality descriptors
   - Include style-specific elements
   - Consider brand guidelines
   - Maintain professional appearance

5. **Negative Elements:**
   - Avoid text distortion
   - Prevent unclear or illegible text
   - Exclude unwanted styles
   - Maintain brand consistency

Output Format:
Generate a single, detailed sentence that incorporates:
1. Main text/logo content
2. Style and design elements
3. Technical specifications
4. Quality modifiers
5. Brand-specific requirements

The final prompt should read like a professional designer's specification, emphasizing clarity and brand consistency while maintaining visual appeal."""

# Logo Generation Templates
LOGO_TEMPLATES = {
    "minimalist": {
        "style": "minimalist, clean lines, simple shapes",
        "elements": ["geometric forms", "negative space", "typography"],
        "quality": ["crisp", "precise", "professional"]
    },
    "modern": {
        "style": "contemporary, sleek, innovative",
        "elements": ["gradients", "shadows", "dynamic shapes"],
        "quality": ["high-end", "sophisticated", "trendy"]
    },
    "vintage": {
        "style": "retro, classic, timeless",
        "elements": ["textures", "ornaments", "traditional typography"],
        "quality": ["authentic", "detailed", "nostalgic"]
    },
    "playful": {
        "style": "fun, energetic, vibrant",
        "elements": ["bright colors", "whimsical shapes", "dynamic elements"],
        "quality": ["engaging", "memorable", "eye-catching"]
    },
    "corporate": {
        "style": "professional, trustworthy, established",
        "elements": ["clean typography", "balanced composition", "corporate colors"],
        "quality": ["polished", "credible", "authoritative"]
    }
}

# Text Generation Templates
TEXT_TEMPLATES = {
    "headline": {
        "style": "bold, impactful, attention-grabbing",
        "elements": ["large text", "strong contrast", "clear hierarchy"],
        "quality": ["sharp", "readable", "memorable"]
    },
    "body": {
        "style": "clean, legible, professional",
        "elements": ["proper spacing", "consistent alignment", "balanced layout"],
        "quality": ["clear", "well-spaced", "professional"]
    },
    "decorative": {
        "style": "artistic, stylized, ornamental",
        "elements": ["flourishes", "decorative elements", "unique typography"],
        "quality": ["elegant", "detailed", "artistic"]
    },
    "minimal": {
        "style": "simple, clean, modern",
        "elements": ["sparse design", "negative space", "essential elements"],
        "quality": ["crisp", "refined", "contemporary"]
    }
}

# Text and Logo Quality Modifiers
TEXT_LOGO_QUALITY_MODIFIERS = {
    "general_quality": [
        "high-quality",
        "professional",
        "crisp",
        "sharp",
        "clean",
        "precise",
        "detailed",
        "polished"
    ],
    "text_quality": [
        "legible",
        "readable",
        "clear",
        "well-spaced",
        "balanced",
        "harmonious",
        "consistent",
        "refined"
    ],
    "logo_quality": [
        "memorable",
        "distinctive",
        "scalable",
        "versatile",
        "timeless",
        "unique",
        "balanced",
        "proportional"
    ],
    "custom_quality": []  # For user-defined quality modifiers
}

# Text and Logo Style Modifiers
TEXT_LOGO_STYLE_MODIFIERS = {
    "typography": [
        "serif",
        "sans-serif",
        "script",
        "display",
        "handwritten",
        "monospace",
        "decorative",
        "geometric"
    ],
    "effects": [
        "gradient",
        "shadow",
        "outline",
        "3D",
        "glow",
        "texture",
        "pattern",
        "emboss"
    ],
    "composition": [
        "centered",
        "aligned",
        "stacked",
        "overlapping",
        "interwoven",
        "balanced",
        "asymmetrical",
        "dynamic"
    ],
    "custom_style": []  # For user-defined style modifiers
}

# Text and Logo Background Modifiers
TEXT_LOGO_BACKGROUND_MODIFIERS = {
    "solid": [
        "white",
        "black",
        "transparent",
        "gradient",
        "pattern",
        "texture",
        "color-block",
        "custom"
    ],
    "effects": [
        "blur",
        "noise",
        "grain",
        "vignette",
        "gradient",
        "pattern",
        "texture",
        "custom"
    ],
    "custom_background": []  # For user-defined background modifiers
} 