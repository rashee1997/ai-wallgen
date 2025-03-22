# Frequently Asked Questions

## General Questions

### Q: What is AI Wallpaper Generator?
A: It's a tool that uses Google's Imagen 3 AI model to generate custom wallpapers based on text descriptions or prompts.

### Q: Is it free to use?
A: The tool itself is free and open source, but you need a Gemini API key. Google offers a free trial with 100 generations per month.

### Q: Which operating systems are supported?
A: The tool works on Linux, Windows, and macOS.

## API and Usage

### Q: How do I get an API key?
A: Visit [Google AI Studio](https://makersuite.google.com/app/apikey) to get your API key. See our [API Setup Guide](api-setup.md) for details.

### Q: What are the API usage limits?
A: Free tier includes 100 generations/month. Paid tiers offer higher limits. Check [API Setup Guide](api-setup.md) for current limits.

### Q: Can I use the generated images commercially?
A: Check Google's terms of service for commercial usage rights. Generally, you own the images you generate.

## Technical Questions

### Q: What's the maximum resolution?
A: The tool supports up to 8K resolution, but actual limits may depend on your API tier.

### Q: Does it support multiple monitors?
A: Yes, the tool supports multi-monitor setups with individual settings for each display.

### Q: How does the caching system work?
A: Generated images and prompts are cached locally to improve performance and reduce API calls.

## Troubleshooting

### Q: Why are my images not generating?
A: Common reasons include:
- Invalid API key
- Rate limit exceeded
- Network issues
- Invalid prompt

### Q: How can I improve image quality?
A: Try:
- Using more detailed prompts
- Specifying technical parameters
- Using higher resolution settings
- Following our [Prompt Engineering Guide](prompt-engineering.md)

### Q: Where are the generated images stored?
A: Images are saved in the `genimage` directory by default.

## Development

### Q: Can I contribute to the project?
A: Yes! Check our [Contributing Guide](contributing.md) for guidelines.

### Q: How can I report bugs?
A: Open an issue on GitHub with:
- Detailed description
- Steps to reproduce
- Error messages
- System information 