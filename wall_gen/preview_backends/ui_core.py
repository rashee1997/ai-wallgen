# preview_backends/ui_core.py
"""
Core UI components for the Qt image preview and editor.
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

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

    def mousePressEvent(self, event: QtGui.QMouseEvent):
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

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
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

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
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
    Custom widget for displaying the image.
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
    
    def clear(self):
        """Clears the displayed pixmap."""
        self.setPixmap(QtGui.QPixmap()) # Set an empty pixmap
        self.setFixedSize(0,0) # Reset size
        self.update()


    def paintEvent(self, event: QtGui.QPaintEvent):
        """Override paint event to draw the pixmap."""
        painter = QtGui.QPainter(self) # Paint on this widget

        if self._pixmap.isNull():
            return # Nothing to draw

        # Draw the image pixmap
        painter.drawPixmap(self.rect(), self._pixmap)
        painter.end() # End the painter
