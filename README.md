## Note

The project is currently undergoing transition from pip-based build to uv-based build. Therefore, there may be problems with some installation instructions.

# DarkCoverage

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

## Installation

### With pip

Install from PyPI:

```bash
pip install darkcoverage
```

### With uv

First, install uv if you haven't already (see uv docs for more information)

Then install DarkCoverage:

```bash
uv add darkcoverage
```

Or install globally with uvx:

```bash
uvx darkcoverage
```

### From Source

#### With pip

1. Clone the repository:
   ```bash
   git clone https://github.com/TZ387/darkcoverage.git
   cd darkcoverage
   ```

2. Install the package:
   ```bash
   pip install -e .
   ```

#### With uv

1. Clone the repository:
   ```bash
   git clone https://github.com/TZ387/darkcoverage.git
   cd darkcoverage
   ```

2. Install dependencies and set up the project:
   ```bash
   uv sync
   ```

## Usage

### If installed with pip

Run the application:

```bash
darkcoverage
```

### If installed with uv

Run the application:

```bash
# If installed with uv add
uv run darkcoverage

# If installed with uvx
uvx darkcoverage
```

### From Source

#### With pip

```bash
python -m darkcoverage.main
```

#### With uv

```bash
uv run python -m darkcoverage.main
```

### Basic Workflow

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
├── .gitignore
├── uv.lock
├── LICENSE
├── pyproject.toml
├── README.md
├── Demonstration.png
└── Example.jpg
```

## Requirements

- Python 3.8+
- PySide6
- Pillow
- NumPy

## License

This project is licensed under the MIT License - see the LICENSE file for details.