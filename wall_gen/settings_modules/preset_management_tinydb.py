import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

from tinydb import TinyDB, Query
from tinydb.operations import delete

from rapidfuzz import fuzz

from ui_utils import (
    print_section, print_option, print_success, print_error, print_warning, print_info, get_validated_input,
    print_menu_options, get_menu_choice
)
from file_utils import deep_update
from .settings_manager import get_preferences

DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "presets_db.json")
db = TinyDB(DB_FILE)

def save_preset_tinydb(settings: Dict[str, Any], preset_name: str) -> bool:
    """
    Save a preset to TinyDB. If preset exists, overwrite it.
    """
    try:
        presets_table = db.table('presets')
        existing = presets_table.get(Query().preset_name == preset_name)
        if existing:
            presets_table.update({'settings': settings, 'updated_at': datetime.now().isoformat()}, Query().preset_name == preset_name)
        else:
            presets_table.insert({'preset_name': preset_name, 'settings': settings, 'created_at': datetime.now().isoformat(), 'updated_at': datetime.now().isoformat()})
        return True
    except Exception as e:
        logging.error(f"Error saving preset '{preset_name}' to TinyDB: {e}")
        print_error(f"Error saving preset '{preset_name}' to database.")
        return False

def load_preset_tinydb() -> Optional[Tuple[Dict[str, Any], str]]:
    """
    Display presets from TinyDB and allow user to select one to load.
    Returns settings and preset_name or None.
    """
    presets_table = db.table('presets')
    presets = presets_table.all()
    if not presets:
        print_error("No presets found in database.")
        return None

    print_section("Available Presets (TinyDB)")
    for i, preset in enumerate(presets, 1):
        # Get description, check in multiple possible locations
        desc = preset['settings'].get('metadata', {}).get('description')
        if desc is None:
            # Also check for top-level description in the settings
            desc = preset['settings'].get('description')
        if desc is None:
            desc = 'Description not available'
        created = preset.get('created_at', 'Unknown date')
        
        # Get style information (similar to how we do it in handle_search_load_preset_tinydb)
        styles = []
        if 'preferred_styles' in preset['settings']:
            pref_styles = preset['settings']['preferred_styles']
            if isinstance(pref_styles, str):
                styles.append(pref_styles)
            elif isinstance(pref_styles, list):
                for s in pref_styles:
                    if isinstance(s, str):
                        styles.append(s)
                    elif isinstance(s, dict) and 'name' in s:
                        styles.append(s['name'])
        
        # Format the created date more nicely
        try:
            created_dt = datetime.fromisoformat(created)
            created = created_dt.strftime("%Y-%m-%d %H:%M")
        except (ValueError, TypeError):
            pass  # Keep original format if parsing fails
            
        # Display with style information
        style_info = ""
        if styles:
            style_display = ", ".join(styles[:2])
            if len(styles) > 2:
                style_display += f" (+{len(styles)-2} more)"
            style_info = f" | Styles: {style_display}"
            
        print(f"{i}. {preset['preset_name']} - {desc}{style_info} (Created: {created})")
    print("b. Back")
    choice = get_validated_input(f"Select preset (1-{len(presets)}, b)", [str(i) for i in range(1, len(presets)+1)] + ['b'])
    if choice == 'b':
        return None
    try:
        selected = presets[int(choice)-1]
        return selected['settings'], selected['preset_name']
    except Exception as e:
        print_error(f"Error loading preset: {e}")
        return None

def handle_search_load_preset_tinydb():
    """
    Search presets by name, description, or styles and allow user to select one to load.
    """
    presets_table = db.table('presets')
    presets = presets_table.all()
    if not presets:
        print_error("No presets found in database.")
        return

    search_term = get_validated_input("Enter search term (or 'b' to go back)", allow_empty=True)
    if search_term.lower() == 'b':
        return

    # Filter presets by name, description, or styles (case-insensitive)
    filtered = []
    
    # Split the search term into words for more flexible matching
    search_words = search_term.lower().split()
    
    for preset in presets:
        name = preset['preset_name']
        
        # Get description from both possible locations
        desc = preset['settings'].get('metadata', {}).get('description', '')
        # If not found in metadata, check top-level description
        if not desc and 'description' in preset['settings']:
            desc = preset['settings']['description']
        
        # Get styles from all possible locations
        styles = preset['settings'].get('preferred_styles', [])
        styles_alt = preset['settings'].get('styles', [])
        # Also check 'style' singular key
        style_singular = preset['settings'].get('style', None)
        if style_singular:
            styles_alt = style_singular if styles_alt == [] else styles_alt
        
        # Combine all style sources
        combined_styles = []
        if isinstance(styles, str):
            combined_styles.append(styles)
        elif isinstance(styles, list):
            combined_styles.extend(styles)
        if isinstance(styles_alt, str):
            combined_styles.append(styles_alt)
        elif isinstance(styles_alt, list):
            combined_styles.extend(styles_alt)
            
        # Normalize combined styles to list of strings, handling dicts with 'name' key
        styles_list = []
        for s in combined_styles:
            if isinstance(s, str):
                styles_list.append(s)
            elif isinstance(s, dict) and 'name' in s and isinstance(s['name'], str):
                styles_list.append(s['name'])
            elif isinstance(s, dict):
                # Also check other string values in the dict, explicitly avoiding 'negative_prompts'
                for k, v in s.items():
                    if k == 'negative_prompts':  # Skip 'negative_prompts' key
                        continue
                    if isinstance(v, str):
                        styles_list.append(v)
                    # Also check nested dictionaries (one level deeper)
                    elif isinstance(v, dict):
                        for nested_k, nested_v in v.items(): # Iterate nested dict
                            if nested_k == 'negative_prompts': # Skip in nested too
                                continue
                            if isinstance(nested_v, str):
                                styles_list.append(nested_v)
        
        # Enhanced matching logic with prioritization and fuzzy matching
        matched = False
        search_term_lower = search_term.lower()

        # Priority 1: Full search term in name
        if search_term_lower in name.lower():
            matched = True
        # Priority 2: Full search term in description (if name didn't match)
        elif search_term_lower in desc.lower():
            matched = True
        else:
            # Priority 3: Style matching (more precise first)
            for style_item in styles_list:
                style_item_lower = style_item.lower()

                # 3a: Exact full phrase match in style
                if search_term_lower in style_item_lower:
                    matched = True
                    break
                # 3b: Full phrase match with hyphen/space normalization
                if style_item_lower.replace('-', ' ') == search_term_lower or \
                   style_item_lower.replace(' ', '') == search_term_lower.replace(' ', ''):
                    matched = True
                    break
                
                # 3c: All words from search term must be in the style item (if search term has multiple words)
                if len(search_words) > 1 and all(word in style_item_lower for word in search_words):
                    matched = True
                    break

            # Priority 4: Match all words across multiple style strings (not necessarily in the same string)
            if not matched and len(search_words) > 1:
                # Check if all words appear in the combined styles collectively
                combined_styles_text = " ".join(styles_list).lower()
                if all(word in combined_styles_text for word in search_words):
                    matched = True

            # Priority 5: Fuzzy matching on name and styles (threshold 80)
            if not matched:
                ratio_name = fuzz.partial_ratio(search_term_lower, name.lower())
                if ratio_name >= 80:
                    matched = True
                else:
                    for style_item in styles_list:
                        ratio_style = fuzz.partial_ratio(search_term_lower, style_item.lower())
                        if ratio_style >= 80:
                            matched = True
                            break

        if matched:
            filtered.append(preset)





    if not filtered:
        print_warning("No presets matched your search.")
        input("Press Enter to continue...")
        return

    print_section(f"Search Results for '{search_term}'")
    for i, preset in enumerate(filtered, 1):
        # Extract preset details
        preset_name = preset['preset_name']
        # Get description, check in multiple possible locations
        desc = preset['settings'].get('metadata', {}).get('description')
        if desc is None:
            # Also check for top-level description in the settings
            desc = preset['settings'].get('description')
        if desc is None:
            desc = 'Description not available'
        created = preset.get('created_at', 'Unknown date')
        updated = preset.get('updated_at', created)
        
        # Extract style information (mirroring load_preset_tinydb for consistency)
        styles = []
        # Check 'preferred_styles'
        if 'preferred_styles' in preset['settings']:
            pref_styles_val = preset['settings']['preferred_styles']
            if isinstance(pref_styles_val, str):
                styles.append(pref_styles_val)
            elif isinstance(pref_styles_val, list):
                for s_item in pref_styles_val:
                    if isinstance(s_item, str):
                        styles.append(s_item)
                    elif isinstance(s_item, dict) and 'name' in s_item and isinstance(s_item['name'], str):
                        styles.append(s_item['name'])
        
        # Check 'styles' (plural) as an alternative
        if not styles and 'styles' in preset['settings']:
            styles_alt_val = preset['settings']['styles']
            if isinstance(styles_alt_val, str):
                styles.append(styles_alt_val)
            elif isinstance(styles_alt_val, list):
                for s_item in styles_alt_val:
                    if isinstance(s_item, str):
                        styles.append(s_item)
                    elif isinstance(s_item, dict) and 'name' in s_item and isinstance(s_item['name'], str):
                        styles.append(s_item['name'])

        # Check 'style' (singular) as a further alternative
        if not styles and 'style' in preset['settings']:
            style_singular_val = preset['settings']['style']
            if isinstance(style_singular_val, str):
                styles.append(style_singular_val)
            elif isinstance(style_singular_val, dict) and 'name' in style_singular_val and isinstance(style_singular_val['name'], str):
                styles.append(style_singular_val['name'])
            # Handle case where 'style' might be a list (less common but possible)
            elif isinstance(style_singular_val, list):
                 for s_item in style_singular_val:
                    if isinstance(s_item, str):
                        styles.append(s_item)
                    elif isinstance(s_item, dict) and 'name' in s_item and isinstance(s_item['name'], str):
                        styles.append(s_item['name'])
        
        # Extract genre information
        genres = []
        if 'preferred_genres' in preset['settings']:
            pref_genres = preset['settings']['preferred_genres']
            if isinstance(pref_genres, str):
                genres.append(pref_genres)
            elif isinstance(pref_genres, list):
                for g in pref_genres:
                    if isinstance(g, str):
                        genres.append(g)
        
        # Format the created date more nicely if possible
        try:
            created_dt = datetime.fromisoformat(created)
            created = created_dt.strftime("%Y-%m-%d %H:%M")
        except (ValueError, TypeError):
            pass  # Keep original format if parsing fails
            
        # Display preset in a structured format
        print_info(f"\n{i}. {preset_name}")
        print_info(f"   Description: {desc}")
        print_info(f"   Created: {created}")
        
        # Display styles if available
        if styles:
            styles_str = ", ".join(styles[:3])
            if len(styles) > 3:
                styles_str += f" (+{len(styles) - 3} more)"
            print_info(f"   Styles: {styles_str}")
            
        # Display genres if available
        if genres:
            genres_str = ", ".join(genres[:3])
            if len(genres) > 3:
                genres_str += f" (+{len(genres) - 3} more)"
            print_info(f"   Genres: {genres_str}")
        
        # Add a separator between presets for better readability
        if i < len(filtered):
            print("   " + "-" * 40)
    
    print("\nb. Back")
    choice = get_validated_input(f"Select preset (1-{len(filtered)}, b)", [str(i) for i in range(1, len(filtered)+1)] + ['b'])
    if choice == 'b':
        return

    try:
        selected = filtered[int(choice)-1]
        settings = selected['settings']
        preset_name = selected['preset_name']

        # Apply preset settings
        user_prefs = get_preferences()
        print_section("Load Settings")
        load_options = ["Replace current settings with preset", "Merge preset with current settings"]
        print_menu_options([(str(i+1), option) for i, option in enumerate(load_options)])
        valid_choices = ["b"] + [str(i+1) for i in range(len(load_options))]
        load_choice = get_menu_choice(f"Select option (1-{len(load_options)}, b)", valid_choices)
        if load_choice == "_INTERRUPTED_":
            return
        if load_choice == "b":
            return
        if load_choice == "1":
            if apply_preset_settings(settings, replace=True):
                print_success("Settings replaced with preset")
            else:
                print_error("Failed to apply preset settings (replace)")
                return
        elif load_choice == "2":
            if apply_preset_settings(settings, replace=False):
                print_success("Settings merged with preset")
            else:
                print_error("Failed to apply preset settings (merge)")
                return

        user_prefs.last_preset = preset_name
        user_prefs.save_preferences()
    except Exception as e:
        print_error(f"Error loading preset: {e}")
        logging.exception("Error in handle_search_load_preset_tinydb")




def delete_preset_tinydb() -> Optional[str]:
    """
    Delete a preset from TinyDB.
    Returns the name of deleted preset or None.
    """
    presets_table = db.table('presets')
    presets = presets_table.all()
    if not presets:
        print_warning("No saved presets found to delete")
        input("Press Enter to continue...")
        return None

    print_section("Available Presets to Delete (TinyDB)")
    for i, preset in enumerate(presets, 1):
        print_option(str(i), preset['preset_name'])
    print_option("b", "Back")

    valid_choices = ["b"] + [str(i) for i in range(1, len(presets)+1)]
    choice = get_validated_input("Select preset to delete", valid_choices)
    if choice == "b":
        return None

    preset = presets[int(choice)-1]
    preset_name = preset['preset_name']
    confirm = get_validated_input(f"Are you sure you want to delete preset '{preset_name}'? (y/n)", ["y", "n"])
    if confirm.lower() == "y":
        try:
            presets_table.remove(Query().preset_name == preset_name)
            print_success(f"Preset '{preset_name}' deleted")
            return preset_name
        except Exception as e:
            print_error(f"Error deleting preset: {e}")
            return None
    else:
        print_info("Deletion cancelled")
        return None

def handle_delete_preset_tinydb():
    """
    Wrapper to delete preset and update user preferences if needed.
    """
    user_prefs = get_preferences()
    current_preset = getattr(user_prefs, 'last_preset', None)
    deleted_preset = delete_preset_tinydb()
    if deleted_preset and current_preset == deleted_preset:
        user_prefs.last_preset = None
        user_prefs.save_preferences()

def view_preset_details_tinydb():
    """
    Display details of the currently loaded preset.
    """
    user_prefs = get_preferences()
    current_preset = getattr(user_prefs, 'last_preset', None)
    if not current_preset:
        print_warning("No preset currently loaded")
        input("\nPress Enter to continue...")
        return
    presets_table = db.table('presets')
    preset = presets_table.get(Query().preset_name == current_preset)
    if not preset:
        print_error(f"Preset '{current_preset}' not found in database.")
        user_prefs.last_preset = None
        user_prefs.save_preferences()
        return
    settings = preset.get('settings', {})
    print_section(f"Preset Details: {current_preset}")

    def _display_section(settings, section, title, indent=0):
        if section not in settings:
            return
        data = settings.get(section)
        if data is None:
            return
        print_info(f"\n{'  ' * indent}{title}:")
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, dict):
                    _display_section({k: v}, k, k, indent + 1)
                elif isinstance(v, list):
                    print_info(f"{'  ' * (indent + 1)}{k}:")
                    if v:
                        for item in v:
                            print_info(f"{'  ' * (indent + 2)}- {item}")
                    else:
                        print_info(f"{'  ' * (indent + 2)}<empty>")
                else:
                    print_info(f"{'  ' * (indent + 1)}{k}: {v}")
        elif isinstance(data, list):
            if data:
                for item in data:
                    print_info(f"{'  ' * (indent + 1)}- {item}")
            else:
                print_info(f"{'  ' * (indent + 1)}<empty>")
        else:
            print_info(f"{'  ' * (indent + 1)}{data}")

    _display_section(settings, "metadata", "Metadata")
    _display_section(settings, "imagen_settings", "Imagen Settings")
    _display_section(settings, "wallpaper_settings", "Wallpaper Settings")
    _display_section(settings, "preferred_genres", "Preferred Genres")
    _display_section(settings, "preferred_styles", "Preferred Styles")
    _display_section(settings, "preferred_moods", "Preferred Moods")
    _display_section(settings, "negative_prompts", "Negative Prompts")
    if "aspect_ratio" in settings:
        _display_section(settings, "aspect_ratio", "Aspect Ratio")
    input("\nPress Enter to continue...")

def apply_preset_settings(settings: Dict[str, Any], replace: bool = True) -> bool:
    """
    Apply preset settings to user preferences.
    """
    user_prefs = get_preferences()
    try:
        from .preset_management import _apply_preset_settings as apply_settings
        return apply_settings(settings, replace)
    except ImportError:
        return False


def manage_presets_tinydb():
    """
    Manage presets menu for TinyDB presets.
    Provides options to load, search/load, delete, view details, and return.
    """
    while True:
        print_section("Manage Presets (TinyDB)")
        menu_options = [
            ("1", "Load Preset"),
            ("2", "Search and Load Preset"),
            ("3", "Delete Preset"),
            ("4", "View Preset Details"),
            ("b", "Back"),
        ]
        print_menu_options(menu_options)
        choice = get_validated_input("Select option (1-4, b)", ["1", "2", "3", "4", "b"])
        if choice == "b":
            break
        elif choice == "1":
            result = load_preset_tinydb()
            if result is None:
                continue
            settings, preset_name = result
            if apply_preset_settings(settings, replace=True):
                print_success(f"Preset '{preset_name}' loaded and applied.")
            else:
                print_warning(f"Failed to apply preset '{preset_name}'.")
        elif choice == "2":
            handle_search_load_preset_tinydb()
        elif choice == "3":
            handle_delete_preset_tinydb()
        elif choice == "4":
            view_preset_details_tinydb()
