"""
.. _pandas_visualization:

===============================
Data Visualization with pandas
===============================

A tutorial on effectively visualizing pandas DataFrames with Matplotlib.

This tutorial demonstrates how to create various types of visualizations
using pandas DataFrames with Matplotlib. pandas is a powerful data analysis
library that works seamlessly with Matplotlib to create insightful
visualizations of tabular data.
"""

# %%
# Introduction to pandas and Matplotlib integration
# =================================================
#
# pandas DataFrames provide built-in plotting functionality that is built
# on top of Matplotlib. This makes it easy to create visualizations directly
# from your data without having to extract arrays or convert data types.
#
# First, let's import the necessary libraries and create some sample data:

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Set the style to a more visually appealing one
plt.style.use('seaborn-v0_8-whitegrid')

# Create a sample DataFrame with various data types
np.random.seed(42)  # For reproducibility
dates = pd.date_range('20230101', periods=12)
df = pd.DataFrame({
    'date': dates,
    'value_a': np.random.randn(12).cumsum(),
    'value_b': np.random.randn(12).cumsum(),
    'value_c': np.random.randn(12).cumsum(),
    'category': np.random.choice(['A', 'B', 'C'], 12)
})

# Display the first few rows of the DataFrame
print(df.head())

# %%
# Basic Line Plots
# ===============
#
# The simplest way to visualize time series or sequential data is with a line plot.
# pandas makes this extremely easy with the `plot()` method:

# Create a simple line plot of the three value columns
ax = df.plot(x='date', y=['value_a', 'value_b', 'value_c'], figsize=(10, 6))
ax.set_xlabel('Date')
ax.set_ylabel('Value')
ax.set_title('Time Series Data')
plt.tight_layout()
plt.show()

# %%
# You can also create individual line plots for each column using the `subplots=True` parameter:

# Create separate subplots for each column
fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
df.plot(x='date', y='value_a', ax=axes[0], legend=False, color='blue')
df.plot(x='date', y='value_b', ax=axes[1], legend=False, color='green')
df.plot(x='date', y='value_c', ax=axes[2], legend=False, color='red')

# Set titles for each subplot
axes[0].set_title('Value A')
axes[1].set_title('Value B')
axes[2].set_title('Value C')

# Set common labels
axes[2].set_xlabel('Date')
fig.text(0.04, 0.5, 'Value', va='center', rotation='vertical')

plt.tight_layout()
plt.show()

# %%
# Bar Charts
# ==========
#
# Bar charts are excellent for comparing categorical data or showing values
# across different categories:

# Group by category and calculate the mean of each value column
category_means = df.groupby('category').mean(numeric_only=True)

# Create a bar chart
ax = category_means.plot(kind='bar', figsize=(10, 6))
ax.set_xlabel('Category')
ax.set_ylabel('Mean Value')
ax.set_title('Mean Values by Category')
plt.tight_layout()
plt.show()

# %%
# Scatter Plots
# =============
#
# Scatter plots are useful for showing the relationship between two variables:

# Create a scatter plot
ax = df.plot.scatter(x='value_a', y='value_b', c='value_c', 
                    cmap='viridis', figsize=(10, 6), s=50)
ax.set_xlabel('Value A')
ax.set_ylabel('Value B')
ax.set_title('Scatter Plot: Value A vs Value B (colored by Value C)')
plt.colorbar(ax.collections[0], label='Value C')
plt.tight_layout()
plt.show()

# %%
# Histograms and Density Plots
# ============================
#
# Histograms and density plots help visualize the distribution of data:

# Create a figure with multiple subplots
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Create a histogram
df[['value_a', 'value_b', 'value_c']].plot.hist(alpha=0.5, bins=10, ax=axes[0])
axes[0].set_xlabel('Value')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Histogram of Values')

# Create a density plot
df[['value_a', 'value_b', 'value_c']].plot.kde(ax=axes[1])
axes[1].set_xlabel('Value')
axes[1].set_ylabel('Density')
axes[1].set_title('Density Plot of Values')

plt.tight_layout()
plt.show()

# %%
# Box Plots
# =========
#
# Box plots are great for showing the distribution of data across categories:

# Create a box plot grouped by category
df.boxplot(column=['value_a', 'value_b', 'value_c'], by='category', figsize=(12, 6))
plt.suptitle('Box Plots by Category')
plt.tight_layout()
plt.show()

# %%
# Heatmaps
# ========
#
# Heatmaps are useful for visualizing correlations or patterns in tabular data:

# Calculate the correlation matrix
corr = df[['value_a', 'value_b', 'value_c']].corr()

# Create a heatmap
fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(corr, cmap='coolwarm')

# Add labels and colorbar
ax.set_xticks(np.arange(len(corr.columns)))
ax.set_yticks(np.arange(len(corr.columns)))
ax.set_xticklabels(corr.columns)
ax.set_yticklabels(corr.columns)

# Rotate the tick labels and set their alignment
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Add colorbar
cbar = ax.figure.colorbar(im, ax=ax)
cbar.ax.set_ylabel('Correlation', rotation=-90, va="bottom")

# Add text annotations
for i in range(len(corr.columns)):
    for j in range(len(corr.columns)):
        text = ax.text(j, i, f"{corr.iloc[i, j]:.2f}",
                       ha="center", va="center", color="black")

ax.set_title("Correlation Heatmap")
fig.tight_layout()
plt.show()

# %%
# Area Plots
# ==========
#
# Area plots are useful for showing values over time:

# Create an area plot
ax = df.plot.area(x='date', y=['value_a', 'value_b', 'value_c'], 
                 figsize=(10, 6), alpha=0.5, stacked=False)
ax.set_xlabel('Date')
ax.set_ylabel('Value')
ax.set_title('Area Plot of Values Over Time')
plt.tight_layout()
plt.show()

# %%
# Customizing pandas Plots
# =======================
#
# pandas plots are Matplotlib plots under the hood, so you can customize them
# using all the Matplotlib customization options:

# Create a custom plot with specific colors, markers, and styles
fig, ax = plt.subplots(figsize=(10, 6))

# Plot each column with custom styling
df.plot(x='date', y='value_a', ax=ax, label='Series A', 
       color='blue', marker='o', linestyle='-')
df.plot(x='date', y='value_b', ax=ax, label='Series B', 
       color='green', marker='s', linestyle='--')
df.plot(x='date', y='value_c', ax=ax, label='Series C', 
       color='red', marker='^', linestyle=':')

# Customize the plot
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Value', fontsize=12)
ax.set_title('Custom Styled Time Series Plot', fontsize=14)
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend(loc='best', frameon=True, fancybox=True, shadow=True)

# Add annotations
max_a_idx = df['value_a'].idxmax()
ax.annotate(f'Max A: {df.loc[max_a_idx, "value_a"]:.2f}',
           xy=(df.loc[max_a_idx, 'date'], df.loc[max_a_idx, 'value_a']),
           xytext=(10, 20), textcoords='offset points',
           arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))

plt.tight_layout()
plt.show()

# %%
# Working with Missing Data
# ========================
#
# pandas handles missing data gracefully in visualizations:

# Create a DataFrame with some missing values
df_missing = df.copy()
df_missing.loc[3:5, 'value_a'] = np.nan
df_missing.loc[7:9, 'value_b'] = np.nan

# Plot with missing values
ax = df_missing.plot(x='date', y=['value_a', 'value_b', 'value_c'], figsize=(10, 6))
ax.set_xlabel('Date')
ax.set_ylabel('Value')
ax.set_title('Time Series with Missing Values')
plt.tight_layout()
plt.show()

# %%
# Combining Multiple Plot Types
# ============================
#
# You can combine different plot types to create more complex visualizations:

# Create a figure and primary axis
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot line charts on the primary axis
df.plot(x='date', y=['value_a', 'value_b'], ax=ax1, style=['-', '--'])
ax1.set_xlabel('Date')
ax1.set_ylabel('Values A & B', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Create a secondary y-axis
ax2 = ax1.twinx()
df.plot(x='date', y='value_c', ax=ax2, color='red', style=':')
ax2.set_ylabel('Value C', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Add a title and adjust the layout
plt.title('Multiple Plot Types on Dual Y-Axes')
fig.tight_layout()
plt.show()

# %%
# Conclusion
# ==========
#
# pandas provides a powerful and convenient interface to Matplotlib for
# creating a wide variety of visualizations from DataFrame data. By leveraging
# the integration between these libraries, you can quickly create insightful
# visualizations with minimal code.
#
# The key benefits of using pandas with Matplotlib include:
#
# - Direct plotting from DataFrames without data extraction
# - Automatic handling of dates, categories, and missing values
# - Simple creation of common plot types with sensible defaults
# - Full access to Matplotlib's customization capabilities
#
# This tutorial covered the basics, but there are many more plot types and
# customization options available. Experiment with different combinations to
# find the best way to visualize your specific data.