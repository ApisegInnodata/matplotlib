"""
.. _publication_quality_figures:

==============================
Creating Publication-Quality Figures
==============================

A tutorial on creating publication-ready figures with Matplotlib.

This tutorial demonstrates techniques for creating high-quality figures
suitable for academic publications, presentations, and reports. We'll
cover layout, styling, typography, and export settings to create
professional visualizations.
"""

# %%
# Introduction
# ============
#
# Creating figures for publications requires attention to detail and
# adherence to certain standards. This tutorial will guide you through
# the process of creating publication-quality figures with Matplotlib.
#
# We'll start by importing the necessary libraries:

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
import os, matplotlib

if os.environ.get("TEST_MODE") == "1":
    matplotlib.use("Agg")


# Set a seed for reproducibility
np.random.seed(42)

# %%
# Figure Size and Resolution
# =========================
#
# One of the most important aspects of publication-quality figures is
# choosing the right size and resolution. Most journals have specific
# requirements for figure dimensions and DPI (dots per inch).
#
# Here's how to set up a figure with specific dimensions in inches:

# Create a figure with specific dimensions (width, height in inches)
plt.figure(figsize=(7, 5))  # Common size for a single-column figure

# Create some sample data
x = np.linspace(0, 10, 100)
y = np.sin(x) * np.exp(-0.1 * x)

# Create a simple plot
plt.plot(x, y, 'b-', linewidth=1.5)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Sample Figure')

# Add a grid for better readability
plt.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

# %%
# When saving figures for publication, you'll want to use a high DPI setting:
#
# ```python
# plt.savefig('figure_name.png', dpi=300, bbox_inches='tight')
# plt.savefig('figure_name.pdf', bbox_inches='tight')  # Vector format for best quality
# ```
#
# Typography and Fonts
# ===================
#
# Typography is crucial for readability. Many journals prefer sans-serif fonts
# like Arial or Helvetica. Here's how to set up your figures with appropriate fonts:

# Set the font family globally
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'figure.titlesize': 18
})

# Create a figure with improved typography
fig, ax = plt.subplots(figsize=(7, 5))

# Plot the same data
ax.plot(x, y, 'b-', linewidth=1.5)

# Add labels with LaTeX formatting for mathematical symbols
ax.set_xlabel(r'Time ($t$)')
ax.set_ylabel(r'Amplitude ($\alpha$)')
ax.set_title('Damped Sine Wave')

# Add a grid
ax.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

# %%
# Color Selection
# ==============
#
# Color choice is important for clarity and accessibility. For publications,
# it's best to use a color scheme that works well in both color and grayscale
# (in case your paper is printed in black and white).

# Create a figure with a colorblind-friendly palette
fig, ax = plt.subplots(figsize=(7, 5))

# Create some sample data
x = np.linspace(0, 10, 100)
y1 = np.sin(x) * np.exp(-0.1 * x)
y2 = np.cos(x) * np.exp(-0.1 * x)
y3 = 0.5 * np.exp(-0.1 * x)

# Use a colorblind-friendly palette
# These colors are distinguishable even in grayscale
colors = ['#0072B2', '#D55E00', '#009E73']  # Blue, orange-red, green

# Plot the data
ax.plot(x, y1, color=colors[0], linewidth=2, label='Sine')
ax.plot(x, y2, color=colors[1], linewidth=2, label='Cosine')
ax.plot(x, y3, color=colors[2], linewidth=2, label='Exponential')

# Add labels
ax.set_xlabel('Time')
ax.set_ylabel('Amplitude')
ax.set_title('Multiple Curves with Colorblind-Friendly Colors')

# Add a legend with a clean, transparent background
ax.legend(framealpha=0.9, loc='upper right')

# Add a grid
ax.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

# %%
# Line Styles and Markers
# ======================
#
# For publications, it's important to use line styles and markers that are
# clearly distinguishable, especially when plotting multiple datasets:

# Create a figure with distinct line styles and markers
fig, ax = plt.subplots(figsize=(7, 5))

# Create some sample data
x = np.linspace(0, 10, 20)  # Fewer points to make markers more visible
y1 = np.sin(x) * np.exp(-0.1 * x)
y2 = np.cos(x) * np.exp(-0.1 * x)
y3 = 0.5 * np.exp(-0.1 * x)

# Plot with different line styles and markers
ax.plot(x, y1, 'o-', color='#0072B2', linewidth=1.5, 
       markersize=6, label='Sine')
ax.plot(x, y2, 's--', color='#D55E00', linewidth=1.5, 
       markersize=6, label='Cosine')
ax.plot(x, y3, '^:', color='#009E73', linewidth=1.5, 
       markersize=6, label='Exponential')

# Add labels
ax.set_xlabel('Time')
ax.set_ylabel('Amplitude')
ax.set_title('Multiple Curves with Distinct Styles')

# Add a legend
ax.legend(frameon=True, fancybox=False, edgecolor='black')

# Add a grid
ax.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

# %%
# Axis Styling
# ===========
#
# Professional-looking figures often have well-styled axes with appropriate
# tick marks, limits, and labels:

# Create a figure with well-styled axes
fig, ax = plt.subplots(figsize=(7, 5))

# Create some sample data
x = np.linspace(0, 10, 100)
y = np.sin(x) * np.exp(-0.1 * x)

# Plot the data
ax.plot(x, y, 'b-', linewidth=1.5)

# Set axis limits
ax.set_xlim(0, 10)
ax.set_ylim(-1, 1)

# Add major and minor ticks
ax.xaxis.set_major_locator(MultipleLocator(2))
ax.xaxis.set_minor_locator(MultipleLocator(0.5))
ax.yaxis.set_major_locator(MultipleLocator(0.5))
ax.yaxis.set_minor_locator(MultipleLocator(0.1))

# Style the ticks
ax.tick_params(which='major', length=6, width=1, direction='out')
ax.tick_params(which='minor', length=3, width=1, direction='out')

# Add labels
ax.set_xlabel('Time')
ax.set_ylabel('Amplitude')
ax.set_title('Well-Styled Axes')

# Add a grid aligned with major ticks
ax.grid(True, which='major', linestyle='-', alpha=0.3)
ax.grid(True, which='minor', linestyle=':', alpha=0.2)

plt.tight_layout()
plt.show()

# %%
# Multi-panel Figures
# ==================
#
# Publications often require multi-panel figures to present related data
# together. Here's how to create a professional multi-panel figure:

# Create a multi-panel figure
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# Flatten the axes array for easier indexing
axes = axes.flatten()

# Create some sample data
x = np.linspace(0, 10, 100)
y1 = np.sin(x) * np.exp(-0.1 * x)
y2 = np.cos(x) * np.exp(-0.1 * x)
y3 = np.sin(2*x) * np.exp(-0.1 * x)
y4 = np.cos(2*x) * np.exp(-0.1 * x)

# Plot data in each panel
axes[0].plot(x, y1, 'b-')
axes[0].set_title('Panel A: Damped Sine')
axes[0].set_xlabel('Time')
axes[0].set_ylabel('Amplitude')

axes[1].plot(x, y2, 'r-')
axes[1].set_title('Panel B: Damped Cosine')
axes[1].set_xlabel('Time')
axes[1].set_ylabel('Amplitude')

axes[2].plot(x, y3, 'g-')
axes[2].set_title('Panel C: Double Frequency Sine')
axes[2].set_xlabel('Time')
axes[2].set_ylabel('Amplitude')

axes[3].plot(x, y4, 'm-')
axes[3].set_title('Panel D: Double Frequency Cosine')
axes[3].set_xlabel('Time')
axes[3].set_ylabel('Amplitude')

# Add a grid to all panels
for ax in axes:
    ax.grid(True, linestyle='--', alpha=0.7)

# Adjust spacing between subplots
plt.tight_layout()

# Add a main title for the entire figure
fig.suptitle('Multi-panel Figure Example', fontsize=16, y=1.02)

plt.show()

# %%
# Adding Annotations
# =================
#
# Annotations can help highlight important features in your data:

# Create a figure with annotations
fig, ax = plt.subplots(figsize=(7, 5))

# Create some sample data
x = np.linspace(0, 10, 100)
y = np.sin(x) * np.exp(-0.1 * x)

# Plot the data
ax.plot(x, y, 'b-', linewidth=1.5)

# Find the maximum point
max_idx = np.argmax(y)
max_x, max_y = x[max_idx], y[max_idx]

# Find the first zero crossing after the maximum
zero_crossings = np.where(np.diff(np.signbit(y)))[0]
first_zero_after_max = next((i for i in zero_crossings if x[i] > max_x), None)
zero_x, zero_y = x[first_zero_after_max], y[first_zero_after_max]

# Add annotations
ax.annotate('Maximum', 
           xy=(max_x, max_y), xytext=(max_x+1, max_y+0.2),
           arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
           fontsize=12)

ax.annotate('Zero Crossing', 
           xy=(zero_x, zero_y), xytext=(zero_x+1, zero_y-0.2),
           arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
           fontsize=12)

# Add a horizontal line at y=0
ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)

# Add labels
ax.set_xlabel('Time')
ax.set_ylabel('Amplitude')
ax.set_title('Annotated Figure')

# Add a grid
ax.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

# %%
# Error Bars and Uncertainty
# =========================
#
# Scientific publications often require error bars to represent uncertainty:

# Create a figure with error bars
fig, ax = plt.subplots(figsize=(7, 5))

# Create some sample data with error
x = np.linspace(0, 10, 10)
y = np.sin(x) * np.exp(-0.1 * x)
y_err = 0.1 * np.random.rand(len(x))

# Plot the data with error bars
ax.errorbar(x, y, yerr=y_err, fmt='o-', capsize=3, capthick=1, 
           ecolor='gray', markersize=6, linewidth=1.5)

# Add labels
ax.set_xlabel('Time')
ax.set_ylabel('Amplitude')
ax.set_title('Data with Error Bars')

# Add a grid
ax.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

# %%
# Statistical Visualizations
# =========================
#
# Publications often include statistical visualizations like box plots
# or violin plots:

# Create a figure with statistical visualizations
fig, ax = plt.subplots(figsize=(7, 5))

# Create some sample data
data = [np.random.normal(0, std, 100) for std in range(1, 5)]
labels = ['Group A', 'Group B', 'Group C', 'Group D']

# Create a box plot
ax.boxplot(data, labels=labels, patch_artist=True,
          boxprops=dict(facecolor='lightblue', color='blue'),
          whiskerprops=dict(color='blue'),
          capprops=dict(color='blue'),
          medianprops=dict(color='red'))

# Add labels
ax.set_xlabel('Group')
ax.set_ylabel('Value')
ax.set_title('Box Plot for Statistical Comparison')

# Add a grid
ax.grid(True, axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

# %%
# Consistent Style Across Multiple Figures
# =======================================
#
# For publications with multiple figures, it's important to maintain a
# consistent style. You can use a style sheet or create a custom style:

# Define a custom style dictionary
custom_style = {
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'axes.grid': True,
    'grid.linestyle': '--',
    'grid.alpha': 0.7,
    'lines.linewidth': 1.5,
    'axes.spines.top': False,
    'axes.spines.right': False,
}

# Apply the custom style
with plt.style.context(custom_style):
    # Create two figures with consistent styling
    fig1, ax1 = plt.subplots(figsize=(7, 5))
    x = np.linspace(0, 10, 100)
    y = np.sin(x) * np.exp(-0.1 * x)
    ax1.plot(x, y)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Amplitude')
    ax1.set_title('Figure 1: Damped Sine Wave')
    
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    x = np.linspace(0, 10, 100)
    y = np.cos(x) * np.exp(-0.1 * x)
    ax2.plot(x, y)
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Amplitude')
    ax2.set_title('Figure 2: Damped Cosine Wave')
    
    if os.environ.get("TEST_MODE") == "1":
        plt.savefig("test_output_pub_quality.png")
    else:
        plt.show()


# %%
# Exporting Figures for Publication
# ================================
#
# When preparing figures for publication, it's important to export them
# in the right format and with the right settings:
#
# ```python
# # Save as a high-resolution PNG (raster format)
# plt.savefig('figure_name.png', dpi=300, bbox_inches='tight')
#
# # Save as a PDF (vector format, preferred for publications)
# plt.savefig('figure_name.pdf', bbox_inches='tight')
#
# # Save as EPS (another vector format often required by journals)
# plt.savefig('figure_name.eps', bbox_inches='tight')
# ```
#
# The `bbox_inches='tight'` parameter ensures that the figure is cropped
# tightly around the content, eliminating unnecessary white space.
#
# Conclusion
# ==========
#
# Creating publication-quality figures requires attention to detail in
# several areas:
#
# - Figure size and resolution
# - Typography and fonts
# - Color selection
# - Line styles and markers
# - Axis styling
# - Multi-panel layouts
# - Annotations and error bars
# - Consistent styling across figures
# - Proper export settings
#
# By following the guidelines in this tutorial, you can create professional
# figures that effectively communicate your results and meet the standards
# of academic journals and professional publications.
