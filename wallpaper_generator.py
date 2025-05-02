#!/usr/bin/env python3
"""AI Wallpaper Generator - Create stunning AI-generated desktop wallpapers

This script generates high-quality desktop wallpapers using Google's Imagen 3 model
via the Gemini API. It offers various customization options and prompt engineering
techniques to create visually appealing wallpapers tailored to your preferences.
"""
# Standard library imports
import json
import os
import platform
import random
import subprocess
import shlex
import logging
import sys
import time
import threading
import re
# Removed duplicate import of signal; signal handling is managed by graceful_exit.py

# Import graceful exit handler early to register the signal handler
import graceful_exit
import hashlib
import html
import shutil
from urllib.parse import quote

# Import utility functions
from file_utils import get_generated_image_path
from datetime import datetime
from typing import Optional, Dict, List, Any, Tuple
import argparse

# Third-party imports
import bleach
import ctypes
import google.generativeai as genai

# Local application imports
from settings_modules.settings_import_export import export_settings, import_settings
from settings_modules.settings_utils import update_history_with_filenames, load_last_genre, save_last_genre
from settings_modules.settings_manager import initialize_settings, get_preferences
from settings_modules.menu_management import main_menu
from settings_modules.preset_management import manage_presets, load_preset, save_preset, delete_preset
from settings_modules.user_preferences import UserPreferences
# The following functions are now called from within the menu management modules,
# so they do not need to be imported directly in wallpaper_generator.py:
# manage_genres, manage_styles, manage_moods, manage_wallpaper_settings, manage_imagen_settings, configure_advanced_options

from config import (
    nature_tags, space_tags, sea_tags, flowers_tags, urban_tags,
    fantasy_tags, abstract_tags, mood_tags, available_genres,
    PROMPT_INSTRUCTIONS, CUSTOM_PROMPT_INSTRUCTIONS,
    style_to_tags # Added style_to_tags import
)
from ui_utils import (
    print_header, print_section, print_option, print_success, print_error,
    print_warning, print_info, print_prompt, get_validated_input, show_spinner,
    print_breadcrumb, print_colored
)
from prompt_generator import (
    generate_prompt_gemini, generate_prompt_random, enhance_custom_prompt,
    enforce_prompt_format, select_random_tags, generate_random_style_mix,
    set_prompt_preferences, use_user_preferences, SimplePrefs
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("wallpaper_generator.log")
    ]
)

# Check for required dependencies
def check_dependencies():
    """Check if all required dependencies are installed."""
    missing_deps = []

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
        print_warning("\nMissing optional dependencies:")
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
    print_warning("\nGEMINI_API_KEY environment variable not set.")
    print_info("AI image generation will not be available.\n")

# Create a cache for generated prompts
prompt_cache = {}

# Ensure cache directories exist
os.makedirs("cache", exist_ok=True)
os.makedirs("genimage", exist_ok=True)

# Initialize user preferences
user_prefs = initialize_settings()

# Set default Gemini model
gemini_model_name = "gemini-2.5-pro-exp-03-25"

def _extract_imagen_settings(user_prefs):
    """Extract relevant Imagen settings from user preferences with enhanced style support."""
    settings = user_prefs.imagen_settings
    return {
        "camera_settings": settings.get("camera_settings", {}),
        "lighting_settings": settings.get("lighting_settings", {}),
        "composition_settings": settings.get("composition_settings", {}),
        "environment_settings": settings.get("environment_settings", {}),
        "style_settings": settings.get("style_settings", {}),
        "detail_settings": settings.get("detail_settings", {}),
        "color_settings": settings.get("color_settings", {}),
        "quality_settings": settings.get("quality_settings", {}),
        "negative_prompt": settings.get("negative_prompt", ""),
        "aspect_ratio": user_prefs.aspect_ratio,
        "digital_settings": settings.get("digital_settings", {}),
        "game_engine_settings": settings.get("game_engine_settings", {}),
        "software_settings": settings.get("software_settings", {}),
        "medium_settings": settings.get("medium_settings", {}),
        "illustration_settings": settings.get("illustration_settings", {}),
        "abstract_settings": settings.get("abstract_settings", {}),
        "material_settings": settings.get("material_settings", {})
    }

def generate_prompt_gemini(tags, user_prefs):
    """Generate a detailed prompt using Gemini and user preferences with enhanced style support."""
    try:
        cache_key = str(tags) + str(user_prefs.imagen_settings) + str(gemini_model_name)
        # Check if we have this prompt cached
        if cache_key in prompt_cache:
            return prompt_cache[cache_key]

        # Extract settings using the helper function
        settings_data = _extract_imagen_settings(user_prefs)
        camera_settings = settings_data["camera_settings"]
        lighting_settings = settings_data["lighting_settings"]
        composition_settings = settings_data["composition_settings"]
        environment_settings = settings_data["environment_settings"]
        style_settings = settings_data["style_settings"]
        detail_settings = settings_data["detail_settings"]
        color_settings = settings_data["color_settings"]
        quality_settings = settings_data["quality_settings"]
        negative_prompt = settings_data["negative_prompt"]
        aspect_ratio = settings_data["aspect_ratio"]
        digital_settings = settings_data["digital_settings"]
        game_engine_settings = settings_data["game_engine_settings"]
        medium_settings = settings_data["medium_settings"]
        illustration_settings = settings_data["illustration_settings"]
        abstract_settings = settings_data["abstract_settings"]
        material_settings = settings_data["material_settings"]

        # Get user preferences (style and mood are still accessed directly for clarity)
        style = user_prefs.preferred_styles[0] if user_prefs.preferred_styles else None
        mood = user_prefs.preferred_moods[0] if user_prefs.preferred_moods else None

        # Extract style-specific settings
        digital_software = digital_settings.get("software", "")
        digital_effects = digital_settings.get("digital_effects", [])
        game_engine = game_engine_settings.get("engine_type", "")
        game_genre = game_engine_settings.get("game_genre", "")
        painting_medium = medium_settings.get("painting_medium", "")
        illustration_style = illustration_settings.get("style", "")
        abstract_composition = abstract_settings.get("composition_type", "")
        material_type = material_settings.get("material_type", "")

        # Extract specific settings for the prompt
        camera_model = camera_settings.get("camera_model")
        lens_type = camera_settings.get("lens_type")
        aperture = camera_settings.get("aperture")
        special_lens = camera_settings.get("special_lens")
        depth_of_field = composition_settings.get("depth_of_field")

        time_of_day = lighting_settings.get("time_of_day")
        lighting_type = lighting_settings.get("lighting_type")
        light_source = lighting_settings.get("light_source")
        light_quality = lighting_settings.get("light_quality")
        artificial_sources = lighting_settings.get("artificial_sources", [])

        technique = composition_settings.get("technique")
        camera_angle = composition_settings.get("camera_angle")
        visual_flow = composition_settings.get("visual_flow")
        depth_layering = composition_settings.get("depth_layering")

        weather = environment_settings.get("weather")
        season = environment_settings.get("season")
        location_type = environment_settings.get("location_type")
        atmospheric_effects = environment_settings.get("atmospheric_effects", [])

        art_movement = style_settings.get("art_movement")
        post_processing = style_settings.get("post_processing", [])

        detail_level = detail_settings.get("detail_level")
        texture_quality = detail_settings.get("texture_quality")
        special_effects = detail_settings.get("special_effects", [])

        color_scheme = color_settings.get("color_scheme")
        palette_type = color_settings.get("palette_type")
        color_temperature = color_settings.get("color_temperature")

        resolution = quality_settings.get("resolution", "3840x2160")
        rendering_quality = quality_settings.get("rendering_quality")

        # Format tags for prompt
        formatted_tags = ", ".join(tags)

        # If no negative prompt is specified, use default negative prompt
        if not negative_prompt:
            negative_prompt = "ugly, disfigured, low quality, blurry, nsfw, watermark, signature, out of frame, extra limbs, poorly drawn face, twisted limbs, distorted face, bad proportions, bad anatomy"

        # Use PROMPT_INSTRUCTIONS from prompt_config.py with proper formatting
        instruction_context = PROMPT_INSTRUCTIONS.format(
            resolution=resolution if resolution else "Not specified",
            aspect_ratio=aspect_ratio if aspect_ratio else "16:9",
            color_scheme=color_scheme if color_scheme else "Not specified",
            lighting=lighting_type if lighting_type else "Not specified",
            composition=technique if technique else "Not specified",
            depth_of_field=depth_of_field if depth_of_field else "Not specified"
        )

        # Create a more comprehensive technical context with all settings
        technical_context = f"""
Create a detailed description for a wallpaper image featuring: {formatted_tags}

SUBJECT ANALYSIS:
Carefully analyze the subject "{formatted_tags}" and tailor your description to highlight its unique characteristics:
- For natural subjects: emphasize organic elements, textures, and environmental context
- For urban subjects: focus on architectural details, perspective, and urban atmosphere
- For abstract subjects: highlight patterns, shapes, and conceptual elements
- For space/cosmic subjects: emphasize scale, wonder, and celestial phenomena
- For fantasy subjects: create a cohesive magical or surreal atmosphere

USER STYLE PREFERENCES:
- Style: {style if style else "Use what makes sense for the subject"}
- Mood: {mood if mood else "Use what makes sense for the subject"}
- Art Movement: {art_movement if art_movement else "Use what makes sense for the subject"}

MANDATORY TECHNICAL PARAMETERS:
Resolution: {resolution} - YOU MUST INCLUDE THIS IN YOUR FINAL PROMPT
Aspect Ratio: {aspect_ratio} - YOU MUST INCLUDE THIS IN YOUR FINAL PROMPT

TECHNICAL SPECIFICATIONS:
- Camera model: {camera_model if camera_model else "Not specified"}
- Lens: {lens_type if lens_type else "Not specified"}
- Aperture: {aperture if aperture else "Not specified"}
- Special lens: {special_lens if special_lens else "Not specified"}
- Depth of field: {depth_of_field if depth_of_field else "Not specified"}
- Lighting type: {lighting_type if lighting_type else "Not specified"}
- Light quality: {light_quality if light_quality else "Not specified"}
- Time of day: {time_of_day if time_of_day else "Not specified"}
- Light source: {light_source if light_source else "Not specified"}
- Artificial lighting: {", ".join(artificial_sources) if artificial_sources else "None"}
- Composition technique: {technique if technique else "Not specified"}
- Camera angle: {camera_angle if camera_angle else "Not specified"}
- Visual flow: {visual_flow if visual_flow else "Not specified"}
- Depth layering: {depth_layering if depth_layering else "Not specified"}
- Weather: {weather if weather else "Not specified"}
- Season: {season if season else "Not specified"}
- Location type: {location_type if location_type else "Not specified"}
- Atmospheric effects: {", ".join(atmospheric_effects) if atmospheric_effects else "None"}
- Post-processing: {", ".join(post_processing) if post_processing else "None"}
- Detail level: {detail_level if detail_level else "Not specified"}
- Texture quality: {texture_quality if texture_quality else "Not specified"}
- Special effects: {", ".join(special_effects) if special_effects else "None"}
- Color scheme: {color_scheme if color_scheme else "Not specified"}
- Palette type: {palette_type if palette_type else "Not specified"}
- Color temperature: {color_temperature if color_temperature else "Not specified"}
- Resolution: {resolution if resolution else "Not specified"}
- Rendering quality: {rendering_quality if rendering_quality else "Not specified"}
- Aspect ratio: {aspect_ratio if aspect_ratio else "16:9"}

IMPORTANT GUIDELINES:
1. Create a cohesive, detailed prompt that incorporates all specified settings naturally
2. IGNORE any "Not specified" or "None" settings - do not include them
3. Focus on creating a visually striking image suitable for a desktop wallpaper
4. Ensure the subject "{formatted_tags}" remains the central focus
5. Adapt the style and technical details to suit the specific subject matter
6. MUST end the description with "{resolution} resolution, {aspect_ratio} aspect ratio"
7. Always include a negative prompt section at the end

OUTPUT FORMAT:
Your response must follow this exact format:
1. A single, detailed paragraph describing the image
2. MUST end the description with "{resolution} resolution, {aspect_ratio} aspect ratio"
3. End with "Avoid: [negative elements]"

NEGATIVE PROMPT - ALWAYS INCLUDE:
The following elements must be avoided in the image: {negative_prompt}
"""

        # Generate prompt using Gemini
        if not GEMINI_API_KEY:
            logging.warning("No Gemini API key configured")
            # Return a formatted version of the simple tags
            return enforce_prompt_format(formatted_tags, resolution, aspect_ratio, negative_prompt)

        try:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel(gemini_model_name)
            response = model.generate_content(instruction_context + "\n\n" + technical_context)

            if response.text:
                full_response = response.text.strip()

                # Parse the response to separate prompt and negative prompt
                prompt_parts = full_response.split("Avoid:")

                if len(prompt_parts) > 1:
                    # If successfully parsed into two parts
                    main_prompt = prompt_parts[0].strip()
                    negative_part = prompt_parts[1].strip()

                    # Combine them with "Avoid:" format
                    final_prompt = f"{main_prompt} Avoid: {negative_part}"
                else:
                    # If not in expected format, just add negative prompt
                    final_prompt = full_response
                    if "avoid" not in final_prompt.lower():
                        final_prompt += f" Avoid: {negative_prompt}"

                # Ensure proper formatting with resolution and aspect ratio
                final_prompt = enforce_prompt_format(final_prompt, resolution, aspect_ratio, negative_prompt)

                prompt_cache[cache_key] = final_prompt
                return final_prompt
            else:
                # Return a formatted version of the simple tags
                formatted_prompt = enforce_prompt_format(formatted_tags, resolution, aspect_ratio, negative_prompt)
                return formatted_prompt
        except Exception as e:
            logging.error(f"Error generating prompt with Gemini: {e}")
            # Return a formatted version of the simple tags
            return enforce_prompt_format(formatted_tags, resolution, aspect_ratio, negative_prompt)
    except Exception as e:
        logging.error(f"Error in generate_prompt_gemini: {e}")
        formatted_tags_str = ", ".join(tags)
        # Return a formatted version of the simple tags
        return enforce_prompt_format(formatted_tags_str, "3840x2160", "16:9", negative_prompt)

def generate_prompt_random(tags, user_prefs):
    """Generate a random prompt with selected tags and user preferences."""
    try:
        # Extract settings using the helper function
        settings_data = _extract_imagen_settings(user_prefs)
        camera_settings = settings_data["camera_settings"]
        lighting_settings = settings_data["lighting_settings"]
        quality_settings = settings_data["quality_settings"]
        style_settings = settings_data["style_settings"]
        color_settings = settings_data["color_settings"]

        # User preferences (style and mood are still accessed directly for clarity)
        style = user_prefs.preferred_styles[0] if user_prefs.preferred_styles else None
        mood = user_prefs.preferred_moods[0] if user_prefs.preferred_moods else None

        # Extract specific settings for enhancers
        camera_model = camera_settings.get("camera_model")
        lens_type = camera_settings.get("lens_type")
        time_of_day = lighting_settings.get("time_of_day")
        lighting_type = lighting_settings.get("lighting_type")
        detail_level = quality_settings.get("detail_level")
        rendering_quality = quality_settings.get("rendering_quality")
        art_movement = style_settings.get("art_movement")
        color_scheme = color_settings.get("color_scheme")

        # Build the prompt
        prompt_parts = []
        for tag in tags:
            # Try to enhance tag selection based on user preferences
            prompt_parts.append(tag)

        prompt = ", ".join(prompt_parts)

        # Add image quality enhancers
        quality_enhancers = []

        if style:
            quality_enhancers.append(style)
        if mood:
            quality_enhancers.append(mood)
        if art_movement:
            quality_enhancers.append(art_movement)
        if rendering_quality:
            quality_enhancers.append(rendering_quality)
        if detail_level:
            quality_enhancers.append(detail_level)
        if color_scheme:
            quality_enhancers.append(color_scheme)
        if camera_model:
            quality_enhancers.append(f"shot on {camera_model}")
        if lens_type:
            quality_enhancers.append(f"{lens_type} lens")
        if time_of_day:
            quality_enhancers.append(time_of_day.replace('_', ' '))
        if lighting_type:
            quality_enhancers.append(lighting_type.replace('_', ' '))

        # Add quality enhancers if available
        if quality_enhancers:
            prompt += ", " + ", ".join(quality_enhancers)

        return prompt
    except Exception as e:
        print(f"Error in generate_prompt_random: {e}")
        return ", ".join(tags)  # Fallback to basic tags if error occurs



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
        model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')
        
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
        ) # Added closing parenthesis

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
        logging.debug(f"Ensuring genimage directory exists at: {genimage_dir}")
    except Exception as e:
        logging.error(f"Error creating genimage directory: {e}")
        # Fallback to relative path if absolute path fails
        genimage_dir = "genimage"
        os.makedirs(genimage_dir, exist_ok=True)
        
    # Return absolute path to ensure consistency
    return os.path.join(genimage_dir, filename)

def list_sorted_genimages(directory):
    """List and sort image files in a directory by modification time."""
    try:
        # Ensure the directory exists with absolute path
        abs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), directory)
        os.makedirs(abs_dir, exist_ok=True)

        # Get list of image files with full paths for sorting
        files_with_paths = [os.path.join(abs_dir, f) for f in os.listdir(abs_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        # Sort by modification time (newest first)
        sorted_files_with_paths = sorted(files_with_paths, key=os.path.getmtime, reverse=True)

        # Return just the filenames
        image_filenames = [os.path.basename(f) for f in sorted_files_with_paths]

        return image_filenames
    except (FileNotFoundError, OSError) as e:
        logging.error(f"Error listing images in {directory}: {e}")
        return []



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
    """Set the wallpaper using the appropriate method for the current desktop environment."""
    try:
        os_name = platform.system()
        
        # Ensure we have an absolute path from the project directory
        if not os.path.isabs(image_path):
            # Convert relative path to absolute path based on the project directory
            absolute_path = os.path.abspath(image_path)
        else:
            absolute_path = image_path
        
        # Save the original path for later verification
        original_path = image_path
        
        if os_name == "Windows":
            SPI_SETDESKWALLPAPER = 0x0014
            SPIF_UPDATEINIFILE = 0x01
            SPIF_SENDWININICHANGE = 0x02
            # Success
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)
            logging.debug("Wallpaper set successfully on Windows")
            return True
        elif os_name == "Darwin":
            script = f'tell application "Finder" to set desktop picture to POSIX file "{absolute_path}"'
            command = f"osascript -e '{script}'"
            subprocess.run(shlex.split(command), check=True, capture_output=True, text=True)
            logging.debug("Wallpaper set successfully on macOS")
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
                logging.debug(f"Wallpaper set successfully on Linux using path: {absolute_path}")
                logging.debug(f"Original path was: {original_path}")
                return True
            elif desktop_env == 'CINNAMON':
                # Cinnamon
                command = ["gsettings", "set", "org.cinnamon.desktop.background", "picture-uri", file_uri]
                subprocess.run(command, check=True, capture_output=True, text=True)
                logging.debug("Wallpaper set successfully on Linux")
                return True
            elif desktop_env == 'MATE':
                # MATE
                command = ["gsettings", "set", "org.mate.background", "picture-filename", absolute_path]
                subprocess.run(command, check=True, capture_output=True, text=True)
                logging.debug("Wallpaper set successfully on Linux")
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
                        logging.debug("Wallpaper set successfully on Linux")
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
                    logging.debug("Wallpaper set successfully on Linux")
                    return True
                except (subprocess.SubprocessError, FileNotFoundError):
                    print_warning("Failed to set wallpaper using KDE Plasma method")
                    return False
            elif desktop_env in ['I3', 'SWAY']:
                # i3/sway - try feh first, then nitrogen
                try:
                    command = ["feh", "--bg-fill", absolute_path]
                    subprocess.run(command, check=True, capture_output=True, text=True)
                    logging.debug("Wallpaper set successfully on Linux")
                    return True
                except (subprocess.SubprocessError, FileNotFoundError):
                    try:
                        command = ["nitrogen", "--set-zoom-fill", absolute_path]
                        subprocess.run(command, check=True, capture_output=True, text=True)
                        logging.debug("Wallpaper set successfully on Linux")
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
                    logging.debug("Wallpaper set successfully on Linux")
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

def sanitize_log_content(content):
    """Sanitize content for logging by removing sensitive data."""
    return re.sub(r'api_key=[\w-]+', 'api_key=REDACTED', content)

def save_prompts_to_json(gemini_prompt, enhanced_prompt, filename="prompts.json"):
    """Save prompts to a JSON file."""
    with open(filename, "w") as f:
        json.dump({
            "gemini_prompt": gemini_prompt,
            "enhanced_prompt": enhanced_prompt,
            "timestamp": datetime.now().isoformat()
        }, f, indent=4)

# Note: configure_advanced_options() has been moved to wallpaper_settings.py

class GenerationHistory:
    """Class to manage the wallpaper generation history."""
    
    def __init__(self, history_file="generation_history.json"):
        """Initialize the history object."""
        self.history = []
        # Use absolute path for history file
        if not os.path.isabs(history_file):
            self.history_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), history_file)
        else:
            self.history_file = history_file
        logging.debug(f"Generation history file path: {self.history_file}")
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
                logging.debug(f"Loaded {len(self.history)} history entries")
            else:
                logging.debug(f"No history file found at {self.history_file}, creating new history")
                self.history = []
        except Exception as e:
            logging.error(f"Error loading history: {e}")
            self.history = []
    
    def save_history(self):
        """Save history to file."""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=4)
            logging.debug(f"Saved {len(self.history)} history entries to {self.history_file}")
            # Verify the file was saved correctly
            if os.path.exists(self.history_file):
                logging.debug(f"Verified history file exists at {self.history_file}")
            else:
                logging.error(f"Failed to save history file at {self.history_file}")
        except Exception as e:
            logging.error(f"Error saving history: {e}")
            # Try to save to a fallback location
            try:
                fallback_path = "generation_history_fallback.json"
                with open(fallback_path, 'w') as f:
                    json.dump(self.history, f, indent=4)
                logging.debug(f"Saved history to fallback location: {fallback_path}")
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
                logging.debug(f"Adding history entry with image filename: {image_filename}")
            
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
            logging.debug(f"Added entry to history, current count: {len(self.history)}")
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
                        else:
                            print(f"✗ Image file not found in home directory: {possible_home_path}")
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

def generate_random_style_mix():
    """Generate a random style mix using either AI or predefined categories."""
    # First try using AI style generation if available
    try:
        from ai_style_generator import generate_random_style
        if GEMINI_API_KEY:
            ai_style = generate_random_style()
            if ai_style:
                return ai_style
    except (ImportError, Exception) as e:
        logging.debug(f"AI style generation not available: {e}")
    
    # Fallback to predefined categories
    settings = user_prefs.imagen_settings
    style_settings = settings.get("style_settings", {})
    
    # Import style categories from configuration
    from config import style_categories as default_style_categories
    
    # Use custom categories if available, otherwise use defaults
    style_categories = style_settings.get("style_categories", default_style_categories)
    
    # Save default categories if needed
    if not style_settings.get("style_categories"):
        style_settings["style_categories"] = default_style_categories
        user_prefs.imagen_settings["style_settings"] = style_settings
        user_prefs.save_preferences()
    
    # Select a random category
    category = random.choice(list(style_categories.keys()))
    num_styles = random.randint(2, 3)
    available_styles = style_categories[category]
    selected_styles = random.sample(available_styles, min(num_styles, len(available_styles)))
    return " + ".join(selected_styles)

# Import get_preferences from wallpaper_settings
from wallpaper_settings import get_preferences
# Import use_user_preferences from prompt_generator
from prompt_generator import use_user_preferences

def generate_wallpaper(prompt_type=None, custom_prompt=None, mood=None, style=None, resolution=None, color_scheme=None, lighting=None, generate_only=False):
    """Generate wallpaper based on given parameters.
    
    Args:
        prompt_type: Type of prompt to generate ('gemini', 'random', 'custom')
        custom_prompt: Custom prompt text if prompt_type is 'custom'
        mood: Mood for the image
        style: Style for the image
        resolution: Image resolution
        color_scheme: Color scheme for the image
        lighting: Lighting settings
        generate_only: If True, only generate the prompt without creating the image
    """
    # Fetch the LATEST preferences right before generation
    user_prefs = get_preferences()
    global generation_history # Keep global for history
    
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
        
        # Check if we should use user preferences
        if use_user_preferences:
            enhanced_prompt = enhance_custom_prompt(sanitized_prompt, user_prefs)
        else:
            enhanced_prompt = enhance_custom_prompt(sanitized_prompt)

        if not enhanced_prompt:
            print_warning("Failed to enhance custom prompt, using original prompt.")
            enhanced_prompt = sanitized_prompt

        # Defensive fallback: ensure enhanced_prompt is a string
        if enhanced_prompt is None:
            enhanced_prompt = sanitized_prompt

    elif prompt_type == "random":
        print_info("Generating random prompt...")
        # Use select_random_tags to get a subset of tags rather than all tags
        random_tags = select_random_tags()
        
        # Check if we should use user preferences
        if use_user_preferences:
            # Use the imported function from prompt_generator.py
            from prompt_generator import generate_prompt_random as generator_random
            gemini_prompt = generator_random(random_tags, user_prefs)
            # Enhance the random prompt to make it more detailed
            enhanced_prompt = enhance_custom_prompt(gemini_prompt, user_prefs)
            print(f"Enhanced random prompt: {enhanced_prompt}")
        else:
            # Use the imported function from prompt_generator.py
            from prompt_generator import generate_prompt_random as generator_random
            gemini_prompt = generator_random(random_tags)
            # Enhance the random prompt to make it more detailed
            enhanced_prompt = enhance_custom_prompt(gemini_prompt)
            print(f"Enhanced random prompt: {enhanced_prompt}")
    else:  # gemini
        print_section("Generating AI Prompt")
        print_info("Using Google's Gemini AI to create a unique wallpaper prompt...")
        all_tags = nature_tags + space_tags + sea_tags + flowers_tags + urban_tags + fantasy_tags + abstract_tags
        
        # If user has preferred genres, prioritize those
        user_tags = []
        if use_user_preferences and user_prefs.preferred_genres:
            user_tags.extend(user_prefs.preferred_genres)
            print_info(f"Using your preferred genres: {', '.join(user_prefs.preferred_genres)}")
        
        # If specific mood was provided, add related tags
        if mood:
            mood_related = [tag for tag in mood_tags if mood in tag or tag.startswith(mood)]
            if mood_related:
                user_tags.extend(mood_related[:2])
                print_info(f"Adding tags for your selected mood: {mood}")
        
        # If specific style was provided, add related tags
        if style:
            # from prompt_config import style_to_tags # Removed local import
            if style in style_to_tags: # Use the top-level imported style_to_tags
                available_tags = style_to_tags[style]
                user_tags.extend(random.sample(available_tags, min(2, len(available_tags))))
                print_info(f"Adding tags for your selected style: {style}")
        
        # If we have user tags, use them, otherwise use all tags
        tags_to_use = user_tags if user_tags else all_tags
        
        show_spinner("Analyzing your preferences and generating ideas...", 1)
        
        # Check if we should use user preferences
        if use_user_preferences:
            # Use the imported function from prompt_generator.py 
            from prompt_generator import generate_prompt_gemini as generator_gemini
            gemini_prompt = generator_gemini(tags_to_use, user_prefs)
        else:
            # Use the imported function from prompt_generator.py
            from prompt_generator import generate_prompt_gemini as generator_gemini
            gemini_prompt = generator_gemini(tags_to_use)
        
        if not gemini_prompt:
            print_warning("Gemini encountered an issue. Generating a random prompt instead...")
            if use_user_preferences:
                gemini_prompt = generate_prompt_random(tags_to_use, user_prefs)
            else:
                gemini_prompt = generate_prompt_random(tags_to_use)
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
        "user_preferences": {
            "preferred_genres": user_prefs.preferred_genres,
            "preferred_styles": user_prefs.preferred_styles,
            "preferred_moods": user_prefs.preferred_moods,
            "negative_prompts": user_prefs.negative_prompts,
            "aspect_ratio": user_prefs.aspect_ratio,
            # Note: imagen_settings and wallpaper_settings are saved separately below
            # history_file and last_preset are likely not needed in the history entry itself
        },
        "imagen_settings": user_prefs.imagen_settings,
        "wallpaper_settings": user_prefs.wallpaper_settings,
        "output": None  # Will be updated when image is generated
    })
    
    # Step 2: Display the prompt and handle next steps
    if enhanced_prompt:
        print_section("Generated Prompt")
        print_info(enhanced_prompt)
        
        # If generate_only is True, handle prompt saving and return early
        if generate_only:
            save_choice = get_validated_input("Would you like to save this prompt to a file? (y/n)", ["y", "n"])
            if save_choice.lower() == "y":
                filename = get_validated_input("Enter filename (or press Enter for default 'saved_prompt.txt'): ", allow_empty=True)
                if not filename:
                    filename = "saved_prompt.txt"
                try:
                    with open(filename, "w") as f:
                        f.write(enhanced_prompt)
                    print_success(f"Prompt saved to {filename}")
                except Exception as e:
                    print_error(f"Error saving prompt: {e}")
            return True
        
        # Otherwise proceed with image generation confirmation
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
                    # Check if we should use user preferences
                    if use_user_preferences:
                        enhanced_prompt = enhance_custom_prompt(sanitized_prompt, user_prefs)
                    else:
                        enhanced_prompt = enhance_custom_prompt(sanitized_prompt)
                elif prompt_type == "random":
                    # Use select_random_tags to get a subset of tags rather than all tags
                    random_tags = select_random_tags()
                    # Check if we should use user preferences
                    if use_user_preferences:
                        gemini_prompt = generate_prompt_random(random_tags, user_prefs)
                        # Enhance the random prompt to make it more detailed
                        enhanced_prompt = enhance_custom_prompt(gemini_prompt, user_prefs)
                        print(f"Enhanced random prompt: {enhanced_prompt}")
                    else:
                        gemini_prompt = generate_prompt_random(random_tags)
                        # Enhance the random prompt to make it more detailed
                        enhanced_prompt = enhance_custom_prompt(gemini_prompt)
                        print(f"Enhanced random prompt: {enhanced_prompt}")
                else:  # gemini
                    all_tags = nature_tags + space_tags + sea_tags + flowers_tags + urban_tags + fantasy_tags + abstract_tags
                    # Check if we should use user preferences
                    if use_user_preferences:
                        gemini_prompt = generate_prompt_gemini(all_tags, user_prefs)
                        if not gemini_prompt:
                            print_warning("Failed to generate prompt with Gemini, using random tags instead.")
                            # Use select_random_tags instead of all_tags
                            random_tags = select_random_tags()
                            gemini_prompt = generate_prompt_random(random_tags, user_prefs)
                    else:
                        gemini_prompt = generate_prompt_gemini(all_tags)
                        if not gemini_prompt:
                            print_warning("Failed to generate prompt with Gemini, using random tags instead.")
                            # Use select_random_tags instead of all_tags
                            random_tags = select_random_tags()
                            gemini_prompt = generate_prompt_random(random_tags)
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
            valid_ratios = ["16:9", "4:3", "1:1", "9:16"]
            if aspect_ratio not in valid_ratios:
                print_warning(f"Invalid aspect ratio: {aspect_ratio}. Using default 16:9.")
                aspect_ratio = "16:9"
                user_prefs.aspect_ratio = aspect_ratio
                user_prefs.save_preferences()
            
            try:
                # Get negative prompt from user preferences if available
                negative_prompt = user_prefs.imagen_settings.get("negative_prompt", "")
                if negative_prompt:
                    print_info(f"Using negative prompt: {negative_prompt}")
                
                # Create generation config with supported parameters
                config = types.GenerateImagesConfig(
                    number_of_images=user_prefs.imagen_settings["number_of_images"],
                    aspect_ratio=aspect_ratio
                )
                
                # Add seed if specified
                if user_prefs.imagen_settings["seed"] is not None:
                    config.seed = user_prefs.imagen_settings["seed"]
                    print_info(f"Using seed: {user_prefs.imagen_settings['seed']}")
                
                # NOTE: We don't add negative_prompt directly to config anymore
                # It's already incorporated into the enhanced_prompt by the Gemini flash model
                
                # List available models first
                try:
                    available_models = client.list_models()
                    logging.info("Available models:")
                    for model in available_models:
                        logging.info(f"- {model.name}")
                except Exception as e:
                    logging.error(f"Error listing models: {e}")

                # Customize config based on user's imagen_settings
                if user_prefs.imagen_settings.get("model_version"):
                    model_version = user_prefs.imagen_settings["model_version"]
                else:
                    model_version = 'imagen-3.0-generate-002'  # Default to known working model
                
                # Log the configuration details
                # Log configuration details
                logging.info(f"Using model: {model_version}")
                logging.info(f"Aspect ratio: {aspect_ratio}")
                logging.info(f"Negative prompt: {negative_prompt}")
                logging.info(f"Number of images: {user_prefs.imagen_settings['number_of_images']}")
                if user_prefs.imagen_settings["seed"] is not None:
                    logging.info(f"Seed: {user_prefs.imagen_settings['seed']}")
                
                # Generate the image
                response = client.models.generate_images(
                    model=model_version,
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
                        logging.debug(f"Temporary image path: {temp_image_path}")
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
        error_msg = str(e)
        if "billed users" in error_msg:
            print_error("Image generation requires a Google Cloud billing account")
            print_info("Please visit https://ai.google.dev/tutorials/setup to set up billing")
        else:
            print_error(f"Error generating image: {error_msg}")
        return False
    
    # Step 4: Set the wallpaper
    try:
        print_section("Preview and Set Wallpaper")
        
        # Make sure we're using an absolute path
        if not os.path.isabs(cache_path):
            cache_path = os.path.abspath(cache_path)
        
        # Make sure the file exists before previewing/setting it
        if not os.path.exists(cache_path):
            logging.warning(f"Wallpaper file not found at {cache_path} before preview")
            print_warning(f"Wallpaper file may be missing: {cache_path}")
            return False
        
        # Check if preview should be skipped
        # Check both direct attribute and wallpaper_settings for backward compatibility
        skip_preview = getattr(user_prefs, 'skip_preview', False) or user_prefs.wallpaper_settings.get('skip_preview', False)
        
        if skip_preview:
            print_info("Preview skipped. Applying wallpaper directly...")
            logging.info("Image preview skipped due to user preference")
            set_wallpaper_confirmed = True
        else:
            print_info("Preview your new wallpaper before setting it...")
            print_info("Preview your new wallpaper before setting it...")
            logging.info(f"Previewing wallpaper with path: {cache_path}")
            
            gui_backend = user_prefs.wallpaper_settings.get('gui_preview_backend', 'qt')
            preview_func = None
            
            if gui_backend == 'qt':
                try:
                    from qt_preview import preview_image_gui as preview_func
                except ImportError:
                    print_warning("Qt preview backend selected but PySide6 (or PyQt5/6) not found.")
                    print_info("Please install PySide6: pip install PySide6")
                    print_info("Falling back to no preview.")
                    preview_func = None
            elif gui_backend == 'tkinter':
                 try:
                     from tkinter_preview import preview_image_gui as preview_func
                 except ImportError:
                     print_warning("Tkinter preview backend selected but Tkinter not available.")
                     print_info("Tkinter is usually included with Python, but may require a separate package on some Linux distributions.")
                     print_info("Falling back to no preview.")
                     preview_func = None
            else:
                print_warning(f"Unknown GUI preview backend specified: {gui_backend}. Falling back to no preview.")
                preview_func = None

            set_wallpaper_confirmed = False
            if preview_func:
                try:
                    set_wallpaper_confirmed = preview_func(cache_path, set_wallpaper)
                    if set_wallpaper_confirmed:
                        # The GUI has already set the wallpaper, so we can return
                        print_success("Wallpaper successfully applied!")
                        print_info(f"Your desktop is now displaying: {os.path.basename(cache_path)}")
                        logging.info(f"Wallpaper successfully set to: {cache_path}")
                        return True
                except Exception as e:
                    print_error(f"GUI preview failed: {e}")
                    print_info("Please check that your system supports GUI preview")
                    set_wallpaper_confirmed = False
            else:
                print_info("GUI preview is not available or failed to load. Skipping preview.")
                set_wallpaper_confirmed = False # Ensure this is False if preview isn't used

            if set_wallpaper_confirmed:
                logging.info("User confirmed to set the wallpaper after preview")
            else:
                logging.info("User decided not to set the wallpaper after preview, or preview was skipped/failed.")
        
        # If preview was skipped, failed, or user chose not to set from preview
        if not skip_preview and not set_wallpaper_confirmed:
             # If preview was attempted but user didn't confirm, or it failed
             print_info("Wallpaper not set. You can find the generated image at:")
             print_info(cache_path)
             return True # Still return True since image generation was successful
        elif set_wallpaper_confirmed:
             # If preview was skipped but set_wallpaper_confirmed is True (e.g. via CLI arg)
             result = set_wallpaper(cache_path)
             if result:
                 print_success("Wallpaper successfully applied!")
                 print_info(f"Your desktop is now displaying: {os.path.basename(cache_path)}")
                 logging.info(f"Wallpaper successfully set to: {cache_path}")
                 return True
             else:
                 print_warning("Wallpaper may not have been set correctly.")
                 print_info("Please check your desktop settings manually.")
                 return False
        elif skip_preview:
             # If preview was explicitly skipped via setting/CLI arg
             result = set_wallpaper(cache_path)
             if result:
                 print_success("Wallpaper successfully applied!")
                 print_info(f"Your desktop is now displaying: {os.path.basename(cache_path)}")
                 logging.info(f"Wallpaper successfully set to: {cache_path}")
                 return True
             else:
                 print_warning("Wallpaper may not have been set correctly.")
                 print_info("Please check your desktop settings manually.")
                 return False
        else:
             # Should not reach here if logic is correct, but as a fallback
             print_info("Wallpaper not set. You can find the generated image at:")
             print_info(cache_path)
             return True # Still return True since image generation was successful


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

def view_history():
    """View the wallpaper generation history."""
    history = GenerationHistory()
    history.view_history()

def add_to_history(entry):
    """Add an entry to the generation history."""
    history = GenerationHistory()
    history.add_entry(entry)

def configure_logging(level=logging.INFO):
    """Configure logging with file and console handlers."""
    # Configure file handler
    file_handler = logging.FileHandler("wallpaper_generator.log")
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    
    # Get root logger and clear any existing handlers
    root_logger = logging.getLogger()
    root_logger.handlers = []
    
    # Set new level and add file handler only
    root_logger.setLevel(level)
    root_logger.addHandler(file_handler)
    
    logging.debug("Logging configured with level: %s", level)

# Global flag to track if we're in the process of exiting
exiting = False

# Removed local signal handler; global handler in graceful_exit.py will manage exit.

def main():
    """Main function handling command-line arguments."""
    global user_prefs
    
    # Signal handler registration removed; handled globally by graceful_exit.py
    
    # Removed redundant atexit handler; preference saving on interrupt
    # is handled by the signal handler in graceful_exit.py.
    # Normal exit (option 5) saves preferences explicitly.
    
    args = parse_arguments()
    
    # Configure logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    configure_logging(log_level)
    
    # Import use_user_preferences and set_prompt_preferences from prompt_generator
    from prompt_generator import use_user_preferences, set_prompt_preferences
    
    # Load user preferences
    user_prefs = load_user_preferences()
    
    # Check if we should use user preferences
    if args.dont_use_user_prefs:
        # Don't use user preferences if specified
        set_prompt_preferences(False)
    
    # Apply command-line settings if provided
    if args.resolution:
        user_prefs.resolution = args.resolution
    if args.aspect_ratio:
        user_prefs.aspect_ratio = args.aspect_ratio
    
    # Store whether to skip preview
    user_prefs.skip_preview = args.skip_preview if hasattr(args, 'skip_preview') else False
    # Also update wallpaper_settings for consistency
    user_prefs.wallpaper_settings['skip_preview'] = user_prefs.skip_preview
    
    # Import preview functionality
    preview_func = None
    gui_backend = None
    try:
        gui_backend = user_prefs.wallpaper_settings.get('gui_preview_backend', 'qt')
    except Exception:
        gui_backend = 'qt'
    
    if gui_backend == 'qt':
        try:
            from qt_preview import preview_image_gui as preview_func
        except ImportError:
            print_warning("Qt preview backend selected but PySide6 (or PyQt5/6) not found.")
            print_info("Please install PySide6: pip install PySide6")
            print_info("Falling back to no preview.")
            preview_func = None
    elif gui_backend == 'tkinter':
        try:
            from tkinter_preview import preview_image_gui as preview_func
        except ImportError:
            print_warning("Tkinter preview backend selected but Tkinter not available.")
            print_info("Tkinter is usually included with Python, but may require a separate package on some Linux distributions.")
            print_info("Falling back to no preview.")
            preview_func = None
    else:
        print_warning(f"Unknown GUI preview backend specified: {gui_backend}. Falling back to no preview.")
        preview_func = None
    
    # List and preview images if requested
    if args.list_images:
        # Get list of images using helper function
        image_files = list_sorted_genimages("genimage")
        
        if not image_files:
            print_warning("No images found in the genimage directory.")
            return
        
        print_section("Generated Images")
        print_info(f"Found {len(image_files)} images in the genimage directory.")
        
        # Display the images with their numbers
        for i, image_file in enumerate(image_files, 1):
            creation_time = datetime.fromtimestamp(
                os.path.getmtime(os.path.join(genimage_dir, image_file))
            ).strftime("%Y-%m-%d %H:%M:%S")
            print(f"{i}: {image_file} - Generated: {creation_time}")
        
        # Ask user which image to preview
        try:
            choice = get_validated_input(
                f"Enter image number to preview (1-{len(image_files)}) or 'q' to quit", 
                [str(i) for i in range(1, len(image_files) + 1)] + ['q']
            )
            
            if choice.lower() == 'q':
                return
            
            # Preview the selected image
            image_path = os.path.join(genimage_dir, image_files[int(choice) - 1])
            print_info(f"Previewing image: {image_files[int(choice) - 1]}")
            
            # Use GUI preview
            if preview_func:
                result = preview_func(image_path, set_wallpaper)
            else:
                result = False
            
            # If user chooses to set as wallpaper, do so
            if result:
                print_info(f"Setting image as wallpaper: {image_path}")
                if set_wallpaper(image_path):
                    print_success("Wallpaper set successfully!")
                else:
                    print_error("Failed to set wallpaper")
            
        except (ValueError, IndexError) as e:
            print_error(f"Invalid selection: {e}")
        
        return
    
    # Preview latest image if requested
    if args.preview_latest:
        # Get the latest image in genimage directory
        genimage_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "genimage")
        try:
            image_files = sorted(
                [f for f in os.listdir(genimage_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))],
                key=lambda x: os.path.getmtime(os.path.join(genimage_dir, x)),
                reverse=True
            )
            
            if not image_files:
                print_warning("No images found in the genimage directory.")
                return
            
            # Get the latest image
            latest_image = image_files[0]
            image_path = os.path.join(genimage_dir, latest_image)
            
            print_info(f"Previewing latest image: {latest_image}")
            
            # Preview image with GUI
            if preview_func:
                result = preview_func(image_path, set_wallpaper)
            else:
                result = False
            if result:
                print_success("Wallpaper set successfully!")
            
        except (FileNotFoundError, IndexError) as e:
            print_error(f"Error accessing latest image: {e}")
        
        return
    
    # Preview specific image if requested
    if args.preview_image:
        image_path = args.preview_image
        # Use absolute path if needed
        if not os.path.isabs(image_path):
            image_path = os.path.abspath(image_path)
        
        print_info(f"Previewing image: {image_path}")
        if not os.path.exists(image_path):
            print_error(f"Image file not found: {image_path}")
            return
        
        # Preview image with GUI
        if preview_func:
            result = preview_func(image_path, set_wallpaper)
        else:
            result = False
        if result:
            print_success("Wallpaper set successfully!")
        return
    
    # Check for command-line specific operations
    if args.test_prompt:
        # Check if we should use user preferences
        if use_user_preferences:
            generated_prompt = generate_prompt_gemini([args.test_prompt], user_prefs)
        else:
            generated_prompt = generate_prompt_gemini([args.test_prompt])
        print(f"Generated prompt: {generated_prompt}")
        return
    
    if args.test_custom_prompt:
        if use_user_preferences:
            enhanced_prompt = enhance_custom_prompt(args.test_custom_prompt, user_prefs)
        else:
            enhanced_prompt = enhance_custom_prompt(args.test_custom_prompt)
        print(f"Enhanced prompt: {enhanced_prompt}")
        return
    
    if args.prompt or args.random:
        # Generate with command-line parameters
        if args.no_generate:
            # Only generate/test prompt, but don't generate image
            if args.prompt:
                if use_user_preferences:
                    enhanced_prompt = enhance_custom_prompt(args.prompt, user_prefs)
                else:
                    enhanced_prompt = enhance_custom_prompt(args.prompt)
                print(f"Enhanced prompt: {enhanced_prompt}")
            else:  # --random
                # Use select_random_tags to get a subset of tags rather than all tags
                random_tags = select_random_tags()
                if use_user_preferences:
                    gemini_prompt = generate_prompt_random(random_tags, user_prefs)
                    # Enhance the random prompt to make it more detailed
                    enhanced_prompt = enhance_custom_prompt(gemini_prompt, user_prefs)
                    print(f"Enhanced random prompt: {enhanced_prompt}")
                else:
                    gemini_prompt = generate_prompt_random(random_tags)
                    # Enhance the random prompt to make it more detailed
                    enhanced_prompt = enhance_custom_prompt(gemini_prompt)
                    print(f"Enhanced random prompt: {enhanced_prompt}")
        else:
            # Generate wallpaper
            if args.prompt:
                generate_wallpaper(prompt_type="custom", custom_prompt=args.prompt)
            else:  # --random
                generate_wallpaper(prompt_type="random")
        return
    
    # No command-line arguments provided, check dependencies and start UI
    check_dependencies()
    main_menu.run_main_menu()

def show_ascii_art():
    """Display ASCII art header."""
    print("\n" + "=" * 80)
    print(" " * 29 + "AI Wallpaper Generator" + " " * 29)
    print("=" * 80 + "\n")
    print_info("Welcome to the AI Wallpaper Generator! This tool helps you create stunning wallpapers using AI.")


def select_random_tags():
    """Select a random set of tags from all available tag categories."""
    all_tags = nature_tags + space_tags + sea_tags + flowers_tags + urban_tags + fantasy_tags + abstract_tags
    num_tags = random.randint(3, 6)  # Select between 3-6 tags
    return random.sample(all_tags, min(num_tags, len(all_tags)))

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="AI Wallpaper Generator")
    parser.add_argument("--prompt", help="Custom prompt for wallpaper generation")
    parser.add_argument("--random", action="store_true", help="Generate a random wallpaper")
    parser.add_argument("--test-prompt", help="Test prompt generation without creating an image")
    parser.add_argument("--test-custom-prompt", help="Test custom prompt enhancement")
    parser.add_argument("--resolution", help="Set resolution (e.g., '3840x2160')")
    parser.add_argument("--aspect-ratio", help="Set aspect ratio (e.g., '16:9')")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--dont-use-user-prefs", action="store_true", help="Do not use user preferences for prompt generation")
    parser.add_argument("--no-generate", action="store_true", help="Don't generate the image, just show the prompt")
    parser.add_argument("--no-preset", action="store_true", help="Skip loading the last preset on startup")
    parser.add_argument("--skip-preview", action="store_true", help="Skip the image preview and set wallpaper directly")
    parser.add_argument("--preview-image", help="Preview an image using the GUI without setting as wallpaper")
    parser.add_argument("--preview-latest", action="store_true", help="Preview the latest generated image without setting as wallpaper")
    parser.add_argument("--list-images", action="store_true", help="List all generated images and preview one by number")
    return parser.parse_args()

def load_user_preferences():
    """Load user preferences using initialize_settings from wallpaper_settings."""
    # Import here to avoid circular imports
    from wallpaper_settings import initialize_settings
    return initialize_settings()


if __name__ == "__main__":
    main()
