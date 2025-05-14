#!/usr/bin/env python3
"""Test module for prompt enhancers.

This module contains test cases for the prompt enhancement functionality,
including both logo and general prompt enhancement.
"""

import unittest
from typing import Any, Dict, Optional

from .base import BasePromptEnhancer, PromptEnhancementError, ValidationError
from .logo import LogoPromptEnhancer
from .general import GeneralPromptEnhancer
from . import enhance_prompt, generate_logo

class MockPrefs:
    """Mock user preferences for testing."""
    def __init__(self, settings: Optional[Dict[str, Any]] = None):
        self.imagen_settings = settings or {
            'quality_settings': {'resolution': '3840x2160'},
            'negative_prompt': 'test negative prompt'
        }
        self.aspect_ratio = '16:9'

class TestPromptEnhancers(unittest.TestCase):
    """Test cases for prompt enhancers."""

    def setUp(self):
        """Set up test cases."""
        self.mock_prefs = MockPrefs()
        self.test_prompt = "A beautiful sunset"
        self.test_logo = "TestBrand"

    def test_validation(self):
        """Test input validation."""
        enhancer = GeneralPromptEnhancer(self.mock_prefs)
        
        with self.assertRaises(ValidationError):
            enhancer._validate_input("")
        
        with self.assertRaises(ValidationError):
            enhancer._validate_input(None)
        
        # Valid input should not raise
        enhancer._validate_input(self.test_prompt)

    def test_logo_enhancer(self):
        """Test logo prompt enhancement."""
        enhancer = LogoPromptEnhancer(self.mock_prefs)
        
        # Test basic logo enhancement
        result = enhancer.enhance_prompt(self.test_logo)
        self.assertIsInstance(result, str)
        self.assertIn(self.test_logo, result)
        self.assertIn("resolution", result.lower())
        self.assertIn("aspect ratio", result.lower())
        
        # Test with taglines
        result = enhancer.enhance_prompt(self.test_logo, tag_lines="Innovation First")
        self.assertIn("Innovation First", result)

    def test_general_enhancer(self):
        """Test general prompt enhancement."""
        enhancer = GeneralPromptEnhancer(self.mock_prefs)
        
        # Test basic enhancement
        result = enhancer.enhance_prompt(self.test_prompt)
        self.assertIsInstance(result, str)
        self.assertIn(self.test_prompt, result)
        self.assertIn("3840x2160", result)
        self.assertIn("16:9", result)
        
        # Test art medium detection
        result = enhancer.enhance_prompt("A watercolor painting of mountains")
        self.assertIn("watercolor", result.lower())
        self.assertNotIn("3d render", result.lower())

    def test_enhance_prompt_interface(self):
        """Test the main enhance_prompt interface."""
        # Test general prompt
        result = enhance_prompt(self.test_prompt, user_prefs=self.mock_prefs)
        self.assertIsInstance(result, str)
        self.assertIn(self.test_prompt, result)
        
        # Test logo prompt
        result = enhance_prompt(self.test_logo, is_logo=True, user_prefs=self.mock_prefs)
        self.assertIsInstance(result, str)
        self.assertIn(self.test_logo, result)

    def test_generate_logo_interface(self):
        """Test the generate_logo interface."""
        result = generate_logo(
            logo_text=self.test_logo,
            tag_lines="Innovation First",
            logo_style="minimalist",
            user_prefs=self.mock_prefs
        )
        self.assertIsInstance(result, str)
        self.assertIn(self.test_logo, result)
        self.assertIn("Innovation First", result)

    def test_error_handling(self):
        """Test error handling."""
        # Test with invalid input
        with self.assertRaises(PromptEnhancementError):
            enhance_prompt("")
        
        # Test with invalid enhancer type
        with self.assertRaises(ValueError):
            from . import create_enhancer
            create_enhancer("invalid_type")

if __name__ == '__main__':
    unittest.main()
