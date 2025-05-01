from ui_utils import (
    print_section, print_option, print_info, print_success,
    print_warning, print_error, get_validated_input
)
from ..settings_manager import get_preferences

def manage_imagen_settings():
    """Manage Imagen 3 specific settings like number of images, seed, etc."""
    user_prefs = get_preferences()
    while True:
        print_section("Imagen 3 Settings")
        print_option("1", "Number of Images")
        print_option("2", "Set Specific Seed")
        print_option("3", "Model Version")
        print_option("4", "View Current Settings")
        print_option("5", "Reset to Defaults")
        print_option("b", "Back")
        
        choice = get_validated_input("Select an option (1-5, b)", ["1", "2", "3", "4", "5", "b"])
        
        if choice == "b":
            return
        
        if choice == "1":
            print_section("Number of Images")
            print_info(f"Current setting: {user_prefs.imagen_settings.get('number_of_images', 1)}")
            print_option("1", "1 image")
            print_option("2", "2 images")
            print_option("3", "3 images")
            print_option("4", "4 images")
            print_option("b", "Back")
            
            num_choice = get_validated_input("Select number of images (1-4, b)", ["1", "2", "3", "4", "b"])
            if num_choice == "_INTERRUPTED_":
                continue
            if num_choice == "b":
                continue
            user_prefs.imagen_settings["number_of_images"] = int(num_choice)
            print_success(f"Number of images set to {num_choice}")
            user_prefs.save_preferences()
            
        elif choice == "2":
            print_section("Set Specific Seed")
            print_info(f"Current seed: {user_prefs.imagen_settings.get('seed') or 'Random (None)'}")
            print_info("Setting a specific seed allows you to reproduce the same image style.")
            print_option("1", "Use Random Seed (None)")
            print_option("2", "Set Specific Seed")
            print_option("b", "Back")
            
            seed_choice = get_validated_input("Select option (1-2, b)", ["1", "2", "b"])
            if seed_choice == "_INTERRUPTED_":
                continue
            
            if seed_choice == "b":
                continue
            elif seed_choice == "1":
                user_prefs.imagen_settings["seed"] = None
                print_success("Seed set to Random (None)")
                user_prefs.save_preferences()
            else:
                try:
                    new_seed = input("Enter seed (integer number): ").strip()
                    if new_seed:
                        user_prefs.imagen_settings["seed"] = int(new_seed)
                        print_success(f"Seed set to {new_seed}")
                    else:
                        user_prefs.imagen_settings["seed"] = None
                        print_success("Seed set to Random (None)")
                    user_prefs.save_preferences()
                except ValueError:
                    print_error("Invalid seed value. Please enter a valid integer.")
            
        elif choice == "3":
            print_section("Model Version")
            print_info("Select Imagen model version:")
            print_option("1", "imagen-3.0-generate-002 (Default)")
            print_option("2", "imagen-3.0-generate-001 (Legacy)")
            print_option("b", "Back")
            
            model_choice = get_validated_input("Select model version (1-2, b)", ["1", "2", "b"])
            if model_choice == "_INTERRUPTED_":
                continue
            if model_choice == "b":
                continue
            models = {
                "1": "imagen-3.0-generate-002",
                "2": "imagen-3.0-generate-001"
            }
            
            user_prefs.imagen_settings["model_version"] = models[model_choice]
            print_success(f"Model version set to {models[model_choice]}")
            user_prefs.save_preferences()
            
        elif choice == "4":
            print_section("Current Settings")
            print_info(f"Number of Images: {user_prefs.imagen_settings.get('number_of_images', 1)}")
            print_info(f"Seed: {user_prefs.imagen_settings.get('seed') or 'Random (None)'}")
            print_info(f"Model Version: {user_prefs.imagen_settings.get('model_version', 'imagen-3.0-generate-002')}")
            print_info(f"Negative Prompt: {user_prefs.imagen_settings.get('negative_prompt', '') or 'None'}")
            print_info(f"Aspect Ratio: {user_prefs.aspect_ratio}")
            
            print("\nPress Enter to continue...")
            input()
            
        elif choice == "5":
            print_section("Reset to Defaults")
            confirm = get_validated_input("Are you sure you want to reset Imagen settings to defaults? (y/n)", ["y", "n"])
            
            if confirm.lower() == "y":
                user_prefs.imagen_settings["number_of_images"] = 1
                user_prefs.imagen_settings["seed"] = None
                user_prefs.imagen_settings["model_version"] = "imagen-3.0-generate-002"
                user_prefs.imagen_settings["negative_prompt"] = ""
                user_prefs.aspect_ratio = "16:9"
                
                user_prefs.save_preferences()
                print_success("Imagen settings reset to defaults")
