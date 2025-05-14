#!/usr/bin/env python3
"""General prompt enhancement functionality.

This module provides enhancement for general (non-logo) prompts, with support
for artistic styles, technical parameters, and comprehensive scene descriptions.
"""

import logging
from typing import Any, Dict, List, Optional, Set, Union

from .base import BasePromptEnhancer, PromptEnhancementError

class GeneralPromptEnhancer(BasePromptEnhancer):
    """Enhancer for general (non-logo) prompts."""

    # Default negative prompt
    DEFAULT_NEGATIVE_PROMPT = (
        "ugly, disfigured, low quality, blurry, nsfw, watermark, signature, "
        "out of frame, extra limbs, poorly drawn face, twisted limbs, distorted face, "
        "bad proportions, bad anatomy"
    )

    # Art medium mapping for negative prompt handling
    ART_MEDIUMS = {
        "watercolor": ["3d", "3d render", "3d art", "digital art", "oil painting", "acrylic", "photograph"],
        "oil painting": ["3d", "3d render", "3d art", "digital art", "watercolor", "acrylic", "photograph"],
        "sketch": ["3d", "3d render", "3d art", "digital art", "oil painting", "acrylic", "photograph"],
        "pencil": ["3d", "3d render", "3d art", "digital art", "oil painting", "acrylic", "photograph"],
        "acrylic": ["3d", "3d render", "3d art", "oil painting", "watercolor", "photograph"],
        "drawing": ["3d", "3d render", "3d art", "digital art", "oil painting", "acrylic", "photograph"],
        "illustration": ["3d", "3d render", "3d art", "photograph"],
        "photograph": ["3d", "3d render", "3d art", "digital art", "oil painting", "acrylic", "watercolor"],
        "3d": ["oil painting", "watercolor", "acrylic", "pencil", "sketch", "drawing", "photograph"],
        "digital art": ["oil painting", "watercolor", "acrylic", "pencil", "sketch", "photograph"],
    }

    def _detect_art_medium(self, prompt: str) -> Optional[str]:
        """Detect art medium mentioned in the prompt.

        Args:
            prompt: The input prompt.

        Returns:
            Optional[str]: Detected art medium or None.
        """
        prompt_lower = prompt.lower()
        for medium in self.ART_MEDIUMS:
            if medium.lower() in prompt_lower:
                return medium
        return None

    def _update_negative_prompt(self, negative_prompt: str, detected_medium: Optional[str]) -> str:
        """Update negative prompt based on detected art medium.

        Args:
            negative_prompt: Current negative prompt.
            detected_medium: Detected art medium.

        Returns:
            str: Updated negative prompt.
        """
        if not detected_medium:
            return negative_prompt or self.DEFAULT_NEGATIVE_PROMPT

        # Convert current negative prompt to set of terms
        current_terms: Set[str] = {
            term.strip() for term in negative_prompt.split(',')
            if term.strip()
        }

        # Add competing mediums to negative terms
        competing_mediums = self.ART_MEDIUMS.get(detected_medium, [])
        current_terms.update(competing_mediums)

        # Convert back to string
        return ", ".join(sorted(current_terms)) or self.DEFAULT_NEGATIVE_PROMPT

    def _construct_enhancement_instruction(self, prompt: str, prefs: Dict[str, Any],
                                        detected_medium: Optional[str]) -> str:
        """Construct the instruction for general prompt enhancement.

        Args:
            prompt: The input prompt.
            prefs: Extracted preferences.
            detected_medium: Detected art medium.

        Returns:
            str: The constructed instruction string.
        """
        # Extract settings from preferences
        style_settings = prefs.get('style_settings', {})
        lighting_settings = prefs.get('lighting_settings', {})
        composition_settings = prefs.get('composition_settings', {})
        color_settings = prefs.get('color_settings', {})
        detail_settings = prefs.get('detail_settings', {})
        environment_settings = prefs.get('environment_settings', {})

        # Construct medium-specific instruction if needed
        medium_instruction = ""
        if detected_medium:
            medium_instruction = f"""
CRITICAL: This prompt explicitly mentions the art medium "{detected_medium}".
You MUST preserve this EXACT medium in your enhancement.
DO NOT convert it to any other medium (especially not 3D or digital art if traditional medium was specified).
Use terminology specific to {detected_medium} in your enhancement.
The negative prompt has been configured to exclude competing art styles.
"""

        return f"""ENHANCE THIS EXACT PROMPT: "{prompt}"

CRITICAL INSTRUCTION:
If this prompt specifies ANY artistic medium (watercolor, oil painting, 3D, digital art, etc.), you MUST PRESERVE IT EXACTLY.
DO NOT convert between mediums - a watercolor must stay watercolor, an oil painting must stay oil painting, etc.
{medium_instruction}

SUBJECT ANALYSIS:
Carefully analyze the subject "{prompt}" and tailor your enhancement while STRICTLY PRESERVING the original content:
- For natural subjects: emphasize organic elements, textures, and environmental context
- For urban subjects: focus on architectural details, perspective, and urban atmosphere
- For abstract subjects: highlight patterns, shapes, and conceptual elements
- For space/cosmic subjects: emphasize scale, wonder, and celestial phenomena
- For fantasy subjects: create a cohesive magical or surreal atmosphere

MANDATORY TECHNICAL PARAMETERS:
Resolution: {prefs['resolution']} - YOU MUST INCLUDE THIS IN YOUR FINAL PROMPT
Aspect Ratio: {prefs['aspect_ratio']} - YOU MUST INCLUDE THIS IN YOUR FINAL PROMPT

ARTISTIC VISION:
• Style: {style_settings.get('style', 'Not specified')}
• Art Movement: {style_settings.get('art_movement', 'Not specified')}
• Style Era: {style_settings.get('style_era', 'Not specified')}

ATMOSPHERE & ENVIRONMENT:
• Weather: {environment_settings.get('weather', 'Not specified')}
• Season: {environment_settings.get('season', 'Not specified')}
• Location Type: {environment_settings.get('location_type', 'Not specified')}
• Atmospheric Effects: {', '.join(environment_settings.get('atmospheric_effects', []))}

VISUAL ELEMENTS:
• Lighting Type: {lighting_settings.get('lighting_type', 'Not specified')}
• Light Quality: {lighting_settings.get('light_quality', 'Not specified')}
• Time of Day: {lighting_settings.get('time_of_day', 'Not specified')}
• Color Scheme: {color_settings.get('color_scheme', 'Not specified')}
• Color Temperature: {color_settings.get('color_temperature', 'Not specified')}

COMPOSITION:
• Technique: {composition_settings.get('technique', 'Not specified')}
• Visual Flow: {composition_settings.get('visual_flow', 'Not specified')}
• Focal Point: {composition_settings.get('focal_point', 'Not specified')}
• Detail Level: {detail_settings.get('detail_level', 'Not specified')}
• Texture Quality: {detail_settings.get('texture_quality', 'Not specified')}

OUTPUT FORMAT:
Your response should be a single, flowing paragraph that transforms "{prompt}" into a detailed scene,
incorporating the technical elements naturally. End with resolution and aspect ratio specifications.

NEGATIVE ELEMENTS TO AVOID:
{prefs.get('negative_prompt', self.DEFAULT_NEGATIVE_PROMPT)}
"""

    def enhance_prompt(self, prompt: str, description: Optional[str] = None, **kwargs) -> str:
        """Enhance a general (non-logo) prompt.

        Args:
            prompt: The input prompt to enhance.
            description: Optional description to include.
            **kwargs: Additional keyword arguments.

        Returns:
            str: The enhanced prompt.

        Raises:
            PromptEnhancementError: If enhancement fails.
        """
        try:
            # Validate input
            self._validate_input(prompt)

            # Extract preferences
            prefs = self._extract_preferences()

            # Detect art medium and update negative prompt
            detected_medium = self._detect_art_medium(prompt)
            prefs['negative_prompt'] = self._update_negative_prompt(
                prefs.get('negative_prompt', ''),
                detected_medium
            )

            # Construct instruction
            instruction = self._construct_enhancement_instruction(
                prompt, prefs, detected_medium
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
                negative_prompt=prefs['negative_prompt']
            )

        except Exception as e:
            logging.error(f"General prompt enhancement failed: {str(e)}", exc_info=True)
            raise PromptEnhancementError(f"Failed to enhance general prompt: {str(e)}")
