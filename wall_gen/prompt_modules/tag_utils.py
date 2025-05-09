#!/usr/bin/env python3
"""Tag Utilities Module - Functions for generating and managing tags for prompts

This module contains utility functions for working with tags, including random 
tag selection and style mixing for prompt generation.
"""
import random
from typing import List, Dict, Any, Optional

# For type hints
from .types import SimplePrefs


def select_random_tags(user_prefs: Optional[Any] = None) -> List[str]:
    """
    Select a focused set of tags for Gemini prompt generation by sampling from a limited set of 
    related categories. Prioritizes user preferences when available.
    
    Args:
        user_prefs: Optional user preferences object to consider when selecting tags
    
    Returns:
        list: A carefully curated selection of 3-5 related tags
    """
    # Import from core to avoid circular imports
    try:
        from .core import use_user_preferences
    except ImportError:
        use_user_preferences = True
    
    # Import here to avoid circular imports
    try:
        from ..config import (
            nature_tags, space_tags, sea_tags, flowers_tags, urban_tags, fantasy_tags, 
            abstract_tags, mood_tags, weather_tags, time_tags, season_tags, color_tags,
            material_tags, lighting_tags, pattern_tags, terrain_tags, emotion_tags, 
            architecture_tags
        )
    except ImportError:
        # Fallback minimal tags if config not available
        nature_tags = ["mountains", "forest", "river", "sunset"]
        fantasy_tags = ["dragon", "castle", "wizard", "magic"]
        urban_tags = ["cityscape", "skyscraper", "street", "neon"]
        abstract_tags = ["geometric", "fractal", "minimalist", "pattern"]
        mood_tags = ["peaceful", "dramatic", "serene", "mysterious"]
        # Empty lists for other categories
        space_tags, sea_tags, flowers_tags = [], [], []
        weather_tags, time_tags, season_tags = [], [], []
        color_tags, material_tags, lighting_tags = [], [], []
        pattern_tags, terrain_tags, emotion_tags, architecture_tags = [], [], [], []
    
    # Check if user has preferred subjects in their preferences
    preferred_subjects = []
    if user_prefs and use_user_preferences:
        # Try to get preferred subjects from user preferences
        if hasattr(user_prefs, 'preferred_subjects'):
            preferred_subjects = getattr(user_prefs, 'preferred_subjects', [])
        
        # Also check in imagen_settings
        settings = getattr(user_prefs, 'imagen_settings', {}) or {}
        if 'preferred_subjects' in settings:
            preferred_subjects.extend(settings['preferred_subjects'])
    
    # If we have preferred subjects, prioritize them
    if preferred_subjects:
        # Take 2-3 preferred subjects if available
        if len(preferred_subjects) >= 3:
            return random.sample(preferred_subjects, random.randint(2, 3))
        # Otherwise use all preferred subjects
        selected_tags = preferred_subjects.copy()
        # We'll add more from related categories later
    else:
        selected_tags = []
    
    # Choose a primary category for coherence (if no user preferences)
    if not selected_tags:
        primary_categories = [
            ("nature", nature_tags),
            ("fantasy", fantasy_tags),
            ("urban", urban_tags),
            ("abstract", abstract_tags)
        ]
        # Filter out empty categories
        valid_categories = [(name, tags) for name, tags in primary_categories if tags]
        
        # If no valid categories, return some basic tags
        if not valid_categories:
            return ["landscape", "artistic", "wallpaper"]
            
        # Choose one primary category
        primary_name, primary_tags = random.choice(valid_categories)
        
        # Select 1-2 tags from primary category
        num_primary = min(len(primary_tags), random.randint(1, 2))
        selected_tags.extend(random.sample(primary_tags, num_primary))
    
    # Define related category groups for coherence
    related_categories = {
        "nature": [nature_tags, season_tags, weather_tags, terrain_tags],
        "fantasy": [fantasy_tags, mood_tags, emotion_tags],
        "urban": [urban_tags, architecture_tags, time_tags],
        "abstract": [abstract_tags, pattern_tags, color_tags],
        "general": [mood_tags, lighting_tags, material_tags]
    }
    
    # Choose 1-2 related categories to sample from
    all_related = []
    # If we have user preferences, use general + 1 random category
    if preferred_subjects:
        all_related.extend(related_categories["general"])
        # Add one more random category
        random_category = random.choice(list(related_categories.keys()))
        all_related.extend(related_categories[random_category])
    # Otherwise use related categories based on the primary one we chose
    else:
        # Add general mood tags to any selection
        all_related.extend(related_categories["general"])
        # Try to add related categories for the primary if it exists
        if 'primary_name' in locals() and primary_name in related_categories:
            all_related.extend(related_categories[primary_name])
    
    # Filter out empty categories
    valid_related = [cat for cat in all_related if cat]
    
    # Sample from related categories until we have 3-5 total tags
    while len(selected_tags) < 5 and valid_related:
        # Pick a random related category
        related_category = random.choice(valid_related)
        # Remove this category to avoid resampling
        valid_related.remove(related_category)
        
        # If there are tags in this category, add one
        if related_category:
            tag = random.choice(related_category)
            # Only add if not already selected
            if tag not in selected_tags:
                selected_tags.append(tag)
    
    # Ensure we have at least 2 tags
    if len(selected_tags) < 2:
        # Add generic tags if needed
        generic_tags = ["artistic", "beautiful", "detailed"]
        for tag in generic_tags:
            if tag not in selected_tags:
                selected_tags.append(tag)
            if len(selected_tags) >= 3:
                break
    
    # Shuffle the order for variety
    random.shuffle(selected_tags)
    
    # Limit to 3-5 tags maximum for coherence
    max_tags = min(len(selected_tags), random.randint(3, 5))
    return selected_tags[:max_tags]


def generate_random_style_mix(user_prefs: Optional[Any] = None) -> str:
    """Generate a random mix of artistic styles.
    
    This function combines styles from different categories to create unique
    style combinations for image generation prompts.
    
    Args:
        user_prefs: Optional user preferences object. If None and use_user_preferences
                   is True, the function will use the global user_prefs.
    
    Returns:
        str: A string containing a combination of artistic styles, joined with " + "
    """
    # Import here to avoid circular imports
    from .core import use_user_preferences

    # If user_prefs is not provided and we should use preferences, get them from global
    if user_prefs is None and use_user_preferences:
        # Import here to avoid circular imports
        try:
            from ..settings_modules import get_preferences
            user_prefs = get_preferences()
        except ImportError:
            # Fallback if settings_modules is not available
            pass
    
    # Define default style categories
    default_style_categories = {
        "traditional_art": ["art_deco", "art_nouveau", "charcoal", "expressionism", 
                           "gothic", "impressionism", "oil_painting", "pastel", 
                           "pencil_sketch", "realism", "sketch", "watercolor", "woodcut"],
        "digital_art": ["abstract", "cinematic", "cyberpunk", "digital_art", "double_exposure", 
                       "fantasy", "futurism", "glitch_art", "hyperrealism", "isometric", 
                       "landscape", "low_poly", "minimalist", "retrowave", "sci_fi",
                       "stained_glass", "steampunk", "surrealism", "vaporwave"],
        "illustration": ["anime", "cartoon", "comic_book", "divisionism", "graffiti", 
                        "ink_drawing", "line_art", "manga", "paper_cut", "pixel_art", 
                        "pointillism", "pop_art", "ukiyo_e"]
    }
    
    # Try to import STYLE_CATEGORIES from config
    try:
        from ..config import STYLE_CATEGORIES
        if STYLE_CATEGORIES:
            default_style_categories = STYLE_CATEGORIES
    except (ImportError, AttributeError):
        # Use default_style_categories if STYLE_CATEGORIES is not available
        pass
    
    # Check if user has custom style categories in preferences
    custom_style_categories = {}
    if user_prefs and use_user_preferences:
        settings = getattr(user_prefs, 'imagen_settings', {}) or {}
        style_settings = settings.get("style_settings", {})
        custom_style_categories = style_settings.get("style_categories", {})
    
    # Use custom categories if available, otherwise use the default ones
    categories_to_use = custom_style_categories if custom_style_categories else default_style_categories
    
    # Select a random category
    category = random.choice(list(categories_to_use.keys()))
    # Select 2-3 compatible styles from the same category
    num_styles = random.randint(2, 3)
    available_styles = categories_to_use[category]
    if len(available_styles) < num_styles:
        num_styles = len(available_styles)
    selected_styles = random.sample(available_styles, num_styles)
    return " + ".join(selected_styles)
