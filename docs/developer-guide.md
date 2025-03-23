# Developer Guide

```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   ██████╗ ███████╗██╗   ██╗    ██████╗ ██╗   ██╗██╗██████╗ ███████╗       ║
║   ██╔══██╗██╔════╝██║   ██║    ██╔════╝ ██║   ██║██║██╔══██╗██╔════╝       ║
║   ██║  ██║█████╗  ██║   ██║    ██║  ███╗██║   ██║██║██║  ██║█████╗         ║
║   ██║  ██║██╔══╝  ╚██╗ ██╔╝    ██║   ██║██║   ██║██║██║  ██║██╔══╝         ║
║   ██████╔╝███████╗ ╚████╔╝     ╚██████╔╝╚██████╔╝██║██████╔╝███████╗       ║
║   ╚═════╝ ╚══════╝  ╚═══╝       ╚═════╝  ╚═════╝ ╚═╝╚═════╝ ╚══════╝       ║
║                                                                            ║
║   Technical Reference for Wallgen Developers                               ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

## Introduction

This developer guide provides comprehensive technical information for developers who want to extend, modify, or contribute to the Wallgen project. It covers the application architecture, component interactions, development environment setup, code conventions, and contribution processes.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Development Environment Setup](#development-environment-setup)
- [Project Structure](#project-structure)
- [Core Components](#core-components)
- [API Integration](#api-integration)
- [Testing](#testing)
- [Adding New Features](#adding-new-features)
- [Contributing Guidelines](#contributing-guidelines)

## Architecture Overview

Wallgen follows a simple architecture with clear separation of concerns:

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│                     │     │                     │     │                     │
│   User Interface    │◄───►│   Core Generator    │◄───►│   API Integration   │
│                     │     │                     │     │                     │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
          ▲                           ▲                           ▲
          │                           │                           │
          ▼                           ▼                           ▼
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│                     │     │                     │     │                     │
│  Settings Manager   │◄───►│   File Management   │     │   Prompt System     │
│                     │     │                     │     │                     │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
```

### Key Design Principles

1. **Simplicity**: Components are straightforward with clear responsibilities
2. **Separation of Concerns**: Each module has a specific purpose
3. **Extensibility**: Easy to add new features without modifying existing code
4. **Error Handling**: Basic error handling and recovery
5. **User Preferences**: Simple settings management

## Development Environment Setup

### Prerequisites

- Python 3.8 or higher
- Git
- A text editor or IDE (VS Code recommended)
- Google Gemini API key for testing

### Setting Up Local Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/rasheedh/wallgen.git
   cd wallgen
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your Gemini API key
   ```

## Project Structure

```
wallgen/
├── wallpaper_generator.py    # Main entry point
├── api/                      # API integration
│   ├── __init__.py
│   └── gemini_client.py      # Gemini API client
├── core/                     # Core generation logic
│   ├── __init__.py
│   └── generator.py          # Main generation engine
├── ui/                       # User interface
│   ├── __init__.py
│   └── ui_utils.py           # UI utilities
├── settings/                 # Settings management
│   ├── __init__.py
│   └── preferences.py        # User preferences
├── utils/                    # Utility functions
│   ├── __init__.py
│   └── file_utils.py         # File management utilities
├── tests/                    # Test suite
│   ├── test_generator.py
│   └── test_preferences.py
├── docs/                     # Documentation
├── asset/                    # Assets like images and banners
├── requirements.txt          # Dependencies
└── setup.py                  # Package setup script
```

## Core Components

### Core Generator

The central component responsible for wallpaper generation:

```python
# Example usage of the core generator

from core.generator import WallpaperGenerator
from settings.preferences import UserPreferences

# Initialize with user preferences
prefs = UserPreferences.load()
generator = WallpaperGenerator(prefs)

# Generate a wallpaper
result = generator.generate(
    prompt="A mountain landscape --style digital art",
    output_path="genimage/mountain_landscape.png"
)

print(f"Generated wallpaper at: {result.image_path}")
```

Key classes and methods:

- `WallpaperGenerator`: Main generation class
  - `generate()`: Create wallpaper from prompt
  - `enhance_prompt()`: Add tags to user prompts

### Settings Manager

Handles user preferences and configuration:

```python
# Example of settings management

from settings.preferences import UserPreferences

# Load preferences
prefs = UserPreferences.load()

# Modify settings
prefs.imagen_settings["quality_settings"]["resolution"] = "1920x1080"
prefs.preferred_styles = ["digital art", "cinematic"]

# Save changes
prefs.save()
```

Key classes:

- `UserPreferences`: Handles loading/saving preferences

### File Management

Manages generated wallpapers and file operations:

```python
# Example of file management

from utils.file_utils import WallpaperManager

# Initialize manager
manager = WallpaperManager()

# List wallpapers
wallpapers = manager.list_wallpapers()
for wp in wallpapers[:5]:  # Show latest 5
    print(f"{wp.filename} - {wp.creation_date}")
```

### UI Utilities

Provides terminal UI components:

```python
# Example of UI utilities

from ui.ui_utils import (
    print_header, print_section, print_option, 
    get_validated_input, show_spinner
)

# Print a header
print_header("Wallgen - AI Wallpaper Generator")

# Show a menu section
print_section("Main Menu")
print_option(1, "Generate New Wallpaper")
print_option(2, "Exit")

# Get user input
choice = get_validated_input("Select an option", ["1", "2"])

# Show a loading spinner
with show_spinner("Generating your wallpaper..."):
    # Generation code here
    pass
```

## API Integration

### Gemini API Client

Handles communication with the Google Gemini API:

```python
# Example of API client usage

from api.gemini_client import GeminiClient

# Initialize client
client = GeminiClient(api_key="your_api_key")

# Generate an image
response = client.generate_image(
    prompt="A mountain landscape --style digital art",
    negative_prompt="-people -text -watermark"
)

# Save the image
response.save("genimage/mountain_landscape.png")
```

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

## Adding New Features

When adding new features:

1. Create a new branch for your feature
2. Add tests for new functionality
3. Update documentation
4. Submit a pull request

## Contributing Guidelines

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit a pull request

For more details, see [CONTRIBUTING.md](../CONTRIBUTING.md).

---

<div align="center">
<img src="../asset/logo/gemini.svg" alt="Logo" width="64" height="64">

Documentation last updated: 2024-03-28
</div> 