# ai_prest_gen/prompt_builder.py
"""
Handles the construction of detailed prompts for the Gemini AI to generate presets.
"""
import json
import logging
from typing import Dict, Any

# Attempt to import dependencies for prompt building
try:
    from .style_category_catalog import instructions_for_category
    from .style_templates import get_template_for_category
    PROMPT_BUILDER_DEPS_AVAILABLE = True
except ImportError as e:
    logging.error(f"PresetPromptBuilder: Failed to import dependencies (instructions_for_category, get_template_for_category): {e}")
    PROMPT_BUILDER_DEPS_AVAILABLE = False
    # Define fallbacks if necessary, though this class might not be usable without them
    def instructions_for_category(cat: str, style: str) -> str: # type: ignore
        logging.warning("PresetPromptBuilder: Using fallback instructions_for_category.")
        return "No specific instructions available due to import error."

    def get_template_for_category(cat: str) -> Dict[str, Any]: # type: ignore
        logging.warning("PresetPromptBuilder: Using fallback get_template_for_category.")
        return {"error": "Template not available due to import error."}


class PresetPromptBuilder:
    """
    Constructs detailed prompts for the Gemini AI to generate preset settings
    based on style, category, instructions, and a base template.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if not PROMPT_BUILDER_DEPS_AVAILABLE:
            self.logger.critical("PresetPromptBuilder initialized without core dependencies. Prompt generation will likely fail or be incorrect.")

    def build_preset_generation_prompt(self, base_style_name: str, style_category: str) -> str:
        """
        Constructs the detailed prompt string for the Gemini AI.

        Args:
            base_style_name: The name of the base style.
            style_category: The detected category for the base style.

        Returns:
            str: The fully constructed prompt string for the Gemini API,
                 or an error message string if dependencies are missing.
        """
        if not PROMPT_BUILDER_DEPS_AVAILABLE:
            return "Error: PresetPromptBuilder dependencies (catalog/templates) not available. Cannot build prompt."

        category_instructions_text = instructions_for_category(style_category, base_style_name)
        template = get_template_for_category(style_category)

        self.logger.info(f"Building prompt for style: '{base_style_name}', category: '{style_category}'")
        self.logger.debug(f"Using template: {template}")
        self.logger.debug(f"Using category instructions: {category_instructions_text}")

        if not template or not isinstance(template, dict):
            self.logger.error(f"No valid template found for category: {style_category}. Using minimal default for prompt.")
            template = {
                "preset_name": f"{base_style_name.replace('_', ' ').title()} Default Prompt",
                "styles": [base_style_name],
                "moods": ["Neutral"],
                "description": f"Default prompt structure for {base_style_name}.",
                "aspect_ratio": "16:9",
                "imagen_settings": {
                    "negative_prompt": "low quality",
                    "style_negative_prompt": "clashing styles",
                    "camera_settings": {
                        "aperture": "f/2.8",
                        "shutter_speed": "1/125",
                        "iso": 100,
                        "focal_length": "50mm",
                        "lens_type": "Standard",
                        "camera_model": "Generic DSLR"
                    }
                }
            }

        instruction_header = f"Select settings that work well with \"{base_style_name}\" (category: {style_category}):"

        template_for_prompt = template.copy()
        template_for_prompt["styles"] = [base_style_name]
        template_for_prompt.setdefault("description", f"AI preset for {base_style_name}.")
        template_for_prompt.setdefault("aspect_ratio", "16:9")

        prompt = f"""
Generate settings for a wallpaper with style: "{base_style_name}"

Instructions:
1. Create a unique `preset_name` inspired by the style "{base_style_name}" and category "{style_category}".
2. Create a `description` field describing the preset.
3. Choose ONE mood for the "moods" list.
4. Follow the specific guidance for the detected category "{style_category}":
   {instruction_header}
   {category_instructions_text}
5. For `negative_prompt`, generate text avoiding elements conflicting with the *category* "{style_category}".
6. For `style_negative_prompt`, generate text avoiding elements conflicting with the *base style* "{base_style_name}".
7. Ensure `aspect_ratio` is "16:9".
8. Fill in ALL fields from the template below with specific, fitting values. Do NOT leave default template values unchanged unless they are truly appropriate. Do NOT use placeholders.
9. **CRITICAL:** Ensure the output JSON includes ALL top-level keys (`preset_name`, `moods`, `aspect_ratio`, `description`, `styles`, `imagen_settings`) and ALL nested dictionaries (`style_settings`, `lighting_settings`, `composition_settings`, `color_settings`, `detail_settings`, `environment_settings`, `quality_settings`, `camera_settings` if present in the template, etc.) exactly as they appear in the template structure provided below. Do not omit any sections.
10. Generate detailed and dynamic `camera_settings` including parameters such as aperture, shutter speed, ISO, focal length, lens type, camera model, and any other relevant photographic settings. Do NOT reuse static or default camera settings from the template; instead, create unique and contextually appropriate camera settings for this preset.
11. Output ONLY the valid JSON object, starting with `{{` and ending with `}}`. No ```json.

JSON Template to Fill:
```json
{json.dumps(template_for_prompt, indent=4)}
```
"""
        return prompt
