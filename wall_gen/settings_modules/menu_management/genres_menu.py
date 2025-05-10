# settings_modules/menu_management/genres_menu.py

from typing import List, Tuple
# Updated imports
from wall_gen.ui_utils import (
    print_header,
    print_section,
    print_option,
    print_info,
    # print_prompt, # Removed, use get_interactive_input or get_confirmation
    print_success,
    print_warning,
    print_error,
    get_validated_input,
    get_interactive_input, # Added
    get_confirmation,    # Added
    clear_screen, # Added
)
# Updated imports
from wall_gen.config import available_genres
from ..settings_manager import get_preferences # Relative import is correct


def manage_genres():
    """Manage user's preferred genres for wallpaper generation."""
    user_prefs = get_preferences()
    while True:
        clear_screen()
        print_header("Manage Genres")
        # print_section("Current Preferred Genres") # Header is sufficient
        print_info("\nYour Preferred Genres:") # More descriptive

        if not user_prefs.preferred_genres:
            print_info("No preferred genres set yet.")
        else:
            for i, genre in enumerate(user_prefs.preferred_genres, 1):
                print_option(str(i), genre)

        print_section("Available Genres")
        for i, genre in enumerate(available_genres, 1):
            print_option(str(i), genre)

        print_section("Options")
        print_option("1", "Add genre")
        print_option("2", "Remove genre")
        print_option("3", "Clear all genres")
        print_option("b", "Back")

        choice = get_validated_input(
            prompt="\nEnter your choice", 
            options=["1", "2", "3", "b"],
            help_context_id="GENRES_MENU"
        )
        if choice == "_HELP_SHOWN_":
            continue
        if choice == "_INTERRUPTED_":
            return  # Exit genre management

        if choice == "b":
            return

        if choice == "1":
            genre_choice = get_interactive_input("\nEnter the number of the genre to add (or 'b' to go back): ").lower()

            if genre_choice == "b":
                continue

            try:
                genre_index = int(genre_choice) - 1
                if 0 <= genre_index < len(available_genres):
                    genre = available_genres[genre_index]
                    if genre not in user_prefs.preferred_genres:
                        user_prefs.add_genre(genre)
                        print_success(f"\nAdded '{genre}' to preferred genres.")
                    else:
                        print_warning(
                            f"\n'{genre}' is already in your preferred genres."
                        )
                else:
                    print_error("\nInvalid genre number.")
            except ValueError:
                print_error("\nPlease enter a valid number.")

        elif choice == "2":
            if not user_prefs.preferred_genres:
                print_warning("\nNo genres to remove.")
                continue

            genre_choice = get_interactive_input(
                "\nEnter the number of the genre to remove (or 'b' to go back): "
            ).lower()

            if genre_choice == "b":
                continue

            try:
                genre_index = int(genre_choice) - 1
                if 0 <= genre_index < len(user_prefs.preferred_genres):
                    removed_genre = user_prefs.preferred_genres.pop(genre_index)
                    user_prefs.save_preferences()
                    print_success(f"\nRemoved '{removed_genre}' from preferred genres.")
                else:
                    print_error("\nInvalid genre number.")
            except ValueError:
                print_error("\nPlease enter a valid number.")

        elif choice == "3":
            if not user_prefs.preferred_genres:
                print_warning("\nNo genres to clear.")
                continue

            print_warning( # This is now a Rich print_warning
                "\nAre you sure you want to clear all preferred genres? This cannot be undone."
            ) # (y/n) part removed as get_confirmation handles it
            if get_confirmation("Clear all preferred genres?", default=False): # Default to No for safety
                user_prefs.preferred_genres.clear()
                user_prefs.save_preferences()
                print_success("\nCleared all preferred genres.")

        elif choice == "b":
            return
