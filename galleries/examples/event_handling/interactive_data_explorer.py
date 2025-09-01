"""
=======================
Interactive Data Explorer
=======================

This example demonstrates how to create an interactive data exploration tool
with Matplotlib. It allows users to:

1. Zoom and pan to explore different regions of the data
2. Hover over points to see their values
3. Click on points to highlight them
4. Use a slider to filter data based on a threshold

This type of interactive visualization is useful for exploratory data analysis
and for presentations where you want to demonstrate data features dynamically.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button
import matplotlib.patheffects as path_effects

# Generate some sample data
np.random.seed(42)
n_points = 100
x = np.random.rand(n_points) * 10
y = np.random.rand(n_points) * 10
sizes = np.random.rand(n_points) * 100 + 50
colors = np.random.rand(n_points)

# Create the figure and axis
fig, ax = plt.subplots(figsize=(10, 8))
fig.subplots_adjust(bottom=0.25)  # Make room for the slider

# Create the scatter plot
scatter = ax.scatter(x, y, s=sizes, c=colors, cmap='viridis', 
                    alpha=0.8, picker=True, pickradius=5)

# Add a colorbar
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Value')

# Set up the axis labels and title
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_title('Interactive Data Explorer')

# Add grid for better readability
ax.grid(True, linestyle='--', alpha=0.7)

# Create annotation object for hover tooltips (initially empty)
annot = ax.annotate("", xy=(0, 0), xytext=(10, 10),
                   textcoords="offset points",
                   bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=0.8),
                   arrowprops=dict(arrowstyle="->"),
                   visible=False)

# Add a slider for filtering points based on their color value
ax_threshold = plt.axes([0.25, 0.1, 0.65, 0.03])
threshold_slider = Slider(
    ax=ax_threshold,
    label='Color Threshold',
    valmin=0,
    valmax=1,
    valinit=0,
)

# Add a reset button
ax_reset = plt.axes([0.8, 0.025, 0.1, 0.04])
reset_button = Button(ax_reset, 'Reset', hovercolor='0.975')

# Variable to store the currently highlighted point
highlighted_point = None

# Function to update the plot based on the threshold
def update_threshold(val):
    # Get the current threshold value
    threshold = threshold_slider.val
    
    # Update the scatter plot to show only points above the threshold
    facecolors = scatter.get_facecolors()
    sizes_array = scatter.get_sizes()
    
    for i, color_val in enumerate(colors):
        if color_val >= threshold:
            # If above threshold, show at full opacity
            facecolors[i, 3] = 0.8
            sizes_array[i] = sizes[i]
        else:
            # If below threshold, show at reduced opacity
            facecolors[i, 3] = 0.1
            sizes_array[i] = sizes[i] * 0.5
    
    scatter.set_facecolors(facecolors)
    scatter.set_sizes(sizes_array)
    fig.canvas.draw_idle()

# Connect the slider to the update function
threshold_slider.on_changed(update_threshold)

# Function to reset the view and slider
def reset(event):
    threshold_slider.reset()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    fig.canvas.draw_idle()

# Connect the reset button to the reset function
reset_button.on_clicked(reset)

# Function to handle hover events
def hover(event):
    global annot
    vis = annot.get_visible()
    
    if event.inaxes == ax:
        cont, ind = scatter.contains(event)
        if cont:
            # Get the index of the point under the cursor
            index = ind["ind"][0]
            
            # Update the position of the annotation
            pos = scatter.get_offsets()[index]
            annot.xy = pos
            
            # Create the text for the annotation
            text = f"Point {index}\nX: {x[index]:.2f}\nY: {y[index]:.2f}\nValue: {colors[index]:.2f}"
            annot.set_text(text)
            
            # Make the annotation visible
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            # If the cursor is not over a point, hide the annotation
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

# Function to handle pick events (clicking on points)
def on_pick(event):
    global highlighted_point
    
    if event.artist == scatter:
        # Get the index of the clicked point
        ind = event.ind[0]
        
        # Remove previous highlight if it exists
        if highlighted_point is not None:
            highlighted_point.remove()
            highlighted_point = None
        
        # Highlight the clicked point with a red circle
        pos = scatter.get_offsets()[ind]
        highlighted_point = ax.plot(pos[0], pos[1], 'o', ms=15, mfc='none', 
                                   mec='red', mew=2, alpha=0.8)[0]
        
        # Add a text label with a white outline for better visibility
        text = ax.text(pos[0], pos[1] + 0.5, f"Selected: {ind}", 
                      ha='center', va='bottom', fontweight='bold')
        text.set_path_effects([path_effects.withStroke(linewidth=3, foreground='white')])
        
        fig.canvas.draw_idle()

# Connect the event handlers
fig.canvas.mpl_connect('motion_notify_event', hover)
fig.canvas.mpl_connect('pick_event', on_pick)

plt.show()

# %%
#
# .. admonition:: References
#
#    The use of the following functions, methods, classes and modules is shown
#    in this example:
#
#    - `matplotlib.figure.Figure`
#    - `matplotlib.axes.Axes.scatter`
#    - `matplotlib.axes.Axes.annotate`
#    - `matplotlib.widgets.Slider`
#    - `matplotlib.widgets.Button`
#    - `matplotlib.patheffects`