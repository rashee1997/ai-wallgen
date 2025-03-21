# AI Wallpaper Generator 🎨

A powerful command-line tool that generates and sets beautiful wallpapers using AI generation (via Google's Imagen 3) and popular image providers like Unsplash and Pexels.

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

## 🚀 Prerequisites

- Python 3.8 or higher
- Required packages:
  - `google-generativeai>=0.3.0`
  - `requests>=2.31.0`
  - `bleach>=6.1.0`
  - `colorama>=0.4.6`
  - `pillow>=10.0.0`
  - `absl-py>=2.0.0`

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/wallgen.git
cd wallgen
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables for API keys:
```bash
export GEMINI_API_KEY="your_gemini_api_key"
export UNSPLASH_ACCESS_KEY="your_unsplash_key"  # Optional
export PEXELS_API_KEY="your_pexels_key"        # Optional
```

## 🎮 Usage

Run the script:
```bash
python wallpaper_generator.py
```

### Main Menu Options:

1. **Generate Wallpaper**: Create a new wallpaper using AI or fetch from providers
   - Choose source (AI Generation/Unsplash/Pexels)
   - Select prompt type (Gemini AI/Random/Custom)
   - Customize mood and style
   - Set aspect ratio

2. **Manage Preferences**: Configure your preferences
   - Set preferred genres
   - Define preferred styles
   - Specify preferred moods
   - Add negative prompts
   - Choose default aspect ratio

3. **Exit**: Close the application

## 🎨 Advanced Features

### Prompt Generation
- **Gemini AI**: Smart context-aware prompts
- **Random**: Generated from predefined tags
- **Custom**: Your own creative prompts

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
- and more...

## ⚙️ Configuration

User preferences are stored in `~/.config/wallgen/preferences.json` and include:
- Preferred genres
- Preferred styles
- Preferred moods
- Negative prompts
- Default aspect ratio

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