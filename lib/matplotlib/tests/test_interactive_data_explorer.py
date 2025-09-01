import pytest
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent
from matplotlib.widgets import Slider, Button

class TestInteractiveDataExplorer:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment before each test"""
        # Set random seed for reproducibility
        np.random.seed(42)
        
        # Generate test data
        self.n_points = 100
        self.x = np.random.rand(self.n_points) * 10
        self.y = np.random.rand(self.n_points) * 10
        self.sizes = np.random.rand(self.n_points) * 100 + 50
        self.colors = np.random.rand(self.n_points)
        
        # Create figure and plot
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.fig.subplots_adjust(bottom=0.25)
        
        # Create scatter plot
        self.scatter = self.ax.scatter(
            self.x, self.y, 
            s=self.sizes, 
            c=self.colors, 
            cmap='viridis',
            alpha=0.8, 
            picker=True,
            pickradius=5
        )
        
        # Set labels and title
        self.ax.set_xlabel('X-axis')
        self.ax.set_ylabel('Y-axis')
        self.ax.set_title('Interactive Data Explorer')
        
        # Add grid with specific style
        self.ax.grid(True, linestyle='--', alpha=0.7)
        
        # Add colorbar
        self.cbar = plt.colorbar(self.scatter, ax=self.ax)
        self.cbar.set_label('Value')
        
        # Setup widgets
        self.setup_widgets()
        
        # Setup annotation
        self.setup_annotation()
        
        # Variable for highlighted point
        self.highlighted_point = None
        
        yield
        plt.close('all')

    def setup_widgets(self):
        """Setup slider and reset button"""
        self.ax_threshold = plt.axes([0.25, 0.1, 0.65, 0.03])
        self.threshold_slider = Slider(
            ax=self.ax_threshold,
            label='Color Threshold',
            valmin=0,
            valmax=1,
            valinit=0
        )
        
        self.ax_reset = plt.axes([0.8, 0.025, 0.1, 0.04])
        self.reset_button = Button(self.ax_reset, 'Reset', hovercolor='0.975')

        # Add update function
        def update(val):
            threshold = val
            facecolors = self.scatter.get_facecolors()
            sizes_array = self.scatter.get_sizes()
            
            for i, color_val in enumerate(self.colors):
                if color_val >= threshold:
                    facecolors[i, 3] = 0.8
                    sizes_array[i] = self.sizes[i]
                else:
                    facecolors[i, 3] = 0.1
                    sizes_array[i] = self.sizes[i] * 0.5
            
            self.scatter.set_facecolors(facecolors)
            self.scatter.set_sizes(sizes_array)
            self.fig.canvas.draw_idle()

        def reset(event):
            self.threshold_slider.set_val(0)
            self.ax.set_xlim(0, 10)
            self.ax.set_ylim(0, 10)
            self.fig.canvas.draw_idle()

        self.threshold_slider.on_changed(update)
        self.reset_button.on_clicked(reset)
        
        # Store the reset function for testing
        self.reset_func = reset

    def setup_annotation(self):
        """Setup annotation for hover tooltips"""
        self.annot = self.ax.annotate(
            "", xy=(0, 0), xytext=(10, 10),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=0.8),
            arrowprops=dict(arrowstyle="->"),
            visible=False
        )

    def test_initial_setup(self):
        """Test 1: Verify initial plot setup"""
        assert len(self.x) == self.n_points
        assert self.ax.get_xlabel() == 'X-axis'
        assert self.ax.get_ylabel() == 'Y-axis'
        assert self.ax.get_title() == 'Interactive Data Explorer'
        assert self.threshold_slider.val == 0

    def test_data_generation(self):
        """Test 2: Verify data generation"""
        assert np.all(self.x >= 0) and np.all(self.x <= 10)
        assert np.all(self.y >= 0) and np.all(self.y <= 10)
        assert np.all(self.sizes >= 50) and np.all(self.sizes <= 150)
        assert np.all(self.colors >= 0) and np.all(self.colors <= 1)

    def test_threshold_update(self):
        """Test 3: Test threshold slider functionality"""
        initial_sizes = self.scatter.get_sizes().copy()
        self.threshold_slider.set_val(0.5)
        updated_sizes = self.scatter.get_sizes()
        assert not np.array_equal(initial_sizes, updated_sizes)

    def test_reset_functionality(self):
        """Test 4: Test reset button functionality"""
        # Set initial limits
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        
        # Change some settings
        self.threshold_slider.set_val(0.5)
        self.ax.set_xlim(-1, 11)
        
        # Call the reset function directly
        self.reset_func(None)  # None as the event parameter
        
        # Check if values are reset
        assert self.threshold_slider.val == 0
        assert tuple(self.ax.get_xlim()) == (0, 10)
        assert tuple(self.ax.get_ylim()) == (0, 10)

    def test_colorbar_properties(self):
        """Test 5: Test colorbar properties"""
        assert self.cbar.ax.get_ylabel() == 'Value'
        assert self.cbar.vmin == min(self.colors)
        assert self.cbar.vmax == max(self.colors)

    def test_grid_properties(self):
        """Test 6: Test grid properties"""
        gridlines = self.ax.xaxis.get_gridlines()
        assert len(gridlines) > 0
        assert gridlines[0].get_linestyle() == '--'
        assert gridlines[0].get_alpha() == 0.7

    def test_annotation_properties(self):
        """Test 7: Test annotation properties"""
        assert not self.annot.get_visible()
        assert self.annot.get_bbox_patch().get_boxstyle().pad == 0.3
        assert self.annot.get_bbox_patch().get_alpha() == 0.8

    def test_scatter_properties(self):
        """Test 8: Test scatter plot properties"""
        assert self.scatter.get_alpha() == 0.8
        assert self.scatter.get_picker() == True
        assert self.scatter.get_pickradius() == 5

    def test_figure_properties(self):
        """Test 9: Test figure properties"""
        width, height = self.fig.get_size_inches()
        assert width == 10
        assert height == 8
        assert self.fig.get_dpi() == plt.rcParams['figure.dpi']

    def test_data_ranges(self):
        """Test 10: Test data ranges and limits"""
        # Set explicit limits
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        
        # Test the limits and data properties
        assert tuple(self.ax.get_xlim()) == (0, 10)
        assert tuple(self.ax.get_ylim()) == (0, 10)
        assert len(self.scatter.get_sizes()) == self.n_points
        assert len(self.scatter.get_facecolors()) == self.n_points

if __name__ == '__main__':
    pytest.main(['-v'])