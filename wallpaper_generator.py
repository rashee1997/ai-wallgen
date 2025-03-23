#!/usr/bin/env python3
"""AI Wallpaper Generator - Create stunning AI-generated desktop wallpapers

This script generates high-quality desktop wallpapers using Google's Imagen 3 model
via the Gemini API. It offers various customization options and prompt engineering 
techniques to create visually appealing wallpapers tailored to your preferences.
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
import bleach
import ctypes
import html
from absl import logging
from prompt_config import (
    nature_tags, space_tags, sea_tags, flowers_tags, urban_tags,
    fantasy_tags, abstract_tags, mood_tags, available_genres,
    PROMPT_INSTRUCTIONS, CUSTOM_PROMPT_INSTRUCTIONS
)
from datetime import datetime
import shutil
import threading
import re
import glob
import tkinter as tk

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

# User preferences
class UserPreferences:
    """Class to manage user preferences."""
    def __init__(self):
        """Initialize user preferences."""
        self.preferred_genres = []
        self.preferred_styles = []
        self.preferred_moods = []
        self.aspect_ratio = "16:9"
        self.negative_prompts = []
        self.imagen_settings = {
            "number_of_images": 1,
            "seed": None,
            "aspect_ratio": "16:9",
            "negative_prompt": "",
            "camera_settings": {
                "camera_model": "ARRI Alexa",
                "lens_type": "50mm",
                "aperture": "f/2.8",
                "special_lens": None,
                "depth_of_field": "medium"
            }
        }
        self.wallpaper_settings = {}
        self.current_preset = None
        self.load_preferences()
    
    def load_preferences(self, filename: str = "user_preferences.json") -> None:
        """Load preferences from file."""
        # Use absolute path for the preferences file
        if not os.path.isabs(filename):
            abs_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        else:
            abs_filename = filename
            
        if os.path.exists(abs_filename):
            try:
                with open(abs_filename) as f:
                    data = json.load(f)
                    # Load main settings
                    self.imagen_settings = data.get("imagen_settings", {})
                    self.wallpaper_settings = data.get("wallpaper_settings", {})
                    self.current_preset = data.get("current_preset", None)
                    
                    # Load preferred genres, styles, and moods
                    self.preferred_genres = data.get("preferred_genres", [])
                    self.preferred_styles = data.get("preferred_styles", [])
                    self.preferred_moods = data.get("preferred_moods", [])
                    self.aspect_ratio = data.get("aspect_ratio", "16:9")
                    self.negative_prompts = data.get("negative_prompts", [])
                    
                    logging.info(f"Loaded preferences from {abs_filename}")
                    logging.info(f"Preferred genres: {self.preferred_genres}")
                    logging.info(f"Preferred styles: {self.preferred_styles}")
                    logging.info(f"Preferred moods: {self.preferred_moods}")
            except Exception as e:
                print_error(f"Error loading preferences: {e}")
                logging.error(f"Error loading preferences from {abs_filename}: {e}")
                # Don't reset everything, just leave the defaults
        else:
            logging.info(f"No preferences file found at {abs_filename}, using defaults")
    
    def save_preferences(self, filename: str = "user_preferences.json") -> None:
        """Save preferences to file."""
        # Use absolute path for the preferences file
        if not os.path.isabs(filename):
            abs_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        else:
            abs_filename = filename
            
        try:
            data = {
                "imagen_settings": self.imagen_settings,
                "wallpaper_settings": self.wallpaper_settings,
                "current_preset": self.current_preset,
                "preferred_genres": self.preferred_genres,
                "preferred_styles": self.preferred_styles,
                "preferred_moods": self.preferred_moods,
                "aspect_ratio": self.aspect_ratio,
                "negative_prompts": self.negative_prompts
            }
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(abs_filename), exist_ok=True)
            
            with open(abs_filename, "w") as f:
                json.dump(data, f, indent=4)
                
            logging.info(f"Saved preferences to {abs_filename}")
            logging.info(f"Preferred genres: {self.preferred_genres}")
            logging.info(f"Preferred styles: {self.preferred_styles}")
            logging.info(f"Preferred moods: {self.preferred_moods}")
        except Exception as e:
            print_error(f"Error saving preferences: {e}")
            logging.error(f"Error saving preferences to {abs_filename}: {e}")

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
        style: Optional style to incorporate (e.g., "photograph", "digital_art")
    
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

    # Build the prompt with user preferences
    prompt_parts = [PROMPT_INSTRUCTIONS]
    
    # Add user's preferred genres if available
    if user_prefs.preferred_genres:
        prompt_parts.append(f"Preferred genres: {', '.join(user_prefs.preferred_genres)}")
    
    # Add user's preferred styles if available
    if user_prefs.preferred_styles:
        prompt_parts.append(f"Preferred styles: {', '.join(user_prefs.preferred_styles)}")
    
    # Add user's preferred moods if available
    if user_prefs.preferred_moods:
        prompt_parts.append(f"Preferred moods: {', '.join(user_prefs.preferred_moods)}")
    
    # Add provided tags
    prompt_parts.append(f"Tags: {', '.join(tags)}")
    
    # Add specific mood if provided
    if mood:
        prompt_parts.append(f"Specific mood: {mood}")
    
    # Add specific style if provided
    if style:
        prompt_parts.append(f"Specific style: {style}")
    
    # Add all imagen_settings preferences
    settings = user_prefs.imagen_settings
    
    # Camera Settings
    camera_settings = settings.get("camera_settings", {})
    if camera_settings:
        camera_parts = []
        if camera_settings.get("camera_model"):
            camera_parts.append(f"camera model: {camera_settings['camera_model']}")
        if camera_settings.get("lens_type"):
            camera_parts.append(f"lens: {camera_settings['lens_type']}")
        if camera_settings.get("aperture"):
            camera_parts.append(f"aperture: {camera_settings['aperture']}")
        if camera_settings.get("depth_of_field"):
            camera_parts.append(f"depth of field: {camera_settings['depth_of_field']}")
        if camera_parts:
            prompt_parts.append(f"Camera settings: {', '.join(camera_parts)}")
    
    # Lighting Settings
    lighting_settings = settings.get("lighting_settings", {})
    if lighting_settings:
        lighting_parts = []
        if lighting_settings.get("time_of_day"):
            lighting_parts.append(f"time of day: {lighting_settings['time_of_day']}")
        if lighting_settings.get("lighting_style"):
            lighting_parts.append(f"lighting style: {lighting_settings['lighting_style']}")
        if lighting_settings.get("light_quality"):
            lighting_parts.append(f"light quality: {lighting_settings['light_quality']}")
        if lighting_settings.get("artificial_sources"):
            lighting_parts.append(f"artificial sources: {', '.join(lighting_settings['artificial_sources'])}")
        if lighting_parts:
            prompt_parts.append(f"Lighting settings: {', '.join(lighting_parts)}")
    
    # Composition Settings
    composition_settings = settings.get("composition_settings", {})
    if composition_settings:
        composition_parts = []
        if composition_settings.get("technique"):
            composition_parts.append(f"technique: {composition_settings['technique']}")
        if composition_settings.get("camera_angle"):
            composition_parts.append(f"camera angle: {composition_settings['camera_angle']}")
        if composition_settings.get("perspective"):
            composition_parts.append(f"perspective: {composition_settings['perspective']}")
        if composition_parts:
            prompt_parts.append(f"Composition settings: {', '.join(composition_parts)}")
    
    # Environment Settings
    environment_settings = settings.get("environment_settings", {})
    if environment_settings:
        environment_parts = []
        if environment_settings.get("weather"):
            environment_parts.append(f"weather: {environment_settings['weather']}")
        if environment_settings.get("season"):
            environment_parts.append(f"season: {environment_settings['season']}")
        if environment_settings.get("atmospheric_effects"):
            environment_parts.append(f"atmospheric effects: {', '.join(environment_settings['atmospheric_effects'])}")
        if environment_parts:
            prompt_parts.append(f"Environment settings: {', '.join(environment_parts)}")
    
    # Style Settings
    style_settings = settings.get("style_settings", {})
    if style_settings:
        style_parts = []
        if style_settings.get("overall_style"):
            style_parts.append(f"overall style: {style_settings['overall_style']}")
        if style_settings.get("art_movement"):
            style_parts.append(f"art movement: {style_settings['art_movement']}")
        if style_settings.get("post_processing"):
            style_parts.append(f"post-processing: {', '.join(style_settings['post_processing'])}")
        if style_parts:
            prompt_parts.append(f"Style settings: {', '.join(style_parts)}")
    
    # Detail Settings
    detail_settings = settings.get("detail_settings", {})
    if detail_settings:
        detail_parts = []
        if detail_settings.get("detail_level"):
            detail_parts.append(f"detail level: {detail_settings['detail_level']}")
        if detail_settings.get("texture_quality"):
            detail_parts.append(f"texture quality: {detail_settings['texture_quality']}")
        if detail_settings.get("special_effects"):
            detail_parts.append(f"special effects: {', '.join(detail_settings['special_effects'])}")
        if detail_parts:
            prompt_parts.append(f"Detail settings: {', '.join(detail_parts)}")
    
    # Color Settings
    color_settings = settings.get("color_settings", {})
    if color_settings:
        color_parts = []
        if color_settings.get("color_scheme"):
            color_parts.append(f"color scheme: {color_settings['color_scheme']}")
        if color_settings.get("palette_type"):
            color_parts.append(f"palette type: {color_settings['palette_type']}")
        if color_settings.get("color_temperature"):
            color_parts.append(f"color temperature: {color_settings['color_temperature']}")
        if color_parts:
            prompt_parts.append(f"Color settings: {', '.join(color_parts)}")
    
    # Quality Settings
    quality_settings = settings.get("quality_settings", {})
    if quality_settings:
        quality_parts = []
        if quality_settings.get("resolution"):
            quality_parts.append(f"resolution: {quality_settings['resolution']}")
        if quality_settings.get("rendering_quality"):
            quality_parts.append(f"rendering quality: {quality_settings['rendering_quality']}")
        if quality_parts:
            prompt_parts.append(f"Quality settings: {', '.join(quality_parts)}")
    
    # Add aspect ratio preference
    prompt_parts.append(f"Aspect ratio: {user_prefs.aspect_ratio}")
    
    # Add negative prompts if available
    if user_prefs.negative_prompts:
        prompt_parts.append(f"Negative prompts (elements to avoid): {', '.join(user_prefs.negative_prompts)}")
    
    # Combine all parts into the final prompt
    final_prompt = "\n".join(prompt_parts)
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(final_prompt)

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
    """Generate a random prompt using selected tags and user preferences."""
    try:
        # Get user preferences
        style = user_prefs.preferred_styles[0] if user_prefs.preferred_styles else "photorealistic"
        mood = user_prefs.preferred_moods[0] if user_prefs.preferred_moods else "neutral"
        
        # Get all settings from imagen_settings with default values
        settings = user_prefs.imagen_settings
        
        # Camera & Technical Settings
        camera_settings = settings.get("camera_settings", {})
        camera_model = camera_settings.get("camera_model", "ARRI Alexa")
        lens_type = camera_settings.get("lens_type", "50mm")
        aperture = camera_settings.get("aperture", "f/2.8")
        special_lens = camera_settings.get("special_lens", "standard")
        depth_of_field = camera_settings.get("depth_of_field", "medium")
        
        # Lighting & Atmosphere
        lighting_settings = settings.get("lighting_settings", {})
        time_of_day = lighting_settings.get("time_of_day", "golden_hour")
        lighting_style = lighting_settings.get("lighting_style", "natural")
        light_quality = lighting_settings.get("light_quality", "soft")
        artificial_sources = lighting_settings.get("artificial_sources", [])
        
        # Composition & Environment
        composition_settings = settings.get("composition_settings", {})
        technique = composition_settings.get("technique", "rule_of_thirds")
        camera_angle = composition_settings.get("camera_angle", "eye_level")
        perspective = composition_settings.get("perspective", "wide")
        
        environment_settings = settings.get("environment_settings", {})
        weather = environment_settings.get("weather", "clear")
        season = environment_settings.get("season", "summer")
        atmospheric_effects = environment_settings.get("atmospheric_effects", [])
        
        # Style & Artistic Settings
        style_settings = settings.get("style_settings", {})
        art_movement = style_settings.get("art_movement", "Realism")
        post_processing = style_settings.get("post_processing", [])
        
        # Detail & Quality Settings
        detail_settings = settings.get("detail_settings", {})
        detail_level = detail_settings.get("detail_level", "ultra_detailed")
        texture_quality = detail_settings.get("texture_quality", "high")
        special_effects = detail_settings.get("special_effects", [])
        
        # Color Settings
        color_settings = settings.get("color_settings", {})
        color_scheme = color_settings.get("color_scheme", "natural")
        palette_type = color_settings.get("palette_type", "analogous")
        color_temperature = color_settings.get("color_temperature", "neutral")
        
        # Quality Settings
        quality_settings = settings.get("quality_settings", {})
        resolution = quality_settings.get("resolution", "1920x1080")
        rendering_quality = quality_settings.get("rendering_quality", "photorealistic")
        
        # Randomly select tags
        selected_tags = random.sample(tags, min(3, len(tags)))
        
        # Format the prompt with all settings
        prompt = f"A {style} {mood} {rendering_quality} image of {', '.join(selected_tags)}, "
        prompt += f"captured with a {camera_model} using a {lens_type} lens at {aperture} with {depth_of_field} depth of field, "
        prompt += f"during {time_of_day} with {lighting_style} {light_quality} lighting"
        
        if artificial_sources:
            prompt += f" and {', '.join(artificial_sources)} artificial lighting"
        
        prompt += f", composed using {technique} from a {camera_angle} angle with {perspective} perspective, "
        prompt += f"in {weather} weather during {season}"
        
        if atmospheric_effects:
            prompt += f" with {', '.join(atmospheric_effects)}"
        
        prompt += f", styled in {art_movement} movement"
        
        if post_processing:
            prompt += f" with {', '.join(post_processing)} post-processing"
        
        prompt += f", featuring {detail_level} details and {texture_quality} texture quality"
        
        if special_effects:
            prompt += f" with {', '.join(special_effects)} effects"
        
        prompt += f", using a {color_scheme} color scheme with {palette_type} palette and {color_temperature} temperature, "
        prompt += f"rendered at {resolution} resolution"
        
        return prompt
    except Exception as e:
        print_error(f"Error generating random prompt: {str(e)}")
        return None

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

def create_filename_from_prompt(prompt, max_length=30):
    """Create a descriptive filename from the prompt.
    
    Args:
        prompt: The prompt to create a filename from
        max_length: Maximum length of the descriptive part of the filename
        
    Returns:
        A sanitized, shortened filename based on the prompt
    """
    # Remove special characters and replace spaces with underscores
    sanitized = re.sub(r'[^\w\s-]', '', prompt.lower())
    sanitized = re.sub(r'[-\s]+', '_', sanitized)
    
    # Truncate to the maximum length
    if len(sanitized) > max_length:
        # Try to cut at a word boundary
        sanitized = sanitized[:max_length].rsplit('_', 1)[0]
    
    # Add a unique identifier (first 8 chars of the hash)
    hash_object = hashlib.sha256(prompt.encode())
    short_hash = hash_object.hexdigest()[:8]
    
    return f"{sanitized}_{short_hash}.png"

def extract_subject_from_prompt(prompt):
    """Extract the main subject from a prompt using Gemini.
    
    Args:
        prompt: The prompt to extract the subject from
        
    Returns:
        A string containing the main subject of the prompt
    """
    if not GEMINI_API_KEY:
        logging.warning("No Gemini API key configured, using fallback filename generation")
        return None
        
    try:
        # Use the same approach as generate_prompt_gemini
        import google.generativeai as genai
        
        # Set up the model
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Create the analysis request
        analysis_prompt = f"""
        Extract the main subject or theme from this wallpaper description in 2-5 words.
        Only return the extracted subject - no explanations or additional text.
        Make it suitable for use as a filename.
        
        Description: {prompt}
        """
        
        # Get the response
        response = model.generate_content(
            contents=analysis_prompt
        )
        
        if response and hasattr(response, 'candidates') and response.candidates:
            text = response.candidates[0].content.parts[0].text
            subject = text.strip()
            # Clean up any quotes or extra formatting
            subject = subject.replace('"', '').replace("'", "")
            
            # Sanitize for filename use
            subject = re.sub(r'[^\w\s-]', '', subject.lower())
            subject = re.sub(r'[-\s]+', '_', subject)
            
            logging.debug(f"Extracted subject from prompt: {subject}")
            return subject
        else:
            logging.warning("Empty response from Gemini for subject extraction")
            return None
    except Exception as e:
        logging.error(f"Error extracting subject with Gemini: {e}")
        return None

def get_generated_image_path(prompt):
    """Get the cache path for the generated image."""
    # Try to extract a meaningful subject from the prompt
    subject = extract_subject_from_prompt(prompt)
    
    if subject:
        # Use the extracted subject for the filename
        hash_object = hashlib.sha256(prompt.encode())
        short_hash = hash_object.hexdigest()[:8]
        filename = f"{subject}_{short_hash}.png"
    else:
        # Fall back to the original method
        filename = create_filename_from_prompt(prompt)
    
    # Ensure the genimage directory exists with absolute path
    genimage_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "genimage")
    try:
        os.makedirs(genimage_dir, exist_ok=True)
        logging.info(f"Ensuring genimage directory exists at: {genimage_dir}")
    except Exception as e:
        logging.error(f"Error creating genimage directory: {e}")
        # Fallback to relative path if absolute path fails
        genimage_dir = "genimage"
        os.makedirs(genimage_dir, exist_ok=True)
        
    # Return absolute path to ensure consistency
    return os.path.join(genimage_dir, filename)

def generate_prompt(custom_prompt=None):
    """Generate a prompt using either AI, random tags, or custom input."""
    try:
        if custom_prompt:
            print_info("Processing custom prompt...")
            try:
                # Enhance the custom prompt with current settings
                enhanced_prompt = enhance_custom_prompt(custom_prompt)
                if enhanced_prompt:
                    print_prompt(enhanced_prompt)
                    return enhanced_prompt
                else:
                    print_warning("Failed to enhance custom prompt, using original")
                    return custom_prompt
            except Exception as e:
                logging.error(f"Error enhancing custom prompt: {e}")
                print_warning("Failed to enhance custom prompt, using original")
                return custom_prompt
        
        print_section("Prompt Generation")
        print_info("Choose prompt generation method:")
        print_option("1", "AI-Powered Prompt")
        print_option("2", "Random Tag Combination")
        print_option("3", "Custom Prompt Input")
        print_option("4", "Return to main menu")
        
        choice = get_validated_input("Select option (1-4)", ["1", "2", "3", "4"])
        
        if choice == "4":
            return None
            
        if choice == "1":
            # Get user preferences for prompt generation
            tags = []
            if user_prefs.preferred_genres:
                tags.extend(user_prefs.preferred_genres)
            
            # Generate prompt using Gemini
            prompt = generate_prompt_gemini(tags)
            if prompt:
                print_prompt(prompt)
                return prompt
                
        elif choice == "2":
            # Get user preferences for prompt generation
            tags = []
            if user_prefs.preferred_genres:
                tags.extend(user_prefs.preferred_genres)
            
            # Generate prompt using random tags
            prompt = generate_prompt_random(tags)
            if prompt:
                print_prompt(prompt)
                return prompt
                
        elif choice == "3":
            custom_prompt = get_validated_input("Enter your custom prompt (or 'b' to go back)", allow_empty=False)
            if custom_prompt.lower() == 'b':
                return None
            
            if custom_prompt:
                print_info("Processing custom prompt...")
                try:
                    # Enhance the custom prompt with current settings
                    enhanced_prompt = enhance_custom_prompt(custom_prompt)
                    if enhanced_prompt:
                        print_prompt(enhanced_prompt)
                        return enhanced_prompt
                    else:
                        print_warning("Failed to enhance custom prompt, using original")
                        return custom_prompt
                except Exception as e:
                    logging.error(f"Error enhancing custom prompt: {e}")
                    print_warning("Failed to enhance custom prompt, using original")
                    return custom_prompt
            else:
                print_warning("Empty prompt provided")
                return None
        
        return None
        
    except Exception as e:
        logging.error(f"Error in generate_prompt: {e}")
        print_error("An unexpected error occurred while generating the prompt")
        return None

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
    
    # Ensure we have an absolute path from the project directory
    if not os.path.isabs(image_path):
        # Convert relative path to absolute path based on the project directory
        absolute_path = os.path.abspath(image_path)
    else:
        absolute_path = image_path
    
    # Save the original path for later verification
    original_path = image_path
        
    try:
        if os_name == "Windows":
            SPI_SETDESKWALLPAPER = 0x0014
            SPIF_UPDATEINIFILE = 0x01
            SPIF_SENDWININICHANGE = 0x02
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, absolute_path, SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)
            logging.info("Wallpaper set successfully on Windows")
            return True
        elif os_name == "Darwin":
            script = f'tell application "Finder" to set desktop picture to POSIX file "{absolute_path}"'
            command = f"osascript -e '{script}'"
            subprocess.run(shlex.split(command), check=True, capture_output=True, text=True)
            logging.info("Wallpaper set successfully on macOS")
            return True
        elif os_name == "Linux":
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
                logging.info(f"Wallpaper set successfully on Linux using path: {absolute_path}")
                logging.info(f"Original path was: {original_path}")
                return True
            elif desktop_env == 'CINNAMON':
                # Cinnamon
                command = ["gsettings", "set", "org.cinnamon.desktop.background", "picture-uri", file_uri]
                subprocess.run(command, check=True, capture_output=True, text=True)
                logging.info("Wallpaper set successfully on Linux")
                return True
            elif desktop_env == 'MATE':
                # MATE
                command = ["gsettings", "set", "org.mate.background", "picture-filename", absolute_path]
                subprocess.run(command, check=True, capture_output=True, text=True)
                logging.info("Wallpaper set successfully on Linux")
                return True
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
                        logging.info("Wallpaper set successfully on Linux")
                        return True
                    else:
                        print_warning("No monitors found for XFCE")
                        return False
                except (subprocess.SubprocessError, FileNotFoundError):
                    print_warning("Failed to set wallpaper using xfconf-query")
                    return False
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
                    logging.info("Wallpaper set successfully on Linux")
                    return True
                except (subprocess.SubprocessError, FileNotFoundError):
                    print_warning("Failed to set wallpaper using KDE Plasma method")
                    return False
            elif desktop_env in ['I3', 'SWAY']:
                # i3/sway - try feh first, then nitrogen
                try:
                    command = ["feh", "--bg-fill", absolute_path]
                    subprocess.run(command, check=True, capture_output=True, text=True)
                    logging.info("Wallpaper set successfully on Linux")
                    return True
                except (subprocess.SubprocessError, FileNotFoundError):
                    try:
                        command = ["nitrogen", "--set-zoom-fill", absolute_path]
                        subprocess.run(command, check=True, capture_output=True, text=True)
                        logging.info("Wallpaper set successfully on Linux")
                        return True
                    except (subprocess.SubprocessError, FileNotFoundError):
                        print_warning("Failed to set wallpaper using feh or nitrogen")
                        return False
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
                    logging.info("Wallpaper set successfully on Linux")
                    return True
                else:
                    print_warning("Could not set wallpaper with any known method")
                    return False
            
        else:
            logging.warning(f"Unsupported operating system: {os_name}")
            return False
    except subprocess.CalledProcessError as e:
        logging.error(f"Error setting wallpaper (subprocess): {e}")
        logging.error(f"Stdout: {e.stdout}")
        logging.error(f"Stderr: {e.stderr}")
        return False
    except OSError as e:
        logging.error(f"OS error setting wallpaper: {e}")
        return False
    except ValueError as e:
        logging.error(f"Value error setting wallpaper: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error setting wallpaper: {e}")
        return False

def enhance_custom_prompt(custom_prompt):
    """Enhance the custom prompt using the Gemini model based on user preferences."""
    try:
        # Get user preferences
        style = user_prefs.preferred_styles[0] if user_prefs.preferred_styles else "photorealistic"
        mood = user_prefs.preferred_moods[0] if user_prefs.preferred_moods else "neutral"
        
        # Get all settings from imagen_settings
        settings = user_prefs.imagen_settings
        
        # Camera Settings
        camera_settings = settings.get("camera_settings", {})
        camera_model = camera_settings.get("camera_model", "RED Digital Cinema")
        lens_type = camera_settings.get("lens_type", "50mm")
        aperture = camera_settings.get("aperture", "f/2.8")
        special_lens = camera_settings.get("special_lens", "standard")
        depth_of_field = camera_settings.get("depth_of_field", "medium")
        
        # Lighting Settings
        lighting_settings = settings.get("lighting_settings", {})
        time_of_day = lighting_settings.get("time_of_day", "midday")
        lighting_style = lighting_settings.get("lighting_style", "natural")
        light_quality = lighting_settings.get("light_quality", "soft")
        artificial_sources = lighting_settings.get("artificial_sources", [])
        
        # Composition Settings
        composition_settings = settings.get("composition_settings", {})
        technique = composition_settings.get("technique", "framing")
        camera_angle = composition_settings.get("camera_angle", "eye_level")
        perspective = composition_settings.get("perspective", "wide")
        
        # Environment Settings
        environment_settings = settings.get("environment_settings", {})
        weather = environment_settings.get("weather", "clear")
        season = environment_settings.get("season", "summer")
        atmospheric_effects = environment_settings.get("atmospheric_effects", [])
        
        # Style Settings
        style_settings = settings.get("style_settings", {})
        art_movement = style_settings.get("art_movement", "Abstract Expressionism")
        post_processing = style_settings.get("post_processing", [])
        
        # Detail Settings
        detail_settings = settings.get("detail_settings", {})
        detail_level = detail_settings.get("detail_level", "ultra_detailed")
        texture_quality = detail_settings.get("texture_quality", "high")
        special_effects = detail_settings.get("special_effects", [])
        
        # Color Settings
        color_settings = settings.get("color_settings", {})
        color_scheme = color_settings.get("color_scheme", "natural")
        palette_type = color_settings.get("palette_type", "analogous")
        color_temperature = color_settings.get("color_temperature", "neutral")
        
        # Quality Settings
        quality_settings = settings.get("quality_settings", {})
        resolution = quality_settings.get("resolution", "8k")
        rendering_quality = quality_settings.get("rendering_quality", "photorealistic")
        
        # Format the custom prompt instructions with all settings
        enhancement_instructions = CUSTOM_PROMPT_INSTRUCTIONS.format(
            style=style,
            mood=mood,
            resolution=resolution,
            aspect_ratio=user_prefs.aspect_ratio,
            color_scheme=color_scheme,
            lighting=lighting_style,
            composition=technique,
            camera_model=camera_model,
            lens_type=lens_type,
            aperture=aperture,
            special_lens=special_lens,
            depth_of_field=depth_of_field,
            time_of_day=time_of_day,
            light_quality=light_quality,
            artificial_sources=", ".join(artificial_sources) if artificial_sources else "none",
            camera_angle=camera_angle,
            perspective=perspective,
            weather=weather,
            season=season,
            atmospheric_effects=", ".join(atmospheric_effects) if atmospheric_effects else "none",
            art_movement=art_movement,
            post_processing=", ".join(post_processing) if post_processing else "none",
            detail_level=detail_level,
            texture_quality=texture_quality,
            special_effects=", ".join(special_effects) if special_effects else "none",
            palette_type=palette_type,
            color_temperature=color_temperature,
            rendering_quality=rendering_quality
        )
        
        # Generate enhanced prompt using Gemini
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(enhancement_instructions + "\n\nPrompt to enhance: " + custom_prompt)

        if response.parts:
            enhanced_prompt = response.parts[0].text.strip()
            
            # Clean up the prompt format
            # Remove any markdown formatting
            enhanced_prompt = enhanced_prompt.replace("**", "")
            
            # Remove any explanatory text after the prompt
            if "Explanation" in enhanced_prompt:
                enhanced_prompt = enhanced_prompt.split("Explanation")[0].strip()
            
            # Remove any "Prompt:" or similar headers
            if "Prompt:" in enhanced_prompt:
                enhanced_prompt = enhanced_prompt.split("Prompt:")[1].strip()
            
            # Remove any quotes around the prompt
            if enhanced_prompt.startswith('"') and enhanced_prompt.endswith('"'):
                enhanced_prompt = enhanced_prompt[1:-1]
            
            # Remove any numbered options
            if "Option" in enhanced_prompt:
                enhanced_prompt = enhanced_prompt.split("Option")[0].strip()
            
            return enhanced_prompt
        else:
            return custom_prompt

    except Exception as e:
        logging.error(f"Error enhancing prompt with Gemini: {e}")
        return custom_prompt

def sanitize_log_content(content):
    """Sanitize log content by masking sensitive information."""
    if isinstance(content, str):
        content = content.replace(os.environ.get("GEMINI_API_KEY", ""), "<GEMINI_API_KEY>")
    return content

def save_prompts_to_json(gemini_prompt, enhanced_prompt, filename="prompts.json"):
    """Save the prompts to a JSON file."""
    try:
        with open(filename, "a") as f:
            json.dump({"gemini_prompt": gemini_prompt, "enhanced_prompt": enhanced_prompt}, f)
            f.write("\n")
    except Exception as e:
        logging.error(f"Error saving prompts to JSON: {e}")

def manage_imagen_settings():
    """Manage Imagen 3 specific settings."""
    print_header("Imagen 3 Settings")
    
    while True:
        print_section("Options")
        print_option("1", "View Current Settings")
        print_option("2", "Reset to Defaults")
        print_option("3", "Return to Main Menu")
        
        choice = get_validated_input("Select an option (1-3)", ["1", "2", "3"])
        
        if choice == "1":
            print_section("Current Settings")
            print_info(f"Number of Images: {user_prefs.imagen_settings['number_of_images']}")
            print_info(f"Seed: {user_prefs.imagen_settings['seed'] or 'Random'}")
            print_info(f"Negative Prompt: {user_prefs.imagen_settings['negative_prompt'] or 'None'}")
            print_info(f"Aspect Ratio: {user_prefs.aspect_ratio}")
            print_info(f"Color Scheme: {user_prefs.imagen_settings.get('color_scheme', 'natural')}")
            print_info(f"Lighting: {user_prefs.imagen_settings.get('lighting', 'natural')}")
            print_info(f"Composition: {user_prefs.imagen_settings.get('composition', 'rule_of_thirds')}")
            print_info(f"Depth of Field: {user_prefs.imagen_settings.get('depth_of_field', 'medium')}")
            
        elif choice == "2":
            print_section("Reset to Defaults")
            user_prefs.imagen_settings = {
                "number_of_images": 1,
                "seed": None,
                "aspect_ratio": "16:9",
                "negative_prompt": "",
                "color_scheme": "natural",
                "lighting": "natural",
                "composition": "rule_of_thirds",
                "depth_of_field": "medium"
            }
            user_prefs.save_preferences()
            print_success("Settings reset to defaults")
            
        elif choice == "3":
            break

def configure_advanced_options():
    """Configure advanced options for image generation."""
    print_section("Advanced Options")
    print_info("Fine-tune the generation parameters:")
    
    while True:
        print_option("1", "Style & Artistic Settings")
        print_option("2", "Camera & Technical Settings")
        print_option("3", "Lighting & Atmosphere")
        print_option("4", "Composition & Environment")
        print_option("5", "Color & Detail Settings")
        print_option("6", "Show Current Settings")
        print_option("7", "Customize All Parameters")
        print_option("8", "Return to previous menu")
        
        advanced_choice = get_validated_input("Select option (1-8)", ["1", "2", "3", "4", "5", "6", "7", "8"])
        
        if advanced_choice == "1":
            print_section("Style & Artistic Settings")
            print_info("Choose the artistic style and style-specific settings:")
            print_option("1", "Style Selection")
            print_option("2", "Art Movement")
            print_option("3", "Post-processing Effects")
            print_option("4", "Return")
            
            style_choice = get_validated_input("Select option (1-4)", ["1", "2", "3", "4"])
            if style_choice == "4":
                continue
                
            if style_choice == "1":
                print_info("Choose the artistic style for your wallpaper:")
                print_option("1", "Photorealistic")
                print_option("2", "Digital Art")
                print_option("3", "Sketch")
                print_option("4", "Watercolor")
                print_option("5", "Cyberpunk")
                print_option("6", "Pop Art")
                print_option("7", "Oil Painting")
                print_option("8", "Pixel Art")
                print_option("9", "Anime")
                print_option("10", "3D Render")
                print_option("11", "Abstract")
                print_option("12", "Impressionism")
                print_option("13", "Minimalist")
                print_option("14", "Surrealism")
                print_option("15", "Random Style Mix (combines 2-3 compatible styles)")
                print_option("16", "More Styles...")
                print_option("17", "Custom Style")
                print_option("18", "Return")
                
                style_select = get_validated_input("Select style (1-18)", [str(i) for i in range(1, 19)])
                if style_select == "18":
                    continue
                
                if style_select == "16":
                    # Show more styles submenu
                    print_info("Additional art styles:")
                    print_option("1", "Art Deco")
                    print_option("2", "Art Nouveau")
                    print_option("3", "Cartoon")
                    print_option("4", "Charcoal")
                    print_option("5", "Cinematic")
                    print_option("6", "Comic Book")
                    print_option("7", "Cubism")
                    print_option("8", "Fantasy")
                    print_option("9", "Futurism")
                    print_option("10", "Gothic")
                    print_option("11", "Manga")
                    print_option("12", "Retro/Vaporwave")
                    print_option("13", "Sci-Fi")
                    print_option("14", "Steampunk")
                    print_option("15", "Return")
                    
                    more_style_select = get_validated_input("Select style (1-15)", [str(i) for i in range(1, 16)])
                    if more_style_select == "15":
                        continue
                    
                    more_styles = {
                        "1": "art_deco",
                        "2": "art_nouveau",
                        "3": "cartoon",
                        "4": "charcoal",
                        "5": "cinematic",
                        "6": "comic_book",
                        "7": "cubism",
                        "8": "fantasy",
                        "9": "futurism",
                        "10": "gothic",
                        "11": "manga",
                        "12": "vaporwave",
                        "13": "sci_fi",
                        "14": "steampunk"
                    }
                    
                    selected_style = more_styles[more_style_select]
                    user_prefs.preferred_styles = [selected_style]
                    print_success(f"Style set to {selected_style}")
                    continue
                    
                if style_select == "17":
                    custom_style = input("Enter your custom style: ").strip()
                    if custom_style:
                        user_prefs.preferred_styles = [custom_style]
                        print_success(f"Custom style set to: {custom_style}")
                    continue
                
                if style_select == "15":
                    # Use the same style categories defined elsewhere
                    style_categories = {
                        "traditional_art": ["art_deco", "art_nouveau", "charcoal", "expressionism", 
                                          "gothic", "impressionism", "oil_painting", "pastel", 
                                          "pencil_sketch", "realism", "sketch", "watercolor", "woodcut"],
                        "digital_art": ["abstract", "cinematic", "cyberpunk", "digital_art", "double_exposure", 
                                      "fantasy", "futurism", "glitch_art", "hyperrealism", "isometric", 
                                      "landscape", "low_poly", "minimalist", "retrowave", "sci_fi",
                                      "stained_glass", "steampunk", "surrealism", "vaporwave"],
                        "illustration": ["anime", "cartoon", "comic_book", "divisionism", "graffiti", 
                                       "ink_drawing", "line_art", "manga", "paper_cut", "pixel_art", 
                                       "pointillism", "pop_art", "ukiyo_e"]
                    }
                    
                    # Select a random category
                    category = random.choice(list(style_categories.keys()))
                    # Select 2-3 compatible styles from the same category
                    num_styles = random.randint(2, 3)
                    available_styles = style_categories[category]
                    if len(available_styles) < num_styles:
                        num_styles = len(available_styles)
                    selected_styles = random.sample(available_styles, num_styles)
                    style_mix = " + ".join(selected_styles)
                    
                    print_info(f"Generated random style mix: {style_mix}")
                    user_prefs.preferred_styles = [style_mix]
                    
                    # Ask if the user wants to save this style mix to their preferences long-term
                    save_style = get_validated_input("Save this style mix for future use? (y/n)", ["y", "n"])
                    if save_style == "y":
                        if style_mix not in user_prefs.preferred_styles:
                            user_prefs.preferred_styles.append(style_mix)
                            user_prefs.save_preferences()
                            print_success(f"Added '{style_mix}' to preferred styles")
                        else:
                            print_warning(f"'{style_mix}' is already in your preferred styles")
                    
                    print_success(f"Style set to {style_mix}")
                    continue
                    
                styles = {
                    "1": "photograph",
                    "2": "digital_art",
                    "3": "sketch",
                    "4": "watercolor",
                    "5": "cyberpunk",
                    "6": "pop_art",
                    "7": "oil_painting",
                    "8": "pixel_art",
                    "9": "anime",
                    "10": "3d_render",
                    "11": "abstract",
                    "12": "impressionism",
                    "13": "minimalist",
                    "14": "surrealism"
                }
                
                selected_style = styles[style_select]
                user_prefs.preferred_styles = [selected_style]
                print_success(f"Style set to {selected_style}")
                continue
                
            elif style_choice == "2":
                print_info("Select art movement:")
                print_option("1", "Abstract Expressionism")
                print_option("2", "Impressionism")
                print_option("3", "Surrealism")
                print_option("4", "Minimalism")
                print_option("5", "Cubism")
                print_option("6", "Custom")
                print_option("7", "Return")
                
                movement_choice = get_validated_input("Select movement (1-7)", [str(i) for i in range(1, 8)])
                if movement_choice == "7":
                    continue
                    
                if movement_choice == "6":
                    custom_movement = input("Enter custom art movement: ").strip()
                    if custom_movement:
                        user_prefs.imagen_settings["style_settings"]["art_movement"] = custom_movement
                        print_success(f"Custom art movement set to: {custom_movement}")
                    continue
                    
                movements = {
                    "1": "Abstract Expressionism",
                    "2": "Impressionism",
                    "3": "Surrealism",
                    "4": "Minimalism",
                    "5": "Cubism"
                }
                
                user_prefs.imagen_settings["style_settings"]["art_movement"] = movements[movement_choice]
                print_success(f"Art movement set to {movements[movement_choice]}")
                continue
                
            elif style_choice == "3":
                print_info("Select post-processing effects (comma-separated):")
                print_option("1", "Vintage")
                print_option("2", "HDR")
                print_option("3", "Film Grain")
                print_option("4", "Color Grading")
                print_option("5", "Custom")
                print_option("6", "Return")
                
                effects_choice = get_validated_input("Select option (1-6)", ["1", "2", "3", "4", "5", "6"])
                if effects_choice == "6":
                    continue
                    
                if effects_choice == "5":
                    custom_effects = input("Enter custom effects (comma-separated): ").strip()
                    if custom_effects:
                        user_prefs.imagen_settings["style_settings"]["post_processing"] = [e.strip() for e in custom_effects.split(",")]
                        print_success(f"Custom effects set to: {custom_effects}")
                    continue
                    
                effects = {
                    "1": ["vintage"],
                    "2": ["hdr"],
                    "3": ["film_grain"],
                    "4": ["color_grading"]
                }
                
                user_prefs.imagen_settings["style_settings"]["post_processing"] = effects[effects_choice]
                print_success(f"Post-processing effects set to {effects[effects_choice]}")
                continue
                
        elif advanced_choice == "2":
            print_section("Camera & Technical Settings")
            print_info("Configure camera and technical parameters:")
            print_option("1", "Camera Model")
            print_option("2", "Lens Settings")
            print_option("3", "Resolution & Quality")
            print_option("4", "Return")
            
            tech_choice = get_validated_input("Select option (1-4)", ["1", "2", "3", "4"])
            if tech_choice == "4":
                continue
                
            if tech_choice == "1":
                print_info("Select camera model:")
                print_option("1", "ARRI Alexa")
                print_option("2", "RED Digital Cinema")
                print_option("3", "Sony Venice")
                print_option("4", "Custom")
                print_option("5", "Return")
                
                camera_choice = get_validated_input("Select camera (1-5)", ["1", "2", "3", "4", "5"])
                if camera_choice == "5":
                    continue
                    
                if camera_choice == "4":
                    custom_camera = input("Enter custom camera model: ").strip()
                    if custom_camera:
                        user_prefs.imagen_settings["camera_settings"]["camera_model"] = custom_camera
                        print_success(f"Custom camera model set to: {custom_camera}")
                    continue
                    
                cameras = {
                    "1": "ARRI Alexa",
                    "2": "RED Digital Cinema",
                    "3": "Sony Venice"
                }
                
                user_prefs.imagen_settings["camera_settings"]["camera_model"] = cameras[camera_choice]
                print_success(f"Camera model set to {cameras[camera_choice]}")
                continue
                
            elif tech_choice == "2":
                print_info("Configure lens settings:")
                print_option("1", "Lens Type")
                print_option("2", "Aperture")
                print_option("3", "Special Lens")
                print_option("4", "Depth of Field")
                print_option("5", "Return")
                
                lens_choice = get_validated_input("Select option (1-5)", ["1", "2", "3", "4", "5"])
                if lens_choice == "5":
                    continue
                    
                if lens_choice == "1":
                    print_info("Select lens type:")
                    print_option("1", "50mm")
                    print_option("2", "85mm")
                    print_option("3", "24mm")
                    print_option("4", "Custom")
                    print_option("5", "Return")
                    
                    lens_type = get_validated_input("Select lens type (1-5)", ["1", "2", "3", "4", "5"])
                    if lens_type == "5":
                        continue
                        
                    if lens_type == "4":
                        custom_lens = input("Enter custom lens type: ").strip()
                        if custom_lens:
                            user_prefs.imagen_settings["camera_settings"]["lens_type"] = custom_lens
                            print_success(f"Custom lens type set to: {custom_lens}")
                        continue
                        
                    lenses = {
                        "1": "50mm",
                        "2": "85mm",
                        "3": "24mm"
                    }
                    
                    user_prefs.imagen_settings["camera_settings"]["lens_type"] = lenses[lens_type]
                    print_success(f"Lens type set to {lenses[lens_type]}")
                    continue
                    
                elif lens_choice == "2":
                    print_info("Select aperture:")
                    print_option("1", "f/1.8")
                    print_option("2", "f/2.8")
                    print_option("3", "f/4")
                    print_option("4", "f/8")
                    print_option("5", "Custom")
                    print_option("6", "Return")
                    
                    aperture_choice = get_validated_input("Select aperture (1-6)", ["1", "2", "3", "4", "5", "6"])
                    if aperture_choice == "6":
                        continue
                        
                    if aperture_choice == "5":
                        custom_aperture = input("Enter custom aperture: ").strip()
                        if custom_aperture:
                            user_prefs.imagen_settings["camera_settings"]["aperture"] = custom_aperture
                            print_success(f"Custom aperture set to: {custom_aperture}")
                        continue
                        
                    apertures = {
                        "1": "f/1.8",
                        "2": "f/2.8",
                        "3": "f/4",
                        "4": "f/8"
                    }
                    
                    user_prefs.imagen_settings["camera_settings"]["aperture"] = apertures[aperture_choice]
                    print_success(f"Aperture set to {apertures[aperture_choice]}")
                    continue
                    
                elif lens_choice == "3":
                    print_info("Select special lens (optional):")
                    print_option("1", "Tilt-shift")
                    print_option("2", "Fisheye")
                    print_option("3", "Macro")
                    print_option("4", "None")
                    print_option("5", "Custom")
                    print_option("6", "Return")
                    
                    special_choice = get_validated_input("Select special lens (1-6)", ["1", "2", "3", "4", "5", "6"])
                    if special_choice == "6":
                        continue
                        
                    if special_choice == "5":
                        custom_special = input("Enter custom special lens: ").strip()
                        if custom_special:
                            user_prefs.imagen_settings["camera_settings"]["special_lens"] = custom_special
                            print_success(f"Custom special lens set to: {custom_special}")
                        continue
                        
                    if special_choice == "4":
                        user_prefs.imagen_settings["camera_settings"]["special_lens"] = None
                        print_success("Special lens set to None")
                        continue
                        
                    special_lenses = {
                        "1": "tilt_shift",
                        "2": "fisheye",
                        "3": "macro"
                    }
                    
                    user_prefs.imagen_settings["camera_settings"]["special_lens"] = special_lenses[special_choice]
                    print_success(f"Special lens set to {special_lenses[special_choice]}")
                    continue
                    
                elif lens_choice == "4":
                    print_info("Select depth of field:")
                    print_option("1", "Shallow")
                    print_option("2", "Medium")
                    print_option("3", "Deep")
                    print_option("4", "Custom")
                    print_option("5", "Return")
                    
                    dof_choice = get_validated_input("Select depth of field (1-5)", ["1", "2", "3", "4", "5"])
                    if dof_choice == "5":
                        continue
                        
                    if dof_choice == "4":
                        custom_dof = input("Enter custom depth of field: ").strip()
                        if custom_dof:
                            user_prefs.imagen_settings["camera_settings"]["depth_of_field"] = custom_dof
                            print_success(f"Custom depth of field set to: {custom_dof}")
                        continue
                        
                    dof_options = {
                        "1": "shallow",
                        "2": "medium",
                        "3": "deep"
                    }
                    
                    user_prefs.imagen_settings["camera_settings"]["depth_of_field"] = dof_options[dof_choice]
                    print_success(f"Depth of field set to {dof_options[dof_choice]}")
                    continue
                    
            elif tech_choice == "3":
                print_info("Configure resolution and quality settings:")
                print_option("1", "Resolution")
                print_option("2", "Detail Level")
                print_option("3", "Rendering Quality")
                print_option("4", "Return")
                
                quality_choice = get_validated_input("Select option (1-4)", ["1", "2", "3", "4"])
                if quality_choice == "4":
                    continue
                    
                if quality_choice == "1":
                    print_info("Select resolution:")
                    print_option("1", "1920x1080 (Full HD)")
                    print_option("2", "2560x1440 (2K)")
                    print_option("3", "3840x2160 (4K)")
                    print_option("4", "5120x2880 (5K)")
                    print_option("5", "7680x4320 (8K)")
                    print_option("6", "Custom")
                    print_option("7", "Return")
                    
                    res_choice = get_validated_input("Select resolution (1-7)", ["1", "2", "3", "4", "5", "6", "7"])
                    if res_choice == "7":
                        continue
                        
                    if res_choice == "6":
                        custom_res = input("Enter custom resolution (e.g., 1920x1080): ").strip()
                        if "x" in custom_res:
                            user_prefs.imagen_settings["quality_settings"]["resolution"] = custom_res
                            print_success(f"Custom resolution set to: {custom_res}")
                        continue
                        
                    resolutions = {
                        "1": "1920x1080",
                        "2": "2560x1440",
                        "3": "3840x2160",
                        "4": "5120x2880",
                        "5": "7680x4320"
                    }
                    
                    user_prefs.imagen_settings["quality_settings"]["resolution"] = resolutions[res_choice]
                    print_success(f"Resolution set to {resolutions[res_choice]}")
                    continue
                    
                elif quality_choice == "2":
                    print_info("Select detail level:")
                    print_option("1", "Ultra Detailed")
                    print_option("2", "High Detail")
                    print_option("3", "Medium Detail")
                    print_option("4", "Low Detail")
                    print_option("5", "Custom")
                    print_option("6", "Return")
                    
                    detail_choice = get_validated_input("Select detail level (1-6)", ["1", "2", "3", "4", "5", "6"])
                    if detail_choice == "6":
                        continue
                        
                    if detail_choice == "5":
                        custom_detail = input("Enter custom detail level: ").strip()
                        if custom_detail:
                            user_prefs.imagen_settings["quality_settings"]["detail_level"] = custom_detail
                            print_success(f"Custom detail level set to: {custom_detail}")
                        continue
                        
                    detail_levels = {
                        "1": "ultra_detailed",
                        "2": "high_detail",
                        "3": "medium_detail",
                        "4": "low_detail"
                    }
                    
                    user_prefs.imagen_settings["quality_settings"]["detail_level"] = detail_levels[detail_choice]
                    print_success(f"Detail level set to {detail_levels[detail_choice]}")
                    continue
                    
                elif quality_choice == "3":
                    print_info("Select rendering quality:")
                    print_option("1", "Photorealistic")
                    print_option("2", "High Quality")
                    print_option("3", "Medium Quality")
                    print_option("4", "Custom")
                    print_option("5", "Return")
                    
                    render_choice = get_validated_input("Select rendering quality (1-5)", ["1", "2", "3", "4", "5"])
                    if render_choice == "5":
                        continue
                        
                    if render_choice == "4":
                        custom_render = input("Enter custom rendering quality: ").strip()
                        if custom_render:
                            user_prefs.imagen_settings["quality_settings"]["rendering_quality"] = custom_render
                            print_success(f"Custom rendering quality set to: {custom_render}")
                        continue
                        
                    render_qualities = {
                        "1": "photorealistic",
                        "2": "high_quality",
                        "3": "medium_quality"
                    }
                    
                    user_prefs.imagen_settings["quality_settings"]["rendering_quality"] = render_qualities[render_choice]
                    print_success(f"Rendering quality set to {render_qualities[render_choice]}")
                    continue
                    
        elif advanced_choice == "3":
            print_section("Lighting & Atmosphere")
            print_info("Configure lighting and atmospheric settings:")
            print_option("1", "Time of Day")
            print_option("2", "Lighting Style")
            print_option("3", "Light Quality")
            print_option("4", "Artificial Sources")
            print_option("5", "Return")
            
            light_choice = get_validated_input("Select option (1-5)", ["1", "2", "3", "4", "5"])
            if light_choice == "5":
                continue
                
            if light_choice == "1":
                print_info("Select time of day:")
                print_option("1", "Golden Hour")
                print_option("2", "Blue Hour")
                print_option("3", "Midday")
                print_option("4", "Night")
                print_option("5", "Custom")
                print_option("6", "Return")
                
                time_choice = get_validated_input("Select time of day (1-6)", ["1", "2", "3", "4", "5", "6"])
                if time_choice == "6":
                    continue
                    
                if time_choice == "5":
                    custom_time = input("Enter custom time of day: ").strip()
                    if custom_time:
                        user_prefs.imagen_settings["lighting_settings"]["time_of_day"] = custom_time
                        print_success(f"Custom time of day set to: {custom_time}")
                    continue
                    
                times = {
                    "1": "golden_hour",
                    "2": "blue_hour",
                    "3": "midday",
                    "4": "night"
                }
                
                user_prefs.imagen_settings["lighting_settings"]["time_of_day"] = times[time_choice]
                print_success(f"Time of day set to {times[time_choice]}")
                
            elif light_choice == "2":
                print_info("Select lighting style:")
                print_option("1", "Natural")
                print_option("2", "Studio")
                print_option("3", "Dramatic")
                print_option("4", "Soft")
                print_option("5", "Harsh")
                print_option("6", "Volumetric")
                print_option("7", "Custom")
                print_option("8", "Return")
                
                style_choice = get_validated_input("Select lighting style (1-8)", ["1", "2", "3", "4", "5", "6", "7", "8"])
                if style_choice == "8":
                    continue
                    
                if style_choice == "7":
                    custom_style = input("Enter custom lighting style: ").strip()
                    if custom_style:
                        user_prefs.imagen_settings["lighting_settings"]["lighting_style"] = custom_style
                        print_success(f"Custom lighting style set to: {custom_style}")
                    continue
                    
                styles = {
                    "1": "natural",
                    "2": "studio",
                    "3": "dramatic",
                    "4": "soft",
                    "5": "harsh",
                    "6": "volumetric"
                }
                
                user_prefs.imagen_settings["lighting_settings"]["lighting_style"] = styles[style_choice]
                print_success(f"Lighting style set to {styles[style_choice]}")
                continue
                
            elif light_choice == "3":
                print_info("Select light quality:")
                print_option("1", "Soft")
                print_option("2", "Hard")
                print_option("3", "Diffused")
                print_option("4", "Direct")
                print_option("5", "Custom")
                print_option("6", "Return")
                
                quality_choice = get_validated_input("Select light quality (1-6)", ["1", "2", "3", "4", "5", "6"])
                if quality_choice == "6":
                    continue
                    
                if quality_choice == "5":
                    custom_quality = input("Enter custom light quality: ").strip()
                    if custom_quality:
                        user_prefs.imagen_settings["lighting_settings"]["light_quality"] = custom_quality
                        print_success(f"Custom light quality set to: {custom_quality}")
                    continue
                    
                qualities = {
                    "1": "soft",
                    "2": "hard",
                    "3": "diffused",
                    "4": "direct"
                }
                
                user_prefs.imagen_settings["lighting_settings"]["light_quality"] = qualities[quality_choice]
                print_success(f"Light quality set to {qualities[quality_choice]}")
                continue
                
            elif light_choice == "4":
                print_info("Add artificial light sources (comma-separated):")
                print_option("1", "LED")
                print_option("2", "Neon")
                print_option("3", "Spotlight")
                print_option("4", "Custom")
                print_option("5", "None")
                print_option("6", "Return")
                
                source_choice = get_validated_input("Select option (1-6)", ["1", "2", "3", "4", "5", "6"])
                if source_choice == "6":
                    continue
                    
                if source_choice == "4":
                    custom_sources = input("Enter custom light sources (comma-separated): ").strip()
                    if custom_sources:
                        user_prefs.imagen_settings["lighting_settings"]["artificial_sources"] = [s.strip() for s in custom_sources.split(",")]
                        print_success(f"Custom light sources set to: {custom_sources}")
                    continue
                    
                if source_choice == "5":
                    user_prefs.imagen_settings["lighting_settings"]["artificial_sources"] = []
                    print_success("Light sources set to None")
                    continue
                    
                sources = {
                    "1": ["led"],
                    "2": ["neon"],
                    "3": ["spotlight"]
                }
                
                user_prefs.imagen_settings["lighting_settings"]["artificial_sources"] = sources[source_choice]
                print_success(f"Light sources set to {sources[source_choice]}")
                continue
                
        elif advanced_choice == "4":
            print_section("Composition & Environment")
            print_info("Configure composition and environmental settings:")
            print_option("1", "Composition Technique")
            print_option("2", "Camera Angle")
            print_option("3", "Perspective")
            print_option("4", "Weather")
            print_option("5", "Season")
            print_option("6", "Atmospheric Effects")
            print_option("7", "Return")
            
            comp_choice = get_validated_input("Select option (1-7)", ["1", "2", "3", "4", "5", "6", "7"])
            if comp_choice == "7":
                continue
                
            if comp_choice == "1":
                print_info("Select composition technique:")
                print_option("1", "Rule of Thirds")
                print_option("2", "Leading Lines")
                print_option("3", "Framing")
                print_option("4", "Symmetry")
                print_option("5", "Asymmetry")
                print_option("6", "Custom")
                print_option("7", "Return")
                
                technique_choice = get_validated_input("Select technique (1-7)", ["1", "2", "3", "4", "5", "6", "7"])
                if technique_choice == "7":
                    continue
                    
                if technique_choice == "6":
                    custom_technique = input("Enter custom composition technique: ").strip()
                    if custom_technique:
                        user_prefs.imagen_settings["composition_settings"]["technique"] = custom_technique
                        print_success(f"Custom composition technique set to: {custom_technique}")
                    continue
                    
                techniques = {
                    "1": "rule_of_thirds",
                    "2": "leading_lines",
                    "3": "framing",
                    "4": "symmetry",
                    "5": "asymmetry"
                }
                
                user_prefs.imagen_settings["composition_settings"]["technique"] = techniques[technique_choice]
                print_success(f"Composition technique set to {techniques[technique_choice]}")
                continue
                
            elif comp_choice == "2":
                print_info("Select camera angle:")
                print_option("1", "Eye Level")
                print_option("2", "Low Angle")
                print_option("3", "High Angle")
                print_option("4", "Dutch Angle")
                print_option("5", "Custom")
                print_option("6", "Return")
                
                angle_choice = get_validated_input("Select camera angle (1-6)", ["1", "2", "3", "4", "5", "6"])
                if angle_choice == "6":
                    continue
                    
                if angle_choice == "5":
                    custom_angle = input("Enter custom camera angle: ").strip()
                    if custom_angle:
                        user_prefs.imagen_settings["composition_settings"]["camera_angle"] = custom_angle
                        print_success(f"Custom camera angle set to: {custom_angle}")
                    continue
                    
                angles = {
                    "1": "eye_level",
                    "2": "low_angle",
                    "3": "high_angle",
                    "4": "dutch_angle"
                }
                
                user_prefs.imagen_settings["composition_settings"]["camera_angle"] = angles[angle_choice]
                print_success(f"Camera angle set to {angles[angle_choice]}")
                continue
                
            elif comp_choice == "3":
                print_info("Select perspective:")
                print_option("1", "Wide")
                print_option("2", "Telephoto")
                print_option("3", "Macro")
                print_option("4", "Custom")
                print_option("5", "Return")
                
                perspective_choice = get_validated_input("Select perspective (1-5)", ["1", "2", "3", "4", "5"])
                if perspective_choice == "5":
                    continue
                    
                if perspective_choice == "4":
                    custom_perspective = input("Enter custom perspective: ").strip()
                    if custom_perspective:
                        user_prefs.imagen_settings["composition_settings"]["perspective"] = custom_perspective
                        print_success(f"Custom perspective set to: {custom_perspective}")
                    continue
                    
                perspectives = {
                    "1": "wide",
                    "2": "telephoto",
                    "3": "macro"
                }
                
                user_prefs.imagen_settings["composition_settings"]["perspective"] = perspectives[perspective_choice]
                print_success(f"Perspective set to {perspectives[perspective_choice]}")
                continue
                
            elif comp_choice == "4":
                print_info("Select weather conditions:")
                print_option("1", "Clear")
                print_option("2", "Cloudy")
                print_option("3", "Rainy")
                print_option("4", "Snowy")
                print_option("5", "Foggy")
                print_option("6", "Custom")
                print_option("7", "Return")
                
                weather_choice = get_validated_input("Select weather (1-7)", ["1", "2", "3", "4", "5", "6", "7"])
                if weather_choice == "7":
                    continue
                    
                if weather_choice == "6":
                    custom_weather = input("Enter custom weather: ").strip()
                    if custom_weather:
                        user_prefs.imagen_settings["environment_settings"]["weather"] = custom_weather
                        print_success(f"Custom weather set to: {custom_weather}")
                    continue
                    
                weathers = {
                    "1": "clear",
                    "2": "cloudy",
                    "3": "rainy",
                    "4": "snowy",
                    "5": "foggy"
                }
                
                user_prefs.imagen_settings["environment_settings"]["weather"] = weathers[weather_choice]
                print_success(f"Weather set to {weathers[weather_choice]}")
                continue
                
            elif comp_choice == "5":
                print_info("Select season:")
                print_option("1", "Spring")
                print_option("2", "Summer")
                print_option("3", "Autumn")
                print_option("4", "Winter")
                print_option("5", "Custom")
                print_option("6", "Return")
                
                season_choice = get_validated_input("Select season (1-6)", ["1", "2", "3", "4", "5", "6"])
                if season_choice == "6":
                    continue
                    
                if season_choice == "5":
                    custom_season = input("Enter custom season: ").strip()
                    if custom_season:
                        user_prefs.imagen_settings["environment_settings"]["season"] = custom_season
                        print_success(f"Custom season set to: {custom_season}")
                    continue
                    
                seasons = {
                    "1": "spring",
                    "2": "summer",
                    "3": "autumn",
                    "4": "winter"
                }
                
                user_prefs.imagen_settings["environment_settings"]["season"] = seasons[season_choice]
                print_success(f"Season set to {seasons[season_choice]}")
                continue
                
            elif comp_choice == "6":
                print_info("Add atmospheric effects (comma-separated):")
                print_option("1", "Fog")
                print_option("2", "Mist")
                print_option("3", "Rain")
                print_option("4", "Snow")
                print_option("5", "Custom")
                print_option("6", "None")
                print_option("7", "Return")
                
                effect_choice = get_validated_input("Select option (1-7)", ["1", "2", "3", "4", "5", "6", "7"])
                if effect_choice == "7":
                    continue
                    
                if effect_choice == "5":
                    custom_effects = input("Enter custom atmospheric effects (comma-separated): ").strip()
                    if custom_effects:
                        user_prefs.imagen_settings["environment_settings"]["atmospheric_effects"] = [e.strip() for e in custom_effects.split(",")]
                        print_success(f"Custom atmospheric effects set to: {custom_effects}")
                    continue
                    
                if effect_choice == "6":
                    user_prefs.imagen_settings["environment_settings"]["atmospheric_effects"] = []
                    print_success("Atmospheric effects set to None")
                    continue
                    
                effects = {
                    "1": ["fog"],
                    "2": ["mist"],
                    "3": ["rain"],
                    "4": ["snow"]
                }
                
                user_prefs.imagen_settings["environment_settings"]["atmospheric_effects"] = effects[effect_choice]
                print_success(f"Atmospheric effects set to {effects[effect_choice]}")
                continue
                
        elif advanced_choice == "5":
            print_section("Color & Detail Settings")
            print_info("Configure color and detail settings:")
            print_option("1", "Color Scheme")
            print_option("2", "Color Palette")
            print_option("3", "Color Temperature")
            print_option("4", "Texture Quality")
            print_option("5", "Special Effects")
            print_option("6", "Return")
            
            color_choice = get_validated_input("Select option (1-6)", ["1", "2", "3", "4", "5", "6"])
            if color_choice == "6":
                continue
                
            if color_choice == "1":
                print_info("Select color scheme:")
                print_option("1", "Natural")
                print_option("2", "Warm")
                print_option("3", "Cool")
                print_option("4", "Monochromatic")
                print_option("5", "Vibrant")
                print_option("6", "Pastel")
                print_option("7", "Custom")
                print_option("8", "Return")
                
                scheme_choice = get_validated_input("Select color scheme (1-8)", ["1", "2", "3", "4", "5", "6", "7", "8"])
                if scheme_choice == "8":
                    continue
                    
                if scheme_choice == "7":
                    custom_scheme = input("Enter custom color scheme: ").strip()
                    if custom_scheme:
                        user_prefs.imagen_settings["color_settings"]["color_scheme"] = custom_scheme
                        print_success(f"Custom color scheme set to: {custom_scheme}")
                    continue
                    
                schemes = {
                    "1": "natural",
                    "2": "warm",
                    "3": "cool",
                    "4": "monochromatic",
                    "5": "vibrant",
                    "6": "pastel"
                }
                
                user_prefs.imagen_settings["color_settings"]["color_scheme"] = schemes[scheme_choice]
                print_success(f"Color scheme set to {schemes[scheme_choice]}")
                continue
                
            elif color_choice == "2":
                print_info("Select color palette type:")
                print_option("1", "Analogous")
                print_option("2", "Complementary")
                print_option("3", "Triadic")
                print_option("4", "Split Complementary")
                print_option("5", "Custom")
                print_option("6", "Return")
                
                palette_choice = get_validated_input("Select palette type (1-6)", ["1", "2", "3", "4", "5", "6"])
                if palette_choice == "6":
                    continue
                    
                if palette_choice == "5":
                    custom_palette = input("Enter custom palette type: ").strip()
                    if custom_palette:
                        user_prefs.imagen_settings["color_settings"]["palette_type"] = custom_palette
                        print_success(f"Custom palette type set to: {custom_palette}")
                    continue
                    
                palettes = {
                    "1": "analogous",
                    "2": "complementary",
                    "3": "triadic",
                    "4": "split_complementary"
                }
                
                user_prefs.imagen_settings["color_settings"]["palette_type"] = palettes[palette_choice]
                print_success(f"Palette type set to {palettes[palette_choice]}")
                continue
                
            elif color_choice == "3":
                print_info("Select color temperature:")
                print_option("1", "Warm")
                print_option("2", "Cool")
                print_option("3", "Neutral")
                print_option("4", "Custom")
                print_option("5", "Return")
                
                temp_choice = get_validated_input("Select color temperature (1-5)", ["1", "2", "3", "4", "5"])
                if temp_choice == "5":
                    continue
                    
                if temp_choice == "4":
                    custom_temp = input("Enter custom color temperature: ").strip()
                    if custom_temp:
                        user_prefs.imagen_settings["color_settings"]["color_temperature"] = custom_temp
                        print_success(f"Custom color temperature set to: {custom_temp}")
                    continue
                    
                temperatures = {
                    "1": "warm",
                    "2": "cool",
                    "3": "neutral"
                }
                
                user_prefs.imagen_settings["color_settings"]["color_temperature"] = temperatures[temp_choice]
                print_success(f"Color temperature set to {temperatures[temp_choice]}")
                continue
                
            elif color_choice == "4":
                print_info("Select texture quality:")
                print_option("1", "Ultra High")
                print_option("2", "High")
                print_option("3", "Medium")
                print_option("4", "Low")
                print_option("5", "Custom")
                print_option("6", "Return")
                
                texture_choice = get_validated_input("Select texture quality (1-6)", ["1", "2", "3", "4", "5", "6"])
                if texture_choice == "6":
                    continue
                    
                if texture_choice == "5":
                    custom_texture = input("Enter custom texture quality: ").strip()
                    if custom_texture:
                        user_prefs.imagen_settings["detail_settings"]["texture_quality"] = custom_texture
                        print_success(f"Custom texture quality set to: {custom_texture}")
                    continue
                    
                textures = {
                    "1": "ultra_high",
                    "2": "high",
                    "3": "medium",
                    "4": "low"
                }
                
                user_prefs.imagen_settings["detail_settings"]["texture_quality"] = textures[texture_choice]
                print_success(f"Texture quality set to {textures[texture_choice]}")
                continue
                
            elif color_choice == "5":
                print_info("Add special effects (comma-separated):")
                print_option("1", "Bloom")
                print_option("2", "Glow")
                print_option("3", "Motion Blur")
                print_option("4", "Depth of Field")
                print_option("5", "Custom")
                print_option("6", "None")
                print_option("7", "Return")
                
                effect_choice = get_validated_input("Select option (1-7)", ["1", "2", "3", "4", "5", "6", "7"])
                if effect_choice == "7":
                    continue
                    
                if effect_choice == "5":
                    custom_effects = input("Enter custom special effects (comma-separated): ").strip()
                    if custom_effects:
                        user_prefs.imagen_settings["detail_settings"]["special_effects"] = [e.strip() for e in custom_effects.split(",")]
                        print_success(f"Custom special effects set to: {custom_effects}")
                    continue
                    
                if effect_choice == "6":
                    user_prefs.imagen_settings["detail_settings"]["special_effects"] = []
                    print_success("Special effects set to None")
                    continue
                    
                effects = {
                    "1": ["bloom"],
                    "2": ["glow"],
                    "3": ["motion_blur"],
                    "4": ["depth_of_field"]
                }
                
                user_prefs.imagen_settings["detail_settings"]["special_effects"] = effects[effect_choice]
                print_success(f"Special effects set to {effects[effect_choice]}")
                continue
                
        elif advanced_choice == "6":
            print_section("Current Settings")
            print_info("Style & Artistic Settings:")
            print_info(f"- Current Style: {user_prefs.preferred_styles[0] if user_prefs.preferred_styles else 'Not set'}")
            print_info(f"- Art Movement: {user_prefs.imagen_settings['style_settings'].get('art_movement', 'Not set')}")
            print_info(f"- Post-processing: {', '.join(user_prefs.imagen_settings['style_settings'].get('post_processing', [])) or 'None'}")
            
            print_info("\nCamera & Technical Settings:")
            print_info(f"- Camera Model: {user_prefs.imagen_settings['camera_settings'].get('camera_model', 'Not set')}")
            print_info(f"- Lens Type: {user_prefs.imagen_settings['camera_settings'].get('lens_type', 'Not set')}")
            print_info(f"- Aperture: {user_prefs.imagen_settings['camera_settings'].get('aperture', 'Not set')}")
            print_info(f"- Special Lens: {user_prefs.imagen_settings['camera_settings'].get('special_lens', 'None')}")
            print_info(f"- Resolution: {user_prefs.imagen_settings['quality_settings'].get('resolution', 'Not set')}")
            print_info(f"- Detail Level: {user_prefs.imagen_settings['quality_settings'].get('detail_level', 'Not set')}")
            print_info(f"- Rendering Quality: {user_prefs.imagen_settings['quality_settings'].get('rendering_quality', 'Not set')}")
            
            print_info("\nLighting & Atmosphere:")
            print_info(f"- Time of Day: {user_prefs.imagen_settings['lighting_settings'].get('time_of_day', 'Not set')}")
            print_info(f"- Lighting Style: {user_prefs.imagen_settings['lighting_settings'].get('lighting_style', 'Not set')}")
            print_info(f"- Light Quality: {user_prefs.imagen_settings['lighting_settings'].get('light_quality', 'Not set')}")
            print_info(f"- Artificial Sources: {', '.join(user_prefs.imagen_settings['lighting_settings'].get('artificial_sources', [])) or 'None'}")
            
            print_info("\nComposition & Environment:")
            print_info(f"- Composition Technique: {user_prefs.imagen_settings['composition_settings'].get('technique', 'Not set')}")
            print_info(f"- Camera Angle: {user_prefs.imagen_settings['composition_settings'].get('camera_angle', 'Not set')}")
            print_info(f"- Perspective: {user_prefs.imagen_settings['composition_settings'].get('perspective', 'Not set')}")
            print_info(f"- Weather: {user_prefs.imagen_settings['environment_settings'].get('weather', 'Not set')}")
            print_info(f"- Season: {user_prefs.imagen_settings['environment_settings'].get('season', 'Not set')}")
            print_info(f"- Atmospheric Effects: {', '.join(user_prefs.imagen_settings['environment_settings'].get('atmospheric_effects', [])) or 'None'}")
            
            print_info("\nColor & Detail Settings:")
            print_info(f"- Color Scheme: {user_prefs.imagen_settings['color_settings'].get('color_scheme', 'Not set')}")
            print_info(f"- Palette Type: {user_prefs.imagen_settings['color_settings'].get('palette_type', 'Not set')}")
            print_info(f"- Color Temperature: {user_prefs.imagen_settings['color_settings'].get('color_temperature', 'Not set')}")
            print_info(f"- Texture Quality: {user_prefs.imagen_settings['detail_settings'].get('texture_quality', 'Not set')}")
            print_info(f"- Special Effects: {', '.join(user_prefs.imagen_settings['detail_settings'].get('special_effects', [])) or 'None'}")
            
        elif advanced_choice == "7":
            print_section("Customize All Parameters")
            print_info("Enter custom values for all parameters (leave blank to keep current):")
            
            # Style & Artistic Settings
            custom_style = input("Custom style: ").strip()
            if custom_style:
                user_prefs.preferred_styles = [custom_style]
            
            custom_movement = input("Custom art movement: ").strip()
            if custom_movement:
                user_prefs.imagen_settings["style_settings"]["art_movement"] = custom_movement
            
            custom_processing = input("Custom post-processing effects (comma-separated): ").strip()
            if custom_processing:
                user_prefs.imagen_settings["style_settings"]["post_processing"] = [e.strip() for e in custom_processing.split(",")]
            
            # Camera & Technical Settings
            custom_camera = input("Custom camera model: ").strip()
            if custom_camera:
                user_prefs.imagen_settings["camera_settings"]["camera_model"] = custom_camera
            
            custom_lens = input("Custom lens type: ").strip()
            if custom_lens:
                user_prefs.imagen_settings["camera_settings"]["lens_type"] = custom_lens
            
            custom_aperture = input("Custom aperture: ").strip()
            if custom_aperture:
                user_prefs.imagen_settings["camera_settings"]["aperture"] = custom_aperture
            
            custom_special_lens = input("Custom special lens: ").strip()
            if custom_special_lens:
                user_prefs.imagen_settings["camera_settings"]["special_lens"] = custom_special_lens
            
            custom_resolution = input("Custom resolution: ").strip()
            if custom_resolution:
                user_prefs.imagen_settings["quality_settings"]["resolution"] = custom_resolution
            
            custom_detail = input("Custom detail level: ").strip()
            if custom_detail:
                user_prefs.imagen_settings["quality_settings"]["detail_level"] = custom_detail
            
            custom_render = input("Custom rendering quality: ").strip()
            if custom_render:
                user_prefs.imagen_settings["quality_settings"]["rendering_quality"] = custom_render
            
            # Lighting & Atmosphere
            custom_time = input("Custom time of day: ").strip()
            if custom_time:
                user_prefs.imagen_settings["lighting_settings"]["time_of_day"] = custom_time
            
            custom_light_style = input("Custom lighting style: ").strip()
            if custom_light_style:
                user_prefs.imagen_settings["lighting_settings"]["lighting_style"] = custom_light_style
            
            custom_light_quality = input("Custom light quality: ").strip()
            if custom_light_quality:
                user_prefs.imagen_settings["lighting_settings"]["light_quality"] = custom_light_quality
            
            custom_sources = input("Custom artificial light sources (comma-separated): ").strip()
            if custom_sources:
                user_prefs.imagen_settings["lighting_settings"]["artificial_sources"] = [s.strip() for s in custom_sources.split(",")]
            
            # Composition & Environment
            custom_technique = input("Custom composition technique: ").strip()
            if custom_technique:
                user_prefs.imagen_settings["composition_settings"]["technique"] = custom_technique
            
            custom_angle = input("Custom camera angle: ").strip()
            if custom_angle:
                user_prefs.imagen_settings["composition_settings"]["camera_angle"] = custom_angle
            
            custom_perspective = input("Custom perspective: ").strip()
            if custom_perspective:
                user_prefs.imagen_settings["composition_settings"]["perspective"] = custom_perspective
            
            custom_weather = input("Custom weather: ").strip()
            if custom_weather:
                user_prefs.imagen_settings["environment_settings"]["weather"] = custom_weather
            
            custom_season = input("Custom season: ").strip()
            if custom_season:
                user_prefs.imagen_settings["environment_settings"]["season"] = custom_season
            
            custom_atmospheric = input("Custom atmospheric effects (comma-separated): ").strip()
            if custom_atmospheric:
                user_prefs.imagen_settings["environment_settings"]["atmospheric_effects"] = [e.strip() for e in custom_atmospheric.split(",")]
            
            # Color & Detail Settings
            custom_scheme = input("Custom color scheme: ").strip()
            if custom_scheme:
                user_prefs.imagen_settings["color_settings"]["color_scheme"] = custom_scheme
            
            custom_palette = input("Custom palette type: ").strip()
            if custom_palette:
                user_prefs.imagen_settings["color_settings"]["palette_type"] = custom_palette
            
            custom_temp = input("Custom color temperature: ").strip()
            if custom_temp:
                user_prefs.imagen_settings["color_settings"]["color_temperature"] = custom_temp
            
            custom_texture = input("Custom texture quality: ").strip()
            if custom_texture:
                user_prefs.imagen_settings["detail_settings"]["texture_quality"] = custom_texture
            
            custom_effects = input("Custom special effects (comma-separated): ").strip()
            if custom_effects:
                user_prefs.imagen_settings["detail_settings"]["special_effects"] = [e.strip() for e in custom_effects.split(",")]
            
            print_success("All custom parameters updated")
            
        elif advanced_choice == "8":
            break
            
        user_prefs.save_preferences()

class GenerationHistory:
    """Class to manage the history of generated images."""
    
    def __init__(self, history_file="generation_history.json"):
        """Initialize the history object."""
        self.history = []
        # Use absolute path for history file
        if not os.path.isabs(history_file):
            self.history_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), history_file)
        else:
            self.history_file = history_file
        logging.info(f"Generation history file path: {self.history_file}")
        self.load_history()
    
    def load_history(self):
        """Load history from file."""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.history = data
                    else:
                        logging.error(f"Invalid history format in {self.history_file}")
                        self.history = []
                logging.info(f"Loaded {len(self.history)} history entries")
            else:
                logging.info(f"No history file found at {self.history_file}, creating new history")
                self.history = []
        except Exception as e:
            logging.error(f"Error loading history: {e}")
            self.history = []
    
    def save_history(self):
        """Save history to file."""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=4)
            logging.info(f"Saved {len(self.history)} history entries to {self.history_file}")
            # Verify the file was saved correctly
            if os.path.exists(self.history_file):
                logging.info(f"Verified history file exists at {self.history_file}")
            else:
                logging.error(f"Failed to save history file at {self.history_file}")
        except Exception as e:
            logging.error(f"Error saving history: {e}")
            # Try to save to a fallback location
            try:
                fallback_path = "generation_history_fallback.json"
                with open(fallback_path, 'w') as f:
                    json.dump(self.history, f, indent=4)
                logging.info(f"Saved history to fallback location: {fallback_path}")
            except Exception as fallback_e:
                logging.error(f"Error saving to fallback location: {fallback_e}")
    
    def add_entry(self, entry_data):
        """Add a new generation entry to history."""
        try:
            # Get the image filename if we have an enhanced prompt
            image_filename = None
            if entry_data.get("enhanced_prompt"):
                image_path = get_generated_image_path(entry_data["enhanced_prompt"])
                image_filename = os.path.basename(image_path)
                logging.info(f"Adding history entry with image filename: {image_filename}")
            
            entry = {
                "date": datetime.now().isoformat(),
                "prompt": entry_data.get("prompt", ""),
                "enhanced_prompt": entry_data.get("enhanced_prompt", ""),
                "gemini_prompt": entry_data.get("gemini_prompt", ""),
                "image_filename": image_filename,
                "settings": {
                    "user_preferences": entry_data.get("user_preferences", {}),
                    "imagen_settings": entry_data.get("imagen_settings", {}),
                    "wallpaper_settings": entry_data.get("wallpaper_settings", {})
                },
                "output": entry_data.get("output", "")
            }
            
            # Insert at beginning to show most recent first
            self.history.insert(0, entry)
            self.history = self.history[:50]  # Keep only last 50 entries
            
            # Save immediately to ensure it's persisted
            self.save_history()
            logging.info(f"Added entry to history, current count: {len(self.history)}")
        except Exception as e:
            logging.error(f"Error adding entry to history: {e}")
            # Try to save anyway in case it's just the add_entry logic that failed
            try:
                self.save_history()
            except:
                pass

    def view_history(self):
        """Display the generation history in a formatted way."""
        try:
            if not self.history:
                print("\nℹ No generation history available.")
                return

            for i, entry in enumerate(self.history, 1):
                print(f"\nGeneration #{i}")
                print("-" * 13)
                
                # Always show date and original prompt
                print(f"Date: {entry.get('date', 'Not recorded')}")
                print(f"Original Prompt: {entry.get('prompt', 'Not recorded')}")
                
                # Only show enhanced prompt if it exists and is different from original
                if entry.get('enhanced_prompt') and entry['enhanced_prompt'] != entry.get('prompt'):
                    print(f"Enhanced Prompt: {entry['enhanced_prompt']}")
                
                # Only show Gemini prompt if it exists and is different from original
                if entry.get('gemini_prompt') and entry['gemini_prompt'] != entry.get('prompt'):
                    print(f"Gemini Prompt: {entry['gemini_prompt']}")
                
                # Show settings if they exist
                if entry.get('settings'):
                    print("\nSettings Used:")
                    settings = entry['settings']
                    
                    # User preferences
                    if settings.get('user_preferences'):
                        print("User Preferences:")
                        for key, value in settings['user_preferences'].items():
                            if value:  # Only show non-empty values
                                print(f"  {key}: {value}")
                    
                    # Imagen settings
                    if settings.get('imagen_settings'):
                        print("\nImagen Settings:")
                        for key, value in settings['imagen_settings'].items():
                            if value is not None:  # Show even if False
                                print(f"  {key}: {value}")
                    
                    # Wallpaper settings
                    if settings.get('wallpaper_settings'):
                        print("\nWallpaper Settings:")
                        for key, value in settings['wallpaper_settings'].items():
                            if value is not None:  # Show even if False
                                print(f"  {key}: {value}")
                
                # Show the image file if available
                if entry.get('image_filename'):
                    image_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "genimage", entry['image_filename'])
                    print(f"\nImage Filename: {entry['image_filename']}")
                    
                    # Check if the file exists
                    if os.path.exists(image_file):
                        print(f"Image exists at: {image_file}")
                    else:
                        print(f"⚠️ Image file not found at expected location: {image_file}")
                        
                        # Try to find the file
                        basename = entry['image_filename']
                        home_dir = os.path.expanduser("~")
                        possible_home_path = os.path.join(home_dir, basename)
                        
                        if os.path.exists(possible_home_path):
                            print(f"✓ Found image in home directory: {possible_home_path}")
                elif entry.get('enhanced_prompt'):
                    # Fallback for entries created before this feature was added
                    image_path = get_generated_image_path(entry['enhanced_prompt'])
                    if os.path.exists(image_path):
                        print(f"\nImage Filename: {os.path.basename(image_path)}")
                        print(f"Image exists at: {image_path}")
                
                print("-" * 40)
        except Exception as e:
            logging.error(f"Error displaying history: {e}")
            print(f"Error displaying history: {e}")

# Initialize history at module level
generation_history = GenerationHistory()

def generate_wallpaper(prompt_type=None, custom_prompt=None, mood=None, style=None, resolution=None, color_scheme=None, lighting=None):
    """Generate wallpaper based on given parameters."""
    global generation_history, user_prefs
    
    # Create settings dictionary with all necessary parameters
    current_settings = {
        "prompt_type": prompt_type,
        "custom_prompt": custom_prompt,
        "mood": mood,
        "style": style,
        "resolution": resolution,
        "color_scheme": color_scheme,
        "lighting": lighting,
        "imagen_settings": user_prefs.imagen_settings.copy(),
        "wallpaper_settings": user_prefs.wallpaper_settings.copy()
    }
    
    enhanced_prompt = None
    gemini_prompt = None
    
    # Step 1: Generate or get the prompt
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
    
    # Add to generation history
    generation_history.add_entry({
        "prompt": custom_prompt if custom_prompt else gemini_prompt,
        "enhanced_prompt": enhanced_prompt,
        "gemini_prompt": gemini_prompt,
        "user_preferences": user_prefs.__dict__,
        "imagen_settings": user_prefs.imagen_settings,
        "wallpaper_settings": user_prefs.wallpaper_settings,
        "output": None  # Will be updated when image is generated
    })
    
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
    
    # Step 3: Generate the image
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
        print_info(f"Image will be saved as: {os.path.basename(cache_path)}")
        
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
                # Create generation config with supported parameters
                config = types.GenerateImagesConfig(
                    number_of_images=user_prefs.imagen_settings["number_of_images"],
                    aspect_ratio=aspect_ratio
                )
                
                # Add seed if specified
                if user_prefs.imagen_settings["seed"] is not None:
                    config.seed = user_prefs.imagen_settings["seed"]
                
                # Add negative prompt if specified
                if user_prefs.imagen_settings["negative_prompt"]:
                    config.negative_prompt = user_prefs.imagen_settings["negative_prompt"]
                
                response = client.models.generate_images(
                    model='imagen-3.0-generate-002',
                    prompt=enhanced_prompt,
                    config=config
                )
                
                if response and hasattr(response, 'generated_images'):
                    if response.generated_images:
                        for i, generated_image in enumerate(response.generated_images):
                            # Create temp file with absolute path in project directory
                            temp_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"generated_image_{i}.png")
                            with open(temp_image_path, "wb") as f:
                                f.write(generated_image.image.image_bytes)
                        
                        # Log the paths being used
                        logging.info(f"Temporary image path: {temp_image_path}")
                        logging.info(f"Target cache path: {cache_path}")
                        
                        # Make sure the directory exists using absolute path
                        cache_dir = os.path.dirname(os.path.abspath(cache_path))
                        os.makedirs(cache_dir, exist_ok=True)
                        logging.info(f"Ensuring cache directory exists: {cache_dir}")
                        
                        try:
                            # Copy instead of rename to avoid issues with files being in different filesystems
                            shutil.copy2(temp_image_path, cache_path)
                            
                            # Verify the file was copied correctly
                            if os.path.exists(cache_path):
                                print_success(f"Image generated and saved as: {os.path.basename(cache_path)}")
                                logging.info(f"Image successfully saved to: {cache_path}")
                                
                                # Update generation history with the image filename
                                if generation_history.history and len(generation_history.history) > 0:
                                    filename = os.path.basename(cache_path)
                                    generation_history.history[0]["image_filename"] = filename
                                    logging.info(f"Updating history with image filename: {filename}")
                                    generation_history.save_history()
                                
                                # Remove the temporary file after successful copy
                                try:
                                    os.remove(temp_image_path)
                                    logging.info(f"Temporary file removed: {temp_image_path}")
                                except Exception as e:
                                    # Non-critical error, just log it
                                    logging.warning(f"Could not remove temporary file {temp_image_path}: {e}")
                            else:
                                print_warning(f"Image was generated but may not have been saved properly to {cache_path}")
                                logging.error(f"Failed to save image to {cache_path}, file does not exist after copy")
                                # Keep the temp file as a backup
                                print_info(f"Temporary file preserved at {temp_image_path}")
                        except Exception as e:
                            print_warning(f"Error saving image to final location: {e}")
                            logging.error(f"Exception while saving image to {cache_path}: {e}")
                            print_info(f"Temporary file preserved at {temp_image_path}")
                            # Use the temp file as the cache path
                            cache_path = temp_image_path
                    else:
                        print_error("Failed to generate image - no images returned")
                        logging.error(f"Empty response from Imagen 3 for prompt: {enhanced_prompt}")
                        return False
                else:
                    print_error("Failed to generate image - invalid response format")
                    logging.error(f"Invalid response format from Imagen 3: {response}")
                    return False
            except AttributeError as e:
                print_error(f"Error with Gemini client: {e}")
                print_info("This might be due to an API version mismatch. Check your google-generativeai package version.")
                return False
    except Exception as e:
        print_error(f"Error generating image: {e}")
        return False
    
    # Step 4: Set the wallpaper
    try:
        print_section("Setting Wallpaper")
        print_info("Applying your new wallpaper...")
        show_spinner("Configuring desktop settings...", 1)
        
        # Make sure we're using an absolute path
        if not os.path.isabs(cache_path):
            cache_path = os.path.abspath(cache_path)
        
        logging.info(f"Setting wallpaper with path: {cache_path}")
        
        # Make sure the file exists before setting it
        if not os.path.exists(cache_path):
            logging.warning(f"Wallpaper file not found at {cache_path} before setting")
            print_warning(f"Wallpaper file may be missing: {cache_path}")
        
        result = set_wallpaper(cache_path)
        if result:
            print_success("Wallpaper successfully applied!")
            print_info(f"Your desktop is now displaying: {os.path.basename(cache_path)}")
            logging.info(f"Wallpaper successfully set to: {cache_path}")
            
            # Update the generation history with the correct image file path
            # First, find the most recent entry which should be the one for this generation
            if generation_history.history and len(generation_history.history) > 0:
                # Update the most recent entry with the correct image filename
                filename = os.path.basename(cache_path)
                generation_history.history[0]["image_filename"] = filename
                logging.info(f"Updated history entry with image filename: {filename}")
                
                # Save the history to ensure the image filename is recorded
                generation_history.save_history()
                
                # Make sure the file really exists in genimage
                if not os.path.exists(cache_path):
                    print_warning("Image file not found in expected location, attempting to recreate it")
                    logging.warning(f"Image file not found at {cache_path} after setting wallpaper")
                    
                    # The wallpaper might have been saved to the home directory instead of project directory
                    basename = os.path.basename(cache_path)
                    home_dir = os.path.expanduser("~")
                    possible_home_path = os.path.join(home_dir, basename)
                    
                    if os.path.exists(possible_home_path):
                        print_success(f"Found the image file in home directory: {possible_home_path}")
                        logging.info(f"Found missing image file in home directory: {possible_home_path}")
                        try:
                            # Ensure the genimage directory exists
                            genimage_dir = os.path.dirname(cache_path)
                            os.makedirs(genimage_dir, exist_ok=True)
                            
                            # Copy the file to the genimage directory
                            shutil.copy2(possible_home_path, cache_path)
                            print_success(f"Successfully copied the file to project location: {cache_path}")
                            logging.info(f"Copied file from {possible_home_path} to {cache_path}")
                        except Exception as e:
                            print_warning(f"Error copying file from home directory: {e}")
                            logging.error(f"Error copying file from {possible_home_path} to {cache_path}: {e}")
                    else:
                        # This extensive search might be needed but is expensive, so log it
                        logging.info(f"Image not found in home directory, starting deeper search for {basename}")
                        # Search for the file in the home directory
                        found_file = None
                        
                        try:
                            # Search in common locations
                            common_dirs = [
                                home_dir,
                                os.path.join(home_dir, "Downloads"),
                                os.path.join(home_dir, "Pictures"),
                                "/tmp",
                                "."
                            ]
                            
                            for directory in common_dirs:
                                if os.path.exists(os.path.join(directory, basename)):
                                    found_file = os.path.join(directory, basename)
                                    print_success(f"Found the image file at: {found_file}")
                                    break
                            
                            # More extensive search if needed
                            if not found_file:
                                for directory in common_dirs:
                                    for root, dirs, files in os.walk(directory, topdown=True):
                                        # Skip hidden directories and large system directories
                                        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['.cache', '.local']]
                                        
                                        if basename in files:
                                            found_file = os.path.join(root, basename)
                                            print_success(f"Found the image file at: {found_file}")
                                            break
                                    
                                    if found_file:
                                        break
                                        
                                    # Limit search depth for performance
                                    if directory == home_dir:
                                        break
                            
                            if found_file:
                                # Ensure the genimage directory exists
                                os.makedirs(os.path.dirname(cache_path), exist_ok=True)
                                
                                # Copy the file to the genimage directory
                                shutil.copy2(found_file, cache_path)
                                print_success(f"Successfully copied the file to: {cache_path}")
                            else:
                                print_warning("Image file not found in common locations, please check manually.")
                        except Exception as e:
                            print_warning(f"Error while searching for the file: {e}")
                    
                    # This shouldn't happen, but if it does, ensure the directory exists
                    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            
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

def manage_preferences():
    """Manage user preferences for wallpaper generation."""
    print_header("Wallpaper Preferences")
    
    while True:
        print_section("Options")
        print_option("1", "Manage Genres")
        print_option("2", "Manage Styles")
        print_option("3", "Manage Moods")
        print_option("4", "Manage Wallpaper Settings")
        print_option("5", "View Current Preferences")
        print_option("6", "Reset to Defaults")
        print_option("7", "Return to Main Menu")
                
        choice = get_validated_input("Select an option (1-7)", ["1", "2", "3", "4", "5", "6", "7"])
        
        if choice == "1":
            print_section("Manage Genres")
            print_info("Current preferred genres:")
            for genre in user_prefs.preferred_genres:
                print_info(f"- {genre}")
            
            print_info("\nAvailable genres:")
            for i, genre in enumerate(available_genres, 1):
                print_option(str(i), genre)
            
            print_option("a", "Add genre")
            print_option("r", "Remove genre")
            print_option("c", "Clear all")
            print_option("b", "Back")
            
            action = get_validated_input("Select action", ["a", "r", "c", "b"] + [str(i) for i in range(1, len(available_genres) + 1)])
            
            if action == "a":
                genre = input("Enter genre to add: ").strip()
                if genre in available_genres and genre not in user_prefs.preferred_genres:
                    user_prefs.preferred_genres.append(genre)
                    print_success(f"Added genre: {genre}")
                else:
                    print_warning("Invalid genre or already in preferences")
            elif action == "r":
                if user_prefs.preferred_genres:
                    print_info("Select genre to remove:")
                    for i, genre in enumerate(user_prefs.preferred_genres, 1):
                        print_option(str(i), genre)
                    idx = int(get_validated_input("Enter number", [str(i) for i in range(1, len(user_prefs.preferred_genres) + 1)])) - 1
                    removed = user_prefs.preferred_genres.pop(idx)
                    print_success(f"Removed genre: {removed}")
                else:
                    print_warning("No genres to remove")
            elif action == "c":
                user_prefs.preferred_genres.clear()
                print_success("Cleared all genres")
            elif action == "b":
                continue
            else:
                idx = int(action) - 1
                if 0 <= idx < len(available_genres):
                    genre = available_genres[idx]
                    if genre not in user_prefs.preferred_genres:
                        user_prefs.preferred_genres.append(genre)
                        print_success(f"Added genre: {genre}")
                    else:
                        print_warning("Genre already in preferences")
        
        elif choice == "2":
            print_section("Manage Styles")
            print_info("Current preferred styles:")
            for style in user_prefs.preferred_styles:
                print_info(f"- {style}")
            
            print_info("\nAvailable styles:")
            style_options = ["abstract", "anime", "art_deco", "art_nouveau", "cartoon", "charcoal", 
                           "cinematic", "comic_book", "constructivism", "cubism", "cyberpunk", 
                           "digital_art", "divisionism", "double_exposure", "expressionism", 
                           "fantasy", "futurism", "glitch_art", "gothic", "graffiti", 
                           "hyperrealism", "impressionism", "ink_drawing", "isometric", "landscape", 
                           "line_art", "low_poly", "manga", "minimalist", "oil_painting", 
                           "paper_cut", "pastel", "pencil_sketch", "photograph", "pixel_art", 
                           "pointillism", "pop_art", "realism", "retrowave", "sci_fi", 
                           "sketch", "stained_glass", "steampunk", "surrealism", "ukiyo_e", 
                           "vaporwave", "watercolor", "woodcut"]
            
            # Group styles by compatibility for random mixing
            style_categories = {
                "traditional_art": ["art_deco", "art_nouveau", "charcoal", "expressionism", 
                                   "gothic", "impressionism", "oil_painting", "pastel", 
                                   "pencil_sketch", "realism", "sketch", "watercolor", "woodcut"],
                "digital_art": ["abstract", "cinematic", "cyberpunk", "digital_art", "double_exposure", 
                               "fantasy", "futurism", "glitch_art", "hyperrealism", "isometric", 
                               "landscape", "low_poly", "minimalist", "retrowave", "sci_fi",
                               "stained_glass", "steampunk", "surrealism", "vaporwave"],
                "illustration": ["anime", "cartoon", "comic_book", "divisionism", "graffiti", 
                                "ink_drawing", "line_art", "manga", "paper_cut", "pixel_art", 
                                "pointillism", "pop_art", "ukiyo_e"]
            }
            
            def generate_random_style_mix():
                # Select a random category
                category = random.choice(list(style_categories.keys()))
                # Select 2-3 compatible styles from the same category
                num_styles = random.randint(2, 3)
                available_styles = style_categories[category]
                if len(available_styles) < num_styles:
                    num_styles = len(available_styles)
                selected_styles = random.sample(available_styles, num_styles)
                return " + ".join(selected_styles)
            
            for i, style in enumerate(style_options, 1):
                print_option(str(i), style)
            
            print_option(str(len(style_options) + 1), "Random Style Mix (combines 2-3 compatible styles)")
            print_option("a", "Add style")
            print_option("r", "Remove style")
            print_option("c", "Clear all")
            print_option("b", "Back")
            
            style_choice = get_validated_input("Select an option", 
                                              [str(i) for i in range(1, len(style_options) + 2)] + ["a", "r", "c", "b"])
            
            if style_choice == "b":
                return
            elif style_choice == "a":
                style = input("Enter style to add: ").strip()
                if style:
                    if style not in user_prefs.preferred_styles:
                        user_prefs.preferred_styles.append(style)
                        user_prefs.save_preferences()
                        print_success(f"Added '{style}' to preferred styles")
                    else:
                        print_warning(f"'{style}' is already in your preferred styles")
            elif style_choice == "r":
                if not user_prefs.preferred_styles:
                    print_warning("You don't have any preferred styles to remove")
                    continue
                
                print_info("Select style to remove:")
                for i, style in enumerate(user_prefs.preferred_styles, 1):
                    print_option(str(i), style)
                
                remove_choice = get_validated_input("Select style to remove (or 'c' to cancel)", 
                                                   [str(i) for i in range(1, len(user_prefs.preferred_styles) + 1)] + ["c"])
                
                if remove_choice == "c":
                    continue
                
                style_to_remove = user_prefs.preferred_styles[int(remove_choice) - 1]
                user_prefs.preferred_styles.remove(style_to_remove)
                user_prefs.save_preferences()
                print_success(f"Removed '{style_to_remove}' from preferred styles")
            elif style_choice == "c":
                confirm = get_validated_input("Are you sure you want to clear all styles? (y/n)", ["y", "n"])
                if confirm == "y":
                    user_prefs.preferred_styles.clear()
                    user_prefs.save_preferences()
                    print_success("Cleared all preferred styles")
            elif style_choice == str(len(style_options) + 1):
                # Random style mix option
                style_mix = generate_random_style_mix()
                print_info(f"Generated random style mix: {style_mix}")
                add_to_preferences = get_validated_input("Add this mix to your preferred styles? (y/n)", ["y", "n"])
                if add_to_preferences == "y":
                    if style_mix not in user_prefs.preferred_styles:
                        user_prefs.preferred_styles.append(style_mix)
                        user_prefs.save_preferences()
                        print_success(f"Added '{style_mix}' to preferred styles")
                    else:
                        print_warning(f"'{style_mix}' is already in your preferred styles")
            else:
                # Add the selected style from the list
                try:
                    selected_style = style_options[int(style_choice) - 1]
                    if selected_style not in user_prefs.preferred_styles:
                        user_prefs.preferred_styles.append(selected_style)
                        user_prefs.save_preferences()
                        print_success(f"Added '{selected_style}' to preferred styles")
                    else:
                        print_warning(f"'{selected_style}' is already in your preferred styles")
                except (ValueError, IndexError):
                    print_error(f"Invalid selection: {style_choice}")
        
        elif choice == "3":
            print_section("Manage Moods")
            print_info("Current preferred moods:")
            for mood in user_prefs.preferred_moods:
                print_info(f"- {mood}")
            
            print_info("\nAvailable moods:")
            mood_options = ["peaceful", "dramatic", "mysterious", "energetic", "melancholic",
                          "joyful", "romantic", "eerie", "nostalgic", "contemplative"]
            for i, mood in enumerate(mood_options, 1):
                print_option(str(i), mood)
            
            print_option("a", "Add mood")
            print_option("r", "Remove mood")
            print_option("c", "Clear all")
            print_option("b", "Back")
            
            action = get_validated_input("Select action", ["a", "r", "c", "b"] + [str(i) for i in range(1, len(mood_options) + 1)])
            
            if action == "a":
                mood = input("Enter mood to add: ").strip()
                if mood in mood_options and mood not in user_prefs.preferred_moods:
                    user_prefs.preferred_moods.append(mood)
                    print_success(f"Added mood: {mood}")
                else:
                    print_warning("Invalid mood or already in preferences")
            elif action == "r":
                if user_prefs.preferred_moods:
                    print_info("Select mood to remove:")
                    for i, mood in enumerate(user_prefs.preferred_moods, 1):
                        print_option(str(i), mood)
                    idx = int(get_validated_input("Enter number", [str(i) for i in range(1, len(user_prefs.preferred_moods) + 1)])) - 1
                    removed = user_prefs.preferred_moods.pop(idx)
                    print_success(f"Removed mood: {removed}")
                else:
                    print_warning("No moods to remove")
            elif action == "c":
                user_prefs.preferred_moods.clear()
                print_success("Cleared all moods")
            elif action == "b":
                continue
            else:
                idx = int(action) - 1
                if 0 <= idx < len(mood_options):
                    mood = mood_options[idx]
                    if mood not in user_prefs.preferred_moods:
                        user_prefs.preferred_moods.append(mood)
                        print_success(f"Added mood: {mood}")
                    else:
                        print_warning("Mood already in preferences")
        
        elif choice == "4":
            print_section("Wallpaper Settings")
            print_option("1", "Auto-set wallpaper")
            print_option("2", "Cache duration")
            print_option("3", "Fit mode")
            print_option("4", "Background color")
            print_option("5", "Multi-monitor mode")
            print_option("6", "Refresh rate")
            print_option("7", "Back")
            
            setting_choice = get_validated_input("Select setting to configure (1-7)", ["1", "2", "3", "4", "5", "6", "7"])
            
            if setting_choice == "1":
                print_info("Auto-set wallpaper after generation")
                print_option("1", "Enabled")
                print_option("2", "Disabled")
                auto_set = get_validated_input("Select option (1-2)", ["1", "2"])
                user_prefs.wallpaper_settings["auto_set"] = (auto_set == "1")
                print_success(f"Auto-set wallpaper {'enabled' if user_prefs.wallpaper_settings['auto_set'] else 'disabled'}")
            
            elif setting_choice == "2":
                print_info("Set cache duration (days)")
                try:
                    days = int(input("Enter number of days (1-365): ").strip())
                    days = max(1, min(365, days))
                    user_prefs.wallpaper_settings["cache_duration"] = days
                    print_success(f"Cache duration set to {days} days")
                except ValueError:
                    print_warning("Invalid input. Using default value.")
            
            elif setting_choice == "3":
                print_info("Select wallpaper fit mode")
                print_option("1", "Fill (stretch to fill)")
                print_option("2", "Fit (maintain aspect ratio)")
                print_option("3", "Center (no scaling)")
                print_option("4", "Tile (repeat pattern)")
                fit_mode = get_validated_input("Select option (1-4)", ["1", "2", "3", "4"])
                modes = ["fill", "fit", "center", "tile"]
                user_prefs.wallpaper_settings["fit_mode"] = modes[int(fit_mode) - 1]
                print_success(f"Fit mode set to {user_prefs.wallpaper_settings['fit_mode']}")
            
            elif setting_choice == "4":
                print_info("Set background color (hex format)")
                print_info("Example: #000000 for black")
                color = input("Enter hex color code: ").strip()
                if color.startswith("#") and len(color) == 7:
                    try:
                        int(color[1:], 16)  # Validate hex
                        user_prefs.wallpaper_settings["background_color"] = color
                        print_success(f"Background color set to {color}")
                    except ValueError:
                        print_warning("Invalid hex color code")
                else:
                    print_warning("Invalid color format")
            
            elif setting_choice == "5":
                print_info("Select multi-monitor mode")
                print_option("1", "Mirror (same wallpaper on all monitors)")
                print_option("2", "Extend (different wallpapers)")
                print_option("3", "Individual (customize per monitor)")
                monitor_mode = get_validated_input("Select option (1-3)", ["1", "2", "3"])
                modes = ["mirror", "extend", "individual"]
                user_prefs.wallpaper_settings["multi_monitor"] = modes[int(monitor_mode) - 1]
                print_success(f"Multi-monitor mode set to {user_prefs.wallpaper_settings['multi_monitor']}")
            
            elif setting_choice == "6":
                print_info("Select wallpaper refresh rate")
                print_option("1", "Daily")
                print_option("2", "Weekly")
                print_option("3", "Monthly")
                print_option("4", "Never")
                refresh_rate = get_validated_input("Select option (1-4)", ["1", "2", "3", "4"])
                rates = ["daily", "weekly", "monthly", "never"]
                user_prefs.wallpaper_settings["refresh_rate"] = rates[int(refresh_rate) - 1]
                print_success(f"Refresh rate set to {user_prefs.wallpaper_settings['refresh_rate']}")
        
        elif choice == "5":
            print_section("Current Preferences")
            print_info("Preferred Genres:")
            for genre in user_prefs.preferred_genres:
                print_info(f"- {genre}")
            
            print_info("\nPreferred Styles:")
            for style in user_prefs.preferred_styles:
                print_info(f"- {style}")
            
            print_info("\nPreferred Moods:")
            for mood in user_prefs.preferred_moods:
                print_info(f"- {mood}")
            
            print_info("\nWallpaper Settings:")
            print_info(f"- Auto-set: {'Enabled' if user_prefs.wallpaper_settings['auto_set'] else 'Disabled'}")
            print_info(f"- Cache Duration: {user_prefs.wallpaper_settings['cache_duration']} days")
            print_info(f"- Fit Mode: {user_prefs.wallpaper_settings['fit_mode']}")
            print_info(f"- Background Color: {user_prefs.wallpaper_settings['background_color']}")
            print_info(f"- Multi-monitor Mode: {user_prefs.wallpaper_settings['multi_monitor']}")
            print_info(f"- Refresh Rate: {user_prefs.wallpaper_settings['refresh_rate']}")
        
        elif choice == "6":
            print_section("Reset to Defaults")
            confirm = get_validated_input("Are you sure you want to reset all preferences? (yes/no)", ["yes", "no"])
            if confirm == "yes":
                user_prefs.preferred_genres = []
                user_prefs.preferred_styles = ["photograph"]  # Default to photograph style
                user_prefs.preferred_moods = []
                user_prefs.aspect_ratio = "16:9"
                user_prefs.negative_prompts = []
                user_prefs.imagen_settings = {
                    "number_of_images": 1,
                    "seed": None,
                    "aspect_ratio": "16:9",
                    "negative_prompt": "",
                    "color_scheme": "natural",
                    "lighting": "natural",
                    "composition": "rule_of_thirds",
                    "depth_of_field": "medium"
                }
                user_prefs.wallpaper_settings = {
                    "auto_set": True,
                    "cache_duration": 30,
                    "fit_mode": "fill",
                    "background_color": "#000000",
                    "multi_monitor": "mirror",
                    "refresh_rate": "daily",
                    "last_refresh": None
                }
                user_prefs.save_preferences()
                print_success("All preferences reset to defaults")
        
        elif choice == "7":
            break
        
        user_prefs.save_preferences()

def manage_presets():
    """Manage generation presets."""
    while True:
        print_section("Manage Presets")
        
        # Show current preset if one is loaded
        current_preset = getattr(user_prefs, 'current_preset', None)
        if current_preset:
            print_info(f"Current Preset: {current_preset}")
        print()
        
        print_option("1", "Save Current Settings as Preset")
        print_option("2", "Load Preset")
        print_option("3", "Delete Preset")
        print_option("4", "View Current Preset Details")
        print_option("5", "Back to Main Menu")
        
        choice = get_validated_input("Select option (1-5)", ["1", "2", "3", "4", "5"])
        
        if choice == "1":
            # Get preset name from user
            preset_name = get_validated_input("Enter preset name (or 'b' to go back)", allow_empty=False)
            if preset_name.lower() == 'b':
                continue
                
            # Validate preset name
            if not preset_name.strip() or any(c in r'\/:*?"<>|' for c in preset_name):
                print_error("Invalid preset name. Please avoid special characters.")
                continue
                
            # Check if preset already exists
            if os.path.exists(os.path.join("presets", f"{preset_name}.json")):
                confirm = get_validated_input(f"Preset '{preset_name}' already exists. Overwrite? (y/n)", ["y", "n"])
                if confirm.lower() != "y":
                    continue
            
            try:
                # Collect current settings
                current_settings = {
                    "imagen_settings": user_prefs.imagen_settings if hasattr(user_prefs, 'imagen_settings') else {},
                    "wallpaper_settings": user_prefs.wallpaper_settings if hasattr(user_prefs, 'wallpaper_settings') else {},
                    "metadata": {
                        "created_at": datetime.now().isoformat(),
                        "description": "User preset"
                    }
                }
                
                # Save the preset
                if save_preset(current_settings, preset_name):
                    print_success(f"Preset '{preset_name}' saved successfully")
                    user_prefs.current_preset = preset_name
                    user_prefs.save_preferences()
                else:
                    print_error("Failed to save preset")
                    
            except Exception as e:
                print_error(f"Error preparing preset data: {e}")
            
        elif choice == "2":
            # Load preset
            result = load_preset()
            if result:
                settings, preset_name = result  # Unpack the returned tuple
                try:
                    print_section("Load Settings")
                    print_option("1", "Replace current settings with preset")
                    print_option("2", "Merge preset with current settings")
                    print_option("b", "Back")
                    
                    load_choice = get_validated_input("Select option (1-2 or b)", ["1", "2", "b"])
                    if load_choice == "b":
                        continue
                    
                    if load_choice == "1":
                        # Replace settings completely
                        if "imagen_settings" in settings and hasattr(user_prefs, 'imagen_settings'):
                            user_prefs.imagen_settings = settings["imagen_settings"].copy()
                        if "wallpaper_settings" in settings and hasattr(user_prefs, 'wallpaper_settings'):
                            user_prefs.wallpaper_settings = settings["wallpaper_settings"].copy()
                        print_success("Settings replaced with preset")
                    else:
                        # Merge settings (update existing)
                        if "imagen_settings" in settings and hasattr(user_prefs, 'imagen_settings'):
                            user_prefs.imagen_settings.update(settings["imagen_settings"])
                        if "wallpaper_settings" in settings and hasattr(user_prefs, 'wallpaper_settings'):
                            user_prefs.wallpaper_settings.update(settings["wallpaper_settings"])
                        print_success("Settings merged with preset")
                    
                    # Update current preset name
                    user_prefs.current_preset = preset_name
                    user_prefs.save_preferences()
                    
                except Exception as e:
                    print_error(f"Error applying preset settings: {e}")
            
        elif choice == "3":
            delete_preset()
            # If deleted preset was current, clear current preset
            if current_preset and not os.path.exists(os.path.join("presets", f"{current_preset}.json")):
                user_prefs.current_preset = None
                user_prefs.save_preferences()
            
        elif choice == "4":
            # View current preset details
            if not current_preset:
                print_warning("No preset currently loaded")
                continue
                
            print_section(f"Current Preset: {current_preset}")
            try:
                preset_file = os.path.join("presets", f"{current_preset}.json")
                if os.path.exists(preset_file):
                    with open(preset_file) as f:
                        settings = json.load(f)
                        
                    # Display metadata if available
                    if "metadata" in settings:
                        print_info("Metadata:")
                        for key, value in settings["metadata"].items():
                            print_info(f"  {key}: {value}")
                        print()
                        
                    # Display imagen settings
                    if "imagen_settings" in settings:
                        print_info("Imagen Settings:")
                        for key, value in settings["imagen_settings"].items():
                            if isinstance(value, dict):
                                print_info(f"  {key}:")
                                for k, v in value.items():
                                    print_info(f"    {k}: {v}")
                            else:
                                print_info(f"  {key}: {value}")
                        print()
                        
                    # Display wallpaper settings
                    if "wallpaper_settings" in settings:
                        print_info("Wallpaper Settings:")
                        for key, value in settings["wallpaper_settings"].items():
                            print_info(f"  {key}: {value}")
                    
                    input("\nPress Enter to continue...")
                else:
                    print_error(f"Preset file not found: {preset_file}")
            except Exception as e:
                print_error(f"Error reading preset details: {e}")
            
        else:  # choice == "5"
            return

def view_history():
    """View wallpaper generation history."""
    global generation_history
    generation_history.view_history()

def add_to_history(entry):
    """Add a generation entry to history."""
    global generation_history
    generation_history.add_entry(entry)

def load_preset():
    """Load a saved preset."""
    if not os.path.exists("presets"):
        os.makedirs("presets")
    
    presets = [f for f in os.listdir("presets") if f.endswith(".json")]
    if not presets:
        print_warning("No saved presets found")
        return None
    
    print_section("Available Presets")
    for i, preset in enumerate(presets, 1):
        print_option(str(i), preset.replace(".json", ""))
    print_option("b", "Back")
    
    choice = get_validated_input("Select preset to load", ["b"] + [str(i) for i in range(1, len(presets) + 1)])
    if choice == "b":
        return None
    
    preset_file = presets[int(choice) - 1]
    preset_name = os.path.splitext(preset_file)[0]
    
    try:
        with open(os.path.join("presets", preset_file)) as f:
            settings = json.load(f)
        return settings, preset_name
    except Exception as e:
        print_error(f"Error loading preset: {e}")
        return None

def save_preset(settings, name):
    """Save current settings as a preset."""
    if not os.path.exists("presets"):
        try:
            os.makedirs("presets")
            print_info("Created presets directory")
        except Exception as e:
            print_error(f"Error creating presets directory: {e}")
            return False
    
    filename = f"{name}.json"
    temp_file = os.path.join("presets", f"{filename}.tmp")
    final_file = os.path.join("presets", filename)
    
    print_info(f"Saving preset to {final_file}")
    
    try:
        # First write to a temporary file
        with open(temp_file, "w") as f:
            json.dump(settings, f, indent=4)
            f.flush()
            os.fsync(f.fileno())  # Ensure data is written to disk
            
        print_info("Temporary file written successfully")
            
        # If successful, rename to final filename (atomic operation)
        if os.path.exists(final_file):
            backup_file = os.path.join("presets", f"{filename}.bak")
            if os.path.exists(backup_file):
                os.remove(backup_file)
                print_info("Removed old backup file")
            os.rename(final_file, backup_file)
            print_info("Created backup of existing preset")
            
        os.rename(temp_file, final_file)
        print_info("Renamed temporary file to final preset file")
        return True
        
    except Exception as e:
        print_error(f"Error saving preset: {e}")
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
                print_info("Cleaned up temporary file after error")
            except:
                pass
        return False

def delete_preset():
    """Delete a saved preset."""
    if not os.path.exists("presets"):
        print_warning("No presets directory found")
        return
    
    presets = [f for f in os.listdir("presets") if f.endswith(".json") and not f.endswith((".tmp", ".bak"))]
    if not presets:
        print_warning("No saved presets found")
        return
    
    print_section("Select Preset to Delete")
    for i, preset in enumerate(presets, 1):
        print_option(str(i), preset.replace(".json", ""))
    print_option("b", "Back")
    
    choice = get_validated_input("Select preset to delete", ["b"] + [str(i) for i in range(1, len(presets) + 1)])
    if choice == "b":
        return
    
    preset_file = presets[int(choice) - 1]
    preset_name = preset_file.replace(".json", "")
    
    # Ask for confirmation
    confirm = get_validated_input(f"Are you sure you want to delete preset '{preset_name}'? (y/n)", ["y", "n"])
    if confirm.lower() != "y":
        print_info("Deletion cancelled")
        return
    
    try:
        preset_path = os.path.join("presets", preset_file)
        backup_path = os.path.join("presets", f"{preset_file}.bak")
        
        # Create backup before deletion
        if os.path.exists(preset_path):
            shutil.copy2(preset_path, backup_path)
            
        # Delete the preset
        os.remove(preset_path)
        print_success(f"Deleted preset: {preset_name}")
        
        # Keep backup for 24 hours
        def cleanup_backup():
            time.sleep(86400)  # 24 hours
            try:
                if os.path.exists(backup_path):
                    os.remove(backup_path)
            except:
                pass
        
        threading.Thread(target=cleanup_backup, daemon=True).start()
        
    except Exception as e:
        print_error(f"Error deleting preset: {e}")
        # Try to restore from backup if deletion failed
        if os.path.exists(backup_path) and not os.path.exists(preset_path):
            try:
                shutil.move(backup_path, preset_path)
                print_warning("Restored preset from backup after deletion error")
            except:
                pass

def export_settings():
    """Export current settings to file."""
    print_section("Export Settings")
    try:
        filename = get_validated_input("Enter filename for export (without extension)", allow_empty=False)
        filename = f"{filename}.json"
        
        settings = {
            "preferences": user_prefs.__dict__,
            "imagen_settings": user_prefs.imagen_settings,
            "export_date": datetime.now().isoformat()
        }
        
        with open(filename, "w") as f:
            json.dump(settings, f, indent=4)
        print_success(f"Settings exported to {filename}")
    except Exception as e:
        print_error(f"Error exporting settings: {e}")

def import_settings():
    """Import settings from file."""
    print_section("Import Settings")
    try:
        filename = get_validated_input("Enter filename to import (with extension)", allow_empty=False)
        if not os.path.exists(filename):
            print_error("File not found")
            return
        
        with open(filename) as f:
            settings = json.load(f)
        
        # Update preferences
        for key, value in settings["preferences"].items():
            setattr(user_prefs, key, value)
        
        # Update imagen settings
        user_prefs.imagen_settings.update(settings["imagen_settings"])
        
        user_prefs.save_preferences()
        print_success("Settings imported successfully")
    except Exception as e:
        print_error(f"Error importing settings: {e}")

def update_history_with_filenames(silent=False):
    """Update the generation history to include image filenames for existing entries.
    
    Args:
        silent: If True, don't print status messages
    """
    try:
        if os.path.exists("generation_history.json"):
            with open("generation_history.json", "r") as f:
                history = json.load(f)
            
            updated = False
            for entry in history:
                if "image_filename" not in entry and entry.get("enhanced_prompt"):
                    image_path = get_generated_image_path(entry["enhanced_prompt"])
                    if os.path.exists(image_path) or True:  # Include even if file doesn't exist
                        entry["image_filename"] = os.path.basename(image_path)
                        updated = True
            
            if updated:
                with open("generation_history.json", "w") as f:
                    json.dump(history, f, indent=4)
                if not silent:
                    print_info("Generation history updated with image filenames")
    except Exception as e:
        logging.error(f"Error updating history with filenames: {e}")

def main():
    """Main function to execute the script."""
    try:
        # Check dependencies
        check_dependencies()
        
        # Check and create necessary directories
        os.makedirs("genimage", exist_ok=True)
        
        # Update existing history entries with image filenames (silently)
        update_history_with_filenames(silent=True)
        
        print_header("AI Wallpaper Generator")
        print_info("Welcome to the AI Wallpaper Generator! This tool helps you create stunning wallpapers using AI.")
        
        while True:
            print_section("Main Menu")
            print_option("1", "Generate AI Wallpaper - Create custom wallpapers using AI")
            print_option("2", "Manage Preferences - Customize wallpaper settings")
            print_option("3", "Tools & Utilities")
            print_option("4", "View Generation History")
            print_option("5", "Exit - Save and exit")
            
            try:
                choice = get_validated_input("Select an option (1-5)", ["1", "2", "3", "4", "5"])
            except KeyboardInterrupt:
                print_info("\nSaving preferences before exit...")
                user_prefs.save_preferences()
                print_success("Goodbye!")
                sys.exit(0)
            
            if choice == "1":
                print_section("Generate AI Wallpaper")
                print_breadcrumb(["Main Menu", "Generate AI Wallpaper"])
                print_option("1", "Use Gemini AI to generate a prompt")
                print_option("2", "Use a random prompt")
                print_option("3", "Enter your own custom prompt")
                print_option("4", "Advanced Options - Fine-tune generation parameters")
                print_option("5", "Load Saved Preset")
                print_option("6", "Return to Main Menu")
                
                try:
                    prompt_choice = get_validated_input("Select option (1-6)", ["1", "2", "3", "4", "5", "6"])
                except KeyboardInterrupt:
                    print_info("\nSaving preferences before exit...")
                    user_prefs.save_preferences()
                    print_success("Goodbye!")
                    sys.exit(0)
                
                if prompt_choice == "6":
                    continue
                elif prompt_choice == "5":
                    settings = load_preset()
                    if settings:
                        generate_wallpaper(**settings)
                    continue
                
                if prompt_choice == "1":
                    # Get mood and style preferences for this generation
                    print_section("Optional Parameters")
                    print_info("You can specify a mood and style for your wallpaper (leave empty to use random)")
                    
                    mood_options = ["peaceful", "dramatic", "mysterious", "energetic", "melancholic",
                                  "joyful", "romantic", "eerie", "nostalgic", "contemplative"]
                    style_options = ["abstract", "anime", "art_deco", "art_nouveau", "cartoon", "charcoal", 
                                   "cinematic", "comic_book", "constructivism", "cubism", "cyberpunk", 
                                   "digital_art", "divisionism", "double_exposure", "expressionism", 
                                   "fantasy", "futurism", "glitch_art", "gothic", "graffiti", 
                                   "hyperrealism", "impressionism", "ink_drawing", "isometric", "landscape", 
                                   "line_art", "low_poly", "manga", "minimalist", "oil_painting", 
                                   "paper_cut", "pastel", "pencil_sketch", "photograph", "pixel_art", 
                                   "pointillism", "pop_art", "realism", "retrowave", "sci_fi", 
                                   "sketch", "stained_glass", "steampunk", "surrealism", "ukiyo_e", 
                                   "vaporwave", "watercolor", "woodcut"]
                    
                    # Group styles by compatibility for random mixing
                    style_categories = {
                        "traditional_art": ["art_deco", "art_nouveau", "charcoal", "expressionism", 
                                           "gothic", "impressionism", "oil_painting", "pastel", 
                                           "pencil_sketch", "realism", "sketch", "watercolor", "woodcut"],
                        "digital_art": ["abstract", "cinematic", "cyberpunk", "digital_art", "double_exposure", 
                                       "fantasy", "futurism", "glitch_art", "hyperrealism", "isometric", 
                                       "landscape", "low_poly", "minimalist", "retrowave", "sci_fi",
                                       "stained_glass", "steampunk", "surrealism", "vaporwave"],
                        "illustration": ["anime", "cartoon", "comic_book", "divisionism", "graffiti", 
                                        "ink_drawing", "line_art", "manga", "paper_cut", "pixel_art", 
                                        "pointillism", "pop_art", "ukiyo_e"]
                    }
                    
                    def generate_random_style_mix():
                        # Select a random category
                        category = random.choice(list(style_categories.keys()))
                        # Select 2-3 compatible styles from the same category
                        num_styles = random.randint(2, 3)
                        available_styles = style_categories[category]
                        if len(available_styles) < num_styles:
                            num_styles = len(available_styles)
                        selected_styles = random.sample(available_styles, num_styles)
                        return " + ".join(selected_styles)
                    
                    print_info(f"Mood options: {', '.join(mood_options)}")
                    mood = input("Enter mood (optional): ").strip().lower()
                    if mood and mood not in mood_options:
                        print_warning(f"'{mood}' is not in the suggested moods, but we'll try to use it anyway")
                    
                    print_info(f"Style options: {', '.join(style_options)}")
                    print_info("You can also enter 'random_mix' to combine 2-3 compatible styles for creative results")
                    style = input("Enter style (optional): ").strip().lower()
                    
                    if style == "random_mix":
                        style = generate_random_style_mix()
                        print_info(f"Selected style mix: {style}")
                        # Ask if the user wants to save this style mix to their preferences
                        save_style = get_validated_input("Save this style mix to your preferences? (y/n)", ["y", "n"])
                        if save_style == "y":
                            if style not in user_prefs.preferred_styles:
                                user_prefs.preferred_styles.append(style)
                                user_prefs.save_preferences()
                                print_success(f"Added '{style}' to preferred styles")
                            else:
                                print_warning(f"'{style}' is already in your preferred styles")
                    elif style and style not in style_options:
                        print_warning(f"'{style}' is not in the suggested styles, but we'll try to use it anyway")
                    
                    generate_wallpaper("gemini", mood=mood, style=style)
                    
                elif prompt_choice == "2":
                    generate_wallpaper("random")
                    
                elif prompt_choice == "3":
                    custom_prompt = get_validated_input("Enter your custom prompt (or 'b' to go back)", allow_empty=False)
                    if custom_prompt.lower() == 'b':
                        continue
                    generate_wallpaper("custom", custom_prompt=custom_prompt)
                
                elif prompt_choice == "4":
                    configure_advanced_options()
            
            elif choice == "2":
                manage_preferences()
                
            elif choice == "3":
                print_section("Tools & Utilities")
                print_breadcrumb(["Main Menu", "Tools & Utilities"])
                print_option("1", "Manage Presets")
                print_option("2", "View Generation History")
                print_option("3", "Export Settings")
                print_option("4", "Import Settings")
                print_option("5", "Update History Filenames")
                print_option("6", "Return to Main Menu")
                
                tools_choice = get_validated_input("Select option (1-6)", ["1", "2", "3", "4", "5", "6"])
                
                if tools_choice == "1":
                    manage_presets()
                elif tools_choice == "2":
                    view_history()
                elif tools_choice == "3":
                    export_settings()
                elif tools_choice == "4":
                    import_settings()
                elif tools_choice == "5":
                    print_info("Updating generation history with descriptive filenames...")
                    update_history_with_filenames(silent=False)
                continue
            
            elif choice == "4":
                view_history()
            elif choice == "5":
                print_info("Saving preferences before exit...")
                user_prefs.save_preferences()
                print_success("Goodbye!")
                break

    except KeyboardInterrupt:
        print_info("\nSaving preferences before exit...")
        user_prefs.save_preferences()
        print_success("Goodbye!")
        sys.exit(0)

def print_breadcrumb(path_list):
    """Print navigation breadcrumb."""
    print_info(" > ".join(path_list))

if __name__ == "__main__":
    main()

