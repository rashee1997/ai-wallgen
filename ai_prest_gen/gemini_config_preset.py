# ai_prest_gen/gemini_config_preset.py
"""
Manages Google Gemini API configuration and model selection specifically for the
AI Preset Generator (`ai_prest_gen`) module.

This module handles:
- API key retrieval (prioritizing environment variables).
- Initialization of the `google.generativeai` client for preset generation tasks.
- Tracking initialization status and errors.
- Defining available Gemini models suitable for preset generation.
- Getting and setting the user's preferred Gemini model for presets via a
  `UserPreferences` object.

It maintains its own initialization state (`_preset_is_initialized`) separate
from any global Gemini configuration that might be used by other parts of the
larger `wall_gen` application, ensuring that preset generation has a dedicated
and correctly configured API client.
"""
import os
import logging
import google.generativeai as genai
from typing import Optional, List, Any

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
    Retrieves the Gemini API key for preset generation.

    It first checks if a key has already been loaded into the module's global
    `_PRESET_GEMINI_API_KEY`. If not, it attempts to load it from the
    `GEMINI_API_KEY` environment variable.

    Returns:
        Optional[str]: The Gemini API key if found, otherwise None.
                       Sets `_preset_last_error` if the key is not found.
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
    Initializes or re-initializes the Google Generative AI client (`genai`)
    for the specific context of preset generation.

    It uses an API key provided by `api_key_override` or falls back to
    `get_preset_api_key()` (which checks environment variables).
    This function updates the module's global state regarding initialization
    status (`_preset_is_initialized`) and any errors (`_preset_last_error`).

    Args:
        api_key_override (Optional[str]): An API key to use, overriding any
                                          environment variable or cached key.

    Returns:
        bool: True if `genai.configure()` was successful or if the module
              considers itself already initialized with a valid key.
              False if no API key is found or if `genai.configure()` fails.
    """
    global _preset_is_initialized, _preset_last_error, _PRESET_GEMINI_API_KEY

    # If already initialized by this module and no new key is forced, assume good.
    if _preset_is_initialized and not api_key_override and _PRESET_GEMINI_API_KEY:
        return True

    current_api_key = api_key_override or get_preset_api_key()

    if not current_api_key:
        # _preset_last_error is typically set by get_preset_api_key if key is missing.
        # If it's somehow not set, provide a generic message.
        if not _preset_last_error:
            _preset_last_error = "Gemini API key not available for preset generation."
        logging.error(_preset_last_error)
        _preset_is_initialized = False
        return False

    try:
        # Configure the genai client. This might affect genai's global state.
        genai.configure(api_key=current_api_key)
        _PRESET_GEMINI_API_KEY = current_api_key  # Cache the key used for this module
        logging.info(f"Google Generative AI client configured/reconfigured for preset generation with key ending: ...{current_api_key[-4:]}.")
        
        _preset_is_initialized = True  # Mark success for this module's context
        _preset_last_error = None
        return True
    except Exception as e:
        _preset_last_error = f"Failed to configure Gemini for preset generation: {e}"
        logging.error(_preset_last_error, exc_info=True)
        _preset_is_initialized = False
        return False

def is_preset_gemini_initialized() -> bool:
    """
    Checks if the Gemini client has been successfully configured by this module
    for preset generation.

    Returns:
        bool: True if initialized, False otherwise.
    """
    return _preset_is_initialized

def get_preset_last_error() -> Optional[str]:
    """
    Returns the last error message recorded during preset-specific Gemini initialization.

    Returns:
        Optional[str]: The last error message, or None if no error occurred.
    """
    return _preset_last_error

# --- Model Selection for Preset Generation ---
def get_selected_preset_model(user_prefs: Any) -> str:
    """
    Retrieves the user's preferred Gemini model for preset generation from their preferences.

    If no preference is set, or if the stored preference is not a valid/available
    model, it falls back to `DEFAULT_PRESET_MODEL`.

    Args:
        user_prefs (Any): The user preferences object (expected to have attributes
                          that can be get/set, e.g., an instance of a class).

    Returns:
        str: The name of the selected Gemini model.
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
    Sets the user's preferred Gemini model for preset generation in their preferences
    and attempts to save the preferences.

    Args:
        model_name (str): The name of the Gemini model to set as preferred.
                          Must be one of the `AVAILABLE_PRESET_MODELS`.
        user_prefs (Any): The user preferences object, which should have a
                          `save_preferences` method if persistence is desired.

    Returns:
        bool: True if the model name is valid and was set (and saved, if applicable),
              False otherwise.
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
