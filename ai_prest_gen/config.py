# ai_prest_gen/config.py
"""
Configuration constants for the AI Preset Generator module.
"""
import os
from pathlib import Path

# Base directory of the ai_prest_gen module
# This assumes config.py is in the root of ai_prest_gen
AI_PREST_GEN_DIR = Path(__file__).resolve().parent

# Path to the catalog_data directory within ai_prest_gen
CATALOG_DATA_PATH = AI_PREST_GEN_DIR / "catalog_data"

# --- File Names and Directory Names ---
LOG_FILE_NAME = "ai_preset_generator.log"
PRESETS_CACHE_FILE_NAME = "generated_presets_cache.json"
PRESETS_DIR_NAME = "presets"

MAX_GENERATION_ATTEMPTS = 3
# --- Directory Paths ---
# The PRESETS_DIR is often created relative to the current working directory
# of the main script that calls the generator.
# If ai_preset_generator.py is run directly, it will be in its CWD.
# If imported, the main application (wall_gen) might define a global presets directory.
# For now, this module will assume PRESETS_DIR_NAME is relative to the CWD
# where preset operations (like saving) are performed.
# The main script (ai_preset_generator.py) will handle os.makedirs(PRESETS_DIR_NAME).

# Path for the log file, typically within the ai_prest_gen module directory or a dedicated logs folder
# For simplicity, placing it alongside the cache file if one were to be module-local.
# However, ai_preset_generator.py currently creates LOG_FILE_NAME in its CWD.
# Let's keep it as a name and let the main script decide the full path.

# Path for the cache file, typically within the ai_prest_gen module directory or a user data folder.
# ai_preset_generator.py currently creates PRESETS_CACHE_FILE in its CWD.
# Let's keep it as a name and let the main script decide the full path.

# Note: Actual full paths for PRESETS_DIR, LOG_FILE, and PRESETS_CACHE_FILE
# will be constructed in ai_preset_generator.py or other modules that use them,
# often relative to the current working directory or a project root.
# This config file primarily provides the *names*.