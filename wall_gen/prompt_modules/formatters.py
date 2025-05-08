#!/usr/bin/env python3
"""Formatters Module - Functions for formatting prompts

This module contains functions for formatting and standardizing prompts 
to ensure consistency in structure and content.
"""
import re
from typing import Optional


def enforce_prompt_format(prompt: str, resolution: str, aspect_ratio: str, 
                         negative_prompt: str = "") -> str:
    """
    Enforce a consistent format for all prompts to ensure technical parameters are included.
    
    Args:
        prompt (str): The original prompt text
        resolution (str): Resolution setting (e.g., "1920x1080")
        aspect_ratio (str): Aspect ratio setting (e.g., "16:9")
        negative_prompt (str): Negative prompt text
        
    Returns:
        str: A properly formatted prompt that includes all required parameters
    """
    # Start by splitting the prompt into main and negative parts
    main_prompt = prompt
    neg_prompt = negative_prompt
    
    # Check if the prompt already contains a negative prompt section
    if "avoid:" in prompt.lower():
        parts = prompt.lower().split("avoid:")
        main_prompt = parts[0].strip()
        
        # If there's already a negative part, use it (but don't include any resolution/aspect ratio from it)
        if len(parts) > 1:
            neg_part = parts[1].strip()
            
            # Remove any resolution information from the negative part
            if resolution.lower() in neg_part.lower():
                neg_part = re.sub(r'(?i)' + re.escape(resolution) + r'(?:\s+resolution)?', '', neg_part)
            
            # Remove any aspect ratio information from the negative part
            if aspect_ratio.lower() in neg_part.lower():
                neg_part = re.sub(r'(?i)' + re.escape(aspect_ratio) + r'(?:\s+aspect\s+ratio)?', '', neg_part)
            
            # Use this cleaned negative part
            neg_prompt = neg_part
    else:
        # No negative part in the prompt, use main_prompt as is
        main_prompt = prompt
    
    # Clean up the main prompt
    clean_prompt = main_prompt.strip()
    
    # Remove any existing resolution mentions to avoid duplication
    if resolution.lower() in clean_prompt.lower():
        clean_prompt = re.sub(r'(?i)' + re.escape(resolution) + r'(?:\s+resolution)?', '', clean_prompt)
    
    # Remove any existing aspect ratio mentions to avoid duplication
    if aspect_ratio.lower() in clean_prompt.lower():
        clean_prompt = re.sub(r'(?i)' + re.escape(aspect_ratio) + r'(?:\s+aspect\s+ratio)?', '', clean_prompt)
    
    # Remove any trailing placeholder words without values
    clean_prompt = re.sub(r'(?i)resolution\s*$', '', clean_prompt)
    clean_prompt = re.sub(r'(?i)aspect\s+ratio\s*$', '', clean_prompt)
    
    # Clean up any resulting double commas or trailing commas
    clean_prompt = re.sub(r',\s*,', ',', clean_prompt)
    clean_prompt = re.sub(r',\s*$', '', clean_prompt)
    
    # Add resolution to main prompt
    if not clean_prompt.endswith(".") and not clean_prompt.endswith(","):
        clean_prompt += ","
    clean_prompt += f" {resolution} resolution"
    
    # Add aspect ratio to main prompt
    if not clean_prompt.endswith(".") and not clean_prompt.endswith(","):
        clean_prompt += ","
    clean_prompt += f" {aspect_ratio} aspect ratio"
    
    # Clean up any additional trailing commas before adding negative prompt
    clean_prompt = re.sub(r',\s*$', '', clean_prompt)
    
    # Add the negative prompt
    if neg_prompt:
        clean_prompt += f". Avoid: {neg_prompt}"
    
    return clean_prompt


# Patch original function to handle double "Avoid:" with user/AI sections
_original_enforce_prompt_format = enforce_prompt_format


def patched_enforce_prompt_format(prompt: str, resolution: str, aspect_ratio: str, 
                                 negative_prompt: str = "") -> str:
    """
    Patched version of enforce_prompt_format that handles duplicate 'Avoid:' sections by
    replacing the second occurrence with 'AI generated negative prompt'.
    
    Args:
        prompt (str): The original prompt text
        resolution (str): Resolution setting (e.g., "1920x1080")
        aspect_ratio (str): Aspect ratio setting (e.g., "16:9")
        negative_prompt (str): Negative prompt text
        
    Returns:
        str: A properly formatted prompt that includes all required parameters
    """
    formatted = _original_enforce_prompt_format(prompt, resolution, aspect_ratio, negative_prompt)
    # Fix: If duplicate Avoid:, replace second with "AI generated negative prompt:"
    if formatted.lower().count("avoid:") > 1:
        first = formatted.lower().find("avoid:")
        second = formatted.lower().find("avoid:", first + 1)
        if second != -1:
            # Replace just the second occurrence
            formatted = formatted[:second] + "AI generated negative prompt:" + formatted[second+6:]
    return formatted


# Replace the original function with the patched version
enforce_prompt_format = patched_enforce_prompt_format
