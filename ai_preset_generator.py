#!/usr/bin/env python3
"""AI Preset Generator - Generate random wallpaper preferences using Gemini AI

This script uses Google's Gemini AI to create intelligent, coherent random presets 
for the wallpaper generator application.
"""

import os
import json
import logging
import random
import hashlib
from typing import Dict, Any, List, Optional

# Import Gemini API
try:
    import google.generativeai as genai
except ImportError:
    print("Error: google-generativeai package not installed")
    print("Please install it with: pip install google-generativeai")
    exit(1)

# Import from wallpaper_settings for user preferences
from wallpaper_settings import UserPreferences, get_preferences, initialize_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ai_preset_generator.log")
    ]
)

# Default style categories for style mixing
DEFAULT_STYLE_CATEGORIES = {
    "photographic": ["cinematic", "documentary", "film_grain", "polaroid", 
                  "analog_film", "lomography", "long_exposure"],
    "artistic": ["abstract", "impressionism", "expressionism", "cubism", 
                 "minimalism", "watercolor", "oil_painting", "acrylic", 
                 "stained_glass", "steampunk", "surrealism", "vaporwave"],
    "illustration": ["anime", "cartoon", "comic_book", "divisionism", "graffiti", 
                   "ink_drawing", "line_art", "manga", "paper_cut", "pixel_art", 
                   "pointillism", "pop_art", "ukiyo_e"]
}

# Cache file for storing previously generated presets
PRESETS_CACHE_FILE = "generated_presets_cache.json"

def get_gemini_api_key() -> Optional[str]:
    """
    Retrieve the Gemini API key from environment variable or config file.
    
    Returns:
        str: The API key if found, None otherwise
    """
    # First try environment variable
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        return api_key
    
    # Then try config file
    try:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                config = json.load(f)
                return config.get("gemini_api_key")
    except Exception as e:
        logging.error(f"Error reading config file: {e}")
    
    return None

def generate_random_style_mix() -> str:
    """Generate a random style mix from compatible styles.
    
    Returns:
        str: A string containing 2-3 compatible styles joined with " + "
    """
    # Select a random category
    category = random.choice(list(DEFAULT_STYLE_CATEGORIES.keys()))
    
    # Select 2-3 compatible styles from the same category
    num_styles = random.randint(2, 3)
    available_styles = DEFAULT_STYLE_CATEGORIES[category]
    if len(available_styles) < num_styles:
        num_styles = len(available_styles)
    
    selected_styles = random.sample(available_styles, num_styles)
    return " + ".join(selected_styles)

def load_cached_presets() -> List[str]:
    """Load previously generated preset hashes from cache file."""
    if os.path.exists(PRESETS_CACHE_FILE):
        try:
            with open(PRESETS_CACHE_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading presets cache: {e}")
    return []

def save_preset_to_cache(preset_data: Dict[str, Any]) -> None:
    """Save a preset hash to the cache file to avoid regenerating it."""
    preset_hash = hashlib.md5(json.dumps(preset_data, sort_keys=True).encode()).hexdigest()
    
    cached_presets = load_cached_presets()
    cached_presets.append(preset_hash)
    
    # Keep only the last 50 presets to avoid infinite growth
    if len(cached_presets) > 50:
        cached_presets = cached_presets[-50:]
    
    try:
        with open(PRESETS_CACHE_FILE, 'w') as f:
            json.dump(cached_presets, f)
    except Exception as e:
        logging.error(f"Error saving to presets cache: {e}")

def is_preset_unique(preset_data: Dict[str, Any]) -> bool:
    """Check if a preset is unique compared to previously generated ones."""
    preset_hash = hashlib.md5(json.dumps(preset_data, sort_keys=True).encode()).hexdigest()
    cached_presets = load_cached_presets()
    return preset_hash not in cached_presets

def generate_ai_preset(user_prefs: UserPreferences) -> bool:
    """
    Generate a random preset with coherent settings using Gemini AI.
    
    This function uses Gemini to create a set of preferences that are coherent
    and stylistically matched, rather than just randomly selecting values.
    
    Args:
        user_prefs: The UserPreferences object to update with AI-generated settings
        
    Returns:
        bool: True if successful, False otherwise
    """
    api_key = get_gemini_api_key()
    if not api_key:
        logging.error("No Gemini API key found. Please set GEMINI_API_KEY environment variable or add it to config.json")
        return False
        
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-pro-preview-03-25')
        
        # Decide whether to use mixed styles (50% chance)
        use_mixed_styles = random.choice([True, False])
        
        # If using mixed styles, generate them now
        mixed_style = None
        if use_mixed_styles:
            mixed_style = generate_random_style_mix()
            logging.info(f"Using mixed style: {mixed_style}")
        
        # Create the request for a coherent set of preferences
        prompt = """
        Generate a random but coherent set of wallpaper generation preferences. Create settings that would work well together artistically.
        The output should be valid JSON format with the following structure:
        {
            "preset_name": "[a creative name for this preset]",
            "genres": [list of 1 genres that work well together],
            "styles": [list of 1 artistic style],
            "moods": [list of 1 moods that fit with the genres and styles],
            "imagen_settings": {
                "style_settings": {
                    "art_movement": "[a fitting art movement]",
                    "post_processing": [list of 0-1 post-processing effects]
                },
                "camera_settings": {
                    "camera_model": "[appropriate camera model]",
                    "lens_type": "[appropriate lens type]",
                    "aperture": "[appropriate aperture setting]",
                    "depth_of_field": "[appropriate depth setting]"
                },
                "lighting_settings": {
                    "lighting_type": "[appropriate lighting type]",
                    "time_of_day": "[appropriate time of day]",
                    "light_quality": "[appropriate light quality]"
                },
                "composition_settings": {
                    "technique": "[appropriate composition technique]",
                    "camera_angle": "[appropriate camera angle]"
                },
                "color_settings": {
                    "color_scheme": "[appropriate color scheme]",
                    "palette_type": "[appropriate palette type]",
                    "color_temperature": "[appropriate color temperature]"
                }
            },
            "aspect_ratio": "[choose ONLY from these specific values: 16:9, 4:3, 1:1, or 9:16]"
        }
        
        Choose 1 from these genre options:
        ["Nature & Landscapes", "Mountains & Peaks", "Forests & Woods", "Desert & Dunes", "Waterfalls & Rivers", "Urban & Architecture", "Modern Cityscapes", "Space & Cosmos", "Sea & Ocean", "Fantasy Landscapes", "Abstract & 3D"]
        """
        
        # If using a mixed style, tell Gemini to use it
        if mixed_style:
            prompt += f"""
        
        For the "styles" field, use exactly this value:
        ["{mixed_style}"]
        """
        else:
            prompt += """
        
        Choose 1 from these style options:
        ["traditional_art", "digital_art", "abstract", "anime", "art_deco", "art_nouveau", "cartoon", "charcoal", "cinematic", "comic_book", "cyberpunk", "divisionism", "double_exposure", "expressionism", "fantasy", "futurism", "glitch_art", "gothic", "graffiti", "hyperrealism", "impressionism", "ink_drawing", "isometric", "landscape", "line_art", "low_poly", "manga", "minimalist", "oil_painting", "paper_cut", "pastel", "pencil_sketch", "pixel_art", "pointillism", "pop_art", "realism", "retrowave", "sci_fi", "sketch", "stained_glass", "steampunk", "surrealism", "ukiyo_e", "vaporwave", "watercolor", "woodcut"]
        """
        
        prompt += """
        
        Choose 1 from these mood options:
        ["peaceful", "serene", "tranquil", "calm", "relaxing", "soothing", "energetic", "vibrant", "dynamic", "exciting", "dramatic", "intense", "mysterious", "enigmatic", "cryptic", "eerie", "romantic", "passionate", "tender", "joyful", "cheerful", "happy", "playful", "whimsical", "dreamy", "contemplative", "thoughtful", "philosophical", "inspiring", "uplifting", "motivational"]
        
        Ensure all settings are coherent and artistically compatible.
        """
        
        # Try up to 3 times to generate a unique preset
        for attempt in range(3):
            # Get the response
            response = model.generate_content(contents=prompt)
            
            if response:
                # Extract the JSON from the response
                response_text = response.text.strip()
                
                # Find JSON content (in case there's any extra text)
                import re
                json_match = re.search(r'({[\s\S]*})', response_text)
                if json_match:
                    json_content = json_match.group(1)
                    preset_data = json.loads(json_content)
                    
                    # Check if this preset is unique compared to previous ones
                    if is_preset_unique(preset_data):
                        # Apply the generated preset to user preferences
                        preset_name = preset_data.get("preset_name", "AI Generated Preset")
                        print(f"Applying AI-generated preset: {preset_name}")
                        
                        # Save this preset to cache so we don't generate it again
                        save_preset_to_cache(preset_data)
                        
                        # Reset existing values first to prevent accumulation
                        user_prefs.preferred_genres = []
                        user_prefs.preferred_styles = []
                        user_prefs.preferred_moods = []
                        
                        # Reset imagen settings to minimal defaults (preserving essential structure)
                        user_prefs.imagen_settings = {
                            "number_of_images": 1,
                            "seed": None,
                            "negative_prompt": "",
                            "quality_settings": {},
                            "style_settings": {},
                            "camera_settings": {},
                            "lighting_settings": {},
                            "composition_settings": {},
                            "environment_settings": {},
                            "color_settings": {},
                            "detail_settings": {}
                        }
                        
                        # Reset wallpaper settings
                        user_prefs.wallpaper_settings = {"auto_set": False}
                        
                        # Update user preferences
                        user_prefs.preferred_genres = preset_data.get("genres", [])[:1]  # Take only first item
                        
                        # For styles, ensure it's a single string (even if it's a mixed style)
                        styles = preset_data.get("styles", [])
                        user_prefs.preferred_styles = styles[:1] if styles else []
                        
                        user_prefs.preferred_moods = preset_data.get("moods", [])[:1]  # Take only first item
                        
                        # Validate aspect ratio - only use supported values
                        aspect_ratio = preset_data.get("aspect_ratio", "16:9")
                        valid_ratios = ["16:9", "4:3", "1:1", "9:16"]
                        if aspect_ratio not in valid_ratios:
                            print(f"Warning: Generated aspect ratio '{aspect_ratio}' is not supported. Using default 16:9 instead.")
                            aspect_ratio = "16:9"
                        user_prefs.aspect_ratio = aspect_ratio
                        
                        # Update imagen settings
                        imagen_settings = preset_data.get("imagen_settings", {})
                        
                        # Quality Settings - with more complete information
                        quality_settings = imagen_settings.get("quality_settings", {})
                        user_prefs.imagen_settings["quality_settings"] = {
                            "resolution": quality_settings.get("resolution", "1920x1080"),
                            "detail_level": quality_settings.get("detail_level", "high"),
                            "rendering_quality": quality_settings.get("rendering_quality", "high")
                        }
                        
                        # Style settings
                        style_settings = imagen_settings.get("style_settings", {})
                        
                        # Only add style_categories if they don't already exist in user preferences
                        # or if we're using a mixed style that needs them
                        if mixed_style or "style_categories" not in user_prefs.imagen_settings.get("style_settings", {}):
                            user_prefs.imagen_settings["style_settings"] = {
                                "art_movement": style_settings.get("art_movement"),
                                "post_processing": style_settings.get("post_processing", []),
                                # Include style categories for mixed style functionality
                                "style_categories": DEFAULT_STYLE_CATEGORIES
                            }
                        else:
                            # Don't include style_categories if they already exist
                            user_prefs.imagen_settings["style_settings"] = {
                                "art_movement": style_settings.get("art_movement"),
                                "post_processing": style_settings.get("post_processing", [])
                            }
                        
                        # Camera settings - with more complete information
                        camera_settings = imagen_settings.get("camera_settings", {})
                        user_prefs.imagen_settings["camera_settings"] = {
                            "camera_model": camera_settings.get("camera_model"),
                            "lens_type": camera_settings.get("lens_type"),
                            "aperture": camera_settings.get("aperture"),
                            "depth_of_field": camera_settings.get("depth_of_field"),
                            "special_lens": camera_settings.get("special_lens", None),
                            "camera_brand": camera_settings.get("camera_brand", None),
                            "focal_length": camera_settings.get("focal_length", None),
                            "sensor_type": camera_settings.get("sensor_type", None)
                        }
                        
                        # Lighting settings - with more complete information
                        lighting_settings = imagen_settings.get("lighting_settings", {})
                        user_prefs.imagen_settings["lighting_settings"] = {
                            "lighting_type": lighting_settings.get("lighting_type"),
                            "time_of_day": lighting_settings.get("time_of_day"),
                            "light_quality": lighting_settings.get("light_quality"),
                            "light_source": lighting_settings.get("light_source", None),
                            "artificial_sources": lighting_settings.get("artificial_sources", [])
                        }
                        
                        # Composition settings - with more complete information
                        composition_settings = imagen_settings.get("composition_settings", {})
                        user_prefs.imagen_settings["composition_settings"] = {
                            "technique": composition_settings.get("technique"),
                            "camera_angle": composition_settings.get("camera_angle"),
                            "visual_flow": composition_settings.get("visual_flow", None),
                            "depth_layering": composition_settings.get("depth_layering", None)
                        }
                        
                        # Environment settings - more complete
                        environment_settings = imagen_settings.get("environment_settings", {})
                        user_prefs.imagen_settings["environment_settings"] = {
                            "weather": environment_settings.get("weather", None),
                            "season": environment_settings.get("season", None),
                            "atmospheric_effects": environment_settings.get("atmospheric_effects", []),
                            "location_type": environment_settings.get("location_type", None)
                        }
                        
                        # Color settings - more complete
                        color_settings = imagen_settings.get("color_settings", {})
                        user_prefs.imagen_settings["color_settings"] = {
                            "color_scheme": color_settings.get("color_scheme"),
                            "palette_type": color_settings.get("palette_type"),
                            "color_temperature": color_settings.get("color_temperature")
                        }
                        
                        # Detail settings - more complete
                        detail_settings = imagen_settings.get("detail_settings", {})
                        user_prefs.imagen_settings["detail_settings"] = {
                            "texture_quality": detail_settings.get("texture_quality", None),
                            "special_effects": detail_settings.get("special_effects", [])
                        }
                        
                        # Add a default negative prompt if none exists
                        if "negative_prompt" not in user_prefs.imagen_settings or not user_prefs.imagen_settings["negative_prompt"]:
                            user_prefs.imagen_settings["negative_prompt"] = "ugly, disfigured, low quality, blurry, nsfw, watermark, signature, out of frame, extra limbs, poorly drawn face, twisted limbs, distorted face, bad proportions, bad anatomy"
                        
                        # Save the preferences
                        user_prefs.save_preferences()
                        
                        return True
                    else:
                        logging.info(f"Generated preset was not unique, trying again (attempt {attempt+1}/3)")
                        # Continue to the next attempt
                else:
                    logging.error("Could not extract JSON from Gemini response")
                    return False
            else:
                logging.error("Empty response from Gemini")
                return False
                
        # If we get here, we failed to generate a unique preset after 3 attempts
        logging.warning("Could not generate a unique preset after 3 attempts")
        print("Generating a preset with random style mix as fallback...")
        
        # Fallback to a simple preset with random style mix
        fallback_preset = {
            "preset_name": f"Random Mix Preset {random.randint(1, 1000)}",
            "genres": [random.choice(["Nature & Landscapes", "Space & Cosmos", "Urban & Architecture", "Fantasy Landscapes"])],
            "styles": [generate_random_style_mix()],  # This always generates a mixed style
            "moods": [random.choice(["peaceful", "mysterious", "dramatic", "energetic", "dreamy"])],
            "aspect_ratio": random.choice(["16:9", "4:3", "1:1", "9:16"]),
            "imagen_settings": {
                "quality_settings": {
                    "resolution": "1920x1080",
                    "detail_level": "high",
                    "rendering_quality": "high"
                },
                "style_settings": {
                    "art_movement": random.choice(["Impressionism", "Surrealism", "Abstract Expressionism", "Pop Art", "Minimalism"]),
                    "post_processing": random.sample(["film grain", "color grading", "vintage", "HDR"], k=random.randint(0, 2))
                },
                "camera_settings": {
                    "camera_model": random.choice(["Canon EOS R5", "Sony A7R IV", "Hasselblad X1D", "Fujifilm GFX", None]),
                    "lens_type": random.choice(["wide angle", "standard", "telephoto", "macro", None]),
                    "aperture": random.choice(["f/1.8", "f/2.8", "f/4", "f/8", None]),
                    "depth_of_field": random.choice(["shallow", "medium", "deep", None])
                },
                "lighting_settings": {
                    "lighting_type": random.choice(["natural", "studio", "dramatic", "ambient", None]),
                    "time_of_day": random.choice(["golden hour", "blue hour", "midday", "sunset", "twilight", None]),
                    "light_quality": random.choice(["soft", "hard", "diffused", "directional", None])
                },
                "composition_settings": {
                    "technique": random.choice(["rule of thirds", "golden ratio", "symmetry", "leading lines", None]),
                    "camera_angle": random.choice(["eye level", "low angle", "high angle", "bird's eye", None])
                },
                "color_settings": {
                    "color_scheme": random.choice(["analogous", "complementary", "monochromatic", "triadic", None]),
                    "palette_type": random.choice(["vibrant", "muted", "pastel", "dark", None]),
                    "color_temperature": random.choice(["warm", "cool", "neutral", None])
                }
            }
        }
        
        # Reset existing values first to prevent accumulation
        user_prefs.preferred_genres = []
        user_prefs.preferred_styles = []
        user_prefs.preferred_moods = []
        
        # Reset imagen settings to minimal defaults (preserving essential structure)
        user_prefs.imagen_settings = {
            "number_of_images": 1,
            "seed": None,
            "negative_prompt": "ugly, disfigured, low quality, blurry, nsfw, watermark, signature, out of frame, extra limbs, poorly drawn face, twisted limbs, distorted face, bad proportions, bad anatomy",
            "quality_settings": {},
            "style_settings": {},
            "camera_settings": {},
            "lighting_settings": {},
            "composition_settings": {},
            "environment_settings": {},
            "color_settings": {},
            "detail_settings": {}
        }
        
        # Since fallback always uses a mixed style, we need to add style_categories
        user_prefs.imagen_settings["style_settings"] = {
            "style_categories": DEFAULT_STYLE_CATEGORIES
        }
        
        # Reset wallpaper settings
        user_prefs.wallpaper_settings = {"auto_set": False}
        
        # Update user preferences with fallback
        user_prefs.preferred_genres = fallback_preset["genres"][:1]  # Take only first item
        user_prefs.preferred_styles = fallback_preset["styles"][:1]  # Take only first item
        user_prefs.preferred_moods = fallback_preset["moods"][:1]    # Take only first item
        user_prefs.aspect_ratio = fallback_preset["aspect_ratio"]
        
        # Update all imagen settings from the fallback preset
        imagen_settings = fallback_preset.get("imagen_settings", {})
        
        # Quality Settings
        quality_settings = imagen_settings.get("quality_settings", {})
        user_prefs.imagen_settings["quality_settings"] = {
            "resolution": quality_settings.get("resolution", "1920x1080"),
            "detail_level": quality_settings.get("detail_level", "high"),
            "rendering_quality": quality_settings.get("rendering_quality", "high")
        }
        
        # Style settings - already set with style_categories above, now add more
        style_settings = imagen_settings.get("style_settings", {})
        user_prefs.imagen_settings["style_settings"]["art_movement"] = style_settings.get("art_movement")
        user_prefs.imagen_settings["style_settings"]["post_processing"] = style_settings.get("post_processing", [])
        
        # Camera settings
        camera_settings = imagen_settings.get("camera_settings", {})
        user_prefs.imagen_settings["camera_settings"] = {
            "camera_model": camera_settings.get("camera_model"),
            "lens_type": camera_settings.get("lens_type"),
            "aperture": camera_settings.get("aperture"),
            "depth_of_field": camera_settings.get("depth_of_field"),
            "special_lens": camera_settings.get("special_lens", None),
            "camera_brand": camera_settings.get("camera_brand", None),
            "focal_length": camera_settings.get("focal_length", None),
            "sensor_type": camera_settings.get("sensor_type", None)
        }
        
        # Lighting settings
        lighting_settings = imagen_settings.get("lighting_settings", {})
        user_prefs.imagen_settings["lighting_settings"] = {
            "lighting_type": lighting_settings.get("lighting_type"),
            "time_of_day": lighting_settings.get("time_of_day"),
            "light_quality": lighting_settings.get("light_quality"),
            "light_source": lighting_settings.get("light_source", None),
            "artificial_sources": lighting_settings.get("artificial_sources", [])
        }
        
        # Composition settings
        composition_settings = imagen_settings.get("composition_settings", {})
        user_prefs.imagen_settings["composition_settings"] = {
            "technique": composition_settings.get("technique"),
            "camera_angle": composition_settings.get("camera_angle"),
            "visual_flow": composition_settings.get("visual_flow", None),
            "depth_layering": composition_settings.get("depth_layering", None)
        }
        
        # Environment settings - basic default values
        user_prefs.imagen_settings["environment_settings"] = {
            "weather": None,
            "season": None,
            "atmospheric_effects": [],
            "location_type": None
        }
        
        # Color settings
        color_settings = imagen_settings.get("color_settings", {})
        user_prefs.imagen_settings["color_settings"] = {
            "color_scheme": color_settings.get("color_scheme"),
            "palette_type": color_settings.get("palette_type"),
            "color_temperature": color_settings.get("color_temperature")
        }
        
        # Detail settings - basic defaults
        user_prefs.imagen_settings["detail_settings"] = {
            "texture_quality": None,
            "special_effects": []
        }
        
        # Save the preferences
        user_prefs.save_preferences()
        
        return True
            
    except Exception as e:
        logging.error(f"Error generating AI preset: {e}")
        return False

if __name__ == "__main__":
    # For testing
    from wallpaper_settings import get_preferences, initialize_settings
    
    # Make sure preferences are initialized
    user_prefs = get_preferences()
    if user_prefs is None:
        user_prefs = initialize_settings()
        
    if generate_ai_preset(user_prefs):
        print("Successfully generated and applied AI preset")
    else:
        print("Failed to generate AI preset") 