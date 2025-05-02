# Installation and CLI Guide for Wallgen

## Overview

This guide provides comprehensive information on setting up and using Wallgen, a terminal-based AI wallpaper generator, via its command line interface. You'll learn how to install the application, configure API access, and utilize all available command line options for generating and managing wallpapers without the interactive menu system.

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
   git clone https://github.com/rasheedh/wallgen.git
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
   git clone https://github.com/rasheedh/wallgen.git
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

## Command Line Interface (CLI) Guide

### Basic Usage

The basic syntax for running AI Wallgen from the command line is:

```bash
python wallpaper_generator.py [OPTIONS]
```

If no options are provided, AI Wallgen will start in interactive mode with the main menu.

### Available Options

#### Prompt Options

| Option | Description |
|:------:|:------------|
| `--prompt TEXT` | Custom prompt for wallpaper generation |
| `--random` | Generate a random wallpaper |
| `--test-prompt TEXT` | Test prompt generation without creating an image |
| `--test-custom-prompt TEXT` | Test custom prompt enhancement |
| `--dont-use-user-prefs` | Do not use user preferences for prompt generation |

##### The `--prompt` Option

The `--prompt` option allows you to specify a custom text prompt for generating a wallpaper. This prompt will be enhanced by the AI to create a more detailed and artistic description before generating the image.

**Usage:**
```bash
python wallpaper_generator.py --prompt "your custom text prompt here"
```

**Example:**
```bash
python wallpaper_generator.py --prompt "mountain landscape with snow peaks at sunset"
```

**What happens:**
1. AI Wallgen first sanitizes your prompt to ensure it's safe for image generation
2. The prompt is then enhanced using the AI to add artistic details (this uses your saved preferences by default)
3. You'll be shown the enhanced prompt and asked to confirm before generation begins
4. If you approve, the AI will generate an image based on the enhanced prompt

> **💡 Tips:**
> - Be specific about what you want to see in the image
> - Include styles or artistic elements if you have a particular look in mind
> - You can combine with other options like `--resolution` or `--aspect-ratio`
> - For more control, you can use the `--dont-use-user-prefs` flag to avoid using your saved preferences

**Examples with combinations:**
```bash
# Generate a wallpaper with custom prompt and specific resolution
python wallpaper_generator.py --prompt "cyberpunk city at night with neon lights" --resolution 1920x1080

# Generate a custom prompt image with a square aspect ratio
python wallpaper_generator.py --prompt "abstract geometric patterns in vibrant colors" --aspect-ratio 1:1

# Generate from a prompt without using saved preferences
python wallpaper_generator.py --prompt "forest with fog and sunbeams" --dont-use-user-prefs
```

#### The `--random` Option

The `--random` option generates a wallpaper using randomly selected tags and AI enhancement, without requiring you to provide a specific prompt.

**Usage:**
```bash
python wallpaper_generator.py --random
```

**What happens:**
1. AI Wallgen selects 3-6 random tags from its internal categories (nature, space, urban, abstract, etc.)
2. These tags are used to generate an initial prompt
3. The prompt is enhanced using the AI (with your preferences by default)
4. You'll be shown the enhanced prompt and asked to confirm
5. If you approve, the AI will generate an image based on the enhanced prompt

> **💡 Tips:**
> - This is perfect for discovering new wallpaper ideas
> - If you don't like the first prompt, you can reject it and AI Wallgen will generate another
> - You can combine with other options like `--resolution` or `--aspect-ratio`
> - For unpredictable results, use with `--dont-use-user-prefs` to ignore your saved styles and preferences

**Examples with combinations:**
```bash
# Generate a random wallpaper with specific resolution
python wallpaper_generator.py --random --resolution 3840x2160

# Generate a random wallpaper with square aspect ratio
python wallpaper_generator.py --random --aspect-ratio 1:1

# Generate a random wallpaper without using your saved preferences
python wallpaper_generator.py --random --dont-use-user-prefs

# See the random prompt that would be generated without actually creating an image
python wallpaper_generator.py --random --no-generate
```

#### The `--test-prompt` Option

The `--test-prompt` option allows you to test how AI Wallgen transforms a simple subject or concept into a detailed generation prompt, without actually creating an image.

**Usage:**
```bash
python wallpaper_generator.py --test-prompt "subject or concept"
```

**Example:**
```bash
python wallpaper_generator.py --test-prompt "forest"
```

**What happens:**
1. AI Wallgen takes your subject or concept and passes it to the Gemini AI
2. The AI uses it to generate a detailed, artistic prompt
3. The generated prompt is displayed in the terminal
4. No image is generated, making this useful for experimentation

> **💡 Tips:**
> - This is useful for testing what kind of prompts AI Wallgen can generate from simple concepts
> - You can use this to experiment with different subjects before committing to image generation
> - By default, your user preferences will be applied to the prompt generation
> - Combine with `--dont-use-user-prefs` to see generation without your saved preferences

**Examples with combinations:**
```bash
# Test a prompt with a simple concept
python wallpaper_generator.py --test-prompt "ocean"

# Test a prompt with a more specific idea
python wallpaper_generator.py --test-prompt "cyberpunk cityscape"

# Test a prompt without using saved preferences
python wallpaper_generator.py --test-prompt "mountains" --dont-use-user-prefs
```

#### The `--test-custom-prompt` Option

The `--test-custom-prompt` option allows you to see how AI Wallgen would enhance a detailed prompt you've written, without actually generating an image.

**Usage:**
```bash
python wallpaper_generator.py --test-custom-prompt "your detailed prompt here"
```

**Example:**
```bash
python wallpaper_generator.py --test-custom-prompt "a misty mountain range at sunrise with golden light"
```

**What happens:**
1. AI Wallgen takes your custom prompt and passes it to the AI enhancer
2. The AI adds artistic details and technical specifications to your prompt
3. The enhanced prompt is displayed in the terminal
4. No image is generated, so you can test enhancements quickly

**Difference from `--test-prompt`:**
- `--test-prompt` transforms a simple concept into a complete prompt
- `--test-custom-prompt` enhances an already detailed prompt that you provide

> **💡 Tips:**
> - Use this to refine your prompts before generating images
> - The enhancement adds technical details like lighting, composition, and style
> - By default, enhancements use your saved user preferences
> - Combine with `--dont-use-user-prefs` to see enhancements without your saved settings

**Examples with combinations:**
```bash
# Test enhancement of a landscape prompt
python wallpaper_generator.py --test-custom-prompt "desert landscape with red rock formations under a blue sky"

# Test enhancement of a detailed artistic prompt
python wallpaper_generator.py --test-custom-prompt "cyberpunk city at night with neon signs and flying cars in the rain"

# Test enhancement without using saved preferences
python wallpaper_generator.py --test-custom-prompt "underwater coral reef with colorful fish" --dont-use-user-prefs
```

#### The `--dont-use-user-prefs` Option

The `--dont-use-user-prefs` option allows you to generate prompts and images without applying your saved user preferences, resulting in more neutral or varied outputs.

**Usage:**
```bash
python wallpaper_generator.py --prompt "your prompt" --dont-use-user-prefs
python wallpaper_generator.py --random --dont-use-user-prefs
```

**What happens:**
1. AI Wallgen skips loading your saved preferences for prompt generation
2. No preferred styles, moods, or technical settings are applied to the generated or enhanced prompts
3. The prompt generation uses default settings instead of your customized ones
4. This results in different outputs compared to what you would get with your preferences

> **💡 Tips:**
> - Use this when you want to explore different styles outside your usual preferences
> - Helpful for getting "fresh" results after you've generated many images with your preferences
> - Combine with `--random` for truly unpredictable results
> - Can be used with any prompt-related options to see how they behave without your preferences

**Examples with combinations:**
```bash
# Generate a custom prompt image without applying your preferences
python wallpaper_generator.py --prompt "forest landscape" --dont-use-user-prefs

# Generate a random wallpaper ignoring your preferred styles and settings
python wallpaper_generator.py --random --dont-use-user-prefs

# Test how a prompt would be enhanced without your preferences
python wallpaper_generator.py --test-prompt "cityscape" --dont-use-user-prefs

# Test custom prompt enhancement without applying your saved preferences
python wallpaper_generator.py --test-custom-prompt "mountain valley with river" --dont-use-user-prefs

# View a random prompt without generating an image or using preferences
python wallpaper_generator.py --random --no-generate --dont-use-user-prefs
```

---

### Image Settings

| Option | Description |
|:------:|:------------|
| `--resolution WIDTHxHEIGHT` | Set output resolution (e.g., '1920x1080') |
| `--aspect-ratio RATIO` | Set aspect ratio (e.g., '16:9', '4:3', '1:1') |

#### The `--resolution` and `--aspect-ratio` Options

These options allow you to control the dimensions of the generated wallpapers to match your display requirements.

**Usage:**
```bash
python wallpaper_generator.py --resolution "WIDTHxHEIGHT"
python wallpaper_generator.py --aspect-ratio "RATIO"
```

**Examples:**
```bash
python wallpaper_generator.py --resolution "1920x1080"
python wallpaper_generator.py --aspect-ratio "16:9"
```

**What happens:**
1. The specified resolution or aspect ratio overwrites your saved preferences for the current session
2. When generating wallpapers, these values are used to create images with the appropriate dimensions
3. For aspect ratio, the resulting image will maintain that proportional relationship
4. For resolution, the image will be generated at exactly the specified dimensions

<table>
  <tr>
    <td valign="top">
      <strong>Supported Aspect Ratios:</strong>
      <ul>
        <li><code>16:9</code> - Standard widescreen (default)</li>
        <li><code>16:10</code> - Widescreen with more vertical space</li>
        <li><code>4:3</code> - Traditional/standard</li>
        <li><code>21:9</code> - Ultrawide</li>
        <li><code>32:9</code> - Super ultrawide</li>
        <li><code>1:1</code> - Square</li>
        <li><code>9:16</code> - Mobile portrait</li>
        <li>Custom ratios (e.g., <code>3:2</code>)</li>
      </ul>
    </td>
    <td valign="top">
      <strong>Supported Resolutions:</strong>
      <p>You can specify any resolution, but common ones include:</p>
      <ul>
        <li><code>1920x1080</code> - Full HD</li>
        <li><code>2560x1440</code> - 2K / QHD</li>
        <li><code>3840x2160</code> - 4K / UHD</li>
        <li><code>7680x4320</code> - 8K</li>
      </ul>
    </td>
  </tr>
</table>

> **💡 Tips:**
> - These options are particularly useful when generating wallpapers for specific devices
> - They can be combined with other options like `--prompt` or `--random`
> - When specifying a custom resolution, make sure it matches the aspect ratio you want
> - Using a higher resolution will create larger, more detailed images but may take longer to generate

**Examples with combinations:**
```bash
# Generate a 4K wallpaper with a custom prompt
python wallpaper_generator.py --prompt "sunset over mountains" --resolution "3840x2160"

# Generate a random wallpaper with ultrawide aspect ratio
python wallpaper_generator.py --random --aspect-ratio "21:9"

# Test a prompt with square format
python wallpaper_generator.py --test-prompt "abstract geometric patterns" --aspect-ratio "1:1"

# Generate a mobile wallpaper
python wallpaper_generator.py --prompt "starry night sky" --aspect-ratio "9:16"
```

---

### Behavior Options

| Option | Description |
|:------:|:------------|
| `--no-generate` | Don't generate the image, just show the prompt |
| `--no-preset` | Skip loading the last preset on startup |

#### The `--no-generate` Option

The `--no-generate` option allows you to generate and view prompts without proceeding to image generation, which is useful for previewing what would be generated.

**Usage:**
```bash
python wallpaper_generator.py --prompt "your prompt" --no-generate
python wallpaper_generator.py --random --no-generate
```

**What happens:**
1. When used with `--prompt`: The custom prompt is enhanced, and the enhanced version is displayed in the terminal
2. When used with `--random`: A random prompt is generated, enhanced, and displayed in the terminal
3. In both cases, the application exits after showing the prompt without generating an image
4. This saves time and computational resources when you just want to see what prompt would be used

> **💡 Tips:**
> - Use this when iterating on prompt ideas to quickly see how they'll be enhanced
> - This is a quick way to test the AI's enhancement of your prompts before committing to image generation
> - Particularly useful for exploring random prompt generation without waiting for image creation
> - Can be combined with `--dont-use-user-prefs` to see how prompts would be enhanced without your preferences

**Examples with combinations:**
```bash
# Preview how a custom prompt would be enhanced
python wallpaper_generator.py --prompt "mountain landscape with a castle" --no-generate

# See what random prompt would be generated without creating an image
python wallpaper_generator.py --random --no-generate

# Preview enhancement without using saved preferences
python wallpaper_generator.py --prompt "city skyline at night" --no-generate --dont-use-user-prefs
```

#### The `--no-preset` Option

The `--no-preset` option is defined in the command line parser but appears to not be fully implemented in the current version of the application. It is intended to skip loading the last used preset when starting the application.

**Usage:**
```bash
python wallpaper_generator.py --no-preset
```

> **⚠️ Note:**
> This option is reserved for future implementation. In a future version, it may control whether the application loads the most recently used preset settings on startup.

---

### Image Preview Options

| Option | Description |
|:------:|:------------|
| `--skip-preview` | Skip the image preview and set wallpaper directly |
| `--preview-image PATH` | Preview a specific image in the terminal without setting as wallpaper |
| `--preview-latest` | Preview the latest generated image without setting as wallpaper |
| `--list-images` | List all generated images and preview one by number |

> **💡 Note on GUI Preview:**
> The graphical preview window (using Qt or Tkinter, depending on your configuration and installed libraries) is used for image previews when available. You can configure the preferred GUI backend in the application's settings.

#### The `--skip-preview` Option

The `--skip-preview` option allows you to bypass the image preview step and automatically set the generated wallpaper as your desktop background.

**Usage:**
```bash
python wallpaper_generator.py --prompt "your prompt" --skip-preview
```

**What happens:**
1. AI Wallgen generates the wallpaper image as usual
2. Instead of showing a preview and asking for confirmation, it immediately sets the image as your desktop wallpaper
3. This streamlines the process when you're confident about the result or running batch operations

> **💡 Tips:**
> - This option is useful for automation or when you want to quickly generate and apply wallpapers
> - Combine with `--prompt` or `--random` for a completely non-interactive experience
> - Be aware that you won't have a chance to reject or modify the image before it's applied

**Examples with combinations:**
```bash
# Generate a random wallpaper and apply it immediately
python wallpaper_generator.py --random --skip-preview

# Generate a custom prompt wallpaper at 4K resolution and apply it immediately
python wallpaper_generator.py --prompt "mountain landscape with lakes" --resolution 3840x2160 --skip-preview
```

#### The `--preview-image` Option

The `--preview-image` option allows you to preview any existing image file in the terminal or GUI without generating a new wallpaper.

**Usage:**
```bash
python wallpaper_generator.py --preview-image "path/to/image.png"
```

**What happens:**
1. AI Wallgen loads the specified image file
2. The image is displayed in the terminal or a graphical window, depending on your <a href="#gui-preview-note">GUI preview settings</a>.
3. You're given options to set the image as wallpaper or exit.
4. This is useful for reviewing previously generated images or any image file.

> **💡 Tips:**
> - You can use relative or absolute paths to the image file.
> - This works with any PNG, JPG, or JPEG image, not just those generated by AI Wallgen.
> - The graphical preview (Qt or Tkinter) provides a better visual experience with larger images if configured.

**Examples with combinations:**
```bash
# Preview a specific image in the terminal (if GUI preview is not configured)
python wallpaper_generator.py --preview-image "genimage/mountain_sunset_12345678.png"

# Preview an image using the configured GUI window
python wallpaper_generator.py --preview-image "genimage/abstract_pattern_87654321.png"
```

#### The `--preview-latest` Option

The `--preview-latest` option allows you to quickly preview the most recently generated wallpaper image without having to specify its path.

**Usage:**
```bash
python wallpaper_generator.py --preview-latest
```

**What happens:**
1. AI Wallgen identifies the most recently created image in the `genimage` directory.
2. The image is displayed in the terminal or a graphical window, depending on your <a href="#gui-preview-note">GUI preview settings</a>.
3. You're given options to set the image as wallpaper or exit.
4. This is convenient for checking or applying the last image you generated.

> **💡 Tips:**
> - This is useful when you've generated multiple images and want to review the latest one.
> - The "latest" is determined by file creation time, not by filename.
> - The graphical preview (Qt or Tkinter) provides a better visual experience if configured.

**Examples with combinations:**
```bash
# Preview the latest generated image in the terminal (if GUI preview is not configured)
python wallpaper_generator.py --preview-latest

# Preview the latest image using the configured GUI window
python wallpaper_generator.py --preview-latest
```

#### The `--list-images` Option

The `--list-images` option displays a chronological list of all generated wallpaper images and allows you to select one to preview.

**Usage:**
```bash
python wallpaper_generator.py --list-images
```

**What happens:**
1. AI Wallgen scans the `genimage` directory and lists all wallpaper images.
2. Images are displayed in reverse chronological order (newest first) with numbers.
3. You can select an image by number to preview it in the terminal or a graphical window, depending on your <a href="#gui-preview-note">GUI preview settings</a>.
4. After preview, you can choose to set it as wallpaper or return to the list.

> **💡 Tips:**
> - This is useful for browsing your wallpaper collection without using a file manager.
> - Each image is shown with its creation timestamp for easy reference.
> - You can exit the listing at any time by entering 'q'.
> - The graphical preview (Qt or Tkinter) provides a better visual experience if configured.

**Examples with combinations:**
```bash
# List all images and allow selection for preview (terminal or GUI based on settings)
python wallpaper_generator.py --list-images
```

### Debug Options

| Option | Description |
|:------:|:------------|
| `--verbose` | Enable verbose output (currently similar to --debug) |
| `--debug` | Enable detailed debug logging |

#### The `--debug` Option

The `--debug` option enables detailed debug logging to help identify issues when the application isn't working as expected.

**Usage:**
```bash
python wallpaper_generator.py --debug
```

**What happens:**
1. Sets the logging level to DEBUG instead of the default INFO level
2. More detailed log messages are written to the `wallpaper_generator.log` file
3. Helps troubleshoot issues with the application's internal processes
4. Primarily useful for developers or when reporting bugs

> **💡 Tips:**
> - Use this option when you encounter errors and need to provide detailed logs for troubleshooting
> - Combine with other options to debug specific functionality
> - Check the `wallpaper_generator.log` file in the application directory for the detailed logs
> - The log file includes timestamps, making it easier to track the sequence of events

**Examples with combinations:**
```bash
# Debug an issue with custom prompt generation
python wallpaper_generator.py --prompt "sunset over mountains" --debug

# Debug random prompt generation
python wallpaper_generator.py --random --debug

# Test prompt enhancement with debug logging
python wallpaper_generator.py --test-custom-prompt "forest with fog" --debug
```

#### The `--verbose` Option

The `--verbose` option enables verbose output, which currently functions similarly to the `--debug` flag by setting the logging level.

**Usage:**
```bash
python wallpaper_generator.py --verbose
```

> **💡 Tips:**
> - While this option sets the logging level, the `--debug` option is recommended for the most detailed logging output to the `wallpaper_generator.log` file.
> **💡 Tips:**
> - While this option sets the logging level, the `--debug` option is recommended for the most detailed logging output to the `wallpaper_generator.log` file.
> - Its behavior may be expanded in future versions to provide more detailed console output.

---

### AI Preset Generator CLI (`ai_preset_generator.py`)

This script allows you to manage AI-generated presets directly from the command line.

**Usage:**
```bash
python ai_preset_generator.py [COMMAND] [OPTIONS]
```

**Available Commands:**

| Command | Description | Options |
|:--------|:------------|:--------|
| `generate` | Generate a new AI preset. | `--style TEXT`: Use a specific style as a base for generation. |
| `list` | List all saved presets. | None |
| `load` | Load a preset and apply its settings to your user preferences. | `name`: The name of the preset file (without `.json`). |
| `delete` | Delete a saved preset file. | `name`: The name of the preset file (without `.json`). |

**Examples:**
```bash
# Generate a new preset based on the "photographic" style
python ai_preset_generator.py generate --style photographic

# List all saved presets
python ai_preset_generator.py list

# Load the settings from a preset named "cinematic_mood"
python ai_preset_generator.py load cinematic_mood

# Delete the preset named "my_abstract_preset"
python ai_preset_generator.py delete my_abstract_preset
```

---

### AI Style Generator CLI (`ai_style_generator.py`)

This script allows you to generate AI art styles directly from the command line.

**Usage:**
```bash
python ai_style_generator.py [OPTIONS]
```

**Available Options:**

| Option | Description |
|:-------|:------------|
| `--key TEXT` | Provide your Gemini API key directly (optional if set as environment variable). |
| `--category TEXT` | Generate a style within a specific canonical category (e.g., `oil_painting`, `geometric`, `photographic`). |
| `--detailed` | Generate a detailed style output including a name and description. |
| `--save` | Automatically save the generated style to your user preferences. |

**Examples:**
```bash
# Generate a simple style in the "watercolor" category
python ai_style_generator.py --category watercolor

# Generate a detailed style (name + description) for the "sci_fi" category
python ai_style_generator.py --category sci_fi --detailed

# Generate a random detailed style and save it to preferences
python ai_style_generator.py --detailed --save
```

---

## Common Command Combinations

### Image Preview and Management
```bash
# List all generated images and preview them in the GUI
python wallpaper_generator.py --list-images --gui-preview

# Generate a wallpaper and immediately set it as desktop background
python wallpaper_generator.py --prompt "mountain landscape with lakes" --skip-preview

# Preview the most recently generated wallpaper
python wallpaper_generator.py --preview-latest

# Preview a specific image file using the GUI
python wallpaper_generator.py --preview-image "genimage/abstract_pattern_87654321.png" --gui-preview
```

Below are some practical combinations of command-line options to help you accomplish specific tasks more efficiently:

### Production Wallpaper Generation

```bash
# Generate a 4K wallpaper with a custom prompt
python wallpaper_generator.py --prompt "mountain landscape with lakes at sunset" --resolution 3840x2160

# Generate a dual-monitor wallpaper with ultra-wide aspect ratio
python wallpaper_generator.py --random --aspect-ratio 32:9 --resolution 7680x2160

# Generate a 1080p random wallpaper without applying your saved preferences
python wallpaper_generator.py --random --resolution 1920x1080 --dont-use-user-prefs
```

### Testing and Iteration

```bash
# Preview several random prompts quickly without generating images
python wallpaper_generator.py --random --no-generate

# Test how a prompt would be enhanced with and without your preferences
python wallpaper_generator.py --test-custom-prompt "forest path in autumn" 
python wallpaper_generator.py --test-custom-prompt "forest path in autumn" --dont-use-user-prefs

# Quickly test multiple prompt concepts
python wallpaper_generator.py --test-prompt "ocean"
python wallpaper_generator.py --test-prompt "mountains"
python wallpaper_generator.py --test-prompt "cityscape"
```

### Specialized Use Cases

```bash
# Generate mobile wallpapers
python wallpaper_generator.py --prompt "starry night with silhouette of trees" --aspect-ratio 9:16 --resolution 1080x1920

# Generate square art for social media
python wallpaper_generator.py --prompt "abstract geometric patterns in blue and gold" --aspect-ratio 1:1 --resolution 2048x2048

# Debug issues with prompt generation
python wallpaper_generator.py --prompt "fantasy castle on a floating island" --debug
```

### Advanced Workflows

```bash
# Generate image series with the same settings but different prompts
python wallpaper_generator.py --prompt "winter landscape with snow" --resolution 2560x1440
python wallpaper_generator.py --prompt "spring landscape with cherry blossoms" --resolution 2560x1440
python wallpaper_generator.py --prompt "summer landscape with green fields" --resolution 2560x1440
python wallpaper_generator.py --prompt "autumn landscape with colorful leaves" --resolution 2560x1440

# Test how different aspect ratios affect the same prompt
python wallpaper_generator.py --prompt "sci-fi cityscape" --aspect-ratio 16:9 --no-generate
python wallpaper_generator.py --prompt "sci-fi cityscape" --aspect-ratio 21:9 --no-generate
python wallpaper_generator.py --prompt "sci-fi cityscape" --aspect-ratio 1:1 --no-generate
```

---

## Troubleshooting

Common issues when using the command line interface:

### API Key Issues

**Issue**: `Error: Gemini API key not found or invalid`

**Solution**: 
1. Make sure you have set up your Gemini API key correctly
2. Check that the `.env` file exists in the application directory with the correct `GEMINI_API_KEY=your_key_here` format
3. Try regenerating your API key from the Google AI Studio if the error persists

### Prompt Generation Failures

**Issue**: `Error: Failed to generate prompt with Gemini API`

**Solution**:
1. Check your internet connection
2. Verify your API key hasn't expired or reached its quota limit
3. Try using the `--debug` flag to get more detailed error information
4. Consider using `--dont-use-user-prefs` if your custom preferences are causing issues

### Resolution and Aspect Ratio Issues

**Issue**: `Invalid resolution format. Use WIDTHxHEIGHT (e.g., 1920x1080)`

**Solution**:
1. Make sure you're using the correct format (e.g., `1920x1080`)
2. Don't use spaces around the 'x'
3. Use whole numbers for both width and height

**Issue**: `Invalid aspect ratio format. Use W:H (e.g., 16:9)`

**Solution**:
1. Use the format `width:height` (e.g., `16:9`)
2. Don't use spaces around the colon
3. Use whole numbers for both width and height values

### Command Combination Issues

**Issue**: Using conflicting options like `--prompt` and `--random` together

**Solution**:
1. Use only one prompt source option at a time (`--prompt`, `--random`, `--test-prompt`, or `--test-custom-prompt`)
2. Check the examples in this guide for valid combinations

### Miscellaneous Issues

**Issue**: `Error: Image generation failed`

**Solution**:
1. Check that you have the correct dependencies installed (especially Stability API SDK)
2. Verify your internet connection
3. Make sure your prompt doesn't contain content that might be rejected by the image generation API
4. Use the `--debug` flag to get more detailed error information

**Issue**: Application hangs during prompt generation

**Solution**:
1. API calls may take time, especially when servers are busy
2. If it takes more than 1-2 minutes, try pressing Ctrl+C once to interrupt
3. Try again with a simpler prompt or using `--dont-use-user-prefs`
4. Check your internet connection

**Issue**: `PermissionError` when saving generated images

**Solution**:
1. Make sure the application has write permissions for the output directory
2. Check if the output file is open in another application
3. Try running the application with appropriate permissions

---

<div align="center">
<p>For persistent issues not covered here, please check the logs using the <code>--debug</code> flag and refer to the project's issue tracker or discussion forum for additional support.</p>

![Command Reference](https://img.shields.io/badge/Command-Reference-1f425f.svg?style=flat-square)
![Image Generator](https://img.shields.io/badge/Image-Generator-purple?style=flat-square)
![Last Updated](https://img.shields.io/badge/Last%20Updated-March%202025-orange?style=flat-square)
</div> <environment_details>
# VSCode Visible Files
docs/getting-started.md

# VSCode Open Tabs
docs/user-guide.md
docs/getting-started.md
docs/command-line-guide.md

# Current Time
5/2/2025, 10:20:59 AM (Asia/Qatar, UTC+3:00)

# Current Mode
ACT MODE
</environment_details>
