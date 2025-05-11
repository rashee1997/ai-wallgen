"""
Style Category Catalog for AI Preset Generator (Merged & Improved)

This module contains the merged and refined data structures for categorizing
style names, combining the strengths of the user's original upload and the
enhanced V3 catalog. It aims for maximum style detection coverage.

Includes:
- A comprehensive preferred order for resolving category conflicts.
- Definitions for hybrid styles (token-based and keyword-based).
- Extensive keywords for identifying various art styles and categories.
- Instructions for the AI when generating presets for specific categories.
- A list of all defined categories for reference.
"""
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple, Union

# --- Path for External Catalog Data ---
_DATA_PATH = Path(__file__).parent / "catalog_data"

# --- Comprehensive Preferred Order of Categories (Loaded from JSON) ---
def _load_preferred_order() -> List[str]:
    """
    Loads the preferred_order list from 'preferred_order.json'.
    This list dictates the priority for resolving style category conflicts.

    Returns:
        List[str]: A list of category names in order of preference.
    """
    with open(_DATA_PATH / "preferred_order.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    # The JSON file should contain the already de-duplicated list.
    return data

preferred_order: List[str] = _load_preferred_order()


# --- Hybrid Style Definitions (Token-based - Loaded from JSON) ---
def _load_hybrid_styles() -> Dict[frozenset[str], str]:
    """
    Loads token-based hybrid style rules from 'hybrid_token_rules.json'.
    These rules map sets of style tokens (keywords) to a specific hybrid category.

    Returns:
        Dict[frozenset[str], str]: A dictionary where keys are frozensets of
                                   token strings and values are the corresponding
                                   hybrid category names.
    """
    loaded_rules: List[Dict[str, Union[List[str], str]]] = []
    with open(_DATA_PATH / "hybrid_token_rules.json", "r", encoding="utf-8") as f:
        loaded_rules = json.load(f)
    
    hybrid_styles_reconstructed: Dict[frozenset[str], str] = {}
    for rule in loaded_rules:
        tokens_list = rule.get("tokens")
        category_str = rule.get("category")
        if isinstance(tokens_list, list) and isinstance(category_str, str) and category_str:
            # Ensure all items in tokens_list are strings before creating frozenset
            if all(isinstance(token, str) for token in tokens_list):
                hybrid_styles_reconstructed[frozenset(tokens_list)] = category_str
    return hybrid_styles_reconstructed

hybrid_styles: Dict[frozenset[str], str] = _load_hybrid_styles()

# --- Keyword-based Hybrid Category Definitions (Loaded from JSON) ---
def _load_hybrid_categories_keywords() -> Dict[str, List[Tuple[str, ...]]]:
    """
    Loads keyword-phrase based hybrid style rules from 'hybrid_keyword_rules.json'.
    These rules map hybrid category names to a list of keyword phrases (tuples of strings)
    that identify them.

    Returns:
        Dict[str, List[Tuple[str, ...]]]: A dictionary where keys are hybrid category
                                          names and values are lists of keyword phrases.
    """
    with open(_DATA_PATH / "hybrid_keyword_rules.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    # Convert inner lists of keywords back to tuples to match original type hint
    return {category: [tuple(phrase) for phrase in phrases] for category, phrases in data.items()}

hybrid_categories_keywords: Dict[str, List[Tuple[str, ...]]] = _load_hybrid_categories_keywords()

# --- General Category Keywords (Loaded from JSON) ---
def _load_categories_keywords() -> Dict[str, List[str]]:
    """
    Loads the general category keywords from 'style_keywords.json'.
    This dictionary maps category names to a list of keywords that help identify them.

    Returns:
        Dict[str, List[str]]: A dictionary where keys are category names and
                              values are lists of associated keyword strings.
    """
    with open(_DATA_PATH / "style_keywords.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    # Assuming keywords in JSON are already de-duplicated per category during its creation.
    return data

categories_keywords: Dict[str, List[str]] = _load_categories_keywords()

# --- All Categories List (Dynamically Generated - Merged) ---
def get_all_defined_categories() -> List[str]:
    """
    Generates and returns a sorted list of all unique category names
    defined across the various catalog data structures in this module.

    This includes categories from `preferred_order`, `hybrid_styles`,
    `hybrid_categories_keywords`, and `categories_keywords`.

    Returns:
        List[str]: A sorted list of all unique category names.
    """
    _all_cats: Set[str] = set(preferred_order) # Start with merged preferred order
    _all_cats.update(hybrid_styles.values())
    _all_cats.update(hybrid_categories_keywords.keys())
    _all_cats.update(categories_keywords.keys())
    return sorted(list(_all_cats))

all_categories: List[str] = get_all_defined_categories()

# --- Instructions for AI based on Category (Loaded from JSON) ---
_style_instructions: Dict[str, str] = {}

def _load_style_instructions():
    """
    Loads style instructions from 'style_instructions.json', processes internal templates
    (e.g., replacing placeholders like '{_portrait_base}'), and populates the
    global '_style_instructions' dictionary for runtime use.

    Additionally, this function saves the processed instructions to
    'style_instructions_corrected.json'. This corrected file serves as an
    import-time artifact, allowing developers to inspect the result of the
    template processing. The runtime logic in 'instructions_for_category'
    uses the in-memory '_style_instructions' dictionary.
    """
    global _style_instructions
    with open(_DATA_PATH / "style_instructions.json", "r", encoding="utf-8") as f:
        raw_instructions = json.load(f)

    # Resolve internal template references (e.g., {_portrait_base})
    # This is a simple one-level replacement; more complex templating could be added if needed.
    processed_instructions: Dict[str, str] = {}
    portrait_base_template = raw_instructions.get("_portrait_base", "")  # Get the base template string
    
    for key, value in raw_instructions.items():
        if isinstance(value, str):
            # Replace {_portrait_base} if present in the current instruction string
            temp_value = value.replace("{_portrait_base}", portrait_base_template)
            # Example for future: Add more template replacements here if other base templates are introduced
            # e.g., another_base_template = raw_instructions.get("_another_base", "")
            # temp_value = temp_value.replace("{_another_base}", another_base_template)
            processed_instructions[key] = temp_value
        else:
            # Handles non-string values like _default or _portrait_base if they are not meant to be processed themselves
            # but are used as templates by other string values.
            # It also correctly carries over any non-string, non-template values from the JSON.
            processed_instructions[key] = value

    _style_instructions = processed_instructions # Store processed instructions for runtime use

    # Save the fully processed instructions to 'style_instructions_corrected.json'.
    # This file can be useful for debugging or for external tools that might need
    # the resolved instructions. It is overwritten each time this module is imported.
    try:
        with open(_DATA_PATH / "style_instructions_corrected.json", "w", encoding="utf-8") as f_corrected:
            json.dump(processed_instructions, f_corrected, indent=4, ensure_ascii=False)
        # print(f"Successfully wrote processed instructions to style_instructions_corrected.json") # Optional: for debugging
    except IOError as e:
        # Handle potential error during writing, e.g., log it or print a warning
        print(f"Warning (IOError): Could not write to style_instructions_corrected.json: {e}")
    except Exception as e:
        # Catch any other exceptions during the dump/write
        print(f"ERROR (General Exception) during writing style_instructions_corrected.json: {type(e).__name__} - {e}")


_load_style_instructions() # Load at module initialization

def instructions_for_category(category: str, base_style: str) -> str:
    """Return specific instructions for the AI based on the detected style category."""
    category = category.lower()
    base_style_clean = base_style.replace('_', ' ').title()
    
    instruction_template = _style_instructions.get(category, _style_instructions.get("_default", ""))
    
    # Ensure the template is a string before formatting
    if not isinstance(instruction_template, str):
        # Fallback if template is somehow not a string (e.g. if _default was missing or not a string)
        default_fallback_template = "Emphasize the core characteristics of '{base_style_clean}'. Ensure settings enhance its unique aesthetic."
        return default_fallback_template.format(base_style_clean=base_style_clean)

    return instruction_template.format(base_style_clean=base_style_clean)
