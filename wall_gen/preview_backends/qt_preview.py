# preview_backends/qt_preview.py
"""
Main entry point for the Qt Image Preview and Editor.
This file now primarily assembles components from other modules.
"""
import os
import sys

# Set QT environment variables
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
if "QT_DEVICE_PIXEL_RATIO" in os.environ:
    del os.environ["QT_DEVICE_PIXEL_RATIO"]

from PyQt5 import QtWidgets, QtCore, QtGui # Basic Qt imports
from PyQt5.QtWidgets import QMessageBox # For __main__ block

# Import the main application class from its new module
try:
    from .gallery_app import ImageManagerApp
except ImportError as e:
    print(f"FATAL ERROR: Could not import ImageManagerApp from .gallery_app: {e}")
    print("Ensure gallery_app.py, editor_widgets.py, and ui_core.py are in the same directory.")
    ImageManagerApp = None # To prevent further errors if script is run directly

# PIL import for dummy image creation in __main__
from PIL import Image


def preview_image_gui(image_path, set_wallpaper_callback):
    """
    Launches the ImageManagerApp GUI to preview the given image and optionally set it as wallpaper.

    Parameters:
    - image_path (str): Path to the image file to preview.
    - set_wallpaper_callback (callable): Function to call to set the wallpaper.

    Returns:
    - bool: True if the user confirmed setting the wallpaper, False otherwise.
    """
    if ImageManagerApp is None:
        # Show a simple Qt message box if the main app class couldn't be imported
        app_fallback = QtWidgets.QApplication.instance()
        if app_fallback is None: app_fallback = QtWidgets.QApplication(sys.argv)
        QMessageBox.critical(None, "Import Error", 
                             "Failed to load the Image Manager application components. Please check the console for details.")
        return False

    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)

    folder_for_gallery = os.path.dirname(image_path) if image_path and os.path.isfile(image_path) else 'genimage'
    
    manager = ImageManagerApp(app, image_folder=folder_for_gallery, set_wallpaper_callback=set_wallpaper_callback)

    # Load gallery and pre-select the image
    manager.load_gallery() # Load full gallery first
    if image_path and os.path.isfile(image_path):
        # Try to find in QListWidget first (if it's in the current batch)
        # Corrected: Qt.MatchExactly to QtCore.Qt.MatchExactly
        items = manager.gallery_list.findItems(os.path.basename(image_path), QtCore.Qt.MatchExactly)
        if items:
            manager.gallery_list.setCurrentItem(items[0]) # This triggers selection logic
        else:
            # If not in the current batch of gallery_list, or external, select it directly
            manager.select_image(image_path)
            # If image is external to current gallery folder, clear gallery selection visually
            if os.path.dirname(image_path) != os.path.abspath(folder_for_gallery):
                manager.gallery_list.clearSelection() 

    exit_code, was_wallpaper_set, final_path = manager.run()
    return was_wallpaper_set


if __name__ == "__main__":
    # This block is for direct testing of qt_preview.py
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)

    if ImageManagerApp is None:
        print("Cannot run test: ImageManagerApp failed to import.")
        # A simple Qt message box can be shown here too if desired, similar to preview_image_gui
        sys.exit(1)

    def dummy_wallpaper_callback(path_to_set):
        """A simple callback for testing wallpaper setting."""
        print(f"--- DUMMY CALLBACK: Setting wallpaper to: {path_to_set} ---")
        # QMessageBox.information(None, "Wallpaper Set (Dummy)", 
        #                         f"Wallpaper would be set to:\n{os.path.basename(path_to_set)}")
        # To simulate success for testing the return value of manager.run()
        return True 

    image_to_select_on_start = None
    # Use a dedicated test folder to avoid cluttering other directories
    folder_to_use_for_gallery = 'genimage_editor_test_folder' 

    # Create test folder if it doesn't exist and add a dummy image
    if not os.path.exists(folder_to_use_for_gallery):
        try:
            os.makedirs(folder_to_use_for_gallery)
            print(f"Created test gallery folder: {os.path.abspath(folder_to_use_for_gallery)}")
            # Create a dummy image for testing
            dummy_img = Image.new('RGB', (200,150), color='teal')
            dummy_img_path = os.path.join(folder_to_use_for_gallery, "dummy_teal_image.png")
            dummy_img.save(dummy_img_path)
            print(f"Created a dummy test image: {dummy_img_path}")
            if image_to_select_on_start is None: # Select this dummy image if no other is specified
                 image_to_select_on_start = dummy_img_path
        except Exception as e:
            print(f"Could not create dummy test folder/image: {e}")

    # Basic argument parsing for testing
    if len(sys.argv) > 1:
         arg_path = sys.argv[1]
         if os.path.isdir(arg_path): 
             folder_to_use_for_gallery = arg_path
             image_to_select_on_start = None # Don't preselect if a folder is given
         elif os.path.isfile(arg_path):
             folder_to_use_for_gallery = os.path.dirname(arg_path)
             image_to_select_on_start = arg_path
         else:
             print(f"Warning: Argument '{arg_path}' is not a valid file or directory. Using default test folder.")
    
    print(f"Starting Image Manager. Gallery folder: {os.path.abspath(folder_to_use_for_gallery)}")
    if image_to_select_on_start: 
        print(f"Attempting to pre-select: {image_to_select_on_start}")

    manager = ImageManagerApp(app, image_folder=folder_to_use_for_gallery, set_wallpaper_callback=dummy_wallpaper_callback)

    if image_to_select_on_start and os.path.isfile(image_to_select_on_start):
         manager.load_gallery() 
         # Corrected: Qt.MatchExactly to QtCore.Qt.MatchExactly
         items = manager.gallery_list.findItems(os.path.basename(image_to_select_on_start), QtCore.Qt.MatchExactly)
         if items:
             manager.gallery_list.setCurrentItem(items[0])
         else: 
             print(f"Image '{os.path.basename(image_to_select_on_start)}' not in initial gallery view. Previewing directly.")
             manager.select_image(image_to_select_on_start)
             if os.path.dirname(image_to_select_on_start) != os.path.abspath(folder_to_use_for_gallery):
                manager.gallery_list.clearSelection()

    exit_code, result_flag, final_selected_path = manager.run()

    print("\n--- Image Manager Exited (Test Run) ---")
    print(f"Exit Code: {exit_code}")
    print(f"Result (Set Wallpaper chosen?): {result_flag}")
    if result_flag and final_selected_path:
        print(f"Selected Path for Wallpaper: {final_selected_path}")
    print("---------------------------------------")
    sys.exit(exit_code)
