# User Guide

```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   ██╗   ██╗███████╗███████╗██████╗      ██████╗ ██╗   ██╗██╗██████╗ ███████╗ ║
║   ██║   ██║██╔════╝██╔════╝██╔══██╗    ██╔════╝ ██║   ██║██║██╔══██╗██╔════╝ ║
║   ██║   ██║███████╗█████╗  ██████╔╝    ██║  ███╗██║   ██║██║██║  ██║█████╗   ║
║   ██║   ██║╚════██║██╔══╝  ██╔══██╗    ██║   ██║██║   ██║██║  ██║██╔══╝   ║
║   ╚██████╔╝███████║███████╗██║  ██║    ╚██████╔╝╚██████╔╝██║██████╔╝███████╗ ║
║    ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝     ╚═════╝  ╚═════╝ ╚═╝╚═════╝ ╚══════╝ ║
║                                                                            ║
║   Complete Guide for Wallgen Users                                         ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

## Introduction

Welcome to the user guide for Wallgen, a terminal-based AI wallpaper generator. This guide provides information on using Wallgen, from installation to basic operations. Whether you're a new user or looking to explore Wallgen's capabilities, this guide will help you use the application effectively.

## Table of Contents

- [Installation](#installation)
- [Getting Started](#getting-started)
- [Basic Usage](#basic-usage)
- [Working with Prompts](#working-with-prompts)
- [Managing Generated Images](#managing-generated-images)
- [Basic Settings](#basic-settings)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)

## Installation

### System Requirements

For system requirements and detailed installation instructions, see the [Getting Started Guide](getting-started.md#prerequisites).

### API Key Setup

Wallgen requires a Google Gemini API key to function. See the [Getting Started Guide](getting-started.md#setting-up-api-access) for detailed instructions on obtaining and setting up your API key.

## Getting Started

### First Launch

1. Start Wallgen using:
   ```bash
   python wallgen.py
   ```

2. You'll see the main menu with options for generating wallpapers and browsing generated wallpapers.

### Application Layout

Wallgen uses a simple text-based interface with these components:

- **Menus**: Lists of numbered options
- **Prompts**: Input requests with guidance
- **Messages**: Success, error, and information displays

## Basic Usage

### Generating Your First Wallpaper

1. From the main menu, select **"Generate New Wallpaper"**

2. Choose a generation method:
   - **Random Generation**: Creates wallpaper with a random theme
   - **Custom Prompt**: Allows you to provide a specific prompt

3. If using **Custom Prompt**, enter your description of the desired wallpaper

4. Wait for the API to process your request (typically 10-30 seconds)

5. When complete, you'll see:
   - Preview information
   - Save location

For a step-by-step example of this process, see the [Getting Started Guide](getting-started.md#generating-your-first-wallpaper).

### Viewing Generated Wallpapers

1. From the main menu, select **"Browse Generated Wallpapers"**

2. Navigate using the displayed commands:
   - **Next/Previous**: Move through your collection
   - **View**: Open the current wallpaper in your default image viewer
   - **Delete**: Remove the wallpaper
   - **Back**: Return to main menu

## Working with Prompts

### Prompt Structure

Effective prompts typically include:

- **Subject**: What should be in the image
- **Style**: How it should be rendered
- **Mood/Atmosphere**: The feeling it should evoke

### Example Prompts

Basic prompt:
```
A mountain landscape at sunset
```

Detailed prompt:
```
A majestic mountain range at sunset with golden light illuminating
snow-capped peaks. Digital art style.
```

### Prompt Enhancement

Wallgen automatically enhances your prompts to improve results. This process:

1. Adds technical details
2. Expands descriptive elements
3. Improves style consistency

### Using Negative Prompts

For information on using negative prompts to avoid unwanted elements in your images, see the [Advanced Features Guide](advanced-features.md#negative-prompts).

## Managing Generated Images

### Organization System

All generated wallpapers are saved to the `generated/` directory with a timestamp and theme identifier in the filename.

## Basic Settings

### Resolution Settings

For information on specifying resolution and other settings when generating wallpapers, see the [Quick Reference Guide](QUICK_REFERENCE.md#command-line-options).

## Troubleshooting

For common issues and their solutions, see the comprehensive [Troubleshooting Guide](troubleshooting.md).

## FAQ

For answers to frequently asked questions, see the [FAQ](faq.md).

## See Also

- [Quick Reference Guide](QUICK_REFERENCE.md)
- [Advanced Features Guide](advanced-features.md)
- [Troubleshooting Guide](troubleshooting.md)
- [API Reference](api-reference.md)

---

<div align="center">
<img src="../asset/logo/gemini.svg" alt="Logo" width="64" height="64">

Documentation last updated: 2024-03-25
</div> 