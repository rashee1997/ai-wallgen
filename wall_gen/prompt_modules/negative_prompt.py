#!/usr/bin/env python3
"""Negative Prompt Module - Functions for handling negative prompts

This module contains functions for working with negative prompts, including
generating, enhancing, and inferring negative prompts for image generation.
"""
import re
import logging
import os
from typing import List, Dict, Any, Optional, Union, Set
from .. import gemini_config # Added for centralized Gemini config
from .types import SimplePrefs # To handle cases where user_prefs might be None

# It's better if UserPreferences can be fetched if not provided.
# Attempting to import get_preferences for this purpose.
try:
    from ..settings_modules import get_preferences as get_global_user_prefs
except ImportError:
    # Fallback if direct import from settings_modules fails
    get_global_user_prefs = None
    logging.warning("Could not import get_preferences from ..settings_modules in negative_prompt.py; user_prefs may need to be passed explicitly.")


def infer_subject_negatives_gemini(positive_prompt: str, user_prefs: Optional[Any] = None) -> List[str]:
    """
    Use Gemini to infer subject-specific negative prompt terms from the positive prompt text.
    Returns a list of negative prompt terms suitable for merging and deduplication.
    Implements caching to avoid repeated calls for the same prompt.
    Now uses selected Gemini model from gemini_config.
    
    Args:
        positive_prompt (str): The positive prompt to infer negatives from
        user_prefs (Optional[Any]): User preferences instance. If None, attempts to fetch globally or uses SimplePrefs.
        
    Returns:
        List[str]: A list of negative prompt terms
    """
    try:
        import google.generativeai as genai
    except ImportError:
        logging.warning("google.generativeai module not found. Some features will be disabled.")
        return []
        
    # Ensure Gemini is initialized
    if not gemini_config.is_initialized():
        if not gemini_config.initialize_gemini_globally():
            logging.error(f"Gemini not initialized for infer_subject_negatives_gemini: {gemini_config.get_last_error()}")
            return []

    # Handle user_prefs
    effective_user_prefs = user_prefs
    if effective_user_prefs is None:
        if get_global_user_prefs:
            effective_user_prefs = get_global_user_prefs()
        if effective_user_prefs is None: # If still None, use SimplePrefs
            effective_user_prefs = SimplePrefs()
            logging.debug("infer_subject_negatives_gemini: using SimplePrefs as user_prefs was None.")


    selected_model_name = gemini_config.get_selected_gemini_model(effective_user_prefs)
    
    # Cache key should now include the selected model name
    cache_key_parts = [positive_prompt, selected_model_name]
    cache_key = "_".join(cache_key_parts) # Simpler cache key

    # Simple in-memory cache to avoid repeated calls for the same prompt
    if not hasattr(infer_subject_negatives_gemini, "_cache"):
        infer_subject_negatives_gemini._cache = {}
    cache = infer_subject_negatives_gemini._cache
    if cache_key in cache: # Use updated cache_key
        logging.debug(f"Using cached subject negatives for prompt with model {selected_model_name}.")
        return cache[cache_key]

    try:
        # genai.configure is handled by gemini_config.initialize_gemini_globally()
        model = genai.GenerativeModel(selected_model_name)
        instruction = f"""
Extract a comma-separated list of 3-8 subject-specific negative prompt terms that should be explicitly avoided for the following positive image generation prompt. 
Focus on subtle, nuanced, and mutually exclusive visual confounders, class confusion, or obvious subject/scene artifacts the model may produce, but do not copy generic negatives (e.g., "blurry, watermark, bad anatomy").
If the subject is an animal, exclude rival/confusing animals or breeds; if a place, exclude different environments or features; for portraits, exclude age/gender confounders, double faces, etc.
Avoid generic artifact terms (e.g., "blurry, watermark, distortion, extra limbs")—only include terms directly related to the prompt's main subject/theme.
Provide only the comma-separated list without any additional explanation or formatting.

Prompt: {positive_prompt}

Negative terms:
"""
        response = model.generate_content(instruction)
        if response.text:
            text = response.text.strip()
            raw_terms = [term.strip().lower() for term in re.split(r',|\n', text) if term.strip()]
            # Remove duplicates while preserving order
            seen = set()
            unique_terms = []
            for term in raw_terms:
                if term not in seen:
                    seen.add(term)
                    unique_terms.append(term)
            logging.debug(f"Subject negatives inferred: {unique_terms} using model {selected_model_name}")
            cache[cache_key] = unique_terms # Use updated cache_key
            return unique_terms
        else:
            logging.warning(f"Gemini returned empty response for subject negatives (model: {selected_model_name}).")
            cache[cache_key] = [] # Use updated cache_key
            return []
    except Exception as e:
        logging.error(f"Error inferring subject negatives with Gemini (model: {selected_model_name}): {e}", exc_info=True)
        cache[cache_key] = [] # Use updated cache_key
        return []


def enhance_negative_prompt(negative_prompt_text: str, user_prefs: Optional[Any] = None) -> str:
    """
    Builds a negative prompt for image generation:
    - Includes up to 7 unique user-provided terms (from comma-separated input)
    - Adds up to 4 unique inferred subject-specific negatives (if present, not redundant), using user_prefs for model selection.
    - Appends vetted technical artifact defaults (if not present): blurry, low quality, nsfw, watermark, out of frame
    The total is capped at 13 entries, priority: user > subject > default, and deduplicated.
    
    Also, prevents "Avoid: ... Avoid: ..." repeat pattern when negative prompt is merged downstream:
    if the final prompt has two "Avoid:" sections, the second is replaced with "AI generated negative prompt:".
    
    Args:
        negative_prompt_text (str): The negative prompt text to enhance
        user_prefs (Optional[Any]): User preferences instance, passed to infer_subject_negatives_gemini.
        
    Returns:
        str: The enhanced negative prompt
    """
    # User terms (allow up to 7)
    user_terms = [t.strip() for t in negative_prompt_text.split(",") if t.strip()]
    user_terms = list(dict.fromkeys(user_terms))[:7]  # Remove duplicates and limit to 7

    # Try to infer up to 4 subject negatives (optional)
    # Pass user_prefs to infer_subject_negatives_gemini
    effective_user_prefs = user_prefs
    if effective_user_prefs is None:
        if get_global_user_prefs:
            effective_user_prefs = get_global_user_prefs()
        if effective_user_prefs is None:
            effective_user_prefs = SimplePrefs()
            logging.debug("enhance_negative_prompt: using SimplePrefs for infer_subject_negatives_gemini.")
            
    try:
        subject_terms = []
        for t in user_terms:
            if t:  # Only try if user terms look like a subject/concept
                nt = infer_subject_negatives_gemini(t, user_prefs=effective_user_prefs) # Pass effective_user_prefs
                if nt:
                    subject_terms.extend(nt)
        # Deduplicate, but add at most 4 not already covered by user
        subject_terms = [
            t for t in subject_terms if t not in user_terms
        ]
        if len(subject_terms) > 4:
            subject_terms = subject_terms[:4]
    except Exception as e:
        logging.warning(f"Error inferring subject negatives: {e}")
        subject_terms = []

    # Technical artifact defaults (these should always be present at least once)
    default_artifact_terms = [
        "blurry", "low quality", "nsfw", "watermark", "out of frame"
    ]
    
    # Combine all terms with priority: user > subject > default
    all_terms = []
    all_terms.extend(user_terms)
    for t in subject_terms:
        if t not in all_terms:
            all_terms.append(t)
    for t in default_artifact_terms:
        if t not in all_terms:
            all_terms.append(t)

    # Final cap at 13
    concise = all_terms[:13]
    negative_prompt = ", ".join(concise)
    return negative_prompt
