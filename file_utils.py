"""Utility functions for file operations and prompt-related helpers."""

import os
import hashlib
import re
import logging
import html
import google.generativeai as genai # Needed for extract_subject_from_prompt
from typing import Dict, Any # Needed for deep_update

# Helper function for recursive dictionary update (moved from wallpaper_settings.py)
def deep_update(d, u):
    """Recursively update nested dictionaries."""
    for k, v in u.items():
        if isinstance(v, dict):
            d[k] = deep_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


# Helper function to extract subject from prompt using Gemini
def extract_subject_from_prompt(prompt):
    """Extract the main subject from a prompt using Gemini.

    Args:
        prompt: The prompt to extract the subject from

    Returns:
        A string containing the main subject of the prompt
    """
    # Rely on genai being configured by the caller
    # if not GEMINI_API_KEY: # Removed direct access to GEMINI_API_KEY
    #     logging.warning("No Gemini API key configured, using fallback filename generation")
    #     return None

    try:
        # Use the same approach as generate_prompt_gemini
        # import google.generativeai as genai # Redundant import, removed

        # Set up the model - assuming genai is configured
        model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')

        # Create the analysis request
        analysis_prompt = f"""
        Extract the main subject or theme from this wallpaper description in 2-5 words.
        Only return the extracted subject - no explanations or additional text.
        Make it suitable for use as a filename.

        Description: {prompt}
        """

        # Get the response
        response = model.generate_content(
            contents=analysis_prompt
        )

        if response and hasattr(response, 'candidates') and response.candidates:
            text = response.candidates[0].content.parts[0].text
            subject = text.strip()
            # Clean up any quotes or extra formatting
            subject = subject.replace('"', '').replace("'", "")

            # Sanitize for filename use
            subject = re.sub(r'[^\w\s-]', '', subject.lower())
            subject = re.sub(r'[-\s]+', '_', subject)

            logging.debug(f"Extracted subject from prompt: {subject}")
            return subject
        else:
            logging.warning("Empty response from Gemini for subject extraction")
            return None
    except Exception as e:
        logging.error(f"Error extracting subject with Gemini: {e}")
        return None

# Helper function to create a filename from a prompt (fallback)
def create_filename_from_prompt(prompt, max_length=30):
    """Create a descriptive filename from the prompt.

    Args:
        prompt: The prompt to create a filename from
        max_length: Maximum length of the descriptive part of the filename

    Returns:
        A sanitized, shortened filename based on the prompt
    """
    # Remove special characters and replace spaces with underscores
    sanitized = re.sub(r'[^\w\s-]', '', prompt.lower())
    sanitized = re.sub(r'[-\s]+', '_', sanitized)

    # Truncate to the maximum length
    if len(sanitized) > max_length:
        # Try to cut at a word boundary
        sanitized = sanitized[:max_length].rsplit('_', 1)[0]

    # Add a unique identifier (first 8 chars of the hash)
    hash_object = hashlib.sha256(prompt.encode())
    short_hash = hash_object.hexdigest()[:8]

    return f"{sanitized}_{short_hash}.png"


def get_generated_image_path(prompt):
    """Get the cache path for the generated image."""
    # Try to extract a meaningful subject from the prompt
    # Rely on extract_subject_from_prompt being available (defined above)
    subject = extract_subject_from_prompt(prompt)

    if subject:
        # Use the extracted subject for the filename
        hash_object = hashlib.sha256(prompt.encode()) # FIX: Use hashlib.sha256
        short_hash = hash_object.hexdigest()[:8]
        filename = f"{subject}_{short_hash}.png"
    else:
        # Fall back to the original method
        # Rely on create_filename_from_prompt being available (defined above)
        filename = create_filename_from_prompt(prompt)

    # Ensure the genimage directory exists with absolute path
    genimage_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "genimage")
    try:
        os.makedirs(genimage_dir, exist_ok=True)
        logging.debug(f"Ensuring genimage directory exists at: {genimage_dir}")
    except Exception as e:
        logging.error(f"Error creating genimage directory: {e}")
        # Fallback to relative path if absolute path fails
        genimage_dir = "genimage"
        os.makedirs(genimage_dir, exist_ok=True)

    # Return absolute path to ensure consistency
    return os.path.join(genimage_dir, filename)
