import re
from ui_utils import (
    print_section,
    print_option,
    print_info,
    print_success,
    print_error,
    get_validated_input,
)
from ..settings_manager import get_preferences


def manage_output_quality_settings():
    """Manage output quality settings."""
    user_prefs = get_preferences()
    while True:
        print_section("Output Quality Settings")
        print_option("1", "Resolution")
        print_option("2", "Detail Level")
        print_option("3", "Rendering Quality")
        print_option("b", "Back")

        choice = get_validated_input("Select option (1-3, b)", ["1", "2", "3", "b"])
        if choice == "_INTERRUPTED_":
            return  # Exit output quality settings

        if choice == "b":
            return

        if choice == "1":
            print_info("Select resolution:")
            print_option("1", "HD (1280x720)")
            print_option("2", "Full HD (1920x1080)")
            print_option("3", "2K (2560x1440)")
            print_option("4", "4K (3840x2160)")
            print_option("5", "8K (7680x4320)")
            print_option("6", "Custom Resolution")
            print_option("b", "Back")

            res_choice = get_validated_input(
                "Select resolution (1-6, b)", ["1", "2", "3", "4", "5", "6", "b"]
            )
            if res_choice == "_INTERRUPTED_":
                continue

            if res_choice == "b":
                continue
            resolutions = {
                "1": "1280x720",
                "2": "1920x1080",
                "3": "2560x1440",
                "4": "3840x2160",
                "5": "7680x4320",
            }

            if res_choice == "6":
                while True:
                    custom_res = input(
                        "Enter custom resolution (width x height, e.g. 1920x1080): "
                    ).strip()
                    if re.match(r"^\d+x\d+$", custom_res):
                        user_prefs.imagen_settings["quality_settings"][
                            "resolution"
                        ] = custom_res
                        print_success(f"Resolution set to: {custom_res}")
                        break
                    else:
                        print_error(
                            "Invalid resolution format. Please use width x height (e.g., 1920x1080)"
                        )
            else:
                user_prefs.imagen_settings["quality_settings"]["resolution"] = (
                    resolutions[res_choice]
                )
                print_success(f"Resolution set to: {resolutions[res_choice]}")

            user_prefs.save_preferences()

        elif choice == "2":
            print_info("Select detail level:")
            print_option("1", "Low")
            print_option("2", "Medium")
            print_option("3", "High")
            print_option("4", "Ultra")
            print_option("5", "None")
            print_option("b", "Back")

            detail_choice = get_validated_input(
                "Select detail level (1-5, b)", ["1", "2", "3", "4", "5", "b"]
            )
            if detail_choice == "_INTERRUPTED_":
                continue

            if detail_choice == "b":
                continue
            detail_levels = {
                "1": "low",
                "2": "medium",
                "3": "high",
                "4": "ultra",
                "5": None,
            }

            user_prefs.imagen_settings["quality_settings"]["detail_level"] = (
                detail_levels[detail_choice]
            )
            print_success(
                f"Detail level set to: {detail_levels[detail_choice] if detail_levels[detail_choice] else 'None'}"
            )
            user_prefs.save_preferences()

        elif choice == "3":
            print_info("Select rendering quality:")
            print_option("1", "Draft")
            print_option("2", "Standard")
            print_option("3", "High")
            print_option("4", "Maximum")
            print_option("5", "None")
            print_option("b", "Back")

            quality_choice = get_validated_input(
                "Select rendering quality (1-5, b)", ["1", "2", "3", "4", "5", "b"]
            )
            if quality_choice == "_INTERRUPTED_":
                continue

            if quality_choice == "b":
                continue
            quality_levels = {
                "1": "draft",
                "2": "standard",
                "3": "high",
                "4": "maximum",
                "5": None,
            }

            user_prefs.imagen_settings["quality_settings"]["rendering_quality"] = (
                quality_levels[quality_choice]
            )
            print_success(
                f"Rendering quality set to: {quality_levels[quality_choice] if quality_levels[quality_choice] else 'None'}"
            )
            user_prefs.save_preferences()
