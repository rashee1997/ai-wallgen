# settings_modules/menu_management/genres_menu.py

from typing import List, Tuple
from ui_utils import (
    print_header, print_section, print_option, print_info, print_prompt,
    print_success, print_warning, print_error, get_validated_input
)
from config import available_genres
from ..settings_manager import get_preferences

def manage_genres():
    """Manage user's preferred genres for wallpaper generation."""
    user_prefs = get_preferences()
    while True:
        print_header("Manage Genres")
        print_section("Current Preferred Genres")
        
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
        
        choice = get_validated_input("\nEnter your choice (1-3, b): ", ["1", "2", "3", "b"])
        if choice == "_INTERRUPTED_":
            return # Exit genre management

        if choice == "b":
            return
            
        if choice == "1":
            print_prompt("\nEnter the number of the genre to add (or 'b' to go back): ")
            genre_choice = input().strip().lower()
            
            if genre_choice == 'b':
                continue
            
            try:
                genre_index = int(genre_choice) - 1
                if 0 <= genre_index < len(available_genres):
                    genre = available_genres[genre_index]
                    if genre not in user_prefs.preferred_genres:
                        user_prefs.add_genre(genre)
                        print_success(f"\nAdded '{genre}' to preferred genres.")
                    else:
                        print_warning(f"\n'{genre}' is already in your preferred genres.")
                else:
                    print_error("\nInvalid genre number.")
            except ValueError:
                print_error("\nPlease enter a valid number.")
        
        elif choice == "2":
            if not user_prefs.preferred_genres:
                print_warning("\nNo genres to remove.")
                continue
            
            print_prompt("\nEnter the number of the genre to remove (or 'b' to go back): ")
            genre_choice = input().strip().lower()
            
            if genre_choice == 'b':
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
            
            print_warning("\nAre you sure you want to clear all preferred genres? (y/n): ")
            if input().strip().lower() == 'y':
                user_prefs.preferred_genres.clear()
                user_prefs.save_preferences()
                print_success("\nCleared all preferred genres.")
        
        elif choice == "b":
            return
