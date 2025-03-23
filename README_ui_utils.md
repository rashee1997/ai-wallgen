# UI Utilities Module

![UI Module Banner](https://i.imgur.com/placeholder2.png)

## Overview

The `ui_utils.py` module provides a comprehensive set of utilities for creating beautiful, consistent terminal interfaces in the AI Wallpaper Generator application. It handles everything from colored text output to user input validation, ensuring a smooth and intuitive user experience.

## Key Features

- **Colored Text Output** - Make your terminal interface visually appealing and easier to navigate
- **Consistent UI Elements** - Headers, sections, prompts, and options with unified styling
- **Input Validation** - Robust handling of user input with clear error messages
- **Interactive Elements** - Progress indicators and loading spinners
- **Cross-Platform Support** - Graceful fallbacks for terminals without color support

## Core Components

### Text Formatting Functions

Create visually appealing terminal interfaces with minimal effort:

| Function | Description |
|----------|-------------|
| `print_header()` | Display prominent section headers |
| `print_section()` | Create visually distinct subsections |
| `print_option()` | Format menu options consistently |
| `print_success()` | Highlight successful operations in green |
| `print_error()` | Emphasize errors in red |
| `print_warning()` | Display cautionary messages in yellow |
| `print_info()` | Present informational messages in blue |
| `print_prompt()` | Format user prompts consistently |

```python
# Example: Creating a menu
from ui_utils import print_header, print_section, print_option

print_header("AI Wallpaper Generator")
print_section("Main Menu")
print_option("1", "Generate New Wallpaper")
print_option("2", "Manage Settings")
print_option("3", "Exit")
```

### User Input Handling

Simplify input collection and validation:

```python
# Example: Getting validated input
from ui_utils import get_validated_input

choice = get_validated_input("Select an option (1-3)", ["1", "2", "3"])
```

### Interactive Elements

Enhance user experience during longer operations:

```python
# Example: Showing a loading spinner
from ui_utils import show_spinner
import time

with show_spinner("Generating image"):
    # Perform a long-running operation
    time.sleep(5)
```

### Navigation Aids

Help users understand where they are in the application:

```python
# Example: Displaying navigation breadcrumbs
from ui_utils import print_breadcrumb

print_breadcrumb(["Main Menu", "Settings", "Advanced Options"])
```

## Integration with Main Application

The UI utilities are designed to be imported and used throughout the application:

```python
from ui_utils import (
    print_header, print_section, print_option,
    print_success, print_error, print_info,
    get_validated_input
)
```

## Best Practices

- **Consistent Usage**: Use the same UI functions for similar operations throughout the application
- **Input Validation**: Always validate user input using `get_validated_input()`
- **Error Handling**: Use appropriate message types (error, warning, info) based on context
- **Progress Indication**: Show spinners for operations taking more than a second

## For Developers

The module is built with flexibility in mind:

- Automatic detection and fallback for terminals without color support
- Consistent styling that can be updated in one place
- Extensible design for adding new UI elements

## Technical Details

- Uses `colorama` for cross-platform colored terminal output
- Provides fallbacks when colorama is not available
- Implements thread-safe operations for interactive elements

## Future Enhancements

- Terminal UI framework integration
- Enhanced interactive elements like progress bars
- Theming capabilities for customizable interfaces
- Accessibility improvements

---

> "A great interface disappears, leaving only the experience." 