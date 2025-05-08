#!/usr/bin/env python3
"""
Simplified Tkinter Image Preview for Wallpaper Generator.

This module provides a basic GUI window to preview images
before setting them as wallpaper, without image manipulations.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import logging

class SimpleImagePreviewApp:
    """
    A simplified Tkinter application for previewing images before setting as wallpaper.
    
    Features:
    - Basic image display
    - Simple UI with Set/Cancel buttons
    """
    
    def __init__(self, image_path, set_wallpaper_callback=None):
        """Initialize the image preview window."""
        self.image_path = image_path
        self.set_wallpaper_callback = set_wallpaper_callback
        self.result = False
        
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Wallpaper Preview")
        
        # Set a modern color scheme for the window background
        self.root.configure(bg="#2e2e2e")  # dark gray background
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set window size (75% of screen)
        window_width = int(screen_width * 0.75)
        window_height = int(screen_height * 0.75)
        self.root.geometry(f"{window_width}x{window_height}")
        
        # Center the window
        x_offset = (screen_width - window_width) // 2
        y_offset = (screen_height - window_height) // 2
        self.root.geometry(f"+{x_offset}+{y_offset}")
        
        # Configure the grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Create widgets
        self.create_widgets()
        
        # Bind events
        self.root.bind("<Return>", lambda e: self.set_wallpaper())
        self.root.bind("<Escape>", lambda e: self.cancel())
        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
    
    def create_widgets(self):
        """Create and arrange all the widgets for the application."""
        # Main frame with custom background color
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        
        # Title with image name - use nicer font and color
        image_name = os.path.basename(self.image_path)
        title_font = tkfont.Font(family="Tahoma", size=22, weight="normal")
        status_font = tkfont.Font(family="Tahoma", size=14, weight="normal")
        self.title_label = ttk.Label(self.main_frame, 
                                     text=f"Preview: {image_name}",
                                     font=title_font,
                                     foreground="#ffffff",
                                     background="#2e2e2e")
        self.title_label.grid(row=0, column=0, padx=15, pady=15, sticky="w")
        
        # Label for displaying image with border and relief
        self.image_label = ttk.Label(self.main_frame, background='#1e1e1e', relief="sunken", borderwidth=3)
        self.image_label.grid(row=1, column=0, sticky="nsew", padx=25, pady=15)
        
        # Status label with custom font and color
        self.status_label = ttk.Label(self.main_frame, text="Loading image...",
                                      font=status_font,
                                      foreground="#cccccc",
                                      background="#2e2e2e")
        self.status_label.grid(row=2, column=0, padx=25, pady=8, sticky="w")
        
        # Buttons frame with background color
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=3, column=0, padx=25, pady=15, sticky="ew")
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        
        # Style for buttons
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton',
                        font=('Segoe UI', 12, 'normal'),
                        foreground='#ffffff',
                        background='#4a90e2',
                        borderwidth=0,
                        focusthickness=3,
                        focuscolor='none',
                        padding=10)
        style.map('TButton',
                  background=[('active', '#5a9bf6'), ('pressed', '#357ABD')],
                  foreground=[('disabled', '#a3a3a3')])
        style.configure('TButton', relief='flat')
        style.map('TButton',
                  relief=[('pressed', 'sunken'), ('!pressed', 'flat')])
        
        # Set wallpaper button with custom style
        self.set_button = ttk.Button(self.button_frame,
                                     text="Set as Wallpaper",
                                     command=self.set_wallpaper,
                                     style='TButton')
        self.set_button.grid(row=0, column=0, padx=15, pady=10, sticky="e")
        
        # Cancel button with custom style
        self.cancel_button = ttk.Button(self.button_frame,
                                        text="Cancel",
                                        command=self.cancel,
                                        style='TButton')
        self.cancel_button.grid(row=0, column=1, padx=15, pady=10, sticky="w")
    
    def load_image(self):
        """Load and display the image (basic version)."""
        try:
            # Check if file exists
            if not os.path.exists(self.image_path):
                self.status_label.configure(text=f"Error: File not found: {self.image_path}")
                return False
            
            # Try to display directly using tkinter's PhotoImage
            try:
                # Only for GIF, PPM, PGM, PNG formats
                self.tk_image = tk.PhotoImage(file=self.image_path)
                self.status_label.configure(text="Image loaded successfully (native format)")
            except Exception as e:
                # Fallback to PIL for other formats
                try:
                    img = Image.open(self.image_path)
                    self.tk_image = ImageTk.PhotoImage(img)
                    self.status_label.configure(text="Image loaded successfully (using PIL)")
                except Exception as e:
                    self.status_label.configure(text=f"Error loading image: {str(e)}")
                    return False
            
            # Display the image
            self.image_label.configure(image=self.tk_image)
            return True
            
        except Exception as e:
            self.status_label.configure(text=f"Unexpected error: {str(e)}")
            return False
    
    def set_wallpaper(self):
        """Set the wallpaper and close the window."""
        self.result = True
        if self.set_wallpaper_callback:
            try:
                self.set_wallpaper_callback(self.image_path)
            except Exception as e:
                print(f"Error setting wallpaper: {e}")
        self.root.quit()
        self.root.destroy()
    
    def cancel(self):
        """Cancel and close the window."""
        self.result = False
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Run the application."""
        # Load the image before entering mainloop
        if self.load_image():
            self.root.mainloop()
        else:
            # If image loading fails, wait a bit then close
            self.root.after(3000, self.root.destroy)
            self.root.mainloop()
        return self.result


def preview_image_gui(image_path, set_wallpaper_callback=None):
    """
    Show a simple Tkinter window to preview the image.
    
    Args:
        image_path (str): Path to the image file
        set_wallpaper_callback (callable, optional): Callback for setting as wallpaper
        
    Returns:
        bool: True if user chose to set as wallpaper, False otherwise
    """
    app = SimpleImagePreviewApp(image_path, set_wallpaper_callback)
    return app.run()


if __name__ == "__main__":
    # Test the preview window if this file is run directly
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        
        def dummy_callback(path):
            print(f"Would set wallpaper: {path}")
        
        result = preview_image_gui(image_path, dummy_callback)
        print(f"Set as wallpaper: {result}")
    else:
        print("Usage: python tkinter_preview.py [image_path]")
