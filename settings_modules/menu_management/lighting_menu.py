from ui_utils import (
    print_section, print_option, print_info, print_success,
    print_warning, print_error, get_validated_input
)
from ..settings_manager import get_preferences

def manage_lighting_settings():
    """Manage lighting and atmosphere settings."""
    user_prefs = get_preferences()
    while True:
        print_section("Lighting & Atmosphere Settings")
        print_option("1", "Lighting Type")
        print_option("2", "Time of Day")
        print_option("3", "Light Source")
        print_option("4", "Light Quality")
        print_option("5", "Artificial Light Sources")
        print_option("b", "Back")
        
        choice = get_validated_input("Select option (1-5, b)", ["1", "2", "3", "4", "5", "b"])
        if choice == "_INTERRUPTED_":
            return # Exit lighting settings

        if choice == "b":
            return
            
        if choice == "1":
            print_info("Select lighting type:")
            print_option("1", "Natural")
            print_option("2", "Artificial")
            print_option("3", "Mixed")
            print_option("4", "Dramatic")
            print_option("5", "Ambient")
            print_option("6", "Custom")
            print_option("b", "Back")
            
            type_choice = get_validated_input("Select lighting type (1-6, b)", ["1", "2", "3", "4", "5", "6", "b"])
            if type_choice == "_INTERRUPTED_":
                continue

            if type_choice == "b":
                continue
            lighting_types = {
                "1": "natural",
                "2": "artificial",
                "3": "mixed",
                "4": "dramatic",
                "5": "ambient"
            }
            
            if type_choice == "6":
                custom_type = input("Enter custom lighting type: ").strip()
                if custom_type:
                    user_prefs.imagen_settings["lighting_settings"]["lighting_type"] = custom_type
                    print_success(f"Lighting type set to: {custom_type}")
            else:
                user_prefs.imagen_settings["lighting_settings"]["lighting_type"] = lighting_types[type_choice]
                print_success(f"Lighting type set to: {lighting_types[type_choice]}")
            
            user_prefs.save_preferences()
            
        elif choice == "2":
            print_info("Select time of day:")
            print_option("1", "Dawn")
            print_option("2", "Morning")
            print_option("3", "Noon")
            print_option("4", "Afternoon")
            print_option("5", "Sunset")
            print_option("6", "Dusk")
            print_option("7", "Night")
            print_option("8", "Custom")
            print_option("b", "Back")
            
            time_choice = get_validated_input("Select time of day (1-8, b)", ["1", "2", "3", "4", "5", "6", "7", "8", "b"])
            if time_choice == "_INTERRUPTED_":
                continue

            if time_choice == "b":
                continue
            times = {
                "1": "dawn",
                "2": "morning",
                "3": "noon",
                "4": "afternoon",
                "5": "sunset",
                "6": "dusk",
                "7": "night"
            }
            
            if time_choice == "8":
                custom_time = input("Enter custom time of day: ").strip()
                if custom_time:
                    user_prefs.imagen_settings["lighting_settings"]["time_of_day"] = custom_time
                    print_success(f"Time of day set to: {custom_time}")
            else:
                user_prefs.imagen_settings["lighting_settings"]["time_of_day"] = times[time_choice]
                print_success(f"Time of day set to: {times[time_choice]}")
            
            user_prefs.save_preferences()
            
        elif choice == "3":
            print_info("Select light source:")
            print_option("1", "Sun")
            print_option("2", "Moon")
            print_option("3", "Fire")
            print_option("4", "Electric")
            print_option("5", "Multiple Sources")
            print_option("6", "Custom")
            print_option("b", "Back")
            
            source_choice = get_validated_input("Select light source (1-6, b)", ["1", "2", "3", "4", "5", "6", "b"])
            if source_choice == "_INTERRUPTED_":
                continue

            if source_choice == "b":
                continue
            sources = {
                "1": "sun",
                "2": "moon",
                "3": "fire",
                "4": "electric",
                "5": "multiple"
            }
            
            if source_choice == "6":
                custom_source = input("Enter custom light source: ").strip()
                if custom_source:
                    user_prefs.imagen_settings["lighting_settings"]["light_source"] = custom_source
                    print_success(f"Light source set to: {custom_source}")
            else:
                user_prefs.imagen_settings["lighting_settings"]["light_source"] = sources[source_choice]
                print_success(f"Light source set to: {sources[source_choice]}")
            
            user_prefs.save_preferences()
            
        elif choice == "4":
            print_info("Select light quality:")
            print_option("1", "Soft")
            print_option("2", "Hard")
            print_option("3", "Diffused")
            print_option("4", "Directional")
            print_option("5", "Atmospheric")
            print_option("6", "Custom")
            print_option("b", "Back")
            
            quality_choice = get_validated_input("Select light quality (1-6, b)", ["1", "2", "3", "4", "5", "6", "b"])
            if quality_choice == "_INTERRUPTED_":
                continue

            if quality_choice == "b":
                continue
            qualities = {
                "1": "soft",
                "2": "hard",
                "3": "diffused",
                "4": "directional",
                "5": "atmospheric"
            }
            
            if quality_choice == "6":
                custom_quality = input("Enter custom light quality: ").strip()
                if custom_quality:
                    user_prefs.imagen_settings["lighting_settings"]["light_quality"] = custom_quality
                    print_success(f"Light quality set to: {custom_quality}")
            else:
                user_prefs.imagen_settings["lighting_settings"]["light_quality"] = qualities[quality_choice]
                print_success(f"Light quality set to: {qualities[quality_choice]}")
            
            user_prefs.save_preferences()
            
        elif choice == "5":
            while True:
                print_info("Manage artificial light sources:")
                current_sources = user_prefs.imagen_settings["lighting_settings"].get("artificial_sources", [])
                if current_sources:
                    print_info("Current artificial sources:")
                    for i, source in enumerate(current_sources, 1):
                        print(f"{i}. {source}")
                else:
                    print_info("No artificial light sources set")
                
                print_option("1", "Add Source")
                print_option("2", "Remove Source")
                print_option("3", "Clear All Sources")
                print_option("b", "Back")
                
                source_choice = get_validated_input("Select option (1-3, b)", ["1", "2", "3", "b"])
                if source_choice == "_INTERRUPTED_":
                    break # Exit artificial sources loop

                if source_choice == "b":
                    break
                    
                if source_choice == "1":
                    print_info("Select source to add:")
                    print_option("1", "Lamp")
                    print_option("2", "LED")
                    print_option("3", "Neon")
                    print_option("4", "Fluorescent")
                    print_option("5", "Candle")
                    print_option("6", "Custom")
                    
                    add_choice = get_validated_input("Select source (1-6)", ["1", "2", "3", "4", "5", "6"])
                    
                    sources = {
                        "1": "lamp",
                        "2": "led",
                        "3": "neon",
                        "4": "fluorescent",
                        "5": "candle"
                    }
                    
                    if add_choice == "6":
                        custom_source = input("Enter custom light source: ").strip()
                        if custom_source and custom_source not in current_sources:
                            current_sources.append(custom_source)
                            print_success(f"Added artificial source: {custom_source}")
                    else:
                        source = sources[add_choice]
                        if source not in current_sources:
                            current_sources.append(source)
                            print_success(f"Added artificial source: {source}")
                        else:
                            print_warning(f"{source} is already in the list")
                    
                    user_prefs.imagen_settings["lighting_settings"]["artificial_sources"] = current_sources
                    user_prefs.save_preferences()
                    
                elif source_choice == "2":
                    if current_sources:
                        try:
                            idx = int(input("Enter number of source to remove: ")) - 1
                            if 0 <= idx < len(current_sources):
                                removed = current_sources.pop(idx)
                                print_success(f"Removed artificial source: {removed}")
                                user_prefs.imagen_settings["lighting_settings"]["artificial_sources"] = current_sources
                                user_prefs.save_preferences()
                            else:
                                print_error("Invalid source number")
                        except ValueError:
                            print_error("Please enter a valid number")
                    else:
                        print_warning("No sources to remove")
                        
                elif source_choice == "3":
                    if current_sources:
                        confirm = get_validated_input("Are you sure you want to clear all sources? (y/n)", ["y", "n"])
                        if confirm.lower() == "y":
                            user_prefs.imagen_settings["lighting_settings"]["artificial_sources"] = []
                            print_success("Cleared all artificial sources")
                            user_prefs.save_preferences()
                    else:
                        print_warning("No sources to clear")
