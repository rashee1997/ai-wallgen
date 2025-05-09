# ai_prest_gen/gemini_config_preset.py
"""
Centralized configuration and initialization for Google Gemini models
specifically for the AI Preset Generator.
"""
import os
import logging
import google.generativeai as genai
from typing import Optional, List

# --- Global State for Preset Gemini Configuration ---
_PRESET_GEMINI_API_KEY = None
_preset_is_initialized = False
_preset_last_error = None

# --- Model Definitions for Preset Generation ---
# Users can select from these models for preset generation.
AVAILABLE_PRESET_MODELS: List[str] = [
    "gemini-1.5-flash",          # Good general purpose, often a default
    "gemini-pro",                # For more complex generation tasks
    "gemini-1.5-pro-latest",     # Latest Pro model
    "gemini-2.5-flash-preview-04-17", # Specific preview model, as used before in preset_generator
    "gemini-2.0-flash",          # Another flash variant
]
DEFAULT_PRESET_MODEL: str = "gemini-1.5-flash" # Default if no selection or invalid

# Preference key for storing the selected model in UserPreferences
PRESET_MODEL_PREF_KEY = "selected_preset_gemini_model" # Ensure this key is unique if UserPreferences is shared

# --- API Key Management ---
def get_preset_api_key() -> Optional[str]:
    """
    Retrieves the Gemini API key, prioritizing environment variable.
    This key is used for preset generation context.
    """
    global _PRESET_GEMINI_API_KEY
    if _PRESET_GEMINI_API_KEY:
        return _PRESET_GEMINI_API_KEY
    
    env_api_key = os.environ.get("GEMINI_API_KEY")
    if env_api_key:
        _PRESET_GEMINI_API_KEY = env_api_key
        logging.info("Preset Gemini API Key loaded from GEMINI_API_KEY environment variable.")
        return _PRESET_GEMINI_API_KEY
    
    logging.warning("GEMINI_API_KEY environment variable not set for preset generator.")
    _preset_last_error = "GEMINI_API_KEY environment variable not set."
    return None

# --- Initialization ---
def initialize_preset_gemini(api_key_override: Optional[str] = None) -> bool:
    """
    Initializes the Google Generative AI client for preset generation.
    Uses the API key from environment variable, or an override.
    Returns True if initialization was successful or already initialized, False otherwise.
    """
    global _preset_is_initialized, _preset_last_error, _PRESET_GEMINI_API_KEY

    # If this module previously initialized successfully and no override is given, trust our state.
    # This avoids re-checking genai's global state if our module already did its job.
    if _preset_is_initialized and not api_key_override:
        return True

    current_api_key = api_key_override or get_preset_api_key()

    if not current_api_key:
        # _preset_last_error is set by get_preset_api_key if key is missing
        # logging.error(_preset_last_error) # Already logged by get_preset_api_key
        _preset_is_initialized = False
        return False

    try:
        # Directly configure/re-configure. Assumes genai.configure is idempotent
        # or safely updates the configuration if called multiple times.
        genai.configure(api_key=current_api_key)
        _PRESET_GEMINI_API_KEY = current_api_key 
        logging.info(f"Google Generative AI client configured/reconfigured for preset generation with key ending: ...{current_api_key[-4:] if current_api_key else 'N/A'}.")
        
        _preset_is_initialized = True # Mark success for this module's context
        _preset_last_error = None
        return True
    except Exception as e:
        _preset_last_error = f"Failed to configure Gemini for preset generation: {e}"
        logging.error(_preset_last_error, exc_info=True)
        _preset_is_initialized = False
        return False

def is_preset_gemini_initialized() -> bool:
    """Checks if Gemini has been successfully configured by this module's initialize_preset_gemini."""
    return _preset_is_initialized

def get_preset_last_error() -> Optional[str]:
    """Returns the last initialization error message for preset generation."""
    return _preset_last_error

# --- Model Selection for Preset Generation ---
def get_selected_preset_model(user_prefs) -> str:
    """
    Gets the currently selected Gemini model for preset generation from user preferences.
    Falls back to DEFAULT_PRESET_MODEL if not set or invalid.
    """
    if not user_prefs:
        logging.warning("UserPreferences not provided to get_selected_preset_model. Using default: %s", DEFAULT_PRESET_MODEL)
        return DEFAULT_PRESET_MODEL

    selected_model = getattr(user_prefs, PRESET_MODEL_PREF_KEY, DEFAULT_PRESET_MODEL)
    
    if selected_model not in AVAILABLE_PRESET_MODELS:
        logging.warning(
            f"Selected preset Gemini model '{selected_model}' is not in available list {AVAILABLE_PRESET_MODELS}. "
            f"Falling back to default: {DEFAULT_PRESET_MODEL}."
        )
        return DEFAULT_PRESET_MODEL
    
    logging.debug(f"Using selected preset Gemini model: {selected_model}")
    return selected_model

def set_selected_preset_model(model_name: str, user_prefs) -> bool:
    """
    Sets the user's preferred Gemini model for preset generation in their preferences.
    """
    if not user_prefs:
        logging.error("UserPreferences not provided to set_selected_preset_model.")
        return False

    if model_name in AVAILABLE_PRESET_MODELS:
        try:
            setattr(user_prefs, PRESET_MODEL_PREF_KEY, model_name)
            if hasattr(user_prefs, 'save_preferences') and callable(user_prefs.save_preferences):
                user_prefs.save_preferences()
                logging.info(f"User's preferred preset Gemini model set to: {model_name} and saved.")
            else:
                # If no save_preferences method, the change is in-memory for the session.
                logging.info(f"User's preferred preset Gemini model set to: {model_name} (in-memory).")
            return True
        except Exception as e:
            logging.error(f"Failed to save selected preset Gemini model '{model_name}' to preferences: {e}", exc_info=True)
            return False
    else:
        logging.warning(f"Attempted to set invalid preset Gemini model: {model_name}. Not in {AVAILABLE_PRESET_MODELS}")
        return False

# Attempt to initialize when module is loaded, if key is available.
# This is a soft initialization; the main script can re-initialize if needed.
# It won't reconfigure if genai is already configured by another module (e.g. wall_gen.gemini_config)
# unless the key is different or forced by an override.
if not is_preset_gemini_initialized():
    initialize_preset_gemini()
