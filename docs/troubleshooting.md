# Troubleshooting Guide

```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   ████████╗██████╗  ██████╗ ██╗   ██╗██████╗ ██╗     ███████╗              ║
║   ╚══██╔══╝██╔══██╗██╔═══██╗██║   ██║██╔══██╗██║     ██╔════╝              ║
║      ██║   ██████╔╝██║   ██║██║   ██║██████╔╝██║     █████╗                ║
║      ██║   ██╔══██╗██║   ██║██║   ██║██╔══██╗██║     ██╔══╝                ║
║      ██║   ██║  ██║╚██████╔╝╚██████╔╝██████╔╝███████╗███████╗              ║
║      ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═════╝ ╚══════╝╚══════╝              ║
║                                                                            ║
║   Solving Common Issues in Wallgen                                         ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

## Overview

This troubleshooting guide addresses common issues you might encounter when using Wallgen, the AI-powered wallpaper generator. It provides step-by-step solutions to installation, configuration, generation, and usage problems.

## Table of Contents

- [Installation Issues](#installation-issues)
- [API Configuration Problems](#api-configuration-problems)
- [Generation Failures](#generation-failures)
- [Image Quality Issues](#image-quality-issues)
- [Performance Problems](#performance-problems)
- [Setting and Preference Issues](#setting-and-preference-issues)
- [Integration Problems](#integration-problems)
- [Error Messages Reference](#error-messages-reference)
- [Getting Further Help](#getting-further-help)

## Installation Issues

### Python Environment Problems

**Issue**: Unable to create or activate virtual environment

**Solution**:
1. Ensure Python 3.8+ is installed:
   ```bash
   python --version
   ```

2. For venv creation errors:
   ```bash
   # Try installing venv if not included in Python
   python -m pip install --user virtualenv
   
   # On Linux/macOS if your Python is system installed
   sudo apt-get install python3-venv  # For Debian/Ubuntu
   ```

3. For activation errors:
   - On Windows, ensure execution policy allows script execution:
     ```powershell
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
     ```
   - On Linux/macOS, ensure script is executable:
     ```bash
     chmod +x venv/bin/activate
     ```

### Dependency Installation Failures

**Issue**: Unable to install dependencies with pip

**Solution**:
1. Update pip to the latest version:
   ```bash
   python -m pip install --upgrade pip
   ```

2. Try installing dependencies one by one to identify problematic packages:
   ```bash
   pip install colorama
   pip install python-dotenv
   # Continue with other packages...
   ```

3. If specific package installation fails, check for platform-specific requirements:
   ```bash
   # For Linux systems, you might need:
   sudo apt-get install python3-dev
   ```

### OS-Specific Installation Issues

#### Windows

**Issue**: Missing C++ build tools when installing dependencies

**Solution**:
1. Install Visual C++ Build Tools from [Microsoft's Visual Studio Downloads](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Retry installation:
   ```bash
   pip install -r requirements.txt
   ```

#### macOS

**Issue**: SSL certificate verification failed

**Solution**:
1. Navigate to Applications > Python folder
2. Locate and run "Install Certificates.command"
3. Retry installation

#### Linux

**Issue**: Missing system libraries

**Solution**:
```bash
# For Debian/Ubuntu:
sudo apt-get update
sudo apt-get install python3-dev libffi-dev libssl-dev

# For Red Hat/Fedora:
sudo dnf install python3-devel libffi-devel openssl-devel
```

## API Configuration Problems

### API Key Issues

**Issue**: "Invalid API Key" or "API Key Not Found" errors

**Solution**:

For detailed instructions on obtaining and configuring your API key, see the [Getting Started Guide section on API setup](getting-started.md#setting-up-api-access).

If you've already obtained an API key but are experiencing issues:

1. Verify your Gemini API key is valid in [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Check that your key is correctly set up using one of these methods:
   - As an environment variable: `GEMINI_API_KEY=your_api_key_here`
   - In a `.env` file in the project root
3. Restart the application after making changes to ensure the new key is loaded

### API Connection Failures

**Issue**: "Cannot connect to API" or timeout errors

**Solution**:
1. Check your internet connection
2. Verify that [Google's API service](https://status.cloud.google.com/) is operational
3. Try with a direct connectivity test:
   ```python
   import requests
   response = requests.get("https://generativelanguage.googleapis.com/v1beta/models")
   print(response.status_code)  # Should be 200 if connection is good
   ```
4. If behind a proxy or firewall, ensure it allows connections to Google's API endpoints
5. Try setting an increased timeout value:
   ```python
   # In your code or settings
   request_timeout = 30  # Seconds
   ```

### API Rate Limiting

**Issue**: "Rate limit exceeded" errors

**Solution**:
1. Check your [quota usage](https://console.cloud.google.com/apis/dashboard) on Google Cloud Console
2. Implement exponential backoff retry logic:
   ```python
   import time
   
   def api_call_with_retry(func, max_retries=5):
       for attempt in range(max_retries):
           try:
               return func()
           except Exception as e:
               if "rate limit" in str(e).lower():
                   wait_time = 2 ** attempt  # Exponential backoff
                   print(f"Rate limit hit, retrying in {wait_time} seconds...")
                   time.sleep(wait_time)
               else:
                   raise
       raise Exception("Maximum retry attempts reached")
   ```
3. Consider upgrading your API tier if you consistently hit limits

## Generation Failures

### Prompt Rejection

**Issue**: Prompt rejected by the API with safety concerns

**Solution**:

For guidelines on creating effective and compliant prompts, see the [Advanced Features Guide section on effective prompt construction](advanced-features.md#effective-prompt-construction).

If your prompts are being rejected:

1. Review your prompt for potentially problematic content
2. Avoid explicit, violent, or other content that may violate Google's usage policies
3. Try reformulating the prompt to be more generic
4. Use negative prompts to clarify what you don't want included

For information on using negative prompts, see the [Advanced Features Guide section on negative prompts](advanced-features.md#negative-prompts).

### Generation Timeout

**Issue**: Generation takes too long and eventually times out

**Solution**:
1. Try a simpler prompt with fewer details
2. Reduce the resolution in settings:
   ```python
   from wallpaper_settings import get_preferences
   
   prefs = get_preferences()
   prefs.imagen_settings["quality_settings"]["resolution"] = "1920x1080"  # Lower resolution
   prefs.save_preferences()
   ```
3. Check your internet connection stability
4. Increase the timeout setting if your connection is slower:
   ```python
   # In advanced settings
   prefs.system_settings["api_timeout"] = 60  # Seconds
   ```

### Empty or Corrupt Images

**Issue**: Generation completes but produces empty, black, or corrupted images

**Solution**:
1. Check disk space availability (corrupt files may occur when disk is full)
2. Verify write permissions to the output directory
3. Try clearing the image cache:
   ```bash
   # Remove cached images
   rm -rf generated/cache/*
   ```
4. Test with a simple, known-working prompt:
   ```
   A simple landscape with blue sky and green fields
   ```
5. Check if the issue occurs with different output formats (PNG vs JPG)

## Image Quality Issues

### Blurry or Low-Quality Images

**Issue**: Generated images appear blurry or lack detail

**Solution**:
1. Increase the detail level in settings:
   ```python
   prefs.imagen_settings["quality_settings"]["detail_level"] = "maximum_detail"
   ```
2. Add specific detail instructions to your prompt:
   ```
   Highly detailed mountain landscape with intricate textures, sharp details, 8K, photorealistic
   ```
3. Ensure you're using a high enough resolution setting
4. Try different rendering quality settings:
   ```python
   prefs.imagen_settings["quality_settings"]["rendering_quality"] = "enhanced"
   ```

### Style Inconsistency

**Issue**: Generated image style doesn't match what was requested

**Solution**:
1. Make the style more explicit in your prompt:
   ```
   Landscape in the style of [specific artist or style], with clear [style] elements
   ```
2. Use style weights to emphasize the desired style:
   ```python
   from wallgen.style_mixer import mix_styles
   
   custom_style = mix_styles({
       "desired_style": 0.8,
       "secondary_style": 0.2
   })
   ```
3. Add reference to well-known works in that style
4. Use a preset specifically designed for that style

### Unwanted Elements in Images

**Issue**: Images contain unwanted elements not in the prompt

**Solution**:
1. Use negative prompts to explicitly exclude elements:
   ```python
   prefs.imagen_settings["negative_prompt"] = "text, watermark, people, faces, signature, blurry"
   ```
2. Be more specific in your positive prompt about what should be included
3. Try using composition settings to control the image layout:
   ```python
   prefs.imagen_settings["composition_settings"] = {
       "focus": "center",
       "framing": "medium",
       "perspective": "normal"
   }
   ```

## Performance Problems

### Slow Application Startup

**Issue**: Application takes a long time to start

**Solution**:
1. Check for large cache directories:
   ```bash
   du -sh generated/cache
   ```
2. Limit cache size in settings:
   ```python
   prefs.system_settings["cache"]["max_size_mb"] = 1024  # 1GB
   ```
3. Disable unused features in advanced settings
4. Consider using the lightweight mode:
   ```bash
   python wallgen.py --lightweight
   ```

### High Memory Usage

**Issue**: Application uses excessive memory

**Solution**:
1. Limit concurrent operations:
   ```python
   prefs.system_settings["max_concurrent_operations"] = 1
   ```
2. Reduce cache size (as above)
3. Clear history regularly:
   ```python
   from wallpaper_settings import clear_history
   
   clear_history(keep_recent=10)  # Keep only 10 most recent entries
   ```
4. Avoid extremely high resolutions unless needed
5. Use the memory-optimized mode:
   ```bash
   python wallgen.py --memory-optimized
   ```

### Slow Image Generation

**Issue**: Image generation takes longer than expected

**Solution**:
1. Check your internet connection speed
2. Reduce the resolution temporarily for testing
3. Simplify prompts to reduce complexity
4. Monitor system resource usage during generation
5. Clear application cache:
   ```bash
   python wallgen.py --clear-cache
   ```

## Setting and Preference Issues

### Settings Not Saving

**Issue**: Changes to settings don't persist between sessions

**Solution**:
1. Check file permissions in the application directory
2. Ensure settings are saved explicitly:
   ```python
   prefs.save_preferences()
   ```
3. Verify the preferences file exists and is not corrupted:
   ```bash
   cat user_preferences.json
   ```
4. Create a backup of your settings:
   ```python
   from wallpaper_settings import export_settings
   
   export_settings("backup_settings.json")
   ```

### Preset Loading Failures

**Issue**: Unable to load saved presets

**Solution**:
1. Check that the preset file exists:
   ```bash
   ls presets/
   ```
2. Try loading the preset with replace rather than merge:
   ```python
   from wallpaper_settings import load_preset
   
   load_preset("preset_name", merge=False)
   ```
3. Verify preset file integrity:
   ```bash
   python -m json.tool presets/preset_name.json
   ```
4. If corrupted, restore from backup or recreate the preset

### Configuration Conflicts

**Issue**: Multiple settings conflict, causing unexpected behavior

**Solution**:
1. Reset to default settings:
   ```python
   from wallpaper_settings import reset_to_defaults
   
   reset_to_defaults()
   ```
2. Apply changes incrementally to identify conflicting settings
3. Check for outdated presets created with previous versions
4. Use the configuration validator:
   ```python
   from wallpaper_settings import validate_config
   
   issues = validate_config()
   if issues:
       print("Configuration issues:", issues)
   ```

## Integration Problems

### Desktop Integration Issues

**Issue**: Generated wallpapers don't set as desktop background

**Solution**:

#### Windows:
1. Ensure the app has permissions to change system settings
2. Try different wallpaper styles (centered, stretched, etc.):
   ```python
   prefs.wallpaper_settings["fit_mode"] = "stretch"  # Options: center, stretch, fill, fit
   ```
3. Verify the wallpaper file path is accessible
4. Try setting manually using:
   ```python
   from wallgen.system_integration import set_wallpaper
   
   set_wallpaper("path/to/wallpaper.png", mode="center")
   ```

#### Linux:
1. Check which desktop environment you're using:
   ```bash
   echo $XDG_CURRENT_DESKTOP
   ```
2. Install necessary dependencies for your desktop:
   ```bash
   # For GNOME
   sudo apt-get install gnome-tweaks
   
   # For KDE
   sudo apt-get install plasma-desktop
   ```
3. Try using the system command:
   ```python
   import os
   
   if os.environ.get('XDG_CURRENT_DESKTOP') == 'GNOME':
       os.system(f"gsettings set org.gnome.desktop.background picture-uri file://{wallpaper_path}")
   ```

#### macOS:
1. Grant the application necessary permissions
2. Try the direct approach:
   ```python
   import subprocess
   
   applescript = f'''
   tell application "Finder"
   set desktop picture to POSIX file "{wallpaper_path}"
   end tell
   '''
   subprocess.run(["osascript", "-e", applescript])
   ```

### Multi-monitor Setup Issues

**Issue**: Wallpapers don't apply correctly on multi-monitor setups

**Solution**:
1. Configure monitor-specific settings:
   ```python
   prefs.wallpaper_settings["multi_monitor"] = {
       "mode": "individual",  # Options: same, individual, span
       "monitors": {
           "0": {"fit_mode": "fill"},
           "1": {"fit_mode": "center"}
       }
   }
   ```
2. For spanning mode, ensure resolution is sufficient for combined monitors
3. Try system-specific settings based on your OS
4. Identify monitors and their indices:
   ```python
   from wallgen.system_integration import list_monitors
   
   monitors = list_monitors()
   print(monitors)  # Shows available monitors
   ```

## Error Messages Reference

### Common API Errors

| Error Code | Message | Solution |
|------------|---------|----------|
| 400 | Bad Request | Check prompt content and format |
| 401 | Unauthorized | Verify API key is valid and set correctly |
| 403 | Forbidden | Check API key permissions and quota |
| 429 | Too Many Requests | Implement rate limiting and retry logic |
| 500 | Server Error | Wait and retry, check API status |

### Application Error Codes

| Error Code | Description | Solution |
|------------|-------------|----------|
| E001 | Configuration file not found | Recreate default configuration |
| E002 | Invalid preset format | Recreate preset or import from backup |
| E003 | API connection failed | Check internet and API status |
| E004 | Image processing failed | Verify image libraries are installed |
| E005 | Permission denied | Check file/folder permissions |

## Getting Further Help

If you've tried the solutions in this guide and are still experiencing issues:

1. Check the [FAQ](faq.md) for additional common questions
2. Search for your issue on the [project's GitHub repository](https://github.com/yourusername/wallgen/issues)
3. Submit a detailed bug report with:
   - Complete error message
   - Steps to reproduce
   - System information:
     ```bash
     python --version
     pip list
     uname -a  # On Linux/macOS
     systeminfo  # On Windows
     ```
   - Screenshots if applicable

4. For quick troubleshooting, run the diagnostic tool:
   ```bash
   python wallgen.py --diagnose
   ```
   This will generate a report of your system configuration and potential issues.

## See Also

- [Getting Started Guide](getting-started.md)
- [Advanced Features Guide](advanced-features.md)
- [FAQ](faq.md)
- [Quick Reference](../QUICK_REFERENCE.md)

---

<div align="center">
<img src="../asset/logo/gemini.svg" alt="Logo" width="64" height="64">

Documentation last updated: 2024-03-25
</div> 