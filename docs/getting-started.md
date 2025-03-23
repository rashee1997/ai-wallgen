# Getting Started with Wallgen

```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   ██╗    ██╗ █████╗ ██╗     ██╗      ██████╗ ███████╗███╗   ██╗           ║
║   ██║    ██║██╔══██╗██║     ██║     ██╔════╝ ██╔════╝████╗  ██║           ║
║   ██║ █╗ ██║███████║██║     ██║     ██║  ███╗█████╗  ██╔██╗ ██║           ║
║   ██║███╗██║██╔══██║██║     ██║     ██║   ██║██╔══╝  ██║╚██╗██║           ║
║   ╚███╔███╔╝██║  ██║███████╗███████╗╚██████╔╝███████╗██║ ╚████║           ║
║    ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝           ║
║                                                                            ║
║   Getting Started Guide                                                    ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

## Overview

This guide will help you quickly set up and start using Wallgen, a terminal-based wallpaper generator that uses Google's Imagen 3 and Gemini API to create wallpapers from text prompts. You'll learn how to install the application and generate your first wallpaper.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setting Up API Access](#setting-up-api-access)
- [First Run](#first-run)
- [Generating Your First Wallpaper](#generating-your-first-wallpaper)
- [Basic Commands](#basic-commands)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have the following:

- **Python 3.8+** installed on your system
- **pip** (Python package manager)
- A **Google Gemini API key** (obtain from [Google AI Studio](https://makersuite.google.com/app/apikey))
- Internet connection for API communication

## Installation

### Linux/macOS

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/wallgen.git
   cd wallgen
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Windows

1. Clone the repository:
   ```powershell
   git clone https://github.com/yourusername/wallgen.git
   cd wallgen
   ```

2. Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Setting Up API Access

Wallgen requires a Google Gemini API key to function:

1. Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

2. Set the API key as an environment variable:

   **Linux/macOS**:
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```

   **Windows (PowerShell)**:
   ```powershell
   $env:GEMINI_API_KEY="your_api_key_here"
   ```

   **Windows (Command Prompt)**:
   ```
   set GEMINI_API_KEY=your_api_key_here
   ```

3. Alternatively, you can create a `.env` file in the project root with the content:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## First Run

1. Start the application:
   ```bash
   python wallgen.py
   ```

2. You'll see the main menu with options for generating wallpapers and browsing generated wallpapers.

## Generating Your First Wallpaper

Let's create your first AI-generated wallpaper:

1. From the main menu, select **"Generate New Wallpaper"**

2. Choose a generation method:
   - **Random Generation**: Creates a wallpaper with a randomly generated theme
   - **Custom Prompt**: Allows you to write your own prompt

3. If you select **"Custom Prompt"**, enter a description of what you want to see. For tips on creating effective prompts, see the [FAQ section on prompt creation](faq.md#can-i-use-negative-prompts).

4. Wait for the API to process your request (typically 10-30 seconds)

5. When generation completes, your new wallpaper will be saved to the `generated/` directory

### Example Session

```
===============================================
       Wallgen - AI Wallpaper Generator       
===============================================

Main Menu
---------
  1: Generate New Wallpaper
  2: Browse Generated Wallpapers
  3: Exit

> Select an option 1

Generation Method
----------------
  1: Random Generation
  2: Custom Prompt

> Select an option 2

Enter your prompt:
> A mountain landscape at sunset with pine trees

⠋ Generating your wallpaper...
⠙ Generating your wallpaper...
⠹ Generating your wallpaper...

✓ Wallpaper generated successfully!
✓ Saved to: generated/mountain_landscape_20240325_123456.png

> Return to main menu? (Y/n) Y
```

## Basic Commands

For detailed command-line options and examples, see the [Quick Reference Guide](QUICK_REFERENCE.md#command-line-options).

Here are some basic commands to get you started:

```bash
# Generate with a custom prompt
python wallgen.py --prompt "mountain landscape at sunset"

# Generate with a random prompt
python wallgen.py --random

# Show help
python wallgen.py --help
```

## Troubleshooting

For a comprehensive list of common issues and solutions, see the [Troubleshooting Guide](troubleshooting.md).

### Common Issues

#### API Key Issues

**Problem**: Error message about invalid API key
**Solution**: Double-check that you've correctly set the API key in environment variables or the `.env` file

#### Connection Problems

**Problem**: "Failed to connect to API" error
**Solution**: 
1. Check your internet connection
2. Verify that the Gemini API service is available
3. Ensure your API key has not expired

#### Generation Failures

**Problem**: Image generation fails
**Solution**:
1. Try a simpler prompt
2. Check if you've hit API rate limits
3. Verify your API key permissions include image generation

### Getting Help

If you encounter issues not covered here:

1. Check the [Troubleshooting Guide](troubleshooting.md) for more detailed solutions
2. If problems persist, please report issues on the GitHub repository

---

<div align="center">
<img src="../asset/logo/gemini.svg" alt="Logo" width="64" height="64">

Documentation last updated: 2024-03-25
</div> 