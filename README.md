# AI Wallpaper Generator 🎨

A powerful Python script that generates stunning desktop wallpapers using Google's Imagen 3 model via the Gemini API. Create unique, high-quality wallpapers tailored to your preferences with advanced customization options.

## ✨ Features

- 🤖 **AI-Powered Generation**: Uses Google's Imagen 3 model through the Gemini API to create unique wallpapers
- 🧠 **Smart Prompt Engineering**: Leverages Gemini AI to generate optimized prompts based on your preferences
- 🎨 **Customization Options**:
  - 📐 Multiple aspect ratios (16:9, 21:9, 4:3, 1:1, 9:16)
  - ✍️ Custom prompts and negative prompts
  - 🎭 Style preferences (photograph, digital art, landscape, etc.)
  - 🌟 Mood settings (peaceful, dramatic, mysterious, etc.)
  - 🎯 Color schemes and lighting styles
- ⚙️ **Advanced Settings**:
  - 🖼️ Multiple image generation (1-4 variations)
  - 🌱 Seed control for reproducible results
  - 🚫 Negative prompts to exclude unwanted elements
- 💾 **Wallpaper Management**:
  - 🖥️ Automatic wallpaper setting for various desktop environments
  - 📺 Multi-monitor support
  - 🎯 Customizable fit modes and background colors
  - ⚡ Configurable refresh rates
- 🌐 **Cross-Platform Support**:
  - 🪟 Windows
  - 🍎 macOS
  - 🐧 Linux (supports GNOME, KDE, XFCE, MATE, Cinnamon, i3, and more)

## 🚀 Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Required Python packages (install via `pip install -r requirements.txt`)

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

3. Set up your environment variables:
   ```bash
   export GEMINI_API_KEY='your-api-key-here'
   ```

## 🎮 Usage

Run the script:
```bash
python wallpaper_generator.py
```

### Main Features

1. 🎨 **Generate AI Wallpaper**
   - 🤖 Use Gemini AI to generate prompts
   - 🎲 Create random prompts
   - ✍️ Enter custom prompts
   - ⚙️ Fine-tune generation parameters

2. ⚙️ **Manage Preferences**
   - 🎭 Configure preferred genres, styles, and moods
   - 🖥️ Set wallpaper display options
   - ⚙️ Customize generation settings

3. 🎯 **Imagen 3 Settings**
   - 🖼️ Configure number of images
   - 🌱 Set random seeds
   - 🚫 Manage negative prompts
   - 📐 Adjust aspect ratios

## ⚙️ Configuration

The script uses several configuration files:
- 📝 `user_preferences.json`: Stores user preferences and settings
- 💭 `prompts.json`: Saves generated prompts for reference
- 🎭 `last_genre.json`: Remembers the last used genre

## 🖥️ Supported Desktop Environments

### Linux
- GNOME
- KDE Plasma
- XFCE
- MATE
- Cinnamon
- i3
- Sway
- Other environments (via fallback methods)

### Windows
- Windows 10/11

### macOS
- All recent versions

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini API and Imagen 3 model
- The open-source community for various wallpaper setting methods

## 🔄 Changelog

### Version 1.0.0
- Initial release
- AI wallpaper generation with Imagen 3
- Cross-platform support
- User preference management
- Advanced customization options

## 💬 Support

For support, please open an issue in the GitHub repository or contact the maintainers. 