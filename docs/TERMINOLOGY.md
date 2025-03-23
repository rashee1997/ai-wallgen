# Wallgen Terminology Reference

```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ ██████╗ ██╗      ██████╗  ║
║   ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔═══██╗██║     ██╔════╝  ║
║      ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║██║   ██║██║     ██║  ███╗ ║
║      ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██║   ██║██║     ██║   ██║ ║
║      ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║╚██████╔╝███████╗╚██████╔╝ ║
║      ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝ ╚═════╝  ║
║                                                                            ║
║   Wallgen Terminology Reference Guide                                     ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

## Overview

This document serves as the canonical reference for terminology used throughout the Wallgen project documentation. It defines standard terms for components, processes, and concepts to ensure consistency across all documentation files.

> **Note on Current Implementation:** This terminology reference includes both currently implemented components and planned features for future development. Components that are planned but not yet implemented are marked with ⏳.

## Table of Contents

- [Core Components](#core-components)
- [API Integration](#api-integration)
- [User Interface](#user-interface)
- [File Management](#file-management)
- [Settings and Configuration](#settings-and-configuration)
- [Prompt Processing](#prompt-processing)
- [Error Handling](#error-handling)
- [Relationships Between Components](#relationships-between-components)

## Core Components

| Standard Term | Class/Implementation Name | Description | Status |
|---------------|---------------------------|-------------|--------|
| Core Generator | `WallpaperGenerator` | The central component responsible for coordinating wallpaper generation process | Implemented |
| Settings Manager | `UserPreferences` | Handles loading, saving, and managing user configuration settings | Implemented |
| Prompt Engineer | `PromptEnhancer` | Processes and enhances user prompts for better generation results | Implemented |
| File Manager | `FileManager` | Manages generated wallpapers and file system operations | Implemented |
| UI Utilities | `UIManager` | Provides terminal-based user interface elements | Implemented |

## API Integration

| Standard Term | Class/Implementation Name | Description | Status |
|---------------|---------------------------|-------------|--------|
| Google Gemini API | External service | The external API provided by Google that powers image generation | Implemented |
| Gemini Client | `GeminiClient` | Low-level client that directly interfaces with the Google Gemini API | Implemented |
| Wallgen API | `WallgenAPI` | High-level interface providing unified access to all Wallgen functionality | ⏳ Planned |
| Rate Limiter | `RateLimiter` | Manages API request frequency to avoid quota issues | ⏳ Planned |

## User Interface

| Standard Term | Class/Implementation Name | Description | Status |
|---------------|---------------------------|-------------|--------|
| Terminal UI | `UIManager` | Text-based user interface for command-line interaction | Implemented |
| Menu System | `MenuManager` | Handles displaying and processing menu options | ⏳ Planned |
| Progress Indicator | `ProgressIndicator` | Shows operation progress during long-running tasks | Implemented |
| Input Validator | `InputValidator` | Validates and processes user input | ⏳ Planned |

## File Management

| Standard Term | Class/Implementation Name | Description | Status |
|---------------|---------------------------|-------------|--------|
| Wallpaper Manager | `WallpaperManager` | Organizes and manages generated wallpapers | Implemented |
| Metadata Storage | `MetadataManager` | Handles saving and loading generation metadata | ⏳ Planned |
| Tagging System | `TagManager` | Manages user-assigned tags for wallpapers | ⏳ Planned |
| Export Utility | `ExportManager` | Handles exporting wallpapers with or without metadata | ⏳ Planned |

## Settings and Configuration

| Standard Term | Class/Implementation Name | Description | Status |
|---------------|---------------------------|-------------|--------|
| User Preferences | `UserPreferences` | Stores user's settings and preferences | Implemented |
| Preset System | `PresetManager` | Manages saved configurations as presets | ⏳ Planned |
| Configuration File | `.wallgen.config` | File storing persistent configuration | Implemented |
| Settings Schema | `PreferencesSchema` | Defines the structure of settings data | ⏳ Planned |

## Prompt Processing

| Standard Term | Class/Implementation Name | Description | Status |
|---------------|---------------------------|-------------|--------|
| Prompt Enhancement | `enhance_prompt()` | Process of improving user prompts for better results | Implemented |
| Style Mixer | `StyleMixer` | Combines multiple artistic styles with weights | ⏳ Planned |
| Prompt Sanitizer | `sanitize_prompt()` | Removes problematic content from prompts | Implemented |
| Prompt Strategy | `PromptStrategy` | Interface for different prompt generation methods | ⏳ Planned |

## Error Handling

| Standard Term | Class/Implementation Name | Description | Status |
|---------------|---------------------------|-------------|--------|
| Wallgen Error | `WallgenError` | Base class for all Wallgen exceptions | Implemented |
| API Key Error | `WallgenAPIKeyError` | Errors related to the API key | Implemented |
| Configuration Error | `WallgenConfigError` | Errors in configuration processing | Implemented |
| Generation Error | `WallgenGenerationError` | Failures during image generation | Implemented |
| Settings Error | `WallgenSettingsError` | Errors in settings management | ⏳ Planned |
| Preset Error | `WallgenPresetError` | Errors in preset handling | ⏳ Planned |
| File Error | `WallgenFileError` | File operation failures | Implemented |
| System Error | `WallgenSystemError` | System integration failures | ⏳ Planned |

## Relationships Between Components

The following diagram illustrates the relationships between major components that are currently implemented:

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│                     │     │                     │     │                     │
│   UI Utilities      │◄───►│   Core Generator    │◄───►│   Gemini Client     │
│   (UIManager)       │     │   (WallpaperGen.)   │     │   (GeminiClient)    │
│                     │     │                     │     │                     │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
          ▲                           ▲                           ▲
          │                           │                           │
          ▼                           ▼                           ▼
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│                     │     │                     │     │                     │
│  Settings Manager   │◄───►│   File Manager      │     │   Prompt Engineer   │
│  (UserPreferences)  │     │   (FileManager)     │     │   (PromptEnhancer)  │
│                     │     │                     │     │                     │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
```

### Key Relationships

- **Core Generator** coordinates between other components
- **Gemini Client** communicates exclusively with the Google Gemini API
- **Settings Manager** provides configuration to other components
- **Prompt Engineer** works with the Core Generator to prepare prompts
- **File Manager** handles all file system operations
- **UI Utilities** interact with the user and display information

> **Note:** The high-level Wallgen API wrapper that provides unified access to all components is planned for future development.

## Usage Guidelines

When writing documentation for the Wallgen project:

1. Always use the standard terms from this reference
2. Use class names when referring specifically to implementation details
3. Use standard terms when describing concepts or components generally
4. Maintain consistency in capitalization and formatting
5. When introducing a new term, add it to this reference document
6. Clearly distinguish between implemented features and future plans

## Future Terminology Roadmap

As Wallgen continues to develop, the following enhancements to the terminology framework are planned:

1. Formalization of component interfaces and contracts
2. Addition of new components as they are implemented
3. Development of standard naming conventions for new modules
4. Consistency reviews for all documentation using automated tools

---

<div align="center">
<img src="../asset/logo/gemini.svg" alt="Logo" width="64" height="64">

Documentation last updated: 2024-03-28
</div> 