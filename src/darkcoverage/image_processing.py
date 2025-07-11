import numpy as np
from PIL import Image


def process_image(original_image, threshold_values, grid_size, color_dark_parts=True):
    """
    Process an image by applying thresholds to grid cells and coloring parts above/below threshold.

    Args:
        original_image (PIL.Image): Grayscale image to process
        threshold_values (list): List of threshold values for each grid cell
        grid_size (tuple): Grid dimensions as (rows, columns)
        color_dark_parts (bool): If True, color parts below threshold; otherwise color parts above threshold

    Returns:
        tuple: (processed_image, colored_ratios, total_result)
            - processed_image: PIL Image with colored regions
            - colored_ratios: 2D array with percentage of colored pixels per cell
            - total_result: Overall percentage of colored pixels
    """
    n, m = grid_size
    width, height = original_image.size

    # Convert image to NumPy array for faster processing
    img_array = np.array(original_image)

    # Pre-allocate output array (more efficient than stacking)
    output_array = np.zeros((height, width, 3), dtype=np.uint8)

    # Copy grayscale values to all channels (avoid stack operation)
    output_array[:, :, 0] = output_array[:, :, 1] = output_array[:, :, 2] = img_array

    # Calculate cell dimensions
    base_sub_w = width // m
    base_sub_h = height // n
    rem_w = width % m
    rem_h = height % n

    # Pre-compute cell boundaries for efficiency
    x_bounds = []
    y_bounds = []

    x_pos = 0
    for j in range(m):
        cell_w = base_sub_w + (1 if j < rem_w else 0)
        x_bounds.append((x_pos, x_pos + cell_w))
        x_pos += cell_w

    y_pos = 0
    for i in range(n):
        cell_h = base_sub_h + (1 if i < rem_h else 0)
        y_bounds.append((y_pos, y_pos + cell_h))
        y_pos += cell_h

    # Process each cell with optimized array operations
    colored_ratios = np.zeros((n, m))
    total_colored_pixels = 0
    total_pixels = 0

    for i in range(n):
        for j in range(m):
            # Get cell boundaries
            start_y, end_y = y_bounds[i]
            start_x, end_x = x_bounds[j]

            # Extract sub-image region
            sub_img = img_array[start_y:end_y, start_x:end_x]
            cell_pixels = sub_img.size
            total_pixels += cell_pixels

            # Threshold value for this cell
            threshold = threshold_values[i * m + j]

            # Create mask based on color mode selection
            if color_dark_parts:
                mask = sub_img < threshold
            else:
                mask = sub_img >= threshold

            # Count colored pixels and calculate ratio
            colored_pixels = np.sum(mask)
            colored_ratios[i, j] = (colored_pixels / cell_pixels) * 100
            total_colored_pixels += colored_pixels

            # Apply coloring - red for colored parts
            # This operation is more efficient as it modifies the pre-allocated array
            output_region = output_array[start_y:end_y, start_x:end_x]
            output_region[mask, 0] = 255  # R
            output_region[mask, 1] = 0  # G
            output_region[mask, 2] = 0  # B

    # Calculate total result (more accurate than averaging the ratios)
    total_result = (total_colored_pixels / total_pixels) * 100

    # Convert back to PIL Image
    processed_img = Image.fromarray(output_array)

    return processed_img, colored_ratios, total_result
