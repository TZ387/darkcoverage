from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPainter, QPen, QPixmap, QImage
from PySide6.QtCore import Qt


class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_size = (3, 3)
        self.setMinimumSize(400, 400)
        self.original_pixmap = None

    def setGridSize(self, n, m):
        self.grid_size = (n, m)
        self.update()

    def setImage(self, pil_image):
        """Set the source PIL image to display, scaled to fit the label."""
        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")

        qimage = QImage(
            pil_image.tobytes(),
            pil_image.width,
            pil_image.height,
            pil_image.width * 3,  # bytes per line
            QImage.Format_RGB888,
        )
        self.original_pixmap = QPixmap.fromImage(qimage)
        self.rescale()

    def rescale(self):
        """Rescale the cached source pixmap to fit the label's current size."""
        if self.original_pixmap:
            scaled_pixmap = self.original_pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatio,
                Qt.FastTransformation,  # Faster than SmoothTransformation
            )
            self.setPixmap(scaled_pixmap)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.pixmap():
            painter = QPainter(self)
            pen = QPen(Qt.green)
            pen.setWidth(2)
            painter.setPen(pen)

            pixmap_rect = self.pixmap().rect()

            x_offset = (self.width() - pixmap_rect.width()) // 2
            y_offset = (self.height() - pixmap_rect.height()) // 2

            width, height = pixmap_rect.width(), pixmap_rect.height()

            base_cell_w = width // self.grid_size[1]
            base_cell_h = height // self.grid_size[0]
            rem_w = width % self.grid_size[1]
            rem_h = height % self.grid_size[0]

            x_pos = 0
            for i in range(1, self.grid_size[1]):
                # Add extra pixel for columns that get the remainder
                x_pos += base_cell_w + (1 if i <= rem_w else 0)
                scaled_x = x_offset + x_pos
                painter.drawLine(
                    scaled_x, y_offset, scaled_x, y_offset + pixmap_rect.height()
                )

            y_pos = 0
            for i in range(1, self.grid_size[0]):
                # Add extra pixel for rows that get the remainder
                y_pos += base_cell_h + (1 if i <= rem_h else 0)
                scaled_y = y_offset + y_pos
                painter.drawLine(
                    x_offset, scaled_y, x_offset + pixmap_rect.width(), scaled_y
                )
