#!/usr/bin/env python3
"""
Simplified Qt Image Preview for Wallpaper Generator.

This module provides a basic GUI window to preview images
before setting them as wallpaper, with zoom, crop, and save functions.
"""

import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class SimpleImagePreviewApp(QtWidgets.QWidget):
    """
    A simplified Qt application for previewing images before setting as wallpaper.
    
    Features:
    - Basic image display
    - Zoom in/out
    - Mouse scroll zoom
    - Simple UI with Set/Cancel buttons
    """
    def __init__(self, image_path, set_wallpaper_callback=None):
        super().__init__()
        self.image_path = image_path
        self.set_wallpaper_callback = set_wallpaper_callback
        self.result = False
        
        self.init_ui()
        self.load_image()
    
    def init_ui(self):
        self.setWindowTitle("Wallpaper Preview")
        
        # Set dark background color and add gradient background
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                background-image: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 #2c2c2c, stop:1 #121212);
                color: #e0e0e0;
                font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            }
            QLabel#titleLabel {
                color: #ffffff;
                font-weight: 600;
                font-size: 28pt;
                margin-bottom: 10px;
            }
            QLabel#statusLabel {
                color: #a0a0a0;
                font-style: italic;
                font-size: 13pt;
                margin-top: 8px;
            }
            QPushButton {
                background-color: #005a9e;
                color: white;
                font: 14pt "Segoe UI";
                border: none;
                padding: 10px 22px;
                border-radius: 8px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #0078d7;
            }
            QPushButton:pressed {
                background-color: #004a7c;
            }
            QPushButton:disabled {
                background-color: #444444;
                color: #888888;
            }
        """)
        
        # Layouts
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)
        self.resize(450, 600)
        
        # Title label with image name
        image_name = os.path.basename(self.image_path)
        self.title_label = QtWidgets.QLabel(f"Preview: {image_name}")
        self.title_label.setObjectName("titleLabel")
        title_font = QtGui.QFont("Segoe UI", 28, QtGui.QFont.DemiBold)
        self.title_label.setFont(title_font)
        main_layout.addWidget(self.title_label, alignment=QtCore.Qt.AlignLeft)
        
        # Image display label with border and shadow effect
        self.image_label = QtWidgets.QLabel()
        self.image_label.setStyleSheet("""
            background-color: #1e1e1e;
            border: 2px solid #555555;
            border-radius: 6px;
        """)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.image_label.setMinimumSize(380, 270)
        # Add drop shadow effect
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(12)
        shadow.setColor(QtGui.QColor(0, 0, 0, 180))
        shadow.setOffset(0, 0)
        self.image_label.setGraphicsEffect(shadow)
        main_layout.addWidget(self.image_label, stretch=1)
        
        # Status label
        self.status_label = QtWidgets.QLabel("Loading image...")
        self.status_label.setObjectName("statusLabel")
        status_font = QtGui.QFont("Segoe UI", 13, QtGui.QFont.StyleItalic)
        self.status_label.setFont(status_font)
        main_layout.addWidget(self.status_label, alignment=QtCore.Qt.AlignLeft)
        
        # Buttons layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(12)
        
        # Zoom out button
        self.zoom_out_button = QtWidgets.QPushButton("-")
        self.zoom_out_button.setFixedSize(42, 42)
        self.zoom_out_button.setToolTip("Zoom Out")
        self.zoom_out_button.clicked.connect(self.zoom_out)
        button_layout.addWidget(self.zoom_out_button)
        
        # Zoom in button
        self.zoom_in_button = QtWidgets.QPushButton("+")
        self.zoom_in_button.setFixedSize(42, 42)
        self.zoom_in_button.setToolTip("Zoom In")
        self.zoom_in_button.clicked.connect(self.zoom_in)
        button_layout.addWidget(self.zoom_in_button)
        
        # Spacer to push buttons to center
        button_layout.addStretch()
        
        # Set as Wallpaper button
        self.set_button = QtWidgets.QPushButton("Set as Wallpaper")
        self.set_button.setFixedHeight(45)
        self.set_button.clicked.connect(self.set_wallpaper)
        button_layout.addWidget(self.set_button)
        
        # Cancel button
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setFixedHeight(45)
        self.cancel_button.clicked.connect(self.cancel)
        button_layout.addWidget(self.cancel_button)
        
        # Spacer to push buttons to center
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)

        # Enable mouse wheel zoom on image_label
        self.image_label.wheelEvent = self.wheelEvent
    
    def load_image(self):
        """Load and display the image."""
        if not os.path.exists(self.image_path):
            self.status_label.setText(f"Error: File not found: {self.image_path}")
            self.set_button.setEnabled(False)
            return
        
        self.original_pixmap = QtGui.QPixmap(self.image_path)
        if self.original_pixmap.isNull():
            self.status_label.setText("Error loading image: Unsupported or corrupted file")
            self.set_button.setEnabled(False)
            return
        
        self.current_pixmap = self.original_pixmap
        self.scale_factor = 1.0
        self.update_image_display()
        self.set_button.setEnabled(True)
        
        # Remove crop functionality: no cropping
        # Remove rubber band and crop event handlers
        self.is_cropping = False
        self.crop_rect = QtCore.QRect()
        self.rubber_band = None
        # Remove mouse event overrides for cropping
        self.image_label.mousePressEvent = lambda event: None
        self.image_label.mouseMoveEvent = lambda event: None
        self.image_label.mouseReleaseEvent = lambda event: None

    def update_image_display(self):
        """Update the image display with current pixmap and scale."""
        if self.current_pixmap:
            label_size = self.image_label.size()
            scaled_pixmap = self.current_pixmap.scaled(label_size * self.scale_factor, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
    
    def zoom_in(self):
        self.scale_factor *= 1.25
        self.update_image_display()
    
    def zoom_out(self):
        self.scale_factor /= 1.25
        self.update_image_display()
    
    def wheelEvent(self, event):
        """Zoom in/out with mouse wheel."""
        delta = event.angleDelta().y()
        if delta > 0:
            self.zoom_in()
        elif delta < 0:
            self.zoom_out()
        event.accept()
    
    def resizeEvent(self, event):
        """Handle window resize to rescale image."""
        super().resizeEvent(event)
        self.update_image_display()
    
    def center(self):
        """Center the window on the screen."""
        frame_gm = self.frameGeometry()
        screen = QtWidgets.QApplication.primaryScreen()
        center_point = screen.availableGeometry().center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())
    
    def set_wallpaper(self):
        """Set the wallpaper and close the window."""
        self.result = True
        if self.set_wallpaper_callback:
            try:
                self.set_wallpaper_callback(self.image_path)
            except Exception as e:
                print(f"Error setting wallpaper: {e}")
        self.close()
    
    def cancel(self):
        """Cancel and close the window."""
        self.result = False
        self.close()
    
    def run(self):
        """Run the application."""
        self.show()
        app = QtWidgets.QApplication.instance()
        if app is None:
            app = QtWidgets.QApplication(sys.argv)
        app.exec_()
        return self.result


def preview_image_gui(image_path, set_wallpaper_callback=None):
    """
    Show a simple Qt window to preview the image.
    
    Args:
        image_path (str): Path to the image file
        set_wallpaper_callback (callable, optional): Callback for setting as wallpaper
        
    Returns:
        bool: True if user chose to set as wallpaper, False otherwise
    """
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    preview = SimpleImagePreviewApp(image_path, set_wallpaper_callback)
    result = preview.run()
    return result


if __name__ == "__main__":
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        
        def dummy_callback(path):
            print(f"Would set wallpaper: {path}")
        
        result = preview_image_gui(image_path, dummy_callback)
        print(f"Set as wallpaper: {result}")
    else:
        print("Usage: python qt_preview.py [image_path]")
