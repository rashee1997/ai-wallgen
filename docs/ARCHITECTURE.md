# Wallgen Architecture

```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║    █████╗ ██████╗ ██╗   ██╗ ██████╗███████╗██████╗ ██╗   ██╗ ██████╗ ███████╗ ║
║   ██╔══██╗██╔══██╗██║   ██║██╔════╝██╔════╝██╔══██╗██║   ██║██╔═══██╗██╔════╝ ║
║   ███████║██████╔╝██║   ██║██║     █████╗  ██████╔╝██║   ██║██║   ██║█████╗   ║
║   ██╔══██║██╔══██╗██║   ██║██║     ██╔══╝  ██╔══██╗██║   ██║██║   ██║██╔══╝   ║
║   ██║  ██║██║  ██║╚██████╔╝╚██████╗███████╗██║  ██║╚██████╔╝╚██████╔╝███████╗ ║
║   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝ ║
║                                                                            ║
║   System Architecture of Wallgen                                           ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

## Overview

This document describes the architecture and system design of the Wallgen project. It provides a comprehensive overview of the components, their interactions, and the overall data flow of the wallpaper generation system.

## Table of Contents

- [System Components](#system-components)
- [Component Interactions](#component-interactions)
- [Data Flow](#data-flow)
- [Key Classes and Interfaces](#key-classes-and-interfaces)
- [Implementation Details](#implementation-details)
- [See Also](#see-also)

## System Components

The Wallgen application is structured into the following primary components:

1. **Core Generator** - Primary wallpaper generation logic
2. **Settings Management** - User preferences and configuration
3. **UI Utilities** - Terminal interface elements
4. **File Management** - Image storage and organization
5. **API Integration** - Gemini API communication

### Component Diagram

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│                     │     │                     │     │                     │
│   User Interface    │◄───►│   Core Generator    │◄───►│   API Integration   │
│                     │     │                     │     │                     │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
          ▲                           ▲                           ▲
          │                           │                           │
          ▼                           ▼                           ▼
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│                     │     │                     │     │                     │
│  Settings Manager   │◄───►│   File Management   │     │   Prompt System     │
│                     │     │                     │     │                     │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
```

## Component Interactions

### Core Generator
- Interacts with Settings Manager to retrieve user preferences
- Uses Prompt System to enhance user prompts
- Communicates with API Client to generate images
- Uses File Manager to save generated wallpapers
- Leverages UI Utilities for user interaction

### Settings Manager
- Handles user preferences persistence
- Provides configuration to Core Generator
- Manages basic settings like resolution and style preferences

### UI Utilities
- Provides terminal UI elements for all components
- Handles user input and validation
- Displays progress and status information
- Implements consistent UI styling

### File Manager
- Handles saving and loading images
- Implements filename generation with timestamps
- Organizes wallpapers in the genimage directory

### API Client
- Manages communication with Gemini API
- Handles authentication and API keys
- Processes API responses
- Implements basic error handling

## Data Flow

1. **User Input Flow**
   - User provides input via terminal interface (UI Utilities)
   - Input is validated and processed
   - Settings Manager records user preferences
   - Core Generator initiates wallpaper creation

2. **Prompt Generation Flow**
   - Core Generator receives user prompt
   - Prompt System enhances prompt with tags
   - Enhanced prompt is sent to API Client

3. **Image Generation Flow**
   - API Client sends prompt to Gemini API
   - API responds with generated image
   - Core Generator receives image from API Client
   - File Manager saves image with timestamp
   - UI Utilities display success message and image path

## Key Classes and Interfaces

### Core Classes
- `WallpaperGenerator`: Main application class
- `UserPreferences`: Stores and manages user settings
- `GeminiClient`: Manages API communication
- `WallpaperManager`: Handles file operations
- `UIUtils`: Provides terminal UI elements

## Implementation Details

### File Structure
```
wallgen/
├── wallpaper_generator.py    # Main entry point
├── api/                      # API integration
│   ├── __init__.py
│   └── gemini_client.py      # Gemini API client
├── core/                     # Core generation logic
│   ├── __init__.py
│   └── generator.py          # Main generation engine
├── ui/                       # User interface
│   ├── __init__.py
│   └── ui_utils.py           # UI utilities
├── settings/                 # Settings management
│   ├── __init__.py
│   └── preferences.py        # User preferences
├── utils/                    # Utility functions
│   ├── __init__.py
│   └── file_utils.py         # File management utilities
├── tests/                    # Test suite
│   ├── test_generator.py
│   └── test_preferences.py
├── docs/                     # Documentation
├── asset/                    # Assets like images and banners
├── requirements.txt          # Dependencies
└── setup.py                  # Package setup script
```

### Dependencies
- `google-generativeai`: Gemini API client
- `python-dotenv`: Environment variable management
- `colorama`: Terminal colors
- `pillow`: Image processing

## See Also

- [Developer Guide](developer-guide.md): Technical documentation for developers
- [API Reference](api-reference.md): API integration details
- [User Guide](user-guide.md): User documentation
- [Getting Started Guide](getting-started.md): Setup and first steps

---

<div align="center">
<img src="../asset/logo/gemini.svg" alt="Logo" width="64" height="64">

Documentation last updated: 2024-03-28
</div> 