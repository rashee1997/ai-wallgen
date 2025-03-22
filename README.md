# AI Wallpaper Generator 🎨

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

A powerful tool that generates stunning desktop wallpapers using Google's Imagen 3 model via the Gemini API. Create beautiful, personalized wallpapers with advanced customization options and AI-powered prompt generation.

[Installation](#installation) • [Usage](#usage) • [Features](#features) • [Documentation](#documentation)

</div>

## 📋 Menu Structure

```mermaid
graph TD
    A[Main Menu] --> B[Generate AI Wallpaper]
    A --> C[Manage Preferences]
    A --> D[Manage Imagen 3 Settings]
    A --> E[Exit]

    B --> B1[AI-Powered Prompt]
    B --> B2[Random Tag Combination]
    B --> B3[Custom Prompt Input]

    C --> C1[Manage Genres]
    C --> C2[Manage Styles]
    C --> C3[Manage Moods]
    C --> C4[Return]

    D --> D1[Style & Artistic Settings]
    D --> D2[Camera & Technical Settings]
    D --> D3[Lighting & Atmosphere]
    D --> D4[Composition & Environment]
    D --> D5[Color & Detail Settings]
    D --> D6[Show Current Settings]
    D --> D7[Customize All Parameters]
    D --> D8[Return]

    D1 --> D1a[Style Selection]
    D1 --> D1b[Art Movement]
    D1 --> D1c[Post-processing Effects]

    D2 --> D2a[Camera Model]
    D2 --> D2b[Lens Settings]
    D2 --> D2c[Aperture]
    D2 --> D2d[Special Lens]

    D3 --> D3a[Time of Day]
    D3 --> D3b[Lighting Style]
    D3 --> D3c[Light Quality]
    D3 --> D3d[Artificial Sources]

    D4 --> D4a[Composition Technique]
    D4 --> D4b[Camera Angle]
    D4 --> D4c[Perspective]
    D4 --> D4d[Weather & Season]

    D5 --> D5a[Color Scheme]
    D5 --> D5b[Palette Type]
    D5 --> D5c[Color Temperature]
    D5 --> D5d[Detail Level]
```

## ✨ Features

<div align="center">

| Category | Features |
|----------|----------|
| 🤖 **AI Generation** | • Imagen 3 model integration<br>• Gemini API powered<br>• High-quality output<br>• Advanced prompt engineering |
| 🎲 **Generation Modes** | • AI-powered prompts<br>• Random tag combinations<br>• Custom prompt input<br>• Prompt enhancement |
| 🎨 **Style Settings** | • Multiple artistic styles<br>• Art movements<br>• Post-processing effects<br>• Custom style support |
| 📸 **Camera Settings** | • Professional camera models<br>• Lens configurations<br>• Aperture control<br>• Special lens effects |
| 💡 **Lighting & Atmosphere** | • Time of day control<br>• Lighting styles<br>• Light quality<br>• Artificial sources |
| 🖼️ **Composition** | • Rule of thirds<br>• Camera angles<br>• Perspectives<br>• Environmental context |
| 🎯 **Technical Settings** | • Resolution control<br>• Aspect ratio selection<br>• Quality parameters<br>• Detail levels |
| 🌈 **Color & Detail** | • Color schemes<br>• Palette types<br>• Temperature control<br>• Special effects |
| 🌐 **Platforms** | • Windows<br>• macOS<br>• Linux |
| 🔧 **Smart Features** | • Prompt caching<br>• Style preservation<br>• Technical optimization<br>• Error handling |

</div>

### 🎨 Available Styles
- **Photorealistic** - Ultra-realistic photography
- **Digital Art** - Modern digital artwork
- **Sketch** - Hand-drawn illustrations
- **Watercolor** - Artistic watercolor effects
- **Cyberpunk** - Futuristic tech aesthetics
- **Pop Art** - Bold, vibrant designs
- **Oil Painting** - Classic oil painting style
- **Pixel Art** - Retro pixel graphics
- **Anime** - Japanese animation style
- **3D Render** - Computer-generated 3D

### 🎭 Available Art Movements
- **Abstract Expressionism** - Bold, emotional expression
- **Impressionism** - Light and color emphasis
- **Surrealism** - Dreamlike and fantastical
- **Minimalism** - Simple and essential
- **Cubism** - Geometric abstraction
- **Realism** - True-to-life representation
- **Custom** - User-defined movement

### 🌟 Available Moods
- **Peaceful** - Calm and serene
- **Dramatic** - Bold and impactful
- **Mysterious** - Enigmatic and intriguing
- **Energetic** - Dynamic and vibrant
- **Melancholic** - Thoughtful and reflective
- **Joyful** - Bright and cheerful
- **Romantic** - Dreamy and romantic
- **Eerie** - Haunting and atmospheric
- **Nostalgic** - Retro and nostalgic
- **Futuristic** - Sci-fi and modern

### 📸 Camera & Technical Options
- **Camera Models**: ARRI Alexa, RED Digital Cinema, Sony Venice
- **Lens Types**: 50mm, 85mm, 24mm, Custom
- **Aperture Settings**: f/1.8, f/2.8, f/4, f/8
- **Special Lenses**: Tilt-shift, Fisheye, Macro
- **Resolutions**: 8K, 4K, 2K, 1920x1080
- **Aspect Ratios**: 16:9, 21:9, 4:3, 1:1, 9:16

### 💡 Lighting & Atmosphere Options
- **Time of Day**: Golden hour, Blue hour, Twilight
- **Lighting Styles**: Natural, Studio, Dramatic, Ambient
- **Light Quality**: Soft, Hard, Diffused, Directional
- **Artificial Sources**: LED, Neon, Tungsten
- **Weather**: Clear, Cloudy, Rainy, Foggy
- **Seasons**: Spring, Summer, Autumn, Winter

### 🎨 Color & Detail Options
- **Color Schemes**: Monochromatic, Complementary, Analogous
- **Palette Types**: Warm, Cool, Neutral, Vibrant
- **Color Temperature**: Warm, Cool, Neutral
- **Detail Levels**: Ultra-detailed, High-detail, Medium-detail
- **Texture Quality**: High, Medium, Low
- **Special Effects**: Bloom, Glow, Motion blur, Depth of field

## 🚀 Installation

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

## 💻 Usage

### Basic Usage

1. **Run the script**
   ```bash
   python wallpaper_generator.py
   ```

2. **Main Menu Options**
   - 🎨 Generate AI Wallpaper
   - ⚙️ Manage Preferences
   - 🔧 Manage Imagen 3 Settings
   - 🚪 Exit

### Advanced Features

#### 1. Prompt Generation

<div align="center">

| Mode | Features |
|------|----------|
| **Gemini AI** | • Contextual prompts<br>• Mood & style support<br>• Technical parameters<br>• Prompt caching |
| **Random** | • Tag combinations<br>• Theme variety<br>• Curated lists |
| **Custom** | • Manual input<br>• Auto-enhancement<br>• Quality optimization |

</div>

#### 2. Advanced Options

<div align="center">

| Category | Options |
|----------|---------|
| **Style & Artistic** | • Multiple styles<br>• Art movements<br>• Post-processing<br>• Custom styles |
| **Camera & Technical** | • Camera models<br>• Lens settings<br>• Aperture control<br>• Special effects |
| **Lighting & Atmosphere** | • Time of day<br>• Lighting styles<br>• Light quality<br>• Weather & season |
| **Composition & Environment** | • Composition rules<br>• Camera angles<br>• Perspectives<br>• Environmental effects |
| **Color & Detail** | • Color schemes<br>• Palette types<br>• Detail levels<br>• Special effects |

</div>

#### 3. Preferences Management

<div align="center">

| Category | Options |
|----------|---------|
| **Genres** | • 80+ categories<br>• Add/remove<br>• Clear all |
| **Styles** | • 10+ options<br>• Custom styles<br>• Style removal |
| **Moods** | • 10+ options<br>• Mood combinations<br>• Clear moods |

</div>

#### 4. Wallpaper Settings

- **Display Options**
  - Auto-set wallpaper
  - Fit modes (Fill/Fit/Center/Tile)
  - Background color
  - Multi-monitor support

- **Refresh Settings**
  - Daily/Weekly/Monthly/Never
  - Manual refresh
  - Cache duration (1-365 days)

- **Platform Support**
  - Windows 10/11
  - macOS
  - Linux (GNOME/KDE/XFCE/MATE/Cinnamon/i3/Sway)

### ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|---------|
| `Ctrl+C` / `Cmd+C` | Exit program |
| `Enter` | Confirm selection |
| `Backspace` | Previous menu |

## ⚙️ Configuration

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

## 🔧 Troubleshooting

### Common Issues

<div align="center">

| Issue | Solution |
|-------|----------|
| **API Key Missing** | • Check environment variables<br>• Verify API key format |
| **Wallpaper Not Setting** | • Check permissions<br>• Verify compatibility<br>• Confirm file existence |
| **Generation Failures** | • Check internet<br>• Verify API key<br>• Review prompts |
| **Display Issues** | • Check settings<br>• Verify permissions<br>• Test fit modes |

</div>

### Desktop Environment Support

<div align="center">

| Platform | Method |
|----------|---------|
| **Windows** | Windows Desktop API |
| **macOS** | AppleScript |
| **Linux** | Environment-specific commands |

</div>

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini API and Imagen 3 model
- The open-source community for wallpaper setting methods

## 🔄 Changelog

### Version 1.0.0
- Initial release
- AI wallpaper generation with Imagen 3
- Cross-platform support
- User preference management
- Advanced customization options
- Comprehensive menu system
- Enhanced prompt generation
- Detailed technical settings

## 💬 Support

<div align="center">

For support, please:
- Open an issue in the GitHub repository
- Contact the maintainers
- Check the documentation

</div>

---

<div align="center">

Made with ❤️ by [Your Name]

</div>