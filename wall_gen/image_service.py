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

# First try to import the Vertex AI SDK which has better Imagen support
try:
    import vertexai
    from vertexai.preview.vision_models import ImageGenerationModel
    VERTEX_AI_AVAILABLE = True
except ImportError:
    VERTEX_AI_AVAILABLE = False
    logging.warning("Vertex AI SDK not found. Falling back to Google GenAI SDK.")

# Then try to import the Google GenAI SDK as fallback
try:
    # Try importing with the newer unified Google GenAI SDK
    from google import genai
    from google.genai import types # Import types for config object
    GENAI_SDK_AVAILABLE = True
    NEW_GENAI_SDK = True
except ImportError:
    try:
        # Fall back to legacy Google GenerativeAI package
        import google.generativeai as genai
        # Attempt to import types from legacy location if needed (may not exist)
        try:
            from google.generativeai import types
        except ImportError:
            types = None # Indicate types might not be available
        GENAI_SDK_AVAILABLE = True
        NEW_GENAI_SDK = False
    except ImportError:
        GENAI_SDK_AVAILABLE = False
        NEW_GENAI_SDK = False
        logging.error("Neither Vertex AI nor Google GenAI SDK is available. Install at least one of them.")

from wall_gen.file_utils import create_temp_file  # To create temporary files for images

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", None)  # For Vertex AI

# Default models for different SDKs
IMAGEN_MODEL_NAME = "imagen-3.0-generate-002"  # For Vertex AI
IMAGEN_FAST_MODEL_NAME = "imagen-3.0-fast-generate-001"  # Faster Imagen model for Vertex AI
GENAI_IMAGEN_MODEL = "imagen-3.0-generate-002"  # For GenAI SDK
GEMINI_FALLBACK_MODEL = "gemini-1.5-flash"  # Fallback model for GenAI SDK

def generate_image_from_api(prompt_text_with_negative, user_prefs):
    """
    Generates an image using the Google Imagen API and saves it to temporary file(s).
    Will try to use Vertex AI first, then fall back to Google GenAI SDK if available.

    Args:
        prompt_text_with_negative (str): The full prompt string, including any "Avoid:" clauses.
        user_prefs (UserPreferences): User preferences object containing imagen_settings and aspect_ratio.

    Returns:
        list: A list of paths to the temporary image files generated, or an empty list on failure.
    """
    if not GEMINI_API_KEY and not PROJECT_ID:
        logging.error("Image generation failed: Neither GEMINI_API_KEY nor PROJECT_ID is configured.")
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

        # Try Vertex AI first (preferred method)
        if VERTEX_AI_AVAILABLE and PROJECT_ID:
            return generate_image_with_vertex_ai(
                prompt_text_with_negative, 
                num_images, 
                aspect_ratio, 
                seed
            )
        
        # Fall back to Google GenAI SDK if Vertex AI is not available
        elif GENAI_SDK_AVAILABLE and GEMINI_API_KEY:
            return generate_image_with_genai_sdk(
                prompt_text_with_negative, 
                num_images, 
                aspect_ratio, 
                seed
            )
        
        # No supported SDKs available
        else:
            logging.error("Image generation failed: No supported image generation SDKs available.")
            logging.error("Please install either 'vertexai' or 'google-generativeai' package.")
            return []

    except Exception as e:
        error_msg = str(e)
        logging.error(f"Unexpected error during image generation: {error_msg}")
        
        if "billed users" in error_msg.lower() or "billing" in error_msg.lower():
            logging.error("Image generation likely requires a Google Cloud billing account.")
        elif "permission" in error_msg.lower() or "access" in error_msg.lower():
            logging.error("You may not have permission to use the Imagen API. This API may require whitelisting.")
            
        return []

def generate_image_with_vertex_ai(prompt, num_images=1, aspect_ratio="1:1", seed=None):
    """
    Generate images using Vertex AI Vision models (recommended method).
    
    Args:
        prompt: Text prompt for image generation
        num_images: Number of images to generate (1-4)
        aspect_ratio: Aspect ratio of the generated images
        seed: Optional random seed
    
    Returns:
        list: Paths to generated temporary image files
    """
    logging.info(f"Using Vertex AI to generate images with model: {IMAGEN_MODEL_NAME}")
    temp_image_paths = []
    
    try:
        # Initialize Vertex AI
        vertexai.init(project=PROJECT_ID, location="us-central1")
        
        # Load the image generation model
        model = ImageGenerationModel.from_pretrained(IMAGEN_MODEL_NAME)
        
        # Set up generation parameters
        generation_kwargs = {
            "prompt": prompt,
            "number_of_images": num_images,
            "aspect_ratio": aspect_ratio,
        }
        
        # Add optional seed parameter if provided
        if seed is not None:
            generation_kwargs["seed"] = seed
            # Note: You can't use seed and watermark together, so disable watermark
            generation_kwargs["add_watermark"] = False
        
        # Generate the images
        images = model.generate_images(**generation_kwargs)
        
        # Process and save the generated images
        for i, img in enumerate(images):
            # In Vertex AI SDK, images can be directly saved
            temp_file_path = create_temp_file(suffix=".png")
            
            if temp_file_path:
                # Save image to temporary file
                img.save(location=temp_file_path, include_generation_parameters=False)
                temp_image_paths.append(temp_file_path)
                logging.info(f"Image {i+1} saved to: {temp_file_path}")
            else:
                logging.error(f"Failed to create temporary file for image {i+1}")
        
    except Exception as e:
        logging.error(f"Error using Vertex AI for image generation: {e}")
        # Don't raise, let caller decide what to do
    
    return temp_image_paths

def generate_image_with_genai_sdk(prompt, num_images=1, aspect_ratio="1:1", seed=None):
    """
    Generate images using Google GenAI SDK (fallback method).
    
    Args:
        prompt: Text prompt for image generation
        num_images: Number of images to generate (1-4)
        aspect_ratio: Aspect ratio of the generated images
        seed: Optional random seed
    
    Returns:
        list: Paths to generated temporary image files
    """
    logging.info(f"Using Google GenAI SDK to generate images")
    temp_image_paths = []
    
    try:
        # Initialize the GenAI client based on SDK version
        client = None
        if NEW_GENAI_SDK:
            # New SDK uses Client object
            client = genai.Client(api_key=GEMINI_API_KEY)
        else:
            # Old SDK uses configure method
            genai.configure(api_key=GEMINI_API_KEY)
        
        # Try to generate images using the direct Imagen API first
        try:
            if NEW_GENAI_SDK:
                # Configure generation parameters using GenerateImagesConfig
                gen_config_params = {
                    "number_of_images": num_images,
                    "aspect_ratio": aspect_ratio,
                }
                
                # Add seed if provided
                if seed is not None:
                    gen_config_params["seed"] = seed
                    # Disable watermark when using seed
                    gen_config_params["add_watermark"] = False
                
                # Ensure google.genai.types was imported successfully
                if 'types' not in globals() or types is None:
                     raise ImportError("google.genai.types module not available for GenerateImagesConfig.")

                config = types.GenerateImagesConfig(**gen_config_params)
                
                # Using the newer Client-based SDK with config object
                response = client.models.generate_images(
                    model=GENAI_IMAGEN_MODEL,
                    prompt=prompt,  # Prompt is separate from config
                    config=config    # Pass the config object
                )
                
                # Process the response
                if hasattr(response, "generated_images"):
                    for i, img in enumerate(response.generated_images):
                        try:
                            # Extract image data from response
                            # The response structure provides the bytes directly
                            if hasattr(img, "image") and img.image and hasattr(img.image, "image_bytes"):
                                image_bytes = img.image.image_bytes # Get bytes directly

                                # Save the image bytes to a temporary file
                                temp_file_path = create_temp_file(suffix=".png") # Assuming PNG, might need check mime_type if available
                                if temp_file_path:
                                    with open(temp_file_path, "wb") as f:
                                        f.write(image_bytes) # Write the direct bytes
                                    temp_image_paths.append(temp_file_path)
                                    logging.info(f"Image {i+1} saved to: {temp_file_path}")
                                else:
                                    logging.error(f"Failed to create temporary file for image {i+1}")
                            else:
                                logging.warning(f"Could not extract image_bytes from response part {i+1}")
                        except Exception as img_error:
                            logging.error(f"Error processing image {i+1}: {img_error}")
                
            else:
                # --- OLD SDK Path ---
                # Attempting to use generate_images with the older SDK.
                # This might fail if the method doesn't exist or parameters differ significantly.
                model = genai.GenerativeModel(GENAI_IMAGEN_MODEL)

                # Older SDK might not support GenerateImagesConfig or specific params.
                # Sticking to the simpler structure that failed previously,
                # anticipating the fallback to generate_content.
                generation_params = {
                    "prompt": prompt,
                    # "aspect_ratio": aspect_ratio, # Likely unsupported here
                    # "number_of_images": num_images # Likely unsupported here
                }
                if seed is not None:
                    generation_params["seed"] = seed

                # This call is expected to fail for older SDKs based on previous errors
                response = model.generate_images(**generation_params)

                # Process the response (likely unreachable for old SDK)
                for i, img in enumerate(response):
                    try:
                        # Extract image data from response (e.g., base64)
                        if hasattr(img, "base64"):
                            image_bytes = base64.b64decode(img.base64)
                        elif hasattr(img, "_image_bytes"):
                             image_bytes = img._image_bytes
                        # ... (other potential attributes) ...
                        else:
                            logging.warning(f"Could not extract image data from OLD SDK response {i+1}")
                            continue

                        # Save the image to a temporary file
                        temp_file_path = create_temp_file(suffix=".png")
                        if temp_file_path:
                            with open(temp_file_path, "wb") as f:
                                f.write(image_bytes)
                            temp_image_paths.append(temp_file_path)
                            logging.info(f"Image {i+1} saved to: {temp_file_path} (OLD SDK path)")
                        else:
                            logging.error(f"Failed to create temporary file for image {i+1} (OLD SDK path)")
                    except Exception as img_error:
                        logging.error(f"Error processing image {i+1} (OLD SDK path): {img_error}")

        except Exception as direct_error:
            logging.warning(f"Direct Imagen API call failed: {direct_error}")
            logging.info("Falling back to content generation API")
            
            # Fallback using generate_content API
            fallback_model_name = GEMINI_FALLBACK_MODEL
            generation_prompt = f"Generate an image: {prompt}"

            try:
                if NEW_GENAI_SDK:
                    # Using new SDK client
                    response = client.models.generate_content(
                        model=fallback_model_name,
                        contents=generation_prompt
                        # Removed response_modalities
                    )
                else:
                    # Using old SDK GenerativeModel
                    model = genai.GenerativeModel(fallback_model_name)
                    response = model.generate_content(
                        generation_prompt,
                        stream=False
                    )

                # Extract images from generate_content response (common processing)
                if hasattr(response, "candidates") and response.candidates:
                    for candidate in response.candidates:
                        if hasattr(candidate, "content") and candidate.content:
                            if hasattr(candidate.content, "parts"):
                                for i, part in enumerate(candidate.content.parts):
                                    # Check for inline image data
                                    if hasattr(part, "inline_data") and part.inline_data:
                                        image_bytes = getattr(part.inline_data, "data", None)
                                        mime_type = getattr(part.inline_data, "mime_type", "")
                                        if image_bytes and "image" in mime_type:
                                            # Determine suffix based on mime type if possible
                                            suffix = "." + mime_type.split("/")[-1] if "/" in mime_type else ".png"
                                            temp_file_path = create_temp_file(suffix=suffix)
                                            if temp_file_path:
                                                with open(temp_file_path, "wb") as f:
                                                    f.write(image_bytes)
                                                temp_image_paths.append(temp_file_path)
                                                logging.info(f"Image {i+1} saved using fallback content generation to {temp_file_path}")
                                            else:
                                                logging.error(f"Failed to create temp file for fallback image {i+1}")
            except Exception as fallback_error:
                 logging.error(f"Content generation fallback API also failed: {fallback_error}")

    except Exception as e:
        logging.error(f"Error using Google GenAI SDK for image generation: {e}")
        # Don't raise, let caller decide what to do
    
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
