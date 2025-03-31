from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                              QPushButton, QFileDialog, QLabel,
                              QRadioButton, QButtonGroup, QSizePolicy)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
from PIL import Image

from .widgets import ImageLabel, ReferenceWindow, SlidersWindow
from .image_processing import process_image

class ImageThresholdApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DarkCoverage - Image Threshold Adjustment")
        self.threshold_values = []  # Initialize threshold_values 
        self.original_pixmap = None  # Store the original pixmap
        
        # Set a default size for the main window
        self.resize(400, 500)  # Slightly larger to accommodate controls
        
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
        
        # Set size policy to expand both horizontally and vertically
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        layout.addWidget(self.image_label)
        
        # Color mode selection - compact layout
        color_mode_layout = QHBoxLayout()
        color_mode_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        color_mode_layout.setSpacing(10)  # Reduce spacing between radio buttons
        
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
        
        # Set fixed size policy for the radio buttons layout with minimal margins
        radio_widget = QWidget()
        radio_widget.setLayout(color_mode_layout)
        radio_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        radio_widget.setContentsMargins(0, 0, 0, 0)  # Remove margins around the widget
        
        # Add the radio buttons with minimal spacing
        layout.addWidget(radio_widget)
        layout.setSpacing(6)  # Reduce spacing between layout elements
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        
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
        
        # Set fixed size policy for the button layout with minimal margins
        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        button_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        button_widget.setContentsMargins(0, 0, 0, 0)  # Remove margins around the widget
        
        layout.addWidget(button_widget)

        # Add total result label with fixed size policy
        self.total_result_label = QLabel("Total Result: 0%")
        self.total_result_label.setAlignment(Qt.AlignCenter)
        font = self.total_result_label.font()
        font.setPointSize(12)  # Make the font a bit larger
        font.setBold(True)     # Make it bold
        self.total_result_label.setFont(font)
        
        # Set a fixed size policy for the label
        self.total_result_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.total_result_label.setContentsMargins(0, 0, 0, 0)  # Remove margins
        
        layout.addWidget(self.total_result_label)
        
        # Reduce margins around the main layout to make everything more compact
        layout.setContentsMargins(9, 9, 9, 9)  # Slightly smaller than default
        
        # Set layout stretch factors to make image_label take all extra space
        layout.setStretchFactor(self.image_label, 10)
        
        self.setLayout(layout)
        
    def on_thresholds_changed(self, values):
        self.threshold_values = values
        # Update grid lines when grid size changes
        n, m = self.sliders_window.get_grid_size()
        self.image_label.setGridSize(n, m)
        if hasattr(self, 'original_image'):
            self.reference_window.image_label.setGridSize(n, m)
            self.process_image()  # Automatically process image when thresholds change

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Rescale the image when the window is resized
        self.scale_image()

    def scale_image(self):
        if hasattr(self, 'current_image') and self.current_image:
            # Create QImage from the current PIL image
            if self.current_image.mode != 'RGB':
                img = self.current_image.convert('RGB')
            else:
                img = self.current_image
                
            qimage = QImage(img.tobytes(), 
                        img.width, 
                        img.height, 
                        img.width * 3,  # bytes per line 
                        QImage.Format_RGB888)
            
            self.original_pixmap = QPixmap.fromImage(qimage)
            
            # Scale the pixmap to fit the label size, keeping aspect ratio
            scaled_pixmap = self.original_pixmap.scaled(
                self.image_label.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            
            self.image_label.setPixmap(scaled_pixmap)
            n, m = self.sliders_window.get_grid_size()
            self.image_label.setGridSize(n, m)
    
    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_name:
            original_color_image = Image.open(file_name)  # Keep original color image
            self.original_image = original_color_image.convert('L')  # Store grayscale for processing
            self.current_image = self.original_image.copy()  # Working copy
            
            # Update the image display
            self.update_image_label()
            
            # Update reference window with original color image
            grid_size = self.sliders_window.get_grid_size()
            self.reference_window.update_image(original_color_image, grid_size)
            
            # Position reference window below the main window
            base_x, base_y = self.pos().x(), self.pos().y()
            self.reference_window.move(base_x + 850, base_y)  # Position to the right
            self.reference_window.show()
            
            # Process image immediately after loading
            self.process_image()
    
    def update_image_label(self):
        # We'll just use scale_image now, since it will handle everything
        self.scale_image()
    
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