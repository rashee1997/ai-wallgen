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
- [Setting and Preference Issues](#setting-and-preference-issues)
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

### API Rate Limiting

**Issue**: "Rate limit exceeded" errors

**Solution**:
1. Check your [quota usage](https://console.cloud.google.com/apis/dashboard) on Google Cloud Console
2. Wait a few minutes before trying again
3. Consider upgrading your API tier if you consistently hit limits

## Generation Failures

### Prompt Rejection

**Issue**: Prompt rejected by the API with safety concerns

**Solution**:

For guidelines on creating effective and compliant prompts, see the [Advanced Features Guide section on tag-based prompt system](advanced-features.md#tag-based-prompt-system).

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
2. Check your internet connection stability
3. Wait a few minutes before trying again
4. If the issue persists, try using the random generation option

### Empty or Corrupt Images

**Issue**: Generation completes but produces empty, black, or corrupted images

**Solution**:
1. Check disk space availability (corrupt files may occur when disk is full)
2. Verify write permissions to the `genimage/` directory
3. Try clearing the image cache:
   ```bash
   # Remove cached images
   rm -rf genimage/cache/*
   ```
4. Test with a simple, known-working prompt:
   ```
   A simple landscape with blue sky and green fields
   ```

## Image Quality Issues

### Blurry or Low-Quality Images

**Issue**: Generated images appear blurry or lack detail

**Solution**:
1. Use the `--quality` tag in your prompt to request higher quality:
   ```
   A mountain landscape --quality high detail
   ```
2. Try adding more specific details to your prompt
3. Use negative prompts to avoid unwanted elements
4. If the issue persists, try generating multiple times with the same prompt

## Setting and Preference Issues

### Preference Loading Problems

**Issue**: Settings not being saved or loaded correctly

**Solution**:
1. Check file permissions in the project directory
2. Verify the `preferences.json` file exists and is readable
3. Try resetting preferences by deleting the `preferences.json` file
4. Restart the application to reload default settings

### Theme Selection Issues

**Issue**: Unable to select or change themes

**Solution**:
1. Verify that the theme files exist in the `themes/` directory
2. Check file permissions on theme files
3. Try selecting a different theme
4. If the issue persists, try restarting the application

## Error Messages Reference

### Common Error Messages

1. **"API Key Not Found"**
   - Cause: Missing or invalid API key
   - Solution: Set up your API key as described in the [Getting Started Guide](getting-started.md#setting-up-api-access)

2. **"Connection Failed"**
   - Cause: Network issues or API service problems
   - Solution: Check your internet connection and [API service status](https://status.cloud.google.com/)

3. **"Rate Limit Exceeded"**
   - Cause: Too many requests in a short time
   - Solution: Wait a few minutes before trying again

4. **"Invalid Prompt"**
   - Cause: Prompt contains invalid characters or format
   - Solution: Review your prompt and remove any special characters

5. **"Generation Failed"**
   - Cause: API processing error
   - Solution: Try a simpler prompt or wait a few minutes

## Getting Further Help

If you encounter issues not covered here:

1. Check the [Getting Started Guide](getting-started.md) for basic setup instructions
2. Review the [Advanced Features Guide](advanced-features.md) for detailed usage information
3. If problems persist, please report issues on the GitHub repository

---

<div align="center">
<img src="../asset/logo/gemini.svg" alt="Logo" width="64" height="64">

Documentation last updated: 2024-03-25
</div> 