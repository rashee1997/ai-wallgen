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
- [Testing Framework](#testing-framework)
- [Adding New Features](#adding-new-features)
- [UI Development Guidelines](#ui-development-guidelines)
- [Performance Optimization](#performance-optimization)
- [Contributing Guidelines](#contributing-guidelines)

## Architecture Overview

Wallgen follows a modular architecture with clear separation of concerns:

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
│  Settings Manager   │◄───►│   File Management   │     │   Prompt Engineer   │
│                     │     │                     │     │                     │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
```

### Key Design Principles

1. **Modularity**: Components are self-contained with well-defined interfaces
2. **Separation of Concerns**: Each module has a clear responsibility
3. **Extensibility**: Easy to add new features without modifying existing code
4. **Configurability**: Extensive settings system for customization
5. **Error Resilience**: Robust error handling and recovery

For a more detailed architectural overview, see [ARCHITECTURE.md](../ARCHITECTURE.md).

## Development Environment Setup

### Prerequisites

- Python 3.8 or higher
- Git
- A text editor or IDE (VS Code recommended)
- Google Gemini API key for testing

### Setting Up Local Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/wallgen.git
   cd wallgen
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   ```

3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

4. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

5. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your Gemini API key
   ```

### Development Tools

- **Testing**: pytest
- **Linting**: flake8, pylint
- **Formatting**: black, isort
- **Type Checking**: mypy
- **Documentation**: mkdocs

## Project Structure

```
wallgen/
├── wallgen/                  # Main package
│   ├── __init__.py           # Package initialization
│   ├── wallgen.py            # Entry point
│   ├── api/                  # API integration
│   │   ├── __init__.py
│   │   ├── gemini_client.py  # Gemini API client
│   │   └── ...
│   ├── core/                 # Core generation logic
│   │   ├── __init__.py
│   │   ├── generator.py      # Main generation engine
│   │   └── ...
│   ├── ui/                   # User interface
│   │   ├── __init__.py
│   │   ├── ui_utils.py       # UI utilities
│   │   └── ...
│   ├── settings/             # Settings management
│   │   ├── __init__.py
│   │   ├── settings.py       # Settings manager
│   │   └── ...
│   └── utils/                # Utility functions
│       ├── __init__.py
│       ├── file_utils.py     # File management utilities
│       └── ...
├── tests/                    # Test suite
│   ├── test_generator.py
│   ├── test_settings.py
│   └── ...
├── docs/                     # Documentation
├── asset/                    # Assets like images and banners
├── examples/                 # Example code
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
└── setup.py                  # Package setup script
```

## Core Components

### Core Generator

The central component responsible for wallpaper generation:

```python
# Example usage of the core generator

from wallgen.core.generator import WallpaperGenerator
from wallgen.settings.settings import UserPreferences

# Initialize with user preferences
prefs = UserPreferences.load()
generator = WallpaperGenerator(prefs)

# Generate a wallpaper
result = generator.generate(
    prompt="Mountain landscape at sunset",
    output_path="generated/mountain_sunset.png"
)

print(f"Generated wallpaper at: {result.image_path}")
```

Key classes and methods:

- `WallpaperGenerator`: Main generation class
  - `generate()`: Create wallpaper from prompt
  - `batch_generate()`: Create multiple variations
  - `enhance_prompt()`: Improve user prompts

### Settings Manager

Handles user preferences and configuration:

```python
# Example of settings management

from wallgen.settings.settings import UserPreferences, PresetManager

# Load preferences
prefs = UserPreferences.load()

# Modify settings
prefs.imagen_settings["quality_settings"]["resolution"] = "3840x2160"
prefs.preferred_styles = ["digital art", "cinematic"]

# Save changes
prefs.save()

# Working with presets
preset_manager = PresetManager()
preset_manager.save_preset("high_res_cinematic", prefs, 
                          description="High resolution cinematic settings")
```

Key classes:

- `UserPreferences`: Handles loading/saving preferences
- `PresetManager`: Manages preset storage and loading

### File Management

Manages generated wallpapers and file operations:

```python
# Example of file management

from wallgen.utils.file_manager import WallpaperManager

# Initialize manager
manager = WallpaperManager()

# List wallpapers
wallpapers = manager.list_wallpapers()
for wp in wallpapers[:5]:  # Show latest 5
    print(f"{wp.filename} - {wp.creation_date}")

# Set a wallpaper as desktop background
manager.set_as_wallpaper("generated/mountain_sunset.png")

# Add tags
manager.add_tags("generated/mountain_sunset.png", ["landscape", "sunset"])
```

### UI Utilities

Provides terminal UI components:

```python
# Example of UI utilities

from wallgen.ui.ui_utils import (
    print_header, print_section, print_option, 
    get_validated_input, show_spinner
)

# Display UI elements
print_header("Wallgen - Main Menu")
print_section("Generation Options")
print_option("1", "Generate New Wallpaper")
print_option("2", "Browse Generated Wallpapers")

# Get validated input
choice = get_validated_input("Select an option", ["1", "2", "3", "4"])

# Show a loading spinner
with show_spinner("Generating wallpaper"):
    # Operation happens here
    time.sleep(3)
```

## API Integration

### Gemini API Client

The API client handles communication with Google's Gemini API:

```python
# Example of API client usage

from wallgen.api.gemini_client import GeminiClient

# Initialize client
client = GeminiClient(api_key="your_api_key")

# Generate an image
response = client.generate_image(
    prompt="A cyberpunk cityscape at night with neon lights",
    resolution="1920x1080",
    quality="high"
)

# Check for success
if response.success:
    # Process the image
    image_data = response.image_data
    # ... save or process the image
else:
    # Handle error
    print(f"Error: {response.error_message}")
```

### Request Rate Limiting

The API client implements rate limiting to avoid quota issues:

```python
# Rate limiting configuration

from wallgen.api.rate_limiter import RateLimiter

# Configure rate limiting
limiter = RateLimiter(
    max_requests_per_minute=30,
    max_requests_per_day=1000
)

# Apply to client
client.set_rate_limiter(limiter)
```

### Error Handling

API error handling strategy:

```python
# API error handling

try:
    response = client.generate_image(prompt="Mountain landscape")
    # Process successful response
except GeminiAPIError as e:
    if e.is_rate_limit_error():
        # Handle rate limiting
        wait_time = e.get_retry_after() or 30
        print(f"Rate limited. Retrying in {wait_time} seconds...")
        time.sleep(wait_time)
        # Retry the request
    elif e.is_input_error():
        # Handle prompt issues
        print("The prompt may contain prohibited content.")
    else:
        # General API error
        print(f"API Error: {e}")
```

## Testing Framework

### Unit Tests

Wallgen uses pytest for unit testing:

```python
# Example test file: tests/test_generator.py

import pytest
from wallgen.core.generator import WallpaperGenerator
from wallgen.settings.settings import UserPreferences

class TestGenerator:
    @pytest.fixture
    def generator(self):
        prefs = UserPreferences()
        return WallpaperGenerator(prefs)
    
    def test_prompt_enhancement(self, generator):
        original = "Mountain landscape"
        enhanced = generator.enhance_prompt(original)
        
        # Check that enhancement adds details
        assert len(enhanced) > len(original)
        assert "mountain" in enhanced.lower()
        
    def test_generate_with_invalid_prompt(self, generator):
        with pytest.raises(ValueError):
            generator.generate("")
```

### Mock Testing

Testing API integration without real API calls:

```python
# Example mock test

import pytest
from unittest.mock import patch, MagicMock
from wallgen.api.gemini_client import GeminiClient

class TestGeminiClient:
    @patch('wallgen.api.gemini_client.requests.post')
    def test_generate_image_success(self, mock_post):
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'image': {'b64_json': 'base64encodeddata'},
        }
        mock_post.return_value = mock_response
        
        # Test client with mock
        client = GeminiClient(api_key="test_key")
        result = client.generate_image("test prompt")
        
        # Assertions
        assert result.success is True
        assert mock_post.called
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=wallgen

# Run specific test file
pytest tests/test_generator.py

# Run tests matching a pattern
pytest -k "prompt or settings"
```

## Adding New Features

### Feature Development Process

1. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/new-feature-name
   ```

2. **Implement the Feature**:
   - Follow code style guidelines
   - Add unit tests
   - Update documentation

3. **Run Tests**:
   ```bash
   pytest
   ```

4. **Submit a Pull Request**:
   - Describe the feature
   - Reference any related issues
   - Include test results

### Example: Adding a New Generation Style

```python
# Example: Adding a new style to the style mixer

from wallgen.core.style_mixer import StyleMixer

class StyleMixer:
    # ... existing code ...
    
    def add_watercolor_style(self, prompt, intensity=1.0):
        """
        Add watercolor painting style to the prompt.
        
        Args:
            prompt (str): Original prompt
            intensity (float): Style intensity from 0.0 to 1.0
            
        Returns:
            str: Enhanced prompt with watercolor style
        """
        watercolor_elements = [
            "loose watercolor style",
            "flowing watercolor technique",
            "wet-on-wet watercolor painting",
            "subtle watercolor washes",
        ]
        
        # Select elements based on intensity
        num_elements = max(1, int(intensity * 3))
        selected_elements = random.sample(watercolor_elements, num_elements)
        
        # Create style description
        style_text = ", ".join(selected_elements)
        
        # Add to prompt
        if "style" in prompt.lower():
            # Blend with existing style
            return f"{prompt}, with {style_text}"
        else:
            # Add as primary style
            return f"{prompt}, {style_text}"
    
    # Add to style map for automatic discovery
    def __init__(self):
        self.style_map = {
            # ... existing styles ...
            "watercolor": self.add_watercolor_style,
        }
```

### Creating a New Module

When adding a new module:

1. Create the module directory and files:
   ```
   wallgen/
   └── new_module/
       ├── __init__.py
       └── module_implementation.py
   ```

2. Update imports in `__init__.py`:
   ```python
   from .module_implementation import NewFeature
   
   __all__ = ["NewFeature"]
   ```

3. Add tests in the test directory:
   ```
   tests/
   └── test_new_module.py
   ```

## UI Development Guidelines

### Terminal UI Principles

When extending the UI:

1. **Consistency**: Use existing UI utilities
2. **Feedback**: Always provide clear feedback for actions
3. **Error Handling**: Display helpful error messages
4. **Progressive Disclosure**: Show complex options only when needed

### Adding UI Elements

```python
# Example: Adding a new UI element

def print_info_box(title, text):
    """
    Print an information box with a title and text.
    
    Args:
        title (str): Box title
        text (str): Information text
    """
    width = min(80, max(len(title) + 4, len(text) + 4))
    
    # Top border
    print("┌" + "─" * (width - 2) + "┐")
    
    # Title
    title_padding = (width - len(title) - 2) // 2
    print("│" + " " * title_padding + title + " " * (width - title_padding - len(title) - 2) + "│")
    
    # Separator
    print("├" + "─" * (width - 2) + "┤")
    
    # Text (with word wrapping)
    words = text.split()
    line = ""
    for word in words:
        if len(line) + len(word) + 1 <= width - 4:
            line += word + " "
        else:
            print("│ " + line + " " * (width - len(line) - 4) + " │")
            line = word + " "
    
    if line:
        print("│ " + line + " " * (width - len(line) - 4) + " │")
    
    # Bottom border
    print("└" + "─" * (width - 2) + "┘")
```

### Menu System

When adding new menu options:

```python
# Example: Adding a menu item to the main menu

def build_main_menu():
    menu_items = [
        ("Generate New Wallpaper", generate_wallpaper),
        ("Browse Generated Wallpapers", browse_wallpapers),
        ("Manage Settings", manage_settings),
        # Add new menu item
        ("Advanced Features", advanced_features),
        ("Exit", exit_application),
    ]
    
    return menu_items

def display_menu(menu_items):
    print_header("Wallgen - Main Menu")
    
    for i, (name, _) in enumerate(menu_items, 1):
        print_option(str(i), name)
    
    choice = get_validated_input("Select an option", 
                               [str(i) for i in range(1, len(menu_items) + 1)])
    
    # Execute selected function
    _, func = menu_items[int(choice) - 1]
    func()
```

## Performance Optimization

### Resource Management

Wallgen handles various resources that need optimization:

- **Memory Usage**: Image processing can be memory-intensive
- **Disk Usage**: Generated images and cache management
- **API Usage**: Rate limiting and quota management

### Optimization Techniques

```python
# Example: Image processing optimization

from PIL import Image
import os

def optimize_wallpaper(image_path, quality=85):
    """
    Optimize a wallpaper image for size without significant quality loss.
    
    Args:
        image_path (str): Path to image file
        quality (int): JPEG quality (1-100)
        
    Returns:
        str: Path to optimized image
    """
    # Get file information
    file_size_before = os.path.getsize(image_path)
    
    # Load image
    img = Image.open(image_path)
    
    # Create optimized filename
    filename, ext = os.path.splitext(image_path)
    optimized_path = f"{filename}_optimized.jpg"
    
    # Save with optimization
    img.save(optimized_path, "JPEG", quality=quality, optimize=True)
    
    # Get new file size
    file_size_after = os.path.getsize(optimized_path)
    
    # Calculate reduction
    reduction = (file_size_before - file_size_after) / file_size_before * 100
    
    print(f"Optimized: {file_size_before / 1024:.1f}KB → "
          f"{file_size_after / 1024:.1f}KB ({reduction:.1f}% reduction)")
    
    return optimized_path
```

### Caching Strategy

```python
# Example: Implementing a caching system

from functools import lru_cache
import time
import json
import os

class APICacheManager:
    def __init__(self, cache_dir="cache", max_age_hours=24):
        self.cache_dir = cache_dir
        self.max_age_seconds = max_age_hours * 3600
        
        # Create cache directory if it doesn't exist
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_cached_response(self, prompt, settings):
        """Get cached API response if available and not expired"""
        cache_key = self._generate_cache_key(prompt, settings)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if os.path.exists(cache_file):
            # Check age
            file_age = time.time() - os.path.getmtime(cache_file)
            if file_age < self.max_age_seconds:
                # Cache is valid
                with open(cache_file, 'r') as f:
                    return json.load(f)
        
        return None
    
    def cache_response(self, prompt, settings, response):
        """Cache an API response"""
        cache_key = self._generate_cache_key(prompt, settings)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        with open(cache_file, 'w') as f:
            json.dump(response, f)
    
    def _generate_cache_key(self, prompt, settings):
        """Generate a unique key for the prompt and settings"""
        import hashlib
        # Create a string representation of prompt and relevant settings
        settings_str = json.dumps(settings, sort_keys=True)
        combined = f"{prompt}|{settings_str}"
        
        # Create hash
        return hashlib.md5(combined.encode()).hexdigest()
    
    def clear_expired_cache(self):
        """Clear expired cache entries"""
        current_time = time.time()
        cleared_count = 0
        
        for filename in os.listdir(self.cache_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.cache_dir, filename)
                file_age = current_time - os.path.getmtime(filepath)
                
                if file_age > self.max_age_seconds:
                    os.remove(filepath)
                    cleared_count += 1
        
        return cleared_count
```

## Contributing Guidelines

For detailed contribution guidelines, please refer to [CONTRIBUTING.md](../CONTRIBUTING.md). Here's a summary:

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Document all public classes and functions
- Keep line length to 88 characters (Black formatter standard)

### Git Workflow

1. Fork the repository
2. Create a feature branch
3. Make changes with clear commit messages
4. Add tests
5. Update documentation
6. Submit a pull request

### Commit Message Format

```
[type]: Brief description (50 chars max)

Longer description with details about the change, why it was made,
and any relevant context. Wrap lines at 72 characters.

Closes #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`

### Pull Request Process

1. Ensure code passes all tests
2. Update documentation
3. Get at least one code review
4. Maintain branch with latest changes from main

## Additional Resources

- [Architecture Overview](../ARCHITECTURE.md)
- [API Reference](api-reference.md)
- [Troubleshooting Guide](troubleshooting.md)
- [Quick Reference](../QUICK_REFERENCE.md)

---

<div align="center">
<img src="../asset/logo/gemini.svg" alt="Logo" width="64" height="64">

Documentation last updated: 2024-03-25
</div> 