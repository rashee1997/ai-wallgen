# wall_gen/cache_utils.py
"""
Utilities for caching mechanisms and directory initialization.
NOTE: This module uses absolute imports assuming it's part of the 'wall_gen' package.
It may not run correctly as a standalone script without sys.path adjustments.
"""

import collections
import logging
import os

# --- LRU Cache Implementation ---

class LRUCache(collections.OrderedDict):
    """
    Simple Least Recently Used (LRU) Cache implementation based on OrderedDict.
    (Moved from wallpaper_generator.py)
    """
    def __init__(self, capacity=100):
        super().__init__()
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("LRUCache capacity must be a positive integer.")
        self.capacity = capacity
        logging.info(f"LRUCache initialized with capacity: {self.capacity}")

    def __getitem__(self, key):
        """Get item and mark it as recently used."""
        try:
            value = super().__getitem__(key)
            self.move_to_end(key)
            logging.debug(f"Cache hit for key: {str(key)[:50]}...")
            return value
        except KeyError:
            logging.debug(f"Cache miss for key: {str(key)[:50]}...")
            raise # Re-raise KeyError as expected

    def __setitem__(self, key, value):
        """Set item, removing the oldest if capacity is exceeded."""
        if key in self:
            # Move existing key to the end to mark as recently used
            self.move_to_end(key)
        super().__setitem__(key, value)
        # Check if capacity is exceeded after adding/updating
        if len(self) > self.capacity:
            oldest_key = next(iter(self))
            logging.info(f"Cache capacity ({self.capacity}) exceeded. Evicting oldest entry: {str(oldest_key)[:50]}...")
            del self[oldest_key]

    def get(self, key, default=None):
        """Get item with a default value if key is not found."""
        try:
            return self[key]
        except KeyError:
            return default

# --- Prompt Cache Instance ---

# Instantiate the prompt cache for use by prompt_service
# The capacity can be made configurable later if needed
prompt_cache = LRUCache(capacity=100)
logging.info("Prompt cache (LRUCache) instantiated.")


# --- Cache Directory Initialization ---

def initialize_cache_directories(project_root_dir: str, dir_names: list = ["cache", "genimage"]):
    """
    Ensures that specified cache directories exist within the project root.
    (New function as per plan)

    Args:
        project_root_dir (str): Absolute path to the project's root directory.
        dir_names (list): A list of directory names to create under the root.
    """
    if not os.path.isdir(project_root_dir):
        logging.error(f"Project root directory not found: {project_root_dir}. Cannot initialize cache directories.")
        return

    logging.info(f"Initializing cache directories in: {project_root_dir}")
    for dir_name in dir_names:
        dir_path = os.path.join(project_root_dir, dir_name)
        try:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
                logging.info(f"Created cache directory: {dir_path}")
            elif not os.path.isdir(dir_path):
                logging.error(f"Path exists but is not a directory: {dir_path}. Cannot create cache directory.")
            else:
                logging.debug(f"Cache directory already exists: {dir_path}")
        except OSError as e:
            logging.error(f"Error creating cache directory '{dir_path}': {e}")
        except Exception as e:
            logging.error(f"Unexpected error creating cache directory '{dir_path}': {e}", exc_info=True)

if __name__ == '__main__':
    # Example usage for testing
    logging.basicConfig(level=logging.DEBUG)
    
    # Test LRUCache
    cache = LRUCache(capacity=2)
    cache['a'] = 1
    cache['b'] = 2
    print(f"Cache state 1: {cache}")
    cache['c'] = 3 # Should evict 'a'
    print(f"Cache state 2: {cache}")
    _ = cache['b'] # Access 'b', making it most recent
    print(f"Cache state 3: {cache}")
    cache['d'] = 4 # Should evict 'c'
    print(f"Cache state 4: {cache}")

    # Test directory initialization (creates dirs in current dir if run standalone)
    test_root = os.path.abspath(".")
    print(f"\nTesting directory initialization in: {test_root}")
    initialize_cache_directories(test_root, ["test_cache_dir1", "test_cache_dir2"])
    # Clean up test dirs if needed
    # import shutil
    # if os.path.exists("test_cache_dir1"): shutil.rmtree("test_cache_dir1")
    # if os.path.exists("test_cache_dir2"): shutil.rmtree("test_cache_dir2")
