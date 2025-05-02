# settings_modules/menu_management/styles_menu.py

import os
import logging
from typing import List, Tuple
from ui_utils import (
    print_section, print_info, print_option, print_success, print_warning,
    print_error, get_validated_input, print_menu_options, get_menu_choice
)
from config import STYLE_CATEGORIES
from ..settings_manager import get_preferences

try:
    from prompt_generator import generate_random_style_mix
    PROMPT_GEN_AVAILABLE = True
except ImportError:
    PROMPT_GEN_AVAILABLE = False

try:
    from ai_style_generator import handle_style_generation, initialize_gemini
    AI_STYLE_GEN_AVAILABLE = True
except ImportError:
    AI_STYLE_GEN_AVAILABLE = False

def manage_styles():
    """Manage user's preferred styles for wallpaper generation."""
    user_prefs = get_preferences() # Get preferences object here
    predefined_style_categories = {
        "Artistic & Painterly": [
            "oil_painting", "watercolor", "pastel", "impressionism", "expressionism", "pointillism", "divisionism", "art_nouveau", "art_deco", "cubism", "constructivism", "futurism", "surrealism", "pop_art", "ukiyo_e", "woodcut"
        ],
        "Drawing & Sketching": [
            "pencil_sketch", "charcoal", "ink_drawing", "sketch", "line_art"
        ],
        "Digital & Modern": [
            "digital_art", "minimalist", "abstract", "geometric", "low_poly", "pixel_art", "glitch_art", "vaporwave", "retrowave"
        ],
        "Photographic & Realistic": [
            "photograph", "cinematic", "hyperrealism", "realism", "double_exposure", "landscape"
        ],
        "Illustrative & Cartoon": [
            "cartoon", "comic_book", "manga", "anime", "graffiti", "paper_cut", "stained_glass"
        ],
        "Themed & Fantasy": [
            "fantasy", "sci_fi", "cyberpunk", "steampunk", "gothic", "isometric"
        ]
    }
    while True:
        try:
            print_section("Manage Styles")
            print_info("Current preferred style:")
            if user_prefs.preferred_styles:
                print_info(f"- {user_prefs.preferred_styles}")
            else:
                print_info("No preferred style set.")

            print_section("Options")
            print_option("1", "Random Style Mix (combines 2-3 compatible styles)")
            print_option("2", "AI-Generated Style")
            print_option("3", "Custom Style")
            print_option("4", "Set style (type name)")
            print_option("5", "Clear style")
            print_option("6", "Art Movement")
            print_option("7", "Style Era")
            print_option("8", "Post-Processing Effects")
            print_option("9", "Predefined Styles")
            print_option("b", "Back")

            valid_choices = ["4", "5", "b", "1", "2", "3", "6", "7", "8", "9"]
            style_choice = get_validated_input(
                "Select an option (or type a style name to set)",
                valid_choices,
                allow_empty=True,
            )
            if style_choice == "b":
                return
            elif style_choice == "4":
                style = input("Enter style to set: ").strip()
                if style:
                    user_prefs.preferred_styles.clear()
                    user_prefs.add_style(style)
                    print_success(f"Set preferred style to '{style}'")
            elif style_choice == "5":
                confirm = get_validated_input(
                    "Are you sure you want to clear the preferred style? (y/n)", ["y", "n"]
                )
                if confirm == "y":
                    user_prefs.clear_style()
                    print_success("Cleared preferred style")
            elif style_choice == "1":
                style_mix = generate_random_style_mix()
                print_info(f"Generated random style mix: {style_mix}")
                add_to_preferences = get_validated_input(
                    "Set this mix as your preferred style? (y/n)", ["y", "n"]
                )
                if add_to_preferences == "y":
                    if style_mix:
                        user_prefs.preferred_styles.clear()
                        user_prefs.add_style(style_mix)
                        print_success(f"Set preferred style to '{style_mix}'")
                    else:
                        print_warning("Generated random style mix was empty.")
            elif style_choice == "2":
                try:
                    from ai_style_generator import handle_style_generation, initialize_gemini

                    if "GEMINI_API_KEY" in os.environ:
                        initialize_gemini(os.environ["GEMINI_API_KEY"])
                        generated_style = handle_style_generation(user_prefs)
                        if generated_style:
                            user_prefs.add_style(generated_style)
                            print_success(f"Set preferred style to '{generated_style}'")
                        else:
                            print_warning("AI style generation did not return a style.")
                    else:
                        print_error(
                            "Gemini API key not found. Please set GEMINI_API_KEY environment variable."
                        )
                except ImportError:
                    print_error(
                        "AI style generation requires google-generativeai package."
                    )
                    print_info("Install with: pip install google-generativeai")
                continue
            elif style_choice == "3":
                style = input("Enter custom style to set: ").strip()
                if style:
                    user_prefs.preferred_styles.clear()
                    user_prefs.add_style(style)
                    print_success(f"Set preferred style to '{style}'")
                continue
            elif style_choice == "6":
                while True:
                    print_info("Select art movement:")
                    print_option("0", "None (No specific art movement)")
                    print_option("1", "Abstract Expressionism")
                    print_option("2", "Impressionism")
                    print_option("3", "Surrealism")
                    print_option("4", "Cubism")
                    print_option("5", "Pop Art")
                    print_option("6", "Custom Movement")
                    print_option("b", "Back")

                    movement_choice = get_validated_input("Select art movement (0-6, b)", ["0", "1", "2", "3", "4", "5", "6", "b"])
                    if movement_choice == "b":
                        break

                    if movement_choice == "0":
                        user_prefs.imagen_settings.setdefault("style_settings", {})["art_movement"] = None
                        print_success("Art movement set to None")
                        user_prefs.save_preferences()
                        continue

                    if movement_choice == "6":
                        custom_movement = input("Enter custom art movement: ").strip()
                        if custom_movement:
                            user_prefs.imagen_settings.setdefault("style_settings", {})["art_movement"] = custom_movement
                            print_success(f"Custom art movement set to: {custom_movement}")
                            user_prefs.save_preferences()
                        continue

                    movements = {
                        "1": "Abstract Expressionism",
                        "2": "Impressionism",
                        "3": "Surrealism",
                        "4": "Cubism",
                        "5": "Pop Art"
                    }

                    user_prefs.imagen_settings.setdefault("style_settings", {})["art_movement"] = movements[movement_choice]
                    print_success(f"Art movement set to {movements[movement_choice]}")
                    user_prefs.save_preferences()
            elif style_choice == "7":
                print_info("Set Style Era (e.g., Modern, Golden Age, Silver Age, or custom):")
                print_option("1", "Modern")
                print_option("2", "Golden Age")
                print_option("3", "Silver Age")
                print_option("4", "Custom Era")
                print_option("b", "Back")
                era_choice = get_validated_input("Select style era (1-4, b)", ["1", "2", "3", "4", "b"])
                if era_choice == "b":
                    pass
                else:
                    eras = {
                        "1": "Modern",
                        "2": "Golden Age",
                        "3": "Silver Age"
                    }
                    if era_choice == "4":
                        custom_era = input("Enter custom style era: ").strip()
                        if custom_era:
                            user_prefs.imagen_settings["style_settings"]["style_era"] = custom_era
                            print_success(f"Style era set to: {custom_era}")
                            user_prefs.save_preferences()
                    else:
                        user_prefs.imagen_settings["style_settings"]["style_era"] = eras[era_choice]
                        print_success(f"Style era set to: {eras[era_choice]}")
                        user_prefs.save_preferences()
            elif style_choice == "8":
                while True:
                    print_info("Select post-processing effects:")
                    print_option("1", "Bloom Effect")
                    print_option("2", "Vignette Effect")
                    print_option("3", "Color Grading")
                    print_option("4", "Depth of Field")
                    print_option("5", "Motion Blur")
                    print_option("6", "Film Grain")
                    print_option("7", "Lens Flare")
                    print_option("8", "Chromatic Aberration")
                    print_option("9", "Sharpening")
                    print_option("10", "Tone Mapping")
                    print_option("11", "HDR Effect")
                    print_option("12", "Light Leaks")
                    print_option("13", "No Post-Processing")
                    print_option("14", "Custom Effects")
                    print_option("b", "Back")

                    effects_choice = get_validated_input("Select post-processing effects (1-14, b)", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "b"])
                    if effects_choice == "b":
                        break

                    if effects_choice == "13":
                        user_prefs.imagen_settings["style_settings"]["post_processing"] = []
                        print_success("Post-processing effects cleared")
                        user_prefs.save_preferences()
                        continue

                    if effects_choice == "14":
                        custom_effects = input("Enter custom post-processing effects (comma-separated): ").strip()
                        if custom_effects:
                            effects_list = [e.strip() for e in custom_effects.split(",")]
                            user_prefs.imagen_settings["style_settings"]["post_processing"] = effects_list
                            print_success(f"Custom post-processing effects set to: {', '.join(effects_list)}")
                            user_prefs.save_preferences()
                        continue

                    effects = {
                        "1": ["bloom"],
                        "2": ["vignette"],
                        "3": ["color_grading"],
                        "4": ["depth_of_field"],
                        "5": ["motion_blur"],
                        "6": ["film_grain"],
                        "7": ["lens_flare"],
                        "8": ["chromatic_aberration"],
                        "9": ["sharpening"],
                        "10": ["tone_mapping"],
                        "11": ["hdr"],
                        "12": ["light_leaks"]
                    }

                    user_prefs.imagen_settings["style_settings"]["post_processing"] = effects[effects_choice]
                    print_success(f"Post-processing effects set to {effects[effects_choice][0]}")
                    user_prefs.save_preferences()
            elif style_choice == "9":
                predefined_style_categories = {
                    "Artistic & Painterly": [
                        "oil_painting", "watercolor", "pastel", "impressionism", "expressionism", "pointillism", "divisionism", "art_nouveau", "art_deco", "cubism", "constructivism", "futurism", "surrealism", "pop_art", "ukiyo_e", "woodcut"
                    ],
                    "Drawing & Sketching": [
                        "pencil_sketch", "charcoal", "ink_drawing", "sketch", "line_art"
                    ],
                    "Digital & Modern": [
                        "digital_art", "minimalist", "abstract", "geometric", "low_poly", "pixel_art", "glitch_art", "vaporwave", "retrowave"
                    ],
                    "Photographic & Realistic": [
                        "photograph", "cinematic", "hyperrealism", "realism", "double_exposure", "landscape"
                    ],
                    "Illustrative & Cartoon": [
                        "cartoon", "comic_book", "manga", "anime", "graffiti", "paper_cut", "stained_glass"
                    ],
                    "Themed & Fantasy": [
                        "fantasy", "sci_fi", "cyberpunk", "steampunk", "gothic", "isometric"
                    ]
                }
                while True:
                    print_info("Select a style category:")
                    categories = list(predefined_style_categories.keys())
                    for i, category in enumerate(categories, start=1):
                        print_info(f"{i}. {category}")
                    print_option("b", "Back")

                    cat_choice = input("Enter category number or 'b' to go back: ").strip()
                    if cat_choice == "b":
                        break
                    if not cat_choice.isdigit():
                        print_warning("Invalid input. Please enter a number or 'b'.")
                        continue
                    cat_index = int(cat_choice)
                    if cat_index < 1 or cat_index > len(categories):
                        print_warning("Invalid number. Please select a valid category number.")
                        continue

                    selected_category = categories[cat_index - 1]
                    styles_in_category = predefined_style_categories[selected_category]

                    while True:
                        print_info(f"Select a style from '{selected_category}':")
                        for j, style in enumerate(styles_in_category, start=1):
                            print_info(f"{j}. {style}")
                        print_option("b", "Back")

                        style_choice_sub = input("Enter style number or 'b' to go back: ").strip()
                        if style_choice_sub == "b":
                            break
                        if not style_choice_sub.isdigit():
                            print_warning("Invalid input. Please enter a number or 'b'.")
                            continue
                        style_index = int(style_choice_sub)
                        if style_index < 1 or style_index > len(styles_in_category):
                            print_warning("Invalid number. Please select a valid style number.")
                            continue

                        selected_style = styles_in_category[style_index - 1]
                        user_prefs.preferred_styles.clear()
                        user_prefs.add_style(selected_style)
                        print_success(f"Set preferred style to '{selected_style}'")
                        user_prefs.save_preferences()
                        break
                continue
        except Exception as e:
            print_error(f"An error occurred: {e}")
            return
