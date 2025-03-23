# Wallpaper Settings Module

```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   ███████╗███████╗████████╗████████╗██╗███╗   ██╗ ██████╗ ███████╗        ║
║   ██╔════╝██╔════╝╚══██╔══╝╚══██╔══╝██║████╗  ██║██╔════╝ ██╔════╝        ║
║   ███████╗█████╗     ██║      ██║   ██║██╔██╗ ██║██║  ███╗███████╗        ║
║   ╚════██║██╔══╝     ██║      ██║   ██║██║╚██╗██║██║   ██║╚════██║        ║
║   ███████║███████╗   ██║      ██║   ██║██║ ╚████║╚██████╔╝███████║        ║
║   ╚══════╝╚══════╝   ╚═╝      ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝        ║
║                                                                            ║
║   Customization & Configuration Management for Wallgen                     ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

> For information about importing and exporting settings, see [Settings Import/Export Guide](GUIDE_settings_import_export.md).
> For information about the UI components, see [UI Utilities Module](README_ui_utils.md).

## Overview

The `wallpaper_settings.py` module serves as the central hub for all settings management in the Wallgen application. This module encapsulates user preferences, preset management, and import/export functionality, providing a clean separation of concerns from the main application logic.

## Key Features

- 🎛️ **User Preferences Management** - Store and retrieve user preferences including favorite genres, styles, and image settings
- 🖼️ **Imagen Settings Management** - Configure AI generation parameters like resolution, seed values, and detail levels
- 💾 **Preset System** - Save, load, and manage favorite configuration presets
- 📤 **Import/Export** - Backup and restore your settings across different installations
- 📋 **History Management** - Track and organize your generated wallpapers

## Core Components

### UserPreferences Class

The backbone of the settings system, handling loading, saving, and accessing user preferences:

```python
class UserPreferences:
    """
    Class to manage user preferences for the wallpaper generator.
    
    This class handles loading, saving, and providing access to user preferences
    including image generation settings, style preferences, and application configuration.
    It maintains persistent storage of settings between application runs.
    """
```

Key attributes of the UserPreferences class:

| Attribute | Description | Example Value |
|-----------|-------------|---------------|
| `preferred_genres` | List of genres the user prefers | `["nature", "space", "abstract"]` |
| `preferred_styles` | List of style combinations | `["digital art", "watercolor", "cinematic"]` |
| `preferred_moods` | List of mood modifiers | `["mysterious", "peaceful", "dramatic"]` |
| `imagen_settings` | Dictionary of AI settings | `{"resolution": "1920x1080", "seed": 12345}` |
| `wallpaper_settings` | Dictionary of app settings | `{"auto_set": True, "fit_mode": "center"}` |
| `aspect_ratio` | Preferred aspect ratio | `"16:9"` |

### Settings Initialization Example

```python
# Example: Initializing settings in your application
from wallpaper_settings import initialize_settings

# Initialize with defaults or load from saved file
user_prefs = initialize_settings()

# Access settings
print(f"Current resolution: {user_prefs.imagen_settings['quality_settings']['resolution']}")
print(f"Preferred genres: {', '.join(user_prefs.preferred_genres)}")

# Save changes
user_prefs.preferred_genres.append("fantasy")
user_prefs.save_preferences()
```

### Complete Settings Management Flow

```python
# Example: Complete settings workflow
from wallpaper_settings import (
    initialize_settings, 
    manage_preferences,
    manage_imagen_settings,
    manage_presets,
    export_settings
)

# 1. Initialize settings
user_prefs = initialize_settings()

# 2. Let user modify preferences (interactive)
manage_preferences()

# 3. Configure image generation settings
manage_imagen_settings()

# 4. Save current settings as a preset
from wallpaper_settings import save_preset
save_preset("my_fantasy_preset", "Fantasy-themed settings with high detail")

# 5. Export settings for backup
export_settings()
```

### Preset Management

Save, load, and manage your favorite configurations:

```python
# Example: Managing presets
from wallpaper_settings import manage_presets, load_preset, save_preset, delete_preset

# Interactive preset management
manage_presets()

# Load a specific preset
success = load_preset("landscape_preset")
if success:
    print("Loaded landscape preset successfully")

# Save current settings as a preset with metadata
preset_data = {
    "name": "sci_fi_space",
    "description": "Science fiction space scene with high detail",
    "created": "2023-03-22",
    "tags": ["space", "scifi", "dark", "stars"]
}
save_preset(preset_data, "sci_fi_space")

# Delete an unused preset
delete_preset("old_preset")
```

## Settings Configuration Options

### Quality Settings

Control the visual quality and resolution of generated wallpapers:

```python
# Available quality settings options
quality_settings = {
    "resolution": "1920x1080",  # Common options: "3840x2160" (4K), "2560x1440" (2K)
    "detail_level": "rich_details",  # Options: "standard", "rich_details", "maximum_detail"
    "rendering_quality": "photorealistic"  # Options: "standard", "photorealistic", "enhanced"
}

# Example: Updating resolution
user_prefs.imagen_settings["quality_settings"]["resolution"] = "3840x2160"
user_prefs.save_preferences()
```

### Style Settings

Configure visual style preferences for AI generation:

```python
# Example style settings
style_settings = {
    "art_style": "digital art",  # Options: "digital art", "watercolor", "oil painting", etc.
    "visual_style": "cinematic",  # Options: "cinematic", "realistic", "fantasy", "anime", etc.
    "color_palette": "vibrant",  # Options: "vibrant", "muted", "monochrome", "pastel", etc.
    "lighting": "dramatic"  # Options: "natural", "dramatic", "soft", "high_contrast", etc.
}
```

## Best Practices

- **Preference Changes**: Always use the provided functions to modify preferences rather than direct manipulation
- **Schema Compatibility**: When adding new settings, ensure backward compatibility with existing saved preferences
- **Presets**: Use descriptive names and add relevant tags for better organization
- **Backups**: Regularly export your settings to avoid losing your customizations
- **Testing**: Test your settings changes with a variety of prompts to ensure consistency

## Working with User Preferences

### Reading Preferences

```python
# Access user preferences
from wallpaper_settings import get_preferences

prefs = get_preferences()

# Check if a specific genre is preferred
if "nature" in prefs.preferred_genres:
    print("User prefers nature wallpapers")

# Get current resolution
resolution = prefs.imagen_settings["quality_settings"]["resolution"]
width, height = resolution.split("x")
print(f"Current resolution: {width} × {height}")
```

### Updating Preferences

```python
# Update preferences programmatically
from wallpaper_settings import get_preferences

prefs = get_preferences()

# Update a simple preference
prefs.preferred_moods = ["peaceful", "serene", "calm"]

# Update a nested setting
prefs.imagen_settings["quality_settings"]["resolution"] = "2560x1440"
prefs.imagen_settings["seed"] = random.randint(1, 1000000)

# Save changes
prefs.save_preferences()
```

## Technical Details

- **Storage Format**: Settings are stored in JSON format in `user_preferences.json`
- **History Tracking**: Generation history is kept in `generation_history.json`
- **Presets Location**: Saved in the `presets/` directory with individual JSON files
- **Backup Format**: Complete settings are exported as timestamped JSON files

## For Developers

The module is designed with extensibility in mind:

- **Clean Architecture**: Clear separation between UI, logic, and data storage
- **Type Hinting**: Well-documented functions with comprehensive type hints
- **Error Handling**: Consistent error handling and recovery mechanisms
- **Lazy Loading**: Settings are loaded on-demand to improve startup time

### Adding New Settings

To add a new setting to the module:

1. Update the `UserPreferences.__init__` method with the new default value
2. Add the new setting to the `load_preferences` and `save_preferences` methods
3. Create appropriate UI functions in the settings management menus
4. Update relevant documentation

```python
# Example: Adding a new setting category
def __init__(self):
    # ... existing code ...
    
    # Add new setting category
    self.optimization_settings = {
        "cache_enabled": True,
        "parallel_processing": False,
        "memory_limit": "2GB"
    }
    
    # ... rest of method ...
```

## Future Enhancements

- 🌐 Cloud synchronization of settings across devices
- 👥 Collaborative preset sharing and community repository
- 🏷️ Enhanced preset categorization and tagging system
- 🔄 Settings migration tools for version compatibility
- 📊 Analytics and usage statistics for optimizing defaults

---

> "Perfect customization is when the tool disappears and becomes an extension of yourself." 