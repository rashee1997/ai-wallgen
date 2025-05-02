"""
Image preview menu module.

This module provides functionality for previewing and managing generated images.
"""

from typing import List
from datetime import datetime
import os
from ui_utils import (
    print_section, print_info, print_warning, print_error, print_success,
    get_validated_input
)

def run_image_preview_menu():
    """
    Display and preview recent generated images.
    
    Returns:
        None
    """
    try:
        # Get list of images using helper function
        from wallpaper_generator import list_sorted_genimages
        image_files = list_sorted_genimages("genimage")

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
        preview_func = None
        gui_backend = None
        try:
            from settings_modules.settings_manager import get_preferences
            user_prefs = get_preferences()
            gui_backend = user_prefs.wallpaper_settings.get('gui_preview_backend', 'qt')
        except Exception:
            gui_backend = 'qt'

        if gui_backend == 'qt':
            try:
                from qt_preview import preview_image_gui as preview_func
            except ImportError:
                print_warning("Qt preview backend selected but PySide6 (or PyQt5/6) not found.")
                print_info("Please install PySide6: pip install PySide6")
                print_info("Falling back to no preview.")
                preview_func = None
        elif gui_backend == 'tkinter':
            try:
                from tkinter_preview import preview_image_gui as preview_func
            except ImportError:
                print_warning("Tkinter preview backend selected but Tkinter not available.")
                print_info("Tkinter is usually included with Python, but may require a separate package on some Linux distributions.")
                print_info("Falling back to no preview.")
                preview_func = None
        else:
            print_warning(f"Unknown GUI preview backend specified: {gui_backend}. Falling back to no preview.")
            preview_func = None

        # Ask user which image to preview in a loop until they quit
        try:
            while True:
                valid_choices = [str(i) for i in range(1, max_display + 1)] + ['q']
                choice = get_validated_input(
                    f"Enter image number to preview (1-{max_display}) or 'q' to quit",
                    valid_choices
                )

                if choice.lower() == 'q':
                    return

                # Preview the selected image - need full path
                image_path = os.path.join("genimage", display_files[int(choice) - 1])
                print_info(f"Previewing image: {display_files[int(choice) - 1]}")

                # Preview image with GUI
                if preview_func:
                    from wallpaper_generator import set_wallpaper
                    result = preview_func(image_path, set_wallpaper)
                    if result:
                        print_success("Wallpaper set successfully!")
                else:
                    print_warning("Preview functionality not available.")

                # After viewing one image, we allow picking another or returning to menu
                print_section("Recent Generated Images")

        except (ValueError, IndexError) as e:
            print_error(f"Invalid selection: {e}")

    except (FileNotFoundError, OSError) as e:
        print_error(f"Error accessing images directory: {e}")
