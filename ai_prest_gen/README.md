# AI Preset Generator (`ai_prest_gen`) Module

## Overview

The `ai_prest_gen` module is a core component of the AI Wallpaper Generator project, responsible for intelligently generating creative and coherent presets for wallpaper generation. It leverages Google's Gemini AI to produce diverse settings based on style categories, user inputs, and a comprehensive catalog of artistic styles.

The primary goal of this module is to automate and enhance the creative process by providing users with unique, AI-generated starting points for their wallpaper designs.

## Architecture

The module is designed with a modular and data-driven approach:

1.  **Main Orchestrator (`ai_preset_generator.py`):**
    *   This is the entry point and central script for generating AI presets.
    *   It handles user interaction (if not run with direct style arguments), Gemini API communication, style categorization, prompt construction, response parsing, validation, and preset saving (including caching).
    *   It utilizes helper functions to manage distinct parts of the generation workflow.

2.  **Gemini Configuration (`gemini_config_preset.py`):**
    *   Manages the initialization and configuration of the Google Gemini API specifically for the needs of this preset generation module.
    *   Handles API key retrieval and allows for selection from available Gemini models for preset generation.

3.  **Style Categorization (`style_category_catalog.py`):**
    *   Contains the logic to categorize a given style name (e.g., "oil painting", "cyberpunk action") into a predefined category.
    *   This categorization is crucial for selecting appropriate templates and AI instructions.
    *   It loads its data (keywords, hybrid rules, preferred order, AI instructions) from JSON files located in the `catalog_data/` subdirectory.

4.  **Style Template Dispatcher (`style_templates.py`):**
    *   Acts as a central router (`get_template_for_category` function) that, based on a detected style category, delegates to the appropriate specialized template module to fetch a base JSON template structure.
    *   Uses a priority list (defined in `catalog_data/preferred_order.json` via `style_category_catalog.py`) to resolve conflicts if a style name matches multiple categories.

5.  **Specialized Template Modules (`*_style_templates.py`):**
    *   A collection of Python files, each dedicated to a broad group of styles (e.g., `photographic_style_templates.py`, `digital_style_templates.py`, `hybrid_style_templates.py`, `traditional_style_templates.py`, `illustration_style_templates.py`, `portrait_style_templates.py`, `three_d_style_templates.py`, `unique_style_templates.py`).
    *   Each module contains specific `get_<style_name>_template()` functions that return detailed JSON-like dictionary structures tailored for that particular style. These templates provide the foundation upon which the Gemini AI builds the final preset.

6.  **Camera Settings (`camera_settings.py`):**
    *   Provides dynamic and realistic camera settings (`get_dynamic_camera_settings`) for photographic and 3D styles, enhancing the technical accuracy of generated presets for these categories.

7.  **Catalog Data (`catalog_data/` directory):**
    *   This subdirectory is central to the module's data-driven design. It contains JSON files that define:
        *   `style_keywords.json`: Keywords used to map style names to categories.
        *   `hybrid_keyword_rules.json` & `hybrid_token_rules.json`: Rules for identifying complex hybrid styles.
        *   `preferred_order.json`: A list defining the priority for resolving style category conflicts.
        *   `style_instructions.json`: Base instructions for the Gemini AI, which can be tailored per category. (The system processes this into `style_instructions_corrected.json` at import time for internal template replacements).

## Key Files and Their Roles

*   **`ai_preset_generator.py`**: Main script; orchestrates preset generation.
*   **`style_category_catalog.py`**: Handles style name categorization and loads AI instructions. Relies heavily on `catalog_data/`.
*   **`style_templates.py`**: Central dispatcher for retrieving base templates for styles. Imports functions from all specialized `*_style_templates.py` modules.
*   **`gemini_config_preset.py`**: Manages Gemini API setup and model selection for this module.
*   **`camera_settings.py`**: Provides dynamic camera settings.
*   **`digital_style_templates.py`**: Templates for digital art styles (e.g., vector, pixel art, glitch).
*   **`hybrid_style_templates.py`**: Templates for fusion styles (e.g., watercolor_pencil, cyberpunk_action).
*   **`illustration_style_templates.py`**: Templates for various illustration sub-genres (e.g., comic, anime, children's).
*   **`photographic_style_templates.py`**: Templates for photographic styles (e.g., cinematic, noir, street).
*   **`portrait_style_templates.py`**: Templates for different portrait styles.
*   **`three_d_style_templates.py`**: Templates for 3D rendering styles (e.g., voxel, low_poly, anime_3d).
*   **`traditional_style_templates.py`**: Templates for traditional art mediums (e.g., oil_painting, watercolor, charcoal).
*   **`unique_style_templates.py`**: Contains templates for styles that don't neatly fit into other broad categories or have very distinct characteristics (e.g., psychedelic, biopunk).
*   **`catalog_data/*.json`**: Data files driving categorization and AI instruction.

## Extending with New Styles or Categories

To add a new style or category:

1.  **Define Keywords (if necessary):**
    *   If the new style needs specific keywords for detection, add them to `catalog_data/style_keywords.json` under an existing or new category.
    *   For complex hybrid styles, define rules in `catalog_data/hybrid_keyword_rules.json` or `catalog_data/hybrid_token_rules.json`.

2.  **Update Preferred Order (if new category):**
    *   If you've added a new category, add it to `catalog_data/preferred_order.json` in a sensible position to manage how it's prioritized if a style name matches multiple categories.

3.  **Create/Update AI Instructions (optional but recommended):**
    *   Add specific instructions for the Gemini AI for the new style/category in `catalog_data/style_instructions.json`. This helps the AI generate more relevant and nuanced presets.

4.  **Implement the Template Function:**
    *   Decide which specialized `*_style_templates.py` module is most appropriate for the new style (e.g., a new digital technique would go into `digital_style_templates.py`).
    *   Create a new function, e.g., `get_my_new_style_template(style_category: str) -> Dict[str, Any]:`, within that module.
    *   This function should return a dictionary representing the base template structure for "my_new_style". Refer to existing template functions for structure and detail.

5.  **Update the Main Dispatcher (`style_templates.py`):**
    *   Import your new `get_my_new_style_template` function at the top of `style_templates.py` from its respective module.
    *   Add an `elif main_category == "my_new_style":` condition to the `get_template_for_category` function to call your new template function. Ensure it's placed correctly according to the desired dispatch priority if it's a very specific style.

6.  **Testing:**
    *   Manually test by running `ai_preset_generator.py` and trying to generate a preset for your new style.
    *   If a testing suite is in place (as per enhancement plans), add unit tests for the new template function and categorization logic.

By following these steps, the module can be systematically extended to support a wider range of artistic styles.
