#!/usr/bin/env python3
"""
AI Wallpaper Generator - Main Application Script (Refactored)

This script serves as the main entry point for the AI Wallpaper Generator.
It handles command-line arguments, initializes the application, and orchestrates
the wallpaper generation process by calling services from the 'wall_gen' package.
"""

import argparse
import atexit  # Import atexit
import logging
import os
import sys

from typing import Optional
from datetime import datetime  # Added for history timestamp

# Constants for magic strings
GEMINI_API_KEY_ENV = "GEMINI_API_KEY"
LAST_PROMPT_FILENAME = "last_prompt.json"

# --- Initialize wall_gen package ---
# Add project root to sys.path to ensure wall_gen package is found
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)  # Add project root

# --- Imports from wall_gen package ---
try:
    from wall_gen.app_utils import (
        configure_app_logging,
        display_startup_message,
        check_system_dependencies,
        initialize_temp_file_cleanup,
    )
    from wall_gen.cache_utils import initialize_cache_directories
    from wall_gen.settings_modules import (
        initialize_settings,
        UserPreferences,
        get_preferences,
    )
    from wall_gen.prompt_service import generate_final_prompt
    from wall_gen.image_service import generate_image_from_api
    from wall_gen.file_utils import (
        get_image_cache_path,
        check_image_cache,
        move_temp_image_to_cache,
        save_json_data,
        remove_temp_file,
    )
    from wall_gen.preview_service import (
        show_preview_and_confirm_set,
        handle_list_images_cli,
        handle_preview_latest_cli,
        handle_preview_image_cli,
    )
    from wall_gen.history.history_manager import add_to_history
    from wall_gen import graceful_exit  # Import graceful_exit to set the excepthook
except ImportError as e:
    print(
        f"FATAL ERROR: Could not import necessary modules from 'wall_gen' package: {e}"
    )
    print(
        "Please ensure the 'wall_gen' directory and its contents exist and are structured correctly."
    )
    sys.exit(1)

# --- Imports from root (as per user decisions) ---
try:
    from wall_gen.prompt_generator import set_prompt_preferences, use_user_preferences
except ImportError as e:
    import logging

    logging.warning(
        f"Could not import from 'wall_gen.prompt_generator': {e}. Using fallback dummy functions."
    )

    def set_prompt_preferences(use_prefs):
        logging.warning(
            "Fallback set_prompt_preferences called; no operation performed."
        )

    def use_user_preferences():
        logging.warning(
            "Fallback use_user_preferences called; returning True by default."
        )
        return True


# --- Preference Saving on Exit ---
def save_prefs_on_exit(prefs_to_save: Optional[UserPreferences]):
    """Function to be called by atexit to save preferences."""
    try:
        from wall_gen.ui_utils import print_info, print_success, print_error

        ui_available = True
    except ImportError:
        ui_available = False

    if prefs_to_save and isinstance(prefs_to_save, UserPreferences):
        try:
            if ui_available:
                print_info("\nAttempting to save preferences on exit...")
            logging.info("Attempting to save preferences via atexit handler...")
            prefs_to_save.save_preferences()
            if ui_available:
                print_success("Preferences saved successfully.")
            logging.info("Preferences saved successfully via atexit.")
        except Exception as e:
            if ui_available:
                print_error(f"Error saving preferences on exit: {e}")
            logging.error(f"Error saving preferences via atexit: {e}", exc_info=True)
    else:
        logging.warning("No valid UserPreferences object available to save on exit.")


# --- Argument Parsing ---
def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="AI Wallpaper Generator (Refactored Entry Point)",
        formatter_class=argparse.RawTextHelpFormatter,  # Preserve formatting in help
    )
    # Generation Modes
    gen_group = parser.add_argument_group("Generation Modes")
    gen_group.add_argument(
        "--prompt", help="Generate wallpaper using a custom prompt text."
    )
    gen_group.add_argument(
        "--random",
        action="store_true",
        help="Generate a random wallpaper based on preferences or general tags.",
    )
    gen_group.add_argument(
        "--preset", help="Generate wallpaper using a saved preset name."
    )  # New/Improved

    # Testing & Debugging
    test_group = parser.add_argument_group("Testing & Debugging")
    test_group.add_argument(
        "--test-prompt",
        help="Test prompt generation for a subject without creating an image.",
    )
    test_group.add_argument(
        "--test-custom-prompt",
        help="Test custom prompt enhancement without creating an image.",
    )
    test_group.add_argument(
        "--no-generate",
        action="store_true",
        help="Generate and show the prompt, but do not generate the image.",
    )
    test_group.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output (INFO level logging).",
    )
    test_group.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging (DEBUG level logging).",
    )

    # Preference Overrides
    pref_group = parser.add_argument_group("Preference Overrides")
    pref_group.add_argument(
        "--resolution", help="Override resolution (e.g., '1920x1080')."
    )
    pref_group.add_argument(
        "--aspect-ratio", help="Override aspect ratio (e.g., '16:9', '9:16')."
    )
    pref_group.add_argument(
        "--dont-use-user-prefs",
        action="store_true",
        help="Ignore saved user preferences for prompt generation.",
    )
    pref_group.add_argument(
        "--no-preset-load",
        action="store_true",
        help="Skip loading the last used preset on startup (for menu mode).",
    )

    # Image Management & Preview
    img_group = parser.add_argument_group("Image Management & Preview")
    img_group.add_argument(
        "--skip-preview",
        action="store_true",
        help="Skip the image preview GUI and set wallpaper directly.",
    )
    img_group.add_argument(
        "--preview-image", help="Preview a specific image file using the GUI."
    )
    img_group.add_argument(
        "--preview-latest",
        action="store_true",
        help="Preview the latest generated image from the 'genimage' folder.",
    )
    img_group.add_argument(
        "--list-images",
        action="store_true",
        help="List generated images and choose one to preview/set.",
    )

    # AI Preset Generator
    ai_preset_group = parser.add_argument_group("AI Preset Generator")
    ai_preset_group.add_argument(
        "--generate-preset", help="Generate AI wallpaper preset for a given style."
    )
    ai_preset_group.add_argument(
        "--apply-preset", help="Apply a preset by name or file path."
    )

    return parser.parse_args()


# --- Helper functions for orchestration ---
def _generate_prompt(prompt_type, user_prefs_obj, custom_prompt=None, preset_name=None):
    """Generate the final prompt and base prompt for history."""
    from wall_gen.ui_utils import print_info, print_error, print_warning

    if prompt_type == "preset":
        print_warning(
            f"Preset loading via CLI not fully implemented yet. Treating '{preset_name}' as custom prompt."
        )
        prompt_type = "custom"
        custom_prompt = preset_name

    try:
        if prompt_type == "custom":
            if not custom_prompt:
                print_error("Custom prompt text is required for 'custom' prompt type.")
                return None, None
            print_info("Enhancing custom prompt...")
            return generate_final_prompt("custom", user_prefs_obj, custom_prompt)
        elif prompt_type == "random":
            print_info("Generating random prompt...")
            return generate_final_prompt("random", user_prefs_obj)
        else:  # Default to 'gemini'
            print_info("Generating AI prompt using preferences...")
            return generate_final_prompt("gemini", user_prefs_obj)
    except Exception as e:
        logging.error(f"Error during prompt generation: {e}", exc_info=True)
        print_error(f"Failed to generate prompt: {e}")
        return None, None


def _generate_image(final_prompt, user_prefs_obj):
    """Generate image from API and return temp image path."""
    from wall_gen.ui_utils import print_error, print_success, show_spinner

    if not os.environ.get(GEMINI_API_KEY_ENV):
        print_error(
            f"Cannot generate image: {GEMINI_API_KEY_ENV} environment variable not set."
        )
        return None

    show_spinner("Requesting image from AI...", 2)
    try:
        temp_image_paths = generate_image_from_api(final_prompt, user_prefs_obj)
        if not temp_image_paths:
            print_error("Image generation failed (no image data returned).")
            return None
        temp_image_path = temp_image_paths[0]
        print_success(
            f"Image data received, saved to temporary file: {temp_image_path}"
        )
        return temp_image_path
    except Exception as e:
        logging.error(f"Error during image generation API call: {e}", exc_info=True)
        print_error(f"Image generation failed: {e}")
        return None


def _cache_and_save_image(final_prompt, temp_image_path):
    """Cache and save the generated image, return final image path."""
    from wall_gen.ui_utils import print_info, print_success, print_error

    try:
        final_image_path = get_image_cache_path(final_prompt, PROJECT_ROOT)
        print_info(
            f"Image will be saved to: {os.path.relpath(final_image_path, PROJECT_ROOT)}"
        )

        if check_image_cache(final_image_path):
            print_info("Image already exists in cache. Using cached version.")
            remove_temp_file(temp_image_path)
            return final_image_path
        else:
            if move_temp_image_to_cache(temp_image_path, final_image_path):
                print_success(
                    f"Image saved successfully: {os.path.basename(final_image_path)}"
                )
                return final_image_path
            else:
                print_error("Failed to move image to final cache location.")
                return None
    except Exception as e:
        logging.error(f"Error during image caching/saving: {e}", exc_info=True)
        print_error(f"Failed to save image: {e}")
        return None


def _add_history_entry(
    prompt_type, base_prompt_for_history, final_prompt, final_image_path, user_prefs_obj
):
    """Add generation details to history."""
    try:
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt_type": prompt_type,
            "base_prompt": base_prompt_for_history,
            "final_prompt": final_prompt,
            "image_filename": (
                os.path.basename(final_image_path) if final_image_path else None
            ),
            "settings_summary": {
                "aspect_ratio": user_prefs_obj.aspect_ratio,
                "resolution": user_prefs_obj.imagen_settings.get(
                    "quality_settings", {}
                ).get("resolution"),
                "style": (
                    user_prefs_obj.preferred_styles[0]
                    if user_prefs_obj.preferred_styles
                    else None
                ),
                "mood": (
                    user_prefs_obj.preferred_moods[0]
                    if user_prefs_obj.preferred_moods
                    else None
                ),
                "seed": user_prefs_obj.imagen_settings.get("seed"),
            },
        }
        add_to_history(history_entry)
        logging.info(
            f"Added entry to history for image: {history_entry['image_filename']}"
        )
    except Exception as e:
        logging.error(f"Failed to add entry to history: {e}", exc_info=True)
        from wall_gen.ui_utils import print_warning

        print_warning("Failed to save generation details to history.")


def _preview_and_set_wallpaper(final_image_path, user_prefs_obj):
    """Show preview and confirm setting wallpaper."""
    from wall_gen.ui_utils import print_info, print_success, print_error

    try:
        wallpaper_set_successfully = show_preview_and_confirm_set(
            final_image_path, user_prefs_obj
        )
        if wallpaper_set_successfully:
            print_success("Wallpaper process completed successfully.")
            return True
        else:
            print_info("Wallpaper was generated but not set.")
            return True
    except Exception as e:
        logging.error(f"Error during preview/set wallpaper stage: {e}", exc_info=True)
        print_error(f"Failed during preview/set wallpaper: {e}")
        return False


# --- Core Orchestration Logic ---
def orchestrate_wallpaper_generation(
    prompt_type: str,  # 'gemini', 'random', 'custom', 'preset'
    user_prefs_obj: UserPreferences,
    custom_prompt: Optional[str] = None,
    preset_name: Optional[str] = None,
    generate_only: bool = False,
):
    """
    Orchestrates the wallpaper generation process.
    (Refactored from generate_wallpaper in original script)
    """
    final_prompt = None
    base_prompt_for_history = (
        None  # Store the initial prompt (custom or gemini-generated base)
    )
    temp_image_path = None  # Define here for cleanup in finally block

    from wall_gen.ui_utils import print_section

    try:
        print_section("Generating Prompt")
        final_prompt, base_prompt_for_history = _generate_prompt(
            prompt_type, user_prefs_obj, custom_prompt, preset_name
        )
        if not final_prompt:
            return False

        print_section("Confirm Prompt")
        from wall_gen.ui_utils import print_info

        print_info(f"Generated Prompt:\n{final_prompt}")

        save_json_data(
            {"base_prompt": base_prompt_for_history, "final_prompt": final_prompt},
            LAST_PROMPT_FILENAME,
            PROJECT_ROOT,
        )

        if generate_only:
            from wall_gen.ui_utils import print_success

            print_success("Prompt generation complete (image generation skipped).")
            return True

        from wall_gen.ui_utils import get_validated_input

        confirm = get_validated_input(
            "Proceed with this prompt? (yes/no)", ["yes", "no", "y", "n"]
        )
        if confirm.lower() not in ["yes", "y"]:
            from wall_gen.ui_utils import print_info

            print_info("Generation cancelled by user.")
            return False

        print_section("Generating Image")
        temp_image_path = _generate_image(final_prompt, user_prefs_obj)
        if not temp_image_path:
            return False

        final_image_path = _cache_and_save_image(final_prompt, temp_image_path)
        if not final_image_path:
            return False

        _add_history_entry(
            prompt_type,
            base_prompt_for_history,
            final_prompt,
            final_image_path,
            user_prefs_obj,
        )

        return _preview_and_set_wallpaper(final_image_path, user_prefs_obj)

    finally:
        if temp_image_path and os.path.exists(temp_image_path):
            logging.warning(
                f"Cleaning up orphaned temporary image file: {temp_image_path}"
            )
            remove_temp_file(temp_image_path)


# --- Main Execution ---
def main():
    """Main function handling initialization and command-line dispatch."""
    global user_prefs

    args = parse_args()

    # Configure Logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    configure_app_logging(log_level, project_root_dir=PROJECT_ROOT)
    logging.info("--- AI Wallpaper Generator Session Start ---")

    # Display Startup Message
    display_startup_message()

    # Check Dependencies
    check_system_dependencies()

    # Initialize Cache Dirs
    initialize_cache_directories(project_root_dir=PROJECT_ROOT)

    # Register Temp File Cleanup
    initialize_temp_file_cleanup()

    # Load User Preferences
    try:
        user_prefs = initialize_settings()
        if not isinstance(user_prefs, UserPreferences):
            raise TypeError("initialize_settings did not return UserPreferences object")
        # Register the save function to be called on exit
        atexit.register(save_prefs_on_exit, user_prefs)
    except Exception as e:
        logging.error(f"Failed to initialize user preferences: {e}", exc_info=True)
        from wall_gen.ui_utils import print_error

        print_error(f"Critical error: Could not load user preferences: {e}")
        sys.exit(1)

    # Handle Preference Overrides from CLI args
    set_prompt_preferences(not args.dont_use_user_prefs)
    if args.resolution:
        user_prefs.imagen_settings.setdefault("quality_settings", {})[
            "resolution"
        ] = args.resolution
        logging.info(f"CLI override: Resolution set to {args.resolution}")
    if args.aspect_ratio:
        # TODO: Validate aspect ratio format here
        user_prefs.aspect_ratio = args.aspect_ratio
        logging.info(f"CLI override: Aspect ratio set to {args.aspect_ratio}")
    if args.skip_preview:
        user_prefs.wallpaper_settings["skip_preview"] = True
        logging.info("CLI override: Skipping preview.")

    # Check API Key (essential for generation)
    if not os.environ.get(GEMINI_API_KEY_ENV):
        from wall_gen.ui_utils import (
            print_warning as ui_print_warning,
            print_info as ui_print_info,
        )

        ui_print_warning(
            f"\nWARNING: {GEMINI_API_KEY_ENV} environment variable not set."
        )
        ui_print_info(
            "AI image generation and AI prompt features will not be available."
        )

    # Import AI preset generator functions
    try:
        from ai_prest_gen.ai_preset_generator import generate_ai_preset
    except ImportError as e:
        logging.error(
            f"Failed to import AI preset generator functions: {e}", exc_info=True
        )
        generate_ai_preset = None

    # --- Dispatch based on CLI Arguments ---
    exit_code = 0
    try:
        if args.generate_preset:
            if generate_ai_preset is None:
                logging.error("AI preset generator function not available.")
                from wall_gen.ui_utils import print_error

                print_error("AI preset generator function not available.")
                exit_code = 1
            else:
                from wall_gen.ui_utils import print_info, print_success, print_error

                print_info(f"Generating AI preset for style: {args.generate_preset}")
                try:
                    success = generate_ai_preset(
                        style_override=args.generate_preset, user_prefs=user_prefs
                    )
                    if success:
                        print_success("AI preset generated successfully.")
                    else:
                        print_error("AI preset generation failed.")
                        exit_code = 1
                except Exception as e:
                    logging.error(
                        f"Error during AI preset generation: {e}", exc_info=True
                    )
                    print_error(f"Error during AI preset generation: {e}")
                    exit_code = 1
        elif args.apply_preset:
            from wall_gen.ui_utils import print_info, print_success, print_error

            print_info(f"Applying preset: {args.apply_preset}")
            try:
                from wall_gen.settings_modules.preset_management import (
                    _apply_preset_settings,
                )

                presets_dir = os.path.join(PROJECT_ROOT, "presets")
                preset_identifier = args.apply_preset

                if os.path.exists(
                    preset_identifier
                ) and preset_identifier.lower().endswith(".json"):
                    preset_path = preset_identifier
                else:
                    preset_name = preset_identifier
                    if not preset_name.lower().endswith(".json"):
                        preset_name += ".json"
                    preset_path = os.path.join(presets_dir, preset_name)

                if not os.path.exists(preset_path):
                    print_error(f"Preset file '{preset_path}' not found.")
                    exit_code = 1
                else:
                    import json

                    with open(preset_path, "r") as f:
                        settings_to_apply = json.load(f)
                    success = _apply_preset_settings(settings_to_apply, replace=True)
                    if success:
                        print_success("Preset applied successfully.")
                    else:
                        print_error("Preset application failed.")
                        exit_code = 1
            except Exception as e:
                logging.error(f"Error during preset application: {e}", exc_info=True)
                print_error(f"Error during preset application: {e}")
                exit_code = 1

        elif args.list_images:
            if user_prefs is not None:
                handle_list_images_cli(user_prefs)
            else:
                logging.error("User preferences not initialized; cannot list images.")
        elif args.preview_latest:
            if user_prefs is not None:
                handle_preview_latest_cli(user_prefs)
            else:
                logging.error(
                    "User preferences not initialized; cannot preview latest image."
                )
        elif args.preview_image:
            if user_prefs is not None:
                handle_preview_image_cli(args.preview_image, user_prefs)
            else:
                logging.error("User preferences not initialized; cannot preview image.")
        elif args.test_prompt:
            from wall_gen.ui_utils import (
                print_section as ui_print_section,
                print_info as ui_print_info,
            )

            ui_print_section("Testing Prompt Generation")
            if user_prefs is not None:
                test_final_prompt, _ = generate_final_prompt(
                    "gemini", user_prefs, custom_prompt_text=None
                )
                ui_print_info(f"Test Generated Prompt:\n{test_final_prompt}")
            else:
                logging.error(
                    "User preferences not initialized; cannot test prompt generation."
                )
        elif args.test_custom_prompt:
            from wall_gen.ui_utils import (
                print_section as ui_print_section,
                print_info as ui_print_info,
            )

            ui_print_section("Testing Custom Prompt Enhancement")
            if user_prefs is not None:
                test_final_prompt, _ = generate_final_prompt(
                    "custom", user_prefs, custom_prompt_text=args.test_custom_prompt
                )
                ui_print_info(f"Test Enhanced Prompt:\n{test_final_prompt}")
            else:
                logging.error(
                    "User preferences not initialized; cannot test custom prompt enhancement."
                )
        elif args.prompt:
            if user_prefs is not None:
                orchestrate_wallpaper_generation(
                    "custom",
                    user_prefs,
                    custom_prompt=args.prompt,
                    generate_only=args.no_generate,
                )
            else:
                logging.error(
                    "User preferences not initialized; cannot generate wallpaper."
                )
        elif args.random:
            if user_prefs is not None:
                orchestrate_wallpaper_generation(
                    "random", user_prefs, generate_only=args.no_generate
                )
            else:
                logging.error(
                    "User preferences not initialized; cannot generate wallpaper."
                )
        elif args.preset:
            if user_prefs is not None:
                orchestrate_wallpaper_generation(
                    "preset",
                    user_prefs,
                    preset_name=args.preset,
                    generate_only=args.no_generate,
                )
            else:
                logging.error(
                    "User preferences not initialized; cannot generate wallpaper."
                )
        else:
            from wall_gen.ui_utils import print_info as ui_print_info

            ui_print_info("\n🚀 No CLI task given. Launching interactive menu to explore possibilities...")
            try:
                from wall_gen.settings_modules.menu_management import main_menu

                main_menu.run_main_menu()
            except ImportError as e:
                from wall_gen.ui_utils import print_error as ui_print_error

                ui_print_error(f"Could not load the main menu: {e}")
                logging.error("Failed to import or run main_menu", exc_info=True)
                exit_code = 1
    except Exception as e:
        logging.critical(
            f"An unhandled error occurred in main dispatch: {e}", exc_info=True
        )
        from wall_gen.ui_utils import print_error as ui_print_error

        ui_print_error(f"An unexpected error occurred: {e}")
        exit_code = 1
    finally:
        logging.info("--- AI Wallpaper Generator Session End ---")
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
