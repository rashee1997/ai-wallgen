# Updated import
from wall_gen.ui_utils import (
    print_section,
    print_option,
    print_info,
    print_success,
    print_error,
    get_validated_input,
)
from ..settings_manager import get_preferences # Relative import is correct


def manage_moods():
    """Manage user's preferred moods for wallpaper generation."""
    user_prefs = get_preferences()
    while True:
        print_section("Manage Moods")
        print_info("Current preferred moods:")
        for mood in user_prefs.preferred_moods:
            print_info(f"- {mood}")

        print_info("\nAvailable moods:")
        mood_options = [
            "peaceful",
            "dramatic",
            "mysterious",
            "energetic",
            "melancholic",
            "joyful",
            "romantic",
            "eerie",
            "nostalgic",
            "contemplative",
        ]
        for i, mood in enumerate(mood_options, 1):
            print_option(str(i), mood)

        print_option("b", "Back")

        action = get_validated_input(
            f"Select mood (1-{len(mood_options)}, b)",
            ["b"] + [str(i) for i in range(1, len(mood_options) + 1)],
        )
        if action == "_INTERRUPTED_":
            continue  # Go back to the Manage Moods menu loop

        if action == "b":
            return

        # Action is a number corresponding to a mood
        idx = int(action) - 1
        if 0 <= idx < len(mood_options):
            mood = mood_options[idx]
            # Use add_mood to replace the existing mood
            user_prefs.add_mood(mood)
            print_success(f"Set preferred mood to: {mood}")
            # add_mood already calls save_preferences, no need to call it again here
        else:
            # This case should ideally not be reached due to get_validated_input
            print_error("Invalid selection.")
