from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
from .image_label import ImageLabel

class ReferenceWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window)  # Use Qt.Window flag to create an independent window
        self.setWindowTitle("Original Image Reference")
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
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))
        self.image_label.setGridSize(*grid_size)