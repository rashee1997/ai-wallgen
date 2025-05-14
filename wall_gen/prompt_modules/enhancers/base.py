#!/usr/bin/env python3
"""Base classes for prompt enhancement functionality.

This module provides the base classes and interfaces for prompt enhancement,
including both logo and general prompt enhancement capabilities.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union

from ... import gemini_config
from ..types import SimplePrefs

class PromptEnhancementError(Exception):
    """Base exception for prompt enhancement errors."""
    pass

class GeminiClientError(PromptEnhancementError):
    """Exception raised for Gemini client-related errors."""
    pass

class PreferenceExtractionError(PromptEnhancementError):
    """Exception raised for errors during preference extraction."""
    pass

class ValidationError(PromptEnhancementError):
    """Exception raised for input validation errors."""
    pass

class BasePromptEnhancer(ABC):
    """Abstract base class for prompt enhancers."""

    def __init__(self, user_prefs: Optional[Any] = None):
        """Initialize the prompt enhancer.

        Args:
            user_prefs: Optional user preferences object.
        """
        self.user_prefs = user_prefs or SimplePrefs()
        self.gemini_client = None
        self._initialize_gemini()

    def _initialize_gemini(self) -> None:
        """Initialize the Gemini client.

        Raises:
            GeminiClientError: If Gemini client initialization fails.
        """
        if not gemini_config.is_initialized():
            if not gemini_config.initialize_gemini_globally():
                error_msg = f"Gemini initialization failed: {gemini_config.get_last_error()}"
                logging.error(error_msg)
                raise GeminiClientError(error_msg)
        
        self.gemini_client = gemini_config.get_gemini_client()
        if not self.gemini_client:
            error_msg = "Failed to get Gemini client after initialization"
            logging.error(error_msg)
            raise GeminiClientError(error_msg)

    def _validate_input(self, prompt: str) -> None:
        """Validate the input prompt.

        Args:
            prompt: The input prompt to validate.

        Raises:
            ValidationError: If the input prompt is invalid.
        """
        if not prompt or not isinstance(prompt, str):
            raise ValidationError("Prompt must be a non-empty string")
        if len(prompt.strip()) == 0:
            raise ValidationError("Prompt cannot be empty or whitespace only")

    @abstractmethod
    def enhance_prompt(self, prompt: str, **kwargs) -> str:
        """Enhance the given prompt.

        Args:
            prompt: The prompt to enhance.
            **kwargs: Additional keyword arguments.

        Returns:
            str: The enhanced prompt.

        Raises:
            PromptEnhancementError: If enhancement fails.
        """
        pass

    def _get_model_name(self) -> str:
        """Get the appropriate Gemini model name based on user preferences.

        Returns:
            str: The selected model name.
        """
        return gemini_config.get_selected_gemini_model(self.user_prefs)

    def _handle_gemini_response(self, response: Any) -> str:
        """Handle the response from Gemini API.

        Args:
            response: The response from Gemini API.

        Returns:
            str: The processed response text.

        Raises:
            PromptEnhancementError: If response processing fails.
        """
        if not hasattr(response, 'text') or not response.text:
            raise PromptEnhancementError("Empty or invalid response from Gemini")
        return response.text.strip()

    def _extract_preferences(self) -> Dict[str, Any]:
        """Extract relevant preferences from user_prefs.

        Returns:
            Dict[str, Any]: Dictionary of extracted preferences.

        Raises:
            PreferenceExtractionError: If preference extraction fails.
        """
        try:
            settings = getattr(self.user_prefs, 'imagen_settings', {})
            return {
                'resolution': settings.get('quality_settings', {}).get('resolution', '3840x2160'),
                'aspect_ratio': getattr(self.user_prefs, 'aspect_ratio', '16:9'),
                'negative_prompt': settings.get('negative_prompt', ''),
                'style_settings': settings.get('style_settings', {}),
                'lighting_settings': settings.get('lighting_settings', {}),
                'composition_settings': settings.get('composition_settings', {}),
                'color_settings': settings.get('color_settings', {}),
                'detail_settings': settings.get('detail_settings', {}),
                'environment_settings': settings.get('environment_settings', {})
            }
        except Exception as e:
            raise PreferenceExtractionError(f"Failed to extract preferences: {str(e)}")

    def _format_prompt(self, enhanced_text: str, original_prompt: str,
                      resolution: str, aspect_ratio: str,
                      negative_prompt: str) -> str:
        """Format the final prompt with technical specifications.

        Args:
            enhanced_text: The enhanced prompt text.
            original_prompt: The original input prompt.
            resolution: The desired resolution.
            aspect_ratio: The desired aspect ratio.
            negative_prompt: The negative prompt string.

        Returns:
            str: The formatted prompt string.
        """
        # Ensure original prompt is included
        if original_prompt.lower() not in enhanced_text.lower():
            enhanced_text = f"{original_prompt}, {enhanced_text}"

        # Add resolution and aspect ratio if not present
        if resolution not in enhanced_text:
            enhanced_text += f", {resolution} resolution"
        if aspect_ratio not in enhanced_text:
            enhanced_text += f", {aspect_ratio} aspect ratio"

        # Handle negative prompt
        if negative_prompt:
            if "avoid:" not in enhanced_text.lower():
                enhanced_text += f" Avoid: {negative_prompt}"
            elif negative_prompt not in enhanced_text:
                avoid_idx = enhanced_text.lower().index("avoid:")
                enhanced_text = (
                    enhanced_text[:avoid_idx] +
                    f"Avoid: {negative_prompt}, " +
                    enhanced_text[avoid_idx + 6:]
                )

        return enhanced_text.strip()
