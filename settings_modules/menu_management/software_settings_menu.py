import logging
from ui_utils import (
    print_section, print_option, print_info, print_success, print_warning,
    print_error, get_validated_input
)
from ..settings_manager import get_preferences

def manage_software_settings():
    """
    Interactive menu for editing 3D/CGI software settings:
        - suite (e.g. Blender, Maya, Cinema 4D)
        - renderer (e.g. Cycles, Arnold, Octane, Eevee)
        - version (e.g. 3.6, 2024, R25, etc.)
    """
    user_prefs = get_preferences()
    software_settings = user_prefs.imagen_settings.get("software_settings", {})

    suite_options = [
        "Blender", "Maya", "Cinema 4D", "3ds Max", "Unreal Engine",
        "ZBrush", "Houdini", "SketchUp", "KeyShot", "Custom"
    ]
    renderer_options = [
        "Cycles", "Eevee", "Arnold", "Octane", "Redshift", "V-Ray", "Corona", "Custom"
    ]

    while True:
        print_section("3D/CGI Software Settings")
        print_info(f"Suite: {software_settings.get('suite', '[Not Set]')}")
        print_info(f"Renderer: {software_settings.get('renderer', '[Not Set]')}")
        print_info(f"Version: {software_settings.get('version', '[Not Set]')}")
        print_option("1", "Edit Suite")
        print_option("2", "Edit Renderer")
        print_option("3", "Edit Version")
        print_option("c", "Clear All")
        print_option("b", "Back to Advanced Options")

        choice = get_validated_input("Choose:", ["1", "2", "3", "c", "b"])
        if choice == "1":
            for idx, val in enumerate(suite_options, 1):
                print_option(str(idx), val)
            idx_map = {str(i+1): v for i, v in enumerate(suite_options)}
            idx_map["1"] = suite_options[0]
            suite_choice = get_validated_input("Choose suite (or 'b' to cancel):", [str(i+1) for i in range(len(suite_options))] + ["b"])
            if suite_choice != "b":
                suite_val = suite_options[int(suite_choice)-1]
                if suite_val == "Custom":
                    suite_val = get_validated_input("Enter custom suite:", allow_empty=False)
                software_settings["suite"] = suite_val
                print_success(f"Suite set to {suite_val}")
        elif choice == "2":
            for idx, val in enumerate(renderer_options, 1):
                print_option(str(idx), val)
            idx_map = {str(i+1): v for i, v in enumerate(renderer_options)}
            idx_map["1"] = renderer_options[0]
            renderer_choice = get_validated_input("Choose renderer (or 'b' to cancel):", [str(i+1) for i in range(len(renderer_options))] + ["b"])
            if renderer_choice != "b":
                renderer_val = renderer_options[int(renderer_choice)-1]
                if renderer_val == "Custom":
                    renderer_val = get_validated_input("Enter custom renderer:", allow_empty=False)
                software_settings["renderer"] = renderer_val
                print_success(f"Renderer set to {renderer_val}")
        elif choice == "3":
            version_val = get_validated_input("Enter version string (e.g. '3.6', '2024', 'R25'):", allow_empty=True)
            software_settings["version"] = version_val if version_val else None
            print_success(f"Version set to {version_val if version_val else '[Not Set]'}")
        elif choice == "c":
            software_settings["suite"] = None
            software_settings["renderer"] = None
            software_settings["version"] = None
            print_success("Software settings cleared.")
        elif choice == "b":
            break

        # Save updated settings after every change
        user_prefs.imagen_settings["software_settings"] = software_settings
        user_prefs.save_preferences()
