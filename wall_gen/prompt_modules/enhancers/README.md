# Prompt Enhancers Package

This package provides a modular system for enhancing prompts used in AI image generation, with specialized support for both logo generation and general image prompts.

## Overview

The package consists of several modules that work together to provide comprehensive prompt enhancement capabilities:

- `base.py`: Contains base classes and common functionality
- `logo.py`: Specialized enhancement for logo generation prompts
- `general.py`: Enhancement for general (non-logo) prompts
- `__init__.py`: Main interface and factory functions
- `tests.py`: Unit tests for the package

## Usage

### Basic Usage

```python
from wall_gen.prompt_modules.enhancers import enhance_prompt, generate_logo

# Enhance a general prompt
enhanced_prompt = enhance_prompt(
    prompt="A beautiful sunset over mountains",
    user_prefs=user_preferences  # Optional
)

# Generate a logo prompt
logo_prompt = generate_logo(
    logo_text="BrandName",
    tag_lines="Your Tagline Here",
    logo_style="minimalist",
    logo_color="#FF5733",
    logo_industry="Technology"
)
```

### Using Enhancers Directly

```python
from wall_gen.prompt_modules.enhancers.general import GeneralPromptEnhancer
from wall_gen.prompt_modules.enhancers.logo import LogoPromptEnhancer

# Create enhancer instances
general_enhancer = GeneralPromptEnhancer(user_prefs)
logo_enhancer = LogoPromptEnhancer(user_prefs)

# Enhance prompts
enhanced_general = general_enhancer.enhance_prompt(
    prompt="A beautiful sunset",
    description="Additional context"
)

enhanced_logo = logo_enhancer.enhance_prompt(
    prompt="BrandName",
    tag_lines="Your Tagline",
    logo_style="minimalist"
)
```

## Features

### General Prompt Enhancement

- Preserves specified art mediums (watercolor, oil painting, etc.)
- Handles technical parameters (resolution, aspect ratio)
- Incorporates user preferences for style, lighting, composition, etc.
- Manages negative prompts intelligently
- Detects and preserves art mediums

### Logo Prompt Enhancement

- Supports both structured and unstructured formats
- Handles brand identity elements
- Incorporates typography and design guidance
- Manages logo-specific technical parameters
- Supports taglines and industry context

### Common Features

- Comprehensive error handling
- Type checking and validation
- Detailed logging
- Fallback mechanisms
- User preference integration

## Error Handling

The package provides custom exceptions for different error scenarios:

```python
from wall_gen.prompt_modules.enhancers.base import (
    PromptEnhancementError,
    GeminiClientError,
    PreferenceExtractionError,
    ValidationError
)

try:
    enhanced = enhance_prompt(prompt)
except ValidationError:
    # Handle invalid input
except GeminiClientError:
    # Handle Gemini API issues
except PreferenceExtractionError:
    # Handle preference extraction issues
except PromptEnhancementError:
    # Handle general enhancement errors
```

## Testing

Run the test suite:

```bash
python -m unittest wall_gen.prompt_modules.enhancers.tests
```

## Architecture

### Base Classes

The `BasePromptEnhancer` class provides common functionality:

- Gemini client initialization
- Input validation
- Preference extraction
- Response handling
- Prompt formatting

### Specialized Enhancers

Both `LogoPromptEnhancer` and `GeneralPromptEnhancer` extend `BasePromptEnhancer` with specialized functionality:

- Custom validation rules
- Specific preference handling
- Tailored enhancement logic
- Medium-specific formatting

## Configuration

The enhancers use several configuration sources:

1. User preferences object
2. Logo templates (for logo enhancement)
3. Default values for various parameters
4. Environment-specific Gemini configuration

## Best Practices

1. Always provide user preferences when possible
2. Handle exceptions appropriately
3. Use the factory functions (`enhance_prompt`, `generate_logo`) for most cases
4. Test thoroughly with different input types
5. Monitor and log enhancement results

## Contributing

When contributing to this package:

1. Add tests for new functionality
2. Update documentation
3. Follow existing code style
4. Handle errors gracefully
5. Maintain backward compatibility

## Dependencies

- Google Generative AI SDK
- Python 3.7+
- Logging module
- Type hints support
