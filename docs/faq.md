# Frequently Asked Questions

```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   ███████╗ █████╗  ██████╗                                                 ║
║   ██╔════╝██╔══██╗██╔═══██╗                                                ║
║   █████╗  ███████║██║   ██║                                                ║
║   ██╔══╝  ██╔══██║██║▄▄ ██║                                                ║
║   ██║     ██║  ██║╚██████╔╝                                                ║
║   ╚═╝     ╚═╝  ╚═╝ ╚══▀▀═╝                                                 ║
║                                                                            ║
║   Frequently Asked Questions About Wallgen                                 ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

## General Questions

### What is Wallgen?

Wallgen is a terminal-based AI wallpaper generator that uses Google's Gemini API to create wallpapers from text prompts. It allows you to generate custom wallpapers based on your descriptions without requiring artistic skills.

### What are the system requirements?

For detailed system requirements, see the [Getting Started Guide](getting-started.md#prerequisites).

### Do I need an API key?

Yes, Wallgen requires a Google Gemini API key to function. For detailed instructions on obtaining and setting up your API key, see the [Getting Started Guide](getting-started.md#setting-up-api-access).

### Is it free to use?

Wallgen itself is free and open-source software. However, you'll need a Google Gemini API key which may have free tier limitations or costs depending on usage.

## Prompt-Related Questions

### How do I create effective prompts?

For guidance on creating effective prompts, see the [Advanced Features Guide](advanced-features.md#effective-prompt-construction).

### Can I use negative prompts?

Yes, negative prompts tell the AI what to avoid in the generated image. For details on using negative prompts, see the [Advanced Features Guide](advanced-features.md#negative-prompts).

### Why are my images not matching my prompts?

There could be several reasons:

1. The prompt might be too vague
2. The API may have content filters blocking certain elements
3. The AI model may interpret your prompt differently than intended

Try providing more specific details in your prompts and checking for any terminology that might trigger content filters.

### Does the model understand all art styles?

The Gemini model understands many art styles, but results may vary. Common styles like "digital art," "oil painting," "watercolor," and "photorealistic" generally produce good results. Highly specific or niche styles may not be interpreted as accurately.

## Technical Questions

### Where are generated wallpapers saved?

All generated wallpapers are saved to the `generated/` directory in the Wallgen project folder with a timestamp and theme identifier in the filename.

### What resolutions can I generate?

You can specify various resolutions when generating wallpapers, with the available options depending on your API tier. For information on specifying resolution, see the [Advanced Features Guide](advanced-features.md#resolution-settings).

### How do I run Wallgen from the command line?

For a complete reference of command-line options and examples, see the [Quick Reference Guide](QUICK_REFERENCE.md#command-line-options).

### What happens if the API is unavailable?

If the API is unavailable or returns an error:

1. Wallgen will display an appropriate error message
2. No image will be generated
3. You can try again later or check your internet connection

For troubleshooting API connection issues, see the [Troubleshooting Guide](troubleshooting.md#api-connection-issues).

## Error and Troubleshooting

### I'm getting "API Key Invalid" errors

For solutions to API key issues, see the [Troubleshooting Guide](troubleshooting.md#api-key-issues).

### Why is generation sometimes slow?

Image generation speed depends on several factors:

1. Your internet connection speed
2. Current load on the Google Gemini API servers
3. Complexity of your prompt
4. Current API rate limits on your account

Most generations should complete within 10-30 seconds under normal conditions.

### How do I report bugs or suggest features?

For information on contributing to Wallgen, including bug reports and feature requests, see the [Contributing Guide](../CONTRIBUTING.md).

## See Also

- [Getting Started Guide](getting-started.md)
- [User Guide](user-guide.md)
- [Advanced Features Guide](advanced-features.md)
- [Troubleshooting Guide](troubleshooting.md)
- [Quick Reference Guide](QUICK_REFERENCE.md)

---

<div align="center">
<img src="../asset/logo/gemini.svg" alt="Logo" width="64" height="64">

Documentation last updated: 2024-03-25
</div> 