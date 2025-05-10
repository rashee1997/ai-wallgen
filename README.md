# 🎨 AI Wallpaper Generator

<div align="center">

  <a href="https://www.python.org/downloads/" title="Requires Python 3.8+">
    <img alt="Python 3.8+" src="https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white&style=for-the-badge">
  </a>
  <a href="LICENSE" title="MIT License">
    <img alt="License MIT" src="https://img.shields.io/badge/License-MIT-brightgreen?style=for-the-badge">
  </a>
  <a href="https://ai.google.dev/" title="Gemini API">
    <img alt="Gemini API" src="https://img.shields.io/badge/Gemini%20API-Enabled-blue?style=for-the-badge&logo=google">
  </a>
  <a href="#prerequisites" title="Supported Platforms">
    <img alt="Platform" src="https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey?style=for-the-badge&logo=linux">
  </a>

</div>

---

<div align="center">
  <img src="asset/logo/gemini.svg" alt="Gemini Logo" width="128" height="128">
</div>

<div align="center">

> Powered by [Google's Imagen 3](https://ai.google.dev/) and [Gemini API](https://ai.google.dev/).  
> This project uses Google AI services for image generation.  
> All generated images are subject to Google's terms of service.
>
> **Disclaimer**: This tool uses experimental AI technology that may sometimes provide inaccurate or unexpected content.  
> Use discretion when generating and using the wallpapers.  
> The generated content does not represent Google's views.

</div>

---

A terminal-based tool for generating wallpapers using Google's Imagen 3 model via the Gemini API. Create desktop wallpapers with customizable prompts and settings.

---

## 🧑‍💻 Project Architecture & Codebase Overview

This project features a modular Python structure with a service-oriented design. The main entry point is `run_wallgen.py`, and the core logic resides in the `wall_gen/` package.

For a detailed breakdown of the architecture, components, and operational flows, please see the [Project Overview & Architecture document](docs/PROJECT_OVERVIEW.md).

---

### 🔍 Development & Contribution

The codebase is designed for modularity. Contributions are welcome! Please refer to our [Git Commit Guide](docs/git-commit-guide.md) for commit standards. Bug reports and feature suggestions can be made via GitHub Issues.

---

[Features](#✨-key-features) • [Prerequisites](#🚀-prerequisites) • [Quick Usage](#⚡-quick-usage) • [Documentation](#📚-documentation) • [License](#📝-license)

<p align="center">
  <code>#ai-image-generation</code> •
  <code>#gemini-api</code> •
  <code>#imagen3</code> •
  <code>#wallpaper-generator</code> •
  <code>#python-ai</code>
</p>

---

## 🎭 Showcase

Here are some examples of wallpapers generated using this tool:

<div align="center">

|     |     |
| --- | --- |
| <img src="asset/samples/palace_corridor.png" alt="Palace Corridor" width="400"/><br><em>Ancient Palace Corridor</em> | <img src="asset/samples/mosque_street.png" alt="Mosque Street" width="400"/><br><em>Middle Eastern Street View</em> |
| <img src="asset/samples/garden_art.png" alt="Garden Art" width="400"/><br><em>Topiary Garden Art</em> | <img src="asset/samples/taj_mahal.png" alt="Taj Mahal" width="400"/><br><em>Taj Mahal at Sunset</em> |

</div>

---

## ✨ Key Features

- **AI-Powered Generation:** Create unique wallpapers using Google's Imagen 3 model via the Gemini API.
- **Multiple Generation Methods:** Choose from AI-generated, random, or custom user prompts.
- **Advanced Settings & Customization:** Fine-tune generation with detailed Imagen settings (camera, lighting, composition, color), manage presets, and personalize user preferences. See [Dynamic Configuration](docs/feature_dynamic_configuration.md) for advanced customization.
- **AI Preset Generation:** Automatically generate coherent setting presets using AI. Full details in the [AI Preset Generation Guide](docs/AI_PRESET_GENERATOR.md).
- **AI Style Generation:** Generate unique artistic styles using AI. See the [AI Style Generation Guide](docs/feature_ai_style_generation.md).
- **Detailed Prompt Engineering:** Utilizes sophisticated prompt enhancement techniques for optimal results. Learn more in the [Prompt Engineering Guide](docs/feature_prompt_engineering.md).
- **GUI Image Preview:** Preview generated images in a graphical window (Qt or Tkinter).
- **Cross-Platform Wallpaper Setting:** Automatically sets wallpapers on Windows, macOS, and various Linux desktop environments. More details in [Other Key Features](docs/other_key_features.md).
- **Generation History:** Keep track of and view previously generated wallpapers and their settings. More details in [Other Key Features](docs/other_key_features.md).
- **Terminal-Based UI & CLI:** Offers both an interactive menu for ease of use and a comprehensive command-line interface for advanced control. See the [Installation and CLI Guide](docs/INSTALLATION_AND_CLI_GUIDE.md) for all CLI options.

---

## 🚀 Prerequisites

- Python 3.8+
- A Google Gemini API Key is required. You can obtain one from [Google AI Studio](https://makersuite.google.com/app/apikey).

For complete setup instructions, installation steps for different operating systems, and detailed command-line usage, please refer to the comprehensive [Installation and CLI Guide](docs/INSTALLATION_AND_CLI_GUIDE.md).

---

## ⚡ Quick Usage

After installation and setting up your API key, run the application:

```bash
python run_wallgen.py
```
This will start the interactive menu.

For command-line operations, here are a couple of basic examples:

```bash
# Generate a wallpaper with a random prompt
python run_wallgen.py --random

# Generate with a custom prompt
python run_wallgen.py --prompt "a serene beach at sunset"
```

For a full list of all CLI commands, options, and detailed examples for `run_wallgen.py`, `ai_preset_generator.py`, and `ai_style_generator.py`, please consult the [Installation and CLI Guide](docs/INSTALLATION_AND_CLI_GUIDE.md).

---

## 📚 Documentation

- [Installation and CLI Guide](docs/INSTALLATION_AND_CLI_GUIDE.md) — Detailed installation and command-line usage
- [Project Overview & Architecture](docs/PROJECT_OVERVIEW.md) — High-level system design, component breakdown, and **operational flow diagrams**.
- [Git Commit Guide](docs/git-commit-guide.md) — Guidelines for writing Git commit messages
- [Changelog](CHANGELOG.md) — Version history and updates

---

## 📝 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
<a href="https://github.com/rashee1997" target="_blank" rel="noopener noreferrer" style="text-decoration:none; border-radius: 12px; padding: 6px 12px; background-color: #e55353; color: white; font-weight: 600; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: inline-flex; align-items: center; gap: 6px;">
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="white" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41 0.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
  Made with by Rasheed
</a>
</div>
