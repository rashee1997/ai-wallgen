# wall_gen/gemini_config.py
"""
Centralized configuration and initialization for Google Gemini models.
NOTE: This module uses absolute imports assuming it's part of the 'wall_gen' package.
It may not run correctly as a standalone script without sys.path adjustments.
"""
import os
import logging
from google import genai # Use the new SDK import
from google.genai import types # Import types for consistency
from typing import Optional

# --- Global State for Gemini Configuration ---
_GEMINI_API_KEY = None
_is_initialized = False
_last_error = None

# --- Model Definitions ---
# User can modify these defaults if needed, but selection will be stored in UserPreferences
AVAILABLE_GEMINI_MODELS = [
    "gemini-1.5-flash", # General purpose, good default
    "gemini-pro", # For more complex tasks if flash is not enough (example, user might change to this)
    # User-requested models:
    "gemini-2.5-flash-preview-04-17", # This seems like a specific preview, might be outdated. Keeping user's request.
    "gemini-2.0-flash", # Older flash model
    "gemini-1.5-latest" # This is not a standard model name, usually it's gemini-1.5-pro-latest or gemini-1.5-flash-latest.
                        # Using gemini-1.5-pro-latest as a more robust interpretation.
                        # If user means "the latest available 1.5 model", that's usually Pro.
                        # Forcing a more standard name here for better API compatibility.
                        # If user truly has access to "gemini-1.5-latest" as a distinct model, they can edit this list.
    "gemini-1.5-pro-latest", # Added as a more standard interpretation of "gemini-1.5-latest"
]
# Default model if no selection is found in user_prefs or if selected is invalid
DEFAULT_GEMINI_MODEL = "gemini-1.5-flash" # A generally available and capable model

# --- API Key Management ---
def get_api_key() -> Optional[str]:
    """
    Retrieves the Gemini API key, prioritizing environment variable.
    """
    global _GEMINI_API_KEY
    if _GEMINI_API_KEY:
        return _GEMINI_API_KEY
    
    env_api_key = os.environ.get("GEMINI_API_KEY")
    if env_api_key:
        _GEMINI_API_KEY = env_api_key
        logging.info("Gemini API Key loaded from GEMINI_API_KEY environment variable.")
        return _GEMINI_API_KEY
    
    logging.warning("GEMINI_API_KEY environment variable not set and no key provided.")
    return None

# --- Initialization ---
def initialize_gemini_globally(api_key_override: Optional[str] = None) -> bool:
    """
    Initializes the Google Generative AI client globally.
    Uses the API key from environment variable, or an override.
    Returns True if initialization was successful or already initialized, False otherwise.
    """
    global _is_initialized, _last_error, _GEMINI_API_KEY

    if _is_initialized and not api_key_override: # Already initialized with existing key
        return True
    
    current_api_key = api_key_override or get_api_key()

    if not current_api_key:
        _last_error = "Gemini API Key is not available. Set GEMINI_API_KEY environment variable or provide it."
        logging.error(_last_error)
        _is_initialized = False
        return False

    global _gemini_client # Add global declaration for the client instance
    try:
        _gemini_client = genai.Client(api_key=current_api_key) # Create a client instance
        _GEMINI_API_KEY = current_api_key # Store the key used for initialization
        _is_initialized = True
        _last_error = None
        logging.info(f"Google Generative AI client initialized successfully with {'override' if api_key_override else 'configured'} key.")
        return True
    except Exception as e:
        _last_error = f"Failed to initialize Google Generative AI client: {e}"
        logging.error(_last_error, exc_info=True)
        _is_initialized = False
        _gemini_client = None # Ensure client is None on failure
        return False

# Add a global variable to store the client instance
_gemini_client = None

def is_initialized() -> bool:
    """Checks if the Gemini client is initialized."""
    return _is_initialized and _gemini_client is not None # Check if the client instance exists

# Add a function to get the client instance
def get_gemini_client() -> Optional[genai.Client]:
    """Returns the initialized Gemini client instance."""
    if is_initialized():
        return _gemini_client
    return None

def get_last_error() -> Optional[str]:
    """Returns the last initialization error message."""
    return _last_error

# --- Model Selection ---
def get_selected_gemini_model(user_prefs) -> str:
    """
    Gets the currently selected non-Imagen Gemini model from user preferences.
    Falls back to DEFAULT_GEMINI_MODEL if not set or invalid.
    """
    if not user_prefs:
        logging.warning("UserPreferences not provided to get_selected_gemini_model. Using default.")
        return DEFAULT_GEMINI_MODEL

    selected_model = getattr(user_prefs, 'selected_gemini_model', DEFAULT_GEMINI_MODEL)
    
    if selected_model not in AVAILABLE_GEMINI_MODELS:
        logging.warning(
            f"Selected Gemini model '{selected_model}' is not in available list. "
            f"Falling back to default: {DEFAULT_GEMINI_MODEL}."
        )
        # Optionally, update user_prefs to the default if an invalid model was stored
        # setattr(user_prefs, 'selected_gemini_model', DEFAULT_GEMINI_MODEL)
        # user_prefs.save_preferences() # If auto-correction is desired
        return DEFAULT_GEMINI_MODEL
    
    logging.debug(f"Using selected Gemini model: {selected_model}")
    return selected_model

def set_selected_gemini_model(model_name: str, user_prefs) -> bool:
    """
    Sets the user's preferred non-Imagen Gemini model in their preferences.
    """
    if not user_prefs:
        logging.error("UserPreferences not provided to set_selected_gemini_model.")
        return False

    if model_name in AVAILABLE_GEMINI_MODELS:
        try:
            user_prefs.selected_gemini_model = model_name
            user_prefs.save_preferences() # Assumes UserPreferences has a save method
            logging.info(f"User's preferred Gemini model set to: {model_name}")
            return True
        except Exception as e:
            logging.error(f"Failed to save selected Gemini model '{model_name}' to preferences: {e}", exc_info=True)
            return False
    else:
        logging.warning(f"Attempted to set invalid Gemini model: {model_name}. Not in {AVAILABLE_GEMINI_MODELS}")
        return False

# --- Auto-initialize on module load ---
# This attempts to configure Gemini as soon as this module is imported,
# using the environment variable if available.
if not _is_initialized:
    initialize_gemini_globally()

# --- Specific Model Accessors (Optional, for clarity if tasks truly need different models later) ---
# For now, all tasks will use the single get_selected_gemini_model.
# If per-task models were needed, functions like these would be used:

# def get_style_generation_model(user_prefs) -> str:
#     # In a multi-model selection scenario, this would fetch a specific preference
#     return get_selected_gemini_model(user_prefs) 

# def get_filename_extraction_model(user_prefs) -> str:
#     return get_selected_gemini_model(user_prefs)

# def get_prompt_service_model(user_prefs) -> str:
#     return get_selected_gemini_model(user_prefs)

# def get_image_service_fallback_model(user_prefs) -> str:
#     return get_selected_gemini_model(user_prefs)
