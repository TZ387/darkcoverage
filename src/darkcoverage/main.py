import sys
from PySide6.QtWidgets import QApplication
from .gui import ImageThresholdApp

def main():
    """Main entry point for the DarkCoverage application."""
    app = QApplication(sys.argv)
    window = ImageThresholdApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()