import numpy as np
import pytest
from PIL import Image

from darkcoverage.image_processing import process_image


def make_gray_image(rows):
    """Build a grayscale PIL image from a 2D list/array of pixel values."""
    return Image.fromarray(np.array(rows, dtype=np.uint8), mode="L")


def test_dark_mode_colors_pixels_below_threshold():
    # 2x2 image, single cell, threshold 100 -> only the two pixels < 100 are colored
    image = make_gray_image([[50, 150], [90, 200]])

    processed, colored_ratios, total_result = process_image(
        image, threshold_values=[100], grid_size=(1, 1), color_dark_parts=True
    )

    assert colored_ratios[0, 0] == pytest.approx(50.0)  # 2 of 4 pixels
    assert total_result == pytest.approx(50.0)

    pixels = np.array(processed)
    assert list(pixels[0, 0]) == [255, 0, 0]  # 50 < 100 -> colored red
    assert list(pixels[0, 1]) == [150, 150, 150]  # 150 >= 100 -> untouched grayscale
    assert list(pixels[1, 0]) == [255, 0, 0]  # 90 < 100 -> colored red
    assert list(pixels[1, 1]) == [200, 200, 200]  # 200 >= 100 -> untouched grayscale


def test_light_mode_colors_pixels_at_or_above_threshold():
    image = make_gray_image([[50, 150], [90, 200]])

    processed, colored_ratios, total_result = process_image(
        image, threshold_values=[100], grid_size=(1, 1), color_dark_parts=False
    )

    assert colored_ratios[0, 0] == pytest.approx(50.0)  # 2 of 4 pixels
    assert total_result == pytest.approx(50.0)

    pixels = np.array(processed)
    assert list(pixels[0, 0]) == [50, 50, 50]  # 50 < 100 -> untouched grayscale
    assert list(pixels[0, 1]) == [255, 0, 0]  # 150 >= 100 -> colored red
    assert list(pixels[1, 0]) == [90, 90, 90]  # 90 < 100 -> untouched grayscale
    assert list(pixels[1, 1]) == [255, 0, 0]  # 200 >= 100 -> colored red


def test_dark_and_light_modes_are_complementary_per_cell():
    image = make_gray_image([[10, 20, 30], [200, 210, 220], [5, 250, 128]])

    _, dark_ratios, _ = process_image(
        image, threshold_values=[128] * 9, grid_size=(3, 3), color_dark_parts=True
    )
    _, light_ratios, _ = process_image(
        image, threshold_values=[128] * 9, grid_size=(3, 3), color_dark_parts=False
    )

    # Every pixel falls into exactly one of the two categories.
    assert dark_ratios + light_ratios == pytest.approx(np.full((3, 3), 100.0))


def test_each_cell_uses_its_own_threshold():
    # 1 row, 2 columns; left cell all 100s, right cell all 100s, but different thresholds
    image = make_gray_image([[100, 100, 100, 100]])

    _, colored_ratios, _ = process_image(
        image, threshold_values=[150, 50], grid_size=(1, 2), color_dark_parts=True
    )

    assert colored_ratios[0, 0] == pytest.approx(100.0)  # 100 < 150 -> all colored
    assert colored_ratios[0, 1] == pytest.approx(0.0)  # 100 >= 50 -> none colored


def test_uneven_grid_dimensions_cover_every_pixel_exactly_once():
    # 5x5 image split into a 2x2 grid: dimensions aren't evenly divisible,
    # so some cells must absorb the remainder rows/columns.
    rows = [[(r * 5 + c) for c in range(5)] for r in range(5)]
    image = make_gray_image(rows)

    _, colored_ratios, total_result = process_image(
        image, threshold_values=[128] * 4, grid_size=(2, 2), color_dark_parts=True
    )

    manual_colored = np.sum(np.array(rows) < 128)
    assert total_result == pytest.approx((manual_colored / 25) * 100)

    # Cell sizes from the remainder-distribution logic: 5 // 2 = 2 with
    # remainder 1, so the first row/column of cells absorbs the extra pixel.
    # Height: 3, 2. Width: 3, 2.
    cell_pixel_counts = np.array([[3 * 3, 3 * 2], [2 * 3, 2 * 2]])
    assert cell_pixel_counts.sum() == 25  # every pixel accounted for exactly once

    # Reconstructing total colored pixels from each cell's own ratio and size
    # must match the manual count — this fails if cells overlap or leave gaps.
    reconstructed_colored = np.sum(colored_ratios / 100 * cell_pixel_counts)
    assert reconstructed_colored == pytest.approx(manual_colored)


def test_output_image_has_same_size_and_is_rgb():
    image = make_gray_image([[0, 255], [255, 0]])

    processed, _, _ = process_image(
        image, threshold_values=[128], grid_size=(1, 1), color_dark_parts=True
    )

    assert processed.size == image.size
    assert processed.mode == "RGB"


def test_total_result_is_weighted_by_pixel_count_not_averaged_ratios():
    # 1x5 image split into 2 columns of uneven width (5 // 2 = 2, remainder 1
    # -> left cell absorbs the extra column and is 3px wide, right is 2px).
    image = make_gray_image([[0, 0, 0, 255, 255]])

    # Left cell (3px, all dark) is fully colored; right cell (2px, all light)
    # is not colored at all. A plain average of the two ratios would give
    # (100+0)/2 = 50%, but the true pixel-weighted total is 3/5 = 60%.
    _, colored_ratios, total_result = process_image(
        image, threshold_values=[128, 128], grid_size=(1, 2), color_dark_parts=True
    )

    assert colored_ratios[0, 0] == pytest.approx(100.0)
    assert colored_ratios[0, 1] == pytest.approx(0.0)
    assert total_result == pytest.approx(60.0)


def test_grid_larger_than_image_leaves_empty_cells_at_zero_not_nan():
    # 2x2 image with a 3x3 grid: the last grid row/column has no pixels to
    # cover, so those cells' 0/0 ratio must not surface as NaN.
    image = make_gray_image([[0, 0], [0, 0]])

    _, colored_ratios, total_result = process_image(
        image, threshold_values=[128] * 9, grid_size=(3, 3), color_dark_parts=True
    )

    assert not np.isnan(colored_ratios).any()
    assert colored_ratios[2, 2] == pytest.approx(0.0)  # empty cell
    assert colored_ratios[0, 0] == pytest.approx(100.0)  # the one real pixel cell
    assert total_result == pytest.approx(100.0)  # all 4 actual pixels are dark


def test_zero_size_image_leaves_total_result_at_zero_not_dividing_by_zero():
    # A 0x0 image has no pixels anywhere, so total_pixels is 0 too; that
    # must not raise ZeroDivisionError.
    image = Image.new("L", (0, 0))

    processed, colored_ratios, total_result = process_image(
        image, threshold_values=[128], grid_size=(1, 1), color_dark_parts=True
    )

    assert processed.size == (0, 0)
    assert colored_ratios[0, 0] == pytest.approx(0.0)
    assert total_result == pytest.approx(0.0)
