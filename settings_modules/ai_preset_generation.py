import os
import logging
from ui_utils import (
    print_section, print_option, print_success, print_error, print_warning,
    print_info, get_validated_input
)
from .settings_manager import get_preferences

def generate_ai_preset():
    """
    Generate an AI-based preset using Gemini (or other AI backend).
    This function wraps the ai_preset_generator module's functionality for interactive use.
    """
    user_prefs = get_preferences()
    while True:
        print_section("Generate AI Preset")
        print_option("1", "Generate New AI Preset using Gemini")
        print_option("b", "Back")

        choice = get_validated_input("Select option (1, b)", ["1", "b"])
        if choice == "b":
            return

        if choice == "1":
            # Added style source submenu
            while True:
                print_section("Choose Style Source for Preset")
                print_option("1", "Enter Custom Style")
                print_option("2", "Generate AI Style")
                print_option("b", "Back")
                style_choice = get_validated_input("Select option (1-2, b)", ["1", "2", "b"])
                if style_choice == "b":
                    break

                try:
                    from ai_preset_generator import generate_ai_preset as ai_gen_preset

                    # Only show "Attempting to generate AI preset" if generating AI style (not for custom)
                    if style_choice == "1":
                        base_style = get_validated_input("Enter your custom style: ", allow_empty=False)
                        if not base_style:
                            print_error("No style entered.")
                            break
                    else:
                        print_info("Attempting to generate AI preset (this may take a moment)...")
                        # Generate AI Style
                        try:
                            from ai_style_generator import generate_random_style, initialize_gemini
                            api_key = os.environ.get("GEMINI_API_KEY")
                            if not api_key:
                                print_error("GEMINI_API_KEY environment variable not set.")
                                break
                            print_info("Generating AI style...")
                            initialize_gemini(api_key)
                            base_style = generate_random_style()
                            if not base_style:
                                print_error("Failed to generate AI style.")
                                break
                            print_success(f"Generated AI style: {base_style}")
                        except ImportError:
                            print_error("AI style generation is not available (ai_style_generator import failed).")
                            break

                    result = ai_gen_preset(user_prefs, base_style_override=base_style)

                    if isinstance(result, str):
                        print_success(f"AI preset generated and saved successfully!")
                        print_info(f"Saved to: {result}")
                    elif result is None:
                        print_info("AI preset generated but discarded by user.")
                    else:  # result is False
                        print_warning("Failed to generate AI preset. See logs or previous messages for details.")

                except ImportError:
                    print_warning("AI preset generator module (ai_preset_generator.py) not found or google-generativeai is not installed.")
                    print_info("Please ensure the file exists and run: pip install google-generativeai")
                except Exception as e:
                    print_error(f"An unexpected error occurred during AI preset generation: {e}")
                    logging.exception("Error in ai_preset_generation.generate_ai_preset wrapper")
                break

        input("\nPress Enter to return to the AI Preset menu...")
