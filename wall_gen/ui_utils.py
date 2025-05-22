# clrprint library setup removed as all UI functions now use Rich.

import os
import sys
import time
import threading
import textwrap
from typing import List, Optional

# --- Rich library imports and console instance ---
from rich.console import Console
from rich.text import Text
from rich.style import Style
from rich.panel import Panel
from rich.rule import Rule
from rich.status import Status
from rich.prompt import Prompt, Confirm
from rich.padding import Padding # Added for help panel

console = Console()

# --- Rich Progress Bar setup ---
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TaskID
_current_progress_bar: Optional[Progress] = None
_current_progress_task_id: Optional[TaskID] = None
# --- End Rich library setup ---

def print_header(text: str) -> None:
    """
    Print a formatted and feature-rich header using Rich Rules and Text for all headers.
    """
    # Apply a consistent feature-rich style to all headers
    header_text_str = f"🌟 {text} 🌟"  # Generic decoration
    rule_char = "─"  # BOX DRAWINGS LIGHT HORIZONTAL - consistent rule character
    header_style = "bold yellow"  # Consistent style for the header text
    rule_style = "yellow"  # Consistent style for the rule lines

    header_text = Text(header_text_str, justify="center", style=header_style)
    
    console.print() 
    console.print(Rule(style=rule_style, characters=rule_char)) 
    console.print(header_text) 
    console.print(Rule(style=rule_style, characters=rule_char)) 
    console.print()

def print_section(title: str) -> None: # Parameter renamed from text to title for clarity
    """
    Print a formatted section title using Rich Rule.
    """
    console.print() # Preserves the initial newline from the original implementation
    console.print(Rule(f"[bold bright_green]{title}[/bold bright_green]", style="green"))
    # console.print() by default adds a newline, so the behavior of ending with a newline is preserved.

def print_option(key: str, description: str, shortcut: Optional[str] = None) -> None:
    """
    Print a menu option with its key, description, and optional keyboard shortcut using Rich.
    """
    option_text = Text("  ") # Indentation
    option_text.append(f"{key}: ", style="yellow") # Key in yellow
    if shortcut:
        option_text.append(f"[{shortcut}] ", style="magenta") # Shortcut in magenta
    option_text.append(description) # Description in default style
    console.print(option_text)

def print_success(text: str, timestamp: bool = False) -> None:
    """
    Print a success message using Rich, optionally with a timestamp.
    """
    message_parts = []
    if timestamp:
        message_parts.append(Text(f"{time.strftime('%H:%M:%S')} ", style="dim"))

    message_parts.append(Text("✅  ", style="green")) # Added extra space
    message_parts.append(Text(text, style="green"))

    console.print(Text.assemble(*message_parts))

def print_error(text: str, timestamp: bool = False) -> None:
    """
    Print an error message using Rich, optionally with a timestamp.
    """
    message_parts = []
    if timestamp:
        message_parts.append(Text(f"{time.strftime('%H:%M:%S')} ", style="dim"))

    message_parts.append(Text("❌  ", style="bold red")) # Added extra space
    message_parts.append(Text(text, style="bold red"))

    console.print(Text.assemble(*message_parts))

def print_warning(text: str, timestamp: bool = False) -> None:
    """
    Print a warning message using Rich, optionally with a timestamp.
    """
    message_parts = []
    if timestamp:
        message_parts.append(Text(f"{time.strftime('%H:%M:%S')} ", style="dim"))

    message_parts.append(Text("⚠️  ", style="yellow")) # Added extra space
    message_parts.append(Text(text, style="yellow")) # Styling the message text as well

    console.print(Text.assemble(*message_parts))

def print_info(text: str, timestamp: bool = False) -> None:
    """
    Print an informational message using Rich, optionally with a timestamp.
    """
    if not text or text.strip() == "": # Check if text is None, empty, or just whitespace
        console.print("[bold red on yellow]!!!! DEBUG: print_info called with effectively empty text !!!![/bold red on yellow]", locals())
        # import traceback
        # traceback.print_stack(file=sys.stderr) # Alternative to raising for call stack
        # Forcing a more visible marker for now.
        # If this marker appears, we've found the culprit's timing.

    message_parts = []
    if timestamp:
        message_parts.append(Text(f"{time.strftime('%H:%M:%S')} ", style="dim"))

    message_parts.append(Text("ℹ  ", style="blue")) # Added extra space, Using U+2139 INFO symbol
    message_parts.append(Text(text))

    console.print(Text.assemble(*message_parts))

# Function print_prompt removed as its functionality is incorporated into Rich-based input functions.

try:
    from .help_content import get_help_text, HelpSection # For contextual help and help structure
except ImportError:
    # Fallback if help_content is not found, to prevent crashes during development/testing
    def get_help_text(context_id: str) -> str:
        # In a real scenario, might log this warning
        # print_warning(f"Warning: help_content.py not found or get_help_text failed for context: {context_id}")
        return "Help system component (help_content.py) not found."
    
    # Dummy HelpSection class if original can't be imported
    class HelpSection:
        def __init__(self, title: str, content: str, icon: Optional[str] = None):
            self.title = title
            self.content = content
            self.icon = icon or "📌"

def get_interactive_input(prompt_text: str) -> str:
    """
    Get user input interactively using Rich Prompt.
    Allows empty input, similar to input().strip().
    (This function might become less used as get_validated_input and get_confirmation directly use Rich prompts)
    """
    # Construct the prompt text with the ">" prefix and desired style to mimic original print_prompt
    # The original print_prompt used magenta for "> {text}"
    styled_prompt_text = Text.assemble(Text("> ", style="magenta"), Text(prompt_text, style="magenta"))
    # To allow empty input (like raw input()), set default="" for Prompt.ask.
    # Prompt.ask will return this default if the user just presses Enter.
    return Prompt.ask(styled_prompt_text, default="").strip()

def get_validated_input(
    prompt: str, 
    options: Optional[List[str]] = None,
    default: Optional[str] = None, 
    allow_empty: bool = False,
    help_context_id: Optional[str] = None # New parameter for contextual help
) -> str:
    """
    Get and validate user input using Rich Prompt, with integrated help.
    """
    effective_default = default
    if default is None and allow_empty and not options: # Rich handles default with choices differently
        effective_default = ""
    
    should_show_default_in_prompt = bool(default is not None)
    
    prompt_suffix = ""
    if help_context_id:
        prompt_suffix = " (type 'h' or '?' for help)"

    while True:
        full_prompt_text = f"{prompt}{prompt_suffix}"
        
        # Using Rich Prompt.ask for input.
        # We will check for 'h' or '?' before Rich's own choice validation if options are provided.
        raw_user_input = Prompt.ask(
            full_prompt_text,
            choices=None, # We handle choice validation manually after help check to allow 'h','?'
            default=effective_default if not options else None, # Default handling by Rich is tricky with choices
            show_default=should_show_default_in_prompt if not options else False
        )
        if raw_user_input is None:
            # Treat None as empty string to avoid AttributeError on .strip()
            raw_user_input = ""
        else:
            raw_user_input = raw_user_input.strip()


        if help_context_id and raw_user_input.lower() in ['h', '?']:
            # Use the enhanced display_help_content function instead
            display_help_content(help_context_id)
            # After help, the screen is clear. The menu needs to redraw before next prompt.
            return "_HELP_SHOWN_" # Return sentinel value instead of continue

        # Manual validation against options if provided
        if options:
            if raw_user_input.lower() in [opt.lower() for opt in options]:
                for opt_val in options: # Return with original casing
                    if opt_val.lower() == raw_user_input.lower():
                        return opt_val
                # This part should ideally not be reached if the above finds a match
                return raw_user_input 
            else:
                # Constructing the valid options string for the error message
                valid_options_str = ", ".join(options)
                print_error(f"Invalid choice. Please enter one of [{valid_options_str}]{prompt_suffix if help_context_id else ''}.")
                # Loop continues, re-prompting. Menu should redraw.
                continue
        
        # If no options to validate against
        if allow_empty and not raw_user_input: # If empty input is allowed and input is empty
            return ""
        
        if not allow_empty and not raw_user_input: # If empty input is not allowed and input is empty
            print_error(f"Input cannot be empty.{prompt_suffix if help_context_id else ''}")
            # Loop continues, re-prompting. Menu should redraw.
            continue
            
        # If no options, and input is not empty (or empty is allowed and it's not empty)
        return raw_user_input

def get_confirmation(prompt: str, default: Optional[bool] = None) -> bool:
    """
    Prompt the user for a yes/no confirmation using Rich Confirm.
    Returns True for yes, False for no.
    """
    # Rich's Confirm.ask handles the prompt suffix (e.g., [y/N]),
    # validation, and re-prompting for invalid input.
    return Confirm.ask(prompt, default=default)

def clear_screen(force: bool = False) -> None:
    """
    Clear the terminal screen if enabled in user preferences.
    
    Args:
        force (bool): If True, clears the screen regardless of user preferences
    """
    # Try to access user preferences to check if screen clearing is disabled
    try:
        from wall_gen.settings_modules import get_preferences
        user_prefs = get_preferences()
        if user_prefs and user_prefs.wallpaper_settings.get("disable_screen_clearing", False) and not force:
            # Skip screen clearing if disabled in preferences and not forced
            return
    except (ImportError, AttributeError):
        # If we can't access preferences, continue with default behavior
        pass
        
    # Clear screen as before
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def print_wrapped_text(text: str, width: int = 70, indent: int = 4) -> None:
    """
    Print multi-line wrapped text with indentation using textwrap and Rich console.
    """
    wrapper = textwrap.TextWrapper(width=width, subsequent_indent=' ' * indent)
    wrapped = wrapper.fill(text)
    console.print(wrapped)

def display_help_section(section: HelpSection, index: int, total: int) -> None:
    """
    Displays a single help section within the enhanced help system.
    
    Args:
        section: The HelpSection object containing title, content and icon
        index: Current section index (1-based)
        total: Total number of sections
    """
    # Create a stylized title with section number, icon and navigation information
    title_text = Text()
    # Add section number indicator if multiple sections exist
    if total > 1:
        title_text.append(f"[{index}/{total}] ", style="dim cyan")
    
    # Add icon and title
    title_text.append(f"{section.icon} ", style="bold")
    title_text.append(section.title, style="bold cyan")
    
    # Create the panel with Rich markup-enabled content
    section_panel = Panel(
        section.content,  # Rich markup is directly supported here
        title=title_text,
        border_style="blue",
        expand=False
    )
    
    console.print(section_panel)

def display_help_content(context_id: str) -> None:
    """
    Enhanced help display system that handles both structured help content (list of HelpSection objects)
    and legacy string-based help content.
    
    Args:
        context_id: The context ID to retrieve help content for
    """
    # Clear screen before showing help
    clear_screen()
    
    # Get the help content
    help_content = get_help_text(context_id)
    
    # Format the title from the context_id
    formatted_title = context_id.replace('_', ' ').title()
    
    console.print(Rule(f"[bold cyan]{formatted_title} Help[/bold cyan]", style="cyan"))
    console.print()
    
    if not help_content:
        console.print(Text("No help content provided.", style="yellow"))
    elif isinstance(help_content, list):  # New structured format (list of HelpSection objects)
        total_sections = len(help_content)
        current_section = 0
        
        # Initial display of the first section
        if total_sections > 0:
            display_help_section(help_content[current_section], current_section + 1, total_sections)
        
        # Navigation controls if there are multiple sections
        if total_sections > 1:
            console.print()
            controls_text = Text("Navigation: ", style="cyan")
            controls_text.append("[N]ext ", style="green bold")
            controls_text.append("[P]revious ", style="yellow bold")
            controls_text.append("[Q]uit help", style="red bold")
            console.print(controls_text, justify="center")
            
            # Interactive section navigation
            while True:
                command = get_interactive_input("").lower()
                
                if command in ['q', 'quit', 'exit']:
                    break
                elif command in ['n', 'next'] and current_section < total_sections - 1:
                    current_section += 1
                    clear_screen()
                    console.print(Rule(f"[bold cyan]{formatted_title} Help[/bold cyan]", style="cyan"))
                    console.print()
                    display_help_section(help_content[current_section], current_section + 1, total_sections)
                    console.print()
                    console.print(controls_text, justify="center")
                elif command in ['p', 'prev', 'previous'] and current_section > 0:
                    current_section -= 1
                    clear_screen()
                    console.print(Rule(f"[bold cyan]{formatted_title} Help[/bold cyan]", style="cyan"))
                    console.print()
                    display_help_section(help_content[current_section], current_section + 1, total_sections)
                    console.print()
                    console.print(controls_text, justify="center")
        else:
            # Single section, just wait for any key to close
            console.print()
            console.print(Text("Press Enter to close help...", style="dim italic cyan"), justify="center")
            input()
    else:  # Legacy string-based format
        # Create a panel with padding
        legacy_panel = Panel(
            Padding(Text(help_content), (1, 2)),  # Top/bottom padding 1, left/right padding 2
            border_style="blue",
            expand=False  # Panel will size to content, up to console width
        )
        console.print(legacy_panel)
        console.print(Text("Press Enter to close help...", style="dim italic cyan"), justify="center")
        input()
    
    # Always clear the screen when exiting help
    clear_screen()

def display_help_panel(help_text: str, title: str = "Help") -> None:
    """
    Displays the given help text in a Rich Panel.
    Clears the screen after the help panel is dismissed.
    """
    if not help_text:
        console.print(Text("No help content provided.", style="yellow"))
        return

    content = Text(help_text, style="default")

    # Create a panel with padding
    help_panel = Panel(
        Padding(content, (1, 2)), # Top/bottom padding 1, left/right padding 2
        title=f"[bold cyan]{title}[/bold cyan]",
        border_style="blue",
        expand=False # Panel will size to content, up to console width
    )
    console.print() # Newline before panel
    console.print(help_panel)
    console.print(Text("Press any key to close help...", style="dim italic cyan", justify="center"))
    
    try:
        if sys.stdin.isatty(): # Check if running in an interactive terminal
            input() 
        else: # Non-interactive, maybe just pause briefly or skip
            time.sleep(0.1) # Small pause if not interactive
    except KeyboardInterrupt:
        pass # Allow Ctrl+C to break out
    finally:
        clear_screen() # CRITICAL: Clear screen after help display

def show_spinner(message: str, duration: float = 2) -> None:
    """
    Display a Rich status spinner for the specified duration.
    """
    # The 'spinner' argument in status can be customized, e.g., "line", "moon", "aesthetic"
    # Default spinner for rich.status.Status is "dots" if not specified.
    with console.status(message, spinner="dots"):
        time.sleep(duration)
    # Spinner stops automatically when the 'with' block exits.

def print_progress_bar(current_value: float, total_value: float = 1.0, length: int = 40, description: str = "Progress") -> None:
    """
    Print or update a Rich progress bar.
    Manages a single global progress bar instance.
    current_value: current progress
    total_value: total value representing 100%
    length: approximate width of the bar column, 0 or negative for auto.
    description: text to display for the progress bar
    """
    global _current_progress_bar, _current_progress_task_id

    # Handle potential division by zero if total_value is 0, common for indeterminate starts
    effective_total = total_value if total_value > 0 else 1.0
    # Ensure current_value does not exceed effective_total for initial add_task if total_value was 0
    safe_current_value = min(current_value, effective_total)

    if _current_progress_bar is None or _current_progress_task_id is None:
        if _current_progress_bar: # If bar exists but task_id is somehow None, stop old bar
            _current_progress_bar.stop()
            _current_progress_bar = None # Ensure it's reset for re-initialization

        bar_column_width = length if length > 0 else None
        _current_progress_bar = Progress(
            TextColumn("[progress.description]{task.description}", table_column={"min_width": len(description) + 2 if description else 10}),
            BarColumn(bar_width=bar_column_width),
            TextColumn("[progress.percentage]{task.percentage:>3.1f}%"),
            TimeRemainingColumn(),
            console=console,
            transient=False, # Keep visible until explicitly stopped/completed
        )
        _current_progress_task_id = _current_progress_bar.add_task(description, total=effective_total, completed=safe_current_value)
        _current_progress_bar.start()
    else:
        # Update existing progress bar
        _current_progress_bar.update(_current_progress_task_id, completed=current_value, total=effective_total, description=description)

    if current_value >= effective_total and _current_progress_bar:
        # Ensure the bar visually completes to 100% if it was slightly off due to float precision
        _current_progress_bar.update(_current_progress_task_id, completed=effective_total)
        _current_progress_bar.stop()
        _current_progress_bar = None
        _current_progress_task_id = None
        # Rich Progress usually handles the final cursor position well.
        # A console.print() here might add an unwanted extra line if Rich already printed one.

def print_footer(text: str) -> None:
    """
    Print a footer or status bar line using Rich.
    """
    footer_text = Text(text, justify="center", style="cyan")
    console.print(footer_text)

def print_breadcrumb(path_list: List[str]) -> None:
    """
    Print a breadcrumb trail using Rich.
    """
    if not path_list:
        return

    breadcrumb_text = Text(style="cyan") # Base style for path items
    for i, item in enumerate(path_list):
        breadcrumb_text.append(item)
        if i < len(path_list) - 1:
            # Apply a slightly different style to the separator for visual distinction
            breadcrumb_text.append(" > ", style="dim cyan") 
    
    console.print(breadcrumb_text)
    console.print() # To match the original behavior of an extra newline

def print_menu_options(options: List[tuple[str, str, Optional[str]]]) -> None:
    """
    Print menu options given a list of (key, description, optional shortcut) tuples.
    """
    for key, description, *rest in options:
        shortcut = rest[0] if rest else None
        print_option(key, description, shortcut)

def get_menu_choice(
    prompt: str, 
    valid_choices: List[str], 
    help_context_id: Optional[str] = None, # New parameter
    allow_empty: bool = False
) -> str:
    """
    Get a validated menu choice from the user, using enhanced get_validated_input.
    Handles KeyboardInterrupt and EOFError.
    """
    try:
        # Pass valid_choices to options parameter of get_validated_input
        return get_validated_input(
            prompt, 
            options=valid_choices, 
            help_context_id=help_context_id, 
            allow_empty=allow_empty
        )
    except KeyboardInterrupt:
        # console.print("\nOperation interrupted by user (Ctrl+C).", style="yellow") # Rich console for consistency
        print_warning("\nOperation interrupted by user (Ctrl+C).") # Using existing styled print
        return "_INTERRUPTED_"
    except EOFError:
        # console.print("\nInput stream closed (Ctrl+D).", style="yellow")
        print_warning("\nInput stream closed (Ctrl+D).") # Using existing styled print
        return "_EOF_"

# Function show_ascii_art() removed as it was redundant with app_utils.display_startup_message
# and its only potential call site was commented out.

def print_styled_prompt(label: str, prompt_string: str, label_style: str = "bold default", prompt_style: str = "italic cyan") -> None:
    """
    Prints a label and the AI-generated prompt with specific styles.
    The label and prompt are printed on separate lines.
    """
    console.print(Text(label, style=label_style))
    console.print(Text(prompt_string, style=prompt_style))
