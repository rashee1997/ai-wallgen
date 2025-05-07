try:
    import clrprint
    from clrprint import clrprint as print_colored, clrinput
    CLRPRINT_AVAILABLE = True
except ImportError:
    CLRPRINT_AVAILABLE = False
    print("Note: For colored output in PowerShell, install clrprint with: pip install clrprint")

import os
import sys
import time
import threading
from typing import List, Optional

def print_header(text: str) -> None:
    """
    Print a formatted header with a border using clrprint.
    """
    width = 80
    try:
        width = min(80, os.get_terminal_size().columns)
    except (AttributeError, OSError):
        pass
    border = "=" * width
    print_colored(border, clr="cyan", end="\n")
    print_colored(f" {text.center(width - 2)} ", clr="cyan", end="\n")
    print_colored(border, clr="cyan", end="\n\n")

def print_section(text: str) -> None:
    """
    Print a formatted section title using clrprint.
    """
    print_colored(f"\n{text}", clr="green", end="\n")
    print_colored("-" * len(text), clr="green", end="\n")

def print_option(key: str, description: str) -> None:
    """
    Print a menu option with its key and description using clrprint.
    """
    print_colored(f"  {key}: ", clr="yellow", end="")
    print(description)

def print_success(text: str) -> None:
    """
    Print a success message using clrprint.
    """
    print_colored(f"✓ {text}", clr="green")

def print_error(text: str) -> None:
    """
    Print an error message using clrprint.
    """
    print_colored(f"✗ {text}", clr="red")

def print_warning(text: str) -> None:
    """
    Print a warning message using clrprint.
    """
    print_colored(f"⚠ {text}", clr="yellow")

def print_info(text: str) -> None:
    """
    Print an informational message using clrprint.
    """
    print_colored(f"  {text}", clr="blue")

def print_prompt(text: str) -> None:
    """
    Print a user prompt using clrprint.
    """
    print_colored(f"> {text}", clr="magenta", end=" ")

def get_interactive_input(prompt_text: str) -> str:
    """
    Get user input interactively using clrinput if available, else fallback to input().
    """
    if CLRPRINT_AVAILABLE:
        try:
            return clrinput(f"> {prompt_text} ").strip()
        except Exception:
            pass
    # Fallback
    print_prompt(prompt_text)
    return input().strip()

def get_validated_input(prompt: str, options: Optional[List[str]] = None,
                        default: Optional[str] = None, allow_empty: bool = False) -> str:
    """
    Get and validate user input against a set of allowed options, using interactive input.
    """
    while True:
        user_input = get_interactive_input(prompt)
        if not user_input:
            if default is not None:
                return default
            elif allow_empty:
                return ""
            else:
                print_warning("Input cannot be empty. Please try again.")
                continue
        if options is not None and user_input not in options:
            print_warning(f"Invalid input. Please enter one of: {', '.join(options)}")
            continue
        return user_input

def show_spinner(message: str, duration: float = 2) -> None:
    """
    Display a spinner animation for the specified duration.
    """
    def spin():
        spinner_chars = ['|', '/', '-', '\\']
        end_time = time.time() + duration
        i = 0
        try:
            while time.time() < end_time:
                sys.stdout.write(f"\r{spinner_chars[i]} {message}")
                sys.stdout.flush()
                time.sleep(0.1)
                i = (i + 1) % len(spinner_chars)
            sys.stdout.write(f"\r{' ' * (len(message) + 2)}\r")
            sys.stdout.flush()
        except:
            sys.stdout.write("\r\n")
            sys.stdout.flush()
    spinner_thread = threading.Thread(target=spin)
    spinner_thread.start()
    spinner_thread.join()

def print_breadcrumb(path_list: List[str]) -> None:
    """
    Print a breadcrumb trail to show navigation path.
    """
    if not path_list:
        return
    breadcrumb = " > ".join(path_list)
    print_colored(breadcrumb, clr="cyan")
    print()

def print_menu_options(options: List[tuple[str, str]]) -> None:
    """
    Print menu options given a list of (key, description) tuples.
    """
    for key, description in options:
        print_option(key, description)

def get_menu_choice(prompt: str, valid_choices: List[str], allow_empty: bool = False) -> str:
    """
    Get a validated menu choice from the user.
    """
    try:
        return get_validated_input(prompt, valid_choices, allow_empty=allow_empty)
    except KeyboardInterrupt:
        print("\nOperation interrupted.")
        return "_INTERRUPTED_"
    except EOFError:
        print("\nInput closed. Exiting menu.")
        return "_EOF_"

def show_ascii_art():
    """
    Display ASCII art header for the application.
    """
    print("\n" + "=" * 80)
    print(" " * 29 + "AI Wallpaper Generator" + " " * 29)
    print("=" * 80 + "\n")
    print_info("Welcome to the AI Wallpaper Generator! This tool helps you create stunning wallpapers using AI.")
