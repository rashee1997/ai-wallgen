#!/usr/bin/env python3
"""Prompt enhancement functionality.

This module provides the main interface for prompt enhancement, automatically
selecting and using the appropriate enhancer based on the prompt type and context.
"""

import logging
from typing import Any, Dict, Optional, Union

from .base import BasePromptEnhancer, PromptEnhancementError
from .logo import LogoPromptEnhancer
from .general import GeneralPromptEnhancer

def create_enhancer(enhancer_type: str = "general", user_prefs: Optional[Any] = None) -> BasePromptEnhancer:
    """Create an appropriate prompt enhancer instance.

    Args:
        enhancer_type: Type of enhancer to create ("logo" or "general").
        user_prefs: Optional user preferences object.

    Returns:
        BasePromptEnhancer: An instance of the appropriate enhancer.

    Raises:
        ValueError: If an invalid enhancer_type is provided.
    """
    if enhancer_type.lower() == "logo":
        return LogoPromptEnhancer(user_prefs)
    elif enhancer_type.lower() == "general":
        return GeneralPromptEnhancer(user_prefs)
    else:
        raise ValueError(f"Invalid enhancer type: {enhancer_type}")

def enhance_prompt(prompt: str, is_logo: bool = False, user_prefs: Optional[Any] = None,
                  **kwargs) -> str:
    """Enhance a prompt using the appropriate enhancer.

    This is the main entry point for prompt enhancement. It automatically selects
    and uses the appropriate enhancer based on the prompt type.

    Args:
        prompt: The prompt to enhance.
        is_logo: Whether this is a logo generation prompt.
        user_prefs: Optional user preferences object.
        **kwargs: Additional keyword arguments to pass to the enhancer.
            For logo prompts:
                - tag_lines: Optional taglines for the logo
                - logo_style: Style template to use
                - logo_color: Primary color for the logo
                - logo_industry: Industry context
            For general prompts:
                - description: Optional description to include

    Returns:
        str: The enhanced prompt.

    Raises:
        PromptEnhancementError: If enhancement fails.
    """
    try:
        # Create appropriate enhancer
        enhancer_type = "logo" if is_logo else "general"
        enhancer = create_enhancer(enhancer_type, user_prefs)

        # Enhance the prompt
        return enhancer.enhance_prompt(prompt, **kwargs)

    except Exception as e:
        logging.error(f"Prompt enhancement failed: {str(e)}", exc_info=True)
        raise PromptEnhancementError(f"Failed to enhance prompt: {str(e)}")

def generate_logo(logo_text: str, tag_lines: Optional[str] = None,
                 logo_style: str = "minimalist", logo_color: Optional[str] = None,
                 logo_industry: Optional[str] = None, save_template: bool = False,
                 user_prefs: Optional[Any] = None, generate_only: bool = False) -> str:
    """Generate a logo prompt string.

    This is a convenience function that wraps the logo prompt enhancement
    functionality with a more intuitive interface specifically for logo generation.

    Args:
        logo_text: The main text/brand name for the logo.
        tag_lines: Optional taglines or secondary text.
        logo_style: Style template to use.
        logo_color: Primary color for the logo.
        logo_industry: Industry context for design influence.
        save_template: Whether to save the generated prompt as a template.
        user_prefs: Optional user preferences object.
        generate_only: If True, only generate the prompt string without image generation.

    Returns:
        str: The generated logo prompt string.

    Raises:
        PromptEnhancementError: If logo prompt generation fails.
    """
    try:
        # Create logo enhancer
        enhancer = create_enhancer("logo", user_prefs)

        # Generate the logo prompt
        prompt = enhancer.enhance_prompt(
            prompt=logo_text,
            tag_lines=tag_lines,
            logo_style=logo_style,
            logo_color=logo_color,
            logo_industry=logo_industry
        )

        if save_template:
            # TODO: Implement template saving logic
            logging.info(f"Save template requested for prompt: {prompt}")

        return prompt

    except Exception as e:
        logging.error(f"Logo generation failed: {str(e)}", exc_info=True)
        raise PromptEnhancementError(f"Failed to generate logo prompt: {str(e)}")
