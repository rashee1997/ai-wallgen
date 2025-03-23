# Settings Import/Export Guide

![Import/Export Banner](https://i.imgur.com/placeholder3.png)

> For detailed information about the settings module, see [Wallpaper Settings Module](README_wallpaper_settings.md).

## Introduction

The AI Wallpaper Generator allows you to back up, restore, and share your carefully crafted settings through its powerful import/export functionality. This guide will walk you through everything you need to know about managing your settings.

## Why Use Import/Export?

- **Backup Your Perfect Setup** - Save your carefully tuned preferences before making major changes
- **Transfer Between Devices** - Move your settings from one computer to another
- **Share With Friends** - Export your amazing configuration for others to enjoy
- **Create Multiple Profiles** - Maintain different settings sets for various purposes

## Exporting Your Settings

### What Gets Exported?

When you export your settings, the following information is saved:

- All user preferences (genres, styles, moods, etc.)
- Imagen AI settings (resolution, seed values, quality settings)
- Export date and time for reference

> ⚠️ **Note**: Your generation history and presets are not included in exports.

### How to Export Settings

1. From the main menu, select **"Tools & Utilities"**
2. Choose **"Export Settings"**
3. Enter a meaningful filename (without extension)
4. Your settings will be saved as a JSON file in the current directory

```
Main Menu > Tools & Utilities > Export Settings
```

### Example

```
================================================================================
                               Export Settings                                 
================================================================================

Enter filename for export (without extension): my_nature_settings

✅ Settings exported to my_nature_settings.json
```

## Importing Settings

### Before You Import

- Consider exporting your current settings as a backup
- Ensure the import file is from a trusted source
- Verify the file has the correct format (usually created by the export function)

### How to Import Settings

1. From the main menu, select **"Tools & Utilities"**
2. Choose **"Import Settings"**
3. Enter the filename (with .json extension)
4. Your settings will be updated with the imported values

```
Main Menu > Tools & Utilities > Import Settings
```

### Example

```
================================================================================
                               Import Settings                                 
================================================================================

Enter filename to import (with extension): my_nature_settings.json

✅ Settings imported successfully
```

## Managing Image Filenames

The AI Wallpaper Generator can automatically update your generation history with consistent filenames, making it easier to track and locate your generated images.

### How to Update History with Filenames

1. From the main menu, select **"Tools & Utilities"**
2. Choose **"Update History Filenames"**
3. The system will process your generation history and add appropriate filenames

```
Main Menu > Tools & Utilities > Update History Filenames
```

### Example

```
================================================================================
                           Update History Filenames                             
================================================================================

ℹ Generation history updated with image filenames
```

## Advanced Usage

### Command Line Export/Import

For advanced users, you can script the export/import process:

```python
# Export settings programmatically
from wallpaper_settings import export_settings
export_settings("my_backup")  # Will save to my_backup.json

# Import settings programmatically
from wallpaper_settings import import_settings
import_settings("my_backup.json")
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| "File not found" error | Verify the file path and name are correct |
| Import fails | Ensure the file is a valid JSON export file |
| Settings not updating | Check file permissions and try again |
| Lost settings | Use your most recent export file to restore |

## Best Practices

- **Regular Backups**: Export your settings regularly, especially after making significant changes
- **Descriptive Filenames**: Use meaningful names like "nature_style_june2025.json" instead of "settings1.json"
- **Version Control**: Consider adding dates to your export filenames
- **Organized Storage**: Keep your exports in a dedicated folder for easy access

## Examples and Use Cases

### Scenario 1: Upgrading Your System

1. Export your settings from your old system
2. Install the AI Wallpaper Generator on your new system
3. Copy the export file to your new system
4. Import the settings

### Scenario 2: A/B Testing Different Styles

1. Configure settings for Style A and export them
2. Change to Style B and export with a different name
3. Switch between them by importing as needed

---

> "The ability to save and restore is the foundation of experimentation." 