# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2024-03-24

### Added
- New modular architecture with dedicated modules:
  - `wallpaper_settings.py` for all settings management
  - `ui_utils.py` for UI-related utilities
- Comprehensive documentation for new modules
- Test organization with dedicated tests directory
- Planning documentation and project structure improvements

### Changed
- Refactored settings management into a dedicated module
- Moved UI utility functions to a separate module
- Improved code organization and separation of concerns
- Enhanced import structure to avoid circular dependencies
- Better organization of test scripts
- Updated .gitignore to exclude user-specific files and test data

### Fixed
- Circular dependency issues between modules
- Duplicate function definitions across files
- Missing shutil import in wallpaper_generator.py
- Inconsistent import organization

## [1.1.0] - 2024-03-23

### Added
- Comprehensive preset management system:
  - Save current settings as presets
  - Load presets with merge or replace options
  - View detailed preset information
  - Track currently active preset
  - Delete presets with backup functionality
- Enhanced settings management:
  - Atomic file operations for data safety
  - Automatic backup system
  - Settings validation and error handling
  - Current preset tracking across sessions
- Improved user interface:
  - Clear preset management menu
  - Detailed settings display
  - Better error messages and user feedback
  - Session persistence for user preferences

### Changed
- Improved settings storage format for better compatibility
- Enhanced error handling in file operations
- Better user feedback for all operations
- Streamlined preset loading workflow

### Fixed
- Settings persistence across sessions
- File handling safety issues
- Error handling in preset operations
- Settings validation and sanitization

## [1.0.0] - 2024-03-22

### Added
- Initial release of AI Wallpaper Generator
- Integration with Google's Imagen 3 model via Gemini API
- Multiple prompt generation methods:
  - AI-powered prompts using Gemini
  - Random tag combinations
  - Custom prompt input
  - Enhanced prompts with user preferences
- Comprehensive artistic controls:
  - Multiple artistic styles (Photorealistic, Digital Art, Sketch)
  - Art movements (Abstract Expressionism, Impressionism)
  - Post-processing effects
  - Color schemes and palette types
  - Detail levels and texture quality
- Advanced technical features:
  - Professional camera models (ARRI Alexa, RED, Sony Venice)
  - Lens options (50mm, 85mm, 24mm, Special lenses)
  - Resolution options up to 8K
  - Lighting and atmosphere controls
  - Weather conditions and seasonal effects
- Wallpaper management features:
  - Auto-setting wallpaper functionality
  - Cache management system
  - Multi-monitor support
  - Custom fit modes
  - Background color options
  - Refresh rate settings
- User preferences system with persistent storage
- Cross-platform support (Windows, macOS, Linux)
- Colored terminal output with colorama
- Comprehensive logging system
- Prompt caching and management
- Genre-based tag system
- Advanced prompt engineering capabilities

### Dependencies
- Python 3.8 or higher
- google-generativeai >= 0.3.0
- requests >= 2.31.0
- bleach >= 6.1.0
- colorama >= 0.4.6
- pillow >= 10.0.0
- absl-py >= 2.0.0
- PyQt6 >= 6.4.0

### Security
- Secure API key handling
- Input sanitization for prompts
- URL masking for sensitive data
- Safe file operations

### Documentation
- Comprehensive README with installation and usage instructions
- Detailed feature documentation
- Code style guidelines
- License information
- Contributing guidelines

### Known Limitations
- Requires Gemini API key for AI-powered features
- Some features may be platform-specific
- High-resolution generation may require significant processing time

### Future Improvements
- Enhanced error handling and recovery
- Additional artistic styles and effects
- Batch processing capabilities
- Advanced image editing features
- Community prompt sharing
- Performance optimizations

[Previous versions...] 