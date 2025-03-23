# UI Utilities Module

```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   ██╗   ██╗██╗    ██╗   ██╗████████╗██╗██╗     ███████╗                   ║
║   ██║   ██║██║    ██║   ██║╚══██╔══╝██║██║     ██╔════╝                   ║
║   ██║   ██║██║    ██║   ██║   ██║   ██║██║     ███████╗                   ║
║   ██║   ██║██║    ██║   ██║   ██║   ██║████████╚════██║                   ║
║   ╚██████╔╝██║    ╚██████╔╝   ██║   ██║███████╗███████║                   ║
║    ╚═════╝ ╚═╝     ╚═════╝    ╚═╝   ╚═╝╚══════╝╚══════╝                   ║
║                                                                            ║
║   Beautiful Terminal Interfaces for Wallgen                                ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

> For detailed information about settings management, see [Wallpaper Settings Module](README_wallpaper_settings.md).

## Overview

The `ui_utils.py` module provides a comprehensive set of utilities for creating beautiful, consistent terminal interfaces in the Wallgen application. It handles everything from colored text output to user input validation, ensuring a smooth and intuitive user experience across the entire application.

## Key Features

- 🎨 **Colored Text Output** - Create visually appealing terminal interfaces with customizable colors and styles
- 🧩 **Consistent UI Elements** - Headers, sections, prompts, and options with unified styling
- ✅ **Input Validation** - Robust handling of user input with clear error messages and default values
- 🔄 **Interactive Elements** - Progress indicators and loading spinners for long-running operations
- 🖥️ **Cross-Platform Support** - Graceful fallbacks for terminals without color support

## Core Components

### Text Formatting Functions

Create visually appealing terminal interfaces with minimal effort:

| Function | Description | Example Usage |
|----------|-------------|---------------|
| `print_header()` | Display prominent section headers | `print_header("Main Menu")` |
| `print_section()` | Create visually distinct subsections | `print_section("Settings")` |
| `print_option()` | Format menu options consistently | `print_option("1", "Generate New Wallpaper")` |
| `print_success()` | Highlight successful operations in green | `print_success("Wallpaper saved!")` |
| `print_error()` | Emphasize errors in red | `print_error("API connection failed")` |
| `print_warning()` | Display cautionary messages in yellow | `print_warning("Low disk space")` |
| `print_info()` | Present informational messages in blue | `print_info("Current resolution: 1920x1080")` |
| `print_prompt()` | Format user prompts consistently | `print_prompt("Enter a prompt")` |

### Example: Creating a Complete Menu

```python
from ui_utils import print_header, print_section, print_option, print_info, get_validated_input

def show_main_menu():
    print_header("Wallgen - AI Wallpaper Generator")
    
    print_section("Main Menu")
    print_option("1", "Generate New Wallpaper")
    print_option("2", "Browse Generated Wallpapers")
    print_option("3", "Manage Settings")
    print_option("4", "Exit")
    
    print_info("Use numbers 1-4 to navigate")
    
    choice = get_validated_input("Select an option", ["1", "2", "3", "4"])
    return choice
```

Output:
```
===============================================
       Wallgen - AI Wallpaper Generator       
===============================================

Main Menu
---------
  1: Generate New Wallpaper
  2: Browse Generated Wallpapers
  3: Manage Settings
  4: Exit

  Use numbers 1-4 to navigate
> Select an option 
```

### User Input Handling

Simplify input collection and validation with robust error handling:

```python
# Basic validation (restricted options)
choice = get_validated_input("Select an option", ["1", "2", "3"])

# With default value
resolution = get_validated_input("Enter resolution (default: 1920x1080)", 
                               default="1920x1080")

# Complex validation with custom function
def is_valid_resolution(value):
    import re
    return bool(re.match(r'^\d+x\d+$', value))

resolution = get_validated_input("Enter resolution (WxH)", 
                               validator=is_valid_resolution,
                               error_message="Please enter resolution in format WIDTHxHEIGHT")
```

### Interactive Elements

Enhance user experience during longer operations with progress indicators:

```python
# Example: Showing a loading spinner during API calls
from ui_utils import show_spinner
import time

def generate_wallpaper(prompt):
    with show_spinner("Generating your wallpaper"):
        # Simulate API call and image processing
        time.sleep(3)
        # Actual API call would go here
        return "path/to/generated/wallpaper.jpg"
```

Output:
```
⠋ Generating your wallpaper
⠙ Generating your wallpaper
⠹ Generating your wallpaper
...
✓ Wallpaper generated successfully!
```

### Navigation Aids

Help users understand where they are in the application with breadcrumb navigation:

```python
from ui_utils import print_breadcrumb

# Display the current navigation path
print_breadcrumb(["Main Menu", "Settings", "Advanced Options"])
```

Output:
```
Main Menu > Settings > Advanced Options
```

## Integration with Main Application

The UI utilities are designed to be imported and used throughout the application:

```python
# Import specific functions
from ui_utils import print_header, print_section, get_validated_input

# Import all UI utilities
from ui_utils import *
```

## Best Practices

- **Consistent Usage**: Use the same UI functions for similar operations throughout the application
- **Color Psychology**: Use colors meaningfully - green for success, red for errors, yellow for warnings
- **Input Validation**: Always validate user input using `get_validated_input()` to prevent errors
- **Error Handling**: Provide clear error messages that help users understand what went wrong
- **Progress Indication**: Show spinners for operations taking more than a second to provide feedback
- **Graceful Degradation**: Account for terminals that don't support colors or special characters

## For Developers

The module is built with flexibility in mind:

- **Automatic Detection**: Terminals without color support get clean, readable output
- **Thread Safety**: Interactive elements like spinners use thread-safe operations
- **Extensible Design**: Add new UI elements by following the established patterns
- **Minimal Dependencies**: Only requires `colorama` for cross-platform color support

### Adding New UI Elements

To add a new UI element, follow this pattern:

```python
def print_new_element(text: str, additional_param: str = "default") -> None:
    """
    Print a new UI element with documentation.
    
    Args:
        text (str): The text to display
        additional_param (str, optional): Description of the parameter. 
                                         Defaults to "default".
    
    Example:
        >>> print_new_element("Sample text", "custom")
    """
    # Implementation here
    print_colored(f"[{additional_param}] {text}", Fore.CYAN)
```

## Technical Details

- Uses `colorama` for cross-platform colored terminal output
- Provides fallbacks when colorama is not available
- Implements thread-safe operations for interactive elements
- Adjusts output format based on terminal width when possible

## Future Enhancements

- Terminal UI framework integration for more advanced interfaces
- Enhanced interactive elements like progress bars and animated menus
- Theming capabilities for customizable color schemes
- Accessibility improvements for screen readers
- Internationalization support for multilingual interfaces

---

> "Good UI is invisible. It guides users without getting in their way." 