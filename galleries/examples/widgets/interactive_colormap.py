"""
=======================
Interactive Colormap Adjuster
=======================

This example demonstrates how to create an interactive tool for adjusting
colormap parameters in Matplotlib. It allows users to:

1. Select different colormaps from a dropdown menu
2. Adjust the colormap normalization (linear, log, symmetric log)
3. Modify colormap limits using sliders
4. Apply colormap to both 2D images and scatter plots

This type of interactive visualization is useful for exploring how different
colormaps and settings affect the perception of your data.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons
from matplotlib.colors import Normalize, LogNorm, SymLogNorm
from matplotlib.cm import ScalarMappable

# Generate some sample data
np.random.seed(42)

# Create a 2D Gaussian for the image data
x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = np.exp(-(X**2 + Y**2)/2)

# Add some noise and features to make it more interesting
Z = Z + np.random.randn(100, 100) * 0.1
Z[30:40, 30:40] = Z[30:40, 30:40] * 2  # Add a bright spot
Z[60:80, 60:80] = Z[60:80, 60:80] * 1.5  # Add another feature

# Create scatter data
n_points = 200
scatter_x = np.random.randn(n_points) * 2
scatter_y = np.random.randn(n_points) * 2
scatter_c = np.sqrt(scatter_x**2 + scatter_y**2)  # Distance from origin

# Create the figure and axes
fig = plt.figure(figsize=(12, 8))
fig.subplots_adjust(left=0.3, bottom=0.25)

# Create two subplots: one for the image, one for the scatter
ax_image = plt.subplot(121)
ax_scatter = plt.subplot(122)

# Initial colormap
initial_cmap = 'viridis'
available_cmaps = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 
                  'coolwarm', 'RdBu_r', 'jet', 'turbo', 'rainbow']

# Initial normalization
initial_norm = 'linear'
vmin_init, vmax_init = 0, 1

# Create the initial plots with default settings
img = ax_image.imshow(Z, cmap=initial_cmap, 
                     norm=Normalize(vmin=vmin_init, vmax=vmax_init))
ax_image.set_title('2D Image with Colormap')

scatter = ax_scatter.scatter(scatter_x, scatter_y, c=scatter_c, s=50, 
                           cmap=initial_cmap, 
                           norm=Normalize(vmin=vmin_init, vmax=vmax_init))
ax_scatter.set_title('Scatter Plot with Colormap')
ax_scatter.set_xlim(-4, 4)
ax_scatter.set_ylim(-4, 4)

# Add a colorbar that updates with both plots
cbar_ax = fig.add_axes([0.92, 0.25, 0.02, 0.5])
cbar = fig.colorbar(img, cax=cbar_ax)

# Create axes for the widgets
ax_cmap = fig.add_axes([0.05, 0.7, 0.15, 0.15])
ax_norm = fig.add_axes([0.05, 0.4, 0.15, 0.15])
ax_vmin = fig.add_axes([0.25, 0.1, 0.65, 0.03])
ax_vmax = fig.add_axes([0.25, 0.15, 0.65, 0.03])
ax_reset = fig.add_axes([0.05, 0.05, 0.15, 0.05])

# Create the widgets
cmap_buttons = RadioButtons(ax_cmap, available_cmaps, active=available_cmaps.index(initial_cmap))
norm_buttons = RadioButtons(ax_norm, ['linear', 'log', 'symlog'], active=0)

vmin_slider = Slider(
    ax=ax_vmin,
    label='Min Value',
    valmin=0,
    valmax=2,
    valinit=vmin_init,
)

vmax_slider = Slider(
    ax=ax_vmax,
    label='Max Value',
    valmin=0,
    valmax=2,
    valinit=vmax_init,
)

reset_button = Button(ax_reset, 'Reset', hovercolor='0.975')

# Add titles to the widget sections
ax_cmap.set_title('Colormap')
ax_norm.set_title('Normalization')

# Function to update the plots based on widget values
def update_plots():
    # Get current values from widgets
    cmap = cmap_buttons.value_selected
    norm_type = norm_buttons.value_selected
    vmin = vmin_slider.val
    vmax = vmax_slider.val
    
    # Create the appropriate normalization
    if norm_type == 'linear':
        norm = Normalize(vmin=vmin, vmax=vmax)
    elif norm_type == 'log':
        # Ensure vmin is positive for log scale
        vmin = max(vmin, 0.01)
        norm = LogNorm(vmin=vmin, vmax=vmax)
    elif norm_type == 'symlog':
        norm = SymLogNorm(linthresh=0.1, vmin=vmin, vmax=vmax)
    
    # Update the image
    img.set_cmap(cmap)
    img.set_norm(norm)
    
    # Update the scatter plot
    scatter.set_cmap(cmap)
    scatter.set_norm(norm)
    
    # Update the colorbar
    cbar.update_normal(ScalarMappable(norm=norm, cmap=plt.get_cmap(cmap)))
    
    # Redraw the figure
    fig.canvas.draw_idle()

# Connect the update function to the widgets
def update_cmap(label):
    update_plots()

def update_norm(label):
    # If switching to log, ensure vmin is positive
    if label == 'log' and vmin_slider.val <= 0:
        vmin_slider.set_val(0.01)
    update_plots()

def update_vmin(val):
    # Ensure vmin < vmax
    if val >= vmax_slider.val:
        vmax_slider.set_val(val + 0.1)
    # Ensure vmin is positive for log scale
    if norm_buttons.value_selected == 'log' and val <= 0:
        vmin_slider.set_val(0.01)
    update_plots()

def update_vmax(val):
    # Ensure vmax > vmin
    if val <= vmin_slider.val:
        vmin_slider.set_val(val - 0.1)
    update_plots()

def reset(event):
    vmin_slider.reset()
    vmax_slider.reset()
    cmap_buttons.set_active(available_cmaps.index(initial_cmap))
    norm_buttons.set_active(0)
    update_plots()

# Connect callbacks
cmap_buttons.on_clicked(update_cmap)
norm_buttons.on_clicked(update_norm)
vmin_slider.on_changed(update_vmin)
vmax_slider.on_changed(update_vmax)
reset_button.on_clicked(reset)

# Set the figure title
fig.suptitle('Interactive Colormap Adjuster', fontsize=16)

plt.show()

# %%
#
# .. admonition:: References
#
#    The use of the following functions, methods, classes and modules is shown
#    in this example:
#
#    - `matplotlib.figure.Figure`
#    - `matplotlib.axes.Axes.imshow`
#    - `matplotlib.axes.Axes.scatter`
#    - `matplotlib.widgets.Slider`
#    - `matplotlib.widgets.Button`
#    - `matplotlib.widgets.RadioButtons`
#    - `matplotlib.colors.Normalize`
#    - `matplotlib.colors.LogNorm`
#    - `matplotlib.colors.SymLogNorm`