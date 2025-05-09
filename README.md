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
  <a href="#features" title="Wallpaper Generator">
    <img alt="Wallpaper Generator" src="https://img.shields.io/badge/Wallpaper-Generator-brightgreen?style=for-the-badge&logo=wallpaperflare">
  </a>
  <a href="https://ai.google.dev/" title="AI Powered">
    <img alt="AI Powered" src="https://img.shields.io/badge/AI--Powered-orange?style=for-the-badge&logo=artificial-intelligence">
  </a>
  <a href="https://ai.google.dev/" title="Imagen 3 Enabled">
    <img alt="Imagen 3" src="https://img.shields.io/badge/Imagen%203-Enabled-purple?style=for-the-badge&logo=google">
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

- **Modular Python project using a service-oriented structure for maintainability.**
- **Entrypoint:** `run_wallgen.py` — handles CLI parsing, initialization, user orchestration.
- **Core logic:** `wall_gen/` package:
    - `prompt_service.py`, `image_service.py`, `wallpaper_service.py`, `preview_service.py`
    - Utilities: `app_utils.py`, `file_utils.py`, `ui_utils.py`, `cache_utils.py`, `graceful_exit.py`, `image_editor.py`
    - Configuration: `gemini_config.py`, `config.py`
    - **Sub-packages:**
        - `settings_modules/`: user preferences, import/export, menu management
        - `prompt_modules/`: prompt formatting, random/custom generation, negative prompt support
        - `preview_backends/`: separate Qt and Tkinter GUI previewers
        - `history/`: user image/prompt generation history tools
- **Preset & Style CLI tools in root:**
    - `ai_style_generator.py` — Generate/preview AI styles by category with Imagen 3/Gemini.
    - `ai_prest_gen/` — Preset generator/logic, templates, and management.
- **Data/asset directories:** `presets/`, `genimage/`, `asset/logo/`, `asset/samples/`
- **All user customizations support deep/nested JSON via `user_preferences.json`.**
- **Image preview via terminal or GUI (PyQt5/Tkinter).**
- **Cross-platform support:** Windows, macOS, Linux DEs (uses platform-specific handlers for setting wallpapers).

---

### 🔍 Development & Contribution

- **Codebase follows a modular design for ease of customization and testing.**
- All modules in `wall_gen/` use absolute imports for clean execution from project root.
- **Contributions:** Please see [docs/git-commit-guide.md](docs/git-commit-guide.md) for Commit Standards.
- Bug reports and feature suggestions are welcome via GitHub Issues.
- No automated tests yet: testing is manual, but several modules include if __name__ == '__main__': blocks with example/test code.
- **Refactor:** Recent refactor replaced all relative imports to prevent import errors and ease top-level execution.
- **Known limitation:** No integrated unit/integration tests. GUI preview requires PyQt5 or Tkinter installed; headless systems may need tweaks.

---

## Recent Changes

- Major refactor to modularize the codebase into multiple packages and modules for better maintainability and extensibility.
- Added AI-powered preset and style generation features.
- Enhanced CLI with new options and improved user experience.
- See [CHANGELOG.md](CHANGELOG.md) for detailed version history and updates.

> **Note**: The codebase has been recently modularized. The main entry point is now `run_wallgen.py`.

> **⚠️ UNDER DEVELOPMENT**: This project is currently under active development. Features may change, and some functionality might be incomplete or experimental.

[Features](#✨-key-features) • [Installation](#🚀-prerequisites) • [System Components](#🧩-system-components) • [Quick Usage](#⚡-quick-usage) • [Documentation](#📚-documentation) • [License](#📝-license)

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

---

## ✨ Key Features

- <img src="https://api.iconify.design/mdi/brain.svg?color=%236200ea" alt="AI Icon" width="20" height="20" style="vertical-align:middle;"> **AI-Powered Generation:** Generate wallpapers using Google's Imagen 3 model via Gemini API.
- <img src="https://api.iconify.design/mdi/shuffle-variant.svg?color=%2303a9f4" alt="Methods Icon" width="20" height="20" style="vertical-align:middle;"> **Multiple Generation Methods:** Choose from AI-generated, random, or custom prompts.
- <img src="https://api.iconify.design/mdi/tune.svg?color=%23ff9800" alt="Settings Icon" width="20" height="20" style="vertical-align:middle;"> **Advanced Settings & Customization:** Fine-tune generation with detailed Imagen settings (camera, lighting, composition, color, etc.), manage presets, and save user preferences.
- <img src="https://api.iconify.design/mdi/creation.svg?color=%234caf50" alt="Preset Icon" width="20" height="20" style="vertical-align:middle;"> **AI Preset Generation:** Automatically generate coherent setting presets using AI, with CLI commands for generation, listing, loading, and deletion.
- <img src="https://api.iconify.design/mdi/palette-swatch-outline.svg?color=%23e91e63" alt="Style Icon" width="20" height="20" style="vertical-align:middle;"> **AI Style Generation:** Generate unique artistic styles using AI, with CLI options for category selection, detailed output, and saving to preferences.
- <img src="https://api.iconify.design/mdi/pencil-circle-outline.svg?color=%232196f3" alt="Prompt Icon" width="20" height="20" style="vertical-align:middle;"> **Detailed Prompt Engineering:** Sophisticated prompt enhancement techniques for optimal results.
- <img src="https://api.iconify.design/mdi/image-outline.svg?color=%23795548" alt="Preview Icon" width="20" height="20" style="vertical-align:middle;"> **GUI Image Preview:** Preview generated images in a graphical window (Qt or Tkinter), with options for terminal or GUI previews.
- <img src="https://api.iconify.design/mdi/desktop-mac-dashboard.svg?color=%23607d8b" alt="Platform Icon" width="20" height="20" style="vertical-align:middle;"> **Cross-Platform Wallpaper Setting:** Automatically sets wallpapers on Windows, macOS, and various Linux desktop environments, with options to skip preview and apply wallpapers directly.
- <img src="https://api.iconify.design/mdi/history.svg?color=%239c27b0" alt="History Icon" width="20" height="20" style="vertical-align:middle;"> **Generation History:** View previously generated wallpapers along with the settings used.
- <img src="https://api.iconify.design/mdi/console-line.svg?color=%233f51b5" alt="Terminal Icon" width="20" height="20" style="vertical-align:middle;"> **Terminal-Based UI:** Simple, text-based interface for interactive use.
- <img src="https://api.iconify.design/mdi/keyboard-settings-outline.svg?color=%23009688" alt="CLI Icon" width="20" height="20" style="vertical-align:middle;"> **Command-Line Interface:** Control generation, presets, styles, image previews, and advanced options directly via CLI arguments.

---

## 🛠️ Advanced: Adding Custom Keys in User Preferences (Dynamic Settings)

**Wallgen supports unlimited customization!** You can add any custom settings/key–value pairs (at any depth) in your `user_preferences.json` or via the UI/settings menus, and *all* such fields will be automatically discovered and included in prompt generation, thanks to dynamic flattening of settings.

This lets you extend Imagen settings, styles, or user metadata with no code changes.

**Example: Adding custom keys and nested fields to user preferences**

```json
{
  "preferred_styles": ["fantasy", "minimalist"],
  "aspect_ratio": "21:9",
  "imagen_settings": {
    "lighting_settings": {
      "lighting_type": "neon",
      "custom_light_mode": "ambient disco"
    },
    "composition_settings": {
      "technique": "rule_of_thirds",
      "experimental_composition": {
        "geometry_focus": "hexagonal_pattern",
        "symmetry_level": 0.75
      }
    },
    "my_extra_tag": "magic glow",
    "custom_materials": ["silk", "obsidian"]
  },
  "my_global_note": "I love ultra-wide scenes"
}
```

> *Wallgen will auto-flatten all such entries. Any (non-ignored) keys, even arbitrary new fields/nesting, immediately show up as creative context in prompts or sample output, e.g.:*
>
> ...and with magic glow my extra tag that, using custom light mode that, geometry focus: hexagonal_pattern, symmetry level: 0.75, custom materials that, I love ultra-wide scenes my global note that, ...

You can freely add fields without changing code, and all will enhance the AI's creative awareness.

> **Note:** Avoid using reserved names (like `negative_prompt`, which is handled separately), and use human-readable/custom key names for best readability in prompt context.

---

## � Prerequisites

- Python 3.8+
- Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

For complete setup instructions, including installation steps for different operating systems and detailed command-line usage, please refer to the [Installation and CLI Guide](docs/INSTALLATION_AND_CLI_GUIDE.md).

---

## 🧩 System Components

The application is structured as follows:

- **Main Entry Point:** `run_wallgen.py` (Handles CLI args, initialization, orchestration)
- **Core Logic Package:** `wall_gen/`
    - **Services:** `prompt_service.py`, `image_service.py`, `wallpaper_service.py`, `preview_service.py`
    - **Utilities:** `app_utils.py`, `cache_utils.py`, `file_utils.py`, `ui_utils.py`, `image_editor.py`, `graceful_exit.py`
    - **Configuration:** `config.py`
    - **Sub-packages:** `settings_modules/`, `history/`, `prompt_modules/`, `preview_backends/`
- **Root Modules:** `prompt_generator.py` (Facade), `ai_style_generator.py`, `ai_prest_gen/` (Preset Generation CLI/Logic), `no_preferences_prompt.py`
- **Data/Assets:** `presets/`, `genimage/`, `cache/`, `asset/`

---

## ⚡ Quick Usage

After installation, run the application using the new entry point. Run without arguments for the interactive menu:

```bash
python run_wallgen.py
```

### Common Commands

```bash
# Generate with a random prompt
python run_wallgen.py --random

# Generate with a custom prompt
python run_wallgen.py --prompt "mountain landscape at sunset"

# Specify resolution (if supported by your API tier)
python run_wallgen.py --prompt "forest scene" --resolution "1920x1080"
```

**AI Preset Generation:**

```bash
# Generate a new preset based on the "photographic" style
python ai_preset_generator.py generate --style photographic

# List available presets
python ai_preset_generator.py list

# Load a preset by name
python ai_preset_generator.py load cinematic_mood

# Delete a preset by name
python ai_preset_generator.py delete my_abstract_preset
```

**AI Style Generation:**

```bash
# Generate a simple style in the "watercolor" category
python ai_style_generator.py --category watercolor

# Generate a detailed style for the "sci_fi" category
python ai_style_generator.py --category sci_fi --detailed

# Generate a random detailed style and save it to preferences
python ai_style_generator.py --detailed --save
```

---

### Image Preview and Management

```bash
# Preview the latest generated wallpaper
python run_wallgen.py --preview-latest

# Preview a specific image file
python run_wallgen.py --preview-image "genimage/abstract_pattern_87654321.png"

# List all generated images and preview one by number
python run_wallgen.py --list-images

# Generate a wallpaper and immediately set it as desktop background
python run_wallgen.py --prompt "mountain landscape with lakes" --skip-preview
```

For more examples and usage options, see the [Installation and CLI Guide](docs/INSTALLATION_AND_CLI_GUIDE.md).

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
