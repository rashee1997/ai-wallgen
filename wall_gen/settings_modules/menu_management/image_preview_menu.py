"""
Image preview menu module.

This module provides functionality for previewing and managing generated images.
"""

import logging # Added logging
import os
from datetime import datetime
from typing import List
# Updated imports
from wall_gen.ui_utils import (
    print_section,
    print_info,
    print_warning,
    print_error,
    print_success,
    get_validated_input,
)


def run_image_preview_menu():
    """
    Display and preview recent generated images.

    Returns:
        None
    """
    try:
        # Get list of images using helper function from wall_gen.file_utils
        from wall_gen.file_utils import list_sorted_generated_images
        # Assuming 'genimage' is relative to project root (where run_wallgen.py is)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) # Navigate up from wall_gen/settings_modules/menu_management
        genimage_abs_path = os.path.join(project_root, "genimage")

        image_files = list_sorted_generated_images(genimage_abs_path)

        if not image_files:
            print_warning("No images found in the genimage directory.")
            return

        print_section("Recent Generated Images")
        print_info(f"Found {len(image_files)} images in the genimage directory.")

        # Limit to showing the 20 most recent images for better user experience
        max_display = min(20, len(image_files))
        display_files = image_files[:max_display]

        # Display the images with their numbers
        for i, image_file in enumerate(display_files, 1):
            # Need to construct the full path to get modification time
            full_path = os.path.join("genimage", image_file)
            creation_time = datetime.fromtimestamp(
                os.path.getmtime(full_path)
            ).strftime("%Y-%m-%d %H:%M:%S")
            print(f"{i}: {image_file} - Generated: {creation_time}")

        # Import the appropriate preview function based on user preferences
        preview_func_qt = None
        preview_func_tkinter = None
        gui_backend = None
        try:
            # Use relative import for settings_manager
            from ..settings_manager import get_preferences
            user_prefs = get_preferences()
            # Ensure wallpaper_settings exists
            if hasattr(user_prefs, 'wallpaper_settings') and isinstance(user_prefs.wallpaper_settings, dict):
                gui_backend = user_prefs.wallpaper_settings.get("gui_preview_backend", "qt")
            else:
                gui_backend = "qt" # Default if setting is missing
        except Exception:
            gui_backend = "qt"

        # Import preview backends using absolute package paths
        if gui_backend == "qt":
            try:
                from wall_gen.preview_backends.qt_preview import preview_image_gui as preview_func_qt
            except ImportError:
                print_warning(
                    "Qt preview backend selected but PySide6 (or PyQt5/6) not found." # Keep user message
                )
                print_info("Please install PySide6: pip install PySide6")
                print_info("Falling back to no preview.")
                preview_func_qt = None
        elif gui_backend == "tkinter":
            try:
                from wall_gen.preview_backends.tkinter_preview import preview_image_gui as preview_func_tkinter
            except ImportError:
                print_warning(
                    "Tkinter preview backend selected but Tkinter not available." # Keep user message
                )
                print_info(
                    "Tkinter is usually included with Python, but may require a separate package on some Linux distributions."
                )
                print_info("Falling back to no preview.")
                preview_func_tkinter = None
        else:
            print_warning(
                f"Unknown GUI preview backend specified: {gui_backend}. Falling back to no preview."
            )
            # preview_func remains None

        # Select the correct preview function based on preference
        selected_preview_func = preview_func_qt if gui_backend == "qt" else preview_func_tkinter

        # Ask user which image to preview in a loop until they quit
        try:
            while True:
                valid_choices = [str(i) for i in range(1, max_display + 1)] + ["q"]
                choice = get_validated_input(
                    f"Enter image number to preview (1-{max_display}) or 'q' to quit",
                    valid_choices,
                )

                if choice.lower() == "q":
                    return

                # Preview the selected image - need full absolute path
                image_filename = display_files[int(choice) - 1]
                image_path_abs = os.path.abspath(os.path.join("genimage", image_filename)) # Ensure absolute path
                print_info(f"Previewing image: {image_filename}")

                # Preview image with GUI
                if selected_preview_func:
                    try:
                        # Import the correct wallpaper setting function
                        from wall_gen.wallpaper_service import set_os_wallpaper
                        # The preview function now handles calling set_os_wallpaper if confirmed
                        wallpaper_set = selected_preview_func(image_path_abs, set_os_wallpaper)
                        if wallpaper_set:
                            print_success("Wallpaper set successfully via preview!")
                        # else: # User cancelled or preview closed without setting
                        #    print_info("Wallpaper not set from preview.")
                    except ImportError:
                         print_error("Could not import wallpaper setting function.")
                    except Exception as preview_err:
                         print_error(f"Error during GUI preview: {preview_err}")
                         logging.error(f"Error in preview GUI for {image_path_abs}: {preview_err}", exc_info=True)
                else:
                    print_warning("Preview functionality not available.")

                # After viewing one image, we allow picking another or returning to menu
                print_section("Recent Generated Images")

        except (ValueError, IndexError) as e:
            print_error(f"Invalid selection: {e}")

    except (FileNotFoundError, OSError) as e:
        print_error(f"Error accessing images directory: {e}")
