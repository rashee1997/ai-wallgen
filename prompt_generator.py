#!/usr/bin/env python3
"""Prompt Generator Module - Functions for generating AI wallpaper prompts

This module contains functions for generating and enhancing prompts using
the Gemini API, random tags, and custom user input. It supports using user
preferences or generating prompts independently of user preferences.
"""
# Standard library imports
import logging
import os

# Re-export all relevant functionality from prompt_modules
from prompt_modules import (
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
from prompt_modules.core import prompt_cache, gemini_model_name, use_user_preferences

# Import configuration for backward compatibility
try:
    from config import (
        nature_tags, space_tags, sea_tags, flowers_tags, urban_tags,
        fantasy_tags, abstract_tags, mood_tags, available_genres,
        PROMPT_INSTRUCTIONS, CUSTOM_PROMPT_INSTRUCTIONS,
        STYLE_CATEGORIES
    )
except ImportError:
    logging.warning("Could not import some configuration items from config.py")

# Import no-preferences prompt instructions for backward compatibility
try:
    from no_preferences_prompt import (
        NO_PREFS_PROMPT_INSTRUCTIONS,
        NO_PREFS_RANDOM_INSTRUCTIONS,
        enforce_art_medium
    )
except ImportError:
    logging.warning("no_preferences_prompt.py not found. Using default instructions.")
    # Define fallbacks in case import fails
    try:
        NO_PREFS_PROMPT_INSTRUCTIONS = CUSTOM_PROMPT_INSTRUCTIONS
        NO_PREFS_RANDOM_INSTRUCTIONS = PROMPT_INSTRUCTIONS
    except NameError:
        logging.warning("Could not set fallback prompt instructions.")
        NO_PREFS_PROMPT_INSTRUCTIONS = ""
        NO_PREFS_RANDOM_INSTRUCTIONS = ""
    
    # Define a simple fallback enforce_art_medium function if import fails
    def enforce_art_medium(prompt, original_prompt):
        return prompt  # Simply return prompt unchanged if module not found

# Import necessary third-party libraries for backward compatibility
try:
    import google.generativeai as genai
except ImportError:
    logging.warning("google.generativeai module not found. Some features will be disabled.")

# Note: Most actual functionality is now in prompt_modules/*
# This file simply re-exports the API for backward compatibility.
