#!/usr/bin/env python3
"""Logo prompt enhancement functionality.

This module provides specialized enhancement for logo generation prompts,
with support for brand identity, typography, and design elements.
"""

import logging
from typing import Any, Dict, Optional, Union

from .base import BasePromptEnhancer, PromptEnhancementError, ValidationError

class LogoPromptEnhancer(BasePromptEnhancer):
    """Enhancer specifically for logo generation prompts."""

    def _validate_logo_input(self, prompt: str, tag_lines: Optional[str] = None) -> None:
        """Validate logo-specific input parameters.

        Args:
            prompt: The main logo text/brand name.
            tag_lines: Optional taglines for the logo.

        Raises:
            ValidationError: If the input parameters are invalid.
        """
        super()._validate_input(prompt)
        if tag_lines is not None and not isinstance(tag_lines, str):
            raise ValidationError("tag_lines must be a string if provided")

    def _extract_logo_preferences(self) -> Dict[str, Any]:
        """Extract logo-specific preferences from user_prefs.

        Returns:
            Dict[str, Any]: Dictionary of logo-specific preferences.
        """
        prefs = self._extract_preferences()
        
        # Extract logo template data if available
        logo_template = getattr(self.user_prefs, 'logo_template_data', {})
        if logo_template and isinstance(logo_template, dict):
            prefs.update({
                'prompt_structure': logo_template.get('imagen3_prompt_structure', ''),
                'negative_prompt_suggestions': logo_template.get('negative_prompt_suggestions', ''),
                'logo_style_description': logo_template.get('logo_style_description', ''),
                'key_elements_guidance': logo_template.get('key_elements_guidance', ''),
                'color_palette_guidance': logo_template.get('color_palette_guidance', ''),
                'typography_guidance': logo_template.get('typography_guidance', ''),
                'composition_guidance': logo_template.get('composition_guidance', ''),
                'description': logo_template.get('description', ''),
                'moods': logo_template.get('moods', []),
                'aspect_ratio': logo_template.get('aspect_ratio', '1:1'),  # Default for logos
                'resolution': logo_template.get('imagen_settings', {}).get(
                    'quality_settings', {}).get('resolution', '1024x1024')  # Default for logos
            })

        return prefs

    def _construct_logo_instruction(self, prompt: str, tag_lines: Optional[str],
                                  prefs: Dict[str, Any], use_structured_format: bool = False) -> str:
        """Construct the instruction for logo prompt enhancement.

        Args:
            prompt: The main logo text/brand name.
            tag_lines: Optional taglines for the logo.
            prefs: Extracted preferences dictionary.
            use_structured_format: Whether to use structured format.

        Returns:
            str: The constructed instruction string.
        """
        # Common elements
        logo_style = prefs.get('logo_style_description', '')
        key_elements = prefs.get('key_elements_guidance', '')
        color_guidance = prefs.get('color_palette_guidance', '')
        typography = prefs.get('typography_guidance', '')
        composition = prefs.get('composition_guidance', '')
        description = prefs.get('description', '')
        moods = prefs.get('moods', [])

        if use_structured_format:
            return f"""
**Logo Text/Initials:** {prompt}{f', {tag_lines}' if tag_lines else ''}
**Core Concept/Industry:** [Synthesize brand essence from inputs]
**Style Description:** {logo_style or 'Create a versatile, professional logo design'}
**Key Visual Elements:** {key_elements or 'Focus on clean lines and essential forms'}
**Color Palette:** {color_guidance or 'Suggest a professional color palette with specific hex codes'}
**Typography Style:** {typography or f'Clean, modern font for "{prompt}"'}{f' and "{tag_lines}"' if tag_lines else ''}
**Composition Guidance:** {composition or 'Balance all elements harmoniously'}
**Desired Output Format:** Vector illustration, white background, {prefs['resolution']}, {prefs['aspect_ratio']}
**Negative Prompt:** {prefs.get('negative_prompt', '')}
"""
        else:
            return f"""
Given the user's core logo subject/text: "{prompt}"
{f'Associated Taglines: "{tag_lines}"' if tag_lines else ''} 
Preset Description: {description or 'Not specified.'}
Overall Moods: {', '.join(moods) if moods else 'Not specified.'}

🎨 PRIMARY LOGO DESIGN DIRECTIVES 🎨
- Logo Style Concept: {logo_style or 'Focus on a unique and memorable design.'}
- Key Visual Elements: {key_elements or 'Suggest 1-2 core visual elements representing the core concept.'}
- Color Palette Concept: {color_guidance or 'Suggest a suitable color palette.'}
- Typography Concept: {typography or 'Suggest a clean, modern font style.'}
{f'- Tagline Typography & Integration: Integrate "{tag_lines}" harmoniously.' if tag_lines else ''}
- Composition Concept: {composition or 'Emphasize balance and proportion.'}

✨ CREATIVE LOGO DESIGN MISSION ✨
Create a detailed prompt for a professional logo design that captures the essence of "{prompt}".
The final output should be a vector illustration, isolated on a white background.
Resolution: {prefs['resolution']}
Aspect Ratio: {prefs['aspect_ratio']}

🚫 NEGATIVE ELEMENTS TO AVOID:
{prefs.get('negative_prompt', '')}
"""

    def enhance_prompt(self, prompt: str, tag_lines: Optional[str] = None,
                      logo_style: str = "minimalist", logo_color: Optional[str] = None,
                      logo_industry: Optional[str] = None, **kwargs) -> str:
        """Enhance a logo generation prompt.

        Args:
            prompt: The main logo text/brand name.
            tag_lines: Optional taglines or secondary text.
            logo_style: Style template to use.
            logo_color: Primary color for the logo.
            logo_industry: Industry context for design influence.
            **kwargs: Additional keyword arguments.

        Returns:
            str: The enhanced logo prompt.

        Raises:
            PromptEnhancementError: If enhancement fails.
        """
        try:
            # Validate inputs
            self._validate_logo_input(prompt, tag_lines)

            # Extract preferences
            prefs = self._extract_logo_preferences()
            
            # Update preferences with function parameters
            if logo_color:
                prefs['color_palette_guidance'] = f"Use {logo_color} as primary color"
            if logo_industry:
                prefs['description'] = f"Logo for {logo_industry} industry"
            
            # Determine format
            use_structured_format = getattr(self.user_prefs, 'use_structured_logo_prompt_format', False)

            # Construct instruction
            instruction = self._construct_logo_instruction(
                prompt, tag_lines, prefs, use_structured_format
            )

            # Get response from Gemini
            response = self.gemini_client.models.generate_content(
                model=self._get_model_name(),
                contents=instruction
            )

            # Process response
            enhanced_text = self._handle_gemini_response(response)

            # Format final prompt
            return self._format_prompt(
                enhanced_text=enhanced_text,
                original_prompt=prompt,
                resolution=prefs['resolution'],
                aspect_ratio=prefs['aspect_ratio'],
                negative_prompt=prefs.get('negative_prompt', '')
            )

        except Exception as e:
            logging.error(f"Logo prompt enhancement failed: {str(e)}", exc_info=True)
            raise PromptEnhancementError(f"Failed to enhance logo prompt: {str(e)}")
