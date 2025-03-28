from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                              QPushButton, QFileDialog, QLabel,
                              QRadioButton, QButtonGroup)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, QPoint
from PIL import Image

from .widgets import ImageLabel, ReferenceWindow, SlidersWindow
from .image_processing import process_image

class ImageThresholdApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DarkCoverage - Image Threshold Adjustment")
        self.threshold_values = []  # Initialize threshold_values 
        
        # Create windows
        self.sliders_window = SlidersWindow()
        self.reference_window = ReferenceWindow()
        self.sliders_window.thresholds_changed.connect(self.on_thresholds_changed)
        
        # Position the windows smartly but keep original sizes
        base_x, base_y = 100, 100
        self.move(base_x, base_y)  # Main window position
        
        # Position slider window to the right of main window
        self.sliders_window.move(base_x + 450, base_y)
        self.sliders_window.show()
        
        # Initialize threshold_values with default values
        n, m = self.sliders_window.get_grid_size()
        self.threshold_values = [160] * (n * m) 
        
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Image display using custom ImageLabel
        self.image_label = ImageLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setText("Load an image to process")
        layout.addWidget(self.image_label)
        
        # Color mode selection
        color_mode_layout = QHBoxLayout()
        self.color_mode_group = QButtonGroup()
        
        self.dark_parts_radio = QRadioButton("Color Dark Parts")
        self.light_parts_radio = QRadioButton("Color Light Parts")
        self.dark_parts_radio.setChecked(True)  # Default selection
        
        self.color_mode_group.addButton(self.dark_parts_radio)
        self.color_mode_group.addButton(self.light_parts_radio)
        
        color_mode_layout.addWidget(self.dark_parts_radio)
        color_mode_layout.addWidget(self.light_parts_radio)
        
        # Connect radio buttons to process image
        self.dark_parts_radio.toggled.connect(self.process_image)
        self.light_parts_radio.toggled.connect(self.process_image)
        
        layout.addLayout(color_mode_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        # Load image button
        self.load_button = QPushButton("Load Image")
        self.load_button.clicked.connect(self.load_image)
        button_layout.addWidget(self.load_button)
        
        # Save button
        self.save_button = QPushButton("Save Image")
        self.save_button.clicked.connect(self.save_image)
        button_layout.addWidget(self.save_button)
        
        # Reset button
        self.reset_button = QPushButton("Reset Image")
        self.reset_button.clicked.connect(self.reset_image)
        button_layout.addWidget(self.reset_button)
        
        layout.addLayout(button_layout)

        # Add total result label
        self.total_result_label = QLabel("Total Result: 0%")
        self.total_result_label.setAlignment(Qt.AlignCenter)
        font = self.total_result_label.font()
        font.setPointSize(12)  # Make the font a bit larger
        font.setBold(True)     # Make it bold
        self.total_result_label.setFont(font)
        layout.addWidget(self.total_result_label)
        
        self.setLayout(layout)
        
    def on_thresholds_changed(self, values):
        self.threshold_values = values
        # Update grid lines when grid size changes
        n, m = self.sliders_window.get_grid_size()
        self.image_label.setGridSize(n, m)
        if hasattr(self, 'original_image'):
            self.reference_window.image_label.setGridSize(n, m)
            self.process_image()  # Automatically process image when thresholds change
    
    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_name:
            original_color_image = Image.open(file_name)  # Keep original color image
            self.original_image = original_color_image.convert('L')  # Store grayscale for processing
            self.current_image = self.original_image.copy()  # Working copy
            self.update_image_label()
            
            # Update reference window with original color image
            grid_size = self.sliders_window.get_grid_size()
            self.reference_window.update_image(original_color_image, grid_size)
            
            # Position reference window below the main window
            base_x, base_y = self.pos().x(), self.pos().y()
            self.reference_window.move(base_x + 850, base_y)  # Position below main window
            self.reference_window.show()
            
            # Process image immediately after loading
            self.process_image()
    
    def update_image_label(self):
        # Convert the image to RGB if it's not already
        if self.current_image.mode != 'RGB':
            self.current_image = self.current_image.convert('RGB')
        
        qimage = QImage(self.current_image.tobytes(), 
                    self.current_image.width, 
                    self.current_image.height, 
                    self.current_image.width * 3,  # bytes per line 
                    QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        
        # Scale the pixmap while maintaining aspect ratio
        scaled_pixmap = pixmap.scaled(
            400, 400,  # max size
            Qt.KeepAspectRatio,  # maintain aspect ratio
            Qt.SmoothTransformation  # high-quality scaling
        )
        
        self.image_label.setPixmap(scaled_pixmap)
        n, m = self.sliders_window.get_grid_size()
        self.image_label.setGridSize(n, m)
    
    def reset_image(self):
        if hasattr(self, 'original_image'):
            self.current_image = self.original_image.copy()
            self.update_image_label()
    
    def process_image(self):
        if not hasattr(self, 'original_image'):
            return
            
        n, m = self.sliders_window.get_grid_size()
        color_dark_parts = self.dark_parts_radio.isChecked()
        
        processed_img, colored_ratios, total_result = process_image(
            self.original_image, 
            self.threshold_values, 
            (n, m), 
            color_dark_parts
        )
        
        # Update total result
        self.total_result_label.setText(f"Total Result: {total_result:.1f}%")
        
        self.current_image = processed_img
        self.update_image_label()
        self.sliders_window.update_dark_ratios(colored_ratios)
    
    def save_image(self):
        if hasattr(self, 'current_image'):
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", 
                                                     "Images (*.png *.jpg *.jpeg)")
            if file_name:
                self.current_image.save(file_name)