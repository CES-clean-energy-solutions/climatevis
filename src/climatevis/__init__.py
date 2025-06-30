"""
ClimateVis - Professional Weather Data Visualization Library

A comprehensive Python package for creating professional weather and climate
data visualizations using Plotly.
"""

__version__ = "0.1.0"
__author__ = "ClimateVis Team"

# Import key functions at package level for easy access
from .plots import (
    wind_rose,
    exceedance,
    exceedance_bands,
    annual_heatmap,
    annual_profile_daily,
    annual_profile_multiple,
    plot_series,
    plot_timeseries_df,
    plot_rotated_box,
    histogram,
    cumulative_probability,
    monthly_profiles,
    monthly_profiles_bands
)

# Import utility functions
from .util import util_plotly

# Import components (with optional marimo dependency)
try:
    from .components import weather_selection
    _HAS_MARIMO = True
except ImportError:
    _HAS_MARIMO = False

__all__ = [
    'wind_rose',
    'exceedance',
    'exceedance_bands',
    'annual_heatmap',
    'annual_profile_daily',
    'annual_profile_multiple',
    'plot_series',
    'plot_timeseries_df',
    'plot_rotated_box',
    'histogram',
    'cumulative_probability',
    'monthly_profiles',
    'monthly_profiles_bands',
    'util_plotly'
]

if _HAS_MARIMO:
    __all__.append('weather_selection')