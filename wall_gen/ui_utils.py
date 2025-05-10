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

console = Console()

# --- Rich Progress Bar setup ---
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TaskID
_current_progress_bar: Optional[Progress] = None
_current_progress_task_id: Optional[TaskID] = None
# --- End Rich library setup ---

def print_header(text: str) -> None:
    """
    Print a formatted header using Rich Rules and Text.
    """
    header_text = Text(text, justify="center", style="bold cyan")
    
    console.print() # For the initial newline before the first border
    console.print(Rule(style="cyan", characters="=")) 
    console.print(header_text) 
    console.print(Rule(style="cyan", characters="=")) 
    console.print() # For the additional newline (original had \n\n after last border)

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

def get_validated_input(prompt: str, options: Optional[List[str]] = None,
                        default: Optional[str] = None, allow_empty: bool = False) -> str:
    """
    Get and validate user input using Rich Prompt.
    """
    effective_default = default
    if default is None and allow_empty:
        # If allow_empty is True and no specific default is given,
        # an empty string is effectively the default for blank input.
        effective_default = ""
    
    # show_default should reflect if an original default was provided by the caller,
    # not our internally set effective_default of "" if that was the case.
    should_show_default_in_prompt = bool(default is not None)

    return Prompt.ask(
        prompt,
        choices=options,
        default=effective_default,
        show_default=should_show_default_in_prompt
    )

def get_confirmation(prompt: str, default: Optional[bool] = None) -> bool:
    """
    Prompt the user for a yes/no confirmation using Rich Confirm.
    Returns True for yes, False for no.
    """
    # Rich's Confirm.ask handles the prompt suffix (e.g., [y/N]),
    # validation, and re-prompting for invalid input.
    return Confirm.ask(prompt, default=default)

def clear_screen() -> None:
    """
    Clear the terminal screen.
    """
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

def get_menu_choice(prompt: str, valid_choices: List[str], allow_empty: bool = False) -> str:
    """
    Get a validated menu choice from the user.
    """
    try:
        return get_validated_input(prompt, valid_choices, allow_empty=allow_empty)
    except KeyboardInterrupt:
        print("\nOperation interrupted.")
        return "_INTERRUPTED_"
    except EOFError:
        print("\nInput closed. Exiting menu.")
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
