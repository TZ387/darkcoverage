import pytest
from PySide6.QtWidgets import QApplication


@pytest.fixture(scope="session")
def qapp():
    """A single headless QApplication shared by all tests that need one."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(["pytest", "-platform", "offscreen"])
    return app
