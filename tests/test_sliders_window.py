import numpy as np
import pytest

from darkcoverage.widgets.sliders_window import SlidersWindow


@pytest.fixture
def sliders_window(qapp):
    return SlidersWindow()


def test_default_grid_creates_one_slider_and_label_per_cell(sliders_window):
    assert sliders_window.get_grid_size() == (3, 3)
    assert len(sliders_window.sliders) == 9
    assert len(sliders_window.ratio_labels) == 9
    assert all(slider.value() == 160 for slider in sliders_window.sliders)


def test_resizing_grid_rebuilds_sliders_and_labels_to_match(sliders_window):
    sliders_window.n_input.setValue(2)
    sliders_window.m_input.setValue(4)

    assert sliders_window.get_grid_size() == (2, 4)
    assert len(sliders_window.sliders) == 8
    assert len(sliders_window.ratio_labels) == 8


def test_slider_values_are_collected_in_row_major_order(sliders_window):
    sliders_window.n_input.setValue(2)
    sliders_window.m_input.setValue(3)

    for i, slider in enumerate(sliders_window.sliders):
        slider.setValue(i)

    received = []
    sliders_window.thresholds_changed.connect(received.append)
    sliders_window.on_slider_change()

    assert received == [[0, 1, 2, 3, 4, 5]]


def test_update_dark_ratios_maps_2d_ratios_to_labels_in_row_major_order(sliders_window):
    # A non-square grid so a transposed (row, col) mix-up would be caught.
    sliders_window.n_input.setValue(2)
    sliders_window.m_input.setValue(3)

    ratios = np.array([[10.0, 20.0, 30.0], [40.0, 50.0, 60.0]])
    sliders_window.update_dark_ratios(ratios)

    texts = [label.text() for label in sliders_window.ratio_labels]
    assert texts == [
        "Colored: 10.0%",
        "Colored: 20.0%",
        "Colored: 30.0%",
        "Colored: 40.0%",
        "Colored: 50.0%",
        "Colored: 60.0%",
    ]


def test_reset_ratios_clears_every_label_regardless_of_grid_shape(sliders_window):
    sliders_window.n_input.setValue(2)
    sliders_window.m_input.setValue(3)
    sliders_window.update_dark_ratios(
        np.array([[10.0, 20.0, 30.0], [40.0, 50.0, 60.0]])
    )

    sliders_window.reset_ratios()

    texts = [label.text() for label in sliders_window.ratio_labels]
    assert texts == ["Colored: 0.0%"] * 6


def test_ratio_labels_stay_correctly_mapped_after_a_grid_resize(sliders_window):
    # Populate at the default 3x3 grid first, then resize to a different,
    # non-square shape and confirm the mapping realigns rather than reusing
    # stale row/col math from the old grid.
    sliders_window.update_dark_ratios(np.zeros((3, 3)))

    sliders_window.n_input.setValue(4)
    sliders_window.m_input.setValue(2)

    ratios = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [7.0, 8.0]])
    sliders_window.update_dark_ratios(ratios)

    texts = [label.text() for label in sliders_window.ratio_labels]
    assert texts == [
        "Colored: 1.0%",
        "Colored: 2.0%",
        "Colored: 3.0%",
        "Colored: 4.0%",
        "Colored: 5.0%",
        "Colored: 6.0%",
        "Colored: 7.0%",
        "Colored: 8.0%",
    ]
