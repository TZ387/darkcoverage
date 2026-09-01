from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from .image_label import ImageLabel


class ReferenceWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(
            parent, Qt.Window
        )  # Use Qt.Window flag to create an independent window
        self.setWindowTitle("Original Image Reference")

        # Set a default size for the reference window
        self.resize(400, 400)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.image_label = ImageLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)
        self.setLayout(layout)

    def update_image(self, image, grid_size):
        self.image_label.setImage(image)
        self.image_label.setGridSize(*grid_size)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Rescale the image when the window is resized
        self.image_label.rescale()
