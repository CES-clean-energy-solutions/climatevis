"""
Test module to verify all plot functions can be imported and called with sample data.

This is a comprehensive validation for task 4.6 to ensure all 14+ plot functions
are available and functional with basic data.
"""

import pytest
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta


@pytest.fixture(scope="session", autouse=True)
def setup_templates():
    """Load the plotly template before running tests."""
    from climatevis.util import util_plotly

    # Load the base templates
    util_plotly.load_plotly_template('base', 'base')
    util_plotly.load_plotly_template('base_autosize', 'base-auto')
    yield
    # No cleanup needed


@pytest.fixture
def sample_data():
    """Create comprehensive sample data for testing all plot functions."""
    # Create 1 year of hourly data
    np.random.seed(42)
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(hours=i) for i in range(8760)]

    # Generate realistic weather data
    temperature = 15 + 10 * np.sin(np.arange(8760) * 2 * np.pi / (24 * 365)) + np.random.normal(0, 3, 8760)
    wind_speed = np.abs(np.random.normal(5, 3, 8760))
    wind_direction = np.random.uniform(0, 360, 8760)
    humidity = np.random.uniform(30, 90, 8760)
    pressure = np.random.normal(1013, 20, 8760)

    # Create sectors for wind rose (simplified to N, E, S, W pattern)
    sectors = np.random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'], 8760)

    return {
        'datetime': dates,
        'temperature': temperature,
        'wind_speed': wind_speed,
        'wind_direction': wind_direction,
        'humidity': humidity,
        'pressure': pressure,
        'sectors': sectors
    }


class TestAllPlotFunctions:
    """Test that all plot functions can be imported and called."""

    def test_wind_rose_function(self, sample_data):
        """Test wind_rose function import and basic call."""
        from climatevis import wind_rose

        # Convert arrays to pandas Series with DatetimeIndex
        wind_speed_series = pd.Series(
            sample_data['wind_speed'][:1000],
            index=pd.DatetimeIndex(sample_data['datetime'][:1000])
        )
        sector_series = pd.Series(
            sample_data['sectors'][:1000],
            index=pd.DatetimeIndex(sample_data['datetime'][:1000])
        )

        fig = wind_rose(wind_speed_series, sector_series, 'base', 'A4_LANDSCAPE')
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0

    def test_exceedance_function(self, sample_data):
        """Test exceedance function import and basic call."""
        from climatevis import exceedance

        # Convert to pandas Series with DatetimeIndex
        temp_series = pd.Series(
            sample_data['temperature'],
            index=pd.DatetimeIndex(sample_data['datetime'])
        )

        fig = exceedance(temp_series, 'base', 'A4_LANDSCAPE')
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0

        # Test with parameters
        fig_params = exceedance(
            temp_series,
            'base',
            'A4_LANDSCAPE',
            x_title="Probability (%)",
            y_title="Temperature (°C)"
        )
        assert isinstance(fig_params, go.Figure)

    def test_exceedance_bands_function(self, sample_data):
        """Test exceedance_bands function import and basic call."""
        from climatevis import exceedance_bands

        # Create multiple series with DatetimeIndex - ensure they all have overlapping time ranges
        base_start = sample_data['datetime'][0]
        series_list = [
            pd.Series(
                sample_data['temperature'][:3000],
                index=pd.DatetimeIndex(sample_data['datetime'][:3000])
            ),
            pd.Series(
                sample_data['temperature'][1000:4000],
                index=pd.DatetimeIndex(sample_data['datetime'][1000:4000])
            ),
            pd.Series(
                sample_data['temperature'][2000:5000],
                index=pd.DatetimeIndex(sample_data['datetime'][2000:5000])
            )
        ]

        fig = exceedance_bands(series_list, 'base', 'A4_LANDSCAPE')
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0

    def test_annual_heatmap_function(self, sample_data):
        """Test annual_heatmap function import and basic call."""
        from climatevis import annual_heatmap

        # Create pandas Series with DatetimeIndex
        temp_series = pd.Series(
            sample_data['temperature'],
            index=pd.DatetimeIndex(sample_data['datetime'])
        )

        fig = annual_heatmap(temp_series, 'base', 'A4_LANDSCAPE')
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0

    def test_annual_profile_daily_function(self, sample_data):
        """Test annual_profile_daily function import and basic call."""
        from climatevis import annual_profile_daily

        # Create pandas Series with DatetimeIndex
        temp_series = pd.Series(
            sample_data['temperature'],
            index=pd.DatetimeIndex(sample_data['datetime'])
        )

        fig = annual_profile_daily(temp_series, 'base', 'A4_LANDSCAPE')
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0

    def test_annual_profile_multiple_function(self, sample_data):
        """Test annual_profile_multiple function import and basic call."""
        from climatevis import annual_profile_multiple

        # Create multiple pandas Series with DatetimeIndex
        series_list = [
            pd.Series(
                sample_data['temperature'][:4000],
                index=pd.DatetimeIndex(sample_data['datetime'][:4000])
            ),
            pd.Series(
                sample_data['temperature'][2000:6000] + 1,
                index=pd.DatetimeIndex(sample_data['datetime'][2000:6000])
            ),
            pd.Series(
                sample_data['temperature'][4000:8000] - 0.5,
                index=pd.DatetimeIndex(sample_data['datetime'][4000:8000])
            )
        ]

        fig = annual_profile_multiple(series_list, 'base', 'A4_LANDSCAPE')
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0

    def test_plot_series_function(self, sample_data):
        """Test plot_series function import and basic call."""
        from climatevis import plot_series

        # Create pandas Series with datetime index
        df = pd.DataFrame({
            'temperature': sample_data['temperature'][:100]
        }, index=pd.DatetimeIndex(sample_data['datetime'][:100]))

        series_list = [df['temperature']]

        fig = plot_series(series_list, 'base', 'A4_LANDSCAPE')
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0

        # Test with title
        fig_titled = plot_series(
            series_list,
            'base',
            'A4_LANDSCAPE',
            y1_axis_title="Temperature (°C)"
        )
        assert isinstance(fig_titled, go.Figure)

    def test_plot_timeseries_df_function(self, sample_data):
        """Test plot_timeseries_df function import and basic call."""
        from climatevis import plot_timeseries_df

        # Create DataFrame with datetime index - only numeric columns
        df = pd.DataFrame({
            'temperature': sample_data['temperature'],
            'wind_speed': sample_data['wind_speed'],
            'humidity': sample_data['humidity'],
            'pressure': sample_data['pressure']
        }, index=pd.DatetimeIndex(sample_data['datetime']))

        # This function uses the default 'base-auto' template which we've loaded
        fig = plot_timeseries_df(df)
        assert isinstance(fig, go.Figure)

    def test_plot_rotated_box_function(self):
        """Test plot_rotated_box function import and basic call."""
        from climatevis import plot_rotated_box
        import matplotlib.pyplot as plt

        # This function takes rotation_deg as parameter and returns matplotlib figure
        rotation_deg = 45

        fig = plot_rotated_box(rotation_deg)
        # It returns a matplotlib figure, not plotly
        assert hasattr(fig, 'savefig')  # matplotlib figure attribute

    def test_histogram_function(self, sample_data):
        """Test histogram function import and basic call."""
        from climatevis import histogram

        temp_series = pd.Series(
            sample_data['temperature'],
            index=pd.DatetimeIndex(sample_data['datetime'])
        )
        fig = histogram(temp_series, 'base', 'A4_LANDSCAPE')
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0

        # Don't test bins parameter as it may not be supported in this signature

    def test_cumulative_probability_function(self, sample_data):
        """Test cumulative_probability function import and basic call."""
        from climatevis import cumulative_probability

        temp_series = pd.Series(
            sample_data['temperature'],
            index=pd.DatetimeIndex(sample_data['datetime'])
        )
        fig = cumulative_probability(temp_series, 'base', 'A4_LANDSCAPE')
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0

    def test_monthly_profiles_function(self, sample_data):
        """Test monthly_profiles function import and basic call."""
        from climatevis import monthly_profiles

        # Create pandas Series with DatetimeIndex
        temp_series = pd.Series(
            sample_data['temperature'],
            index=pd.DatetimeIndex(sample_data['datetime'])
        )

        fig = monthly_profiles(temp_series, 'base', 'A4_LANDSCAPE')
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0

    def test_monthly_profiles_bands_function(self, sample_data):
        """Test monthly_profiles_bands function import and basic call."""
        from climatevis import monthly_profiles_bands

        # Create multiple pandas Series with DatetimeIndex
        series_list = [
            pd.Series(
                sample_data['temperature'][:2920],
                index=pd.DatetimeIndex(sample_data['datetime'][:2920])
            ),
            pd.Series(
                sample_data['temperature'][1000:3920] + 1,
                index=pd.DatetimeIndex(sample_data['datetime'][1000:3920])
            ),
            pd.Series(
                sample_data['temperature'][2000:4920] - 0.5,
                index=pd.DatetimeIndex(sample_data['datetime'][2000:4920])
            )
        ]

        fig = monthly_profiles_bands(series_list, 'base', 'A4_LANDSCAPE')
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0


class TestUtilityFunction:
    """Test utility function availability."""

    def test_util_plotly_availability(self):
        """Test that util_plotly is available and has expected functions."""
        from climatevis import util_plotly

        assert util_plotly is not None
        assert hasattr(util_plotly, 'load_plotly_template')
        assert callable(util_plotly.load_plotly_template)

        # Test template loading with correct signature
        template = util_plotly.load_plotly_template('base', 'test_template')
        assert isinstance(template, dict)
        assert 'layout' in template


class TestComponentsAvailability:
    """Test component availability."""

    def test_weather_selection_availability(self):
        """Test that weather_selection component is available."""
        import climatevis

        # Check if weather_selection is available (depends on marimo)
        if hasattr(climatevis, 'weather_selection'):
            from climatevis import weather_selection
            assert weather_selection is not None
            assert callable(weather_selection)
        else:
            # If not available, that's also acceptable (marimo not installed)
            assert True


class TestFunctionCount:
    """Test that we have all expected functions available."""

    def test_all_functions_count(self):
        """Test that all expected functions are available in the package."""
        import climatevis

        # Count plotting functions (excluding util_plotly and weather_selection)
        plotting_functions = [f for f in climatevis.__all__
                            if f not in ['util_plotly', 'weather_selection']]

        # We expect at least 13 core plotting functions
        expected_min_functions = 13
        assert len(plotting_functions) >= expected_min_functions, \
            f"Expected at least {expected_min_functions} plotting functions, got {len(plotting_functions)}: {plotting_functions}"

        # Verify specific key functions are present
        key_functions = [
            'wind_rose', 'exceedance', 'annual_heatmap', 'plot_series',
            'histogram', 'cumulative_probability', 'monthly_profiles'
        ]

        for func in key_functions:
            assert func in climatevis.__all__, f"Key function {func} not found in __all__"

    def test_all_functions_callable(self):
        """Test that all exported functions are callable."""
        import climatevis

        for func_name in climatevis.__all__:
            if func_name != 'weather_selection':  # Skip optional marimo function
                func = getattr(climatevis, func_name)
                if func_name != 'util_plotly':  # util_plotly is a module, not a function
                    assert callable(func), f"Function {func_name} is not callable"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])