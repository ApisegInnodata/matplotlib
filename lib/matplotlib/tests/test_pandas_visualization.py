import unittest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import check_figures_equal
import matplotlib.collections as mcollections


class TestPandasVisualization(unittest.TestCase):
    """Test suite for pandas visualization functionality with exactly 10 test cases."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures for the whole test class."""
        plt.style.use('seaborn-v0_8-whitegrid')

    def setUp(self):
        """Set up test fixtures before each test."""
        # Create reproducible test data
        np.random.seed(42)
        self.dates = pd.date_range('20230101', periods=12)
        self.df = pd.DataFrame({
            'date': self.dates,
            'value_a': np.random.randn(12).cumsum(),
            'value_b': np.random.randn(12).cumsum(),
            'value_c': np.random.randn(12).cumsum(),
            'category': np.random.choice(['A', 'B', 'C'], 12)
        })

    def tearDown(self):
        """Clean up after each test."""
        plt.close('all')

    def test_1_dataframe_creation(self):
        """Test case 1: Verify DataFrame creation and structure."""
        self.assertEqual(self.df.shape, (12, 5))
        self.assertListEqual(list(self.df.columns), ['date', 'value_a', 'value_b', 'value_c', 'category'])
        self.assertTrue(isinstance(self.df['date'][0], pd.Timestamp))
        self.assertEqual(len(self.df['category'].unique()), 3)

    def test_2_line_plot(self):
        """Test case 2: Test basic line plot creation and properties."""
        ax = self.df.plot(x='date', y=['value_a', 'value_b', 'value_c'])

        # Verify plot properties
        self.assertEqual(len(ax.lines), 3)
        self.assertEqual(ax.get_xlabel(), 'date')
        self.assertEqual(len(ax.get_legend().get_texts()), 3)

        # Verify data integrity
        line_data = ax.lines[0].get_xydata()
        self.assertEqual(len(line_data), len(self.df))

    def test_3_scatter_plot(self):
        """Test case 3: Test scatter plot creation and properties."""
        ax = self.df.plot.scatter(x='value_a', y='value_b', c='value_c', cmap='viridis')

        # Verify scatter plot properties
        self.assertTrue(isinstance(ax.collections[0], plt.cm.ScalarMappable))
        self.assertEqual(ax.get_xlabel(), 'value_a')
        self.assertEqual(ax.get_ylabel(), 'value_b')
        self.assertEqual(len(ax.collections[0].get_offsets()), len(self.df))

    def test_4_bar_plot(self):
        """Test case 4: Test bar plot creation and properties."""
        category_means = self.df.groupby('category').mean(numeric_only=True)
        ax = category_means.plot(kind='bar')
        
        # Verify bar plot properties
        self.assertTrue(isinstance(ax.patches[0], plt.Rectangle))
        self.assertEqual(len(ax.patches), len(category_means.columns) * len(category_means.index))
        self.assertEqual(ax.get_xlabel(), 'category')  # Changed from '' to 'category'

    def test_5_histogram(self):
        """Test case 5: Test histogram creation and properties."""
        ax = self.df[['value_a', 'value_b', 'value_c']].plot.hist(bins=10, alpha=0.5)

        # Verify histogram properties
        self.assertEqual(len(ax.patches), 30)  # 3 columns * 10 bins
        self.assertEqual(ax.get_ylabel(), 'Frequency')

        # Verify all patches are Rectangle objects
        self.assertTrue(all(isinstance(patch, plt.Rectangle) for patch in ax.patches))

    def test_6_box_plot(self):
        """Test case 6: Test box plot creation and statistical properties."""
        # Create box plot
        ax = self.df.boxplot(column=['value_a', 'value_b', 'value_c'], by='category')
        
        # Verify box plot properties
        self.assertEqual(len(ax), 2)  # Number of axes in the array
        
        # Get the actual box plot elements from the first axis
        box_elements = ax.flat[0].get_children()
        
        # Count the number of lines (medians, whiskers, caps, fliers)
        lines = [element for element in box_elements if isinstance(element, plt.Line2D)]
        
        # Each box has:
        # - 1 median line
        # - 2 whiskers
        # - 2 caps
        # - 2 flier lines (outliers)
        # For 3 columns (value_a, value_b, value_c), we expect 21 lines total (7 lines × 3 boxes)
        self.assertEqual(len(lines), 21)

    def test_7_heatmap_correlation(self):
        """Test case 7: Test heatmap creation and correlation matrix."""
        corr = self.df[['value_a', 'value_b', 'value_c']].corr()
        fig, ax = plt.subplots()
        im = ax.imshow(corr, cmap='coolwarm')

        # Verify heatmap properties
        self.assertEqual(im.get_array().shape, (3, 3))
        self.assertTrue(np.array_equal(im.get_array(), corr.values))
        self.assertEqual(im.get_cmap().name, 'coolwarm')

    def test_8_missing_data_handling(self):
        """Test case 8: Test plotting with missing data."""
        df_missing = self.df.copy()
        df_missing.loc[3:5, 'value_a'] = np.nan
        df_missing.loc[7:9, 'value_b'] = np.nan

        ax = df_missing.plot(x='date', y=['value_a', 'value_b', 'value_c'])

        # Verify handling of missing data
        self.assertEqual(len(ax.lines), 3)
        self.assertTrue(np.any(np.isnan(df_missing['value_a'])))
        self.assertTrue(np.any(np.isnan(df_missing['value_b'])))

    def test_9_plot_customization(self):
        """Test case 9: Test plot customization options."""
        fig, ax = plt.subplots(figsize=(10, 6))
        self.df.plot(x='date', y='value_a', ax=ax,
                     color='red', marker='o', linestyle='--',
                     label='Custom Series')

        # Verify customization properties
        self.assertEqual(ax.lines[0].get_color(), 'red')
        self.assertEqual(ax.lines[0].get_marker(), 'o')
        self.assertEqual(ax.lines[0].get_linestyle(), '--')
        self.assertEqual(fig.get_size_inches().tolist(), [10.0, 6.0])

    def test_10_area_plot(self):
        """Test case 10: Test area plot creation and stacking."""
        ax = self.df.plot.area(x='date', y=['value_a', 'value_b', 'value_c'], stacked=False)
        
        # Verify area plot properties
        self.assertEqual(len(ax.collections), 3)  # One collection per series
        self.assertTrue(all(isinstance(col, mcollections.PolyCollection) 
                      for col in ax.collections))
        self.assertEqual(ax.get_xlabel(), 'date')


if __name__ == '__main__':
    unittest.main(verbosity=2)