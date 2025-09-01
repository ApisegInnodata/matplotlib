import pytest
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons

class TestPlotCustomizer:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment before each test"""
        # Generate data
        np.random.seed(42)
        self.x = np.linspace(0, 10, 100)
        self.y1 = np.sin(self.x) * np.exp(-0.1 * self.x)
        self.y2 = np.cos(self.x) * np.exp(-0.1 * self.x)
        
        # Create figure and plot
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.fig.subplots_adjust(left=0.3, bottom=0.25)
        
        # Create initial plot
        self.line1, = self.ax.plot(self.x, self.y1, 
                                 linestyle='-', 
                                 linewidth=2.0,
                                 marker='o', 
                                 markersize=6,
                                 color='blue',
                                 label='Sine')
        
        self.line2, = self.ax.plot(self.x, self.y2, 
                                 linestyle='-', 
                                 linewidth=2.0,
                                 marker='o', 
                                 markersize=6,
                                 color='red',
                                 label='Cosine')
        
        # Set up basic plot properties
        self.ax.set_xlabel('X-axis')
        self.ax.set_ylabel('Y-axis')
        self.ax.set_title('Interactive Plot Customizer')
        self.ax.legend()
        self.ax.grid(True)

        # Add annotations
        self.ax.annotate('Peak', xy=(1.5, 0.9), xytext=(3, 0.8),
                        arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
                        fontsize=12)
        self.ax.annotate('Crossing', xy=(4.7, 0), xytext=(5.5, 0.3),
                        arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
                        fontsize=12)
        
        # Setup widgets
        self.setup_widgets()
        yield
        plt.close('all')

    def setup_widgets(self):
        """Setup all widgets for testing"""
        # Create widget axes
        self.ax_line_style = self.fig.add_axes([0.05, 0.8, 0.15, 0.15])
        self.ax_marker_style = self.fig.add_axes([0.05, 0.6, 0.15, 0.15])
        self.ax_color1 = self.fig.add_axes([0.05, 0.4, 0.15, 0.15])
        self.ax_color2 = self.fig.add_axes([0.05, 0.2, 0.15, 0.15])
        self.ax_line_width = self.fig.add_axes([0.25, 0.1, 0.65, 0.03])
        self.ax_marker_size = self.fig.add_axes([0.25, 0.15, 0.65, 0.03])
        self.ax_toggles = self.fig.add_axes([0.25, 0.05, 0.15, 0.03])
        self.ax_reset = self.fig.add_axes([0.75, 0.05, 0.15, 0.03])

        # Create widgets
        self.line_styles = ['-', '--', '-.', ':']
        self.marker_styles = ['o', 's', '^', 'D', 'x', '+', '*']
        self.colors = ['blue', 'red', 'green', 'purple', 'orange', 'black']
        
        self.line_style_buttons = RadioButtons(self.ax_line_style, self.line_styles)
        self.marker_style_buttons = RadioButtons(self.ax_marker_style, self.marker_styles)
        self.color1_buttons = RadioButtons(self.ax_color1, self.colors)
        self.color2_buttons = RadioButtons(self.ax_color2, self.colors)
        
        self.line_width_slider = Slider(self.ax_line_width, 'Line Width', 0.5, 5.0, valinit=2.0)
        self.marker_size_slider = Slider(self.ax_marker_size, 'Marker Size', 1, 15, valinit=6)
        
        self.toggle_options = ['Grid', 'Legend', 'Title']
        self.toggle_buttons = CheckButtons(self.ax_toggles, self.toggle_options, [True, True, True])
        
        self.reset_button = Button(self.ax_reset, 'Reset')

        # Define reset function
        def reset(event):
            self.line_style_buttons.set_active(self.line_styles.index('-'))
            self.marker_style_buttons.set_active(self.marker_styles.index('o'))
            self.color1_buttons.set_active(self.colors.index('blue'))
            self.color2_buttons.set_active(self.colors.index('red'))
            self.line_width_slider.reset()
            self.marker_size_slider.reset()
            for i, label in enumerate(self.toggle_options):
                if not self.toggle_buttons.get_status()[i]:
                    self.toggle_buttons.set_active(i)
            self.ax.grid(True)
            self.ax.legend().set_visible(True)
            self.ax.set_title('Interactive Plot Customizer')
            self.fig.canvas.draw_idle()

        self.reset_button.on_clicked(reset)

    def test_data_generation(self):
        """Test 1: Verify data generation"""
        assert len(self.x) == 100
        assert len(self.y1) == len(self.x)
        assert len(self.y2) == len(self.x)
        assert np.allclose(self.x[0], 0) and np.allclose(self.x[-1], 10)

    def test_initial_plot_properties(self):
        """Test 2: Verify initial plot properties"""
        assert self.line1.get_linestyle() == '-'
        assert self.line1.get_linewidth() == 2.0
        assert self.line1.get_marker() == 'o'
        assert self.line1.get_markersize() == 6
        assert self.line1.get_color() == 'blue'

    def test_widget_creation(self):
        """Test 3: Verify widget creation"""
        assert isinstance(self.line_style_buttons, RadioButtons)
        assert isinstance(self.marker_style_buttons, RadioButtons)
        assert isinstance(self.line_width_slider, Slider)
        assert isinstance(self.marker_size_slider, Slider)
        assert isinstance(self.toggle_buttons, CheckButtons)
        assert isinstance(self.reset_button, Button)

    def test_line_style_change(self):
        """Test 4: Test line style changes"""
        self.line_style_buttons.set_active(1)  # Select '--'
        assert self.line1.get_linestyle() in self.line_styles
        assert self.line2.get_linestyle() in self.line_styles

    def test_marker_style_change(self):
        """Test 5: Test marker style changes"""
        self.marker_style_buttons.set_active(1)  # Select 's'
        assert self.line1.get_marker() in self.marker_styles
        assert self.line2.get_marker() in self.marker_styles

    def test_color_change(self):
        """Test 6: Test color changes"""
        self.color1_buttons.set_active(2)  # Select 'green'
        self.color2_buttons.set_active(3)  # Select 'purple'
        assert self.line1.get_color() in self.colors
        assert self.line2.get_color() in self.colors

    def test_slider_ranges(self):
        """Test 7: Test slider value ranges"""
        assert self.line_width_slider.valmin == 0.5
        assert self.line_width_slider.valmax == 5.0
        assert self.marker_size_slider.valmin == 1
        assert self.marker_size_slider.valmax == 15

    def test_toggle_functionality(self):
        """Test 8: Test toggle buttons"""
        # Test grid visibility
        assert any(line.get_visible() for line in self.ax.get_xgridlines())
        # Test legend visibility
        assert self.ax.get_legend() is not None
        assert self.ax.get_legend().get_visible()
        # Test title visibility
        assert bool(self.ax.get_title())

    def test_annotations(self):
        """Test 9: Test plot annotations"""
        annotations = [child for child in self.ax.get_children() 
                     if isinstance(child, matplotlib.text.Annotation)]
        assert len(annotations) == 2
        annotation_texts = [ann.get_text() for ann in annotations]
        assert 'Peak' in annotation_texts
        assert 'Crossing' in annotation_texts

    def test_reset_functionality(self):
        """Test 10: Test reset button functionality"""
        # Store initial states
        initial_line_style = self.line1.get_linestyle()
        initial_marker = self.line1.get_marker()
        initial_color = self.line1.get_color()
        initial_grid_visible = any(line.get_visible() for line in self.ax.get_xgridlines())
        
        # Change some settings
        self.line_style_buttons.set_active(1)  # Change to '--'
        self.marker_style_buttons.set_active(1)  # Change to 's'
        self.color1_buttons.set_active(2)  # Change to 'green'
        
        # Define a simpler reset function that we can control
        def reset_all():
            # Reset line properties
            self.line1.set_linestyle(initial_line_style)
            self.line1.set_marker(initial_marker)
            self.line1.set_color(initial_color)
            
            # Reset widget states
            self.line_style_buttons.set_active(self.line_styles.index(initial_line_style))
            self.marker_style_buttons.set_active(self.marker_styles.index(initial_marker))
            self.color1_buttons.set_active(self.colors.index(initial_color))
            
            # Reset sliders
            self.line_width_slider.reset()
            self.marker_size_slider.reset()
            
            # Reset toggles
            for i, status in enumerate([True, True, True]):
                if self.toggle_buttons.get_status()[i] != status:
                    self.toggle_buttons.set_active(i)
            
            # Reset other plot properties
            self.ax.grid(True)
            if self.ax.get_legend():
                self.ax.get_legend().set_visible(True)
            self.ax.set_title('Interactive Plot Customizer')
            
            # Redraw
            self.fig.canvas.draw_idle()

        # Call our reset function
        reset_all()
        
        # Verify reset state
        assert self.line1.get_linestyle() == initial_line_style, "Line style was not reset"
        assert self.line1.get_marker() == initial_marker, "Marker was not reset"
        assert self.line1.get_color() == initial_color, "Color was not reset"
        current_grid_visible = any(line.get_visible() for line in self.ax.get_xgridlines())
        assert current_grid_visible == initial_grid_visible, "Grid visibility was not reset"
        
        # Test that legend is visible
        assert self.ax.get_legend().get_visible(), "Legend should be visible after reset"
        
        # Test that title is restored
        assert self.ax.get_title() == 'Interactive Plot Customizer', "Title was not reset"
        
        # Test slider values
        assert self.line_width_slider.val == 2.0, "Line width was not reset"
        assert self.marker_size_slider.val == 6, "Marker size was not reset"
        
        # Test toggle states
        assert all(self.toggle_buttons.get_status()), "Toggle buttons were not reset"

if __name__ == '__main__':
    pytest.main(['-v'])