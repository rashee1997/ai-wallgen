# ai_prest_gen/preset_cache_manager.py
"""
Manages the caching of generated preset hashes to avoid duplicates.
"""
import os
import json
import hashlib
import logging
from typing import List, Dict, Any

class PresetCacheManager:
    """
    Handles loading, saving, and checking uniqueness of presets against a cache file.
    """
    def __init__(self, cache_file_name: str, max_cache_size: int = 50):
        """
        Initializes the PresetCacheManager.

        Args:
            cache_file_name (str): The name of the cache file.
                                   The actual path might be CWD-relative.
            max_cache_size (int): Maximum number of preset hashes to keep in the cache.
        """
        self.cache_file_path = cache_file_name # Assumes CWD or pre-defined path by caller
        self.max_cache_size = max_cache_size
        self.logger = logging.getLogger(__name__)

    def _calculate_preset_hash(self, preset_data: Dict[str, Any]) -> str:
        """Calculates an MD5 hash for the given preset data."""
        # Ensure "styles" is a list for consistent hashing if it exists
        # This mutable operation should be done on a copy if preset_data is to be preserved outside
        # For now, assuming this is acceptable as it mirrors original logic.
        # A more robust approach might involve deepcopying preset_data before modification.
        data_to_hash = preset_data.copy() # Work on a copy
        if "styles" in data_to_hash and not isinstance(data_to_hash["styles"], list):
            data_to_hash["styles"] = [data_to_hash["styles"]]
        return hashlib.md5(json.dumps(data_to_hash, sort_keys=True).encode()).hexdigest()

    def load_cached_presets(self) -> List[str]:
        """Loads previously generated preset hashes from the cache file."""
        if os.path.exists(self.cache_file_path):
            try:
                with open(self.cache_file_path, 'r') as f:
                    content = json.load(f)
                    return content if isinstance(content, list) else []
            except (json.JSONDecodeError, IOError) as e:
                self.logger.error(f"Error loading presets cache '{self.cache_file_path}': {e}")
        return []

    def save_preset_hash_to_cache(self, preset_data: Dict[str, Any]) -> None:
        """
        Calculates a preset hash and saves it to the cache file if it's new.
        Manages cache size.
        """
        try:
            preset_hash = self._calculate_preset_hash(preset_data)
            cached_presets = self.load_cached_presets()

            if preset_hash not in cached_presets:
                cached_presets.append(preset_hash)
                if len(cached_presets) > self.max_cache_size:
                    cached_presets = cached_presets[-self.max_cache_size:]
                
                try:
                    with open(self.cache_file_path, 'w') as f:
                        json.dump(cached_presets, f)
                except IOError as e:
                    self.logger.error(f"Error writing to presets cache '{self.cache_file_path}': {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error in save_preset_hash_to_cache: {e}", exc_info=True)

    def is_preset_unique(self, preset_data: Dict[str, Any]) -> bool:
        """Checks if a preset is unique compared to previously generated ones."""
        try:
            preset_hash = self._calculate_preset_hash(preset_data)
            cached_presets = self.load_cached_presets()
            return preset_hash not in cached_presets
        except Exception as e:
            self.logger.error(f"Error checking preset uniqueness: {e}", exc_info=True)
            return True # Fallback to assuming unique to avoid blocking generation