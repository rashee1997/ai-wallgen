#!/usr/bin/env python3
"""Prompt Generator Package - Functions for generating AI wallpaper prompts

This package contains modules for generating and enhancing prompts using
the Gemini API, random tags, and custom user input. It supports using user
preferences or generating prompts independently of user preferences.
"""
# Re-export public API for backward compatibility
from wall_gen.prompt_modules.core import (
    set_prompt_preferences,
    generate_prompt_gemini,
    generate_prompt_random,
    enhance_custom_prompt,
    SimplePrefs
)
from wall_gen.prompt_modules.settings_utils import (
    flatten_settings,
    dynamic_technical_context
)
from wall_gen.prompt_modules.formatters import (
    enforce_prompt_format
)
from wall_gen.prompt_modules.tag_utils import (
    select_random_tags,
    generate_random_style_mix
)
from wall_gen.prompt_modules.negative_prompt import (
    enhance_negative_prompt,
    infer_subject_negatives_gemini
)

# For backward compatibility at the module level
from wall_gen.prompt_modules.core import prompt_cache, use_user_preferences
