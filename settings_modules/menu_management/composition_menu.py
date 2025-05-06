from ui_utils import (
    print_section,
    print_option,
    print_info,
    print_success,
    print_warning,
    print_error,
    get_validated_input,
)
from ..settings_manager import get_preferences


def manage_composition_settings():
    """Manage composition and environment settings."""
    user_prefs = get_preferences()
    while True:
        print_section("Composition & Environment Settings")
        print_option("1", "Composition Technique")
        print_option("2", "Camera Angle")
        print_option("3", "Visual Flow")
        print_option("4", "Depth Layering")
        print_option("5", "Focal Point")
        print_option("6", "Perspective")
        print_option("7", "Environment Settings")
        print_option("b", "Back")

        choice = get_validated_input(
            "Select option (1-7, b)", ["1", "2", "3", "4", "5", "6", "7", "b"]
        )

        if choice == "b":
            return

        if choice == "5":
            focal_point = input(
                "Enter focal point (e.g., subject, feature, or theme to emphasize): "
            ).strip()
            if focal_point:
                user_prefs.imagen_settings["composition_settings"][
                    "focal_point"
                ] = focal_point
                print_success(f"Focal point set to: {focal_point}")
            user_prefs.save_preferences()

        elif choice == "6":
            perspective = input(
                "Enter perspective (e.g., wide, narrow, linear, forced, atmospheric, or custom): "
            ).strip()
            if perspective:
                user_prefs.imagen_settings["composition_settings"][
                    "perspective"
                ] = perspective
                print_success(f"Perspective set to: {perspective}")
            user_prefs.save_preferences()

        elif choice == "1":
            print_info("Select composition technique:")
            print_option("1", "Rule of Thirds")
            print_option("2", "Golden Ratio")
            print_option("3", "Symmetry")
            print_option("4", "Leading Lines")
            print_option("5", "Framing")
            print_option("6", "Custom")
            print_option("b", "Back")

            technique_choice = get_validated_input(
                "Select technique (1-6, b)", ["1", "2", "3", "4", "5", "6", "b"]
            )

            if technique_choice == "b":
                continue
            techniques = {
                "1": "rule_of_thirds",
                "2": "golden_ratio",
                "3": "symmetry",
                "4": "leading_lines",
                "5": "framing",
            }

            if technique_choice == "6":
                custom_technique = input("Enter custom composition technique: ").strip()
                if custom_technique:
                    user_prefs.imagen_settings["composition_settings"][
                        "technique"
                    ] = custom_technique
                    print_success(f"Composition technique set to: {custom_technique}")
            else:
                user_prefs.imagen_settings["composition_settings"]["technique"] = (
                    techniques[technique_choice]
                )
                print_success(
                    f"Composition technique set to: {techniques[technique_choice]}"
                )

            user_prefs.save_preferences()

        elif choice == "2":
            print_info("Select camera angle:")
            print_option("1", "Eye Level")
            print_option("2", "Low Angle")
            print_option("3", "High Angle")
            print_option("4", "Bird's Eye")
            print_option("5", "Dutch Angle")
            print_option("6", "Custom")
            print_option("b", "Back")

            angle_choice = get_validated_input(
                "Select camera angle (1-6, b)", ["1", "2", "3", "4", "5", "6", "b"]
            )

            if angle_choice == "b":
                continue
            angles = {
                "1": "eye_level",
                "2": "low_angle",
                "3": "high_angle",
                "4": "birds_eye",
                "5": "dutch_angle",
            }

            if angle_choice == "6":
                custom_angle = input("Enter custom camera angle: ").strip()
                if custom_angle:
                    user_prefs.imagen_settings["composition_settings"][
                        "camera_angle"
                    ] = custom_angle
                    print_success(f"Camera angle set to: {custom_angle}")
            else:
                user_prefs.imagen_settings["composition_settings"]["camera_angle"] = (
                    angles[angle_choice]
                )
                print_success(f"Camera angle set to: {angles[angle_choice]}")

            user_prefs.save_preferences()

        elif choice == "3":
            print_info("Select visual flow:")
            print_option("1", "Linear")
            print_option("2", "Circular")
            print_option("3", "Diagonal")
            print_option("4", "Triangular")
            print_option("5", "Z-Pattern")
            print_option("6", "Custom")
            print_option("b", "Back")

            flow_choice = get_validated_input(
                "Select visual flow (1-6, b)", ["1", "2", "3", "4", "5", "6", "b"]
            )

            if flow_choice == "b":
                continue
            flows = {
                "1": "linear",
                "2": "circular",
                "3": "diagonal",
                "4": "triangular",
                "5": "z_pattern",
            }

            if flow_choice == "6":
                custom_flow = input("Enter custom visual flow: ").strip()
                if custom_flow:
                    user_prefs.imagen_settings["composition_settings"][
                        "visual_flow"
                    ] = custom_flow
                    print_success(f"Visual flow set to: {custom_flow}")
            else:
                user_prefs.imagen_settings["composition_settings"]["visual_flow"] = (
                    flows[flow_choice]
                )
                print_success(f"Visual flow set to: {flows[flow_choice]}")

            user_prefs.save_preferences()

        elif choice == "4":
            print_info("Select depth layering:")
            print_option("1", "Foreground Focus")
            print_option("2", "Middle Ground Focus")
            print_option("3", "Background Focus")
            print_option("4", "Multi-Layer")
            print_option("5", "Flat")
            print_option("6", "Custom")
            print_option("b", "Back")

            depth_choice = get_validated_input(
                "Select depth layering (1-6, b)", ["1", "2", "3", "4", "5", "6", "b"]
            )

            if depth_choice == "b":
                continue
            depths = {
                "1": "foreground_focus",
                "2": "middle_ground_focus",
                "3": "background_focus",
                "4": "multi_layer",
                "5": "flat",
            }

            if depth_choice == "6":
                custom_depth = input("Enter custom depth layering: ").strip()
                if custom_depth:
                    user_prefs.imagen_settings["composition_settings"][
                        "depth_layering"
                    ] = custom_depth
                    print_success(f"Depth layering set to: {custom_depth}")
            else:
                user_prefs.imagen_settings["composition_settings"]["depth_layering"] = (
                    depths[depth_choice]
                )
                print_success(f"Depth layering set to: {depths[depth_choice]}")

            user_prefs.save_preferences()

        elif choice == "7":
            while True:
                print_info("Environment Settings:")
                print_option("1", "Weather")
                print_option("2", "Season")
                print_option("3", "Atmospheric Effects")
                print_option("4", "Location Type")
                print_option("b", "Back")

                env_choice = get_validated_input(
                    "Select option (1-4, b)", ["1", "2", "3", "4", "b"]
                )
                if env_choice == "_INTERRUPTED_":
                    break  # Exit environment settings loop

                if env_choice == "b":
                    break

                if env_choice == "1":
                    print_info("Select weather:")
                    print_option("1", "Clear")
                    print_option("2", "Cloudy")
                    print_option("3", "Rainy")
                    print_option("4", "Stormy")
                    print_option("5", "Snowy")
                    print_option("6", "Foggy")
                    print_option("7", "Custom")
                    print_option("b", "Back")

                    weather_choice = get_validated_input(
                        "Select weather (1-7, b)",
                        ["1", "2", "3", "4", "5", "6", "7", "b"],
                    )

                    if weather_choice == "b":
                        continue
                    weather_types = {
                        "1": "clear",
                        "2": "cloudy",
                        "3": "rainy",
                        "4": "stormy",
                        "5": "snowy",
                        "6": "foggy",
                    }

                    if weather_choice == "7":
                        custom_weather = input("Enter custom weather: ").strip()
                        if custom_weather:
                            user_prefs.imagen_settings["environment_settings"][
                                "weather"
                            ] = custom_weather
                            print_success(f"Weather set to: {custom_weather}")
                    else:
                        user_prefs.imagen_settings["environment_settings"][
                            "weather"
                        ] = weather_types[weather_choice]
                        print_success(
                            f"Weather set to: {weather_types[weather_choice]}"
                        )

                    user_prefs.save_preferences()

                elif env_choice == "2":
                    print_info("Select season:")
                    print_option("1", "Spring")
                    print_option("2", "Summer")
                    print_option("3", "Autumn")
                    print_option("4", "Winter")
                    print_option("5", "Custom")
                    print_option("b", "Back")

                    season_choice = get_validated_input(
                        "Select season (1-5, b)", ["1", "2", "3", "4", "5", "b"]
                    )

                    if season_choice == "b":
                        continue
                    seasons = {
                        "1": "spring",
                        "2": "summer",
                        "3": "autumn",
                        "4": "winter",
                    }

                    if season_choice == "5":
                        custom_season = input("Enter custom season: ").strip()
                        if custom_season:
                            user_prefs.imagen_settings["environment_settings"][
                                "season"
                            ] = custom_season
                            print_success(f"Season set to: {custom_season}")
                    else:
                        user_prefs.imagen_settings["environment_settings"]["season"] = (
                            seasons[season_choice]
                        )
                        print_success(f"Season set to: {seasons[season_choice]}")

                    user_prefs.save_preferences()

                elif env_choice == "3":
                    while True:
                        print_info("Manage atmospheric effects:")
                        current_effects = user_prefs.imagen_settings[
                            "environment_settings"
                        ].get("atmospheric_effects", [])
                        if current_effects:
                            print_info("Current effects:")
                            for i, effect in enumerate(current_effects, 1):
                                print(f"{i}. {effect}")
                        else:
                            print_info("No atmospheric effects set")

                        print_option("1", "Add Effect")
                        print_option("2", "Remove Effect")
                        print_option("3", "Clear All Effects")
                        print_option("b", "Back")

                        effect_choice = get_validated_input(
                            "Select option (1-3, b)", ["1", "2", "3", "b"]
                        )

                        if effect_choice == "b":
                            break

                        if effect_choice == "1":
                            print_info("Select effect to add:")
                            print_option("1", "Mist")
                            print_option("2", "Rain")
                            print_option("3", "Snow")
                            print_option("4", "Dust")
                            print_option("5", "Haze")
                            print_option("6", "Custom")

                            add_choice = get_validated_input(
                                "Select effect (1-6)", ["1", "2", "3", "4", "5", "6"]
                            )

                            effects = {
                                "1": "mist",
                                "2": "rain",
                                "3": "snow",
                                "4": "dust",
                                "5": "haze",
                            }

                            if add_choice == "6":
                                custom_effect = input(
                                    "Enter custom atmospheric effect: "
                                ).strip()
                                if (
                                    custom_effect
                                    and custom_effect not in current_effects
                                ):
                                    current_effects.append(custom_effect)
                                    print_success(f"Added effect: {custom_effect}")
                            else:
                                effect = effects[add_choice]
                                if effect not in current_effects:
                                    current_effects.append(effect)
                                    print_success(f"Added effect: {effect}")
                                else:
                                    print_warning(f"{effect} is already in the list")

                            user_prefs.imagen_settings["environment_settings"][
                                "atmospheric_effects"
                            ] = current_effects
                            user_prefs.save_preferences()

                        elif effect_choice == "2":
                            if current_effects:
                                try:
                                    idx = (
                                        int(input("Enter number of effect to remove: "))
                                        - 1
                                    )
                                    if 0 <= idx < len(current_effects):
                                        removed = current_effects.pop(idx)
                                        print_success(f"Removed effect: {removed}")
                                        user_prefs.imagen_settings[
                                            "environment_settings"
                                        ]["atmospheric_effects"] = current_effects
                                        user_prefs.save_preferences()
                                    else:
                                        print_error("Invalid effect number")
                                except ValueError:
                                    print_error("Please enter a valid number")
                            else:
                                print_warning("No effects to remove")

                        elif effect_choice == "3":
                            if current_effects:
                                confirm = get_validated_input(
                                    "Are you sure you want to clear all effects? (y/n)",
                                    ["y", "n"],
                                )
                                if confirm.lower() == "y":
                                    user_prefs.imagen_settings["environment_settings"][
                                        "atmospheric_effects"
                                    ] = []
                                    print_success("Cleared all atmospheric effects")
                                    user_prefs.save_preferences()
                            else:
                                print_warning("No effects to clear")

                elif env_choice == "4":
                    print_info("Select location type:")
                    print_option("1", "Indoor")
                    print_option("2", "Outdoor")
                    print_option("3", "Urban")
                    print_option("4", "Rural")
                    print_option("5", "Underwater")
                    print_option("6", "Space")
                    print_option("7", "Custom")
                    print_option("b", "Back")

                    location_choice = get_validated_input(
                        "Select location type (1-7, b)",
                        ["1", "2", "3", "4", "5", "6", "7", "b"],
                    )

                    if location_choice == "b":
                        continue
                    locations = {
                        "1": "indoor",
                        "2": "outdoor",
                        "3": "urban",
                        "4": "rural",
                        "5": "underwater",
                        "6": "space",
                    }

                    if location_choice == "7":
                        custom_location = input("Enter custom location type: ").strip()
                        if custom_location:
                            user_prefs.imagen_settings["environment_settings"][
                                "location_type"
                            ] = custom_location
                            print_success(f"Location type set to: {custom_location}")
                    else:
                        user_prefs.imagen_settings["environment_settings"][
                            "location_type"
                        ] = locations[location_choice]
                        print_success(
                            f"Location type set to: {locations[location_choice]}"
                        )

                    user_prefs.save_preferences()
