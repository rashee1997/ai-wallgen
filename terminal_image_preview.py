#!/usr/bin/env python3
"""
Terminal Image Preview for Wallpaper Generator.

This module provides functions to preview images in the terminal
before setting them as wallpaper.
"""

import os
import subprocess
import platform
import logging
from typing import Optional

# Check if Pillow is available for image processing
try:
    from PIL import Image
    PILLOW_AVAILABLE = True
    
    # Handle different Pillow versions (LANCZOS vs ANTIALIAS)
    try:
        # For Pillow >= 9.1.0
        RESIZE_FILTER = Image.LANCZOS
    except AttributeError:
        try:
            # For Pillow < 9.1.0, which uses ANTIALIAS
            RESIZE_FILTER = Image.ANTIALIAS
        except AttributeError:
            # Fallback to BICUBIC if neither is available
            RESIZE_FILTER = Image.BICUBIC
except ImportError:
    PILLOW_AVAILABLE = False

# Import UI utilities
from ui_utils import (
    print_colored, print_info, print_warning, print_error, 
    print_success, get_validated_input
)

# Import tkinter preview (with fallback)
try:
    from tkinter_preview import preview_image_gui
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

def detect_terminal_support():
    """
    Detect if the terminal supports image display.
    
    Returns:
        tuple: (bool, str) - Whether image display is supported and the method to use
    """
    # Check for common terminal emulators that support inline images
    terminal = os.environ.get("TERM_PROGRAM", "")
    term_type = os.environ.get("TERM", "")
    
    # Check for iTerm2
    if terminal == "iTerm.app":
        return True, "iterm2"
    
    # Check for Kitty
    if terminal == "kitty" or "KITTY_WINDOW_ID" in os.environ:
        return True, "kitty"
    
    # Check for sixel support
    if "sixel" in term_type:
        return True, "sixel"
    
    # Check for terminals that might support Sixel 
    if term_type in ["xterm-256color", "vt340", "ms-terminal"]:
        try:
            result = subprocess.run(
                ["tput", "Co"], 
                capture_output=True, 
                text=True, 
                check=False
            )
            if "256" in result.stdout:
                return True, "sixel"
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
    
    # Default to ASCII art if no graphical method is available
    return True, "ascii"

def preview_image_ascii(image_path: str) -> bool:
    """
    Display an image as ASCII art in the terminal.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        bool: True if preview was successful, False otherwise
    """
    if not PILLOW_AVAILABLE:
        print_warning("Pillow library is required for ASCII art preview.")
        return False
    
    try:
        # Open image
        with Image.open(image_path) as img:
            # Get terminal dimensions
            try:
                term_width = os.get_terminal_size().columns
                term_height = os.get_terminal_size().lines - 10  # Reserve lines for UI
            except (AttributeError, OSError):
                term_width, term_height = 80, 24
            
            # Calculate target dimensions for ASCII art
            # Characters in terminal are taller than they are wide, 
            # so we need to compensate for that
            orig_width, orig_height = img.size
            aspect_ratio = orig_width / orig_height
            
            # Limit width to terminal width or 100 characters
            target_width = min(term_width - 4, 100)
            
            # Calculate height based on aspect ratio (with character height adjustment)
            # Most terminal fonts are roughly 2x taller than wide
            char_adjust = 0.5  # Character width/height adjustment factor
            target_height = int(target_width / aspect_ratio * char_adjust)
            
            # Ensure height doesn't exceed terminal height
            target_height = min(target_height, term_height)
            
            # Ensure minimum dimensions
            target_width = max(10, target_width)
            target_height = max(5, target_height)
            
            # Resize image for ASCII conversion
            img = img.resize((target_width, target_height), RESIZE_FILTER)
            
            # Convert to grayscale
            img = img.convert("L")
            
            # Define ASCII character set from dark to light
            # ascii_chars = '@%#*+=-:. '  # Original set
            ascii_chars = '@%#*+=-:. '  # Alternate set
            
            # Generate ASCII art
            pixels = list(img.getdata())
            ascii_art = []
            
            for i in range(target_height):
                line = ''
                for j in range(target_width):
                    # Get pixel value (0-255) and map to ASCII character
                    pixel_idx = i * target_width + j
                    if pixel_idx < len(pixels):  # Safety check
                        pixel_val = pixels[pixel_idx]
                        # Map pixel value to character index
                        char_idx = min(int(pixel_val * len(ascii_chars) / 256), len(ascii_chars) - 1)
                        line += ascii_chars[char_idx]
                ascii_art.append(line)
            
            # Print ASCII art
            print_info(f"ASCII Preview of {os.path.basename(image_path)}:")
            for line in ascii_art:
                print(line)
            
            return True
            
    except Exception as e:
        print_error(f"Error generating ASCII preview: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def preview_image_kitty(image_path: str) -> bool:
    """
    Display an image in the Kitty terminal.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        bool: True if preview was successful, False otherwise
    """
    try:
        # Get terminal size
        try:
            term_width = os.get_terminal_size().columns
            term_height = os.get_terminal_size().lines - 5
        except (AttributeError, OSError):
            term_width, term_height = 80, 24
        
        # Construct the kitty graphics protocol command
        cmd = ["kitty", "+kitten", "icat", "--align", "center", 
               "--scale-up", "--place", f"{term_width}x{term_height}@0x0", 
               image_path]
        
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        print_error(f"Error displaying image with kitty: {e}")
        return False

def preview_image_iterm2(image_path: str) -> bool:
    """
    Display an image in the iTerm2 terminal.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        bool: True if preview was successful, False otherwise
    """
    try:
        # Get file size
        file_size = os.path.getsize(image_path)
        
        # Read the image file
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        # Get terminal size for scaling
        try:
            term_width = os.get_terminal_size().columns
            term_height = os.get_terminal_size().lines - 5
        except (AttributeError, OSError):
            term_width, term_height = 80, 24
        
        # Base64 encode the image data
        import base64
        b64_data = base64.b64encode(image_data).decode("ascii")
        
        # iTerm2 escape sequence for inline images
        # Format: ESC]1337;File=name=NAME;size=SIZE;inline=1:BASE64_DATA^G
        print(f"\033]1337;File=name={os.path.basename(image_path)};size={file_size};width={term_width};height={term_height};inline=1:{b64_data}\007")
        return True
    except Exception as e:
        print_error(f"Error displaying image with iTerm2: {e}")
        return False

def preview_image_sixel(image_path: str) -> bool:
    """
    Display an image using Sixel graphics.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        bool: True if preview was successful, False otherwise
    """
    try:
        # Check for img2sixel
        cmd = ["img2sixel", image_path]
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        try:
            # Try with convert (ImageMagick) if img2sixel is not available
            cmd = ["convert", image_path, "sixel:-"]
            result = subprocess.run(cmd, check=True)
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            print_error(f"Error displaying image with Sixel: {e}")
            return False

def preview_image_external(image_path: str) -> bool:
    """
    Display an image using an external viewer based on the operating system.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        bool: True if preview was successful, False otherwise
    """
    os_name = platform.system()
    
    try:
        if os_name == "Windows":
            os.startfile(image_path)
            return True
        elif os_name == "Darwin":  # macOS
            subprocess.run(["open", image_path], check=True)
            return True
        elif os_name == "Linux":
            # Try different viewers in order
            viewers = ["display", "feh", "eog", "xdg-open"]
            for viewer in viewers:
                try:
                    subprocess.run([viewer, image_path], check=True)
                    return True
                except (subprocess.SubprocessError, FileNotFoundError):
                    continue
            
            print_warning("No suitable image viewer found.")
            return False
        else:
            print_warning(f"Unsupported operating system: {os_name}")
            return False
    except Exception as e:
        print_error(f"Error displaying image with external viewer: {e}")
        return False

def preview_image(image_path: str, method: Optional[str] = None) -> bool:
    """
    Display an image in the terminal or external viewer.
    
    Args:
        image_path (str): Path to the image file
        method (Optional[str]): Force a specific display method
        
    Returns:
        bool: True if preview was successful, False otherwise
    """
    # Check if file exists
    if not os.path.isfile(image_path):
        print_error(f"Image file not found: {image_path}")
        return False
    
    # If method is not specified, detect terminal support
    if method is None:
        supported, method = detect_terminal_support()
    
    # Display image using the appropriate method
    if method == "gui" or method == "tkinter":
        success = preview_image_gui(image_path)
    elif method == "kitty":
        success = preview_image_kitty(image_path)
    elif method == "iterm2":
        success = preview_image_iterm2(image_path)
    elif method == "sixel":
        success = preview_image_sixel(image_path)
    elif method == "ascii":
        success = preview_image_ascii(image_path)
    else:
        # Fallback to external viewer
        success = preview_image_external(image_path)
    
    return success

def terminal_preview_menu(image_path: str) -> bool:
    """
    Display a menu to preview an image and confirm setting it as wallpaper.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        bool: True if user wants to set as wallpaper, False otherwise
    """
    # Check if file exists
    if not os.path.isfile(image_path):
        print_error(f"Image file not found: {image_path}")
        return False
    
    # Use GUI preview by default if available
    if TKINTER_AVAILABLE:
        # Try to use the GUI preview first
        try:
            from wallpaper_generator import set_wallpaper as set_wp_func
            return preview_image_gui(image_path, set_wp_func)
        except Exception as e:
            print_warning(f"GUI preview failed, falling back to terminal: {e}")
    
    # Detect terminal capabilities (as fallback or if GUI not available)
    supported, default_method = detect_terminal_support()
    
    # Preview with default method
    print_info(f"Previewing image: {os.path.basename(image_path)}")
    preview_image(image_path, default_method)
    
    # Show preview menu
    while True:
        print_info("\nPreview options:")
        print("1: Preview with ASCII art")
        print("2: Preview with external viewer")
        if TKINTER_AVAILABLE:
            print("3: Preview with graphical window")
            print("4: Set as wallpaper")
            print("5: Cancel (don't set as wallpaper)")
            valid_options = ["1", "2", "3", "4", "5"]
        else:
            print("3: Set as wallpaper")
            print("4: Cancel (don't set as wallpaper)")
            valid_options = ["1", "2", "3", "4"]
        
        choice = get_validated_input("Select an option", valid_options)
        
        if choice == "1":
            preview_image(image_path, "ascii")
        elif choice == "2":
            preview_image(image_path, "external")
        elif TKINTER_AVAILABLE and choice == "3":
            try:
                from wallpaper_generator import set_wallpaper as set_wp_func
                result = preview_image_gui(image_path, set_wp_func)
                if result:
                    # User already set the wallpaper from the GUI
                    return True
            except Exception as e:
                print_error(f"Error with GUI preview: {e}")
        elif (TKINTER_AVAILABLE and choice == "4") or (not TKINTER_AVAILABLE and choice == "3"):
            print_success("Setting as wallpaper...")
            return True
        elif (TKINTER_AVAILABLE and choice == "5") or (not TKINTER_AVAILABLE and choice == "4"):
            print_info("Cancelled. Wallpaper not set.")
            return False
    
    return False

if __name__ == "__main__":
    # Simple test if this file is run directly
    import sys
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        result = terminal_preview_menu(image_path)
        print(f"Set as wallpaper: {result}")
    else:
        print("Usage: python terminal_image_preview.py [image_path]") 