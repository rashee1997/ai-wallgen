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

    def view_history(self, limit=50):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT date, prompt, enhanced_prompt, gemini_prompt, image_filename, settings_json, output FROM generation_history ORDER BY datetime(date) DESC LIMIT ?",
            (limit,)
        )
        rows = cursor.fetchall()
        # Table headers (fixed, to fit terminal)
        headers = [
            "No",
            "Date",
            "Prompt",
            "Enhanced Prompt",
            "Gemini Prompt",
            "Image Filename",
            "User Prefs",
            "Output",
        ]
        table = []
        import textwrap
        for i, entry in enumerate(rows, 1):
            date, prompt, enhanced_prompt, gemini_prompt, image_filename, settings_json, output = entry
            # settings: summarize user prefs keys and values
            user_prefs_summary = ""
            if settings_json:
                try:
                    settings = json.loads(settings_json)
                    userprefs = settings.get("user_preferences", {})
                    if userprefs:
                        kvs = "; ".join(f"{k}={str(v)[:15]+('...' if len(str(v))>15 else '')}" for k, v in userprefs.items())
                        user_prefs_summary = kvs
                except Exception:
                    user_prefs_summary = ""
            # word wrap for prompt columns
            def wrap(val, width=30):
                if val is None: return ""
                return "\n".join(textwrap.wrap(str(val), width=width, break_long_words=True, replace_whitespace=False)) or ""
            row = [
                i,
                wrap(date, 19),
                wrap(prompt, 30),
                wrap(enhanced_prompt, 30),
                wrap(gemini_prompt, 30),
                wrap(image_filename, 20),
                wrap(user_prefs_summary, 22),
                wrap(output, 20),
            ]
            table.append(row)
        # Print the ASCII table
        if not table:
            print("\nℹ No generation history available.")
            return
        # Calculate column widths
        col_widths = [max(len(str(x)) for x in col) for col in zip(headers, *table)]
        # Print header
        header_row = " | ".join(f"{h:<{w}}" for h, w in zip(headers, col_widths))
        print("=" * len(header_row))
        print(header_row)
        print("=" * len(header_row))
        # Print table rows
        for row in table:
            print(" | ".join(f"{str(cell):<{w}}" for cell, w in zip(row, col_widths)))
        print("=" * len(header_row))

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
