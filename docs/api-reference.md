# API Reference

```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║    █████╗ ██████╗ ██╗    ██████╗ ███████╗███████╗                         ║
║   ██╔══██╗██╔══██╗██║    ██╔══██╗██╔════╝██╔════╝                         ║
║   ███████║██████╔╝██║    ██████╔╝█████╗  █████╗                           ║
║   ██╔══██║██╔═══╝ ██║    ██╔══██╗██╔══╝  ██╔══╝                           ║
║   ██║  ██║██║     ██║    ██║  ██║███████╗██║                              ║
║   ╚═╝  ╚═╝╚═╝     ╚═╝    ╚═╝  ╚═╝╚══════╝╚═╝                              ║
║                                                                            ║
║   Programmatic Interfaces for Wallgen                                      ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

## Overview

This document provides comprehensive information about Wallgen's programmatic interfaces. All documented features are currently implemented and available for use.

## Table of Contents

- [Core Functions](#core-functions)
- [Settings Management](#settings-management)
- [File Operations](#file-operations)
- [API Integration](#api-integration)
- [Error Handling](#error-handling)
- [Examples](#examples)

## Core Functions

### Wallpaper Generation

```python
def generate_wallpaper(prompt: str) -> str:
    """
    Generate a wallpaper using the provided prompt.
    
    Args:
        prompt (str): The prompt describing the desired wallpaper.
    
    Returns:
        str: Path to the generated image in the genimage directory.
    
    Raises:
        GenerationError: If generation fails.
        APIError: If API communication fails.
    """
```

### Prompt Enhancement

```python
def enhance_prompt(prompt: str, tags: List[str]) -> str:
    """
    Enhance a prompt using the tag-based system.
    
    Args:
        prompt (str): Base prompt to enhance
        tags (List[str]): List of tags to incorporate
    
    Returns:
        str: Enhanced prompt string
    
    Example tags:
        - Art styles: "digital_art", "photograph", "oil_painting"
        - Moods: "peaceful", "dramatic", "mysterious"
        - Quality: "high_quality", "detailed", "realistic"
    """
```

## Settings Management

### UserPreferences Class

```python
class UserPreferences:
    """
    Class to manage user preferences for the wallpaper generator.
    
    Attributes:
        api_key (str): Google Gemini API key
        resolution (Tuple[int, int]): Fixed resolution (1920, 1080)
        output_dir (str): Directory for generated images (genimage)
    """
    
    def __init__(self):
        """Initialize user preferences with default values."""
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.resolution = (1920, 1080)
        self.output_dir = "genimage"
    
    def save(self) -> None:
        """Save preferences to environment variables."""
        os.environ["GEMINI_API_KEY"] = self.api_key
    
    def load(self) -> None:
        """Load preferences from environment variables."""
        self.api_key = os.getenv("GEMINI_API_KEY", self.api_key)
```

## File Operations

### File Management

```python
def save_image(image: Image.Image, prompt: str) -> str:
    """
    Save a generated image with a timestamp-based filename.
    
    Args:
        image (Image.Image): The PIL Image to save
        prompt (str): The prompt used to generate the image
    
    Returns:
        str: Path to the saved image file
    """

def get_image_path(timestamp: str) -> str:
    """
    Get the path for a generated image.
    
    Args:
        timestamp (str): Timestamp for the image
    
    Returns:
        str: Full path in the genimage directory
    """
```

## API Integration

### Gemini Client

```python
class GeminiClient:
    """
    Client for interacting with the Google Gemini API.
    
    Attributes:
        api_key (str): The Gemini API key
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the Gemini client.
        
        Args:
            api_key (str): Google Gemini API key
        """
        self.api_key = api_key
    
    def generate_image(self, prompt: str) -> Image.Image:
        """
        Generate an image using the Gemini API.
        
        Args:
            prompt (str): The prompt to use for generation
        
        Returns:
            Image.Image: The generated image
        
        Raises:
            APIError: If the API request fails
        """
```

## Error Handling

The following exceptions are used in the API:

```python
class GenerationError(Exception):
    """Raised when wallpaper generation fails."""
    pass

class APIError(Exception):
    """Raised when API communication fails."""
    pass

class ConfigError(Exception):
    """Raised when configuration is invalid."""
    pass
```

## Examples

### Basic Usage

```python
from wallpaper_generator import generate_wallpaper
from settings import UserPreferences

# Initialize preferences
prefs = UserPreferences()
prefs.api_key = "your-api-key-here"
prefs.save()

# Generate a wallpaper
image_path = generate_wallpaper("A serene mountain landscape")
print(f"Generated wallpaper saved to: {image_path}")
```

### Using Tags

```python
from wallpaper_generator import generate_wallpaper, enhance_prompt

# Create a prompt with tags
base_prompt = "A mountain landscape"
tags = ["digital_art", "peaceful", "high_quality"]
enhanced_prompt = enhance_prompt(base_prompt, tags)

# Generate wallpaper with enhanced prompt
image_path = generate_wallpaper(enhanced_prompt)
print(f"Generated wallpaper saved to: {image_path}")
```

### Error Handling

```python
from wallpaper_generator import generate_wallpaper
from wallpaper_generator.errors import GenerationError, APIError

try:
    image_path = generate_wallpaper("A mountain landscape")
except APIError as e:
    print(f"API Error: {e}")
except GenerationError as e:
    print(f"Generation Error: {e}")
```

---

<div align="center">
<img src="../asset/logo/gemini.svg" alt="Logo" width="64" height="64">

Documentation last updated: 2024-03-28
</div> 