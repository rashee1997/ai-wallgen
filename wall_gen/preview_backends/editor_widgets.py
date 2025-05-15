# preview_backends/editor_widgets.py
"""
Contains the ImageEditTab class for the Qt image editor.
"""
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer # Qt was already imported via QtCore
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, 
                             QFileDialog, QMessageBox, QSlider, QScrollArea, QGroupBox)
import PIL
from PIL import Image, UnidentifiedImageError # Explicitly import Image from PIL

from wall_gen.image_editor import (
    adjust_brightness, adjust_contrast, adjust_saturation, adjust_sharpness,
    apply_gamma_correction, apply_blur, apply_grayscale, apply_invert,
    rotate_image, ai_enhance, remove_background, apply_high_pass_filter,
    apply_histogram_equalization, apply_contour_detection, add_gaussian_noise,
    apply_pencil_sketch, apply_sepia, apply_sharpen_filter, add_border,
    apply_xray_effect, apply_emboss, apply_edge_enhance, apply_edge_enhance_more,
    apply_find_edges, apply_detail, apply_smooth, apply_smooth_more,
    apply_laplace, apply_sobel, apply_scharr, apply_prewitt, apply_roberts,
    apply_gabor, apply_otsu_threshold, apply_niblack_threshold,
    apply_sauvola_threshold, ImageHistory
)

# Import new modularized features with error handling
try:
    from .lut_utils import load_lut_from_file, apply_lut_to_pil_image
except ImportError as e:
    print(f"Editor Tab: Could not import LUT utilities: {e}. LUT features will be disabled.")
    load_lut_from_file = None
    apply_lut_to_pil_image = None

try:
    from .stylize_filters import apply_oil_painting, apply_cartoon_effect
except ImportError as e:
    print(f"Editor Tab: Could not import stylize filters: {e}. Stylize features will be disabled.")
    apply_oil_painting = None
    apply_cartoon_effect = None

# Import UI components
from .ui_core import ImageDisplayWidget, PannableScrollArea


class ImageEditTab(QWidget):
    """
    Separate tab for image editing with various editing controls.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_image = None  # PIL Image
        self.edited_image = None    # PIL Image
        self.image_path = None
        self.current_lut = None # For storing loaded LUT object
        self.loaded_lut_label = None # To display LUT filename

        self.history = ImageHistory(max_length=20) 

        self.edit_apply_timer = QTimer(self)
        self.edit_apply_timer.setSingleShot(True)
        self.edit_apply_timer.timeout.connect(self._apply_edits_from_timer)
        self.slider_debounce_time = 200  # milliseconds

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12) 

        self.image_scroll_area = PannableScrollArea()
        self.image_display_widget = ImageDisplayWidget() 
        self.image_scroll_area.setWidget(self.image_display_widget)
        self.image_scroll_area.setAlignment(QtCore.Qt.AlignCenter) 
        self.image_scroll_area.setMinimumSize(300, 200) # Ensure it takes some space
        layout.addWidget(self.image_scroll_area, stretch=1) 

        self.sub_tabs = QtWidgets.QTabWidget()
        layout.addWidget(self.sub_tabs)

        # --- Basic Adjustments Tab ---
        basic_tab = QWidget()
        basic_layout = QVBoxLayout(basic_tab)
        basic_layout.setSpacing(8)
        brightness_layout = QHBoxLayout()
        brightness_label = QLabel("Brightness:")
        self.brightness_slider = QSlider(QtCore.Qt.Horizontal) 
        self.brightness_slider.setRange(0, 200); self.brightness_slider.setValue(100)
        self.brightness_slider.valueChanged.connect(self.on_slider_value_changed)
        brightness_layout.addWidget(brightness_label); brightness_layout.addWidget(self.brightness_slider)
        basic_layout.addLayout(brightness_layout)
        contrast_layout = QHBoxLayout()
        contrast_label = QLabel("Contrast:")
        self.contrast_slider = QSlider(QtCore.Qt.Horizontal) 
        self.contrast_slider.setRange(0, 200); self.contrast_slider.setValue(100)
        self.contrast_slider.valueChanged.connect(self.on_slider_value_changed)
        contrast_layout.addWidget(contrast_label); contrast_layout.addWidget(self.contrast_slider)
        basic_layout.addLayout(contrast_layout)
        saturation_layout = QHBoxLayout()
        saturation_label = QLabel("Saturation:")
        self.saturation_slider = QSlider(QtCore.Qt.Horizontal) 
        self.saturation_slider.setRange(0, 200); self.saturation_slider.setValue(100)
        self.saturation_slider.valueChanged.connect(self.on_slider_value_changed)
        saturation_layout.addWidget(saturation_label); saturation_layout.addWidget(self.saturation_slider)
        basic_layout.addLayout(saturation_layout)
        basic_layout.addStretch()
        self.sub_tabs.addTab(basic_tab, "Basic")

        # --- Tone & Detail Tab ---
        tone_detail_tab = QWidget()
        tone_detail_layout = QVBoxLayout(tone_detail_tab)
        tone_detail_layout.setSpacing(8)
        sharpness_layout = QHBoxLayout()
        sharpness_label = QLabel("Sharpness:")
        self.sharpness_slider = QSlider(QtCore.Qt.Horizontal) 
        self.sharpness_slider.setRange(0, 200); self.sharpness_slider.setValue(100)
        self.sharpness_slider.valueChanged.connect(self.on_slider_value_changed)
        sharpness_layout.addWidget(sharpness_label); sharpness_layout.addWidget(self.sharpness_slider)
        tone_detail_layout.addLayout(sharpness_layout)
        gamma_layout = QHBoxLayout()
        gamma_label = QLabel("Gamma:")
        self.gamma_slider = QSlider(QtCore.Qt.Horizontal) 
        self.gamma_slider.setRange(20, 220); self.gamma_slider.setValue(100)
        self.gamma_slider.valueChanged.connect(self.on_slider_value_changed)
        gamma_layout.addWidget(gamma_label); gamma_layout.addWidget(self.gamma_slider)
        tone_detail_layout.addLayout(gamma_layout)
        blur_layout = QHBoxLayout()
        blur_label = QLabel("Blur:")
        self.blur_slider = QSlider(QtCore.Qt.Horizontal) 
        self.blur_slider.setRange(0, 20); self.blur_slider.setValue(0)
        self.blur_slider.valueChanged.connect(self.on_slider_value_changed)
        blur_layout.addWidget(blur_label); blur_layout.addWidget(self.blur_slider)
        tone_detail_layout.addLayout(blur_layout)
        tone_detail_layout.addStretch()
        self.sub_tabs.addTab(tone_detail_tab, "Tone & Detail")

        # --- General Filters Tab ---
        general_filters_tab = QWidget()
        gf_scroll = QScrollArea(); gf_scroll.setWidgetResizable(True)
        gf_widget = QWidget()
        general_filters_layout = QVBoxLayout(gf_widget); general_filters_layout.setSpacing(10)
        filter_buttons1 = QHBoxLayout()
        self.grayscale_button = QPushButton("Grayscale"); self.grayscale_button.setCheckable(True); self.grayscale_button.toggled.connect(self.apply_edits_toggle)
        filter_buttons1.addWidget(self.grayscale_button)
        self.invert_button = QPushButton("Invert Colors"); self.invert_button.setCheckable(True); self.invert_button.toggled.connect(self.apply_edits_toggle)
        filter_buttons1.addWidget(self.invert_button)
        general_filters_layout.addLayout(filter_buttons1)
        filter_buttons2 = QHBoxLayout()
        self.sepia_button = QPushButton("Sepia Tone"); self.sepia_button.setCheckable(True); self.sepia_button.toggled.connect(self.apply_edits_toggle)
        filter_buttons2.addWidget(self.sepia_button)
        self.xray_button = QPushButton("X-Ray Effect"); self.xray_button.setCheckable(True); self.xray_button.toggled.connect(self.apply_edits_toggle)
        filter_buttons2.addWidget(self.xray_button)
        general_filters_layout.addLayout(filter_buttons2)
        filter_buttons3 = QHBoxLayout()
        self.high_pass_button = QPushButton("High Pass"); self.high_pass_button.setCheckable(True); self.high_pass_button.toggled.connect(self.apply_edits_toggle)
        filter_buttons3.addWidget(self.high_pass_button)
        self.hist_eq_button = QPushButton("Histogram Equalize"); self.hist_eq_button.setCheckable(True); self.hist_eq_button.toggled.connect(self.apply_edits_toggle)
        filter_buttons3.addWidget(self.hist_eq_button)
        general_filters_layout.addLayout(filter_buttons3)
        filter_buttons4 = QHBoxLayout()
        self.noise_button = QPushButton("Add Noise"); self.noise_button.setCheckable(True); self.noise_button.toggled.connect(self.apply_edits_toggle)
        filter_buttons4.addWidget(self.noise_button)
        self.border_button = QPushButton("Add Border"); self.border_button.setCheckable(True); self.border_button.toggled.connect(self.apply_edits_toggle)
        filter_buttons4.addWidget(self.border_button)
        general_filters_layout.addLayout(filter_buttons4)
        general_filters_layout.addStretch(); gf_widget.setLayout(general_filters_layout); gf_scroll.setWidget(gf_widget)
        self.sub_tabs.addTab(gf_scroll, "General Filters")

        # --- Advanced Filters Tab ---
        adv_filters_tab = QWidget()
        adv_scroll = QScrollArea(); adv_scroll.setWidgetResizable(True)
        adv_widget = QWidget()
        adv_filters_layout = QVBoxLayout(adv_widget); adv_filters_layout.setSpacing(10)
        pillow_group = QGroupBox("Pillow Filters"); pillow_layout = QVBoxLayout(pillow_group)
        pillow_row1 = QHBoxLayout()
        self.emboss_button = QPushButton("Emboss"); self.emboss_button.setCheckable(True); self.emboss_button.toggled.connect(self.apply_edits_toggle)
        pillow_row1.addWidget(self.emboss_button)
        self.detail_button = QPushButton("Detail Enhance"); self.detail_button.setCheckable(True); self.detail_button.toggled.connect(self.apply_edits_toggle)
        pillow_row1.addWidget(self.detail_button); pillow_layout.addLayout(pillow_row1)
        pillow_row2 = QHBoxLayout()
        self.edge_enhance_button = QPushButton("Edge Enhance"); self.edge_enhance_button.setCheckable(True); self.edge_enhance_button.toggled.connect(self.apply_edits_toggle)
        pillow_row2.addWidget(self.edge_enhance_button)
        self.edge_enhance_more_button = QPushButton("Edge Enhance More"); self.edge_enhance_more_button.setCheckable(True); self.edge_enhance_more_button.toggled.connect(self.apply_edits_toggle)
        pillow_row2.addWidget(self.edge_enhance_more_button); pillow_layout.addLayout(pillow_row2)
        pillow_row3 = QHBoxLayout()
        self.find_edges_button = QPushButton("Find Edges"); self.find_edges_button.setCheckable(True); self.find_edges_button.toggled.connect(self.apply_edits_toggle)
        pillow_row3.addWidget(self.find_edges_button)
        self.contour_button = QPushButton("Contour"); self.contour_button.setCheckable(True); self.contour_button.toggled.connect(self.apply_edits_toggle)
        pillow_row3.addWidget(self.contour_button); pillow_layout.addLayout(pillow_row3)
        pillow_row4 = QHBoxLayout()
        self.smooth_button = QPushButton("Smooth"); self.smooth_button.setCheckable(True); self.smooth_button.toggled.connect(self.apply_edits_toggle)
        pillow_row4.addWidget(self.smooth_button)
        self.smooth_more_button = QPushButton("Smooth More"); self.smooth_more_button.setCheckable(True); self.smooth_more_button.toggled.connect(self.apply_edits_toggle)
        pillow_row4.addWidget(self.smooth_more_button); pillow_layout.addLayout(pillow_row4)
        adv_filters_layout.addWidget(pillow_group)
        scikit_edge_group = QGroupBox("Edge Detection Filters"); scikit_edge_layout_main = QVBoxLayout(scikit_edge_group)
        scikit_edge_row1 = QHBoxLayout()
        self.laplace_button = QPushButton("Laplace"); self.laplace_button.setCheckable(True); self.laplace_button.toggled.connect(self.apply_edits_toggle)
        scikit_edge_row1.addWidget(self.laplace_button)
        self.sobel_button = QPushButton("Sobel"); self.sobel_button.setCheckable(True); self.sobel_button.toggled.connect(self.apply_edits_toggle)
        scikit_edge_row1.addWidget(self.sobel_button); scikit_edge_layout_main.addLayout(scikit_edge_row1)
        scikit_edge_row2 = QHBoxLayout()
        self.scharr_button = QPushButton("Scharr"); self.scharr_button.setCheckable(True); self.scharr_button.toggled.connect(self.apply_edits_toggle)
        scikit_edge_row2.addWidget(self.scharr_button)
        self.prewitt_button = QPushButton("Prewitt"); self.prewitt_button.setCheckable(True); self.prewitt_button.toggled.connect(self.apply_edits_toggle)
        scikit_edge_row2.addWidget(self.prewitt_button); scikit_edge_layout_main.addLayout(scikit_edge_row2)
        scikit_edge_row3 = QHBoxLayout()
        self.roberts_button = QPushButton("Roberts Cross"); self.roberts_button.setCheckable(True); self.roberts_button.toggled.connect(self.apply_edits_toggle)
        scikit_edge_row3.addWidget(self.roberts_button); scikit_edge_row3.addStretch(); scikit_edge_layout_main.addLayout(scikit_edge_row3)
        adv_filters_layout.addWidget(scikit_edge_group)
        scikit_other_group = QGroupBox("Thresholding & Other Filters"); scikit_other_layout_main = QVBoxLayout(scikit_other_group)
        scikit_other_row1 = QHBoxLayout()
        self.gabor_button = QPushButton("Gabor Filter"); self.gabor_button.setCheckable(True); self.gabor_button.toggled.connect(self.apply_edits_toggle)
        scikit_other_row1.addWidget(self.gabor_button)
        self.otsu_button = QPushButton("Otsu Threshold"); self.otsu_button.setCheckable(True); self.otsu_button.toggled.connect(self.apply_edits_toggle)
        scikit_other_row1.addWidget(self.otsu_button); scikit_other_layout_main.addLayout(scikit_other_row1)
        scikit_other_row2 = QHBoxLayout()
        self.niblack_button = QPushButton("Niblack Threshold"); self.niblack_button.setCheckable(True); self.niblack_button.toggled.connect(self.apply_edits_toggle)
        scikit_other_row2.addWidget(self.niblack_button)
        self.sauvola_button = QPushButton("Sauvola Threshold"); self.sauvola_button.setCheckable(True); self.sauvola_button.toggled.connect(self.apply_edits_toggle)
        scikit_other_row2.addWidget(self.sauvola_button); scikit_other_layout_main.addLayout(scikit_other_row2)
        adv_filters_layout.addWidget(scikit_other_group)
        adv_filters_layout.addStretch(); adv_widget.setLayout(adv_filters_layout); adv_scroll.setWidget(adv_widget)
        self.sub_tabs.addTab(adv_scroll, "Advanced Filters")

        # --- Artistic & Stylize Tab ---
        artistic_tab = QWidget()
        artistic_scroll = QScrollArea(); artistic_scroll.setWidgetResizable(True)
        art_widget = QWidget()
        artistic_layout = QVBoxLayout(art_widget); artistic_layout.setSpacing(10)
        art_row1 = QHBoxLayout()
        self.pencil_sketch_button = QPushButton("Pencil Sketch"); self.pencil_sketch_button.setCheckable(True); self.pencil_sketch_button.toggled.connect(self.apply_edits_toggle)
        art_row1.addWidget(self.pencil_sketch_button)
        if apply_oil_painting:
            self.oil_painting_button = QPushButton("Oil Painting"); self.oil_painting_button.setCheckable(True); self.oil_painting_button.toggled.connect(self.apply_edits_toggle)
            art_row1.addWidget(self.oil_painting_button)
        artistic_layout.addLayout(art_row1)
        art_row2 = QHBoxLayout()
        if apply_cartoon_effect:
            self.cartoon_button = QPushButton("Cartoon Effect"); self.cartoon_button.setCheckable(True); self.cartoon_button.toggled.connect(self.apply_edits_toggle)
            art_row2.addWidget(self.cartoon_button)
            self.cartoon_sketch_button = QPushButton("Cartoon Sketch"); self.cartoon_sketch_button.setCheckable(True); self.cartoon_sketch_button.toggled.connect(self.apply_edits_toggle)
            art_row2.addWidget(self.cartoon_sketch_button)
        artistic_layout.addLayout(art_row2)
        artistic_layout.addStretch(); art_widget.setLayout(artistic_layout); artistic_scroll.setWidget(art_widget)
        self.sub_tabs.addTab(artistic_scroll, "Artistic")

        # --- LUTs & Color Grading Tab ---
        if load_lut_from_file: 
            lut_tab = QWidget()
            lut_layout = QVBoxLayout(lut_tab); lut_layout.setSpacing(10)
            lut_controls_layout = QHBoxLayout()
            self.load_lut_button = QPushButton("Load 3D LUT (.cube)"); self.load_lut_button.clicked.connect(self.load_lut_action)
            lut_controls_layout.addWidget(self.load_lut_button)
            self.clear_lut_button = QPushButton("Clear LUT"); self.clear_lut_button.clicked.connect(self.clear_lut_action); self.clear_lut_button.setEnabled(False)
            lut_controls_layout.addWidget(self.clear_lut_button); lut_layout.addLayout(lut_controls_layout)
            self.loaded_lut_label = QLabel("Current LUT: None"); self.loaded_lut_label.setStyleSheet("font-style: italic; color: #aaaaaa;")
            lut_layout.addWidget(self.loaded_lut_label)
            lut_layout.addStretch()
            self.sub_tabs.addTab(lut_tab, "LUTs & Color")

        # --- Main Control Buttons ---
        control_button_layout = QHBoxLayout(); control_button_layout.setSpacing(10)
        self.undo_button = QPushButton("Undo"); self.undo_button.clicked.connect(self.undo); self.undo_button.setEnabled(False) 
        control_button_layout.addWidget(self.undo_button)
        self.redo_button = QPushButton("Redo"); self.redo_button.clicked.connect(self.redo); self.redo_button.setEnabled(False) 
        control_button_layout.addWidget(self.redo_button)
        self.reset_button = QPushButton("Reset All Edits"); self.reset_button.clicked.connect(self.reset_edits)
        control_button_layout.addWidget(self.reset_button)
        control_button_layout.addStretch() 
        self.save_button = QPushButton("Save"); self.save_button.clicked.connect(self.save_image)
        control_button_layout.addWidget(self.save_button)
        self.save_as_button = QPushButton("Save As..."); self.save_as_button.clicked.connect(self.save_image_as)
        control_button_layout.addWidget(self.save_as_button)
        self.back_button = QPushButton("Back to Gallery")
        control_button_layout.addWidget(self.back_button)  
        layout.addLayout(control_button_layout)

    def on_slider_value_changed(self):
        self.edit_apply_timer.start(self.slider_debounce_time)

    def _apply_edits_from_timer(self):
        self.apply_edits(save_history=True)

    def apply_edits_toggle(self, checked):
        self.apply_edits(save_history=True)

    def load_image(self, image_path):
        try:
            self.image_path = image_path
            self.original_image = PIL.Image.open(image_path).convert('RGBA')
            self.edited_image = self.original_image.copy()
            self.reset_controls_to_default()
            
            # Clear history stacks directly
            if hasattr(self.history, 'undo_stack'):
                self.history.undo_stack.clear()
            if hasattr(self.history, 'redo_stack'):
                self.history.redo_stack.clear()
            
            self.history.push(self.original_image.copy()) # Add initial state to history
            self.update_history_buttons() 
            self.update_image_display_widget() 
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"Image file not found: {image_path}")
            self.original_image = None; self.edited_image = None
        except UnidentifiedImageError: 
            QMessageBox.critical(self, "Error", f"Cannot identify image file (corrupted or unsupported format): {os.path.basename(image_path)}")
            self.original_image = None; self.edited_image = None
        except Exception as e:
            # Catch the specific error from the screenshot to provide a more targeted message
            if isinstance(e, AttributeError) and "object has no attribute 'can_undo'" in str(e):
                 QMessageBox.critical(self, "Error", f"Failed to load image {os.path.basename(image_path)} due to an internal history error (can_undo). Please check ImageHistory class.")
            elif isinstance(e, AttributeError) and "object has no attribute 'clear'" in str(e):
                 QMessageBox.critical(self, "Error", f"Failed to load image {os.path.basename(image_path)} due to an internal history error (clear). Please check ImageHistory class.")
            else:
                QMessageBox.critical(self, "Error", f"Failed to load image {os.path.basename(image_path)}: {e}")
            self.original_image = None; self.edited_image = None


    def update_image_display_widget(self):
        if self.edited_image is None:
            self.image_display_widget.setPixmap(QtGui.QPixmap()); return
        try:
            if self.edited_image.mode == "RGBA":
                 qt_image = QtGui.QImage(self.edited_image.tobytes("raw", "RGBA"), self.edited_image.width, self.edited_image.height, QtGui.QImage.Format_RGBA8888)
            elif self.edited_image.mode == "RGB":
                 qt_image = QtGui.QImage(self.edited_image.tobytes("raw", "RGB"), self.edited_image.width, self.edited_image.height, QtGui.QImage.Format_RGB888)
            elif self.edited_image.mode == "L":
                 qt_image = QtGui.QImage(self.edited_image.tobytes("raw", "L"), self.edited_image.width, self.edited_image.height, QtGui.QImage.Format_Grayscale8)
            else: 
                 temp_img = self.edited_image.convert("RGBA")
                 qt_image = QtGui.QImage(temp_img.tobytes("raw", "RGBA"), temp_img.width, temp_img.height, QtGui.QImage.Format_RGBA8888)
            pixmap = QtGui.QPixmap.fromImage(qt_image)
            self.image_display_widget.setPixmap(pixmap)
        except Exception as e:
            print(f"Error updating image display widget: {e}")
            self.image_display_widget.setPixmap(QtGui.QPixmap())

    def reset_controls_to_default(self):
        controls_to_reset = [
            (self.brightness_slider, 100), (self.contrast_slider, 100),
            (self.saturation_slider, 100), (self.sharpness_slider, 100),
            (self.gamma_slider, 100), (self.blur_slider, 0)
        ]
        for control, value in controls_to_reset:
            control.blockSignals(True); control.setValue(value); control.blockSignals(False)
        
        buttons_to_reset = [
            self.grayscale_button, self.invert_button, self.high_pass_button, self.hist_eq_button,
            self.contour_button, self.noise_button, self.pencil_sketch_button, self.sepia_button,
            self.border_button, self.xray_button, self.emboss_button,
            self.edge_enhance_button, self.edge_enhance_more_button, self.find_edges_button,
            self.detail_button, self.smooth_button, self.smooth_more_button, self.laplace_button,
            self.sobel_button, self.scharr_button, self.prewitt_button, self.roberts_button,
            self.gabor_button, self.otsu_button, self.niblack_button, self.sauvola_button
        ]
        if hasattr(self, 'oil_painting_button') and self.oil_painting_button: buttons_to_reset.append(self.oil_painting_button)
        if hasattr(self, 'cartoon_button') and self.cartoon_button: buttons_to_reset.append(self.cartoon_button)
        if hasattr(self, 'cartoon_sketch_button') and self.cartoon_sketch_button: buttons_to_reset.append(self.cartoon_sketch_button)

        for btn in buttons_to_reset:
            if btn: 
                btn.blockSignals(True); btn.setChecked(False); btn.blockSignals(False)
        self.clear_lut_action(triggered_by_reset=True)

    def apply_edits(self, save_history=True):
        if self.original_image is None: return
        img = self.original_image.copy()

        brightness_factor = self.brightness_slider.value() / 100.0
        contrast_factor = self.contrast_slider.value() / 100.0
        saturation_factor = self.saturation_slider.value() / 100.0
        sharpness_factor = self.sharpness_slider.value() / 100.0
        gamma_value = self.gamma_slider.value() / 100.0
        blur_radius = self.blur_slider.value()

        img = adjust_brightness(img, brightness_factor)
        img = adjust_contrast(img, contrast_factor)
        img = adjust_saturation(img, saturation_factor)
        img = adjust_sharpness(img, sharpness_factor)
        img = apply_gamma_correction(img, gamma_value)
        if blur_radius > 0: img = apply_blur(img, blur_radius)

        if self.grayscale_button.isChecked(): img = apply_grayscale(img)
        if self.invert_button.isChecked(): img = apply_invert(img)
        if self.high_pass_button.isChecked(): img = apply_high_pass_filter(img)
        if self.hist_eq_button.isChecked(): img = apply_histogram_equalization(img)
        if self.contour_button.isChecked(): img = apply_contour_detection(img)
        if self.noise_button.isChecked(): img = add_gaussian_noise(img)
        if hasattr(self, 'pencil_sketch_button') and self.pencil_sketch_button.isChecked(): img = apply_pencil_sketch(img)
        if self.sepia_button.isChecked(): img = apply_sepia(img)
        if self.border_button.isChecked(): img = add_border(img, 10)
        if self.xray_button.isChecked(): img = apply_xray_effect(img)
        if self.emboss_button.isChecked(): img = apply_emboss(img)
        if self.edge_enhance_button.isChecked(): img = apply_edge_enhance(img)
        if self.edge_enhance_more_button.isChecked(): img = apply_edge_enhance_more(img)
        if self.find_edges_button.isChecked(): img = apply_find_edges(img)
        if self.detail_button.isChecked(): img = apply_detail(img)
        if self.smooth_button.isChecked(): img = apply_smooth(img)
        if self.smooth_more_button.isChecked(): img = apply_smooth_more(img)
        if self.laplace_button.isChecked(): img = apply_laplace(img)
        if self.sobel_button.isChecked(): img = apply_sobel(img)
        if self.scharr_button.isChecked(): img = apply_scharr(img)
        if self.prewitt_button.isChecked(): img = apply_prewitt(img)
        if self.roberts_button.isChecked(): img = apply_roberts(img)
        if self.gabor_button.isChecked(): img = apply_gabor(img, frequency=0.6)
        if self.otsu_button.isChecked(): img = apply_otsu_threshold(img)
        if self.niblack_button.isChecked(): img = apply_niblack_threshold(img, window_size=25, k=0.8)
        if self.sauvola_button.isChecked(): img = apply_sauvola_threshold(img, window_size=25, k=0.8)

        if hasattr(self, 'oil_painting_button') and self.oil_painting_button and self.oil_painting_button.isChecked() and apply_oil_painting:
            img = apply_oil_painting(img)
        if hasattr(self, 'cartoon_button') and self.cartoon_button and self.cartoon_button.isChecked() and apply_cartoon_effect:
            img = apply_cartoon_effect(img, sketch_mode=False)
        if hasattr(self, 'cartoon_sketch_button') and self.cartoon_sketch_button and self.cartoon_sketch_button.isChecked() and apply_cartoon_effect:
            img = apply_cartoon_effect(img, sketch_mode=True)

        if self.current_lut and apply_lut_to_pil_image:
            img = apply_lut_to_pil_image(img, self.current_lut)

        self.edited_image = img
        if save_history:
            # Ensure edited_image is not None before tobytes()
            if self.edited_image is not None and (not self.history.undo_stack or self.edited_image.tobytes() != self.history.undo_stack[-1].tobytes()):
                self.history.push(self.edited_image.copy())
        self.update_image_display_widget()
        self.update_history_buttons()

    def update_history_buttons(self):
        # Check if undo_stack has more than one item (initial state + at least one change)
        # or if your ImageHistory class has a more specific way to determine this.
        # Assuming the first item in undo_stack is the original and not "undoable" to a prior state.
        can_undo_flag = hasattr(self.history, 'undo_stack') and len(self.history.undo_stack) > 1
        can_redo_flag = hasattr(self.history, 'redo_stack') and bool(self.history.redo_stack)
        
        self.undo_button.setEnabled(can_undo_flag)
        self.redo_button.setEnabled(can_redo_flag)


    def undo(self):
        # This logic depends heavily on how ImageHistory.undo() is implemented.
        # If undo() returns the state *to be displayed* and handles stack management:
        if hasattr(self.history, 'undo_stack') and len(self.history.undo_stack) > 1: # Check if can actually undo
            previous_state = self.history.undo() # Assuming this pops from undo and pushes to redo
            if previous_state is not None: # If undo returns the state to set
                self.edited_image = previous_state
            else: # If undo returns None or modifies stacks internally, re-fetch from undo_stack top
                 if self.history.undo_stack: # Check if undo_stack is not empty
                    self.edited_image = self.history.undo_stack[-1].copy() # Display the new top of undo stack
                 # else: handle case where undo_stack might be empty (should not happen if can_undo was true)
            self.update_image_display_widget()
        self.update_history_buttons()


    def redo(self):
        # Similar to undo, depends on ImageHistory.redo()
        if hasattr(self.history, 'redo_stack') and bool(self.history.redo_stack):
            redone_state = self.history.redo() # Assuming this pops from redo and pushes to undo
            if redone_state is not None:
                self.edited_image = redone_state
                self.update_image_display_widget()
        self.update_history_buttons()


    def reset_edits(self):
        if self.original_image is None: return
        self.reset_controls_to_default()
        self.edited_image = self.original_image.copy()
        # Clear history stacks directly
        if hasattr(self.history, 'undo_stack'):
            self.history.undo_stack.clear()
        if hasattr(self.history, 'redo_stack'):
            self.history.redo_stack.clear()
        self.history.push(self.original_image.copy())
        self.update_image_display_widget()
        self.update_history_buttons()

    def rotate_image_action(self, angle):
        if self.edited_image is None: return
        self.history.push(self.edited_image.copy())
        self.original_image = rotate_image(self.original_image, angle) # Rotate original
        self.apply_edits(save_history=False) # Re-apply current settings to new original
        # apply_edits will push to history if changes occurred, but we want to ensure this rotated state is explicitly pushed
        if self.edited_image is not None and (not self.history.undo_stack or self.edited_image.tobytes() != self.history.undo_stack[-1].tobytes()):
            self.history.push(self.edited_image.copy())
        self.update_history_buttons()

    def load_lut_action(self):
        if not load_lut_from_file:
            QMessageBox.warning(self, "LUT Error", "LUT loading unavailable."); return
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Load 3D LUT File", os.path.expanduser("~"),
                                                  "CUBE Files (*.cube);;All Files (*)", options=options)
        if filePath:
            new_lut = load_lut_from_file(filePath)
            if new_lut:
                self.current_lut = new_lut
                if self.loaded_lut_label: self.loaded_lut_label.setText(f"Current LUT: {os.path.basename(filePath)}")
                if hasattr(self, 'clear_lut_button'): self.clear_lut_button.setEnabled(True)
                self.apply_edits(save_history=True) 
            else:
                QMessageBox.warning(self, "LUT Error", f"Failed to load LUT: {os.path.basename(filePath)}")

    def clear_lut_action(self, triggered_by_reset=False):
        if self.current_lut is not None:
            self.current_lut = None
            if self.loaded_lut_label: self.loaded_lut_label.setText("Current LUT: None")
            if hasattr(self, 'clear_lut_button'): self.clear_lut_button.setEnabled(False)
            if not triggered_by_reset: self.apply_edits(save_history=True)

    def save_image(self):
        if self.image_path and self.edited_image:
            try:
                pil_original_image_info = PIL.Image.open(self.image_path)
                original_format = pil_original_image_info.format
                save_kwargs = {}
                if original_format:
                    save_kwargs['format'] = original_format
                    if original_format.upper() == 'JPEG':
                        save_kwargs['quality'] = pil_original_image_info.info.get('quality', 95)
                        save_kwargs['subsampling'] = pil_original_image_info.info.get('subsampling', 0) 
                        if 'icc_profile' in pil_original_image_info.info: save_kwargs['icc_profile'] = pil_original_image_info.info['icc_profile']
                        if 'exif' in pil_original_image_info.info: save_kwargs['exif'] = pil_original_image_info.info['exif']
                    elif original_format.upper() == 'PNG':
                         if 'icc_profile' in pil_original_image_info.info: save_kwargs['icc_profile'] = pil_original_image_info.info['icc_profile']
                
                save_image = self.edited_image
                if original_format and original_format.upper() in ['JPEG', 'BMP'] and save_image.mode == 'RGBA':
                    background = PIL.Image.new('RGB', save_image.size, (255, 255, 255))
                    background.paste(save_image, mask=save_image.split()[3]) 
                    save_image = background
                elif save_image.mode == 'P' and original_format and original_format.upper() != 'GIF':
                    save_image = save_image.convert('RGB')

                save_image.save(self.image_path, **save_kwargs)
                QMessageBox.information(self, "Save Image", "Image saved successfully.")
                self.original_image = self.edited_image.copy()
                # Clear history stacks directly
                if hasattr(self.history, 'undo_stack'): self.history.undo_stack.clear()
                if hasattr(self.history, 'redo_stack'): self.history.redo_stack.clear()
                self.history.push(self.original_image.copy())
                self.update_history_buttons()
                
                # Notify parent (ImageManagerApp) to reload gallery
                parent_manager = self.parent_manager()
                if parent_manager:
                    parent_manager.load_gallery()
            except Exception as e:
                QMessageBox.warning(self, "Save Image", f"Failed to save image: {e}")

    def save_image_as(self):
        if self.edited_image is None: return
        options = QFileDialog.Options()
        suggested_name = "edited_" + os.path.basename(self.image_path) if self.image_path else "edited_image.png"
        default_dir = os.path.dirname(self.image_path) if self.image_path else os.path.expanduser("~")
        file_path, selected_filter = QFileDialog.getSaveFileName(self, "Save Image As",
                                                                  os.path.join(default_dir, suggested_name),
                                                                  "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;BMP Files (*.bmp);;GIF Files (*.gif);;TIFF Files (*.tif *.tiff);;All Files (*)",
                                                                  options=options)
        if file_path:
            try:
                file_ext = os.path.splitext(file_path)[1].lower()
                save_format = None
                if 'png' in selected_filter.lower() or file_ext == '.png': save_format = 'PNG'
                elif 'jpeg' in selected_filter.lower() or file_ext in ['.jpg', '.jpeg']: save_format = 'JPEG'
                elif 'bmp' in selected_filter.lower() or file_ext == '.bmp': save_format = 'BMP'
                elif 'gif' in selected_filter.lower() or file_ext == '.gif': save_format = 'GIF'
                elif 'tiff' in selected_filter.lower() or file_ext in ['.tif', '.tiff']: save_format = 'TIFF'
                
                save_kwargs = {}
                if save_format:
                    save_kwargs['format'] = save_format
                    if save_format == 'JPEG': save_kwargs['quality'] = 95 
                
                save_image = self.edited_image
                if save_format in ['JPEG', 'BMP'] and save_image.mode == 'RGBA':
                     background = PIL.Image.new('RGB', save_image.size, (255, 255, 255))
                     background.paste(save_image, mask=save_image.split()[3])
                     save_image = background
                elif save_image.mode == 'P' and save_format != 'GIF':
                    save_image = save_image.convert('RGB')

                save_image.save(file_path, **save_kwargs)
                QMessageBox.information(self, "Save Image As", f"Image saved as {os.path.basename(file_path)}.")
                
                parent_manager = self.parent_manager()
                if parent_manager and os.path.dirname(file_path) == parent_manager.image_folder:
                    parent_manager.load_gallery() 
            except Exception as e:
                QMessageBox.warning(self, "Save Image As", f"Failed to save image: {e}")

    def parent_manager(self):
        """Helper to get ImageManagerApp instance if it's a parent or grandparent."""
        parent = self.parent()
        if parent and hasattr(parent, 'image_folder') and hasattr(parent, 'load_gallery'): 
            return parent
        elif parent and parent.parent() and hasattr(parent.parent(), 'image_folder') and hasattr(parent.parent(), 'load_gallery'): 
            return parent.parent()
        return None
