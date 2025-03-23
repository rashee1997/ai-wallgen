# Advanced Features Guide

```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║    █████╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗ ██████╗███████╗██████╗       ║
║   ██╔══██╗██╔══██╗██║   ██║██╔══██╗████╗  ██║██╔════╝██╔════╝██╔══██╗      ║
║   ███████║██║  ██║██║   ██║███████║██╔██╗ ██║██║     █████╗  ██║  ██║      ║
║   ██╔══██║██║  ██║╚██╗ ██╔╝██╔══██║██║╚██╗██║██║     ██╔══╝  ██║  ██║      ║
║   ██║  ██║██████╔╝ ╚████╔╝ ██║  ██║██║ ╚████║╚██████╗███████╗██████╔╝      ║
║   ╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝       ║
║                                                                            ║
║   Additional Features for Wallgen                                          ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

## Overview

This guide outlines the additional features available in Wallgen beyond basic wallpaper generation. These features help you get more out of the application through prompt techniques and basic configuration options.

## Table of Contents

- [Prompt Engineering Techniques](#prompt-engineering-techniques)
- [Basic Generation Settings](#basic-generation-settings)
- [History Management](#history-management)
- [Command-Line Usage](#command-line-usage)

## Prompt Engineering Techniques

### Effective Prompt Construction

Create effective prompts that produce better results from the Imagen 3 model:

- **Subject-Style-Mood Structure**
  ```
  [subject] in [art style] with [mood] atmosphere
  ```
  
  Example: "A mountain landscape in digital art style with peaceful atmosphere"

- **Technical Parameter Inclusion**
  ```
  [subject] in [style], [technical parameters]
  ```
  
  Example: "A cityscape in cinematic style, 4K resolution, dramatic lighting"

For more guidance on creating effective prompts, see the [User Guide section on prompt structure](user-guide.md#prompt-structure).

### Negative Prompts

Negative prompts tell the AI what to avoid:

```
A forest scene with mountain backdrop -people -text -watermark -signature
```

Common elements to exclude:
- Text and watermarks
- People (if not desired)
- Specific objects or styles

### Prompt Enhancement

Wallgen can automatically enhance your basic prompts:

1. Type a simple prompt like "mountain landscape at sunset"
2. The system will add details and technical parameters
3. The enhanced prompt produces better results than the basic input

For more details on how prompt enhancement works, see the [User Guide section on prompt enhancement](user-guide.md#prompt-enhancement).

## Basic Generation Settings

### Resolution Settings

You can specify resolution when generating wallpapers from the command line. For detailed command-line options, see the [Quick Reference Guide](QUICK_REFERENCE.md#command-line-options).

Basic resolution example:
```bash
# Generate with specific resolution (if supported by your API tier)
python wallpaper_generator.py --prompt "forest scene" --resolution "1920x1080"
```

Available resolution options depend on your API tier limitations.

### Random vs Custom Generation

Choose your preferred generation method:

```bash
# Generate with a random prompt
python wallpaper_generator.py --random

# Generate with a custom prompt
python wallpaper_generator.py --prompt "mountain landscape at sunset"
```

For a complete list of command options, see the [Quick Reference Guide](QUICK_REFERENCE.md#command-line-options).

## History Management

### Viewing Generated Wallpapers

All generated wallpapers are saved to the `generated/` directory with a timestamp and theme identifier in the filename.

To browse your generated wallpapers, select "Browse Generated Wallpapers" from the main menu.

For more information on managing your generated images, see the [User Guide section on managing generated images](user-guide.md#managing-generated-images).

## Command-Line Usage

For a complete reference of command-line options and examples, see the [Quick Reference Guide](QUICK_REFERENCE.md#command-line-options).

## See Also

- [Getting Started Guide](getting-started.md)
- [Quick Reference Guide](QUICK_REFERENCE.md)
- [Troubleshooting Guide](troubleshooting.md)
- [User Guide](user-guide.md)

---

<div align="center">
<img src="../asset/logo/gemini.svg" alt="Logo" width="64" height="64">

Documentation last updated: 2024-03-25
</div>