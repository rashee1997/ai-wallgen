# Advanced Prompt Engineering in AI Wallgen

AI Wallgen employs a sophisticated prompt engineering pipeline to translate user preferences, custom inputs, and random elements into detailed, effective prompts for the Imagen 3 AI. This document explores the key components and techniques involved.

## Overview of the Prompt Pipeline

The generation of the final prompt sent to the image generation API typically involves these stages:

1.  **Input Gathering:** Depending on the chosen mode, this can be:
    *   A user-provided custom prompt string.
    *   A set of randomly selected tags.
    *   An AI-generated base prompt (from Gemini, based on user preferences or random tags).
2.  **Contextual Enhancement (AI-driven):**
    *   User settings (from `user_preferences.json`), including preferred styles, moods, and detailed `imagen_settings` (camera, lighting, color, etc.), are processed.
    *   Custom keys added by the user within `imagen_settings` are dynamically flattened and incorporated (see [Dynamic Configuration](./feature_dynamic_configuration.md)).
    *   This rich context is used to instruct a Gemini model to either enhance a custom prompt or build a new one from tags, aiming for coherence and artistic quality.
3.  **Negative Prompt Construction:**
    *   User-defined negative terms are combined with AI-inferred subject-specific negatives and default technical artifact exclusions.
4.  **Formatting:**
    *   The generated prompt (main content + negative prompt) is standardized to ensure critical parameters like resolution and aspect ratio are correctly appended.

Key Modules Involved:
-   `wall_gen.prompt_service`: Orchestrates the overall prompt generation flow.
-   `wall_gen.prompt_modules.core`: Contains core prompt generation logic, often using Gemini.
-   `wall_gen.prompt_modules.custom_generator`: Specializes in enhancing user-provided custom prompts.
-   `wall_gen.prompt_modules.random_generator`: Generates prompts based on random tags and user settings.
-   `wall_gen.prompt_modules.negative_prompt`: Manages the creation of effective negative prompts.
-   `wall_gen.prompt_modules.tag_utils`: Provides utilities for selecting random tags.
-   `wall_gen.prompt_modules.formatters`: Ensures final prompt standardization.
-   `wall_gen.settings_modules.user_preferences` & `settings_manager`: Provide the user settings that heavily influence prompt generation.

## Prompt Generation Methods

AI Wallgen supports several methods to generate the base for an image prompt:

### 1. Custom Prompts with AI Enhancement (`custom_generator.py`)

-   **Function:** `enhance_custom_prompt(custom_prompt, user_prefs, description)`
-   **Process:**
    -   Takes a user's raw `custom_prompt`.
    -   If `user_prefs` are provided, it extracts a vast amount of detail (camera, lighting, composition, color, style settings, preferred styles/moods, and any dynamically added custom keys within `imagen_settings`).
    -   It then crafts a highly detailed set of instructions for a Gemini AI model. These instructions guide the AI to "breathe life" into the original `custom_prompt`, weaving in all the user's settings "organically" to create a "vivid, immersive scene" that elevates the original idea without losing its core essence. The AI is encouraged to be "bold and poetic."
    -   If `user_prefs` are *not* used, a stricter instruction set is employed, focusing on preserving the original custom prompt (especially any specified art medium) while adding technical parameters.
    -   The Gemini model generates an enhanced prompt, which is then parsed and returned.
-   **Outcome:** A user's basic idea can be transformed into a rich, detailed prompt that reflects their comprehensive settings.

### 2. Random Prompts with AI Enhancement (`random_generator.py`)

-   **Function:** `generate_prompt_random(tags, user_prefs)`
-   **Process:**
    -   **Tag Selection (`tag_utils.select_random_tags`):** Initially, a set of 3-5 related tags is selected. This function prioritizes `user_prefs.preferred_subjects` if available, otherwise, it picks a primary theme (nature, fantasy, etc.) and adds related contextual tags (moods, weather, materials).
    -   These `tags` are then given to `generate_prompt_random`.
    -   Similar to custom prompt enhancement, if `user_prefs` are available, a detailed "CREATIVE VISION QUEST" instruction is sent to Gemini. The AI is tasked to "weave a single, coherent visual tapestry" from these random tags, making them feel intentional and harmonizing them with all user settings.
    -   If `user_prefs` are not used, a simpler instruction asks Gemini to create a prompt incorporating all tags.
-   **Outcome:** Generates creative and often unexpected prompts based on a random seed of ideas, refined by AI and user settings.

### 3. AI-Generated Base Prompts (`prompt_service.py` & `prompt_modules.core.py`)

-   **Function:** `_build_gemini_prompt_from_settings` (in `prompt_service.py`) or `generate_prompt_gemini` (in `prompt_modules.core.py`).
-   **Process:**
    -   This method uses Gemini to generate the *entire* descriptive part of the prompt based on a few high-level inputs like `tags` (which can be derived from `user_prefs.preferred_genres`, moods, styles, or random tags).
    -   It heavily utilizes the `dynamic_technical_context` function (from `prompt_service.py`), which flattens all relevant `user_prefs.imagen_settings` (including custom ones) into natural language phrases.
    -   The instruction to Gemini asks it to create a "vivid, detailed, and coherent single-paragraph description," incorporating the subject tags, preferred style/mood, and all the flattened technical/artistic specifications.
-   **Outcome:** A highly detailed prompt generated almost entirely by AI, deeply informed by all aspects of the user's configuration.

## Dynamic Flattening of Settings

A key aspect of AI Wallgen's prompt engineering is the "dynamic flattening" of settings (see [Dynamic Configuration](./feature_dynamic_configuration.md) for more).
-   Functions like `flatten_settings` and `dynamic_technical_context` (primarily in `prompt_service.py`) process the `user_preferences.json` (especially the `imagen_settings` dictionary).
-   They recursively convert all key-value pairs, including any custom ones added by the user within these structures, into a series of descriptive phrases.
-   This flattened, natural-language context is then fed to the Gemini model when it's tasked with enhancing or generating a prompt. This ensures that even deeply nested or custom user settings can influence the final AI-generated prompt.

## Negative Prompts (`negative_prompt.py`)

Effective negative prompts are crucial for guiding the AI away from undesirable outputs.
-   **Function:** `enhance_negative_prompt(negative_prompt_text, user_prefs)`
-   **Process:**
    1.  **User Input:** Takes user-provided negative terms (comma-separated). Up to 7 unique terms are prioritized.
    2.  **AI-Inferred Subject Negatives (`infer_subject_negatives_gemini`):** For the user's terms, it can optionally use Gemini to infer related subject-specific negatives (e.g., if the prompt is "cat", it might suggest avoiding "dog"). Up to 4 unique, non-redundant inferred terms are added.
    3.  **Default Artifacts:** A standard list of technical artifact terms ("blurry", "low quality", "nsfw", "watermark", "out of frame") is appended if not already covered.
    4.  **Combination & Capping:** All terms are combined (user > inferred > default) and capped at 13 terms.
-   **Outcome:** A robust negative prompt string.

## Final Formatting (`formatters.py`)

-   **Function:** `enforce_prompt_format(prompt, resolution, aspect_ratio, negative_prompt)`
-   **Purpose:** Ensures every prompt, regardless of how it was generated, adheres to a final consistent structure before being sent to Imagen 3.
-   **Process:**
    -   Cleans the main prompt content, removing duplicate or misplaced resolution/aspect ratio mentions.
    -   Appends the correct `resolution` and `aspect_ratio` (e.g., ", 3840x2160 resolution, 16:9 aspect ratio").
    -   Appends the negative prompt content, clearly demarcated (e.g., ". Avoid: blurry, low quality").
    -   Includes a patch to handle potential duplicate "Avoid:" clauses by renaming the second one.
-   **Outcome:** A standardized, clean prompt ready for the image generation API.

## Tips for Effective Prompt Engineering with AI Wallgen

-   **Leverage `user_preferences.json`:** Don't just rely on the main prompt text. Populate your `imagen_settings` with details about camera, lighting, color, style, etc. Add custom keys for unique effects. The AI prompt generators are designed to use this rich context.
-   **Use AI Preset/Style Generation:** Generate diverse starting points for your settings using the [AI Preset](./feature_ai_preset_generation.md) and [AI Style](./feature_ai_style_generation.md) generators.
-   **Iterate with Custom Prompts:** Start with a simple idea in a custom prompt, let AI Wallgen enhance it using your detailed preferences, then refine further if needed.
-   **Master Negative Prompts:** Provide specific negative terms. Let the AI infer additional subject-specific negatives by providing clear positive concepts.

By understanding these components, you can better control and guide AI Wallgen's powerful prompt engineering capabilities to achieve your desired artistic vision.
