import os
import logging
from wall_gen.ui_utils import (
    print_section, print_option, print_success, print_error, print_warning,
    print_info, get_validated_input
)
from .settings_manager import get_preferences

# Imports for AI Preset Generator core components
try:
    import ai_prest_gen.preset_generator_engine as preset_generator_engine
    import ai_prest_gen.style_categorizer as style_categorizer
    import ai_prest_gen.prompt_builder as prompt_builder
    import ai_prest_gen.preset_cache_manager as preset_cache_manager
    import ai_prest_gen.config as ai_prest_gen_config # Import config for cache file name

    PRESET_GENERATOR_AVAILABLE = True
except ImportError as e:
    PRESET_GENERATOR_AVAILABLE = False
    logging.error(f"AI Preset Generator core components or config missing: {e}")
    print_error("AI Preset Generator core components are not available. Preset generation will be unavailable.")

# Imports and fallbacks for Gemini model selection for presets (moved outside main try block)
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

# Fallback for generate_ai_preset if the main generator is not available
if not PRESET_GENERATOR_AVAILABLE:
    def ai_gen_preset_fallback(user_prefs, base_style_override=None, auto_save_flag=False):
        print_error("AI Preset Generator is not available due to missing components.")
        return False
    # Need to define a dummy PresetGenerator instance or handle its absence
    # The logic below in generate_ai_preset will need to check PRESET_GENERATOR_AVAILABLE

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
            if not PRESET_GENERATOR_AVAILABLE:
                print_error("AI Preset Generator is not available due to missing components. Cannot generate preset.")
                input("\nPress Enter to continue...")
                continue # Continue outer menu loop

            # Instantiate dependencies and the PresetGenerator
            try:
                style_categorizer_instance = style_categorizer.StyleCategorizer()
                prompt_builder_instance = prompt_builder.PresetPromptBuilder()
                # Use config for cache file name
                preset_cache_manager_instance = preset_cache_manager.PresetCacheManager(ai_prest_gen_config.PRESETS_CACHE_FILE_NAME)
                preset_generator_instance = preset_generator_engine.PresetGenerator(
                    style_categorizer=style_categorizer_instance,
                    prompt_builder=prompt_builder_instance,
                    preset_cache_manager=preset_cache_manager_instance
                )
            except Exception as e:
                print_error(f"Failed to initialize AI Preset Generator components: {e}")
                logging.error("Error initializing PresetGenerator components", exc_info=True)
                input("\nPress Enter to continue...")
                continue # Continue outer menu loop

            while True: # Inner loop for style source
                print_section("Choose Style Source for Preset")
                print_option("1", "Enter Custom Style")
                print_option("2", "Generate AI Style")
                print_option("b", "Back")
                style_choice = get_validated_input("Select option (1-2, b): ", ["1", "2", "b"])
                if style_choice == "b":
                    break

                base_style = None # Initialize base_style

                if style_choice == "1":
                    base_style_input = get_validated_input("Enter your custom style: ", allow_empty=False)
                    if not base_style_input:
                        print_error("No style entered.")
                        break # Break from inner style source loop
                    base_style = base_style_input
                elif style_choice == "2": # Generate AI Style
                    print_info("Attempting to generate base AI style (this may take a moment)...")
                    try:
                        # AI Style Generator likely uses its own global Gemini config from wall_gen.gemini_config
                        # No need to pass API key if that global config handles it.
                        from wall_gen.ai_style_generator import generate_random_style, initialize_gemini as init_style_gem_global
                        if not init_style_gem_global(None): # Assuming it can init without explicit key if globally set
                            print_error("Failed to initialize Gemini for AI Style Generation.")
                            break # Break from inner style source loop

                        generated_style_obj = generate_random_style(style_type="detailed")
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

                if base_style: # Only proceed if a base style was successfully determined
                    # Proceed to generate preset with the determined base_style
                    print_info(f"Now generating full AI preset for style: {base_style}...")
                    # Call the generate_ai_preset method on the instantiated object
                    result = preset_generator_instance.generate_ai_preset(user_prefs, base_style_override=base_style)

                    if isinstance(result, str):
                        print_success(f"AI preset '{result}' generated and saved successfully!")
                    elif result is None: # User cancelled save or non-unique and retries exhausted
                        print_info("AI preset generation was cancelled or no unique preset could be made.")
                    else:  # result is False (generation failed)
                        print_error("Failed to generate AI preset. See logs or previous messages for details.")
                    break # Break from inner style source loop after attempting generation
                else:
                    # If base_style is None, it means the user cancelled or an error occurred in style selection
                    print_info("Base style selection cancelled or failed.")
                    break # Break from inner style source loop

        elif choice == "2" and PRESET_MODEL_CONFIG_AVAILABLE:
            select_preset_model_submenu(user_prefs)

        # This input was inside the choice == "1" block, moved out to apply after any action in this menu
        if choice != "b": # Don't ask for Enter if going back immediately
            input("\nPress Enter to return to AI Preset Options menu...")

        # This input was inside the choice == "1" block, moved out to apply after any action in this menu
        if choice != "b": # Don't ask for Enter if going back immediately
            input("\nPress Enter to return to AI Preset Options menu...")
