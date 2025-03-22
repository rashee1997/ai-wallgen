# Getting Started with AI Wallpaper Generator

This guide will help you get up and running with the AI Wallpaper Generator quickly.

## Prerequisites

Before you begin, ensure you have:
- Python 3.8 or higher installed
- UV package manager (recommended) or pip
- Git installed
- A Gemini API key

## Quick Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/rashee1997/wallgen.git
   cd wallgen
   ```

2. **Set Up Virtual Environment**
   ```bash
   # Using UV (recommended)
   uv venv
   source .venv/bin/activate  # On Unix/macOS
   # or
   .venv\Scripts\activate  # On Windows
   ```

3. **Install Dependencies**
   ```bash
   uv pip install -r requirements.txt
   ```

4. **Configure API Key**
   ```bash
   # On Unix/macOS
   export GEMINI_API_KEY='your-api-key-here'

   # On Windows (PowerShell)
   $env:GEMINI_API_KEY='your-api-key-here'
   ```

## Basic Usage

1. **Start the Application**
   ```bash
   python wallpaper_generator.py
   ```

2. **Generate Your First Wallpaper**
   - Select "Generate AI Wallpaper" from the main menu
   - Choose a generation method:
     - Use Gemini AI for smart prompts
     - Use random prompts for quick results
     - Enter your own custom prompt
   - Wait for the generation to complete
   - Your wallpaper will be saved in the `genimage` directory

## Next Steps

- Read the [Prompt Engineering Guide](prompt-engineering.md) to create better prompts
- Check out [Advanced Features](advanced-features.md) for more options
- Learn about [API Best Practices](api-best-practices.md)
- Review [Common Issues](troubleshooting.md) if you encounter problems

## Need Help?

- Check our [FAQ](faq.md) for common questions
- Review [Troubleshooting](troubleshooting.md) for solutions
- Open an issue on GitHub for additional support 