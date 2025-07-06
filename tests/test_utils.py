"""
Test utilities for ClimateVis

Common helper functions and fixtures for testing the climatevis library.
"""

import pandas as pd
import numpy as np
import pytest
from datetime import datetime, timedelta


def generate_synthetic_climate_data(hours=8760, start_date='2023-01-01'):
    """
    Generate synthetic climate data for testing

    Args:
        hours (int): Number of hours to generate (default: 8760 for full year)
        start_date (str): Start date for the data

    Returns:
        tuple: (temp_series, wind_series) with pandas Series objects
    """
    # Create hourly datetime index
    dates = pd.date_range(start_date, periods=hours, freq='h')
    n_hours = len(dates)
    days_of_year = np.arange(n_hours) / 24.0

    # Generate realistic temperature data with seasonal variation
    seasonal_component = 15 + 12 * np.sin(2 * np.pi * (days_of_year - 90) / 365.25)
    daily_component = 8 * np.sin(2 * np.pi * (np.arange(n_hours) % 24 - 6) / 24)
    noise = np.random.normal(0, 3, n_hours)
    temperature = seasonal_component + daily_component + noise

    # Generate realistic wind speed data
    base_wind = 8 + 4 * np.sin(2 * np.pi * (days_of_year - 270) / 365.25)
    daily_wind = 2 * np.sin(2 * np.pi * (np.arange(n_hours) % 24 - 12) / 24)
    wind_noise = np.random.exponential(2, n_hours)
    wind_speed = np.maximum(0, base_wind + daily_wind + wind_noise)

    # Create pandas Series with proper names and units
    temp_series = pd.Series(temperature, index=dates, name="Air Temperature")
    temp_series.attrs["unit"] = "°C"

    wind_series = pd.Series(wind_speed, index=dates, name="Wind Speed")
    wind_series.attrs["unit"] = "m/s"

    return temp_series, wind_series


def generate_small_test_dataset(hours=100):
    """
    Generate a smaller dataset for faster testing

    Args:
        hours (int): Number of hours to generate

    Returns:
        tuple: (temp_series, wind_series) with pandas Series objects
    """
    return generate_synthetic_climate_data(hours=hours)


@pytest.fixture
def sample_climate_data():
    """Fixture providing sample climate data for tests"""
    return generate_synthetic_climate_data(hours=100)


@pytest.fixture
def full_year_climate_data():
    """Fixture providing full year (8760 hours) of climate data"""
    return generate_synthetic_climate_data(hours=8760)


@pytest.fixture
def invalid_data():
    """Fixture providing invalid data for testing error handling"""
    return {
        'empty_list': [],
        'non_series': [1, 2, 3, 4, 5],
        'string': "invalid_input",
        'none': None,
        'empty_series': pd.Series([], name="Empty"),
        'series_without_index': pd.Series([1, 2, 3], name="No Index")
    }


def assert_plotly_figure(fig):
    """
    Assert that an object is a valid Plotly figure

    Args:
        fig: Object to check
    """
    assert fig is not None
    assert hasattr(fig, 'add_trace')
    assert hasattr(fig, 'data')
    assert hasattr(fig, 'layout')


def assert_series_properties(series, expected_name=None, expected_unit=None, min_length=1):
    """
    Assert that a pandas Series has the expected properties

    Args:
        series: pandas Series to check
        expected_name (str): Expected name of the series
        expected_unit (str): Expected unit attribute
        min_length (int): Minimum expected length
    """
    assert isinstance(series, pd.Series)
    assert len(series) >= min_length
    assert series.index is not None

    if expected_name:
        assert series.name == expected_name

    if expected_unit and hasattr(series, 'attrs'):
        assert series.attrs.get("unit") == expected_unit


def assert_datetime_index(series, freq='h'):
    """
    Assert that a series has a proper datetime index

    Args:
        series: pandas Series to check
        freq (str): Expected frequency of the index
    """
    assert isinstance(series.index, pd.DatetimeIndex)
    assert series.index.freq == pd.Timedelta(freq)
    assert not series.index.isnull().any()


def create_test_template_config():
    """
    Create a test template configuration for testing

    Returns:
        dict: Template configuration dictionary
    """
    return {
        "name": "test_template",
        "layout": {
            "template": "plotly_white",
            "width": 800,
            "height": 600,
            "title": {"text": "Test Plot"}
        },
        "traces": {
            "default": {
                "mode": "lines",
                "line": {"width": 2}
            }
        }
    }