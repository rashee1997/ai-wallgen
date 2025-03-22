# AI Wallpaper Generator 🎨

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

A powerful tool for generating stunning AI wallpapers using Google's Imagen 3 model via the Gemini API. Create beautiful, customized desktop wallpapers with advanced artistic and technical controls.

[Installation](#installation) • [Usage](#usage) • [Features](#features) • [Documentation](#documentation)

</div>

## ✨ Features

<div align="center">

### 🤖 AI Generation
<table>
<tr>
<td>

- Powered by Google's Imagen 3 model via Gemini API
- Multiple prompt generation methods:
  - AI-powered prompts (Gemini)
  - Random tag combinations
  - Custom prompt input
  - Enhanced prompts with user preferences

</td>
</tr>
</table>

### 🎲 Generation Modes
<table>
<tr>
<td>

- AI Generation with Gemini
- Random Tag Generation
- Custom Prompt Generation
- Advanced Options for fine-tuning

</td>
</tr>
</table>

### 🎨 Style Settings
<table>
<tr>
<td>

- Multiple artistic styles:
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
- Art movements:
  - Abstract Expressionism
  - Impressionism
  - Surrealism
  - Minimalism
  - Cubism
- Post-processing effects
- Custom style options

</td>
</tr>
</table>

### 📸 Camera & Technical Settings
<table>
<tr>
<td>

- Camera models:
  - ARRI Alexa
  - RED Digital Cinema
  - Sony Venice
  - Custom options
- Lens options:
  - 50mm
  - 85mm
  - 24mm
  - Special lenses (tilt-shift, fisheye, macro)
- Aperture settings
- Depth of field control
- Resolution options (up to 8K)

</td>
</tr>
</table>

### 💡 Lighting & Atmosphere
<table>
<tr>
<td>

- Time of day settings
- Lighting styles:
  - Natural
  - Studio
  - Dramatic
  - Soft
  - Harsh
  - Volumetric
- Light quality options
- Artificial light sources
- Weather conditions
- Seasonal effects
- Atmospheric effects

</td>
</tr>
</table>

### 🖼️ Composition & Environment
<table>
<tr>
<td>

- Composition techniques:
  - Rule of thirds
  - Leading lines
  - Framing
  - Symmetry
  - Asymmetry
- Camera angles
- Perspective options
- Weather conditions
- Seasonal settings
- Atmospheric effects

</td>
</tr>
</table>

### 🎯 Color & Detail Settings
<table>
<tr>
<td>

- Color schemes:
  - Natural
  - Warm
  - Cool
  - Monochromatic
  - Vibrant
  - Pastel
- Palette types:
  - Analogous
  - Complementary
  - Triadic
  - Split Complementary
- Color temperature
- Texture quality
- Special effects
- Detail levels

</td>
</tr>
</table>

### ⚡ Quality Settings
<table>
<tr>
<td>

- Resolution options:
  - 1920x1080 (Full HD)
  - 2560x1440 (2K)
  - 3840x2160 (4K)
  - 5120x2880 (5K)
  - 7680x4320 (8K)
- Detail levels
- Rendering quality
- Texture quality

</td>
</tr>
</table>

### 🖥️ Wallpaper Management
<table>
<tr>
<td>

- Auto-setting wallpaper
- Cache management
- Multi-monitor support:
  - Mirror mode
  - Extend mode
  - Individual mode
- Fit modes:
  - Fill
  - Fit
  - Center
  - Tile
- Background color options
- Refresh rate settings:
  - Daily
  - Weekly
  - Monthly
  - Never

</td>
</tr>
</table>

</div>

## 📋 Menu Structure

```mermaid
graph TD
    %% Main Menu
    A[Main Menu] --> B[Generate AI Wallpaper]
    A --> C[Manage Preferences]
    A --> D[Manage Imagen 3 Settings]
    A --> E[Exit]

    %% Generate AI Wallpaper Submenu
    B --> F[Use Gemini AI]
    B --> G[Use Random Prompt]
    B --> H[Custom Prompt]
    B --> I[Advanced Options]

    %% Manage Preferences Submenu
    C --> J[Manage Genres]
    C --> K[Manage Styles]
    C --> L[Manage Moods]
    C --> M[Manage Wallpaper Settings]
    C --> N[View Current Preferences]
    C --> O[Reset to Defaults]

    %% Manage Imagen 3 Settings Submenu
    D --> P[Style & Artistic Settings]
    D --> Q[Camera & Technical Settings]
    D --> R[Lighting & Atmosphere]
    D --> S[Composition & Environment]
    D --> T[Color & Detail Settings]
    D --> U[Show Current Settings]
    D --> V[Customize All Parameters]

    %% Styling
    classDef mainMenu fill:#f9f,stroke:#333,stroke-width:2px
    classDef subMenu fill:#bbf,stroke:#333,stroke-width:2px
    classDef option fill:#dfd,stroke:#333,stroke-width:1px

    class A mainMenu
    class B,C,D mainMenu
    class F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V option
```

<div align="center">

<table>
<tr>
<td>

### Menu Navigation Guide

| Menu Level | Description |
|------------|-------------|
| **Main Menu** | Primary navigation hub |
| **Generate AI Wallpaper** | Create new wallpapers |
| **Manage Preferences** | Customize user settings |
| **Manage Imagen 3 Settings** | Configure generation parameters |

</td>
</tr>
</table>

</div>

## 🚀 Installation

<div align="center">

<table>
<tr>
<td>

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/wallgen.git
   cd wallgen
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API key**
   ```bash
   export GEMINI_API_KEY='your-api-key-here'
   ```

</td>
</tr>
</table>

</div>

## 💻 Usage

<div align="center">

<table>
<tr>
<td>

1. **Run the script**
   ```bash
   python wallpaper_generator.py
   ```

2. **Main Menu Options**
   - 🎨 Generate AI Wallpaper
   - ⚙️ Manage Preferences
   - 🔧 Manage Imagen 3 Settings
   - 🚪 Exit

</td>
</tr>
</table>

</div>

## ⚙️ Configuration

<div align="center">

<table>
<tr>
<td>

### User Preferences

Preferences are stored in `user_preferences.json`:

<details>
<summary>View Configuration</summary>

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

</details>

### Cache Management

- 📁 Generated images in `genimage` directory
- ⏱️ Configurable cache duration (1-365 days)
- 🧹 Automatic cache cleanup
- 💾 Prompt caching for efficiency

</td>
</tr>
</table>

</div>

## 🔧 Troubleshooting

<div align="center">

<table>
<tr>
<td>

### Common Issues

| Issue | Solution |
|-------|----------|
| **API Key Missing** | • Check environment variables<br>• Verify API key format |
| **Wallpaper Not Setting** | • Check permissions<br>• Verify compatibility<br>• Confirm file existence |
| **Generation Failures** | • Check internet<br>• Verify API key<br>• Review prompts |
| **Display Issues** | • Check settings<br>• Verify permissions<br>• Test fit modes |

### Desktop Environment Support

| Platform | Method |
|----------|---------|
| **Windows** | Windows Desktop API |
| **macOS** | AppleScript |
| **Linux** | Environment-specific commands |

</td>
</tr>
</table>

</div>

## 🤝 Contributing

<div align="center">

<table>
<tr>
<td>

Contributions are welcome! Please feel free to submit a Pull Request.

</td>
</tr>
</table>

</div>

## 📄 License

<div align="center">

<table>
<tr>
<td>

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

</td>
</tr>
</table>

</div>

## 🙏 Acknowledgments

<div align="center">

<table>
<tr>
<td>

- Google Gemini API and Imagen 3 model
- The open-source community for wallpaper setting methods

</td>
</tr>
</table>

</div>

## 🔄 Changelog

<div align="center">

<table>
<tr>
<td>

### Version 1.0.0
- Initial release
- AI wallpaper generation with Imagen 3
- Cross-platform support
- User preference management
- Advanced customization options
- Comprehensive menu system
- Enhanced prompt generation
- Detailed technical settings

</td>
</tr>
</table>

</div>

## 💬 Support

<div align="center">

<table>
<tr>
<td>

For support, please:
- Open an issue in the GitHub repository
- Contact the maintainers
- Check the documentation

</td>
</tr>
</table>

</div>

---

<div align="center">

Made with ❤️ by [Your Name]

</div>