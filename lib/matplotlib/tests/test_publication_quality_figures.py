import pytest
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.testing.decorators import check_figures_equal
from matplotlib.testing.conftest import mpl_test_settings


class TestPublicationFigures:
    @pytest.fixture
    def setup_data(self):
        """Fixture to set up common test data"""
        np.random.seed(42)
        x = np.linspace(0, 10, 100)
        y = np.sin(x) * np.exp(-0.1 * x)
        return x, y

    def test_figure_dimensions(self, setup_data):
        """Test 1: Verify figure dimensions are set correctly"""
        x, y = setup_data
        fig = plt.figure(figsize=(7, 5))
        plt.plot(x, y)
        assert fig.get_size_inches().tolist() == [7.0, 5.0]
        plt.close()

    def test_font_settings(self):
        """Test 2: Verify font settings are applied correctly"""
        plt.rcParams.update({
            'font.family': 'sans-serif',
            'font.size': 12
        })
        assert plt.rcParams['font.family'] == ['sans-serif']
        assert plt.rcParams['font.size'] == 12

    @check_figures_equal(extensions=['png'])
    def test_colorblind_friendly_colors(self, fig_test, fig_ref):
        """Test 3: Verify colorblind-friendly colors are used correctly"""
        colors = ['#0072B2', '#D55E00', '#009E73']

        # Test figure
        ax_test = fig_test.add_subplot(111)
        for i, color in enumerate(colors):
            ax_test.plot([0, 1], [i, i], color=color)

        # Reference figure
        ax_ref = fig_ref.add_subplot(111)
        for i, color in enumerate(colors):
            ax_ref.plot([0, 1], [i, i], color=color)

    def test_error_bars(self, setup_data):
        """Test 4: Verify error bar functionality"""
        x, y = setup_data
        y_err = 0.1 * np.random.rand(len(x))
        fig, ax = plt.subplots()
        ax.errorbar(x, y, yerr=y_err, capsize=3)
        assert len(ax.lines) > 0  # Verify error bars were created
        plt.close()

    def test_multi_panel_layout(self):
        """Test 5: Test multi-panel figure layout"""
        fig, axes = plt.subplots(2, 2, figsize=(10, 8))
        assert axes.shape == (2, 2)
        assert fig.get_size_inches().tolist() == [10.0, 8.0]
        plt.close()

    @pytest.mark.parametrize("style_param", [
        ("axes.titlesize", 16),
        ("axes.labelsize", 14),
        ("xtick.labelsize", 12),
        ("ytick.labelsize", 12)
    ])
    def test_style_parameters(self, style_param):
        """Test 6: Verify style parameters are set correctly"""
        param, value = style_param
        plt.rcParams[param] = value
        assert plt.rcParams[param] == value

    def test_annotations(self, setup_data):
        """Test 7: Test annotation functionality"""
        x, y = setup_data
        fig, ax = plt.subplots()
        ax.plot(x, y)
        annotation = ax.annotate('Test', xy=(0, 0), xytext=(1, 1))
        assert annotation.get_text() == 'Test'
        plt.close()

    def test_legend_properties(self, setup_data):
        """Test 8: Test legend properties"""
        x, y = setup_data
        fig, ax = plt.subplots()
        line, = ax.plot(x, y, label='Test Label')
        legend = ax.legend()
        assert legend.get_texts()[0].get_text() == 'Test Label'
        plt.close()

    def test_grid_properties(self):
        """Test 9: Test grid properties"""
        fig, ax = plt.subplots()
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Check if grid lines exist
        x_gridlines = ax.xaxis.get_gridlines()
        y_gridlines = ax.yaxis.get_gridlines()
        
        # Verify grid properties
        assert len(x_gridlines) > 0
        assert len(y_gridlines) > 0
        assert x_gridlines[0].get_linestyle() == '--'
        assert y_gridlines[0].get_alpha() == 0.7
        plt.close()

    @pytest.mark.parametrize("format_type", ['png', 'pdf'])
    def test_save_figure(self, setup_data, tmp_path, format_type):
        """Test 10: Test figure saving functionality"""
        x, y = setup_data
        fig, ax = plt.subplots()
        ax.plot(x, y)

        output_path = tmp_path / f"test_figure.{format_type}"
        fig.savefig(output_path, dpi=300 if format_type == 'png' else None)
        assert output_path.exists()
        plt.close()


class TestPublicationFiguresIntegration:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup and teardown for each test"""
        self.original_params = dict(plt.rcParams)
        yield
        plt.rcParams.update(self.original_params)
        plt.close('all')

    def test_complete_figure_workflow(self):
        """Integration test for complete figure creation workflow"""
        # 1. Set up style parameters
        plt.style.use('default')
        plt.rcParams.update({
            'font.family': 'sans-serif',
            'font.size': 12,
            'axes.titlesize': 16
        })

        # 2. Create multi-panel figure
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 8))

        # 3. Generate test data
        x = np.linspace(0, 10, 100)
        y1 = np.sin(x) * np.exp(-0.1 * x)
        y2 = np.cos(x) * np.exp(-0.1 * x)
        y_err = 0.1 * np.random.rand(len(x))

        # 4. Create different types of plots
        # Panel 1: Basic line plot
        ax1.plot(x, y1, color='#0072B2', linewidth=1.5)
        ax1.set_title('Panel A')
        ax1.grid(True, linestyle='--', alpha=0.7)

        # Panel 2: Error bar plot
        ax2.errorbar(x[::5], y2[::5], yerr=y_err[::5],
                     fmt='o', capsize=3, color='#D55E00')
        ax2.set_title('Panel B')

        # Panel 3: Filled plot
        ax3.fill_between(x, y1, alpha=0.3, color='#009E73')
        ax3.set_title('Panel C')

        # Panel 4: Scatter plot with annotation
        scatter = ax4.scatter(x[::3], y2[::3], c='#CC79A7')
        ax4.annotate('Peak', xy=(2, y2[20]), xytext=(3, 0.8),
                     arrowprops=dict(facecolor='black', shrink=0.05))
        ax4.set_title('Panel D')

        # 5. Adjust layout
        plt.tight_layout()

        # Verify various aspects of the figure
        assert fig.get_size_inches().tolist() == [10.0, 8.0]
        assert len(fig.axes) == 4
        assert isinstance(ax4.collections[0], mpl.collections.PathCollection)

        # Modified verification section:
        assert fig.get_size_inches().tolist() == [10.0, 8.0]
        assert len(fig.axes) == 4
        
        # Verify grid on ax1
        x_gridlines = ax1.xaxis.get_gridlines()
        y_gridlines = ax1.yaxis.get_gridlines()
        assert len(x_gridlines) > 0
        assert len(y_gridlines) > 0
        assert x_gridlines[0].get_linestyle() == '--'
        assert x_gridlines[0].get_alpha() == 0.7
        
        # Rest of the test remains the same...
        plt.close()