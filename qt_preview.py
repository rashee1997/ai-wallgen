"""
Simplified Qt Image Preview for Wallpaper Generator.

This module provides a basic GUI window to preview images
before setting them as wallpaper, with zoom, crop, and save functions.
"""

import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer # Import QTimer

from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QFileDialog, QMessageBox, QSlider, QScrollArea
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QImage, QColor
import PIL
import numpy as np # Import numpy
import cv2 # Import cv2
from image_editor import (
    adjust_brightness,
    adjust_contrast,
    adjust_saturation,
    adjust_sharpness,
    apply_gamma_correction,
    apply_blur,
    apply_grayscale,
    apply_invert,
    rotate_image,
    ai_enhance,
    remove_background,
    apply_high_pass_filter,
    apply_histogram_equalization,
    apply_contour_detection,
    add_gaussian_noise,
    apply_pencil_sketch,
    apply_sepia,
    apply_sharpen_filter,
    add_border,
    apply_xray_effect,
    apply_emboss,
    apply_edge_enhance,
    apply_edge_enhance_more,
    apply_find_edges,
    apply_detail,
    apply_smooth,
    apply_smooth_more,
    apply_laplace,
    apply_sobel,
    apply_scharr,
    apply_prewitt,
    apply_roberts,
    apply_gabor,
    apply_otsu_threshold,
    apply_niblack_threshold,
    apply_sauvola_threshold,
    ImageHistory,
)

# Moved PannableScrollArea class definition to module level
class PannableScrollArea(QtWidgets.QScrollArea):
    """A QScrollArea that allows panning by dragging with the left mouse button."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.last_mouse_pos = None
        self._initial_h_scroll = 0
        self._initial_v_scroll = 0
        self.setWidgetResizable(True) # Ensure widget resizes with area
        self.setAlignment(Qt.AlignCenter) # Center content when smaller
        self.setMouseTracking(True) # Needed for mouseMoveEvent without button press sometimes

    def mousePressEvent(self, event):
        """Handles mouse press events for panning."""
        if event.button() == Qt.LeftButton: # Use LeftButton for panning
            self.last_mouse_pos = event.pos()
            # Store initial scroll bar values
            self._initial_h_scroll = self.horizontalScrollBar().value()
            self._initial_v_scroll = self.verticalScrollBar().value()
            self.setCursor(Qt.ClosedHandCursor) # Change cursor to indicate dragging
            event.accept()
        else:
            # Pass other button events to the default handler
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Handles mouse move events for panning."""
        if event.buttons() & Qt.LeftButton and self.last_mouse_pos is not None: # Check for LeftButton
            delta = event.pos() - self.last_mouse_pos
            # Update scroll bar values based on mouse movement
            self.horizontalScrollBar().setValue(self._initial_h_scroll - delta.x())
            self.verticalScrollBar().setValue(self._initial_v_scroll - delta.y())
            event.accept()
        else:
            # Pass other move events to the default handler
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Handles mouse release events for panning."""
        if event.button() == Qt.LeftButton and self.last_mouse_pos is not None: # Check for LeftButton
            self.last_mouse_pos = None
            self.setCursor(Qt.ArrowCursor) # Restore default cursor
            event.accept()
        else:
            # Pass other release events to the default handler
            super().mouseReleaseEvent(event)


class ImageDisplayWidget(QtWidgets.QWidget):
    """
    Custom widget for displaying the image and handling selection drawing.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._pixmap = QtGui.QPixmap() # Store the image pixmap
        self.setAttribute(Qt.WA_OpaquePaintEvent) # Optimize painting

    def setPixmap(self, pixmap: QtGui.QPixmap):
        """Sets the pixmap to be displayed and updates widget size."""
        self._pixmap = pixmap
        self.setFixedSize(pixmap.size()) # Set widget size to pixmap size
        self.update() # Trigger repaint

    def pixmap(self) -> QtGui.QPixmap:
        """Returns the current pixmap."""
        return self._pixmap

    def paintEvent(self, event):
        """Override paint event to draw the pixmap and selection outline."""
        painter = QtGui.QPainter(self) # Paint on this widget

        if self._pixmap.isNull():
            return # Nothing to draw

        # Draw the image pixmap
        painter.drawPixmap(self.rect(), self._pixmap)



        painter.end() # End the painter




class ImageEditTab(QWidget):
    """
    Separate tab for image editing with basic editing controls.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_image = None  # PIL Image
        self.edited_image = None    # PIL Image
        self.image_path = None

        # History manager for undo/redo
        self.history = ImageHistory(max_length=10)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12) # Increased vertical spacing

        # Place the ImageDisplayWidget inside a PannableScrollArea
        self.image_scroll_area = PannableScrollArea()
        self.image_display_widget = ImageDisplayWidget() # Create the custom widget
        self.image_scroll_area.setWidget(self.image_display_widget)
        self.image_scroll_area.setAlignment(Qt.AlignCenter) # Center the widget in the scroll area
        layout.addWidget(self.image_scroll_area, stretch=1) # Add scroll area to layout

        # Create tab widget for sub-tabs
        self.sub_tabs = QtWidgets.QTabWidget()
        layout.addWidget(self.sub_tabs)

        # --- Basic Adjustments Tab ---
        basic_tab = QWidget()
        basic_layout = QVBoxLayout(basic_tab)
        basic_layout.setSpacing(6)

        # Brightness
        brightness_layout = QHBoxLayout()
        brightness_label = QLabel("Brightness")
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(0, 200)
        self.brightness_slider.setValue(100)
        self.brightness_slider.valueChanged.connect(self.apply_edits)
        brightness_layout.addWidget(brightness_label)
        brightness_layout.addWidget(self.brightness_slider)
        basic_layout.addLayout(brightness_layout)

        # Contrast
        contrast_layout = QHBoxLayout()
        contrast_label = QLabel("Contrast")
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(0, 200)
        self.contrast_slider.setValue(100)
        self.contrast_slider.valueChanged.connect(self.apply_edits)
        contrast_layout.addWidget(contrast_label)
        contrast_layout.addWidget(self.contrast_slider)
        basic_layout.addLayout(contrast_layout)

        # Saturation
        saturation_layout = QHBoxLayout()
        saturation_label = QLabel("Saturation")
        self.saturation_slider = QSlider(Qt.Horizontal)
        self.saturation_slider.setRange(0, 200)
        self.saturation_slider.setValue(100)
        self.saturation_slider.valueChanged.connect(self.apply_edits)
        saturation_layout.addWidget(saturation_label)
        saturation_layout.addWidget(self.saturation_slider)
        basic_layout.addLayout(saturation_layout)

        self.sub_tabs.addTab(basic_tab, "Basic Adjustments")



        # --- Advanced Adjustments Tab ---
        advanced_tab = QWidget()
        advanced_layout = QVBoxLayout(advanced_tab)
        advanced_layout.setSpacing(6)

        # Sharpness
        sharpness_layout = QHBoxLayout()
        sharpness_label = QLabel("Sharpness")
        self.sharpness_slider = QSlider(Qt.Horizontal)
        self.sharpness_slider.setRange(0, 200)
        self.sharpness_slider.setValue(100)
        self.sharpness_slider.valueChanged.connect(self.apply_edits)
        sharpness_layout.addWidget(sharpness_label)
        sharpness_layout.addWidget(self.sharpness_slider)
        advanced_layout.addLayout(sharpness_layout)

        # Gamma
        gamma_layout = QHBoxLayout()
        gamma_label = QLabel("Gamma")
        self.gamma_slider = QSlider(Qt.Horizontal)
        self.gamma_slider.setRange(20, 220)  # Represents 0.2 to 2.2
        self.gamma_slider.setValue(100)
        self.gamma_slider.valueChanged.connect(self.apply_edits)
        gamma_layout.addWidget(gamma_label)
        gamma_layout.addWidget(self.gamma_slider)
        advanced_layout.addLayout(gamma_layout)

        # Blur
        blur_layout = QHBoxLayout()
        blur_label = QLabel("Blur")
        self.blur_slider = QSlider(Qt.Horizontal)
        self.blur_slider.setRange(0, 10)
        self.blur_slider.setValue(0)
        self.blur_slider.valueChanged.connect(self.apply_edits)
        blur_layout.addWidget(blur_label)
        blur_layout.addWidget(self.blur_slider)
        advanced_layout.addLayout(blur_layout)

        self.sub_tabs.addTab(advanced_tab, "Advanced Adjustments")

        # --- Filters Tab ---
        filters_tab = QWidget()
        filters_layout = QHBoxLayout(filters_tab)
        filters_layout.setSpacing(8) # Reduced spacing

        # Toggle buttons for grayscale/invert
        self.grayscale_button = QPushButton("Grayscale")
        self.grayscale_button.setCheckable(True)
        self.grayscale_button.toggled.connect(self.apply_edits)
        self.grayscale_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed) # Fixed height
        filters_layout.addWidget(self.grayscale_button)

        self.invert_button = QPushButton("Invert")
        self.invert_button.setCheckable(True)
        self.invert_button.toggled.connect(self.apply_edits)
        self.invert_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed) # Fixed height
        filters_layout.addWidget(self.invert_button)

        # New buttons for advanced filters
        self.high_pass_button = QPushButton("High Pass")
        self.high_pass_button.setCheckable(True)
        self.high_pass_button.toggled.connect(self.apply_edits)
        filters_layout.addWidget(self.high_pass_button)

        self.hist_eq_button = QPushButton("Hist Equalize")
        self.hist_eq_button.setCheckable(True)
        self.hist_eq_button.toggled.connect(self.apply_edits)
        filters_layout.addWidget(self.hist_eq_button)

        self.contour_button = QPushButton("Contour")
        self.contour_button.setCheckable(True)
        self.contour_button.toggled.connect(self.apply_edits)
        filters_layout.addWidget(self.contour_button)

        self.noise_button = QPushButton("Noise")
        self.noise_button.setCheckable(True)
        self.noise_button.toggled.connect(self.apply_edits)
        filters_layout.addWidget(self.noise_button)

        self.pencil_sketch_button = QPushButton("Pencil Sketch")
        self.pencil_sketch_button.setCheckable(True)
        self.pencil_sketch_button.toggled.connect(self.apply_edits)
        filters_layout.addWidget(self.pencil_sketch_button)

        self.sepia_button = QPushButton("Sepia")
        self.sepia_button.setCheckable(True)
        self.sepia_button.toggled.connect(self.apply_edits)
        filters_layout.addWidget(self.sepia_button)

        filters_layout.addStretch() # Push buttons to the right

        self.sub_tabs.addTab(filters_tab, "Filters")

        # --- Additional Effects Tab ---
        effects_tab = QWidget()
        effects_layout = QHBoxLayout(effects_tab)
        effects_layout.setSpacing(8)

        self.sharpen_button = QPushButton("Sharpen")
        self.sharpen_button.setCheckable(True)
        self.sharpen_button.toggled.connect(self.apply_edits)
        effects_layout.addWidget(self.sharpen_button)

        self.border_button = QPushButton("Border")
        self.border_button.setCheckable(True)
        self.border_button.toggled.connect(self.apply_edits)
        effects_layout.addWidget(self.border_button)

        self.xray_button = QPushButton("X-Ray")
        self.xray_button.setCheckable(True)
        self.xray_button.toggled.connect(self.apply_edits)
        effects_layout.addWidget(self.xray_button)

        effects_layout.addStretch()

        self.sub_tabs.addTab(effects_tab, "Additional Effects")

        # --- Advanced Filters Tab ---
        advanced_filters_tab = QWidget()
        advanced_filters_layout = QVBoxLayout(advanced_filters_tab)
        advanced_filters_layout.setSpacing(6) # Vertical spacing

        # Pillow ImageFilter buttons
        pillow_filters_layout = QHBoxLayout()
        pillow_filters_layout.setSpacing(8)
        self.emboss_button = QPushButton("Emboss")
        self.emboss_button.setCheckable(True)
        self.emboss_button.toggled.connect(self.apply_edits)
        pillow_filters_layout.addWidget(self.emboss_button)

        self.edge_enhance_button = QPushButton("Edge Enhance")
        self.edge_enhance_button.setCheckable(True)
        self.edge_enhance_button.toggled.connect(self.apply_edits)
        pillow_filters_layout.addWidget(self.edge_enhance_button)

        self.edge_enhance_more_button = QPushButton("Edge Enhance More")
        self.edge_enhance_more_button.setCheckable(True)
        self.edge_enhance_more_button.toggled.connect(self.apply_edits)
        pillow_filters_layout.addWidget(self.edge_enhance_more_button)

        self.find_edges_button = QPushButton("Find Edges")
        self.find_edges_button.setCheckable(True)
        self.find_edges_button.toggled.connect(self.apply_edits)
        pillow_filters_layout.addWidget(self.find_edges_button)

        self.detail_button = QPushButton("Detail")
        self.detail_button.setCheckable(True)
        self.detail_button.toggled.connect(self.apply_edits)
        pillow_filters_layout.addWidget(self.detail_button)

        self.smooth_button = QPushButton("Smooth")
        self.smooth_button.setCheckable(True)
        self.smooth_button.toggled.connect(self.apply_edits)
        pillow_filters_layout.addWidget(self.smooth_button)

        self.smooth_more_button = QPushButton("Smooth More")
        self.smooth_more_button.setCheckable(True)
        self.smooth_more_button.toggled.connect(self.apply_edits)
        pillow_filters_layout.addWidget(self.smooth_more_button)
        pillow_filters_layout.addStretch() # Push buttons to the right
        advanced_filters_layout.addLayout(pillow_filters_layout)

        # Scikit-image filter buttons (Edge Detection)
        scikit_edge_layout = QHBoxLayout()
        scikit_edge_layout.setSpacing(8)
        self.laplace_button = QPushButton("Laplace")
        self.laplace_button.setCheckable(True)
        self.laplace_button.toggled.connect(self.apply_edits)
        scikit_edge_layout.addWidget(self.laplace_button)

        self.sobel_button = QPushButton("Sobel")
        self.sobel_button.setCheckable(True)
        self.sobel_button.toggled.connect(self.apply_edits)
        scikit_edge_layout.addWidget(self.sobel_button)

        self.scharr_button = QPushButton("Scharr")
        self.scharr_button.setCheckable(True)
        self.scharr_button.toggled.connect(self.apply_edits)
        scikit_edge_layout.addWidget(self.scharr_button)

        self.prewitt_button = QPushButton("Prewitt")
        self.prewitt_button.setCheckable(True)
        self.prewitt_button.toggled.connect(self.apply_edits)
        scikit_edge_layout.addWidget(self.prewitt_button)

        self.roberts_button = QPushButton("Roberts")
        self.roberts_button.setCheckable(True)
        self.roberts_button.toggled.connect(self.apply_edits)
        scikit_edge_layout.addWidget(self.roberts_button)
        scikit_edge_layout.addStretch()
        advanced_filters_layout.addLayout(scikit_edge_layout)

        # Scikit-image filter buttons (Thresholding/Other)
        scikit_other_layout = QHBoxLayout()
        scikit_other_layout.setSpacing(8)
        self.gabor_button = QPushButton("Gabor")
        self.gabor_button.setCheckable(True)
        self.gabor_button.toggled.connect(self.apply_edits)
        scikit_other_layout.addWidget(self.gabor_button)

        self.otsu_button = QPushButton("Otsu Threshold")
        self.otsu_button.setCheckable(True)
        self.otsu_button.toggled.connect(self.apply_edits)
        scikit_other_layout.addWidget(self.otsu_button)

        self.niblack_button = QPushButton("Niblack Threshold")
        self.niblack_button.setCheckable(True)
        self.niblack_button.toggled.connect(self.apply_edits)
        scikit_other_layout.addWidget(self.niblack_button)

        self.sauvola_button = QPushButton("Sauvola Threshold")
        self.sauvola_button.setCheckable(True)
        self.sauvola_button.toggled.connect(self.apply_edits)
        scikit_other_layout.addWidget(self.sauvola_button)
        scikit_other_layout.addStretch()
        advanced_filters_layout.addLayout(scikit_other_layout)


        advanced_filters_layout.addStretch() # Push everything up

        self.sub_tabs.addTab(advanced_filters_tab, "Advanced Filters")


        # Buttons: Undo, Redo, Save, Save As, Back to Gallery
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8) # Reduced spacing between buttons

        self.undo_button = QPushButton("Undo")
        self.undo_button.clicked.connect(self.undo)
        self.undo_button.setEnabled(False) # Initially disabled
        self.undo_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed) # Fixed height
        button_layout.addWidget(self.undo_button)

        self.redo_button = QPushButton("Redo")
        self.redo_button.clicked.connect(self.redo)
        self.redo_button.setEnabled(False) # Initially disabled
        self.redo_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed) # Fixed height
        button_layout.addWidget(self.redo_button)

        # Reset button to clear all edits
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_edits)
        self.reset_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed) # Fixed height
        button_layout.addWidget(self.reset_button)

        button_layout.addStretch() # Push history buttons to the left, save/back to the right

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_image)
        self.save_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed) # Fixed height
        button_layout.addWidget(self.save_button)

        self.save_as_button = QPushButton("Save As")
        self.save_as_button.clicked.connect(self.save_image_as)
        self.save_as_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed) # Fixed height
        button_layout.addWidget(self.save_as_button)

        self.back_button = QPushButton("Back to Gallery")
        self.back_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed) # Fixed height
        button_layout.addWidget(self.back_button)  # Signal to be connected externally

        layout.addLayout(button_layout)

    def load_image(self, image_path):
        """Load image from path for editing."""
        self.image_path = image_path
        self.original_image = PIL.Image.open(image_path).convert('RGBA')
        self.edited_image = self.original_image.copy()
        self.reset_sliders()
        self.history.undo_stack.clear()
        self.history.redo_stack.clear()
        self.update_history_buttons() # New method to update button states
        self.update_image_display_widget() # Update the new display widget

    def update_image_display_widget(self):
        """Update the ImageDisplayWidget with the current edited image."""
        if self.edited_image is None:
            self.image_display_widget.setPixmap(QtGui.QPixmap()) # Clear pixmap
            self.image_display_widget.current_selection_mask = None # Clear mask
            return

        try:
            # Convert PIL image to QPixmap efficiently
            if self.edited_image.mode == "RGBA":
                 qt_image = QtGui.QImage(self.edited_image.tobytes("raw", "RGBA"), self.edited_image.width, self.edited_image.height, QtGui.QImage.Format_RGBA8888)
            elif self.edited_image.mode == "RGB":
                 qt_image = QtGui.QImage(self.edited_image.tobytes("raw", "RGB"), self.edited_image.width, self.edited_image.height, QtGui.QImage.Format_RGB888)
            elif self.edited_image.mode == "L": # Grayscale
                 qt_image = QtGui.QImage(self.edited_image.tobytes("raw", "L"), self.edited_image.width, self.edited_image.height, QtGui.QImage.Format_Grayscale8)
            else:
                 # Fallback: Convert to RGBA for display if mode is unusual
                 temp_img = self.edited_image.convert("RGBA")
                 qt_image = QtGui.QImage(temp_img.tobytes("raw", "RGBA"), temp_img.width, temp_img.height, QtGui.QImage.Format_RGBA8888)

            pixmap = QtGui.QPixmap.fromImage(qt_image)

            # Set the pixmap on the ImageDisplayWidget
            self.image_display_widget.setPixmap(pixmap)

            # The ImageDisplayWidget's paintEvent will draw the pixmap and the selection outline
            # The scroll area will handle scaling and panning based on the widget's size

        except Exception as e:
            print(f"Error updating image display widget: {e}")
            # Handle error, maybe set a placeholder text on the widget
            # self.image_display_widget.setText("Error displaying image") # ImageDisplayWidget is not a QLabel

    def reset_sliders(self):
        self.brightness_slider.setValue(100)
        self.contrast_slider.setValue(100)
        self.saturation_slider.setValue(100)
        self.sharpness_slider.setValue(100)
        self.gamma_slider.setValue(100)
        self.blur_slider.setValue(0)
        self.grayscale_button.setChecked(False)
        self.invert_button.setChecked(False)

    def apply_edits(self):
        """Apply all edits: brightness, contrast, saturation, sharpness, gamma, blur, grayscale, invert, and advanced filters."""
        if self.original_image is None:
            return
        img = self.original_image.copy()

        # Save current state to undo history before applying new edits
        if self.edited_image is not None:
            if not self.history.undo_stack or self.edited_image.tobytes() != self.history.undo_stack[-1].tobytes():
                self.history.push(self.edited_image)

        # Apply edits using modular functions with mask
        brightness_factor = self.brightness_slider.value() / 100.0
        contrast_factor = self.contrast_slider.value() / 100.0
        saturation_factor = self.saturation_slider.value() / 100.0
        sharpness_factor = self.sharpness_slider.value() / 100.0
        gamma_value = self.gamma_slider.value() / 100.0
        blur_radius = self.blur_slider.value()
        grayscale = self.grayscale_button.isChecked()
        invert = self.invert_button.isChecked()
        high_pass = self.high_pass_button.isChecked()
        hist_eq = self.hist_eq_button.isChecked()
        contour = self.contour_button.isChecked()
        noise = self.noise_button.isChecked()
        pencil_sketch = self.pencil_sketch_button.isChecked()
        sepia = self.sepia_button.isChecked()
        sharpen = self.sharpen_button.isChecked()
        border = self.border_button.isChecked()
        xray = self.xray_button.isChecked()

        img = adjust_brightness(img, brightness_factor)
        img = adjust_contrast(img, contrast_factor)
        img = adjust_saturation(img, saturation_factor)
        img = adjust_sharpness(img, sharpness_factor)
        img = apply_gamma_correction(img, gamma_value)
        img = apply_blur(img, blur_radius)
        if grayscale:
            img = apply_grayscale(img)
        if invert:
            img = apply_invert(img)
        if high_pass:
            img = apply_high_pass_filter(img)
        if hist_eq:
            img = apply_histogram_equalization(img)
        if contour:
            img = apply_contour_detection(img)
        if noise:
            img = add_gaussian_noise(img)
        if pencil_sketch:
            img = apply_pencil_sketch(img)
        if sepia:
            img = apply_sepia(img)
        if sharpen:
            img = apply_sharpen_filter(img)
        if border:
            border_size = 10  # Default border size, can be made adjustable
            img = add_border(img, border_size)  # Border likely applies to whole image, no mask param
        if xray:
            img = apply_xray_effect(img)

        # Apply new Pillow ImageFilter filters
        if self.emboss_button.isChecked():
            img = apply_emboss(img)
        if self.edge_enhance_button.isChecked():
            img = apply_edge_enhance(img)
        if self.edge_enhance_more_button.isChecked():
            img = apply_edge_enhance_more(img)
        if self.find_edges_button.isChecked():
            img = apply_find_edges(img)
        if self.detail_button.isChecked():
            img = apply_detail(img)
        if self.smooth_button.isChecked():
            img = apply_smooth(img)
        if self.smooth_more_button.isChecked():
            img = apply_smooth_more(img)

        # Apply new Scikit-image filters
        if self.laplace_button.isChecked():
            img = apply_laplace(img)
        if self.sobel_button.isChecked():
            img = apply_sobel(img)
        if self.scharr_button.isChecked():
            img = apply_scharr(img)
        if self.prewitt_button.isChecked():
            img = apply_prewitt(img)
        if self.roberts_button.isChecked():
            img = apply_roberts(img)
        if self.gabor_button.isChecked():
            # Gabor filter has a frequency parameter, using a default for now
            img = apply_gabor(img, frequency=0.6)  # No mask param in original, keep as is
        if self.otsu_button.isChecked():
            img = apply_otsu_threshold(img)  # No mask param in original, keep as is
        if self.niblack_button.isChecked():
            # Niblack threshold has window_size and k parameters, using defaults
            img = apply_niblack_threshold(img, window_size=25, k=0.8)  # No mask param in original
        if self.sauvola_button.isChecked():
            # Sauvola threshold has window_size and k parameters, using defaults
            img = apply_sauvola_threshold(img, window_size=25, k=0.8)  # No mask param in original


        self.edited_image = img
        self.update_image_display_widget()

    def update_history_buttons(self):
        """Updates the enabled state of undo/redo buttons."""
        self.undo_button.setEnabled(bool(self.history.undo_stack))
        self.redo_button.setEnabled(bool(self.history.redo_stack))

    def undo(self):
        """Undoes the last editing step."""
        if not self.history.undo_stack:
            return
        # Pass current image and mask to undo, get restored image and mask
        self.edited_image = self.history.undo(self.edited_image)
        self.update_image_display_widget()
        self.update_history_buttons()

    def redo(self):
        """Redoes the last undone editing step."""
        if not self.history.redo_stack:
            return
        # Pass current image and mask to redo, get restored image and mask
        self.edited_image = self.history.redo(self.edited_image)
        self.update_image_display_widget()
        self.update_history_buttons()

    def reset_edits(self):
        """Reset all edits and UI controls to original image."""
        if self.original_image is None:
            return
        self.reset_sliders()
        self.history.undo_stack.clear()
        self.history.redo_stack.clear()
        self.edited_image = self.original_image.copy()
        self.update_image_display_widget()
        self.update_history_buttons()

    def rotate_image(self, angle):
        """Rotates the image by the specified angle."""
        if self.edited_image is None:
            return
        self.history.push(self.edited_image)
        self.edited_image = rotate_image(self.edited_image, angle)
        self.update_image_display_widget()
        self.update_history_buttons()

    def apply_ai_enhance(self):
        """Applies AI image enhancement (placeholder)."""
        if self.edited_image is None:
            return
        self.history.push(self.edited_image)
        self.edited_image = ai_enhance(self.edited_image)
        self.update_image_display_widget()
        self.update_history_buttons()

    def remove_background(self):
        """Removes the image background using AI (placeholder)."""
        if self.edited_image is None:
            return
        self.history.push(self.edited_image)
        self.edited_image = remove_background(self.edited_image)
        self.update_image_display_widget()


    def save_image(self):
        """Save edits to the original image file."""
        if self.image_path and self.edited_image:
            try:
                # Determine original format for saving if possible
                original_format = PIL.Image.open(self.image_path).format
                save_kwargs = {}
                if original_format:
                    save_kwargs['format'] = original_format
                    # Preserve quality settings for JPEG if applicable
                    if original_format.upper() == 'JPEG':
                         # Try to get original quality, default if not found
                        try:
                             info = PIL.Image.open(self.image_path).info
                             quality = info.get('quality', 95) # Default 95 if not found
                             save_kwargs['quality'] = quality
                             save_kwargs['subsampling'] = info.get('subsampling', 0) # Default 0 (4:4:4)
                        except Exception:
                            save_kwargs['quality'] = 95 # Fallback quality

                # Convert back to original mode if necessary (e.g., if edited to RGBA but was JPG)
                # Be careful with transparency if original was not PNG/GIF etc.
                save_image = self.edited_image
                if original_format and original_format.upper() in ['JPEG', 'BMP']:
                    if save_image.mode == 'RGBA':
                        # Need to handle transparency before saving as JPEG/BMP
                        # Create a white background and paste RGBA image onto it
                        background = PIL.Image.new('RGB', save_image.size, (255, 255, 255))
                        background.paste(save_image, mask=save_image.split()[3]) # Paste using alpha channel as mask
                        save_image = background
                    elif save_image.mode == 'P': # Palette mode might cause issues
                        save_image = save_image.convert('RGB')

                save_image.save(self.image_path, **save_kwargs)

                QMessageBox.information(self, "Save Image", "Image saved successfully.")
                # Update original image to reflect saved changes
                self.original_image = self.edited_image.copy()
                # Reload gallery to reflect potential changes (like file size/date)
                if self.parent() and hasattr(self.parent(), 'load_gallery'):
                    self.parent().load_gallery() # Assuming parent is ImageManagerApp

            except Exception as e:
                QMessageBox.warning(self, "Save Image", f"Failed to save image: {e}")

    def save_image_as(self):
        """Save edits to a new file."""
        if self.edited_image is None:
            return
        options = QFileDialog.Options()
        # Suggest a filename based on the original
        suggested_name = "edited_" + os.path.basename(self.image_path) if self.image_path else "edited_image.png"
        default_dir = os.path.dirname(self.image_path) if self.image_path else "."

        file_path, selected_filter = QFileDialog.getSaveFileName(self, "Save Image As",
                                                                  os.path.join(default_dir, suggested_name),
                                                                  "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;BMP Files (*.bmp);;All Files (*)",
                                                                  options=options)
        if file_path:
            try:
                # Determine format from selected filter or file extension
                file_ext = os.path.splitext(file_path)[1].lower()
                save_format = None
                if 'png' in selected_filter.lower() or file_ext == '.png':
                    save_format = 'PNG'
                elif 'jpeg' in selected_filter.lower() or file_ext in ['.jpg', '.jpeg']:
                    save_format = 'JPEG'
                elif 'bmp' in selected_filter.lower() or file_ext == '.bmp':
                    save_format = 'BMP'
                # Add more formats if needed

                save_kwargs = {}
                if save_format:
                    save_kwargs['format'] = save_format
                    if save_format == 'JPEG':
                        save_kwargs['quality'] = 95 # Good default quality for JPEG

                # Handle transparency if saving to format that doesn't support it (like JPEG, BMP)
                save_image = self.edited_image
                if save_format in ['JPEG', 'BMP']:
                    if save_image.mode == 'RGBA':
                         background = PIL.Image.new('RGB', save_image.size, (255, 255, 255))
                         background.paste(save_image, mask=save_image.split()[3])
                         save_image = background
                    elif save_image.mode == 'P':
                        save_image = save_image.convert('RGB')

                save_image.save(file_path, **save_kwargs)
                QMessageBox.information(self, "Save Image As", f"Image saved successfully as {os.path.basename(file_path)}.")
                 # Optionally reload gallery if saved within the gallery folder
                if self.parent() and hasattr(self.parent(), 'image_folder'):
                    if os.path.dirname(file_path) == self.parent().image_folder:
                        self.parent().load_gallery() # Reload gallery if saved in the same folder

            except Exception as e:
                QMessageBox.warning(self, "Save Image As", f"Failed to save image: {e}")

    # Removed paintEvent override in ImageEditTab related to selection drawing




class ImageManagerApp(QtWidgets.QWidget):
    """
A complete Qt application for managing images in the 'genimage' folder.

Features:
- Gallery view with thumbnails of images in 'genimage'
- Image preview with zoom in/out and mouse wheel zoom
- Set as wallpaper and cancel buttons
- Image management: delete and rename images
- Separate image editing tab with basic editing functions
"""

    def __init__(self, app, image_folder='genimage', set_wallpaper_callback=None):
        super().__init__()
        self.app = app # Store the QApplication instance
        self.image_folder = image_folder
        self.set_wallpaper_callback = set_wallpaper_callback
        self.result = False
        self.current_image_path = None
        self.scale_factor = 1.0
        self.original_pixmap = None # Initialize original_pixmap

        # Pagination settings
        self.batch_size = 50
        self.current_batch = 1
        self.all_image_paths = []  # All image paths in the folder
        self.displayed_images = []  # Currently displayed image paths

        self.init_ui()
        self.load_gallery()
        # Select the first image only if the gallery is not empty
        if self.gallery_list.count() > 0:
             self.gallery_list.setCurrentRow(0) # This triggers on_gallery_selection_changed
        else:
             self.update_status_label() # Ensure status label is correct if folder is empty


    def init_ui(self):
        # --- Dynamically size window and show minimize/maximize/close buttons ---
        # Get available screen geometry
        screen = QtWidgets.QApplication.primaryScreen()
        if screen is not None:
            geo = screen.availableGeometry()
            avail_width, avail_height = geo.width(), geo.height()
        else:
            # fallback
            avail_width, avail_height = 1280, 720

        # Choose window size: conservative default, must fit display
        init_width = min(1000, avail_width - 64)
        init_height = min(700, avail_height - 64)

        # Apply ideal window flags for standard decorations/buttons
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.WindowMinMaxButtonsHint |
            QtCore.Qt.WindowCloseButtonHint
        )
        self.setWindowTitle("Image Manager")
        self.resize(init_width, init_height)
        # Only set max if needed (e.g., > display), but do not shrink below screen available geometry
        self.setMaximumSize(avail_width, avail_height)
        self.setMinimumSize(600, 400)  # Prevent tiny window, but allow further resizing
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        # Set dark background color and add gradient background
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e; /* Darker background */
                color: #e0e0e0; /* Light grey text */
                font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
                font-size: 10pt;
            }
            QLabel {
                color: #e0e0e0;
            }
            QLabel#titleLabel {
                color: #ffffff; /* White title */
                font-weight: bold;
                font-size: 14pt; /* Slightly smaller title */
                margin-bottom: 8px;
                padding-bottom: 4px;
                border-bottom: 1px solid #3a3a3a; /* Subtle separator */
            }
            QLabel#statusLabel {
                font-style: italic;
                color: #aaaaaa; /* Muted status text */
                font-size: 9pt;
            }
            QListWidget {
                background-color: #2a2a2a; /* Slightly lighter dark */
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 4px;
            }
            QListWidget::item {
                padding: 6px;
                margin: 1px;
                border-bottom: 1px solid #3a3a3a; /* Separator between items */
                color: #e0e0e0; /* Ensure item text is light */
            }
            QListWidget::item:last {
                border-bottom: none; /* No separator for the last item */
            }
            QListWidget::item:selected {
                background-color: #0078d7; /* Standard blue selection */
                color: white;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #0078d7; /* Standard blue */
                color: white;
                font-size: 10pt;
                border: none;
                padding: 6px 12px; /* Increased padding */
                border-radius: 4px; /* Slightly smaller radius */
                min-width: 80px; /* Reduced min width slightly */
                min-height: 24px; /* Reduced min height slightly */
            }
            QPushButton:hover {
                background-color: #005a9e; /* Darker blue on hover */
            }
            QPushButton:pressed {
                background-color: #004a7c; /* Even darker on press */
            }
            QPushButton:disabled {
                background-color: #3a3a3a; /* Dark grey when disabled */
                color: #888888; /* Grey text when disabled */
            }
            QLineEdit {
                background-color: #2a2a2a;
                border: 1px solid #555555;
                border-radius: 4px;
                color: #e0e0e0;
                padding: 4px 8px;
                font-size: 10pt;
            }
            QSlider::groove:horizontal {
                border: 1px solid #555555;
                height: 6px; /* Reduced height */
                background: #3a3a3a;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #0078d7;
                border: 1px solid #555555;
                width: 14px; /* Reduced handle size */
                height: 14px;
                margin: -4px 0; /* Center handle vertically */
                border-radius: 7px;
            }
            QSlider::add-page:horizontal {
                background: #555555;
            }
            QSlider::sub-page:horizontal {
                background: #0078d7;
            }
            QScrollArea {
                border: 1px solid #555555;
                border-radius: 4px;
                background-color: #2a2a2a; /* Match list widget background */
            }
            /* Style the viewport specifically */
            QScrollArea > QWidget > QWidget {
                 background-color: #2a2a2a; /* Match scroll area background */
            }
            QGroupBox {
                 border: 1px solid #555555;
                 border-radius: 4px;
                 margin-top: 10px; /* Space for title */
                 font-weight: bold;
                 color: #e0e0e0;
            }
            QGroupBox::title {
                 subcontrol-origin: margin;
                 subcontrol-position: top left;
                 padding: 0 5px 0 5px;
                 left: 10px; /* Position title slightly indented */
                 background-color: #1e1e1e; /* Match window background */
            }
            QComboBox {
                 background-color: #2a2a2a;
                 border: 1px solid #555555;
                 border-radius: 3px;
                 padding: 2px 18px 2px 5px; /* Padding for text and arrow */
                 min-width: 6em; /* Minimum width */
                 color: #e0e0e0;
            }
            QComboBox::drop-down {
                 subcontrol-origin: padding;
                 subcontrol-position: top right;
                 width: 15px;
                 border-left-width: 1px;
                 border-left-color: #555555;
                 border-left-style: solid;
                 border-top-right-radius: 3px;
                 border-bottom-right-radius: 3px;
                 background-color: #3a3a3a;
            }
            QComboBox::down-arrow {
                 image: url(:/qt-project.org/styles/commonstyle/images/standardbutton-down-16.png); /* Use a standard arrow */
                 width: 10px;
                 height: 10px;
            }
            QComboBox QAbstractItemView { /* Style the dropdown list */
                 background-color: #2a2a2a;
                 border: 1px solid #555555;
                 selection-background-color: #0078d7;
                 color: #e0e0e0;
            }
            QTabWidget::pane { /* The tab widget frame */
                 border-top: 1px solid #555555;
                 margin-top: -1px; /* Align pane border with tab bar bottom */
            }
            QTabBar::tab { /* The tab buttons */
                 background: #2a2a2a;
                 border: 1px solid #555555;
                 border-bottom-color: #555555; /* Match pane border */
                 border-top-left-radius: 4px;
                 border-top-right-radius: 4px;
                 min-width: 8ex;
                 padding: 5px 10px;
                 color: #aaaaaa; /* Non-selected tab text color */
            }
            QTabBar::tab:selected, QTabBar::tab:hover {
                 background: #1e1e1e; /* Match window background for selected tab */
                 color: #e0e0e0; /* Selected tab text color */
                 border-color: #555555;
                 border-bottom-color: #1e1e1e; /* Make selected tab blend into pane */
            }
            QTabBar::tab:!selected {
                 margin-top: 2px; /* Make non-selected tabs look slightly recessed */
            }
        """)

        # Main layout with tabs
        self.tabs = QTabWidget()
        self.main_tab = QWidget()
        # Pass self (ImageManagerApp) as parent to ImageEditTab
        self.edit_tab = ImageEditTab(parent=self)
        # Connect the back button signal
        self.edit_tab.back_button.clicked.connect(self.on_back_to_gallery)

        self.tabs.addTab(self.main_tab, "Gallery")
        self.tabs.addTab(self.edit_tab, "Edit Image")
        self.tabs.setTabVisible(1, False)  # Hide edit tab initially

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.tabs)

        # Setup main tab UI
        self.setup_main_tab_ui()

    def setup_main_tab_ui(self):
        layout = QHBoxLayout(self.main_tab)
        # Adjust margins and spacing for better visual separation
        layout.setContentsMargins(12, 12, 12, 12) # Slightly reduced margins
        layout.setSpacing(12) # Slightly reduced spacing

        # Left pane: Gallery list
        gallery_layout = QVBoxLayout()
        gallery_label = QLabel("Gallery")
        gallery_label.setObjectName("titleLabel")
        gallery_layout.addWidget(gallery_label)

        # Sort options combo box
        sort_layout = QHBoxLayout()
        sort_label = QLabel("Sort by:")
        sort_label.setStyleSheet("color: #e0e0e0; font: 10pt 'Segoe UI';") # Adjusted font size
        sort_layout.addWidget(sort_label)
        self.sort_combo = QtWidgets.QComboBox()
        self.sort_combo.addItems(["Name Asc", "Name Desc", "Date Modified", "Size"])
        self.sort_combo.currentIndexChanged.connect(self.load_gallery)
        sort_layout.addWidget(self.sort_combo)
        sort_layout.addStretch()
        gallery_layout.addLayout(sort_layout)

        self.gallery_list = QtWidgets.QListWidget()
        self.gallery_list.setIconSize(QSize(100, 100))
        self.gallery_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.gallery_list.itemSelectionChanged.connect(self.on_gallery_selection_changed)
        gallery_layout.addWidget(self.gallery_list, stretch=1)

        # Load more button
        self.load_more_button = QPushButton("Load More Images")
        self.load_more_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed) # Fixed height
        self.load_more_button.clicked.connect(self.load_next_batch)
        self.load_more_button.setEnabled(False)  # Initially disabled until we know there are more to load
        gallery_layout.addWidget(self.load_more_button)

        # Management buttons for gallery
        gallery_button_layout = QHBoxLayout()
        gallery_button_layout.setSpacing(8) # Reduced spacing between buttons
        self.delete_button = QPushButton("Delete")
        self.delete_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed) # Fixed height
        self.delete_button.clicked.connect(self.delete_selected_image)
        self.delete_button.setEnabled(False)
        gallery_button_layout.addWidget(self.delete_button)
        self.rename_button = QPushButton("Rename")
        self.rename_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed) # Fixed height
        self.rename_button.clicked.connect(self.rename_selected_image)
        self.rename_button.setEnabled(False)
        gallery_button_layout.addWidget(self.rename_button)
        self.edit_button = QPushButton("Edit Image")
        self.edit_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed) # Fixed height
        self.edit_button.clicked.connect(self.open_edit_tab)
        self.edit_button.setEnabled(False)
        gallery_button_layout.addWidget(self.edit_button)

        # Add Open button
        self.open_button = QPushButton("Open Image")
        self.open_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed) # Fixed height
        self.open_button.clicked.connect(self.open_image_dialog)
        gallery_button_layout.addWidget(self.open_button)

        gallery_layout.addLayout(gallery_button_layout)

        # Gallery sidebar sizing
        gallery_layout.setContentsMargins(0, 0, 0, 0) # Let the main layout handle outer margins
        self.gallery_list.setMinimumWidth(150) # Reduced minimum width
        self.gallery_list.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        layout.addLayout(gallery_layout, stretch=1)

        # Right pane: Preview and controls
        preview_layout = QVBoxLayout()
        self.preview_title_label = QLabel("Preview")
        self.preview_title_label.setObjectName("titleLabel")
        preview_layout.addWidget(self.preview_title_label)

        # Use PannableScrollArea for zoom and pan
        # THIS IS THE LINE THAT CAUSED THE ERROR - IT SHOULD WORK NOW
        self.scroll_area = PannableScrollArea()
        self.scroll_area.setBackgroundRole(QtGui.QPalette.Dark)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignCenter) # Center the image when smaller than scroll area
        # Apply scroll area specific style from main stylesheet
        # self.scroll_area.setStyleSheet(...) # Not needed if covered by main QScrollArea style

        # Replaced QLabel with ImageDisplayWidget for image display and selection
        self.image_display_widget = ImageDisplayWidget()
        self.scroll_area.setWidget(self.image_display_widget)

        # Preview width: adaptive based on window size, moderately large for clarity
        self.scroll_area.setMinimumSize(320, 200)
        self.scroll_area.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # Shadow effect on the scroll area, not the label inside
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8) # Reduced blur radius
        shadow.setColor(QColor(0, 0, 0, 150)) # Slightly less opaque shadow
        shadow.setOffset(0, 2) # Offset shadow slightly downwards
        self.scroll_area.setGraphicsEffect(shadow)

        preview_layout.addWidget(self.scroll_area, stretch=1)

        self.status_label = QLabel("")
        self.status_label.setObjectName("statusLabel")
        status_font = QtGui.QFont("Segoe UI", 9, QtGui.QFont.StyleItalic) # Adjusted font size
        self.status_label.setFont(status_font)
        preview_layout.addWidget(self.status_label)

        # Add labels for image information
        self.info_filename_label = QLabel("")
        self.info_resolution_label = QLabel("")
        self.info_size_label = QLabel("")
        info_font = QtGui.QFont("Segoe UI", 9) # Adjusted font size
        self.info_filename_label.setFont(info_font)
        self.info_resolution_label.setFont(info_font)
        self.info_size_label.setFont(info_font)
        # Ensure info labels have light text color explicitly if needed
        self.info_filename_label.setStyleSheet("color: #e0e0e0;")
        self.info_resolution_label.setStyleSheet("color: #e0e0e0;")
        self.info_size_label.setStyleSheet("color: #e0e0e0;")


        info_layout = QVBoxLayout()
        info_layout.setSpacing(2) # Reduced spacing between info labels
        info_layout.addWidget(self.info_filename_label)
        info_layout.addWidget(self.info_resolution_label)
        info_layout.addWidget(self.info_size_label)
        # info_layout.addStretch() # Removed stretch to keep info labels grouped

        preview_layout.addLayout(info_layout) # Moved info_layout below status_label


        # Zoom buttons
        zoom_layout = QHBoxLayout()
        zoom_layout.setSpacing(8) # Reduced spacing
        self.zoom_out_button = QPushButton("-")
        self.zoom_out_button.setMinimumSize(28, 28) # Adjusted size
        self.zoom_out_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed) # Fixed size
        self.zoom_out_button.setToolTip("Zoom Out (Mouse Wheel Down)")
        self.zoom_out_button.clicked.connect(self.zoom_out)
        zoom_layout.addWidget(self.zoom_out_button)
        self.zoom_in_button = QPushButton("+")
        self.zoom_in_button.setMinimumSize(28, 28) # Adjusted size
        self.zoom_in_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed) # Fixed size
        self.zoom_in_button.setToolTip("Zoom In (Mouse Wheel Up)")
        self.zoom_in_button.clicked.connect(self.zoom_in)
        zoom_layout.addWidget(self.zoom_in_button)

        # Add Fit button for preview area
        self.fit_button = QPushButton("Fit")
        self.fit_button.setMinimumSize(50, 28) # Adjusted size
        self.fit_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed) # Fixed size
        self.fit_button.setToolTip("Zoom to Fit Preview Area")
        self.fit_button.clicked.connect(self.zoom_to_fit)
        zoom_layout.addWidget(self.fit_button)

        zoom_layout.addStretch()
        preview_layout.addLayout(zoom_layout)

        # Wallpaper/cancel buttons
        action_layout = QHBoxLayout()
        action_layout.setSpacing(8) # Reduced spacing between buttons
        action_layout.addStretch() # Push buttons to the right
        self.set_button = QPushButton("Set as Wallpaper")
        self.set_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed) # Fixed height
        self.set_button.clicked.connect(self.set_wallpaper)
        self.set_button.setEnabled(False)
        action_layout.addWidget(self.set_button)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed) # Fixed height
        self.cancel_button.clicked.connect(self.cancel)
        action_layout.addWidget(self.cancel_button)
        preview_layout.addLayout(action_layout)

        layout.addLayout(preview_layout, stretch=3)

        # Mouse event handling for panning is now done within the PannableScrollArea class
        # self.last_mouse_pos = None # No longer needed here
        # self.scroll_area.setMouseTracking(True) # Handled in PannableScrollArea


    def keyPressEvent(self, event):
        """Handles key press events for navigation."""
        if event.key() == Qt.Key_Up or event.key() == Qt.Key_Left:
            current_row = self.gallery_list.currentRow()
            if current_row > 0:
                self.gallery_list.setCurrentRow(current_row - 1)
            elif self.gallery_list.count() > 0:
                # Wrap around to the last item
                self.gallery_list.setCurrentRow(self.gallery_list.count() - 1)
            event.accept()
        elif event.key() == Qt.Key_Down or event.key() == Qt.Key_Right:
            current_row = self.gallery_list.currentRow()
            if current_row < self.gallery_list.count() - 1:
                self.gallery_list.setCurrentRow(current_row + 1)
            elif self.gallery_list.count() > 0:
                # Wrap around to the first item
                self.gallery_list.setCurrentRow(0)
            event.accept()
        # Add Delete key shortcut
        elif event.key() == Qt.Key_Delete:
             if self.delete_button.isEnabled():
                 self.delete_selected_image()
                 event.accept()
        # Add Enter key shortcut for Set Wallpaper
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
             if self.set_button.isEnabled():
                 self.set_wallpaper()
                 event.accept()
        else:
            super().keyPressEvent(event)

    def load_gallery(self):
        """Load images from the image folder into the gallery list, preserving selection if possible."""
        current_selection_path = self.current_image_path # Store current selection before clearing

        # Clear existing items but store their paths first
        existing_paths = [self.gallery_list.item(i).data(Qt.UserRole) for i in range(self.gallery_list.count())]
        self.gallery_list.clear()
        self.all_image_paths = []
        # No need to clear image_list or displayed_images here, load_batch_images handles it

        if not os.path.exists(self.image_folder):
            try:
                os.makedirs(self.image_folder)
            except OSError as e:
                 QMessageBox.critical(self, "Error", f"Could not create image folder: {self.image_folder}\n{e}")
                 self.close()
                 return

        # Scan directory for images
        for filename in os.listdir(self.image_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                full_path = os.path.join(self.image_folder, filename)
                self.all_image_paths.append(full_path)

        self.sort_all_images() # Sort the full list

        # Reset batching and load the first batch
        self.current_batch = 1
        self.load_batch_images() # This populates gallery_list and displayed_images

        # Try to restore selection
        restored_selection = False
        if current_selection_path and current_selection_path in self.displayed_images:
            # Find the item in the *new* list
            for i in range(self.gallery_list.count()):
                item = self.gallery_list.item(i)
                if item.data(Qt.UserRole) == current_selection_path:
                    self.gallery_list.setCurrentRow(i)
                    restored_selection = True
                    break

        # If selection couldn't be restored (e.g., deleted or not in first batch), select first item if available
        if not restored_selection and self.gallery_list.count() > 0:
            self.gallery_list.setCurrentRow(0)
        elif not restored_selection and self.gallery_list.count() == 0:
             # If gallery is now empty, clear preview and disable buttons
             self.image_label.clear()
             self.current_image_path = None
             self.original_pixmap = None
             self.info_filename_label.setText("")
             self.info_resolution_label.setText("")
             self.info_size_label.setText("")
             self.delete_button.setEnabled(False)
             self.rename_button.setEnabled(False)
             self.set_button.setEnabled(False)
             self.edit_button.setEnabled(False)


        self.update_status_label()
        self.update_load_more_button_state()


    def update_status_label(self):
        """Updates the status label with gallery information."""
        total_images = len(self.all_image_paths)
        displayed_count = len(self.displayed_images)
        if total_images > 0:
            status = f"Displaying {displayed_count} of {total_images} images."
            if self.current_image_path:
                 status += f" Selected: {os.path.basename(self.current_image_path)}"
            self.status_label.setText(status)
        else:
            self.status_label.setText("No images found in gallery folder.")


    def on_gallery_selection_changed(self):
        selected_items = self.gallery_list.selectedItems()
        if not selected_items:
            # Don't clear everything if selection is temporarily lost (e.g., during reload)
            # Only disable buttons if selection is truly gone
            # self.current_image_path = None
            # self.image_display_widget.clear()
            # self.status_label.setText("No image selected.")
            self.delete_button.setEnabled(False)
            self.rename_button.setEnabled(False)
            self.set_button.setEnabled(False)
            self.edit_button.setEnabled(False)
            return

        selected_item = selected_items[0]
        # Use data role to store the full path robustly
        image_path = selected_item.data(Qt.UserRole)

        # Check if the path is valid before proceeding
        if not image_path or not os.path.exists(image_path):
             QMessageBox.warning(self, "Error", f"Selected image path is invalid or file not found:\n{image_path}")
             # Attempt to remove the invalid item or reload
             if image_path in self.all_image_paths: self.all_image_paths.remove(image_path)
             if image_path in self.displayed_images: self.displayed_images.remove(image_path)
             row = self.gallery_list.row(selected_item)
             self.gallery_list.takeItem(row)
             self.update_status_label()
             return


        self.select_image(image_path)
        self.delete_button.setEnabled(True)
        self.rename_button.setEnabled(True)
        self.set_button.setEnabled(True)
        self.edit_button.setEnabled(True)

    def select_image(self, image_path):
        if not os.path.exists(image_path):
            self.status_label.setText(f"Error: File not found: {os.path.basename(image_path)}")
            self.image_label.clear()
            self.original_pixmap = None
            self.set_button.setEnabled(False)
            self.current_image_path = None # Ensure current path is cleared on error
             # Clear info labels on error
            self.info_filename_label.setText("")
            self.info_resolution_label.setText("")
            self.info_size_label.setText("")
            return

        pixmap = QtGui.QPixmap(image_path)
        if pixmap.isNull():
            self.status_label.setText(f"Error loading image: {os.path.basename(image_path)} (unsupported/corrupted?)")
            self.image_label.clear()
            self.original_pixmap = None
            self.set_button.setEnabled(False)
            self.current_image_path = None # Ensure current path is cleared on error
             # Clear info labels on error
            self.info_filename_label.setText("")
            self.info_resolution_label.setText("")
            self.info_size_label.setText("")
            return

        self.current_image_path = image_path
        self.original_pixmap = pixmap # Store the original full-resolution pixmap
        self.scale_factor = 1.0 # Reset scale factor for new image
        # self.update_image_display() # Update display is called by zoom_to_fit
        self.zoom_to_fit() # Automatically fit new image to preview area
        self.update_status_label() # Update status label with new selection
        self.set_button.setEnabled(True)

        # Update image information labels
        try:
            # Use QPixmap for resolution to avoid reloading with PIL unless needed
            width = pixmap.width()
            height = pixmap.height()
            self.info_filename_label.setText(f"File: {os.path.basename(image_path)}")
            self.info_resolution_label.setText(f"Resolution: {width}x{height}")
            # Format file size nicely
            size_bytes = os.path.getsize(image_path)
            if size_bytes < 1024:
                size_str = f"{size_bytes} B"
            elif size_bytes < 1024 * 1024:
                size_str = f"{size_bytes / 1024:.2f} KB"
            else:
                size_str = f"{size_bytes / (1024 * 1024):.2f} MB"
            self.info_size_label.setText(f"Size: {size_str}")
        except Exception as e:
            self.info_filename_label.setText(f"File: {os.path.basename(image_path)}")
            self.info_resolution_label.setText("Resolution: N/A")
            self.info_size_label.setText("Size: N/A")
            print(f"Error reading image info: {e}")


    def update_image_display(self):
        if self.current_image_path and self.original_pixmap and not self.original_pixmap.isNull():
            # Ensure scale factor is reasonable
            self.scale_factor = max(0.01, self.scale_factor) # Prevent zero or negative scale

            # Calculate the size of the pixmap based on the current scale factor
            scaled_size = self.original_pixmap.size() * self.scale_factor
            # Check for potentially huge sizes to prevent performance issues/crashes
            max_dim = 16384 # Example limit, adjust as needed
            if scaled_size.width() > max_dim or scaled_size.height() > max_dim:
                 # If scaled size is too large, clamp scale factor
                 scale_x = max_dim / self.original_pixmap.width() if self.original_pixmap.width() > 0 else 1
                 scale_y = max_dim / self.original_pixmap.height() if self.original_pixmap.height() > 0 else 1
                 self.scale_factor = min(scale_x, scale_y, self.scale_factor)
                 scaled_size = self.original_pixmap.size() * self.scale_factor


            # Use SmoothTransformation for better quality when scaling down
            # Use FastTransformation when scaling up significantly? (Test performance)
            transform_mode = QtCore.Qt.SmoothTransformation # Generally good default

            scaled_pixmap = self.original_pixmap.scaled(scaled_size, QtCore.Qt.KeepAspectRatio, transform_mode)

            self.image_display_widget.setPixmap(scaled_pixmap)
            # Resize the label to the scaled pixmap size so the scroll area knows when to show scrollbars
            self.image_display_widget.resize(scaled_pixmap.size())

            # Panning is handled by PannableScrollArea and QScrollArea itself
        else:
             # Clear label if no valid image/pixmap
             self.image_display_widget.clear()
             self.image_display_widget.resize(1,1) # Reset size


    def zoom_to_fit(self):
        """Scales the image to exactly fit the preview scroll area."""
        if not self.original_pixmap or self.original_pixmap.isNull():
             return

        # Get the size of the scroll area's viewport, accounting for scrollbars
        viewport_size = self.scroll_area.viewport().size()
        # Subtract approx scrollbar width/height if they are visible (conservative estimate)
        vsb_policy = self.scroll_area.verticalScrollBarPolicy()
        hsb_policy = self.scroll_area.horizontalScrollBarPolicy()
        sb_width = self.scroll_area.verticalScrollBar().width() if vsb_policy != Qt.ScrollBarAlwaysOff else 0
        sb_height = self.scroll_area.horizontalScrollBar().height() if hsb_policy != Qt.ScrollBarAlwaysOff else 0

        available_width = max(1, viewport_size.width() - sb_width)
        available_height = max(1, viewport_size.height() - sb_height)


        pixmap_size = self.original_pixmap.size()
        if pixmap_size.width() <= 0 or pixmap_size.height() <= 0:
             return # Avoid division by zero

        width_scale = available_width / pixmap_size.width()
        height_scale = available_height / pixmap_size.height()

        # Use the smaller scale factor to ensure the whole image fits
        self.scale_factor = min(width_scale, height_scale)

        # Ensure the image isn't scaled *larger* than 100% if it already fits
        self.scale_factor = min(self.scale_factor, 1.0)


        self.update_image_display()
         # After fitting, reset scrollbars to top-left
        self.scroll_area.horizontalScrollBar().setValue(0)
        self.scroll_area.verticalScrollBar().setValue(0)


    def zoom_in(self):
        """Increases the image scale factor for zooming in."""
        # Store center point before zoom
        center_h = self.scroll_area.horizontalScrollBar().value() + self.scroll_area.viewport().width() / 2
        center_v = self.scroll_area.verticalScrollBar().value() + self.scroll_area.viewport().height() / 2
        old_scale = self.scale_factor

        self.scale_factor *= 1.25
        self.update_image_display()

        # Adjust scrollbars to keep the center point
        new_h = center_h * (self.scale_factor / old_scale) - self.scroll_area.viewport().width() / 2
        new_v = center_v * (self.scale_factor / old_scale) - self.scroll_area.viewport().height() / 2
        self.scroll_area.horizontalScrollBar().setValue(int(new_h))
        self.scroll_area.verticalScrollBar().setValue(int(new_v))


    def zoom_out(self):
        """Decreases the image scale factor for zooming out."""
         # Store center point before zoom
        center_h = self.scroll_area.horizontalScrollBar().value() + self.scroll_area.viewport().width() / 2
        center_v = self.scroll_area.verticalScrollBar().value() + self.scroll_area.viewport().height() / 2
        old_scale = self.scale_factor

        new_scale_factor = self.scale_factor / 1.25

        # Optional: Check against fit size to prevent zooming out too far
        # viewport_size = self.scroll_area.viewport().size()
        # pixmap_size = self.original_pixmap.size()
        # if pixmap_size.width() > 0 and pixmap_size.height() > 0:
        #     fit_width_scale = viewport_size.width() / pixmap_size.width()
        #     fit_height_scale = viewport_size.height() / pixmap_size.height()
        #     min_scale = min(fit_width_scale, fit_height_scale)
        #     # Don't zoom out smaller than fitting the screen, maybe with a small margin
        #     if new_scale_factor < min_scale * 0.9:
        #          return # Or set scale_factor = min_scale

        self.scale_factor = new_scale_factor
        self.update_image_display()

        # Adjust scrollbars to keep the center point
        new_h = center_h * (self.scale_factor / old_scale) - self.scroll_area.viewport().width() / 2
        new_v = center_v * (self.scale_factor / old_scale) - self.scroll_area.viewport().height() / 2
        self.scroll_area.horizontalScrollBar().setValue(int(new_h))
        self.scroll_area.verticalScrollBar().setValue(int(new_v))


    def wheelEvent(self, event):
        """Handles mouse wheel scrolling for zooming, restricted to the scroll area."""
        # Check if the mouse pointer is over the scroll area widget
        if self.scroll_area.underMouse():
            # Check if Ctrl key is pressed (optional modifier for zoom)
            # modifiers = QtWidgets.QApplication.keyboardModifiers()
            # if modifiers == QtCore.Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoom_in()
            else:
                self.zoom_out()
            event.accept() # Accept the event to prevent it propagating further
        else:
            # If not over the scroll area, let the base class handle it (e.g., scrolling the list widget)
            super().wheelEvent(event)


    def sort_all_images(self):
        if not self.all_image_paths:
            return
        sort_option = self.sort_combo.currentText()
        metadata_list = []
        for path in self.all_image_paths:
            try:
                stat = os.stat(path)
                metadata_list.append({
                    'path': path,
                    'name': os.path.basename(path).lower(), # Lowercase for case-insensitive sort
                    'mtime': stat.st_mtime,
                    'size': stat.st_size
                })
            except Exception as e:
                 print(f"Warning: Could not stat file {path}: {e}")
                 # Add with default values so it doesn't break sorting entirely
                 metadata_list.append({
                    'path': path,
                    'name': os.path.basename(path).lower(),
                    'mtime': 0,
                    'size': 0
                })
        if sort_option == "Name Asc":
            metadata_list.sort(key=lambda x: x['name'])
        elif sort_option == "Name Desc":
            metadata_list.sort(key=lambda x: x['name'], reverse=True)
        elif sort_option == "Date Modified":
            metadata_list.sort(key=lambda x: x['mtime'], reverse=True)
        elif sort_option == "Size":
            metadata_list.sort(key=lambda x: x['size'], reverse=True)
        else: # Default to Name Asc
            metadata_list.sort(key=lambda x: x['name'])
        self.all_image_paths = [item['path'] for item in metadata_list]

    def load_batch_images(self):
        start_idx = (self.current_batch - 1) * self.batch_size
        end_idx = start_idx + self.batch_size # Slice includes start, excludes end
        batch_paths = self.all_image_paths[start_idx:end_idx]

        # If it's the first batch, clear the list completely
        if self.current_batch == 1:
             self.gallery_list.clear()
             self.displayed_images = []

        # Add new batch items
        for path in batch_paths:
             if path not in self.displayed_images: # Avoid duplicates if logic allows
                 icon = QtGui.QIcon(path)
                 filename = os.path.basename(path)
                 list_item = QtWidgets.QListWidgetItem(icon, filename)
                 list_item.setData(Qt.UserRole, path) # Store full path in item data
                 self.gallery_list.addItem(list_item)
                 self.displayed_images.append(path)


        # No need to reset selection here, load_gallery handles initial selection logic
        # self.update_status_label() # Called by load_gallery or load_next_batch
        self.update_load_more_button_state()

    def load_next_batch(self):
        """Increments batch number and loads the next batch of images."""
        if self.current_batch * self.batch_size < len(self.all_image_paths):
            self.current_batch += 1
            self.load_batch_images()
            self.update_status_label() # Update status after adding more images


    def update_load_more_button_state(self):
        """Enables/disables the load more button based on remaining images."""
        if len(self.displayed_images) < len(self.all_image_paths):
            self.load_more_button.setEnabled(True)
            self.load_more_button.setText(f"Load More ({len(self.all_image_paths) - len(self.displayed_images)} remaining)")
        else:
            self.load_more_button.setEnabled(False)
            self.load_more_button.setText("Load More Images")


    def delete_selected_image(self):
        """Deletes the currently selected image file."""
        selected_items = self.gallery_list.selectedItems()
        if not selected_items:
            return
        selected_item = selected_items[0]
        # Use stored path from item data
        image_path = selected_item.data(Qt.UserRole)
        image_name = os.path.basename(image_path)

        reply = QMessageBox.question(self, 'Delete Image',
                                     f"Are you sure you want to delete '{image_name}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                os.remove(image_path)
                # QMessageBox.information(self, "Delete Image", f"'{image_name}' deleted successfully.") # Can be annoying
                # Remove from internal lists before reloading gallery
                if image_path in self.all_image_paths: self.all_image_paths.remove(image_path)
                if image_path in self.displayed_images: self.displayed_images.remove(image_path)
                # Remove from QListWidget directly
                row = self.gallery_list.row(selected_item)
                self.gallery_list.takeItem(row)
                 # After removing, update counts and potentially select the next item
                if row >= self.gallery_list.count() and self.gallery_list.count() > 0:
                     row = self.gallery_list.count() - 1 # Select last item if previous last was deleted
                if self.gallery_list.count() > 0:
                     self.gallery_list.setCurrentRow(row) # Select next/previous item
                else:
                     # Gallery is now empty
                     self.on_gallery_selection_changed() # Trigger update for empty state


                self.update_status_label()
                self.update_load_more_button_state() # Update button state after deletion

            except Exception as e:
                QMessageBox.warning(self, "Delete Image", f"Failed to delete image:\n{e}")

    def rename_selected_image(self):
        """Renames the currently selected image file."""
        selected_items = self.gallery_list.selectedItems()
        if not selected_items:
            return
        selected_item = selected_items[0]
        # Use stored path from item data
        current_image_path = selected_item.data(Qt.UserRole)
        current_image_name = os.path.basename(current_image_path)
        current_dir = os.path.dirname(current_image_path)


        new_name, ok = QtWidgets.QInputDialog.getText(self, "Rename Image", "Enter new name:",
                                                      QtWidgets.QLineEdit.Normal, current_image_name)

        if ok and new_name and new_name != current_image_name:
             # Basic validation for new name (e.g., prevent invalid characters)
            if any(c in new_name for c in r'/\:*?"<>|'):
                 QMessageBox.warning(self, "Rename Image", "New name contains invalid characters.")
                 return
            # Ensure the extension is preserved or handled correctly
            # This example assumes user includes extension, add logic if needed
            base_name, ext = os.path.splitext(current_image_name)
            new_base_name, new_ext = os.path.splitext(new_name)
            if not new_ext: # If user didn't provide extension, use the old one
                new_name += ext
            elif new_ext.lower() != ext.lower():
                 reply = QMessageBox.question(self, 'Change Extension',
                                         f"The file extension will be changed from '{ext}' to '{new_ext}'. Proceed?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                 if reply == QMessageBox.No:
                     return

            new_path = os.path.join(current_dir, new_name)


            if os.path.exists(new_path):
                QMessageBox.warning(self, "Rename Image", f"File '{new_name}' already exists.")
                return

            try:
                os.rename(current_image_path, new_path)
                # QMessageBox.information(self, "Rename Image", f"'{current_image_name}' renamed to '{new_name}'.") # Optional message
                # Update internal lists and the list widget item
                idx = self.all_image_paths.index(current_image_path)
                self.all_image_paths[idx] = new_path
                idx_disp = self.displayed_images.index(current_image_path)
                self.displayed_images[idx_disp] = new_path

                # Update the QListWidgetItem
                selected_item.setText(new_name)
                selected_item.setData(Qt.UserRole, new_path)
                # Update the selected image path and info labels
                self.select_image(new_path)

                # Re-sort the list widget if sorting by name
                if "Name" in self.sort_combo.currentText():
                     self.load_gallery() # Easiest way to re-sort correctly

            except Exception as e:
                QMessageBox.warning(self, "Rename Image", f"Failed to rename image:\n{e}")


    def open_edit_tab(self):
        """Switches to the edit tab and loads the selected image."""
        selected_items = self.gallery_list.selectedItems()
        if not selected_items:
             # If called when no item selected (e.g. button clicked mistakenly), do nothing
             return

        # Use stored path from item data
        image_path = selected_items[0].data(Qt.UserRole)

        if not image_path or not os.path.exists(image_path):
             QMessageBox.warning(self, "Edit Image", "Cannot edit. Selected image path is invalid or file not found.")
             return

        self.edit_tab.load_image(image_path)
        self.tabs.setTabVisible(1, True)
        self.tabs.setCurrentIndex(1)

    def set_wallpaper(self):
        """Sets the current image as wallpaper using the provided callback."""
        if self.current_image_path and self.set_wallpaper_callback:
            try:
                 # Ensure the file exists before calling callback
                if not os.path.exists(self.current_image_path):
                    QMessageBox.warning(self, "Set Wallpaper", "Selected image file not found.")
                    return

                self.set_wallpaper_callback(self.current_image_path)
                self.result = True
                self.close() # Close after setting
            except Exception as e:
                 QMessageBox.critical(self, "Set Wallpaper Error", f"Failed to set wallpaper:\n{e}")

        elif not self.current_image_path:
            QMessageBox.warning(self, "Set Wallpaper", "No image selected.")
        elif not self.set_wallpaper_callback:
             # This case should ideally not happen if the button logic is correct
             # but provides a fallback message.
            QMessageBox.warning(self, "Set Wallpaper", "Wallpaper setting function not available.")


    def cancel(self):
        """Closes the image manager window."""
        self.result = False
        self.close()

    def open_image_dialog(self):
        """Opens a file dialog to select and load an image from anywhere."""
        options = QFileDialog.Options()
        # Start directory could be user's Pictures folder or the current gallery folder
        start_dir = os.path.expanduser("~/Pictures") if os.path.exists(os.path.expanduser("~/Pictures")) else self.image_folder

        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", start_dir,
                                                   "Image Files (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)",
                                                   options=options)
        if file_path:
            # Check if the opened file is *already* in the current gallery folder and displayed list
            is_in_gallery = False
            if os.path.dirname(file_path) == os.path.abspath(self.image_folder):
                 # Find the item in the list widget
                 items = self.gallery_list.findItems(os.path.basename(file_path), Qt.MatchExactly)
                 if items:
                     self.gallery_list.setCurrentItem(items[0])
                     is_in_gallery = True
                     # No need to call select_image again, selection change handles it
                 else:
                     # File is in the folder but not in the currently loaded batch
                     # Option 1: Just preview it (simplest)
                     # Option 2: Reload gallery to show it (can be slow/disruptive)
                     # Let's go with Option 1 for now - preview it without changing gallery state much
                      self.select_image(file_path)
                      # Deselect gallery item visually since preview is external/not-in-batch
                      self.gallery_list.clearSelection()
                      # Disable management buttons for external preview
                      self.delete_button.setEnabled(False)
                      self.rename_button.setEnabled(False)
                      # Keep Edit enabled if you want to allow editing external files
                      self.edit_button.setEnabled(True) # Or False, depending on desired behavior
                      is_in_gallery = False # Treat as external for button state


            if not is_in_gallery:
                 # If the opened file is outside the gallery folder or not in current batch
                 self.select_image(file_path)
                 # Deselect any item in the gallery list
                 self.gallery_list.clearSelection()
                 # Disable management buttons that don't make sense for external files
                 self.delete_button.setEnabled(False)
                 self.rename_button.setEnabled(False)
                 # Allow editing and setting wallpaper for external files
                 self.edit_button.setEnabled(True)
                 self.set_button.setEnabled(True) # Allow setting external file as wallpaper


    def run(self):
        """Shows the window and starts the Qt application event loop."""
        self.show()
        exit_code = self.app.exec_()
        return exit_code, self.result, self.current_image_path # Return results


    def on_back_to_gallery(self):
        """Switches back to the main gallery tab and potentially reloads."""
        # Check if the image being edited still exists and is the selected one
        if self.current_image_path and os.path.exists(self.current_image_path):
             # Potentially reload the gallery item and preview if changes were saved
             # Find the item corresponding to the edited image
            items = self.gallery_list.findItems(os.path.basename(self.current_image_path), Qt.MatchExactly)
            if items:
                 self.gallery_list.setCurrentItem(items[0]) # Reselect to refresh preview etc.
                 # Optionally, update the thumbnail icon too if needed
                 # items[0].setIcon(QtGui.QIcon(self.current_image_path))
            else:
                 # If item not found (e.g., renamed/deleted externally, or not in batch)
                 self.load_gallery() # Reload the whole gallery as a safe fallback
        else:
             # If the image doesn't exist anymore or path is invalid, reload gallery
             self.load_gallery()


        self.tabs.setCurrentIndex(0)
        self.tabs.setTabVisible(1, False)

    def closeEvent(self, event):
         """Handle the window close event."""
         # If result is not set (e.g., closed via 'X' button), treat as cancel
         if not hasattr(self, 'result') or self.result is None: # Check if result exists
             self.result = False
         print(f"Closing window. Result: {self.result}, Path: {self.current_image_path}")
         super().closeEvent(event)


if __name__ == "__main__":
    import sys
    from PyQt5 import QtWidgets

    def dummy_callback(path):
        print(f"--- DUMMY CALLBACK: Would set wallpaper to: {path} ---")
        # Simulate success/failure or user action
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(f"Set wallpaper to:\n{os.path.basename(path)}?")
        msg_box.setInformativeText("This is a dummy action. Click OK to simulate success.")
        msg_box.setWindowTitle("Set Wallpaper")
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        ret = msg_box.exec_()
        if ret == QMessageBox.Ok:
            print("--- DUMMY CALLBACK: Simulated Success ---")
            # In a real scenario, the OS call would happen here
            pass
        else:
            print("--- DUMMY CALLBACK: Simulated Cancel ---")
            raise Exception("User cancelled wallpaper setting (simulated)") # Simulate callback failure

    # Ensure QApplication exists
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)

    image_to_select = None
    folder_to_use = 'genimage' # Default folder

    # Basic argument parsing
    if len(sys.argv) > 1:
         arg_path = sys.argv[1]
         if os.path.isdir(arg_path):
             folder_to_use = arg_path
         elif os.path.isfile(arg_path):
             folder_to_use = os.path.dirname(arg_path)
             image_to_select = arg_path
         else:
             print(f"Warning: Argument '{arg_path}' is not a valid file or directory. Using default folder '{folder_to_use}'.")


    print(f"Starting Image Manager in folder: {os.path.abspath(folder_to_use)}")
    if image_to_select:
        print(f"Attempting to pre-select image: {image_to_select}")


    manager = ImageManagerApp(app, image_folder=folder_to_use, set_wallpaper_callback=dummy_callback)

    # If a specific image was passed as argument, try to select it AFTER the UI is loaded
    if image_to_select:
         # Need to ensure gallery is loaded first
         manager.load_gallery() # Ensure gallery is populated
         items = manager.gallery_list.findItems(os.path.basename(image_to_select), Qt.MatchExactly)
         if items:
             manager.gallery_list.setCurrentItem(items[0])
         else:
              # If not found in the (first batch of the) gallery, try selecting directly
              # This will preview it but might deselect gallery item if it's outside the folder
             print(f"Image '{os.path.basename(image_to_select)}' not found in initial gallery view. Previewing directly.")
             manager.select_image(image_to_select)


    exit_code, result, selected_path = manager.run()

    print("\n--- Image Manager Exited ---")
    print(f"Exit Code: {exit_code}")
    print(f"Result (Set Wallpaper clicked?): {result}")
    if result and selected_path:
        print(f"Selected Wallpaper Path: {selected_path}")
    print("----------------------------")

    sys.exit(exit_code)


def preview_image_gui(image_path, set_wallpaper_callback):
    """
    Launches the ImageManagerApp GUI to preview the given image and optionally set it as wallpaper.

    Parameters:
    - image_path (str): Path to the image file to preview.
    - set_wallpaper_callback (callable): Function to call to set the wallpaper.

    Returns:
    - bool: True if the user confirmed setting the wallpaper, False otherwise.
    """
    app = QtWidgets.QApplication.instance()
    if app is None:
        import sys
        app = QtWidgets.QApplication(sys.argv)

    import os
    folder_to_use = os.path.dirname(image_path) if os.path.isfile(image_path) else 'genimage'

    manager = ImageManagerApp(app, image_folder=folder_to_use, set_wallpaper_callback=set_wallpaper_callback)

    # Load gallery and pre-select the image if it exists
    manager.load_gallery()
    if os.path.isfile(image_path):
        items = manager.gallery_list.findItems(os.path.basename(image_path), Qt.MatchExactly)
        if items:
            manager.gallery_list.setCurrentItem(items[0])
        else:
            manager.select_image(image_path)

    exit_code, result, selected_path = manager.run()
    return result
