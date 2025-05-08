# wall_gen/preview_service.py
"""
Service module for image preview logic (GUI and CLI).
"""
import os
import logging
from datetime import datetime

try:
    # Use absolute package import for ui_utils
    from wall_gen.ui_utils import (
        print_info, print_warning, print_error,
        print_section, get_validated_input, print_success
    )
    # Use absolute imports for sibling modules within the package
    from wall_gen.wallpaper_service import set_os_wallpaper 
    from wall_gen.file_utils import list_sorted_generated_images 
except ImportError:
    logging.warning("Imports failed in preview_service.py. Ensure wall_gen package structure is correct.")
    # Fallback imports (less likely needed now) - Keep absolute
    from wall_gen.ui_utils import (
        print_info, print_warning, print_error,
        print_section, get_validated_input, print_success
    ) 
    from wall_gen.wallpaper_service import set_os_wallpaper
    from wall_gen.file_utils import list_sorted_generated_images


# Attempt to import GUI preview backends
# These will be located in wall_gen/preview_backends/
preview_func_qt = None
preview_func_tkinter = None

try:
    from .preview_backends.qt_preview import preview_image_gui as preview_func_qt
    logging.info("Qt preview backend loaded successfully.")
except ImportError:
    logging.info("Qt preview backend (PySide6/PyQt5/6) not found or failed to load.")
except Exception as e:
    logging.warning(f"Error loading Qt preview backend: {e}")


try:
    from .preview_backends.tkinter_preview import preview_image_gui as preview_func_tkinter
    logging.info("Tkinter preview backend loaded successfully.")
except ImportError:
    logging.info("Tkinter preview backend not found or failed to load.")
except Exception as e:
    logging.warning(f"Error loading Tkinter preview backend: {e}")


def show_preview_and_confirm_set(image_path, user_prefs):
    """
    Handles image preview using the configured GUI backend and confirms if wallpaper should be set.
    (Refactored from preview_and_set_wallpaper in wallpaper_generator.py)

    Args:
        image_path (str): Absolute path to the image to preview.
        user_prefs (UserPreferences): User preferences object.
        
    Returns:
        bool: True if the wallpaper was set, False otherwise.
    """
    print_section("Preview and Set Wallpaper")

    if not os.path.isabs(image_path):
        image_path = os.path.abspath(image_path)
        logging.debug(f"Converted relative image path to absolute: {image_path}")

    if not os.path.exists(image_path):
        logging.error(f"Wallpaper file not found at {image_path} for preview.")
        print_error(f"Preview error: Image file may be missing: {os.path.basename(image_path)}")
        return False

    skip_preview = getattr(user_prefs, "skip_preview", False) or \
                   user_prefs.wallpaper_settings.get("skip_preview", False)

    if skip_preview:
        print_info("Preview skipped by user preference. Attempting to set wallpaper directly...")
        logging.info("Image preview skipped due to user preference.")
        if set_os_wallpaper(image_path):
            print_success(f"Wallpaper successfully applied: {os.path.basename(image_path)}")
            return True
        else:
            print_warning("Wallpaper may not have been set correctly (direct set).")
            return False

    print_info("Preparing to preview your new wallpaper...")
    logging.info(f"Previewing wallpaper with path: {image_path}")

    gui_backend_preference = user_prefs.wallpaper_settings.get("gui_preview_backend", "qt")
    selected_preview_func = None

    if gui_backend_preference == "qt" and preview_func_qt:
        selected_preview_func = preview_func_qt
        logging.info("Using Qt preview backend.")
    elif gui_backend_preference == "tkinter" and preview_func_tkinter:
        selected_preview_func = preview_func_tkinter
        logging.info("Using Tkinter preview backend.")
    else:
        if gui_backend_preference == "qt":
            print_warning("Qt preview backend selected but not available. Check PySide6/PyQt installation.")
        elif gui_backend_preference == "tkinter":
            print_warning("Tkinter preview backend selected but not available.")
        else:
            print_warning(f"Unknown or unavailable GUI preview backend: {gui_backend_preference}.")
        logging.warning(f"GUI preview backend '{gui_backend_preference}' not available.")
        selected_preview_func = None

    wallpaper_set_by_gui = False
    if selected_preview_func:
        try:
            wallpaper_set_by_gui = selected_preview_func(image_path, set_os_wallpaper)
            if wallpaper_set_by_gui:
                print_success(f"Wallpaper successfully applied via GUI: {os.path.basename(image_path)}")
                logging.info(f"Wallpaper set to {image_path} via GUI confirmation.")
                return True 
            else:
                print_info("Wallpaper not set from GUI preview (e.g., user cancelled).")
                logging.info("User did not set wallpaper from GUI preview or preview was closed.")
                return False 
        except Exception as e:
            print_error(f"GUI preview failed: {e}")
            logging.error(f"Error during GUI preview with {gui_backend_preference}: {e}", exc_info=True)
            print_info("GUI preview encountered an error. You can try setting wallpaper via command line.")
    else:
        print_info("No GUI preview available. Proceeding to command-line confirmation.")
    
    confirm_cli = get_validated_input(
        f"Set '{os.path.basename(image_path)}' as wallpaper? (yes/no)", ["yes", "no", "y", "n"]
    )
    if confirm_cli.lower() in ["yes", "y"]:
        if set_os_wallpaper(image_path):
            print_success(f"Wallpaper successfully applied: {os.path.basename(image_path)}")
            return True
        else:
            print_warning("Wallpaper may not have been set correctly (CLI set).")
            return False
    else:
        print_info("Wallpaper not set by user (CLI choice).")
        return False


def handle_list_images_cli(user_prefs):
    """
    Handle listing and previewing images via CLI.
    (Moved from wallpaper_generator.py)
    """
    image_files = list_sorted_generated_images("genimage") 

    if not image_files:
        print_warning("No images found in the genimage directory.")
        return

    print_section("Generated Images")
    print_info(f"Found {len(image_files)} images in the 'genimage' directory.")

    base_genimage_dir = os.path.join(os.getcwd(), "genimage") 

    for i, image_filename in enumerate(image_files, 1):
        full_image_path = os.path.join(base_genimage_dir, image_filename)
        try:
            creation_time_ts = os.path.getmtime(full_image_path)
            creation_time_str = datetime.fromtimestamp(creation_time_ts).strftime("%Y-%m-%d %H:%M:%S")
            print(f"{i}: {image_filename} - Generated: {creation_time_str}")
        except FileNotFoundError:
            print(f"{i}: {image_filename} - Error: File not found at expected path.")


    try:
        choice = get_validated_input(
            f"Enter image number to preview/set (1-{len(image_files)}) or 'q' to quit",
            [str(i) for i in range(1, len(image_files) + 1)] + ["q"],
        )

        if choice.lower() == "q":
            return

        selected_filename = image_files[int(choice) - 1]
        image_path_to_preview = os.path.abspath(os.path.join("genimage", selected_filename)) 
        
        print_info(f"Selected image: {selected_filename}")
        show_preview_and_confirm_set(image_path_to_preview, user_prefs)

    except (ValueError, IndexError) as e:
        print_error(f"Invalid selection: {e}")
    except Exception as e:
        logging.error(f"Error in handle_list_images_cli: {e}", exc_info=True)
        print_error("An unexpected error occurred while listing/previewing images.")


def handle_preview_latest_cli(user_prefs):
    """
    Handle previewing the latest generated image via CLI.
    (Moved from wallpaper_generator.py)
    """
    image_files = list_sorted_generated_images("genimage") 

    if not image_files:
        print_warning("No images found in the genimage directory to preview latest.")
        return

    latest_image_filename = image_files[0] 
    image_path_to_preview = os.path.abspath(os.path.join("genimage", latest_image_filename))

    print_info(f"Previewing latest image: {latest_image_filename}")
    show_preview_and_confirm_set(image_path_to_preview, user_prefs)


def handle_preview_image_cli(image_path_arg, user_prefs):
    """
    Handle previewing a specific image via CLI argument.
    (Moved from wallpaper_generator.py)
    """
    image_path_to_preview = os.path.abspath(image_path_arg)

    print_info(f"Previewing specified image: {image_path_to_preview}")
    if not os.path.exists(image_path_to_preview):
        print_error(f"Image file not found: {image_path_to_preview}")
        return

    show_preview_and_confirm_set(image_path_to_preview, user_prefs)
