#!/usr/bin/env python3
"""Custom Prompt Generator Module - Functions for enhancing custom AI wallpaper prompts

This module contains functions for enhancing custom user-provided prompts with
additional details, style parameters, and technical specifications. It integrates
user preferences into the custom prompts to generate more detailed and consistent results.

This is a transitional module that uses the new enhancer system while maintaining
backward compatibility with existing code.
"""

import logging
from typing import Any, Dict, Optional, Union

from .enhancers import enhance_prompt, generate_logo, PromptEnhancementError
from .formatters import enforce_prompt_format
from .types import SimplePrefs

def enhance_custom_prompt(custom_prompt: str, user_prefs: Optional[Any] = None,
                        description: Optional[str] = None, tag_lines: Optional[str] = None,
                        logo_industry_for_template: Optional[str] = None) -> str:
    """Enhance the custom prompt using the new enhancer system.
    
    This function maintains backward compatibility while using the new enhancer
    modules under the hood.
    
    Args:
        custom_prompt: The original prompt to enhance.
        user_prefs: Optional user preferences object.
        description: Optional description string from preset to include in prompt generation.
        tag_lines: Optional taglines to include in the prompt generation.
        logo_industry_for_template: Optional industry context for logo template generation.
    
    Returns:
        str: An enhanced version of the custom prompt.
    """
    try:
        # Check if this is a logo prompt
        is_logo = bool(logo_industry_for_template or tag_lines)

        if is_logo:
            # Use logo enhancer
            return generate_logo(
                logo_text=custom_prompt,
                tag_lines=tag_lines,
                logo_industry=logo_industry_for_template,
                user_prefs=user_prefs
            )
        else:
            # Use general enhancer
            return enhance_prompt(
                prompt=custom_prompt,
                is_logo=False,
                user_prefs=user_prefs,
                description=description
            )

    except PromptEnhancementError as e:
        logging.error(f"Prompt enhancement failed: {str(e)}")
        # Fallback to basic formatting
        if not user_prefs:
            user_prefs = SimplePrefs()
        
        settings = getattr(user_prefs, 'imagen_settings', {})
        quality_settings = settings.get('quality_settings', {})
        
        resolution = quality_settings.get('resolution', '3840x2160')
        aspect_ratio = getattr(user_prefs, 'aspect_ratio', '16:9')
        negative_prompt = settings.get('negative_prompt', (
            'ugly, disfigured, low quality, blurry, nsfw, watermark, signature, '
            'out of frame, extra limbs, poorly drawn face, twisted limbs, distorted face, '
            'bad proportions, bad anatomy'
        ))
        
        return enforce_prompt_format(custom_prompt, resolution, aspect_ratio, negative_prompt)

    except Exception as e:
        logging.exception(f"Unexpected error in enhance_custom_prompt: {e}")
        return custom_prompt  # Return original prompt as ultimate fallback

def generate_logo_prompt(
    logo_text: str,
    tag_lines: str = None,
    logo_style: str = "minimalist",
    logo_color: str = None,
    logo_industry: str = None,
    save_template: bool = False,
    user_prefs: object = None,
    generate_only: bool = False,
) -> str:
    """Generate a logo prompt string based on inputs and user preferences.
    
    This function maintains backward compatibility while using the new logo
    enhancer under the hood.

    Args:
        logo_text: The main text/brand name for the logo.
        tag_lines: Optional taglines or secondary text.
        logo_style: Style template to use.
        logo_color: Primary color for the logo.
        logo_industry: Industry context for design influence.
        save_template: Whether to save the generated prompt as a template.
        user_prefs: User preferences object.
        generate_only: If True, only generate the prompt string without image generation.

    Returns:
        str: The generated logo prompt string.
    """
    try:
        return generate_logo(
            logo_text=logo_text,
            tag_lines=tag_lines,
            logo_style=logo_style,
            logo_color=logo_color,
            logo_industry=logo_industry,
            save_template=save_template,
            user_prefs=user_prefs,
            generate_only=generate_only
        )
    except PromptEnhancementError as e:
        logging.error(f"Logo generation failed: {str(e)}")
        # Fallback to basic formatting with logo-specific defaults
        if not user_prefs:
            user_prefs = SimplePrefs()
        
        settings = getattr(user_prefs, 'imagen_settings', {})
        quality_settings = settings.get('quality_settings', {})
        
        resolution = quality_settings.get('resolution', '1024x1024')  # Logo-specific default
        aspect_ratio = getattr(user_prefs, 'aspect_ratio', '1:1')  # Logo-specific default
        negative_prompt = settings.get('negative_prompt', (
            'ugly, disfigured, low quality, blurry, nsfw, watermark, signature, '
            'out of frame, poorly drawn, bad proportions'
        ))
        
        return enforce_prompt_format(logo_text, resolution, aspect_ratio, negative_prompt)

    except Exception as e:
        logging.exception(f"Unexpected error in generate_logo_prompt: {e}")
        return logo_text  # Return original text as ultimate fallback
