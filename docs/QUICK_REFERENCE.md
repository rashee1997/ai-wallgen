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

This quick reference guide provides a comprehensive summary of commands, settings, and common usage patterns for the Wallgen application. It focuses on currently implemented features, with notes about planned future enhancements.

## Table of Contents

- [Command Reference](#command-reference)
- [Settings Reference](#settings-reference)
- [Prompt Patterns](#prompt-patterns)
- [File Locations](#file-locations)
- [Common Tasks](#common-tasks)
- [See Also](#see-also)

## Command Reference

### Basic Commands

| Command | Description | Example |
|---------|-------------|---------|
| `python wallpaper_generator.py` | Start the application | `python wallpaper_generator.py` |
| `python wallpaper_generator.py --help` | Display help information | `python wallpaper_generator.py --help` |
| `python wallpaper_generator.py --quiet` | Run in quiet mode (reduced output) | `python wallpaper_generator.py --quiet` |
| `python wallpaper_generator.py --debug` | Run in debug mode (verbose output) | `python wallpaper_generator.py --debug` |

### Generation Commands

| Command | Description | Example |
|---------|-------------|---------|
| `python wallpaper_generator.py --random` | Generate with random prompt | `python wallpaper_generator.py --random` |
| `python wallpaper_generator.py --prompt "..."` | Generate with custom prompt | `python wallpaper_generator.py --prompt "mountain sunset"` |
| `python wallpaper_generator.py --resolution "..."` | Set output resolution | `python wallpaper_generator.py --resolution "3840x2160"` |

> **Note:** Some commands shown in documentation, such as preset management and desktop wallpaper setting, are planned for future implementation.

## Settings Reference

### Resolution Options

| Setting | Description | Values |
|---------|-------------|--------|
| `resolution` | Output resolution | `1080p`, `4K`, `8K`, or custom (`WIDTHxHEIGHT`) |
| `aspect_ratio` | Aspect ratio | `16:9`, `21:9`, `4:3`, `1:1` |

### Style Options

| Setting | Description | Values |
|---------|-------------|--------|
| `style` | Artistic style | `photorealistic`, `digital_art`, `sketch`, etc. |

## Prompt Patterns

### Basic Patterns

```
[subject] in [style] style
[location] during [time of day]
[subject] with [lighting] lighting
[adjective] [subject] in [environment]
```

### Advanced Patterns

```
[adjective], [adjective] [subject] in [environment], [lighting] lighting, [camera] lens, [style] style
```

### Example Prompts

```
"Misty mountain landscape at sunrise, photorealistic style"
"Cyberpunk cityscape at night with neon lights, 85mm lens, shallow depth of field"
"Abstract geometric patterns in vibrant colors, minimalist style, ultra-detailed"
"Ancient temple ruins overgrown with vegetation, dramatic lighting, cinematic style"
```

For more guidance on creating effective prompts, see the [Advanced Features Guide section on effective prompt construction](advanced-features.md#effective-prompt-construction).

## File Locations

| File/Directory | Description | Location |
|----------------|-------------|----------|
| Generated Images | Output wallpapers | `./generated/` |
| Logs | Application logs | `./logs/` |

## Common Tasks

### Generate a Wallpaper with Random Prompt

```bash
# Generate a wallpaper using a random prompt
python wallpaper_generator.py --random
```

### Generate a Wallpaper with Custom Prompt

```bash
# Generate a wallpaper with a specific prompt
python wallpaper_generator.py --prompt "mountain landscape at sunset"
```

### Specify Resolution

```bash
# Generate with specific resolution
python wallpaper_generator.py --prompt "forest scene" --resolution "1920x1080"
```

### Use Negative Prompts

```bash
# Generate with negative prompts
python wallpaper_generator.py --prompt "forest scene" --negative "people, text, watermark"
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