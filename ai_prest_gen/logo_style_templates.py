# ai_prest_gen/logo_style_templates.py
"""
Logo Style Templates Module for AI Preset Generator.

This module provides specific template functions for various logo styles.
Each function returns a dictionary guiding the AI to generate a detailed
text prompt suitable for Google's Imagen 3 model.
"""
from typing import Dict, Any

def get_logo_minimalist_template(style_category: str) -> Dict[str, Any]:
    """
    Improved minimalist logo template logic:
    - Clear field descriptions for maintainability.
    - Actionable negative prompts.
    - Explicit placeholder routines for extensibility.
    """
    return {
        "preset_name": "Minimalist Logo Concept",
        "ai_prompt_focus": "Generate a detailed text prompt for Imagen 3 to create a minimalist, highly scalable, accessible logo. Prioritize simple geometry, strong identity, superb contrast, and negative space.",
        "logo_style_description": (
            "A minimalist logo using clean lines, geometric forms, and a strictly limited color palette "
            "(e.g., black, white, plus one accent). Prioritize recognizability at all sizes. "
            "Design should embody timelessness, modularity, and clear visual hierarchy. Negative space should be used creatively."
        ),
        "key_elements_guidance": (
            "Propose 1–2 essential shapes—e.g., a single stylized letter, simple icon, or clever abstraction of [USER_PROVIDED_CONCEPT_OR_INDUSTRY]. "
            "If achievable, use negative space to suggest dual imagery or hidden meaning. "
            "Ensure the design works in pure monochrome (black/white) plus accent version."
        ),
        "color_palette_guidance": (
            "Constrain palette to 2–3 high-contrast modern or neutral colors. Provide each as a hex code string, with rationale. "
            "E.g., '#1A1A1A, #FFFFFF' (black/white) + accent like '#00CFFF'. For additional inclusivity, explain color accessibility."
        ),
        "typography_guidance": (
            "Recommend a geometric, contemporary, sans-serif typeface (e.g., 'Montserrat', 'Open Sans'). "
            "If text is present ([LOGO_TEXT_PLACEHOLDER]), clarify if text is featured, secondary, or omitted; define clear kerning and line weight suggestions. "
            "Specify crisp, consistent stroke widths and explicit letter spacing, no decorative flourishes."
        ),
        "composition_guidance": (
            "Explain how icon and text relate spatially (e.g., icon left-of, above, or integrated with text). "
            "Require centered symmetry unless an intentional offset is justified. Outline margin/padding recommendations. "
            "Indicate preferred negative space arrangements and overall area balance."
        ),
        "industry_applications": (
            "Adapt icon forms to reflect: "
            "— Tech: sleek, angular. "
            "— Finance: stable rectangles, subtle notching. "
            "— Healthcare: soft, rounded corners, approachable shapes. "
            "— Creative: abstract, playful geometry, still using restraint."
        ),
        "negative_prompt_suggestions": (
            "Exclude: fine detail, gradients, photo/bitmap/raster effects, textured or multi-directional shadows, unnecessary outlines, "
            "busy backgrounds, any photorealism, 3D, symbol/library clip art, inconsistent weights, or fonts with serifs/handwriting."
        ),
        "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for a minimalist logo.
**Logo Text/Initials:** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Description:** {logo_style_description}
**Key Visual Elements:** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style:** {typography_output}
**Composition Guidance:** {composition_guidance}
**Desired Output Format:** Flat vector illustration, isolated on a white background. Ensure clean, sharp edges and pixel-perfect geometry.
**Negative Prompt:** {negative_prompt_suggestions}

Combine these into a single, detailed prompt for Imagen 3 as:
'Create a minimalist logo for "[LOGO_TEXT_PLACEHOLDER]" representing [USER_PROVIDED_CONCEPT_OR_INDUSTRY]. Use [key_elements_output] and a palette of [color_palette_output]. Typography: [typography_output]. Placement: [composition_guidance]. Output clean, flat vector, white background, no effects. Negative prompt: [negative_prompt_suggestions].'
"""
    }

def get_logo_emblem_template(style_category: str) -> Dict[str, Any]:
    """
    Improved emblem logo template logic:
    - Focused on hierarchy, legibility, integration logic.
    - Improved prompts for text and icon integration.
    - Field clarity and model-best-practice execution.
    """
    return {
        "preset_name": "Emblem Logo Concept",
        "ai_prompt_focus": (
            "Generate a detailed text prompt for Imagen 3 to create an emblem-style logo. "
            "Emphasize classic structure, clear text-symbol integration, and timeless authority cues."
        ),
        "logo_style_description": (
            "A contained emblem where text is woven into a cohesive visual mark. Style cues include shields, badges, seals, and crests, "
            "with defined borders/shapes holding together layered elements (icons, text, embellishments). The mark should feel both historic and memorable."
        ),
        "key_elements_guidance": (
            "Define a bold primary shape (e.g., shield, circle, or hexagon), with [LOGO_TEXT_PLACEHOLDER] distinctly integrated within or around it. "
            "Suggest an industry-relevant symbol and a logic for layering/hierarchy (e.g., central icon, then primary text, secondary motto/tagline or date). "
            "Describe the text curvature if any; recommend symmetry or justified composition for visual authority."
        ),
        "color_palette_guidance": (
            "Recommend a strong, traditional palette: e.g., blue/gold/silver/red/green, with color rationales. "
            "Provide hex codes and suggest how color signals heritage or adapts to modern/trendy variants. "
            "Ensure color contrast remains strong when the mark is rendered in monochrome."
        ),
        "typography_guidance": (
            "Recommend formal serif (e.g., 'Garamond', 'Baskerville') or serious sans-serif (e.g., 'Trajan', 'Gotham Bold'). "
            "Define size/weight hierarchy: main line bold, secondary line lighter/smaller. If text is wrapped or curved, specify precise arc/placement logic."
        ),
        "composition_guidance": (
            "Prioritize perfect symmetry. Specify how to center the central icon/symbol and how text curves, frames, or sits within shape. "
            "Provide minimum spacing/margins. All elements should have visual grounding (e.g., bottom anchor line or weighted border)."
        ),
        "industry_applications": (
            "Education: book/lamp/shield motifs. Food/Bev: circular wheat bundles or cutlery. Automotive: crests, gears, or wings. Gov/Legal: strong seals (eagle, scales, columns). "
            "Hospitality: framed crests/shields with iconography that signals welcome or service."
        ),
        "negative_prompt_suggestions": (
            "Avoid: flattened/minimalist-only style, photographic textures, raster/bitmap art, asymmetric or irregular layouts, illegible fonts, excessive or distressed grunge, "
            "crowding, symbol-icon disconnect, multiple conflicting focal points."
        ),
        "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for an emblem logo.
**Logo Text/Brand Name:** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Description:** {logo_style_description}
**Key Visual Elements & Text Integration:** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style:** {typography_output}
**Composition Guidance:** {composition_guidance}
**Desired Output Format:** Vector illustration, suitable for an emblem, isolated on white. Ensure crisp edges and legible, well-integrated text.
**Negative Prompt:** {negative_prompt_suggestions}

Combine as:
'Create an emblem logo for "[LOGO_TEXT_PLACEHOLDER]" in [USER_PROVIDED_CONCEPT_OR_INDUSTRY]. Icon: [key_elements_output]; palette: [color_palette_output]. Typography: [typography_output]. Layout: [composition_guidance]. Output a sharp, vector emblem on white, perfect symmetry. Negative prompt: [negative_prompt_suggestions].'
"""
    }

def get_logo_wordmark_template(style_category: str) -> Dict[str, Any]:
    """
    Improved wordmark logo template logic:
    - Explicitly defines typographic focus, kerning, and distinctions.
    - Stronger instructions for distinctive, readable, and scalable type.
    - Separates advanced and legacy pitfalls in negative prompts.
    """
    return {
        "preset_name": "Wordmark Logo Concept",
        "ai_prompt_focus": (
            "Generate a detailed text prompt for Imagen 3 to create a typographically-driven wordmark logo. "
            "All identity comes from unique text design and careful kerning—no icons."
        ),
        "logo_style_description": (
            "A wordmark is a pure typographic logo—brand name as the sole visual element. Success relies on custom letterforms, "
            "distinctive spacing, and intentional graphical modifications (but nothing that compromises legibility)."
        ),
        "key_elements_guidance": (
            "Describe a one-of-a-kind font or hand-lettering approach. Suggest subtle customizations: e.g., ligatures, monoline alternates, smart use of negative space between/inside letters, "
            "minor graphical extensions (e.g., stylized crossbar, underlines). For short names, suggest iconic initials/letter combos; for long names, focus on horizontal balance and abbreviation strategies."
        ),
        "color_palette_guidance": (
            "Recommend a maximum of three colors used as solid fills (never gradients by default). Explain color choice for accenting specific glyphs/sections. "
            "Include hex codes. Remind the model to check contrast and outline adaptability when rendered in black/white."
        ),
        "typography_guidance": (
            "Typography is the entire identity. Define primary font—category (serif, sans, slab, script, display), weight variance, use of upper/lower/mixed case. "
            "Fine-tune letter spacing (kerning), line spacing if multi-line, and suggest which (if any) letters could be stylized for unique effect. Boldly reject decorative fonts that reduce clarity."
        ),
        "composition_guidance": (
            "Specify desired orientation (horizontal is default; vertical stacking for long/2-word brands only if superior). Recommend flush left or perfect centered alignment. "
            "Describe baseline, optical alignment, and 'breathing room' (ample white space around letters)."
        ),
        "industry_applications": (
            "Luxury: elegant serif or custom script, refined color accent. Tech: geometric sans, blue/gray palette, even spacing. Creative: playful letter interactions. Legal/finance: bold, stable sans or square-serif."
        ),
        "negative_prompt_suggestions": (
            "Do NOT include: standalone icons, graphic marks, decorative swooshes detached from letters. Avoid excessive ligatures, thin/illegible fonts, drop shadows, gradients, busy backgrounds. "
            "Never use handdrawn cursive unless specified by brand context."
        ),
        "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for a wordmark logo.
**Logo Text:** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Description:** {logo_style_description}
**Key Visual Elements (Typography Focus):** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style:** {typography_output}
**Composition Guidance:** {composition_guidance}
**Desired Output Format:** Flat vector illustration, isolated on a white background. Typographically crisp, optically well-spaced.
**Negative Prompt:** {negative_prompt_suggestions}

Prompt format example:
'Design a wordmark for "[LOGO_TEXT_PLACEHOLDER]" representing [USER_PROVIDED_CONCEPT_OR_INDUSTRY]. Use [key_elements_output] and colors [color_palette_output]. Typography: [typography_output]. Composition: [composition_guidance]. Output a flat logo with background whitespace, perfect typographic focus. Negative prompt: [negative_prompt_suggestions].'
"""
    }

def get_logo_lettermark_template(style_category: str) -> Dict[str, Any]:
    """
    Improved lettermark logo template logic:
    - Explicit monogram construction strategy (interlocking, stacking, geometry).
    - Professionally focused spacing and icon/letterform fusion details.
    - Modernized negative prompts (AI-specific pitfalls).
    """
    return {
        "preset_name": "Lettermark Logo Concept",
        "ai_prompt_focus": (
            "Generate a prompt for Imagen 3 to create a professional, high-clarity lettermark (monogram) logo. Focus on distinct, memorable initial interactions."
        ),
        "logo_style_description": (
            "A lettermark logo consists solely of 1–3 stylized initials. Encourage geometric fusion—overlap, interlock, or radial arrangement (as balanced, not crowded). "
            "Every detail highlights interplay between letters and clear, compact silhouette. Should scale well and remain recognizable even at favicon/app-icon size."
        ),
        "key_elements_guidance": (
            "Explain which letterforms should connect, share strokes, or use negative space for internal shapes. Suggest whether to enclose the mark (circle, square) or let it remain open "
            "based on the initial set. “Initial stacking” for tall monograms, or symmetry for short/wide ones."
        ),
        "color_palette_guidance": (
            "Suggest up to three harmonious colors for visual separation of letters (outline/fill/accents). List hex codes. State how design translates to black-and-white. Contrast and distinction are critical."
        ),
        "typography_guidance": (
            "Recommend a display sans or hybrid serif for clarity and modernity. For legal/corporate: square, bold sans. For creative brands: moderate flair, but always clarity first. Clearly state relative sizing/weight if not all initials are equal."
        ),
        "composition_guidance": (
            "Arrange initials for maximum recognition: either stacked, horizontal, or overlapped (brief rationale). Set precise spacing allowances. Clarify if surrounded by a border/shape or ‘break out’ effect. Show how the mark sits optically centered."
        ),
        "industry_applications": (
            "Tech: strong geometric monograms, angular. Finance/law: upright, enclosed shapes, no ambiguity. Fashion: elegant curve or contrasting weights. Sports: bold, dynamic diagonals or motion cues."
        ),
        "negative_prompt_suggestions": (
            "Do NOT include entire brand name, clipart, non-letter icons, photographic textures, unnecessary gradients, drop-shadows, or outline clutter. Avoid illegibility, excessive embellishment, or letter ambiguity."
        ),
        "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for a lettermark logo.
**Logo Initials:** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Description:** {logo_style_description}
**Key Visual Elements (Stylized Initials):** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style:** {typography_output}
**Composition Guidance:** {composition_guidance}
**Desired Output Format:** Flat vector, no effects, extremely clean outline, optically balanced.
**Negative Prompt:** {negative_prompt_suggestions}

Prompt format example:
'Design a lettermark logo for the initials "[LOGO_TEXT_PLACEHOLDER]" ([USER_PROVIDED_CONCEPT_OR_INDUSTRY]). Shape: [key_elements_output], palette: [color_palette_output], typography: [typography_output], structure: [composition_guidance]. Output as a flat, scalable, vector file on white. Negative prompt: [negative_prompt_suggestions].'
"""
    }

def get_logo_abstract_template(style_category: str) -> Dict[str, Any]:
    """
    Improved abstract logo template logic:
    - Highlights visual metaphor, geometric vs organic, emotional target.
    - Field-level advice for best use of AI's form+psycho-color abilities.
    - Strict prompt structure for legacy and multi-model compatibility.
    """
    return {
        "preset_name": "Abstract Logo Concept",
        "ai_prompt_focus": (
            "Generate a detailed prompt for Imagen 3 to create an abstract logo (no literal objects, pure shape/metaphor)."
            "Prioritize strong formal symbolism and clean, recognizable shapes."
        ),
        "logo_style_description": (
            "Abstract logos use geometric or flowing forms to represent a concept, value, or emotion—not a pictorial object. "
            "These marks excel in universality and timelessness, must be memorable without direct imagery. Modern, dynamic, and adaptable."
        ),
        "key_elements_guidance": (
            "Describe 2–3 abstract forms or movements (e.g., rising arc = growth; interlocking rings = partnership). "
            "Clarify which brand attribute each shape hints at. Indicate whether forms should touch, overlap, or float in relation."
        ),
        "color_palette_guidance": (
            "Pick up to four colors that carry meaning (blue = dependability, green = sustainability, red = passion), give hex codes/rationale. "
            "Define primary/accent roles, and ensure design is high-contrast and equivalent in monochrome."
        ),
        "typography_guidance": (
            "If text present, use a minimal clean sans or geometric font below/beside mark—keep it discrete. "
            "Specify size ratio, spacing, and whether text can be omitted for icon-only usage."
        ),
        "composition_guidance": (
            "Forms may be perfectly symmetrical (for order/stability) or asymmetrical (for energy/innovation). "
            "Define negative space: how does eye move through, what is the central visual impact, and how does mark adapt to squares/circles or open space."
        ),
        "industry_applications": (
            "Tech: connected dots or digital motifs. Creative: expressive curves, motion lines. Finance: sturdy geometric foundation (rect/tri/circle mix). Energy: dynamic waves/arcs."
        ),
        "negative_prompt_suggestions": (
            "Do NOT: include understandable icons, pictograms, photographs, visual clutter, gradients (unless strongly justified), busy backgrounds, or conflicting geometric themes. Avoid over-detailing and soft focus."
        ),
        "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for an abstract logo.
**Logo Text (if any):** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Description:** {logo_style_description}
**Key Visual Elements (Abstract Forms):** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style (if text included):** {typography_output}
**Composition Guidance:** {composition_guidance}
**Desired Output Format:** Flat vector, sharp clean lines, high contrast, isolated on white.
**Negative Prompt:** {negative_prompt_suggestions}

Prompt structure:
"Create an abstract logo for [USER_PROVIDED_CONCEPT_OR_INDUSTRY], not using any direct symbols. Shapes: [key_elements_output], palette: [color_palette_output], typography: [typography_output], layout: [composition_guidance]. Output as pure vector, white background, sharp shapes, no extraneous detail. Negative prompt: [negative_prompt_suggestions]."
"""
    }

def get_logo_mascot_template(style_category: str) -> Dict[str, Any]:
    """
    Improved mascot logo template logic:
    - Focuses on character-as-brand, clear interaction with text/scene.
    - Makes explicit key posture, emotion, and scaling robust to small sizes.
    - Actionable negative prompts address AI mascot rendering pathologies.
    """
    return {
        "preset_name": "Mascot Logo Concept",
        "ai_prompt_focus": (
            "Generate a rich text prompt for Imagen 3 to create a mascot-based logo—a character with brand-appropriate personality, in a pose that instantly signals approachability or energy."
        ),
        "logo_style_description": (
            "A mascot logo uses a unique, illustrated character or anthropomorphized element, usually created specifically for the brand. The character needs a clear personality—expressed by posture, face, eyes, and clothing or symbolic accessories (if included). Should look inviting, not generic."
        ),
        "key_elements_guidance": (
            "Define animal/type/species or object/abstract. Specify distinguishing features: e.g., eye size, primary color, clothing, tool/prop. Indicate pose or motion (sitting, jumping, waving, etc.), emotion (smile, focus), and whether mascot interacts with logo text or is separate."
        ),
        "color_palette_guidance": (
            "Suggest 3-5 colors per part: body, accent, clothing/accessory, always supply hex codes. Use high-contrast or strong, vibrant colors for legibility and impact. Note: must read clearly at tiny scale."
        ),
        "typography_guidance": (
            "If text is included, recommend a playful, bold, or stylized font matching the mascot’s personality—childlike if kid-focused, heroic if for sports, etc. State whether text is beneath, beside, or incorporated into mascot's outline. Recommend spacing to avoid crowding or obscured features."
        ),
        "composition_guidance": (
            "Specify if full-body or head-only works best. Position mascot so primary face looks at viewer. Specify whether the logo should be circularly contained, or loose on a white background with drop shadow forbidden. State minimum spacing/padding around subject/text for sticker/app usage."
        ),
        "industry_applications": (
            "Food/Bev: happy chef/ingredient/animal. Sports: dynamic creature/persona. Tech: cute bot/robot, not menacing. Education: wise owl, playful bookman, friendly animal."
        ),
        "negative_prompt_suggestions": (
            "Avoid: uncanny or photo-realistic human faces; scary or angry expressions; cluttered or detailed backgrounds; photobashing, collage, or fractal-like effects; cultural/gender stereotypes; thin lines that fail at icon size; more than four colors if possible."
        ),
        "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for a mascot logo.
**Logo Text (if any):** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Description:** {logo_style_description}
**Key Visual Elements (Mascot Character):** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style (if text included):** {typography_output}
**Composition Guidance:** {composition_guidance}
**Desired Output Format:** Illustration of mascot, vector, isolated on white background, with strong outline.
**Negative Prompt:** {negative_prompt_suggestions}

Prompt format example:
"Design a mascot logo: [key_elements_output]; brand: [USER_PROVIDED_CONCEPT_OR_INDUSTRY]; palette: [color_palette_output]; typography: [typography_output]; composition: [composition_guidance]. Output vector illustration on white, suitable for icon/sticker. Negative prompt: [negative_prompt_suggestions]."
"""
    }

def get_logo_illustrative_template(style_category: str) -> Dict[str, Any]:
    """
    Improved illustrative logo template logic:
    - Emphasis on focal storytelling and image-prompt synthesis.
    - Explicit field guidance for scalability and AI-unique strengths.
    - Negative prompt tailored to avoid common illustrative AI mishaps.
    """
    return {
        "preset_name": "Illustrative Logo Concept",
        "ai_prompt_focus": (
            "Generate a detailed text prompt for Imagen 3 to create a genuinely illustrative, story-driven logo. Must work at both large and icon/fav size."
        ),
        "logo_style_description": (
            "An illustrative logo uses hand-drawn or digital illustration techniques, combining focal imagery and/or scene with clear brand concept. Must be readable at small scale—story conveyed efficiently."
        ),
        "key_elements_guidance": (
            "Define the main illustrated subject and setting: e.g., '[USER_PROVIDED_CONCEPT_OR_INDUSTRY]' as a character, landscape, or symbolic object. Indicate level of detail (where main shapes are simple and secondary elements can be more textured). Suggest visual focal point and possible background/text combinations."
        ),
        "color_palette_guidance": (
            "Recommend a palette of 3–5 colors, matching the story and style (e.g., muted for vintage, saturated for playful, warm for tradition). Provide hex codes, primary/accent/contour assignments. State how the design will work in grayscale if necessary."
        ),
        "typography_guidance": (
            "Propose a font that matches the illustration’s visual style: e.g., hand-lettered, script, casual sans, or elegant serif. Clarify if text should be incorporated into the illustration (e.g., banner, scroll) or placed below/separate."
        ),
        "composition_guidance": (
            "Define main subject placement (center, left, within a frame, or over a background). Specify minimum/maximum negative space, and recommend simplified/zoomed variants for small-scale (favicon, sticker) usage."
        ),
        "industry_applications": (
            "Food: logo as drawn ingredient/scene. Adventure/outdoors: landmark, mapped scene, or adventurous pose. Crafts: tool or process illustrative narrative. Tourism: local landmark with ambient details."
        ),
        "negative_prompt_suggestions": (
            "Exclude: overly photographic look, background clutter, excessive minor details that are unreadable at small sizes, inconsistent line quality, muddled focal points, piecemeal collage, copy-paste feel, scale confusion."
        ),
        "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for an illustrative logo.
**Logo Text (if any):** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Description:** {logo_style_description}
**Key Visual Elements (Illustration):** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style (if text included):** {typography_output}
**Composition Guidance:** {composition_guidance}
**Desired Output Format:** Vector or raster illustration, clear focal subject, isolated on white. Must be scalable and readable as favicon.
**Negative Prompt:** {negative_prompt_suggestions}

Prompt structure example:
'Design an illustrative logo for [USER_PROVIDED_CONCEPT_OR_INDUSTRY]: [key_elements_output]. Palette: [color_palette_output]. Typography: [typography_output]. Layout: [composition_guidance]. Output: story-driven vector on white, recognizable at any size. Negative prompt: [negative_prompt_suggestions].'
"""
    }

def get_logo_3d_template(style_category: str) -> Dict[str, Any]:
    """
    Improved 3D logo template logic:
    - Explicit geometric/material/lighting cues, translation for 2D icon use.
    - Strict negative prompts: no soft/busy render or visual pollution.
    - Prompt structure for multi-view/model compatibility.
    """
    return {
        "preset_name": "3D Logo Concept",
        "ai_prompt_focus": (
            "Generate a detailed Imagen 3 prompt to create a visually impactful 3D logo—depth, reflection, clarity—always keeping its core shape recognizable in 2D exports."
        ),
        "logo_style_description": (
            "A 3D logo uses extrusion, realistic/inventive materials, and depth cues (lighting, shadows) to create a modern, memorable brand image. Must look strong both rendered and flattened as vector."
        ),
        "key_elements_guidance": (
            "State the core logo structure: e.g., extruded monogram, layered geometrics, or symbolic object. Define how surfaces curve, intersect, or layer. "
            "Describe perspective—front or slight isometric. Emphasize minimal, clear silhouette for adaptation to flat icon."
        ),
        "color_palette_guidance": (
            "Choose 2–4 main material colors—metallics (gold, silver, chrome), glass (blue, clear, frosted), plastic, or organic. Specify hex codes. "
            "If including gradients/reflection, keep them sharp and purposeful. Output should translate crisply to black and white."
        ),
        "typography_guidance": (
            "If text included, suggest a font style with high weight/thickness, simple geometry, and minimal serifs. Specify if text is extruded, embossed, or inset. Recommend no fine details or overlapping occlusion."
        ),
        "composition_guidance": (
            "Position mark at 15–30° tilt (top and side visible if extruded object), or completely flat-on if symbol. Set strong front lighting, optional rim light. Shadow on white or transparent. Zone of interest must remain clear if resized to 48x48px."
        ),
        "industry_applications": (
            "Tech: glossy blue/gray/black metal or glass with etched/engraved logotype. Construction: heavy stone/metallic chamfered edges. Luxe: gold accents, glass, reflective shadow. Entertainment: dynamic, colorful plastic."
        ),
        "negative_prompt_suggestions": (
            "Do NOT include photoreal background, soft blurry effects, noise, clutter, illegible reflections, too-high polygon count, visible rendering artifacts, or more than four color zones. No excessive depth or occlusion."
        ),
        "imagen3_prompt_structure": """
Generate an Imagen 3 prompt for a 3D logo.
**Logo Text (if any):** [LOGO_TEXT_PLACEHOLDER]
**Core Concept/Industry:** [USER_PROVIDED_CONCEPT_OR_INDUSTRY]
**Style Description:** {logo_style_description}
**Key Visual Elements (3D Form & Materials):** {key_elements_output}
**Color Palette (Hex Codes):** {color_palette_output}
**Typography Style (if text included):** {typography_output}
**Composition Guidance:** {composition_guidance}
**Desired Output Format:** 3D render, strong materials, crisp lighting, isolated on white or transparent BG. Must reduce well to flat icon.
**Negative Prompt:** {negative_prompt_suggestions}

Prompt structure example:
"Design a 3D logo for [USER_PROVIDED_CONCEPT_OR_INDUSTRY]: [key_elements_output]. Materials/palette: [color_palette_output]; typography: [typography_output]; composition: [composition_guidance]. Output: high-quality 3D render and vector export. Negative prompt: [negative_prompt_suggestions]."
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
