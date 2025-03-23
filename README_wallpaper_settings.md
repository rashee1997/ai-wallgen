# Wallpaper Settings Module

![Settings Module Banner](https://i.imgur.com/placeholder.png)

## Overview

The `wallpaper_settings.py` module serves as the central hub for all settings management in the AI Wallpaper Generator application. This module encapsulates user preferences, preset management, and import/export functionality, providing a clean separation of concerns from the main application logic.

## Key Features

- **User Preferences Management** - Store and retrieve user preferences including favorite genres, styles, and image settings
- **Imagen Settings Management** - Configure AI generation parameters like resolution, seed values, and detail levels
- **Preset System** - Save, load, and manage favorite configuration presets
- **Import/Export** - Backup and restore your settings across different installations
- **History Management** - Track and organize your generated wallpapers

## Core Components

### UserPreferences Class

The backbone of the settings system, handling loading, saving, and accessing user preferences.

```python
# Example: Initializing settings
from wallpaper_settings import initialize_settings

user_prefs = initialize_settings()
print(f"Current preferred genres: {user_prefs.preferred_genres}")
```

### Settings Management Functions

Comprehensive utilities for managing all aspects of the application settings:

| Function | Description |
|----------|-------------|
| `manage_preferences()` | Interactive menu for adjusting user preferences |
| `manage_imagen_settings()` | Configure AI image generation parameters |
| `configure_advanced_options()` | Fine-tune advanced generation settings |

### Preset Management

Save your favorite configurations for quick access:

```python
# Example: Saving a preset
from wallpaper_settings import save_preset

save_preset("nature_sunset", "My favorite sunset settings")
```

### Import/Export Functionality

Backup and share your settings:

```python
# Example: Exporting settings
from wallpaper_settings import export_settings

export_settings()  # Will prompt for filename
```

## Integration with Main Application

The settings module is designed to integrate seamlessly with the main wallpaper generator application:

1. Import the module: `import wallpaper_settings`
2. Initialize settings: `user_prefs = wallpaper_settings.initialize_settings()`
3. Access settings throughout the application

## Best Practices

- **Preference Changes**: Always use the provided functions to modify preferences rather than direct manipulation
- **Presets**: Use descriptive names for presets to easily identify them later
- **Backups**: Regularly export your settings to avoid losing your customizations

## Technical Details

- **File Storage**: Settings are stored in JSON format in `user_preferences.json`
- **History**: Generation history is kept in `generation_history.json`
- **Presets**: Saved in the `presets/` directory with individual JSON files

## For Developers

The module is designed with extensibility in mind:

- Clear separation of UI and logic
- Well-documented functions with type hints
- Consistent error handling patterns

## Future Enhancements

- Cloud synchronization of settings
- Collaborative preset sharing
- Enhanced preset categorization
- Settings migration tools

---

> "The power of customization is at your fingertips." 