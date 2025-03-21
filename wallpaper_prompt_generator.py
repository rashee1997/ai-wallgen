#!/usr/bin/env python3
"""AI Wallpaper Prompt Generator - A tool for generating detailed text prompts for AI wallpaper generation.

This script generates text prompts based on user input, enhancing them with the Gemini AI model.
It features robust caching, error handling, and multiple prompt generation methods.
"""
import json
import os
import random
import logging
import bleach
import html
import hashlib
import time
from typing import Optional, Dict, List, Tuple
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("prompt_generator.log", mode="a")
    ]
)

# Configure the Gemini API key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logging.warning("GEMINI_API_KEY environment variable not set. Some features may be limited.")

try:
    import google.generativeai as genai
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        GEMINI_AVAILABLE = True
    else:
        GEMINI_AVAILABLE = False
except ImportError:
    logging.warning("google.generativeai library not found. Using fallback prompt generation.")
    logging.info("To install, run: pip install google-generativeai")
    GEMINI_AVAILABLE = False
except Exception as e:
    logging.error(f"Error configuring Gemini API: {e}")
    GEMINI_AVAILABLE = False

# Create cache directory if it doesn't exist
CACHE_DIR = Path("prompt_cache")
CACHE_DIR.mkdir(exist_ok=True)

# File-based cache for generated prompts
def load_prompt_cache() -> Dict[str, str]:
    """Load the prompt cache from disk."""
    cache_file = CACHE_DIR / "prompt_cache.json"
    if cache_file.exists():
        try:
            with open(cache_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error loading prompt cache: {e}")
            return {}
    return {}

def save_prompt_cache(cache: Dict[str, str]) -> None:
    """Save the prompt cache to disk."""
    cache_file = CACHE_DIR / "prompt_cache.json"
    try:
        with open(cache_file, "w") as f:
            json.dump(cache, f, indent=2)
    except IOError as e:
        logging.error(f"Error saving prompt cache: {e}")

# Initialize cache
prompt_cache = load_prompt_cache()

# Define tag lists for prompt generation
nature_tags = [
    "landscape", "nature", "mountains", "forest", "trees", "waterfall", "ocean",
    "sea", "lake", "river", "sky", "clouds", "sunset", "sunrise", "stars",
    "moon", "flowers", "plants", "grass", "leaves", "wildlife", "animals",
    "birds", "insects", "butterfly", "deer", "fox", "bear", "wolf", "eagle",
    "meadow", "valley", "canyon", "desert", "rain", "snow", "ice", "mist",
    "fog", "rainbow", "aurora", "volcano", "cave", "beach", "coast", "island",
    "jungle", "rainforest", "savanna", "tundra", "alpine", "coral reef"
]

space_tags = [
    "space", "planet", "galaxy", "star", "astronaut", "rocket", "planetarium",
    "cosmos", "universe", "nebula", "black hole", "supernova", "comet",
    "satellite", "telescope", "astronomy", "cosmic", "interstellar", "orbiter",
    "constellation", "celestial", "starry", "astral", "cosmic", "spacecraft",
    "space station", "spacewalk", "space shuttle", "space probe"
]

sea_tags = [
    "sea", "ocean", "beach", "coast", "waves", "sunset", "sunrise", "tide",
    "current", "ship", "boat", "fishing", "sailboat", "yacht", "maritime",
    "navigation", "shipwreck", "cruise", "sailing", "seafarer", "seafaring"
]

flowers_tags = [
    "flowers", "rose", "tulip", "daisy", "sunflower", "lily", "orchid",
    "dahlia", "chrysanthemum", "carnation", "aster", "iris", "lavender",
    "marigold", "petunia", "zinnia", "gerbera", "hydrangea", "begonia"
]

def load_last_genre(filename: str = "last_genre.json") -> Optional[str]:
    """Loads the last used genre from a JSON file."""
    try:
        with open(filename, "r") as f:
            return json.load(f).get("last_genre")
    except (FileNotFoundError, json.JSONDecodeError, IOError):
        return None

def save_last_genre(genre, filename="last_genre.json"):
    """Saves the last used genre to a JSON file."""
    try:
        with open(filename, "w") as f:
            json.dump({"last_genre": genre}, f)
    except Exception as e:
        logging.error(f"Error saving last genre: {e}")

# Define all available genres
AVAILABLE_GENRES = [
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
    "Foggy Scenes", "Rain Photography", "Snow Scenes", "Rainbow Scenes", "Misty Mountains"
]

def get_cache_key(tags: List[str]) -> str:
    """Generate a unique cache key for the given tags."""
    tags_str = ", ".join(sorted(tags))
    return hashlib.md5(tags_str.encode()).hexdigest()

def select_genre() -> str:
    """Select a genre that hasn't been used recently."""
    last_genre = load_last_genre()
    available_genres = AVAILABLE_GENRES.copy()
    
    if last_genre and last_genre in available_genres:
        available_genres.remove(last_genre)
    
    if not available_genres:
        available_genres = AVAILABLE_GENRES.copy()
    
    chosen_genre = random.choice(available_genres)
    save_last_genre(chosen_genre)
    return chosen_genre

def generate_prompt_gemini(tags: List[str], use_cache: bool = True) -> Optional[str]:
    """Generate a prompt using the Gemini model.
    
    Args:
        tags: List of tags to use for prompt generation
        use_cache: Whether to use cached prompts
        
    Returns:
        str: Generated prompt or None if generation failed
    """
    if not GEMINI_AVAILABLE:
        logging.warning("Gemini API not available. Using random prompt generation instead.")
        return generate_prompt_random(tags)
    
    # Create a unique cache key for these tags
    cache_key = get_cache_key(tags)
    
    # Check if we have a cached prompt for these tags
    if use_cache:
        # First check memory cache
        if cache_key in prompt_cache:
            logging.info(f"Using in-memory cached prompt for tags: {', '.join(tags)}")
            return prompt_cache[cache_key]
        
        # Then check file cache
        cache_file = CACHE_DIR / f"{cache_key}.txt"
        if cache_file.exists():
            try:
                with open(cache_file, "r") as f:
                    cached_prompt = f.read().strip()
                    prompt_cache[cache_key] = cached_prompt  # Update memory cache
                    logging.info(f"Using file-cached prompt for tags: {', '.join(tags)}")
                    return cached_prompt
            except IOError as e:
                logging.error(f"Error reading cache file: {e}")
    
    # No cache hit, generate a new prompt
    chosen_genre = select_genre()

    prompt_instructions = f"""You are an expert prompt engineer for the Imagen 3 image generation model, integrated within Google Gemini. Your task is to craft clear, focused, and highly detailed prompts that maximize Imagen 3's capabilities in generating photorealistic and creative images. To achieve the best results, your prompts should be specific, detailed, and carefully consider the persona, task, context, and format. Strive to create prompts that are neither too short nor too long, and always describe the desired mood or atmosphere.

Choose *{chosen_genre}* from these specialized categories, and use the following guidelines to create effective prompts:

**General Guidelines:**

*   **Clarity and Focus:** Ensure your prompts are clear, concise, and focused on a specific subject or scene. Avoid ambiguity and provide enough detail for Imagen 3 to understand your vision.
*   **Persona, Task, Context, and Format:** Consider the perspective (persona), the desired outcome (task), the surrounding information (context), and the structure of the prompt (format) to guide Gemini and Imagen 3 effectively.
*   **Length:** Avoid prompts that are too short (lacking detail) or too long (overly complicated). Strike a balance to provide sufficient information without overwhelming the model.
*   **Mood and Atmosphere:** Describe the desired mood or atmosphere to influence the overall tone and style of the generated image.

**Specialized Categories:**

Each category below provides specific elements and technical details to enhance your prompts. Remember to maintain photographic realism, focus on a single genre, include technical photography terms, reference real-world lighting conditions, and specify exact camera perspectives and compositions.

**Nature & Landscapes**
- Focus: Dynamic natural environments with atmospheric conditions
- Elements: Golden hour lighting, volumetric fog, water reflections, dramatic weather, diverse flora and fauna
- Examples: Mountain ranges with morning mist, storm-approaching coastlines with crashing waves, sunlit forest canopies teeming with wildlife
- Technical: f/8-f/11 aperture, wide-angle lens perspective (16-35mm), HDR dynamic range, polarizing filter for water reflections

**Urban & Architecture**
- Focus: Architectural details and urban environment interplay, human activity
- Elements: Material textures (glass, steel, concrete), geometric patterns, ambient occlusion, light diffusion, street-level details, human figures
- Examples: Glass-steel skyscrapers at blue hour with bustling street activity, historic stone facades with directional lighting and people walking by
- Technical: Tilt-shift perspective, golden ratio composition, deep depth of field, long exposure for motion blur

**Portrait & People**
- Focus: Natural human expressions and environmental context, cultural elements
- Elements: Soft skin rendering, fabric textures, hair detail, natural poses, diverse cultural backgrounds, environmental storytelling
- Examples: Environmental portraits in natural settings, candid street photography capturing cultural moments, lifestyle moments with authentic expressions
- Technical: 85mm lens perspective, f/1.8-f/2.8 aperture, Rembrandt lighting setup, shallow depth of field for subject isolation

**Still Life & Objects**
- Focus: Material properties and object relationships, artistic arrangement
- Elements: Surface reflections, subsurface scattering, micro-details, carefully arranged objects, artistic composition, storytelling through objects
- Examples: Product photography setups with intricate lighting, carefully arranged natural objects with symbolic meaning
- Technical: Focus stacking, controlled studio lighting, rule of thirds, macro lens for extreme detail

**Water Environments**
- Focus: Liquid dynamics and environmental context, marine life
- Elements: Refraction, reflection, foam, wave patterns, underwater details, marine life (fish, coral), interaction of light and water
- Examples: Ocean waves crashing against cliffs with dramatic spray, underwater macro photography of coral reefs teeming with life
- Technical: Polarizing filters, long exposure, shallow depth of field, underwater housing for camera

**Abstract & 3D**
- Focus: Clean geometric forms with realistic materials, innovative design
- Elements: Surface reflectivity, procedural textures, precise geometry, innovative design elements, interplay of light and shadow, visual complexity
- Examples: Minimalist architectural details with complex geometric patterns, macro photography of natural patterns with abstract interpretations
- Technical: Studio lighting setups, focus stacking, symmetrical composition, rendering software for realistic materials

Essential Technical Specifications:
1. Resolution & Quality
   - Specify "high resolution" or "8K" for maximum detail
   - Include "photorealistic" or "photoreal" for natural rendering
   - Reference professional camera brands for style (e.g., "shot on Hasselblad," "ARRI Alexa," "Canon EOS")
   - Use terms like "ultra-detailed," "hyperrealistic," and "visually stunning"

2. Lighting Parameters
   - Define specific lighting conditions (golden hour, blue hour, studio setup, moonlight, candlelight)
   - Specify light quality (soft, harsh, directional, diffused, volumetric)
   - Include practical light sources when relevant (neon signs, street lamps, firelight)
   - Use terms like "global illumination," "ray tracing," and "ambient occlusion"

3. Composition Elements
   - Define camera position (eye-level, bird's eye, worm's eye, high angle, low angle)
   - Specify focal length (wide-angle 16-35mm, standard 50mm, telephoto 70-200mm, macro lens)
   - Include depth of field requirements (shallow f/1.8, deep f/11, focus stacking)
   - Use composition techniques like "rule of thirds," "golden ratio," "leading lines," and "symmetry"

4. Environmental Context
   - Define time of day and weather conditions (sunny, cloudy, rainy, snowy, foggy, misty)
   - Specify season when relevant (spring, summer, autumn, winter)
   - Include atmospheric effects (fog, haze, rain, snow, dust, smoke)
   - Add environmental details (urban cityscape, tropical beach, mountain range, forest)

5. Color and Tone
   - Reference specific color palettes or color grading styles (warm, cool, monochromatic, vibrant, muted)
   - Specify contrast levels and dynamic range (high contrast, low contrast, HDR)
   - Include color temperature (warm, cool, neutral)
   - Use terms like "color graded," "film grain," and "vintage look"

Critical Requirements:
- Maintain photographic realism at all times
- Focus on a single genre without mixing categories
- Include specific technical photography terms
- Reference real-world lighting conditions
- Specify exact camera perspectives and compositions
- Use descriptive language to enhance details

Avoid:
- AI art buzzwords or style references
- Multiple competing focal points
- Technically impossible scenarios
- Mixed lighting conditions
- Vague or subjective descriptors
- Overly complex or confusing prompts

Output Format:
Generate a single, detailed sentence that incorporates:
1. Main subject and action/state
2. Technical camera specifications (camera, lens, aperture)
3. Lighting conditions (time of day, light quality, light sources)
4. Environmental context (weather, season, location)
5. Color/tone treatment (color palette, contrast, dynamic range)
6. Compositional elements (camera position, focal length, depth of field)

The final prompt should read like a professional photographer's shot description, emphasizing Imagen 3's strengths in photorealism, lighting, and material rendering while maintaining physical accuracy and natural composition."""

    prompt = f"{prompt_instructions} Tags: {', '.join(tags)}" if tags else ""

    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        prompt = prompt  # Ensure 'prompt' is defined before use
        response = model.generate_content(prompt)

        gemini_prompt = None
        if response.parts:
            gemini_prompt = response.parts[0].text.strip()
            logging.info(f"Generated Gemini prompt: {gemini_prompt}")

            # Save to memory cache
            prompt_cache[cache_key] = gemini_prompt
            
            # Save to file cache
            try:
                cache_file = CACHE_DIR / f"{cache_key}.txt"
                with open(cache_file, "w") as f:
                    f.write(gemini_prompt)
            except IOError as e:
                logging.error(f"Error writing to cache file: {e}")
            return gemini_prompt
        else:
            logging.warning("Gemini model returned an empty response.")
            return None

    except Exception as e:
        logging.error(f"Error generating prompt with Gemini: {e}")
        return None

def generate_prompt_random(tags):
    """Generate a random prompt from the given tags with enhanced details."""
    num_tags = random.randint(2, 4)  # Generate 2 to 4 tags
    selected_tags = random.sample(tags, num_tags)

    # Enhanced combinations with more descriptive words and technical details
    combinations = [
        f"A stunning {selected_tags[0]} with {selected_tags[1]}, captured with a 35mm lens at f/1.8, during golden hour, with soft, diffused light, and a warm color palette.",
        f"The beauty of {selected_tags[0]} meeting the serenity of {selected_tags[1]}, shot with a wide-angle lens at f/8, during blue hour, with cool tones and a shallow depth of field.",
        f"An artistic representation of {selected_tags[0]}, blended with {selected_tags[1]} and {selected_tags[2] if num_tags > 2 else ''}, using a 50mm lens at f/2.8, with harsh, direct light, and a vibrant color scheme.",
        f"A photorealistic wallpaper of {selected_tags[0]}, {selected_tags[1]}, and {selected_tags[2] if num_tags > 2 else ''}, with a touch of {selected_tags[3] if num_tags > 3 else ''}, shot with a 85mm lens at f/4, during sunset, with warm, diffused light, and a rich color palette."
    ]

    prompt = random.choice(combinations)
    logging.info(f"Generated random prompt: {prompt}")
    return prompt

def mask_sensitive_data_in_url(url):
    """Masks sensitive data in URLs before logging and decodes HTML entities."""
    if isinstance(url, str):
        url = html.unescape(url)
        if 'key=' in url:
            parts = url.split('key=')
            url = parts[0] + 'key=<HIDDEN>'
        if 'client_id=' in url:
            parts = url.split('client_id=')
            url = parts[0] + 'client_id=<HIDDEN>'
    return url

def sanitize_prompt(prompt):
    """Sanitize the prompt using bleach."""
    allowed_tags = []
    allowed_attributes = {}
    sanitized_prompt = bleach.clean(prompt, tags=allowed_tags, attributes=allowed_attributes, strip=True)
    return sanitized_prompt

def generate_prompt(custom_prompt=None):
    """Generate a prompt based on the given custom prompt or random tags."""
    if custom_prompt:
        prompt = sanitize_prompt(custom_prompt)
        logging.info(f"Using custom prompt: {prompt}")
        return prompt

    all_tags = nature_tags + space_tags + sea_tags + flowers_tags
    prompt = random.choice(all_tags) if all_tags else ""
    logging.info(f"Generated prompt: {prompt}")
    return prompt

def enhance_custom_prompt(custom_prompt: str) -> str:
    """Enhance the custom prompt using the Gemini model.
    
    Args:
        custom_prompt: The custom prompt to enhance
        
    Returns:
        str: The enhanced prompt or the original prompt if enhancement failed
    """
    if not GEMINI_AVAILABLE:
        logging.warning("Gemini API not available. Cannot enhance prompt.")
        return custom_prompt
        
    # Create a cache key for this custom prompt
    cache_key = f"enhance_{hashlib.md5(custom_prompt.encode()).hexdigest()}"
    
    # Check if we have a cached enhanced prompt
    cache_file = CACHE_DIR / f"{cache_key}.txt"
    if cache_file.exists():
        try:
            with open(cache_file, "r") as f:
                cached_prompt = f.read().strip()
                logging.info(f"Using cached enhanced prompt")
                return cached_prompt
        except IOError as e:
            logging.error(f"Error reading enhanced prompt cache file: {e}")
    
    prompt_instructions = f"""
You are an expert prompt engineer for AI image generation models. Your task is to transform the given custom prompt into a highly detailed, visually stunning, and photorealistic masterpiece. Focus on enhancing the prompt with specific technical details related to photography, cinematography, and visual arts to maximize the visual impact, aesthetic appeal, and realism of the generated image.

The goal is to create a prompt that will produce a wallpaper-quality image with exceptional detail, balanced composition, and professional artistic qualities.

To achieve the best results with Imagen 3, consider the following enhancements:

1.  **Camera and Lens Specifications:**
    *   Specify the camera model: e.g., "Shot on Hasselblad," "Canon EOS R5," or "ARRI Alexa."
    *   Define the lens type and focal length: e.g., "35mm lens," "85mm portrait lens," "wide-angle 16mm."
    *   Set the aperture: e.g., "f/1.8" for shallow depth of field, "f/8" for landscape sharpness.
    *   Mention any special lenses: e.g., "Tilt-shift lens," "Macro lens," "Anamorphic lens."
    *   Example: "Shot on ARRI Alexa with a 50mm lens at f/2.8"

2.  **Lighting Conditions:**
    *   Describe the time of day: e.g., "Golden hour," "Blue hour," "Midday sun."
    *   Specify the lighting style: e.g., "Rembrandt lighting," "Studio lighting," "Natural lighting."
    *   Add details about light quality: e.g., "Soft, diffused light," "Harsh, direct light."
    *   Include any artificial light sources: e.g., "Neon lights," "Street lamps," "Candlelight."
    *   Example: "Golden hour with soft, diffused light"

3.  **Composition and Framing:**
    *   Use photography composition techniques: e.g., "Rule of thirds," "Golden ratio," "Leading lines."
    *   Define the camera angle: e.g., "High angle," "Low angle," "Eye-level."
    *   Describe the perspective: e.g., "Wide shot," "Close-up," "Aerial view."
     *   Example: "Rule of thirds, eye-level"

4.  **Environment and Context:**
    *   Set the scene with rich environmental details: e.g., "Foggy morning in a dense forest," "Snowy mountain range at sunset," "Tropical beach with crystal-clear water."
    *   Include specific weather conditions: e.g., "Rainy day with reflections on the pavement," "Snowy landscape with falling snowflakes," "Sunny afternoon with clear blue skies," "Stormy night with lightning strikes."
    *   Specify the season: e.g., "Spring blossoms in a vibrant meadow," "Summer heat shimmering over a desert landscape," "Autumn foliage in a colorful forest," "Winter frost coating a frozen lake."
    *   Example: "Foggy morning in an urban cityscape during autumn, with wet cobblestone streets reflecting the soft light"

5.  **Artistic Style and Post-Processing:**
    *   Define the overall style: e.g., "Photorealistic," "Cinematic," "Vintage," "Modern," "Impressionistic," "Surreal," "Abstract," "Minimalist."
    *   Mention post-processing effects: e.g., "Color graded with a warm tone," "Film grain for a vintage look," "High dynamic range (HDR) for enhanced detail," "Soft focus for a dreamy effect," "Sharpened for crispness," "Bloom," "Chromatic Aberration", "Lens Flare", "Ray Tracing", "Ambient Occlusion", "Screen Space Reflections", "Global Illumination", "Caustics", "Volumetric Lighting."
    *   Reference specific art movements or artists: e.g., "In the style of Van Gogh's Starry Night," "Inspired by Impressionism's use of light and color," "A tribute to Ansel Adams' black and white landscapes," "Reminiscent of a painting by Monet", "Inspired by the works of Pixar", "In the style of Studio Ghibli", "Inspired by the works of Hayao Miyazaki."
    *   Example: "Photorealistic, color graded with a vintage look and subtle film grain, inspired by Ansel Adams' black and white photography"

6.  **Detail Enhancement:**
    *   Add specific details to the subject: e.g., "Intricate details on a flower petal," "Realistic textures on a weathered stone wall," "Fine details in a bird's feathers," "Subsurface scattering in human skin," "Volumetric lighting through a forest canopy," "Reflections on a glass surface," "Caustics in a swimming pool," "Bokeh in the background", "God Rays", "Anisotropic Reflections", "Screen Space Reflections", "Ray Traced Reflections", "Ambient Occlusion", "Displacement Mapping", "Normal Mapping."
    *   Use descriptive adjectives: e.g., "Luminous," "Ethereal," "Majestic," "Serene," "Dynamic," "Vibrant," "Intricate," "Detailed," "Realistic," "Dramatic," "Peaceful," "Mysterious," "Otherworldly," "Hyperrealistic", "Translucent", "Opaque", "Iridescent", "Luminescent", "Volumetric", "Textured", "Sculpted", "Chiseled."
    *   Example: "Intricate details with subsurface scattering and luminous reflections, creating an ethereal and mysterious atmosphere"

7.  **Color Palette:**
    *   Specify the color scheme: e.g., "Warm colors with a golden hue," "Cool colors with a blue tint," "Monochromatic with shades of gray," "Vibrant colors with a rainbow effect," "Muted colors with a desaturated tone," "Pastel colors for a soft and delicate look," "Earthy tones," "Neon colors", "Complementary Colors", "Analogous Colors", "Triadic Colors", "Split-Complementary."
    *   Reference specific color palettes: e.g., "Analogous color palette with shades of green and blue," "Complementary color palette with red and green accents," "Triadic color palette with yellow, blue, and red tones," "A limited color palette for a minimalist aesthetic", "A split-complementary color scheme", "A Tetradic color scheme", "A custom color palette inspired by nature", "A duotone color scheme."
    *   Example: "Warm colors with a monochromatic tone and pastel accents, creating a serene and peaceful atmosphere"

8.  **Wallpaper-Specific Considerations:**
    *   Aspect Ratio: Specify the aspect ratio for optimal display on screens, e.g., "16:9 aspect ratio for widescreen displays," "21:9 for ultrawide monitors," "3:2 for laptop screens," "9:16 for mobile devices."
    *   Screen Space: Consider how elements are distributed across the screen, e.g., "Balanced composition with visual interest across the entire frame," "Clean negative space on the right side for desktop icons," "Subtle details that don't distract from desktop elements."
    *   Visual Impact: Describe the intended visual effect, e.g., "Eye-catching focal point that draws attention without being distracting," "Subtle textures that add depth without overwhelming," "Calming scene that creates a productive work environment."
    *   Resolution: Specify the resolution quality, e.g., "8K resolution for crystal-clear details on high-resolution displays," "4K resolution with sharp details that remain clear at any screen size."

**Advanced Prompt Engineering Techniques for Wallpapers:**

*   **Wallpaper-Optimized Prompting:** Create prompts specifically designed for wallpaper use. For example: "Design a desktop wallpaper featuring [subject] with a clean composition that leaves space for desktop icons, rendered in a high-resolution format with subtle details that remain visually interesting during daily use, and with a color palette that's easy on the eyes during extended viewing periods."

*   **Chain-of-Thought (CoT) Prompting:** Guide the model by providing intermediate reasoning steps. For example, instead of directly asking for a "3D photorealistic rendering of a car," break it down into steps: "First, imagine a detailed 3D model of a car with realistic textures and lighting. Then, add environmental details such as reflections on the car's surface and shadows on the ground. Finally, render the image in a photorealistic style with ray tracing and ambient occlusion to achieve a high level of realism and visual appeal, and consider the wear and tear on the car's paint and the imperfections in the metal, and the subtle curves and aerodynamic design of the vehicle."
*   **Photography Descriptors:** Use specific photography terms to control the image style. Examples include "Long exposure for motion blur," "Shallow depth of field for subject isolation," "Macro photography for extreme close-ups," "Tilt-shift lens for miniature effect," "HDR for enhanced dynamic range," "Bokeh for blurred background," "Pan shot for capturing motion," "Zoom burst for a dynamic effect," "Double Exposure", "Infrared Photography", "Time-Lapse", "Light Painting", "Photogrammetry", "Stereoscopy", "Orthographic Projection", "Isometric Projection", "Fisheye Lens", "Pinhole Photography."
*   **Shapes and Materials:** Specify the shapes and materials of the objects in the scene. For example, "Geometric shapes with clean lines and sharp edges," "Organic forms with natural textures and flowing curves," "Metallic surfaces with reflections and highlights," "Glass reflections with refractions and distortions," "Subsurface scattering in translucent materials like skin and wax," "Rough textures on weathered surfaces like stone and wood," "Smooth surfaces with subtle gradients and soft highlights," "Iridescent Materials", "Luminescent Materials", "Porous Materials", "Fibrous Materials", "Crystalline Materials", "Amorphous Materials", "Procedural Materials", "Displacement Mapping", "Normal Mapping", "Bump Mapping", "Parallax Occlusion Mapping."
*   **Historical Art Movements:** Reference historical art movements to influence the image style. Examples include "Impressionism with its focus on light and color and loose brushstrokes," "Surrealism with its dreamlike imagery and unexpected juxtapositions and illogical scenes," "Pop Art with its bold colors and iconic imagery and mass production aesthetics," "Art Deco with its geometric patterns and luxurious materials and streamlined shapes," "Renaissance with its classical compositions and realistic portrayals and balanced symmetry," "Baroque with its dramatic lighting and ornate details and exaggerated motion," "Abstract Expressionism with its emphasis on emotion and spontaneity and non-representational forms," "Cyberpunk", "Steampunk", "Gothic", "Renaissance", "Rococo", "Neoclassicism", "Art Nouveau", "Bauhaus", "Fauvism", "Constructivism."
*   **Image Quality Modifiers:** Use terms to control the image quality, such as "8K resolution for maximum detail and clarity", "High resolution for crispness and sharpness and detail", "Photorealistic rendering for natural appearance and realism", "Defect-free image with no artifacts or distortions and clean details", "Superb quality with exceptional detail and realism and visual appeal", "Ultra-detailed with intricate textures and patterns and fine elements", "Hyperrealistic with extreme attention to detail and lifelike accuracy", "Visually stunning with a captivating and immersive effect and breathtaking beauty", "Masterpiece", "Sharp Focus", "Clean", "Crisp", "Perfect", "Flawless", "Immaculate", "High Fidelity", "High Definition."
*   **Negative Prompts:** Use negative prompts to exclude unwanted elements or improve image quality (e.g., "No artifacts to remove unwanted distortions and visual glitches", "No blur to ensure sharpness and clarity and crisp details", "No distortions to maintain accurate perspective and proportions", "No AI art buzzwords to avoid generic styles and overused terms", "No watermarks to ensure a clean image and professional look", "No text to prevent unwanted labels and distracting elements", "No human figures to focus on the environment and scenery", "No animals", "No buildings", "No People", "No Grain", "No Noise", "No Jaggies", "No Aliasing", "No Vignetting").

**Wallpaper Style Guidelines:**

*   **Minimalist Wallpaper:** Use terms like "Minimalist desktop wallpaper with clean lines and ample negative space", "Subtle color gradients that won't distract from desktop icons", "Simple geometric elements with perfect balance", "Elegant design with restrained color palette", "Zen-inspired simplicity with a focus on tranquility", "Understated elegance that enhances productivity", "Uncluttered composition with a single focal point", "Monochromatic scheme with subtle texture variations."

*   **Nature Wallpaper:** Incorporate "High-resolution nature wallpaper with stunning detail that remains clear at any screen size", "Balanced composition that works well with desktop elements", "Serene landscape with a calming color palette ideal for extended viewing", "Subtle natural details that add depth without being distracting", "Atmospheric scene with depth that creates a sense of space on the desktop", "Seasonal theme that refreshes the desktop environment", "Golden ratio composition that naturally guides the eye."

*   **Abstract Wallpaper:** Include "Abstract desktop wallpaper with dynamic shapes and flowing forms", "Vibrant color harmonies that energize the workspace", "Geometric patterns with mathematical precision and perfect symmetry", "Fractal designs with infinite detail at any zoom level", "Gradient meshes with smooth color transitions", "Particle effects with depth and dimension", "Generative art with algorithmic precision", "Digital abstract with clean vector elements", "Organic forms with natural flow and rhythm."

*   **3D Illustration:** Use terms like "3D illustration with clean lines and sharp focus and geometric shapes", "High detail with intricate design and vibrant colors and studio lighting", "Digital art with a modern aesthetic and a stylized look", "Isometric perspective for a unique viewpoint and a balanced composition", "Vector Art", "Low Poly", "Cel-Shading", "Ray Tracing", "Ambient Occlusion", "Global Illumination", "Physically Based Rendering (PBR)", "Non-Photorealistic Rendering (NPR)."

*   **3D Photorealistic Rendering:** Include "3D photorealistic rendering with realistic textures and subsurface scattering", "Global illumination and high-resolution and defect-free image with exceptional detail and visual fidelity", "Ray tracing for realistic reflections and refractions and light effects", "Ambient occlusion for subtle shadows and depth of volume", "Volumetric lighting for atmospheric effects and a sense of immersion", "Depth of field for selective focus and a cinematic look", "Caustics", "God Rays", "Anisotropic Filtering", "Texture Filtering", "Subdivision Surface Modeling", "Procedural Texturing", "Physically Based Shading", "Path Tracing."
"""

    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Add the custom prompt to the instructions
        full_prompt = f"{prompt_instructions}\n\nCustom prompt to enhance: {custom_prompt}"
        
        # Set a timeout for the API call
        start_time = time.time()
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                response = model.generate_content(full_prompt)
                break
            except Exception as retry_error:
                retry_count += 1
                if retry_count >= max_retries:
                    raise retry_error
                logging.warning(f"Retry {retry_count}/{max_retries} after error: {retry_error}")
                time.sleep(1)  # Wait before retrying

        if response.parts:
            enhanced_prompt = response.parts[0].text.strip()
            logging.info(f"Enhanced prompt in {time.time() - start_time:.2f}s")
            
            # Save to cache
            try:
                # Ensure the cache directory exists
                cache_file.parent.mkdir(parents=True, exist_ok=True)
                with open(cache_file, "w") as f:
                    f.write(enhanced_prompt)
                logging.info(f"Saved enhanced prompt to cache: {cache_file}")
            except IOError as e:
                logging.error(f"Error writing to enhanced prompt cache file: {e}")
                
            return enhanced_prompt
        else:
            logging.warning("Gemini model returned empty response.")
            return custom_prompt

    except Exception as e:
        logging.error(f"Error enhancing prompt with Gemini: {e}")
        return custom_prompt

def sanitize_log_content(content):
    """Sanitize log content by masking sensitive information."""
    if isinstance(content, str):
        content = content.replace(os.environ.get("GEMINI_API_KEY", ""), "<GEMINI_API_KEY>")
        content = content.replace(os.environ.get("UNSPLASH_ACCESS_KEY", ""), "<UNSPLASH_ACCESS_KEY>")
        content = content.replace(os.environ.get("PEXELS_API_KEY", ""), "<PEXELS_API_KEY>")
    return content

def save_prompts_to_json(gemini_prompt, enhanced_prompt, filename="prompts.json"):
    """Save the prompts to a JSON file."""
    try:
        with open(filename, "a") as f:
            json.dump({"gemini_prompt": gemini_prompt, "enhanced_prompt": enhanced_prompt}, f)
            f.write("\n")
    except Exception as e:
        logging.error(f"Error saving prompts to JSON: {e}")

def display_menu():
    """Display the main menu options."""
    print("\n===== AI Wallpaper Prompt Generator =====")
    print("1. Generate prompt with Gemini AI")
    print("2. Generate random prompt")
    print("3. Enter custom prompt")
    print("4. Exit")
    return input("Select an option (1-4): ").strip()

def main():
    """Main function to execute the script."""
    print(f"AI Wallpaper Prompt Generator v1.0")
    print(f"Gemini API {'available' if GEMINI_AVAILABLE else 'not available'}")
    print(f"Cache directory: {CACHE_DIR}")
    
    all_tags = nature_tags + space_tags + sea_tags + flowers_tags
    
    while True:
        try:
            choice = display_menu()
            
            if choice == "4":
                print("Exiting. Goodbye!")
                break
                
            if choice == "3":
                # Custom prompt
                custom_prompt = input("Enter your custom prompt: ")
                sanitized_prompt = sanitize_prompt(custom_prompt)
                print(f"Enhancing your prompt...")
                gemini_prompt = sanitized_prompt
                enhanced_prompt = enhance_custom_prompt(sanitized_prompt)
            elif choice == "2":
                # Random prompt
                print(f"Generating random prompt...")
                gemini_prompt = generate_prompt_random(all_tags)
                enhanced_prompt = enhance_custom_prompt(gemini_prompt)
            else:
                # Default: Gemini prompt (choice "1" or invalid input)
                print(f"Generating prompt with Gemini AI...")
                gemini_prompt = generate_prompt_gemini(all_tags)
                if not gemini_prompt:
                    print("Failed to generate prompt with Gemini, using random tags instead.")
                    gemini_prompt = generate_prompt_random(all_tags)
                enhanced_prompt = gemini_prompt
            
            # Display the generated prompt
            print("\n===== Generated Prompt =====")
            print(enhanced_prompt)
            print("============================\n")
            
            # Save the prompt
            save_prompts_to_json(gemini_prompt, enhanced_prompt)
            print(f"Prompt saved to prompts.json")
            
            # Ask if user wants to generate another prompt
            if input("Generate another prompt? (yes/no): ").lower() != "yes":
                print("Exiting. Goodbye!")
                break
                
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            break
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            print(f"An error occurred: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()
