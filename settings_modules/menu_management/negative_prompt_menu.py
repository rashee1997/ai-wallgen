from ui_utils import (
    print_section,
    print_option,
    print_info,
    print_success,
    print_warning,
    get_validated_input,
)
from ..settings_manager import get_preferences


def manage_negative_prompt():
    """Manage negative prompt settings."""
    user_prefs = get_preferences()
    while True:
        print_section("Negative Prompt Settings")
        print_info("Negative prompts tell the AI what NOT to include in the image.")

        current_negative = user_prefs.imagen_settings.get("negative_prompt", "")
        print_info(
            f"Current negative prompt: {current_negative if current_negative else 'None'}"
        )

        print_option("1", "Set Custom Negative Prompt")
        print_option("2", "Use Default Negative Prompt")
        print_option("3", "Clear Negative Prompt")
        print_option("b", "Back")

        choice = get_validated_input("Select option (1-3, b)", ["1", "2", "3", "b"])
        if choice == "_INTERRUPTED_":
            return

        if choice == "b":
            return

        if choice == "1":
            print_info(
                "Enter your custom negative prompt (what you want to avoid in the image):"
            )
            custom_negative = input("> ").strip()

            if custom_negative:
                user_prefs.imagen_settings["negative_prompt"] = custom_negative
                print_success("Custom negative prompt set successfully.")
            else:
                print_warning("Empty input. Negative prompt not changed.")

        elif choice == "2":
            default_negative = "ugly, disfigured, low quality, blurry, nsfw, watermark, signature, out of frame, extra limbs, poorly drawn face, twisted limbs, distorted face, bad proportions, bad anatomy"
            user_prefs.imagen_settings["negative_prompt"] = default_negative
            print_success("Default negative prompt set successfully.")

        elif choice == "3":
            user_prefs.imagen_settings["negative_prompt"] = ""
            print_success("Negative prompt cleared.")

        user_prefs.save_preferences()
