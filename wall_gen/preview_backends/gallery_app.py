# preview_backends/gallery_app.py
"""
Contains the ImageManagerApp class for the Qt image editor and gallery.
"""
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, 
                             QFileDialog, QMessageBox, QTabWidget, QInputDialog, QGroupBox)
from PyQt5.QtCore import Qt, QSize
import PIL
from PIL import Image # Explicitly import Image

# Import modularized components
from .ui_core import PannableScrollArea, ImageDisplayWidget
from .editor_widgets import ImageEditTab


class ImageManagerApp(QtWidgets.QWidget):
    """
    Main application window for managing, viewing, and editing images.
    """
    def __init__(self, app, image_folder='genimage', set_wallpaper_callback=None):
        super().__init__()
        self.app = app 
        self.image_folder = image_folder
        self.set_wallpaper_callback = set_wallpaper_callback
        self.result = False 
        self.current_image_path = None 
        self.scale_factor = 1.0 
        self.original_pixmap = None 

        self.batch_size = 50
        self.current_batch = 1
        self.all_image_paths = []  
        self.displayed_images = [] 

        self.init_ui()
        self.load_gallery()
        
        if self.gallery_list.count() > 0:
             self.gallery_list.setCurrentRow(0) 
        else:
             self.update_status_label() 

    def init_ui(self):
        screen = QtWidgets.QApplication.primaryScreen()
        if screen:
            geo = screen.availableGeometry()
            avail_width, avail_height = geo.width(), geo.height()
        else:
            avail_width, avail_height = 1280, 720

        init_width = min(1250, avail_width - 100) # Slightly wider for more space
        init_height = min(820, avail_height - 100)

        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.WindowMinMaxButtonsHint |
            QtCore.Qt.WindowCloseButtonHint
        )
        self.setWindowTitle("Advanced Image Editor & Manager") 
        self.resize(init_width, init_height)
        self.setMaximumSize(avail_width, avail_height)
        self.setMinimumSize(800, 600) 
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        # Enhanced Stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: #282c34; 
                color: #abb2bf; /* Softer text color */
                font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif; 
                font-size: 10pt;
            }
            QLabel#titleLabel { /* For main titles like "Image Preview" */
                color: #61afef; /* Accent color */
                font-weight: bold;
                font-size: 15pt; /* Slightly smaller but still prominent */
                margin-bottom: 8px;
                padding-bottom: 4px;
                border-bottom: 1px solid #3e4451; 
            }
            QLabel#statusLabel {
                font-style: italic;
                color: #7f8c8d; /* Muted status text */
                font-size: 9pt;
                margin-top: 8px; /* More space above status */
                padding: 2px;
            }
            QLabel[objectName="infoLabel"] { /* For File, Resolution, Size */
                color: #abb2bf; /* Standard text color */
                font-size: 9pt;
                margin-top: 3px; /* Tighter spacing for info block */
            }
            QListWidget {
                background-color: #21252b; 
                border: 1px solid #3e4451;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 7px 5px; /* Adjusted padding */
                margin: 1px 0;
                border-bottom: 1px solid #2c313a; 
                color: #abb2bf; 
            }
            QListWidget::item:last-child { border-bottom: none; }
            QListWidget::item:selected {
                background-color: #61afef; 
                color: #21252b; /* Darker text on selection for contrast */
                border-radius: 3px;
            }
            QPushButton {
                background-color: #61afef; 
                color: #282c34; /* Dark text on buttons */
                font-size: 10pt;
                font-weight: bold;
                border: none;
                padding: 8px 12px; /* Standardized padding */
                border-radius: 4px; 
                min-height: 28px; 
            }
            QPushButton:hover { background-color: #528bce; }
            QPushButton:pressed { background-color: #4073a8; }
            QPushButton:disabled {
                background-color: #3a3f4b; /* Slightly lighter disabled */
                color: #7f8c8d; 
            }
            QLineEdit {
                background-color: #21252b;
                border: 1px solid #3e4451;
                border-radius: 4px; /* Consistent radius */
                color: #abb2bf;
                padding: 6px 10px; /* More padding */
            }
            QSlider::groove:horizontal {
                border: 1px solid #3e4451; height: 8px; 
                background: #21252b; border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #61afef; border: 1px solid #528bce;
                width: 16px; height: 16px; margin: -4px 0; 
                border-radius: 8px;
            }
            QScrollArea {
                border: 1px solid #3e4451; border-radius: 5px;
                background-color: #21252b; 
            }
            QScrollArea > QWidget > QWidget { background-color: #21252b; } /* Viewport */
            QGroupBox {
                 border: 1px solid #4a505c; /* Slightly lighter border for groupbox */
                 border-radius: 6px; /* Slightly larger radius */
                 margin-top: 18px; /* More space for title */
                 padding: 10px; /* Padding inside the groupbox */
            }
            QGroupBox::title {
                 subcontrol-origin: margin;
                 subcontrol-position: top left;
                 padding: 2px 10px; /* Padding around title text */
                 left: 12px; /* Indent title */
                 background-color: #61afef; /* Title background */
                 color: #282c34; /* Dark text on title background */
                 font-size: 10pt;
                 font-weight: bold;
                 border-radius: 3px;
            }
            QComboBox {
                 background-color: #21252b; border: 1px solid #3e4451; border-radius: 4px; 
                 padding: 5px 20px 5px 10px; /* Adjusted padding */
                 min-width: 8em; color: #abb2bf;
            }
            QComboBox::drop-down {
                 subcontrol-origin: padding; subcontrol-position: top right; width: 18px; 
                 border-left: 1px solid #3e4451; background-color: #3e4451;
                 border-top-right-radius: 4px; border-bottom-right-radius: 4px;
            }
            QComboBox::down-arrow { image: url(:/qt-project.org/styles/commonstyle/images/standardbutton-down-16.png); }
            QComboBox QAbstractItemView { 
                 background-color: #21252b; border: 1px solid #3e4451;
                 selection-background-color: #61afef; color: #abb2bf;
                 padding: 2px; /* Padding for dropdown items */
            }
            QTabWidget::pane { border-top: 2px solid #61afef; margin-top: -2px; } /* Accent border for pane */
            QTabBar::tab { 
                 background: #21252b; border: 1px solid #3e4451;
                 border-bottom: none; /* Remove bottom border for active tab illusion */
                 border-top-left-radius: 5px; border-top-right-radius: 5px;
                 min-width: 12ex; /* Wider tabs */
                 padding: 8px 18px; 
                 color: #7f8c8d; font-weight: bold;
            }
            QTabBar::tab:selected {
                 background: #282c34; /* Match window bg */
                 color: #61afef; /* Accent color for selected tab text */
                 border-color: #61afef; /* Accent border for selected tab */
                 border-bottom: 2px solid #282c34; /* Blend with pane */
            }
            QTabBar::tab:hover:!selected {
                 background: #2c313a;
                 color: #bdc3c7;
            }
            QTabBar::tab:!selected { margin-top: 2px; }
        """)

        self.tabs = QTabWidget()
        self.main_tab = QWidget() 
        self.edit_tab = ImageEditTab(parent=self) 
        self.edit_tab.back_button.clicked.connect(self.on_back_to_gallery)

        self.tabs.addTab(self.main_tab, "Gallery & Preview") # Corrected typo
        self.tabs.addTab(self.edit_tab, "Image Editor")
        self.tabs.setTabVisible(1, False)  

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10,10,10,10) # Overall window margins
        main_layout.addWidget(self.tabs)
        self.setup_main_tab_ui()

    def setup_main_tab_ui(self):
        layout = QHBoxLayout(self.main_tab)
        # Margins are now handled by QGroupBox or main_layout
        layout.setSpacing(15) 

        # Left pane: Gallery list
        gallery_group = QGroupBox("Image Gallery")
        gallery_layout_outer = QVBoxLayout(gallery_group) # This layout is for the QGroupBox
        gallery_layout_outer.setSpacing(8) # Spacing within the gallery groupbox

        gallery_controls_layout = QHBoxLayout() 
        gallery_controls_layout.setSpacing(10)
        sort_label = QLabel("Sort by:")
        gallery_controls_layout.addWidget(sort_label)
        self.sort_combo = QtWidgets.QComboBox()
        self.sort_combo.addItems(["Name Asc", "Name Desc", "Date Modified", "Size"])
        self.sort_combo.currentIndexChanged.connect(self.load_gallery)
        gallery_controls_layout.addWidget(self.sort_combo, 1) # Add stretch factor
        
        self.open_button = QPushButton("Open External") # Shorter text
        self.open_button.setToolTip("Open an image file from any location")
        self.open_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.open_button.clicked.connect(self.open_image_dialog)
        gallery_controls_layout.addWidget(self.open_button)
        gallery_layout_outer.addLayout(gallery_controls_layout)


        self.gallery_list = QtWidgets.QListWidget()
        self.gallery_list.setIconSize(QSize(70, 70)) # Slightly smaller icons for tighter list
        self.gallery_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.gallery_list.itemSelectionChanged.connect(self.on_gallery_selection_changed)
        gallery_layout_outer.addWidget(self.gallery_list, stretch=1)

        self.load_more_button = QPushButton("Load More Images")
        self.load_more_button.clicked.connect(self.load_next_batch); self.load_more_button.setEnabled(False)  
        gallery_layout_outer.addWidget(self.load_more_button)

        gallery_action_buttons_layout = QHBoxLayout(); gallery_action_buttons_layout.setSpacing(8) 
        self.delete_button = QPushButton("Delete"); self.delete_button.clicked.connect(self.delete_selected_image); self.delete_button.setEnabled(False)
        gallery_action_buttons_layout.addWidget(self.delete_button)
        self.rename_button = QPushButton("Rename"); self.rename_button.clicked.connect(self.rename_selected_image); self.rename_button.setEnabled(False)
        gallery_action_buttons_layout.addWidget(self.rename_button)
        self.edit_button = QPushButton("Edit Selected"); self.edit_button.clicked.connect(self.open_edit_tab); self.edit_button.setEnabled(False)
        gallery_action_buttons_layout.addWidget(self.edit_button)
        gallery_layout_outer.addLayout(gallery_action_buttons_layout)
        
        gallery_group.setMinimumWidth(280) 
        gallery_group.setMaximumWidth(400) 
        layout.addWidget(gallery_group, stretch=2) # Gallery takes 2 parts of stretch


        # Right pane: Preview and controls
        preview_group = QGroupBox("Image Preview & Actions") 
        preview_layout_outer = QVBoxLayout(preview_group)
        preview_layout_outer.setSpacing(8) # Spacing within the preview groupbox

        # No separate title label, QGroupBox title is used.
        # self.preview_title_label = QLabel("Image Preview"); # Removed
        # self.preview_title_label.setObjectName("titleLabel") 
        # self.preview_title_label.setAlignment(Qt.AlignCenter)
        # preview_layout_outer.addWidget(self.preview_title_label)

        self.scroll_area = PannableScrollArea()
        self.scroll_area.setBackgroundRole(QtGui.QPalette.Window) 
        self.image_display_widget = ImageDisplayWidget() 
        self.scroll_area.setWidget(self.image_display_widget)
        self.scroll_area.setMinimumSize(300, 200) # Adjusted min size
        preview_layout_outer.addWidget(self.scroll_area, stretch=1) 

        # Image Info and Status
        info_status_layout = QVBoxLayout(); info_status_layout.setSpacing(4) # Increased spacing
        self.info_filename_label = QLabel("File: N/A"); self.info_filename_label.setObjectName("infoLabel")
        self.info_resolution_label = QLabel("Resolution: N/A"); self.info_resolution_label.setObjectName("infoLabel")
        self.info_size_label = QLabel("Size: N/A"); self.info_size_label.setObjectName("infoLabel")
        self.status_label = QLabel("No image selected."); self.status_label.setObjectName("statusLabel")
        info_status_layout.addWidget(self.info_filename_label); info_status_layout.addWidget(self.info_resolution_label)
        info_status_layout.addWidget(self.info_size_label); 
        preview_layout_outer.addLayout(info_status_layout)
        preview_layout_outer.addWidget(self.status_label) # Status label separate for more emphasis


        # Zoom controls
        zoom_controls_layout = QHBoxLayout(); zoom_controls_layout.setSpacing(8)
        self.zoom_out_button = QPushButton("Zoom Out (-)"); self.zoom_out_button.setToolTip("Zoom Out (Mouse Wheel Down)"); self.zoom_out_button.clicked.connect(self.zoom_out)
        zoom_controls_layout.addWidget(self.zoom_out_button)
        self.zoom_in_button = QPushButton("Zoom In (+)"); self.zoom_in_button.setToolTip("Zoom In (Mouse Wheel Up)"); self.zoom_in_button.clicked.connect(self.zoom_in)
        zoom_controls_layout.addWidget(self.zoom_in_button)
        self.fit_button = QPushButton("Fit to View"); self.fit_button.setToolTip("Zoom to Fit Preview Area"); self.fit_button.clicked.connect(self.zoom_to_fit)
        zoom_controls_layout.addWidget(self.fit_button); zoom_controls_layout.addStretch()
        preview_layout_outer.addLayout(zoom_controls_layout)

        # Main action buttons (Set Wallpaper, Cancel)
        main_action_layout = QHBoxLayout(); main_action_layout.setSpacing(10); 
        main_action_layout.addStretch() 
        self.set_button = QPushButton("Set as Wallpaper"); self.set_button.clicked.connect(self.set_wallpaper); self.set_button.setEnabled(False)
        main_action_layout.addWidget(self.set_button)
        self.cancel_button = QPushButton("Close Editor"); self.cancel_button.clicked.connect(self.cancel)
        main_action_layout.addWidget(self.cancel_button)
        preview_layout_outer.addLayout(main_action_layout)
        layout.addWidget(preview_group, stretch=5) # Preview takes 5 parts of stretch

    def keyPressEvent(self, event):
        active_tab_index = self.tabs.currentIndex()
        if event.key() == QtCore.Qt.Key_Escape: # Corrected: Qt.Key_Escape to QtCore.Qt.Key_Escape
            if active_tab_index == 1: self.on_back_to_gallery()
            else: self.cancel()
            event.accept(); return

        if active_tab_index == 0: 
            if event.key() == QtCore.Qt.Key_Up or event.key() == QtCore.Qt.Key_Left: # Corrected
                current_row = self.gallery_list.currentRow()
                if current_row > 0: self.gallery_list.setCurrentRow(current_row - 1)
                elif self.gallery_list.count() > 0: self.gallery_list.setCurrentRow(self.gallery_list.count() - 1)
                event.accept()
            elif event.key() == QtCore.Qt.Key_Down or event.key() == QtCore.Qt.Key_Right: # Corrected
                current_row = self.gallery_list.currentRow()
                if current_row < self.gallery_list.count() - 1: self.gallery_list.setCurrentRow(current_row + 1)
                elif self.gallery_list.count() > 0: self.gallery_list.setCurrentRow(0)
                event.accept()
            elif event.key() == QtCore.Qt.Key_Delete: # Corrected
                 if self.delete_button.isEnabled(): self.delete_selected_image(); event.accept()
            elif event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter: # Corrected
                 if self.edit_button.isEnabled(): self.open_edit_tab(); event.accept()
                 elif self.set_button.isEnabled(): self.set_wallpaper(); event.accept()
            else: super().keyPressEvent(event)
        
        elif active_tab_index == 1: 
            modifiers = QtWidgets.QApplication.keyboardModifiers()
            if modifiers == QtCore.Qt.ControlModifier:
                if event.key() == QtCore.Qt.Key_Z:  # Corrected
                    if self.edit_tab.undo_button.isEnabled(): self.edit_tab.undo(); event.accept()
                elif event.key() == QtCore.Qt.Key_Y: # Corrected
                    if self.edit_tab.redo_button.isEnabled(): self.edit_tab.redo(); event.accept()
                elif event.key() == QtCore.Qt.Key_S:  # Corrected
                    if self.edit_tab.save_button.isEnabled(): self.edit_tab.save_image(); event.accept()
                elif event.key() == QtCore.Qt.Key_O: self.open_image_dialog(); event.accept() # Corrected
            elif event.key() == QtCore.Qt.Key_R and modifiers == (QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier) : # Corrected
                if self.edit_tab.reset_button.isEnabled(): self.edit_tab.reset_edits(); event.accept()
            else: super().keyPressEvent(event) 
        else: super().keyPressEvent(event)

    def load_gallery(self):
        current_selection_path = self.current_image_path 
        self.gallery_list.clear(); self.all_image_paths = []
        if not os.path.exists(self.image_folder):
            try: os.makedirs(self.image_folder)
            except OSError as e:
                 QMessageBox.critical(self, "Error", f"Could not create image folder: {self.image_folder}\n{e}"); self.close(); return
        for filename in os.listdir(self.image_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')):
                self.all_image_paths.append(os.path.join(self.image_folder, filename))
        self.sort_all_images(); self.current_batch = 1; self.load_batch_images() 
        restored_selection = False
        if current_selection_path and current_selection_path in self.displayed_images:
            for i in range(self.gallery_list.count()):
                if self.gallery_list.item(i).data(QtCore.Qt.UserRole) == current_selection_path: # Corrected
                    self.gallery_list.setCurrentRow(i); restored_selection = True; break
        if not restored_selection and self.gallery_list.count() > 0: self.gallery_list.setCurrentRow(0)
        elif self.gallery_list.count() == 0:
             self.image_display_widget.clear() 
             self.current_image_path = None; self.original_pixmap = None
             self.info_filename_label.setText("File: N/A"); self.info_resolution_label.setText("Resolution: N/A"); self.info_size_label.setText("Size: N/A")
             self.delete_button.setEnabled(False); self.rename_button.setEnabled(False); self.set_button.setEnabled(False); self.edit_button.setEnabled(False)
        self.update_status_label(); self.update_load_more_button_state()

    def update_status_label(self):
        total_images = len(self.all_image_paths); displayed_count = len(self.displayed_images)
        status_text = f"Displaying {displayed_count} of {total_images} images. " if total_images > 0 else "No images found. "
        if self.current_image_path: status_text += f"Selected: {os.path.basename(self.current_image_path)}"
        self.status_label.setText(status_text)
        # Update the main window's status bar if it exists (it doesn't by default for QWidget)
        # If you were using QMainWindow, you could do: self.statusBar().showMessage(status_text)


    def on_gallery_selection_changed(self):
        selected_items = self.gallery_list.selectedItems()
        if not selected_items:
            # self.image_display_widget.clear() # Avoid clearing if selection is temporarily lost
            # self.info_filename_label.setText("File: N/A"); self.info_resolution_label.setText("Resolution: N/A"); self.info_size_label.setText("Size: N/A")
            # self.status_label.setText("No image selected.") # Keep last status or a generic one
            self.delete_button.setEnabled(False); self.rename_button.setEnabled(False); self.set_button.setEnabled(False); self.edit_button.setEnabled(False); return
        image_path = selected_items[0].data(QtCore.Qt.UserRole) # Corrected
        if not image_path or not os.path.exists(image_path):
             QMessageBox.warning(self, "Error", f"Invalid image path:\n{image_path}")
             if image_path in self.all_image_paths: self.all_image_paths.remove(image_path)
             if image_path in self.displayed_images: self.displayed_images.remove(image_path)
             self.gallery_list.takeItem(self.gallery_list.row(selected_items[0])); self.update_status_label(); return
        self.select_image(image_path)
        self.delete_button.setEnabled(True); self.rename_button.setEnabled(True); self.set_button.setEnabled(True); self.edit_button.setEnabled(True)

    def select_image(self, image_path):
        if not os.path.exists(image_path):
            self.status_label.setText(f"Error: File not found: {os.path.basename(image_path)}")
            self.image_display_widget.clear(); self.original_pixmap = None; self.set_button.setEnabled(False); self.current_image_path = None 
            self.info_filename_label.setText("File: N/A"); self.info_resolution_label.setText("Resolution: N/A"); self.info_size_label.setText("Size: N/A"); return
        try:
            pixmap = QtGui.QPixmap(image_path)
            if pixmap.isNull():
                try:
                    pil_img = PIL.Image.open(image_path).convert("RGBA")
                    q_image = QtGui.QImage(pil_img.tobytes("raw", "RGBA"), pil_img.width, pil_img.height, QtGui.QImage.Format_RGBA8888)
                    pixmap = QtGui.QPixmap.fromImage(q_image)
                    if pixmap.isNull(): raise ValueError("Pixmap null after PIL.")
                except Exception as pil_e:
                    self.status_label.setText(f"Error loading: {os.path.basename(image_path)}. PIL: {pil_e}")
                    self.image_display_widget.clear(); self.original_pixmap = None; self.set_button.setEnabled(False); self.current_image_path = None; return
            self.current_image_path = image_path; self.original_pixmap = pixmap; self.scale_factor = 1.0 
            self.zoom_to_fit(); self.update_status_label(); self.set_button.setEnabled(True)
            width = pixmap.width(); height = pixmap.height()
            self.info_filename_label.setText(f"File: {os.path.basename(image_path)}"); self.info_resolution_label.setText(f"Resolution: {width}x{height}")
            size_bytes = os.path.getsize(image_path)
            if size_bytes < 1024: size_str = f"{size_bytes} B"
            elif size_bytes < 1024*1024: size_str = f"{size_bytes/1024:.2f} KB"
            else: size_str = f"{size_bytes/(1024*1024):.2f} MB"
            self.info_size_label.setText(f"Size: {size_str}")
        except Exception as e:
            self.status_label.setText(f"Error displaying {os.path.basename(image_path)}: {e}")
            self.image_display_widget.clear(); self.original_pixmap = None; self.set_button.setEnabled(False); self.current_image_path = None

    def update_image_display(self):
        if self.current_image_path and self.original_pixmap and not self.original_pixmap.isNull():
            self.scale_factor = max(0.01, self.scale_factor) 
            scaled_size = self.original_pixmap.size() * self.scale_factor
            max_dim = 16384 
            if scaled_size.width() > max_dim or scaled_size.height() > max_dim:
                 scale_x = max_dim / self.original_pixmap.width() if self.original_pixmap.width() > 0 else 1
                 scale_y = max_dim / self.original_pixmap.height() if self.original_pixmap.height() > 0 else 1
                 self.scale_factor = min(scale_x, scale_y, self.scale_factor); scaled_size = self.original_pixmap.size() * self.scale_factor
            scaled_pixmap = self.original_pixmap.scaled(scaled_size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self.image_display_widget.setPixmap(scaled_pixmap)
        else: self.image_display_widget.clear()

    def zoom_to_fit(self):
        if not self.original_pixmap or self.original_pixmap.isNull(): return
        viewport_size = self.scroll_area.viewport().size()
        sb_width = self.scroll_area.verticalScrollBar().width() if self.scroll_area.verticalScrollBarPolicy() != QtCore.Qt.ScrollBarAlwaysOff and self.scroll_area.verticalScrollBar().isVisible() else 0 # Corrected
        sb_height = self.scroll_area.horizontalScrollBar().height() if self.scroll_area.horizontalScrollBarPolicy() != QtCore.Qt.ScrollBarAlwaysOff and self.scroll_area.horizontalScrollBar().isVisible() else 0 # Corrected
        available_width = max(1, viewport_size.width() - sb_width); available_height = max(1, viewport_size.height() - sb_height)
        pixmap_size = self.original_pixmap.size()
        if pixmap_size.width() <= 0 or pixmap_size.height() <= 0: return 
        width_scale = available_width / pixmap_size.width(); height_scale = available_height / pixmap_size.height()
        self.scale_factor = min(width_scale, height_scale, 1.0) 
        self.update_image_display()
        self.scroll_area.horizontalScrollBar().setValue(0); self.scroll_area.verticalScrollBar().setValue(0)

    def zoom_in(self):
        if not self.original_pixmap: return
        center_h_ratio = (self.scroll_area.horizontalScrollBar().value() + self.scroll_area.viewport().width() / 2) / (self.image_display_widget.width() or 1)
        center_v_ratio = (self.scroll_area.verticalScrollBar().value() + self.scroll_area.viewport().height() / 2) / (self.image_display_widget.height() or 1)
        self.scale_factor *= 1.25; self.update_image_display()
        new_h_scroll = center_h_ratio * self.image_display_widget.width() - self.scroll_area.viewport().width() / 2
        new_v_scroll = center_v_ratio * self.image_display_widget.height() - self.scroll_area.viewport().height() / 2
        self.scroll_area.horizontalScrollBar().setValue(int(new_h_scroll)); self.scroll_area.verticalScrollBar().setValue(int(new_v_scroll))

    def zoom_out(self):
        if not self.original_pixmap: return
        center_h_ratio = (self.scroll_area.horizontalScrollBar().value() + self.scroll_area.viewport().width() / 2) / (self.image_display_widget.width() or 1)
        center_v_ratio = (self.scroll_area.verticalScrollBar().value() + self.scroll_area.viewport().height() / 2) / (self.image_display_widget.height() or 1)
        self.scale_factor /= 1.25; self.update_image_display()
        new_h_scroll = center_h_ratio * self.image_display_widget.width() - self.scroll_area.viewport().width() / 2
        new_v_scroll = center_v_ratio * self.image_display_widget.height() - self.scroll_area.viewport().height() / 2
        self.scroll_area.horizontalScrollBar().setValue(int(new_h_scroll)); self.scroll_area.verticalScrollBar().setValue(int(new_v_scroll))

    def wheelEvent(self, event: QtGui.QWheelEvent):
        if self.scroll_area.underMouse():
            if event.angleDelta().y() > 0: self.zoom_in()
            else: self.zoom_out()
            event.accept() 
        else: super().wheelEvent(event)

    def sort_all_images(self):
        if not self.all_image_paths: return
        sort_option = self.sort_combo.currentText(); metadata_list = []
        for path in self.all_image_paths:
            try:
                stat = os.stat(path)
                metadata_list.append({'path': path, 'name': os.path.basename(path).lower(), 'mtime': stat.st_mtime, 'size': stat.st_size})
            except Exception: metadata_list.append({'path': path, 'name': os.path.basename(path).lower(), 'mtime': 0, 'size': 0})
        if sort_option == "Name Asc": metadata_list.sort(key=lambda x: x['name'])
        elif sort_option == "Name Desc": metadata_list.sort(key=lambda x: x['name'], reverse=True)
        elif sort_option == "Date Modified": metadata_list.sort(key=lambda x: x['mtime'], reverse=True)
        elif sort_option == "Size": metadata_list.sort(key=lambda x: x['size'], reverse=True)
        self.all_image_paths = [item['path'] for item in metadata_list]

    def load_batch_images(self):
        start_idx = (self.current_batch - 1) * self.batch_size; end_idx = start_idx + self.batch_size 
        batch_paths = self.all_image_paths[start_idx:end_idx]
        if self.current_batch == 1: self.gallery_list.clear(); self.displayed_images = []
        for path in batch_paths:
             if path not in self.displayed_images: 
                 try: icon = QtGui.QIcon(path) 
                 except Exception: icon = QtGui.QIcon() 
                 list_item = QtWidgets.QListWidgetItem(icon, os.path.basename(path))
                 list_item.setData(QtCore.Qt.UserRole, path); self.gallery_list.addItem(list_item); self.displayed_images.append(path) # Corrected
        self.update_load_more_button_state()

    def load_next_batch(self):
        if self.current_batch * self.batch_size < len(self.all_image_paths):
            self.current_batch += 1; self.load_batch_images(); self.update_status_label() 

    def update_load_more_button_state(self):
        remaining = len(self.all_image_paths) - len(self.displayed_images)
        if remaining > 0: self.load_more_button.setEnabled(True); self.load_more_button.setText(f"Load More ({remaining} remaining)")
        else: self.load_more_button.setEnabled(False); self.load_more_button.setText("All Images Loaded")

    def delete_selected_image(self):
        selected_items = self.gallery_list.selectedItems()
        if not selected_items: return
        image_path = selected_items[0].data(QtCore.Qt.UserRole) # Corrected
        reply = QMessageBox.question(self, 'Delete Image', f"Delete '{os.path.basename(image_path)}'?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                os.remove(image_path)
                if image_path in self.all_image_paths: self.all_image_paths.remove(image_path)
                if image_path in self.displayed_images: self.displayed_images.remove(image_path)
                row = self.gallery_list.row(selected_items[0]); self.gallery_list.takeItem(row)
                if self.gallery_list.count() > 0:
                     self.gallery_list.setCurrentRow(max(0, min(row, self.gallery_list.count() - 1)))
                else: self.on_gallery_selection_changed() 
                self.update_status_label(); self.update_load_more_button_state() 
            except Exception as e: QMessageBox.warning(self, "Delete Image", f"Failed to delete: {e}")

    def rename_selected_image(self):
        selected_items = self.gallery_list.selectedItems();
        if not selected_items: return
        current_item = selected_items[0]; current_image_path = current_item.data(QtCore.Qt.UserRole) # Corrected
        current_image_name = os.path.basename(current_image_path); current_dir = os.path.dirname(current_image_path)
        new_name, ok = QInputDialog.getText(self, "Rename Image", "New name (with extension):", QtWidgets.QLineEdit.Normal, current_image_name)
        if ok and new_name and new_name != current_image_name:
            if any(c in new_name for c in r'/\:*?"<>|'): QMessageBox.warning(self, "Rename Image", "Invalid characters."); return
            _, current_ext = os.path.splitext(current_image_name); new_base, new_ext = os.path.splitext(new_name)
            if not new_ext: new_name += current_ext 
            new_path = os.path.join(current_dir, new_name)
            if os.path.exists(new_path): QMessageBox.warning(self, "Rename Image", f"'{new_name}' already exists."); return
            try:
                os.rename(current_image_path, new_path)
                if current_image_path in self.all_image_paths: self.all_image_paths[self.all_image_paths.index(current_image_path)] = new_path
                if current_image_path in self.displayed_images: self.displayed_images[self.displayed_images.index(current_image_path)] = new_path
                current_item.setText(new_name); current_item.setData(QtCore.Qt.UserRole, new_path) # Corrected
                self.current_image_path = new_path; self.select_image(new_path) 
                if "Name" in self.sort_combo.currentText(): self.load_gallery() 
            except Exception as e: QMessageBox.warning(self, "Rename Image", f"Failed to rename: {e}")

    def open_edit_tab(self):
        selected_items = self.gallery_list.selectedItems()
        image_path_to_edit = self.current_image_path if not selected_items and self.current_image_path and os.path.exists(self.current_image_path) else (selected_items[0].data(QtCore.Qt.UserRole) if selected_items else None) # Corrected
        if not image_path_to_edit: QMessageBox.information(self, "Edit Image", "Select an image or open an external one."); return
        if not os.path.exists(image_path_to_edit): QMessageBox.warning(self, "Edit Image", "Image path invalid."); return
        self.edit_tab.load_image(image_path_to_edit)
        self.tabs.setTabVisible(1, True); self.tabs.setCurrentIndex(1)

    def set_wallpaper(self):
        if self.current_image_path and self.set_wallpaper_callback:
            try:
                if not os.path.exists(self.current_image_path): QMessageBox.warning(self, "Set Wallpaper", "File not found."); return
                self.set_wallpaper_callback(self.current_image_path); self.result = True; self.close() 
            except Exception as e: QMessageBox.critical(self, "Set Wallpaper Error", f"Failed: {e}")
        elif not self.current_image_path: QMessageBox.warning(self, "Set Wallpaper", "No image selected.")
        elif not self.set_wallpaper_callback: QMessageBox.warning(self, "Set Wallpaper", "Callback not available.")

    def cancel(self): self.result = False; self.close()

    def open_image_dialog(self):
        options = QFileDialog.Options()
        start_dir = os.path.expanduser("~/Pictures") if os.path.exists(os.path.expanduser("~/Pictures")) else self.image_folder
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", start_dir, "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp);;All Files (*)", options=options)
        if file_path:
            is_in_gallery_folder = os.path.dirname(file_path) == os.path.abspath(self.image_folder)
            item_in_list = next((self.gallery_list.item(i) for i in range(self.gallery_list.count()) if self.gallery_list.item(i).data(QtCore.Qt.UserRole) == file_path), None) # Corrected
            if item_in_list: self.gallery_list.setCurrentItem(item_in_list)
            elif is_in_gallery_folder:
                 if file_path not in self.all_image_paths: self.all_image_paths.append(file_path); self.sort_all_images()
                 self.select_image(file_path); self.gallery_list.clearSelection()
                 self.delete_button.setEnabled(False); self.rename_button.setEnabled(False)
                 self.edit_button.setEnabled(True); self.set_button.setEnabled(True)
            else: 
                 self.select_image(file_path); self.gallery_list.clearSelection()
                 self.delete_button.setEnabled(False); self.rename_button.setEnabled(False)
                 self.edit_button.setEnabled(True); self.set_button.setEnabled(True)

    def run(self):
        self.show(); return self.app.exec_(), self.result, self.current_image_path 

    def on_back_to_gallery(self):
        image_still_valid = False
        if self.edit_tab.image_path and os.path.exists(self.edit_tab.image_path):
            if self.edit_tab.image_path == self.current_image_path: image_still_valid = True
            else:
                for i in range(self.gallery_list.count()):
                    if self.gallery_list.item(i).data(QtCore.Qt.UserRole) == self.edit_tab.image_path: # Corrected
                        self.gallery_list.setCurrentRow(i); image_still_valid = True; break
        if not image_still_valid:
            if self.current_image_path and os.path.exists(self.current_image_path):
                found_in_gallery = any(self.gallery_list.item(i).data(QtCore.Qt.UserRole) == self.current_image_path for i in range(self.gallery_list.count())) # Corrected
                if found_in_gallery: self.gallery_list.setCurrentRow([i for i in range(self.gallery_list.count()) if self.gallery_list.item(i).data(QtCore.Qt.UserRole) == self.current_image_path][0]) # Corrected
                else: self.select_image(self.current_image_path)
            else: self.load_gallery()
        self.tabs.setCurrentIndex(0); self.tabs.setTabVisible(1, False)

    def closeEvent(self, event: QtGui.QCloseEvent): # Added type hint
         if not hasattr(self, 'result') or self.result is None: self.result = False
         print(f"Closing Image Manager. Result: {self.result}, Path: {self.current_image_path}")
         if self.edit_tab and hasattr(self.edit_tab, 'history'): # Check if edit_tab and history exist
             # Clear history stacks directly
             if hasattr(self.edit_tab.history, 'undo_stack'):
                 self.edit_tab.history.undo_stack.clear()
             if hasattr(self.edit_tab.history, 'redo_stack'):
                 self.edit_tab.history.redo_stack.clear()
            
             # Nullify image references to potentially help with garbage collection
             self.edit_tab.original_image = None
             self.edit_tab.edited_image = None
         super().closeEvent(event)
