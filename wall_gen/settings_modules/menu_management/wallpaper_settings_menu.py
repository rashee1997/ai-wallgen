# settings_modules/menu_management/wallpaper_settings_menu.py

import re
# Updated import
from wall_gen.ui_utils import (
    print_section,
    print_option,
    print_info,
    print_success,
    print_warning,
    get_validated_input,
    clear_screen, # Added
    print_header, # Added
)
from wall_gen.settings_modules.settings_manager import get_preferences


def manage_wallpaper_settings():
    """
    User menu for configuring wallpaper output settings such as auto-set, preview, and backend.
    """
    user_prefs = get_preferences()
    settings = user_prefs.wallpaper_settings

    while True:
        clear_screen()
        print_header("Wallpaper Settings")
        # print_section("Wallpaper Settings") # Replaced by print_header
        print_option(
            "1",
            f"Automatically Set Wallpaper: {'Yes' if settings.get('auto_set') else 'No'}",
        )
        print_option(
            "2", f"Skip Preview: {'Yes' if settings.get('skip_preview') else 'No'}"
        )
        print_option(
            "3", f"Preview GUI Backend: {settings.get('gui_preview_backend', 'qt')}"
        )
        print_option(
            "4", f"Disable Screen Clearing: {'Yes' if settings.get('disable_screen_clearing') else 'No'}"
        )
        print_option("b", "Back to Previous Menu")

        choice = get_validated_input(
            prompt="Choose an option", 
            options=["1", "2", "3", "4", "b"],
            help_context_id="WALLPAPER_SETTINGS_MENU"
        )
        if choice == "_HELP_SHOWN_":
            continue
        if choice == "1":
            curr = settings.get("auto_set", False)
            settings["auto_set"] = not curr
            print_info(f"Set to {'Yes' if settings['auto_set'] else 'No'}")
        elif choice == "2":
            curr = settings.get("skip_preview", False)
            settings["skip_preview"] = not curr
            print_info(
                f"Skip Preview set to {'Yes' if settings['skip_preview'] else 'No'}"
            )
        elif choice == "3":
            print_info("Select Preview Backend:")
            options = ["qt", "gtk", "console"]
            opt_map = {str(i + 1): val for i, val in enumerate(options)}
            for k, v in opt_map.items():
                print_option(k, v)
            selection = get_validated_input(
                prompt="Choose backend (or 'b' to cancel)", 
                options=list(opt_map.keys()) + ["b"],
                help_context_id="WALLPAPER_SETTINGS_PREVIEW_BACKEND_CHOICE"
            )
            if selection == "_HELP_SHOWN_":
                continue # Will re-enter the main loop of manage_wallpaper_settings, then if '3' is chosen, it re-shows this sub-section
            if selection != "b":
                settings["gui_preview_backend"] = opt_map[selection]
                print_success(f"Preview backend set to {opt_map[selection]}")
        elif choice == "4":
            curr = settings.get("disable_screen_clearing", False)
            settings["disable_screen_clearing"] = not curr
            print_info(f"Disable Screen Clearing set to {'Yes' if settings['disable_screen_clearing'] else 'No'}")
            print_info("This setting will take effect immediately for help screens and menus.")
        elif choice == "b":
            user_prefs.save_preferences()
            return
