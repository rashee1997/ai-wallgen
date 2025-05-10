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
    """Loads the preferred_order list from an external JSON file."""
    with open(_DATA_PATH / "preferred_order.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    # The JSON file should contain the already de-duplicated list.
    return data

preferred_order: List[str] = _load_preferred_order()


# --- Hybrid Style Definitions (Token-based - Loaded from JSON) ---
def _load_hybrid_styles() -> Dict[frozenset[str], str]:
    """Loads token-based hybrid style rules from an external JSON file."""
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
    """Loads keyword-phrase based hybrid rules from an external JSON file."""
    with open(_DATA_PATH / "hybrid_keyword_rules.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    # Convert inner lists of keywords back to tuples to match original type hint
    return {category: [tuple(phrase) for phrase in phrases] for category, phrases in data.items()}

hybrid_categories_keywords: Dict[str, List[Tuple[str, ...]]] = _load_hybrid_categories_keywords()

# --- General Category Keywords (Loaded from JSON) ---
def _load_categories_keywords() -> Dict[str, List[str]]:
    """Loads the categories_keywords dictionary from an external JSON file."""
    with open(_DATA_PATH / "style_keywords.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    # Assuming keywords in JSON are already de-duplicated per category during its creation.
    return data

categories_keywords: Dict[str, List[str]] = _load_categories_keywords()

# --- All Categories List (Dynamically Generated - Merged) ---
def get_all_defined_categories() -> List[str]:
    """Returns a sorted list of all unique category names defined in this merged catalog."""
    _all_cats: Set[str] = set(preferred_order) # Start with merged preferred order
    _all_cats.update(hybrid_styles.values())
    _all_cats.update(hybrid_categories_keywords.keys())
    _all_cats.update(categories_keywords.keys())
    return sorted(list(_all_cats))

all_categories: List[str] = get_all_defined_categories()

# --- Instructions for AI based on Category (Loaded from JSON) ---
_style_instructions: Dict[str, str] = {}

def _load_style_instructions():
    """Loads style instructions from an external JSON file and processes internal templates."""
    global _style_instructions
    with open(_DATA_PATH / "style_instructions.json", "r", encoding="utf-8") as f:
        raw_instructions = json.load(f)

    # Resolve internal template references (e.g., {_portrait_base})
    # This is a simple one-level replacement; more complex templating could be added if needed.
    processed_instructions: Dict[str, str] = {}
    portrait_base_template = raw_instructions.get("_portrait_base", "")
    
    for key, value in raw_instructions.items():
        if isinstance(value, str):
            # Replace {_portrait_base} if present
            temp_value = value.replace("{_portrait_base}", portrait_base_template)
            # Add more template replacements here if other base templates are introduced
            # e.g., temp_value = temp_value.replace("{_another_base}", raw_instructions.get("_another_base", ""))
            processed_instructions[key] = temp_value
        else:
    # Non-string values (like _default, _portrait_base themselves if not used as templates in others)
            processed_instructions[key] = value

    _style_instructions = processed_instructions

    # Save the processed instructions to the corrected file
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
