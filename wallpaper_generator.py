
#!/usr/bin/env python3
"""AI Wallpaper Generator - Create stunning AI-generated desktop wallpapers

This script generates high-quality desktop wallpapers using Google's Imagen 3 model
via the Gemini API, or fetches images from providers like Unsplash and Pexels.
It offers various customization options and prompt engineering techniques to create
visually appealing wallpapers tailored to your preferences.
"""
import json
from typing import Optional, Dict, List, Any, Tuple
import os
import platform
import random
import subprocess
import shlex
import logging
import sys
import time
from urllib.parse import quote
import hashlib
import google.generativeai as genai
import requests
import bleach
import ctypes
import html
from absl import logging
# Try to import colorama, but provide fallbacks if not available
try:
    import colorama
    from colorama import Fore, Style, Back
    # Initialize colorama for cross-platform colored terminal output
    colorama.init()
    COLORAMA_AVAILABLE = True
except ImportError:
    # Create dummy classes for Fore, Style, and Back if colorama is not available
    class DummyColorClass:
        def __getattr__(self, name):
            return ""
    
    Fore = DummyColorClass()
    Style = DummyColorClass()
    Back = DummyColorClass()
    COLORAMA_AVAILABLE = False
    print("Note: For colored output, install colorama with: pip install colorama")

# Configure logging
logging.set_verbosity(logging.INFO)

# Check for required dependencies
def check_dependencies():
    """Check if all required dependencies are installed."""
    missing_deps = []
    
    # Check for colorama
    if not COLORAMA_AVAILABLE:
        missing_deps.append("colorama")
    
    # Check for PIL/Pillow
    try:
        import PIL
    except ImportError:
        missing_deps.append("pillow")
    
    # Check for bleach
    try:
        import bleach
    except ImportError:
        missing_deps.append("bleach")
    
    if missing_deps:
        print("\nMissing optional dependencies:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\nTo install missing dependencies, run:")
        print(f"  pip install {' '.join(missing_deps)}")
        print("\nThe script will still run, but some features may be limited.\n")

# Configure the Gemini API key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("\nWarning: GEMINI_API_KEY environment variable not set.")
    print("AI image generation will not be available.\n")

# Create a cache for generated prompts
prompt_cache = {}

# Ensure cache directories exist
os.makedirs("cache", exist_ok=True)
os.makedirs("genimage", exist_ok=True)

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

# User preferences
class UserPreferences:
    """Class to store and manage user preferences."""
    def __init__(self):
        self.preferred_genres = []
        self.preferred_styles = []
        self.preferred_moods = []
        self.aspect_ratio = "16:9"
        self.negative_prompts = []
        self.load_preferences()
    
    def load_preferences(self, filename: str = "user_preferences.json") -> None:
        """Load user preferences from a JSON file."""
        try:
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    prefs = json.load(f)
                    self.preferred_genres = prefs.get("preferred_genres", [])
                    self.preferred_styles = prefs.get("preferred_styles", [])
                    self.preferred_moods = prefs.get("preferred_moods", [])
                    self.aspect_ratio = prefs.get("aspect_ratio", "16:9")
                    self.negative_prompts = prefs.get("negative_prompts", [])
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error loading preferences: {e}")
    
    def save_preferences(self, filename: str = "user_preferences.json") -> None:
        """Save user preferences to a JSON file."""
        try:
            prefs = {
                "preferred_genres": self.preferred_genres,
                "preferred_styles": self.preferred_styles,
                "preferred_moods": self.preferred_moods,
                "aspect_ratio": self.aspect_ratio,
                "negative_prompts": self.negative_prompts
            }
            with open(filename, "w") as f:
                json.dump(prefs, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving preferences: {e}")

# Initialize user preferences
user_prefs = UserPreferences()

def load_last_genre(filename: str = "last_genre.json") -> Optional[str]:
    """Loads the last used genre from a JSON file."""
    try:
        if os.path.exists(filename):
            with open(filename, "r") as f:
                return json.load(f).get("last_genre")
    except (FileNotFoundError, json.JSONDecodeError, IOError) as e:
        logging.error(f"Error loading last genre: {e}")
    return None

def save_last_genre(genre, filename="last_genre.json"):
    """Saves the last used genre to a JSON file."""
    try:
        with open(filename, "w") as f:
            json.dump({"last_genre": genre}, f, indent=2)
    except Exception as e:
        logging.error(f"Error saving last genre: {e}")

def print_colored(text, color=Fore.WHITE, style=Style.NORMAL, end="\n"):
    """Print colored text to the terminal."""
    print(f"{style}{color}{text}{Style.RESET_ALL}", end=end)

def print_header(text):
    """Print a formatted header."""
    try:
        width = min(80, os.get_terminal_size().columns)
    except (AttributeError, OSError):
        # Default width if terminal size cannot be determined
        width = 80
    
    print_colored("\n" + "=" * width, Fore.CYAN, Style.BRIGHT)
    print_colored(f" {text.center(width - 2)} ", Fore.CYAN, Style.BRIGHT)
    print_colored("=" * width + "\n", Fore.CYAN, Style.BRIGHT)

def print_section(text):
    """Print a formatted section header."""
    print_colored(f"\n{text}", Fore.GREEN, Style.BRIGHT)
    print_colored("-" * len(text), Fore.GREEN, Style.BRIGHT)

def print_option(key, description):
    """Print a formatted option."""
    print_colored(f"  {key}: ", Fore.YELLOW, Style.BRIGHT, end="")
    print_colored(description)

def print_success(text):
    """Print a success message."""
    print_colored(f"✓ {text}", Fore.GREEN, Style.BRIGHT)

def print_error(text):
    """Print an error message."""
    print_colored(f"✗ {text}", Fore.RED, Style.BRIGHT)

def print_warning(text):
    """Print a warning message."""
    print_colored(f"⚠ {text}", Fore.YELLOW, Style.BRIGHT)

def print_info(text):
    """Print an info message."""
    print_colored(f"ℹ {text}", Fore.BLUE, Style.NORMAL)

def print_prompt(text):
    """Print a prompt message."""
    print_colored(f"\n> {text} ", Fore.MAGENTA, Style.BRIGHT, end="")

def get_validated_input(prompt, options=None, default=None, allow_empty=False):
    """Get validated input from the user."""
    while True:
        print_prompt(prompt)
        user_input = input().strip().lower()
        
        if not user_input:
            if allow_empty and default is not None:
                return default
            elif allow_empty:
                return ""
            print_warning("Input cannot be empty. Please try again.")
            continue
            
        if options and user_input not in options:
            print_warning(f"Invalid input. Please choose from: {', '.join(options)}")
            continue
            
        return user_input

def show_spinner(message, duration=2):
    """Show a spinner animation with a message."""
    # Check if we're in an interactive terminal
    if not sys.stdout.isatty() or not COLORAMA_AVAILABLE:
        # Just print the message if not in an interactive terminal
        print_info(message)
        time.sleep(duration)
        return
    
    try:
        spinner = ["|", "/", "-", "\\"]
        start_time = time.time()
        i = 0
        
        while time.time() - start_time < duration:
            sys.stdout.write(f"\r{Fore.CYAN}{spinner[i % len(spinner)]} {message}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        
        sys.stdout.write("\r" + " " * (len(message) + 2) + "\r")
        sys.stdout.flush()
    except (IOError, ValueError):
        # Fallback if spinner fails
        print_info(message)
        time.sleep(duration)

def generate_prompt_gemini(tags, use_cache=True, mood=None, style=None):
    """Generate a prompt using the Gemini model with enhanced options.
    
    Args:
        tags: List of tags to include in the prompt
        use_cache: Whether to use cached prompts
        mood: Optional mood to incorporate (e.g., "peaceful", "dramatic")
        style: Optional style to incorporate (e.g., "cinematic", "minimalist")
    
    Returns:
        A generated prompt string
    """
    # Create a unique cache key that includes all parameters
    cache_params = [", ".join(tags)]
    if mood:
        cache_params.append(f"mood:{mood}")
    if style:
        cache_params.append(f"style:{style}")
    
    cache_key = " | ".join(cache_params)

    if use_cache and cache_key in prompt_cache:
        print_info(f"Using cached prompt for: {cache_key}")
        return prompt_cache[cache_key]

    # Load available genres
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

    # Prioritize user's preferred genres if available
    if user_prefs.preferred_genres:
        preferred_available = [g for g in user_prefs.preferred_genres if g in available_genres]
        if preferred_available:
            available_genres = preferred_available + [g for g in available_genres if g not in preferred_available]

    # Avoid repeating the last genre
    last_genre = load_last_genre()
    if last_genre and last_genre in available_genres:
        available_genres.remove(last_genre)

    # Select a genre
    if not available_genres:
        # If somehow we've exhausted all genres, reset the list
        chosen_genre = random.choice([
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
        ])
    else:
        chosen_genre = random.choice(available_genres)

    # Save the chosen genre for next time
    save_last_genre(chosen_genre)
    
    # Show what we're doing
    show_spinner(f"Generating prompt for {chosen_genre}...", 1)

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

The final prompt should read like a professional photographer's shot description, emphasizing Imagen 3's strengths in photorealism, lighting, and material rendering while maintaining physical accuracy and natural composition.

**Abstract & 3D Specialized Guidelines**

Core Focus Areas:
1. Geometric Composition
   - Primary shapes: spheres, cubes, pyramids, toruses, cones, cylinders
   - Complex geometry: fractals, voronoi patterns, tessellations, NURBS surfaces
   - Architectural abstractions: deconstructed forms, minimalist structures, parametric designs
   - Organic abstractions: fluid dynamics, smoke patterns, wave forms, cellular structures

2. Material Properties
   - Metals: brushed, polished, oxidized, chrome, gold, copper, aluminum, steel, titanium
   - Glass: clear, frosted, textured, prismatic, colored, dichroic
   - Composites: carbon fiber, marble, concrete, ceramics, wood, stone
   - Surfaces: matte, glossy, reflective, translucent, subsurface scattering, anisotropic

3. Lighting Scenarios
   - Studio setups: 3-point lighting, rim lighting, area lights, softboxes, reflectors
   - Environmental lighting: HDRI environments, global illumination, natural daylight
   - Dramatic effects: volumetric lighting, caustics, light painting, lens flares
   - Color lighting: split complementary, RGB, gradient mapping, spectral rendering

4. Camera Technical Specs
   - Macro photography: extreme close-ups of textures and patterns, microscopic details
   - Tilt-shift: selective focus on geometric elements, miniature effect
   - Focus stacking: ultra-sharp detail across entire scene, extended depth of field
   - Long exposure: motion blur and light trails, time-lapse effects

Composition Frameworks:
1. Geometric Arrangements
   - Golden ratio spiral compositions, Fibonacci sequence
   - Rule of thirds with tension points, visual balance
   - Symmetrical balance, mirrored elements
   - Dynamic diagonal flow, leading lines
   - Repetition and rhythm, patterns and sequences

2. Space and Scale
   - Micro to macro transitions, zooming effects
   - Forced perspective, optical illusions
   - Infinite recursion, fractal patterns
   - Negative space utilization, minimalist design

3. Motion and Flow
   - Particle systems, dynamic simulations
   - Fluid dynamics, liquid simulations
   - Kinetic sculptures, moving elements
   - Time-based patterns, animated sequences

Material Combinations:
1. Hard Surface
   - Chrome + matte black, high-tech aesthetic
   - Polished metal + frosted glass, elegant design
   - Concrete + brass, industrial style
   - Carbon fiber + aluminum, modern look

2. Organic Abstract
   - Liquid metal, fluid forms
   - Crystalline structures, geometric patterns
   - Smoke and particle effects, ethereal visuals
   - Natural pattern abstractions, organic textures

Prompt Structure for Abstract/3D:
"[Primary Form] with [Material Properties] captured using [Camera Technique], featuring [Lighting Setup] and [Environmental Context], rendered in [Color Scheme] with [Composition Style] composition, emphasizing [Technical Detail] at [Scale/Perspective], with [Artistic Style] influence"

Example Prompts:
1. Geometric: "A polished chrome sphere intersecting with frosted glass cubes, captured in ultra-sharp 8K detail using focus stacking with a macro lens, lit by three-point studio lighting with cyan and magenta rim lights, composed using golden ratio spiral, emphasizing reflections and refractions at macro scale, with a minimalist design influence"

2. Organic Abstract: "Flowing liquid metal forms creating abstract patterns, shot with a tilt-shift lens for selective focus, illuminated by gradient-mapped HDRI lighting in cool tones, featuring subtle caustics and subsurface scattering, composed with dynamic diagonal movement, with a surrealist art influence"

3. Architectural Abstract: "Minimalist concrete and steel geometric forms photographed with a wide-angle lens, utilizing natural daylight through volumetric fog, emphasizing sharp edges and material transitions, composed with strong symmetry and repeated elements, with a Bauhaus architectural influence"

Technical Requirements:
- Always specify exact material properties (e.g., polished chrome, frosted glass)
- Include at least one specific lighting technique (e.g., three-point lighting, HDRI)
- Define camera position and lens choice (e.g., macro lens, wide-angle lens)
- Mention post-processing treatment (if any) (e.g., color graded, film grain)
- Specify scale and perspective (e.g., macro scale, wide shot)
- Include composition framework (e.g., golden ratio, rule of thirds)
- Reference artistic style (e.g., minimalist, surrealist, Bauhaus)

Avoid:
- Mixing too many materials (stick to 2-3 maximum)
- Unrealistic material behaviors (e.g., floating objects without support)
- Physically impossible lighting (e.g., light sources from nowhere)
- Over-complicated compositions (e.g., too many elements)
- Vague material descriptions (e.g., "shiny metal")
- Generic abstract terms (e.g., "abstract art")

The final prompt should create a clear mental image of a physically accurate, visually striking abstract or 3D scene that maximizes Imagen 3's capabilities in material rendering, lighting simulation, and geometric precision, while also incorporating artistic and design influences."""

    prompt = f"{prompt_instructions} Tags: {', '.join(tags)}"
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)

        if response.parts:
            gemini_prompt = response.parts[0].text.strip()
            logging.info(f"Generated Gemini prompt: {gemini_prompt}")

            prompt_cache[cache_key] = gemini_prompt
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
    prompt = random.choice(all_tags)
    logging.info(f"Generated prompt: {prompt}")
    return prompt

def get_provider_cache_path(prompt):
    """Get the cache path for the provider image."""
    hash_object = hashlib.sha256(prompt.encode())
    return f"cache/{hash_object.hexdigest()}.png"

def get_generated_image_path(prompt):
    """Get the cache path for the generated image."""
    hash_object = hashlib.sha256(prompt.encode())
    return f"genimage/{hash_object.hexdigest()}.png"

def detect_linux_desktop_environment():
    """Detect the Linux desktop environment."""
    # Check environment variables
    desktop_env = os.environ.get('XDG_CURRENT_DESKTOP', '')
    if desktop_env:
        return desktop_env.upper()
    
    # Check for common processes
    try:
        output = subprocess.check_output(['ps', '-e'], text=True)
        if 'gnome-session' in output:
            return 'GNOME'
        elif 'kwin' in output:
            return 'KDE'
        elif 'xfce4-session' in output:
            return 'XFCE'
        elif 'mate-session' in output:
            return 'MATE'
        elif 'cinnamon-session' in output:
            return 'CINNAMON'
        elif 'i3' in output:
            return 'I3'
        elif 'sway' in output:
            return 'SWAY'
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    
    return 'UNKNOWN'

def set_wallpaper(image_path):
    """Set the wallpaper based on the operating system."""
    os_name = platform.system()
    try:
        if os_name == "Windows":
            SPI_SETDESKWALLPAPER = 0x0014
            SPIF_UPDATEINIFILE = 0x01
            SPIF_SENDWININICHANGE = 0x02
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)
            logging.info("Wallpaper set successfully on Windows")
        elif os_name == "Darwin":
            script = f'tell application "Finder" to set desktop picture to POSIX file "{image_path}"'
            command = f"osascript -e '{script}'"
            subprocess.run(shlex.split(command), check=True, capture_output=True, text=True)
            logging.info("Wallpaper set successfully on macOS")
        elif os_name == "Linux":
            absolute_path = os.path.abspath(image_path)
            file_uri = "file://" + absolute_path
            
            # Detect desktop environment
            desktop_env = detect_linux_desktop_environment()
            print_info(f"Detected Linux desktop environment: {desktop_env}")
            
            if desktop_env in ['GNOME', 'UBUNTU:GNOME', 'UNITY', 'UBUNTU']:
                # GNOME, Unity
                command = ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", file_uri]
                subprocess.run(command, check=True, capture_output=True, text=True)
                # For GNOME 42+ with dark mode support
                try:
                    command = ["gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", file_uri]
                    subprocess.run(command, check=True, capture_output=True, text=True)
                except subprocess.CalledProcessError:
                    pass  # Ignore if not supported
            elif desktop_env == 'CINNAMON':
                # Cinnamon
                command = ["gsettings", "set", "org.cinnamon.desktop.background", "picture-uri", file_uri]
                subprocess.run(command, check=True, capture_output=True, text=True)
            elif desktop_env == 'MATE':
                # MATE
                command = ["gsettings", "set", "org.mate.background", "picture-filename", absolute_path]
                subprocess.run(command, check=True, capture_output=True, text=True)
            elif desktop_env == 'XFCE':
                # XFCE
                try:
                    # Get the current monitor
                    output = subprocess.check_output(["xfconf-query", "-c", "xfce4-desktop", "-l"], text=True)
                    monitors = [line for line in output.split('\n') if line.endswith("last-image")]
                    
                    if monitors:
                        for monitor in monitors:
                            command = ["xfconf-query", "-c", "xfce4-desktop", "-p", monitor, "-s", absolute_path]
                            subprocess.run(command, check=True, capture_output=True, text=True)
                    else:
                        print_warning("No monitors found for XFCE")
                except (subprocess.SubprocessError, FileNotFoundError):
                    print_warning("Failed to set wallpaper using xfconf-query")
            elif desktop_env in ['KDE', 'PLASMA', 'PLASMA:KDE']:
                # KDE Plasma
                try:
                    script = f"""
                    var allDesktops = desktops();
                    for (var i=0; i<allDesktops.length; i++) {{
                        d = allDesktops[i];
                        d.wallpaperPlugin = "org.kde.image";
                        d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
                        d.writeConfig("Image", "{absolute_path}");
                    }}
                    """
                    command = ["qdbus", "org.kde.plasmashell", "/PlasmaShell", "org.kde.PlasmaShell.evaluateScript", script]
                    subprocess.run(command, check=True, capture_output=True, text=True)
                except (subprocess.SubprocessError, FileNotFoundError):
                    print_warning("Failed to set wallpaper using KDE Plasma method")
            elif desktop_env in ['I3', 'SWAY']:
                # i3/sway - try feh first, then nitrogen
                try:
                    command = ["feh", "--bg-fill", absolute_path]
                    subprocess.run(command, check=True, capture_output=True, text=True)
                except (subprocess.SubprocessError, FileNotFoundError):
                    try:
                        command = ["nitrogen", "--set-zoom-fill", absolute_path]
                        subprocess.run(command, check=True, capture_output=True, text=True)
                    except (subprocess.SubprocessError, FileNotFoundError):
                        print_warning("Failed to set wallpaper using feh or nitrogen")
            else:
                # Try common methods as fallback
                success = False
                
                # Try gsettings (GNOME/Unity/Cinnamon)
                try:
                    command = ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", file_uri]
                    subprocess.run(command, check=True, capture_output=True, text=True)
                    success = True
                except (subprocess.SubprocessError, FileNotFoundError):
                    pass
                
                # Try feh (works with many window managers)
                if not success:
                    try:
                        command = ["feh", "--bg-fill", absolute_path]
                        subprocess.run(command, check=True, capture_output=True, text=True)
                        success = True
                    except (subprocess.SubprocessError, FileNotFoundError):
                        pass
                
                # Try nitrogen (another common wallpaper setter)
                if not success:
                    try:
                        command = ["nitrogen", "--set-zoom-fill", absolute_path]
                        subprocess.run(command, check=True, capture_output=True, text=True)
                        success = True
                    except (subprocess.SubprocessError, FileNotFoundError):
                        pass
                
                if success:
                    print_info("Wallpaper set using fallback method")
                else:
                    print_warning("Could not set wallpaper with any known method")
                    return False
            
            logging.info("Wallpaper set successfully on Linux")
        else:
            logging.warning(f"Unsupported operating system: {os_name}")
            return False
    except subprocess.CalledProcessError as e:
        logging.error(f"Error setting wallpaper (subprocess): {e}")
        logging.error(f"Stdout: {e.stdout}")
        logging.error(f"Stderr: {e.stderr}")
    except OSError as e:
        logging.error(f"OS error setting wallpaper: {e}")
    except ValueError as e:
        logging.error(f"Value error setting wallpaper: {e}")
    except Exception as e:
        logging.error(f"Unexpected error setting wallpaper: {e}")

def enhance_custom_prompt(custom_prompt):
    """Enhance the custom prompt using the Gemini model."""
    prompt_instructions = f"""
You are an expert prompt engineer for the Imagen 3 image generation model. Your task is to transform the given custom prompt into a highly detailed and photorealistic masterpiece. Focus on adding specific technical details related to photography and cinematography to maximize the visual impact and realism of the generated image.

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

**Advanced Prompt Engineering Techniques:**

*   **Chain-of-Thought (CoT) Prompting:** Guide the model by providing intermediate reasoning steps. For example, instead of directly asking for a "3D photorealistic rendering of a car," break it down into steps: "First, imagine a detailed 3D model of a car with realistic textures and lighting. Then, add environmental details such as reflections on the car's surface and shadows on the ground. Finally, render the image in a photorealistic style with ray tracing and ambient occlusion to achieve a high level of realism and visual appeal, and consider the wear and tear on the car's paint and the imperfections in the metal, and the subtle curves and aerodynamic design of the vehicle."
*   **Photography Descriptors:** Use specific photography terms to control the image style. Examples include "Long exposure for motion blur," "Shallow depth of field for subject isolation," "Macro photography for extreme close-ups," "Tilt-shift lens for miniature effect," "HDR for enhanced dynamic range," "Bokeh for blurred background," "Pan shot for capturing motion," "Zoom burst for a dynamic effect," "Double Exposure", "Infrared Photography", "Time-Lapse", "Light Painting", "Photogrammetry", "Stereoscopy", "Orthographic Projection", "Isometric Projection", "Fisheye Lens", "Pinhole Photography."
*   **Shapes and Materials:** Specify the shapes and materials of the objects in the scene. For example, "Geometric shapes with clean lines and sharp edges," "Organic forms with natural textures and flowing curves," "Metallic surfaces with reflections and highlights," "Glass reflections with refractions and distortions," "Subsurface scattering in translucent materials like skin and wax," "Rough textures on weathered surfaces like stone and wood," "Smooth surfaces with subtle gradients and soft highlights," "Iridescent Materials", "Luminescent Materials", "Porous Materials", "Fibrous Materials", "Crystalline Materials", "Amorphous Materials", "Procedural Materials", "Displacement Mapping", "Normal Mapping", "Bump Mapping", "Parallax Occlusion Mapping."
*   **Historical Art Movements:** Reference historical art movements to influence the image style. Examples include "Impressionism with its focus on light and color and loose brushstrokes," "Surrealism with its dreamlike imagery and unexpected juxtapositions and illogical scenes," "Pop Art with its bold colors and iconic imagery and mass production aesthetics," "Art Deco with its geometric patterns and luxurious materials and streamlined shapes," "Renaissance with its classical compositions and realistic portrayals and balanced symmetry," "Baroque with its dramatic lighting and ornate details and exaggerated motion," "Abstract Expressionism with its emphasis on emotion and spontaneity and non-representational forms," "Cyberpunk", "Steampunk", "Gothic", "Renaissance", "Rococo", "Neoclassicism", "Art Nouveau", "Bauhaus", "Fauvism", "Constructivism."
*   **Image Quality Modifiers:** Use terms to control the image quality, such as "8K resolution for maximum detail and clarity", "High resolution for crispness and sharpness and detail", "Photorealistic rendering for natural appearance and realism", "Defect-free image with no artifacts or distortions and clean details", "Superb quality with exceptional detail and realism and visual appeal", "Ultra-detailed with intricate textures and patterns and fine elements", "Hyperrealistic with extreme attention to detail and lifelike accuracy", "Visually stunning with a captivating and immersive effect and breathtaking beauty", "Masterpiece", "Sharp Focus", "Clean", "Crisp", "Perfect", "Flawless", "Immaculate", "High Fidelity", "High Definition."
*   **Negative Prompts:** Use negative prompts to exclude unwanted elements or improve image quality (e.g., "No artifacts to remove unwanted distortions and visual glitches", "No blur to ensure sharpness and clarity and crisp details", "No distortions to maintain accurate perspective and proportions", "No AI art buzzwords to avoid generic styles and overused terms", "No watermarks to ensure a clean image and professional look", "No text to prevent unwanted labels and distracting elements", "No human figures to focus on the environment and scenery", "No animals", "No buildings", "No People", "No Grain", "No Noise", "No Jaggies", "No Aliasing", "No Vignetting").

**Specific Styles Guidelines:**

*   **3D Illustration:** Use terms like "3D illustration with clean lines and sharp focus and geometric shapes", "High detail with intricate design and vibrant colors and studio lighting", "Digital art with a modern aesthetic and a stylized look", "Isometric perspective for a unique viewpoint and a balanced composition", "Vector Art", "Low Poly", "Cel-Shading", "Ray Tracing", "Ambient Occlusion", "Global Illumination", "Physically Based Rendering (PBR)", "Non-Photorealistic Rendering (NPR)."
*   **3D Cartoon:** Incorporate "3D cartoon with animated character design and stylized features and exaggerated proportions", "Smooth shading and soft lighting for a whimsical style and a playful mood", "Exaggerated features and bright colors for a fun and engaging look and a cheerful atmosphere", "Simplified forms and dynamic poses for a lively effect and a sense of energy", "Claymation", "Stop Motion", "Puppet Animation", "Anime", "Chibi Style", "Kawaii Style", "Toon Shading", "Silhouette Animation", "Hand-Painted Textures", "Stylized Proportions."
*   **3D Photorealistic Rendering (Pixar Style):** Include "3D photorealistic rendering in the style of Pixar with realistic textures and subsurface scattering", "Global illumination and high-resolution and defect-free image with exceptional detail and visual fidelity", reference specific Pixar films or characters for inspiration (e.g., "In the style of Toy Story with realistic textures and lighting and a heartwarming atmosphere", "Inspired by Finding Nemo with vibrant colors and underwater details and a sense of wonder"), and use techniques like "Ray tracing for realistic reflections and refractions and light effects", "Ambient occlusion for subtle shadows and depth and a sense of volume", "Volumetric lighting for atmospheric effects and a sense of immersion", "Depth of field for selective focus and a cinematic look", "Caustics", "God Rays", "Anisotropic Filtering", "Texture Filtering", "Subdivision Surface Modeling", "Procedural Texturing", "Physically Based Shading", "Path Tracing", "Microfacet Theory", "Bidirectional Reflectance Distribution Function (BRDF)."

**Example Prompts:**

*   Original: "A lone tree on a hill."
*   Enhanced: "Shot on Hasselblad with a 35mm lens at f/8, a lone tree on a hill during golden hour, with soft, diffused light, using the rule of thirds for composition, photorealistic style, color graded with warm colors and a vintage look, ultra-detailed with subsurface scattering, creating an ethereal and mysterious atmosphere, reminiscent of a painting by Monet, with ray tracing and ambient occlusion, showcasing the intricate bark texture and the way light filters through the leaves, rendered with global illumination for a truly immersive 3D experience, using physically based rendering for realistic material properties, and displacement mapping to add fine details to the bark and leaves."

*   Original: "A futuristic cityscape."
*   Enhanced: "ARRI Alexa captures a futuristic cityscape at blue hour, with neon lights and volumetric lighting, using a wide-angle 16mm lens, high dynamic range (HDR), cinematic style, leading lines for composition, and a cool color palette with vibrant accents, visually stunning with intricate details, creating a dynamic and captivating effect, inspired by the cyberpunk art movement, with screen space reflections and iridescent materials, showcasing the towering skyscrapers and the bustling streets below, rendered with ray traced reflections and anisotropic filtering for a hyperrealistic 3D effect, using displacement mapping to add fine details to the building surfaces, and volumetric lighting to create a sense of depth and atmosphere."

Your enhanced prompt should be a single, descriptive sentence that combines the original prompt with the technical details mentioned above. Focus on creating a vivid and realistic image in the mind of the viewer, using specific details and descriptive language to maximize the visual impact and create a truly immersive experience. The enhanced prompt should read like a professional photographer's or cinematographer's shot description, emphasizing Imagen 3's strengths in photorealism, lighting, and material rendering while maintaining physical accuracy and natural composition. It should also emphasize 3D characteristics such as realistic textures, lighting, and reflections, and utilize advanced rendering techniques to achieve a high level of visual fidelity.
"""

    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt_instructions + custom_prompt)

        if response.parts:
            enhanced_prompt = response.parts[0].text.strip()
            logging.info(f"Original prompt: {sanitize_log_content(custom_prompt)}")
            logging.info(f"Enhanced prompt: {sanitize_log_content(enhanced_prompt)}")
            return enhanced_prompt
        else:
            logging.warning("Gemini model returned empty response, using original prompt")
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

def manage_preferences():
    """Manage user preferences for wallpaper generation."""
    print_header("Wallpaper Generator Preferences")
    
    while True:
        print_section("Current Preferences")
        print_info(f"Preferred Genres: {', '.join(user_prefs.preferred_genres) if user_prefs.preferred_genres else 'None'}")
        print_info(f"Preferred Styles: {', '.join(user_prefs.preferred_styles) if user_prefs.preferred_styles else 'None'}")
        print_info(f"Preferred Moods: {', '.join(user_prefs.preferred_moods) if user_prefs.preferred_moods else 'None'}")
        print_info(f"Aspect Ratio: {user_prefs.aspect_ratio}")
        print_info(f"Negative Prompts: {', '.join(user_prefs.negative_prompts) if user_prefs.negative_prompts else 'None'}")
        
        print_section("Options")
        print_option("1", "Add/Remove Preferred Genres")
        print_option("2", "Add/Remove Preferred Styles")
        print_option("3", "Add/Remove Preferred Moods")
        print_option("4", "Change Aspect Ratio")
        print_option("5", "Add/Remove Negative Prompts")
        print_option("6", "Save and Return to Main Menu")
        
        choice = get_validated_input("Select an option (1-6)", ["1", "2", "3", "4", "5", "6"])
        
        if choice == "1":
            manage_list_preference("Preferred Genres", user_prefs.preferred_genres, [
                "Nature & Landscapes", "Mountains & Peaks", "Forests & Woods", "Desert & Dunes",
                "Urban & Architecture", "Modern Cityscapes", "Space & Cosmos", "Sea & Ocean",
                "Abstract & 3D", "Geometric Patterns", "Fantasy Landscapes", "Sci-Fi Environments"
            ])
        elif choice == "2":
            manage_list_preference("Preferred Styles", user_prefs.preferred_styles, [
                "Photorealistic", "Cinematic", "Vintage", "Modern", "Minimalist",
                "Surreal", "Abstract", "Impressionistic", "Cyberpunk", "Steampunk"
            ])
        elif choice == "3":
            manage_list_preference("Preferred Moods", user_prefs.preferred_moods, [
                "Peaceful", "Dramatic", "Mysterious", "Energetic", "Melancholic",
                "Joyful", "Romantic", "Eerie", "Nostalgic", "Contemplative"
            ])
        elif choice == "4":
            print_section("Aspect Ratio Options")
            print_option("1", "16:9 (Widescreen)")
            print_option("2", "21:9 (Ultrawide)")
            print_option("3", "4:3 (Standard)")
            print_option("4", "1:1 (Square)")
            print_option("5", "9:16 (Portrait)")
            
            ratio_choice = get_validated_input("Select an aspect ratio (1-5)", ["1", "2", "3", "4", "5"])
            if ratio_choice == "1":
                user_prefs.aspect_ratio = "16:9"
            elif ratio_choice == "2":
                user_prefs.aspect_ratio = "21:9"
            elif ratio_choice == "3":
                user_prefs.aspect_ratio = "4:3"
            elif ratio_choice == "4":
                user_prefs.aspect_ratio = "1:1"
            elif ratio_choice == "5":
                user_prefs.aspect_ratio = "9:16"
            
            print_success(f"Aspect ratio set to {user_prefs.aspect_ratio}")
        elif choice == "5":
            manage_list_preference("Negative Prompts", user_prefs.negative_prompts, [
                "text", "watermark", "blur", "distortion", "artifacts", "noise",
                "people", "animals", "buildings", "vehicles", "logos"
            ])
        elif choice == "6":
            user_prefs.save_preferences()
            print_success("Preferences saved!")
            break

def manage_list_preference(name, preference_list, suggestions):
    """Manage a list preference by adding or removing items."""
    print_section(f"Manage {name}")
    print_info(f"Current {name}: {', '.join(preference_list) if preference_list else 'None'}")
    
    print_section("Options")
    print_option("1", f"Add to {name}")
    print_option("2", f"Remove from {name}")
    print_option("3", "Return to Preferences Menu")
    
    choice = get_validated_input("Select an option (1-3)", ["1", "2", "3"])
    
    if choice == "1":
        print_section(f"Suggested {name}")
        for i, suggestion in enumerate(suggestions, 1):
            print_option(str(i), suggestion)
        print_option("c", "Custom entry")
        
        add_choice = get_validated_input(f"Select a suggestion (1-{len(suggestions)}) or 'c' for custom",
                                        [str(i) for i in range(1, len(suggestions)+1)] + ["c"])
        
        if add_choice == "c":
            custom_entry = input(f"Enter custom {name.lower()[:-1]}: ").strip()
            if custom_entry and custom_entry not in preference_list:
                preference_list.append(custom_entry)
                print_success(f"Added '{custom_entry}' to {name.lower()}")
            elif custom_entry in preference_list:
                print_warning(f"'{custom_entry}' is already in your {name.lower()}")
            else:
                print_warning("Nothing added (empty input)")
        else:
            suggestion_idx = int(add_choice) - 1
            if suggestions[suggestion_idx] not in preference_list:
                preference_list.append(suggestions[suggestion_idx])
                print_success(f"Added '{suggestions[suggestion_idx]}' to {name.lower()}")
            else:
                print_warning(f"'{suggestions[suggestion_idx]}' is already in your {name.lower()}")
    
    elif choice == "2":
        if not preference_list:
            print_warning(f"No {name.lower()} to remove")
            return
        
        print_section(f"Current {name}")
        for i, item in enumerate(preference_list, 1):
            print_option(str(i), item)
        
        remove_choice = get_validated_input(f"Select item to remove (1-{len(preference_list)})",
                                           [str(i) for i in range(1, len(preference_list)+1)])
        
        removed_item = preference_list.pop(int(remove_choice) - 1)
        print_success(f"Removed '{removed_item}' from {name.lower()}")

def generate_wallpaper(source_type, prompt_type=None, custom_prompt=None, mood=None, style=None):
    """Generate a wallpaper based on the specified parameters."""
    enhanced_prompt = None
    gemini_prompt = None
    
    # Step 1: Generate or get the prompt
    if source_type == "generate":
        if prompt_type == "custom" and custom_prompt:
            print_info("Processing custom prompt...")
            sanitized_prompt = sanitize_prompt(custom_prompt)
            gemini_prompt = sanitized_prompt
            enhanced_prompt = enhance_custom_prompt(sanitized_prompt)
        elif prompt_type == "random":
            print_info("Generating random prompt...")
            all_tags = nature_tags + space_tags + sea_tags + flowers_tags + urban_tags + fantasy_tags + abstract_tags
            gemini_prompt = generate_prompt_random(all_tags)
            enhanced_prompt = enhance_custom_prompt(gemini_prompt)
        else:  # gemini
            print_section("Generating AI Prompt")
            print_info("Using Google's Gemini AI to create a unique wallpaper prompt...")
            all_tags = nature_tags + space_tags + sea_tags + flowers_tags + urban_tags + fantasy_tags + abstract_tags
            
            show_spinner("Analyzing your preferences and generating ideas...", 1)
            gemini_prompt = generate_prompt_gemini(all_tags, mood=mood, style=style)
            
            if not gemini_prompt:
                print_warning("Gemini encountered an issue. Generating a random prompt instead...")
                gemini_prompt = generate_prompt_random(all_tags)
                print_info("Here's your random prompt:")
            else:
                print_success("AI prompt generated successfully!")
                
            enhanced_prompt = gemini_prompt
            print_info("Review your prompt below:")
    elif source_type == "provider":
        print_info("Generating prompt for image provider...")
        all_tags = nature_tags + space_tags + sea_tags + flowers_tags + urban_tags
        gemini_prompt = generate_prompt_random(all_tags)
        enhanced_prompt = gemini_prompt
    
    # Step 2: Display the prompt and get confirmation
    if enhanced_prompt:
        print_section("Generated Prompt")
        print_info(enhanced_prompt)
        
        for attempt in range(3):
            save_prompts_to_json(gemini_prompt, enhanced_prompt)
            confirmation = get_validated_input(f"Proceed with this prompt? (yes/no) (Attempt {attempt + 1}/3)", ["yes", "no", "y", "n"])
            if confirmation in ["yes", "y"]:
                break
            else:
                if prompt_type == "custom":
                    custom_prompt = get_validated_input("Enter your custom prompt", allow_empty=False)
                    sanitized_prompt = sanitize_prompt(custom_prompt)
                    gemini_prompt = sanitized_prompt
                    enhanced_prompt = enhance_custom_prompt(sanitized_prompt)
                elif prompt_type == "random":
                    all_tags = nature_tags + space_tags + sea_tags + flowers_tags + urban_tags + fantasy_tags + abstract_tags
                    gemini_prompt = generate_prompt_random(all_tags)
                    enhanced_prompt = enhance_custom_prompt(gemini_prompt)
                else:  # gemini
                    all_tags = nature_tags + space_tags + sea_tags + flowers_tags + urban_tags + fantasy_tags + abstract_tags
                    gemini_prompt = generate_prompt_gemini(all_tags, use_cache=False, mood=mood, style=style)
                    if not gemini_prompt:
                        print_warning("Failed to generate prompt with Gemini, using random tags instead.")
                        gemini_prompt = generate_prompt_random(all_tags)
                    enhanced_prompt = gemini_prompt
                
                print_section("New Generated Prompt")
                print_info(enhanced_prompt)
        else:
            print_warning("Limit reached. Stopping the process.")
            return False
    
    # Step 3: Generate or fetch the image
    if source_type == "generate":
        if not GEMINI_API_KEY:
            print_error("No Gemini API key configured - please check your environment variables")
            return False
        
        try:
            from google import genai
            from google.genai import types
            try:
                from PIL import Image
                PIL_AVAILABLE = True
            except ImportError:
                PIL_AVAILABLE = False
                print_warning("PIL not installed. Some image processing features may be limited.")
                print_info("To install PIL: pip install pillow")
            from io import BytesIO

            print_info("Generating image with Imagen 3...")
            show_spinner("Generating image...", 2)
            
            client = genai.Client(api_key=GEMINI_API_KEY)
            
            cache_path = get_generated_image_path(enhanced_prompt)
            if os.path.exists(cache_path):
                print_info("Using cached image")
                image_path = cache_path
            else:
                print_info("Requesting new image from Imagen 3...")
                
                # Validate aspect ratio format
                aspect_ratio = user_prefs.aspect_ratio
                valid_ratios = ["16:9", "21:9", "4:3", "1:1", "9:16"]
                if aspect_ratio not in valid_ratios:
                    print_warning(f"Invalid aspect ratio: {aspect_ratio}. Using default 16:9.")
                    aspect_ratio = "16:9"
                
                try:
                    response = client.models.generate_images(
                        model='imagen-3.0-generate-002',
                        prompt=enhanced_prompt,
                        config=types.GenerateImagesConfig(
                            number_of_images=1,
                            aspect_ratio=aspect_ratio,
                        )
                    )
                    
                    if response.generated_images is not None:
                        for i, generated_image in enumerate(response.generated_images):
                            image_path = f"generated_image_{i}.png"
                            with open(image_path, "wb") as f:
                                f.write(generated_image.image.image_bytes)
                        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
                        os.rename(image_path, cache_path)
                        print_success("Image generated successfully!")
                    else:
                        print_error("Failed to generate image - no images returned")
                        return False
                except AttributeError as e:
                    print_error(f"Error with Gemini client: {e}")
                    print_info("This might be due to an API version mismatch. Check your google-generativeai package version.")
                    return False
        except Exception as e:
            print_error(f"Error generating image: {e}")
            return False
    
    elif source_type == "provider":
        try:
            with requests.Session() as session:
                unsplash_access_key = os.environ.get("UNSPLASH_ACCESS_KEY")
                pexels_api_key = os.environ.get("PEXELS_API_KEY")

                providers = []
                if unsplash_access_key and len(unsplash_access_key.strip()) > 0:
                    providers.append("unsplash")
                if pexels_api_key and len(pexels_api_key.strip()) > 0:
                    providers.append("pexels")

                if not providers:
                    print_error("No valid API keys configured for image providers")
                    return False

                selected_provider = random.choice(providers)
                print_info(f"Fetching image from {selected_provider.capitalize()}...")
                show_spinner(f"Fetching image from {selected_provider.capitalize()}...", 2)

                if selected_provider == "unsplash":
                    url = "https://api.unsplash.com/photos/random"
                    params = {
                        "query": gemini_prompt.strip(),
                        "client_id": unsplash_access_key
                    }
                    try:
                        response = session.get(url, params=params, timeout=10)
                        if response.status_code >= 400:
                            if response.status_code in (400, 401, 403):
                                print_error("Unsplash API authentication failed")
                            else:
                                print_error(f"Unsplash API request failed with HTTP {response.status_code}")
                            return False
                    except requests.exceptions.RequestException as e:
                        print_error(f"Request error: {e}")
                        return False

                    try:
                        data = response.json()
                    except json.JSONDecodeError as e:
                        print_error(f"JSONDecodeError: {e}")
                        return False
                    
                    if isinstance(data, dict) and data.get('urls') and data['urls'].get('full'):
                        image_url = data['urls']['full']
                    else:
                        print_error(f"No images found for '{gemini_prompt}' using {selected_provider}")
                        return False

                elif selected_provider == "pexels":
                    url = "https://api.pexels.com/v1/search"
                    params = {
                        "query": gemini_prompt.strip(),
                        "per_page": 1
                    }
                    headers = {"Authorization": pexels_api_key}
                    try:
                        response = session.get(url, params=params, headers=headers, timeout=10)
                        if response.status_code >= 400:
                            if response.status_code in (400, 401, 403):
                                print_error("Pexels API authentication failed")
                            else:
                                print_error(f"Pexels API request failed with HTTP {response.status_code}")
                            return False
                    except requests.exceptions.RequestException as e:
                        print_error(f"Request error: {e}")
                        return False

                    data = response.json()
                    if 'photos' in data and data['photos']:
                        image_url = data['photos'][0]['src']['original']
                    else:
                        print_error(f"No images found for '{gemini_prompt}' using {selected_provider}")
                        return False

                cache_path = get_provider_cache_path(gemini_prompt)
                if os.path.exists(cache_path):
                    print_info("Using cached image")
                    image_path = cache_path
                else:
                    print_info(f"Downloading image from {selected_provider}...")
                    response = requests.get(image_url, stream=True)
                    response.raise_for_status()
                    image_path = "provider_image.jpg"
                    with open(image_path, "wb") as file:
                        for chunk in response.iter_content(chunk_size=8192):
                            file.write(chunk)
                    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
                    os.replace(image_path, cache_path)
                    print_success("Image downloaded successfully!")
        except requests.exceptions.RequestException as e:
            print_error(f"Request error: {e}")
            return False
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as e:
            print_error(f"JSON error: {e}")
            return False
        except Exception as e:
            print_error(f"Unexpected error: {e}")
            return False
    
    # Step 4: Set the wallpaper
    try:
        print_section("Setting Wallpaper")
        print_info("Applying your new wallpaper...")
        show_spinner("Configuring desktop settings...", 1)
        
        result = set_wallpaper(cache_path)
        if result:
            print_success("Wallpaper successfully applied!")
            print_info("Your desktop should now display the new wallpaper.")
            return True
        else:
            print_warning("Wallpaper may not have been set correctly.")
            print_info("Please check your desktop settings manually.")
            return False
            
    except subprocess.CalledProcessError as e:
        print_error("Failed to set wallpaper due to a system command error")
        print_info(f"Command: {e.cmd}")
        if e.stdout:
            print_info(f"Command output: {e.stdout}")
        if e.stderr:
            print_error(f"Command error: {e.stderr}")
        print_info("Please ensure your system supports automatic wallpaper changes.")
        
    except OSError as e:
        print_error("Operating system error while setting wallpaper")
        print_info(f"Error details: {e}")
        print_info("Please check file permissions and system settings.")
        
    except ValueError as e:
        print_error("Invalid configuration while setting wallpaper")
        print_info(f"Error details: {e}")
        print_info("Please verify your system's wallpaper settings.")
        
    except Exception as e:
        print_error("Unexpected error while setting wallpaper")
        print_info(f"Error details: {e}")
        print_info("Please check your system's compatibility with automatic wallpaper changes.")
    
    return False

def main():
    """Main function to execute the script."""
    # Check dependencies
    check_dependencies()
    
    print_header("AI Wallpaper Generator")
    print_info("Welcome to the AI Wallpaper Generator! This tool helps you create stunning wallpapers using AI.")
    
    while True:
        print_section("Main Menu")
        print_option("1", "Generate AI Wallpaper - Create custom wallpapers using AI")
        print_option("2", "Fetch Wallpaper - Get wallpapers from Unsplash/Pexels")
        print_option("3", "Manage Preferences - Customize wallpaper settings")
        print_option("4", "Exit - Save and exit")
        
        choice = get_validated_input("Select an option (1-4)", ["1", "2", "3", "4"])
        
        if choice == "1":
            print_section("Generate AI Wallpaper")
            print_option("1", "Use Gemini AI to generate a prompt")
            print_option("2", "Use a random prompt")
            print_option("3", "Enter your own custom prompt")
            print_option("4", "Return to Main Menu")
            
            prompt_choice = get_validated_input("Select prompt type (1-4)", ["1", "2", "3", "4"])
            
            if prompt_choice == "1":
                # Get mood and style preferences for this generation
                print_section("Optional Parameters")
                print_info("You can specify a mood and style for your wallpaper (leave empty to use random)")
                
                mood_options = ["peaceful", "dramatic", "mysterious", "energetic", "melancholic",
                               "joyful", "romantic", "eerie", "nostalgic", "contemplative"]
                style_options = ["photorealistic", "cinematic", "vintage", "modern", "minimalist",
                                "surreal", "abstract", "impressionistic", "cyberpunk", "steampunk"]
                
                print_info(f"Mood options: {', '.join(mood_options)}")
                mood = input("Enter mood (optional): ").strip().lower()
                if mood and mood not in mood_options:
                    print_warning(f"'{mood}' is not in the suggested moods, but we'll try to use it anyway")
                
                print_info(f"Style options: {', '.join(style_options)}")
                style = input("Enter style (optional): ").strip().lower()
                if style and style not in style_options:
                    print_warning(f"'{style}' is not in the suggested styles, but we'll try to use it anyway")
                
                generate_wallpaper("generate", "gemini", mood=mood, style=style)
            elif prompt_choice == "2":
                generate_wallpaper("generate", "random")
            elif prompt_choice == "3":
                custom_prompt = get_validated_input("Enter your custom prompt", allow_empty=False)
                generate_wallpaper("generate", "custom", custom_prompt=custom_prompt)
            elif prompt_choice == "4":
                continue
        
        elif choice == "2":
            if not (os.environ.get("UNSPLASH_ACCESS_KEY") or os.environ.get("PEXELS_API_KEY")):
                print_error("No API keys configured for image providers. Please set UNSPLASH_ACCESS_KEY or PEXELS_API_KEY environment variables.")
                continue
            
            generate_wallpaper("provider")
        
        elif choice == "3":
            manage_preferences()
        
        elif choice == "4":
            print_header("Thank you for using AI Wallpaper Generator!")
            break

if __name__ == "__main__":
    main()
