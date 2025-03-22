# 🎨 AI Wallpaper Generator

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Gemini API](https://img.shields.io/badge/Gemini%20API-Enabled-blue)](https://ai.google.dev/)

A powerful and intuitive tool for generating stunning AI wallpapers using Google's Imagen 3 model via the Gemini API. Create beautiful, customized desktop wallpapers with advanced artistic and technical controls.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation)

</div>

## ✨ Features

### 🤖 AI Generation
- Powered by Google's Imagen 3 model via Gemini API
- Multiple prompt generation methods:
  - AI-powered prompts (Gemini)
  - Pre-defined genre-based prompts (Nature, Space, Sea, Flowers, Urban, Fantasy, Abstract)
  - Random tag combinations from curated lists
  - Custom prompt input with style guidance
  - Enhanced prompts with user preferences

### 🎨 Artistic Controls
- **Style Settings:**
  - Multiple artistic styles (Photorealistic, Digital Art, Sketch, etc.)
  - Art movements (Abstract Expressionism, Impressionism, etc.)
  - Post-processing effects
- **Color & Detail:**
  - Color schemes (Natural, Warm, Cool, etc.)
  - Palette types (Analogous, Complementary, etc.)
  - Detail levels and texture quality

### 📸 Technical Features
- **Camera & Resolution:**
  - Professional camera models (ARRI Alexa, RED, Sony Venice)
  - Lens options (50mm, 85mm, 24mm, Special lenses)
  - Resolution options up to 8K
- **Lighting & Atmosphere:**
  - Time of day settings
  - Lighting styles (Natural, Studio, Dramatic)
  - Weather conditions and seasonal effects

### 🖥️ Wallpaper Management
- Auto-setting wallpaper with system integration
- Intelligent caching system for generated images
- Multi-monitor support
- Custom fit modes
- Background color options
- Refresh rate settings

### 💾 System Features
- Persistent user preferences
- Intelligent prompt caching
- Genre-based prompt generation
- Comprehensive logging system
- Cross-platform compatibility

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- UV package manager (recommended) or pip
- Git
- Gemini API key

### Getting Your Gemini API Key

1. **Visit Google AI Studio:**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account

2. **Create API Key:**
   - Click on "Get API key" button
   - If you don't have an API key, click "Create API key"
   - Copy your API key immediately (you won't be able to see it again)

3. **Set Up API Key:**
   ```bash
   # On Unix/macOS
   export GEMINI_API_KEY='your-api-key-here'

   # On Windows (PowerShell)
   $env:GEMINI_API_KEY='your-api-key-here'
   ```

   > ⚠️ **Important:** Never commit your API key to version control. Keep it secure and private.

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rashee1997/wallgen.git
   cd wallgen
   ```

2. **Set up virtual environment:**
   ```bash
   # Using UV (recommended)
   uv venv
   source .venv/bin/activate  # On Unix/macOS
   # or
   .venv\Scripts\activate  # On Windows

   # Or using pip
   python -m venv .venv
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

## 💻 Usage

1. **Run the script:**
   ```bash
   python wallpaper_generator.py
   ```

2. **Main Menu Options:**
   - Generate Wallpaper
   - Settings & Preferences
   - Wallpaper Management
   - Help & Information
   - Exit

## 📁 Project Structure

```
wallgen/
├── wallpaper_generator.py    # Main application script
├── wallpaper_config.py      # Wallpaper generation configuration
├── prompt_config.py         # Prompt generation settings
├── requirements.txt         # Project dependencies
├── user_preferences.json    # User settings storage
├── prompts.json            # Pre-defined prompts database
├── cache/                  # Generated image cache
├── prompt_cache/          # Prompt generation cache
└── genimage/              # Generated image storage
```

## 📋 Advanced Features

### Prompt Generation System
- Genre-based prompt templates
- Dynamic tag combination
- AI-enhanced prompt refinement
- Custom prompt validation
- Prompt history tracking

### User Preferences
- Persistent settings storage
- Customizable default options
- Genre preferences
- Style preferences
- Technical preferences

### Caching System
- Intelligent image caching
- Prompt generation caching
- Cache management tools
- Automatic cache cleanup
- Cache statistics

### Error Handling
- Comprehensive logging
- Graceful error recovery
- User-friendly error messages
- Debug mode support
- System compatibility checks

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google's Gemini API and Imagen 3 model for AI image generation
- The open-source community for various tools and libraries
- All contributors to this project
- Special thanks to the Python community for the excellent libraries used in this project

---

<div align="center">
Made with ❤️ by [Rasheed](https://github.com/rashee1997)
</div>