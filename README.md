# 🎨 AI Wallpaper Generator

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Gemini API](https://img.shields.io/badge/Gemini%20API-Enabled-blue)](https://ai.google.dev/)

<!-- Additional Badges -->
[![AI](https://img.shields.io/badge/AI-Powered-orange.svg)](https://ai.google.dev/)
[![Imagen](https://img.shields.io/badge/Imagen%203-Enabled-purple.svg)](https://ai.google.dev/)
[![Wallpaper](https://img.shields.io/badge/Wallpaper-Generator-brightgreen.svg)](#features)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey.svg)](#prerequisites)

<div align="center">
<img src="asset/logo/gemini.svg" alt="Gemini Logo" width="128" height="128">

> Powered by [Google's Imagen 3](https://ai.google.dev/) and [Gemini API](https://ai.google.dev/). This project uses Google AI services for image generation. All generated images are subject to Google's terms of service.

**Disclaimer**: This tool uses experimental AI technology that may sometimes provide inaccurate or unexpected content. Use discretion when generating and using the wallpapers. The generated content does not represent Google's views.
</div>

A terminal-based tool for generating wallpapers using Google's Imagen 3 model via the Gemini API. Create desktop wallpapers with customizable prompts and settings.

> **⚠️ UNDER DEVELOPMENT**: This project is currently under active development. Features may change, and some functionality might be incomplete or experimental.

[Features](#key-features) • [Installation](#prerequisites) • [Documentation](#documentation) • [License](#license)

<!-- Trending Tags -->
<p align="center">
  <code>#ai-image-generation</code> •
  <code>#gemini-api</code> •
  <code>#imagen3</code> •
  <code>#wallpaper-generator</code> •
  <code>#python-ai</code>
</p>

</div>

## 🎭 Showcase

Here are some examples of wallpapers generated using this tool:

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="asset/samples/palace_corridor.png" alt="Palace Corridor" width="400"/><br><em>Ancient Palace Corridor</em></td>
      <td align="center"><img src="asset/samples/mosque_street.png" alt="Mosque Street" width="400"/><br><em>Middle Eastern Street View</em></td>
    </tr>
    <tr>
      <td align="center"><img src="asset/samples/garden_art.png" alt="Garden Art" width="400"/><br><em>Topiary Garden Art</em></td>
      <td align="center"><img src="asset/samples/taj_mahal.png" alt="Taj Mahal" width="400"/><br><em>Taj Mahal at Sunset</em></td>
    </tr>
  </table>
</div>

## ✨ Key Features

- **AI-Powered Generation**: Generate wallpapers using Google's Imagen 3 model via Gemini API
- **Multiple Generation Methods**: Choose from AI-generated, random, or custom prompts
- **Basic Settings**: Set resolution and image quality preferences
- **Prompt Enhancement**: Automatically improve user-provided prompts
- **Generation History**: View your previously generated wallpapers
- **Terminal-Based UI**: Simple, text-based interface for all operating systems

For detailed feature documentation, see the [Advanced Features Guide](docs/advanced-features.md).

## 🚀 Prerequisites

- Python 3.8+
- Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

For complete setup instructions, including installation steps for different operating systems, please refer to our [Getting Started Guide](docs/getting-started.md).

## 🧩 System Components

Wallgen's main components include:

- **Core Generator**: Controls the wallpaper generation process
- **Settings Management Package**: Manages user preferences and settings through a modular structure, including dedicated user preferences modules for customization
- **UI Utilities**: Provides terminal interface elements
- **Prompt Engineer**: Enhances prompts for better results
- **API Client**: Communicates with the Gemini API

For a detailed architecture explanation, see our [Architecture Documentation](docs/ARCHITECTURE.md).


## ⚡ Quick Usage

After installation, run the application:

```bash
python wallpaper_generator.py
```

### Common Commands

```bash
# Generate with a random prompt
python wallpaper_generator.py --random

# Generate with a custom prompt
python wallpaper_generator.py --prompt "mountain landscape at sunset"

# Specify resolution (if supported by your API tier)
python wallpaper_generator.py --prompt "forest scene" --resolution "1920x1080"
```

For more examples and usage options, see the [Quick Reference Guide](docs/QUICK_REFERENCE.md).

## 📚 Documentation

### Getting Started
- [Getting Started Guide](docs/getting-started.md) - Installation and basic usage
- [Quick Reference Guide](docs/QUICK_REFERENCE.md) - Commands and common tasks
- [Troubleshooting Guide](docs/troubleshooting.md) - Common issues and solutions

### User Documentation
- [Advanced Features](docs/advanced-features.md) - Detailed feature documentation
- [User Guide](docs/user-guide.md) - Comprehensive usage instructions
- [Settings Import/Export Guide](docs/GUIDE_settings_import_export.md) - Managing your settings

### Developer Documentation
- [Architecture Overview](docs/ARCHITECTURE.md) - System design
- [API Reference](docs/api-reference.md) - Programmatic interface
- [Contributing Guide](CONTRIBUTING.md) - How to contribute
- [Terminology Reference](docs/TERMINOLOGY.md) - Standard terminology
- [UI Utilities Module](docs/README_ui_utils.md) - Terminal interface components
- [Wallpaper Settings Module](docs/README_wallpaper_settings.md) - Settings management
- [Testing Guide](docs/testing-guide.md) - Testing framework and guidelines

### Reference
- [Changelog](CHANGELOG.md) - Version history and updates

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
Made with ❤️ by [Rasheed](https://github.com/rashee1997)
</div>
