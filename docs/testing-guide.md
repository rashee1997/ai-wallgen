# Testing Guide

```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║    ████████╗███████╗███████╗████████╗██╗███╗   ██╗ ██████╗               ║
║    ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██║████╗  ██║██╔════╝               ║
║       ██║   █████╗  ███████╗   ██║   ██║██╔██╗ ██║██║  ███╗              ║
║       ██║   ██╔══╝  ╚════██║   ██║   ██║██║╚██╗██║██║   ██║              ║
║       ██║   ███████╗███████║   ██║   ██║██║ ╚████║╚██████╔╝              ║
║       ╚═╝   ╚══════╝╚══════╝   ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝               ║
║                                                                            ║
║   Testing Guide for Wallgen                                               ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

## Overview

This guide provides comprehensive information about testing the Wallgen project. It covers test organization, setup, execution, and development guidelines.

## Table of Contents

- [Test Structure](#test-structure)
- [Test Categories](#test-categories)
- [Running Tests](#running-tests)
- [Test Development](#test-development)
- [See Also](#see-also)

## Test Structure

### Directory Organization

```
tests/
├── __init__.py          # Package initialization
├── conftest.py          # Common fixtures and configurations
├── README.md            # Test documentation
├── test_integration.py  # Integration tests
├── test_presets.py      # Preset management tests
├── test_settings.py     # Core settings tests
└── test_import_export.py # Import/Export functionality tests
```

### Common Fixtures

The `conftest.py` file provides common test fixtures and configurations:

```python
# Constants for test files
TEST_SETTINGS_FILE = "test_settings.json"
TEST_EXPORT_FILE = "test_export.json"
TEST_HISTORY_FILE = "test_history.json"
USER_PREFS_FILE = "user_preferences.json"
USER_PREFS_BACKUP = "user_preferences.json.bak"

def setup_test_logging():
    """Configure logging for tests."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
    return logging
```

### Test Environment

Each test module includes environment setup and cleanup:

```python
def setup_test_environment():
    """Set up test environment with sample data."""
    # Back up user preferences
    # Create test files
    # Set up directories

def cleanup_test_environment():
    """Clean up test files and directories."""
    # Remove test files
    # Restore original settings
```

## Test Categories

### Integration Tests

Integration tests verify the interaction between different components:

```python
# test_integration.py
def test_wallpaper_generation():
    """Test end-to-end wallpaper generation."""
    # Set up test environment
    # Generate wallpaper
    # Verify output
    # Clean up

def test_settings_integration():
    """Test settings module integration."""
    # Initialize settings
    # Modify settings
    # Verify changes
```

### Settings Tests

Tests for the settings management functionality:

```python
# test_settings.py
def test_user_preferences():
    """Test user preferences management."""
    # Create preferences
    # Modify values
    # Verify persistence

def test_api_key_management():
    """Test API key handling."""
    # Set API key
    # Verify storage
    # Test encryption
```

### Preset Tests

Tests for preset functionality:

```python
# test_presets.py
def test_save_load_preset():
    """Test saving and loading presets."""
    # Create test preset
    # Save preset
    # Load preset
    # Verify data
```

### Import/Export Tests

Tests for settings import/export:

```python
# test_import_export.py
def test_export_settings():
    """Test settings export."""
    # Create test settings
    # Export settings
    # Verify file contents

def test_import_settings():
    """Test settings import."""
    # Create test file
    # Import settings
    # Verify imported data
```

## Running Tests

### Environment Setup

1. Install test dependencies:
   ```bash
   pip install pytest pytest-cov
   ```

2. Set up test environment:
   ```bash
   export PYTHONPATH=.
   export GEMINI_API_KEY=your_test_api_key
   ```

### Running Individual Tests

Run specific test files:

```bash
# Run integration tests
python -m pytest tests/test_integration.py

# Run settings tests
python -m pytest tests/test_settings.py

# Run preset tests
python -m pytest tests/test_presets.py

# Run import/export tests
python -m pytest tests/test_import_export.py
```

### Running All Tests

Run the entire test suite:

```bash
python -m pytest tests/
```

## Test Development

### Writing New Tests

1. Create a new test file in the `tests` directory
2. Import required modules and fixtures
3. Define test functions with clear names
4. Use appropriate assertions
5. Include setup and cleanup

Example:

```python
def test_new_feature():
    """Test description."""
    # Setup
    setup_test_environment()
    
    try:
        # Test implementation
        result = feature_function()
        assert result == expected_value
    finally:
        # Cleanup
        cleanup_test_environment()
```

### Using Fixtures

1. Import fixtures from `conftest.py`
2. Use fixture decorators
3. Clean up resources

Example:

```python
@pytest.fixture
def test_data():
    """Provide test data."""
    data = setup_test_data()
    yield data
    cleanup_test_data()

def test_with_fixture(test_data):
    """Test using fixture."""
    assert process_data(test_data) == expected_result
```

### Test Naming Conventions

- Use descriptive names that indicate what is being tested
- Follow the pattern: `test_<feature>_<scenario>`
- Include positive and negative test cases

Examples:
```python
def test_wallpaper_generation_success():
    """Test successful wallpaper generation."""

def test_wallpaper_generation_invalid_prompt():
    """Test wallpaper generation with invalid prompt."""

def test_settings_save_load():
    """Test saving and loading settings."""
```

## See Also

- [Developer Guide](developer-guide.md)
- [API Reference](api-reference.md)
- [Troubleshooting Guide](troubleshooting.md)

---

<div align="center">
<img src="../asset/logo/gemini.svg" alt="Logo" width="64" height="64">

Documentation last updated: 2024-03-28
</div> 