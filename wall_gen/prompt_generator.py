#!/usr/bin/env python3
"""Prompt Generator Module - Functions for generating AI wallpaper prompts

This module contains functions for generating and enhancing prompts using
the Gemini API, random tags, and custom user input. It supports using user
preferences or generating prompts independently of user preferences.
Located within the wall_gen package.
"""
# Standard library imports
import logging
import os

# Re-export all relevant functionality from prompt_modules
# Using absolute imports for better compatibility
from wall_gen.prompt_modules import (
    # Core functionality
    set_prompt_preferences,
    generate_prompt_gemini,
    generate_prompt_random,
    enhance_custom_prompt,

    # Utilities
    flatten_settings,
    dynamic_technical_context,
    enforce_prompt_format,
    select_random_tags,
    generate_random_style_mix,
    enhance_negative_prompt,
    infer_subject_negatives_gemini,

    # SimplePrefs class
    SimplePrefs
)
# For backward compatibility, re-export these variables from the modules
from wall_gen.prompt_modules.core import prompt_cache, use_user_preferences # gemini_model_name removed


# Import configuration using absolute import
from wall_gen.config import (
    nature_tags, space_tags, sea_tags, flowers_tags, urban_tags,
    fantasy_tags, abstract_tags, mood_tags, available_genres,
    PROMPT_INSTRUCTIONS, CUSTOM_PROMPT_INSTRUCTIONS,
    STYLE_CATEGORIES
)


# Import no-preferences prompt instructions using absolute import from within wall_gen
# NOTE: This module assumes no_preferences_prompt.py is part of the wall_gen package.
try:
    from wall_gen.no_preferences_prompt import (
        NO_PREFS_PROMPT_INSTRUCTIONS,
        NO_PREFS_RANDOM_INSTRUCTIONS,
        enforce_art_medium
    )
except ImportError:
    logging.warning("Could not import from wall_gen.no_preferences_prompt. Using default instructions.")
    # Define fallbacks in case import fails
    try:
        # Use instructions from config if available as fallback
        NO_PREFS_PROMPT_INSTRUCTIONS = CUSTOM_PROMPT_INSTRUCTIONS
        NO_PREFS_RANDOM_INSTRUCTIONS = PROMPT_INSTRUCTIONS
    except NameError:
        logging.warning("Could not set fallback prompt instructions.")
        NO_PREFS_PROMPT_INSTRUCTIONS = ""
        NO_PREFS_RANDOM_INSTRUCTIONS = ""
    
    def enforce_art_medium(prompt, original_prompt):
        return prompt

# Import necessary third-party libraries for backward compatibility
try:
    import google.generativeai as genai
except ImportError:
    logging.warning("google.generativeai module not found. Some features will be disabled.")

# Note: Most actual functionality is now in prompt_modules/*
# This file primarily re-exports the API. Further refactoring might merge this into prompt_service.
