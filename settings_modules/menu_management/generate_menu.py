"""
Generate menu module for wallpaper generation.

This module provides functionality for generating wallpapers and prompts,
including options to use Gemini AI, random prompts, or custom prompts.
"""

from typing import List, Tuple, Dict, Any, Optional
from ui_utils import (
    print_section, print_menu_options, get_menu_choice, 
    print_info, print_warning, print_success, print_breadcrumb,
    get_validated_input, show_spinner
)

# Import from other internal modules
from settings_modules.settings_manager import get_preferences
from settings_modules.preset_management import load_preset
from settings_modules.menu_management.advanced_options_menu import configure_advanced_options
from prompt_generator import (
    use_user_preferences, enhance_custom_prompt, 
    generate_random_style_mix
)

def run_generate_menu(generate_only: bool = False):
    """
    Run the Generate menu for wallpaper or prompt generation.
    
    Args:
        generate_only: If True, only generate the prompt without creating an image
    
    Returns:
        None
    """
    section_title = "Generate Prompt Only" if generate_only else "Generate AI Wallpaper"
    breadcrumb = ["Main Menu", section_title]
    
    menu_options: List[Tuple[str, str]] = [
        ("1", "Use Gemini AI to generate a prompt"),
        ("2", "Use a random prompt"),
        ("3", "Enter your own custom prompt"),
        ("4", "Advanced Options - Fine-tune generation parameters"),
        ("5", "Load Saved Preset"),
        ("6", "Return to Main Menu")
    ]
    
    while True:
        print_section(section_title)
        print_breadcrumb(breadcrumb)
        print_menu_options(menu_options)
        
        choice = get_menu_choice("Select option (1-6)", ["1", "2", "3", "4", "5", "6"])
        if choice == "_INTERRUPTED_":
            return  # Exit if interrupted
            
        if choice == "6":
            return
            
        if choice == "5":
            # Load preset menu
            settings = load_preset()
            if settings:
                from wallpaper_generator import generate_wallpaper
                generate_wallpaper(**settings)
            continue
            
        if choice == "4":
            # Advanced options menu
            configure_advanced_options()
            continue
            
        if choice in ["1", "2", "3"]:
            if choice == "1":
                handle_gemini_generation(generate_only)
            elif choice == "2":
                handle_random_generation(generate_only)
            elif choice == "3":
                handle_custom_generation(generate_only)


def handle_gemini_generation(generate_only: bool):
    """Handle Gemini AI prompt generation."""
    # Get mood and style preferences for this generation
    print_section("Optional Parameters")
    print_info("You can specify a mood and style for your wallpaper (leave empty to use random)")
    
    # Define available options
    mood_options = [
        "peaceful", "dramatic", "mysterious", "energetic", "melancholic",
        "joyful", "romantic", "eerie", "nostalgic", "contemplative"
    ]
    
    style_options = [
        "abstract", "anime", "art_deco", "art_nouveau", "cartoon", "charcoal",
        "cinematic", "comic_book", "constructivism", "cubism", "cyberpunk",
        "digital_art", "divisionism", "double_exposure", "expressionism",
        "fantasy", "futurism", "glitch_art", "gothic", "graffiti",
        "hyperrealism", "impressionism", "ink_drawing", "isometric", "landscape",
        "line_art", "low_poly", "manga", "minimalist", "oil_painting",
        "paper_cut", "pastel", "pencil_sketch", "photograph", "pixel_art",
        "pointillism", "pop_art", "realism", "retrowave", "sci_fi",
        "sketch", "stained_glass", "steampunk", "surrealism", "ukiyo_e",
        "vaporwave", "watercolor", "woodcut"
    ]
    
    # Get user inputs for mood and style
    print_info(f"Mood options: {', '.join(mood_options)}")
    mood = input("Enter mood (optional): ").strip().lower()
    if mood and mood not in mood_options:
        print_warning(f"'{mood}' is not in the suggested moods, but we'll try to use it anyway")
    
    print_info(f"Style options: {', '.join(style_options)}")
    print_info("You can also enter 'random_mix' to combine 2-3 compatible styles for creative results")
    style = input("Enter style (optional): ").strip().lower()
    
    user_prefs = get_preferences()
    
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
    
    # Now call the generator function
    from wallpaper_generator import generate_wallpaper
    generate_wallpaper("gemini", mood=mood, style=style, generate_only=generate_only)


def handle_random_generation(generate_only: bool):
    """Handle random prompt generation."""
    from wallpaper_generator import generate_wallpaper
    generate_wallpaper("random", generate_only=generate_only)


def handle_custom_generation(generate_only: bool):
    """Handle custom prompt entry and generation."""
    custom_prompt = get_validated_input("Enter your custom prompt (or 'b' to go back)", allow_empty=False)
    if custom_prompt.lower() == 'b':
        return
        
    print_info("Processing custom prompt...")
    from wallpaper_generator import generate_wallpaper
    generate_wallpaper("custom", custom_prompt=custom_prompt, generate_only=generate_only)
