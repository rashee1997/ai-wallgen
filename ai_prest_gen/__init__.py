"""
AI Preset Generation Package (`ai_prest_gen`).

This package encapsulates all modules related to the generation of AI-driven
wallpaper presets for the AI Wallpaper Generator project. It includes functionalities
for style categorization, template management, Gemini AI interaction, and
preset configuration.

Key submodules:
- `ai_preset_generator`: The main orchestrator for preset generation.
- `style_category_catalog`: Handles style detection and AI instruction loading.
- `style_templates`: Dispatches to various specialized style template modules.
- `gemini_config_preset`: Manages Gemini API setup for this package.
- `camera_settings`: Provides dynamic camera configurations.
- `*_style_templates.py`: Collections of specific style templates.
- `catalog_data/`: Directory containing JSON data for style keywords, rules,
  and AI instructions.
"""

# This file makes ai_prest_gen a Python package
