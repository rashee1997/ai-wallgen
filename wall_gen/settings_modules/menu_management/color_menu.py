from wall_gen.ui_utils import (
    print_section,
    print_option,
    print_info,
    print_success,
    print_warning,
    print_error,
    get_validated_input,
    clear_screen, # Added
    print_header, # Added
)
from ..settings_manager import get_preferences


def manage_color_settings():
    """Manage color and detail settings."""
    user_prefs = get_preferences()
    while True:
        clear_screen()
        print_header("Color & Detail Settings")
        # print_section("Color & Detail Settings") # Replaced by print_header
        print_option("1", "Color Scheme")
        print_option("2", "Palette Type")
        print_option("3", "Color Temperature")
        print_option("4", "Detail Level")
        print_option("5", "Texture Quality")
        print_option("b", "Back")

        choice = get_validated_input(
            prompt="Select an option", 
            options=["1", "2", "3", "4", "5", "b"],
            help_context_id="COLOR_DETAIL_MENU"
        )
        if choice == "_HELP_SHOWN_":
            continue
        if choice == "b":
            return

        if choice == "1":
            print_info("Select color scheme:")
            print_option("1", "Monochromatic")
            print_option("2", "Complementary")
            print_option("3", "Analogous")
            print_option("4", "Triadic")
            print_option("5", "Split Complementary")
            print_option("6", "Tetradic")
            print_option("7", "Custom")
            print_option("b", "Back")

            scheme_choice = get_validated_input(
                prompt="Select color scheme", 
                options=["1", "2", "3", "4", "5", "6", "7", "b"],
                help_context_id="COLOR_SCHEME_CHOICE"
            )
            if scheme_choice == "_HELP_SHOWN_":
                continue
            if scheme_choice == "b":
                continue

            schemes = {
                "1": "monochromatic",
                "2": "complementary",
                "3": "analogous",
                "4": "triadic",
                "5": "split_complementary",
                "6": "tetradic",
            }

            if scheme_choice == "7":
                custom_scheme = input("Enter custom color scheme: ").strip()
                if custom_scheme:
                    user_prefs.imagen_settings["color_settings"][
                        "color_scheme"
                    ] = custom_scheme
                    print_success(f"Color scheme set to: {custom_scheme}")
            else:
                user_prefs.imagen_settings["color_settings"]["color_scheme"] = schemes[
                    scheme_choice
                ]
                print_success(f"Color scheme set to: {schemes[scheme_choice]}")

            user_prefs.save_preferences()

        elif choice == "2":
            print_info("Select palette type:")
            print_option("1", "Warm")
            print_option("2", "Cool")
            print_option("3", "Neutral")
            print_option("4", "Pastel")
            print_option("5", "Vibrant")
            print_option("6", "Muted")
            print_option("7", "Custom")
            print_option("b", "Back")

            palette_choice = get_validated_input(
                prompt="Select palette type", 
                options=["1", "2", "3", "4", "5", "6", "7", "b"],
                help_context_id="COLOR_PALETTE_TYPE_CHOICE"
            )
            if palette_choice == "_HELP_SHOWN_":
                continue
            if palette_choice == "b":
                continue

            palettes = {
                "1": "warm",
                "2": "cool",
                "3": "neutral",
                "4": "pastel",
                "5": "vibrant",
                "6": "muted",
            }

            if palette_choice == "7":
                custom_palette = input("Enter custom palette type: ").strip()
                if custom_palette:
                    user_prefs.imagen_settings["color_settings"][
                        "palette_type"
                    ] = custom_palette
                    print_success(f"Palette type set to: {custom_palette}")
            else:
                user_prefs.imagen_settings["color_settings"]["palette_type"] = palettes[
                    palette_choice
                ]
                print_success(f"Palette type set to: {palettes[palette_choice]}")

            user_prefs.save_preferences()

        elif choice == "3":
            print_info("Select color temperature:")
            print_option("1", "Warm (Red/Yellow)")
            print_option("2", "Cool (Blue/Cyan)")
            print_option("3", "Neutral")
            print_option("4", "Mixed")
            print_option("5", "Custom")
            print_option("b", "Back")

            temp_choice = get_validated_input(
                prompt="Select color temperature", 
                options=["1", "2", "3", "4", "5", "b"],
                help_context_id="COLOR_TEMPERATURE_CHOICE"
            )
            if temp_choice == "_HELP_SHOWN_":
                continue
            if temp_choice == "b":
                continue

            temperatures = {"1": "warm", "2": "cool", "3": "neutral", "4": "mixed"}

            if temp_choice == "5":
                custom_temp = input("Enter custom color temperature: ").strip()
                if custom_temp:
                    user_prefs.imagen_settings["color_settings"][
                        "color_temperature"
                    ] = custom_temp
                    print_success(f"Color temperature set to: {custom_temp}")
            else:
                user_prefs.imagen_settings["color_settings"]["color_temperature"] = (
                    temperatures[temp_choice]
                )
                print_success(f"Color temperature set to: {temperatures[temp_choice]}")

            user_prefs.save_preferences()

        elif choice == "4":
            print_info("Select detail level:")
            print_option("1", "Fine")
            print_option("2", "Medium")
            print_option("3", "Coarse")
            print_option("4", "None")
            print_option("5", "Custom")
            print_option("b", "Back")

            detail_choice = get_validated_input(
                prompt="Select detail level", 
                options=["1", "2", "3", "4", "5", "b"],
                help_context_id="DETAIL_LEVEL_CHOICE"
            )
            if detail_choice == "_HELP_SHOWN_":
                continue
            if detail_choice == "b":
                continue

            detail_levels = {"1": "fine", "2": "medium", "3": "coarse", "4": None}

            if detail_choice == "5":
                custom_detail = input("Enter custom detail level: ").strip()
                if custom_detail:
                    user_prefs.imagen_settings["detail_settings"][
                        "detail_level"
                    ] = custom_detail
                    print_success(f"Detail level set to: {custom_detail}")
            else:
                user_prefs.imagen_settings["detail_settings"]["detail_level"] = (
                    detail_levels[detail_choice]
                )
                print_success(
                    f"Detail level set to: {detail_levels[detail_choice] if detail_levels[detail_choice] else 'None'}"
                )

            user_prefs.save_preferences()

        elif choice == "5":
            print_info("Select texture quality:")
            print_option("1", "High")
            print_option("2", "Medium")
            print_option("3", "Low")
            print_option("4", "None")
            print_option("5", "Custom")
            print_option("b", "Back")

            texture_choice = get_validated_input(
                prompt="Select texture quality", 
                options=["1", "2", "3", "4", "5", "b"],
                help_context_id="TEXTURE_QUALITY_CHOICE"
            )
            if texture_choice == "_HELP_SHOWN_":
                continue
            if texture_choice == "_INTERRUPTED_": # This was likely a copy-paste error in the original, should be handled by get_validated_input
                continue

            if texture_choice == "b":
                continue

            texture_qualities = {"1": "high", "2": "medium", "3": "low", "4": None}

            if texture_choice == "5":
                custom_texture = input("Enter custom texture quality: ").strip()
                if custom_texture:
                    user_prefs.imagen_settings["detail_settings"][
                        "texture_quality"
                    ] = custom_texture
                    print_success(f"Texture quality set to: {custom_texture}")
            else:
                user_prefs.imagen_settings["detail_settings"]["texture_quality"] = (
                    texture_qualities[texture_choice]
                )
                print_success(
                    f"Texture quality set to: {texture_qualities[texture_choice] if texture_qualities[texture_choice] else 'None'}"
                )

            user_prefs.save_preferences()
