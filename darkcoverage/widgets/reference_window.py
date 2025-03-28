from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
from .image_label import ImageLabel

class ReferenceWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window)  # Use Qt.Window flag to create an independent window
        self.setWindowTitle("Original Image Reference")
        self.original_pixmap = None  # Store the original pixmap
        self.init_ui()
       
    def init_ui(self):
        layout = QVBoxLayout()
        self.image_label = ImageLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)
        self.setLayout(layout)
   
    def update_image(self, image, grid_size):
        # Convert PIL Image to QImage maintaining color
        qimage = QImage(image.tobytes("raw", "RGB"),
                        image.width,
                        image.height,
                        image.width * 3,  # bytes per line
                        QImage.Format_RGB888)
        
        # Store the original pixmap
        self.original_pixmap = QPixmap.fromImage(qimage)
       
        # Scale the pixmap to fit the current label size while maintaining aspect ratio
        self.scale_image()
        
        # Set grid size
        self.image_label.setGridSize(*grid_size)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Rescale the image when the window is resized
        self.scale_image()
    
    def scale_image(self):
        if self.original_pixmap:
            # Scale the pixmap to fit the label size, keeping aspect ratio
            scaled_pixmap = self.original_pixmap.scaled(
                self.image_label.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)