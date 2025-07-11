from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QSlider,
    QSpinBox,
)
from PySide6.QtCore import Qt, Signal


class SlidersWindow(QWidget):
    thresholds_changed = Signal(list)

    def __init__(self, parent=None):
        super().__init__(
            parent, Qt.Window
        )  # Use Qt.Window flag to create an independent window
        self.setWindowTitle("Threshold Sliders")
        self.ratio_labels = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Grid size inputs
        control_layout = QGridLayout()
        self.n_input = QSpinBox()
        self.n_input.setRange(1, 10)
        self.n_input.setValue(3)
        self.n_input.setPrefix("Rows: ")
        self.n_input.valueChanged.connect(self.update_grid_size)
        control_layout.addWidget(self.n_input, 0, 0)

        self.m_input = QSpinBox()
        self.m_input.setRange(1, 10)
        self.m_input.setValue(3)
        self.m_input.setPrefix("Cols: ")
        self.m_input.valueChanged.connect(self.update_grid_size)
        control_layout.addWidget(self.m_input, 0, 1)

        layout.addLayout(control_layout)

        # Container for sliders
        self.sliders_container = QWidget()
        self.sliders_layout = QVBoxLayout()
        self.sliders_container.setLayout(self.sliders_layout)
        layout.addWidget(self.sliders_container)

        self.setLayout(layout)
        self.create_sliders()

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())
                    item.layout().deleteLater()

    def create_sliders(self):
        self.clear_layout(self.sliders_layout)
        self.sliders = []
        self.ratio_labels = []
        n, m = self.n_input.value(), self.m_input.value()

        for i in range(n):
            row_layout = QHBoxLayout()
            for j in range(m):
                slider_layout = QVBoxLayout()

                # Threshold slider and label
                slider_label = QLabel(f"Threshold [{i + 1}, {j + 1}]: 160")
                slider = QSlider(Qt.Horizontal)
                slider.setRange(0, 255)
                slider.setValue(160)
                slider.setTickInterval(5)

                # Colored ratio label
                ratio_label = QLabel("Colored: 0%")
                ratio_label.setAlignment(Qt.AlignCenter)
                self.ratio_labels.append(ratio_label)

                def create_slider_callback(label, row, col):
                    return lambda value: (
                        label.setText(f"Threshold [{row + 1}, {col + 1}]: {value}"),
                        self.on_slider_change(),
                    )

                slider.valueChanged.connect(create_slider_callback(slider_label, i, j))
                self.sliders.append(slider)

                slider_layout.addWidget(slider_label)
                slider_layout.addWidget(slider)
                slider_layout.addWidget(ratio_label)
                row_layout.addLayout(slider_layout)

            self.sliders_layout.addLayout(row_layout)

        # Emit initial values
        self.on_slider_change()

    def update_grid_size(self):
        self.create_sliders()

    def on_slider_change(self):
        values = [slider.value() for slider in self.sliders]
        self.thresholds_changed.emit(values)

    def get_grid_size(self):
        return self.n_input.value(), self.m_input.value()

    def update_dark_ratios(self, ratios):
        for i, label in enumerate(self.ratio_labels):
            row = i // self.m_input.value()
            col = i % self.m_input.value()
            label.setText(f"Colored: {ratios[row, col]:.1f}%")
