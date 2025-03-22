# AI Wallpaper Generator 🎨

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A powerful tool for generating stunning AI wallpapers using Google's Imagen 3 model via the Gemini API. Create beautiful, customized desktop wallpapers with advanced artistic and technical controls.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation)

</div>

## ✨ Features

<div align="center">
  <img src="docs/features.png" alt="AI Wallpaper Generator Features" width="800">
</div>

* **🤖 AI Generation:**
    * Powered by Google's Imagen 3 model via Gemini API
    * Multiple prompt generation methods:
        * AI-powered prompts (Gemini)
        * Random tag combinations
        * Custom prompt input
        * Enhanced prompts with user preferences
* **🎲 Generation Modes:**
    * AI Generation with Gemini
    * Random Tag Generation
    * Custom Prompt Generation
    * Advanced Options for fine-tuning
* **🎨 Style Settings:**
    * Multiple artistic styles:
        * Photorealistic, Digital Art, Sketch, Watercolor, Cyberpunk, Pop Art, Oil Painting, Pixel Art, Anime, 3D Render
    * Art movements:
        * Abstract Expressionism, Impressionism, Surrealism, Minimalism, Cubism
    * Post-processing effects
    * Custom style options
* **📸 Camera & Technical Settings:**
    * Camera models: ARRI Alexa, RED Digital Cinema, Sony Venice, Custom options
    * Lens options: 50mm, 85mm, 24mm, Special lenses (tilt-shift, fisheye, macro)
    * Aperture settings
    * Depth of field control
    * Resolution options (up to 8K)
* **💡 Lighting & Atmosphere:**
    * Time of day settings
    * Lighting styles: Natural, Studio, Dramatic, Soft, Harsh, Volumetric
    * Light quality options
    * Artificial light sources
    * Weather conditions, Seasonal effects, Atmospheric effects
* **🖼️ Composition & Environment:**
    * Composition techniques: Rule of thirds, Leading lines, Framing, Symmetry, Asymmetry
    * Camera angles, Perspective options
    * Weather conditions, Seasonal settings, Atmospheric effects
* **🎯 Color & Detail Settings:**
    * Color schemes: Natural, Warm, Cool, Monochromatic, Vibrant, Pastel
    * Palette types: Analogous, Complementary, Triadic, Split Complementary
    * Color temperature, Texture quality, Special effects, Detail levels
* **⚡ Quality Settings:**
    * Resolution options: 1920x1080 (Full HD), 2560x1440 (2K), 3840x2160 (4K), 5120x2880 (5K), 7680x4320 (8K)
    * Detail levels, Rendering quality, Texture quality
* **🖥️ Wallpaper Management:**
    * Auto-setting wallpaper
    * Cache management
    * Multi-monitor support: Mirror mode, Extend mode, Individual mode
    * Fit modes: Fill, Fit, Center, Tile
    * Background color options, Refresh rate settings: Daily, Weekly, Monthly, Never

## 🚀 Installation

### Prerequisites

* Python 3.8 or higher
* UV package manager (recommended) or pip
* Git

### Quick Start

1. **Clone the repository:**

    ```bash
    git clone https://github.com/rashee1997/wallgen.git
    cd wallgen
    ```

2. **Set up UV package manager (recommended):**

    ```bash
    # Install UV
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Create and activate virtual environment
    uv venv
    source .venv/bin/activate  # On Unix/macOS
    # or
    .venv\Scripts\activate  # On Windows
    ```

3. **Install dependencies:**

    ```bash
    # Using UV (recommended)
    uv pip install -r requirements.txt

    # Or using pip
    pip install -r requirements.txt
    ```

4. **Set up API key:**

    ```bash
    # On Unix/macOS
    export GEMINI_API_KEY='your-api-key-here'

    # On Windows (PowerShell)
    $env:GEMINI_API_KEY='your-api-key-here'
    ```

### Alternative Installation Methods

#### Using pip with venv

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

#### Using Poetry

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

## 💻 Usage

1. **Run the script:**

    ```bash
    python wallpaper_generator.py
    ```

2. **Main Menu Options:**

    * Generate Wallpaper
    * Settings & Preferences
    * Wallpaper Management
    * Help & Information
    * Exit

## 📋 Menu Structure

<details>
<summary>Click to expand menu structure</summary>

### Main Menu
1. **Generate AI Wallpaper**
   - Use Gemini AI to generate a prompt
   - Use a random prompt
   - Enter your own custom prompt
   - Advanced Options - Fine-tune generation parameters
   - Return to Main Menu

2. **Manage Preferences**
   - Manage Genres
   - Manage Styles
   - Manage Moods
   - Manage Wallpaper Settings
     - Auto-set wallpaper
     - Cache duration
     - Fit mode (Fill, Fit, Center, Tile)
     - Background color
     - Multi-monitor mode (Mirror, Extend, Individual)
     - Refresh rate (Daily, Weekly, Monthly, Never)
   - View Current Preferences
   - Reset to Defaults
   - Return to Main Menu

3. **Exit**
   - Save and exit

### Advanced Options Menu
1. **Style & Artistic Settings**
   - Style Selection
     - Photorealistic
     - Digital Art
     - Sketch
     - Watercolor
     - Cyberpunk
     - Pop Art
     - Oil Painting
     - Pixel Art
     - Anime
     - 3D Render
     - Custom Style
   - Art Movement
     - Abstract Expressionism
     - Impressionism
     - Surrealism
     - Minimalism
     - Cubism
     - Custom
   - Post-processing Effects

2. **Camera & Technical Settings**
   - Camera Model
   - Lens Options
   - Aperture Settings
   - Depth of Field
   - Resolution

3. **Lighting & Atmosphere**
   - Time of Day
   - Lighting Style
   - Light Quality
   - Weather Conditions
   - Atmospheric Effects

4. **Composition & Environment**
   - Composition Technique
     - Rule of Thirds
     - Leading Lines
     - Framing
     - Symmetry
     - Asymmetry
     - Custom
   - Camera Angle
   - Perspective
   - Weather
     - Clear
     - Cloudy
     - Rainy
     - Snowy
     - Foggy
     - Custom
   - Season
     - Spring
     - Summer
     - Autumn
     - Winter
     - Custom
   - Atmospheric Effects

5. **Color & Detail Settings**
   - Color Scheme
     - Natural
     - Warm
     - Cool
     - Monochromatic
     - Vibrant
     - Pastel
     - Custom
   - Color Palette
     - Analogous
     - Complementary
     - Triadic
     - Split Complementary
     - Custom
   - Color Temperature
   - Texture Quality
   - Special Effects

6. **Show Current Settings**
7. **Customize All Parameters**
8. **Return to previous menu**

### Optional Parameters for Generation
- Mood Options:
  - Peaceful
  - Dramatic
  - Mysterious
  - Energetic
  - Melancholic
  - Joyful
  - Romantic
  - Eerie
  - Nostalgic
  - Contemplative

- Style Options:
  - Photograph
  - Digital Art
  - Landscape
  - Sketch
  - Watercolor
  - Cyberpunk
  - Pop Art

- Additional Parameters:
  - Resolution
  - Color Scheme
  - Lighting
</details>

## ⚙️ Configuration

### User Preferences

Preferences are stored in `user_preferences.json`:

```json
{
  "preferred_genres": [],
  "preferred_styles": [],
  "preferred_moods": [],
  "aspect_ratio": "16:9",
  "negative_prompts": [],
  "imagen_settings": {
    "number_of_images": 1,
    "seed": null,
    "aspect_ratio": "16:9",
    "negative_prompt": "",
    "camera_settings": {
      "camera_model": "ARRI Alexa",
      "lens_type": "50mm",
      "aperture": "f/2.8",
      "special_lens": null
    },
    "lighting_settings": {
      "time_of_day": "golden_hour",
      "lighting_style": "natural",
      "light_quality": "soft",
      "artificial_sources": []
    },
    "composition_settings": {
      "technique": "rule_of_thirds",
      "camera_angle": "eye_level",
      "perspective": "wide"
    },
    "environment_settings": {
      "weather": "clear",
      "season": "summer",
      "atmospheric_effects": []
    },
    "style_settings": {
      "overall_style": "vintage",
      "post_processing": [],
      "art_movement": "Abstract Expressionism"
    },
    "detail_settings": {
      "detail_level": "ultra_detailed",
      "texture_quality": "high",
      "special_effects": []
    },
    "color_settings": {
      "color_scheme": "natural",
      "palette_type": "analogous",
      "color_temperature": "neutral"
    },
    "quality_settings": {
      "resolution": "8k",
      "detail_level": "ultra_detailed",
      "rendering_quality": "photorealistic"
    }
  },
  "wallpaper_settings": {
    "auto_set": true,
    "cache_duration": 30,
    "fit_mode": "fill",
    "background_color": "#000000",
    "multi_monitor": "mirror",
    "refresh_rate": "daily",
    "last_refresh": null
  }
}
```

## 🔧 Troubleshooting

### Common Issues

* **API Key Missing:**
    * Check environment variables
    * Verify API key format
* **Wallpaper Not Setting:**
    * Check permissions
    * Verify compatibility
    * Confirm file existence
* **Generation Failures:**
    * Check internet
    * Verify API key
    * Review prompts
* **Display Issues:**
    * Check settings
    * Verify permissions
    * Test fit modes

### Desktop Environment Support

* **Windows:** Windows Desktop API
* **macOS:** AppleScript
* **Linux:** Environment-specific commands

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

* Google Gemini API and Imagen 3 model
* The open-source community for wallpaper setting methods

## 🔄 Changelog

### Version 1.0.0

* Initial release
* AI wallpaper generation with Imagen 3
* Cross-platform support
* User preference management
* Advanced customization options
* Comprehensive menu system
* Enhanced prompt generation
* Detailed technical settings

## 💬 Support

For support, please:

* Open an issue in the GitHub repository
* Contact the maintainers
* Check the documentation

---

<div align="center">
Made with ❤️ by [rasheedh]
</div>