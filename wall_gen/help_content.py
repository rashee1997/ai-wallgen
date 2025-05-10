"""
Stores context-sensitive help content for the WallGen TUI.
"""
from typing import Dict

HELP_TEXTS: Dict[str, str] = {
    "MAIN_MENU": (
        "Main Menu Help:\n\n"
        "This is the central navigation point for the AI Wallpaper Generator.\n\n"
        "- '1: Generate AI Wallpaper': Start the interactive process to create a new wallpaper using AI, based on your preferences or custom prompts.\n"
        "- '2: Generate Prompt Only': Similar to option 1, but will only generate the text prompt and save it, without calling the AI to generate an image.\n"
        "- '3: Manage Preferences': Access sub-menus to customize various settings like wallpaper styles, moods, AI parameters, output quality, etc.\n"
        "- '4: Tools & Utilities': Access additional tools, which might include cache management, preset utilities, or other helper functions.\n"
        "- '5: View Generation History': Browse a history of previously generated wallpapers and their associated prompts and settings.\n"
        "- '7: Preview Recent Images': Quickly view recently generated images using the configured preview tool.\n"
        "- 'E: Exit': Save any changed preferences and close the application.\n\n"
        "Tip: At most prompts, you can type 'h' or '?' to get contextual help."
    ),
    "MANAGE_PREFERENCES_MENU": (
        "Manage Preferences Menu Help:\n\n"
        "This menu allows you to configure various aspects of the wallpaper generation process.\n\n"
        "- '1: Wallpaper Settings': Adjust general wallpaper settings like preferred styles, moods, artistic influences, and subject matter.\n"
        "- '2: Advanced Options': Configure more detailed AI generation parameters, potentially including specific model settings, negative prompts, and quality adjustments.\n"
        "- '3: Reset All Settings to None': Clears all your saved preferences, reverting to default behavior. Use with caution.\n"
        "- 'b: Back': Return to the Main Menu."
    ),
    # Renaming GENERATE_MENU_PROMPT_TYPE to GENERATE_MENU_OVERALL and updating content
    "GENERATE_MENU_OVERALL": ( 
        "Generate Wallpaper/Prompt Menu Help:\n\n"
        "This menu allows you to choose the method for generating your wallpaper prompt and to access advanced settings or load presets before generation.\n\n"
        "- '1: Use Gemini AI to generate a prompt': The AI will create a prompt based on your configured preferences.\n"
        "- '2: Use a random prompt': Generates a prompt using random tags or styles.\n"
        "- '3: Enter your own custom prompt': You provide the exact prompt text.\n"
        "- '4: Advanced Options - Fine-tune generation parameters': Access detailed settings before this generation run.\n"
        "- '5: Load Saved Preset': Load a previously saved set of configurations to use for this generation.\n"
        "- 'B: Back to Main Menu': Return to the main application menu."
    ),
    "GENERATE_CUSTOM_PROMPT_INPUT": (
        "Enter Custom Prompt Help:\n\n"
        "Please type the text prompt you want to use for generating the wallpaper.\n"
        "The application might apply further enhancements or combine this with your preferences depending on the configuration.\n"
        "Enter 'b' to go back without entering a custom prompt."
    ),
    "AI_PRESET_GENERATOR_MENU": ( 
        "AI Preset Generator Menu Help:\n\n"
        "This tool helps you generate new wallpaper setting presets using AI.\n\n"
        "- '1: Generate New AI Preset': Starts the process to create a new preset. You might be asked for a base style or theme for the AI to work with.\n"
        "- 'q: Quit': Exit the AI Preset Generator and return to the previous menu or exit the script if run standalone.\n\n"
        "Generated presets can be used later to quickly apply a full set of configurations for wallpaper generation."
    ),
    # Add more contexts and their help texts as needed for other menus.
    # Example for a hypothetical tools menu:
    "TOOLS_MENU": (
        "Tools & Utilities Menu Help:\n\n"
        "This menu provides access to various utility functions.\n\n"
        "- '1: Cache Management': Options to view or clear image/prompt caches.\n"
        "- '2: AI Preset Utilities': May include options to list, apply, or manage AI-generated presets.\n"
        "- 'b: Back': Return to the Main Menu."
    ),
    "WALLPAPER_SETTINGS_MENU": (
        "Wallpaper Settings Menu Help:\n\n"
        "Configure the aesthetic and thematic elements of your generated wallpapers.\n"
        "- Options typically include: Preferred Styles, Moods, Artists, Colors, Subject Matter, etc.\n"
        "- 'b: Back': Return to the Manage Preferences Menu."
    ),
    "ADVANCED_OPTIONS_MENU": (
        "Advanced Options Menu Help:\n\n"
        "Fine-tune AI generation parameters and other technical settings.\n"
        "- Options may include: Negative Prompts, AI Model Selection (if applicable), Quality Settings, Aspect Ratio, Resolution Overrides.\n"
        "- 'b: Back': Return to the Manage Preferences Menu."
    ),
    # The duplicated GENERATE_MENU_OVERALL entry is removed here.
    # The first one, which was the correctly updated one, remains.
    "IMAGE_PREVIEW_MENU": (
        "Image Preview Menu Help:\n\n"
        "Preview recently generated images or specific image files.\n"
        "- Options typically allow selecting an image from history or a file path.\n"
        "- You can usually set the previewed image as your wallpaper from here.\n"
        "- 'b: Back': Return to the Main Menu."
    ),
    "AI_PRESET_STYLE_SOURCE_CHOICE": (
        "Choose Style Source for AI Preset Help:\n\n"
        "This step determines the base style the AI will use to generate a new preset.\n"
        "- '1: Enter Custom Style': You will be prompted to type in a style name or description manually.\n"
        "- '2: Generate AI Style': If available, this uses another AI function to generate a random style name/description to serve as the base.\n"
        "- 'b: Back': Cancel preset generation and return."
    ),
    "AI_PRESET_SAVE_CONFIRMATION": (
        "Save AI Generated Preset Help:\n\n"
        "You have reviewed the AI-generated preset settings.\n"
        "- 'y (yes)': Save this preset. It will typically be stored in the 'presets' folder and may be added to a preset database for later use.\n"
        "- 'n (no)': Discard this generated preset. You can try generating another one."
    ),
    "ORCHESTRATE_PROMPT_CONFIRMATION": (
        "Proceed with Prompt Confirmation Help:\n\n"
        "The AI has generated a prompt for your wallpaper.\n"
        "- 'yes' or 'y': Confirm and proceed to generate the image using this prompt.\n"
        "- 'no' or 'n': Cancel this generation attempt. You might return to a previous menu to try generating a different prompt."
    ),
    "WALLPAPER_SETTINGS_PREVIEW_BACKEND_CHOICE": (
        "Preview Backend Selection Help:\n\n"
        "Choose the graphical toolkit or method for displaying image previews.\n"
        "- 'qt': Uses a Qt-based window for preview (requires PyQt5/PySide2).\n"
        "- 'gtk': Uses a GTK-based window for preview (requires PyGObject).\n"
        "- 'console': May attempt a basic preview in the terminal if supported (often limited).\n"
        "Select the one most appropriate for your system or preference."
    ),
    "ADVANCED_OPTIONS_ASPECT_RATIO_CHOICE": (
        "Aspect Ratio Selection Help:\n\n"
        "Choose the desired aspect ratio for your wallpaper.\n"
        "Common options include:\n"
        "- 16:9 (Standard Widescreen)\n"
        "- 21:9 (Ultrawide)\n"
        "- 4:3 (Older Monitors/Tablets)\n"
        "- 3:2 (Common for Photography)\n"
        "- 1:1 (Square)\n"
        "Select 'b' to cancel and keep the current setting."
    ),
    "GENRES_MENU": (
        "Manage Genres Menu Help:\n\n"
        "This menu allows you to manage your list of preferred genres, which can influence AI prompt generation.\n"
        "- '1: Add genre': Select a genre from the available list to add to your preferences.\n"
        "- '2: Remove genre': Remove a genre from your current list of preferences.\n"
        "- '3: Clear all genres': Remove all genres from your preferences.\n"
        "- 'b: Back': Return to the previous menu."
    ),
    "STYLES_MENU": (
        "Manage Styles Menu Help:\n\n"
        "Configure your preferred artistic styles for wallpaper generation.\n"
        "- '1: Add style': Add a new style to your preferred list (you can type a custom style or select from available categories).\n"
        "- '2: Remove style': Remove a style from your preferred list.\n"
        "- '3: Clear all styles': Clear all preferred styles.\n"
        "- '4: Generate Random Style Mix': Let the AI generate a mix of styles for you.\n"
        "- '5: Advanced Style Configuration': Access detailed settings for art movement, era, and post-processing effects related to styles.\n"
        "- 'b: Back': Return to the previous menu."
    ),
    "STYLES_CLEAR_CONFIRMATION": (
        "Clear Preferred Style Confirmation Help:\n\n"
        "You are about to clear your currently set preferred style(s).\n"
        "- 'y (yes)': Proceed to clear the style(s). The application will revert to default style selection behavior or prompt you for new styles.\n"
        "- 'n (no)': Cancel and keep your current preferred style(s)."
    ),
    "STYLES_RANDOM_MIX_CONFIRMATION": (
        "Set Random Style Mix Confirmation Help:\n\n"
        "A random mix of styles has been generated.\n"
        "- 'y (yes)': Set this generated mix as your new preferred style. This will overwrite any previously set preferred style(s).\n"
        "- 'n (no)': Discard this random mix and keep your current preferred style(s)."
    ),
    "STYLES_ART_MOVEMENT_CHOICE": (
        "Select Art Movement Help:\n\n"
        "Choose an art movement to influence the style of the generated wallpaper. This can add a specific historical or artistic character.\n"
        "- Select a number corresponding to a listed movement.\n"
        "- '0: None': Do not apply a specific art movement.\n"
        "- '6: Custom Movement': Allows you to type in a custom art movement name.\n"
        "- 'b: Back': Return to the main Styles menu."
    ),
    "STYLES_STYLE_ERA_CHOICE": (
        "Select Style Era Help:\n\n"
        "Choose a style era to further define the artistic period. This can influence the overall aesthetic.\n"
        "- Select a number corresponding to a listed era (e.g., Modern, Golden Age).\n"
        "- '4: Custom Era': Allows you to type in a custom style era.\n"
        "- 'b: Back': Return to the main Styles menu."
    ),
    "STYLES_POST_PROCESSING_CHOICE": (
        "Select Post-Processing Effects Help:\n\n"
        "Choose post-processing effects to apply to the generated image. These can enhance or alter the final look.\n"
        "- Select a number corresponding to a listed effect (e.g., Bloom, Vignette, Film Grain).\n"
        "- '13: No Post-Processing': Remove all post-processing effects.\n"
        "- '14: Custom Effects': Allows you to type in custom effects, comma-separated.\n"
        "- 'b: Back': Return to the main Styles menu."
    ),
    "CAMERA_MENU": (
        "Camera & Technical Settings Menu Help:\n\n"
        "Configure camera-specific parameters to influence the photographic qualities of your generated image.\n"
        "- Options include: Camera Model, Lens Type, Aperture, Depth of Field, Special Lens Effects, Focal Length, Shutter Speed, ISO, and Filter Type.\n"
        "- 'b: Back': Return to the Advanced Options menu."
    ),
    "CAMERA_FILTER_TYPE_CHOICE": (
        "Select Filter Type Help:\n\n"
        "Choose a camera filter type to apply to the image, affecting color, contrast, or adding effects.\n"
        "- 'UV': Simulates a UV filter, often for protection or slight haze reduction.\n"
        "- 'Polarizer': Reduces reflections and enhances color saturation, especially in skies.\n"
        "- 'ND (Neutral Density)': Reduces overall light, allowing for longer exposures or wider apertures.\n"
        "- 'Color Filter': Applies a specific color tint (e.g., red, blue, green).\n"
        "- 'Soft Focus Filter': Creates a dreamy, soft-focus effect.\n"
        "- 'Custom Filter': Allows you to specify a custom filter type by name.\n"
        "- 'b: Back': Return to the Camera Settings menu."
    ),
    "CAMERA_MODEL_CHOICE": (
        "Select Camera Model Help:\n\n"
        "Choose a camera model type. This can subtly influence the image characteristics (e.g., sensor look, grain).\n"
        "- 'DSLR', 'Mirrorless', 'Medium Format', 'Film Camera': Select a general camera type.\n"
        "- 'Custom Model': Allows you to specify a custom camera model name.\n"
        "- 'b: Back': Return to the Camera Settings menu."
    ),
    "CAMERA_LENS_TYPE_CHOICE": (
        "Select Lens Type Help:\n\n"
        "Choose a lens type, which affects perspective, field of view, and depth characteristics.\n"
        "- 'Wide Angle': Captures a broader scene, can distort perspective.\n"
        "- 'Standard': Mimics human vision (e.g., 50mm equivalent).\n"
        "- 'Telephoto': Compresses perspective, good for distant subjects.\n"
        "- 'Macro': For extreme close-ups.\n"
        "- 'Fish Eye': Creates a strong circular distortion.\n"
        "- 'Custom Lens': Allows you to specify a custom lens type.\n"
        "- 'b: Back': Return to the Camera Settings menu."
    ),
    "CAMERA_APERTURE_CHOICE": (
        "Select Aperture Help:\n\n"
        "Choose an aperture (f-stop) value. This controls depth of field (how much is in focus) and light intake.\n"
        "- Lower f-numbers (e.g., f/1.4, f/2.8) mean wider apertures, shallower depth of field (blurry background), and more light.\n"
        "- Higher f-numbers (e.g., f/8, f/16) mean narrower apertures, deeper depth of field (more in focus), and less light.\n"
        "- 'Custom Aperture': Allows you to specify a custom f-stop value.\n"
        "- 'b: Back': Return to the Camera Settings menu."
    ),
    "CAMERA_DOF_CHOICE": (
        "Select Depth of Field Help:\n\n"
        "Choose the desired depth of field effect, which determines how much of the scene is in sharp focus.\n"
        "- 'Very Shallow' / 'Shallow': Only a small part of the image is in focus, blurring the background/foreground (bokeh).\n"
        "- 'Moderate': A balanced amount of the scene is in focus.\n"
        "- 'Deep' / 'Very Deep': Most or all of the scene is in sharp focus, from foreground to background.\n"
        "- 'Custom Setting': Allows you to specify a custom depth of field description.\n"
        "- 'b: Back': Return to the Camera Settings menu."
    ),
    "CAMERA_LENS_EFFECT_CHOICE": (
        "Select Special Lens Effects Help:\n\n"
        "Choose special optical effects often associated with camera lenses.\n"
        "- 'Bokeh': Pleasing out-of-focus blur, especially in highlights.\n"
        "- 'Lens Flare': Streaks or circles of light caused by bright light sources.\n"
        "- 'Soft Focus': A dreamy, slightly blurred effect.\n"
        "- 'Tilt-Shift': Creates a miniature effect or selective focus plane.\n"
        "- 'Chromatic Aberration': Color fringing around high-contrast edges.\n"
        "- 'Custom Effect': Allows you to specify a custom lens effect.\n"
        "- 'No Special Effects': Avoids adding specific lens effects.\n"
        "- 'b: Back': Return to the Camera Settings menu."
    ),
    "COLOR_DETAIL_MENU": (
        "Color & Detail Settings Menu Help:\n\n"
        "Configure color properties, detail levels, and texture quality for your generated image.\n"
        "- Options include: Color Scheme, Palette Type, Color Temperature, Detail Level, and Texture Quality.\n"
        "- 'b: Back': Return to the Advanced Options menu."
    ),
    "COLOR_SCHEME_CHOICE": (
        "Select Color Scheme Help:\n\n"
        "Choose a color scheme to define the relationships between colors in your image.\n"
        "- 'Monochromatic': Uses variations of a single color.\n"
        "- 'Complementary': Uses colors opposite each other on the color wheel (e.g., red & green).\n"
        "- 'Analogous': Uses colors adjacent to each other on the color wheel (e.g., red, orange, yellow).\n"
        "- 'Triadic': Uses three colors evenly spaced around the color wheel.\n"
        "- 'Split Complementary': A variation of complementary, using two colors adjacent to the complement.\n"
        "- 'Tetradic': Uses four colors arranged into two complementary pairs.\n"
        "- 'Custom': Allows you to specify a custom color scheme description.\n"
        "- 'b: Back': Return to the Color & Detail Settings menu."
    ),
    "COLOR_PALETTE_TYPE_CHOICE": (
        "Select Palette Type Help:\n\n"
        "Choose the overall character of the color palette.\n"
        "- 'Warm': Emphasizes reds, oranges, yellows.\n"
        "- 'Cool': Emphasizes blues, greens, purples.\n"
        "- 'Neutral': Uses grays, browns, whites, blacks.\n"
        "- 'Pastel': Soft, desaturated colors.\n"
        "- 'Vibrant': Bright, saturated colors.\n"
        "- 'Muted': Desaturated, less intense colors.\n"
        "- 'Custom': Allows you to specify a custom palette type description.\n"
        "- 'b: Back': Return to the Color & Detail Settings menu."
    ),
    "COLOR_TEMPERATURE_CHOICE": (
        "Select Color Temperature Help:\n\n"
        "Choose the overall warmth or coolness of the light and colors.\n"
        "- 'Warm (Red/Yellow)': Suggests warmth, like sunlight or firelight.\n"
        "- 'Cool (Blue/Cyan)': Suggests coolness, like shade or moonlight.\n"
        "- 'Neutral': Balanced, without a strong warm or cool cast.\n"
        "- 'Mixed': A combination of warm and cool light sources or areas.\n"
        "- 'Custom': Allows you to specify a custom color temperature description.\n"
        "- 'b: Back': Return to the Color & Detail Settings menu."
    ),
    "DETAIL_LEVEL_CHOICE": (
        "Select Detail Level Help:\n\n"
        "Choose the desired level of detail in the generated image.\n"
        "- 'Fine': High level of intricate detail.\n"
        "- 'Medium': Balanced level of detail.\n"
        "- 'Coarse': Less detail, more emphasis on broad forms or textures.\n"
        "- 'None': Minimal detail, potentially abstract or very simplified.\n"
        "- 'Custom': Allows you to specify a custom detail level description.\n"
        "- 'b: Back': Return to the Color & Detail Settings menu."
    ),
    "TEXTURE_QUALITY_CHOICE": (
        "Select Texture Quality Help:\n\n"
        "Choose the desired quality and prominence of textures in the image.\n"
        "- 'High': Textures are sharp, clear, and well-defined.\n"
        "- 'Medium': Textures are present and noticeable but not overly sharp.\n"
        "- 'Low': Textures are subtle or less defined.\n"
        "- 'None': Minimal or no discernible texture, smooth surfaces.\n"
        "- 'Custom': Allows you to specify a custom texture quality description.\n"
        "- 'b: Back': Return to the Color & Detail Settings menu."
    ),
    "CONFIRM_RESET_ALL_SETTINGS": (
        "Confirm Reset All Settings Help:\n\n"
        "You are about to reset ALL saved preferences to their initial (empty or default) state.\n"
        "This action cannot be undone.\n"
        "- 'y (yes)': Proceed with resetting all settings.\n"
        "- 'n (no)': Cancel and keep your current settings."
    ),
    "TOOLS_SELECT_GEMINI_MODEL_CHOICE": (
        "Select Gemini Model (Non-Imagen) Help:\n\n"
        "Choose which Google Gemini model to use for tasks OTHER than direct image generation (e.g., prompt generation, style analysis, etc.).\n"
        "Different models have varying capabilities, speeds, and potential costs.\n"
        "- Select a number corresponding to an available model.\n"
        "- 'c: Cancel': Return without changing the model."
    ),
    "DEFAULT_HELP": (
        "No specific help available for this context.\n"
        "Try navigating to a main menu section for more options, or check the application's documentation.\n\n"
        "Tip: At most prompts, you can type 'h' or '?' to get contextual help."
    )
}

def get_help_text(context_id: str) -> str:
    """
    Retrieves help text for a given context_id.
    Returns default help if the context_id is not found.
    """
    return HELP_TEXTS.get(context_id, HELP_TEXTS["DEFAULT_HELP"])
