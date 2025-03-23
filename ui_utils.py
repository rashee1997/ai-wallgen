#!/usr/bin/env python3
"""
UI utility functions for the AI Wallpaper Generator.

This module provides a consistent set of utilities for terminal output formatting
and user interaction, ensuring a uniform user experience throughout the application.

Features:
- Text formatting with colors and styles
- Structured output for headers, sections, and options
- User input validation and prompting
- Progress indicators and spinners
- Graceful fallbacks when terminal features are unavailable

The module uses colorama for cross-platform colored terminal output when available,
but provides appropriate fallbacks when it's not installed.
"""

# Standard library imports
import os
import sys
import time
import threading
from typing import List, Optional, Any, Dict, Union, Callable

# Third-party imports (with fallback handling)
try:
    import colorama
    from colorama import Fore, Style, Back
    # Initialize colorama for cross-platform colored terminal output
    colorama.init()
    COLORAMA_AVAILABLE = True
except ImportError:
    # Create dummy classes for Fore, Style, and Back if colorama is not available
    class DummyColorClass:
        """
        Dummy class that returns empty strings for any attribute.
        
        This class is used as a fallback when colorama is not available,
        ensuring that color/style formatting codes will be empty strings
        and thus have no effect on the output.
        """
        def __getattr__(self, name: str) -> str:
            """Return an empty string for any attribute."""
            return ""
    
    Fore = DummyColorClass()
    Style = DummyColorClass()
    Back = DummyColorClass()
    COLORAMA_AVAILABLE = False
    print("Note: For colored output, install colorama with: pip install colorama")

# UI utility functions
def print_colored(text: str, color: str = Fore.WHITE, style: str = Style.NORMAL, end: str = "\n") -> None:
    """
    Print text with the specified color and style.
    
    Args:
        text (str): The text to print
        color (str, optional): The color to use, from colorama.Fore. Defaults to Fore.WHITE.
        style (str, optional): The style to use, from colorama.Style. Defaults to Style.NORMAL.
        end (str, optional): String appended after the last value. Defaults to "\\n".
    
    Example:
        >>> print_colored("Hello, World!", Fore.GREEN, Style.BRIGHT)
    """
    print(f"{style}{color}{text}{Style.RESET_ALL}", end=end)

def print_header(text: str) -> None:
    """
    Print a formatted header with a border.
    
    This function creates a visually distinct header by surrounding the text with
    a border of equal signs. The header is centered within the border, and the
    width is adjusted to the terminal size when possible.
    
    Args:
        text (str): The header text to display
    
    Example:
        >>> print_header("Main Menu")
        ======================
         Main Menu
        ======================
    """
    try:
        width = min(80, os.get_terminal_size().columns)
    except (AttributeError, OSError):
        # Default width if terminal size cannot be determined
        width = 80
    
    print_colored("\n" + "=" * width, Fore.CYAN, Style.BRIGHT)
    print_colored(f" {text.center(width - 2)} ", Fore.CYAN, Style.BRIGHT)
    print_colored("=" * width + "\n", Fore.CYAN, Style.BRIGHT)

def print_section(text: str) -> None:
    """
    Print a formatted section title.
    
    This function creates a visually distinct section title by displaying the text
    in a different color and style than normal text, helping to organize content.
    
    Args:
        text (str): The section title to display
    
    Example:
        >>> print_section("User Preferences")
        User Preferences
        --------------
    """
    print_colored(f"\n{text}", Fore.GREEN, Style.BRIGHT)
    print_colored("-" * len(text), Fore.GREEN, Style.BRIGHT)

def print_option(key: str, description: str) -> None:
    """
    Print a menu option with its key and description.
    
    This function formats a menu option by displaying the key in a highlighted
    style followed by its description. This creates a consistent look for menu
    options throughout the application.
    
    Args:
        key (str): The key or number used to select this option
        description (str): The description of what this option does
    
    Example:
        >>> print_option("1", "Generate a new wallpaper")
        1: Generate a new wallpaper
    """
    print_colored(f"  {key}: ", Fore.YELLOW, Style.BRIGHT, end="")
    print(description)

def print_success(text: str) -> None:
    """
    Print a success message.
    
    This function displays a success message with a visual indicator (checkmark)
    and appropriate coloring to indicate a successful operation.
    
    Args:
        text (str): The success message to display
    
    Example:
        >>> print_success("Wallpaper generated successfully")
        ✓ Wallpaper generated successfully
    """
    print_colored(f"✓ {text}", Fore.GREEN, Style.BRIGHT)

def print_error(text: str) -> None:
    """
    Print an error message.
    
    This function displays an error message with a visual indicator (cross mark)
    and appropriate coloring to indicate an error condition.
    
    Args:
        text (str): The error message to display
    
    Example:
        >>> print_error("Failed to load preferences file")
        ✗ Failed to load preferences file
    """
    print_colored(f"✗ {text}", Fore.RED, Style.BRIGHT)

def print_warning(text: str) -> None:
    """
    Print a warning message.
    
    This function displays a warning message with a visual indicator (warning symbol)
    and appropriate coloring to indicate a warning condition that requires attention.
    
    Args:
        text (str): The warning message to display
    
    Example:
        >>> print_warning("Low disk space available")
        ⚠ Low disk space available
    """
    print_colored(f"⚠ {text}", Fore.YELLOW, Style.BRIGHT)

def print_info(text: str) -> None:
    """
    Print an informational message.
    
    This function displays an informational message with appropriate coloring
    to distinguish it from regular output, without indicating success or error.
    
    Args:
        text (str): The informational message to display
    
    Example:
        >>> print_info("Current resolution is 1920x1080")
        Current resolution is 1920x1080
    """
    print_colored(f"  {text}", Fore.BLUE)

def print_prompt(text: str) -> None:
    """
    Print a user prompt.
    
    This function displays a prompt message with a visual indicator (>) and
    appropriate coloring to indicate that user input is expected.
    
    Args:
        text (str): The prompt message to display
    
    Example:
        >>> print_prompt("Enter your name")
        > Enter your name
    """
    print_colored(f"> {text}", Fore.MAGENTA, Style.BRIGHT, end=" ")

def get_validated_input(prompt: str, options: Optional[List[str]] = None, 
                        default: Optional[str] = None, allow_empty: bool = False) -> str:
    """
    Get and validate user input against a set of allowed options.
    
    This function prompts the user for input and validates it against a list of
    allowed options. It will continue prompting until valid input is received.
    
    Args:
        prompt (str): The prompt to display to the user
        options (Optional[List[str]], optional): List of allowed input values.
                                              If None, any input is accepted.
                                              Defaults to None.
        default (Optional[str], optional): Default value to use if the user provides
                                         empty input. Defaults to None.
        allow_empty (bool, optional): Whether to allow empty input. If False and
                                     default is None, empty input will be rejected.
                                     Defaults to False.
    
    Returns:
        str: The validated user input
    
    Example:
        >>> choice = get_validated_input("Select option", ["1", "2", "3", "q"])
        > Select option 1
        # Returns "1"
    """
    while True:
        print_prompt(prompt)
        user_input = input().strip()
        
        # Handle empty input
        if not user_input:
            if default is not None:
                return default
            elif allow_empty:
                return ""
            else:
                print_warning("Input cannot be empty. Please try again.")
                continue
        
        # Validate against options if provided
        if options is not None and user_input not in options:
            print_warning(f"Invalid input. Please enter one of: {', '.join(options)}")
            continue
        
        return user_input

def show_spinner(message: str, duration: float = 2) -> None:
    """
    Display a spinner animation for the specified duration.
    
    This function shows a spinning animation alongside a message to indicate
    that an operation is in progress. The animation runs for the specified
    duration in seconds.
    
    Args:
        message (str): The message to display alongside the spinner
        duration (float, optional): Duration in seconds to show the spinner.
                                  Defaults to 2.
    
    Example:
        >>> show_spinner("Generating wallpaper...", 3.5)
        # Shows a spinning animation for 3.5 seconds
    """
    def spin():
        """Internal function that runs the spinner animation."""
        spinner_chars = ['|', '/', '-', '\\']
        end_time = time.time() + duration
        i = 0
        
        try:
            while time.time() < end_time:
                sys.stdout.write(f"\r{spinner_chars[i]} {message}")
                sys.stdout.flush()
                time.sleep(0.1)
                i = (i + 1) % len(spinner_chars)
            
            # Clear the spinner line when done
            sys.stdout.write(f"\r{' ' * (len(message) + 2)}\r")
            sys.stdout.flush()
        except:
            # Ensure we don't leave the line hanging if interrupted
            sys.stdout.write("\r\n")
            sys.stdout.flush()
    
    # Run spinner in a separate thread to avoid blocking
    spinner_thread = threading.Thread(target=spin)
    spinner_thread.start()
    spinner_thread.join()

def print_breadcrumb(path_list: List[str]) -> None:
    """
    Print a breadcrumb trail to show navigation path.
    
    This function displays a visual representation of the user's current location
    in a menu hierarchy, with each level separated by a delimiter.
    
    Args:
        path_list (List[str]): List of path components, from highest to lowest level
    
    Example:
        >>> print_breadcrumb(["Main Menu", "Settings", "Display"])
        Main Menu > Settings > Display
    """
    if not path_list:
        return
    
    breadcrumb = " > ".join(path_list)
    print_colored(breadcrumb, Fore.CYAN)
    print()  # Extra line for spacing 