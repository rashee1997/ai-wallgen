# Changelog

All notable changes to the Wallgen project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Added operational flow diagrams (Core Wallpaper Generation, AI Preset Generation) to `docs/PROJECT_OVERVIEW.md` for better architectural understanding.
- AI Preset Generation functionality via `ai_preset_generator.py`.
- AI Style Generation functionality via `ai_style_generator.py`.
- GUI image preview (Qt/Tkinter).
- CLI commands for preset and style generation.
- Cross-platform wallpaper setting.
- Improved prompt engineering.

## [2.0.0] - 2025-05-01

### Changed
- **Major refactoring**: Modularized large `wallpaper_settings.py` file into smaller, logical components.
- Created new `settings_modules/` package with specialized submodules:
  - `settings_manager.py`: Central settings initialization and access.
  - `user_preferences.py`: User preference handling and persistence.
  - `preset_management.py`: Preset saving, loading, and management.
  - `settings_import_export.py`: Settings file export and import functionality.
  - `ai_preset_generation.py`: AI-assisted preset generation.
  - `settings_utils.py`: Utility functions for settings management.
- Organized menu-related code into `settings_modules/menu_management/` with specialized modules:
  - `main_menu.py`: Main settings menu handling.
  - `genres_menu.py`: Genre management interface.
  - `styles_menu.py`: Style management interface.
  - `moods_menu.py`: Mood management interface.
  - `advanced_options_menu.py`: Advanced configuration options.
  - Additional specialized menu modules.
- Moved UI utility functions from settings to `ui_utils.py`.
- Improved code organization with proper import structures.
- Improved main README.md with clearer installation instructions.
- Enhanced structure and formatting of module-specific documentation.
- Standardized documentation format across the project.

### Added
- Proper package initialization with `__init__.py` files.
- Better module boundaries and responsibility separation.
- Clear import hierarchies between modules.
- Comprehensive documentation enhancement across the project.
- User guide with detailed instructions and examples.
- Developer guide for contributors and developers.
- API reference documentation.
- Troubleshooting guide and FAQ section.

### Fixed
- Documentation inconsistencies and broken links.
- Improved cross-referencing between documentation files.

### Benefits
- Improved maintainability through smaller, focused modules.
- Better code navigation and logical grouping.
- Reduced cognitive load when working with settings functionality.
- Enhanced extensibility for future features.

## [1.0.0] - 2024-03-20

### Added
- Initial release of Wallgen.
- Core wallpaper generation functionality using Google Imagen 3.
- Terminal-based user interface with color support.
- Settings management system.
- Preset saving and loading.
- Command-line arguments for direct generation.

### Changed
- Optimized image processing for better performance.
- Enhanced prompt engineering for better results.

### Fixed
- API connection error handling.
- File permission issues on different operating systems.

## [0.9.0] - 2024-03-10

### Added
- Beta release with core functionality.
- Integration with Google Gemini API.
- Basic UI system.
- File management for generated wallpapers.
- Simple settings storage.

### Changed
- Improved prompt processing.
- Enhanced error messages.
- Updated UI elements.

### Fixed
- Initial bugs in API integration.
- Path handling issues.
- Settings persistence problems.

## [0.5.0] - 2024-02-15

### Added
- Alpha release for internal testing.
- Initial API integration.
- Basic command-line interface.
- Minimal documentation.
