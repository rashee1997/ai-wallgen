# AI-Powered Style Generation

AI Wallgen features a dedicated module, `ai_style_generator.py`, that leverages Google's Gemini AI to generate unique and descriptive artistic styles. These generated styles can then be used to influence your wallpaper creations.

## Overview

The AI Style Generator allows you to:
1.  Generate **simple style phrases** (e.g., "Vibrant Cyberpunk Neon").
2.  Generate more **detailed styles** consisting of a concise name and a descriptive sentence.
3.  Optionally constrain style generation to a **specific art category** (e.g., "oil_painting", "cyberpunk").
4.  Save these generated styles to your `user_preferences.json` to be used in future wallpaper prompts.
5.  Export styles to files.

Key Components:
-   `ai_style_generator.py`: The main script for this feature.
-   Gemini AI Model: (e.g., `gemini-2.5-flash-preview-04-17` as seen in the script) is used for the creative generation.
-   `wallpaper_settings.UserPreferences`: Used to save preferred styles.

## How It Works

1.  **Initialization:**
    -   The script attempts to initialize the Gemini AI client using the `GEMINI_API_KEY` environment variable. You can also provide the key via a CLI argument if needed.

2.  **Prompting Gemini for Styles (`generate_style_prompt`):**
    -   A specialized prompt is constructed to guide the Gemini model.
    -   If a `category` is specified (e.g., "photographic", "minimalist_geometric"), the prompt instructs Gemini to focus on characteristics of that category.
    -   The prompt also varies based on whether a `style_type` of "simple" (a short phrase) or "detailed" (a name and a one-sentence description) is requested.

3.  **Style Generation (`generate_random_style`):**
    -   This function sends the constructed prompt to the Gemini model.
    -   It includes retry logic in case of temporary API issues.
    -   The AI's textual response is parsed:
        -   For "simple" styles, the direct response is used as the style name.
        -   For "detailed" styles, the script expects the first line to be the style name and the second line to be its description.
    -   The result is typically returned as a dictionary: `{"name": "Style Name", "description": "Style description..."}`.

4.  **Saving Styles (Optional):**
    -   If using the interactive mode or the `--save` CLI flag, the generated style name can be added to the `preferred_styles` list within your `user_preferences.json` file via the `user_prefs.add_style()` method. For more details on `user_preferences.json`, see the [Dynamic Configuration guide](./feature_dynamic_configuration.md).
    -   These saved styles can then be selected or randomly incorporated when generating prompts in the main AI Wallgen application.

5.  **Canonicalization (`canonicalize_style_name` - Internal):**
    -   The script includes a function to map a generated (often free-form) style name to one of a predefined set of "canonical" categories (e.g., "oil_painting", "cyberpunk"). This is mainly for internal organization or display and uses keyword matching and string similarity.

## Using the AI Style Generator (CLI)

The `ai_style_generator.py` script can be run directly from the command line. The `README.md` provides quick usage examples. Here's a summary:

-   **Generate a simple style in a specific category:**
    ```bash
    python ai_style_generator.py --category oil_painting
    ```

-   **Generate a detailed style for a category:**
    ```bash
    python ai_style_generator.py --category sci_fi --detailed
    ```

-   **Generate a random detailed style and save it to preferences:**
    ```bash
    python ai_style_generator.py --detailed --save
    ```
    (This will add the `name` of the generated style to your `user_preferences.json`)

-   **Export a generated style to a file:**
    ```bash
    python ai_style_generator.py --detailed --export my_new_style.json
    # or
    python ai_style_generator.py --category "vintage cartoon" --export my_cartoon_style.txt
    ```

-   **Interactive Mode:**
    Running `python ai_style_generator.py` without generation-specific arguments (like `--category` or `--detailed` without `--save` or `--export`) may launch an interactive handler (`handle_style_generation`) that repeatedly generates styles (often in random categories for diversity) and asks if you want to save each one.

## How Generated Styles Influence Prompts

When you save a style name (e.g., "Ethereal Dreamscape Watercolor") to your `preferred_styles` in `user_preferences.json`:
-   The main wallpaper generation process (managed by `wall_gen.prompt_service` and `wall_gen.prompt_modules`) can access these preferred styles.
-   Depending on the prompt generation method chosen (e.g., "AI prompt" or "Random prompt"), these style names can be directly incorporated or used as inspiration when constructing the final detailed prompt that is sent to Imagen 3 for image generation.
-   This allows the artistic styles you discover and save with `ai_style_generator.py` to directly shape the aesthetics of your generated wallpapers.

This feature provides a powerful way to explore and define unique artistic directions for your AI-generated art.
