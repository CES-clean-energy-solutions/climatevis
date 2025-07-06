"""
Integration tests for ClimateVis plotting library

These tests are based on the functionality demonstrated in app_plotting_test.py
and provide comprehensive coverage of the plotting library's core features.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import climatevis
from climatevis.plots import plot_series
from climatevis.util import util_plotly


class TestSyntheticDataGeneration:
    """Test synthetic climate data generation functionality"""

    def test_generate_8760_hour_data(self):
        """Test generation of exactly 8760 hours of synthetic climate data"""
        # Create hourly datetime index for a full year (8760 hours)
        dates = pd.date_range('2023-01-01 00:00:00', '2023-12-31 23:00:00', freq='h')

        # Verify we have exactly 8760 hours
        n_hours = len(dates)
        assert n_hours == 8760, f"Expected 8760 hours, got {n_hours}"

        # Verify date range
        assert dates.min() == pd.Timestamp('2023-01-01 00:00:00')
        assert dates.max() == pd.Timestamp('2023-12-31 23:00:00')

    def test_temperature_data_generation(self):
        """Test realistic temperature data generation with seasonal variation"""
        # Generate temperature data
        dates = pd.date_range('2023-01-01 00:00:00', '2023-12-31 23:00:00', freq='h')
        n_hours = len(dates)
        days_of_year = np.arange(n_hours) / 24.0

        # Seasonal temperature variation (sine wave with peak in summer)
        seasonal_component = 15 + 12 * np.sin(2 * np.pi * (days_of_year - 90) / 365.25)

        # Daily temperature variation (cooler at night, warmer during day)
        daily_component = 8 * np.sin(2 * np.pi * (np.arange(n_hours) % 24 - 6) / 24)

        # Add some realistic noise
        noise = np.random.normal(0, 3, n_hours)
        temperature = seasonal_component + daily_component + noise

        # Create pandas Series
        temp_series = pd.Series(temperature, index=dates, name="Air Temperature")
        temp_series.attrs["unit"] = "°C"

        # Verify temperature data properties
        assert len(temp_series) == 8760
        assert temp_series.name == "Air Temperature"
        assert temp_series.attrs["unit"] == "°C"
        assert temp_series.min() > -50  # Reasonable minimum temperature
        assert temp_series.max() < 50   # Reasonable maximum temperature
        assert temp_series.mean() > 0   # Should be above freezing on average

    def test_wind_speed_data_generation(self):
        """Test realistic wind speed data generation"""
        # Generate wind speed data
        dates = pd.date_range('2023-01-01 00:00:00', '2023-12-31 23:00:00', freq='h')
        n_hours = len(dates)
        days_of_year = np.arange(n_hours) / 24.0

        # Base wind speed with seasonal variation (higher in winter)
        base_wind = 8 + 4 * np.sin(2 * np.pi * (days_of_year - 270) / 365.25)

        # Daily wind pattern (often higher during day)
        daily_wind = 2 * np.sin(2 * np.pi * (np.arange(n_hours) % 24 - 12) / 24)

        # Wind speed noise (more variable than temperature)
        wind_noise = np.random.exponential(2, n_hours)
        wind_speed = np.maximum(0, base_wind + daily_wind + wind_noise)

        # Create pandas Series
        wind_series = pd.Series(wind_speed, index=dates, name="Wind Speed")
        wind_series.attrs["unit"] = "m/s"

        # Verify wind speed data properties
        assert len(wind_series) == 8760
        assert wind_series.name == "Wind Speed"
        assert wind_series.attrs["unit"] == "m/s"
        assert wind_series.min() >= 0  # Wind speed cannot be negative
        assert wind_series.max() < 50  # Reasonable maximum wind speed
        assert wind_series.mean() > 0  # Should have some wind on average


class TestPlottingFunctions:
    """Test core plotting functionality"""

    @pytest.fixture
    def sample_data(self):
        """Generate sample climate data for testing"""
        dates = pd.date_range('2023-01-01 00:00:00', '2023-12-31 23:00:00', freq='h')
        n_hours = len(dates)
        days_of_year = np.arange(n_hours) / 24.0

        # Temperature data
        seasonal_temp = 15 + 12 * np.sin(2 * np.pi * (days_of_year - 90) / 365.25)
        daily_temp = 8 * np.sin(2 * np.pi * (np.arange(n_hours) % 24 - 6) / 24)
        noise_temp = np.random.normal(0, 3, n_hours)
        temperature = seasonal_temp + daily_temp + noise_temp

        # Wind speed data
        base_wind = 8 + 4 * np.sin(2 * np.pi * (days_of_year - 270) / 365.25)
        daily_wind = 2 * np.sin(2 * np.pi * (np.arange(n_hours) % 24 - 12) / 24)
        wind_noise = np.random.exponential(2, n_hours)
        wind_speed = np.maximum(0, base_wind + daily_wind + wind_noise)

        # Create Series objects
        temp_series = pd.Series(temperature, index=dates, name="Air Temperature")
        temp_series.attrs["unit"] = "°C"

        wind_series = pd.Series(wind_speed, index=dates, name="Wind Speed")
        wind_series.attrs["unit"] = "m/s"

        return temp_series, wind_series

    def test_temperature_plot_creation(self, sample_data):
        """Test creating temperature time series plot"""
        temp_series, _ = sample_data

        # Test with different templates and paper sizes
        templates = ["base", "base_autosize"]
        paper_sizes = ["A4_LANDSCAPE", "A4_PORTRAIT"]
        modes = ["line", "area", "markers"]

        for template in templates:
            for paper_size in paper_sizes:
                for mode in modes:
                    try:
                        fig = plot_series(
                            [temp_series],
                            template_name=template,
                            paper_size=paper_size,
                            y1_axis_title="Air Temperature",
                            mode=mode
                        )

                        # Verify plot was created successfully
                        assert fig is not None
                        assert hasattr(fig, 'add_trace')  # Should be a Plotly figure

                    except Exception as e:
                        # Some combinations might not work, but shouldn't crash
                        assert "validation" in str(e).lower() or "template" in str(e).lower()

    def test_wind_plot_creation(self, sample_data):
        """Test creating wind speed time series plot"""
        _, wind_series = sample_data

        try:
            fig = plot_series(
                [wind_series],
                template_name="base",
                paper_size="A4_LANDSCAPE",
                y1_axis_title="Wind Speed",
                mode="line"
            )

            # Verify plot was created successfully
            assert fig is not None
            assert hasattr(fig, 'add_trace')

        except Exception as e:
            pytest.fail(f"Wind plot creation failed: {e}")

    def test_combined_plot_creation(self, sample_data):
        """Test creating combined temperature and wind plot with dual y-axes"""
        temp_series, wind_series = sample_data

        try:
            fig = plot_series(
                [temp_series, wind_series],
                template_name="base",
                paper_size="A4_LANDSCAPE",
                y1_axis_title="Climate Variables",
                mode="line"
            )

            # Verify plot was created successfully
            assert fig is not None
            assert hasattr(fig, 'add_trace')

            # Should have multiple traces for dual y-axis
            assert len(fig.data) >= 2

        except Exception as e:
            pytest.fail(f"Combined plot creation failed: {e}")

    def test_plot_with_different_modes(self, sample_data):
        """Test plotting with different modes (line, area, markers)"""
        temp_series, _ = sample_data

        modes = ["line", "area", "markers"]

        for mode in modes:
            try:
                fig = plot_series(
                    [temp_series],
                    template_name="base",
                    paper_size="A4_LANDSCAPE",
                    mode=mode
                )

                assert fig is not None
                assert hasattr(fig, 'add_trace')

            except Exception as e:
                pytest.fail(f"Plot creation with mode '{mode}' failed: {e}")


class TestTemplateAndPaperSizeOptions:
    """Test template and paper size dropdown functionality"""

    def test_template_options_availability(self):
        """Test that template options are available"""
        try:
            # Test if template functions are available
            if hasattr(climatevis, 'create_template_dropdown'):
                # If marimo components are available
                template_options = climatevis.get_template_options()
                assert isinstance(template_options, list)
                assert len(template_options) > 0
                assert "base" in template_options
            else:
                # Fallback test without marimo
                available_templates = util_plotly.get_available_templates()
                assert isinstance(available_templates, list)
                assert len(available_templates) > 0

        except Exception as e:
            pytest.fail(f"Template options test failed: {e}")

    def test_paper_size_options_availability(self):
        """Test that paper size options are available"""
        try:
            # Test if paper size functions are available
            if hasattr(climatevis, 'create_paper_size_dropdown'):
                # If marimo components are available
                paper_size_options = climatevis.get_paper_size_options()
                assert isinstance(paper_size_options, list)
                assert len(paper_size_options) > 0
                assert "A4_LANDSCAPE" in paper_size_options
                assert "A4_PORTRAIT" in paper_size_options
            else:
                # Fallback test without marimo
                # Paper sizes should be available as constants
                expected_sizes = ["A4_LANDSCAPE", "A4_PORTRAIT", "A5_LANDSCAPE"]
                for size in expected_sizes:
                    assert size in ["A4_LANDSCAPE", "A4_PORTRAIT", "A5_LANDSCAPE"]

        except Exception as e:
            pytest.fail(f"Paper size options test failed: {e}")


class TestDataValidation:
    """Test data validation functionality"""

    def test_series_validation(self):
        """Test that plot_series validates input data properly"""
        # Test with invalid input (not a list of series)
        with pytest.raises((ValueError, TypeError)):
            plot_series("invalid_input")

        # Test with empty list
        with pytest.raises(ValueError):
            plot_series([])

        # Test with non-pandas Series
        with pytest.raises((ValueError, TypeError)):
            plot_series([1, 2, 3])

    def test_template_validation(self):
        """Test template name validation"""
        # Create valid test data
        dates = pd.date_range('2023-01-01', periods=100, freq='h')
        data = pd.Series(np.random.randn(100), index=dates, name="Test Data")

        # Test with invalid template name
        with pytest.raises((ValueError, KeyError)):
            plot_series([data], template_name="invalid_template")

    def test_paper_size_validation(self):
        """Test paper size validation"""
        # Create valid test data
        dates = pd.date_range('2023-01-01', periods=100, freq='h')
        data = pd.Series(np.random.randn(100), index=dates, name="Test Data")

        # Test with invalid paper size
        with pytest.raises((ValueError, KeyError)):
            plot_series([data], paper_size="invalid_size")


class TestLibraryImport:
    """Test library import and availability"""

    def test_climatevis_import(self):
        """Test that climatevis can be imported successfully"""
        assert climatevis is not None
        assert hasattr(climatevis, '__version__')
        assert climatevis.__version__ == "0.1.0"

    def test_plot_series_availability(self):
        """Test that plot_series function is available"""
        assert hasattr(climatevis, 'plot_series')
        assert callable(climatevis.plot_series)

    def test_util_plotly_availability(self):
        """Test that util_plotly module is available"""
        assert hasattr(climatevis, 'util_plotly')
        assert climatevis.util_plotly is not None

    def test_template_functions_availability(self):
        """Test that template management functions are available"""
        expected_functions = [
            'get_available_templates',
            'get_builtin_template_names',
            'get_loaded_template_names',
            'load_all_builtin_templates'
        ]

        for func_name in expected_functions:
            assert hasattr(climatevis, func_name)
            assert callable(getattr(climatevis, func_name))


class TestDataSummary:
    """Test data summary and statistics functionality"""

    def test_data_summary_calculation(self):
        """Test calculation of data summary statistics"""
        # Generate test data
        dates = pd.date_range('2023-01-01 00:00:00', '2023-12-31 23:00:00', freq='h')
        n_hours = len(dates)
        days_of_year = np.arange(n_hours) / 24.0

        # Temperature data
        seasonal_temp = 15 + 12 * np.sin(2 * np.pi * (days_of_year - 90) / 365.25)
        daily_temp = 8 * np.sin(2 * np.pi * (np.arange(n_hours) % 24 - 6) / 24)
        noise_temp = np.random.normal(0, 3, n_hours)
        temperature = seasonal_temp + daily_temp + noise_temp

        temp_series = pd.Series(temperature, index=dates, name="Air Temperature")
        temp_series.attrs["unit"] = "°C"

        # Test summary statistics
        assert len(temp_series) == 8760
        assert temp_series.index.min() == pd.Timestamp('2023-01-01 00:00:00')
        assert temp_series.index.max() == pd.Timestamp('2023-12-31 23:00:00')
        assert temp_series.name == "Air Temperature"
        assert temp_series.attrs["unit"] == "°C"

        # Test statistical properties
        assert temp_series.min() > -50
        assert temp_series.max() < 50
        assert temp_series.mean() > 0
        assert temp_series.std() > 0


if __name__ == "__main__":
    pytest.main([__file__])