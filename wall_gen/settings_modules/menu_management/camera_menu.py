import sys
from wall_gen.ui_utils import (
    print_section,
    print_option,
    print_info,
    print_success,
    get_validated_input,
    clear_screen, # Added
    print_header, # Added
)
from ..settings_manager import get_preferences


def manage_camera_settings():
    """Manage camera-specific settings."""
    user_prefs = get_preferences()
    while True:
        clear_screen()
        print_header("Camera & Technical Settings")
        # print_section("Camera & Technical Settings") # Replaced by print_header
        print_option("1", "Camera Model")
        print_option("2", "Lens Type")
        print_option("3", "Aperture")
        print_option("4", "Depth of Field")
        print_option("5", "Special Lens Effects")
        print_option("6", "Focal Length")
        print_option("7", "Shutter Speed")
        print_option("8", "ISO")
        print_option("9", "Filter Type")
        print_option("b", "Back")

        choice = get_validated_input(
            prompt="Select an option", 
            options=["1", "2", "3", "4", "5", "6", "7", "8", "9", "b"],
            help_context_id="CAMERA_MENU"
        )
        if choice == "_HELP_SHOWN_":
            continue
        if choice == "_INTERRUPTED_":
            return  # Exit camera settings

        if choice == "b":
            return

        if choice == "6":
            # Focal Length
            focal_length = input(
                "Enter focal length (e.g., 35mm, 85mm, range, or custom): "
            ).strip()
            if focal_length:
                user_prefs.imagen_settings["camera_settings"][
                    "focal_length"
                ] = focal_length
                print_success(f"Focal length set to: {focal_length}")
            user_prefs.save_preferences()

        elif choice == "7":
            # Shutter Speed
            shutter_speed = input(
                "Enter shutter speed (e.g., 1/60s, 1/200s, Bulb, or custom): "
            ).strip()
            if shutter_speed:
                user_prefs.imagen_settings["camera_settings"][
                    "shutter_speed"
                ] = shutter_speed
                print_success(f"Shutter speed set to: {shutter_speed}")
            user_prefs.save_preferences()

        elif choice == "8":
            # ISO
            iso = input(
                "Enter ISO value (e.g., 100, 400, 1600, Auto, or custom): "
            ).strip()
            if iso:
                user_prefs.imagen_settings["camera_settings"]["iso"] = iso
                print_success(f"ISO set to: {iso}")
            user_prefs.save_preferences()

        elif choice == "9":
            # Filter Type
            print_info("Select filter type:")
            print_option("1", "UV")
            print_option("2", "Polarizer")
            print_option("3", "ND (Neutral Density)")
            print_option("4", "Color Filter")
            print_option("5", "Soft Focus Filter")
            print_option("6", "Custom Filter")
            print_option("b", "Back")
            filter_choice = get_validated_input(
                prompt="Select filter type", 
                options=["1", "2", "3", "4", "5", "6", "b"],
                help_context_id="CAMERA_FILTER_TYPE_CHOICE"
            )
            if filter_choice == "_HELP_SHOWN_":
                continue
            if filter_choice == "_INTERRUPTED_":
                return
            if filter_choice == "b":
                return
            filters = {
                "1": "uv",
                "2": "polarizer",
                "3": "nd",
                "4": "color_filter",
                "5": "soft_focus",
            }
            if filter_choice == "6":
                custom_filter = input("Enter custom filter type: ").strip()
                if custom_filter:
                    user_prefs.imagen_settings["camera_settings"][
                        "filter_type"
                    ] = custom_filter
                    print_success(f"Filter type set to: {custom_filter}")
            else:
                user_prefs.imagen_settings["camera_settings"]["filter_type"] = filters[
                    filter_choice
                ]
                print_success(f"Filter type set to: {filters[filter_choice]}")
            user_prefs.save_preferences()

        elif choice == "1":
            print_info("Select camera model:")
            print_option("1", "DSLR")
            print_option("2", "Mirrorless")
            print_option("3", "Medium Format")
            print_option("4", "Film Camera")
            print_option("5", "Custom Model")
            print_option("b", "Back")

            model_choice = get_validated_input(
                prompt="Select camera model", 
                options=["1", "2", "3", "4", "5", "b"],
                help_context_id="CAMERA_MODEL_CHOICE"
            )
            if model_choice == "_HELP_SHOWN_":
                continue
            if model_choice == "_INTERRUPTED_":
                continue

            if model_choice == "b":
                continue
            models = {
                "1": "dslr",
                "2": "mirrorless",
                "3": "medium_format",
                "4": "film_camera",
            }

            if model_choice == "5":
                custom_model = input("Enter custom camera model: ").strip()
                if custom_model:
                    user_prefs.imagen_settings["camera_settings"][
                        "camera_model"
                    ] = custom_model
                    print_success(f"Camera model set to: {custom_model}")
            else:
                user_prefs.imagen_settings["camera_settings"]["camera_model"] = models[
                    model_choice
                ]
                print_success(f"Camera model set to: {models[model_choice]}")

            user_prefs.save_preferences()

        elif choice == "2":
            print_info("Select lens type:")
            print_option("1", "Wide Angle")
            print_option("2", "Standard")
            print_option("3", "Telephoto")
            print_option("4", "Macro")
            print_option("5", "Fish Eye")
            print_option("6", "Custom Lens")
            print_option("b", "Back")

            lens_choice = get_validated_input(
                prompt="Select lens type", 
                options=["1", "2", "3", "4", "5", "6", "b"],
                help_context_id="CAMERA_LENS_TYPE_CHOICE"
            )
            if lens_choice == "_HELP_SHOWN_":
                continue
            if lens_choice == "_INTERRUPTED_":
                continue

            if lens_choice == "b":
                continue
            lenses = {
                "1": "wide_angle",
                "2": "standard",
                "3": "telephoto",
                "4": "macro",
                "5": "fish_eye",
            }

            if lens_choice == "6":
                custom_lens = input("Enter custom lens type: ").strip()
                if custom_lens:
                    user_prefs.imagen_settings["camera_settings"][
                        "lens_type"
                    ] = custom_lens
                    print_success(f"Lens type set to: {custom_lens}")
            else:
                user_prefs.imagen_settings["camera_settings"]["lens_type"] = lenses[
                    lens_choice
                ]
                print_success(f"Lens type set to: {lenses[lens_choice]}")

            user_prefs.save_preferences()

        elif choice == "3":
            print_info("Select aperture:")
            print_option("1", "f/1.4 (Very shallow depth of field)")
            print_option("2", "f/2.8 (Shallow depth of field)")
            print_option("3", "f/4 (Moderate depth of field)")
            print_option("4", "f/8 (Deep depth of field)")
            print_option("5", "f/16 (Very deep depth of field)")
            print_option("6", "Custom Aperture")
            print_option("b", "Back")

            aperture_choice = get_validated_input(
                prompt="Select aperture", 
                options=["1", "2", "3", "4", "5", "6", "b"],
                help_context_id="CAMERA_APERTURE_CHOICE"
            )
            if aperture_choice == "_HELP_SHOWN_":
                continue
            if aperture_choice == "_INTERRUPTED_":
                continue

            if aperture_choice == "b":
                continue
            apertures = {
                "1": "f/1.4",
                "2": "f/2.8",
                "3": "f/4",
                "4": "f/8",
                "5": "f/16",
            }

            if aperture_choice == "6":
                custom_aperture = input("Enter custom aperture (e.g., f/5.6): ").strip()
                if custom_aperture:
                    user_prefs.imagen_settings["camera_settings"][
                        "aperture"
                    ] = custom_aperture
                    print_success(f"Aperture set to: {custom_aperture}")
            else:
                user_prefs.imagen_settings["camera_settings"]["aperture"] = apertures[
                    aperture_choice
                ]
                print_success(f"Aperture set to: {apertures[aperture_choice]}")

            user_prefs.save_preferences()

        elif choice == "4":
            print_info("Select depth of field:")
            print_option("1", "Very Shallow")
            print_option("2", "Shallow")
            print_option("3", "Moderate")
            print_option("4", "Deep")
            print_option("5", "Very Deep")
            print_option("6", "Custom Setting")
            print_option("b", "Back")

            dof_choice = get_validated_input(
                prompt="Select depth of field", 
                options=["1", "2", "3", "4", "5", "6", "b"],
                help_context_id="CAMERA_DOF_CHOICE"
            )
            if dof_choice == "_HELP_SHOWN_":
                continue
            if dof_choice == "_INTERRUPTED_":
                continue

            if dof_choice == "b":
                continue
            dof_settings = {
                "1": "very_shallow",
                "2": "shallow",
                "3": "moderate",
                "4": "deep",
                "5": "very_deep",
            }

            if dof_choice == "6":
                custom_dof = input("Enter custom depth of field setting: ").strip()
                if custom_dof:
                    user_prefs.imagen_settings["camera_settings"][
                        "depth_of_field"
                    ] = custom_dof
                    print_success(f"Depth of field set to: {custom_dof}")
            else:
                user_prefs.imagen_settings["camera_settings"]["depth_of_field"] = (
                    dof_settings[dof_choice]
                )
                print_success(f"Depth of field set to: {dof_settings[dof_choice]}")

            user_prefs.save_preferences()

        elif choice == "5":
            print_info("Select special lens effects:")
            print_option("1", "Bokeh")
            print_option("2", "Lens Flare")
            print_option("3", "Soft Focus")
            print_option("4", "Tilt-Shift")
            print_option("5", "Chromatic Aberration")
            print_option("6", "Custom Effect")
            print_option("7", "No Special Effects")
            print_option("b", "Back")

            effect_choice = get_validated_input(
                prompt="Select special effect",
                options=["1", "2", "3", "4", "5", "6", "7", "b"],
                help_context_id="CAMERA_LENS_EFFECT_CHOICE"
            )
            if effect_choice == "_HELP_SHOWN_":
                continue
            if effect_choice == "_INTERRUPTED_":
                continue

            if effect_choice == "b":
                continue
            effects = {
                "1": "bokeh",
                "2": "lens_flare",
                "3": "soft_focus",
                "4": "tilt_shift",
                "5": "chromatic_aberration",
            }

            if effect_choice == "6":
                custom_effect = input("Enter custom lens effect: ").strip()
                if custom_effect:
                    user_prefs.imagen_settings["camera_settings"][
                        "special_lens"
                    ] = custom_effect
                    print_success(f"Special lens effect set to: {custom_effect}")
            elif effect_choice == "7":
                user_prefs.imagen_settings["camera_settings"]["special_lens"] = None
                print_success("Special lens effects cleared")
            else:
                user_prefs.imagen_settings["camera_settings"]["special_lens"] = effects[
                    effect_choice
                ]
                print_success(f"Special lens effect set to: {effects[effect_choice]}")

            user_prefs.save_preferences()
