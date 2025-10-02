"""
=======================
Interactive Plot Customizer
=======================

This example demonstrates how to create an interactive tool for customizing
plot appearance in Matplotlib. It allows users to:

1. Adjust line properties (color, style, width)
2. Modify marker properties (style, size, color)
3. Change axis properties (limits, grid, labels)
4. Toggle plot elements (legend, title, annotations)

This type of interactive visualization is useful for exploring different
visual representations of your data and for creating publication-ready figures.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons
import matplotlib
import os

# Use a non-interactive backend for testing environments
if os.environ.get("TEST_MODE") == "1":
    matplotlib.use("Agg")  # non-interactive backend
# Generate some sample data
np.random.seed(42)
x = np.linspace(0, 10, 100)
y1 = np.sin(x) * np.exp(-0.1 * x)
y2 = np.cos(x) * np.exp(-0.1 * x)

# Create the figure and axis
fig, ax = plt.subplots(figsize=(10, 8))
fig.subplots_adjust(left=0.3, bottom=0.25)

# Initial plot settings
initial_line_style = '-'
initial_line_width = 2.0
initial_marker_style = 'o'
initial_marker_size = 6
initial_color1 = 'blue'
initial_color2 = 'red'

# Create the initial plot
line1, = ax.plot(x, y1, 
                linestyle=initial_line_style, 
                linewidth=initial_line_width,
                marker=initial_marker_style, 
                markersize=initial_marker_size,
                color=initial_color1,
                label='Sine')

line2, = ax.plot(x, y2, 
                linestyle=initial_line_style, 
                linewidth=initial_line_width,
                marker=initial_marker_style, 
                markersize=initial_marker_size,
                color=initial_color2,
                label='Cosine')

# Set up the axis labels and title
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_title('Interactive Plot Customizer')
ax.legend()
ax.grid(True)

# Create axes for the widgets
ax_line_style = fig.add_axes([0.05, 0.8, 0.15, 0.15])
ax_marker_style = fig.add_axes([0.05, 0.6, 0.15, 0.15])
ax_color1 = fig.add_axes([0.05, 0.4, 0.15, 0.15])
ax_color2 = fig.add_axes([0.05, 0.2, 0.15, 0.15])
ax_line_width = fig.add_axes([0.25, 0.1, 0.65, 0.03])
ax_marker_size = fig.add_axes([0.25, 0.15, 0.65, 0.03])
ax_toggles = fig.add_axes([0.25, 0.05, 0.15, 0.03])
ax_reset = fig.add_axes([0.75, 0.05, 0.15, 0.03])

# Create the widgets
line_styles = ['-', '--', '-.', ':']
line_style_buttons = RadioButtons(ax_line_style, line_styles, active=line_styles.index(initial_line_style))

marker_styles = ['o', 's', '^', 'D', 'x', '+', '*']
marker_style_buttons = RadioButtons(ax_marker_style, marker_styles, active=marker_styles.index(initial_marker_style))

colors = ['blue', 'red', 'green', 'purple', 'orange', 'black']
color1_buttons = RadioButtons(ax_color1, colors, active=colors.index(initial_color1))
color2_buttons = RadioButtons(ax_color2, colors, active=colors.index(initial_color2))

line_width_slider = Slider(
    ax=ax_line_width,
    label='Line Width',
    valmin=0.5,
    valmax=5.0,
    valinit=initial_line_width,
)

marker_size_slider = Slider(
    ax=ax_marker_size,
    label='Marker Size',
    valmin=1,
    valmax=15,
    valinit=initial_marker_size,
)

toggle_options = ['Grid', 'Legend', 'Title']
toggle_buttons = CheckButtons(ax_toggles, toggle_options, [True, True, True])

reset_button = Button(ax_reset, 'Reset', hovercolor='0.975')

# Add titles to the widget sections
ax_line_style.set_title('Line Style')
ax_marker_style.set_title('Marker Style')
ax_color1.set_title('Line 1 Color')
ax_color2.set_title('Line 2 Color')

# Function to update the plot based on widget values
def update_plot():
    # Get current values from widgets
    line_style = line_style_buttons.value_selected
    marker_style = marker_style_buttons.value_selected
    color1 = color1_buttons.value_selected
    color2 = color2_buttons.value_selected
    line_width = line_width_slider.val
    marker_size = marker_size_slider.val
    
    # Update line 1
    line1.set_linestyle(line_style)
    line1.set_linewidth(line_width)
    line1.set_marker(marker_style)
    line1.set_markersize(marker_size)
    line1.set_color(color1)
    
    # Update line 2
    line2.set_linestyle(line_style)
    line2.set_linewidth(line_width)
    line2.set_marker(marker_style)
    line2.set_markersize(marker_size)
    line2.set_color(color2)
    
    # Redraw the figure
    fig.canvas.draw_idle()

# Function to toggle plot elements
def toggle_plot_elements(label):
    if label == 'Grid':
        ax.grid(not ax.get_xgridlines()[0].get_visible())
    elif label == 'Legend':
        legend = ax.get_legend()
        if legend:
            legend.set_visible(not legend.get_visible())
        else:
            ax.legend()
    elif label == 'Title':
        title = ax.get_title()
        if title:
            ax.set_title('')
        else:
            ax.set_title('Interactive Plot Customizer')
    
    fig.canvas.draw_idle()

# Function to reset all settings
def reset(event):
    line_style_buttons.set_active(line_styles.index(initial_line_style))
    marker_style_buttons.set_active(marker_styles.index(initial_marker_style))
    color1_buttons.set_active(colors.index(initial_color1))
    color2_buttons.set_active(colors.index(initial_color2))
    line_width_slider.reset()
    marker_size_slider.reset()
    
    # Reset toggles
    for i, label in enumerate(toggle_options):
        if toggle_buttons.get_status()[i] != True:
            toggle_buttons.set_active(i)
    
    # Reset axis properties
    ax.grid(True)
    ax.legend().set_visible(True)
    ax.set_title('Interactive Plot Customizer')
    
    update_plot()

# Connect callbacks
line_style_buttons.on_clicked(lambda label: update_plot())
marker_style_buttons.on_clicked(lambda label: update_plot())
color1_buttons.on_clicked(lambda label: update_plot())
color2_buttons.on_clicked(lambda label: update_plot())
line_width_slider.on_changed(lambda val: update_plot())
marker_size_slider.on_changed(lambda val: update_plot())
toggle_buttons.on_clicked(toggle_plot_elements)
reset_button.on_clicked(reset)

# Add annotations to explain the plot
ax.annotate('Peak', xy=(1.5, 0.9), xytext=(3, 0.8),
           arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
           fontsize=12)

ax.annotate('Crossing', xy=(4.7, 0), xytext=(5.5, 0.3),
           arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
           fontsize=12)

if os.environ.get("TEST_MODE") == "1":
    fig.savefig("test_output.png")
else:
    plt.show()


# %%
#
# .. admonition:: References
#
#    The use of the following functions, methods, classes and modules is shown
#    in this example:
#
#    - `matplotlib.figure.Figure`
#    - `matplotlib.axes.Axes.plot`
#    - `matplotlib.axes.Axes.annotate`
#    - `matplotlib.widgets.Slider`
#    - `matplotlib.widgets.Button`
#    - `matplotlib.widgets.RadioButtons`
#    - `matplotlib.widgets.CheckButtons`
