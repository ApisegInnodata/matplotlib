import pytest
import numpy as np
import matplotlib

matplotlib.use('Agg')  # Use non-interactive backend for testing
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LogNorm, SymLogNorm
from matplotlib.widgets import Slider, Button, RadioButtons


@pytest.fixture(scope="module")
def test_data():
    """Generate test data similar to the original script"""
    np.random.seed(42)
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    # Create base Gaussian without random noise first
    Z = np.exp(-(X ** 2 + Y ** 2) / 2)
    # Add noise with smaller magnitude to keep values positive
    Z = Z + np.random.randn(100, 100) * 0.05
    # Ensure minimum value is positive for log scaling
    Z = Z - Z.min() + 0.01

    Z[30:40, 30:40] = Z[30:40, 30:40] * 2
    Z[60:80, 60:80] = Z[60:80, 60:80] * 1.5

    n_points = 200
    scatter_x = np.random.randn(n_points) * 2
    scatter_y = np.random.randn(n_points) * 2
    scatter_c = np.sqrt(scatter_x ** 2 + scatter_y ** 2)

    return Z, scatter_x, scatter_y, scatter_c


def test_data_dimensions(test_data):
    """Test 1: Verify dimensions of generated data"""
    Z, scatter_x, scatter_y, scatter_c = test_data
    assert Z.shape == (100, 100)
    assert len(scatter_x) == 200
    assert len(scatter_y) == 200
    assert len(scatter_c) == 200


def test_data_ranges(test_data):
    """Test 2: Verify data ranges are appropriate"""
    Z, _, _, scatter_c = test_data
    assert np.all(np.isfinite(Z))  # No infinities
    assert np.all(np.isfinite(scatter_c))
    assert Z.min() > 0  # Positive values for log scaling


def test_colormap_validity():
    """Test 3: Verify all specified colormaps exist"""
    available_cmaps = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']
    for cmap in available_cmaps:
        assert cmap in plt.colormaps()


def test_normalization_creation():
    """Test 4: Test creation of different normalizations"""
    vmin, vmax = 0.01, 1
    # Linear normalization
    norm_linear = Normalize(vmin=vmin, vmax=vmax)
    assert isinstance(norm_linear, Normalize)

    # Log normalization
    norm_log = LogNorm(vmin=vmin, vmax=vmax)
    assert isinstance(norm_log, LogNorm)

    # SymLog normalization
    norm_symlog = SymLogNorm(linthresh=0.1, vmin=vmin, vmax=vmax)
    assert isinstance(norm_symlog, SymLogNorm)


def test_gaussian_properties(test_data):
    """Test 5: Verify properties of the Gaussian image"""
    Z, _, _, _ = test_data
    # Check if the peak is at the center
    center_val = Z[50, 50]
    edges_val = np.mean([Z[0, 0], Z[0, -1], Z[-1, 0], Z[-1, -1]])
    assert center_val > edges_val  # Center should be higher than edges


def test_scatter_calculation(test_data):
    """Test 6: Verify scatter color calculation"""
    _, scatter_x, scatter_y, scatter_c = test_data
    # Verify scatter_c is correctly calculated as distance from origin
    expected_c = np.sqrt(scatter_x ** 2 + scatter_y ** 2)
    np.testing.assert_array_almost_equal(scatter_c, expected_c)


def test_figure_creation():
    """Test 7: Test figure creation and properties"""
    fig = plt.figure(figsize=(12, 8))
    assert fig.get_size_inches().tolist() == [12, 8]
    plt.close(fig)


def test_slider_ranges():
    """Test 8: Test slider value ranges"""
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.03])
    slider = Slider(ax=ax, label='Test', valmin=0, valmax=2, valinit=0)
    assert slider.valmin == 0
    assert slider.valmax == 2
    assert slider.val == 0
    plt.close(fig)


def test_button_creation():
    """Test 9: Test radio button creation"""
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.1, 0.1])
    options = ['linear', 'log', 'symlog']
    radio = RadioButtons(ax, options)
    # Test the values of the radio buttons instead of the label objects
    assert [label.get_text() for label in radio.labels] == options
    plt.close(fig)


def test_enhanced_features(test_data):
    """Test 10: Test enhanced features in the data"""
    Z, _, _, _ = test_data
    # Test bright spot (2x enhancement)
    bright_spot_val = np.mean(Z[30:40, 30:40])
    normal_val = np.mean(Z[0:10, 0:10])
    assert bright_spot_val > normal_val * 1.5  # Should be notably brighter


if __name__ == '__main__':
    pytest.main(['-v'])