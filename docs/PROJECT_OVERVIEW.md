# AI Wallpaper Generator - Project Overview

## Introduction

The AI Wallpaper Generator is a modular Python application designed to create AI-powered wallpapers using Google's Imagen 3 and Gemini API. The project emphasizes modularity, scalability, and extensibility, supporting user preferences, presets, and cross-platform compatibility.

---

## Main Entry Point: `run_wallgen.py`

- Serves as the primary CLI interface and orchestration script.
- Handles command-line arguments for various generation modes, testing, debugging, and image management.
- Initializes logging, user preferences, cache directories, and system dependencies.
- Coordinates the wallpaper generation process by invoking services from the `wall_gen` package.
- Supports AI preset generation and application via CLI options.
- Manages image preview, caching, history logging, and wallpaper setting.
- Implements graceful exit and preference saving on termination.

---

## `wall_gen` Package Structure

The `wall_gen` package contains the core logic and services of the application, organized as follows:

### Core Service Modules

- `prompt_service.py`: Generates and enhances prompts for AI image generation.
- `image_service.py`: Interfaces with AI APIs to generate images from prompts.
- `wallpaper_service.py`: Manages wallpaper setting and related operations.
- `preview_service.py`: Handles image preview and user confirmation workflows.

### Utility Modules

- `app_utils.py`: Application-level utilities including logging and startup routines.
- `cache_utils.py`: Manages cache directories and file caching.
- `file_utils.py`: File operations including image caching and JSON data handling.
- `ui_utils.py`: User interface utilities for CLI interactions and messaging.
- `image_editor.py`: Image manipulation and editing utilities.
- `graceful_exit.py`: Handles clean application shutdown and resource cleanup.

### Configuration

- `config.py`: General configuration constants.
- `gemini_config.py`: Configuration related to Gemini API usage.

### Sub-packages

- `settings_modules/`: Manages user preferences, presets, settings import/export, and menu management.
- `history/`: Tracks generation history and logs.
- `prompt_modules/`: Contains prompt generation components and formatters.
- `preview_backends/`: Supports different GUI backends for image preview (e.g., Qt, Tkinter).

---

## Core Operational Flows

This section outlines the primary logical flows within the application.

### 1. Core Wallpaper Generation Orchestration

The following diagram illustrates the main end-to-end process for generating a wallpaper, from user invocation to the final image being set or saved. This flow is primarily orchestrated by `run_wallgen.py` and involves several core services from the `wall_gen` package.

```mermaid
graph TD
    A["User Invocation: CLI / Menu"] --> B["run_wallgen.py: main()"];
    B --> C{"Parse Args & Init"};
    C --> D["Load UserPreferences"];
    D --> E{"Generation Task?"};
    E -- Yes --> F["orchestrate_wallpaper_generation"];
    E -- "No / Other" --> X["Other CLI Handlers / Main Menu"];

    subgraph orchestrate_wallpaper_generation
        F0["Start Orchestration"] --> F1{"Prompt Type?"};
        F1 -- Custom --> F2a["prompt_service.generate_final_prompt (type=custom)"];
        F1 -- Random --> F2b["prompt_service.generate_final_prompt (type=random)"];
        F1 -- "AI/Preset" --> F2c["prompt_service.generate_final_prompt (type=gemini/preset)"];
        F2a --> F3["Generated Prompt"];
        F2b --> F3;
        F2c --> F3;
        F3 --> F4{"User Confirm Prompt? (CLI)"};
        F4 -- No --> F_Cancel["End Generation"];
        F4 -- Yes --> F5["image_service.generate_image_from_api"];
        
        subgraph image_service.generate_image_from_api
            F5_A{"SDK Choice"};
            F5_A -- "Vertex AI" --> F5_B["generate_image_with_vertex_ai"];
            F5_A -- "Google GenAI SDK" --> F5_C["generate_image_with_genai_sdk"];
            F5_C --> F5_D{"Direct Imagen Call"};
            F5_D -- Success --> F5_E["Temp Image Path(s) Created"];
            F5_D -- Fail --> F5_F["Fallback to Gemini Content Gen"];
            F5_F --> F5_E;
            F5_B --> F5_E;
        end
        
        F5 --> F5_Result["Temp Image Path(s) Created"];
        F5_Result --> F7["file_utils: Cache & Save Image"];
        F7 --> F8["history_manager: Add to History"];
        F8 --> F9["preview_service.show_preview_and_confirm_set"];

        subgraph preview_service.show_preview_and_confirm_set
            F9_A{"Skip Preview?"};
            F9_A -- Yes --> F9_B["wallpaper_service.set_os_wallpaper"];
            F9_A -- No --> F9_C{"GUI Backend? (Qt/Tkinter)"};
            F9_C -- Yes --> F9_D["Show GUI Preview & Confirm"];
            F9_D -- Set --> F9_B;
            F9_D -- Cancel --> F9_E["End Preview"];
            F9_C -- "No / Fail" --> F9_F{"CLI Confirm Set?"};
            F9_F -- Yes --> F9_B;
            F9_F -- No --> F9_E;
        end
        F9_B --> F_Success["Wallpaper Set"];
        F9_E --> F_NoSet["Wallpaper Not Set"];
    end
    
    F_Success --> F_End["End Orchestration"];
    F_NoSet --> F_End;
    F_Cancel --> F_End;
    X --> X_End["End Other Task"];
```

---

## AI Style Generation: `ai_style_generator.py`

- Provides functionality to generate artistic style descriptions using the Gemini API.
- Implements retry logic with exponential backoff for robust API interaction.
- Supports style categorization and canonicalization for consistent style naming.
- Includes an interactive CLI for generating and saving AI styles.
- Handles API key initialization and error management.

---

## AI Preset Generation: `ai_prest_gen` Package

- Contains the `ai_preset_generator.py` script for generating AI wallpaper presets.
- Uses Gemini API to create coherent random presets based on style categories.
- Employs a restored style categorization logic and consolidated style templates.
- Supports caching of generated presets to avoid duplicates.
- Provides CLI options for generating and applying presets.
- Integrates with the `wall_gen` settings modules for preset management.

### AI Preset Generation Flow Diagram

The following diagram illustrates the process within `ai_prest_gen/ai_preset_generator.py` for creating AI-driven wallpaper presets:

```mermaid
graph TD
    A["Start AI Preset Generation"] --> B{"Base Style Source?"};
    B -- Override --> C["Use Provided Base Style"];
    B -- Interactive --> D{"Input/Generate Style?"};
    D -- "Input Custom" --> E["User Enters Custom Style"];
    D -- "Generate AI Style" --> F["ai_style_generator.generate_random_style"];
    C --> G["Base Style Determined"];
    E --> G;
    F --> G;

    G --> H{"Initialize Gemini API? (if not already)"};
    H -- Success --> I["categorize_style(Base Style)"];
    H -- Fail --> Z_Fail["End: API Init Error"];
    I --> J["Get Template & Instructions for Category"];
    J --> K["Build Detailed Prompt for Gemini AI (to fill template)"];

    K --> L["Attempt Loop (max 3)"];
    L --> M["Call Gemini AI: model.generate_content()"];
    M --> N{"Response OK? (JSON received)"};
    N -- "No / Error / Blocked" --> O{"Max Retries Reached?"};
    O -- Yes --> Z_Fail_Gen["End: Generation Failed"];
    O -- No --> L;

    N -- Yes --> P["Parse JSON Response"];
    P --> Q["Validate & Refine Preset Settings"];
    Q --> R{"is_preset_unique?"};
    R -- No --> O;
    R -- Yes --> S["Show Preset Preview to User (CLI)"];
    S --> T{"User Confirm Save? (CLI)"};
    T -- No --> U["End: User Cancelled Save"];
    T -- Yes --> V["save_preset_to_cache()"];
    V --> W["preset_management.save_preset()"];
    W --> X_Success["End: Preset Saved Successfully"];
```

---

## External Dependencies

- `google-generativeai`: For interacting with Google's Gemini API.
- `requests`: HTTP requests handling.
- `pillow`: Image processing.
- `numpy`: Numerical operations.
- `PyQt5`: GUI components for image preview.
- `tinydb`: Lightweight database for storing presets and history.
- Other utilities: `bleach`, `colorama`, `opencv-python-headless`, `rapidfuzz`, `absl-py`, `clrprint`, `scikit-image`.

---

## Design Philosophy

- **Modularity:** Clear separation of concerns with dedicated packages and modules.
- **Service-Oriented Architecture:** Core services encapsulate distinct functionalities.
- **Extensibility:** Supports user preferences, AI-generated styles, and presets.
- **Cross-Platform Support:** Compatible with multiple OS environments.
- **User Interaction:** CLI-driven with options for preview, testing, and customization.
- **Robustness:** Includes error handling, retry mechanisms, and graceful shutdown.

---

## Other Key Features

### 1. Generation History Management

- Stores generation history in a local SQLite database (`wall_gen/history/history.db`).
- Logs date/time, prompts, AI-enhanced prompts, image filenames, user preferences, and output messages.
- Accessible via CLI commands to review past generations.
- Facilitates recall, debugging, and creative tracking.

### 2. Image Editing Capabilities

- Provides programmatic image manipulation using Pillow, OpenCV, and Scikit-image.
- Supports undo/redo, selection masks, and various filters and adjustments.
- Includes placeholders for advanced AI-based enhancements.

### 3. Cross-Platform Wallpaper Setting

- Detects OS and desktop environment to set wallpaper automatically.
- Supports Windows, macOS, and various Linux desktop environments.
- Uses native APIs or command-line tools for wallpaper application.
- Includes fallback mechanisms for unknown environments.

---

## Summary

This project combines advanced AI capabilities with a well-structured Python codebase to deliver a flexible and powerful wallpaper generation tool. The modular design facilitates maintenance, testing, and future enhancements.

---

*End of Project Overview*
