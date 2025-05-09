# AI Generation Core: Imagen 3 & Gemini API Integration

AI Wallgen harnesses the power of Google's advanced AI models to generate unique and stunning wallpapers. This document details how the application integrates with Google's Imagen 3 capabilities, primarily through the Gemini API.

## Overview

The core image generation process involves:
1.  **User Input & Settings:** Gathering the user's prompt, style preferences, and various generation settings (aspect ratio, number of images, seed, etc.).
2.  **API Interaction:** Sending a well-crafted prompt and parameters to Google's AI models.
3.  **Image Reception & Processing:** Receiving the generated image data and saving it locally.

Key Modules Involved:
-   `wall_gen.gemini_config`: Manages API key configuration and global initialization for the Google Generative AI client.
-   `wall_gen.image_service`: Handles the actual API calls for image generation, including fallback mechanisms and SDK selection.
-   `wall_gen.prompt_service` (and `wall_gen.prompt_modules`): Constructs the detailed prompts sent to the API. (Covered in more detail in [Advanced Prompt Engineering](./feature_prompt_engineering.md)).

## API Key Configuration

To use AI Wallgen's generation features, you must have a Google Gemini API key.

-   **Environment Variable:** The application primarily looks for the API key in an environment variable named `GEMINI_API_KEY`. This is the recommended way to provide your key.
    ```bash
    export GEMINI_API_KEY="YOUR_API_KEY_HERE" 
    # On Windows, use: set GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```
-   **Initialization:** The `wall_gen.gemini_config` module attempts to initialize the Google Generative AI client (`genai.configure(api_key=...)`) as soon as it's imported, using the key from the environment variable.
-   **Verification:** You can refer to the [Installation and CLI Guide](./INSTALLATION_AND_CLI_GUIDE.md) for detailed setup instructions. The application will log errors if the API key is missing or invalid.

## Image Generation Models & SDKs

AI Wallgen is designed to be flexible and attempts to use the best available methods for interacting with Google's image generation capabilities.

### SDK Preference:

1.  **Vertex AI SDK (Preferred):**
    -   If the `vertexai` Python package is installed and a Google Cloud Project ID (`GOOGLE_CLOUD_PROJECT` environment variable) is configured, AI Wallgen will attempt to use the Vertex AI SDK.
    -   This SDK often provides more direct access to Imagen models and features.
    -   The default Imagen model used via Vertex AI is typically `imagen-3.0-generate-002` (defined as `IMAGEN_MODEL_NAME` in `image_service.py`).
2.  **Google Generative AI SDK (Fallback):**
    -   If Vertex AI is not available or configured, the application falls back to the standard `google-generativeai` Python package.
    -   It handles both newer and older versions of this SDK.
    -   The Imagen model targeted via this SDK is also typically `imagen-3.0-generate-002` (defined as `GENAI_IMAGEN_MODEL`).
    -   **Gemini Fallback:** If direct Imagen calls via the GenAI SDK encounter issues, `image_service.py` includes a further fallback mechanism to use a general Gemini model (like `gemini-1.5-flash`, defined as `GEMINI_FALLBACK_MODEL`) via the `generate_content` API, by prepending "Generate an image:" to the prompt.

### Model Selection (for non-Imagen tasks):
The `wall_gen.gemini_config` module also manages a list of available Gemini models (e.g., `gemini-1.5-flash`, `gemini-pro`) for other potential AI tasks within the application (like AI preset/style generation). Users can select their preferred model, which is stored in user preferences.

## The Generation Process (`image_service.py`)

The `wall_gen.image_service.generate_image_from_api` function is central to generating images:

1.  **Retrieves Settings:** It fetches `imagen_settings` (like `number_of_images`, `seed`) and `aspect_ratio` from the user's preferences.
2.  **Validates Parameters:** Ensures `number_of_images` (1-4) and `aspect_ratio` (e.g., "16:9", "1:1") are valid.
3.  **Selects SDK:** Chooses between Vertex AI and Google GenAI SDKs based on availability and configuration.
4.  **API Call:**
    -   For Vertex AI: Uses `ImageGenerationModel.from_pretrained(IMAGEN_MODEL_NAME).generate_images(...)`.
    -   For Google GenAI SDK: Uses `client.models.generate_images(...)` (new SDK) or `GenerativeModel(GENAI_IMAGEN_MODEL).generate_images(...)` (older SDK), with a fallback to `generate_content` if needed.
5.  **Saves Images:** Generated images are received (often as image bytes) and saved to temporary `.png` files using `wall_gen.file_utils.create_temp_file`. The paths to these temporary files are then returned.

## Key Configuration Points:

-   **`GEMINI_API_KEY` (Environment Variable):** Essential for authentication.
-   **`GOOGLE_CLOUD_PROJECT` (Environment Variable):** Required if you intend to use the Vertex AI SDK.
-   **User Preferences (`user_preferences.json`):**
    -   `imagen_settings`: Contains detailed parameters for Imagen, such as `number_of_images`, `seed`.
    -   `aspect_ratio`: Defines the desired aspect ratio for the generated image.
    -   `selected_gemini_model`: For non-Imagen AI tasks, specifies the preferred Gemini model.

By understanding this core integration, users can better troubleshoot issues and appreciate the AI capabilities powering AI Wallgen. For more on crafting effective prompts, see the [Advanced Prompt Engineering](./feature_prompt_engineering.md) guide.
