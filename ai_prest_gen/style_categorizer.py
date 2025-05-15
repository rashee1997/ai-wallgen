# ai_prest_gen/style_categorizer.py
"""
Handles the categorization of style names based on catalog data.
"""
import re
import logging
from typing import Dict, Any, List, Optional, Union, Set

# Attempt to import catalog data; this module relies heavily on it.
# In a larger refactor, these might be passed in or accessed via a shared context.
try:
    from .style_category_catalog import (
        hybrid_styles,
        hybrid_categories_keywords,
        categories_keywords,
        preferred_order
    )
    CATALOG_DATA_AVAILABLE = True
except ImportError:
    logging.error("StyleCategorizer: Failed to import catalog data from .style_category_catalog. Categorization will be limited.")
    CATALOG_DATA_AVAILABLE = False
    # Define fallbacks for catalog data if not available
    hybrid_styles: Dict[frozenset[str], str] = {}
    hybrid_categories_keywords: Dict[str, List[tuple[str, ...]]] = {} # type: ignore
    categories_keywords: Dict[str, List[str]] = {}
preferred_order: List[str] = ["default", "unknown"]

# Attempt to import the new AI Categorizer
try:
    from .ai_categorizer import AICategorizer, GEMINI_AVAILABLE as AI_CATEGORIZER_AVAILABLE
except ImportError:
    AICategorizer = None
    AI_CATEGORIZER_AVAILABLE = False


def normalize_style_name_for_catalog(style_name: str) -> str:
    """
    Normalizes a style name for consistent matching against catalog keywords.
    This is a direct copy of the normalization logic from ai_preset_generator.py.
    """
    name = str(style_name).lower()
    name = name.replace('_', ' ').replace('-', ' ') # Replace underscores and hyphens with spaces
    name = name.replace('colour', 'color')
    name = name.replace('water color', 'watercolor') # Specific common normalization
    name = re.sub(r'\s+', ' ', name).strip() # Consolidate multiple spaces and strip
    return name


class StyleCategorizer:
    """
    Categorizes a style name based on a comprehensive catalog of keywords,
    hybrid rules, and a preferred order for conflict resolution.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if not CATALOG_DATA_AVAILABLE:
            self.logger.critical("StyleCategorizer initialized without catalog data. Functionality will be severely limited.")

        self.ai_categorizer = None
        if AI_CATEGORIZER_AVAILABLE:
            try:
                self.ai_categorizer = AICategorizer()
                self.logger.info("AI Categorizer initialized.")
            except Exception as e:
                self.logger.error(f"Failed to initialize AI Categorizer: {e}", exc_info=True)
                self.ai_categorizer = None
        # Data is loaded at module level, no need to pass explicitly if using module-level imports
        # self.hybrid_styles = hybrid_styles
        # self.hybrid_categories_keywords = hybrid_categories_keywords
        # self.categories_keywords = categories_keywords
        # self.preferred_order = preferred_order
        
    def categorize_style(self, style_name_input: Union[str, Dict[str, Any]], user_prefs: Optional[Any] = None) -> str:
        """
        Attempts to categorize a style name based on the loaded catalog logic or AI.

        Args:
            style_name_input: The style name string or a dictionary containing a 'name' key.

        Returns:
            The determined style category string (e.g., "oil_painting", "cyberpunk_portrait").
            Returns "unknown" if no specific category can be determined.
        """
        # Check if AI categorization is enabled and available
        use_ai = getattr(user_prefs, 'use_ai_categorization', False) if user_prefs else False
        
        if use_ai and self.ai_categorizer:
            self.logger.debug(f"Attempting AI categorization for input: '{style_name_input}'")
            ai_category = self.ai_categorizer.categorize_style_with_gemini(style_name_input, user_prefs)
            if ai_category is not None: # AI categorization was attempted and returned a result (could be "unknown")
                self.logger.info(f"AI categorization result: '{ai_category}' for input: '{style_name_input}'. Using AI result.")
                return ai_category
            else:
                self.logger.warning(f"AI categorization failed for input: '{style_name_input}'. Falling back to classic logic.")

        # Fallback to classic Python logic if AI is not used, not available, or failed
        self.logger.debug(f"Using classic Python categorization logic for input: '{style_name_input}'.")
        if not CATALOG_DATA_AVAILABLE:
            self.logger.warning("Style catalog data not available, categorization limited to 'unknown'.")
            return "unknown"

        if isinstance(style_name_input, dict):
            style_name_str = style_name_input.get('name', '')
        else:
            style_name_str = str(style_name_input)

        normalized_style = normalize_style_name_for_catalog(style_name_str)
        if not normalized_style:
            self.logger.debug(f"Empty normalized style from input: '{style_name_input}'. Returning 'unknown'.")
            return "unknown"

        style_lower = normalized_style
        self.logger.debug(f"Attempting to categorize normalized style: '{style_lower}' (from input: '{style_name_str}')")

        # 1. Token-based Hybrid Style Mapping
        tokens = [t.strip() for t in re.split(r'[,+/&|\s]+', style_lower) if t.strip()]
        tokens_set = frozenset(tokens)
        self.logger.debug(f"Tokens for matching: {tokens_set}")

        for hybrid_set, hybrid_cat in hybrid_styles.items():
            if hybrid_set.issubset(tokens_set):
                self.logger.info(f"Matched token-based hybrid: '{hybrid_cat}' for '{style_name_str}' using tokens {hybrid_set}")
                return hybrid_cat

        # 2. Keyword-phrase-based Hybrid Category Definitions
        for category, keyword_phrase_list in hybrid_categories_keywords.items():
            for phrase_tuple in keyword_phrase_list: # phrase_tuple is like ('watercolor', 'pencil')
                # Reconstruct phrase for regex, ensuring terms are normalized like in categorize_style
                # This part needs careful handling if terms in JSON aren't pre-normalized
                # Assuming terms in JSON are already simple and don't need re.escape heavily
                # The original logic used normalize_style_name(term) inside the loop for each term in the phrase
                # For simplicity here, we assume the JSON phrases are already normalized or simple enough.
                # A more robust approach would normalize each part of the phrase from JSON.
                
                # Let's refine this to match the original logic more closely:
                # The original logic searched for each *term* within the phrase list using normalize_style_name(term)
                # This seems to imply that `hybrid_categories_keywords` in the original `categorize_style`
                # was structured as `Dict[str, List[str]]` where each string in the list was a single term,
                # not a phrase.
                # Re-checking `ai_preset_generator.py` line 331:
                # `for category, keyword_list in hybrid_categories_keywords.items():`
                # `  for term in keyword_list:` -> here term was a single string.
                # The `hybrid_keyword_rules.json` has `List[List[str]]` which became `List[Tuple[str,...]]`
                # So, the original logic was:
                # for category, list_of_phrases in hybrid_categories_keywords.items():
                #    for phrase_tuple in list_of_phrases:
                #        # This is where it gets tricky. The original code did:
                #        # for term in keyword_list: (where keyword_list was a flat list of strings for a category)
                #        # if re.search(r'\b' + re.escape(normalize_style_name(term)) + r'\b', style_lower):
                # This means the `hybrid_categories_keywords` in `style_category_catalog.py`
                # should be `Dict[str, List[str]]` not `Dict[str, List[Tuple[str,...]]]` if it's to match
                # the loop structure `for term in keyword_list`.
                # Given the JSON structure `{"category": [["kw1", "kw2"], ["kw3"]]}`,
                # the `_load_hybrid_categories_keywords` in `style_category_catalog.py` correctly makes it
                # `Dict[str, List[Tuple[str,...]]]`.
                # The loop in `ai_preset_generator.py` at line 332 was `for term in keyword_list:`,
                # which implies `keyword_list` was a flat list of strings.
                # This suggests a mismatch in my understanding or the original code's variable naming.
                # Let's assume `hybrid_categories_keywords` from `style_category_catalog.py` is `Dict[str, List[str]]`
                # as used in the original `categorize_style` loop.
                # If `hybrid_keyword_rules.json` is `{"category": [["phrase1 word1", "phrase1 word2"], ["phrase2"]]}`,
                # then `hybrid_categories_keywords` should be `Dict[str, List[str]]` where each string is a full phrase.

                # Correcting based on `ai_preset_generator.py` line 331-335:
                # `hybrid_categories_keywords` is `Dict[str, List[str]]` where each string is a keyword.
                # The JSON `hybrid_keyword_rules.json` is `{"category": [["kw1", "kw2"], ["kw3"]]}`
                # This means `hybrid_categories_keywords` in `style_category_catalog.py` should be
                # `Dict[str, List[str]]` by flattening the inner lists or by changing the JSON structure.
                # For now, I will assume `hybrid_categories_keywords` is `Dict[str, List[str]]` as per the original loop.
                # The `_load_hybrid_categories_keywords` in `style_category_catalog.py` would need adjustment
                # if the JSON is truly `List[List[str]]` per category.
                # The current `style_category_catalog.py` loads it as `Dict[str, List[Tuple[str, ...]]]`
                # This means the loop in `ai_preset_generator.py` was iterating over tuples.
                # `for term in keyword_list:` where `keyword_list` is `List[Tuple[str,...]]`
                # This means `term` is a `Tuple[str,...]`. This is not what `re.escape(normalize_style_name(term))` expects.

                # Let's stick to the structure of `hybrid_keyword_rules.json` as `{"category": [["phrase", "word1", "word2"], ["other", "phrase"]]}`
                # and assume `hybrid_categories_keywords` in `style_category_catalog.py` is `Dict[str, List[List[str]]]` or `Dict[str, List[Tuple[str,...]]]`
                # The original code at line 333: `for term in keyword_list:`
                # This implies `keyword_list` was a flat list of terms for that category.
                # The `hybrid_keyword_rules.json` structure is `{"category_name": [ ["keyword1", "keyword2"], ["another_keyword_set"] ]}`.
                # The `style_category_catalog.py` loads this as `Dict[str, List[Tuple[str, ...]]]`
                # The loop in `ai_preset_generator.py` (line 332) `for term in keyword_list:` where `keyword_list` is `List[Tuple[str,...]]`
                # means `term` is a tuple of strings.
                # The regex `re.search(r'\b' + re.escape(normalize_style_name(term)) + r'\b', style_lower)`
                # will fail because `term` is a tuple.

                # The original `categorize_style` (line 331-335) seems to expect `hybrid_categories_keywords`
                # to be `Dict[str, List[str]]` where each string is a single keyword to search for.
                # Let's assume this structure for `hybrid_categories_keywords` for now,
                # meaning `hybrid_keyword_rules.json` should be `{"category": ["keyword1", "keyword2 for this cat"]}`.
                # If `hybrid_keyword_rules.json` is meant for *phrases*, the logic needs to change.
                # The `ai_preset_generator.py` line 333 `for term in keyword_list:` suggests it's a list of single terms.

                # Given the current `hybrid_keyword_rules.json` structure:
                # {"category": [["phrase", "word1", "word2"], ["other", "phrase"]]}
                # and `hybrid_categories_keywords` loaded as `Dict[str, List[Tuple[str,...]]]`
                # The loop should be:
                for category, list_of_phrase_tuples in hybrid_categories_keywords.items():
                    for phrase_tuple in list_of_phrase_tuples:
                        # Convert tuple to a string phrase, normalize it, then search
                        phrase_str = " ".join(phrase_tuple)
                        normalized_phrase_to_search = normalize_style_name_for_catalog(phrase_str)
                        if re.search(r'\b' + re.escape(normalized_phrase_to_search) + r'\b', style_lower):
                            self.logger.info(f"Matched keyword-phrase hybrid: '{category}' using phrase '{phrase_str}' for '{style_name_str}'")
                            return category
        
        # 3. General/Single-Term Category Keywords
        matched_categories: Set[str] = set()
        for category, keyword_list_for_cat in categories_keywords.items():
            for term in keyword_list_for_cat:
                normalized_term_to_search = normalize_style_name_for_catalog(term)
                if re.search(r'\b' + re.escape(normalized_term_to_search) + r'\b', style_lower):
                    # This is where the original code had specific mappings.
                    # For now, we'll just add the matched category.
                    # The plan includes moving these mappings to data later.
                    mapped_category = category # Default to original category
                    
                    # Re-inserting the original mapping logic here for now.
                    # This should be refactored into data files as per the plan.
                    if category == "3d_render": mapped_category = "3d_render"
                    elif category in ["oil_painting", "watercolor", "pastel", "charcoal"]: pass # No change
                    elif category == "line_art": mapped_category = "line_art"
                    elif category in ["pencil_sketch", "ink_drawing"]: mapped_category = "drawing"
                    elif category.startswith("illustration"): pass # No change
                    elif category == "digital_art": mapped_category = "digital_art"
                    elif category == "game_style": mapped_category = "game_style"
                    elif category in ["photographic", "cinematic", "realism"]: pass # No change
                    elif category in ["abstract", "abstract_conceptual"]: mapped_category = "abstract_conceptual"
                    elif category in ["material_sculptural", "sculpture"]: mapped_category = "material_sculptural"
                    elif category in ["fantasy", "sci_fi"]: pass # No change
                    elif category == "traditional_painting_drawing": mapped_category = "traditional_painting_drawing"
                    
                    self.logger.info(f"Matched single-term: '{mapped_category}' (original: '{category}') using term '{term}' for '{style_name_str}'")
                    matched_categories.add(mapped_category)

        # 4. Prioritize and Return
        if matched_categories:
            self.logger.debug(f"Multiple categories matched: {matched_categories}. Applying preferred order.")
            for pref_cat in preferred_order:
                if pref_cat in matched_categories:
                    self.logger.info(f"Prioritized match: '{pref_cat}' for '{style_name_str}'")
                    return pref_cat
            
            # Fallback if no preferred match found among matched_categories (should not happen if preferred_order is comprehensive)
            fallback_match = sorted(list(matched_categories))[0]
            self.logger.info(f"Fallback alphabetical match from matched_categories: '{fallback_match}' for '{style_name_str}'")
            return fallback_match

        # 5. Explicit final fallback for single-term categories (direct match of normalized style to a category key)
        # This was the original code's line 379-383
        single_term_direct_match = style_lower.strip()
        if single_term_direct_match in categories_keywords: # Check if the normalized style itself is a category key
            self.logger.info(f"Final single-term direct category key match: '{single_term_direct_match}' for '{style_name_str}'")
            return single_term_direct_match

        self.logger.warning(f"Could not categorize style: '{style_name_str}'. Falling back to 'unknown'.")
        return "unknown"
