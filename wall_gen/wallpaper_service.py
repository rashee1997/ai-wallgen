# wall_gen/wallpaper_service.py
"""
Service module for OS-specific wallpaper setting and environment detection.
"""
import os
import platform
import subprocess
import shlex
import logging
import ctypes # For Windows
from urllib.parse import quote # For Linux file URIs

try:
    # Use absolute package import for ui_utils
    from wall_gen.ui_utils import print_info, print_warning
except ImportError:
    logging.warning("Import for ui_utils failed in wallpaper_service.py. Ensure wall_gen package structure is correct.")
    # Fallback if run standalone or structure not yet fully in place
    # This assumes wall_gen is in PYTHONPATH or is the CWD for this to work.
    # This assumes wall_gen is in PYTHONPATH or is the CWD for this to work.
    from wall_gen.ui_utils import print_info, print_warning


def detect_linux_desktop_env():
    """
    Detect the Linux desktop environment.
    (Moved from wallpaper_generator.py, renamed)
    """
    desktop_env_vars = [
        "XDG_CURRENT_DESKTOP", "GDMSESSION", "DESKTOP_SESSION", 
        "XDG_SESSION_DESKTOP", "SESSION_DESKTOP"
    ]
    for var in desktop_env_vars:
        desktop_env = os.environ.get(var, "")
        if desktop_env:
            desktop_env_upper = desktop_env.upper()
            if "GNOME" in desktop_env_upper: return "GNOME"
            if "KDE" in desktop_env_upper or "PLASMA" in desktop_env_upper: return "KDE"
            if "XFCE" in desktop_env_upper: return "XFCE"
            if "MATE" in desktop_env_upper: return "MATE"
            if "CINNAMON" in desktop_env_upper: return "CINNAMON"
            if "LXDE" in desktop_env_upper: return "LXDE"
            if "LXQT" in desktop_env_upper: return "LXQT"
            if "BUDGIE" in desktop_env_upper: return "BUDGIE"
            if "DEEPIN" in desktop_env_upper: return "DEEPIN"
            if "I3" in desktop_env_upper: return "I3"
            if "SWAY" in desktop_env_upper: return "SWAY"
            if desktop_env_upper in ["GNOME", "KDE", "XFCE", "MATE", "CINNAMON", "LXDE", "LXQT", "UNITY", "BUDGIE", "DEEPIN", "I3", "SWAY"]:
                 return desktop_env_upper

    try:
        output = subprocess.check_output(["ps", "-e"], text=True, stderr=subprocess.DEVNULL)
        if "gnome-session" in output or "gnome-shell" in output: return "GNOME"
        if "startkde" in output or "plasmashell" in output or "kwin" in output : return "KDE"
        if "xfce4-session" in output: return "XFCE"
        if "mate-session" in output: return "MATE"
        if "cinnamon-session" in output: return "CINNAMON"
        if "lxsession" in output: 
            if os.environ.get("LXQT_SESSION"): return "LXQT"
            return "LXDE"
        if "budgie-desktop" in output : return "BUDGIE"
        if "deepin-wm" in output or "dde-session" in output : return "DEEPIN"
        if "i3" in output and not "sway" in output: return "I3"
        if "sway" in output: return "SWAY"
    except (subprocess.SubprocessError, FileNotFoundError):
        logging.warning("Could not run 'ps -e' to detect Linux DE.")
        pass

    logging.info("Could not definitively detect Linux DE via common methods.")
    return "UNKNOWN"


def set_os_wallpaper(image_path):
    """
    Set the wallpaper using the appropriate method. (Moved from wallpaper_generator.py, renamed)
    Args:
        image_path (str): Absolute path to the image file.
    Returns:
        bool: True if wallpaper set successfully, False otherwise.
    """
    try:
        os_name = platform.system()

        if not os.path.isabs(image_path):
            absolute_path = os.path.abspath(image_path)
            logging.warning(f"Relative image path '{image_path}' provided. Converted to absolute: '{absolute_path}'.")
        else:
            absolute_path = image_path
        
        if not os.path.exists(absolute_path):
            logging.error(f"Wallpaper image not found at: {absolute_path}")
            return False

        if os_name == "Windows":
            SPI_SETDESKWALLPAPER = 0x0014
            SPIF_UPDATEINIFILE = 0x01
            SPIF_SENDWININICHANGE = 0x02
            result = ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER, 0, absolute_path, SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE
            )
            if result:
                logging.info("Wallpaper set successfully on Windows.")
                return True
            else:
                logging.error(f"SystemParametersInfoW failed on Windows. Error code: {ctypes.get_last_error()}")
                return False
        
        elif os_name == "Darwin": 
            script = f'tell application "System Events" to tell every desktop to set picture to "{absolute_path}"'
            command = ["osascript", "-e", script]
            subprocess.run(command, check=True, capture_output=True, text=True)
            logging.info("Wallpaper set successfully on macOS.")
            return True

        elif os_name == "Linux":
            file_uri = "file://" + quote(absolute_path) 

            desktop_env = detect_linux_desktop_env()
            # Use logging instead of print_info directly in this service for better decoupling
            logging.info(f"Detected Linux desktop environment: {desktop_env}")

            command = []
            if desktop_env in ["GNOME", "UNITY", "BUDGIE", "PANTHEON", "DEEPIN", "UBUNTU:GNOME", "UBUNTU"]:
                command = ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", file_uri]
                subprocess.run(command, check=True, capture_output=True, text=True)
                try:
                    command_dark = ["gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", file_uri]
                    subprocess.run(command_dark, check=True, capture_output=True, text=True)
                except subprocess.CalledProcessError:
                    logging.debug("Dark mode picture-uri-dark not supported for GNOME.")
                logging.info(f"Wallpaper set for {desktop_env} using gsettings (GNOME).")
                return True
            
            elif desktop_env == "CINNAMON":
                command = ["gsettings", "set", "org.cinnamon.desktop.background", "picture-uri", file_uri]
            
            elif desktop_env == "MATE":
                command = ["gsettings", "set", "org.mate.background", "picture-filename", absolute_path]

            elif desktop_env == "XFCE":
                try:
                    output = subprocess.check_output(["xfconf-query", "-c", "xfce4-desktop", "-l"], text=True)
                    monitors = [line for line in output.splitlines() if line.endswith("/last-image")]
                    if not monitors:
                         monitors = [prop for prop in output.splitlines() if "workspace0/last-image" in prop]

                    if monitors:
                        for monitor_prop_path in monitors:
                            subprocess.run(
                                ["xfconf-query", "-c", "xfce4-desktop", "-p", monitor_prop_path, "-s", absolute_path],
                                check=True, capture_output=True, text=True
                            )
                        logging.info("Wallpaper set successfully on XFCE.")
                        return True
                    else:
                        logging.warning("No XFCE monitor properties found. Trying fallback.")
                        if _try_linux_fallback_setters(absolute_path): return True
                        return False
                except (subprocess.SubprocessError, FileNotFoundError) as e:
                    logging.error(f"xfconf-query failed for XFCE: {e}. Trying fallback.")
                    if _try_linux_fallback_setters(absolute_path): return True
                    return False
            
            elif desktop_env in ["KDE", "PLASMA", "PLASMA5"]: 
                script_kde = f"""
                var allDesktops = desktops();
                for (var i = 0; i < allDesktops.length; i++) {{
                    var d = allDesktops[i];
                    d.wallpaperPlugin = 'org.kde.image';
                    d.currentConfigGroup = ['Wallpaper', 'org.kde.image', 'General'];
                    d.writeConfig('Image', 'file://{quote(absolute_path)}');
                }}
                """
                command = ["qdbus", "org.kde.plasmashell", "/PlasmaShell", "org.kde.PlasmaShell.evaluateScript", script_kde]
            
            elif desktop_env in ["I3", "SWAY", "OPENBOX", "AWESOME", "BSPWM", "HERBSTLUFTWM"]: 
                logging.info(f"Attempting to set wallpaper for WM: {desktop_env} using fallbacks.")
                if _try_linux_fallback_setters(absolute_path): return True
                logging.warning(f"Could not set wallpaper for {desktop_env} using feh or nitrogen.")
                return False

            else: 
                logging.info(f"Unknown Linux DE '{desktop_env}'. Attempting common fallback methods.")
                if _try_linux_fallback_setters(absolute_path): return True
                logging.warning("Could not set wallpaper with any known Linux method.")
                return False

            if command: 
                subprocess.run(command, check=True, capture_output=True, text=True)
                logging.info(f"Wallpaper set successfully on Linux ({desktop_env}).")
                return True

        else: 
            logging.warning(f"Unsupported OS for wallpaper setting: {os_name}")
            return False

    except subprocess.CalledProcessError as e:
        logging.error(f"Error setting wallpaper (command failed): {e.cmd}")
        logging.error(f"Stderr: {e.stderr.strip() if e.stderr else 'N/A'}")
        return False
    except FileNotFoundError as e:
        logging.error(f"Error setting wallpaper (command not found): {e.filename}")
        # Using logging.warning for user-facing advice, print_warning would be better if ui_utils is guaranteed
        logging.warning(f"A required command ({e.filename}) was not found. Please ensure it's installed and in your PATH.")
        return False
    except Exception as e:
        logging.error(f"Unexpected error setting wallpaper: {e}", exc_info=True)
        return False
    
    return False

def _try_linux_fallback_setters(absolute_path):
    """Tries common Linux wallpaper setters like feh and nitrogen."""
    try:
        subprocess.run(["feh", "--bg-fill", absolute_path], check=True, capture_output=True, text=True)
        logging.info("Wallpaper set using feh.")
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        logging.debug("feh command failed or not found.")

    try:
        subprocess.run(["nitrogen", "--set-zoom-fill", "--save", absolute_path], check=True, capture_output=True, text=True)
        logging.info("Wallpaper set using nitrogen.")
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        logging.debug("nitrogen command failed or not found.")
        
    try:
        file_uri = "file://" + quote(absolute_path)
        command = ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", file_uri]
        subprocess.run(command, check=True, capture_output=True, text=True)
        logging.info("Wallpaper set using gsettings (GNOME fallback).")
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        logging.debug("gsettings (GNOME fallback) failed or not found.")

    return False

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # Mock print_info and print_warning if ui_utils is not available for direct testing
    # For this example, we'll assume logging.info/warning is sufficient for test output.

    test_image_path = "test_wallpaper.png" 
    if not os.path.exists(test_image_path):
        try:
            from PIL import Image, ImageDraw
            img = Image.new('RGB', (100, 100), color = 'blue') # Smaller dummy image
            draw = ImageDraw.Draw(img)
            draw.text((10,10), "Test", fill=(255,255,0))
            img.save(test_image_path)
            logging.info(f"Created dummy image: {test_image_path}")
        except ImportError:
            logging.error("Pillow not installed, cannot create dummy image for testing wallpaper_service.")
    
    if os.path.exists(test_image_path):
        abs_test_image_path = os.path.abspath(test_image_path)
        logging.info(f"Attempting to set wallpaper to: {abs_test_image_path}")
        success = set_os_wallpaper(abs_test_image_path)
        if success:
            logging.info("Test: Wallpaper set_os_wallpaper call reported success.")
        else:
            logging.error("Test: Wallpaper set_os_wallpaper call reported failure.")
        # Consider cleaning up: os.remove(test_image_path) 
    else:
        logging.error(f"Test image {test_image_path} not found. Skipping wallpaper set test.")

    if platform.system() == "Linux":
        detected_de = detect_linux_desktop_env()
        logging.info(f"Test: Detected Linux DE: {detected_de}")
