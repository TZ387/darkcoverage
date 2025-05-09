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

```
pip install darkcoverage
```

### From Source

1. Clone the repository:
   ```
   git clone https://github.com/TZ387/darkcoverage.git
   cd darkcoverage
   ```

2. Install the package:
   ```
   pip install -e .
   ```



## Usage

Run the application:

```
darkcoverage
```

Or from the source code:

```
py -m darkcoverage.main
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
├── darkcoverage/
│   ├── __init__.py
│   ├── main.py
│   ├── gui.py
│   ├── image_processing.py
│   └── widgets/
│       ├── __init__.py
│       ├── image_label.py
│       ├── reference_window.py
│       └── sliders_window.py
├── .gitignore
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

