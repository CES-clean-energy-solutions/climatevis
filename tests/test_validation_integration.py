#!/usr/bin/env python3
"""
Test script to verify that all plotting functions have validation integrated.
This tests the validation utilities and ensures they work correctly with all plotting functions.
"""

import pandas as pd
import numpy as np
import pytest
from datetime import datetime, timedelta

import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import all plotting functions
from climatevis.plots.plot_series import plot_series
from climatevis.plots.plot_series import plot_timeseries_df
from climatevis.plots.wind_rose import wind_rose
from climatevis.plots.exceedance import exceedance
from climatevis.plots.exceedance_bands import exceedance_bands
from climatevis.plots.annual_heatmap import annual_heatmap
from climatevis.plots.histogram import histogram
from climatevis.plots.histogram_multiple import multiple_histograms
from climatevis.plots.cumulative_probability import cumulative_probability
from climatevis.plots.monthly_profiles import monthly_profiles
from climatevis.plots.annual_profile_daily import annual_profile_daily
from climatevis.plots.monthly_profiles_bands import monthly_profiles_bands

# Import validation utilities
from climatevis.util.validation import (
    validate_series_list,
    validate_series_attributes,
    validate_datetime_index,
    validate_template_name,
    validate_paper_size,
    validate_data_quality,
    validate_plot_parameters
)

def create_test_series(name="Test Series", length=1000):
    """Create a test series with DatetimeIndex for testing."""
    start_date = datetime(2020, 1, 1)
    dates = [start_date + timedelta(hours=i) for i in range(length)]
    values = np.random.normal(20, 5, length)
    series = pd.Series(values, index=pd.DatetimeIndex(dates), name=name)
    return series

def create_test_sector_series(length=1000):
    """Create a test sector series for wind rose testing."""
    sectors = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
               'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    start_date = datetime(2020, 1, 1)
    dates = [start_date + timedelta(hours=i) for i in range(length)]
    sector_values = np.random.choice(sectors, length)
    series = pd.Series(sector_values, index=pd.DatetimeIndex(dates), name="Wind Direction")
    return series

class TestValidationIntegration:
    """Test class for validation integration with plotting functions."""

    def setup_method(self):
        """Set up test data for each test method."""
        self.test_series = create_test_series("Temperature", 1000)
        self.test_series2 = create_test_series("Humidity", 1000)
        self.test_sector = create_test_sector_series(1000)
        self.test_windspeed = create_test_series("Wind Speed", 1000)
        self.series_list = [self.test_series, self.test_series2]

    def test_plot_series_validation(self):
        """Test that plot_series function has validation integrated."""
        # Should work with valid inputs
        fig = plot_series(self.test_series, "plotly_white", "A4_PORTRAIT")
        assert fig is not None

        # Should raise error with invalid template
        with pytest.raises(ValueError, match="plot_series: Invalid template name"):
            plot_series(self.test_series, "invalid_template", "A4_PORTRAIT")

        # Should raise error with invalid paper size
        with pytest.raises(ValueError, match="plot_series: Invalid paper size"):
            plot_series(self.test_series, "plotly_white", "invalid_size")

    def test_plot_timeseries_df_validation(self):
        """Test that plot_timeseries_df function has validation integrated."""
        df = self.test_series.to_frame()

        # Should work with valid inputs
        fig = plot_timeseries_df(df, "plotly_white", "A4_PORTRAIT")
        assert fig is not None

        # Should raise error with invalid template
        with pytest.raises(ValueError, match="plot_timeseries_df: Invalid template name"):
            plot_timeseries_df(df, "invalid_template", "A4_PORTRAIT")

    def test_wind_rose_validation(self):
        """Test that wind_rose function has validation integrated."""
        # Should work with valid inputs
        fig = wind_rose(self.test_windspeed, self.test_sector, "plotly_white", "A4_PORTRAIT")
        assert fig is not None

        # Should raise error with invalid template
        with pytest.raises(ValueError, match="wind_rose: Invalid template name"):
            wind_rose(self.test_windspeed, self.test_sector, "invalid_template", "A4_PORTRAIT")

        # Should raise error with mismatched indices
        different_series = create_test_series("Different", 500)
        with pytest.raises(ValueError, match="wind_rose: windspeed and sector must have the same DatetimeIndex"):
            wind_rose(different_series, self.test_sector, "plotly_white", "A4_PORTRAIT")

    def test_exceedance_validation(self):
        """Test that exceedance function has validation integrated."""
        # Should work with valid inputs
        fig = exceedance(self.test_series, "plotly_white", "A4_PORTRAIT")
        assert fig is not None

        # Should raise error with invalid template
        with pytest.raises(ValueError, match="exceedance: Invalid template name"):
            exceedance(self.test_series, "invalid_template", "A4_PORTRAIT")

    def test_exceedance_bands_validation(self):
        """Test that exceedance_bands function has validation integrated."""
        # Should work with valid inputs
        fig = exceedance_bands(self.series_list, "plotly_white", "A4_PORTRAIT")
        assert fig is not None

        # Should raise error with invalid template
        with pytest.raises(ValueError, match="exceedance_bands: Invalid template name"):
            exceedance_bands(self.series_list, "invalid_template", "A4_PORTRAIT")

    def test_annual_heatmap_validation(self):
        """Test that annual_heatmap function has validation integrated."""
        # Should work with valid inputs
        fig = annual_heatmap(self.test_series, "plotly_white", "A4_PORTRAIT")
        assert fig is not None

        # Should raise error with invalid template
        with pytest.raises(ValueError, match="annual_heatmap: Invalid template name"):
            annual_heatmap(self.test_series, "invalid_template", "A4_PORTRAIT")

    def test_histogram_validation(self):
        """Test that histogram function has validation integrated."""
        # Should work with valid inputs
        fig = histogram(self.test_series, "plotly_white", "A4_PORTRAIT")
        assert fig is not None

        # Should raise error with invalid template
        with pytest.raises(ValueError, match="histogram: Invalid template name"):
            histogram(self.test_series, "invalid_template", "A4_PORTRAIT")

    def test_multiple_histograms_validation(self):
        """Test that multiple_histograms function has validation integrated."""
        # Should work with valid inputs
        fig = multiple_histograms(self.series_list, "plotly_white", "A4_PORTRAIT")
        assert fig is not None

        # Should raise error with invalid template
        with pytest.raises(ValueError, match="multiple_histograms: Invalid template name"):
            multiple_histograms(self.series_list, "invalid_template", "A4_PORTRAIT")

    def test_cumulative_probability_validation(self):
        """Test that cumulative_probability function has validation integrated."""
        # Should work with valid inputs
        fig = cumulative_probability(self.series_list, "plotly_white", "A4_PORTRAIT")
        assert fig is not None

        # Should raise error with invalid template
        with pytest.raises(ValueError, match="cumulative_probability: Invalid template name"):
            cumulative_probability(self.series_list, "invalid_template", "A4_PORTRAIT")

        # Should raise error with invalid y_grid_spacing
        with pytest.raises(ValueError, match="cumulative_probability: y_grid_spacing must be an integer between 1 and 100"):
            cumulative_probability(self.series_list, "plotly_white", "A4_PORTRAIT", y_grid_spacing=0)

    def test_monthly_profiles_validation(self):
        """Test that monthly_profiles function has validation integrated."""
        # Should work with valid inputs
        fig = monthly_profiles(self.test_series, "plotly_white", "A4_PORTRAIT")
        assert fig is not None

        # Should raise error with invalid template
        with pytest.raises(ValueError, match="monthly_profiles: Invalid template name"):
            monthly_profiles(self.test_series, "invalid_template", "A4_PORTRAIT")

    def test_annual_profile_daily_validation(self):
        """Test that annual_profile_daily function has validation integrated."""
        # Should work with valid inputs
        fig = annual_profile_daily(self.test_series, "plotly_white", "A4_PORTRAIT")
        assert fig is not None

        # Should raise error with invalid template
        with pytest.raises(ValueError, match="annual_profile_daily: Invalid template name"):
            annual_profile_daily(self.test_series, "invalid_template", "A4_PORTRAIT")

    def test_monthly_profiles_bands_validation(self):
        """Test that monthly_profiles_bands function has validation integrated."""
        # Should work with valid inputs
        fig = monthly_profiles_bands(self.series_list, "plotly_white", "A4_PORTRAIT")
        assert fig is not None

        # Should raise error with invalid template
        with pytest.raises(ValueError, match="monthly_profiles_bands: Invalid template name"):
            monthly_profiles_bands(self.series_list, "invalid_template", "A4_PORTRAIT")

class TestValidationUtilities:
    """Test class for validation utility functions."""

    def setup_method(self):
        """Set up test data for each test method."""
        self.test_series = create_test_series("Temperature", 1000)
        self.test_series2 = create_test_series("Humidity", 1000)
        self.series_list = [self.test_series, self.test_series2]

    def test_validate_series_list(self):
        """Test validate_series_list function."""
        # Valid input
        result = validate_series_list(self.series_list, "test_function")
        assert result == self.series_list

        # Invalid input - not a list
        with pytest.raises(ValueError, match="test_function: series_list must be a list or tuple"):
            validate_series_list(self.test_series, "test_function")

        # Invalid input - empty list
        with pytest.raises(ValueError, match="test_function: series_list cannot be empty"):
            validate_series_list([], "test_function")

        # Invalid input - not all series
        with pytest.raises(ValueError, match="test_function: Item 1 in series_list must be a pandas Series"):
            validate_series_list([self.test_series, "not a series"], "test_function")

    def test_validate_series_attributes(self):
        """Test validate_series_attributes function."""
        # Valid input - should not raise error (require_attributes=False by default)
        validate_series_attributes(self.series_list, "test_function")

        # Invalid input - no name with require_attributes=True
        series_no_name = self.test_series.copy()
        series_no_name.name = None
        with pytest.raises(ValueError, match="test_function: Series 0 must have a 'name' attribute"):
            validate_series_attributes([series_no_name], "test_function", require_attributes=True)

    def test_validate_datetime_index(self):
        """Test validate_datetime_index function."""
        # Valid input
        validate_datetime_index(self.series_list, "test_function")

        # Invalid input - not DatetimeIndex
        series_no_datetime = pd.Series([1, 2, 3], name="Test")
        with pytest.raises(ValueError, match="test_function: Series 0 \\(Temperature\\) must have DatetimeIndex"):
            validate_datetime_index([series_no_datetime], "test_function")

    def test_validate_template_name(self):
        """Test validate_template_name function."""
        # Valid templates
        valid_templates = ["plotly_white", "plotly_dark", "simple_white", "plotly"]
        for template in valid_templates:
            validate_template_name(template, "test_function")

        # Invalid template
        with pytest.raises(ValueError, match="test_function: Invalid template name"):
            validate_template_name("invalid_template", "test_function")

    def test_validate_paper_size(self):
        """Test validate_paper_size function."""
        # Valid paper sizes
        valid_sizes = ["A4_PORTRAIT", "A5_PORTRAIT", "A3_PORTRAIT", "A4_LANDSCAPE", "A5_LANDSCAPE"]
        for size in valid_sizes:
            validate_paper_size(size, "test_function")

        # Invalid paper size
        with pytest.raises(ValueError, match="test_function: Invalid paper size"):
            validate_paper_size("invalid_size", "test_function")

    def test_validate_data_quality(self):
        """Test validate_data_quality function."""
        # Valid data
        validate_data_quality(self.series_list, "test_function")

        # Invalid data - all NaN
        series_all_nan = pd.Series([np.nan, np.nan, np.nan], name="Test")
        with pytest.raises(ValueError, match="test_function: Series 0 contains no valid data"):
            validate_data_quality([series_all_nan], "test_function")

        # Invalid data - all zeros
        series_all_zeros = pd.Series([0, 0, 0], name="Test")
        with pytest.raises(ValueError, match="test_function: Series 0 contains no variation"):
            validate_data_quality([series_all_zeros], "test_function")

    def test_validate_plot_parameters(self):
        """Test validate_plot_parameters function."""
        # Valid single series
        result = validate_plot_parameters(self.test_series, "plotly_white", "A4_PORTRAIT", "test_function")
        assert result == self.test_series

        # Valid series list
        result = validate_plot_parameters(self.series_list, "plotly_white", "A4_PORTRAIT", "test_function")
        assert result == self.series_list

        # Invalid template
        with pytest.raises(ValueError, match="test_function: Invalid template name"):
            validate_plot_parameters(self.test_series, "invalid_template", "A4_PORTRAIT", "test_function")

        # Invalid paper size
        with pytest.raises(ValueError, match="test_function: Invalid paper size"):
            validate_plot_parameters(self.test_series, "plotly_white", "invalid_size", "test_function")

if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])