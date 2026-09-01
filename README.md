# DarkCoverage

[![Tests](https://github.com/TZ387/darkcoverage/actions/workflows/tests.yml/badge.svg)](https://github.com/TZ387/darkcoverage/actions/workflows/tests.yml)
[![PyPI version](https://img.shields.io/pypi/v/darkcoverage.svg)](https://pypi.org/project/darkcoverage/)

DarkCoverage is an image analysis tool that helps you measure and visualize the coverage of dark or light areas in images using customizable thresholds and a grid-based approach.

Its usage is simple: Just run the program, load the image, and then use the sliders to specify appropriate threshold for each area.

![DarkCoverage Screenshot](https://github.com/TZ387/darkcoverage/raw/main/Demonstration.png)

## Features

- Load and analyze images with customizable number of rows and columns
- Set individual thresholds for each grid cell
- Color dark or light areas based on threshold values
- View real-time coverage percentage for each cell and overall image
- Compare with original image reference
- Save processed images

## Installation and Usage

### With pip

**Installation:**
```bash
pip install darkcoverage
```

**Usage:**
```bash
darkcoverage
```
or if the `darkcoverage` script isn't on your PATH
```bash
python -m darkcoverage.main
```

### With uv

First, install uv if you haven't already (see uv docs for more information)

**Installation:**
```bash
uv add darkcoverage
```

**Usage:**
```bash
uv run darkcoverage
```

**Or run it without installing:**
```bash
uvx darkcoverage
```

### From Source

#### With pip

**Installation:**
1. Clone the repository:
   ```bash
   git clone https://github.com/TZ387/darkcoverage.git
   cd darkcoverage
   ```

2. Install the package:
   ```bash
   pip install -e .
   ```

**Usage:**
```bash
python -m darkcoverage.main
```

#### With uv

**Installation:**
1. Clone the repository:
   ```bash
   git clone https://github.com/TZ387/darkcoverage.git
   cd darkcoverage
   ```

2. Install dependencies and set up the project:
   ```bash
   uv sync
   ```

**Usage:**
```bash
uv run python -m darkcoverage.main
```

**Running tests:**
```bash
uv run pytest
```

## Basic Workflow

1. Click "Load Image" to open an image file (such as Example.jpg in the main folder).
2. Adjust the number of rows and columns using the row and column inputs in the sliders window
3. Set threshold values for each cell using the sliders
4. Toggle between "Color Dark Parts" and "Color Light Parts" to choose which areas to highlight
5. View the coverage percentages for each cell and the total image
6. Save the processed image with "Save Image"

In case something goes wrong, you can use reset image option.

## Project Structure

```
DarkCoverage/
├── .github/
│   └── workflows/
│       └── tests.yml
├── src/
│   └── darkcoverage/
│       ├── __init__.py
│       ├── main.py
│       ├── gui.py
│       ├── image_processing.py
│       └── widgets/
│           ├── __init__.py
│           ├── image_label.py
│           ├── reference_window.py
│           └── sliders_window.py
├── tests/
│   ├── conftest.py
│   ├── test_image_processing.py
│   └── test_sliders_window.py
├── .gitignore
├── AGENTS.md
├── CLAUDE.md -> AGENTS.md
├── uv.lock
├── LICENSE
├── pyproject.toml
├── README.md
├── Demonstration.png
└── Example.jpg
```

## Requirements

- Python 3.10+
- PySide6
- Pillow
- NumPy

## License

This project is licensed under the MIT License - see the LICENSE file for details.