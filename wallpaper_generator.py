import json
from typing import Optional
import json
from typing import Optional
#!/usr/bin/env python3
"""AI Wallpaper - A tool for setting AI-generated wallpapers

This script fetches and sets desktop wallpapers using various image APIs and prompts.
"""
import json
import os
import platform
import random
import subprocess
import shlex
import logging
from urllib.parse import quote
import hashlib
import google.generativeai as genai
import requests
import bleach
import ctypes
import html
from absl import logging

logging.set_verbosity(logging.INFO)

# Configure the Gemini API key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Create a cache for generated prompts
prompt_cache = {}

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

def generate_prompt_gemini(tags, use_cache=True):
    """Generate a prompt using the Gemini model."""
    tags_key = ", ".join(tags)

    if use_cache and tags_key in prompt_cache:
        logging.info(f"Using cached Gemini prompt for tags: {tags_key}")
        return prompt_cache[tags_key]

    last_genre = load_last_genre()
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
        "Foggy Scenes", "Rain Photography", "Snow Scenes", "Rainbow Scenes", "Misty Mountains"
    ]

    if last_genre and last_genre in available_genres:
        available_genres.remove(last_genre)

    if not available_genres:
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

    save_last_genre(chosen_genre)

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
- Elements: Golden hour lighting, volumetric fog, water reflections, dramatic weather
- Examples: Mountain ranges with morning mist, storm-approaching coastlines, sunlit forest canopies
- Technical: f/8-f/11 aperture, wide-angle lens perspective, HDR dynamic range

**Urban & Architecture**
- Focus: Architectural details and urban environment interplay
- Elements: Material textures, geometric patterns, ambient occlusion, light diffusion
- Examples: Glass-steel skyscrapers at blue hour, historic stone facades with directional lighting
- Technical: Tilt-shift perspective, golden ratio composition, deep depth of field

**Portrait & People**
- Focus: Natural human expressions and environmental context
- Elements: Soft skin rendering, fabric textures, hair detail, natural poses
- Examples: Environmental portraits, candid street photography, lifestyle moments
- Technical: 85mm lens perspective, f/1.8-f/2.8 aperture, Rembrandt lighting setup
**Still Life & Objects**
- Focus: Material properties and object relationships
- Elements: Surface reflections, subsurface scattering, micro-details
- Examples: Product photography setups, carefully arranged natural objects
- Technical: Focus stacking, controlled studio lighting, rule of thirds

**Water Environments**
- Focus: Liquid dynamics and environmental context
- Elements: Refraction, reflection, foam, wave patterns
- Examples: Ocean waves crashing against cliffs, underwater macro photography
- Technical: Polarizing filters, long exposure, shallow depth of field

**Abstract & 3D**
- Focus: Clean geometric forms with realistic materials
- Elements: Surface reflectivity, procedural textures, precise geometry
- Examples: Minimalist architectural details, macro photography of natural patterns
- Technical: Studio lighting setups, focus stacking, symmetrical composition

Essential Technical Specifications:
1. Resolution & Quality
   - Specify "high resolution" or "8K" for maximum detail
   - Include "photorealistic" or "photoreal" for natural rendering
   - Reference professional camera brands for style (e.g., "shot on Hasselblad")

2. Lighting Parameters
   - Define specific lighting conditions (golden hour, blue hour, studio setup)
   - Specify light quality (soft, harsh, directional, diffused)
   - Include practical light sources when relevant

3. Composition Elements
   - Define camera position (eye-level, bird's eye, worm's eye)
   - Specify focal length (wide-angle 16-35mm, standard 50mm, telephoto 70-200mm)
   - Include depth of field requirements (shallow f/1.8, deep f/11)

4. Environmental Context
   - Define time of day and weather conditions
   - Specify season when relevant
   - Include atmospheric effects (fog, haze, rain)

5. Color and Tone
   - Reference specific color palettes or color grading styles
   - Specify contrast levels and dynamic range
   - Include color temperature (warm, cool, neutral)

Critical Requirements:
- Maintain photographic realism at all times
- Focus on a single genre without mixing categories
- Include specific technical photography terms
- Reference real-world lighting conditions
- Specify exact camera perspectives and compositions

Avoid:
- AI art buzzwords or style references
- Multiple competing focal points
- Technically impossible scenarios
- Mixed lighting conditions
- Vague or subjective descriptors

Output Format:
Generate a single, detailed sentence that incorporates:
1. Main subject and action/state
2. Technical camera specifications
3. Lighting conditions
4. Environmental context
5. Color/tone treatment
6. Compositional elements

The final prompt should read like a professional photographer's shot description, emphasizing Imagen 3's strengths in photorealism, lighting, and material rendering while maintaining physical accuracy and natural composition.
**Abstract & 3D Specialized Guidelines**

Core Focus Areas:
1. Geometric Composition
   - Primary shapes: spheres, cubes, pyramids, toruses
   - Complex geometry: fractals, voronoi patterns, tessellations
   - Architectural abstractions: deconstructed forms, minimalist structures
   - Organic abstractions: fluid dynamics, smoke patterns, wave forms

2. Material Properties
   - Metals: brushed, polished, oxidized, chrome, gold, copper
   - Glass: clear, frosted, textured, prismatic
   - Composites: carbon fiber, marble, concrete, ceramics
   - Surfaces: matte, glossy, reflective, translucent, subsurface scattering

3. Lighting Scenarios
   - Studio setups: 3-point lighting, rim lighting, area lights
   - Environmental lighting: HDRI environments, global illumination
   - Dramatic effects: volumetric lighting, caustics, light painting
   - Color lighting: split complementary, RGB, gradient mapping

4. Camera Technical Specs
   - Macro photography: extreme close-ups of textures and patterns
   - Tilt-shift: selective focus on geometric elements
   - Focus stacking: ultra-sharp detail across entire scene
   - Long exposure: motion blur and light trails

Composition Frameworks:
1. Geometric Arrangements
   - Golden ratio spiral compositions
   - Rule of thirds with tension points
   - Symmetrical balance
   - Dynamic diagonal flow
   - Repetition and rhythm

2. Space and Scale
   - Micro to macro transitions
   - Forced perspective
   - Infinite recursion
   - Negative space utilization

3. Motion and Flow
   - Particle systems
   - Fluid dynamics
   - Kinetic sculptures
   - Time-based patterns

Material Combinations:
1. Hard Surface
   - Chrome + matte black
   - Polished metal + frosted glass
   - Concrete + brass
   - Carbon fiber + aluminum

2. Organic Abstract
   - Liquid metal
   - Crystalline structures
   - Smoke and particle effects
   - Natural pattern abstractions

Prompt Structure for Abstract/3D:
"[Primary Form] with [Material Properties] captured using [Camera Technique], featuring [Lighting Setup] and [Environmental Context], rendered in [Color Scheme] with [Composition Style] composition, emphasizing [Technical Detail] at [Scale/Perspective]"

Example Prompts:
1. Geometric: "A polished chrome sphere intersecting with frosted glass cubes, captured in ultra-sharp 8K detail using focus stacking, lit by three-point studio lighting with cyan and magenta rim lights, composed using golden ratio spiral, emphasizing reflections and refractions at macro scale"

2. Organic Abstract: "Flowing liquid metal forms creating abstract patterns, shot with a tilt-shift lens for selective focus, illuminated by gradient-mapped HDRI lighting in cool tones, featuring subtle caustics and subsurface scattering, composed with dynamic diagonal movement"

3. Architectural Abstract: "Minimalist concrete and steel geometric forms photographed with a wide-angle lens, utilizing natural daylight through volumetric fog, emphasizing sharp edges and material transitions, composed with strong symmetry and repeated elements"

Technical Requirements:
- Always specify exact material properties
- Include at least one specific lighting technique
- Define camera position and lens choice
- Mention post-processing treatment (if any)
- Specify scale and perspective
- Include composition framework

Avoid:
- Mixing too many materials (stick to 2-3 maximum)
- Unrealistic material behaviors
- Physically impossible lighting
- Over-complicated compositions
- Vague material descriptions
- Generic abstract terms

The final prompt should create a clear mental image of a physically accurate, visually striking abstract or 3D scene that maximizes Imagen 3's capabilities in material rendering, lighting simulation, and geometric precision."""

    prompt = f"{prompt_instructions} Tags: {', '.join(tags)}"
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)

        if response.parts:
            gemini_prompt = response.parts[0].text.strip()
            logging.info(f"Generated Gemini prompt: {gemini_prompt}")

            prompt_cache[tags_key] = gemini_prompt
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
            command = ["gsettings", "set", "org.cinnamon.desktop.background", "picture-uri", file_uri]
            subprocess.run(command, check=True, capture_output=True, text=True)
            logging.info("Wallpaper set successfully on Linux")
        else:
            logging.warning(f"Unsupported operating system: {os_name}")
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
    *   Set the scene with environmental details: e.g., "Foggy morning," "Urban cityscape," "Tropical beach."
    *   Include weather conditions: e.g., "Rainy day," "Snowy landscape," "Sunny afternoon."
    *   Example: "Foggy morning in an urban cityscape"

5.  **Artistic Style and Post-Processing:**
    *   Define the overall style: e.g., "Photorealistic," "Cinematic," "Vintage," "Modern."
    *   Mention post-processing effects: e.g., "Color graded," "Film grain," "High dynamic range (HDR)."
    *   Example: "Photorealistic, color graded"

6.  **Detail Enhancement:**
    *   Add specific details to the subject: e.g., "Intricate details," "Realistic textures," "Fine details."
    *   Include elements that enhance realism: e.g., "Subsurface scattering," "Volumetric lighting."
    *   Example: "Intricate details with subsurface scattering"

7.  **Color Palette:**
    *   Specify the color scheme: e.g., "Warm colors," "Cool colors," "Monochromatic."
    *   Example: "Warm colors with a monochromatic tone"

**Advanced Prompt Engineering Techniques:**

*   **Chain-of-Thought (CoT) Prompting:** Guide the model by providing intermediate reasoning steps. For example, instead of directly asking for a "3D photorealistic rendering of a car," break it down into steps: "First, imagine a detailed 3D model of a car. Then, add realistic textures and lighting. Finally, render the image in a photorealistic style."
*   **Photography Descriptors:** Use specific photography terms to control the image style. Examples include "Long exposure," "Shallow depth of field," "Macro photography," "Tilt-shift lens," and "HDR."
*   **Shapes and Materials:** Specify the shapes and materials of the objects in the scene. For example, "Geometric shapes," "Organic forms," "Metallic surfaces," "Glass reflections," and "Subsurface scattering."
*   **Historical Art Movements:** Reference historical art movements to influence the image style. Examples include "Impressionism," "Surrealism," "Pop Art," and "Art Deco."
*   **Image Quality Modifiers:** Use terms to control the image quality, such as "8K," "High resolution," "Photorealistic," "Defect-free," and "Superb quality."
*   **Negative Prompts:** Use negative prompts to exclude unwanted elements or improve image quality (e.g., "No artifacts," "No blur," "No distortions," "No AI art buzzwords").

**Specific Styles Guidelines:**

*   **3D Illustration:** Use terms like "3D illustration," "High detail," "Intricate design," "Digital art," "Vibrant colors," "Geometric composition," and "Studio lighting."
*   **3D Cartoon:** Incorporate "3D cartoon," "Animated," "Character design," "Stylized," "Smooth shading," "Soft lighting," "Exaggerated features," and "Whimsical style."
*   **3D Photorealistic Rendering (Pixar Style):** Include "3D photorealistic rendering," "Pixar style," "Realistic textures," "Subsurface scattering," "Global illumination," "High-resolution," "Defect-free," reference specific Pixar films or characters for inspiration (e.g., "In the style of Toy Story"), and use techniques like "Ray tracing" and "Ambient occlusion."

**Example Prompts:**

*   Original: "A lone tree on a hill."
*   Enhanced: "Shot on Hasselblad, a lone tree on a hill during golden hour, with soft, diffused light, captured with a 35mm lens at f/8, using the rule of thirds for composition, photorealistic style, color graded with warm colors."

*   Original: "A futuristic cityscape."
*   Enhanced: "ARRI Alexa captures a futuristic cityscape at blue hour, with neon lights and volumetric lighting, using a wide-angle 16mm lens, high dynamic range (HDR), cinematic style, and leading lines for composition."

Your enhanced prompt should be a single, descriptive sentence that combines the original prompt with the technical details mentioned above. Focus on creating a vivid and realistic image in the mind of the viewer.
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

def main():
    """Main function to execute the script."""
    source = input("Use provider or generate image? (provider/generate - generate is default): ").lower() or "generate"

    if source == "generate":
        use_custom = input("Use custom prompt, Gemini prompt, or random prompt? (custom/gemini/random - gemini is default): ").lower() or "gemini"

        if use_custom == "custom":
            custom_prompt = input("Enter your custom prompt: ")
            sanitized_prompt = sanitize_prompt(custom_prompt)
            gemini_prompt = enhance_custom_prompt(sanitized_prompt)
            enhanced_prompt = gemini_prompt
        elif use_custom == "random":
            all_tags = nature_tags + space_tags + sea_tags + flowers_tags
            gemini_prompt = generate_prompt_random(all_tags)
            enhanced_prompt = enhance_custom_prompt(gemini_prompt)
        else:
            all_tags = nature_tags + space_tags + sea_tags + flowers_tags
            gemini_prompt = generate_prompt_gemini(all_tags)
            if not gemini_prompt:
                print("Failed to generate prompt with Gemini, using random tags instead.")
                gemini_prompt = generate_prompt_random(all_tags)
            enhanced_prompt = gemini_prompt

        for attempt in range(3):
            save_prompts_to_json(gemini_prompt, enhanced_prompt)
            confirmation = input(f"Proceed with this prompt? (yes/no) (Attempt {attempt + 1}/3): ").lower()
            if confirmation == "yes":
                break
            else:
                if use_custom == "custom":
                    custom_prompt = input("Enter your custom prompt: ")
                    sanitized_prompt = sanitize_prompt(custom_prompt)
                    enhanced_prompt = enhance_custom_prompt(sanitized_prompt)
                    gemini_prompt = sanitized_prompt
                elif use_custom == "random":
                    all_tags = nature_tags + space_tags + sea_tags + flowers_tags
                    gemini_prompt = generate_prompt_random(all_tags)
                    enhanced_prompt = enhance_custom_prompt(gemini_prompt)
                else:
                    all_tags = nature_tags + space_tags + sea_tags + flowers_tags
                    gemini_prompt = generate_prompt_gemini(all_tags, use_cache=False)
                    if not gemini_prompt:
                        print("Failed to generate prompt with Gemini, using random tags instead.")
                        gemini_prompt = generate_prompt_random(all_tags)
                    enhanced_prompt = gemini_prompt
        else:
            print("Limit reached. Stopping the script.")
            return

        if os.environ.get("GEMINI_API_KEY"):
            from google import genai
            from google.genai import types
            from PIL import Image
            from io import BytesIO

            client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

            cache_path = get_generated_image_path(enhanced_prompt)
            if os.path.exists(cache_path):
                image_path = cache_path
            else:
                response = client.models.generate_images(
                    model='imagen-3.0-generate-002',
                    prompt=enhanced_prompt,
                    config=types.GenerateImagesConfig(
                        number_of_images=1,
                        aspect_ratio='16:9',
                    )
                )

                if response.generated_images is not None:
                    for i, generated_image in enumerate(response.generated_images):
                        image_path = f"generated_image_{i}.png"
                        with open(image_path, "wb") as f:
                            f.write(generated_image.image.image_bytes)
                    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
                    os.rename(image_path, cache_path)
                else:
                    logging.error("response.generated_images is None, cannot set wallpaper")
                    return

            try:
                set_wallpaper(cache_path)
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
        else:
            logging.error("No valid API keys configured - please check your environment variables")

    elif source == "provider":
        all_tags = nature_tags + space_tags + sea_tags + flowers_tags
        prompt = generate_prompt_random(all_tags)

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
                    logging.error("No valid API keys configured - please check your environment variables")
                    return

                selected_provider = random.choice(providers)
                images = []

                if selected_provider == "unsplash":
                    url = "https://api.unsplash.com/photos/random"
                    params = {
                        "query": prompt.strip(),
                        "client_id": unsplash_access_key
                    }
                    try:
                        response = session.get(url, params=params, timeout=10)
                        if response.status_code >= 400:
                            if response.status_code in (400, 401, 403):
                                logging.warning("Unsplash API authentication failed - skipping")
                            else:
                                logging.warning(f"Unsplash API request failed with HTTP {response.status_code}")
                            return
                    except requests.exceptions.RequestException as e:
                        logging.error(f"Request error: {e}")
                        return

                    try:
                        data = response.json()
                    except json.JSONDecodeError as e:
                        logging.error(f"JSONDecodeError: {e}")
                        return
                    if isinstance(data, dict) and data.get('urls') and data['urls'].get('full'):
                        image_url = data['urls']['full']
                    else:
                        logging.warning(f"No images found for '{prompt}' using {selected_provider}")
                        return

                elif selected_provider == "pexels":
                    url = "https://api.pexels.com/v1/search"
                    params = {
                        "query": prompt.strip(),
                        "per_page": 1
                    }
                    headers = {"Authorization": pexels_api_key}
                    try:
                        response = session.get(url, params=params, headers=headers, timeout=10)
                        if response.status_code >= 400:
                            if response.status_code in (400, 401, 403):
                                logging.warning("Pexels API authentication failed - skipping")
                            else:
                                logging.warning(f"Pexels API request failed with HTTP {response.status_code}")
                            return
                    except requests.exceptions.RequestException as e:
                        logging.error(f"Request error: {e}")
                        return

                    data = response.json()
                    if 'photos' in data and data['photos']:
                        image_url = data['photos'][0]['src']['original']
                    else:
                        logging.warning(f"No images found for '{prompt}' using {selected_provider}")
                        return

                cache_path = get_provider_cache_path(prompt)
                if os.path.exists(cache_path):
                    image_path = cache_path
                else:
                    response = requests.get(image_url, stream=True)
                    response.raise_for_status()
                    image_path = "provider_image.jpg"
                    with open(image_path, "wb") as file:
                        for chunk in response.iter_content(chunk_size=8192):
                            file.write(chunk)
                    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
                    os.replace(image_path, cache_path)

                try:
                    set_wallpaper(cache_path)
                except subprocess.CalledProcessError as e:
                    logging.error(f"Error setting wallpaper (subprocess): {e}")
                    logging.error(f"Stdout: {e.stdout}")
                    logging.error(f"Stderr: {e.stderr}")
                except Exception as e:
                    logging.error(f"Error setting wallpaper: {e}")

        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {e}")
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as e:
            logging.error(f"JSON error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

    elif source == "generate":
        if os.environ.get("GEMINI_API_KEY"):
            from google import genai
            from google.genai import types
            from PIL import Image
            from io import BytesIO

            client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

            cache_path = get_generated_image_path(prompt)
            if os.path.exists(cache_path):
                image_path = cache_path
            else:
                response = client.models.generate_images(
                    model='imagen-3.0-generate-002',
                    prompt=prompt,
                    config=types.GenerateImagesConfig(
                        number_of_images=1,
                        aspect_ratio='16:9',
                    )
                )

                for i, generated_image in enumerate(response.generated_images):
                    image_path = f"generated_image_{i}.png"
                    with open(image_path, "wb") as f:
                        f.write(generated_image.image.image_bytes)
                os.makedirs(os.path.dirname(cache_path), exist_ok=True)
                os.rename(image_path, cache_path)

            try:
                set_wallpaper(cache_path)
            except subprocess.CalledProcessError as e:
                logging.error(f"Error setting wallpaper (subprocess): {e}")
                logging.error(f"Stdout: {e.stdout}")
                logging.error(f"Stderr: {e.stderr}")
            except Exception as e:
                logging.error(f"Error setting wallpaper: {e}")
        else:
            logging.error("No valid API keys configured - please check your environment variables")
    else:
        print("Invalid source. Please choose 'provider' or 'generate'.")

if __name__ == "__main__":
    main()
