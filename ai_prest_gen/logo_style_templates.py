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
        "logo_style_description": "A minimalist logo featuring clean lines, simple geometric shapes, and a limited color palette (e.g., monochrome with one accent, or two complementary muted tones). Focus on clarity, strong visual identity, and negative space utilization. The design should be timeless, scalable, and instantly recognizable even at small sizes.",
        "key_elements_guidance": "Suggest 1-2 core visual elements (e.g., a stylized letter, an abstract geometric form, a simple icon representing [USER_PROVIDED_CONCEPT_OR_INDUSTRY]). Consider the use of negative space to create dual imagery or hidden meanings. The element should work effectively in both color and monochrome versions.",
        "color_palette_guidance": "Suggest a specific color palette of 2-3 colors suitable for a minimalist logo (e.g., '#000000, #FFFFFF, #FFD700' for black, white, gold). Provide hex codes. Consider color psychology - blues for trust/professionalism, greens for growth/environment, reds for energy/passion. Ensure sufficient contrast for accessibility and small-size legibility.",
        "typography_guidance": "If text like '[LOGO_TEXT_PLACEHOLDER]' is to be included, suggest a clean, modern sans-serif font style (e.g., 'Helvetica Neue', 'Montserrat', 'Open Sans'). Specify if text should be primary, secondary, or integrated with an icon. For minimalist logos, consider custom letter spacing, consistent stroke weight, and the removal of unnecessary serifs or decorative elements. Leverage Imagen 3's superior text rendering capabilities for crisp, precise letterforms.",
        "composition_guidance": "Emphasize balance and proportion. Consider symmetry or intentional asymmetry. Ensure the logo is balanced visually, with proper weight distribution and a clear focal point. The design should feel complete and stable. Provide guidance on appropriate spacing between elements (e.g., icon-to-text relationship).",
        "industry_applications": "For tech/digital: emphasize sleek, innovative shapes. For finance/legal: suggest more structured, stable forms. For healthcare: incorporate gentle curves and approachable elements. For creative industries: consider more playful geometric abstractions that still maintain minimalism.",
        "negative_prompt_suggestions": "common negative prompts for logos: 'complex details, gradients, shadows, realistic textures, photographic elements, busy backgrounds, decorative flourishes, drop shadows, bevels, embossing, multiple competing focal points, inconsistent line weights, overly detailed illustrations'.",
        "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for a minimalist logo.
**Logo Text/Initials:** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Description:** {logo_style_description}
**Key Visual Elements:** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style:** {typography_output}
**Composition Guidance:** {composition_guidance}
**Desired Output Format:** Flat vector illustration, isolated on a white background. Ensure clean edges and precise geometric forms.
**Negative Prompt:** {negative_prompt_suggestions}

Assemble these into a single, coherent, and detailed text prompt for Imagen 3. For example:
'Create a minimalist logo for "[LOGO_TEXT_PLACEHOLDER]" representing [USER_PROVIDED_CONCEPT_OR_INDUSTRY]. Featuring [key_elements_output], using colors [color_palette_output]. Typography: [typography_output]. Design should balance [composition_guidance]. Flat vector illustration, isolated on a white background with clean edges and precise forms. Negative prompt: [negative_prompt_suggestions].'
"""
    }

def get_logo_emblem_template(style_category: str) -> Dict[str, Any]:
    return {
        "preset_name": "Emblem Logo Concept",
        "ai_prompt_focus": "Generate a detailed text prompt for Imagen 3 to create an emblem logo.",
        "logo_style_description": "An emblem logo where text is integrated within a symbol or icon, often with a traditional or classic feel. Think badges, crests, seals, or medallions with a contained, cohesive structure. Emblems convey heritage, authenticity, and authority while creating a self-contained, easily recognizable brand mark.",
        "key_elements_guidance": "Suggest a central containing shape (e.g., shield, circle, hexagon, laurel wreath) and how the text '[LOGO_TEXT_PLACEHOLDER]' can be integrated within or around it. Mention any relevant iconography for [USER_PROVIDED_CONCEPT_OR_INDUSTRY]. Consider hierarchical organization of elements (e.g., central icon, primary text, secondary text, founding date) and ensure all elements work in harmony within the contained shape.",
        "color_palette_guidance": "Suggest a color palette of 2-4 colors suitable for an emblem (e.g., deep blues, golds, silvers, reds, greens). Provide hex codes. Consider traditional color combinations that convey heritage and authority. For a modern emblem, suggest more contemporary color schemes while maintaining the classic structure. Ensure colors retain their impact when converted to monochrome.",
        "typography_guidance": "Suggest a classic serif (e.g., 'Garamond', 'Baskerville') or a strong sans-serif font (e.g., 'Trajan', 'Gotham Bold') that complements an emblem style for the text '[LOGO_TEXT_PLACEHOLDER]'. Consider letter spacing for curved text that follows the emblem's shape. For multi-line text, provide hierarchy guidance (e.g., larger company name, smaller tagline or founding date). Leveraging Imagen 3's precise text rendering, suggest potential decorative serifs or letterform enhancements that maintain legibility.",
        "composition_guidance": "Emphasize symmetry and balance. Provide guidance on centering elements, appropriate spacing between concentric circles or shapes, and text placement that follows the curvature of the containing shape. Consider the need for visual weight to ground the emblem, and ensure readability of text at various sizes.",
        "industry_applications": "For universities/education: academic shields with books or torches. For food/beverage: circular emblems with wheat/ingredients. For automotive: shields with dynamic symbols. For legal/government: official seal-like designs. For hospitality: crests incorporating relevant service elements.",
        "negative_prompt_suggestions": "common negative prompts for logos: 'minimalist style (unless intended), overly abstract elements, photographic elements, irregular or asymmetric containing shapes, cluttered or illegible text, misaligned elements, inconsistent line weights, overly distressed textures (unless vintage style is specified)'.",
        "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for an emblem logo.
**Logo Text/Brand Name:** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Description:** {logo_style_description}
**Key Visual Elements & Text Integration:** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style:** {typography_output}
**Composition Guidance:** {composition_guidance}
**Desired Output Format:** Vector illustration, suitable for an emblem, isolated on a white background. Ensure crisp edges and clear text rendering.
**Negative Prompt:** {negative_prompt_suggestions}

Assemble these into a single, coherent, and detailed text prompt for Imagen 3, emphasizing the integration of text within the emblem structure and the classic, authoritative feel of the design.
"""
    }

def get_logo_wordmark_template(style_category: str) -> Dict[str, Any]:
    return {
        "preset_name": "Wordmark Logo Concept",
        "ai_prompt_focus": "Generate a detailed text prompt for Imagen 3 to create a wordmark logo.",
        "logo_style_description": "A wordmark logo (logotype) that focuses solely on the text '[LOGO_TEXT_PLACEHOLDER]', using unique typography and potentially subtle graphic elements integrated into the text. The brand name itself becomes the visual identifier, relying on distinctive letterforms, custom spacing, and typographic treatments to create a memorable impression. Wordmarks work exceptionally well for brands with distinctive or short names.",
        "key_elements_guidance": "Focus on typographic treatment. Suggest a unique font style (e.g., custom script, bold display font, elegant serif) and any subtle graphic modifications to the text itself (e.g., ligatures, stylized letters, custom letterform adjustments, underlines, crossbars). Consider how specific letters might be modified to create brand distinction. Suggest potential connecting elements between letters or unique treatments of ascenders/descenders. Leveraging Imagen 3's superior text rendering capabilities, recommend precise letter spacing (kerning) and any letter modifications that remain highly legible.",
        "color_palette_guidance": "Suggest a color palette of 1-3 colors that enhances the typography. Provide hex codes. Consider how color can create emphasis on parts of the name or create visual interest in an otherwise text-only design. Consider gradients only if they enhance readability rather than detract from it. Ensure the wordmark remains effective in monochrome for versatile applications.",
        "typography_guidance": "The typography IS the logo. Describe the desired font style and any specific treatments in detail. Consider weight variations within the wordmark (e.g., mixing bold and light), case treatments (all caps vs. mixed case), and specific letter modifications. Recommend the most appropriate font category (serif, sans-serif, slab serif, script, display) based on brand personality. Suggest precise kerning (letter spacing) and leading (line spacing) if multiple lines are used. Leveraging Imagen 3's text rendering capabilities, ensure letterforms are distinct and balanced.",
        "composition_guidance": "Provide guidance on horizontal or vertical orientation, text alignment (centered, left-aligned), and any stacking of words or elements. Consider baseline alignment and any intentional breaking of traditional typographic rules to create visual interest. Recommend white space considerations to ensure the wordmark has room to 'breathe'.",
        "industry_applications": "For luxury brands: elegant serif or script fonts. For tech companies: modern, clean sans-serif. For creative industries: custom, playful letterforms. For legal/financial: structured, authoritative typefaces. For food/hospitality: warm, approachable letterforms that evoke appropriate emotions.",
        "negative_prompt_suggestions": "common negative prompts for logos: 'icon, symbol, complex abstract shape, cluttered background, photographic elements, inconsistent letter spacing, illegible fonts, overly decorative typefaces that sacrifice readability, unnecessary graphic elements, drop shadows or 3D effects (unless specifically desired)'.",
        "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for a wordmark logo.
**Logo Text:** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Description:** {logo_style_description}
**Key Visual Elements (Typography Focus):** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style:** {typography_output}
**Composition Guidance:** {composition_guidance}
**Desired Output Format:** Flat vector illustration, isolated on a white background. Ensure crisp, precise letterforms and consistent spacing.
**Negative Prompt:** {negative_prompt_suggestions}

Assemble these into a single, coherent, and detailed text prompt for Imagen 3, emphasizing the distinctive typography that will make this wordmark instantly recognizable.
"""
    }

def get_logo_lettermark_template(style_category: str) -> Dict[str, Any]:
    return {
        "preset_name": "Lettermark Logo Concept",
        "ai_prompt_focus": "Generate a detailed text prompt for Imagen 3 to create a lettermark logo.",
        "logo_style_description": "A lettermark logo (monogram) using the initials '[LOGO_TEXT_PLACEHOLDER]' (expected to be 1-3 letters). Focus on stylized typography and the interplay of the letters to create a distinctive, concise visual identifier. Lettermarks are excellent for brands with long names that need a compact, memorable symbol, especially for small-scale applications like app icons or favicons.",
        "key_elements_guidance": "Suggest creative ways to combine or stylize the letters '[LOGO_TEXT_PLACEHOLDER]' into a unique symbol. Consider overlapping, interlocking, or abstracting the letterforms while maintaining legibility. Explore how negative space between letters might create additional shapes or meanings. Consider the geometry and balance of the letterforms, potentially placing them in a containing shape (circle, square, shield) if it enhances recognition. Leveraging Imagen 3's precise rendering, recommend subtle details that remain visible at various scales.",
        "color_palette_guidance": "Suggest a color palette of 1-3 colors that works well with the stylized letters. Provide hex codes. Consider using color to create depth, highlight specific parts of letters, or differentiate overlapping elements. Recommend color combinations that remain effective in digital and print applications. Ensure the design remains strong in monochrome for versatile application.",
        "typography_guidance": "The typography IS the logo. Recommend a specific font category (serif, sans-serif, slab, script, display) and treatment that best represents [USER_PROVIDED_CONCEPT_OR_INDUSTRY]. Consider custom modifications to standard letters that create uniqueness while maintaining brand recognition. Using Imagen 3's superior text rendering, suggest precise details on letter weight, serifs, terminals, and connections between letters that can be accurately generated.",
        "composition_guidance": "Provide guidance on the arrangement of letters (e.g., horizontal, stacked, overlapping, radial). Consider the visual weight and balance between different letters, especially if they have varying widths (e.g., 'I' vs. 'W'). Recommend appropriate spacing or connections between letters and whether a containing shape would enhance the design.",
        "industry_applications": "For tech/digital: modern, geometric letterforms. For legal/financial: structured, authoritative monograms. For fashion/luxury: elegant, distinctive letter treatments. For sports: dynamic, energetic letterforms. For education: academic, traditional monogram styles.",
        "negative_prompt_suggestions": "common negative prompts for logos: 'full brand name, complex background elements, photographic textures, drop shadows, gradients, overly complex decorative elements, illegible letter stylizations, inconsistent letter treatments, imbalanced letter scaling'.",
        "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for a lettermark logo.
**Logo Initials:** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Description:** {logo_style_description}
**Key Visual Elements (Stylized Initials):** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style:** {typography_output}
**Composition Guidance:** {composition_guidance}
**Desired Output Format:** Flat vector illustration, isolated on a white background. Ensure crisp, precise letterforms with clean edges.
**Negative Prompt:** {negative_prompt_suggestions}

Assemble these into a single, coherent, and detailed text prompt for Imagen 3, emphasizing how the initials should interact to create a distinctive and memorable lettermark that represents the brand effectively.
"""
    }

def get_logo_abstract_template(style_category: str) -> Dict[str, Any]:
    return {
        "preset_name": "Abstract Logo Concept",
        "ai_prompt_focus": "Generate a detailed text prompt for Imagen 3 to create an abstract logo.",
        "logo_style_description": "An abstract logo mark using geometric or organic shapes to represent the brand concept ([USER_PROVIDED_CONCEPT_OR_INDUSTRY]) without literal imagery. Focus on form, color, and composition to evoke specific emotions and create a distinctive visual signature. Abstract logos are timeless, versatile across applications, and can transcend language barriers while conveying brand personality through visual elements alone.",
        "key_elements_guidance": "Suggest abstract shapes or forms that visually represent [USER_PROVIDED_CONCEPT_OR_INDUSTRY] through metaphor rather than literal depiction (e.g., interconnected nodes for network, fluid shapes for creativity, sharp angles for technology, ascending forms for growth, circular patterns for unity). Consider how these forms interact to create a cohesive symbol while remaining simple enough to be recognizable. Recommend 2-3 core shapes that work together to convey the desired brand attributes. Leveraging Imagen 3's detailed rendering capabilities, suggest subtle textures or depth that enhance the design without overcomplicating it.",
        "color_palette_guidance": "Suggest a color palette of 2-4 colors that enhances the abstract form and concept. Provide hex codes. Consider color psychology and how specific hues can reinforce the brand attributes (e.g., blues for trust/reliability, reds for energy/passion, greens for growth/health). Recommend primary and accent colors, potentially suggesting gradients if they enhance the concept (e.g., smooth transitions for fluid concepts). Ensure the logo remains effective in monochrome applications.",
        "typography_guidance": "If text like '[LOGO_TEXT_PLACEHOLDER]' is included, suggest a clean, modern font that complements the abstract mark, specifying if it should be placed below, beside, or integrated with the symbol. Recommend a font category (serif, sans-serif, slab, display) that balances with the abstract elements. Consider weight, spacing, and how typography should harmonize with the abstract forms without competing for attention. Leveraging Imagen 3's text rendering, ensure letterforms are precisely balanced with the abstract elements.",
        "composition_guidance": "Provide guidance on the arrangement of abstract elements, considering visual flow, balance, and negative space. Recommend whether the composition should be symmetrical or asymmetrical, enclosed or open, dense or airy. Consider the visual center of gravity and how the eye should move through the design. Suggest sizing relationships between abstract elements and typography (if included).",
        "industry_applications": "For tech/digital: precise geometric forms with clear meaning. For creative industries: fluid, expressive abstract shapes. For finance/legal: structured forms suggesting stability/security. For health/wellness: organic, harmonious shapes. For energy/movement: dynamic abstract forms suggesting motion.",
        "negative_prompt_suggestions": "common negative prompts for logos: 'literal imagery, realistic objects, overly complex shapes, cluttered composition, photographic elements, busy backgrounds, inconsistent style between elements, excessive detail that doesn't scale well, drop shadows or 3D effects (unless specifically desired)'.",
        "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for an abstract logo.
**Logo Text (if any):** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Description:** {logo_style_description}
**Key Visual Elements (Abstract Forms):** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style (if text included):** {typography_output}
**Composition Guidance:** {composition_guidance}
**Desired Output Format:** Flat vector illustration, isolated on a white background. Ensure clean edges and precise forms.
**Negative Prompt:** {negative_prompt_suggestions}

Assemble these into a single, coherent, and detailed text prompt for Imagen 3, emphasizing how the abstract elements should convey the essence of the brand concept through form, color, and composition rather than literal representation.
"""
    }

def get_logo_mascot_template(style_category: str) -> Dict[str, Any]:
    return {
        "preset_name": "Mascot Logo Concept",
        "ai_prompt_focus": "Generate a detailed text prompt for Imagen 3 to create a mascot logo.",
        "logo_style_description": "A mascot logo featuring an illustrated character representing the brand ([USER_PROVIDED_CONCEPT_OR_INDUSTRY]). The character should be friendly, memorable, and visually distinct with a personality that embodies the brand's values and creates an emotional connection with the audience. Mascot logos excel at creating brand ambassadors that can be animated, used in different poses, and adapted across marketing materials.",
        "key_elements_guidance": "Suggest a character concept (e.g., an animal, a person, a mythical creature, an anthropomorphized object) and describe its appearance, pose, expression, and distinguishing features in detail. Mention how it relates to [USER_PROVIDED_CONCEPT_OR_INDUSTRY]. Consider the character's proportions (e.g., stylized with larger head/eyes for approachability vs. realistic proportions for authority). Recommend specific personality traits the mascot should embody through its expression and pose. Leveraging Imagen 3's detailed rendering capabilities, suggest the level of detail for the character's features, clothing, or accessories that define its identity.",
        "color_palette_guidance": "Suggest a vibrant and appealing color palette of 3-5 colors for the mascot. Provide hex codes. Consider primary colors for the character itself and accent colors for clothing or accessories. Recommend colors that align with the brand personality (e.g., energetic, trustworthy, playful, authoritative) and ensure the mascot remains recognizable even when simplified for different applications. Consider how colors can define the character's most identifiable features.",
        "typography_guidance": "If text like '[LOGO_TEXT_PLACEHOLDER]' is included, suggest a playful or bold font that complements the mascot style, specifying its placement relative to the character (e.g., above, below, integrated within the design). Consider how the typography can echo the personality of the mascot through similar visual attributes. Using Imagen 3's improved text rendering, recommend custom letterforms that might incorporate elements from the mascot (e.g., a tail forming part of a letter).",
        "composition_guidance": "Provide guidance on the mascot's pose and orientation (e.g., facing forward for approachability, in profile for action). Consider the balance between the character and any text elements, and whether the mascot should be full-body or a head/bust only. Recommend containment treatment (e.g., circular boundary, integrated background) or if the mascot should stand alone. Suggest whether the character should interact with the text elements.",
        "industry_applications": "For food/beverage: appetizing food characters or friendly animals. For sports teams: powerful, dynamic creatures or personas. For children's products: cute, approachable characters. For technology: robot or futuristic beings. For education: wise animals (owls) or friendly scholarly figures.",
        "negative_prompt_suggestions": "common negative prompts for logos: 'realistic human features (unless intended), scary or intimidating expressions, overly complex or detailed backgrounds, photographic style, too many accessories or details that won't scale down well, inappropriately gendered mascots, cultural stereotypes'.",
        "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for a mascot logo.
**Logo Text (if any):** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Description:** {logo_style_description}
**Key Visual Elements (Mascot Character):** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style (if text included):** {typography_output}
**Composition Guidance:** {composition_guidance}
**Desired Output Format:** Illustration with clean vector style, isolated on a white background.
**Negative Prompt:** {negative_prompt_suggestions}

Assemble these into a single, coherent, and detailed text prompt for Imagen 3, emphasizing how the mascot should embody the brand's personality through its expression, pose, and distinguishing visual characteristics.
"""
    }

def get_logo_illustrative_template(style_category: str) -> Dict[str, Any]:
    return {
        "preset_name": "Illustrative Logo Concept",
        "ai_prompt_focus": "Generate a detailed text prompt for Imagen 3 to create an illustrative logo.",
        "logo_style_description": "An illustrative logo featuring a detailed drawing or illustration that serves as the logo mark. This style ranges from hand-drawn to detailed digital illustration, creating a rich visual narrative that tells a story about the brand. Illustrative logos work well for brands that want to convey craftsmanship, tradition, or a distinct visual world, though they must be designed carefully to remain effective at smaller sizes.",
        "key_elements_guidance": "Suggest a detailed illustration concept that represents [USER_PROVIDED_CONCEPT_OR_INDUSTRY]. Describe the style of illustration (e.g., hand-drawn, engraving, linework, watercolor-inspired, detailed digital painting, woodcut) and the specific imagery it should contain. Consider the level of detail appropriate for a logo (rich enough to convey narrative, but simple enough to work at smaller sizes). Recommend focal points and how the illustration tells a story about the brand. Leveraging Imagen 3's detailed rendering capabilities, suggest specific textures, line qualities, or shading techniques that define the illustrative style.",
        "color_palette_guidance": "Suggest a color palette of 3-5 colors that fits the illustration style. Provide hex codes. Consider whether the palette should be vintage/muted or vibrant/contemporary based on the brand personality. Recommend primary colors for key elements and secondary colors for details or backgrounds. Consider how the illustration might work in monochrome for versatile applications. Suggest color layering techniques (if appropriate) for creating visual depth.",
        "typography_guidance": "If text like '[LOGO_TEXT_PLACEHOLDER]' is included, suggest a font style (hand-drawn, script, serif, or complementary display font) and its placement relative to the illustration. Consider whether the typography should mirror elements of the illustration style (e.g., same line quality, similar textures) or provide contrast. Using Imagen 3's text rendering capabilities, recommend lettering that complements the illustration style while maintaining legibility. Consider whether text should be integrated within the illustration or separate.",
        "composition_guidance": "Provide guidance on the arrangement of illustrated elements, considering visual hierarchy, flow, and balance. Recommend whether the illustration should be contained within a shape or frame or stand alone. Consider the relationship between illustrated elements and typography, and which should have visual priority. Suggest how to ensure the design remains clear and impactful even when scaled down.",
        "industry_applications": "For food/beverage: detailed ingredients or preparation scenes. For outdoor/adventure brands: landscapes or activities. For crafts/artisanal products: tools or making process. For historical/traditional brands: vintage-style illustrations. For destination/locale-specific businesses: local landmarks or scenes.",
        "negative_prompt_suggestions": "common negative prompts for logos: 'minimalist, abstract, photographic, excessively simple, too many small details that won't scale down, inconsistent illustration style, cluttered composition, overly complex scenes with no clear focal point'.",
        "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for an illustrative logo.
**Logo Text (if any):** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Description:** {logo_style_description}
**Key Visual Elements (Illustration):** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style (if text included):** {typography_output}
**Composition Guidance:** {composition_guidance}
**Desired Output Format:** Illustration with the specified style, isolated on a white background.
**Negative Prompt:** {negative_prompt_suggestions}

Assemble these into a single, coherent, and detailed text prompt for Imagen 3, emphasizing how the illustrative elements should tell a story about the brand while maintaining the clarity and impact necessary for a logo.
"""
    }

def get_logo_3d_template(style_category: str) -> Dict[str, Any]:
    return {
        "preset_name": "3D Logo Concept",
        "ai_prompt_focus": "Generate a detailed text prompt for Imagen 3 to create a 3D logo.",
        "logo_style_description": "A 3D logo with depth, volume, and realistic or stylized rendering. This can be a 3D wordmark, symbol, or combination mark with a dimensional quality that makes it stand out. 3D logos create impact through lighting, texture, and perspective, giving the brand a modern, substantial presence. While primarily used for digital applications, they can be designed to translate effectively to 2D formats when needed.",
        "key_elements_guidance": "Suggest the 3D form (e.g., extruded text, a volumetric symbol, a rendered object) and how it represents [USER_PROVIDED_CONCEPT_OR_INDUSTRY]. Describe the desired material properties (e.g., polished metal, glass, matte plastic, marble, wood) in detail, including texture, reflectivity, and finish. Consider how light interacts with the surfaces to create highlights and shadows that enhance the form. Recommend a specific perspective or viewing angle that best showcases the 3D elements. Leveraging Imagen 3's enhanced rendering capabilities, suggest subtle material details, texture granularity, or lighting effects that create realistic dimensionality.",
        "color_palette_guidance": "Suggest a color palette of 2-4 colors, considering how light interacts with the 3D form and materials. Provide hex codes. Recommend base colors for the primary materials and accent colors for highlights or secondary elements. Consider how colors might shift across surfaces due to lighting and reflection. Ensure the color strategy works when the logo needs to be displayed in 2D formats. Consider whether metallic or iridescent effects would enhance the design.",
        "typography_guidance": "If text like '[LOGO_TEXT_PLACEHOLDER]' is included, suggest a font style that works well in 3D (e.g., bold sans-serif, block letters, geometric fonts) and how it should be integrated into the dimensional design. Consider whether text should be extruded, beveled, embossed, or given other 3D treatments. Using Imagen 3's detailed rendering capabilities, recommend specific depth, beveling, or extrusion parameters that create clear, legible letterforms even with 3D treatment. Consider how typography interacts with lighting and material properties.",
        "composition_guidance": "Provide guidance on the arrangement of 3D elements, considering perspective, depth, and visual weight. Recommend camera angle, focal length, and lighting direction to best showcase the dimensionality. Consider the balance between showing off 3D qualities and maintaining a clean, recognizable silhouette. Suggest how to ensure the design translates effectively to 2D applications when needed.",
        "industry_applications": "For technology/gaming: sleek, modern materials with dynamic lighting. For construction/architecture: solid, substantial forms with textured materials. For luxury brands: premium materials like gold, glass, or marble. For entertainment: vibrant, dynamic 3D forms with dramatic lighting. For manufacturing: realistic material representations relevant to the industry.",
        "negative_prompt_suggestions": "common negative prompts for logos: 'flat 2D style (unless specifically showing 2D version), vector illustration style, blurry surfaces or edges, unrealistic lighting or shadows, low-quality textures, excessively complex forms that lose recognition at smaller sizes, inappropriate material choices for the brand'.",
        "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for a 3D logo.
**Logo Text (if any):** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Description:** {logo_style_description}
**Key Visual Elements (3D Form & Materials):** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style (if text included):** {typography_output}
**Composition Guidance:** {composition_guidance}
**Desired Output Format:** 3D render with realistic materials and lighting, isolated on a white or transparent background.
**Negative Prompt:** {negative_prompt_suggestions}

Assemble these into a single, coherent, and detailed text prompt for Imagen 3, emphasizing how the 3D elements should create depth, dimension, and material presence while maintaining the clarity and recognition necessary for a logo.
"""
    }


DEFAULT_LOGO_TEMPLATE = {
    "preset_name": "Generic Logo Concept",
    "ai_prompt_focus": "Generate a detailed text prompt for Imagen 3 to create a versatile logo.",
    "logo_style_description": "A versatile logo style that can adapt to multiple applications while maintaining brand recognition. Consider elements from [USER_PROVIDED_STYLE_HINT] combined with professional design principles. The logo should work effectively across digital and physical media, at various sizes, and in both color and monochrome versions.",
    "key_elements_guidance": "Suggest 1-3 core visual elements or concepts for a logo representing [USER_PROVIDED_CONCEPT_OR_INDUSTRY]. Consider both symbolic representations and abstract forms that capture the essence of the brand. Recommend elements that are distinct, memorable, and scale well. Leveraging Imagen 3's rendering capabilities, suggest appropriate level of detail that works across applications.",
    "color_palette_guidance": "Suggest a flexible color palette of 2-4 colors that represents the brand personality and industry positioning. Provide hex codes. Consider color psychology and how the palette might evoke specific emotions or associations. Recommend primary brand colors and accent colors, ensuring sufficient contrast for accessibility. Consider how colors will work across different backgrounds and applications.",
    "typography_guidance": "If text like '[LOGO_TEXT_PLACEHOLDER]' is included, suggest a suitable font style that balances distinctiveness with legibility. Recommend a font category (serif, sans-serif, slab, display, script) that aligns with the brand personality. Consider weight, spacing, and case treatment. Using Imagen 3's improved text rendering capabilities, suggest any custom letterform adjustments that might enhance brand recognition.",
    "composition_guidance": "Provide guidance on the arrangement of visual elements and typography, considering balance, proportion, and visual hierarchy. Recommend whether the logo should be horizontally or vertically oriented, contained within a shape, or left open. Consider white space usage and how elements interact to create a cohesive whole.",
    "industry_applications": "Provide specific recommendations for how this versatile logo might be adapted for the specific industry of [USER_PROVIDED_CONCEPT_OR_INDUSTRY], considering common visual language and consumer expectations in that sector.",
    "negative_prompt_suggestions": "common negative prompts for logos: 'cluttered, blurry, too many colors, complex textures, photographic elements, trendy elements that may quickly date the design, inconsistent styling, poor contrast, illegible text, intricate details that won't scale down well'.",
    "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for a logo.
**Logo Text/Initials:** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Hint (if any):** [USER_PROVIDED_STYLE_HINT]
**Style Description:** {logo_style_description}
**Key Visual Elements:** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style:** {typography_output}
**Composition Guidance:** {composition_guidance}
**Desired Output Format:** Flat vector illustration, isolated on a white background. Ensure clean edges and scalable design.
**Negative Prompt:** {negative_prompt_suggestions}

Assemble these into a single, coherent, and detailed text prompt for Imagen 3, emphasizing how the logo should achieve a balance of distinctiveness, versatility, and timeless design.
"""
}

def get_logo_default_template(style_category: str) -> Dict[str, Any]:
    return DEFAULT_LOGO_TEMPLATE.copy()
