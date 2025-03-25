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
PROMPT_INSTRUCTIONS = """You are an expert prompt engineer for the Imagen 3 image generation model, specializing in creating detailed prompts for both photorealistic and artistic images, with particular expertise in claymation and stop-motion styles.

To achieve the best results, your prompts should be specific, detailed, and carefully consider the following elements:

1. **Style & Artistic Settings:**
   - Overall style (e.g., claymation, photorealistic, digital art, oil painting)
   - Art movement (e.g., Abstract Expressionism, Impressionism, Realism)
   - Post-processing effects (e.g., vintage, HDR, film grain, color grading)
   - Style-specific elements and characteristics
   - Appropriate style-specific terminology
   - Artistic coherence and consistency
   - For claymation:
     * Handcrafted, tactile feel
     * Visible clay textures and imperfections
     * Stop-motion animation aesthetic
     * Character and set design details
     * Lighting that enhances clay's material properties

2. **Camera & Technical Settings:**
   - Camera model (e.g., RED Digital Cinema, ARRI Alexa, Sony Venice)
   - Lens type and focal length (e.g., 50mm, 85mm, 24mm)
   - Aperture settings (e.g., f/1.8, f/2.8, f/4, f/8)
   - Special lens effects (e.g., tilt-shift, fisheye, macro)
   - Depth of field settings
   - Resolution and quality settings
   - Detail level and rendering quality
   - Technical specifications for the chosen style

3. **Lighting & Atmosphere:**
   - Time of day (e.g., midday, golden hour, blue hour, twilight)
   - Lighting style (e.g., natural, studio, dramatic, ambient)
   - Light quality (e.g., soft, hard, diffused, directional)
   - Artificial light sources (e.g., LED, neon, tungsten)
   - Light direction and intensity
   - Shadow characteristics
   - Atmospheric conditions
   - For claymation:
     * Lighting that emphasizes clay's material properties
     * Soft, diffused lighting to avoid harsh shadows
     * Natural light simulation for outdoor scenes

4. **Composition & Environment:**
   - Composition technique (e.g., framing, rule of thirds, leading lines)
   - Camera angle (e.g., eye-level, low angle, high angle, dutch angle)
   - Perspective (e.g., wide, telephoto, aerial, ground-level)
   - Weather conditions (e.g., clear, cloudy, rainy, foggy)
   - Season (e.g., summer, spring, autumn, winter)
   - Atmospheric effects (e.g., fog, mist, rain, snow)
   - Environmental context and setting
   - For claymation:
     * Set design and environment details
     * Scale and proportion considerations
     * Background and foreground elements

5. **Color & Detail Settings:**
   - Color scheme (e.g., natural, monochromatic, complementary, analogous)
   - Palette type (e.g., warm, cool, neutral, vibrant)
   - Color temperature (e.g., warm, cool, neutral)
   - Detail level (e.g., ultra-detailed, high-detail, medium-detail)
   - Texture quality (e.g., high, medium, low)
   - Special effects (e.g., bloom, glow, motion blur)
   - Material properties and surface characteristics
   - For claymation:
     * Clay material colors and textures
     * Color harmony in the scene
     * Surface finish and reflectivity

6. **Quality Settings:**
   - Resolution (e.g., 8K, 4K, 2K, 1920x1080)
   - Aspect ratio (e.g., 16:9, 21:9, 4:3, 1:1)
   - Rendering quality (e.g., photorealistic, high-quality, ultra-high-quality)
   - Overall image quality and sharpness
   - Noise reduction and clarity
   - Dynamic range and contrast
   - For claymation:
     * High detail in clay textures
     * Clear focus on main subjects
     * Balanced exposure

7. **Mood & Atmosphere:**
   - Overall mood (e.g., peaceful, dramatic, mysterious, energetic)
   - Emotional impact and atmosphere
   - Narrative elements and storytelling
   - Cultural and contextual elements
   - Time period and historical accuracy
   - Environmental mood and ambiance
   - For claymation:
     * Whimsical or serious tone
     * Character expressions and poses
     * Scene atmosphere and mood

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
- For claymation:
  * Emphasize handcrafted qualities
  * Maintain consistent scale
  * Consider stop-motion aesthetics
  * Focus on material properties
  * Balance detail with style

Output Format:
Generate a single, detailed paragraph that incorporates:
1. Main subject and action/state
2. Style and artistic direction
3. Camera and technical specifications
4. Lighting and atmospheric conditions
5. Composition and environmental context
6. Color treatment and special effects
7. Quality and detail specifications - RESOLUTION ({resolution}) and ASPECT RATIO ({aspect_ratio}) MUST be explicitly included here
8. Mood and emotional impact

CRITICALLY IMPORTANT FORMAT RULES:
- ALWAYS end the main description with "{resolution} resolution, {aspect_ratio} aspect ratio" before the negative prompt
- Only AFTER the resolution and aspect ratio, add "Avoid: [negative elements]"
- NEVER put resolution or aspect ratio in the negative prompt section
- Follow this exact pattern: "[creative description], {resolution} resolution, {aspect_ratio} aspect ratio. Avoid: [unwanted elements]"

The final prompt should read like a professional artist's or photographer's description, emphasizing the chosen style while maintaining clarity and focus. Ensure all technical specifications are accurate and appropriate for the chosen style. The prompt should be detailed but concise, focusing on the most important elements that will contribute to the final image quality."""

# Custom prompt enhancement instructions
CUSTOM_PROMPT_INSTRUCTIONS = """
YOUR PRIMARY TASK IS TO ENHANCE THIS EXACT PROMPT: "{prompt}"

IMPORTANT: The input prompt MUST remain the central subject and focus. DO NOT replace or rewrite the core concept. 
You are only adding technical details and artistic specifications to the EXISTING prompt, not creating a new one.

Enhance the above prompt for generating a high-quality wallpaper image by incorporating these technical specifications:

Style & Artistic Settings:
- Overall Style: {style}
- Mood: {mood}
- Art Movement: {art_movement}
- Post-processing: {post_processing}
- For 3D Render Pixar Style:
  * Clean, polished 3D rendering
  * Smooth, appealing surfaces
  * Characteristic Pixar lighting
  * Whimsical, family-friendly aesthetic
  * Attention to material properties
  * Balanced composition
  * Emotional storytelling elements

Camera & Technical Settings:
- Camera Model: {camera_model}
- Lens Type: {lens_type}
- Aperture: {aperture}
- Special Lens: {special_lens}
- Depth of Field: {depth_of_field}
- For 3D Render:
  * Cinematic camera angles
  * Professional depth of field
  * Clear focus on main subjects
  * Balanced exposure
  * Dynamic framing

Lighting & Atmosphere:
- Time of Day: {time_of_day}
- Lighting Style: {lighting}
- Light Quality: {light_quality}
- Artificial Sources: {artificial_sources}
- For 3D Render:
  * Global illumination
  * Soft, natural lighting
  * Subtle shadows
  * Ambient occlusion
  * Light bounces and reflections

Composition & Environment:
- Technique: {composition}
- Camera Angle: {camera_angle}
- Visual Flow: {visual_flow}
- Depth Layering: {depth_layering}
- Weather: {weather}
- Season: {season}
- Atmospheric Effects: {atmospheric_effects}
- Location Type: {location_type}
- For 3D Render:
  * Rule of thirds
  * Leading lines
  * Depth layers
  * Environmental storytelling
  * Balanced negative space

Color & Detail Settings:
- Color Scheme: {color_scheme}
- Palette Type: {palette_type}
- Color Temperature: {color_temperature}
- Detail Level: {detail_level}
- Texture Quality: {texture_quality}
- Special Effects: {special_effects}
- For 3D Render:
  * Vibrant, appealing colors
  * Consistent color harmony
  * Material-based textures
  * Surface imperfections
  * Subsurface scattering

Quality Settings:
- Resolution: {resolution}
- Aspect Ratio: {aspect_ratio}
- Rendering Quality: {rendering_quality}
- For 3D Render:
  * High polygon count
  * Anti-aliasing
  * Motion blur
  * Depth of field
  * Global illumination

Critical Requirements:
1. YOU MUST KEEP THE ORIGINAL CONCEPT OF "{prompt}" INTACT - this is non-negotiable
2. Your enhancement should ADD to the original prompt, never replace it
3. If the original prompt describes a specific subject (like "niagara falls" or "mountain landscape"), that subject MUST be the focus
4. Incorporate all specified settings naturally around the original subject
5. Ensure technical accuracy
6. Maintain artistic coherence
7. Balance detail with style
8. For 3D Render:
   - Keep the Pixar-style aesthetic
   - Maintain family-friendly appeal
   - Ensure smooth, polished look
   - Include emotional elements
   - Balance realism with stylization

CRITICALLY IMPORTANT FORMAT RULES:
1. The prompt MUST end with "{resolution} resolution, {aspect_ratio} aspect ratio" before any negative prompt
2. The resolution and aspect ratio MUST be in the main description, NOT in the negative prompt
3. The format should be: "[creative description], {resolution} resolution, {aspect_ratio} aspect ratio. Avoid: [negative elements]"
4. NEVER include resolution or aspect ratio in the negative prompt section
5. If you include "Avoid:" section, it MUST come AFTER the resolution and aspect ratio

Output Format:
Generate a single, detailed paragraph that incorporates:
1. The EXACT SUBJECT from the original prompt as the main focus
2. Style and artistic direction
3. Camera and technical specifications
4. Lighting and atmospheric conditions
5. Composition and environmental context
6. Color treatment and special effects
7. End with "{resolution} resolution, {aspect_ratio} aspect ratio"
8. After all that, include negative elements with "Avoid: [unwanted elements]"

The final prompt should read like a professional description that enhances "{prompt}" with technical details, while maintaining the original concept as the central focus.

Output only the enhanced prompt without any additional explanations or formatting."""

# Negative Prompt Instructions
NEGATIVE_PROMPT_INSTRUCTIONS = """You are an expert in generating intelligent negative prompts for Imagen 3 image generation. Your task is to analyze the user's current preferences and generate appropriate negative prompts to improve image quality by excluding unwanted elements.

Context Analysis:
1. User's Current Preferences:
   - Selected Style/Genre: {style_or_genre}
   - Selected Mood: {mood}
   - Art Movement: {art_movement}
   - Special Requirements: {special_requirements}
   - Selected Tags: {selected_tags}
   - Quality Preferences: {quality_preferences}

Negative Prompt Generation Guidelines:
1. Style Compatibility:
   - Exclude styles that conflict with the user's selected style
   - Remove elements that would disrupt the artistic coherence
   - Avoid mixing incompatible art movements

2. Content Exclusions Based on Genre:
   - For nature scenes: exclude urban elements, industrial objects, etc.
   - For urban scenes: exclude excessive natural elements that don't belong
   - For abstract art: exclude overly representational elements
   - For minimalist styles: exclude cluttered or busy compositions

3. Technical Quality Exclusions:
   - Low quality, pixelated, blurry, noisy, or distorted elements
   - Poor composition, bad framing, or unbalanced layout
   - Inconsistent lighting or shadows
   - Unrealistic proportions or perspectives (unless stylistically appropriate)

4. Mood Consistency:
   - Exclude emotional elements contrary to the selected mood
   - Remove atmospheric conditions that conflict with the desired feeling
   - Avoid color schemes that clash with the intended mood

5. Smart Tag Analysis:
   - Automatically exclude tags from opposite categories
   - Identify potential visual conflicts between selected elements
   - Suggest exclusions based on statistical patterns of successful images

Output Format:
Generate a comma-separated list of negative prompt elements organized by category:

1. Style Exclusions: Elements that conflict with the chosen style
2. Technical Quality: Elements that would reduce image quality
3. Content Exclusions: Subject matter to avoid based on chosen genre
4. Mood Conflicts: Elements that would disrupt the desired mood
5. Visual Artifacts: Common AI generation issues to avoid

The final negative prompt should be concise yet comprehensive, focusing on the most important elements to exclude based on the user's specific preferences while maintaining artistic coherence.

Some common negative elements to always include:
(ugly, disfigured, low quality, blurry, nsfw, watermark, signature, out of frame, extra limbs, badly drawn face, extra fingers)"""

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