# wall_gen/app_utils.py
"""
General application utilities including setup, logging, and cleanup.
NOTE: This module uses absolute imports assuming it's part of the 'wall_gen' package.
It may not run correctly as a standalone script without sys.path adjustments.
"""

import logging
import re
import html
import atexit
import sys # For check_dependencies to suggest pip install command
import os # Added for configure_app_logging path
import shutil # For getting terminal size
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

try:
    # Use absolute package import for ui_utils and file_utils 
    from wall_gen.ui_utils import print_warning, print_info
    from wall_gen.file_utils import _cleanup_all_temp_files # Changed to absolute import
except ImportError:
    # This block is reached if 'wall_gen' is not in sys.path or not installed.
    # Further imports from 'wall_gen' will also likely fail.
    # Logging a warning is appropriate. No functional fallback for these core utils.
    logging.critical("Core imports (ui_utils, file_utils) failed in app_utils.py. "
                     "Ensure 'wall_gen' package is correctly installed and in PYTHONPATH.")
    # Define dummy functions to prevent NameError if execution somehow continues,
    # though the application is unlikely to function correctly.
    def print_warning(msg): logging.warning(f"FALLBACK WARN: {msg}")
    def print_info(msg): logging.info(f"FALLBACK INFO: {msg}")
    def _cleanup_all_temp_files(): logging.warning("FALLBACK: _cleanup_all_temp_files called, but original not loaded.")


# --- Logging Configuration ---

def configure_app_logging(level=logging.INFO, log_filename="wallpaper_generator.log", project_root_dir="."):
    """
    Configure logging with file handler. Console output is handled by ui_utils.
    (Moved from configure_logging in wallpaper_generator.py)

    Args:
        level (int): Logging level (e.g., logging.INFO, logging.DEBUG).
        log_filename (str): Name of the log file.
        project_root_dir (str): Root directory to place the log file in.
    """
    log_file_path = os.path.join(project_root_dir, log_filename)
    
    # Basic config sets up the root logger.
    # Using basicConfig is simple but less flexible if other parts of the app also call it.
    # Consider using logger instances if more complex logging is needed later.
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - [%(name)s] - %(message)s",
        handlers=[logging.FileHandler(log_file_path, encoding='utf-8')] # Ensure UTF-8 encoding
    )
    
    # Optionally, add a StreamHandler for console output if ui_utils isn't used everywhere
    # console_handler = logging.StreamHandler(sys.stdout)
    # console_handler.setLevel(level)
    # console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    # logging.getLogger().addHandler(console_handler)

    logging.info(f"Logging configured. Level: {logging.getLevelName(level)}. Log file: {log_file_path}")


# --- Dependency Check ---

def check_system_dependencies():
    """
    Check if optional dependencies are installed and warn the user if not.
    (Moved from check_dependencies in wallpaper_generator.py)
    """
    missing_deps = []
    outdated_deps = []
    dependencies_to_check = {
        "PIL": "pillow", # Pillow is the package name for PIL
        "bleach": "bleach",
        # Add other optional dependencies here if needed
        # e.g., "PySide6": "PySide6" for Qt preview
    }

    # Special check for Google AI Python SDK
    try:
        import google.generativeai
        import importlib.metadata
        try:
            genai_version = importlib.metadata.version('google-generativeai')
            logging.info(f"Google AI Python SDK version: {genai_version}")
            
            # Check if this is the new SDK (after July 2024)
            if hasattr(google.generativeai, 'Client'):
                logging.info("Using the unified Google AI SDK (google-genai)")
            else:
                logging.debug("Using older Google AI SDK. Consider upgrading to the latest version.")
                outdated_deps.append("google-generativeai")
        except Exception as e:
            logging.warning(f"Could not determine Google AI SDK version: {e}")
    except ImportError:
        missing_deps.append("google-generativeai")
        logging.debug("Google AI SDK (google-generativeai) not found.")

    for module_name, package_name in dependencies_to_check.items():
        try:
            __import__(module_name)
            logging.debug(f"Dependency '{package_name}' found.")
        except ImportError:
            missing_deps.append(package_name)
            logging.debug(f"Optional dependency '{package_name}' not found.")

    if missing_deps:
        logging.debug("\nMissing dependencies:")
        for dep in missing_deps:
            logging.debug(f"  - {dep}")
        logging.debug("\nTo install missing dependencies, run:")
        pip_command = f"{sys.executable} -m pip install {' '.join(missing_deps)}"
        logging.debug(f"  {pip_command}")
        logging.debug("Some features may not work without these dependencies.\n")

    if outdated_deps:
        logging.debug("\nOutdated dependencies:")
        for dep in outdated_deps:
            logging.debug(f"  - {dep}")
        logging.debug("\nTo update dependencies, run:")
        pip_command = f"{sys.executable} -m pip install --upgrade {' '.join(outdated_deps)}"
        logging.debug(f"  {pip_command}")
        logging.debug("Some features may work differently with outdated dependencies.\n")


# --- Data Sanitization ---

def mask_sensitive_url_data(url: str) -> str:
    """
    Masks sensitive data (like API keys) in URLs before logging.
    (Moved from mask_sensitive_data_in_url in wallpaper_generator.py)
    """
    if not isinstance(url, str):
        return url # Return as is if not a string

    masked_url = html.unescape(url) # Decode HTML entities first
    
    # Mask common sensitive parameters
    sensitive_params = ["key", "api_key", "client_id", "token", "password", "secret"]
    for param in sensitive_params:
        # Regex to find param=value ensuring value doesn't contain '&'
        # Handles cases at end of URL or followed by '&'
        masked_url = re.sub(rf'({param}=)[^&]+', rf'\1<HIDDEN>', masked_url, flags=re.IGNORECASE)
        
    return masked_url


def sanitize_logging_content(content: str) -> str:
    """
    Sanitize content for logging by removing potentially sensitive data patterns.
    (Moved from sanitize_log_content in wallpaper_generator.py)
    """
    if not isinstance(content, str):
        return content
        
    # Example: Redact typical API key patterns (adjust regex as needed)
    # This is a basic example, more robust redaction might be needed
    sanitized = re.sub(r"api_key=[\w-]+", "api_key=REDACTED", content, flags=re.IGNORECASE)
    sanitized = re.sub(r"token=[\w.-]+", "token=REDACTED", sanitized, flags=re.IGNORECASE)
    # Add more redaction rules if necessary
    return sanitized


# --- Application Startup Message ---

def display_startup_message():
    """
    Display a rich welcome message using Panel and styled Text, centered.
    """
    console = Console() # Instantiate console

    text_content = Text(justify="center")
    # Using ✧ (White Four Pointed Star) icons
    text_content.append("✧ AI Wallpaper Generator ✧\n", style="bold magenta")
    text_content.append("-" * 30 + "\n", style="dim white") # Adjusted separator length
    text_content.append("Crafting unique visuals, just for you.", style="italic cyan")

    final_panel = Panel(
        text_content,
        title="[bold white]Welcome![/bold white]", # Rich markup in title
        border_style="bright_blue",
        expand=False, # Panel width fits content
        padding=(1, 2) # Padding inside the panel (vertical, horizontal)
    )
    console.print("\n", final_panel, justify="center")


# --- Cleanup Registration ---

_cleanup_registered = False

def initialize_temp_file_cleanup():
    """
    Registers the temporary file cleanup function to run at exit.
    Should be called once during application startup.
    (New function as per plan)
    """
    global _cleanup_registered
    if not _cleanup_registered:
        try:
            atexit.register(_cleanup_all_temp_files)
            _cleanup_registered = True
            logging.info("Temporary file cleanup function registered with atexit.")
        except Exception as e:
            logging.error(f"Failed to register atexit cleanup function: {e}", exc_info=True)
    else:
        logging.debug("Temporary file cleanup function already registered.")


if __name__ == '__main__':
    # Example usage for testing
    logging.basicConfig(level=logging.DEBUG)
    # Mock ui_utils for direct testing
    print_warning = lambda x: print(f"WARN: {x}")
    print_info = lambda x: print(f"INFO: {x}")

    print("\n--- Testing Startup Message ---")
    display_startup_message()

    print("\n--- Testing Dependency Check ---")
    check_system_dependencies() # Will show warnings if Pillow/Bleach are missing

    print("\n--- Testing URL Masking ---")
    test_url_1 = "https://example.com/api?key=12345abc&data=stuff"
    test_url_2 = "https://another.com/auth?client_id=xyz789&redirect=abc"
    test_url_3 = "https://secure.com/resource?token=bearer-token-value&id=1"
    print(f"Original: {test_url_1} -> Masked: {mask_sensitive_url_data(test_url_1)}")
    print(f"Original: {test_url_2} -> Masked: {mask_sensitive_url_data(test_url_2)}")
    print(f"Original: {test_url_3} -> Masked: {mask_sensitive_url_data(test_url_3)}")

    print("\n--- Testing Log Sanitization ---")
    log_line_1 = "API Request: api_key=supersecretkey123, user=test"
    log_line_2 = "Auth Header: Bearer token=abcdef12345.ghij67890"
    print(f"Original: {log_line_1} -> Sanitized: {sanitize_logging_content(log_line_1)}")
    print(f"Original: {log_line_2} -> Sanitized: {sanitize_logging_content(log_line_2)}")

    print("\n--- Testing Logging Config (will create log file) ---")
    configure_app_logging(level=logging.DEBUG, project_root_dir=".")
    logging.debug("This is a debug message after config.")
    logging.info("This is an info message after config.")

    print("\n--- Testing Cleanup Registration ---")
    # Note: Cleanup runs at actual script exit. We test registration here.
    initialize_temp_file_cleanup()
    initialize_temp_file_cleanup() # Test calling again

    print("\n--- App Utils Tests Complete ---")
