# Wallgen Quick Reference Guide

```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   ██████╗ ██╗   ██╗██╗ ██████╗██╗  ██╗    ██████╗ ███████╗███████╗        ║
║   ██╔═══██╗██║   ██║██║██╔════╝██║ ██╔╝    ██╔══██╗██╔════╝██╔════╝        ║
║   ██║   ██║██║   ██║██║██║     █████╔╝     ██████╔╝█████╗  █████╗          ║
║   ██║▄▄ ██║██║   ██║██║██║     ██╔═██╗     ██╔══██╗██╔══╝  ██╔══╝          ║
║   ╚██████╔╝╚██████╔╝██║╚██████╗██║  ██╗    ██║  ██║███████╗██║             ║
║    ╚══▀▀═╝  ╚═════╝ ╚═╝ ╚═════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚══════╝╚═╝             ║
║                                                                            ║
║   Quick Reference Guide for Wallgen                                        ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

## Overview

This quick reference guide provides a comprehensive summary of features, settings, and common usage patterns for the Wallgen application.

## Table of Contents

- [Basic Usage](#basic-usage)
- [Prompt System](#prompt-system)
- [File Locations](#file-locations)
- [Common Tasks](#common-tasks)
- [See Also](#see-also)

## Basic Usage

### Starting the Application

1. Open a terminal
2. Navigate to the Wallgen directory
3. Run the application:
   ```bash
   python wallpaper_generator.py
   ```

### Main Menu Options

1. Generate New Wallpaper
   - Random Generation
   - Custom Prompt

2. Exit

## Prompt System

### Tag-Based System

Wallgen uses a tag-based system to enhance your prompts. Available tags:

| Tag | Description | Example |
|-----|-------------|---------|
| `--style` | Specify art style | `--style digital art` |
| `--mood` | Set the mood/atmosphere | `--mood peaceful` |
| `--quality` | Add quality descriptors | `--quality high detail` |

### Example Prompts

```
# Basic prompt with style
A mountain landscape --style digital art

# Detailed prompt with multiple tags
A cityscape at night --style cyberpunk --mood mysterious --quality high detail

# Prompt with negative elements
A forest scene -people -text -watermark
```

For more guidance on creating effective prompts, see the [Advanced Features Guide section on tag-based prompt system](advanced-features.md#tag-based-prompt-system).

## File Locations

| File/Directory | Description | Location |
|----------------|-------------|----------|
| Generated Images | Output wallpapers | `./genimage/` |
| Preferences | User settings | `./preferences.json` |

## Common Tasks

### Generate a Wallpaper with Random Prompt

1. Start the application
2. Select "Generate New Wallpaper"
3. Choose "Random Generation"
4. Wait for generation to complete

### Generate a Wallpaper with Custom Prompt

1. Start the application
2. Select "Generate New Wallpaper"
3. Choose "Custom Prompt"
4. Enter your prompt with optional tags
5. Wait for generation to complete

### Use Negative Prompts

Add negative elements to your prompt using the `-` prefix:

```
A forest scene -people -text -watermark
```

For information on using negative prompts, see the [Advanced Features Guide section on negative prompts](advanced-features.md#negative-prompts).

## See Also

- [Getting Started Guide](getting-started.md)
- [Advanced Features Guide](advanced-features.md)
- [User Guide](user-guide.md)
- [Troubleshooting Guide](troubleshooting.md)
- [FAQ](faq.md)

---

<div align="center">
<img src="../asset/logo/gemini.svg" alt="Logo" width="64" height="64">

Documentation last updated: 2024-03-28
</div> 