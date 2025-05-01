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
            try:
                from ai_preset_generator import generate_ai_preset as ai_gen_preset

                print_info("Attempting to generate AI preset (this may take a moment)...")
                # result: path (str) if saved, None if discarded, False if failed
                result = ai_gen_preset(user_prefs)

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

        input("\nPress Enter to return to the AI Preset menu...")
