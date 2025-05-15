"""
AI-based style categorization using the Google Gemini model.
"""
import logging
from typing import Optional, Dict, Any, List

# Attempt to import necessary modules
try:
    # Import only the necessary config and catalog modules
    from . import gemini_config_preset # Use the preset-specific config
    from . import style_category_catalog # Import the catalog to get category list
    # We will access the model and types via gemini_config_preset.get_preset_gemini_client()
    GEMINI_AVAILABLE = True
except ImportError as e:
    logging.error(f"AICategorizer: Failed to import necessary modules: {e}. AI categorization will not be available.")
    GEMINI_AVAILABLE = False

class AICategorizer:
    """
    Categorizes a style name using the Google Gemini model.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if not GEMINI_AVAILABLE:
            self.logger.critical("AICategorizer initialized but necessary modules are not available.")
        # Only attempt to load categories if Gemini is available, to avoid errors if catalog also fails
        self.available_categories: List[str] = []
        if GEMINI_AVAILABLE:
            try:
                self.available_categories = style_category_catalog.get_all_defined_categories()
                if not self.available_categories:
                    self.logger.warning("No categories loaded from style_category_catalog. AI categorization may be ineffective.")
            except Exception as e:
                 self.logger.error(f"AICategorizer: Failed to load categories from style_category_catalog: {e}. AI categorization will be ineffective.", exc_info=True)
                 self.available_categories = [] # Ensure it's an empty list on failure


    def categorize_style_with_gemini(self, style_name: str, user_prefs: Optional[Any] = None) -> Optional[str]:
        """
        Uses the Gemini model to categorize a style name.

        Args:
            style_name: The style name string to categorize.
            user_prefs: User preferences object to get the selected Gemini model.

        Returns:
            The determined style category string, or None if categorization fails
            or Gemini is not available/initialized.
        """
        if not GEMINI_AVAILABLE:
            self.logger.error("Necessary modules not available. Cannot perform AI categorization.")
            return None

        if not gemini_config_preset.is_preset_gemini_initialized():
            self.logger.error("Preset Gemini client is not initialized. Cannot perform AI categorization.")
            self.logger.error(f"Last Preset Gemini error: {gemini_config_preset.get_preset_last_error()}")
            return None
            
        if not self.available_categories:
             self.logger.warning("No categories available for AI categorization.")
             return None

        client = gemini_config_preset.get_preset_gemini_client()
        if client is None:
             self.logger.error("Preset Gemini client is None after initialization check. Cannot perform AI categorization.")
             return None

        selected_model_name = gemini_config_preset.get_selected_preset_model(user_prefs)
        if not selected_model_name:
             self.logger.error("No valid Preset Gemini model selected. Cannot perform AI categorization.")
             return None

        try:
            # Access the models object and generate content via the client
            models = client.models
            
            # Construct the prompt
            categories_list_str = ", ".join(self.available_categories)
            prompt = (
                f"Categorize the following art style name into one of the following categories:\n"
                f"{categories_list_str}\n\n"
                f"Style Name: \"{style_name}\"\n\n"
                f"Respond with ONLY the category name. If none of the categories match well, respond with \"unknown\"."
            )

            self.logger.debug(f"Sending prompt to Preset Gemini model '{selected_model_name}':\n{prompt}")

            # Call the Gemini API
            # Use a reasonable timeout and potentially adjust generation config and safety settings
            config = {
                "temperature": 0.1, # Keep temperature low for deterministic categorization
                "top_p": 1,
                "top_k": 1,
                "safety_settings": [
                    gemini_config_preset.types.SafetySetting(
                        category=gemini_config_preset.types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                        threshold=gemini_config_preset.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
                    ),
                    gemini_config_preset.types.SafetySetting(
                        category=gemini_config_preset.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                        threshold=gemini_config_preset.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
                    ),
                    gemini_config_preset.types.SafetySetting(
                        category=gemini_config_preset.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                        threshold=gemini_config_preset.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
                    ),
                    gemini_config_preset.types.SafetySetting(
                        category=gemini_config_preset.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                        threshold=gemini_config_preset.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
                    ),
                ]
            }


            response = models.generate_content(
                model=selected_model_name, # Specify the model name here
                contents=prompt,
                config=config,
            )

            # Parse the response - assuming the response object has a 'text' attribute
            if response and hasattr(response, 'text'):
                predicted_category = response.text.strip()
                self.logger.debug(f"Gemini response text: '{predicted_category}'")

                # Validate the predicted category
                if predicted_category in self.available_categories:
                    self.logger.info(f"AI categorized style '{style_name}' as '{predicted_category}'.")
                    return predicted_category
                elif predicted_category.lower() == "unknown":
                     self.logger.info(f"AI categorized style '{style_name}' as 'unknown'.")
                     return "unknown"
                else:
                    self.logger.warning(f"Gemini returned unexpected category '{predicted_category}' for style '{style_name}'. Falling back to None.")
                    return None
            else:
                self.logger.warning(f"Gemini response was empty or missing text attribute for style '{style_name}'. Falling back to None.")
                return None

        except Exception as e:
            self.logger.error(f"Error during Gemini categorization for style '{style_name}': {e}", exc_info=True)
            return None
