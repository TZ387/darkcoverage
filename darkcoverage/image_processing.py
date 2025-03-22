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
    
    # Calculate cell dimensions including remainders
    base_sub_w = width // m
    base_sub_h = height // n
    
    # Calculate remainders
    rem_w = width % m
    rem_h = height % n
    
    # Convert image to NumPy array for faster processing
    img_array = np.array(original_image)
    
    # Create output array as a color image
    output_array = np.stack([img_array]*3, axis=-1)
    
    # Pre-compute masks and ratios more efficiently
    colored_ratios = np.zeros((n, m))
    
    for i in range(n):
        for j in range(m):
            # Calculate actual cell dimensions including remainder distribution
            sub_w = base_sub_w + (1 if j < rem_w else 0)
            sub_h = base_sub_h + (1 if i < rem_h else 0)
            
            # Calculate start positions
            start_x = sum(base_sub_w + (1 if k < rem_w else 0) for k in range(j))
            start_y = sum(base_sub_h + (1 if k < rem_h else 0) for k in range(i))
            
            # Extract sub-image region
            sub_img = img_array[start_y:start_y+sub_h, start_x:start_x+sub_w]
            
            # Determine mask based on color mode selection
            if color_dark_parts:
                # Color dark parts - pixels BELOW threshold
                mask = sub_img < threshold_values[i * m + j]
            else:
                # Color light parts - pixels ABOVE or EQUAL to threshold
                mask = sub_img >= threshold_values[i * m + j]
            
            # Calculate colored ratio
            colored_ratios[i, j] = np.mean(mask) * 100
            
            # Mark pixels to be colored in red
            output_array[start_y:start_y+sub_h, start_x:start_x+sub_w][mask] = [255, 0, 0]
    
    # Calculate total result
    total_result = np.mean(colored_ratios)
    
    # Convert back to PIL Image
    processed_img = Image.fromarray(output_array)
    
    return processed_img, colored_ratios, total_result