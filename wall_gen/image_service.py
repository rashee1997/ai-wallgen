# wall_gen/image_service.py
"""
Service module for interacting with the image generation API (Google Imagen).
NOTE: This module uses absolute imports assuming it's part of the 'wall_gen' package.
It may not run correctly as a standalone script without sys.path adjustments.
"""
import os
import logging
import base64
from io import BytesIO
from PIL import Image

# Import the Google GenAI SDK
try:
    from google import genai
    from google.genai import types # Import types for config object
    GENAI_SDK_AVAILABLE = True
    logging.info("Successfully imported Google GenAI SDK.")
except ImportError as e:
    GENAI_SDK_AVAILABLE = False
    logging.error(f"Failed to import Google GenAI SDK: {e}")
    logging.error("Please ensure 'google-genai' package is installed.")


from wall_gen.file_utils import create_temp_file  # To create temporary files for images

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Default model for GenAI SDK
GENAI_IMAGEN_MODEL = "imagen-3.0-generate-002"

def generate_image_from_api(prompt_text_with_negative, user_prefs):
    """
    Generates an image using the Google Imagen API (via GenAI SDK) and saves it to temporary file(s).

    Args:
        prompt_text_with_negative (str): The full prompt string, including any "Avoid:" clauses.
        user_prefs (UserPreferences): User preferences object containing imagen_settings and aspect_ratio.

    Returns:
        list: A list of paths to the temporary image files generated, or an empty list on failure.
    """
    # Log API key status
    if GEMINI_API_KEY:
        logging.info("GEMINI_API_KEY is set.")
    else:
        logging.error("GEMINI_API_KEY is not set.")
        logging.error("Image generation failed: GEMINI_API_KEY is not configured.")
        return []

    try:
        # Get settings from user preferences
        imagen_settings = user_prefs.imagen_settings
        aspect_ratio = user_prefs.aspect_ratio

        # Validate aspect ratio
        valid_ratios = ["16:9", "9:16", "4:3", "3:4", "1:1"]
        if aspect_ratio not in valid_ratios:
            logging.warning(f"Invalid aspect ratio: {aspect_ratio}. Using default 1:1 for image generation.")
            aspect_ratio = "1:1"

        # Validate number of images
        num_images = imagen_settings.get("number_of_images", 1)
        if not isinstance(num_images, int) or num_images < 1 or num_images > 4:
            logging.warning(f"Invalid number_of_images: {num_images}. Using default 1.")
            num_images = 1

        # Get seed if available
        seed = imagen_settings.get("seed")
        if seed is not None:
            logging.info(f"Using seed: {seed}")

        # Log generation parameters
        logging.info(f"Prompt (first 100 chars): {prompt_text_with_negative[:100]}...")
        logging.info(f"Number of images: {num_images}, Aspect ratio: {aspect_ratio}")

        # Use Google GenAI SDK if available
        if GENAI_SDK_AVAILABLE and GEMINI_API_KEY:
            return generate_image_with_genai_sdk(
                prompt_text_with_negative,
                num_images,
                aspect_ratio,
                seed
            )

        # SDK not available
        else:
            logging.error("Image generation failed: Google GenAI SDK not available or API key missing.")
            logging.error("Please ensure 'google-genai' package is installed and GEMINI_API_KEY is set.")
            return []

    except Exception as e:
        error_msg = str(e)
        logging.error(f"Unexpected error during image generation: {error_msg}")
        return []

def generate_image_with_genai_sdk(prompt, num_images=1, aspect_ratio="1:1", seed=None):
    """
    Generate images using Google GenAI SDK with an Imagen model.

    Args:
        prompt: Text prompt for image generation
        num_images: Number of images to generate (1-4)
        aspect_ratio: Aspect ratio of the generated images
        seed: Optional random seed

    Returns:
        list: Paths to generated temporary image files
    """
    logging.info(f"Using Google GenAI SDK to generate images with model: {GENAI_IMAGEN_MODEL}")
    temp_image_paths = []

    # Ensure SDK is available before proceeding
    if not GENAI_SDK_AVAILABLE:
        logging.error("Google GenAI SDK is not available, cannot generate image.")
        return []

    try:
        # Initialize the GenAI client
        client = genai.Client(api_key=GEMINI_API_KEY)

        # Configure generation parameters using GenerateImagesConfig
        gen_config_params = {
            "number_of_images": num_images,
            "aspect_ratio": aspect_ratio,
            "output_mime_type": "image/png" # Specify PNG for consistency
        }

        if seed is not None:
            gen_config_params["seed"] = seed
            # Watermark often incompatible with seed, disable if seed is used
            gen_config_params["add_watermark"] = False

        # Create the config object
        config_obj = types.GenerateImagesConfig(**gen_config_params)

        logging.info(f"Attempting image generation with GenAI SDK model: {GENAI_IMAGEN_MODEL}")

        response = client.models.generate_images(
            model=GENAI_IMAGEN_MODEL,
            prompt=prompt,
            config=config_obj
        )

        # Process the response
        if response and hasattr(response, "generated_images"):
            for i, img_data in enumerate(response.generated_images):
                try:
                    # Extract image bytes from the standard structure
                    if hasattr(img_data, "image") and img_data.image and hasattr(img_data.image, "image_bytes"):
                        image_bytes = img_data.image.image_bytes
                    else:
                         logging.error(f"GenAI SDK: Image data for image {i+1} is in unexpected format.")
                         continue # Skip to the next image if data is not found

                    if image_bytes:
                        temp_file_path = create_temp_file(suffix=".png")
                        if temp_file_path:
                            with open(temp_file_path, "wb") as f:
                                f.write(image_bytes)
                            temp_image_paths.append(temp_file_path)
                            logging.info(f"Image {i+1} from GenAI SDK saved to: {temp_file_path}")
                        else:
                            logging.error(f"GenAI SDK: Failed to create temporary file for image {i+1}")
                    else:
                        logging.error(f"GenAI SDK: Image bytes for image {i+1} are empty.")
                except Exception as inner_e:
                    logging.error(f"GenAI SDK: Error processing/saving image {i+1}: {inner_e}")
        elif response:
            logging.error(f"GenAI SDK: Unexpected response structure. No 'generated_images' attribute. Response: {str(response)[:200]}")
        else:
            logging.error("GenAI SDK: No response received from image generation call.")

    except ImportError as ie:
        # This block should ideally not be hit if GENAI_SDK_AVAILABLE is True,
        # but keeping for robustness in case of weird environment issues.
        logging.error(f"Google GenAI SDK configuration error (ImportError): {ie}")
        logging.error("Please ensure the 'google-genai' SDK and its dependencies are correctly installed.")
    except Exception as e:
        error_msg = str(e)
        logging.error(f"Error using Google GenAI SDK for image generation: {error_msg}")
        if "permission" in error_msg.lower() or "allowlist" in error_msg.lower():
             logging.error("The Imagen API via GenAI SDK might require your account to be allowlisted or have specific permissions.")
        elif "api key" in error_msg.lower():
             logging.error("Please check your GEMINI_API_KEY.")
        if "billed user" in error_msg.lower() or "billing" in error_msg.lower():
            logging.error("Ensure your Google Cloud project has billing enabled and is linked if using Vertex AI features through GenAI SDK.")

    return temp_image_paths

if __name__ == '__main__':
    # Test code for debugging
    logging.basicConfig(level=logging.INFO)

    class MockUserPrefs:
        def __init__(self):
            self.imagen_settings = {
                "number_of_images": 1,
                "seed": 12345,
                "safety_filter_level": None,
                "person_generation": None
            }
            self.aspect_ratio = "1:1"

    mock_prefs = MockUserPrefs()
    test_prompt = "A serene landscape with mountains and a lake, digital art. Avoid: text, watermarks"

    logging.info(f"Attempting to generate image with prompt: {test_prompt}")
    generated_files = generate_image_from_api(test_prompt, mock_prefs)

    if generated_files:
        logging.info(f"Successfully generated {len(generated_files)} image(s):")
        for f_path in generated_files:
            logging.info(f"- {f_path}")
    else:
        logging.error("Image generation test failed.")
