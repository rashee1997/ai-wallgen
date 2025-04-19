import os
import google.generativeai as genai
from wallpaper_settings import get_preferences
import sys  

# Global variable to track if Gemini is initialized
gemini_initialized = False

# Attempt to get GEMINI_API_KEY from environment and configure Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_initialized = True
else:
    print("Warning: GEMINI_API_KEY environment variable not set. AI style generation will not work.")

def initialize_gemini(api_key: str):
    """
    Initialize the Gemini model with the provided API key.
    """
    global gemini_initialized
    genai.configure(api_key=api_key)
    gemini_initialized = True

def generate_style_prompt():
    """
    Generate a prompt instructing Gemini to create a random artistic style
    for AI image generation. The prompt guides Gemini to produce a style description
    that can be used as a style modifier in image generation.
    """
    prompt = (
        "You are an expert AI art style generator. "
        "Generate a single cohesive artistic style description that represents ONE clear visual concept. "
        "The style must be simple and focused, avoiding multiple descriptive elements or comma-separated concepts. "
        "Example good response: 'vibrant cyberpunk neon' "
        "Example bad response: 'dark gothic, medieval architecture, with misty atmosphere' "
        "Focus on ONE primary visual style without combining multiple themes or elements. "
        "Keep it concise and avoid any additional explanations or variations."
    )
    return prompt

def generate_random_style():
    """
    Use Gemini to generate a random style based on the style prompt.
    Returns the generated style string or None if generation failed.
    """
    if not gemini_initialized:
        raise RuntimeError("Gemini model is not initialized. Please initialize with your API key first.")
    
    prompt = generate_style_prompt()
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.5-pro-exp-03-25")  # Correct model name as per feedback
        response = model.generate_content(prompt)
        
        if response and hasattr(response, 'text') and response.text:
            style_text = response.text.strip()
        elif response and hasattr(response, 'candidates') and response.candidates:
            style_text = response.candidates[0].content.parts[0].text.strip()
        else:
            style_text = None
        
        if style_text:
            # Clean up style text if needed (remove quotes or newlines)
            style_text = style_text.strip(' "\'\n\r')
            return style_text
        else:
            print("No style text returned from Gemini response.")
            return None
    except Exception as e:
        print(f"Error generating style with Gemini: {e}")
        return None

def handle_style_generation(user_prefs):
    """
    Interactive handler to generate AI styles and ask user to save them.
    Provides a 'next' option to generate another style or exit.
    """
    from ui_utils import print_section, print_info, print_success, print_warning, get_validated_input
    
    if not gemini_initialized:
        print_warning("Gemini model is not initialized. Please ensure GEMINI_API_KEY environment variable is set.")
        return
    
    # Removed try block as KeyboardInterrupt is handled globally
    while True:
        print_section("AI Style Generation")
        print_info("Generating AI style...")
        style = generate_random_style()
        if style is None:
            print_warning("Failed to generate style. Please try again later.")
            return
        
        print_info(f"Generated AI Style:\n  {style}")
        
        save_choice = get_validated_input("Save this style to your preferences? (y/n/q)", ["y", "n", "q"])
        if save_choice == "y":
            if style not in user_prefs.preferred_styles:
                user_prefs.preferred_styles.append(style)
                user_prefs.save_preferences()
                print_success(f"Style '{style}' saved to your preferences.")
            else:
                print_warning("This style is already in your preferences.")
        elif save_choice == "q":
            print_info("Exiting AI style generator.")
            break
        
        next_choice = get_validated_input("Generate next style? (y/n)", ["y", "n"])
        if next_choice != "y":
            print_info("Exiting AI style generator.")
            break
    # Removed KeyboardInterrupt handler; global handler in graceful_exit.py will manage exit.

def main():
    """
    Main entry point for CLI usage of the AI style generator.
    """
    import argparse
    from wallpaper_settings import initialize_settings, get_preferences

    # Initialize settings first
    user_prefs = initialize_settings()

    parser = argparse.ArgumentParser(description='Generate an AI art style description')
    parser.add_argument('--key', help='Gemini API key (optional if set via environment variable)')
    parser.add_argument('--save', action='store_true', help='Automatically save the generated style to preferences')
    
    args = parser.parse_args()
    
    # Initialize Gemini if API key is provided via CLI
    if args.key:
        initialize_gemini(args.key)
    
    # Get user preferences for saving styles
    user_prefs = get_preferences()
    
    try:
        # Generate a style
        style = generate_random_style()
        if style:
            print(f"Generated style: {style}")
            
            # Save if --save flag is used
            if args.save:
                # Replace existing style with new one
                user_prefs.add_style(style)
                print(f"Style saved to preferences")
        else:
            print("Failed to generate style", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
