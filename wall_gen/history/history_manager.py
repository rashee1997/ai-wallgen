import os
import sqlite3
import json
from datetime import datetime

class HistoryManager:
    def __init__(self, db_path=None):
        # Database file is always in history/history.db
        if db_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(base_dir, "history.db")
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self._create_table()

    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS generation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                prompt TEXT,
                enhanced_prompt TEXT,
                gemini_prompt TEXT,
                image_filename TEXT,
                settings_json TEXT,
                output TEXT
            )
        """)
        self.conn.commit()

    def add_entry(self, entry_data):
        cursor = self.conn.cursor()
        settings = {
            "user_preferences": entry_data.get("user_preferences", {}),
            "imagen_settings": entry_data.get("imagen_settings", {}),
            "wallpaper_settings": entry_data.get("wallpaper_settings", {}),
        }
        cursor.execute(
            """
            INSERT INTO generation_history
            (date, prompt, enhanced_prompt, gemini_prompt, image_filename, settings_json, output)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now().isoformat(),
                entry_data.get("prompt", ""),
                entry_data.get("enhanced_prompt", ""),
                entry_data.get("gemini_prompt", ""),
                entry_data.get("image_filename", ""),
                json.dumps(settings),
                entry_data.get("output", "")
            ),
        )
        self.conn.commit()

    def view_history(self, page_size=10): # Default page size, limit removed
        from wall_gen.ui_utils import clear_screen, get_validated_input, print_info, print_header, print_error # Import necessary UI utils
        import textwrap # Keep textwrap import local to the method or move to top if used elsewhere

        cursor = self.conn.cursor()

        # Get total number of entries for pagination
        cursor.execute("SELECT COUNT(*) FROM generation_history")
        total_entries = cursor.fetchone()[0]
        
        if total_entries == 0:
            clear_screen()
            print_header("Generation History")
            print_info("\nℹ No generation history available.")
            get_validated_input("Press Enter to return to menu...", options=None, allow_empty=True) # Wait for user
            return

        total_pages = (total_entries + page_size - 1) // page_size
        current_page = 1

        # Table headers (fixed, to fit terminal) - defined once
        headers = [
            "No", "Date", "Prompt", "Enhanced Prompt", 
            "Gemini Prompt", "Image Filename", "User Prefs", "Output",
        ]

        while True:
            clear_screen() # Clear screen for each page display
            print_header("Generation History") # Display header on each page
            
            offset = (current_page - 1) * page_size
            
            cursor.execute(
                "SELECT date, prompt, enhanced_prompt, gemini_prompt, image_filename, settings_json, output FROM generation_history ORDER BY datetime(date) DESC LIMIT ? OFFSET ?",
                (page_size, offset)
            )
            rows = cursor.fetchall()
            
            table_data_for_page = []
            if rows:
                for i, entry in enumerate(rows, offset + 1): # Use offset for correct numbering
                    date, prompt, enhanced_prompt, gemini_prompt, image_filename, settings_json, output_text = entry
                    user_prefs_summary = ""
                    if settings_json:
                        try:
                            settings = json.loads(settings_json)
                            userprefs = settings.get("user_preferences", {})
                            if userprefs:
                                kvs = "; ".join(f"{k}={str(v)[:15]+('...' if len(str(v))>15 else '')}" for k, v in userprefs.items())
                                user_prefs_summary = kvs
                        except Exception:
                            user_prefs_summary = "Error parsing settings"
                    
                    def wrap(val, width=30):
                        if val is None: return ""
                        # Ensure val is a string before wrapping
                        return "\n".join(textwrap.wrap(str(val), width=width, break_long_words=True, replace_whitespace=False)) or ""

                    row_content = [
                        i,
                        wrap(date, 19),
                        wrap(prompt, 30),
                        wrap(enhanced_prompt, 30),
                        wrap(gemini_prompt, 30),
                        wrap(image_filename, 20),
                        wrap(user_prefs_summary, 22),
                        wrap(output_text, 20), # Renamed output to output_text to avoid conflict
                    ]
                    table_data_for_page.append(row_content)

            if not table_data_for_page: # This condition implies no rows for the current page
                if current_page == 1 and total_entries == 0: # Already handled above
                    pass
                else: # Should ideally not be reached if total_pages is correct, but good for safety
                    print_info("\nℹ No history entries on this page.")
            else:
                # Calculate column widths based on current page's data and headers
                # Ensure all cells are strings for len() calculation
                stringified_table = [[str(cell) for cell in row] for row in table_data_for_page]
                col_widths = [max(len(str(x)) for x in col) for col in zip(*([headers] + stringified_table))]

                # Print header
                header_row_str = " | ".join(f"{h:<{w}}" for h, w in zip(headers, col_widths))
                print_info("=" * len(header_row_str)) # Use print_info or console.print for consistency
                print_info(header_row_str)
                print_info("=" * len(header_row_str))
                # Print table rows
                for r_data in table_data_for_page:
                    print_info(" | ".join(f"{str(cell):<{w}}" for cell, w in zip(r_data, col_widths)))
                print_info("=" * len(header_row_str))

            # Pagination info and navigation
            print_info(f"\nPage {current_page} of {total_pages}")
            nav_prompt_parts = []
            valid_choices_nav = ['e'] # Exit is always an option

            if current_page > 1:
                nav_prompt_parts.append("(P)revious")
                valid_choices_nav.append('p')
            if current_page < total_pages:
                nav_prompt_parts.append("(N)ext")
                valid_choices_nav.append('n')
            nav_prompt_parts.append("(E)xit to menu")
            
            prompt_message = "Navigate: " + ", ".join(nav_prompt_parts) + " > "
            
            # Add a help context ID if one is defined for history navigation
            # For now, omitting help_context_id for simplicity unless specified
            choice = get_validated_input(
                prompt_message,
                options=valid_choices_nav,
                allow_empty=False 
            ).lower()
            
            if choice == "_HELP_SHOWN_": # If help was shown, ui_utils clears screen, so we need to redraw
                continue # Redraw current page

            if choice == 'n' and 'n' in valid_choices_nav:
                current_page += 1
            elif choice == 'p' and 'p' in valid_choices_nav:
                current_page -= 1
            elif choice == 'e':
                break # Exit the while loop, returning to main menu
            # Invalid choices are handled by get_validated_input, which will re-prompt.
            # The loop will continue, effectively redrawing the current page.

    def close(self):
        self.conn.close()

# Convenience wrappers matching previous API
_global_history_manager = None

def get_history_manager():
    global _global_history_manager
    if _global_history_manager is None:
        _global_history_manager = HistoryManager()
    return _global_history_manager

def add_to_history(entry):
    get_history_manager().add_entry(entry)

def view_history():
    get_history_manager().view_history()
