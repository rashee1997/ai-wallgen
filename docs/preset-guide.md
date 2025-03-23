# Note About Preset Management

This document was previously created to document the preset management system. However, the preset management functionality is not currently implemented in the Wallgen codebase.

## Current Status

At present, Wallgen has a simplified approach to wallpaper generation that does not include:
- Saving or loading presets
- Preset management menus
- Preset inheritance or export options

## Alternative Approaches

Instead of using presets, you can:

1. **Use command-line arguments** to specify your preferred settings each time:
   ```bash
   python wallgen.py --prompt "forest scene" --resolution "1920x1080"
   ```

2. **Document effective prompts** that you've used in the past for reference

## Future Development

Preset management is on the roadmap for future development. When implemented, this guide will be updated with accurate information on how to:
- Save your current settings as named presets
- Load presets
- Manage and organize your presets

---

<div align="center">
<img src="../asset/logo/gemini.svg" alt="Logo" width="64" height="64">

Documentation last updated: 2024-03-25 