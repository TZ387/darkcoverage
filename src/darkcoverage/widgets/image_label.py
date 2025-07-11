from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt


class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_size = (3, 3)  # Default grid size
        self.setMinimumSize(400, 400)

    def setGridSize(self, n, m):
        self.grid_size = (n, m)
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.pixmap():
            painter = QPainter(self)
            pen = QPen(Qt.green)
            pen.setWidth(2)  # Increase pen thickness
            painter.setPen(pen)

            # Get the actual displayed image size
            pixmap_rect = self.pixmap().rect()
            scaled_rect = pixmap_rect

            # Calculate the offset to center the image
            x_offset = (self.width() - scaled_rect.width()) // 2
            y_offset = (self.height() - scaled_rect.height()) // 2

            width, height = pixmap_rect.width(), pixmap_rect.height()

            # Calculate base cell dimensions and remainders
            base_cell_w = width // self.grid_size[1]
            base_cell_h = height // self.grid_size[0]
            rem_w = width % self.grid_size[1]
            rem_h = height % self.grid_size[0]

            # Draw vertical lines
            x_pos = 0
            for i in range(1, self.grid_size[1]):
                # Add extra pixel for columns that get the remainder
                x_pos += base_cell_w + (1 if i <= rem_w else 0)
                # Scale the position to match the displayed size
                scaled_x = x_offset + (x_pos * scaled_rect.width() // width)
                painter.drawLine(
                    scaled_x, y_offset, scaled_x, y_offset + scaled_rect.height()
                )

            # Draw horizontal lines
            y_pos = 0
            for i in range(1, self.grid_size[0]):
                # Add extra pixel for rows that get the remainder
                y_pos += base_cell_h + (1 if i <= rem_h else 0)
                # Scale the position to match the displayed size
                scaled_y = y_offset + (y_pos * scaled_rect.height() // height)
                painter.drawLine(
                    x_offset, scaled_y, x_offset + scaled_rect.width(), scaled_y
                )
