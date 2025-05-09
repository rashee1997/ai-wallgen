# Other Key Features in AI Wallgen

Beyond the core AI-driven generation and advanced prompt engineering, AI Wallgen offers several other useful features to enhance your experience.

## 1. Generation History Management

AI Wallgen keeps a record of your wallpaper generation attempts, allowing you to review past creations, the prompts used, and the settings that led to them.

**Key Aspects:**

-   **Storage:** History is stored in a local SQLite database located at `wall_gen/history/history.db`.
-   **Logged Information:** For each generation, the following details are typically saved:
    -   Date and time of generation.
    -   The initial prompt or tags used.
    -   The AI-enhanced prompt (if applicable).
    -   The prompt used for AI-driven preset/style generation (if applicable).
    -   The filename of the generated image.
    -   A JSON string containing the `user_preferences`, `imagen_settings`, and `wallpaper_settings` active at the time.
    -   Output messages related to the generation (e.g., success/failure).
-   **Accessing History:** The application provides a way to view this history, typically through a CLI command (e.g., `python run_wallgen.py --view-history`). The history is displayed in a formatted table in the console.
-   **Benefits:**
    -   Easily recall settings for successful generations.
    -   Track your creative process.
    -   Helpful for debugging or understanding why certain prompts yielded particular results.

The `wall_gen.history.history_manager.HistoryManager` class is responsible for all history-related operations, including adding new entries and fetching records for display.

## 2. Image Editing Capabilities

AI Wallgen includes an `image_editor.py` module that provides a range of image manipulation functionalities, primarily leveraging libraries like Pillow, OpenCV, and Scikit-image. While not a full-fledged image editor GUI, these functions can be used programmatically or potentially integrated into future interactive editing features.

**Core Features:**

-   **Undo/Redo:** An `ImageHistory` class supports undoing and redoing editing operations.
-   **Selection Masks (`SelectionMask` class):**
    -   Allows for creating boolean masks (rectangle, ellipse, lasso/free-form polygon) to apply edits to specific regions of an image.
    -   Masks can be inverted, cleared, combined (union, intersection, difference), and serialized.
    -   The `apply_with_mask` function enables applying any processing function only to the masked area.
-   **Basic Adjustments (Pillow-based):**
    -   Brightness, Contrast, Saturation (Color), Sharpness.
    -   Gamma Correction, Blur (GaussianBlur), Grayscale conversion, Invert colors.
    -   Rotation (with transparency handling), Cropping, Adding Borders.
-   **Pillow ImageFilter Effects:**
    -   Emboss, Edge Enhance, Edge Enhance More, Find Edges, Detail, Smooth, Smooth More.
-   **OpenCV-based Filters:**
    -   High-Pass Filter, Histogram Equalization (color-preserving), Contour Detection (Canny).
    -   Gaussian Noise addition, Pencil Sketch effect, Sepia tone, Sharpen (kernel-based), X-Ray effect.
-   **Scikit-image Filters:**
    -   Edge Detection: Laplace, Sobel, Scharr, Prewitt, Roberts.
    -   Gabor filter (for texture analysis).
    -   Thresholding: Otsu, Niblack, Sauvola.
-   **Placeholders:** Some advanced functions like `ai_enhance` and `remove_background` are defined but are placeholders, indicating potential future integrations requiring dedicated AI models or libraries.

These editing tools provide a foundation for post-processing generated wallpapers or for more complex image manipulation tasks within the application's ecosystem.

## 3. Cross-Platform Wallpaper Setting

AI Wallgen attempts to automatically set the generated image as your desktop wallpaper across different operating systems.

**Key Aspects (`wall_gen.wallpaper_service.py`):**

-   **OS Detection:** It first determines the operating system (Windows, macOS, Linux).
-   **Windows:** Uses the `SystemParametersInfoW` function via `ctypes` to set the desktop wallpaper.
-   **macOS (Darwin):** Executes an AppleScript command using `osascript` to tell System Events to set the desktop picture.
-   **Linux:**
    -   **Desktop Environment Detection (`detect_linux_desktop_env`):** This is a crucial step on Linux. The script tries to identify the current desktop environment (e.g., GNOME, KDE, XFCE, MATE, Cinnamon) by checking environment variables and running processes.
    -   **Specific Commands:** Based on the detected DE, it uses appropriate command-line tools:
        -   `gsettings`: For GNOME, Unity, Budgie, Pantheon, Deepin, Cinnamon, MATE.
        -   `xfconf-query`: For XFCE.
        -   `qdbus` with a PlasmaShell script: For KDE/Plasma.
    -   **Fallback Setters (`_try_linux_fallback_setters`):** If the DE is unknown or a specific command fails, it attempts to use common Linux wallpaper utilities like:
        -   `feh --bg-fill <path>`
        -   `nitrogen --set-zoom-fill --save <path>`
        -   A general `gsettings` command for GNOME as a last resort.
-   **Path Handling:** Ensures absolute image paths are used.
-   **Error Handling:** Includes error logging if commands fail or required tools are not found.

This feature provides convenience by allowing users to immediately apply their generated creations, with options often available in the main application (e.g., `python run_wallgen.py --skip-preview`) to set the wallpaper directly after generation.
