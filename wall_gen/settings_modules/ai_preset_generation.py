import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import os
import logging
from ui_utils import (
    print_section, print_option, print_success, print_error, print_warning,
    print_info, get_validated_input
)
from .settings_manager import get_preferences

# Imports for Gemini model selection for presets
try:
    from ai_prest_gen.gemini_config_preset import (
        get_selected_preset_model,
        set_selected_preset_model,
        AVAILABLE_PRESET_MODELS
    )
    PRESET_MODEL_CONFIG_AVAILABLE = True
except ImportError:
    PRESET_MODEL_CONFIG_AVAILABLE = False
    # This warning will appear if ai_prest_gen or its config is missing
    logging.warning("AI Preset Generator's Gemini model configuration (gemini_config_preset.py) not found. Model selection for presets will be unavailable.")
    def get_selected_preset_model(prefs): return "N/A (config missing)" # Fallback
    def set_selected_preset_model(model, prefs): print_error("Model selection unavailable."); return False # Fallback
    AVAILABLE_PRESET_MODELS = [] # Fallback


def select_preset_model_submenu(user_prefs):
    """Allows user to select a Gemini model for AI Preset Generation."""
    if not PRESET_MODEL_CONFIG_AVAILABLE:
        print_error("Model selection feature for presets is not available due to missing configuration.")
        input("\nPress Enter to continue...")
        return

    print_section("Select Gemini Model for AI Preset Generation")
    current_model = get_selected_preset_model(user_prefs)
    print_info(f"Current model for AI Presets: {current_model}")
    
    if not AVAILABLE_PRESET_MODELS:
        print_warning("No preset models available for selection in config.")
        input("\nPress Enter to continue...")
        return

    for i, model_name in enumerate(AVAILABLE_PRESET_MODELS):
        print_option(str(i + 1), model_name)
    print_option("b", "Back to AI Preset Options")

    valid_choices_model = [str(i + 1) for i in range(len(AVAILABLE_PRESET_MODELS))] + ["b"]
    choice_model = get_validated_input("Select model number or 'b': ", valid_choices_model)

    if choice_model == 'b':
        return
    
    try:
        selected_index = int(choice_model) - 1
        if 0 <= selected_index < len(AVAILABLE_PRESET_MODELS):
            new_model = AVAILABLE_PRESET_MODELS[selected_index]
            if set_selected_preset_model(new_model, user_prefs):
                print_success(f"AI Preset Generator Gemini model set to: {new_model}")
                # set_selected_preset_model in gemini_config_preset handles saving if UserPrefs has save_preferences
            else:
                print_error(f"Failed to set AI Preset Generator Gemini model.")
        else:
            print_error("Invalid selection.")
    except ValueError:
        print_error("Invalid input. Please enter a number.")
    except Exception as e:
        print_error(f"An error occurred during model selection: {e}")
        logging.error("Error in select_preset_model_submenu", exc_info=True)
    
    input("\nPress Enter to continue...")


def generate_ai_preset():
    """
    Generate an AI-based preset using Gemini (or other AI backend).
    Also allows selection of the Gemini model for preset generation.
    This function wraps the ai_preset_generator module's functionality for interactive use.
    """
    user_prefs = get_preferences()
    while True:
        print_section("AI Preset Generation Options") 
        print_option("1", "Generate New AI Preset")
        if PRESET_MODEL_CONFIG_AVAILABLE:
            print_option("2", "Select Gemini Model for Presets")
        print_option("b", "Back")

        valid_menu_choices = ["1", "b"]
        if PRESET_MODEL_CONFIG_AVAILABLE:
            valid_menu_choices.append("2")
            
        choice = get_validated_input(f"Select option ({', '.join(valid_menu_choices)}): ", valid_menu_choices)
        
        if choice == "b":
            return

        if choice == "1":
            # Logic for generating a new preset
            while True: # Inner loop for style source
                print_section("Choose Style Source for Preset")
                print_option("1", "Enter Custom Style")
                print_option("2", "Generate AI Style")
                print_option("b", "Back")
                style_choice = get_validated_input("Select option (1-2, b)", ["1", "2", "b"])
                if style_choice == "b":
                    break

                try:
                    from ai_prest_gen.ai_preset_generator import generate_ai_preset as ai_gen_preset

                    # Only show "Attempting to generate AI preset" if generating AI style (not for custom)
                    if style_choice == "1":
                        base_style_input = get_validated_input("Enter your custom style: ", allow_empty=False) # Renamed to avoid conflict
                        if not base_style_input:
                            print_error("No style entered.")
                            break # Break from inner style source loop
                        base_style = base_style_input
                    elif style_choice == "2": # Generate AI Style
                        print_info("Attempting to generate base AI style (this may take a moment)...")
                        try:
                            from wall_gen.ai_style_generator import generate_random_style, initialize_gemini as init_style_gem_global
                            # AI Style Generator likely uses its own global Gemini config from wall_gen.gemini_config
                            # No need to pass API key if that global config handles it.
                            if not init_style_gem_global(None): # Assuming it can init without explicit key if globally set
                                print_error("Failed to initialize Gemini for AI Style Generation.")
                                break # Break from inner style source loop
                            
                            generated_style_obj = generate_random_style(style_type="detailed") # Use a different var name
                            if not generated_style_obj or not isinstance(generated_style_obj, dict) or not generated_style_obj.get("name"):
                                print_error("Failed to generate AI style or style name missing.")
                                break # Break from inner style source loop
                            base_style = generated_style_obj.get("name")
                            print_success(f"Generated AI base style: {base_style}")
                        except ImportError:
                            print_error("AI style generation module (wall_gen.ai_style_generator) not available.")
                            break # Break from inner style source loop
                        except Exception as e_style:
                            print_error(f"Error during AI style generation: {e_style}")
                            break
                    else: # Should not happen with validated input
                        break

                    # Proceed to generate preset with the determined base_style
                    print_info(f"Now generating full AI preset for style: {base_style}...")
                    result = ai_gen_preset(user_prefs, base_style_override=base_style) # Call the actual preset generator

                    if isinstance(result, str):
                        print_success(f"AI preset '{result}' generated and saved successfully!")
                        # print_info(f"Saved to: {result}") # preset name is in result
                    elif result is None: # User cancelled save or non-unique and retries exhausted
                        print_info("AI preset generation was cancelled or no unique preset could be made.")
                    else:  # result is False (generation failed)
                        print_error("Failed to generate AI preset. See logs or previous messages for details.")
                    break # Break from inner style source loop after attempting generation

                except ImportError as e:
                    logging.error(f"Import error for ai_prest_gen.ai_preset_generator: {e}")
                    print_error("AI preset generator core module (ai_prest_gen.ai_preset_generator.py) not found.")
                    # print_info("Please ensure the file exists and run: pip install google-generativeai") # This is for genai lib, not my module
                    # import traceback # Not needed for user
                    # traceback.print_exc()
                    break # Break from inner style source loop
                except Exception as e:
                    print_error(f"An unexpected error occurred during AI preset generation: {e}")
                    logging.exception("Error in ai_preset_generation.generate_ai_preset (wrapper for style source)")
                    break # Break from inner style source loop
        
        elif choice == "2" and PRESET_MODEL_CONFIG_AVAILABLE:
            select_preset_model_submenu(user_prefs)

        # This input was inside the choice == "1" block, moved out to apply after any action in this menu
        if choice != "b": # Don't ask for Enter if going back immediately
            input("\nPress Enter to return to AI Preset Options menu...")
