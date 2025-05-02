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
import platform  # Added for OS detection
from typing import List, Optional, Any, Dict, Union, Callable

# Imports for interactive input
if platform.system() != "Windows":
    try:
        import tty
        import termios
        UNIX_INTERACTIVE_INPUT = True
    except ImportError:
        UNIX_INTERACTIVE_INPUT = False
else:
    # Potentially add msvcrt for Windows later if needed
    UNIX_INTERACTIVE_INPUT = False

# Third-party imports (with fallback handling)
try:
    import colorama
    from colorama import Fore, Style, Back
    # Initialize colorama for cross-platform colored terminal output
    # Use specific parameters for better PowerShell support
    colorama.init(convert=False, strip=False)
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
    # This function is now less relevant as the prompt is printed within get_interactive_input
    # Keeping it for potential other uses or direct calls.
    print_colored(f"> {text}", Fore.MAGENTA, Style.BRIGHT, end=" ")

# Helper for Unix interactive input
def _read_char_unix() -> str:
    """Reads a single character from stdin on Unix systems."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        # Handle multi-byte sequences for arrow keys etc.
        if ch == '\x1b':  # Escape character
            next1 = sys.stdin.read(1)
            if next1 == '[':
                next2 = sys.stdin.read(1)
                if next2 == 'D': return "ARROW_LEFT"
                if next2 == 'C': return "ARROW_RIGHT"
                # Add other arrow keys or special keys if needed (e.g., 'A' for UP, 'B' for DOWN)
                # For now, just return the sequence if not left/right
                return ch + next1 + next2
            # Return other escape sequences as is
            return ch + next1
        elif ch == '\x7f' or ch == '\b': # Backspace (check common codes)
             return "BACKSPACE"
        elif ch == '\r' or ch == '\n': # Enter key
             return "ENTER"
        elif ch == '\x03': # Ctrl+C
             raise KeyboardInterrupt
        # Add other special key handling here if needed
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch # Return regular character

def _calculate_physical_pos(logical_pos: int, prompt_len: int, terminal_width: int) -> tuple[int, int]:
    """
    Calculates the physical (row, col) on screen for a logical cursor position
    relative to the start of the prompt line. Assumes prompt doesn't wrap.
    """
    # Treat prompt and buffer as one continuous string for wrapping calculation
    # Add prompt_len to logical_pos to get position relative to start of the line
    effective_pos = prompt_len + logical_pos
    # Calculate 0-based row relative to the prompt line
    row = effective_pos // terminal_width
    # Calculate 0-based column
    col = effective_pos % terminal_width
    return row, col

def get_interactive_input(prompt_text: str) -> str:
    """Gets user input interactively, allowing cursor movement and backspace."""
    if not UNIX_INTERACTIVE_INPUT or not sys.stdin.isatty():
        # Fallback to standard input if not a TTY or not Unix
        return input().strip()

    try:
        # Get terminal width, default if error
        try:
            terminal_width = os.get_terminal_size().columns
        except (AttributeError, OSError):
            terminal_width = 80 # Default width

        # Print the prompt only once at the beginning
        prompt_display = f"> {prompt_text} "
        print_colored(prompt_display, Fore.MAGENTA, Style.BRIGHT, end="")
        sys.stdout.flush()
        prompt_len = len(prompt_display) # Store length for cursor calculations

        buffer = []
        cursor_pos = 0 # Logical cursor position within buffer

        # Calculate initial physical position (start of input area)
        start_row, start_col = _calculate_physical_pos(-1, prompt_len, terminal_width) # Position before first char

        while True:
            # Calculate current physical position before reading next char
            current_row, current_col = _calculate_physical_pos(cursor_pos, prompt_len, terminal_width)

            char = _read_char_unix()

            if char == "ENTER":
                # Move cursor to the end of the buffer physically before printing newline
                end_row, end_col = _calculate_physical_pos(len(buffer), prompt_len, terminal_width)
                row_diff = end_row - current_row
                if row_diff > 0:
                    sys.stdout.write(f'\033[{row_diff}B') # Move down
                sys.stdout.write('\r') # Go to start of line
                sys.stdout.write(f'\033[{end_col}C') # Move to final column
                print() # Newline
                sys.stdout.flush()
                break

            elif char == "BACKSPACE" or char == "ARROW_LEFT" or char == "ARROW_RIGHT" or (isinstance(char, str) and not char.startswith('\x1b') and char.isprintable()):
                # --- Common Redraw/Movement Logic ---
                old_buffer_len = len(buffer)
                old_cursor_pos = cursor_pos

                # 1. Update buffer and logical cursor position
                if char == "BACKSPACE":
                    if cursor_pos > 0:
                        buffer.pop(cursor_pos - 1)
                        cursor_pos -= 1
                    else: continue # No change
                elif char == "ARROW_LEFT":
                    if cursor_pos > 0:
                        cursor_pos -= 1
                    else: continue # No change
                elif char == "ARROW_RIGHT":
                    if cursor_pos < len(buffer):
                        cursor_pos += 1
                    else: continue # No change
                else: # Printable character
                    buffer.insert(cursor_pos, char)
                    cursor_pos += 1

                # 2. Calculate physical positions
                # Position of the start of the input area (relative to prompt line)
                input_start_row, input_start_col = _calculate_physical_pos(0, prompt_len, terminal_width)
                # Target physical position for the cursor after the edit
                target_row, target_col = _calculate_physical_pos(cursor_pos, prompt_len, terminal_width)
                # Physical position at the end of the *old* buffer content
                old_end_row, old_end_col = _calculate_physical_pos(old_buffer_len, prompt_len, terminal_width)

                # 3. Move cursor from current physical position back to the start of the input area
                row_diff = current_row - input_start_row
                if row_diff > 0:
                    sys.stdout.write(f'\033[{row_diff}A') # Move cursor up
                sys.stdout.write('\r') # Go to beginning of line
                sys.stdout.write(f'\033[{input_start_col}C') # Move cursor to input start column

                # 4. Clear screen from cursor down and rewrite prompt + buffer
                sys.stdout.write('\033[J') # Clear Down
                # No need to reprint prompt as we started cursor after it
                sys.stdout.write("".join(buffer))
                sys.stdout.flush()

                # 5. Calculate physical position at the end of the *new* buffer content
                new_end_row, new_end_col = _calculate_physical_pos(len(buffer), prompt_len, terminal_width)

                # 6. Move cursor from current position (end of new buffer) to target physical position
                # Calculate relative moves needed
                row_diff_final = new_end_row - target_row
                col_diff_final = new_end_col - target_col # Not directly used, move line by line

                if row_diff_final > 0:
                    sys.stdout.write(f'\033[{row_diff_final}A') # Move cursor up
                sys.stdout.write('\r') # Go to beginning of target line
                sys.stdout.write(f'\033[{target_col}C') # Move cursor to target column
                sys.stdout.flush()

            # Ignore other non-printable characters or unhandled sequences for now

    except Exception as e:
        # Attempt to restore terminal settings on error
        # This might require saving/restoring original termios settings if needed
        print_error(f"Input error: {e}")
        # Fallback or re-raise depending on desired behavior
        return "".join(buffer) # Return whatever was buffered

    # Note: Original termios settings should ideally be restored here in a finally block
    # if tty.setraw was used directly or if more settings were changed.
    # The _read_char_unix function handles restoring settings after each char read.
    return "".join(buffer)


def get_validated_input(prompt: str, options: Optional[List[str]] = None,
                        default: Optional[str] = None, allow_empty: bool = False) -> str:
    """
    Get and validate user input against a set of allowed options, using interactive input.
    
    This function prompts the user for input using an interactive line editor
    (if supported) and validates it against a list of allowed options.
    It will continue prompting until valid input is received.
    
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
        > Select option [cursor here]
        # Returns validated input
    """
    while True:
        # Use the new interactive input function
        # Note: print_prompt is now called inside get_interactive_input
        # Note: print_prompt is called inside get_interactive_input
        user_input = get_interactive_input(prompt) # Let KeyboardInterrupt propagate

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

def print_menu_options(options: List[tuple[str, str]]) -> None:
    """
    Print menu options given a list of (key, description) tuples.

    Args:
        options: List of tuples where each tuple is (key, description)
    """
    for key, description in options:
        print_option(key, description)

def get_menu_choice(prompt: str, valid_choices: List[str], allow_empty: bool = False) -> str:
    """
    Get a validated menu choice from the user.

    Args:
        prompt: The prompt to display to the user
        valid_choices: List of valid input choices
        allow_empty: Whether to allow empty input (default False)

    Returns:
        The user's validated choice as a string
        
    Note:
        Returns "_INTERRUPTED_" if KeyboardInterrupt is caught, allowing
        for graceful exit handling by the caller.
    """
    try:
        return get_validated_input(prompt, valid_choices, allow_empty=allow_empty)
    except KeyboardInterrupt:
        print("\nOperation interrupted.")
        return "_INTERRUPTED_"

def show_ascii_art():
    """Display ASCII art header for the application."""
    print("\n" + "=" * 80)
    print(" " * 29 + "AI Wallpaper Generator" + " " * 29)
    print("=" * 80 + "\n")
    print_info("Welcome to the AI Wallpaper Generator! This tool helps you create stunning wallpapers using AI.")
