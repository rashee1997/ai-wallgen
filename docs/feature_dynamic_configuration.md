# Dynamic Configuration with `user_preferences.json`

AI Wallgen offers a powerful and flexible way to customize your image generation experience through the `user_preferences.json` file. This file not only stores standard settings but also allows for **dynamic inclusion of custom user-defined parameters** directly into the AI's prompt generation context.

## Overview

The core idea is that users can add their own descriptive keys and values within the `user_preferences.json` structure, particularly within nested settings like `imagen_settings`. AI Wallgen will then "flatten" these settings and incorporate them into the detailed context provided to the Gemini model when it generates the actual prompt for image creation. This allows for a high degree of personalization and creative control.

Key Modules Involved:
-   `wall_gen.settings_modules.user_preferences.UserPreferences`: Class responsible for loading and saving `user_preferences.json`. It defines many standard settings.
-   `wall_gen.prompt_service.flatten_settings`: A crucial function that recursively processes settings dictionaries.
-   `wall_gen.prompt_service.dynamic_technical_context`: Uses the flattened settings to build a natural language context for the AI.

## How It Works

1.  **`user_preferences.json`:** This file, located in the application's root directory, stores your settings. It's a standard JSON file. You can edit it directly or manage settings through the application's UI (which then saves to this file).

2.  **Adding Custom Keys:**
    While `UserPreferences` class has many predefined fields, the real power for advanced users comes from adding custom keys, especially within nested structures like `imagen_settings`. For example:
    ```json
    // user_preferences.json (partial example)
    {
      "imagen_settings": {
        "camera_settings": {
          "camera_model": "Sony A7R IV",
          "lens_type": "Prime 85mm",
          "my_custom_camera_effect": "Vintage Film Grain" // Custom key
        },
        "lighting_settings": {
          "lighting_type": "Studio Softbox",
          "custom_light_modifier": { // Custom nested dictionary
            "type": "Honeycomb Grid",
            "intensity_factor": 0.7
          }
        },
        "my_overall_artistic_goal": "Photorealistic with a touch of surrealism" // Another custom key
      },
      // ... other preferences ...
    }
    ```

3.  **Settings Flattening (`flatten_settings`):**
    When AI Wallgen prepares to generate a prompt (specifically when using the AI-driven prompt generation method), it processes the relevant parts of your `user_preferences` (primarily `imagen_settings`). The `flatten_settings` function in `wall_gen.prompt_service` (and also found in `wall_gen.prompt_modules.core`) recursively traverses these settings.
    -   It converts dictionary keys into a more readable format (e.g., `my_custom_camera_effect` becomes "My custom camera effect").
    -   It creates a list of all settings, including your custom ones, as key-value pairs. For the example above, it might produce items like:
        -   (`Imagen settings - Camera settings`, "My custom camera effect", "Vintage Film Grain")
        -   (`Imagen settings - Lighting settings - Custom light modifier`, "Type", "Honeycomb Grid")
        -   (`Imagen settings - Lighting settings - Custom light modifier`, "Intensity factor", "0.7")
    -   (`Imagen settings`, "My overall artistic goal", "Photorealistic with a touch of surrealism")

4.  **Dynamic Technical Context (`dynamic_technical_context`):**
    The flattened list of settings is then passed to the `dynamic_technical_context` function (detailed further in the [Advanced Prompt Engineering](./feature_prompt_engineering.md) guide). This function attempts to build natural language phrases from these key-value pairs.

    For instance, consider the following custom keys in `user_preferences.json`:
    ```json
    {
      "preferred_styles": ["fantasy", "minimalist"],
      "aspect_ratio": "21:9",
      "imagen_settings": {
        "lighting_settings": {
          "lighting_type": "neon",
          "custom_light_mode": "ambient disco"
        },
        "composition_settings": {
          "technique": "rule_of_thirds",
          "experimental_composition": {
            "geometry_focus": "hexagonal_pattern",
            "symmetry_level": 0.75
          }
        },
        "my_extra_tag": "magic glow",
        "custom_materials": ["silk", "obsidian"]
      },
      "my_global_note": "I love ultra-wide scenes"
    }
    ```
    The `dynamic_technical_context` function might then generate a string portion like:
    `"...and with magic glow my extra tag that, using custom light mode that, geometry_focus: hexagonal_pattern, symmetry_level: 0.75, custom materials that, I love ultra-wide scenes my global note that, ..."`
    (The exact phrasing can vary based on the internal logic of `phrase_from_kv` within `dynamic_technical_context` and other settings processed.)

    The initial example from the "Adding Custom Keys" section would produce phrases like:
    -   "Vintage Film Grain My custom camera effect that"
    -   "Honeycomb Grid Type that"
    -   "0.7 Intensity factor that"
    -   "Photorealistic with a touch of surrealism My overall artistic goal that"


5.  **Informing the AI Prompt Generator:**
    This dynamically generated text, rich with your custom settings, is then included in the instructions given to the Gemini model that generates the *final image prompt*. This means your custom parameters directly influence the AI's understanding of the desired image, leading to more tailored and unique results.

## Benefits

-   **Extensibility:** Add new creative parameters without needing to modify AI Wallgen's core code.
-   **Fine-grained Control:** Inject very specific details or artistic concepts into the prompt generation process.
-   **Experimentation:** Easily test how different custom parameters affect the AI's output.

## Best Practices for Custom Keys

-   **Nest Appropriately:** While you can add keys at various levels, nesting them within relevant sections (e.g., custom camera details inside `camera_settings`) keeps your `user_preferences.json` organized.
-   **Use Descriptive Key Names:** Clear key names (e.g., `my_artistic_theme` instead of `param1`) will translate better into the flattened context.
-   **Avoid Reserved Names:** Be mindful of existing key names used by the application to avoid conflicts, especially for top-level settings directly managed by the `UserPreferences` class. The `flatten_settings` function has an `ignore_keys` set (e.g., for `negative_prompt` which is handled separately).

This dynamic configuration capability is a cornerstone of AI Wallgen's flexibility, allowing users to deeply customize the AI's creative process.
