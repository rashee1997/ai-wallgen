#!/usr/bin/env python3
"""Settings Utilities Module - Functions for handling settings in prompt generation

This module contains utility functions for processing and transforming settings 
data for use in prompt generation.
"""
from typing import Dict, List, Any, Tuple, Optional, Set


def flatten_settings(settings: Dict[str, Any], parent_key: str = "", sep: str = " - ", 
                   ignore_keys: Optional[Set[str]] = None) -> List[Tuple[str, str, str]]:
    """
    Recursively flatten a settings dictionary into a list of (section, field, value) tuples for prompt context.
    Allows for dynamic prompt generation accommodating arbitrary new fields/styles.
    Now handles non-standard settings from user_preferences.json by preserving all valid values.

    Args:
        settings (dict): Nested dictionary of settings.
        parent_key (str): Current section or parent prefix.
        sep (str): Separator between parent and child keys.
        ignore_keys (set): Keys to ignore from output.

    Returns:
        List of (section, field, value) tuples suitable for inclusion in a prompt.
    """
    ignore_keys = ignore_keys or set(["negative_prompt"])  # Negative prompt handled separately
    flattened = []
    if not isinstance(settings, dict):
        return flattened
    for k, v in settings.items():
        if k in ignore_keys:
            continue
        pretty_key = k.replace("_", " ").capitalize()
        full_key = f"{parent_key}{sep}{pretty_key}" if parent_key else pretty_key
        if isinstance(v, dict):
            sub = flatten_settings(v, parent_key=full_key, sep=sep, ignore_keys=ignore_keys)
            flattened.extend(sub)
        elif isinstance(v, list):
            list_val = ", ".join(str(x) for x in v if x)
            if list_val:
                flattened.append((parent_key if parent_key else pretty_key, pretty_key, list_val))
        elif v is not None and v != "" and v != "Not specified" and v != "none" and v != "None":
            flattened.append((parent_key if parent_key else pretty_key, pretty_key, str(v)))
    return flattened


def dynamic_technical_context(settings: Dict[str, Any], aspect_ratio: str = "16:9",
                            resolution: str = "3840x2160") -> str:
    """
    Build a narrative technical context for prompts from all user preferences/settings (dynamic, grouped),
    synthesizing each key/value pair into natural language descriptive phrases for the AI to integrate.
    
    Args:
        settings (dict): Dictionary of settings to include in the technical context.
        aspect_ratio (str): Aspect ratio setting (default: "16:9")
        resolution (str): Resolution setting (default: "3840x2160")
        
    Returns:
        str: A natural language technical context for use in AI prompts
    """
    def phrase_from_kv(section: str, field: str, value: str) -> Optional[str]:
        # Natural language phrasing that blends settings into flowing descriptions
        # Now handles non-standard settings with more flexible matching
        key = field.lower()
        val = str(value)
        
        # Handle empty/null values
        if not val or val.lower() in ("none", "not specified", ""):
            return None
            
        # Standard settings
        if key in ["lighting type", "light quality"]:
            return f"illuminated by {val} lighting that"
        elif key in ["color scheme", "palette type", "color temperature"]:
            return f"using a {val} color palette that"
        elif "brush" in key or "painting" in key or "medium" in key or "canvas" in key:
            return f"rendered in {val} {key.replace('_',' ')} with"
        elif key in ["detail level", "texture quality"]:
            return f"featuring {val} {key.replace('_', ' ')} that"
        elif key in ["focal point"]:
            return f"centered around {val} with"
        elif key in ["season", "weather"]:
            return f"set in {val} conditions where"
        elif key in ["post processing", "special effects"]:
            return f"enhanced with {val} effects creating"
        elif key in ["movement type", "composition type"]:
            return f"composed with {val} movement that"
        elif "style" in key and "style era" not in key:
            return f"in {val} style featuring"
        elif key == "aspect ratio":
            return None
        elif key == "resolution":
            return None
            
        # Handle camera settings explicitly
        camera_keys = [
            "camera model",
            "lens type",
            "aperture",
            "special lens",
            "focal length",
            "shutter speed",
            "iso",
            "filter type",
            "depth of field",
            "white balance",
            "focus mode",
            "exposure mode",
            "image stabilization",
            "metering mode",
            "flash mode",
            "shooting mode",
            "focus point selection",
            "image format",
            "color space",
        ]
        if key in camera_keys:
            return f"captured with {val} {key}"
            
        # Handle non-standard settings with flexible matching
        if "setting" in key or "preference" in key or "option" in key:
            return f"with {val} {key.replace('_', ' ')} that"
            
        # Default natural phrasing for any other fields
        return f"with {val} {key.replace('_', ' ')} that"
    
    flat = flatten_settings(settings)
    # Filter and phrase up all non-empty fields
    phrases = [phrase_from_kv(section, field, value) for section, field, value in flat]
    phrases = [p for p in phrases if p and not p.strip().lower().startswith("none")]
    # Remove redundancies
    deduped = []
    for p in phrases:
        if p not in deduped:
            deduped.append(p)
    if deduped:
        # Join phrases with natural language connectors
        if len(deduped) == 1:
            text = deduped[0]
        else:
            text = ", ".join(deduped[:-1]) + " and " + deduped[-1]
    else:
        text = ""
    # Always enforce aspect ratio/resolution at the end
    if text:
        text += " with "
    text += f"{resolution} resolution in {aspect_ratio} aspect ratio"
    return text
