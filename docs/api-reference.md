# API Reference

```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║    █████╗ ██████╗ ██╗    ██████╗ ███████╗███████╗                         ║
║   ██╔══██╗██╔══██╗██║    ██╔══██╗██╔════╝██╔════╝                         ║
║   ███████║██████╔╝██║    ██████╔╝█████╗  █████╗                           ║
║   ██╔══██║██╔═══╝ ██║    ██╔══██╗██╔══╝  ██╔══╝                           ║
║   ██║  ██║██║     ██║    ██║  ██║███████╗██║                              ║
║   ╚═╝  ╚═╝╚═╝     ╚═╝    ╚═╝  ╚═╝╚══════╝╚═╝                              ║
║                                                                            ║
║   Programmatic Interfaces for Wallgen                                      ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

## Overview

This document provides comprehensive information about Wallgen's programmatic interfaces, outlining both currently implemented features and those planned for future development. Whether you're building plugins, integrating with other tools, or automating wallpaper generation, this reference will help you understand the available APIs.

> **Note on Current Implementation:** This reference includes both currently implemented components and planned features for future development. APIs that are planned but not yet implemented are marked with ⏳.

## Table of Contents

- [Core API](#core-api)
- [WallgenAPI Class](#wallgenapi-class)
- [Generation API](#generation-api)
- [Settings API](#settings-api)
- [Preset Management API](#preset-management-api)
- [File Management API](#file-management-api)
- [Utility Functions](#utility-functions)
- [Event System](#event-system)
- [Error Handling](#error-handling)
- [Examples](#examples)

## Core API

### Module Structure

The Wallgen API is currently being developed with the following planned organization:

```
wallgen/
  ├── api/                    # ⏳ Planned
  │   ├── __init__.py         # ⏳ Planned - Main API entry point
  │   ├── generator.py        # ⏳ Planned - Image generation API
  │   ├── settings.py         # ⏳ Planned - Settings management API
  │   ├── file_manager.py     # ⏳ Planned - File operations API
  │   └── events.py           # ⏳ Planned - Event system API
  └── ...
```

### Importing the API

```python
# ⏳ Planned API imports
from wallgen.api import WallgenAPI

# ⏳ Planned specific module imports
from wallgen.api.generator import generate_wallpaper
from wallgen.api.settings import get_preferences, save_preferences
```

## WallgenAPI Class

The `WallgenAPI` class provides a unified interface to all Wallgen functionality:

```python
# ⏳ Planned for future implementation
class WallgenAPI:
    """
    Main entry point for programmatic interaction with Wallgen.
    
    This class provides access to all Wallgen functionality including
    generation, settings management, and file operations.
    """
    
    def __init__(self, api_key=None, config_path=None):
        """
        Initialize the Wallgen API.
        
        Args:
            api_key (str, optional): Gemini API key. If not provided,
                                     will attempt to load from environment.
            config_path (str, optional): Path to custom configuration file.
        
        Raises:
            WallgenConfigError: If configuration cannot be loaded.
            WallgenAPIKeyError: If API key is not found or invalid.
        """
        pass
```

### Main Methods

| Method | Description | Example Usage | Status |
|--------|-------------|---------------|--------|
| `generate()` | Generate a wallpaper | `api.generate(prompt="Mountain landscape")` | ⏳ Planned |
| `get_settings()` | Get current settings | `settings = api.get_settings()` | ⏳ Planned |
| `update_settings()` | Update settings | `api.update_settings({"resolution": "4k"})` | ⏳ Planned |
| `load_preset()` | Load a settings preset | `api.load_preset("landscape_preset")` | ⏳ Planned |
| `save_preset()` | Save current settings as preset | `api.save_preset("my_preset")` | ⏳ Planned |
| `list_wallpapers()` | List generated wallpapers | `wallpapers = api.list_wallpapers()` | ⏳ Planned |
| `set_wallpaper()` | Set a wallpaper as background | `api.set_wallpaper("path/to/file.png")` | ⏳ Planned |

## Generation API

The Generation API provides functions for creating wallpapers:

```python
# Current implementation available through direct function calls
# ⏳ Planned formal API in wallgen.api.generator module

def generate_wallpaper(
    prompt: str,
    output_path: Optional[str] = None,
    settings: Optional[Dict] = None,
    seed: Optional[int] = None
) -> Dict:
    """
    Generate a wallpaper using the provided prompt and settings.
    
    Args:
        prompt (str): The prompt describing the desired wallpaper.
        output_path (str, optional): Path to save the generated image.
            If not provided, a default path will be used.
        settings (Dict, optional): Generation settings overriding defaults.
        seed (int, optional): Seed value for reproducible generation.
    
    Returns:
        Dict: Information about the generated wallpaper including:
            - image_path (str): Path to the generated image
            - settings (Dict): Settings used for generation
            - prompt (str): Processed prompt
            - timestamp (str): Generation timestamp
    
    Raises:
        WallgenGenerationError: If generation fails.
    """
    pass
```

### Batch Generation

```python
# ⏳ Planned for future implementation
def generate_batch(
    prompt: str,
    variations: int = 3,
    settings: Optional[Dict] = None,
    seed_strategy: str = "random",
    base_seed: Optional[int] = None,
    output_dir: Optional[str] = None,
    parallel: bool = False,
    callback: Optional[Callable] = None
) -> List[str]:
    """
    Generate multiple wallpapers from a single prompt.
    
    Args:
        prompt (str): Base prompt for all variations.
        variations (int): Number of variations to generate.
        settings (Dict, optional): Generation settings.
        seed_strategy (str): "random" or "increment" for seed control.
        base_seed (int, optional): Starting seed if using "increment".
        output_dir (str, optional): Directory to save generated images.
        parallel (bool): Whether to process in parallel.
        callback (Callable, optional): Progress callback function.
    
    Returns:
        List[str]: Paths to all generated images.
    
    Raises:
        WallgenGenerationError: If generation fails.
    """
    pass
```

## Settings API

The Settings API allows programmatic management of preferences:

```python
# Basic implementation exists
# ⏳ Planned enhancement for formal API

def get_preferences() -> UserPreferences:
    """
    Get the current user preferences.
    
    Returns:
        UserPreferences: Object containing all user preferences.
    """
    pass

def save_preferences(preferences: UserPreferences) -> bool:
    """
    Save user preferences to disk.
    
    Args:
        preferences (UserPreferences): Preferences object to save.
    
    Returns:
        bool: True if successful, False otherwise.
    
    Raises:
        WallgenSettingsError: If settings cannot be saved.
    """
    pass

def reset_to_defaults() -> UserPreferences:
    """
    Reset all preferences to default values.
    
    Returns:
        UserPreferences: New preferences object with default values.
    """
    pass
```

### Settings Schema

The `UserPreferences` object has the following structure:

```python
# Basic implementation exists
# ⏳ Planned enhancement with additional fields

class UserPreferences:
    # Basic preferences
    preferred_resolution: str  # Implemented
    
    # Image generation settings
    imagen_settings: Dict[str, Any] = {
        "resolution": str,  # Implemented
        "negative_prompt": str,  # Implemented
    }
    
    # System settings
    system_settings: Dict[str, Any] = {
        "api_key": str,  # Implemented
    }
```

## Preset Management API

The Preset Management API handles saving and loading configuration presets:

```python
# ⏳ Planned for future implementation
def save_preset(
    preset_data: Dict,
    preset_name: str
) -> str:
    """
    Save current settings as a named preset.
    
    Args:
        preset_data (Dict): Preset data including settings and metadata.
        preset_name (str): Name for the preset.
    
    Returns:
        str: Path to the saved preset file.
    
    Raises:
        WallgenPresetError: If preset cannot be saved.
    """
    pass

def load_preset(
    preset_name: str,
    merge: bool = True
) -> bool:
    """
    Load a preset and apply its settings.
    
    Args:
        preset_name (str): Name of the preset to load.
        merge (bool): If True, merge with current settings;
                     If False, replace all settings.
    
    Returns:
        bool: True if preset loaded successfully.
    
    Raises:
        WallgenPresetError: If preset cannot be loaded.
    """
    pass

def list_presets() -> List[Dict]:
    """
    Get a list of all available presets.
    
    Returns:
        List[Dict]: List of preset information including:
            - name (str): Preset name
            - description (str): Preset description
            - created (str): Creation date
            - tags (List[str]): Preset tags
    """
    pass

def delete_preset(preset_name: str) -> bool:
    """
    Delete a preset.
    
    Args:
        preset_name (str): Name of preset to delete.
    
    Returns:
        bool: True if deleted successfully.
    
    Raises:
        WallgenPresetError: If preset cannot be deleted.
    """
    pass
```

## File Management API

The File Management API handles operations on generated wallpapers:

```python
# Basic file operations implemented
# ⏳ Planned enhancement with formal API

def list_wallpapers(
    limit: int = 100,
    offset: int = 0,
    sort_by: str = "date",
    sort_order: str = "desc"
) -> List[Dict]:
    """
    List generated wallpapers.
    
    Args:
        limit (int): Maximum number of wallpapers to return.
        offset (int): Starting offset for pagination.
        sort_by (str): Field to sort by ("date", "name", "size").
        sort_order (str): Sort order ("asc" or "desc").
    
    Returns:
        List[Dict]: List of wallpaper information.
    """
    pass

# ⏳ Planned for future implementation
def get_wallpaper_info(image_path: str) -> Dict:
    """
    Get metadata for a specific wallpaper.
    
    Args:
        image_path (str): Path to wallpaper image.
    
    Returns:
        Dict: Wallpaper metadata.
    
    Raises:
        WallgenFileError: If file does not exist or cannot be read.
    """
    pass

# ⏳ Planned for future implementation
def set_wallpaper(
    image_path: str,
    mode: str = "center"
) -> bool:
    """
    Set a wallpaper as desktop background.
    
    Args:
        image_path (str): Path to wallpaper image.
        mode (str): Fit mode ("center", "stretch", "fill", "fit").
    
    Returns:
        bool: True if successful.
    
    Raises:
        WallgenSystemError: If wallpaper cannot be set.
    """
    pass

# ⏳ Planned for future implementation
def add_wallpaper_tag(
    image_path: str,
    tag: str
) -> bool:
    """
    Add a tag to a wallpaper.
    
    Args:
        image_path (str): Path to wallpaper image.
        tag (str): Tag to add.
    
    Returns:
        bool: True if successful.
    """
    pass

# ⏳ Planned for future implementation
def remove_wallpaper_tag(
    image_path: str,
    tag: str
) -> bool:
    """
    Remove a tag from a wallpaper.
    
    Args:
        image_path (str): Path to wallpaper image.
        tag (str): Tag to remove.
    
    Returns:
        bool: True if successful.
    """
    pass
```

## Utility Functions

### Prompt Utilities

```python
# Basic implementation exists
def enhance_prompt(
    prompt: str,
    enhancement_level: str = "standard"
) -> str:
    """
    Enhance a user prompt with additional details.
    
    Args:
        prompt (str): Base user prompt.
        enhancement_level (str): Level of enhancement 
                                ("minimal", "standard", "maximum").
    
    Returns:
        str: Enhanced prompt.
    """
    pass

# Basic implementation exists
def sanitize_prompt(prompt: str) -> str:
    """
    Sanitize a prompt to remove problematic content.
    
    Args:
        prompt (str): User prompt.
    
    Returns:
        str: Sanitized prompt.
    """
    pass
```

### Style Utilities

```python
# ⏳ Planned for future implementation
def mix_styles(
    styles: Dict[str, float]
) -> str:
    """
    Mix multiple styles with weights.
    
    Args:
        styles (Dict[str, float]): Mapping of style names to weights.
                                  Weights should sum to 1.0.
    
    Returns:
        str: Combined style string for use in prompts.
    """
    pass

# ⏳ Planned for future implementation
def get_available_styles() -> Dict[str, List[str]]:
    """
    Get available style categories and options.
    
    Returns:
        Dict[str, List[str]]: Mapping of categories to available styles.
    """
    pass
```

## Event System

The Event System allows subscribing to notifications about Wallgen operations:

```python
# ⏳ Planned for future implementation
def subscribe(
    event_type: str,
    callback: Callable,
    filters: Optional[Dict] = None
) -> str:
    """
    Subscribe to application events.
    
    Args:
        event_type (str): Type of event to subscribe to.
        callback (Callable): Function to call when event occurs.
        filters (Dict, optional): Filters to apply to events.
    
    Returns:
        str: Subscription ID used to unsubscribe.
    """
    pass

# ⏳ Planned for future implementation
def unsubscribe(subscription_id: str) -> bool:
    """
    Unsubscribe from events.
    
    Args:
        subscription_id (str): ID returned from subscribe.
    
    Returns:
        bool: True if unsubscribed successfully.
    """
    pass
```

### Available Events

> ⏳ All events are planned for future implementation

| Event Type | Description | Data Provided | Status |
|------------|-------------|---------------|--------|
| `generation_start` | Generation process started | Prompt, settings | ⏳ Planned |
| `generation_progress` | Progress update | Percent complete | ⏳ Planned |
| `generation_complete` | Generation completed | Image path, metadata | ⏳ Planned |
| `generation_error` | Generation failed | Error details | ⏳ Planned |
| `settings_changed` | Settings were updated | Changed settings | ⏳ Planned |
| `preset_loaded` | Preset was loaded | Preset name | ⏳ Planned |
| `preset_saved` | Preset was saved | Preset name, data | ⏳ Planned |
| `wallpaper_set` | Wallpaper set as background | Image path | ⏳ Planned |

### Example Event Usage

```python
# ⏳ Planned for future implementation
from wallgen.api.events import subscribe, unsubscribe

# Subscribe to generation completion events
def on_generation_complete(event_data):
    print(f"Wallpaper generated: {event_data['image_path']}")
    # Do something with the new wallpaper

subscription_id = subscribe("generation_complete", on_generation_complete)

# Later, unsubscribe when no longer needed
unsubscribe(subscription_id)
```

## Error Handling

The API uses specific exception types for different error categories:

```python
# Basic implementation exists for core error types
# ⏳ Planned enhancement with additional error types

class WallgenError(Exception):
    """Base class for all Wallgen exceptions"""
    pass

class WallgenAPIKeyError(WallgenError):
    """API key related errors"""
    pass

class WallgenConfigError(WallgenError):
    """Configuration errors"""
    pass

class WallgenGenerationError(WallgenError):
    """Image generation errors"""
    pass

# ⏳ Planned for future implementation
class WallgenSettingsError(WallgenError):
    """Settings management errors"""
    pass

# ⏳ Planned for future implementation
class WallgenPresetError(WallgenError):
    """Preset management errors"""
    pass

class WallgenFileError(WallgenError):
    """File operation errors"""
    pass

# ⏳ Planned for future implementation
class WallgenSystemError(WallgenError):
    """System integration errors"""
    pass
```

### Error Handling Example

```python
# Example shows planned API usage
from wallgen.api import WallgenAPI  # ⏳ Planned
from wallgen.api.exceptions import WallgenGenerationError, WallgenAPIKeyError  # Partially implemented

try:
    # Current implementation uses direct function calls instead of this API
    api = WallgenAPI()  # ⏳ Planned
    result = api.generate(prompt="Mountain landscape at sunset")  # ⏳ Planned
    print(f"Generated wallpaper: {result['image_path']}")
except WallgenAPIKeyError:
    print("API key error: Please check your Gemini API key")
except WallgenGenerationError as e:
    print(f"Generation failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Examples

> **Note:** The following examples demonstrate the planned API usage. Current implementation uses direct function calls.

### Basic Generation

```python
# ⏳ Planned for future implementation
from wallgen.api import WallgenAPI

# Initialize API
api = WallgenAPI()

# Generate a wallpaper
result = api.generate(prompt="A serene forest scene with morning mist")

# Print the result
print(f"Generated image: {result['image_path']}")
print(f"Enhanced prompt: {result['prompt']}")
print(f"Generation time: {result['timestamp']}")

# Set as desktop background
api.set_wallpaper(result['image_path'])
```

### Current Implementation Using Direct Functions

```python
# Current implementation
import os
from wallpaper_generator import generate_wallpaper

# Set API key
os.environ["GEMINI_API_KEY"] = "your_api_key_here"

# Generate a wallpaper
result = generate_wallpaper(prompt="A serene forest scene with morning mist")

# Print the result
print(f"Generated image: {result['image_path']}")
print(f"Enhanced prompt: {result['prompt']}")
```

## Future API Development Roadmap

The Wallgen API is in active development, with the following milestones planned:

1. **Phase 1 (Current)**: Core generation functionality via command-line interface
2. **Phase 2**: Formal API structure with basic generation and settings functions
3. **Phase 3**: Advanced features including preset management and event system
4. **Phase 4**: Complete WallgenAPI class with comprehensive functionality

## See Also

- [Architecture Overview](ARCHITECTURE.md)
- [Developer Guide](developer-guide.md)
- [Advanced Features Guide](advanced-features.md)
- [Troubleshooting Guide](troubleshooting.md)

---

<div align="center">
<img src="../asset/logo/gemini.svg" alt="Logo" width="64" height="64">

Documentation last updated: 2024-03-28
</div> 