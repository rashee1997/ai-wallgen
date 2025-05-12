# ai_prest_gen/logo_style_templates.py
"""
Logo Style Templates Module for AI Preset Generator.

This module provides specific template functions for various logo styles.
Each function returns a dictionary guiding the AI to generate a detailed
text prompt suitable for Google's Imagen 3 model.
"""
from typing import Dict, Any

def get_logo_minimalist_template(style_category: str) -> Dict[str, Any]:
    return {
        "preset_name": "Minimalist Logo Concept",
        "ai_prompt_focus": "Generate a detailed text prompt for Imagen 3 to create a minimalist logo.",
        "logo_style_description": "A minimalist logo featuring clean lines, simple geometric shapes, and a limited color palette (e.g., monochrome with one accent, or two complementary muted tones). Focus on clarity and strong visual identity.",
        "key_elements_guidance": "Suggest 1-2 core visual elements (e.g., a stylized letter, an abstract geometric form, a simple icon representing [USER_PROVIDED_CONCEPT_OR_INDUSTRY]).",
        "color_palette_guidance": "Suggest a specific color palette of 2-3 colors suitable for a minimalist logo (e.g., '#000000, #FFFFFF, #FFD700' for black, white, gold). Provide hex codes.",
        "typography_guidance": "If text like '[LOGO_TEXT_PLACEHOLDER]' is to be included, suggest a clean, modern sans-serif font style (e.g., 'Montserrat', 'Open Sans'). Specify if text should be primary, secondary, or integrated with an icon.",
        "negative_prompt_suggestions": "common negative prompts for logos: 'complex details, cluttered, multiple colors, gradients, shadows, realistic textures, photographic'.",
        "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for a logo.
**Logo Text/Initials:** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Description:** {logo_style_description}
**Key Visual Elements:** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style:** {typography_output}
**Desired Output Format:** Flat vector illustration, isolated on a white background.
**Negative Prompt:** {negative_prompt_suggestions}

Assemble these into a single, coherent, and detailed text prompt for Imagen 3. For example:
'Create a minimalist logo for "[LOGO_TEXT_PLACEHOLDER]" representing [USER_PROVIDED_CONCEPT_OR_INDUSTRY]. Featuring [key_elements_output], using colors [color_palette_output]. Typography: [typography_output]. Flat vector illustration, isolated on a white background. Negative prompt: [negative_prompt_suggestions].'
"""
    }

def get_logo_emblem_template(style_category: str) -> Dict[str, Any]:
    return {
        "preset_name": "Emblem Logo Concept",
        "ai_prompt_focus": "Generate a detailed text prompt for Imagen 3 to create an emblem logo.",
        "logo_style_description": "An emblem logo where text is integrated within a symbol or icon, often with a traditional or classic feel. Think badges, crests, or seals.",
        "key_elements_guidance": "Suggest a central symbol or shape (e.g., shield, circle, laurel wreath) and how the text '[LOGO_TEXT_PLACEHOLDER]' can be integrated within or around it. Mention any relevant iconography for [USER_PROVIDED_CONCEPT_OR_INDUSTRY].",
        "color_palette_guidance": "Suggest a color palette of 2-4 colors suitable for an emblem (e.g., deep blues, golds, silvers, reds). Provide hex codes.",
        "typography_guidance": "Suggest a classic serif or a strong sans-serif font that complements an emblem style for the text '[LOGO_TEXT_PLACEHOLDER]'.",
        "negative_prompt_suggestions": "common negative prompts for logos: 'modern minimalist (unless intended), abstract, photographic, overly complex details outside the emblem'.",
        "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for an emblem logo.
**Logo Text/Brand Name:** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Description:** {logo_style_description}
**Key Visual Elements & Text Integration:** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style:** {typography_output}
**Desired Output Format:** Vector illustration, suitable for an emblem, isolated on a white background.
**Negative Prompt:** {negative_prompt_suggestions}

Assemble these into a single, coherent, and detailed text prompt for Imagen 3.
"""
    }

def get_logo_wordmark_template(style_category: str) -> Dict[str, Any]:
    return {
        "preset_name": "Wordmark Logo Concept",
        "ai_prompt_focus": "Generate a detailed text prompt for Imagen 3 to create a wordmark logo.",
        "logo_style_description": "A wordmark logo (logotype) that focuses solely on the text '[LOGO_TEXT_PLACEHOLDER]', using unique typography and potentially subtle graphic elements integrated into the text.",
        "key_elements_guidance": "Focus on typographic treatment. Suggest a unique font style (e.g., custom script, bold display font, elegant serif) and any subtle graphic modifications to the text itself (e.g., ligatures, stylized letters, underline).",
        "color_palette_guidance": "Suggest a color palette of 1-3 colors that enhances the typography. Provide hex codes.",
        "typography_guidance": "The typography IS the logo. Describe the desired font style and any specific treatments.",
        "negative_prompt_suggestions": "common negative prompts for logos: 'icon, symbol, abstract shape, cluttered background, photographic'.",
        "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for a wordmark logo.
**Logo Text:** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Description:** {logo_style_description}
**Key Visual Elements (Typography Focus):** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style:** {typography_output}
**Desired Output Format:** Flat vector illustration, isolated on a white background.
**Negative Prompt:** {negative_prompt_suggestions}

Assemble these into a single, coherent, and detailed text prompt for Imagen 3.
"""
    }

def get_logo_lettermark_template(style_category: str) -> Dict[str, Any]:
    return {
        "preset_name": "Lettermark Logo Concept",
        "ai_prompt_focus": "Generate a detailed text prompt for Imagen 3 to create a lettermark logo.",
        "logo_style_description": "A lettermark logo (monogram) using the initials '[LOGO_TEXT_PLACEHOLDER]' (expected to be 1-3 letters). Focus on stylized typography and the interplay of the letters.",
        "key_elements_guidance": "Suggest creative ways to combine or stylize the letters '[LOGO_TEXT_PLACEHOLDER]' into a unique symbol. Consider overlapping, interlocking, or abstracting the forms.",
        "color_palette_guidance": "Suggest a color palette of 1-3 colors that works well with the stylized letters. Provide hex codes.",
        "typography_guidance": "The typography IS the logo. Describe the desired stylized treatment of the letters '[LOGO_TEXT_PLACEHOLDER]'.",
        "negative_prompt_suggestions": "common negative prompts for logos: 'full brand name, complex icon, realistic textures, photographic'.",
        "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for a lettermark logo.
**Logo Initials:** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Description:** {logo_style_description}
**Key Visual Elements (Stylized Initials):** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style:** {typography_output}
**Desired Output Format:** Flat vector illustration, isolated on a white background.
**Negative Prompt:** {negative_prompt_suggestions}

Assemble these into a single, coherent, and detailed text prompt for Imagen 3.
"""
    }

def get_logo_abstract_template(style_category: str) -> Dict[str, Any]:
    return {
        "preset_name": "Abstract Logo Concept",
        "ai_prompt_focus": "Generate a detailed text prompt for Imagen 3 to create an abstract logo.",
        "logo_style_description": "An abstract logo mark using geometric or organic shapes to represent the brand concept ([USER_PROVIDED_CONCEPT_OR_INDUSTRY]) without literal imagery. Focus on form, color, and composition.",
        "key_elements_guidance": "Suggest abstract shapes or forms that visually represent [USER_PROVIDED_CONCEPT_OR_INDUSTRY] (e.g., interconnected nodes for network, fluid shapes for creativity, sharp angles for technology).",
        "color_palette_guidance": "Suggest a color palette of 2-4 colors that enhances the abstract form and concept. Provide hex codes.",
        "typography_guidance": "If text like '[LOGO_TEXT_PLACEHOLDER]' is included, suggest a clean, modern font that complements the abstract mark, specifying if it should be placed below or beside the symbol.",
        "negative_prompt_suggestions": "common negative prompts for logos: 'literal imagery, realistic objects, cluttered, photographic'.",
        "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for an abstract logo.
**Logo Text (if any):** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Description:** {logo_style_description}
**Key Visual Elements (Abstract Forms):** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style (if text included):** {typography_output}
**Desired Output Format:** Flat vector illustration, isolated on a white background.
**Negative Prompt:** {negative_prompt_suggestions}

Assemble these into a single, coherent, and detailed text prompt for Imagen 3.
"""
    }

def get_logo_mascot_template(style_category: str) -> Dict[str, Any]:
    return {
        "preset_name": "Mascot Logo Concept",
        "ai_prompt_focus": "Generate a detailed text prompt for Imagen 3 to create a mascot logo.",
        "logo_style_description": "A mascot logo featuring an illustrated character representing the brand ([USER_PROVIDED_CONCEPT_OR_INDUSTRY]). The character should be friendly, memorable, and visually distinct.",
        "key_elements_guidance": "Suggest a character concept (e.g., an animal, a person, a mythical creature) and describe its appearance, pose, and expression. Mention how it relates to [USER_PROVIDED_CONCEPT_OR_INDUSTRY].",
        "color_palette_guidance": "Suggest a vibrant and appealing color palette of 3-5 colors for the mascot. Provide hex codes.",
        "typography_guidance": "If text like '[LOGO_TEXT_PLACEHOLDER]' is included, suggest a playful or bold font that complements the mascot style, specifying its placement relative to the character.",
        "negative_prompt_suggestions": "common negative prompts for logos: 'realistic human/animal (unless intended), scary, complex background, photographic'.",
        "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for a mascot logo.
**Logo Text (if any):** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Description:** {logo_style_description}
**Key Visual Elements (Mascot Character):** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style (if text included):** {typography_output}
**Desired Output Format:** Illustration, isolated on a white background.
**Negative Prompt:** {negative_prompt_suggestions}

Assemble these into a single, coherent, and detailed text prompt for Imagen 3.
"""
    }

def get_logo_illustrative_template(style_category: str) -> Dict[str, Any]:
    return {
        "preset_name": "Illustrative Logo Concept",
        "ai_prompt_focus": "Generate a detailed text prompt for Imagen 3 to create an illustrative logo.",
        "logo_style_description": "An illustrative logo featuring a detailed drawing or illustration that serves as the logo mark. Can range from hand-drawn to detailed digital illustration.",
        "key_elements_guidance": "Suggest a detailed illustration concept that represents [USER_PROVIDED_CONCEPT_OR_INDUSTRY]. Describe the style of illustration (e.g., hand-drawn, linework, detailed digital painting).",
        "color_palette_guidance": "Suggest a color palette of 3-5 colors that fits the illustration style. Provide hex codes.",
        "typography_guidance": "If text like '[LOGO_TEXT_PLACEHOLDER]' is included, suggest a font style (hand-drawn, script, or complementary serif/sans-serif) and its placement.",
        "negative_prompt_suggestions": "common negative prompts for logos: 'minimalist, abstract, photographic, overly simple'.",
        "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for an illustrative logo.
**Logo Text (if any):** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Description:** {logo_style_description}
**Key Visual Elements (Illustration):** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style (if text included):** {typography_output}
**Desired Output Format:** Illustration, isolated on a white background.
**Negative Prompt:** {negative_prompt_suggestions}

Assemble these into a single, coherent, and detailed text prompt for Imagen 3.
"""
    }

def get_logo_3d_template(style_category: str) -> Dict[str, Any]:
    return {
        "preset_name": "3D Logo Concept",
        "ai_prompt_focus": "Generate a detailed text prompt for Imagen 3 to create a 3D logo.",
        "logo_style_description": "A 3D logo with depth, volume, and realistic or stylized rendering. Can be a 3D wordmark, symbol, or combination.",
        "key_elements_guidance": "Suggest the 3D form (e.g., extruded text, a volumetric symbol, a rendered object) and how it represents [USER_PROVIDED_CONCEPT_OR_INDUSTRY]. Describe the desired material properties (e.g., polished metal, glass, matte plastic).",
        "color_palette_guidance": "Suggest a color palette of 2-4 colors, considering how light interacts with the 3D form and materials. Provide hex codes.",
        "typography_guidance": "If text like '[LOGO_TEXT_PLACEHOLDER]' is included, suggest a font style that works well in 3D (e.g., bold sans-serif, block letters) and its integration.",
        "negative_prompt_suggestions": "common negative prompts for logos: 'flat 2d, vector illustration, blurry (unless intentional DoF), low detail'.",
        "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for a 3D logo.
**Logo Text (if any):** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Description:** {logo_style_description}
**Key Visual Elements (3D Form & Materials):** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style (if text included):** {typography_output}
**Desired Output Format:** 3D render, isolated on a white background.
**Negative Prompt:** {negative_prompt_suggestions}

Assemble these into a single, coherent, and detailed text prompt for Imagen 3.
"""
    }


DEFAULT_LOGO_TEMPLATE = {
    "preset_name": "Generic Logo Concept",
    "ai_prompt_focus": "Generate a detailed text prompt for Imagen 3 to create a versatile logo.",
    "logo_style_description": "A versatile logo style. Consider elements from [USER_PROVIDED_STYLE_HINT].",
    "key_elements_guidance": "Suggest 1-3 core visual elements or concepts for a logo representing [USER_PROVIDED_CONCEPT_OR_INDUSTRY].",
    "color_palette_guidance": "Suggest a flexible color palette of 2-4 colors. Provide hex codes.",
    "typography_guidance": "If text like '[LOGO_TEXT_PLACEHOLDER]' is included, suggest a suitable font style.",
    "negative_prompt_suggestions": "common negative prompts for logos: 'cluttered, blurry, too many colors, complex textures'.",
    "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for a logo.
**Logo Text/Initials:** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Hint (if any):** [USER_PROVIDED_STYLE_HINT]
**Style Description:** {logo_style_description}
**Key Visual Elements:** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style:** {typography_output}
**Desired Output Format:** Flat vector illustration, isolated on a white background.
**Negative Prompt:** {negative_prompt_suggestions}

Assemble these into a single, coherent, and detailed text prompt for Imagen 3.
"""
}

def get_logo_default_template(style_category: str) -> Dict[str, Any]:
    return DEFAULT_LOGO_TEMPLATE.copy()
