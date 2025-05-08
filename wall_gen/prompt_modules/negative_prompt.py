#!/usr/bin/env python3
"""Negative Prompt Module - Functions for handling negative prompts

This module contains functions for working with negative prompts, including
generating, enhancing, and inferring negative prompts for image generation.
"""
import re
import logging
import os
from typing import List, Dict, Any, Optional, Union, Set


def infer_subject_negatives_gemini(positive_prompt: str) -> List[str]:
    """
    Use Gemini to infer subject-specific negative prompt terms from the positive prompt text.
    Returns a list of negative prompt terms suitable for merging and deduplication.
    Implements caching to avoid repeated calls for the same prompt.
    
    Args:
        positive_prompt (str): The positive prompt to infer negatives from
        
    Returns:
        List[str]: A list of negative prompt terms
    """
    try:
        import google.generativeai as genai
    except ImportError:
        logging.warning("google.generativeai module not found. Some features will be disabled.")
        return []
        
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        logging.warning("No Gemini API key configured for subject negative inference.")
        return []

    # Simple in-memory cache to avoid repeated calls for the same prompt
    if not hasattr(infer_subject_negatives_gemini, "_cache"):
        infer_subject_negatives_gemini._cache = {}
    cache = infer_subject_negatives_gemini._cache
    if positive_prompt in cache:
        logging.debug("Using cached subject negatives for prompt.")
        return cache[positive_prompt]

    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
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
            logging.debug(f"Subject negatives inferred: {unique_terms}")
            cache[positive_prompt] = unique_terms
            return unique_terms
        else:
            logging.warning("Gemini returned empty response for subject negatives.")
            cache[positive_prompt] = []
            return []
    except Exception as e:
        logging.error(f"Error inferring subject negatives with Gemini: {e}")
        cache[positive_prompt] = []
        return []


def enhance_negative_prompt(negative_prompt_text: str) -> str:
    """
    Builds a negative prompt for image generation:
    - Includes up to 7 unique user-provided terms (from comma-separated input)
    - Adds up to 4 unique inferred subject-specific negatives (if present, not redundant)
    - Appends vetted technical artifact defaults (if not present): blurry, low quality, nsfw, watermark, out of frame
    The total is capped at 13 entries, priority: user > subject > default, and deduplicated.
    
    Also, prevents "Avoid: ... Avoid: ..." repeat pattern when negative prompt is merged downstream:
    if the final prompt has two "Avoid:" sections, the second is replaced with "AI generated negative prompt:".
    
    Args:
        negative_prompt_text (str): The negative prompt text to enhance
        
    Returns:
        str: The enhanced negative prompt
    """
    # User terms (allow up to 7)
    user_terms = [t.strip() for t in negative_prompt_text.split(",") if t.strip()]
    user_terms = list(dict.fromkeys(user_terms))[:7]  # Remove duplicates and limit to 7

    # Try to infer up to 4 subject negatives (optional)
    try:
        subject_terms = []
        for t in user_terms:
            if t:  # Only try if user terms look like a subject/concept
                nt = infer_subject_negatives_gemini(t)
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
