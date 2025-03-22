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
    """Class to store and manage user preferences."""
    def __init__(self):
        self.preferred_genres = []
        self.preferred_styles = []
        self.preferred_moods = []
        self.aspect_ratio = "16:9"
        self.negative_prompts = []
        # Add new Imagen 3 specific settings
        self.imagen_settings = {
            "number_of_images": 1,  # Number of images to generate (1-4)
            "seed": None,  # Optional seed for reproducible results
            "aspect_ratio": "16:9",  # Supported ratios: 16:9, 21:9, 4:3, 1:1, 9:16
            "negative_prompt": ""  # Optional negative prompt
        }
        # Add wallpaper settings
        self.wallpaper_settings = {
            "auto_set": True,  # Whether to automatically set wallpaper after generation
            "cache_duration": 30,  # Days to keep cached images
            "fit_mode": "fill",  # fill, fit, center, tile
            "background_color": "#000000",  # Background color for non-filling modes
            "multi_monitor": "mirror",  # mirror, extend, individual
            "refresh_rate": "daily",  # daily, weekly, monthly, never
            "last_refresh": None,  # Timestamp of last refresh
        }
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
                    # Load Imagen 3 settings
                    if "imagen_settings" in prefs:
                        self.imagen_settings.update(prefs["imagen_settings"])
                    # Load wallpaper settings
                    if "wallpaper_settings" in prefs:
                        self.wallpaper_settings.update(prefs["wallpaper_settings"])
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
                "negative_prompts": self.negative_prompts,
                "imagen_settings": self.imagen_settings,
                "wallpaper_settings": self.wallpaper_settings
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
        # Add style-specific instructions
        if style == "digital_art":
            prompt_parts.append("Style instructions: Create a digital art piece with stylized rendering, artistic effects, and creative composition. Focus on artistic elements rather than photorealism.")
        elif style == "sketch":
            prompt_parts.append("Style instructions: Create a sketch-like artwork with hand-drawn qualities, line work, and artistic shading. Emphasize the sketchy, artistic nature.")
        elif style == "watercolor":
            prompt_parts.append("Style instructions: Create a watercolor painting effect with color blending, transparency, and artistic texture. Focus on watercolor characteristics.")
        elif style == "cyberpunk":
            prompt_parts.append("Style instructions: Create a cyberpunk-style artwork with futuristic elements, neon lighting, and technological details. Focus on high-tech and dystopian elements.")
        elif style == "pop_art":
            prompt_parts.append("Style instructions: Create a pop art piece with bold colors, graphic elements, and cultural references. Focus on vibrant, graphic style.")
    
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
            return True
        elif os_name == "Darwin":
            script = f'tell application "Finder" to set desktop picture to POSIX file "{image_path}"'
            command = f"osascript -e '{script}'"
            subprocess.run(shlex.split(command), check=True, capture_output=True, text=True)
            logging.info("Wallpaper set successfully on macOS")
            return True
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
                logging.info("Wallpaper set successfully on Linux")
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
        resolution = user_prefs.imagen_settings.get("resolution", "1920x1080")
        aspect_ratio = user_prefs.aspect_ratio
        color_scheme = user_prefs.imagen_settings.get("color_scheme", "natural")
        lighting = user_prefs.imagen_settings.get("lighting", "natural")
        composition = user_prefs.imagen_settings.get("composition", "rule_of_thirds")
        depth_of_field = user_prefs.imagen_settings.get("depth_of_field", "medium")
        
        # Format the custom prompt instructions with user preferences
        enhancement_instructions = CUSTOM_PROMPT_INSTRUCTIONS.format(
            style=style,
            mood=mood,
            resolution=resolution,
            aspect_ratio=aspect_ratio,
            color_scheme=color_scheme,
            lighting=lighting,
            composition=composition,
            depth_of_field=depth_of_field
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
        print_option("1", "Style Settings")
        print_option("2", "Mood & Atmosphere")
        print_option("3", "Technical Parameters")
        print_option("4", "Composition & Lighting")
        print_option("5", "Show Current Settings")
        print_option("6", "Customize All Parameters")
        print_option("7", "Return to previous menu")
        
        advanced_choice = get_validated_input("Select option (1-7)", ["1", "2", "3", "4", "5", "6", "7"])
        
        if advanced_choice == "1":
            print_section("Style Settings")
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
            print_option("11", "Custom Style")
            print_option("12", "Return")
            
            style_choice = get_validated_input("Select style (1-12)", [str(i) for i in range(1, 13)])
            if style_choice == "12":
                continue
                
            if style_choice == "11":
                custom_style = input("Enter your custom style: ").strip()
                if custom_style:
                    user_prefs.preferred_styles = [custom_style]
                    print_success(f"Custom style set to: {custom_style}")
                continue
                
            styles = {
                "1": "photorealistic",
                "2": "digital_art",
                "3": "sketch",
                "4": "watercolor",
                "5": "cyberpunk",
                "6": "pop_art",
                "7": "oil_painting",
                "8": "pixel_art",
                "9": "anime",
                "10": "3d_render"
            }
            
            selected_style = styles[style_choice]
            user_prefs.preferred_styles = [selected_style]
            print_success(f"Style set to {selected_style}")
            
        elif advanced_choice == "2":
            print_section("Mood & Atmosphere")
            print_info("Set the mood and atmosphere for your wallpaper:")
            print_option("1", "Peaceful & Serene")
            print_option("2", "Dramatic & Epic")
            print_option("3", "Mysterious & Enigmatic")
            print_option("4", "Energetic & Dynamic")
            print_option("5", "Melancholic & Thoughtful")
            print_option("6", "Joyful & Vibrant")
            print_option("7", "Romantic & Dreamy")
            print_option("8", "Eerie & Haunting")
            print_option("9", "Nostalgic & Retro")
            print_option("10", "Futuristic & Sci-fi")
            print_option("11", "Custom Mood")
            print_option("12", "Return")
            
            mood_choice = get_validated_input("Select mood (1-12)", [str(i) for i in range(1, 13)])
            if mood_choice == "12":
                continue
                
            if mood_choice == "11":
                custom_mood = input("Enter your custom mood: ").strip()
                if custom_mood:
                    user_prefs.preferred_moods = [custom_mood]
                    print_success(f"Custom mood set to: {custom_mood}")
                continue
                
            moods = {
                "1": "peaceful",
                "2": "dramatic",
                "3": "mysterious",
                "4": "energetic",
                "5": "melancholic",
                "6": "joyful",
                "7": "romantic",
                "8": "eerie",
                "9": "nostalgic",
                "10": "futuristic"
            }
            
            selected_mood = moods[mood_choice]
            user_prefs.preferred_moods = [selected_mood]
            print_success(f"Mood set to {selected_mood}")
            
        elif advanced_choice == "3":
            print_section("Technical Parameters")
            print_info("Configure technical aspects of the generation:")
            print_option("1", "Aspect Ratio")
            print_option("2", "Resolution")
            print_option("3", "Color Scheme")
            print_option("4", "Custom Technical Parameters")
            print_option("5", "Return")
            
            tech_choice = get_validated_input("Select parameter (1-5)", ["1", "2", "3", "4", "5"])
            if tech_choice == "5":
                continue
                
            if tech_choice == "4":
                print_info("Enter custom technical parameters (leave blank to skip):")
                custom_res = input("Custom resolution (e.g., 1920x1080): ").strip()
                custom_ratio = input("Custom aspect ratio (e.g., 16:9): ").strip()
                custom_color = input("Custom color scheme: ").strip()
                
                if custom_res:
                    user_prefs.imagen_settings["resolution"] = custom_res
                if custom_ratio:
                    user_prefs.aspect_ratio = custom_ratio
                if custom_color:
                    user_prefs.imagen_settings["color_scheme"] = custom_color
                    
                print_success("Custom technical parameters updated")
                continue
                
            if tech_choice == "1":
                print_info("Select aspect ratio:")
                print_option("1", "16:9 (Widescreen)")
                print_option("2", "21:9 (Ultrawide)")
                print_option("3", "4:3 (Standard)")
                print_option("4", "1:1 (Square)")
                print_option("5", "9:16 (Portrait)")
                ratio_choice = get_validated_input("Select aspect ratio (1-5)", ["1", "2", "3", "4", "5"])
                aspect_ratio = ["16:9", "21:9", "4:3", "1:1", "9:16"][int(ratio_choice) - 1]
                user_prefs.aspect_ratio = aspect_ratio
                print_success(f"Aspect ratio set to {aspect_ratio}")
                
            elif tech_choice == "2":
                print_info("Select resolution:")
                print_option("1", "1920x1080 (Full HD)")
                print_option("2", "2560x1440 (2K)")
                print_option("3", "3840x2160 (4K)")
                print_option("4", "5120x2880 (5K)")
                print_option("5", "Custom")
                res_choice = get_validated_input("Select resolution (1-5)", ["1", "2", "3", "4", "5"])
                if res_choice == "5":
                    custom_res = input("Enter custom resolution (e.g., 1920x1080): ").strip()
                    if "x" in custom_res:
                        user_prefs.imagen_settings["resolution"] = custom_res
                        print_success(f"Resolution set to {custom_res}")
                else:
                    resolutions = ["1920x1080", "2560x1440", "3840x2160", "5120x2880"]
                    user_prefs.imagen_settings["resolution"] = resolutions[int(res_choice) - 1]
                    print_success(f"Resolution set to {resolutions[int(res_choice) - 1]}")
                    
            elif tech_choice == "3":
                print_info("Select color scheme:")
                print_option("1", "Warm colors")
                print_option("2", "Cool colors")
                print_option("3", "Monochromatic")
                print_option("4", "Vibrant colors")
                print_option("5", "Pastel colors")
                print_option("6", "Neutral colors")
                print_option("7", "High contrast")
                print_option("8", "Low contrast")
                print_option("9", "Custom")
                print_option("10", "Return")
                
                color_choice = get_validated_input("Select color scheme (1-10)", [str(i) for i in range(1, 11)])
                if color_choice == "10":
                    continue
                    
                if color_choice == "9":
                    custom_color = input("Enter custom color scheme: ").strip()
                    if custom_color:
                        user_prefs.imagen_settings["color_scheme"] = custom_color
                        print_success(f"Custom color scheme set to: {custom_color}")
                    continue
                    
                color_schemes = {
                    "1": "warm",
                    "2": "cool",
                    "3": "monochromatic",
                    "4": "vibrant",
                    "5": "pastel",
                    "6": "neutral",
                    "7": "high_contrast",
                    "8": "low_contrast"
                }
                
                selected_scheme = color_schemes[color_choice]
                user_prefs.imagen_settings["color_scheme"] = selected_scheme
                print_success(f"Color scheme set to {selected_scheme}")
                
        elif advanced_choice == "4":
            print_section("Composition & Lighting")
            print_info("Configure composition and lighting settings:")
            print_option("1", "Composition Style")
            print_option("2", "Lighting Type")
            print_option("3", "Depth of Field")
            print_option("4", "Custom Lighting")
            print_option("5", "Return")
            
            comp_choice = get_validated_input("Select parameter (1-5)", ["1", "2", "3", "4", "5"])
            if comp_choice == "5":
                continue
                
            if comp_choice == "4":
                print_info("Enter custom lighting settings (leave blank to skip):")
                custom_lighting = input("Custom lighting type: ").strip()
                custom_composition = input("Custom composition style: ").strip()
                custom_dof = input("Custom depth of field: ").strip()
                
                if custom_lighting:
                    user_prefs.imagen_settings["lighting"] = custom_lighting
                if custom_composition:
                    user_prefs.imagen_settings["composition"] = custom_composition
                if custom_dof:
                    user_prefs.imagen_settings["depth_of_field"] = custom_dof
                    
                print_success("Custom lighting settings updated")
                continue
                
            if comp_choice == "1":
                print_info("Select composition style:")
                print_option("1", "Rule of Thirds")
                print_option("2", "Centered")
                print_option("3", "Leading Lines")
                print_option("4", "Symmetrical")
                print_option("5", "Asymmetrical")
                print_option("6", "Framed")
                print_option("7", "Custom")
                print_option("8", "Return")
                
                comp_style = get_validated_input("Select composition style (1-8)", [str(i) for i in range(1, 9)])
                if comp_style == "8":
                    continue
                    
                if comp_style == "7":
                    custom_comp = input("Enter custom composition style: ").strip()
                    if custom_comp:
                        user_prefs.imagen_settings["composition"] = custom_comp
                        print_success(f"Custom composition style set to: {custom_comp}")
                    continue
                    
                compositions = {
                    "1": "rule_of_thirds",
                    "2": "centered",
                    "3": "leading_lines",
                    "4": "symmetrical",
                    "5": "asymmetrical",
                    "6": "framed"
                }
                
                user_prefs.imagen_settings["composition"] = compositions[comp_style]
                print_success(f"Composition style set to {compositions[comp_style]}")
                
            elif comp_choice == "2":
                print_info("Select lighting type:")
                print_option("1", "Natural Light")
                print_option("2", "Studio Light")
                print_option("3", "Dramatic Light")
                print_option("4", "Soft Light")
                print_option("5", "Harsh Light")
                print_option("6", "Volumetric Light")
                print_option("7", "Custom")
                print_option("8", "Return")
                
                light_choice = get_validated_input("Select lighting type (1-8)", [str(i) for i in range(1, 9)])
                if light_choice == "8":
                    continue
                    
                if light_choice == "7":
                    custom_light = input("Enter custom lighting type: ").strip()
                    if custom_light:
                        user_prefs.imagen_settings["lighting"] = custom_light
                        print_success(f"Custom lighting type set to: {custom_light}")
                    continue
                    
                lighting_types = {
                    "1": "natural",
                    "2": "studio",
                    "3": "dramatic",
                    "4": "soft",
                    "5": "harsh",
                    "6": "volumetric"
                }
                
                user_prefs.imagen_settings["lighting"] = lighting_types[light_choice]
                print_success(f"Lighting type set to {lighting_types[light_choice]}")
                
            elif comp_choice == "3":
                print_info("Select depth of field:")
                print_option("1", "Shallow (f/1.8)")
                print_option("2", "Medium (f/4)")
                print_option("3", "Deep (f/8)")
                print_option("4", "Custom")
                print_option("5", "Return")
                
                dof_choice = get_validated_input("Select depth of field (1-5)", ["1", "2", "3", "4", "5"])
                if dof_choice == "5":
                    continue
                    
                if dof_choice == "4":
                    custom_dof = input("Enter custom depth of field: ").strip()
                    if custom_dof:
                        user_prefs.imagen_settings["depth_of_field"] = custom_dof
                        print_success(f"Custom depth of field set to: {custom_dof}")
                    continue
                    
                dof_settings = {
                    "1": "shallow",
                    "2": "medium",
                    "3": "deep"
                }
                
                user_prefs.imagen_settings["depth_of_field"] = dof_settings[dof_choice]
                print_success(f"Depth of field set to {dof_settings[dof_choice]}")
                
        elif advanced_choice == "5":
            print_section("Current Settings")
            print_info("Style Settings:")
            print_info(f"- Current Style: {user_prefs.preferred_styles[0] if user_prefs.preferred_styles else 'Not set'}")
            
            print_info("\nMood & Atmosphere:")
            print_info(f"- Current Mood: {user_prefs.preferred_moods[0] if user_prefs.preferred_moods else 'Not set'}")
            
            print_info("\nTechnical Parameters:")
            print_info(f"- Aspect Ratio: {user_prefs.aspect_ratio}")
            print_info(f"- Resolution: {user_prefs.imagen_settings.get('resolution', 'Not set')}")
            print_info(f"- Color Scheme: {user_prefs.imagen_settings.get('color_scheme', 'Not set')}")
            
            print_info("\nComposition & Lighting:")
            print_info(f"- Composition Style: {user_prefs.imagen_settings.get('composition', 'Not set')}")
            print_info(f"- Lighting Type: {user_prefs.imagen_settings.get('lighting', 'Not set')}")
            print_info(f"- Depth of Field: {user_prefs.imagen_settings.get('depth_of_field', 'Not set')}")
            
        elif advanced_choice == "6":
            print_section("Customize All Parameters")
            print_info("Enter custom values for all parameters (leave blank to keep current):")
            
            # Style
            custom_style = input("Custom style: ").strip()
            if custom_style:
                user_prefs.preferred_styles = [custom_style]
            
            # Mood
            custom_mood = input("Custom mood: ").strip()
            if custom_mood:
                user_prefs.preferred_moods = [custom_mood]
            
            # Technical Parameters
            custom_res = input("Custom resolution (e.g., 1920x1080): ").strip()
            if custom_res:
                user_prefs.imagen_settings["resolution"] = custom_res
                
            custom_ratio = input("Custom aspect ratio (e.g., 16:9): ").strip()
            if custom_ratio:
                user_prefs.aspect_ratio = custom_ratio
                
            custom_color = input("Custom color scheme: ").strip()
            if custom_color:
                user_prefs.imagen_settings["color_scheme"] = custom_color
            
            # Composition & Lighting
            custom_comp = input("Custom composition style: ").strip()
            if custom_comp:
                user_prefs.imagen_settings["composition"] = custom_comp
                
            custom_light = input("Custom lighting type: ").strip()
            if custom_light:
                user_prefs.imagen_settings["lighting"] = custom_light
                
            custom_dof = input("Custom depth of field: ").strip()
            if custom_dof:
                user_prefs.imagen_settings["depth_of_field"] = custom_dof
            
            print_success("All custom parameters updated")
            
        elif advanced_choice == "7":
            break
            
        user_prefs.save_preferences()

def generate_wallpaper(prompt_type=None, custom_prompt=None, mood=None, style=None, resolution=None, color_scheme=None, lighting=None):
    """Generate a wallpaper based on the specified parameters.
    
    Args:
        prompt_type: Type of prompt ("custom", "random", or "gemini")
        custom_prompt: Custom prompt text if prompt_type is "custom"
        mood: Optional mood for the wallpaper
        style: Optional style for the wallpaper
        resolution: Optional resolution (e.g., "1920x1080")
        color_scheme: Optional color scheme (e.g., "warm", "cool")
        lighting: Optional lighting style (e.g., "soft", "harsh")
    """
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
        
        # Enhance prompt with additional parameters if provided
        if resolution or color_scheme or lighting:
            print_info("Enhancing prompt with additional parameters...")
            additional_params = []
            if resolution:
                additional_params.append(f"resolution: {resolution}")
            if color_scheme:
                additional_params.append(f"color scheme: {color_scheme}")
            if lighting:
                additional_params.append(f"lighting: {lighting}")
            
            enhanced_prompt = f"{enhanced_prompt}, with {', '.join(additional_params)}"
            print_info("Enhanced prompt with additional parameters:")
    
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
                            image_path = f"generated_image_{i}.png"
                            with open(image_path, "wb") as f:
                                f.write(generated_image.image.image_bytes)
                        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
                        os.rename(image_path, cache_path)
                        print_success("Image generated successfully!")
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
            style_options = ["photograph", "digital_art", "landscape", "sketch", 
                               "watercolor", "cyberpunk", "pop_art"]
            for i, style in enumerate(style_options, 1):
                print_option(str(i), style)
            
            print_option("a", "Add style")
            print_option("r", "Remove style")
            print_option("c", "Clear all")
            print_option("b", "Back")
            
            action = get_validated_input("Select action", ["a", "r", "c", "b"] + [str(i) for i in range(1, len(style_options) + 1)])
            
            if action == "a":
                style = input("Enter style to add: ").strip()
                if style in style_options and style not in user_prefs.preferred_styles:
                    user_prefs.preferred_styles.append(style)
                    print_success(f"Added style: {style}")
                else:
                    print_warning("Invalid style or already in preferences")
            elif action == "r":
                if user_prefs.preferred_styles:
                    print_info("Select style to remove:")
                    for i, style in enumerate(user_prefs.preferred_styles, 1):
                        print_option(str(i), style)
                    idx = int(get_validated_input("Enter number", [str(i) for i in range(1, len(user_prefs.preferred_styles) + 1)])) - 1
                    removed = user_prefs.preferred_styles.pop(idx)
                    print_success(f"Removed style: {removed}")
                else:
                    print_warning("No styles to remove")
            elif action == "c":
                user_prefs.preferred_styles.clear()
                print_success("Cleared all styles")
            elif action == "b":
                continue
            else:
                idx = int(action) - 1
                if 0 <= idx < len(style_options):
                    style = style_options[idx]
                    if style not in user_prefs.preferred_styles:
                        user_prefs.preferred_styles.append(style)
                        print_success(f"Added style: {style}")
                    else:
                        print_warning("Style already in preferences")
        
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
                    "negative_prompt": ""
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

def main():
    """Main function to execute the script."""
    try:
        # Check dependencies
        check_dependencies()
        
        print_header("AI Wallpaper Generator")
        print_info("Welcome to the AI Wallpaper Generator! This tool helps you create stunning wallpapers using AI.")
        
        while True:
            print_section("Main Menu")
            print_option("1", "Generate AI Wallpaper - Create custom wallpapers using AI")
            print_option("2", "Manage Preferences - Customize wallpaper settings")
            print_option("3", "Manage Imagen 3 Settings - Fine-tune AI generation")
            print_option("4", "Exit - Save and exit")
            
            try:
                choice = get_validated_input("Select an option (1-4)", ["1", "2", "3", "4"])
            except KeyboardInterrupt:
                print_info("\nSaving preferences before exit...")
                user_prefs.save_preferences()
                print_success("Goodbye!")
                sys.exit(0)
            
            if choice == "1":
                print_section("Generate AI Wallpaper")
                print_option("1", "Use Gemini AI to generate a prompt")
                print_option("2", "Use a random prompt")
                print_option("3", "Enter your own custom prompt")
                print_option("4", "Advanced Options - Fine-tune generation parameters")
                print_option("5", "Return to Main Menu")
                
                try:
                    prompt_choice = get_validated_input("Select prompt type (1-5)", ["1", "2", "3", "4", "5"])
                except KeyboardInterrupt:
                    print_info("\nSaving preferences before exit...")
                    user_prefs.save_preferences()
                    print_success("Goodbye!")
                    sys.exit(0)
                
                if prompt_choice == "1":
                    # Get mood and style preferences for this generation
                    print_section("Optional Parameters")
                    print_info("You can specify a mood and style for your wallpaper (leave empty to use random)")
                    
                    mood_options = ["peaceful", "dramatic", "mysterious", "energetic", "melancholic",
                                   "joyful", "romantic", "eerie", "nostalgic", "contemplative"]
                    style_options = ["photograph", "digital_art", "landscape", "sketch", 
                                   "watercolor", "cyberpunk", "pop_art"]
                    
                    print_info(f"Mood options: {', '.join(mood_options)}")
                    try:
                        mood = input("Enter mood (optional): ").strip().lower()
                    except KeyboardInterrupt:
                        print_info("\nSaving preferences before exit...")
                        user_prefs.save_preferences()
                        print_success("Goodbye!")
                        sys.exit(0)
                        
                    if mood and mood not in mood_options:
                        print_warning(f"'{mood}' is not in the suggested moods, but we'll try to use it anyway")
                    
                    print_info(f"Style options: {', '.join(style_options)}")
                    try:
                        style = input("Enter style (optional): ").strip().lower()
                    except KeyboardInterrupt:
                        print_info("\nSaving preferences before exit...")
                        user_prefs.save_preferences()
                        print_success("Goodbye!")
                        sys.exit(0)
                        
                    if style and style not in style_options:
                        print_warning(f"'{style}' is not in the suggested styles, but we'll try to use it anyway")
                    
                    # Add more customization options
                    print_section("Advanced Settings")
                    print_info("You can specify additional parameters for the generation:")
                    print_option("1", "Use default settings")
                    print_option("2", "Customize settings")
                    
                    try:
                        settings_choice = get_validated_input("Select settings option (1-2)", ["1", "2"])
                    except KeyboardInterrupt:
                        print_info("\nSaving preferences before exit...")
                        user_prefs.save_preferences()
                        print_success("Goodbye!")
                        sys.exit(0)
                        
                    if settings_choice == "2":
                        print_info("Enter values for the following parameters (leave blank for default):")
                        try:
                            resolution = input("Resolution (e.g., 1920x1080): ").strip()
                            color_scheme = input("Color scheme (e.g., warm, cool, monochromatic): ").strip()
                            lighting = input("Lighting (e.g., soft, harsh, volumetric): ").strip()
                        except KeyboardInterrupt:
                            print_info("\nSaving preferences before exit...")
                            user_prefs.save_preferences()
                            print_success("Goodbye!")
                            sys.exit(0)
                        # Add these parameters to the generation
                        generate_wallpaper("gemini", mood=mood, style=style,
                                         resolution=resolution, color_scheme=color_scheme, lighting=lighting)
                    else:
                        generate_wallpaper("gemini", mood=mood, style=style)
                    
                elif prompt_choice == "2":
                    generate_wallpaper("random")
                elif prompt_choice == "3":
                    try:
                        custom_prompt = get_validated_input("Enter your custom prompt", allow_empty=False)
                    except KeyboardInterrupt:
                        print_info("\nSaving preferences before exit...")
                        user_prefs.save_preferences()
                        print_success("Goodbye!")
                        sys.exit(0)
                    generate_wallpaper("custom", custom_prompt=custom_prompt)
                elif prompt_choice == "4":
                    configure_advanced_options()
            
            elif choice == "2":
                manage_preferences()
            
            elif choice == "3":
                manage_imagen_settings()
            
            elif choice == "4":
                print_header("Thank you for using AI Wallpaper Generator!")
                break
                
    except KeyboardInterrupt:
        print_info("\nSaving preferences before exit...")
        user_prefs.save_preferences()
        print_success("Goodbye!")
        sys.exit(0)
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        print_info("Saving preferences before exit...")
        user_prefs.save_preferences()
        sys.exit(1)

if __name__ == "__main__":
    main()
