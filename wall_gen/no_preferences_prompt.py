"""
Strict prompt instructions for when user preferences are disabled.
These instructions focus on preserving the exact subject matter mentioned in the prompt.
"""
import re
import logging

# Instructions for enhancing custom prompts without user preferences
NO_PREFS_PROMPT_INSTRUCTIONS = """You are an expert prompt engineer for AI image generation. Your primary task is to STRICTLY PRESERVE THE EXACT SUBJECT MATTER of the original prompt while adding only essential details.

CRITICAL REQUIREMENTS - YOU MUST:
1. NEVER CHANGE THE ARTISTIC MEDIUM/STYLE - you must use EXACTLY what was specified:
   - If "watercolor painting" is mentioned, it MUST remain a watercolor painting
   - If "oil painting" is mentioned, it MUST remain an oil painting
   - If "3D render" is mentioned, it MUST remain a 3D render
   - If "pencil sketch" is mentioned, it MUST remain a pencil sketch
   - NEVER transform one medium into another (e.g., don't turn watercolor into 3D)

2. Maintain the EXACT subjects mentioned (e.g., hummingbird, flowers, city)
3. Preserve ALL descriptive elements (e.g., vibrant, hovering, sparkling)
4. Add ONLY complementary details that enhance without changing the core concept
5. NEVER substitute with different subjects or styles than explicitly requested

COMPOSITION CONTROL TECHNIQUES:
- Use directional terms like "centered subject", "rule of thirds", "foreground", "background", "wide angle"
- For full body shots, explicitly specify "full body visible", "from head to toe", "standing", "full length"  
- For portraits, specify "portrait framing", "headshot", or "bust shot" 
- Control the angle with "front view", "side view", "overhead view", or "from below"
- Describe scene scope: "close-up", "wide shot", "extreme close-up", or "panoramic view"

COMMON AI IMAGE ISSUE FIXES:
- To avoid anatomy issues, specify "anatomically correct", "proper proportions", "correct number of fingers"
- For better hands, include "detailed hands with five fingers", "natural hand pose"
- To prevent "two heads" issue, use "single head", "one face only"
- For full-body images, include terms like "standing", "full length", "legs visible", "feet visible"
- For faces, specify "symmetrical face", "detailed facial features", "proper eye alignment"

Follow these guidelines:
1. Technical Specifications:
   - Resolution: {resolution}
   - Aspect ratio: {aspect_ratio}

2. Subject and Medium Preservation:
   - The original artistic medium MUST BE PRESERVED EXACTLY (watercolor stays watercolor, etc.)
   - The original subjects MUST remain the central focus
   - ALL original descriptive adjectives MUST be preserved
   - ANY specific style, medium or technique MUST be maintained exactly as specified

3. Enhancement Approach:
   - Add technical clarity (lighting, perspective, composition)
   - Include subtle atmospheric elements that complement the scene
   - Enhance textures and surfaces of mentioned subjects while RESPECTING THE MEDIUM
   - Improve visual interest without changing the core concept

REMEMBER: Your primary goal is faithful enhancement of the original prompt. DO NOT introduce new subjects, change artistic styles, or alter the fundamental nature of what was requested.

Your enhanced prompt must be recognizable as a direct enhancement of the original - not a reimagination or reinterpretation.

IMPORTANT NOTES:
- If "watercolor" is specified, use watercolor-specific terminology (wet-on-wet, pigment blooms, paper texture, etc.)
- If "oil painting" is specified, use oil-specific terminology (impasto, brush strokes, canvas texture, etc.)
- If "sketch" is specified, use sketching terminology (hatching, pencil marks, etc.)
- If "3D render" is specified, use 3D terminology (rendering, polygons, etc.)
- MATCH THE TERMINOLOGY TO THE EXACT MEDIUM SPECIFIED
"""

# Instructions for random prompt generation without user preferences
NO_PREFS_RANDOM_INSTRUCTIONS = """You are an expert prompt engineer for AI image generation. Your task is to create a visually interesting prompt based on the provided tags, without relying on specific user preferences.

Follow these guidelines:
1. Technical Specifications:
   - Resolution: {resolution}
   - Aspect ratio: {aspect_ratio}

2. Subject Focus:
   - Use the EXACT tags provided as your primary subjects
   - Create a coherent scene that naturally incorporates all tags
   - Choose ONE clear artistic style that complements the subjects
   - Ensure the prompt has a clear focal point

3. Enhancement Approach:
   - Add clear specifications for lighting, angle, and composition
   - Include atmospheric elements that unify the scene
   - Specify particular details that enhance visual interest
   - Use consistent, complementary color palette descriptions

4. Negative Elements:
   - Avoid conflicting or contradictory descriptions
   - Maintain stylistic coherence throughout
   - Prevent vagueness or ambiguity

Your final prompt should be detailed enough to create a striking image, while maintaining the integrity of the original tags.
"""

# Art medium definitions with better compatibility for digital art styles
ART_MEDIUMS = {
    "watercolor": ["3d", "3d render", "3d art", "digital art", "oil painting", "acrylic", "photograph", "digital", "cgi", "render", "vector", "pixel art", "low poly", "voxel"],
    "oil painting": ["3d", "3d render", "3d art", "digital art", "watercolor", "acrylic", "photograph", "digital", "cgi", "render", "vector", "pixel art", "low poly", "voxel"],
    "sketch": ["3d", "3d render", "3d art", "digital art", "oil painting", "acrylic", "photograph", "digital", "cgi", "render", "vector", "pixel art", "low poly", "voxel"],
    "pencil": ["3d", "3d render", "3d art", "digital art", "oil painting", "acrylic", "photograph", "digital", "cgi", "render", "vector", "pixel art", "low poly", "voxel"],
    "acrylic": ["3d", "3d render", "3d art", "digital art", "oil painting", "watercolor", "photograph", "digital", "cgi", "render", "vector", "pixel art", "low poly", "voxel"],
    "drawing": ["3d", "3d render", "3d art", "digital art", "oil painting", "acrylic", "photograph", "digital", "cgi", "render", "vector", "pixel art", "low poly", "voxel"],
    "illustration": ["photograph", "photograph"], # Allow digital terms for illustration
    "photograph": ["3d", "3d render", "3d art", "digital art", "oil painting", "acrylic", "watercolor", "digital", "cgi", "render", "vector", "pixel art", "low poly", "voxel"],
    "3d": ["oil painting", "watercolor", "acrylic", "pencil", "sketch", "drawing", "photograph"],
    "digital art": ["oil painting", "watercolor", "acrylic", "pencil", "sketch", "photograph"],
    "pixel art": ["oil painting", "watercolor", "acrylic", "pencil", "photograph"], # New compatibility
    "isometric": ["oil painting", "watercolor", "acrylic", "pencil", "photograph"], # New compatibility
    "low poly": ["oil painting", "watercolor", "acrylic", "pencil", "photograph"], # New compatibility
}

# Medium-specific terminology
MEDIUM_TERMS = {
    "watercolor": ["watercolor", "wet-on-wet", "pigment", "wash", "paper", "fluid", "transparent"],
    "oil painting": ["oil painting", "impasto", "brush strokes", "canvas", "textured", "layered"],
    "sketch": ["sketch", "line work", "hatching", "paper", "pencil marks"],
    "pencil": ["pencil", "graphite", "shading", "cross-hatching"],
    "acrylic": ["acrylic", "paint", "canvas", "bold", "vibrant"],
    "drawing": ["drawing", "line art", "illustration", "pen", "ink"],
    "photograph": ["photograph", "photographic", "camera", "lens", "depth of field"],
}

# Style-specific terms that should not appear in traditional art mediums
DIGITAL_STYLE_TERMS = [
    "low poly", "low-poly", "polygonal", "voxel", "3d model", "3d modeling", 
    "3d mesh", "wireframe", "ray tracing", "ray-traced", "cgi", "computer generated",
    "polygon", "geometric mesh", "vertex", "vertices", "render", "rendering",
    "stylized 3d", "game engine", "digital model", "digital mesh", "game asset",
    "digital sculpt", "photorealistic rendering", "particle system", "procedural generation",
    "texture mapping", "shader", "volumetric lighting", "subsurface scattering"
]

# Traditional style terms that should not appear in digital/3D mediums
TRADITIONAL_STYLE_TERMS = [
    "brush stroke", "brushstroke", "impasto", "canvas texture", "pigment", "paint splatter",
    "oil on canvas", "watercolor paper", "wet on wet", "dry brush", "ink wash",
    "palette knife", "glazing technique", "stippling", "hatching", "cross-hatching"
]

def clean_text(text):
    """Clean text by removing excessive punctuation and whitespace."""
    # Remove repeated commas
    text = re.sub(r',\s*,', ',', text)
    # Remove commas before periods
    text = re.sub(r',\s*\.', '.', text)
    # Remove repeated spaces
    text = re.sub(r'\s+', ' ', text)
    # Remove spaces before commas/periods
    text = re.sub(r'\s+([,.])', r'\1', text)
    # Ensure space after commas
    text = re.sub(r',([^\s])', r', \1', text)
    # Remove comma at beginning of string
    text = re.sub(r'^,\s*', '', text)
    # Remove trailing commas
    text = re.sub(r',\s*$', '', text)
    # Fix ., pattern
    text = re.sub(r'\.\s*,', '.', text)
    # Fix period spacing
    text = re.sub(r'\.([^\s])', r'. \1', text)
    return text.strip()

def enforce_art_medium(prompt, original_prompt):
    """
    Enforce the correct art medium in the enhanced prompt.
    
    Args:
        prompt: The enhanced prompt
        original_prompt: The original prompt with art medium specified
        
    Returns:
        str: The corrected prompt with the right art medium
    """
    # Check for specific art medium in the original prompt
    detected_medium = None
    
    # Check for special digital styles first
    digital_styles = ["pixel art", "isometric", "low poly", "voxel art"]
    for style in digital_styles:
        if style.lower() in original_prompt.lower():
            detected_medium = style
            logging.info(f"Detected digital style in original prompt: {style}")
            break
    
    # If no digital style found, check regular mediums
    if not detected_medium:
        for medium in ART_MEDIUMS.keys():
            if medium.lower() in original_prompt.lower():
                detected_medium = medium
                logging.info(f"Detected art medium in original prompt: {medium}")
                break
            
    if not detected_medium:
        return clean_text(prompt)  # No specific medium detected, just clean up and return
    
    # Split into main and negative parts if Avoid: is present
    main_prompt = prompt
    neg_prompt = ""
    
    if "avoid:" in prompt.lower():
        parts = prompt.split("Avoid:")
        if len(parts) < 2:
            parts = prompt.split("avoid:")
        
        if len(parts) >= 2:
            main_prompt = parts[0].strip()
            neg_prompt = parts[1].strip()
    
    # Check if the detected medium is traditional (not 3D or digital)
    is_traditional = detected_medium.lower() not in ["3d", "digital art", "pixel art", "isometric", "low poly", "voxel art"]
    
    # Process the main prompt
    # Replace any direct mentions of competing media
    for competing in ART_MEDIUMS.get(detected_medium, []):
        # Make sure we don't replace parts of words by using word boundaries
        main_prompt = re.sub(r'\b' + re.escape(competing) + r'\b', 
                         detected_medium, 
                         main_prompt, 
                         flags=re.IGNORECASE)
    
    # If we have a traditional medium, remove inappropriate digital style terms
    if is_traditional:
        for term in DIGITAL_STYLE_TERMS:
            if term.lower() in main_prompt.lower():
                logging.warning(f"Removing digital style term '{term}' from {detected_medium} prompt")
                # Remove the term - be careful with word boundaries to not remove partial matches
                main_prompt = re.sub(r'\b' + re.escape(term) + r'\b', 
                             "", 
                             main_prompt, 
                             flags=re.IGNORECASE)
    # If we have a digital/3D medium, remove inappropriate traditional style terms
    else:
        for term in TRADITIONAL_STYLE_TERMS:
            if term.lower() in main_prompt.lower():
                logging.warning(f"Removing traditional style term '{term}' from {detected_medium} prompt")
                # Remove the term
                main_prompt = re.sub(r'\b' + re.escape(term) + r'\b', 
                             "", 
                             main_prompt, 
                             flags=re.IGNORECASE)
    
    # Make sure the medium appears somewhere in the prompt
    if detected_medium.lower() not in main_prompt.lower():
        # Add it at the beginning
        if "," in main_prompt:
            first_part, rest = main_prompt.split(",", 1)
            main_prompt = f"{first_part} in {detected_medium} style,{rest}"
        else:
            main_prompt = f"{main_prompt} in {detected_medium} style"
    
    # Add medium-specific terminology if missing
    if detected_medium in MEDIUM_TERMS:
        has_term = any(term.lower() in main_prompt.lower() 
                      for term in MEDIUM_TERMS[detected_medium])
        if not has_term:
            term_to_add = MEDIUM_TERMS[detected_medium][0]
            # Find a good place to add the term (after the first mention of the medium)
            medium_pos = main_prompt.lower().find(detected_medium.lower())
            if medium_pos >= 0:
                # Find the end of this word/phrase
                end_pos = medium_pos + len(detected_medium)
                while end_pos < len(main_prompt) and main_prompt[end_pos] not in [' ', ',', '.']:
                    end_pos += 1
                
                # Insert our term after this position
                main_prompt = main_prompt[:end_pos] + f" with {term_to_add} techniques" + main_prompt[end_pos:]
            else:
                # Just append it
                main_prompt += f", with {term_to_add} techniques"
    
    # Clean up the main prompt text
    main_prompt = clean_text(main_prompt)
    
    # Verify that the enhanced prompt still contains the core subject
    # Use a more careful approach to avoid over-triggering
    original_words = re.findall(r'\b\w+\b', original_prompt.lower())
    if not all(word in main_prompt.lower() for word in original_words if len(word) > 3):
        logging.warning("Enhanced prompt might not contain original subject, prepending it")
        # Make sure we don't duplicate content
        if not original_prompt.lower() in main_prompt.lower():
            # Remove "Here's your enhanced prompt:" or similar text if present
            main_prompt = re.sub(r"^here['']s (your|an|the) (enhanced|requested|final) prompt:?\s*", "", main_prompt, flags=re.IGNORECASE)
            main_prompt = f"{original_prompt}" + (". " if not original_prompt.endswith(".") else " ") + main_prompt
            main_prompt = clean_text(main_prompt)
    
    # Handle the negative prompt section
    if neg_prompt:
        # Make sure our medium is NOT in the negative prompt
        neg_prompt = re.sub(r'\b' + re.escape(detected_medium) + r'\b', 
                         "", 
                         neg_prompt, 
                         flags=re.IGNORECASE)
        
        # For digital styles like pixel art, remove 3D from the negative prompt
        if detected_medium.lower() in ["pixel art", "isometric", "low poly", "voxel art", "digital art", "3d"]:
            neg_prompt = re.sub(r'\b3d\b', "", neg_prompt, flags=re.IGNORECASE)
            
        # Clean up the negative prompt text
        neg_prompt = clean_text(neg_prompt)
        
        # Reassemble with the negative prompt
        complete_prompt = f"{main_prompt}"
        if complete_prompt.endswith("."):
            complete_prompt += f" Avoid: {neg_prompt}"
        else:
            complete_prompt += f". Avoid: {neg_prompt}"
            
        return complete_prompt
    else:
        # No negative prompt, just return the main part
        return main_prompt 