# Troubleshooting Guide

## Common Issues

### API Related

1. **Invalid API Key**
   ```
   Error: Invalid API key provided
   ```
   **Solution:**
   - Verify your API key is correctly set in environment variables
   - Check if the API key is still valid
   - Ensure you're using the correct API key format

2. **Rate Limit Exceeded**
   ```
   Error: Rate limit exceeded
   ```
   **Solution:**
   - Wait for rate limit to reset
   - Check your current usage in Google AI Studio
   - Consider upgrading your plan

### Generation Issues

1. **Generation Failed**
   ```
   Error: Image generation failed
   ```
   **Solution:**
   - Check your internet connection
   - Verify prompt length and content
   - Try simplifying the prompt
   - Check API status

2. **Low Quality Results**
   **Solution:**
   - Use more detailed prompts
   - Specify technical parameters
   - Check resolution settings
   - Review style settings

### System Issues

1. **Cache Directory Error**
   ```
   Error: Cannot access cache directory
   ```
   **Solution:**
   - Check directory permissions
   - Verify disk space
   - Clear cache manually if needed

2. **Multi-Monitor Issues**
   **Solution:**
   - Check display settings
   - Verify resolution settings
   - Update monitor configuration
   - Reset wallpaper settings

## Debug Mode

Enable debug mode for detailed logs:
```bash
export DEBUG_MODE=true
python wallpaper_generator.py
```

## Getting Help

1. Check the [FAQ](faq.md) for quick answers
2. Review error messages in the log file
3. Open an issue on GitHub with:
   - Error message
   - Steps to reproduce
   - System information
   - Log file contents 