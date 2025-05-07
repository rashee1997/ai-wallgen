#!/usr/bin/env python3
"""Prompt Generator Package - Functions for generating AI wallpaper prompts

This package contains modules for generating and enhancing prompts using
the Gemini API, random tags, and custom user input. It supports using user
preferences or generating prompts independently of user preferences.
"""
# Re-export public API for backward compatibility
from .core import (
    set_prompt_preferences,
    generate_prompt_gemini,
    generate_prompt_random,
    enhance_custom_prompt,
    SimplePrefs
)
from .settings_utils import (
    flatten_settings,
    dynamic_technical_context
)
from .formatters import (
    enforce_prompt_format
)
from .tag_utils import (
    select_random_tags,
    generate_random_style_mix
)
from .negative_prompt import (
    enhance_negative_prompt,
    infer_subject_negatives_gemini
)

# For backward compatibility at the module level
from .core import prompt_cache, gemini_model_name, use_user_preferences
