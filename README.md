# AI Wallpaper Generator 🎨

A powerful Python script that generates stunning desktop wallpapers using Google's Imagen 3 model via the Gemini API, or fetches high-quality images from Unsplash and Pexels.

## ✨ Features

- 🤖 AI-powered wallpaper generation using Google's Imagen 3 model
- 🎯 Smart prompt generation with Gemini AI
- 🖼️ High-quality images from Unsplash and Pexels
- 🎨 Customizable styles and moods
- 📐 Support for various aspect ratios
- 💾 Smart caching system for generated images
- 🔄 Cross-platform wallpaper setting (Windows, macOS, Linux)
- 🎯 User preference management
- 🔒 Secure API key handling
- 🎨 Style Support:
  - photograph
  - digital_art
  - landscape
  - sketch
  - watercolor
  - cyberpunk
  - pop_art
- 🎨 Mood Selection:
  - peaceful
  - dramatic
  - mysterious
  - energetic
  - melancholic
  - joyful
  - romantic
  - eerie
  - nostalgic
  - contemplative
- 🎨 Advanced Customization:
  - Aspect ratio selection (16:9, 21:9, 4:3, 1:1, 9:16)
  - Color palette options
  - Lighting style selection
  - Negative prompts
  - Random seed for reproducibility

## 🚀 Prerequisites

- Python 3.7+
- Google Cloud API key for Gemini
- Optional: Unsplash and Pexels API keys for additional image sources
- Required Python packages:
  - google-generativeai
  - requests
  - pillow
  - colorama (optional, for colored terminal output)
  - bleach (optional, for prompt sanitization)

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/rashee1997/wallgen.git
cd wallgen
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables for API keys:
```bash
export GEMINI_API_KEY="your-gemini-api-key"
export UNSPLASH_ACCESS_KEY="your-unsplash-access-key"  # Optional
export PEXELS_API_KEY="your-pexels-api-key"        # Optional
```

## 🎮 Usage

Run the script:
```bash
python wallpaper_generator.py
```

### Main Menu Options:

1. **Generate AI Wallpaper**: Create a new wallpaper using AI or fetch from providers
   - Choose source (AI Generation/Unsplash/Pexels)
   - Select prompt type (Gemini AI/Random/Custom)
   - Customize mood and style
   - Set aspect ratio

2. **Fetch Wallpaper**: Get wallpapers from Unsplash/Pexels

3. **Manage Preferences**: Configure your preferences
   - Set preferred genres
   - Define preferred styles
   - Specify preferred moods
   - Add negative prompts
   - Choose default aspect ratio
   - Set cache duration
   - Configure multi-monitor settings

4. **Manage Imagen 3 Settings**: Configure number of images

5. **Exit**: Close the application

## 🎨 Advanced Features

### Prompt Generation
- **Gemini AI**: Smart context-aware prompts
- **Random**: Generated from predefined tags
- **Custom**: Your own creative prompts
- **AI-enhanced custom prompts**:
  - Style-specific generation
  - Mood-based generation
  - Negative prompt support

### Image Sources
- **AI Generation**: Using Google's Imagen 3
- **Unsplash**: High-quality free photos
- **Pexels**: Professional stock images

### Supported Aspect Ratios
- 16:9 (Widescreen)
- 21:9 (Ultrawide)
- 4:3 (Standard)
- 1:1 (Square)
- 9:16 (Portrait)

### Linux Desktop Environments
- GNOME
- KDE Plasma
- XFCE
- MATE
- Cinnamon
- i3
- Sway
- and more...

## ⚙️ Configuration

User preferences are stored in `~/.config/wallgen/preferences.json` and include:
- Preferred genres
- Preferred styles
- Preferred moods
- Negative prompts
- Default aspect ratio
- Cache duration
- Multi-monitor settings

## 🔒 Security

- API keys are securely handled via environment variables
- Image caching with proper permissions
- Input sanitization for prompts
- Secure HTTP requests

## 🚀 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google's Imagen 3 and Gemini AI
- Unsplash API
- Pexels API
- Open source community

## 🔄 Changelog

### Version 1.0.0
- Initial release
- AI wallpaper generation
- Image provider integration
- Cross-platform support
- User preference management
- Caching system

## 🤝 Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## 🛣️ Roadmap

- [ ] Support for additional AI models
- [ ] Enhanced prompt generation
- [ ] More image providers
- [ ] Advanced filtering options
- [ ] Batch processing
- [ ] Custom resolution support
- [ ] Image editing features
- [ ] Theme-based generation
- [ ] Schedule-based wallpaper changes
- [ ] Community prompt sharing

## 🎨 Wallpaper Settings

- **Auto-set wallpaper option**: Automatically set the wallpaper on the desktop
- **Multiple fit modes**:
  - Fill
  - Fit
  - Center
  - Tile
- **Background color customization**: Customize the background color of the wallpaper
- **Multi-monitor support**: Apply the wallpaper to multiple monitors
- **Configurable refresh rates**: Set the refresh rate for the wallpaper 