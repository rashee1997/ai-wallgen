# Wallgen Architecture

![Architecture Banner](../asset/doc_banners/template_banner.png)

## Overview

This document describes the architecture and system design of the Wallgen project. It provides a comprehensive overview of the components, their interactions, and the overall data flow of the wallpaper generation system.

## Table of Contents

- [System Components](#system-components)
- [Component Interactions](#component-interactions)
- [Data Flow](#data-flow)
- [Key Classes and Interfaces](#key-classes-and-interfaces)
- [Design Patterns](#design-patterns)
- [Extension Points](#extension-points)
- [Implementation Details](#implementation-details)
- [See Also](#see-also)

## System Components

The Wallgen application is structured into the following primary components:

1. **Core Generator** - Primary wallpaper generation logic
2. **Settings Management** - User preferences and configuration
3. **UI Utilities** - Terminal interface elements
4. **Prompt Engineering** - AI-based prompt generation and enhancement
5. **File Management** - Image and settings storage
6. **API Integration** - Gemini API communication

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Wallgen System                          │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │             │    │             │    │             │     │
│  │ UI Utilities│<───│Core Generator│───>│ File Manager│     │
│  │             │    │             │    │             │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│         ▲                  ▲                  ▲            │
│         │                  │                  │            │
│         ▼                  ▼                  ▼            │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │             │    │             │    │             │     │
│  │  Settings   │<───│   Prompt    │<───│ API Client  │     │
│  │  Manager    │    │  Engineer   │    │             │     │
│  │             │    │             │    │             │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Component Interactions

### Core Generator
- Interacts with Settings Manager to retrieve user preferences
- Uses Prompt Engineer to generate and enhance prompts
- Communicates with API Client to generate images
- Uses File Manager to save generated wallpapers
- Leverages UI Utilities for user interaction

### Settings Manager
- Handles user preferences persistence
- Manages presets and favorite settings
- Provides configuration to Core Generator
- Supports import/export of settings

### UI Utilities
- Provides terminal UI elements for all components
- Handles user input and validation
- Displays progress and status information
- Implements consistent UI styling

### Prompt Engineer
- Generates AI-powered prompts
- Enhances user-provided prompts
- Implements style mixing and compatibility checks
- Manages prompt templates and structures

### File Manager
- Handles saving and loading images
- Manages cache for prompt and image storage
- Implements intelligent filename generation
- Organizes wallpaper history

### API Client
- Manages communication with Gemini API
- Handles authentication and API keys
- Processes API responses
- Implements error handling and retries

## Data Flow

1. **User Input Flow**
   - User provides input via terminal interface (UI Utilities)
   - Input is validated and processed
   - Settings Manager records user preferences
   - Core Generator initiates wallpaper creation

2. **Prompt Generation Flow**
   - Core Generator requests prompt from Prompt Engineer
   - Prompt Engineer creates or enhances prompt using user preferences
   - Enhanced prompt is returned to Core Generator
   - Core Generator sends prompt to API Client

3. **Image Generation Flow**
   - API Client sends prompt to Gemini API
   - API responds with generated image
   - Core Generator receives image from API Client
   - File Manager saves image with appropriate filename
   - UI Utilities display success message and image path

## Key Classes and Interfaces

### Core Classes
- `WallpaperGenerator`: Main application class
- `UserPreferences`: Stores and manages user settings
- `PromptEnhancer`: Handles prompt generation and improvement
- `GeminiClient`: Manages API communication
- `FileManager`: Handles file operations
- `UIManager`: Provides terminal UI elements

### Important Interfaces
- `PromptStrategy`: Interface for different prompt generation strategies
- `APIProvider`: Interface for different API providers
- `StorageProvider`: Interface for different storage mechanisms
- `StyleMixer`: Interface for style combination algorithms

## Design Patterns

The Wallgen project implements several design patterns to promote modularity and maintainability:

1. **Singleton Pattern**
   - Used for `UserPreferences` to ensure single instance
   - Implemented in `GeminiClient` for API connection reuse

2. **Strategy Pattern**
   - Used for prompt generation methods
   - Allows swapping between random, AI-powered, and custom prompts

3. **Factory Pattern**
   - Implemented for creating style combinations
   - Used to generate appropriate UI elements

4. **Observer Pattern**
   - Used for progress updates and notifications
   - Implemented in long-running operations

5. **Command Pattern**
   - Used for executing user commands
   - Enables undo/redo functionality for settings

## Extension Points

The architecture includes several extension points for future enhancements:

1. **API Providers**
   - Alternative image generation APIs
   - Additional AI model integrations

2. **Storage Mechanisms**
   - Cloud storage integration
   - Alternative local storage options

3. **UI Interfaces**
   - Graphical user interface
   - Web interface

4. **Prompt Strategies**
   - Additional prompt generation methods
   - New style combinations

## Implementation Details

### File Structure
```
wallgen/
├── wallpaper_generator.py   # Main application
├── wallpaper_settings.py    # Settings management
├── wallpaper_config.py      # Configuration constants
├── ui_utils.py              # Terminal UI utilities
├── prompt_config.py         # Prompt configuration
├── prompt_generator.log     # Logging
├── genimage/                # Generated images
├── asset/                   # Application assets
├── cache/                   # Cached data
├── history/                 # Generation history
├── presets/                 # User presets
└── docs/                    # Documentation
```

### Dependencies
- `google-generativeai`: Gemini API client
- `requests`: HTTP requests
- `colorama`: Terminal colors
- `pillow`: Image processing
- `absl-py`: Command line parsing

## See Also

- [README.md](../README.md): Main project documentation
- [README_wallpaper_settings.md](../README_wallpaper_settings.md): Settings module documentation
- [README_ui_utils.md](../README_ui_utils.md): UI utilities documentation
- [GUIDE_settings_import_export.md](../GUIDE_settings_import_export.md): Settings management guide

---

<div align="center">
<img src="../asset/logo/gemini.svg" alt="Logo" width="64" height="64">

Documentation last updated: 2024-03-24
</div> 