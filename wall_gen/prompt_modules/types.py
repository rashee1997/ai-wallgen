#!/usr/bin/env python3
"""Types module for prompt generation - Contains type definitions and classes

This module contains type definitions and classes used across prompt generation modules.
"""
from typing import Dict, List, Optional, Any, Union, Tuple, Set


class SimplePrefs:
    """Simple class for minimal user preferences when not using the full user preferences"""
    def __init__(self, aspect_ratio: str = "16:9", imagen_settings: Optional[Dict[str, Any]] = None):
        """Initialize SimplePrefs with basic settings
        
        Args:
            aspect_ratio: Aspect ratio setting (default: "16:9")
            imagen_settings: Dictionary of imagen settings (default: empty dict)
        """
        self.aspect_ratio = aspect_ratio
        self.imagen_settings = imagen_settings or {}
