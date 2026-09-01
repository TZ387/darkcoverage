from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QLabel,
    QRadioButton,
    QButtonGroup,
    QSizePolicy,
    QMessageBox,
)
from PySide6.QtCore import Qt
from PIL import Image

from .widgets import ImageLabel, ReferenceWindow, SlidersWindow
from .image_processing import process_image


class ImageThresholdApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DarkCoverage - Image Threshold Adjustment")
        self._image_version = 0  # Bumped by _set_current_image; drives the pixmap cache

        self.resize(400, 500)  # Slightly larger to accommodate controls

        self.sliders_window = SlidersWindow()
        self.reference_window = ReferenceWindow()
        self.sliders_window.thresholds_changed.connect(self.on_thresholds_changed)

        base_x, base_y = 100, 100
        self.move(base_x, base_y)

        # To the right of the main window
        self.sliders_window.move(base_x + 450, base_y)
        self.sliders_window.show()

        n, m = self.sliders_window.get_grid_size()
        self.threshold_values = [160] * (n * m)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.image_label = ImageLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setText("Load an image to process")
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(self.image_label)

        color_mode_layout = QHBoxLayout()
        color_mode_layout.setContentsMargins(0, 0, 0, 0)
        color_mode_layout.setSpacing(10)

        self.color_mode_group = QButtonGroup()

        self.dark_parts_radio = QRadioButton("Color Dark Parts")
        self.light_parts_radio = QRadioButton("Color Light Parts")
        self.dark_parts_radio.setChecked(True)

        self.color_mode_group.addButton(self.dark_parts_radio)
        self.color_mode_group.addButton(self.light_parts_radio)

        color_mode_layout.addWidget(self.dark_parts_radio)
        color_mode_layout.addWidget(self.light_parts_radio)

        self.dark_parts_radio.toggled.connect(self.process_image)

        radio_widget = QWidget()
        radio_widget.setLayout(color_mode_layout)
        radio_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        radio_widget.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(radio_widget)
        layout.setSpacing(6)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)

        self.load_button = QPushButton("Load Image")
        self.load_button.clicked.connect(self.load_image)
        button_layout.addWidget(self.load_button)

        self.save_button = QPushButton("Save Image")
        self.save_button.clicked.connect(self.save_image)
        button_layout.addWidget(self.save_button)

        self.reset_button = QPushButton("Reset Image")
        self.reset_button.clicked.connect(self.reset_image)
        button_layout.addWidget(self.reset_button)

        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        button_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        button_widget.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(button_widget)

        self.total_result_label = QLabel("Total Result: 0%")
        self.total_result_label.setAlignment(Qt.AlignCenter)
        font = self.total_result_label.font()
        font.setPointSize(12)
        font.setBold(True)
        self.total_result_label.setFont(font)

        self.total_result_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.total_result_label.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.total_result_label)

        layout.setContentsMargins(9, 9, 9, 9)

        # Qt stretch factor: gives image_label the extra space on resize
        layout.setStretchFactor(self.image_label, 10)

        self.setLayout(layout)

    def on_thresholds_changed(self, values):
        self.threshold_values = values
        # thresholds_changed also fires on grid-size changes, so keep grid lines in sync
        n, m = self.sliders_window.get_grid_size()
        self.image_label.setGridSize(n, m)
        if hasattr(self, "original_image"):
            self.reference_window.image_label.setGridSize(n, m)
            self.process_image()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.scale_image()

    def _set_current_image(self, image):
        # Sole place current_image is reassigned, so the version counter
        # can't be forgotten at a call site.
        self.current_image = image
        self._image_version += 1

    def scale_image(self):
        if hasattr(self, "current_image") and self.current_image:
            # Only rebuild the pixmap from current_image if it actually
            # changed; otherwise just rescale the cached one (e.g. on resize).
            if not hasattr(self, "_last_image_version") or self._last_image_version != (
                self._image_version
            ):
                self._last_image_version = self._image_version
                self.image_label.setImage(self.current_image)
            else:
                self.image_label.rescale()

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Images (*.png *.jpg *.jpeg)"
        )
        if file_name:
            try:
                original_color_image = Image.open(file_name)
                original_color_image.load()  # Force read now so bad files fail here
            except (OSError, ValueError) as e:
                QMessageBox.warning(
                    self, "Failed to Load Image", f"Could not open '{file_name}':\n{e}"
                )
                return

            # Thresholding works on luminance, so keep a grayscale copy for processing
            self.original_image = original_color_image.convert("L")
            self._set_current_image(self.original_image.copy())

            self.scale_image()

            grid_size = self.sliders_window.get_grid_size()
            self.reference_window.update_image(original_color_image, grid_size)

            base_x, base_y = self.pos().x(), self.pos().y()
            self.reference_window.move(base_x + 850, base_y)  # To the right
            self.reference_window.show()

            self.process_image()

    def reset_image(self):
        if hasattr(self, "original_image"):
            self._set_current_image(self.original_image.copy())
            self.scale_image()
            # Plain grayscale has nothing colored, so the coverage numbers
            # should reflect that rather than the last-processed values.
            self.total_result_label.setText("Total Result: 0.0%")
            self.sliders_window.reset_ratios()

    def process_image(self):
        if not hasattr(self, "original_image"):
            return

        n, m = self.sliders_window.get_grid_size()
        color_dark_parts = self.dark_parts_radio.isChecked()

        processed_img, colored_ratios, total_result = process_image(
            self.original_image, self.threshold_values, (n, m), color_dark_parts
        )

        self.total_result_label.setText(f"Total Result: {total_result:.1f}%")

        self._set_current_image(processed_img)
        self.scale_image()
        self.sliders_window.update_dark_ratios(colored_ratios)

    def save_image(self):
        if hasattr(self, "current_image"):
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Save Image", "", "Images (*.png *.jpg *.jpeg)"
            )
            if file_name:
                try:
                    self.current_image.save(file_name)
                except (OSError, ValueError) as e:
                    QMessageBox.warning(
                        self,
                        "Failed to Save Image",
                        f"Could not save '{file_name}':\n{e}",
                    )
